# ----------------------------------------------------------------------
# Wordless: Widgets - Buttons
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

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QPushButton

from wl_dialogs import wl_msg_boxes
from wl_utils import wl_misc

_tr = QCoreApplication.translate

class Wl_Button(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wl_misc.find_wl_main(parent)

class Wl_Button_Restore_Default_Settings(Wl_Button):
    def __init__(self, parent, load_settings):
        super().__init__(_tr('Wl_Button_Restore_Default_Settings', 'Restore default settings'), parent)

        self.parent = parent
        self.load_settings = load_settings

        self.setMinimumWidth(200)

        self.clicked.connect(self.restore_default_settings)

    def restore_default_settings(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self.main,
            title = self.tr('Restore default settings'),
            text = self.tr('''
                <div>Do you want to reset all settings to their defaults?</div>
            ''')
        ):
            self.load_settings(defaults = True)

        self.parent.activateWindow()
