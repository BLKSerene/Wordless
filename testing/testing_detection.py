# -*- coding: utf-8 -*-

#
# Wordless: Testing for Detection
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import sys

from PyQt5.QtCore import *

sys.path.append('E:/Wordless')

from wordless_utils import wordless_detection
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

def new_file(file_path):
    file = {}

    file['path'] = os.path.realpath(file_path)
    file['name'] = os.path.split(file['path'])[1]

    file['encoding_code'] = 'utf_8'

    return file

def detect_encoding(file):
	print(f'Detect the encoding of file "{file["name"]}": ', end = '')
	print(wordless_detection.detect_encoding(main, file))

def detect_lang(file):
	print(f'Detect the language of file "{file["name"]}": ', end = '')
	print(wordless_detection.detect_lang(main, file))

# Encodings
file_gb2312 = new_file('testing/Encodings/Chinese (Simplified) (GB2312).txt')
file_hz = new_file('testing/Encodings/Chinese (Simplified) (HZ).txt')
file_big5 = new_file('testing/Encodings/Chinese (Traditional) (Big5).txt')
file_utf_8_with_bom = new_file('testing/Encodings/English (UTF-8 with BOM).txt')
file_utf_8_without_bom = new_file('testing/Encodings/English (UTF-8 Without BOM).txt')
file_utf_8_be_with_bom = new_file('testing/Encodings/English (UTF-16 Big Endian with BOM).txt')
file_utf_8_le_with_bom = new_file('testing/Encodings/English (UTF-16 Little Endian with BOM).txt')
file_iso_2022_jp = new_file('testing/Encodings/Japanese (ISO-2022-JP).txt')
file_shift_jis = new_file('testing/Encodings/Japanese (SHIFT_JIS).txt')
file_euc_kr = new_file('testing/Encodings/Korean (EUC-KR).txt')
file_iso_2022_kr = new_file('testing/Encodings/Korean (ISO-2022-KR).txt')
file_iso_8859_5 = new_file('testing/Encodings/Russian (ISO-8859-5).txt')
file_koi8_r = new_file('testing/Encodings/Russian (KOI8-R).txt')
file_windows_1251 = new_file('testing/Encodings/Russian (Windows-1251).txt')

detect_encoding(file_gb2312)
detect_encoding(file_hz)
detect_encoding(file_big5)
detect_encoding(file_utf_8_with_bom)
detect_encoding(file_utf_8_without_bom)
detect_encoding(file_utf_8_be_with_bom)
detect_encoding(file_utf_8_le_with_bom)
detect_encoding(file_iso_2022_jp)
detect_encoding(file_shift_jis)
detect_encoding(file_euc_kr)
detect_encoding(file_iso_2022_kr)
detect_encoding(file_iso_8859_5)
detect_encoding(file_koi8_r)
detect_encoding(file_windows_1251)

# Languages
file_ara = new_file('testing/Languages/Arabic.txt')
file_zho_cn = new_file('testing/Languages/Chinese (Simplified).txt')
file_zho_tw = new_file('testing/Languages/Chinese (Traditional).txt')
file_eng = new_file('testing/Languages/English.txt')
file_fra = new_file('testing/Languages/French.txt')
file_deu = new_file('testing/Languages/German.txt')
file_ita = new_file('testing/Languages/Italian.txt')
file_jpn = new_file('testing/Languages/Japanese.txt')
file_kor = new_file('testing/Languages/Korean.txt')
file_por = new_file('testing/Languages/Portuguese.txt')
file_rus = new_file('testing/Languages/Russian.txt')
file_spa = new_file('testing/Languages/Spanish.txt')

print('---------- langid.py ----------')

main.settings_custom['lang_detection']['detection_settings']['detection_engine'] = 'langid.py'

detect_lang(file_ara)
detect_lang(file_zho_cn)
detect_lang(file_zho_tw)
detect_lang(file_eng)
detect_lang(file_fra)
detect_lang(file_deu)
detect_lang(file_ita)
detect_lang(file_jpn)
detect_lang(file_kor)
detect_lang(file_por)
detect_lang(file_rus)
detect_lang(file_spa)

print('---------- langdetect ----------')

main.settings_custom['lang_detection']['detection_settings']['detection_engine'] = 'langdetect'

detect_lang(file_ara)
detect_lang(file_zho_cn)
detect_lang(file_zho_tw)
detect_lang(file_eng)
detect_lang(file_fra)
detect_lang(file_deu)
detect_lang(file_ita)
detect_lang(file_jpn)
detect_lang(file_kor)
detect_lang(file_por)
detect_lang(file_rus)
detect_lang(file_spa)
