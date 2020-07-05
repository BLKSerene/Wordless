#
# Wordless: Text - Word Tokenization
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import jieba
import nltk
import nltk.tokenize.nist
import pythainlp
import razdel
import sacremoses
import syntok.segmenter
import underthesea

from wl_checking import wl_checking_unicode
from wl_text import wl_sentence_tokenization, wl_text, wl_text_utils
from wl_utils import wl_conversion, wl_misc

def wl_word_tokenize(main, text, lang, word_tokenizer = 'default', flat_tokens = True):
    tokens_multilevel = []

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    # Check initialization status of word (and sentence) tokenizers
    if flat_tokens:
        wl_text_utils.check_word_tokenizers(main,
                                                  lang = lang,
                                                  word_tokenizer = word_tokenizer)
    else:
        wl_text_utils.check_tokenizers(main,
                                             lang = lang,
                                             word_tokenizer = word_tokenizer)

    # NLTK
    if 'NLTK' in word_tokenizer:
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang)

        if word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
            nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()

            for sentence in sentences:
                tokens_multilevel.append(nist_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - NLTK Tokenizer'):
            nltk_tokenizer = nltk.NLTKWordTokenizer()

            for sentence in sentences:
                tokens_multilevel.append(nltk_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
            treebank_tokenizer = nltk.TreebankWordTokenizer()

            for sentence in sentences:
                tokens_multilevel.append(treebank_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
            toktok_tokenizer = nltk.ToktokTokenizer()

            for sentence in sentences:
                tokens_multilevel.append(toktok_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
            tweet_tokenizer = nltk.TweetTokenizer()

            for sentence in sentences:
                tokens_multilevel.append(tweet_tokenizer.tokenize(sentence))
    # Sacremoses
    elif 'Sacremoses' in word_tokenizer:
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang)

        moses_tokenizer = sacremoses.MosesTokenizer(lang = wl_conversion.to_iso_639_1(main, lang))

        for sentence in sentences:
            tokens_multilevel.append(moses_tokenizer.tokenize(sentence, escape = False))

    # spaCy
    elif 'spaCy' in word_tokenizer:
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)
        # See Issue #3479: https://github.com/explosion/spaCy/issues/3479
        doc.is_parsed = True

        if flat_tokens:
            tokens_multilevel.append([token.text for token in doc])
        else:
            for sentence in doc.sents:
                tokens_multilevel.append([token.text for token in sentence.as_doc()])
    # syntok
    elif word_tokenizer == 'syntok - Word Tokenizer':
        syntok_tokenizer = syntok.tokenizer.Tokenizer()

        if flat_tokens:
            tokens_multilevel.append([token.value for token in syntok_tokenizer.tokenize(text)])
        else:
            for para in syntok.segmenter.analyze(text):
                for sentence in para:
                    tokens_multilevel.append([token.value for token in sentence])
    # Chinese & Japanese
    elif ('jieba' in word_tokenizer or
          'nagisa' in word_tokenizer or
          'Wordless' in word_tokenizer):
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = lang)

        # Chinese
        if word_tokenizer == main.tr('jieba - Chinese Word Tokenizer'):
            for sentence in sentences:
                tokens_multilevel.append(jieba.cut(sentence))
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
                                        tokens.extend(wl_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'eng'))

                                        non_han_start = i + j + 1

                                        break
                            # Other Languages
                            else:
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or wl_checking_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'other'))

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
                                        tokens.extend(wl_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'jpn'))

                                        non_han_start = i + j + 1

                                        break
                            # English
                            elif wl_checking_unicode.is_eng(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wl_checking_unicode.is_eng(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'eng'))

                                        non_han_start = i + j + 1

                                        break
                            # Other Languages
                            else:
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or wl_checking_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wl_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'other'))

                                        non_han_start = i + j + 1

                                        break

                tokens_multilevel.append(tokens)
    # Russian
    elif word_tokenizer == 'razdel - Russian Word Tokenizer':
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = 'rus')

        for sentence in sentences:
            tokens_multilevel.append([token.text for token in razdel.tokenize(sentence)])
    # Thai
    elif 'PyThaiNLP' in word_tokenizer:
        # Preserve sentence boundaries
        sentences = wl_sentence_tokenization.wl_sentence_tokenize(
            main, text,
            lang = 'tha')

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
    # Tibetan
    elif 'botok' in word_tokenizer:
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, text, lang = 'bod')

        for sentence in sentences:
            tokens_multilevel.append([token.text
                                      for token in main.botok_word_tokenizer.tokenize(sentence)])
    # Vietnamese
    elif word_tokenizer == main.tr('Underthesea - Vietnamese Word Tokenizer'):
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wl_sentence_tokenization.wl_sentence_tokenize(
                main, text,
                lang = 'vie',
                sentence_tokenizer = 'Underthesea - Vietnamese Sentence Tokenizer')

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

    # Clause tokenization
    if not flat_tokens:
        for i, sentence in enumerate(tokens_multilevel):
            tokens_multilevel[i] = wl_sentence_tokenization.wl_clause_tokenize(main, sentence, lang)

    # Flatten tokens
    tokens_flat = list(wl_misc.flatten_list(tokens_multilevel))

    if flat_tokens:
        return tokens_flat
    else:
        return tokens_multilevel
