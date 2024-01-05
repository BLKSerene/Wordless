# ----------------------------------------------------------------------
# Wordless: Utilities - Conversion
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

from PyQt5.QtCore import QCoreApplication

_tr = QCoreApplication.translate

# Languages
def normalize_lang_code(lang_code):
    return lang_code.replace('-', '_').lower()

def to_lang_code(main, lang_text):
    return main.settings_global['langs'][lang_text][0]

def to_lang_codes(main, lang_texts):
    return (main.settings_global['langs'][lang_text][0] for lang_text in lang_texts)

def _to_lang_text(main, lang_code):
    lang_code = normalize_lang_code(lang_code)

    for lang_text, (lang_code_639_3, _, _) in main.settings_global['langs'].items():
        if lang_code_639_3 == lang_code:
            return lang_text

    return ''

def to_lang_text(main, lang_code):
    return _to_lang_text(main, lang_code)

def to_lang_texts(main, lang_codes):
    return (_to_lang_text(main, lang_code) for lang_code in lang_codes)

def to_iso_639_3(main, lang_code):
    lang_code = normalize_lang_code(lang_code)

    for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
        if lang_code_639_1 == lang_code:
            return lang_code_639_3

    # ISO 639-1 codes without country codes
    for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
        if lang_code_639_1.startswith(f'{lang_code}_'):
            return lang_code_639_3

    return ''

def to_iso_639_1(main, lang_code, no_suffix = False):
    lang_code = normalize_lang_code(lang_code)

    # Fuzzy matching without code suffixes
    if '_' in lang_code:
        for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
            if lang_code_639_3 == lang_code:
                lang_code_converted = lang_code_639_1
    else:
        for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
            if remove_lang_code_suffixes(main, lang_code_639_3) == remove_lang_code_suffixes(main, lang_code):
                lang_code_converted = lang_code_639_1

    if no_suffix:
        return remove_lang_code_suffixes(main, lang_code_converted)
    else:
        return lang_code_converted

def remove_lang_code_suffixes(main, lang_code): # pylint: disable=unused-argument
    lang_code = normalize_lang_code(lang_code)

    if '_' in lang_code:
        return lang_code.split('_')[0]
    else:
        return lang_code

def get_lang_family(main, lang_code):
    lang_code = normalize_lang_code(lang_code)

    for lang_code_639_3, _, lang_family in main.settings_global['langs'].values():
        if lang_code_639_3 == lang_code:
            return lang_family

    return ''

# Encodings
def to_encoding_code(main, encoding_text):
    return main.settings_global['encodings'][encoding_text]

def to_encoding_text(main, encoding_code):
    for text, code in main.settings_global['encodings'].items():
        if encoding_code == code:
            return text

    return ''

# Yes/No
def to_yes_no_code(yes_no_text):
    if yes_no_text == _tr('wl_conversion', 'Yes'):
        return True
    elif yes_no_text == _tr('wl_conversion', 'No'):
        return False
    else:
        return None

def to_yes_no_text(yes_no_code):
    if yes_no_code is True:
        return _tr('wl_conversion', 'Yes')
    elif yes_no_code is False:
        return _tr('wl_conversion', 'No')
    else:
        return None
