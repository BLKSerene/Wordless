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

import re

import jieba
import pythainlp
import razdel
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

    wl_text_utils.init_word_tokenizers(
        main,
        lang = lang,
        word_tokenizer = word_tokenizer
    )
    
    # spaCy
    if 'spacy' in word_tokenizer:
        # Chinese, English, German, Portuguese
        if lang.find('srp') == -1:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)

        tokens_multilevel.append([])

        len_sents = len(list(doc.sents))
        
        for i, sentence in enumerate(doc.sents):
            tokens_sentence = []
            
            tokens = [token.text for token in sentence]
            len_tokens = len(tokens)
            
            for j, token in enumerate(tokens):
                # Split paragraphs by new line character
                len_lines = len(re.findall(r'\n', token))

                if len_lines:
                    # Check if the last paragraph is empty
                    if i == len_sents - 1 and j == len_tokens - 1 and token.endswith('\n'):
                        len_lines -= 1

                    if tokens_sentence:
                        tokens_multilevel[-1].append(tokens_sentence)

                        tokens_sentence = []

                    tokens_multilevel.extend([[] for j in range(len_lines)])
                else:
                    if token.strip():
                        tokens_sentence.append(token)

            if tokens_sentence:
                tokens_multilevel[-1].append(tokens_sentence)
    else:
        # Split text into paragraphs
        text = re.split(r'\n(?=.|\n)', text)

        for para in text:
            tokens_multilevel.append([])

            if para.strip():
                # NLTK
                if 'nltk' in word_tokenizer:
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang)

                    if word_tokenizer == 'nltk_nist':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(main.nltk_nist_tokenizer.tokenize(sentence))
                    elif word_tokenizer == 'nltk_nltk':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(main.nltk_nltk_tokenizer.tokenize(sentence))
                    elif word_tokenizer == 'nltk_penn_treebank':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(main.nltk_treebank_tokenizer.tokenize(sentence))
                    elif word_tokenizer == 'nltk_tok_tok':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(main.nltk_toktok_tokenizer.tokenize(sentence))
                    elif word_tokenizer == 'nltk_twitter':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(main.nltk_tweet_tokenizer.tokenize(sentence))
                # Sacremoses
                elif word_tokenizer == 'sacremoses_moses':
                    lang = wl_conversion.remove_lang_code_suffixes(main, lang)
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang)
                    
                    for sentence in sentences:
                        tokens_multilevel[-1].append(main.__dict__[f'sacremoses_moses_tokenizer_{lang}'].tokenize(sentence, escape = False))
                # Chinese
                elif word_tokenizer == 'jieba_zho':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(jieba.lcut(sentence))
                elif word_tokenizer == 'pkuseg_zho':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(main.pkuseg_word_tokenizer.cut(sentence))
                elif word_tokenizer == 'wordless_zho_char':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = lang)

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
                                                    lang = 'eng_us'
                                                ))
                                                tokens = list(wl_misc.flatten_list(tokens))

                                                non_han_start = i + j + 1

                                                break
                                    # Other Languages
                                    else:
                                        for j, char in enumerate(sentence[i:]):
                                            if i + j + 1 == len(sentence) or wl_checking_unicode.is_han(sentence[i + j + 1]):
                                                tokens.extend(wl_word_tokenize(
                                                    main, sentence[non_han_start : i + j + 1],
                                                    lang = 'other'
                                                ))
                                                tokens = list(wl_misc.flatten_list(tokens))

                                                non_han_start = i + j + 1

                                                break

                        tokens_multilevel[-1].append(tokens)
                # Japanese
                elif word_tokenizer == 'nagisa_jpn':
                    import nagisa

                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(nagisa.tagging(str(sentence)).words)
                elif word_tokenizer == 'wordless_jpn_kanji':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = lang)

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
                                                     lang = 'jpn'
                                                ))
                                                tokens = list(wl_misc.flatten_list(tokens))

                                                non_han_start = i + j + 1

                                                break
                                    # English
                                    elif wl_checking_unicode.is_eng(char):
                                        for j, char in enumerate(sentence[i:]):
                                            if i + j + 1 == len(sentence) or not wl_checking_unicode.is_eng(sentence[i + j + 1]):
                                                tokens.extend(wl_word_tokenize(
                                                    main, sentence[non_han_start : i + j + 1],
                                                    lang = 'eng_us'
                                                ))
                                                tokens = list(wl_misc.flatten_list(tokens))

                                                non_han_start = i + j + 1

                                                break
                                    # Other Languages
                                    else:
                                        for j, char in enumerate(sentence[i:]):
                                            if i + j + 1 == len(sentence) or wl_checking_unicode.is_han(sentence[i + j + 1]):
                                                tokens.extend(wl_word_tokenize(
                                                    main, sentence[non_han_start : i + j + 1],
                                                    lang = 'other'
                                                ))
                                                tokens = list(wl_misc.flatten_list(tokens))

                                                non_han_start = i + j + 1

                                                break

                        tokens_multilevel[-1].append(tokens)
                # Icelandic
                elif word_tokenizer == 'tokenizer_isl':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
                        main, para,
                        lang = 'isl',
                        sentence_tokenizer = 'tokenizer_isl'
                    )

                    for sentence in sentences:
                        tokens_multilevel[-1].append([
                            token
                            for kind, token, val in tokenizer.tokenize(sentence)
                            if token
                        ])
                # Russian
                elif word_tokenizer == 'razdel_rus':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = 'rus')

                    for sentence in sentences:
                        tokens_multilevel[-1].append([token.text for token in razdel.tokenize(sentence)])
                # Thai
                elif 'pythainlp' in word_tokenizer:
                    # Preserve sentence boundaries
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = 'tha')

                    if word_tokenizer == 'pythainlp_longest_matching':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'longest'))
                    elif word_tokenizer == 'pythainlp_max_matching':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'mm'))
                    elif word_tokenizer == 'pythainlp_max_matching_tcc':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'newmm'))
                    elif word_tokenizer == 'pythainlp_max_matching_tcc_safe_mode':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'newmm-safe'))
                    elif word_tokenizer == 'pythainlp_nercut':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'nercut'))
                # Tibetan
                elif word_tokenizer == 'botok_bod':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, para, lang = 'bod')

                    for sentence in sentences:
                        tokens_multilevel[-1].append([token.text
                                                      for token in main.botok_word_tokenizer.tokenize(sentence)])
                # Vietnamese
                elif word_tokenizer == 'underthesea_vie':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
                        main, para,
                        lang = 'vie',
                        sentence_tokenizer = 'underthesea_vie'
                    )

                    for sentence in sentences:
                        tokens_multilevel[-1].append(underthesea.word_tokenize(str(sentence)))
    
    # Remove empty tokens and strip whitespace
    for para in tokens_multilevel:
        for i, sentence in enumerate(para):
            para[i] = [token.strip()
                       for token in sentence
                       if token.strip()]
    
    # Record token boundaries
    if lang in ['zho_cn', 'zho_tw', 'jpn']:
        for para in tokens_multilevel:
            for sentence in para:
                if sentence:
                    sentence[-1] = wl_text.Wl_Token(sentence[-1], boundary = '', sentence_ending = True)
    else:
        for para in tokens_multilevel:
            for sentence in para:
                if sentence:
                    sentence[-1] = wl_text.Wl_Token(sentence[-1], boundary = ' ', sentence_ending = True)
    
    return tokens_multilevel
