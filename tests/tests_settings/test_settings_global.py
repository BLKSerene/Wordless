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
import requests
import sacremoses
import simplemma
import spacy
import spacy_lookups_data

from tests import wl_test_init
from wordless.wl_nlp import wl_nlp_utils
from wordless.wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

def add_lang_suffixes(lang_codes):
    lang_codes = sorted(set(lang_codes))

    for lang_code in lang_codes.copy():
        if lang_code == 'hye':
            lang_codes.append('hyw')

        if lang_code in ['zh', 'en', 'de', 'pt', 'pa', 'sr']:
            lang_codes.remove(lang_code)

            if lang_code == 'zh':
                lang_codes.extend(['zh_cn', 'zh_tw'])
            elif lang_code == 'en':
                lang_codes.extend(['en_gb', 'en_us'])
            elif lang_code == 'de':
                lang_codes.extend(['de_at', 'de_de', 'de_ch'])
            elif lang_code == 'pt':
                lang_codes.extend(['pt_br', 'pt_pt'])
            elif lang_code == 'pa':
                lang_codes.append('pa_guru')
            elif lang_code == 'sr':
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

class Check_Settings_Global:
    def __init__(self):
        self.lang_utils_missing = False
        self.lang_utils_extra = False
        self.langs_missing = False
        self.langs_extra = False
        self.invalid_lang_utils = False
        self.lang_default_missing = False
        self.lang_default_extra = False
        self.invalid_default_lang_util = False

    def check_missing_extra_langs(self, langs_supported, langs_global, msg):
        for lang_code in langs_supported:
            lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

            if lang_code_639_3 not in langs_global:
                print(f'''Missing language code "{lang_code_639_3}/{lang_code}" found for {msg}!''')

                self.lang_utils_missing = True

        for lang_code in langs_global:
            lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

            if lang_code_639_1 not in langs_supported:
                print(f'''Extra language code "{lang_code}/{lang_code_639_1}" found for {msg}!''')

                self.lang_utils_extra = True

    def check_missing_extra_langs_default(self, langs, langs_default, msg):
        for lang_code in langs:
            if lang_code not in langs_default:
                print(f'Missing language code "{lang_code}" found in the default settings of {msg}!')

                self.lang_default_missing = True

        for lang_code_default in langs_default:
            if lang_code_default not in langs:
                print(f'Extra language code "{lang_code_default}" found in the default settings of {msg}!')

                self.lang_default_extra = True

    def check_invalid_default_lang_utils(self, lang_utils, lang_utils_default, msg):
        for lang, lang_util in lang_utils_default.items():
            if lang_util not in lang_utils[lang]:
                print(f'Invalid default value "{lang_util}" for language "{lang}" found in the default settings of {msg}!')

                self.invalid_default_lang_util = True

    def check_settings_global(self):
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

        # Add custom lists
        for lang, stop_word_lists in settings_stop_word_lists.items():
            stop_word_lists.append('custom')

        # NLTK
        langs_nltk_sentence_tokenizers_supported = []
        langs_nltk_punkt_sentence_tokenizers = []
        langs_nltk_word_tokenizers = []

        for lang in os.listdir(nltk.data.find('tokenizers/punkt_tab/')):
            match lang:
                case 'english':
                    langs_nltk_sentence_tokenizers_supported.extend(['en_gb', 'en_us'])
                case 'german':
                    langs_nltk_sentence_tokenizers_supported.extend(['de_at', 'de_de', 'de_ch'])
                case 'greek':
                    langs_nltk_sentence_tokenizers_supported.append('el')
                case 'norwegian':
                    langs_nltk_sentence_tokenizers_supported.append('nb')
                case 'portuguese':
                    langs_nltk_sentence_tokenizers_supported.extend(['pt_br', 'pt_pt'])
                case 'README':
                    pass
                case _:
                    langs_nltk_sentence_tokenizers_supported.append(wl_conversion.to_lang_code(
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
                langs_nltk_punkt_sentence_tokenizers.append(lang_code)

        self.check_missing_extra_langs(
            langs_nltk_sentence_tokenizers_supported,
            langs_nltk_punkt_sentence_tokenizers,
            "NLTK's Punkt sentence tokenizer"
        )

        for lang_code, word_tokenizers in settings_word_tokenizers.items():
            if (
                lang_code != 'other'
                and any((
                    'nltk_nltk' in word_tokenizer
                    for word_tokenizer in word_tokenizers
                ))
            ):
                langs_nltk_word_tokenizers.append(lang_code)

        for lang_code in settings_word_tokenizers:
            if lang_code != 'other':
                # Exclude languages without spaces between words
                if lang_code not in [
                    'amh', 'mya', 'lzh', 'zho_cn', 'zho_tw',
                    'jpn', 'khm', 'lao', 'tha', 'bod',
                    'vie'
                ]:
                    if lang_code not in langs_nltk_word_tokenizers:
                        print(f'''Missing language code "{lang_code}" found for NLTK's tokenizers!''')

                        self.lang_utils_missing = True
                else:
                    if lang_code in langs_nltk_word_tokenizers:
                        print(f'''Extra language code "{lang_code}" found for NLTK's tokenizers!''')

                        self.lang_utils_extra = True

        # Sacremoses
        langs_sacremoses_supported = []
        langs_sacremoses_moses_tokenizer = []

        for file in os.listdir(os.path.split(sacremoses.__file__)[0] + '/data/nonbreaking_prefixes/'):
            file_ext = os.path.splitext(file)[1][1:]

            if file_ext not in ['yue', 'zh']:
                langs_sacremoses_supported.append(file_ext)

        langs_sacremoses_supported = add_lang_suffixes(langs_sacremoses_supported)

        for lang_code, word_tokenizers in settings_word_tokenizers.items():
            if (
                lang_code != 'other'
                and any((
                    'sacremoses' in word_tokenizer
                    for word_tokenizer in word_tokenizers
                ))
            ):
                langs_sacremoses_moses_tokenizer.append(lang_code)

        self.check_missing_extra_langs(
            langs_sacremoses_supported,
            langs_sacremoses_moses_tokenizer,
            "Sacremoses's Moses tokenizer"
        )

        # simplemma
        langs_simplemma_supported = []
        langs_simplemma_lemmatizers = []

        for lang in simplemma.strategies.dictionaries.dictionary_factory.SUPPORTED_LANGUAGES:

            if lang == 'hbs':
                langs_simplemma_supported.extend(['hr', 'sr_latn'])
            else:
                langs_simplemma_supported.append(lang)

        langs_simplemma_supported = add_lang_suffixes(langs_simplemma_supported)

        for lang_code, lemmatizers in settings_lemmatizers.items():
            if any((
                lemmatizer.startswith('simplemma_')
                for lemmatizer in lemmatizers
            )):
                langs_simplemma_lemmatizers.append(lang_code)

        self.check_missing_extra_langs(
            langs_simplemma_supported,
            langs_simplemma_lemmatizers,
            "simplemma's lemmatizers"
        )

        # spaCy
        langs_spacy_supported = []
        langs_spacy_supported_lemmatizers = []

        langs_spacy_word_tokenizers = []
        langs_spacy_lemmatizers = []

        for lang in pkgutil.iter_modules(spacy.lang.__path__):
            if lang.ispkg:
                # Serbian
                if lang.name == 'sr':
                    langs_spacy_supported.extend(['sr_cyrl', 'sr_latn'])
                elif lang.name not in ['th', 'vi', 'xx']:
                    langs_spacy_supported.append(lang.name)

        langs_spacy_supported = add_lang_suffixes(langs_spacy_supported)

        for file in os.listdir(f'{spacy_lookups_data.__path__[0]}/data/'):
            if 'lemma' in file:
                lang_code = re.search(r'^([a-z]{2,3})_', file).groups()[0]

                langs_spacy_supported_lemmatizers.append(lang_code)

        # Languages without data files for lemmatizers
        langs_spacy_supported_lemmatizers.extend(['fi', 'ja', 'ko', 'sl', 'uk'])
        langs_spacy_supported_lemmatizers = add_lang_suffixes(langs_spacy_supported_lemmatizers)

        for lang_code, sentence_tokenizers in settings_sentence_tokenizers.items():
            if (
                lang_code not in ['khm', 'tha', 'bod', 'vie']
                and not any((
                    sentence_tokenizer.startswith('spacy_')
                    for sentence_tokenizer in sentence_tokenizers
                ))
            ):
                lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

                print(f'''Missing language code "{lang_code}/{lang_code_639_1}" found for spaCy's sentence recognizers or sentencizer!''')

                self.lang_utils_missing = True

        for lang_code, word_tokenizers in settings_word_tokenizers.items():
            if (
                lang_code != 'other'
                and any((
                    'spacy' in word_tokenizer
                    for word_tokenizer in word_tokenizers
                ))
            ):
                langs_spacy_word_tokenizers.append(lang_code)

        self.check_missing_extra_langs(langs_spacy_supported, langs_spacy_word_tokenizers, "spaCy's word tokenizers")

        for lang_code, lemmatizers in settings_lemmatizers.items():
            if (
                lang_code != 'other'
                and any((
                    'spacy' in lemmatizer
                    for lemmatizer in lemmatizers
                ))
            ):
                langs_spacy_lemmatizers.append(lang_code)

        self.check_missing_extra_langs(langs_spacy_supported_lemmatizers, langs_spacy_lemmatizers, "spaCy's lemmatizers")

        # Stanza
        langs_stanza_supported_tokenizers = []
        langs_stanza_supported_pos_taggers = []
        langs_stanza_supported_lemmatizers = []
        langs_stanza_supported_dependency_parsers = []
        langs_stanza_supported_sentiment_analyzers = []

        langs_stanza_sentence_tokenizers = []
        langs_stanza_word_tokenizers = []
        langs_stanza_pos_taggers = []
        langs_stanza_lemmatizers = []
        langs_stanza_dependency_parsers = []
        langs_stanza_sentiment_analyzers = []

        with open('requirements/requirements_tests.txt', 'r', encoding = 'utf_8') as f:
            for line in f:
                if line.startswith('stanza'):
                    ver_stanza = line.split('==')[1].strip()
                    # Replace minor version number with 0
                    ver_stanza = re.sub(r'\.[0-9]$', '.0', ver_stanza)

                    break

        r = requests.get(
            f'https://raw.githubusercontent.com/stanfordnlp/stanza-resources/main/resources_{ver_stanza}.json',
            timeout = 10
        )

        for lang, lang_resources in r.json().items():
            if lang != 'multilingual' and 'default_processors' in lang_resources:
                if 'tokenize' in lang_resources['default_processors']:
                    langs_stanza_supported_tokenizers.append(lang)

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

        for i, langs in enumerate([
            langs_stanza_supported_tokenizers,
            langs_stanza_supported_pos_taggers,
            langs_stanza_supported_lemmatizers,
            langs_stanza_supported_dependency_parsers,
            langs_stanza_supported_sentiment_analyzers
        ]):
            for i, lang in enumerate(langs):
                if lang == 'zh-hans':
                    langs[i] = 'zh_cn'
                elif lang == 'zh-hant':
                    langs[i] = 'zh_tw'
                elif lang == 'sme':
                    langs[i] = 'se'
                elif lang == 'sr':
                    langs[i] = 'sr_latn'

            # Excluding code-switching languages : Arabic-French, Turkish-German
            if 'qaf' in langs:
                langs.remove('qaf')
            if 'qtd' in langs:
                langs.remove('qtd')

        langs_stanza_supported_tokenizers = add_lang_suffixes(langs_stanza_supported_tokenizers)
        langs_stanza_supported_pos_taggers = add_lang_suffixes(langs_stanza_supported_pos_taggers)
        langs_stanza_supported_lemmatizers = add_lang_suffixes(langs_stanza_supported_lemmatizers)
        langs_stanza_supported_dependency_parsers = add_lang_suffixes(langs_stanza_supported_dependency_parsers)
        langs_stanza_supported_sentiment_analyzers = add_lang_suffixes(langs_stanza_supported_sentiment_analyzers)

        for settings_lang_utils, langs, langs_supported, msg_lang_util in [
            (settings_sentence_tokenizers, langs_stanza_sentence_tokenizers, langs_stanza_supported_tokenizers, 'sentence tokenizer'),
            (settings_word_tokenizers, langs_stanza_word_tokenizers, langs_stanza_supported_tokenizers, 'word tokenizer'),
            (settings_pos_taggers, langs_stanza_pos_taggers, langs_stanza_supported_pos_taggers, 'POS tagger'),
            (settings_lemmatizers, langs_stanza_lemmatizers, langs_stanza_supported_lemmatizers, 'lemmatizer'),
            (settings_dependency_parsers, langs_stanza_dependency_parsers, langs_stanza_supported_dependency_parsers, 'dependency parser'),
            (settings_sentiment_analyzers, langs_stanza_sentiment_analyzers, langs_stanza_supported_sentiment_analyzers, 'sentiment analyzer')
        ]:
            for lang_code, lang_utils in settings_lang_utils.items():
                if (
                    lang_code != 'other'
                    and any((
                        'stanza' in lang_util
                        for lang_util in lang_utils
                    ))
                ):
                    langs.append(lang_code)

            self.check_missing_extra_langs(langs_supported, langs, f"Stanza's {msg_lang_util}")

        assert set(langs_stanza_sentence_tokenizers) | {'other'} == wl_nlp_utils.get_langs_stanza(main, util_type = 'sentence_tokenizers')
        assert set(langs_stanza_word_tokenizers) | {'other'} == wl_nlp_utils.get_langs_stanza(main, util_type = 'word_tokenizers')
        assert set(langs_stanza_pos_taggers) == wl_nlp_utils.get_langs_stanza(main, util_type = 'pos_taggers')
        assert set(langs_stanza_lemmatizers) == wl_nlp_utils.get_langs_stanza(main, util_type = 'lemmatizers')
        assert set(langs_stanza_dependency_parsers) == wl_nlp_utils.get_langs_stanza(main, util_type = 'dependency_parsers')
        assert set(langs_stanza_sentiment_analyzers) == wl_nlp_utils.get_langs_stanza(main, util_type = 'sentiment_analyzers')

        # Check for missing and extra languages
        settings_langs = [lang[0] for lang in settings_global['langs'].values()]
        settings_langs_lang_utils = set([
            *settings_sentence_tokenizers,
            *settings_word_tokenizers,
            *settings_syl_tokenizers,
            *settings_pos_taggers,
            *settings_lemmatizers,
            *settings_stop_word_lists,
            *settings_dependency_parsers,
            *settings_sentiment_analyzers
        ])

        for lang in settings_langs_lang_utils:
            if lang not in settings_langs:
                print(f'Found missing language: {lang}!')

                self.langs_missing = True

        for lang in settings_langs:
            if lang not in settings_langs_lang_utils:
                print(f'Found extra language: {lang}!')

                self.langs_extra = True

        # Check for invalid language utils
        for settings_lang_utils, mapping_lang_utils, msg in [
            [settings_sentence_tokenizers, 'sentence_tokenizers', 'sentence tokenizers'],
            [settings_word_tokenizers, 'word_tokenizers', 'word tokenizers'],
            [settings_syl_tokenizers, 'syl_tokenizers', 'syllable tokenizers'],
            [settings_pos_taggers, 'pos_taggers', 'POS taggers'],
            [settings_lemmatizers, 'lemmatizers', 'lemmatizers'],
            [settings_stop_word_lists, 'stop_word_lists', 'stop word lists'],
            [settings_dependency_parsers, 'dependency_parsers', 'dependency parsers'],
            [settings_sentiment_analyzers, 'sentiment_analyzers', 'sentiment analyzers']
        ]:
            lang_utils_registered = main.settings_global['mapping_lang_utils'][mapping_lang_utils].values()

            for lang_utils in settings_lang_utils.values():
                for lang_util in lang_utils:
                    if lang_util not in lang_utils_registered:
                        print(f'Found invalid {msg}: {lang_util}!')

                        self.invalid_lang_utils = True

        # Check for missing and extra languages in default settings
        for langs, langs_default, msg in [
            [settings_sentence_tokenizers, settings_sentence_tokenizers_default, 'sentence tokenizers'],
            [settings_word_tokenizers, settings_word_tokenizers_default, 'word tokenizers'],
            [settings_syl_tokenizers, settings_syl_tokenizers_default, 'syllable tokenizers'],
            [settings_pos_taggers, settings_pos_taggers_default, 'POS taggers'],
            [settings_lemmatizers, settings_lemmatizers_default, 'lemmatizers'],
            [settings_stop_word_lists, settings_stop_word_lists_default, 'stop word lists'],
            [settings_dependency_parsers, settings_dependency_parsers_default, 'dependency parsers'],
            [settings_sentiment_analyzers, settings_sentiment_analyzers_default, 'sentiment analyzers']
        ]:
            self.check_missing_extra_langs_default(langs, langs_default, msg)

        # Check for invalid default values in default settings
        for lang_utils, lang_utils_default, msg in [
            [settings_sentence_tokenizers, settings_sentence_tokenizers_default, 'sentence tokenizers'],
            [settings_word_tokenizers, settings_word_tokenizers_default, 'word tokenizers'],
            [settings_syl_tokenizers, settings_syl_tokenizers_default, 'syllable tokenizers'],
            [settings_pos_taggers, settings_pos_taggers_default, 'POS taggers'],
            [settings_lemmatizers, settings_lemmatizers_default, 'lemmatizers'],
            [settings_stop_word_lists, settings_stop_word_lists_default, 'stop word lists'],
            [settings_dependency_parsers, settings_dependency_parsers_default, 'dependency parsers'],
            [settings_sentiment_analyzers, settings_sentiment_analyzers_default, 'sentiment analyzers']
        ]:
            self.check_invalid_default_lang_utils(lang_utils, lang_utils_default, msg)

def test_settings_global():
    check_settings_global = Check_Settings_Global()
    check_settings_global.check_settings_global()

    assert not check_settings_global.lang_utils_missing
    assert not check_settings_global.lang_utils_extra
    assert not check_settings_global.langs_missing
    assert not check_settings_global.langs_extra
    assert not check_settings_global.invalid_lang_utils
    assert not check_settings_global.lang_default_missing
    assert not check_settings_global.lang_default_extra

if __name__ == '__main__':
    test_settings_global()
