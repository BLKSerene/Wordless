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

to_lang_text = {
    lang_code_639_3: lang_text
    for lang_text, (lang_code_639_3, _, _) in main.settings_global['langs'].items()
}
to_iso_639_1 = {
    lang_code_639_3: lang_code_639_1
    for _, (lang_code_639_3, lang_code_639_1, _) in main.settings_global['langs'].items()
}
to_iso_639_3 = {
    lang_code_639_1: lang_code_639_3
    for _, (lang_code_639_3, lang_code_639_1, _) in main.settings_global['langs'].items()
}

@pytest.mark.parametrize('lang_text', main.settings_global['langs'].keys())
def test_to_lang_code(lang_text):
    lang_code = wl_conversion.to_lang_code(main, lang_text)

    assert lang_code == main.settings_global['langs'][lang_text][0]

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
