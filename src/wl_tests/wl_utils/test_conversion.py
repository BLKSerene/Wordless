#
# Wordless: Tests - Utilities - Conversion
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
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

settings_langs = main.settings_global['langs']
settings_file_encodings = main.settings_global['file_encodings']

to_lang_text = {
    lang_code_639_3: lang_text
    for lang_text, (lang_code_639_3, _, _) in settings_langs.items()
}
to_iso_639_1 = {
    lang_code_639_3: lang_code_639_1
    for lang_code_639_3, lang_code_639_1, _ in settings_langs.values()
}
to_iso_639_3 = {
    lang_code_639_1: lang_code_639_3
    for lang_code_639_3, lang_code_639_1, _ in settings_langs.values()
}
get_lang_family = {
    lang_code_639_3: lang_family
    for lang_code_639_3, _, lang_family in settings_langs.values()
}

@pytest.mark.parametrize('lang_text', settings_langs.keys())
def test_to_lang_code(lang_text):
    lang_code = wl_conversion.to_lang_code(main, lang_text)

    assert lang_code == settings_langs[lang_text][0]

@pytest.mark.parametrize('lang_code', to_lang_text.keys())
def test_to_lang_text(lang_code):
    lang_text = wl_conversion.to_lang_text(main, lang_code)

    assert lang_text == to_lang_text[lang_code]

@pytest.mark.parametrize('lang_code', to_iso_639_1.keys())
def test_to_iso_639_1(lang_code):
    lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

    assert lang_code_639_1 == to_iso_639_1[lang_code]

@pytest.mark.parametrize('lang_code', to_iso_639_3.keys())
def test_to_iso_639_3(lang_code):
    lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

    assert lang_code_639_3 == to_iso_639_3[lang_code]

@pytest.mark.parametrize('lang_code', to_iso_639_1.keys())
def test_get_lang_family(lang_code):
    lang_family = wl_conversion.get_lang_family(main, lang_code)

    assert lang_family == get_lang_family[lang_code]

@pytest.mark.parametrize('encoding_text', settings_file_encodings)
def test_to_encoding_code(encoding_text):
    len_encoding_text = max([len(encoding_text)
                             for encoding_text in settings_file_encodings])
    encoding_code = wl_conversion.to_encoding_code(main, encoding_text)

    assert encoding_code == settings_file_encodings[encoding_text]

@pytest.mark.parametrize('encoding_code', settings_file_encodings.values())
def test_to_encoding_text(encoding_code):
    len_encoding_code = max([len(encoding_code)
                             for encoding_code in settings_file_encodings.values()])
    encoding_text = wl_conversion.to_encoding_text(main, encoding_code)

    assert encoding_text == {encoding_code: encoding_text
                             for encoding_text, encoding_code in settings_file_encodings.items()}[encoding_code]
