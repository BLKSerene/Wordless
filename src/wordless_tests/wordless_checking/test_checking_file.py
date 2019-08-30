#
# Wordless: Tests - Checking - File
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import sys

sys.path.append('.')

from wordless_checking import wordless_checking_file
from wordless_tests import test_init

def get_path(file_name):
    return os.path.normpath(f'wordless_tests/files/checking/{file_name}')

main = test_init.Test_Main()
main.settings_custom['files']['files_open'] = [
    {
        'path': get_path('duplicate.txt')
    }
]
# Disable encoding detection
main.settings_custom['files']['auto_detection_settings']['detect_encodings'] = False

TEST_CHECKING_FILE_MISSING = [get_path('missing.txt')]
TEST_CHECKING_FILE_EMPTY = [get_path('empty.txt')]
TEST_CHECKING_FILE_DUPLICATE = [get_path('duplicate.txt')]
TEST_CHECKING_FILE_UNSUPPORTED = [get_path('unsupported.unsupported')]
TEST_CHECKING_FILE_PARSING_ERROR = [get_path('parsing_error.html')]
TEST_CHECKING_FILE_LOADING_ERROR = [get_path('loading_error.txt')]

def test_checking_file_missing():
    _, files_missing = wordless_checking_file.check_files_missing(main, TEST_CHECKING_FILE_MISSING)
    
    assert files_missing == TEST_CHECKING_FILE_MISSING

def test_checking_file_empty():
    _, files_empty = wordless_checking_file.check_files_empty(main, TEST_CHECKING_FILE_EMPTY)
    
    assert files_empty == TEST_CHECKING_FILE_EMPTY

def test_checking_file_duplicate():
    _, files_duplicate = wordless_checking_file.check_files_duplicate(main, TEST_CHECKING_FILE_DUPLICATE)
    
    assert files_duplicate == TEST_CHECKING_FILE_DUPLICATE

def test_checking_file_unsupported():
    _, files_unsupported = wordless_checking_file.check_files_unsupported(main, TEST_CHECKING_FILE_UNSUPPORTED)
    
    assert files_unsupported == TEST_CHECKING_FILE_UNSUPPORTED

def test_checking_file_parsing_error():
    _, files_parsing_error = wordless_checking_file.check_files_parsing_error(main, TEST_CHECKING_FILE_PARSING_ERROR)
    
    assert files_parsing_error == TEST_CHECKING_FILE_PARSING_ERROR

def test_checking_file_loading_error():
    _, files_loading_error = wordless_checking_file.check_files_loading_error(main, TEST_CHECKING_FILE_LOADING_ERROR,
                                                                                       encodings = ['utf_8'])
    
    assert files_loading_error == TEST_CHECKING_FILE_LOADING_ERROR
