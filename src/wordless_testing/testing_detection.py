#
# Wordless: Testing - Detection
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
from wordless_utils import wordless_detection

def testing_detection_encoding(file_name):
    file = {}

    file['path'] = f'wordless_testing/files/encodings/{file_name}'
    file['name'] = os.path.basename(file['path'])
    file['encoding'] = 'utf_8'

    print(f'Detect the encoding of file "{file["name"]}": ', end = '')

    encoding_code, success = wordless_detection.detect_encoding(main, file["path"])
    print(f"{encoding_code} ({'Success' if success else 'Fail'})")

def testing_detection_lang(file_name):
    file = {}

    file['path'] = f'wordless_testing/files/langs/{file_name}'
    file['name'] = os.path.basename(file['path'])
    file['encoding'] = 'utf_8'

    print(f'Detect the language of file "{file["name"]}": ', end = '')

    lang_code, success = wordless_detection.detect_lang(main, file)

    print(f"{lang_code} ({'Success' if success else 'Fail'})")

main = testing_init.Testing_Main()

main.settings_custom['auto_detection']['detection_settings']['number_lines_no_limit'] = True

# Encoding detection
print('---------- Encoding Detection ----------')

testing_detection_encoding('Arabic (ISO-8859-6).txt')
testing_detection_encoding('Arabic (Windows-1256).txt')

testing_detection_encoding('Baltic Languages - Polish (ISO-8859-13).txt')
testing_detection_encoding('Baltic Languages - Estonian (Windows-1257).txt')

testing_detection_encoding('Central European - Croatian (CP852).txt')
testing_detection_encoding('Central European - Croatian (ISO-8859-2).txt')
testing_detection_encoding('Central European - Croatian (Mac OS Central European).txt')
testing_detection_encoding('Central European - Croatian (Windows-1250).txt')

testing_detection_encoding('Chinese (Simplified) (GB18030).txt')
testing_detection_encoding('Chinese (Simplified) (HZ).txt')
testing_detection_encoding('Chinese (Traditional) (Big5).txt')

testing_detection_encoding('Cyrillic - Russian (CP855).txt')
testing_detection_encoding('Cyrillic - Russian (CP866).txt')
testing_detection_encoding('Cyrillic - Russian (ISO-8859-5).txt')
testing_detection_encoding('Cyrillic - Russian (Mac OS Cyrillic).txt')
testing_detection_encoding('Cyrillic - Russian (Windows-1251).txt')

testing_detection_encoding('English (ASCII).txt')
testing_detection_encoding('English (UTF-8 with BOM).txt')
testing_detection_encoding('English (UTF-8 Without BOM).txt')
testing_detection_encoding('English (UTF-16 Big Endian with BOM).txt')
testing_detection_encoding('English (UTF-16 Little Endian with BOM).txt')

testing_detection_encoding('Esperanto & Maltese - Esperanto (ISO-8859-3).txt')

testing_detection_encoding('Greek (ISO-8859-7).txt')
testing_detection_encoding('Greek (Windows-1253).txt')

testing_detection_encoding('Hebrew (ISO-8859-8).txt')
testing_detection_encoding('Hebrew (Windows-1255).txt')

testing_detection_encoding('Japanese (CP932).txt')
testing_detection_encoding('Japanese (EUC-JP).txt')
testing_detection_encoding('Japanese (ISO-2022-JP).txt')
testing_detection_encoding('Japanese (SHIFT_JIS).txt')

testing_detection_encoding('Korean (ISO-2022-KR).txt')
testing_detection_encoding('Korean (UHC).txt')

testing_detection_encoding('Nordic Languages - Latvian (ISO-8859-10).txt')

testing_detection_encoding('North European - Latvian (ISO-8859-4).txt')

testing_detection_encoding('Russian (KOI8-R).txt')

testing_detection_encoding('South-Eastern European - Croatian (ISO-8859-16).txt')

testing_detection_encoding('Thai (TIS-620).txt')

testing_detection_encoding('Turkish (ISO-8859-9).txt')

testing_detection_encoding('Western European - Italian (ISO-8859-1).txt')
testing_detection_encoding('Western European - Danish (ISO-8859-15).txt')
testing_detection_encoding('Western European - Estonian (Windows-1252).txt')

# Language detection
print('---------- Language Detection ----------')

testing_detection_lang('Arabic.txt')
testing_detection_lang('Chinese (Simplified).txt')
testing_detection_lang('Chinese (Traditional).txt')
testing_detection_lang('English.txt')
testing_detection_lang('French.txt')
testing_detection_lang('German.txt')
testing_detection_lang('Greek.txt')
testing_detection_lang('Hebrew.txt')
testing_detection_lang('Hindi.txt')
testing_detection_lang('Italian.txt')
testing_detection_lang('Japanese.txt')
testing_detection_lang('Korean.txt')
testing_detection_lang('Norwegian Bokmål.txt')
testing_detection_lang('Norwegian Nynorsk.txt')
testing_detection_lang('Portuguese.txt')
testing_detection_lang('Russian.txt')
testing_detection_lang('Spanish.txt')
