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

if platform.system() in ['Windows', 'Darwin']:
    wl_app = QApplication(sys.argv)

    class Wl_Test_Main(QWidget):
        def __init__(self):
            super().__init__()

            self.app = wl_app

            # Default settings
            wl_settings_default.init_settings_default(self)
            
            # Custom settings
            if os.path.exists('wl_tests/wl_settings.pickle'):
                with open('wl_tests/wl_settings.pickle', 'rb') as f:
                    self.settings_custom = pickle.load(f)
            else:
                self.settings_custom = copy.deepcopy(self.settings_default)

            # Global settings
            wl_settings_global.init_settings_global(self)

            # Files
            table = QWidget()
            table.main = self

            self.wl_files = wl_file_area.Wl_Files(table)

        def height(self):
            return 768
# Do not initialize QApplication on Linux during CI
elif platform.system() == 'Linux':
    class Wl_Test_Main(QObject):
        def __init__(self):
            super().__init__()

            # Settings
            wl_settings_default.init_settings_default(self)
            self.settings_custom = copy.deepcopy(self.settings_default)
            wl_settings_global.init_settings_global(self)

            # Files
            table = QObject()
            table.main = self

            self.wl_files = wl_file_area.Wl_Files(table)

        def height(self):
            return 768
