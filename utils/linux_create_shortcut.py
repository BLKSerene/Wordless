# ----------------------------------------------------------------------
# Utilities: Linux - Create Shortcut
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
import subprocess

import wl_utils

wl_ver = wl_utils.get_wl_ver()

path_wl = os.path.split(globals()['__file__'])[0]
path_icon = os.path.join(path_wl, 'imgs', 'wl_icon.ico')
path_desktop = os.path.expanduser('~/.local/share/applications/Wordless.desktop')

# Reference: https://askubuntu.com/a/680699
with open(path_desktop, 'w', encoding = 'utf_8') as f:
    f.write(f'''
        [Desktop Entry]
        Type=Application
        Name=Wordless
        Version={wl_ver}
        Encoding=UTF-8
        Path={path_wl}
        Exec=bash -c "./Wordless.sh; $SHELL"
        Icon={path_icon}
        Terminal=true
    ''')

# Allow excuting file as program
subprocess.run(['chmod', '+x', path_desktop], check = True)
