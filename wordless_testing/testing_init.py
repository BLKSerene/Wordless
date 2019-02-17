#
# Wordless: Testing - Initialization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
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

import wordless_file_area

from wordless_settings import init_settings_default, init_settings_global

class Testing_Main(QObject):
    def __init__(self):
        super().__init__()

        # Settings
        init_settings_default.init_settings_default(self)
        init_settings_global.init_settings_global(self)

        self.settings_custom = self.settings_default

        # Files
        table = QObject()
        table.main = self

        self.wordless_files = wordless_file_area.Wordless_Files(table)
