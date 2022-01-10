# ----------------------------------------------------------------------
# Wordless: Tests - Checking - File
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

import os
import sys

sys.path.append('.')

from wl_checking import wl_checking_file
from wl_utils import wl_misc
from wl_tests import wl_test_init

def get_normalized_file_path(file_name):
    return wl_misc.get_normalized_path(f'wl_tests_files/wl_checking/wl_checking_file/{file_name}')

main = wl_test_init.Wl_Test_Main()
main.settings_custom['file_area']['files_open'] = [
    {
        'path_original': get_normalized_file_path('duplicate.txt')
    }
]

FILE_PATHS_UNSUPPORTED = [
    get_normalized_file_path('unsupported_file_type.unsupported')
]
FILE_PATHS_EMPTY = [
    get_normalized_file_path('empty_txt.txt'),
    get_normalized_file_path('empty_docx.docx')
]
FILE_PATHS_DUPLICATE = [
    get_normalized_file_path('duplicate.txt')
]

def test_check_file_paths_unsupported():
    _, files_unsupported = wl_checking_file.check_file_paths_unsupported(main, FILE_PATHS_UNSUPPORTED)

    assert files_unsupported == FILE_PATHS_UNSUPPORTED

def test_check_file_paths_empty():
    _, files_empty = wl_checking_file.check_file_paths_empty(main, FILE_PATHS_EMPTY)

    assert files_empty == FILE_PATHS_EMPTY

def test_check_file_paths_duplicate():
    _, files_duplicate = wl_checking_file.check_file_paths_duplicate(main, FILE_PATHS_DUPLICATE)
    
    assert files_duplicate == FILE_PATHS_DUPLICATE

if __name__ == '__main__':
    test_check_file_paths_unsupported()
    test_check_file_paths_empty()
    test_check_file_paths_duplicate()
