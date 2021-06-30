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

import pkgutil
import sys

sys.path.append('.')

import pytest
import spacy

from wl_tests import wl_test_init
from wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

def test_settings_global():
    settings_global = main.settings_global
    settings_default = main.settings_default

    settings_sentence_tokenizers = settings_global['sentence_tokenizers']
    settings_sentence_tokenizers_default = settings_default['sentence_tokenization']['sentence_tokenizers']

    langs_sentence_tokenizers = list(settings_sentence_tokenizers.keys())
    langs_sentence_tokenizers_default = list(settings_sentence_tokenizers_default.keys())
    langs_sentence_tokenizers_spacy = []

    lang_missing = False
    lang_extra = False
    lang_default_missing = False
    lang_default_extra = False

    for lang in pkgutil.iter_modules(spacy.lang.__path__):
        if lang.ispkg and lang.name not in ['zh', 'sr', 'xx']:
            langs_sentence_tokenizers_spacy.append(lang.name)
            # Chinese
            langs_sentence_tokenizers_spacy.extend(['zh_cn', 'zh_tw'])
            # Serbian
            langs_sentence_tokenizers_spacy.extend(['sr_cyrl', 'sr_latn'])

    # Check for missing languages for spaCy's sentencizer
    for lang in langs_sentence_tokenizers_spacy:
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang)

        if lang_code_639_3 not in langs_sentence_tokenizers:
            print(f'''Missing language code "{lang} / {lang_code_639_3}" found for spaCy's sentencizer!''')

            lang_missing = True

    # Check for extra languages for spaCy's sentencizer
    for lang, sentence_tokenizers in settings_sentence_tokenizers.items():
        if lang != 'other' and any(['spaCy' in sentence_tokenizer for sentence_tokenizer in sentence_tokenizers]):
            lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang)

            if lang_code_639_1 not in langs_sentence_tokenizers_spacy:
                print(f'''Extra language code "{lang} / {lang_code_639_1}" found for spaCy's sentencizer!''')

                lang_extra = True

    # Check for missing and extra languages for the default settings of sentence tokenizers
    for lang, lang_default in zip(langs_sentence_tokenizers, langs_sentence_tokenizers_default):
        if lang not in langs_sentence_tokenizers_default:
            print(f'Missing language code "{lang}" found for the default settings of sentence tokenizers!')

            lang_default_missing = True

        if lang_default not in langs_sentence_tokenizers:
            print(f'Extra language code "{lang}" found for the default settings of sentence tokenizers!')

            lang_default_extra = True

    assert not lang_missing
    assert not lang_extra
    assert not lang_default_missing
    assert not lang_default_extra

if __name__ == '__main__':
    test_settings_global()
