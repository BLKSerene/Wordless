# ----------------------------------------------------------------------
# Tests: Utilities - Paths
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
import sys

from wordless.wl_utils import wl_paths, wl_misc

def test_get_normalized_path():
    assert wl_paths.get_normalized_path('.') != '.'
    assert wl_paths.get_normalized_path('/')
    assert wl_paths.get_normalized_path('a') != 'a'
    assert wl_paths.get_normalized_path('a/b/c') != 'a/b/c'

def test_get_normalized_dir():
    assert wl_paths.get_normalized_dir('.') != '.'
    assert wl_paths.get_normalized_dir('/')
    assert wl_paths.get_normalized_dir('a') != 'a'
    assert wl_paths.get_normalized_dir('a/b/c') != 'a/b/c'

def test_get_path_file():
    assert wl_paths.get_path_file('')
    assert wl_paths.get_path_file('a', 'b', 'c').endswith(os.path.sep.join(['a', 'b', 'c']))
    assert wl_paths.get_path_file('a', '..', 'b').endswith('b')

    sys._MEIPASS = 'test'

    assert wl_paths.get_path_file('a', internal = True).endswith(os.path.sep.join(['test', 'a']))
    assert wl_paths.get_path_file('a', internal = False).endswith('a')

    check_os_orig = wl_misc.check_os
    wl_misc.check_os = lambda: (False, True, False)

    assert wl_paths.get_path_file('a', internal = False).endswith(os.path.sep.join(['MacOS', 'a']))

    wl_misc.check_os = check_os_orig
    del sys._MEIPASS

def test_get_path_data():
    assert wl_paths.get_path_data('a').endswith(os.path.sep.join(['data', 'a']))

def test_get_path_img():
    assert wl_paths.get_path_img('a').endswith(os.path.sep.join(['imgs', 'a']))

if __name__ == '__main__':
    test_get_normalized_path()
    test_get_normalized_dir()

    test_get_path_file()
    test_get_path_data()
    test_get_path_img()
