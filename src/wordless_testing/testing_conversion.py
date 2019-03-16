#
# Wordless: Testing - Conversion
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import sys

sys.path.append('.')

from wordless_testing import testing_init
from wordless_utils import wordless_conversion

main = testing_init.Testing_Main()

def testing_to_lang_code(lang_text):
    len_lang_text = max([len(lang_text)
                         for lang_text in main.settings_global['langs']])
    lang_code = wordless_conversion.to_lang_code(main, lang_text)

    print(f'{lang_text:{len_lang_text}} -> {lang_code}')

    assert lang_code == main.settings_global['langs'][lang_text]

def testing_to_lang_text(lang_code):
    len_lang_code = max([len(lang_code)
                         for lang_code in main.settings_global['langs'].values()])
    lang_text = wordless_conversion.to_lang_text(main, lang_code)

    print(f'{lang_code:{len_lang_code}} -> {lang_text}')

    assert lang_text == {lang_code: lang_text
                         for lang_text, lang_code in main.settings_global['langs'].items()}[lang_code]

def testing_to_iso_639_1(lang_code):
    len_iso_639_3 = max([len(lang_code)
                         for lang_code in main.settings_global['lang_codes']])
    iso_639_1 = wordless_conversion.to_iso_639_1(main, lang_code)

    print(f'{lang_code:{len_iso_639_3}} -> {iso_639_1}')

    assert iso_639_1 == main.settings_global['lang_codes'][lang_code]

def testing_to_iso_639_3(lang_code):
    len_iso_639_1 = max([len(lang_code)
                         for lang_code in main.settings_global['lang_codes'].values()])
    iso_639_3 = wordless_conversion.to_iso_639_3(main, lang_code)

    print(f'{lang_code:{len_iso_639_1}} -> {iso_639_3}')

    assert iso_639_3 == {iso_639_1: iso_639_3
                         for iso_639_3, iso_639_1 in main.settings_global['lang_codes'].items()}[lang_code]

def testing_to_text_type_code(text_type_text):
    len_text_type_text = max([len(text_type_text)
                              for text_type_text in main.settings_global['text_types']])
    text_type_code = wordless_conversion.to_text_type_code(main, text_type_text)

    print(f'{text_type_text:{len_text_type_text}} -> {text_type_code}')

    assert text_type_code == main.settings_global['text_types'][text_type_text]

def testing_to_text_type_text(text_type_code):
    len_text_type_code = max([len(str(text_type_code))
                              for text_type_code in main.settings_global['text_types'].values()])
    text_type_text = wordless_conversion.to_text_type_text(main, text_type_code)

    print(f'{str(text_type_code):{len_text_type_code}} -> {text_type_text}')

    assert text_type_text == {text_type_code: text_type_text
                              for text_type_text, text_type_code in main.settings_global['text_types'].items()}[text_type_code]

def testing_to_encoding_code(encoding_text):
    len_encoding_text = max([len(encoding_text)
                             for encoding_text in main.settings_global['file_encodings']])
    encoding_code = wordless_conversion.to_encoding_code(main, encoding_text)

    print(f'{encoding_text:{len_encoding_text}} -> {encoding_code}')

    assert encoding_code == main.settings_global['file_encodings'][encoding_text]

def testing_to_encoding_text(encoding_code):
    len_encoding_code = max([len(encoding_code)
                             for encoding_code in main.settings_global['file_encodings'].values()])
    encoding_text = wordless_conversion.to_encoding_text(main, encoding_code)

    print(f'{encoding_code:{len_encoding_code}} -> {encoding_text}')

    assert encoding_text == {encoding_code: encoding_text
                             for encoding_text, encoding_code in main.settings_global['file_encodings'].items()}[encoding_code]

print('---------- Language Text -> Language Code ----------')

for lang_text in main.settings_global['langs']:
    testing_to_lang_code(lang_text)

print('---------- Language Code -> Language Text ----------')

for lang_code in main.settings_global['langs'].values():
    testing_to_lang_text(lang_code)

print('---------- ISO 639-3 Code -> ISO 639-1 Code ----------')

for lang_iso_639_3 in main.settings_global['lang_codes']:
    testing_to_iso_639_1(lang_iso_639_3)

print('---------- ISO 639-1 Code -> ISO 639-3 Code ----------')

for lang_iso_639_1 in main.settings_global['lang_codes'].values():
    testing_to_iso_639_3(lang_iso_639_1)

print('---------- Text Type Text -> Text Type Code ----------')

for text_type_text in main.settings_global['text_types']:
    testing_to_text_type_code(text_type_text)

print('---------- Text Type Code -> Text Type Text ----------')

for text_type_code in main.settings_global['text_types'].values():
    testing_to_text_type_text(text_type_code)

print('---------- Encoding Text -> Encoding Code ----------')

for encoding_text in main.settings_global['file_encodings']:
    testing_to_encoding_code(encoding_text)

print('---------- Encoding Code -> Encoding Text ----------')

for encoding_code in main.settings_global['file_encodings'].values():
    testing_to_encoding_text(encoding_code)
