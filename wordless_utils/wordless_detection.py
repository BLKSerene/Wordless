#
# Wordless: Detection
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chardet
import langdetect
import langid

from wordless_utils import wordless_conversion, wordless_misc

def detect_encoding(main, file_path):
    text_sample = b''
    success = True

    with open(file_path, 'rb') as f:
        for i, line in enumerate(f):
            if i < 100:
                text_sample += line
            else:
                break

        encoding_code = chardet.detect(text_sample)['encoding']
        
        if encoding_code == None:
            encoding_code = 'utf_8'

            success = False
        elif encoding_code == 'EUC-TW':
            encoding_code = 'big5'
        elif encoding_code == 'ISO-2022-CN':
            encoding_code = 'gb2312'
        else:
            encoding_code = encoding_code.lower().replace('-', '_')

    try:
        open(file_path, 'r', encoding = encoding_code)
    except:
        success = False

    return encoding_code, success

def detect_lang(main, file):
    text = ''

    detection_engine = main.settings_custom['lang_detection']['detection_settings']['detection_engine']

    try:
        with open(file['path'], 'r', encoding = file['encoding_code']) as f:
            if main.settings_custom['lang_detection']['detection_settings']['number_lines_no_limit']:
                for line in f:
                    text += line
            else:
                for i, line in enumerate(f):
                    if i < main.settings_custom['lang_detection']['detection_settings']['number_lines']:
                        text += line
                    else:
                        break

            if detection_engine == 'langid.py':
                lang_code_639_1 = langid.classify(text)[0]

                # Chinese (Simplified) & Chinese (Traditional)
                if lang_code_639_1 == 'zh':
                    lang_code_639_1 = 'zh_cn'

                    for lang in sorted(langdetect.detect_langs(text), key = lambda item: -item.prob):
                        if lang.lang in ['zh-cn', 'zh-tw']:
                            lang_code_639_1 = lang.lang

                            break
                # Norwegian
                elif lang_code_639_1 == 'no':
                    lang_code_639_1 = 'nb'
            elif detection_engine == 'langdetect':
                lang_code_639_1 = langdetect.detect(text)

                # Norwegian Bokmål & Norwegian Nynorsk
                if lang_code_639_1 == 'no':
                    langid.set_languages(['nb', 'nn'])

                    lang_code_639_1 = langid.classify(text)[0]

            lang_code = wordless_conversion.to_iso_639_3(main, lang_code_639_1.replace('-', '_'))
            
            success = True
    except:
        lang_code = main.settings_custom['lang_detection']['default_settings']['default_lang']

        success = False

    return lang_code, success
