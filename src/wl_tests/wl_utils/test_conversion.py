#
# Wordless: Tests - Utilities - Conversion
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init
from wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

@pytest.mark.parametrize('lang_text', main.settings_global['langs'])
def test_to_lang_code(lang_text):
    len_lang_text = max([len(lang_text)
                         for lang_text in main.settings_global['langs']])
    lang_code = wl_conversion.to_lang_code(main, lang_text)

    assert lang_code == main.settings_global['langs'][lang_text]

@pytest.mark.parametrize('lang_code', main.settings_global['langs'].values())
def test_to_lang_text(lang_code):
    len_lang_code = max([len(lang_code)
                         for lang_code in main.settings_global['langs'].values()])
    lang_text = wl_conversion.to_lang_text(main, lang_code)

    assert lang_text == {lang_code: lang_text
                         for lang_text, lang_code in main.settings_global['langs'].items()}[lang_code]

@pytest.mark.parametrize('lang_code', main.settings_global['lang_codes'])
def test_to_iso_639_1(lang_code):
    len_iso_639_3 = max([len(lang_code)
                         for lang_code in main.settings_global['lang_codes']])
    iso_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

    assert iso_639_1 == main.settings_global['lang_codes'][lang_code]

@pytest.mark.parametrize('lang_code', main.settings_global['lang_codes'].values())
def test_to_iso_639_3(lang_code):
    len_iso_639_1 = max([len(lang_code)
                         for lang_code in main.settings_global['lang_codes'].values()])
    iso_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

    assert iso_639_3 == {iso_639_1: iso_639_3
                         for iso_639_3, iso_639_1 in main.settings_global['lang_codes'].items()}[lang_code]

@pytest.mark.parametrize('text_type_text', main.settings_global['text_types'])
def test_to_text_type_code(text_type_text):
    len_text_type_text = max([len(text_type_text)
                              for text_type_text in main.settings_global['text_types']])
    text_type_code = wl_conversion.to_text_type_code(main, text_type_text)

    assert text_type_code == main.settings_global['text_types'][text_type_text]

@pytest.mark.parametrize('text_type_code', main.settings_global['text_types'].values())
def test_to_text_type_text(text_type_code):
    len_text_type_code = max([len(str(text_type_code))
                              for text_type_code in main.settings_global['text_types'].values()])
    text_type_text = wl_conversion.to_text_type_text(main, text_type_code)

    assert text_type_text == {text_type_code: text_type_text
                              for text_type_text, text_type_code in main.settings_global['text_types'].items()}[text_type_code]

@pytest.mark.parametrize('encoding_text', main.settings_global['file_encodings'])
def test_to_encoding_code(encoding_text):
    len_encoding_text = max([len(encoding_text)
                             for encoding_text in main.settings_global['file_encodings']])
    encoding_code = wl_conversion.to_encoding_code(main, encoding_text)

    assert encoding_code == main.settings_global['file_encodings'][encoding_text]

@pytest.mark.parametrize('encoding_code', main.settings_global['file_encodings'].values())
def test_to_encoding_text(encoding_code):
    len_encoding_code = max([len(encoding_code)
                             for encoding_code in main.settings_global['file_encodings'].values()])
    encoding_text = wl_conversion.to_encoding_text(main, encoding_code)

    assert encoding_text == {encoding_code: encoding_text
                             for encoding_text, encoding_code in main.settings_global['file_encodings'].items()}[encoding_code]
