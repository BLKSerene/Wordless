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

from tests import (
    wl_test_init,
    wl_test_lang_examples
)
from wordless.wl_utils import (
    wl_conversion,
    wl_detection
)

main = wl_test_init.Wl_Test_Main()

def check_encodings_detected(test_file_dir, encodings, lang):
    encodings_detected = []

    if f'ENCODING_{lang.upper()}' in wl_test_lang_examples.__dict__:
        text = wl_test_lang_examples.__dict__[f'ENCODING_{lang.upper()}']
    else:
        text = ''.join(wl_test_lang_examples.__dict__[f'TEXT_{lang.upper()}'])

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

    assert tuple(encodings_detected) == encodings

def test_detection_encoding():
    test_file_dir = 'tests/tests_utils/_files_detection_encoding'

    os.makedirs(test_file_dir, exist_ok = True)

    with open(f'{test_file_dir}/test.exe', 'wb') as f:
        f.write(b'\xFF\x00\x00')

    assert wl_detection.detect_encoding(main, f'{test_file_dir}/test.exe') == 'utf_8'

    try:
        # All languages
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('utf_8', 'utf_8_sig', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_32', 'utf_32_be', 'utf_32_le'), # 'utf_7'
            lang = 'fra'
        )
        # Arabic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp720', 'iso8859_6', 'cp1256'), # 'cp864', 'mac_arabic'
            lang = 'ara'
        )
        # Baltic languages
        # e.g. Lithuanian, Latvian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp775',), # 'iso8859_13', 'cp1257'
            lang = 'lav'
        )
        # Celtic languages
        # e.g. Irish, Manx, Scottish Gaelic, Welsh
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'iso8859_14'
            lang = 'gle'
        )
        # Chinese (Unified)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('gb18030',), # 'gbk'
            lang = 'zho_tw'
        )
        # Chinese (Simplified)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'gb2312', 'hz'
            lang = 'zho_cn'
        )
        # Chinese (Traditional)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('big5',), # 'big5hkscs', 'cp950'
            lang = 'zho_tw'
        )
        # Croatian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'mac_croatian'
            lang = 'hrv'
        )
        # Cyrillic
        # e.g. Belarusian, Bulgarian, Macedonian, Russian, Serbian (Cyrillic script)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp855', 'cp1251', 'iso8859_5', 'mac_cyrillic'), # 'cp866'
            lang = 'rus'
        )
        # English
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('ascii', 'cp037'), # 'cp437'
            lang = 'eng_us'
        )
        # European
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('hp_roman8',),
            lang = 'fra'
        )
        # European (Central)
        # e.g. Albanian, Croatian, Czech, Finnish, German, Hungarian, Polish, Romanian, Serbian (Latin), Slovak, Slovenian, Sorbian (Lower), Sorbian(Upper)
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp852', 'iso8859_2', 'mac_latin2', 'cp1250'),
            lang = 'hrv'
        )
        # European (Northern)
        # e.g. Estonian, Latvian, Lithuanian, Sámi
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'iso8859_4'
            lang = 'lav'
        )
        # European (Southern)
        # e.g. Esperanto, Maltese, Turkish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('iso8859_3',),
            lang = 'mlt'
        )
        # European (South-Eastern)
        # e.g. Albanian, Croatian, Hungarian, Polish, Romanian, Serbian, Slovenian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('iso8859_16',),
            lang = 'pol'
        )
        # European (Western)
        # e.g. Afrikaans, Albanian, Basque, English, Faroese, Galician, Icelandic, Irish, Indonesian, Italian, Luxembourgish, Malay, Manx, Norwegian, Portuguese, Scottish Gaelic, Spanish, Swahili, Swedish, Tagalog
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp500', 'cp850', 'cp1252'), # 'cp858', 'cp1140', 'latin_1', 'iso8859_15', 'mac_roman'
            lang = 'por'
        )
        # French
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'cp863'
            lang = 'fra'
        )
        # German
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'cp273'
            lang = 'deu'
        )
        # Greek
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp737', 'cp869', 'cp875', 'cp1253', 'mac_greek'), # 'iso8859_7'
            lang = 'ell'
        )
        # Hebrew
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp856', 'cp424', 'cp1255'), # 'cp862', 'iso8859_8'
            lang = 'heb'
        )
        # Icelandic
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'cp861', 'mac_iceland'
            lang = 'isl'
        )
        # Japanese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            # 'euc_jp', 'euc_jisx0213', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213'
            encodings = ('cp932', 'euc_jis_2004', 'iso2022_jp'),
            lang = 'jpn'
        )
        # Kazakh
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('kz1048', 'ptcp154'),
            lang = 'kaz'
        )
        # Korean
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('iso2022_kr', 'johab', 'cp949'), # 'euc_kr'
            lang = 'kor'
        )
        # Nordic languages
        # e.g. Danish, Faroese, Icelandic, Norwegian, Swedish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'cp865', 'iso8859_10'
            lang = 'isl'
        )
        # Persian/Urdu
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'mac_farsi'
            lang = 'fas'
        )
        # Portuguese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'cp860'
            lang = 'por'
        )
        # Romanian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = (), # 'mac_romanian'
            lang = 'ron'
        )
        # Russian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('koi8_r',),
            lang = 'rus'
        )
        # Tajik
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('koi8_t',),
            lang = 'tgk'
        )
        # Thai
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp874',), # 'iso8859_11', 'tis_620'
            lang = 'tha'
        )
        # Turkish
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp857', 'cp1254'), # 'cp1026', 'iso8859_9', 'mac_turkish'
            lang = 'tur'
        )
        # Ukrainian
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp1125', 'koi8_u'),
            lang = 'ukr'
        )
        # Urdu
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp1006',),
            lang = 'urd'
        )
        # Vietnamese
        check_encodings_detected(
            test_file_dir = test_file_dir,
            encodings = ('cp1258',),
            lang = 'vie'
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
    langs_excs = {'bokmal', 'nynorsk', 'punjabi', 'slovene'}
    langs_extra = set()

    for lang in lingua.Language.all(): # pylint: disable=no-member
        if lang.name.lower() not in langs | langs_excs:
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
        for lang in (
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
            'kaz', 'kor',
            'lat', 'lav', 'lit',
            'mkd', 'mar', 'mon_cyrl', # 'msa',
            'nno', # 'nob',
            'pan_guru', 'fas', 'pol', 'por_pt',
            'ron', 'rus',
            'srp_cyrl', 'slk', 'slv', 'spa', 'swa', 'swe',
            'tgl', 'tam', 'tel', 'tha', 'tsn', 'tur',
            'ukr', 'urd',
            'vie',
            'cym',
            'yor',
            'zul'
        ):
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
