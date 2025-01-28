# ----------------------------------------------------------------------
# Wordless: NLP - Sentence tokenization
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

# pylint: disable=unused-argument

import re

import botok
import khmernltk
import laonlp
import nltk
import pythainlp
import underthesea

from wordless.wl_nlp import wl_nlp_utils, wl_texts
from wordless.wl_utils import wl_conversion

LANG_TEXTS_NLTK = {
    'ces': 'czech',
    'dan': 'danish',
    'nld': 'dutch',
    'eng_gb': 'english',
    'eng_us': 'english',
    'est': 'estonian',
    'fin': 'finnish',
    'fra': 'french',
    'deu_at': 'german',
    'deu_de': 'german',
    'deu_ch': 'german',
    'ell': 'greek',
    'ita': 'italian',
    'mal': 'malayalam',
    'nob': 'norwegian',
    'pol': 'polish',
    'por_br': 'portuguese',
    'por_pt': 'portuguese',
    'rus': 'russian',
    'slv': 'slovene',
    'spa': 'spanish',
    'swe': 'swedish',
    'tur': 'turkish',

    'other': 'english'
}

def wl_sentence_tokenize(main, text, lang, sentence_tokenizer = 'default'):
    sentences = []

    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'][lang]

    wl_nlp_utils.init_sentence_tokenizers(
        main,
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    lines = text.splitlines()

    # spaCy
    if sentence_tokenizer.startswith('spacy_'):
        # Dependency parsers
        if sentence_tokenizer.startswith('spacy_dependency_parser_'):
            pipelines_disabled = ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter']
        # Sentence recognizers and sentencizer
        else:
            pipelines_disabled = ['tagger', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler']

        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        if sentence_tokenizer == 'spacy_sentencizer':
            nlp = main.__dict__['spacy_nlp_sentencizer']
        else:
            if lang == 'nno':
                nlp = main.spacy_nlp_nob
            else:
                nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in pipelines_disabled
            if nlp.has_pipe(pipeline)
        ]):
            for doc in nlp.pipe(lines):
                sentences.extend([sentence.text for sentence in doc.sents])
    # Stanza
    elif sentence_tokenizer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'stanza_nlp_{lang}']

        for doc in nlp.bulk_process(lines):
            sentences.extend([sentence.text for sentence in doc.sentences])
    else:
        for line in lines:
            # NLTK
            if sentence_tokenizer.startswith('nltk_punkt'):
                sentences.extend(nltk.sent_tokenize(line, language = LANG_TEXTS_NLTK[lang]))
            # Khmer
            elif sentence_tokenizer == 'khmer_nltk_khm':
                sentences.extend(khmernltk.sentence_tokenize(line))
            # Lao
            elif sentence_tokenizer == 'laonlp_lao':
                sentences.extend(laonlp.sent_tokenize(line))
            # Thai
            elif sentence_tokenizer == 'pythainlp_crfcut':
                sentences.extend(pythainlp.sent_tokenize(line, engine = 'crfcut'))
            elif sentence_tokenizer == 'pythainlp_thaisumcut':
                sentences.extend(pythainlp.sent_tokenize(line, engine = 'thaisum'))
            # Tibetan
            elif sentence_tokenizer == 'botok_bod':
                wl_nlp_utils.init_word_tokenizers(main, lang = 'bod')

                tokens = main.botok_word_tokenizer.tokenize(line)

                for sentence_tokens in botok.sentence_tokenizer(tokens):
                    sentences.append(''.join([
                        sentence_token.text
                        for sentence_token in sentence_tokens['tokens']
                    ]))
            # Vietnamese
            elif sentence_tokenizer == 'underthesea_vie':
                sentences.extend(underthesea.sent_tokenize(line))

    return wl_texts.clean_texts(sentences)

# References:
#     https://stackoverflow.com/questions/9506869/are-there-character-collections-for-all-international-full-stop-punctuations/9508766#9508766
#     https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:Terminal_Punctuation=Yes:]%26[:Sentence_Break=/[AS]Term/:]
SENTENCE_TERMINATORS = ''.join(list(dict.fromkeys([
    '\u0021', '\u002E', '\u003F',
    '\u0589',
    '\u061D', '\u061E', '\u061F', '\u06D4',
    '\u0700', '\u0701', '\u0702',
    '\u07F9',
    '\u0837', '\u0839', '\u083D', '\u083E',
    '\u0964', '\u0965',
    '\u104A', '\u104B',
    '\u1362', '\u1367', '\u1368',
    '\u166E',
    '\u1735', '\u1736',
    '\u17D4', '\u17D5',
    '\u1803', '\u1809',
    '\u1944', '\u1945',
    '\u1AA8', '\u1AA9', '\u1AAA', '\u1AAB',
    '\u1B5A', '\u1B5B', '\u1B5E', '\u1B5F', '\u1B7D', '\u1B7E',
    '\u1C3B', '\u1C3C',
    '\u1C7E', '\u1C7F',
    '\u203C', '\u2047', '\u2048', '\u2049', '\u203D',
    '\u2E2E', '\u2E53', '\u2E54', '\u2E3C',
    '\u3002',
    '\uA4FF',
    '\uA60E', '\uA60F',
    '\uA6F3', '\uA6F7',
    '\uA876', '\uA877',
    '\uA8CE', '\uA8CF',
    '\uA92F',
    '\uA9C8', '\uA9C9',
    '\uAA5D', '\uAA5E', '\uAA5F',
    '\uAAF0', '\uAAF1', '\uABEB',
    '\uFE52', '\uFE56', '\uFE57',
    '\uFF01', '\uFF0E', '\uFF1F', '\uFF61',
    '\U00010A56', '\U00010A57',
    '\U00010F55', '\U00010F56', '\U00010F57', '\U00010F58', '\U00010F59',
    '\U00010F86', '\U00010F87', '\U00010F88', '\U00010F89',
    '\U00011047', '\U00011048',
    '\U000110BE', '\U000110BF', '\U000110C0', '\U000110C1',
    '\U00011141', '\U00011142', '\U00011143',
    '\U000111C5', '\U000111C6', '\U000111CD', '\U000111DE', '\U000111DF',
    '\U00011238', '\U00011239', '\U0001123B', '\U0001123C',
    '\U000112A9',
    '\U0001144B', '\U0001144C',
    '\U000115C2', '\U000115C3', '\U000115C9', '\U000115CA', '\U000115CB', '\U000115CC', '\U000115CD', '\U000115CE', '\U000115CF', '\U000115D0', '\U000115D1', '\U000115D2', '\U000115D3', '\U000115D4', '\U000115D5', '\U000115D6', '\U000115D7',
    '\U00011641', '\U00011642',
    '\U0001173C', '\U0001173D', '\U0001173E',
    '\U00011944', '\U00011946',
    '\U00011A42', '\U00011A43',
    '\U00011A9B', '\U00011A9C',
    '\U00011C41', '\U00011C42',
    '\U00011EF7', '\U00011EF8',
    '\U00011F43', '\U00011F44',
    '\U00016A6E', '\U00016A6F',
    '\U00016AF5',
    '\U00016B37', '\U00016B38', '\U00016B44',
    '\U00016E98',
    '\U0001BC9F',
    '\U0001DA88'
])))

def wl_sentence_split(main, text, terminators = SENTENCE_TERMINATORS):
    re_terminators = re.compile(fr'.+?[{terminators}]+\s|.+?$')

    return [
        sentence.strip()
        for sentence in re_terminators.findall(text.strip())
    ]

# Reference: https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:Terminal_Punctuation=Yes:]
SENTENCE_SEG_TERMINATORS = ''.join(list(dict.fromkeys([
    '\u0021', '\u002C', '\u002E', '\u003A', '\u003B', '\u003F',
    '\u037E', '\u0387',
    '\u0589',
    '\u05C3',
    '\u060C', '\u061B', '\u061D', '\u061E', '\u061F', '\u06D4',
    '\u0700', '\u0701', '\u0702', '\u0703', '\u0704', '\u0705', '\u0706', '\u0707', '\u0708', '\u0709', '\u070A', '\u070C',
    '\u07F8', '\u07F9',
    '\u0830', '\u0831', '\u0832', '\u0833', '\u0834', '\u0835', '\u0836', '\u0837', '\u0838', '\u0839', '\u083A', '\u083B', '\u083C', '\u083D', '\u083E',
    '\u085E',
    '\u0964', '\u0965',
    '\u0E5A', '\u0E5B',
    '\u0F08', '\u0F0D', '\u0F0E', '\u0F0F', '\u0F10', '\u0F11', '\u0F12',
    '\u104A', '\u104B',
    '\u1361', '\u1362', '\u1363', '\u1364', '\u1365', '\u1366', '\u1367', '\u1368',
    '\u166E',
    '\u16EB', '\u16EC', '\u16ED',
    '\u1735', '\u1736',
    '\u17D4', '\u17D5', '\u17D6', '\u17DA',
    '\u1802', '\u1803', '\u1804', '\u1805', '\u1808', '\u1809',
    '\u1944', '\u1945',
    '\u1AA8', '\u1AA9', '\u1AAA', '\u1AAB',
    '\u1B5A', '\u1B5B', '\u1B5D', '\u1B5E', '\u1B5F', '\u1B7D', '\u1B7E',
    '\u1C3B', '\u1C3C', '\u1C3D', '\u1C3E', '\u1C3F',
    '\u1C7E', '\u1C7F',
    '\u203C', '\u2047', '\u2048', '\u2049', '\u203D',
    '\u2E2E', '\u2E4C', '\u2E4E', '\u2E4F', '\u2E53', '\u2E54', '\u2E3C', '\u2E41',
    '\u3001', '\u3002',
    '\uA4FE', '\uA4FF',
    '\uA60D', '\uA60E', '\uA60F',
    '\uA6F3', '\uA6F4', '\uA6F5', '\uA6F6', '\uA6F7',
    '\uA876', '\uA877',
    '\uA8CE', '\uA8CF',
    '\uA92F',
    '\uA9C7', '\uA9C8', '\uA9C9',
    '\uAA5D', '\uAA5E', '\uAA5F',
    '\uAADF',
    '\uAAF0', '\uAAF1', '\uABEB',
    '\uFE50', '\uFE51', '\uFE52', '\uFE54', '\uFE55', '\uFE56', '\uFE57',
    '\uFF01', '\uFF0C', '\uFF0E', '\uFF1A', '\uFF1B', '\uFF1F', '\uFF61', '\uFF64',
    '\U0001039F',
    '\U000103D0',
    '\U00010857',
    '\U0001091F',
    '\U00010A56', '\U00010A57',
    '\U00010AF0', '\U00010AF1', '\U00010AF2', '\U00010AF3', '\U00010AF4', '\U00010AF5',
    '\U00010B3A', '\U00010B3B', '\U00010B3C', '\U00010B3D', '\U00010B3E', '\U00010B3F',
    '\U00010B99', '\U00010B9A', '\U00010B9B', '\U00010B9C',
    '\U00010F55', '\U00010F56', '\U00010F57', '\U00010F58', '\U00010F59',
    '\U00010F86', '\U00010F87', '\U00010F88', '\U00010F89',
    '\U00011047', '\U00011048', '\U00011049', '\U0001104A', '\U0001104B', '\U0001104C', '\U0001104D',
    '\U000110BE', '\U000110BF', '\U000110C0', '\U000110C1',
    '\U00011141', '\U00011142', '\U00011143',
    '\U000111C5', '\U000111C6', '\U000111CD', '\U000111DE', '\U000111DF',
    '\U00011238', '\U00011239', '\U0001123A', '\U0001123B', '\U0001123C',
    '\U000112A9',
    '\U0001144B', '\U0001144C', '\U0001144D', '\U0001145A', '\U0001145B',
    '\U000115C2', '\U000115C3', '\U000115C4', '\U000115C5', '\U000115C9', '\U000115CA', '\U000115CB', '\U000115CC', '\U000115CD', '\U000115CE', '\U000115CF', '\U000115D0', '\U000115D1', '\U000115D2', '\U000115D3', '\U000115D4', '\U000115D5', '\U000115D6', '\U000115D7',
    '\U00011641', '\U00011642',
    '\U0001173C', '\U0001173D', '\U0001173E',
    '\U00011944', '\U00011946',
    '\U00011A42', '\U00011A43',
    '\U00011A9B', '\U00011A9C', '\U00011AA1', '\U00011AA2',
    '\U00011C41', '\U00011C42', '\U00011C43',
    '\U00011C71',
    '\U00011EF7', '\U00011EF8',
    '\U00011F43', '\U00011F44',
    '\U00012470', '\U00012471', '\U00012472', '\U00012473', '\U00012474',
    '\U00016A6E', '\U00016A6F',
    '\U00016AF5',
    '\U00016B37', '\U00016B38', '\U00016B39', '\U00016B44',
    '\U00016E97', '\U00016E98',
    '\U0001BC9F',
    '\U0001DA87', '\U0001DA88', '\U0001DA89', '\U0001DA8A'
])))

def wl_sentence_seg_tokenize(main, text, terminators = SENTENCE_SEG_TERMINATORS):
    re_terminators = re.compile(fr'.+?[{terminators}]+|.+?$')

    return [
        sentence_seg.strip()
        for sentence_seg in re_terminators.findall(text.strip())
    ]

REPLACEMENT_CHAR = '\uFFFF'

def wl_sentence_seg_tokenize_tokens(main, tokens, terminators = SENTENCE_SEG_TERMINATORS):
    # Insert a replacement character between tokens to prevent text from being split within tokens
    text = REPLACEMENT_CHAR.join(tokens)
    re_terminators = re.compile(fr'.+?[{terminators}]+{REPLACEMENT_CHAR}|.+?$')

    return [
        wl_texts.clean_texts(sentence_seg.split(REPLACEMENT_CHAR))
        for sentence_seg in re_terminators.findall(text.strip())
    ]
