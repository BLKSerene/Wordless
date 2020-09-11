#
# Wordless: Text - Stop Word Lists
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import importlib
import json

import nltk
import opencc
import pythainlp

from wl_text import wl_text_utils
from wl_utils import wl_conversion, wl_misc

def wl_get_stop_word_list(main, lang, stop_word_list = 'default'):
    if stop_word_list == 'default':
        stop_word_list = main.settings_custom['stop_word_lists']['stop_word_lists'][lang]

    if stop_word_list == main.tr('Custom List'):
        stop_word_list = main.settings_custom['stop_word_lists']['custom_lists'][lang]
    else:
        lang_639_1 = wl_conversion.to_iso_639_1(main, lang)

        # Chinese (Simplified)
        if lang_639_1 == 'zh_cn':
            lang_639_1 = 'zh'

        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            cc = opencc.OpenCC('s2tw.json')

            stop_word_list_zho_cn = wl_get_stop_word_list(
                main,
                lang = 'zho_cn',
                stop_word_list = stop_word_list.replace('Chinese (Traditional)', 'Chinese (Simplified)'))
            stop_word_list = [cc.convert(stop_word) for stop_word in stop_word_list_zho_cn]
        # extra-stopwords
        elif 'extra-stopwords' in stop_word_list:
            LANG_TEXTS = {
                'sqi': 'albanian',
                'ara': 'arabic',
                'hye': 'armenian',
                'eus': 'basque',
                'bel': 'belarusian',
                'ben': 'bengali',
                'bul': 'bulgarian',
                'cat': 'catalan',
                'zho_cn': 'chinese',
                'hrv': 'croatian',
                'ces': 'czech',
                'dan': 'danish',
                'nld': 'dutch',
                'eng': 'english',
                'est': 'estonian',
                'fin': 'finnish',
                'fra': 'french',
                'glg': 'galician',
                'deu': 'german',
                'ell': 'greek',
                'hau': 'hausa',
                'heb': 'hebrew',
                'hin': 'hindi',
                'hun': 'hungarian',
                'isl': 'icelandic',
                'ind': 'indonesian',
                'gle': 'irish',
                'ita': 'italian',
                'jpn': 'japanese',
                'kor': 'korean',
                'kur': 'kurdish',
                'lav': 'latvian',
                'lit': 'lithuanian',
                'msa': 'malay',
                'mar': 'marathi',
                'mon': 'mongolian',
                'nep': 'nepali',
                # Norwegian Bokmål & Norwegian Nynorsk
                'nob': 'norwegian',
                'nno': 'norwegian',
                'fas': 'persian',
                'pol': 'polish',
                'por': 'portuguese',
                'ron': 'romanian',
                'rus': 'russian',
                'srp_cyrl': 'serbian-cyrillic',
                'srp_latn': 'serbian',
                'slk': 'slovak',
                'slv': 'slovenian',
                'spa': 'spanish',
                'swa': 'swahili',
                'swe': 'swedish',
                'tgl': 'tagalog',
                'tel': 'telugu',
                'tha': 'thai',
                'tur': 'turkish',
                'ukr': 'ukranian',
                'urd': 'urdu',
                'vie': 'vietnamese',
                'yor': 'yoruba'
            }

            with open(wl_misc.get_normalized_path(f'stop_word_lists/extra-stopwords/{LANG_TEXTS[lang]}'), 'r', encoding = 'utf_8') as f:
                stop_word_list = [line.rstrip() for line in f if not line.startswith('#')]
        # NLTK
        elif 'NLTK' in stop_word_list:
            LANG_TEXTS = {
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
                # Norwegian Bokmål & Norwegian Nynorsk
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

            stop_word_list = nltk.corpus.stopwords.words(LANG_TEXTS[lang])
        # spaCy
        elif 'spaCy' in stop_word_list:
            # Serbian (Cyrillic) & Serbian (Latin)
            if lang_639_1 == 'sr_cyrl':
                spacy_lang = importlib.import_module('spacy.lang.sr')

                stop_word_list = spacy_lang.STOP_WORDS
            elif lang_639_1 == 'sr_latn':
                spacy_lang = importlib.import_module('spacy.lang.sr')

                stop_word_list = spacy_lang.STOP_WORDS
                stop_word_list = wl_text_utils.to_srp_latn(stop_word_list)
            else:
                spacy_lang = importlib.import_module(f'spacy.lang.{lang_639_1}')

                stop_word_list = spacy_lang.STOP_WORDS
        # Stopwords ISO
        elif 'Stopwords ISO' in stop_word_list:
            # Greek (Ancient)
            if lang_639_1 == 'grc':
                lang_639_1 = 'el'

            # Norwegian Bokmål & Norwegian Nynorsk
            if lang_639_1 in ['nb', 'nn']:
                lang_639_1 = 'no'

            with open(wl_misc.get_normalized_path('stop_word_lists/Stopwords ISO/stopwords_iso.json'), 'r', encoding = 'utf_8') as f:
                stop_word_list = json.load(f)[lang_639_1]
        # Thai
        elif stop_word_list == main.tr('PyThaiNLP - Thai Stop Word List'):
            stop_word_list = pythainlp.corpus.common.thai_stopwords()

    # Remove empty tokens
    stop_word_list = [stop_word for stop_word in stop_word_list if stop_word]

    return sorted(set(stop_word_list))

def wl_filter_stop_words(main, items, lang):
    if lang not in main.settings_global['stop_word_lists']:
        lang == 'other'

    stop_word_list = wl_get_stop_word_list(main, lang)

    # Check if the list is empty
    if items:
        if type(items[0]) == str:
            items_filtered = [token for token in items if token not in stop_word_list]
        elif type(items[0]) in [list, tuple, set]:
            items_filtered = [ngram
                              for ngram in items
                              if not [token for token in ngram if token in stop_word_list]]
    else:
        items_filtered = []

    return items_filtered
