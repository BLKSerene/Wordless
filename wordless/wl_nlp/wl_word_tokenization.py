# ----------------------------------------------------------------------
# Wordless: NLP - Word Tokenization
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import jieba
import pythainlp
import sudachipy
import underthesea

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import wl_nlp_utils, wl_sentence_tokenization
from wordless.wl_utils import wl_conversion, wl_misc

def wl_word_tokenize(main, text, lang, word_tokenizer = 'default'):
    tokens_multilevel = []

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizer_settings'][lang]

    wl_nlp_utils.init_word_tokenizers(
        main,
        lang = lang,
        word_tokenizer = word_tokenizer
    )

    lines = text.splitlines()

    # spaCy
    if word_tokenizer.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['tagger', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler']
            if nlp.has_pipe(pipeline)
        ]):
            for doc in nlp.pipe([line.strip() for line in lines]):
                tokens_multilevel.append([])

                for sentence in doc.sents:
                    tokens_multilevel[-1].append([token.text for token in sentence])
    else:
        for line in lines:
            tokens_multilevel.append([])

            if (line := line.strip()):
                # NLTK
                if word_tokenizer.startswith('nltk_'):
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang)

                    for sentence in sentences:
                        if word_tokenizer == 'nltk_nist':
                            tokens_multilevel[-1].append(main.nltk_nist_tokenizer.international_tokenize(sentence))
                        elif word_tokenizer == 'nltk_nltk':
                            tokens_multilevel[-1].append(main.nltk_nltk_tokenizer.tokenize(sentence))
                        elif word_tokenizer == 'nltk_penn_treebank':
                            tokens_multilevel[-1].append(main.nltk_treebank_tokenizer.tokenize(sentence))
                        elif word_tokenizer == 'nltk_regex':
                            tokens_multilevel[-1].append(main.nltk_regex_tokenizer.tokenize(sentence))
                        elif word_tokenizer == 'nltk_tok_tok':
                            tokens_multilevel[-1].append(main.nltk_toktok_tokenizer.tokenize(sentence))
                        elif word_tokenizer == 'nltk_twitter':
                            tokens_multilevel[-1].append(main.nltk_tweet_tokenizer.tokenize(sentence))
                # Sacremoses
                elif word_tokenizer == 'sacremoses_moses':
                    lang = wl_conversion.remove_lang_code_suffixes(main, lang)
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append(main.__dict__[f'sacremoses_moses_tokenizer_{lang}'].tokenize(sentence, escape = False))
                # Chinese
                elif lang.startswith('zho_'):
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = lang)

                    for sentence in sentences:
                        if word_tokenizer == 'jieba_zho':
                            tokens_multilevel[-1].append(jieba.lcut(sentence))
                        elif word_tokenizer == 'pkuseg_zho':
                            tokens_multilevel[-1].append(main.pkuseg_word_tokenizer.cut(sentence))
                        elif word_tokenizer == 'wordless_zho_char':
                            tokens = []
                            non_han_start = 0

                            for i, char in enumerate(sentence):
                                if i >= non_han_start:
                                    if wl_checks_tokens.is_han(char):
                                        tokens.append(char)

                                        non_han_start += 1
                                    else:
                                        # English
                                        if wl_checks_tokens.is_eng(char):
                                            for j, _ in enumerate(sentence[i:]):
                                                if i + j + 1 == len(sentence) or not wl_checks_tokens.is_eng(sentence[i + j + 1]):
                                                    tokens.extend(wl_word_tokenize_flat(
                                                        main, sentence[non_han_start : i + j + 1],
                                                        lang = 'eng_us'
                                                    ))

                                                    non_han_start = i + j + 1

                                                    break
                                        # Other Languages
                                        else:
                                            for j, _ in enumerate(sentence[i:]):
                                                if i + j + 1 == len(sentence) or wl_checks_tokens.is_han(sentence[i + j + 1]):
                                                    tokens.extend(wl_word_tokenize_flat(
                                                        main, sentence[non_han_start : i + j + 1],
                                                        lang = 'other'
                                                    ))

                                                    non_han_start = i + j + 1

                                                    break

                            tokens_multilevel[-1].append(tokens)
                # Japanese
                elif word_tokenizer.startswith('sudachipy_jpn'):
                    try:
                        if word_tokenizer == 'sudachipy_jpn_split_mode_a':
                            mode = sudachipy.SplitMode.A
                        elif word_tokenizer == 'sudachipy_jpn_split_mode_b':
                            mode = sudachipy.SplitMode.B
                        elif word_tokenizer == 'sudachipy_jpn_split_mode_c':
                            mode = sudachipy.SplitMode.C
                    # SudachiPy 0.5.4 is used on macOS for backward compatibility
                    except AttributeError:
                        if word_tokenizer == 'sudachipy_jpn_split_mode_a':
                            mode = sudachipy.tokenizer.Tokenizer.SplitMode.A
                        elif word_tokenizer == 'sudachipy_jpn_split_mode_b':
                            mode = sudachipy.tokenizer.Tokenizer.SplitMode.B
                        elif word_tokenizer == 'sudachipy_jpn_split_mode_c':
                            mode = sudachipy.tokenizer.Tokenizer.SplitMode.C

                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append([
                            token.surface()
                            for token in main.sudachipy_word_tokenizer.tokenize(sentence, mode = mode)
                        ])
                elif word_tokenizer == 'wordless_jpn_kanji':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = lang)

                    for sentence in sentences:
                        tokens = []
                        non_han_start = 0

                        for i, char in enumerate(sentence):
                            if i >= non_han_start:
                                if wl_checks_tokens.is_han(char):
                                    tokens.append(char)

                                    non_han_start += 1
                                else:
                                    # Japanese Kana
                                    if wl_checks_tokens.is_kana(char):
                                        for j, _ in enumerate(sentence[i:]):
                                            if i + j + 1 == len(sentence) or not wl_checks_tokens.is_kana(sentence[i + j + 1]):
                                                tokens.extend(wl_word_tokenize_flat(
                                                    main, sentence[non_han_start : i + j + 1],
                                                    lang = 'jpn'
                                                ))

                                                non_han_start = i + j + 1

                                                break
                                    # English
                                    elif wl_checks_tokens.is_eng(char):
                                        for j, _ in enumerate(sentence[i:]):
                                            if i + j + 1 == len(sentence) or not wl_checks_tokens.is_eng(sentence[i + j + 1]):
                                                tokens.extend(wl_word_tokenize_flat(
                                                    main, sentence[non_han_start : i + j + 1],
                                                    lang = 'eng_us'
                                                ))

                                                non_han_start = i + j + 1

                                                break
                                    # Other Languages
                                    else:
                                        for j, _ in enumerate(sentence[i:]):
                                            if i + j + 1 == len(sentence) or wl_checks_tokens.is_han(sentence[i + j + 1]):
                                                tokens.extend(wl_word_tokenize_flat(
                                                    main, sentence[non_han_start : i + j + 1],
                                                    lang = 'other'
                                                ))

                                                non_han_start = i + j + 1

                                                break

                        tokens_multilevel[-1].append(tokens)
                # Thai
                elif word_tokenizer.startswith('pythainlp_'):
                    # Preserve sentence boundaries
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = 'tha')

                    for sentence in sentences:
                        if word_tokenizer == 'pythainlp_longest_matching':
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'longest'))
                        elif word_tokenizer == 'pythainlp_max_matching':
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'mm'))
                        elif word_tokenizer == 'pythainlp_max_matching_tcc':
                            # Use safe mode by default
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'newmm-safe'))
                        elif word_tokenizer == 'pythainlp_nercut':
                            tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'nercut'))
                # Tibetan
                elif word_tokenizer == 'botok_bod':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = 'bod')

                    for sentence in sentences:
                        tokens_multilevel[-1].append([
                            token.text
                            for token in main.botok_word_tokenizer.tokenize(sentence)
                        ])
                # Vietnamese
                elif word_tokenizer == 'underthesea_vie':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
                        main, line,
                        lang = 'vie',
                        sentence_tokenizer = 'underthesea_vie'
                    )

                    for sentence in sentences:
                        tokens_multilevel[-1].append(underthesea.word_tokenize(str(sentence)))

    # Tokenize as sentence segments
    for para in tokens_multilevel:
        for i, sentence in enumerate(para):
            tokens = [token_clean for token in sentence if (token_clean := token.strip())]

            para[i] = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, tokens)

    return tokens_multilevel

def wl_word_tokenize_flat(main, text, lang, word_tokenizer = 'default'):
    tokens_multilevel = wl_word_tokenize(main, text, lang, word_tokenizer)

    return list(wl_misc.flatten_list(tokens_multilevel))
