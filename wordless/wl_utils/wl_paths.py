# ----------------------------------------------------------------------
# Wordless: Utilities - Paths
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

from wordless.wl_utils import wl_misc

def get_normalized_path(path):
    path = os.path.realpath(path)
    path = os.path.normpath(path)

    return path

def get_normalized_dir(path):
    path = get_normalized_path(path)

    return os.path.dirname(path)

def get_path_file(*paths, internal = True):
    if getattr(sys, '_MEIPASS', False):
        if internal:
            path = os.path.join(sys._MEIPASS, *paths)
        else:
            is_windows, is_macos, is_linux = wl_misc.check_os()

            if is_windows or is_linux:
                path = os.path.join(sys._MEIPASS, '..', *paths)
            elif is_macos:
                path = os.path.join(sys._MEIPASS, '..', 'MacOS', *paths)
    else:
        path = os.path.join(*paths)

    return get_normalized_path(path)

def get_path_data(*paths):
    return get_path_file('data', *paths)

def get_path_img(*paths):
    return get_path_file('imgs', *paths)
