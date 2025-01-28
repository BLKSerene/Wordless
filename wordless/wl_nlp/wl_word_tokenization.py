# ----------------------------------------------------------------------
# Wordless: NLP - Word tokenization
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import re

import khmernltk
import laonlp
import pythainlp
import sudachipy
import underthesea

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import wl_nlp_utils, wl_sentence_tokenization, wl_texts
from wordless.wl_utils import wl_conversion, wl_misc

RE_CHAR_HAN_OTHER = re.compile(r'^h+|^o+')
RE_CHAR_HAN_KANJI_OTHER = re.compile(r'^h+|^k+|^o+')

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
            for pipeline in ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler']
            if nlp.has_pipe(pipeline)
        ]):
            for doc in nlp.pipe([line.strip() for line in lines]):
                tokens_multilevel.append([])

                for sentence in doc.sents:
                    tokens_multilevel[-1].append([token.text for token in sentence])
    # Stanza
    elif word_tokenizer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'stanza_nlp_{lang}']

        for doc in nlp.bulk_process([line.strip() for line in lines]):
            tokens_multilevel.append([])

            for sentence in doc.sentences:
                tokens_multilevel[-1].append([token.text for token in sentence.tokens])
    else:
        for line in lines:
            tokens_multilevel.append([])

            if (line := line.strip()):
                # NLTK
                if word_tokenizer.startswith('nltk_'):
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang)

                    match word_tokenizer:
                        case 'nltk_nist':
                            for sentence in sentences:
                                tokens_multilevel[-1].append(main.nltk_nist_tokenizer.international_tokenize(sentence))
                        case 'nltk_nltk':
                            for sentence in sentences:
                                tokens_multilevel[-1].append(main.nltk_nltk_tokenizer.tokenize(sentence))
                        case 'nltk_penn_treebank':
                            for sentence in sentences:
                                tokens_multilevel[-1].append(main.nltk_treebank_tokenizer.tokenize(sentence))
                        case 'nltk_regex':
                            for sentence in sentences:
                                tokens_multilevel[-1].append(main.nltk_regex_tokenizer.tokenize(sentence))
                        case 'nltk_tok_tok':
                            for sentence in sentences:
                                tokens_multilevel[-1].append(main.nltk_toktok_tokenizer.tokenize(sentence))
                        case 'nltk_twitter':
                            for sentence in sentences:
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

                    if word_tokenizer == 'pkuseg_zho':
                        for sentence in sentences:
                            tokens_multilevel[-1].append(main.pkuseg_word_tokenizer.cut(sentence))
                    elif word_tokenizer == 'wordless_zho_char':
                        for sentence in sentences:
                            char_scripts = ''
                            tokens = []

                            for char in sentence:
                                if wl_checks_tokens.is_han(char):
                                    char_scripts += 'h'
                                else:
                                    char_scripts += 'o'

                            while sentence:
                                len_token = len(RE_CHAR_HAN_OTHER.search(char_scripts).group())
                                token = sentence[:len_token]

                                if char_scripts.startswith('h'):
                                    tokens.extend(token)
                                else:
                                    tokens.extend(wl_word_tokenize_flat(
                                        main, token,
                                        lang = 'other'
                                    ))

                                char_scripts = char_scripts[len_token:]
                                sentence = sentence[len_token:]

                            tokens_multilevel[-1].append(tokens)
                # Japanese
                elif word_tokenizer.startswith('sudachipy_jpn'):
                    match word_tokenizer:
                        case 'sudachipy_jpn_split_mode_a':
                            mode = sudachipy.SplitMode.A
                        case 'sudachipy_jpn_split_mode_b':
                            mode = sudachipy.SplitMode.B
                        case 'sudachipy_jpn_split_mode_c':
                            mode = sudachipy.SplitMode.C

                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = lang)

                    for sentence in sentences:
                        tokens_multilevel[-1].append([
                            token.surface()
                            for token in main.sudachipy_word_tokenizer.tokenize(sentence, mode = mode)
                        ])
                elif word_tokenizer == 'wordless_jpn_kanji':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = lang)

                    for sentence in sentences:
                        char_scripts = ''
                        tokens = []

                        for char in sentence:
                            if wl_checks_tokens.is_han(char):
                                char_scripts += 'h'
                            elif wl_checks_tokens.is_kana(char):
                                char_scripts += 'k'
                            else:
                                char_scripts += 'o'

                        while sentence:
                            len_token = len(RE_CHAR_HAN_KANJI_OTHER.search(char_scripts).group())
                            token = sentence[:len_token]

                            if char_scripts.startswith('h'):
                                tokens.extend(token)
                            elif char_scripts.startswith('k'):
                                tokens.extend(wl_word_tokenize_flat(
                                    main, token,
                                    lang = 'jpn',
                                    word_tokenizer = main.settings_default['word_tokenization']['word_tokenizer_settings']['jpn']
                                ))
                            else:
                                tokens.extend(wl_word_tokenize_flat(
                                    main, token,
                                    lang = 'other'
                                ))

                            char_scripts = char_scripts[len_token:]
                            sentence = sentence[len_token:]

                        tokens_multilevel[-1].append(tokens)
                # Khmer
                elif word_tokenizer == 'khmer_nltk_khm':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = 'khm')

                    for sentence in sentences:
                        tokens_multilevel[-1].append(khmernltk.word_tokenize(line))
                # Korean
                elif word_tokenizer == 'python_mecab_ko_mecab':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = 'kor')

                    for sentence in sentences:
                        tokens_multilevel[-1].append(main.python_mecab_ko_mecab.morphs(sentence))
                # Lao
                elif word_tokenizer == 'laonlp_lao':
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = 'lao')

                    for sentence in sentences:
                        tokens_multilevel[-1].append(laonlp.word_tokenize(sentence))
                # Thai
                elif word_tokenizer.startswith('pythainlp_'):
                    # Preserve sentence boundaries
                    sentences = wl_sentence_tokenization.wl_sentence_tokenize(main, line, lang = 'tha')

                    for sentence in sentences:
                        match word_tokenizer:
                            case 'pythainlp_longest_matching':
                                tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'longest'))
                            case 'pythainlp_max_matching':
                                tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'mm'))
                            case 'pythainlp_max_matching_tcc':
                                # Use safe mode by default
                                tokens_multilevel[-1].append(pythainlp.word_tokenize(sentence, engine = 'newmm-safe'))
                            case 'pythainlp_nercut':
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
            para[i] = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(main, wl_texts.clean_texts(sentence))

    for para in tokens_multilevel:
        for sentence in para:
            for i, sentence_seg in enumerate(sentence):
                sentence[i] = wl_texts.to_tokens(sentence_seg, lang)

    return tokens_multilevel

def wl_word_tokenize_flat(main, text, lang, word_tokenizer = 'default'):
    tokens_multilevel = wl_word_tokenize(main, text, lang, word_tokenizer)

    return list(wl_misc.flatten_list(tokens_multilevel))
