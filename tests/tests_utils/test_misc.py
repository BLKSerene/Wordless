# ----------------------------------------------------------------------
# Tests: Utilities - Miscellaneous
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
import platform
import re

from tests import wl_test_init
from wordless.wl_utils import wl_misc

main = wl_test_init.Wl_Test_Main()

def test_check_os():
    is_windows, is_macos, is_linux = wl_misc.check_os()

    if platform.system() == 'Windows':
        assert is_windows and not is_macos and not is_linux
    elif platform.system() == 'Darwin':
        assert not is_windows and is_macos and not is_linux
    elif platform.system() == 'Linux':
        assert not is_windows and not is_macos and is_linux

def test_get_linux_distro():
    assert wl_misc.get_linux_distro() == 'ubuntu'

def test_change_file_owner_to_user():
    with open('test', 'wb'):
        pass

    wl_misc.change_file_owner_to_user('test')

    os.remove('test')

def test_find_wl_main():
    class Widget:
        def parent(self):
            return main

    widget = Widget()
    widget.main = 'test'

    assert wl_misc.find_wl_main(widget) == 'test'

    del widget.main

    assert wl_misc.find_wl_main(widget) == main

def test_get_wl_ver():
    assert re.search(r'^[0-9]+\.[0-9]+\.[0-9]$', str(wl_misc.get_wl_ver()))

def test_wl_get_proxies():
    proxy_settings = main.settings_custom['general']['proxy_settings']

    proxy_settings['use_proxy'] = False
    assert wl_misc.wl_get_proxies(main) is None

    proxy_settings['use_proxy'] = True
    proxy_settings['username'] = 'username'
    proxy_settings['password'] = 'password'
    proxy_settings['address'] = 'address'
    proxy_settings['port'] = 'port'

    assert wl_misc.wl_get_proxies(main) == {'http': 'http://username:password@address:port', 'https': 'http://username:password@address:port'}

    proxy_settings['username'] = ''
    assert wl_misc.wl_get_proxies(main) == {'http': 'http://address:port', 'https': 'http://address:port'}

    # Clear proxies settings
    proxy_settings['use_proxy'] = False

URL_VER = 'https://raw.githubusercontent.com/BLKSerene/Wordless/main/VERSION'

def test_wl_download():
    r, err_msg = wl_misc.wl_download(main, URL_VER)

    assert r
    assert not err_msg

    r, err_msg = wl_misc.wl_download(main, 'https://raw.githubusercontent.com/BLKSerene/Wordless/main/test')

    assert r.status_code == 404
    assert err_msg

    r, err_msg = wl_misc.wl_download(main, 'test')

    assert r is None
    assert err_msg

def test_wl_download_file_size():
    assert wl_misc.wl_download_file_size(main, URL_VER)
    assert wl_misc.wl_download_file_size(main, 'test') == 0

def test_flatten_list():
    assert list(wl_misc.flatten_list([1, 2, [3, 4, [5, 6]]])) == [1, 2, 3, 4, 5, 6]

def test_merge_dicts():
    assert wl_misc.merge_dicts([{1: 10}, {1: 20, 2: 30}]) == {1: [10, 20], 2: [0, 30]}
    assert wl_misc.merge_dicts([{1: [10, 20]}, {1: [30, 40], 2: [50, 60]}]) == {1: [[10, 20], [30, 40]], 2: [[0, 0], [50, 60]]}

def test_normalize_nums():
    assert wl_misc.normalize_nums([1, 2, 3, 4, 5], 0, 100) == [0, 25, 50, 75, 100]
    assert wl_misc.normalize_nums([1, 2, 3, 4, 5], 0, 100, reverse = True) == [100, 75, 50, 25, 0]
    assert wl_misc.normalize_nums([1, 1, 1, 1, 1], 0, 100) == [50] * 5
    assert wl_misc.normalize_nums([1, 2, 3, 4, 5], 0, 0) == [0] * 5

if __name__ == '__main__':
    test_check_os()
    test_get_linux_distro()
    test_change_file_owner_to_user()

    test_find_wl_main()
    test_get_wl_ver()
    test_wl_get_proxies()
    test_wl_download()
    test_wl_download_file_size()

    test_flatten_list()
    test_merge_dicts()
    test_normalize_nums()
