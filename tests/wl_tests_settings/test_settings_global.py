# ----------------------------------------------------------------------
# Wordless: Tests - Settings - Global Settings
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

import os
import pkgutil
import re

import sacremoses
import spacy
import spacy_lookups_data

from tests import wl_test_init
from wordless.wl_settings import wl_settings_global
from wordless.wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

def add_lang_suffixes(lang_codes):
    lang_codes = sorted(set(lang_codes))

    for lang_code in lang_codes.copy():
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

    return sorted(lang_codes)

class Check_Settings_Global():
    def __init__(self):
        self.lang_missing = False
        self.lang_extra = False
        self.lang_default_missing = False
        self.lang_default_extra = False
        self.invalid_default_lang_util = False

    def check_missing_extra_langs(self, langs_supported, langs_global, msg):
        for lang_code in langs_supported:
            lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

            if lang_code_639_3 not in langs_global:
                print(f'''Missing language code "{lang_code_639_3}/{lang_code}" found for {msg}!''')

                self.lang_missing = True

        for lang_code in langs_global:
            lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

            if lang_code_639_1 not in langs_supported:
                print(f'''Extra language code "{lang_code}/{lang_code_639_1}" found for {msg}!''')

                self.lang_extra = True

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
        settings_tagsets_default = settings_default['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger']

        settings_lemmatizers = settings_global['lemmatizers']
        settings_lemmatizers_default = settings_default['lemmatization']['lemmatizer_settings']

        settings_stop_word_lists = settings_global['stop_word_lists']
        settings_stop_word_lists_default = settings_default['stop_word_lists']['stop_word_list_settings']

        # Add custom lists
        for lang, stop_word_lists in settings_stop_word_lists.items():
            stop_word_lists.append('custom')

        langs_supported_sacremoses = []
        langs_supported_spacy = []
        langs_supported_spacy_lemmatizers = []
        langs_supported_spacy_stop_words = []

        langs_sentence_tokenizers = list(settings_sentence_tokenizers)
        langs_sentence_tokenizers_default = list(settings_sentence_tokenizers_default)

        langs_word_tokenizers = list(settings_word_tokenizers)
        langs_word_tokenizers_default = list(settings_word_tokenizers_default)
        langs_word_tokenizers_nltk = []
        langs_word_tokenizers_sacremoses = []
        langs_word_tokenizers_spacy = []

        langs_syl_tokenizers = list(settings_syl_tokenizers)
        langs_syl_tokenizers_default = list(settings_syl_tokenizers_default)

        langs_pos_taggers = list(settings_pos_taggers)
        langs_pos_taggers_default = list(settings_pos_taggers_default)
        langs_tagsets_default = list(settings_tagsets_default)

        langs_lemmatizers = list(settings_lemmatizers)
        langs_lemmatizers_default = list(settings_lemmatizers_default)
        langs_lemmatizers_spacy = []

        langs_stop_word_lists = list(settings_stop_word_lists)
        langs_stop_word_lists_default = list(settings_stop_word_lists_default)
        langs_stop_word_lists_spacy = []

        # Loading languages supported by Sacremoses
        for file in os.listdir(os.path.split(sacremoses.__file__)[0] + '/data/nonbreaking_prefixes/'):
            file_ext = os.path.splitext(file)[1][1:]

            if file_ext not in ['yue', 'zh']:
                langs_supported_sacremoses.append(file_ext)

        langs_supported_sacremoses = add_lang_suffixes(langs_supported_sacremoses)

        # Loading languages supported by spaCy
        for lang in pkgutil.iter_modules(spacy.lang.__path__):
            if lang.ispkg:
                if lang.name not in ['ko', 'sr', 'th', 'vi', 'xx']:
                    langs_supported_spacy.append(lang.name)
                # Serbian
                elif lang.name == 'sr':
                    langs_supported_spacy.extend(['sr_cyrl', 'sr_latn'])

        langs_supported_spacy = add_lang_suffixes(langs_supported_spacy)

        # Lemmatizers
        for file in os.listdir(f'{spacy_lookups_data.__path__[0]}/data/'):
            if 'lemma' in file:
                lang_code = re.search(r'^([a-z]{2,3})_', file).groups()[0]

                langs_supported_spacy_lemmatizers.append(lang_code)

        # Languages without data files
        langs_supported_spacy_lemmatizers.extend(['fi', 'ja', 'uk'])
        langs_supported_spacy_lemmatizers = add_lang_suffixes(langs_supported_spacy_lemmatizers)

        # Stop word lists
        for lang in pkgutil.iter_modules(spacy.lang.__path__):
            if lang.ispkg:
                for file in os.listdir(f'{spacy.lang.__path__[0]}/{lang.name}/'):
                    if file == 'stop_words.py':
                        if lang.name not in ['sr', 'xx']:
                            langs_supported_spacy_stop_words.append(lang.name)
                        elif lang.name == 'sr':
                            langs_supported_spacy_stop_words.extend(['sr_cyrl', 'sr_latn'])

                        break

        langs_supported_spacy_stop_words = add_lang_suffixes(langs_supported_spacy_stop_words)

        # Check for missing and extra languages for spaCy's sentence recognizer / sentencizer
        for lang_code, sentence_tokenizers in settings_sentence_tokenizers.items():
            if (
                lang_code not in ['tha', 'bod', 'vie']
                and not any((sentence_tokenizer.startswith('spacy_') for sentence_tokenizer in sentence_tokenizers))
            ):
                lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

                print(f'''Missing language code "{lang_code}/{lang_code_639_1}" found for spaCy's sentence recognizer / sentencizer!''')

                self.lang_missing = True

        # Check for missing and extra languages for NLTK's word tokenizers
        for lang_code, word_tokenizers in settings_word_tokenizers.items():
            if lang_code != 'other' and any(('nltk_nltk' in word_tokenizer for word_tokenizer in word_tokenizers)):
                langs_word_tokenizers_nltk.append(lang_code)

        for lang_code in langs_word_tokenizers:
            if lang_code != 'other':
                lang_family = wl_conversion.get_lang_family(main, lang_code)

                if lang_family == 'Indo-European':
                    if lang_code not in langs_word_tokenizers_nltk:
                        print(f'''Missing language code "{lang_code}" found for NLTK's tokenizers!''')

                        self.lang_missing = True
                else:
                    if lang_code in langs_word_tokenizers_nltk:
                        print(f'''Extra language code "{lang_code}" found for NLTK's tokenizers!''')

                        self.lang_extra = True

        # Check for missing and extra languages for Sacremoses's Moses tokenizer
        for lang_code, word_tokenizers in settings_word_tokenizers.items():
            if lang_code != 'other' and any(('sacremoses' in word_tokenizer for word_tokenizer in word_tokenizers)):
                langs_word_tokenizers_sacremoses.append(lang_code)

        self.check_missing_extra_langs(langs_supported_sacremoses, langs_word_tokenizers_sacremoses, "Sacremoses's Moses tokenizer")

        # Check for missing and extra languages for spaCy's word tokenizers
        for lang_code, word_tokenizers in settings_word_tokenizers.items():
            if lang_code != 'other' and any(('spacy' in word_tokenizer for word_tokenizer in word_tokenizers)):
                langs_word_tokenizers_spacy.append(lang_code)

        self.check_missing_extra_langs(langs_supported_spacy, langs_word_tokenizers_spacy, "spaCy's word tokenizers")

        # Check for missing and extra languages for spaCy's lemmatizers
        for lang_code, lemmatizers in settings_lemmatizers.items():
            if lang_code != 'other' and any(('spacy' in lemmatizer for lemmatizer in lemmatizers)):
                langs_lemmatizers_spacy.append(lang_code)

        self.check_missing_extra_langs(langs_supported_spacy_lemmatizers, langs_lemmatizers_spacy, "spaCy's lemmatizers")

        # Check for missing and extra languages for spaCy's stop word lists
        for lang_code, stop_word_lists in settings_stop_word_lists.items():
            if lang_code != 'other' and any(('spacy' in stop_word_list for stop_word_list in stop_word_lists)):
                langs_stop_word_lists_spacy.append(lang_code)

        self.check_missing_extra_langs(langs_supported_spacy_stop_words, langs_stop_word_lists_spacy, "spaCy's stop word lists")

        # Check for missing and extra languages in default settings
        self.check_missing_extra_langs_default(langs_sentence_tokenizers, langs_sentence_tokenizers_default, 'sentence tokenizers')
        self.check_missing_extra_langs_default(langs_word_tokenizers, langs_word_tokenizers_default, 'word tokenizers')
        self.check_missing_extra_langs_default(langs_syl_tokenizers, langs_syl_tokenizers_default, 'syllable tokenizers')
        self.check_missing_extra_langs_default(langs_pos_taggers, langs_pos_taggers_default, 'pos_taggers')
        self.check_missing_extra_langs_default(langs_pos_taggers, langs_tagsets_default, 'tagsets')
        self.check_missing_extra_langs_default(langs_lemmatizers, langs_lemmatizers_default, 'lemmatizers')
        self.check_missing_extra_langs_default(langs_stop_word_lists, langs_stop_word_lists_default, 'stop word lists')

        # Check for invalid default values in default settings
        self.check_invalid_default_lang_utils(settings_sentence_tokenizers, settings_sentence_tokenizers_default, 'sentence_tokenizers')
        self.check_invalid_default_lang_utils(settings_word_tokenizers, settings_word_tokenizers_default, 'word tokenizers')
        self.check_invalid_default_lang_utils(settings_syl_tokenizers, settings_syl_tokenizers_default, 'syllable tokenizers')
        self.check_invalid_default_lang_utils(settings_pos_taggers, settings_pos_taggers_default, 'pos_taggers')
        self.check_invalid_default_lang_utils(settings_pos_taggers, settings_tagsets_default, 'tagsets')
        self.check_invalid_default_lang_utils(settings_lemmatizers, settings_lemmatizers_default, 'lemmatizers')
        self.check_invalid_default_lang_utils(settings_stop_word_lists, settings_stop_word_lists_default, 'stop word lists')

def test_settings_global():
    assert wl_settings_global.init_settings_global()

    check_settings_global = Check_Settings_Global()
    check_settings_global.check_settings_global()

    assert not check_settings_global.lang_missing
    assert not check_settings_global.lang_extra
    assert not check_settings_global.lang_default_missing
    assert not check_settings_global.lang_default_extra

if __name__ == '__main__':
    test_settings_global()
