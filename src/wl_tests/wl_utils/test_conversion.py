# ----------------------------------------------------------------------
# Wordless: Tests - Utilities - Conversion
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

def test_to_lang_code():
    for lang_text in settings_langs.keys():
        lang_code = wl_conversion.to_lang_code(main, lang_text)

        assert lang_code == settings_langs[lang_text][0]

def test_to_lang_text():
    for lang_code in to_lang_text.keys():
        lang_text = wl_conversion.to_lang_text(main, lang_code)

        assert lang_text == to_lang_text[lang_code]

def test_to_iso_639_1():
    for lang_code in to_iso_639_1.keys():
        lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

        assert lang_code_639_1 == to_iso_639_1[lang_code]

def test_to_iso_639_3():
    for lang_code in to_iso_639_3.keys():
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        assert lang_code_639_3 == to_iso_639_3[lang_code]

def test_remove_lang_code_suffixes():
    for lang_code_639_3, lang_code_639_1 in to_iso_639_1.items():
        if lang_code_639_3.find('_') > -1:
            lang_code_639_3 = wl_conversion.remove_lang_code_suffixes(main, lang_code_639_3)

            assert lang_code_639_3.find('_') == -1

        if lang_code_639_1.find('_') > -1:
            lang_code_639_1 = wl_conversion.remove_lang_code_suffixes(main, lang_code_639_1)

            assert lang_code_639_1.find('_') == -1

def test_get_lang_family():
    for lang_code in to_iso_639_1.keys():
        lang_family = wl_conversion.get_lang_family(main, lang_code)

        assert lang_family == get_lang_family[lang_code]

def test_to_encoding_code():
    for encoding_text in settings_file_encodings.keys():
        len_encoding_text = max([
            len(encoding_text)
            for encoding_text in settings_file_encodings
        ])
        encoding_code = wl_conversion.to_encoding_code(main, encoding_text)

        assert encoding_code == settings_file_encodings[encoding_text]

def test_to_encoding_text():
    for encoding_code in settings_file_encodings.values():
        len_encoding_code = max([
            len(encoding_code)
            for encoding_code in settings_file_encodings.values()
        ])
        encoding_text = wl_conversion.to_encoding_text(main, encoding_code)

        assert encoding_text == {
            encoding_code: encoding_text
            for encoding_text, encoding_code in settings_file_encodings.items()
        }[encoding_code]

if __name__ == '__main__':
    test_to_lang_code()
    test_to_lang_text()

    test_to_iso_639_1()
    test_to_iso_639_3()

    test_remove_lang_code_suffixes()
    test_get_lang_family()

    test_to_encoding_code()
    test_to_encoding_text()
