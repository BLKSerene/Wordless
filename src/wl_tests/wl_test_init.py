# ----------------------------------------------------------------------
# Wordless: Tests - Initialization
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

import copy
import os
import pickle
import platform
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from wl_settings import wl_settings_default, wl_settings_global

import wl_file_area

# Chinese (Traditional), English, French, German, Greek, Italian, Japanese, Russian, Spanish
SEARCH_TERMS = ['是', 'be', 'être', 'sein', 'είναι', 'essere', 'は', 'быть', 'esta']

if platform.system() in ['Windows', 'Darwin']:
    wl_app = QApplication(sys.argv)

    class Wl_Test_Main(QWidget):
        def __init__(self):
            super().__init__()

            self.app = wl_app

            # Default settings
            self.settings_default = wl_settings_default.init_settings_default(self)

            # Custom settings
            if os.path.exists('wl_tests/wl_settings.pickle'):
                with open('wl_tests/wl_settings.pickle', 'rb') as f:
                    self.settings_custom = pickle.load(f)
            else:
                self.settings_custom = copy.deepcopy(self.settings_default)

            # Global settings
            self.settings_global = wl_settings_global.init_settings_global()

            # Files
            self.wl_file_area = QObject()
            self.wl_file_area.main = self

            self.wl_file_area.get_selected_files = lambda: wl_file_area.Wrapper_File_Area.get_selected_files(self.wl_file_area)
            self.wl_file_area.get_selected_file_names = lambda: wl_file_area.Wrapper_File_Area.get_selected_file_names(self.wl_file_area)
            self.wl_file_area.find_file_by_name = lambda file_name, selected_only = False: wl_file_area.Wrapper_File_Area.find_file_by_name(self.wl_file_area, file_name, selected_only)
            self.wl_file_area.find_files_by_name = lambda file_names, selected_only = False: wl_file_area.Wrapper_File_Area.find_files_by_name(self.wl_file_area, file_names, selected_only)

        def height(self):
            return 768
# Do not initialize QApplication on Linux during CI
elif platform.system() == 'Linux':
    class Wl_Test_Main(QObject):
        def __init__(self):
            super().__init__()

            # Settings
            self.settings_default = wl_settings_default.init_settings_default(self)
            self.settings_custom = copy.deepcopy(self.settings_default)
            self.settings_global = wl_settings_global.init_settings_global()

        def height(self):
            return 768
