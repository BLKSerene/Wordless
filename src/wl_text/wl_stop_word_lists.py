#
# Wordless: Text - Stop Word Lists
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
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

    stop_words = []

    if stop_word_list == 'custom':
        stop_words = main.settings_custom['stop_word_lists']['custom_lists'][lang]
    else:
        lang_639_1 = wl_conversion.to_iso_639_1(main, lang)

        # Chinese (Simplified), English, German, Portuguese
        if lang != 'zho_tw' and 'srp' not in lang:
            lang_639_1 = wl_conversion.remove_lang_code_suffixes(main, wl_conversion.to_iso_639_1(main, lang))
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            cc = opencc.OpenCC('s2tw')

            stop_words_zho_cn = wl_get_stop_word_list(
                main,
                lang = 'zho_cn',
                stop_word_list = stop_word_list.replace('zho_tw', 'zho_cn'))
            stop_words = [cc.convert(stop_word) for stop_word in stop_words_zho_cn]
        elif 'cltk' in stop_word_list:
            stop_words = importlib.import_module(f'stop_word_lists.cltk.{lang}').STOPS
        # extra-stopwords
        elif 'extra_stopwords' in stop_word_list:
            LANG_TEXTS = {
                'sqi': 'albanian',
                'ara': 'arabic',
                'hye': 'armenian',
                'eus': 'basque',
                'bel': 'belarusian',
                'ben': 'bengali',
                'bul': 'bulgarian',
                'cat': 'catalan',
                'zho': 'chinese',
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
                # Norwegian
                'nob': 'norwegian',
                'nno': 'norwegian',
                'fas': 'persian',
                'pol': 'polish',
                'por': 'portuguese',
                'ron': 'romanian',
                'rus': 'russian',
                # Serbian
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
                stop_words = [line.rstrip() for line in f if not line.startswith('#')]
        # NLTK
        elif 'nltk' in stop_word_list:
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

            stop_words = nltk.corpus.stopwords.words(LANG_TEXTS[lang])
        # spaCy
        elif 'spacy' in stop_word_list:
            # Serbian
            if lang_639_1 == 'sr_cyrl':
                spacy_lang = importlib.import_module('spacy.lang.sr')

                stop_words = spacy_lang.STOP_WORDS
            elif lang_639_1 == 'sr_latn':
                spacy_lang = importlib.import_module('spacy.lang.sr')

                stop_words = spacy_lang.STOP_WORDS
                stop_words = wl_text_utils.to_srp_latn(stop_words)
            else:
                spacy_lang = importlib.import_module(f'spacy.lang.{lang_639_1}')

                stop_words = spacy_lang.STOP_WORDS
        # Stopwords ISO
        elif 'stopwords_iso' in stop_word_list:
            # Greek (Ancient)
            if lang_639_1 == 'grc':
                lang_639_1 = 'el'

            # Norwegian
            if lang_639_1 in ['nb', 'nn']:
                lang_639_1 = 'no'

            with open(wl_misc.get_normalized_path('stop_word_lists/Stopwords ISO/stopwords_iso.json'), 'r', encoding = 'utf_8') as f:
                stop_words = json.load(f)[lang_639_1]
        # Thai
        elif stop_word_list == 'pythainlp_tha':
            stop_words = pythainlp.corpus.common.thai_stopwords()

    # Remove empty tokens
    stop_words = [stop_word for stop_word in stop_words if stop_word.strip()]

    return sorted(set(stop_words))

def wl_filter_stop_words(main, items, lang):
    if lang not in main.settings_global['stop_word_lists']:
        lang == 'other'

    stop_word_list = wl_get_stop_word_list(main, lang)

    # Check if the list is empty
    if items:
        items_filtered = [token for token in items if token not in stop_word_list]
    else:
        items_filtered = []

    return items_filtered
