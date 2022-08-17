# ----------------------------------------------------------------------
# Wordless: Tests - Utilities - Detection
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

import glob
import os
import re

import lingua
import pytest

from tests import wl_test_init
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

    assert langs_extra == ['BOSNIAN', 'GANDA', 'GEORGIAN', 'MAORI', 'SHONA', 'TSONGA', 'XHOSA']

# Encoding detection
@pytest.mark.parametrize('file_path', glob.glob('tests/files/wl_utils/wl_detection/encoding/*.txt'))
def test_detection_encoding(file_path):
    file_name = os.path.basename(file_path)

    print(f'Detecting encoding for file "{file_name}"... ', end = '')

    encoding_code = wl_detection.detect_encoding(main, file_path)
    encoding_code_file = re.search(r'(?<=\()[^\(\)]+?(?=\)\.txt)', file_name).group()

    print(f'Detected: {encoding_code}')

    assert encoding_code == encoding_code_file

# Language detection
@pytest.mark.parametrize('file_path', glob.glob('tests/files/wl_utils/wl_detection/lang/*.txt'))
def test_detection_lang(file_path):
    file = {}

    file['path'] = file_path
    file['encoding'] = 'utf_8'

    file_name = os.path.basename(file_path)

    print(f'Detecting language for file "{file_name}"... ', end = '')

    lang_code_file = wl_detection.detect_lang_file(main, file)

    with open(file['path'], 'r', encoding = file['encoding']) as f:
        text = f.read()

    lang_code_text = wl_detection.detect_lang_text(main, text)

    print(f'Detected: {lang_code_file}/{lang_code_text}')

    assert lang_code_file == lang_code_text == file_name.replace('.txt', '')

if __name__ == '__main__':
    test_lingua()

    for file in glob.glob('tests/files/wl_utils/wl_detection/encoding/*.txt'):
        test_detection_encoding(file)

    for file in glob.glob('tests/files/wl_utils/wl_detection/lang/*.txt'):
        test_detection_lang(file)
