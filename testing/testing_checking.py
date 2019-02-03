#
# Wordless: Testing for Checking
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import sys

from PyQt5.QtCore import *

sys.path.append('E:/Wordless')

import wordless_files

from wordless_checking import wordless_checking_file
from wordless_settings import init_settings_default, init_settings_global

main = QObject()
table = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default
table.main = main

main.wordless_files = wordless_files.Wordless_Files(table)

main.settings_custom['files']['files_open'] = [{'path': os.path.realpath('testing/Checking/Duplicate.txt')}]
# Disable encoding detection
main.settings_custom['files']['auto_detection_settings']['detect_encodings'] = False

file_paths = [
    os.path.realpath('testing/Checking/Missing.txt'),
    os.path.realpath('testing/Checking/Empty.txt'),
    os.path.realpath('testing/Checking/Duplicate.txt'),
    os.path.realpath('testing/Checking/Unsupported.unsupported'),
    os.path.realpath('testing/Checking/Encoding Error.html'),
    os.path.realpath('testing/Checking/Loading Error.txt')
]

file_paths, files_missing = wordless_checking_file.check_files_missing(main, file_paths)
file_paths, files_empty = wordless_checking_file.check_files_empty(main, file_paths)
file_paths, files_duplicate = wordless_checking_file.check_files_duplicate(main, file_paths)
file_paths, files_unsupported = wordless_checking_file.check_files_unsupported(main, file_paths)
file_paths, files_encoding_error = wordless_checking_file.check_files_encoding_error(main, file_paths)
file_paths, files_loading_error = wordless_checking_file.check_files_loading_error(main, file_paths, ['utf_8'] * len(file_paths))

print(f'Missing file(s): {files_missing}')
print(f'Empty file(s): {files_empty}')
print(f'Duplicate file(s): {files_duplicate}')
print(f'Unsupported file(s): {files_unsupported}')
print(f'File(s) with encoding error during opening: {files_encoding_error}')
print(f'File(s) with encoding error during loading: {files_loading_error}')
