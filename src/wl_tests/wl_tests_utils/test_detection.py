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

import pytest

from wl_tests import wl_test_init
from wl_utils import wl_detection

main = wl_test_init.Wl_Test_Main()
main.settings_custom['files']['auto_detection_settings']['number_lines_no_limit'] = True

# Encoding detection
@pytest.mark.parametrize('file_path', glob.glob('wl_tests_files/wl_utils/wl_detection/encoding/*.txt'))
def test_detection_encoding(file_path):
    file_name = os.path.basename(file_path)

    print(f'Detecting encoding for file "{file_name}"... ', end = '')

    encoding_code = wl_detection.detect_encoding(main, file_path)
    encoding_code_file = re.search(r'(?<=\()[^\(\)]+?(?=\)\.txt)', file_name).group()

    print(encoding_code)

    assert encoding_code == encoding_code_file

# Language detection
@pytest.mark.parametrize('file_path', glob.glob('wl_tests_files/wl_utils/wl_detection/lang/*.txt'))
def test_detection_lang(file_path):
    file = {}

    file['path'] = file_path
    file['encoding'] = 'utf_8'

    file_name = os.path.basename(file_path)

    print(f'Detecting language for file "{file_name}"... ', end = '')

    lang_code = wl_detection.detect_lang(main, file)

    print(lang_code)

    assert lang_code == file_name.replace('.txt', '')

if __name__ == '__main__':
    for file in glob.glob('wl_tests_files/wl_utils/wl_detection/encoding/*.txt'):
        test_detection_encoding(file)

    for file in glob.glob('wl_tests_files/wl_utils/wl_detection/lang/*.txt'):
        test_detection_lang(file)
