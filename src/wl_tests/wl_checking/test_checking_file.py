#
# Wordless: Tests - Checking - File
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

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
