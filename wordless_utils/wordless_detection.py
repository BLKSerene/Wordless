#
# Wordless: Utilities - Detection
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
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

from wordless_text import wordless_matching
from wordless_utils import wordless_conversion, wordless_misc

def detect_encoding(main, file_path):
    text = b''
    success = True

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
        
        if encoding == 'SHIFT_JIS':
            # CP932
            encoding = chardet.detect(text)['encoding']

            if encoding != 'CP932':
                encoding = 'SHIFT_JIS'
        if encoding == 'EUC-TW':
            encoding = 'BIG5'
        elif encoding == 'ISO-2022-CN':
            encoding = 'GB18030'
        elif encoding == None:
            encoding = main.settings_custom['auto_detection']['default_settings']['default_encoding']

            success = False
        
    try:
        open(file_path, 'r', encoding = encoding)
    except:
        success = False

    return encoding, success

def detect_text_type(main, file):
    tagged_pos = False
    tagged_non_pos = False

    try:
        with open(file['path'], 'r', encoding = file['encoding']) as f:
            re_tags_pos = wordless_matching.get_re_tags(main, tags = 'pos')
            re_tags_non_pos = wordless_matching.get_re_tags(main, tags = 'non_pos')

            if main.settings_custom['auto_detection']['detection_settings']['number_lines_no_limit']:
                for line in f:
                    if re.search(re_tags_pos, line):
                        tagged_pos = True

                        break

                f.seek(0)

                for line in f:
                    if re.search(re_tags_non_pos, line):
                        tagged_non_pos = True

                        break
            else:
                for i, line in enumerate(f):
                    if i >= main.settings_custom['auto_detection']['detection_settings']['number_lines']:
                        break

                    if re.search(re_tags_pos, line):
                        tagged_pos = True

                        break

                f.seek(0)

                for i, line in enumerate(f):
                    if i >= main.settings_custom['auto_detection']['detection_settings']['number_lines']:
                        break

                    if re.search(re_tags_non_pos, line):
                        tagged_non_pos = True

                        break

        if tagged_pos and tagged_non_pos:
            text_type = ['tokenized', 'tagged_both']
        elif tagged_pos:
            text_type = ['tokenized', 'tagged_pos']
        elif tagged_non_pos:
            text_type = ['untokenized', 'tagged_non_pos']
        else:
            text_type = ['untokenized', 'untagged']

        success = True
    except:
        text_type = main.settings_custom['auto_detection']['default_settings']['default_text_type']

        success = False

    return text_type, success

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
                    lang_code_639_1 = lang.lang

                    break
        # Norwegian
        elif lang_code_639_1 == 'no':
            lang_code_639_1 = 'nb'

        lang = wordless_conversion.to_iso_639_3(main, lang_code_639_1.replace('-', '_'))
        
        success = True
    except:
        lang = main.settings_custom['auto_detection']['default_settings']['default_lang']

        success = False

    return lang, success
