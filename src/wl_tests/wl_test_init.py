#
# Wordless: Tests - Initialization
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import os
import pickle
import platform
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append('.')

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
