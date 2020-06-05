#
# Wordless: Utilities - Conversion
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

def to_lang_code(main, lang_text):
    if type(lang_text) == list:
        return [main.settings_global['langs'][item] for item in lang_text]
    else:
        return main.settings_global['langs'][lang_text]

def to_lang_text(main, lang_code):
    langs = {lang_code: lang_text for lang_text, lang_code in main.settings_global['langs'].items()}

    if type(lang_code) == list:
        return [langs[item] for item in lang_code]
    else:
        return langs[lang_code]

def to_iso_639_3(main, lang_code):
    for lang_code_639_3, lang_code_639_1 in main.settings_global['lang_codes'].items():
        if lang_code == lang_code_639_1:
            return lang_code_639_3

def to_iso_639_1(main, lang_code):
    return main.settings_global['lang_codes'][lang_code]

def to_text_type_code(main, text_type_text):
    return main.settings_global['text_types'][text_type_text]

def to_text_type_text(main, text_type_code):
    for text, code in main.settings_global['text_types'].items():
        if text_type_code == code:
            return text

def to_encoding_code(main, encoding_text):
    return main.settings_global['file_encodings'][encoding_text]

def to_encoding_text(main, encoding_code):
    for text, code in main.settings_global['file_encodings'].items():
        if encoding_code == code:
            return text
