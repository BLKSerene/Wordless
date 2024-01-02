# ----------------------------------------------------------------------
# Wordless: Utilities - Detection
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
import lingua
import opencc

def detect_encoding(main, file_path):
    text = b''

    with open(file_path, 'rb') as f:
        if main.settings_custom['files']['auto_detection_settings']['num_lines_no_limit']:
            text = f.read()
        else:
            for i, line in enumerate(f):
                if i < main.settings_custom['files']['auto_detection_settings']['num_lines']:
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

lingua_detector = lingua.LanguageDetectorBuilder.from_all_languages().build() # pylint: disable=no-member

def detect_lang_text(main, text):
    if not main.settings_custom['files']['auto_detection_settings']['num_lines_no_limit']:
        lines = text.splitlines()
        text = '\n'.join(lines[:main.settings_custom['files']['auto_detection_settings']['num_lines']])

    lang = lingua_detector.detect_language_of(text)

    if lang.name == 'CHINESE':
        converter = opencc.OpenCC('t2s')

        if converter.convert(text) == text:
            lang_code = 'zho_cn'
        else:
            lang_code = 'zho_tw'
    elif lang.name == 'ENGLISH':
        lang_code = 'eng_us'
    elif lang.name == 'GERMAN':
        lang_code = 'deu_de'
    elif lang.name == 'PUNJABI':
        lang_code = 'pan_guru'
    elif lang.name == 'PORTUGUESE':
        lang_code = 'por_pt'
    elif lang.name == 'SERBIAN':
        lang_code = 'srp_cyrl'
    # No results
    elif lang is None:
        lang_code = 'other'
    else:
        lang_code = lang.iso_code_639_3.name.lower()

    return lang_code

def detect_lang_file(main, file):
    text = ''

    try:
        with open(file['path'], 'r', encoding = file['encoding']) as f:
            text = f.read()

        lang = detect_lang_text(main, text)
    except UnicodeDecodeError:
        lang = main.settings_custom['files']['default_settings']['lang']

    return lang
