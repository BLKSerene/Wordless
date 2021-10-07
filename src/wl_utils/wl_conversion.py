#
# Wordless: Utilities - Conversion
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

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

def to_iso_639_1(main, lang_code):
    for lang_code_639_3, lang_code_639_1, _ in main.settings_global['langs'].values():
        if lang_code_639_3 == lang_code:
            return lang_code_639_1

def remove_lang_code_suffixes(main, lang_code):
    return lang_code.split('_')[0]

def get_lang_family(main, lang_code):
    for lang_code_639_3, _, lang_family in main.settings_global['langs'].values():
        if lang_code_639_3 == lang_code:
            return lang_family

def to_encoding_code(main, encoding_text):
    return main.settings_global['file_encodings'][encoding_text]

def to_encoding_text(main, encoding_code):
    for text, code in main.settings_global['file_encodings'].items():
        if encoding_code == code:
            return text
