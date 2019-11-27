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
from wordless_tests import wordless_test_init
from wordless_utils import wordless_misc

def get_path(file_name):
    return wordless_misc.get_normalized_path(f'wordless_tests/files/wordless_checking/wordless_checking_file/{file_name}')

def get_file(file_name):
    file = {
        'path': get_path(file_name),
        'encoding': 'utf_8'
    }

    return file

main = wordless_test_init.Wordless_Test_Main()
main.settings_custom['files']['files_open'] = [
    get_file('duplicate.txt')
]

FILES_MISSING = [
    get_path('missing.txt')
]
FILES_EMPTY = [
    get_path('empty_txt.txt'),
    get_path('empty_txt_bom.txt'),
    get_path('empty_docx.docx')
]
FILES_DUPLICATE = [
    get_path('duplicate.txt')
]
FILES_UNSUPPORTED = [
    get_path('unsupported.unsupported')
]
FILES_PARSING_ERROR = [
    get_file('parsing_error_csv.csv'),
    get_file('parsing_error_htm.htm'),
    get_file('parsing_error_html.html'),
    get_file('parsing_error_lrc.lrc'),
    get_file('parsing_error_tmx.tmx'),
    get_file('parsing_error_xml.xml')
]
FILES_DECODING_ERROR = [
    get_file('decoding_error.txt')
]

def test_checking_file_missing():
    _, files_missing = wordless_checking_file.check_files_missing(main, FILES_MISSING)

    assert files_missing == FILES_MISSING

def test_checking_file_empty():
    _, files_empty = wordless_checking_file.check_files_empty(main, FILES_EMPTY)

    assert files_empty == FILES_EMPTY

def test_checking_file_duplicate():
    _, files_duplicate = wordless_checking_file.check_files_duplicate(main, FILES_DUPLICATE)
    
    assert files_duplicate == FILES_DUPLICATE

def test_checking_file_unsupported():
    _, files_unsupported = wordless_checking_file.check_files_unsupported(main, FILES_UNSUPPORTED)
    
    assert files_unsupported == FILES_UNSUPPORTED

def test_checking_file_parsing_error():
    _, files_parsing_error = wordless_checking_file.check_files_parsing_error(main, FILES_PARSING_ERROR)
    
    assert files_parsing_error == FILES_PARSING_ERROR

def test_checking_file_decoding_error():
    _, files_decoding_error = wordless_checking_file.check_files_decoding_error(main, FILES_DECODING_ERROR)

    assert files_decoding_error == FILES_DECODING_ERROR
