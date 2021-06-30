#
# Wordless: Tests - Settings - Global Settings
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import pkgutil
import sys

sys.path.append('.')

import pytest
import sacremoses
import spacy

from wl_tests import wl_test_init
from wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

def test_settings_global():
    settings_global = main.settings_global
    settings_default = main.settings_default

    settings_sentence_tokenizers = settings_global['sentence_tokenizers']
    settings_sentence_tokenizers_default = settings_default['sentence_tokenization']['sentence_tokenizers']
    settings_word_tokenizers = settings_global['word_tokenizers']
    settings_word_tokenizers_default = settings_default['word_tokenization']['word_tokenizers']

    langs_supported_sacremoses = []
    langs_supported_spacy = []
    langs_sentence_tokenizers = list(settings_sentence_tokenizers.keys())
    langs_sentence_tokenizers_default = list(settings_sentence_tokenizers_default.keys())
    langs_sentence_tokenizers_spacy = []
    langs_word_tokenizers = list(settings_word_tokenizers.keys())
    langs_word_tokenizers_default = list(settings_word_tokenizers_default.keys())
    langs_word_tokenizers_sacremoses = []
    langs_word_tokenizers_spacy = []

    lang_missing = False
    lang_extra = False
    lang_default_missing = False
    lang_default_extra = False

    # Loading languages supported by Sacremoses
    for file in os.listdir(os.path.split(sacremoses.__file__)[0] + '/data/nonbreaking_prefixes/'):
        file_ext = os.path.splitext(file)[1][1:]

        if file_ext not in ['yue', 'zh']:
            langs_supported_sacremoses.append(file_ext)

    # Loading languages supported by spaCy
    for lang in pkgutil.iter_modules(spacy.lang.__path__):
        if lang.ispkg and lang.name not in ['ja', 'ko', 'sr', 'th', 'vi', 'zh', 'xx']:
            langs_supported_spacy.append(lang.name)
            # Serbian
            langs_supported_spacy.extend(['sr_cyrl', 'sr_latn'])

    # Check for missing and extra languages for spaCy's sentencizer
    for lang_code, sentence_tokenizers in settings_sentence_tokenizers.items():
        if lang_code != 'other' and any(['spaCy' in sentence_tokenizer for sentence_tokenizer in sentence_tokenizers]):
            langs_sentence_tokenizers_spacy.append(lang_code)

    for lang_code in langs_supported_spacy:
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        if lang_code_639_3 not in langs_sentence_tokenizers_spacy:
            print(f'''Missing language code "{lang_code} / {lang_code_639_3}" found for spaCy's sentencizer!''')

            lang_missing = True

    for lang_code in langs_sentence_tokenizers_spacy:
        lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

        if lang_code_639_1 not in langs_supported_spacy:
            print(f'''Extra language code "{lang_code} / {lang_code_639_1}" found for spaCy's sentencizer!''')

            lang_extra = True

    # Check for missing and extra languages for the default settings of sentence tokenizers
    for lang_code in langs_sentence_tokenizers:
        if lang_code not in langs_sentence_tokenizers_default:
            print(f'Missing language code "{lang_code}" found for the default settings of sentence tokenizers!')

            lang_default_missing = True

    for lang_code_default in langs_sentence_tokenizers_default:
        if lang_code_default not in langs_sentence_tokenizers:
            print(f'Extra language code "{lang_code_default}" found for the default settings of sentence tokenizers!')

            lang_default_extra = True

    # Check for missing and extra languages for Sacremoses's Moses tokenizer
    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if lang_code != 'other' and any(['Sacremoses' in word_tokenizer for word_tokenizer in word_tokenizers]):
            langs_word_tokenizers_sacremoses.append(lang_code)

    for lang_code in langs_supported_sacremoses:
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        if lang_code_639_3 not in langs_word_tokenizers_sacremoses:
            print(f'''Missing language code "{lang_code} / {lang_code_639_3}" found for Sacremoses's Moses tokenizer!''')

            lang_missing = True

    for lang_code in langs_word_tokenizers_sacremoses:
        lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

        if lang_code_639_1 not in langs_supported_sacremoses:
            print(f'''Extra language code "{lang_code} / {lang_code_639_1}" found for Sacremoses's Moses tokenizer!''')

            lang_extra = True

    # Check for missing and extra languages for spaCy's word tokenizers
    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if lang_code != 'other' and any(['spaCy' in word_tokenizer for word_tokenizer in word_tokenizers]):
            langs_word_tokenizers_spacy.append(lang_code)

    for lang_code in langs_supported_spacy:
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        if lang_code_639_3 not in langs_word_tokenizers_spacy:
            print(f'''Missing language code "{lang_code} / {lang_code_639_3}" found for spaCy word tokenizers!''')

            lang_missing = True

    for lang_code in langs_word_tokenizers_spacy:
        lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

        if lang_code_639_1 not in langs_supported_spacy:
            print(f'''Extra language code "{lang_code} / {lang_code_639_1}" found for spaCy word tokenizers!''')

            lang_extra = True

    # Check for missing and extra languages for the default settings of word tokenizers
    for lang_code in langs_word_tokenizers:
        if lang_code not in langs_word_tokenizers_default:
            print(f'Missing language code "{lang_code}" found for the default settings of word tokenizers!')

            lang_default_missing = True

    for lang_code_default in langs_word_tokenizers_default:
        if lang_code_default not in langs_word_tokenizers:
            print(f'Extra language code "{lang_code_default}" found for the default settings of word tokenizers!')

            lang_default_extra = True

    assert not lang_missing
    assert not lang_extra
    assert not lang_default_missing
    assert not lang_default_extra

if __name__ == '__main__':
    test_settings_global()
