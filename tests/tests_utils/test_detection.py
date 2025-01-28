# ----------------------------------------------------------------------
# Tests: Utilities - Detection
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import os
import re
import shutil

import lingua

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_utils import wl_conversion, wl_detection

main = wl_test_init.Wl_Test_Main()

def check_encodings_detected(test_file_dir, encodings, text):
    encodings_detected = []

    for encoding in encodings:
        file_path = os.path.join(test_file_dir, f'{encoding}.txt')

        with open(file_path, 'w', encoding = encoding, errors = 'replace') as f:
            f.write(text)

        main.settings_custom['files']['auto_detection_settings']['num_lines_no_limit'] = True
        encoding_detected_no_limit = wl_detection.detect_encoding(main, file_path)

        main.settings_custom['files']['auto_detection_settings']['num_lines_no_limit'] = False
        encoding_detected = wl_detection.detect_encoding(main, file_path)

        # Check whether the detected code could be successfully converted to text
        encoding_detected_text = wl_conversion.to_encoding_text(main, encoding_detected)

        print(f'{encoding} detected as {encoding_detected} / {encoding_detected_text}')

        assert encoding_detected == encoding_detected_no_limit
        assert encoding_detected_text

        encodings_detected.append(encoding_detected)

    assert encodings_detected == encodings

def test_detection_encoding():
    test_file_dir = 'tests/tests_utils/_files_detection_encoding'

    os.makedirs(test_file_dir, exist_ok = True)

    with open(f'{test_file_dir}/test.exe', 'wb') as f:
        f.write(b'\xFF\x00\x00')

    assert wl_detection.detect_encoding(main, f'{test_file_dir}/test.exe') == 'utf_8'

    try:
        # All languages
        # Charset Normalizer does not return "utf_8_sig"
        # Reference: https://github.com/Ousret/charset_normalizer/pull/38
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['utf_8', 'utf_8_sig', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le'], # 'utf_7'
            text = wl_test_lang_examples.ENCODING_FRA
        )
        # Arabic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp720', 'iso8859_6', 'cp1256'], # 'cp864', 'mac_arabic'
            text = wl_test_lang_examples.ENCODING_ARA
        )
        # Baltic languages
        # e.g. Lithuanian, Latvian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp775'], # 'iso8859_13', 'cp1257'
            text = wl_test_lang_examples.ENCODING_LAV
        )
        # Celtic languages
        # e.g. Irish, Manx, Scottish Gaelic, Welsh
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'iso8859_14'
            text = wl_test_lang_examples.ENCODING_GLE
        )
        # Chinese (Unified)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['gb18030'], # 'gbk'
            text = wl_test_lang_examples.ENCODING_ZHO_TW
        )
        # Chinese (Simplified)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'gb2312', 'hz'
            text = wl_test_lang_examples.ENCODING_ZHO_CN
        )
        # Chinese (Traditional)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['big5'], # 'big5hkscs', 'cp950'
            text = wl_test_lang_examples.ENCODING_ZHO_TW
        )
        # Croatian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'mac_croatian'
            text = wl_test_lang_examples.ENCODING_HRV
        )
        # Cyrillic
        # e.g. Belarusian, Bulgarian, Macedonian, Russian, Serbian (Cyrillic)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp855', 'iso8859_5', 'mac_cyrillic', 'cp1251'], # 'cp866'
            text = wl_test_lang_examples.ENCODING_RUS
        )
        # English
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['ascii', 'cp037'], # 'cp437'
            text = wl_test_lang_examples.ENCODING_ENG
        )
        # European
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['hp_roman8'],
            text = wl_test_lang_examples.ENCODING_FRA
        )
        # European (Central)
        # e.g. Albanian, Croatian, Czech, Finnish, German, Hungarian, Polish, Romanian, Serbian (Latin), Slovak, Slovenian, Sorbian (Lower), Sorbian(Upper)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp852', 'iso8859_2', 'mac_latin2', 'cp1250'],
            text = wl_test_lang_examples.ENCODING_HRV
        )
        # European (Northern)
        # e.g. Estonian, Latvian, Lithuanian, Sámi
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'iso8859_4'
            text = wl_test_lang_examples.ENCODING_LAV
        )
        # European (Southern)
        # e.g. Esperanto, Maltese, Turkish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_3'],
            text = wl_test_lang_examples.ENCODING_MLT
        )
        # European (South-Eastern)
        # e.g. Albanian, Croatian, Hungarian, Polish, Romanian, Serbian, Slovenian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['iso8859_16'],
            text = wl_test_lang_examples.ENCODING_HRV
        )
        # European (Western)
        # e.g. Afrikaans, Albanian, Basque, English, Faroese, Galician, Icelandic, Irish, Indonesian, Italian, Luxembourgish, Malay, Manx, Norwegian, Portuguese, Scottish Gaelic, Spanish, Swahili, Swedish, Tagalog
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp500', 'cp850', 'cp1252'], # 'cp858', 'cp1140', 'latin_1', 'iso8859_15', 'mac_roman'
            text = wl_test_lang_examples.ENCODING_POR
        )
        # French
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp863'
            text = wl_test_lang_examples.ENCODING_FRA
        )
        # German
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp273'
            text = wl_test_lang_examples.ENCODING_DEU
        )
        # Greek
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp737', 'cp869', 'cp875', 'mac_greek', 'cp1253'], # 'iso8859_7'
            text = wl_test_lang_examples.ENCODING_ELL
        )
        # Hebrew
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp856', 'cp424', 'cp1255'], # 'cp862', 'iso8859_8'
            text = wl_test_lang_examples.ENCODING_HEB
        )
        # Icelandic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp861', 'mac_iceland'
            text = wl_test_lang_examples.ENCODING_ISL
        )
        # Japanese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # 'euc_jp', 'euc_jisx0213', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213'
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
            encodings = ['iso2022_kr', 'johab', 'cp949'], # 'euc_kr'
            text = wl_test_lang_examples.ENCODING_KOR
        )
        # Nordic languages
        # e.g. Danish, Faroese, Icelandic, Norwegian, Swedish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp865', 'iso8859_10'
            text = wl_test_lang_examples.ENCODING_ISL
        )
        # Persian/Urdu
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'mac_farsi'
            text = wl_test_lang_examples.ENCODING_URD
        )
        # Portuguese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp860'
            text = wl_test_lang_examples.ENCODING_POR
        )
        # Romanian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'mac_romanian'
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
            encodings = ['koi8_t'],
            text = wl_test_lang_examples.ENCODING_TGK
        )
        # Thai
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp874'], # 'iso8859_11', 'tis_620'
            text = wl_test_lang_examples.ENCODING_THA
        )
        # Turkish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp857', 'cp1254'], # 'cp1026', 'iso8859_9', 'mac_turkish'
            text = wl_test_lang_examples.ENCODING_TUR
        )
        # Ukrainian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ['cp1125', 'koi8_u'],
            text = wl_test_lang_examples.ENCODING_UKR
        )
        # Urdu
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp1006'
            text = wl_test_lang_examples.ENCODING_URD
        )
        # Vietnamese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = [], # 'cp1258'
            text = wl_test_lang_examples.ENCODING_VIE
        )
    except Exception as exc:
        raise exc
    # Clean cache
    finally:
        shutil.rmtree(test_file_dir)

def test_lingua():
    langs = {
        re.search(r'^[^\(\)]+', lang.lower()).group().strip()
        for lang in main.settings_global['langs']
    }
    langs_exceptions = {'bokmal', 'ganda', 'nynorsk'}
    langs_extra = set()

    for lang in lingua.Language.all(): # pylint: disable=no-member
        if lang.name.lower() not in langs | langs_exceptions:
            langs_extra.add(lang.name)

    assert langs_extra == {'BOSNIAN', 'MAORI', 'SHONA', 'SOMALI', 'SOTHO', 'TSONGA', 'XHOSA'}

def test_detection_lang():
    test_file_dir = 'tests/tests_utils/_files_detection_lang'

    os.makedirs(test_file_dir, exist_ok = True)

    file = {'path': f'{test_file_dir}/detect_lang_file_fallback.txt', 'encoding': 'ascii'}

    with open(file['path'], 'w', encoding = 'gb2312') as f:
        f.write('测试')

    assert wl_detection.detect_lang_file(main, file) == main.settings_custom['files']['default_settings']['lang']
    assert wl_detection.detect_lang_text(main, '\x00') == 'other'

    try:
        for lang in [
            'afr', 'sqi', 'ara', 'hye', 'aze',
            'eus', 'bel', 'ben', 'bul',
            'cat', 'zho_cn', 'zho_tw', 'hrv', 'ces',
            'dan', 'nld',
            'eng_us', 'epo', 'est',
            'fin', 'fra',
            'kat', 'deu_de', 'ell', 'guj',
            'heb', 'hin', 'hun',
            'isl', 'ind', 'gle', 'ita',
            'jpn',
            'kor', 'kaz',
            'lat', 'lav', 'lit', 'lug',
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
            file = {'path': file_path, 'encoding': 'utf_8'}
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
    test_detection_encoding()

    test_lingua()
    test_detection_lang()
