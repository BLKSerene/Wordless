# ----------------------------------------------------------------------
# Wordless: Utilities - Conversion
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

def to_lang_code(main, lang_text):
    return main.settings_global['langs'][lang_text][0]

def to_lang_codes(main, lang_texts):
    return (main.settings_global['langs'][lang_text][0] for lang_text in lang_texts)

def _to_lang_text(main, lang_code):
    for lang_text, (lang_code_639_3, _, _) in main.settings_global['langs'].items():
        if lang_code_639_3 == lang_code:
            return lang_text

def to_lang_text(main, lang_code):
    return _to_lang_text(main, lang_code)

def to_lang_texts(main, lang_codes):
    return (_to_lang_text(main, lang_code) for lang_code in lang_codes)

def to_iso_639_3(main, lang_code):
    for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
        if lang_code_639_1 == lang_code:
            return lang_code_639_3

    # ISO 639-1 codes without country codes
    for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
        if lang_code_639_1.startswith(f'{lang_code}_'):
            return lang_code_639_3

def to_iso_639_1(main, lang_code):
    for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
        if lang_code_639_3 == lang_code:
            return lang_code_639_1

def remove_lang_code_suffixes(main, lang_code):
    if '_' in lang_code:
        return lang_code.split('_')[0]
    else:
        return lang_code

def get_lang_family(main, lang_code):
    for lang_code_639_3, _, lang_family in main.settings_global['langs'].values():
        if lang_code_639_3 == lang_code:
            return lang_family

def to_encoding_code(main, encoding_text):
    return main.settings_global['encodings'][encoding_text]

def to_encoding_text(main, encoding_code):
    for text, code in main.settings_global['encodings'].items():
        if encoding_code == code:
            return text
