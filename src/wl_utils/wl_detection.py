# ----------------------------------------------------------------------
# Wordless: Utilities - Detection
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import charset_normalizer
import langdetect
import langid

from wl_utils import wl_conversion

# Force consistent results for language detection
langdetect.DetectorFactory.seed = 0

def detect_encoding(main, file_path):
    text = b''

    with open(file_path, 'rb') as f:
        if main.settings_custom['files']['auto_detection_settings']['number_lines_no_limit']:
            text = f.read()
        else:
            for i, line in enumerate(f):
                if i < main.settings_custom['files']['auto_detection_settings']['number_lines']:
                    text += line
                else:
                    break

    results = charset_normalizer.from_bytes(text)

    if results:
        encoding = results.best().encoding
    else:
        encoding = 'utf_8'

    # Test decodability
    if encoding != 'utf_8':
        try:
            with open(file_path, 'r', encoding = encoding) as f:
                f.read()
        # Fall back to UTF-8 if fail
        except UnicodeDecodeError:
            encoding = 'utf_8'

    return encoding

def detect_lang_text(main, text):
    lang_code_639_1 = langid.classify(text)[0]

    # Chinese (Simplified) & Chinese (Traditional)
    if lang_code_639_1 == 'zh':
        lang_code_639_1 = 'zh_cn'

        for lang in sorted(langdetect.detect_langs(text), key = lambda item: -item.prob):
            if lang.lang in ['zh-cn', 'zh-tw']:
                lang_code_639_1 = lang.lang.replace('-', '_')

                break
    # English
    elif lang_code_639_1 == 'en':
        lang_code_639_1 = 'en_us'
    # German
    elif lang_code_639_1 == 'de':
        lang_code_639_1 = 'de_de'
    # Norwegian Bokmål
    elif lang_code_639_1 == 'no':
        lang_code_639_1 = 'nb'
    # Portuguese
    elif lang_code_639_1 == 'pt':
        lang_code_639_1 = 'pt_pt'
    # Serbian (Cyrillic)
    elif lang_code_639_1 == 'sr':
        lang_code_639_1 = 'sr_cyrl'

    lang = wl_conversion.to_iso_639_3(main, lang_code_639_1)

    # Other Languages
    if lang is None:
        lang = 'other'

    return lang

def detect_lang_file(main, file):
    text = ''

    try:
        with open(file['path'], 'r', encoding = file['encoding']) as f:
            if main.settings_custom['files']['auto_detection_settings']['number_lines_no_limit']:
                for line in f:
                    text += line
            else:
                for i, line in enumerate(f):
                    if i < main.settings_custom['files']['auto_detection_settings']['number_lines']:
                        text += line
                    else:
                        break

        lang = detect_lang_text(main, text)
    except UnicodeDecodeError:
        lang = main.settings_custom['files']['default_settings']['lang']

    return lang
