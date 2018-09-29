#
# Wordless: Detection
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import chardet
import langdetect

from wordless_utils import wordless_conversion, wordless_misc

def detect_encoding(main, file):
    # Defaults
    encoding_code = 'utf_8'
    encoding_lang = None

    if main.settings_custom['file']['auto_detect_encoding']:
        with open(file['path'], 'rb') as f:
            encoding_detected = chardet.detect(f.read())

            encoding_code = encoding_detected['encoding']
            encoding_lang = encoding_detected.get('language')
            
            if encoding_code == None:
                encoding_code = 'utf_8'
            elif encoding_code == 'EUC-TW':
                encoding_code = 'big5'
            elif encoding_code == 'ISO-2022-CN':
                encoding_code = 'gb2312'
            else:
                encoding_code = encoding_code.lower().replace('-', '_')

        try:
            open(file['path'], 'r', encoding = encoding_code)
        except UnicodeDecodeError:
            QMessageBox.warning(main,
                                main.tr('Auto-detection Failure'),
                                main.tr('Failed to auto-detect the encoding of file "{file["name"]}", please select one manually!'),
                                QMessageBox.Ok)

    return encoding_code, encoding_lang

def detect_lang(main, file):
    # Defaults
    lang_code = 'eng'

    if main.settings_custom['file']['auto_detect_lang']:
        try:
            with open(file['path'], 'r', encoding = file['encoding_code']) as f:
                lang_code = wordless_conversion.to_iso_639_3(main, langdetect.detect(f.read()))
        except langdetect.lang_detect_exception.LangDetectException:
            QMessageBox.warning(main,
                                main.tr('Auto-detection Failure'),
                                main.tr(f'Failed to auto-detect the language of file "{file["name"]}", please select one manually!'),
                                QMessageBox.Ok)

    return lang_code
