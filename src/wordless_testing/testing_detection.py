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

def new_file_encoding(file_name):
    file = {}

    file['path'] = f'wordless_testing/files/encodings/{file_name}'
    file['name'] = os.path.basename(file['path'])

    file['encoding'] = 'utf_8'

    return file

def new_file_lang(file_name):
    file = {}

    file['path'] = f'wordless_testing/files/langs/{file_name}'
    file['name'] = os.path.basename(file['path'])

    file['encoding'] = 'utf_8'

    return file

def detect_encoding(file):
	print(f'Detect the encoding of file "{file["name"]}": ', end = '')

	encoding_code, success = wordless_detection.detect_encoding(main, file["path"])
	print(f"{encoding_code} ({'Success' if success else 'Fail'})")

def detect_lang(file):
	print(f'Detect the language of file "{file["name"]}": ', end = '')

	lang_code, success = wordless_detection.detect_lang(main, file)
	print(f"{lang_code} ({'Success' if success else 'Fail'})")

main = testing_init.Testing_Main()

main.settings_custom['auto_detection']['detection_settings']['number_lines_no_limit'] = True

# Encodings
file_iso_8859_6 = new_file_encoding('Arabic (ISO-8859-6).txt')
file_windows_1256 = new_file_encoding('Arabic (Windows-1256).txt')

file_iso_8859_13 = new_file_encoding('Baltic Languages - Polish (ISO-8859-13).txt')
file_windows_1257 = new_file_encoding('Baltic Languages - Estonian (Windows-1257).txt')

file_cp852 = new_file_encoding('Central European - Croatian (CP852).txt')
file_iso_8859_2 = new_file_encoding('Central European - Croatian (ISO-8859-2).txt')
file_mac_central_europe = new_file_encoding('Central European - Croatian (Mac OS Central European).txt')
file_windows_1250 = new_file_encoding('Central European - Croatian (Windows-1250).txt')

file_gb18030 = new_file_encoding('Chinese (Simplified) (GB18030).txt')
file_hz = new_file_encoding('Chinese (Simplified) (HZ).txt')
file_big5 = new_file_encoding('Chinese (Traditional) (Big5).txt')

file_cp855 = new_file_encoding('Cyrillic - Russian (CP855).txt')
file_cp866 = new_file_encoding('Cyrillic - Russian (CP866).txt')
file_iso_8859_5 = new_file_encoding('Cyrillic - Russian (ISO-8859-5).txt')
file_mac_cyrillic = new_file_encoding('Cyrillic - Russian (Mac OS Cyrillic).txt')
file_windows_1251 = new_file_encoding('Cyrillic - Russian (Windows-1251).txt')

file_ascii = new_file_encoding('English (ASCII).txt')
file_utf_8_with_bom = new_file_encoding('English (UTF-8 with BOM).txt')
file_utf_8_without_bom = new_file_encoding('English (UTF-8 Without BOM).txt')
file_utf_16_be_with_bom = new_file_encoding('English (UTF-16 Big Endian with BOM).txt')
file_utf_16_le_with_bom = new_file_encoding('English (UTF-16 Little Endian with BOM).txt')

file_iso_8859_3 = new_file_encoding('Esperanto & Maltese - Esperanto (ISO-8859-3).txt')

file_iso_8859_7 = new_file_encoding('Greek (ISO-8859-7).txt')
file_windows_1253 = new_file_encoding('Greek (Windows-1253).txt')

file_iso_8859_8 = new_file_encoding('Hebrew (ISO-8859-8).txt')
file_windows_1255 = new_file_encoding('Hebrew (Windows-1255).txt')

file_cp932 = new_file_encoding('Japanese (CP932).txt')
file_euc_jp = new_file_encoding('Japanese (EUC-JP).txt')
file_iso_2022_jp = new_file_encoding('Japanese (ISO-2022-JP).txt')
file_shift_jis = new_file_encoding('Japanese (SHIFT_JIS).txt')

file_iso_2022_kr = new_file_encoding('Korean (ISO-2022-KR).txt')
file_uhc = new_file_encoding('Korean (UHC).txt')

file_iso_8859_10 = new_file_encoding('Nordic Languages - Latvian (ISO-8859-10).txt')

file_iso_8859_4 = new_file_encoding('North European - Latvian (ISO-8859-4).txt')

file_koi8_r = new_file_encoding('Russian (KOI8-R).txt')

file_iso_8859_16 = new_file_encoding('South-Eastern European - Croatian (ISO-8859-16).txt')

file_tis_620 = new_file_encoding('Thai (TIS-620).txt')

file_iso_8859_9 = new_file_encoding('Turkish (ISO-8859-9).txt')

file_iso_8859_1 = new_file_encoding('Western European - Italian (ISO-8859-1).txt')
file_iso_8859_15 = new_file_encoding('Western European - Danish (ISO-8859-15).txt')
file_windows_1252 = new_file_encoding('Western European - Estonian (Windows-1252).txt')

print('---------- Encoding Detection ----------')

detect_encoding(file_iso_8859_6)
detect_encoding(file_windows_1256)

detect_encoding(file_iso_8859_13)
detect_encoding(file_windows_1257)

detect_encoding(file_cp852)
detect_encoding(file_iso_8859_2)
detect_encoding(file_mac_central_europe)
detect_encoding(file_windows_1250)

detect_encoding(file_gb18030)
detect_encoding(file_hz)
detect_encoding(file_big5)

detect_encoding(file_cp855)
detect_encoding(file_cp866)
detect_encoding(file_iso_8859_5)
detect_encoding(file_mac_cyrillic)
detect_encoding(file_windows_1251)

detect_encoding(file_ascii)
detect_encoding(file_utf_8_with_bom)
detect_encoding(file_utf_8_without_bom)
detect_encoding(file_utf_16_be_with_bom)
detect_encoding(file_utf_16_le_with_bom)

detect_encoding(file_iso_8859_3)

detect_encoding(file_iso_8859_7)
detect_encoding(file_windows_1253)

detect_encoding(file_iso_8859_8)
detect_encoding(file_windows_1255)

detect_encoding(file_cp932)
detect_encoding(file_euc_jp)
detect_encoding(file_iso_2022_jp)
detect_encoding(file_shift_jis)

detect_encoding(file_iso_2022_kr)
detect_encoding(file_uhc)

detect_encoding(file_iso_8859_10)

detect_encoding(file_iso_8859_4)

detect_encoding(file_koi8_r)

detect_encoding(file_iso_8859_16)

detect_encoding(file_tis_620)

detect_encoding(file_iso_8859_9)

detect_encoding(file_iso_8859_1)
detect_encoding(file_iso_8859_15)
detect_encoding(file_windows_1252)

# Languages
file_ara = new_file_lang('Arabic.txt')
file_zho_cn = new_file_lang('Chinese (Simplified).txt')
file_zho_tw = new_file_lang('Chinese (Traditional).txt')
file_eng = new_file_lang('English.txt')
file_fra = new_file_lang('French.txt')
file_deu = new_file_lang('German.txt')
file_ita = new_file_lang('Italian.txt')
file_jpn = new_file_lang('Japanese.txt')
file_kor = new_file_lang('Korean.txt')
file_nob = new_file_lang('Norwegian Bokmål.txt')
file_nno = new_file_lang('Norwegian Nynorsk.txt')
file_por = new_file_lang('Portuguese.txt')
file_rus = new_file_lang('Russian.txt')
file_spa = new_file_lang('Spanish.txt')

print('---------- Language Detection ----------')

detect_lang(file_ara)
detect_lang(file_zho_cn)
detect_lang(file_zho_tw)
detect_lang(file_eng)
detect_lang(file_fra)
detect_lang(file_deu)
detect_lang(file_ita)
detect_lang(file_jpn)
detect_lang(file_kor)
detect_lang(file_nob)
detect_lang(file_nno)
detect_lang(file_por)
detect_lang(file_rus)
detect_lang(file_spa)
