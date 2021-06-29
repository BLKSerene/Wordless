#
# Wordless: Utilities - Detection
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chardet
import cchardet
import langdetect
import langid

from wl_text import wl_matching
from wl_utils import wl_conversion, wl_misc

# Force consistent results for language detection
langdetect.DetectorFactory.seed = 0

def detect_encoding(main, file_path):
    text = b''

    with open(file_path, 'rb') as f:
        if main.settings_custom['auto_detection']['detection_settings']['number_lines_no_limit']:
            for line in f:
                text += line
        else:
            for i, line in enumerate(f):
                if i < main.settings_custom['auto_detection']['detection_settings']['number_lines']:
                    text += line
                else:
                    break

        encoding = cchardet.detect(text)['encoding']

        # Force ASCII be converted to UTF-8
        if encoding == 'ASCII':
            encoding = 'UTF-8'
        # CP932
        elif encoding == 'SHIFT_JIS':
            encoding = chardet.detect(text)['encoding']

            if encoding != 'CP932':
                encoding = 'SHIFT_JIS'
        if encoding == 'EUC-TW':
            encoding = 'BIG5'
        elif encoding == 'ISO-2022-CN':
            encoding = 'GB18030'
        elif encoding == None:
            encoding = main.settings_custom['auto_detection']['default_settings']['default_encoding']

    encoding = encoding.lower()
    encoding = encoding.replace('-', '_')

    return encoding

def detect_lang(main, file):
    text = ''

    try:
        with open(file['path'], 'r', encoding = file['encoding']) as f:
            if main.settings_custom['auto_detection']['detection_settings']['number_lines_no_limit']:
                for line in f:
                    text += line
            else:
                for i, line in enumerate(f):
                    if i < main.settings_custom['auto_detection']['detection_settings']['number_lines']:
                        text += line
                    else:
                        break

        lang_code_639_1 = langid.classify(text)[0]

        # Chinese (Simplified) & Chinese (Traditional)
        if lang_code_639_1 == 'zh':
            lang_code_639_1 = 'zh_cn'

            for lang in sorted(langdetect.detect_langs(text), key = lambda item: -item.prob):
                if lang.lang in ['zh-cn', 'zh-tw']:
                    lang_code_639_1 = lang.lang.replace('-', '_')

                    break
        # Norwegian Bokmål
        elif lang_code_639_1 == 'no':
            lang_code_639_1 = 'nb'

        # Serbian (Cyrillic)
        elif lang_code_639_1 == 'sr':
            lang_code_639_1 = 'sr_cyrl'

        lang = wl_conversion.to_iso_639_3(main, lang_code_639_1)
    except:
        lang = main.settings_custom['auto_detection']['default_settings']['default_lang']

    return lang
