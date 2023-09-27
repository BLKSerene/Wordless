# ----------------------------------------------------------------------
# Wordless: Tests - Utilities - Detection
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

import os
import re
import shutil

import lingua

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_utils import wl_conversion, wl_detection

main = wl_test_init.Wl_Test_Main()

def test_lingua():
    langs = {
        re.search(r'^[^\(\)]+', lang.lower()).group().strip()
        for lang in main.settings_global['langs']
    }
    langs_exceptions = {'bokmal', 'nynorsk', 'slovene'}
    langs_extra = []

    for lang in dir(lingua.Language):
        if not lang.startswith('__') and lang.lower() not in langs | langs_exceptions:
            langs_extra.append(lang)

    print(f"Extra languages: {', '.join(langs_extra)}\n")

    assert langs_extra == ['BOSNIAN', 'MAORI', 'SHONA', 'SOMALI', 'SOTHO', 'TSONGA', 'XHOSA']

# Encoding detection
def check_encodings_detected(test_file_dir, encodings, text):
    for encoding in encodings:
        file_path = os.path.join(test_file_dir, f'{encoding}.txt')

        # Use same line endings for different OSes run on CI
        with open(file_path, 'w', encoding = encoding, errors = 'replace', newline = '\r\n') as f:
            f.write(text)

        encoding_detected = wl_detection.detect_encoding(main, file_path)
        # Check whether the detected code could be successfully converted to text
        encoding_detected_text = wl_conversion.to_encoding_text(main, encoding_detected)

        print(f'{encoding} detected as {encoding_detected} / {encoding_detected_text}')

        assert encoding_detected == encoding
        assert encoding_detected_text

def test_detection_encoding():
    test_file_dir = 'tests/tests_utils/_files_detection_encoding'

    os.makedirs(test_file_dir, exist_ok = True)

    try:
        # All Languages
        # Charset Normalizer does not return "utf_8_sig"
        # Reference: https://github.com/Ousret/charset_normalizer/pull/38
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['utf_8', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le'], # utf_8_sig, utf_7
            text = wl_test_lang_examples.ENCODING_ENG
        )
        # Arabic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp1256', 'iso8859_6'], # cp720, cp864, mac_arabic
            text = wl_test_lang_examples.ENCODING_ARA
        )
        # Baltic Languages
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp775', 'iso8859_13', 'cp1257'],
            text = wl_test_lang_examples.ENCODING_LAV
        )
        # Celtic Languages
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # iso8859_14
            text = wl_test_lang_examples.ENCODING_GLE
        )
        # Chinese (Unified)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['gb18030'], # gbk
            text = wl_test_lang_examples.ENCODING_ZHO_CN
        )
        # Chinese (Simplified)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # gb2312, hz
            text = wl_test_lang_examples.ENCODING_ZHO_CN
        )
        # Chinese (Traditional)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['big5'], # big5hkscs, cp950
            text = wl_test_lang_examples.ENCODING_ZHO_TW
        )
        # Croatian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # mac_croatian
            text = wl_test_lang_examples.ENCODING_HRV
        )
        # Cyrillic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp855', 'iso8859_5', 'mac_cyrillic', 'cp1251'], # cp866
            text = wl_test_lang_examples.ENCODING_RUS
        )
        # English
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['ascii', 'cp037'], # cp437
            text = wl_test_lang_examples.ENCODING_ENG
        )
        # European
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['hp_roman8'],
            text = wl_test_lang_examples.ENCODING_FRA
        )
        # European (Central)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp852', 'iso8859_2', 'mac_latin2'], # cp1250
            text = wl_test_lang_examples.ENCODING_POL
        )
        # European (Northern)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # iso8859_4
            text = wl_test_lang_examples.ENCODING_EST
        )
        # European (Southern)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_3'],
            text = wl_test_lang_examples.ENCODING_MLT
        )
        # European (South-Eastern)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_16'],
            text = wl_test_lang_examples.ENCODING_RON
        )
        # European (Western)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp850', 'cp1252'], # cp500, cp858, cp1140, latin_1, iso8859_15, mac_roman
            text = wl_test_lang_examples.ENCODING_FRA
        )
        # French
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp863
            text = wl_test_lang_examples.ENCODING_FRA
        )
        # German
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp273
            text = wl_test_lang_examples.ENCODING_DEU
        )
        # Greek
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp869', 'mac_greek', 'cp1253'], # cp737, cp875, iso8859_7
            text = wl_test_lang_examples.ENCODING_ELL
        )
        # Hebrew
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp424', 'cp1255'], # cp856, cp862, iso8859_8
            text = wl_test_lang_examples.ENCODING_HEB
        )
        # Icelandic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp861, mac_iceland
            text = wl_test_lang_examples.ENCODING_ISL
        )
        # Japanese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # euc_jp, euc_jisx0213, iso2022_jp_1, iso2022_jp_2, iso2022_jp_2004, iso2022_jp_3, iso2022_jp_ext, shift_jis, shift_jis_2004, shift_jisx0213
            encodings = ['cp932', 'euc_jis_2004', 'iso2022_jp'],
            text = wl_test_lang_examples.ENCODING_JPN
        )
        # Kazakh
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['kz1048', 'ptcp154'],
            text = wl_test_lang_examples.ENCODING_KAZ
        )
        # Korean
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso2022_kr', 'johab', 'cp949'], # euc_kr
            text = wl_test_lang_examples.ENCODING_KOR
        )
        # Nordic Languages
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp865, iso8859_10
            text = wl_test_lang_examples.ENCODING_ISL
        )
        # Persian/Urdu
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # mac_farsi
            text = wl_test_lang_examples.ENCODING_URD
        )
        # Portuguese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp860
            text = wl_test_lang_examples.ENCODING_POR
        )
        # Romanian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # mac_romanian
            text = wl_test_lang_examples.ENCODING_RON
        )
        # Russian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['koi8_r'],
            text = wl_test_lang_examples.ENCODING_RUS
        )
        # Tajik
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # koi8_t
            text = wl_test_lang_examples.ENCODING_TGK
        )
        # Thai
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_11'], # cp874, tis_620
            text = wl_test_lang_examples.ENCODING_THA
        )
        # Turkish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp857', 'cp1254'], # cp1026, iso8859_9, mac_turkish
            text = wl_test_lang_examples.ENCODING_TUR
        )
        # Ukrainian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp1125'], # koi8_u
            text = wl_test_lang_examples.ENCODING_UKR
        )
        # Urdu
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp1006
            text = wl_test_lang_examples.ENCODING_URD
        )
        # Vietnamese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # cp1258
            text = wl_test_lang_examples.ENCODING_VIE
        )
    except Exception as exc:
        raise exc
    # Clean cache
    finally:
        shutil.rmtree(test_file_dir)

# Language detection
def test_detection_lang():
    test_file_dir = 'tests/tests_utils/_files_detection_lang'

    os.makedirs(test_file_dir, exist_ok = True)

    try:
        for lang in [
            'afr', 'sqi', 'ara', 'hye', 'aze',
            'eus', 'bel', 'ben', 'bul',
            'cat', 'zho_cn', 'zho_tw', 'hrv', 'ces',
            'dan', 'nld',
            'eng_us', 'epo', 'est',
            'fin', 'fra',
            'lug', 'kat', 'deu_de', 'ell', 'guj',
            'heb', 'hin', 'hun',
            'isl', 'ind', 'gle', 'ita',
            'jpn',
            'kor', 'kaz',
            'lat', 'lav', 'lit',
            'mkd', 'mar', 'mon', 'msa',
            'nno', # 'nob',
            'fas', 'pol', 'por_pt', 'pan_guru',
            'ron', 'rus',
            'srp_cyrl', 'slk', 'slv', 'spa', 'swa', 'swe',
            'tgl', 'tam', 'tel', 'tha', 'tsn', 'tur',
            'ukr', 'urd',
            'vie',
            'cym',
            'yor',
            'zul'
        ]:
            file_path = os.path.join(test_file_dir, f'{lang}.txt')
            file = {
                'path': file_path,
                'encoding': 'utf_8'
            }
            text = wl_test_lang_examples.__dict__[f'SENTENCE_{lang.upper()}']

            with open(file_path, 'w', encoding = file['encoding']) as f:
                f.write(text)

            lang_code_file = wl_detection.detect_lang_file(main, file)
            lang_code_text = wl_detection.detect_lang_text(main, text)

            print(f'{lang} detected as {lang_code_file}/{lang_code_text}')
            assert lang == lang_code_file == lang_code_text
    except Exception as exc:
        raise exc
    # Clean cache
    finally:
        shutil.rmtree(test_file_dir)

if __name__ == '__main__':
    test_lingua()
    test_detection_encoding()
    test_detection_lang()
