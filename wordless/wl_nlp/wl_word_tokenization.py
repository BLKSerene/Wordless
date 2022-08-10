# ----------------------------------------------------------------------
# Wordless: NLP - Word Tokenization
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import re

import jieba
import pythainlp
import sudachipy
import tokenizer
import underthesea

from wordless.wl_checking import wl_checking_unicode
from wordless.wl_nlp import wl_nlp_utils, wl_sentence_tokenization, wl_texts
from wordless.wl_utils import wl_conversion, wl_misc

def wl_word_tokenize(main, text, lang, word_tokenizer = 'default'):
    tokens_multilevel = []

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    wl_nlp_utils.init_word_tokenizers(
        main,
        lang = lang,
        word_tokenizer = word_tokenizer
    )

    if word_tokenizer.startswith('spacy_'):
        # Input of SudachiPy cannot be more than 49149 BYTES
        if word_tokenizer == 'spacy_jpn' and len(text) > 49149 // 4:
            # Around 100 tokens per line 6 characters per token and 4 bytes per character (≈ 49149 / 4 / 6 / 100)
            sections = wl_nlp_utils.split_into_chunks_text(text, section_size = 20)
        else:
            sections = wl_nlp_utils.split_into_chunks_text(text, section_size = main.settings_custom['files']['misc_settings']['read_files_in_chunks'])
    else:
        sections = wl_nlp_utils.split_into_chunks_text(text, 1)

    for section in sections:
        # spaCy
        if word_tokenizer.startswith('spacy_'):
            # Chinese, English, German, Portuguese
            if not lang.startswith('srp_'):
                lang = wl_conversion.remove_lang_code_suffixes(main, lang)

            nlp = main.__dict__[f'spacy_nlp_{lang}']
            doc = nlp(section)

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
            tokens_multilevel.append([])

            if section.strip():
                # NLTK
                if word_tokenizer.startswith('nltk_'):
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang)

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
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(main.__dict__[f'sacremoses_moses_tokenizer_{lang}'].tokenize(sentence, escape = False))
                # Chinese
                elif word_tokenizer == 'jieba_zho':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(jieba.lcut(sentence))
                elif word_tokenizer == 'pkuseg_zho':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(main.pkuseg_word_tokenizer.cut(sentence))
                elif word_tokenizer == 'wordless_zho_char':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = lang)

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
                                        for j, _ in enumerate(sentence[i:]):
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
                                        for j, _ in enumerate(sentence[i:]):
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
                elif word_tokenizer.startswith('sudachipy_jpn'):
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = lang)

                    if word_tokenizer == 'sudachipy_jpn_split_mode_a':
                        for sentence in sentences:
                            tokens_multilevel[-1].append([
                                token.surface()
                                for token in main.sudachipy_word_tokenizer.tokenize(sentence, sudachipy.SplitMode.A)
                            ])
                    elif word_tokenizer == 'sudachipy_jpn_split_mode_b':
                        for sentence in sentences:
                            tokens_multilevel[-1].append([
                                token.surface()
                                for token in main.sudachipy_word_tokenizer.tokenize(sentence, sudachipy.SplitMode.B)
                            ])
                    elif word_tokenizer == 'sudachipy_jpn_split_mode_c':
                        for sentence in sentences:
                            tokens_multilevel[-1].append([
                                token.surface()
                                for token in main.sudachipy_word_tokenizer.tokenize(sentence, sudachipy.SplitMode.C)
                            ])
                elif word_tokenizer == 'wordless_jpn_kanji':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = lang)

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
                                        for j, _ in enumerate(sentence[i:]):
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
                                        for j, _ in enumerate(sentence[i:]):
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
                                        for j, _ in enumerate(sentence[i:]):
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
                        main, section,
                        lang = 'isl',
                        sentence_tokenizer = 'tokenizer_isl'
                    )

                    for sentence in sentences:
                        tokens_multilevel[-1].append([
                            token
                            for kind, token, val in tokenizer.tokenize(sentence)
                            if token
                        ])
                # Thai
                elif word_tokenizer.startswith('pythainlp_'):
                    # Preserve sentence boundaries
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = 'tha')

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
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, section, lang = 'bod')

                    for sentence in sentences:
                        tokens_multilevel[-1].append([token.text
                                                      for token in main.botok_word_tokenizer.tokenize(sentence)])
                # Vietnamese
                elif word_tokenizer == 'underthesea_vie':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
                        main, section,
                        lang = 'vie',
                        sentence_tokenizer = 'underthesea_vie'
                    )

                    for sentence in sentences:
                        tokens_multilevel[-1].append(underthesea.word_tokenize(str(sentence)))

    # Remove empty tokens and strip whitespace
    for para in tokens_multilevel:
        for i, sentence in enumerate(para):
            para[i] = [
                token.strip()
                for token in sentence
                if token.strip()
            ]

    # Record token boundaries
    if lang in ['zho_cn', 'zho_tw', 'jpn']:
        for para in tokens_multilevel:
            for sentence in para:
                if sentence:
                    sentence[-1] = wl_texts.Wl_Token(sentence[-1], boundary = '', sentence_ending = True)
    else:
        for para in tokens_multilevel:
            for sentence in para:
                if sentence:
                    sentence[-1] = wl_texts.Wl_Token(sentence[-1], boundary = ' ', sentence_ending = True)

    return tokens_multilevel

def wl_word_tokenize_flat(main, text, lang, word_tokenizer = 'default'):
    tokens_multilevel = wl_word_tokenize(main, text, lang, word_tokenizer)

    return list(wl_misc.flatten_list(tokens_multilevel))
