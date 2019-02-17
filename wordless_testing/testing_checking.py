"show_line_endings": false,#
# Wordless: Testing - Checking
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

from wordless_testing import testing_init
from wordless_checking import wordless_checking_file

def get_path(file_name):
	return f'wordless_testing/files/checking/{file_name}'

main = testing_init.Testing_Main()

main.settings_custom['files']['files_open'] = [
	{
	    'path': get_path('duplicate.txt')
	}
]

# Disable encoding detection
main.settings_custom['files']['auto_detection_settings']['detect_encodings'] = False

file_paths = [
    get_path('missing.txt'),
    get_path('empty.txt'),
    get_path('duplicate.txt'),
    get_path('unsupported.unsupported'),
    get_path('parsing_error.html'),
    get_path('loading_error.txt')
]

file_paths, files_missing = wordless_checking_file.check_files_missing(main, file_paths)
file_paths, files_empty = wordless_checking_file.check_files_empty(main, file_paths)
file_paths, files_duplicate = wordless_checking_file.check_files_duplicate(main, file_paths)
file_paths, files_unsupported = wordless_checking_file.check_files_unsupported(main, file_paths)
file_paths, files_parsing_error = wordless_checking_file.check_files_parsing_error(main, file_paths)
file_paths, files_loading_error = wordless_checking_file.check_files_loading_error(main, file_paths, ['utf_8'] * len(file_paths))

print(f'Missing file(s): {files_missing}')
print(f'Empty file(s): {files_empty}')
print(f'Duplicate file(s): {files_duplicate}')
print(f'Unsupported file(s): {files_unsupported}')
print(f'File(s) with parsing error(s): {files_parsing_error}')
print(f'File(s) with encoding error(s): {files_loading_error}')
