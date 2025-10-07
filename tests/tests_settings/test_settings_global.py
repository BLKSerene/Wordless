# ----------------------------------------------------------------------
# Tests: Settings - Global settings
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

import os
import pkgutil
import re

import nltk
import pyphen
import requests
import sacremoses
import simplemma
import spacy
import spacy_lookups_data

from tests import wl_test_init
from wordless.wl_nlp import wl_nlp_utils
from wordless.wl_utils import (
    wl_conversion,
    wl_misc
)

main = wl_test_init.Wl_Test_Main()

def add_lang_suffixes(lang_codes):
    lang_codes = sorted(set(lang_codes))

    for lang_code in lang_codes.copy():
        if lang_code == 'hy':
            lang_codes.append('hyw')

        if lang_code in {'zh', 'en', 'de', 'pt', 'sr'}:
            lang_codes.remove(lang_code)

            match lang_code:
                case 'zh':
                    lang_codes.extend(('zh_cn', 'zh_tw'))
                case 'en':
                    lang_codes.extend(('en_gb', 'en_us'))
                case 'de':
                    lang_codes.extend(('de_at', 'de_de', 'de_ch'))
                case 'pt':
                    lang_codes.extend(('pt_br', 'pt_pt'))
                case 'sr':
                    lang_codes.append('sr_cyrl')

    # Sorted by language names
    for i, lang_code in enumerate(lang_codes.copy()):
        lang_code = wl_conversion.to_iso_639_3(main, lang_code)
        lang_codes[i] = wl_conversion.to_lang_text(main, lang_code)

    lang_codes = sorted(lang_codes)

    for i, lang_text in enumerate(lang_codes.copy()):
        lang_code = wl_conversion.to_lang_code(main, lang_text)
        lang_codes[i] = wl_conversion.to_iso_639_1(main, lang_code)

    return lang_codes

def check_missing_extra_langs(langs_supported, langs_settings, util_type):
    langs_supported = set(langs_supported)
    langs_settings = set(langs_settings)

    for lang_code in langs_supported:
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        assert lang_code_639_3 in langs_settings, f'Missing language code for {util_type}: {lang_code_639_3}/{lang_code}!'

    for lang_code in langs_settings:
        lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

        assert lang_code_639_1 in langs_supported, f'Extra language code for {util_type}: {lang_code}/{lang_code_639_1}!'

def check_missing_extra_langs_default(langs, langs_default, util_type):
    for lang_code in langs:
        assert lang_code in langs_default, f'Missing language code for default {util_type}: {lang_code}!'

    for lang_code_default in langs_default:
        assert lang_code_default in langs, f'Extra language code for default {util_type}: {lang_code_default}!'

def check_invalid_default_lang_utils(lang_utils, lang_utils_default, util_type):
    for lang, lang_util in lang_utils_default.items():
        assert lang_util in lang_utils[lang], f'Invalid default value for default {util_type}: {lang} - {lang_util}!'

        # Prefer Stanza over spaCy since their accuracy are comparable but spaCy's transformer models are much slower
        if (
            not (
                lang in {'tha', 'vie', 'other'}
                and util_type in {'sentence tokenizers', 'word tokenizers', 'POS taggers', 'sentiment analyzers'}
            )
            and any(('stanza_' in util for util in lang_utils[lang]))
        ):
            assert lang_util.startswith('stanza_'), f'Stanza not set as the default {util_type}: {lang} - {lang_util}!'

def check_lang_order(main, langs, util_type):
    langs_global = [lang_code[0] for lang_code in main.settings_global['langs'].values()]

    for lang, lang_global in zip(langs, [lang for lang in langs_global if lang in langs]):
        assert lang == lang_global, f'Inconsistent language order for {util_type}: {lang} | {lang_global}!'

def test_settings_global():
    settings_global = main.settings_global
    settings_default = main.settings_default

    settings_sentence_tokenizers = settings_global['sentence_tokenizers']
    settings_sentence_tokenizers_default = settings_default['sentence_tokenization']['sentence_tokenizer_settings']
    settings_word_tokenizers = settings_global['word_tokenizers']
    settings_word_tokenizers_default = settings_default['word_tokenization']['word_tokenizer_settings']
    settings_syl_tokenizers = settings_global['syl_tokenizers']
    settings_syl_tokenizers_default = settings_default['syl_tokenization']['syl_tokenizer_settings']
    settings_pos_taggers = settings_global['pos_taggers']
    settings_pos_taggers_default = settings_default['pos_tagging']['pos_tagger_settings']['pos_taggers']
    settings_lemmatizers = settings_global['lemmatizers']
    settings_lemmatizers_default = settings_default['lemmatization']['lemmatizer_settings']
    settings_stop_word_lists = settings_global['stop_word_lists']
    settings_stop_word_lists_default = settings_default['stop_word_lists']['stop_word_list_settings']['stop_word_lists']
    settings_dependency_parsers = settings_global['dependency_parsers']
    settings_dependency_parsers_default = settings_default['dependency_parsing']['dependency_parser_settings']
    settings_sentiment_analyzers = settings_global['sentiment_analyzers']
    settings_sentiment_analyzers_default = settings_default['sentiment_analysis']['sentiment_analyzer_settings']

    # NLTK
    langs_nltk_supported = []
    langs_nltk_settings = []

    for lang in os.listdir(nltk.data.find('tokenizers/punkt_tab/')):
        match lang:
            case 'english':
                langs_nltk_supported.extend(('en_gb', 'en_us'))
            case 'german':
                langs_nltk_supported.extend(('de_at', 'de_de', 'de_ch'))
            case 'greek':
                langs_nltk_supported.append('el')
            case 'norwegian':
                langs_nltk_supported.append('nb')
            case 'portuguese':
                langs_nltk_supported.extend(('pt_br', 'pt_pt'))
            case 'slovene':
                langs_nltk_supported.append('sl')
            case 'README':
                pass
            case _:
                langs_nltk_supported.append(wl_conversion.to_lang_code(
                    main,
                    lang.capitalize(),
                    iso_639_3 = False
                ))

    for lang_code, sentence_tokenizers in settings_sentence_tokenizers.items():
        if (
            lang_code != 'other'
            and any((
                sentence_tokenizer.startswith('nltk_punkt_')
                for sentence_tokenizer in sentence_tokenizers
            ))
        ):
            langs_nltk_settings.append(lang_code)

    check_missing_extra_langs(
        langs_nltk_supported,
        langs_nltk_settings,
        "NLTK's Punkt sentence tokenizer"
    )

    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if lang_code != 'other':
            # Exclude languages without spaces between words and Vietnamese where spaces indicate boundaries of syllables instead of words
            if lang_code not in wl_nlp_utils.LANGS_WITHOUT_SPACES + ('vie',):
                assert all((
                    nltk_word_tokenizer in word_tokenizers
                    for nltk_word_tokenizer in ('nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter')
                )), f"Missing language code for NLTK's tokenizers: {lang_code}!"
            else:
                assert not any((
                    nltk_word_tokenizer in word_tokenizers
                    for nltk_word_tokenizer in ('nltk_nist', 'nltk_nltk', 'nltk_regex', 'nltk_twitter')
                )), f"Extra language code for NLTK's tokenizers: {lang_code}!"

    # Sacremoses
    langs_sacremoses_supported = []
    langs_sacremoses_settings = []

    for file in os.listdir(os.path.split(sacremoses.__file__)[0] + '/data/nonbreaking_prefixes/'):
        file_ext = os.path.splitext(file)[1][1:]

        if file_ext not in {'yue', 'zh'}:
            langs_sacremoses_supported.append(file_ext)

    langs_sacremoses_supported = add_lang_suffixes(langs_sacremoses_supported)

    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if (
            lang_code != 'other'
            and 'sacremoses_moses' in word_tokenizers
        ):
            langs_sacremoses_settings.append(lang_code)

    check_missing_extra_langs(
        langs_sacremoses_supported,
        langs_sacremoses_settings,
        "Sacremoses's Moses tokenizer"
    )

    # Pyphen
    langs_pyphen_supported = []
    langs_pyphen_settings = []

    for lang in pyphen.LANGUAGES:
        match lang:
            case 'de' | 'en' | 'pt':
                pass
            case 'de_AT' | 'de_DE' | 'de_CH' | 'en_GB' | 'en_US' | 'pt_BR' | 'pt_PT':
                langs_pyphen_supported.append(lang.lower())
            case 'mn' | 'mn_MN':
                langs_pyphen_supported.append('mn_cyrl')
            case 'pa':
                langs_pyphen_supported.append('pa_guru')
            case 'sr':
                langs_pyphen_supported.append('sr_cyrl')
            case 'sr_Latn':
                langs_pyphen_supported.append('sr_latn')
            case _:
                langs_pyphen_supported.append(lang.split('_')[0])

    for lang_code, syl_tokenizers in settings_syl_tokenizers.items():
        if (
            lang_code != 'other'
            and any((
                syl_tokenizer.startswith('pyphen_')
                for syl_tokenizer in syl_tokenizers
            ))
        ):
            langs_pyphen_settings.append(lang_code)

    check_missing_extra_langs(
        langs_pyphen_supported,
        langs_pyphen_settings,
        "Pyphen's syllable tokenizer"
    )

    # simplemma
    langs_simplemma_supported = []
    langs_simplemma_settings = []

    for lang in simplemma.strategies.dictionaries.dictionary_factory.SUPPORTED_LANGUAGES:
        if lang == 'hbs':
            langs_simplemma_supported.extend(('hr', 'sr_latn'))
        else:
            langs_simplemma_supported.append(lang)

    langs_simplemma_supported = add_lang_suffixes(langs_simplemma_supported)

    for lang_code, lemmatizers in settings_lemmatizers.items():
        if any((
            lemmatizer.startswith('simplemma_')
            for lemmatizer in lemmatizers
        )):
            langs_simplemma_settings.append(lang_code)

    check_missing_extra_langs(
        langs_simplemma_supported,
        langs_simplemma_settings,
        "simplemma's lemmatizers"
    )

    # spaCy
    langs_spacy_supported_word_tokenizers = []
    langs_spacy_supported_lemmatizers = []
    langs_spacy_supported_stop_word_lists = []

    langs_spacy_settings_word_tokenizers = []
    langs_spacy_settings_lemmatizers = []
    langs_spacy_settings_stop_word_lists = []

    for lang in pkgutil.iter_modules(spacy.lang.__path__):
        # Tibetan tokenizer is not funtional
        # Thai and Vietnamese tokenization are delegated to PyThaiNLP and Pyvi
        if lang.ispkg and lang.name not in {'bo', 'th', 'vi', 'xx'}:
            langs_spacy_supported_word_tokenizers.append(lang.name)

    langs_spacy_supported_word_tokenizers = add_lang_suffixes(langs_spacy_supported_word_tokenizers)

    for file in os.listdir(f'{spacy_lookups_data.__path__[0]}/data/'):
        if 'lemma' in file:
            lang_code = re.search(r'^([a-z]{2,3})_', file).groups()[0]

            langs_spacy_supported_lemmatizers.append(lang_code)

    # Languages without data files for lemmatizers
    langs_spacy_supported_lemmatizers.extend(('fi', 'ja', 'ko', 'sl', 'uk'))
    langs_spacy_supported_lemmatizers = add_lang_suffixes(langs_spacy_supported_lemmatizers)

    for lang in pkgutil.iter_modules(spacy.lang.__path__):
        if lang.ispkg and 'stop_words.py' in os.listdir(f'{spacy.lang.__path__[0]}/{lang.name}/'):
            match lang.name:
                case 'sr':
                    langs_spacy_supported_stop_word_lists.extend(('sr_cyrl', 'sr_latn'))
                case 'bo':
                    langs_spacy_supported_stop_word_lists.extend(('xct', 'bo'))
                case 'xx':
                    continue
                case _:
                    langs_spacy_supported_stop_word_lists.append(lang.name)

    langs_spacy_supported_stop_word_lists = add_lang_suffixes(langs_spacy_supported_stop_word_lists)

    for lang_code, sentence_tokenizers in settings_sentence_tokenizers.items():
        if not any((
            sentence_tokenizer.startswith('spacy_')
            for sentence_tokenizer in sentence_tokenizers
        )):
            lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

            assert lang_code in wl_nlp_utils.LANGS_WITHOUT_SPACES + ('vie',), f"Missing language code for spaCy's sentence recognizers or sentencizer: {lang_code}/{lang_code_639_1}!"

    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if (
            lang_code != 'other'
            and any((
                word_tokenizer.startswith('spacy_')
                for word_tokenizer in word_tokenizers
            ))
        ):
            langs_spacy_settings_word_tokenizers.append(lang_code)

    check_missing_extra_langs(
        langs_spacy_supported_word_tokenizers,
        langs_spacy_settings_word_tokenizers,
        "spaCy's word tokenizers"
    )

    for lang_code, lemmatizers in settings_lemmatizers.items():
        if (
            lang_code != 'other'
            and any((
                lemmatizer.startswith('spacy_')
                for lemmatizer in lemmatizers
            ))
        ):
            langs_spacy_settings_lemmatizers.append(lang_code)

    check_missing_extra_langs(
        langs_spacy_supported_lemmatizers,
        langs_spacy_settings_lemmatizers,
        "spaCy's lemmatizers"
    )

    for lang_code, stop_word_lists in settings_stop_word_lists.items():
        if (
            lang_code != 'other'
            and any((
                stop_word_list.startswith('spacy_')
                for stop_word_list in stop_word_lists
            ))
        ):
            langs_spacy_settings_stop_word_lists.append(lang_code)

    check_missing_extra_langs(
        langs_spacy_supported_stop_word_lists,
        langs_spacy_settings_stop_word_lists,
        "spaCy's stop word lists"
    )

    # Stanza
    langs_stanza_supported_sentence_tokenizers = []
    langs_stanza_supported_word_tokenizers = []
    langs_stanza_supported_pos_taggers = []
    langs_stanza_supported_lemmatizers = []
    langs_stanza_supported_dependency_parsers = []
    langs_stanza_supported_sentiment_analyzers = []

    langs_stanza_settings_sentence_tokenizers = []
    langs_stanza_settings_word_tokenizers = []
    langs_stanza_settings_pos_taggers = []
    langs_stanza_settings_lemmatizers = []
    langs_stanza_settings_dependency_parsers = []
    langs_stanza_settings_sentiment_analyzers = []

    with open('requirements/requirements_tests.txt', 'r', encoding = 'utf_8') as f:
        for line in f:
            if line.startswith('stanza'):
                ver_stanza = line.split('==')[1].strip()
                # Replace minor version number with 0
                ver_stanza = re.sub(r'\.[0-9]$', '.0', ver_stanza)

                break

    r = requests.get(
        f'https://raw.githubusercontent.com/stanfordnlp/stanza-resources/main/resources_{ver_stanza}.json',
        timeout = wl_misc.REQUESTS_TIMEOUT
    )

    for lang, lang_resources in r.json().items():
        if lang != 'multilingual' and 'default_processors' in lang_resources:
            if 'tokenize' in lang_resources['default_processors']:
                langs_stanza_supported_sentence_tokenizers.append(lang)
                langs_stanza_supported_word_tokenizers.append(lang)

            if 'pos' in lang_resources['default_processors']:
                langs_stanza_supported_pos_taggers.append(lang)

            if (
                'lemma' in lang_resources['default_processors']
                and lang_resources['default_processors']['lemma'] != 'identity'
            ):
                langs_stanza_supported_lemmatizers.append(lang)

            if 'depparse' in lang_resources['default_processors']:
                langs_stanza_supported_dependency_parsers.append(lang)

            if 'sentiment' in lang_resources['default_processors']:
                langs_stanza_supported_sentiment_analyzers.append(lang)

    for i, langs in enumerate((
        langs_stanza_supported_sentence_tokenizers,
        langs_stanza_supported_word_tokenizers,
        langs_stanza_supported_pos_taggers,
        langs_stanza_supported_lemmatizers,
        langs_stanza_supported_dependency_parsers,
        langs_stanza_supported_sentiment_analyzers
    )):
        for i, lang in enumerate(langs):
            match lang:
                case 'zh-hans':
                    langs[i] = 'zh_cn'
                case 'zh-hant':
                    langs[i] = 'zh_tw'
                case 'sme':
                    langs[i] = 'se'
                case 'sr':
                    langs[i] = 'sr_latn'

        # Excluding code-switching languages : Arabic-French, Turkish-German
        for lang in ('qaf', 'qtd'):
            if lang in langs:
                langs.remove(lang)

    langs_stanza_supported_sentence_tokenizers.append('sr_cyrl')
    langs_stanza_supported_pos_taggers.append('sr_cyrl')
    langs_stanza_supported_dependency_parsers.append('sr_cyrl')

    langs_stanza_supported_sentence_tokenizers = add_lang_suffixes(langs_stanza_supported_sentence_tokenizers)
    langs_stanza_supported_word_tokenizers = add_lang_suffixes(langs_stanza_supported_word_tokenizers)
    langs_stanza_supported_pos_taggers = add_lang_suffixes(langs_stanza_supported_pos_taggers)
    langs_stanza_supported_lemmatizers = add_lang_suffixes(langs_stanza_supported_lemmatizers)
    langs_stanza_supported_dependency_parsers = add_lang_suffixes(langs_stanza_supported_dependency_parsers)
    langs_stanza_supported_sentiment_analyzers = add_lang_suffixes(langs_stanza_supported_sentiment_analyzers)

    for settings_lang_utils, langs, langs_supported, util_type in (
        (
            settings_sentence_tokenizers,
            langs_stanza_settings_sentence_tokenizers,
            langs_stanza_supported_sentence_tokenizers,
            'sentence tokenizer'
        ), (
            settings_word_tokenizers,
            langs_stanza_settings_word_tokenizers,
            langs_stanza_supported_word_tokenizers,
            'word tokenizer'
        ), (
            settings_pos_taggers,
            langs_stanza_settings_pos_taggers,
            langs_stanza_supported_pos_taggers,
            'POS tagger'
        ), (
            settings_lemmatizers,
            langs_stanza_settings_lemmatizers,
            langs_stanza_supported_lemmatizers,
            'lemmatizer'
        ), (
            settings_dependency_parsers,
            langs_stanza_settings_dependency_parsers,
            langs_stanza_supported_dependency_parsers,
            'dependency parser'
        ), (
            settings_sentiment_analyzers,
            langs_stanza_settings_sentiment_analyzers,
            langs_stanza_supported_sentiment_analyzers,
            'sentiment analyzer'
        )
    ):
        for lang_code, lang_utils in settings_lang_utils.items():
            if (
                lang_code != 'other'
                and any((
                    lang_util.startswith('stanza_')
                    for lang_util in lang_utils
                ))
            ):
                langs.append(lang_code)

        check_missing_extra_langs(langs_supported, langs, f"Stanza's {util_type}")

    for langs_stanza_settings, util_type in (
        (langs_stanza_settings_sentence_tokenizers, 'sentence_tokenizers'),
        (langs_stanza_settings_word_tokenizers, 'word_tokenizers'),
        (langs_stanza_settings_pos_taggers, 'pos_taggers'),
        (langs_stanza_settings_lemmatizers, 'lemmatizers'),
        (langs_stanza_settings_dependency_parsers, 'dependency_parsers'),
        (langs_stanza_settings_sentiment_analyzers, 'sentiment_analyzers'),
    ):
        if langs_stanza_settings in (
            langs_stanza_settings_sentence_tokenizers,
            langs_stanza_settings_word_tokenizers
        ):
            langs_stanza_settings = set(langs_stanza_settings) | {'other'}
        else:
            langs_stanza_settings = set(langs_stanza_settings)

        assert langs_stanza_settings == wl_nlp_utils.get_langs_stanza(main, util_type)

    # Check for missing and extra languages
    settings_langs = [lang[0] for lang in settings_global['langs'].values()]
    settings_langs_lang_utils = {
        *settings_sentence_tokenizers,
        *settings_word_tokenizers,
        *settings_syl_tokenizers,
        *settings_pos_taggers,
        *settings_lemmatizers,
        *settings_stop_word_lists,
        *settings_dependency_parsers,
        *settings_sentiment_analyzers
    }

    for lang in settings_langs_lang_utils:
        assert lang in settings_langs, f'Missing language: {lang}!'

    for lang in settings_langs:
        assert lang in settings_langs_lang_utils, f'Extra language: {lang}!'

    # Check for invalid language utils
    for settings_lang_utils, mapping_lang_utils, util_type in (
        (settings_sentence_tokenizers, 'sentence_tokenizers', 'sentence tokenizers'),
        (settings_word_tokenizers, 'word_tokenizers', 'word tokenizers'),
        (settings_syl_tokenizers, 'syl_tokenizers', 'syllable tokenizers'),
        (settings_pos_taggers, 'pos_taggers', 'POS taggers'),
        (settings_lemmatizers, 'lemmatizers', 'lemmatizers'),
        (settings_stop_word_lists, 'stop_word_lists', 'stop word lists'),
        (settings_dependency_parsers, 'dependency_parsers', 'dependency parsers'),
        (settings_sentiment_analyzers, 'sentiment_analyzers', 'sentiment analyzers')
    ):
        lang_utils_registered = main.settings_global['mapping_lang_utils'][mapping_lang_utils].values()

        for lang_utils in settings_lang_utils.values():
            for lang_util in lang_utils:
                assert lang_util in lang_utils_registered, f'Invalid {util_type}: {lang_util}!'

    # Check for missing and extra languages in default settings
    settings_global_default_util_types = (
        (settings_sentence_tokenizers, settings_sentence_tokenizers_default, 'sentence tokenizers'),
        (settings_word_tokenizers, settings_word_tokenizers_default, 'word tokenizers'),
        (settings_syl_tokenizers, settings_syl_tokenizers_default, 'syllable tokenizers'),
        (settings_pos_taggers, settings_pos_taggers_default, 'POS taggers'),
        (settings_lemmatizers, settings_lemmatizers_default, 'lemmatizers'),
        (settings_stop_word_lists, settings_stop_word_lists_default, 'stop word lists'),
        (settings_dependency_parsers, settings_dependency_parsers_default, 'dependency parsers'),
        (settings_sentiment_analyzers, settings_sentiment_analyzers_default, 'sentiment analyzers')
    )

    for langs, langs_default, util_type in settings_global_default_util_types:
        check_missing_extra_langs_default(langs, langs_default, util_type)

    # Check for invalid default values in default settings
    for lang_utils, lang_utils_default, util_type in settings_global_default_util_types:
        check_invalid_default_lang_utils(lang_utils, lang_utils_default, util_type)

    for lang, stop_word_list in settings_stop_word_lists_default.items():
        if settings_stop_word_lists[lang] != ('custom',):
            assert stop_word_list != 'custom', f'Invalid default stop word list: {lang} - {stop_word_list}!'
        else:
            assert stop_word_list == 'custom', f'Invalid default stop word list: {lang} - {stop_word_list}!'

    # Check language order
    for settings_global, settings_default, util_type in settings_global_default_util_types:
        check_lang_order(main, list(settings_global), util_type)

        # Default values for custom stop word lists are specified after the instantiation of default settings
        if util_type != 'stop word lists':
            check_lang_order(main, list(settings_default), f'default {util_type}')

if __name__ == '__main__':
    test_settings_global()
