#
# Wordless: Utility Functions for Detection
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import chardet
import langdetect

from wordless_utils import wordless_misc

def detect_encoding(main, file, auto_detect = True):
    # Defaults
    encoding_code = 'utf_8'
    encoding_text = wordless_misc.convert_encoding(main, encoding_code)

    if auto_detect:
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

            encoding_text = wordless_misc.convert_encoding(main, encoding_code, encoding_lang)

        try:
            open(file['path'], 'r', encoding = encoding_code)
        except UnicodeDecodeError:
            QMessageBox.warning(main,
                                'Auto-detection Failure',
                                'Failed to auto-detect the encoding of file "{}", please select one manually!'.format(file.name),
                                QMessageBox.Ok)
        finally:
            encoding_text = wordless_misc.convert_encoding(main, encoding_code, encoding_lang)

    return encoding_code, encoding_text

def detect_lang(main, file, auto_detect = True):
    # Map ISO 639-2 codes to ISO 639-3 codes
    lang_mappings = {
        'af': 'afr',
        'ar': 'ara',
        'bg': 'bul',
        'bn': 'ben',
        'ca': 'cat',
        'cs': 'ces',
        'cy': 'cym',
        'da': 'dan',
        'de': 'deu',
        'el': 'ell',
        'en': 'eng',
        'es': 'spa',
        'et': 'est',
        'fa': 'fas',
        'fi': 'fin',
        'fr': 'fra',
        'gu': 'guj',
        'he': 'heb',
        'hi': 'hin',
        'hr': 'hrv',
        'hu': 'hun',
        'id': 'ind',
        'it': 'ita',
        'ja': 'jpn',
        'kn': 'kan',
        'ko': 'kor',
        'lt': 'lit',
        'lv': 'lav',
        'mk': 'mkd',
        'ml': 'mal',
        'mr': 'mar',
        'ne': 'nep',
        'nl': 'nld',
        'no': 'nor',
        'pa': 'pan',
        'pl': 'pol',
        'pt': 'por',
        'ro': 'ron',
        'ru': 'rus',
        'sk': 'slk',
        'sl': 'slv',
        'so': 'som',
        'sq': 'sqi',
        'sv': 'swe',
        'sw': 'swa',
        'ta': 'tam',
        'te': 'tel',
        'th': 'tha',
        'tl': 'tgl',
        'tr': 'tur',
        'uk': 'ukr',
        'ur': 'urd',
        'vi': 'vie',
        'zh-cn': 'zho-cn',
        'zh-tw': 'zho-tw',
    }

    # Defaults
    lang_code = 'eng'
    lang_text = wordless_misc.convert_lang(main, lang_code)
    word_delimiter = ' '

    if auto_detect:
        try:
            with open(file['path'], 'r', encoding = file['encoding_code']) as f:
                lang_code = lang_mappings[langdetect.detect(f.read())]
        except langdetect.lang_detect_exception.LangDetectException:
            QMessageBox.warning(main,
                                'Auto-detection Failure',
                                'Failed to auto-detect the language of file "{}", please select one manually!'.format(file.name),
                                QMessageBox.Ok)
        finally:
            lang_text = wordless_misc.convert_lang(main, lang_code)
            word_delimiter = wordless_misc.convert_word_delimiter(lang_code)

    return lang_code, lang_text, word_delimiter
