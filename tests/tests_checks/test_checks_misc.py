# ----------------------------------------------------------------------
# Tests: Checks - Miscellaneous
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
import shutil

from wordless.wl_checks import wl_checks_misc

def test_check_custom_settings():
    settings_custom = settings_default = {
        'key_1': 'val_2',
        'key_2': {
            'key_3': 'val_3',
            'key_4': 'val_4'
        }
    }

    assert wl_checks_misc.check_custom_settings(settings_custom, settings_default)
    assert not wl_checks_misc.check_custom_settings(settings_custom, {})

def test_check_dir():
    if os.path.exists('temp'):
        shutil.rmtree('temp')

    wl_checks_misc.check_dir('temp')

    assert os.path.exists('temp')

    os.rmdir('temp')

def test_check_new_name():
    assert wl_checks_misc.check_new_name('new_name', ['new_name', 'new_name (2)', 'new_name (4)']) == 'new_name (3)'
    assert wl_checks_misc.check_new_name(
        'new_name', ['new_name', 'new_name (2)', 'new_name (4)'],
        separator = '/'
    ) == 'new_name/2'

def test_check_new_path():
    if os.path.exists('temp'):
        shutil.rmtree('temp')

    os.mkdir('temp')

    for file_name in ['temp', 'temp (2)', 'temp (4)']:
        with open(f'temp/{file_name}.temp', 'w', encoding = 'utf_8'):
            pass

    assert wl_checks_misc.check_new_path('temp/temp.temp') == 'temp/temp (3).temp'

    shutil.rmtree('temp')

if __name__ == '__main__':
    test_check_custom_settings()
    test_check_dir()
    test_check_new_name()
    test_check_new_path()
