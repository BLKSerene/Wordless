# ----------------------------------------------------------------------
# Wordless: Tests - Utilities - Miscellaneous
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

import platform
import re

from wordless.wl_utils import wl_misc

def test_check_os():
    is_windows, is_macos, is_linux = wl_misc.check_os()

    if platform.system() == 'Windows':
        assert is_windows and not is_macos and not is_linux
    elif platform.system() == 'Darwin':
        assert not is_windows and is_macos and not is_linux
    elif platform.system() == 'Linux':
        assert not is_windows and not is_macos and is_linux

def test_get_linux_distro():
    assert wl_misc.get_linux_distro() in ['ubuntu', 'debian']

def test_get_wl_ver():
    assert re.search(r'^[0-9]+\.[0-9]+\.[0-9]$', wl_misc.get_wl_ver())

def test_split_ver():
    assert wl_misc.split_ver('1.2.3') == (1, 2, 3)
    assert wl_misc.split_ver('0.0.0') == (0, 0, 0)
    assert wl_misc.split_ver('10.100.1000') == (10, 100, 1000)

def test_flatten_list():
    assert list(wl_misc.flatten_list([1, 2, [3, 4, [5, 6]]])) == [1, 2, 3, 4, 5, 6]

def test_normalize_nums():
    assert wl_misc.normalize_nums([1, 2, 3, 4, 5], 0, 100) == [0, 25, 50, 75, 100]
    assert wl_misc.normalize_nums([1, 2, 3, 4, 5], 0, 100, reverse = True) == [100, 75, 50, 25, 0]

def test_merge_dicts():
    assert wl_misc.merge_dicts([{1: 10}, {1: 20, 2: 30}]) == {1: [10, 20], 2: [0, 30]}
    assert wl_misc.merge_dicts([{1: [10, 20]}, {1: [30, 40], 2: [50, 60]}]) == {1: [[10, 20], [30, 40]], 2: [[0, 0], [50, 60]]}

if __name__ == '__main__':
    test_check_os()
    test_get_linux_distro()

    test_get_wl_ver()
    test_split_ver()

    test_flatten_list()
    test_normalize_nums()
    test_merge_dicts()
