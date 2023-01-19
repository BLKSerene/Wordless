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
from wordless.wl_utils import wl_detection

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

    assert langs_extra == ['BOSNIAN', 'MAORI', 'SHONA', 'TSONGA', 'XHOSA']

# Encoding detection
def check_encodings_detected(test_file_dir, encodings, text):
    for encoding in encodings:
        file_path = os.path.join(test_file_dir, f'{encoding}.txt')

        # Use same line endings for different OSes run on CI
        with open(file_path, 'w', encoding = encoding, errors = 'replace', newline = '\r\n') as f:
            f.write(text)

        encoding_detected = wl_detection.detect_encoding(main, file_path)

        print(f'{encoding} detected as {encoding_detected}')
        assert encoding_detected == encoding

def test_detection_encoding():
    test_file_dir = 'tests/wl_tests_utils/files_encoding_detection'

    os.makedirs(test_file_dir, exist_ok = True)

    try:
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # utf_8_sig, utf_7
            encodings = ['utf_8', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le'],
            text = wl_test_lang_examples.ENCODING_ENG
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp720, cp864
            encodings = ['cp1256', 'iso8859_6'],
            text = wl_test_lang_examples.ENCODING_ARA
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # gb2312, gbk, hz
            encodings = ['gb18030', 'iso2022_jp_2'],
            text = wl_test_lang_examples.ENCODING_ZHO_CN
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # big5hkscs, cp950, gbk
            encodings = ['big5', 'gb18030'],
            text = wl_test_lang_examples.ENCODING_ZHO_TW
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp852, iso8859_2
            encodings = ['cp1250', 'mac_latin2'],
            text = wl_test_lang_examples.ENCODING_CES
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['ascii', 'cp037'],
            text = wl_test_lang_examples.ENCODING_ENG
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp273'],
            text = wl_test_lang_examples.ENCODING_DEU
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp737, cp875, iso2022_jp_2, iso8859_7
            encodings = ['cp869', 'cp1253', 'mac_greek'],
            text = wl_test_lang_examples.ENCODING_ELL
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp856, cp862, iso8859_8
            encodings = ['cp424', 'cp1255'],
            text = wl_test_lang_examples.ENCODING_HEB
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp858, cp1140, latin_1, iso8859_15, mac_roman
            encodings = ['cp500', 'cp850', 'cp1252', 'iso2022_jp_2'],
            text = wl_test_lang_examples.ENCODING_ITA
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # euc_jp, euc_jisx0213, iso2022_jp_1, iso2022_jp_2, iso2022_jp_2004, iso2022_jp_3, iso2022_jp_ext, shift_jis, shift_jis_2004, shift_jisx0213
            encodings = ['cp932', 'euc_jis_2004', 'iso2022_jp'],
            text = wl_test_lang_examples.ENCODING_JPN
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['kz1048', 'ptcp154'],
            text = wl_test_lang_examples.ENCODING_KAZ
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # euc_kr
            encodings = ['cp949', 'iso2022_jp_2', 'iso2022_kr', 'johab'],
            text = wl_test_lang_examples.ENCODING_KOR
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # iso8859_4
            encodings = ['cp775', 'cp1257', 'iso8859_13'],
            text = wl_test_lang_examples.ENCODING_LAV
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_3'],
            text = wl_test_lang_examples.ENCODING_MLT
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp1250
            encodings = ['cp852', 'iso8859_2', 'mac_latin2'],
            text = wl_test_lang_examples.ENCODING_POL
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_16'],
            text = wl_test_lang_examples.ENCODING_RON
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp866
            encodings = ['cp855', 'cp1251', 'iso8859_5', 'koi8_r', 'mac_cyrillic'],
            text = wl_test_lang_examples.ENCODING_RUS
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp874
            encodings = ['iso8859_11'],
            text = wl_test_lang_examples.ENCODING_THA
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # cp1026, iso8859_9, mac_turkish
            encodings = ['cp857', 'cp1254'],
            text = wl_test_lang_examples.ENCODING_TUR
        )
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # koi8_u
            encodings = ['cp1125'],
            text = wl_test_lang_examples.ENCODING_UKR
        )
    except Exception as exc:
        raise exc
    # Clean cache
    finally:
        shutil.rmtree(test_file_dir)

# Language detection
def test_detection_lang():
    test_file_dir = 'tests/wl_tests_utils/files_encoding_detection'

    os.makedirs(test_file_dir, exist_ok = True)

    try:
        for lang in [
            'afr', 'sqi', 'ara', 'hye', 'aze',
            'eus', 'bel', 'ben', 'bul',
            'cat', 'zho_cn', 'zho_tw', 'hrv', 'ces',
            'dan', 'nld',
            'eng_us', 'epo', 'est',
            'fin', 'fra',
            'deu_de', 'ell', 'guj',
            'heb', 'hin', 'hun',
            'isl', 'ind', 'gle', 'ita',
            'jpn',
            'kat',
            'lat', 'lav', 'lit',
            'mkd', 'mar', 'mon',
            'nno',
            'fas', 'pol', 'por_pt',
            'ron', 'rus',
            'srp_cyrl', 'slk', 'slv', 'spa', 'swa', 'swe',
            'tha', 'tur',
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
