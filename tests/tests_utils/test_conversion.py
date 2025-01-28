# ----------------------------------------------------------------------
# Tests: Utilities - Conversion
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

import pytest

from tests import wl_test_init
from wordless.wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

settings_langs = main.settings_global['langs']
settings_file_encodings = main.settings_global['encodings']

TO_LANG_TEXT = {
    lang_code_639_3: lang_text
    for lang_text, (lang_code_639_3, _) in settings_langs.items()
}
TO_ISO_639_1 = dict(settings_langs.values())
TO_ISO_639_3 = {
    lang_code_639_1: lang_code_639_3
    for lang_code_639_3, lang_code_639_1 in settings_langs.values()
}

def test_normalize_lang_code():
    for lang_code in settings_langs.values():
        assert wl_conversion.normalize_lang_code(lang_code[0].replace('_', '-').upper()) == lang_code[0]

def test_to_lang_code():
    for lang_text, lang_code in settings_langs.items():
        assert wl_conversion.to_lang_code(main, lang_text) == lang_code[0]
        assert wl_conversion.to_lang_code(main, lang_text, iso_639_3 = False) == lang_code[1]

def test_to_lang_codes():
    lang_codes_639_3 = wl_conversion.to_lang_codes(main, settings_langs.keys())
    lang_codes_639_1 = wl_conversion.to_lang_codes(main, settings_langs.keys(), iso_639_3 = False)

    assert list(lang_codes_639_3) == [lang_vals[0] for lang_vals in settings_langs.values()]
    assert list(lang_codes_639_1) == [lang_vals[1] for lang_vals in settings_langs.values()]

def test_to_lang_text():
    for lang_code in TO_LANG_TEXT.keys():
        lang_text = wl_conversion.to_lang_text(main, lang_code)

        assert lang_text == TO_LANG_TEXT[lang_code]

    with pytest.raises(Exception):
        wl_conversion.to_lang_text(main, 'test')

def test_to_lang_texts():
    lang_texts = wl_conversion.to_lang_texts(main, TO_LANG_TEXT.keys())

    assert list(lang_texts) == [TO_LANG_TEXT[lang_code] for lang_code in TO_LANG_TEXT.keys()]

def test_to_iso_639_3():
    for lang_code in TO_ISO_639_3.keys():
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        assert lang_code_639_3 == TO_ISO_639_3[lang_code]

    with pytest.raises(Exception):
        wl_conversion.to_iso_639_3(main, 'test')

def test_to_iso_639_1():
    for lang_code_639_3, lang_code_639_1 in TO_ISO_639_1.items():
        assert wl_conversion.to_iso_639_1(main, lang_code_639_3) == lang_code_639_1

def test_remove_lang_code_suffixes():
    for lang_code_639_3, lang_code_639_1 in TO_ISO_639_1.items():
        if lang_code_639_3.find('_') > -1:
            lang_code_639_3 = wl_conversion.remove_lang_code_suffixes(main, lang_code_639_3)

            assert lang_code_639_3.find('_') == -1

        if lang_code_639_1.find('_') > -1:
            lang_code_639_1 = wl_conversion.remove_lang_code_suffixes(main, lang_code_639_1)

            assert lang_code_639_1.find('_') == -1

def test_to_encoding_code():
    for encoding_text, encoding_code in settings_file_encodings.items():
        assert wl_conversion.to_encoding_code(main, encoding_text) == encoding_code

def test_to_encoding_text():
    for encoding_code in settings_file_encodings.values():
        encoding_text = wl_conversion.to_encoding_text(main, encoding_code)

        assert encoding_text == {
            encoding_code: encoding_text
            for encoding_text, encoding_code in settings_file_encodings.items()
        }[encoding_code]

    with pytest.raises(Exception):
        wl_conversion.to_encoding_text(main, 'test')

def test_to_yes_no_code():
    assert wl_conversion.to_yes_no_code('Yes') is True
    assert wl_conversion.to_yes_no_code('No') is False

    with pytest.raises(Exception):
        wl_conversion.to_yes_no_code('test')

def test_to_yes_no_text():
    assert wl_conversion.to_yes_no_text(True) == 'Yes'
    assert wl_conversion.to_yes_no_text(False) == 'No'

    with pytest.raises(Exception):
        wl_conversion.to_yes_no_text('test')

if __name__ == '__main__':
    test_normalize_lang_code()
    test_to_lang_code()
    test_to_lang_codes()
    test_to_lang_text()
    test_to_lang_texts()

    test_to_iso_639_3()
    test_to_iso_639_1()

    test_remove_lang_code_suffixes()

    test_to_encoding_code()
    test_to_encoding_text()

    test_to_yes_no_code()
    test_to_yes_no_text()
