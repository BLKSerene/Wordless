# ----------------------------------------------------------------------
# Wordless: Utilities - Paths
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

def get_normalized_path(path):
    path = os.path.realpath(path)
    path = os.path.normpath(path)

    return path

def get_normalized_dir(path):
    path = get_normalized_path(path)

    return os.path.dirname(path)

def _get_path(dir_name, file_name):
    path = os.path.join(dir_name, file_name)

    return get_normalized_path(path)

def get_path_data(file_name):
    return _get_path('data', file_name)

def get_path_img(file_name):
    return _get_path('imgs', file_name)
