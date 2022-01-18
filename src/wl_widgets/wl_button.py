# ----------------------------------------------------------------------
# Wordless: Widgets - Button
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
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_msg_boxes
from wl_utils import wl_misc

class Wl_Button(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wl_misc.find_wl_main(parent)

class Wl_Button_Restore_Default_Settings(Wl_Button):
    def __init__(self, parent):
        # Pad with spaces
        super().__init__(parent.tr(' Restore default settings '), parent)

        self.parent = parent

        self.clicked.connect(self.restore_default_settings)

    def restore_default_settings(self):
        if wl_msg_boxes.wl_msg_box_restore_default_settings(self.main):
            self.parent.load_settings(defaults = True)

        self.parent.activateWindow()

class Wl_Button_Reset_All_Settings(Wl_Button):
    def __init__(self, parent):
        # Pad with spaces
        super().__init__(parent.tr(' Reset All Settings '), parent)

        self.parent = parent

        self.clicked.connect(self.reset_settings)

    def reset_settings(self):
        if wl_msg_boxes.wl_msg_box_reset_all_settings(self.main):
            self.parent.load_settings(defaults = True)

        self.parent.activateWindow()
        