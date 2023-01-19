# ----------------------------------------------------------------------
# Wordless: Tests - Utilities - Paths
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

from wordless.wl_utils import wl_paths

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

def test__get_path():
    assert 'a' + os.path.sep + 'b' in wl_paths._get_path('a', 'b')

def test_get_path_data():
    assert 'data' + os.path.sep + 'a' in wl_paths.get_path_data('a')

def test_get_path_img():
    assert 'imgs' + os.path.sep + 'a' in wl_paths.get_path_img('a')

if __name__ == '__main__':
    test_get_normalized_path()
    test_get_normalized_dir()

    test__get_path()
    test_get_path_data()
    test_get_path_img()
