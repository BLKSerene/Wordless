# ----------------------------------------------------------------------
# Tests: Checks - Files
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

from tests import wl_test_init
from wordless.wl_checks import wl_checks_files
from wordless.wl_utils import wl_paths

def get_normalized_file_path(file_name):
    return wl_paths.get_normalized_path(f'tests/files/wl_checks/wl_checks_files/{file_name}')

main = wl_test_init.Wl_Test_Main()
main.settings_custom['file_area']['files_open'] = [
    {
        'path_orig': get_normalized_file_path('dup.txt')
    }
]

FILE_PATHS_UNSUPPORTED = [
    get_normalized_file_path('unsupported.unsupported')
]
FILE_PATHS_EMPTY = [
    get_normalized_file_path('empty_txt.txt'),
    get_normalized_file_path('empty_docx.docx')
]
FILE_PATHS_DUP = [
    get_normalized_file_path('dup.txt'),
    get_normalized_file_path('dup.xml'),
    get_normalized_file_path('dup.xml')
]

def test_check_file_paths_unsupported():
    _, files_unsupported = wl_checks_files.check_file_paths_unsupported(main, ['supported.txt'] + FILE_PATHS_UNSUPPORTED)

    assert files_unsupported == FILE_PATHS_UNSUPPORTED

def test_check_file_paths_empty():
    _, files_empty = wl_checks_files.check_file_paths_empty(main, [FILE_PATHS_DUP[0]] + FILE_PATHS_EMPTY)

    assert files_empty == FILE_PATHS_EMPTY

def test_check_file_paths_duplicate():
    _, files_dup = wl_checks_files.check_file_paths_dup(main, FILE_PATHS_DUP)

    assert files_dup == FILE_PATHS_DUP[:2]

def test_check_err_file_area():
    assert wl_checks_files.check_err_file_area(main, '')

if __name__ == '__main__':
    test_check_file_paths_unsupported()
    test_check_file_paths_empty()
    test_check_file_paths_duplicate()

    test_check_err_file_area()
