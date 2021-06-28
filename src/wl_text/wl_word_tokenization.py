#
# Wordless: Text - Word Tokenization
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import jieba
import pythainlp
import razdel
import syntok.segmenter
import tokenizer
import underthesea

from wl_checking import wl_checking_unicode
from wl_text import wl_sentence_tokenization, wl_text, wl_text_utils
from wl_utils import wl_conversion, wl_misc

def wl_word_tokenize(main, text, lang, word_tokenizer = 'default'):
    tokens_multilevel = []

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    wl_text_utils.init_tokenizers(
        main,
        lang = lang,
        word_tokenizer = word_tokenizer
    )
    
    # NLTK
    if 'NLTK' in word_tokenizer:
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang)

        if word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(main.nltk_nist_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - NLTK Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(main.nltk_nltk_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(main.nltk_treebank_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(main.nltk_toktok_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(main.nltk_tweet_tokenizer.tokenize(sentence))
    # Sacremoses
    elif 'Sacremoses' in word_tokenizer:
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang)

        for sentence in sentences:
            tokens_multilevel.append(main.sacremoses_moses_tokenizer.tokenize(sentence, escape = False))
    # spaCy
    elif 'spaCy' in word_tokenizer:
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)
        # See Issue #3479: https://github.com/explosion/spaCy/issues/3479
        doc.is_parsed = True

        for sentence in doc.sents:
            tokens_multilevel.append([token.text for token in sentence.as_doc()])
    # syntok
    elif word_tokenizer == 'syntok - Word Tokenizer':
        for para in syntok.segmenter.analyze(text):
            for sentence in para:
                tokens_multilevel.append([token.value for token in sentence])
    # Chinese & Japanese
    elif ('jieba' in word_tokenizer or
          'pkuseg' in word_tokenizer or
          'nagisa' in word_tokenizer or
          'Wordless' in word_tokenizer):
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = lang)

        # Chinese
        if word_tokenizer == main.tr('jieba - Chinese Word Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(jieba.lcut(sentence))
        elif word_tokenizer == main.tr('pkuseg - Chinese Word Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(main.pkuseg_word_tokenizer.cut(sentence))
        elif word_tokenizer == main.tr('Wordless - Chinese Character Tokenizer'):
            for sentence in sentences:
                tokens = []
                non_han_start = 0

                for i, char in enumerate(sentence):
                    if i >= non_han_start:
                        if wl_checking_unicode.is_han(char):
                            tokens.append(char)

                            non_han_start += 1
                        else:
                            # English
                            if wl_checking_unicode.is_eng(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wl_checking_unicode.is_eng(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(
                                                          main, sentence[non_han_start : i + j + 1],
                                                          lang = 'eng')
                                                      )
                                        tokens = list(wl_misc.flatten_list(tokens))

                                        non_han_start = i + j + 1

                                        break
                            # Other Languages
                            else:
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or wl_checking_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(
                                                          main, sentence[non_han_start : i + j + 1],
                                                          lang = 'other')
                                                      )
                                        tokens = list(wl_misc.flatten_list(tokens))

                                        non_han_start = i + j + 1

                                        break

                tokens_multilevel.append(tokens)
        # Japanese
        elif word_tokenizer == main.tr('nagisa - Japanese Word Tokenizer'):
            import nagisa

            for sentence in sentences:
                tokens_multilevel.append(nagisa.tagging(str(sentence)).words)
        elif word_tokenizer == main.tr('Wordless - Japanese Kanji Tokenizer'):
            for sentence in sentences:
                tokens = []
                non_han_start = 0

                for i, char in enumerate(sentence):
                    if i >= non_han_start:
                        if wl_checking_unicode.is_han(char):
                            tokens.append(char)

                            non_han_start += 1
                        else:
                            # Japanese Kana
                            if wl_checking_unicode.is_kana(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wl_checking_unicode.is_kana(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(
                                                          main, sentence[non_han_start : i + j + 1],
                                                          lang = 'jpn')
                                                     )
                                        tokens = list(wl_misc.flatten_list(tokens))

                                        non_han_start = i + j + 1

                                        break
                            # English
                            elif wl_checking_unicode.is_eng(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wl_checking_unicode.is_eng(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(
                                                          main, sentence[non_han_start : i + j + 1],
                                                          lang = 'eng')
                                                      )
                                        tokens = list(wl_misc.flatten_list(tokens))

                                        non_han_start = i + j + 1

                                        break
                            # Other Languages
                            else:
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or wl_checking_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(
                                                          main, sentence[non_han_start : i + j + 1],
                                                          lang = 'other')
                                                      )
                                        tokens = list(wl_misc.flatten_list(tokens))

                                        non_han_start = i + j + 1

                                        break

                tokens_multilevel.append(tokens)
    # Icelandic
    elif word_tokenizer == main.tr('Tokenizer - Icelandic Word Tokenizer'):
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(
            main, text,
            lang = 'isl',
            sentence_tokenizer = 'Tokenizer - Icelandic Sentence Tokenizer')

        for sentence in sentences:
            tokens_multilevel.append([token
                                      for kind, token, val in tokenizer.tokenize(sentence)
                                      if token])
    # Russian
    elif word_tokenizer == main.tr('razdel - Russian Word Tokenizer'):
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = 'rus')

        for sentence in sentences:
            tokens_multilevel.append([token.text for token in razdel.tokenize(sentence)])
    # Thai
    elif 'PyThaiNLP' in word_tokenizer:
        # Preserve sentence boundaries
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = 'tha')

        if word_tokenizer == main.tr('PyThaiNLP - Longest Matching'):
            for sentence in sentences:
                tokens_multilevel.append(pythainlp.word_tokenize(sentence, engine = 'longest'))
        elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching'):
            for sentence in sentences:
                tokens_multilevel.append(pythainlp.word_tokenize(sentence, engine = 'mm'))
        elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching + TCC'):
            for sentence in sentences:
                tokens_multilevel.append(pythainlp.word_tokenize(sentence, engine = 'newmm'))
        elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching + TCC (Safe Mode)'):
            for sentence in sentences:
                tokens_multilevel.append(pythainlp.word_tokenize(sentence, engine = 'newmm-safe'))
        elif word_tokenizer == main.tr('PyThaiNLP - NERCut'):
            for sentence in sentences:
                tokens_multilevel.append(pythainlp.word_tokenize(sentence, engine = 'nercut'))
    # Tibetan
    elif 'botok' in word_tokenizer:
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = 'bod')

        for sentence in sentences:
            tokens_multilevel.append([token.text
                                      for token in main.botok_word_tokenizer.tokenize(sentence)])
    # Vietnamese
    elif word_tokenizer == main.tr('Underthesea - Vietnamese Word Tokenizer'):
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(
            main, text,
            lang = 'vie',
            sentence_tokenizer = 'Underthesea - Vietnamese Sentence Tokenizer'
        )

        for sentence in sentences:
            tokens_multilevel.append(underthesea.word_tokenize(str(sentence)))
    
    # Remove empty tokens and strip whitespace
    for i, sentence in enumerate(tokens_multilevel):
        tokens_multilevel[i] = [token.strip()
                                for token in sentence
                                if token.strip()]
    
    # Record token boundaries
    if lang in ['zho_cn', 'zho_tw', 'jpn']:
        for sentence in tokens_multilevel:
            if sentence:
                sentence[-1] = wl_text.Wl_Token(sentence[-1], boundary = '', sentence_ending = True)
    else:
        for sentence in tokens_multilevel:
            if sentence:
                sentence[-1] = wl_text.Wl_Token(sentence[-1], boundary = ' ', sentence_ending = True)
    
    return tokens_multilevel
