# ----------------------------------------------------------------------
# Utilities: Utilities
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

def check_os():
    is_windows = False
    is_macos = False
    is_linux = False

    if platform.system() == 'Windows':
        is_windows = True
    elif platform.system() == 'Darwin':
        is_macos = True
    elif platform.system() == 'Linux':
        is_linux = True

    return is_windows, is_macos, is_linux

def get_wl_ver():
    wl_ver = '1.0.0'

    try:
        # Version file is generated on Windows
        with open('../VERSION', 'r', encoding = 'utf_8', newline = '\r\n') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    wl_ver = line.strip()

                    break
    except (FileNotFoundError, PermissionError):
        pass

    return wl_ver
