#
# Wordless: Tests - Initialization
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import sys

from PyQt5.QtCore import *

sys.path.append('.')

import wl_file_area
from wl_settings import wl_settings_default, wl_settings_global

class Wl_Test_Main(QObject):
    def __init__(self):
        super().__init__()

        # Settings
        wl_settings_default.init_settings_default(self)
        self.settings_custom = self.settings_default
        wl_settings_global.init_settings_global(self)

        # Files
        table = QObject()
        table.main = self

        self.wl_files = wl_file_area.Wl_Files(table)

    def height(self):
        return 768
