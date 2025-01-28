# ----------------------------------------------------------------------
# Wordless: Checks - Miscellaneous
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
import pathlib

def check_custom_settings(settings_custom, settings_default):
    def get_keys(settings, keys):
        for key, value in settings.items():
            keys.append(key)

            if isinstance(value, dict):
                get_keys(value, keys)

        return keys

    keys_custom = []
    keys_default = []

    keys_custom = get_keys(settings_custom, keys_custom)
    keys_default = get_keys(settings_default, keys_default)

    return bool(keys_custom == keys_default)

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        pathlib.Path(dir_name).mkdir(parents = True, exist_ok = True)

    return dir_name

def check_new_name(new_name, names, separator = None):
    i = 2
    names = set(names)

    if new_name in names:
        while True:
            if separator is None:
                new_name_valid = f'{new_name} ({i})'
            else:
                new_name_valid = f'{new_name}{separator}{i}'

            if new_name_valid in names:
                i += 1
            else:
                break
    else:
        new_name_valid = new_name

    return new_name_valid

def check_new_path(new_path):
    i = 2

    if os.path.exists(new_path) and os.path.isfile(new_path):
        while True:
            path_head, ext = os.path.splitext(new_path)
            new_path_valid = f'{path_head} ({i}){ext}'

            if os.path.exists(new_path_valid) and os.path.isfile(new_path_valid):
                i += 1
            else:
                break
    else:
        new_path_valid = new_path

    # Placeholder for the new path
    with open(new_path_valid, 'wb') as _:
        pass

    return new_path_valid
