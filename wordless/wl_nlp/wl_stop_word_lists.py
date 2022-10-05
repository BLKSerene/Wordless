# ----------------------------------------------------------------------
# Wordless: NLP - Stop Word Lists
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

import importlib

import nltk
import opencc
import pythainlp

from data import stopword
from wordless.wl_nlp import wl_nlp_utils
from wordless.wl_utils import wl_conversion

LANG_TEXTS_NLTK = {
    'ara': 'arabic',
    'aze': 'azerbaijani',
    'dan': 'danish',
    'nld': 'dutch',
    'eng': 'english',
    'fin': 'finnish',
    'fra': 'french',
    'deu': 'german',
    'ell': 'greek',
    'hun': 'hungarian',
    'ind': 'indonesian',
    'ita': 'italian',
    'kaz': 'kazakh',
    'nep': 'nepali',
    # Norwegian
    'nob': 'norwegian',
    'nno': 'norwegian',
    'por': 'portuguese',
    'ron': 'romanian',
    'rus': 'russian',
    'slv': 'slovene',
    'spa': 'spanish',
    'swe': 'swedish',
    'tgk': 'tajik',
    'tur': 'turkish'
}

def wl_get_stop_word_list(main, lang, stop_word_list = 'default'):
    if lang not in main.settings_global['stop_word_lists']:
        lang = 'other'

    if stop_word_list == 'default':
        stop_word_list = main.settings_custom['stop_word_lists']['stop_word_list_settings'][lang]

    stop_words = []

    if stop_word_list == 'custom':
        stop_words = main.settings_custom['stop_word_lists']['custom_lists'][lang]
    else:
        # Chinese (Traditional)
        if lang == 'zho_tw':
            converter = opencc.OpenCC('s2twp')

            stop_words_zho_cn = wl_get_stop_word_list(
                main,
                lang = 'zho_cn',
                stop_word_list = stop_word_list.replace('zho_tw', 'zho_cn')
            )
            stop_words = [converter.convert(stop_word) for stop_word in stop_words_zho_cn]
        # NLTK
        elif stop_word_list.startswith('nltk_'):
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)
            stop_words = nltk.corpus.stopwords.words(LANG_TEXTS_NLTK[lang])
        # spaCy
        elif stop_word_list.startswith('spacy_'):
            # Serbian
            if lang.startswith('srp_'):
                spacy_lang = importlib.import_module('spacy.lang.sr')
                stop_words = spacy_lang.STOP_WORDS

                if lang == 'srp_latn':
                    stop_words = wl_nlp_utils.to_srp_latn(stop_words)
            else:
                lang = wl_conversion.to_iso_639_1(main, lang)
                lang = wl_conversion.remove_lang_code_suffixes(main, lang)

                spacy_lang = importlib.import_module(f'spacy.lang.{lang}')
                stop_words = spacy_lang.STOP_WORDS
        # stopword
        elif stop_word_list.startswith('stopword_'):
            if lang == 'por_br':
                stop_words = stopword.porBr
            elif lang == 'pan_guru':
                stop_words = stopword.panGu
            else:
                lang = wl_conversion.remove_lang_code_suffixes(main, lang)
                stop_words = stopword.__dict__[lang]

            stop_words.extend(stopword.num123)

            # Language-specific numbers
            if lang in ['kor', 'mya', 'fas', 'tel']:
                stop_words.extend(stopword.__dict__[f'num{lang.capitalize()}'])
        # PyThaiNLP
        elif stop_word_list == 'pythainlp_tha':
            stop_words = pythainlp.corpus.common.thai_stopwords()

    # Remove empty tokens
    stop_words = [stop_word for stop_word in stop_words if stop_word.strip()]

    return set(stop_words)

def wl_filter_stop_words(main, items, lang):
    stop_word_list = wl_get_stop_word_list(main, lang)

    # Check if the list is empty
    if items:
        items_filtered = [token for token in items if token not in stop_word_list]
    else:
        items_filtered = []

    return items_filtered
