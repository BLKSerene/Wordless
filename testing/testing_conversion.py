#
# Wordless: Testing for Conversion
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import sys

from PyQt5.QtCore import *

sys.path.append('E:/Wordless')

from wordless_utils import wordless_conversion
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

def testing_to_lang_code(lang_text):
    print(f'{lang_text:22} -> {wordless_conversion.to_lang_code(main, lang_text)}')

def testing_to_lang_text(lang_code):
    print(f'{lang_code:6} -> {wordless_conversion.to_lang_text(main, lang_code)}')

def testing_to_iso_639_3(lang_code):
    print(f'{lang_code:5} -> {wordless_conversion.to_iso_639_3(main, lang_code)}')

def testing_to_iso_639_1(lang_code):
    print(f'{lang_code:6} -> {wordless_conversion.to_iso_639_1(main, lang_code)}')

def testing_to_ext_code(ext_text):
    print(f'{ext_text:10} -> {wordless_conversion.to_ext_code(main, ext_text)}')

def testing_to_ext_text(ext_code):
    print(f'{ext_code:5} -> {wordless_conversion.to_ext_text(main, ext_code)}')

def testing_to_encoding_code(encoding_text):
    print(f'{encoding_text:35} -> {wordless_conversion.to_encoding_code(main, encoding_text)}')

def testing_to_encoding_text(encoding_code):
    print(f'{encoding_code:15} -> {wordless_conversion.to_encoding_text(main, encoding_code)}')

print('---------- Language Code -> Language Text ----------')

testing_to_lang_code('Arabic')
testing_to_lang_code('Chinese (Simplified)')
testing_to_lang_code('Chinese (Traditional)')
testing_to_lang_code('English')
testing_to_lang_code('French')
testing_to_lang_code('German')
testing_to_lang_code('Italian')
testing_to_lang_code('Japanese')
testing_to_lang_code('Korean')
testing_to_lang_code('Norwegian Bokmål')
testing_to_lang_code('Norwegian Nynorsk')
testing_to_lang_code('Portuguese')
testing_to_lang_code('Russian')
testing_to_lang_code('Spanish')

print('---------- Language Text -> Language Code ----------')

testing_to_lang_text('ara')
testing_to_lang_text('zho_cn')
testing_to_lang_text('zho_tw')
testing_to_lang_text('eng')
testing_to_lang_text('fra')
testing_to_lang_text('deu')
testing_to_lang_text('ita')
testing_to_lang_text('jpn')
testing_to_lang_text('kor')
testing_to_lang_text('nob')
testing_to_lang_text('nno')
testing_to_lang_text('por')
testing_to_lang_text('rus')
testing_to_lang_text('spa')

print('---------- ISO 639-1 Code -> ISO 639-3 Code ----------')

testing_to_iso_639_3('ar')
testing_to_iso_639_3('zh_cn')
testing_to_iso_639_3('zh_tw')
testing_to_iso_639_3('en')
testing_to_iso_639_3('fr')
testing_to_iso_639_3('de')
testing_to_iso_639_3('it')
testing_to_iso_639_3('ja')
testing_to_iso_639_3('ko')
testing_to_iso_639_3('nb')
testing_to_iso_639_3('nn')
testing_to_iso_639_3('pt')
testing_to_iso_639_3('ru')
testing_to_iso_639_3('es')

print('---------- ISO 639-3 Code -> ISO 639-1 Code ----------')

testing_to_iso_639_1('ara')
testing_to_iso_639_1('zho_cn')
testing_to_iso_639_1('zho_tw')
testing_to_iso_639_1('eng')
testing_to_iso_639_1('fra')
testing_to_iso_639_1('deu')
testing_to_iso_639_1('ita')
testing_to_iso_639_1('jpn')
testing_to_iso_639_1('kor')
testing_to_iso_639_1('nob')
testing_to_iso_639_1('nno')
testing_to_iso_639_1('por')
testing_to_iso_639_1('rus')
testing_to_iso_639_1('spa')

print('---------- Extension Text -> Extension Code ----------')

testing_to_ext_code('Text File')
testing_to_ext_code('HTML Page')

print('---------- Extension Code -> Extension Text ----------')

testing_to_ext_text('.txt')
testing_to_ext_text('.html')
testing_to_ext_text('.htm')

print('---------- Encoding Text -> Encoding Code ----------')

testing_to_encoding_code('All Languages (UTF-8 Without BOM)')
testing_to_encoding_code('All Languages (UTF-8 with BOM)')
testing_to_encoding_code('Arabic (CP720)')
testing_to_encoding_code('Arabic (CP864)')
testing_to_encoding_code('Arabic (ISO-8859-6)')
testing_to_encoding_code('Arabic (Mac OS Arabic)')
testing_to_encoding_code('Arabic (Windows-1256)')
testing_to_encoding_code('Chinese (GB18030)')
testing_to_encoding_code('Chinese (GBK)')
testing_to_encoding_code('Chinese (Simplified) (GB2312)')
testing_to_encoding_code('Chinese (Simplified) (HZ)')
testing_to_encoding_code('Chinese (Traditional) (Big-5)')
testing_to_encoding_code('Chinese (Traditional) (Big5-HKSCS)')
testing_to_encoding_code('Chinese (Traditional) (CP950)')
testing_to_encoding_code('English (ASCII)')
testing_to_encoding_code('English (EBCDIC 037)')
testing_to_encoding_code('English (CP437)')
testing_to_encoding_code('French (CP863)')
testing_to_encoding_code('German (EBCDIC 273)')
testing_to_encoding_code('Japanese (CP932)')
testing_to_encoding_code('Japanese (EUC-JP)')
testing_to_encoding_code('Japanese (EUC-JIS-2004)')
testing_to_encoding_code('Japanese (EUC-JISx0213)')
testing_to_encoding_code('Japanese (ISO-2022-JP)')
testing_to_encoding_code('Japanese (ISO-2022-JP-1)')
testing_to_encoding_code('Japanese (ISO-2022-JP-2)')
testing_to_encoding_code('Japanese (ISO-2022-JP-2004)')
testing_to_encoding_code('Japanese (ISO-2022-JP-3)')
testing_to_encoding_code('Japanese (ISO-2022-JP-EXT)')
testing_to_encoding_code('Japanese (Shift_JIS)')
testing_to_encoding_code('Japanese (Shift_JIS-2004)')
testing_to_encoding_code('Japanese (Shift_JISx0213)')
testing_to_encoding_code('Korean (EUC-KR)')
testing_to_encoding_code('Korean (ISO-2022-KR)')
testing_to_encoding_code('Korean (JOHAB)')
testing_to_encoding_code('Korean (Windows-949)')
testing_to_encoding_code('Portuguese (CP860)')
testing_to_encoding_code('Russian (KOI8-R)')

print('---------- Encoding Code -> Encoding Text ----------')

testing_to_encoding_text('utf_8')
testing_to_encoding_text('utf_8_sig')
testing_to_encoding_text('cp720')
testing_to_encoding_text('cp864')
testing_to_encoding_text('iso8859_6')
testing_to_encoding_text('mac_arabic')
testing_to_encoding_text('cp1256')
testing_to_encoding_text('gb18030')
testing_to_encoding_text('gbk')
testing_to_encoding_text('gb2312')
testing_to_encoding_text('hz_gb_2312')
testing_to_encoding_text('big5')
testing_to_encoding_text('big5hkscs')
testing_to_encoding_text('cp950')
testing_to_encoding_text('ascii')
testing_to_encoding_text('cp037')
testing_to_encoding_text('cp437')
testing_to_encoding_text('cp863')
testing_to_encoding_text('cp273')
testing_to_encoding_text('cp932')
testing_to_encoding_text('euc_jp')
testing_to_encoding_text('euc_jis_2004')
testing_to_encoding_text('euc_jisx0213')
testing_to_encoding_text('iso2022_jp')
testing_to_encoding_text('iso2022_jp_1')
testing_to_encoding_text('iso2022_jp_2')
testing_to_encoding_text('iso2022_jp_2004')
testing_to_encoding_text('iso2022_jp_3')
testing_to_encoding_text('iso2022_jp_ext')
testing_to_encoding_text('shift_jis')
testing_to_encoding_text('shift_jis_2004')
testing_to_encoding_text('shift_jisx0213')
testing_to_encoding_text('euc_kr')
testing_to_encoding_text('iso2022_kr')
testing_to_encoding_text('johab')
testing_to_encoding_text('cp949')
testing_to_encoding_text('cp860')
testing_to_encoding_text('koi8_r')
