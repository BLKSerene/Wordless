# ----------------------------------------------------------------------
# Wordless: Widgets - Box
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_utils import wl_misc

# Combo Box
class Wl_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QComboBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Combo_Box_Adjustable(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

class Wl_Combo_Box_Yes_No(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems([
            self.tr('Yes'),
            self.tr('No')
        ])

class Wl_Combo_Box_Lang(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['langs']))

class Wl_Combo_Box_Encoding(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['file_encodings']))

class Wl_Combo_Box_File_To_Filter(Wl_Combo_Box):
    def __init__(self, parent, table):
        super().__init__(parent)

        self.table = table

        self.table.itemChanged.connect(self.table_item_changed)

        self.table_item_changed()

    def table_item_changed(self):
        self.blockSignals(True)

        file_to_filter_old = self.currentText()

        self.clear()

        for file in self.table.settings['file_area']['files_open']:
            if file['selected']:
                self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        self.setCurrentText(file_to_filter_old)

        self.blockSignals(False)

        self.currentTextChanged.emit(self.currentText())

class Wl_Combo_Box_File(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        # Clip long file names
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        for file in self.main.wl_files.get_selected_files():
            self.addItem(file['name'])

        self.main.wl_files.table.itemChanged.connect(self.wl_files_changed)

        self.wl_files_changed()

    def wl_files_changed(self):
        pass

    def get_file(self):
        return self.main.wl_files.find_file_by_name(self.currentText(), selected_only = True)

class Wl_Combo_Box_File_Figure_Settings(Wl_Combo_Box_File):
    def wl_files_changed(self):
        if self.count() == 1:
            file_old = ''
        else:
            file_old = self.currentText()

        self.clear()

        for file in self.main.wl_files.get_selected_files():
            self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        if file_old and self.findText(file_old) > -1:
            self.setCurrentText(file_old)

class Wl_Combo_Box_File_Concordancer(Wl_Combo_Box_File):
    def wl_files_changed(self):
        if self.currentText() == self.tr('*** None ***'):
            file_old = ''
        else:
            file_old = self.currentText()

        self.clear()

        for file in self.main.wl_files.get_selected_files():
            self.addItem(file['name'])

        if self.count() > 0:
            if self.findText(file_old) > -1:
                self.setCurrentText(file_old)
        else:
            self.addItem(self.tr('*** None ***'))

class Wl_Combo_Box_File_Ref(Wl_Combo_Box_File):
    def __init__(self, parent, list_files):
        super().__init__(parent)

        self.list_files = list_files

        self.currentTextChanged.connect(lambda: self.list_files.itemChanged.emit(self.list_files.item(0)))
        self.currentTextChanged.connect(lambda: self.list_files.file_changed(self))

    def wl_files_changed(self):
        file_old = self.currentText()
        files_selected = self.main.wl_files.get_selected_files()

        if file_old in [file['name'] for file in files_selected]:
            self.blockSignals(True)

            self.clear()

            for file in files_selected:
                self.addItem(file['name'])

            self.setCurrentText(file_old)

            self.blockSignals(False)
        else:
            self.list_files.wl_file_removed(self)

class Wl_Combo_Box_Font_Family(QFontComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QComboBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Combo_Box_Font_Size(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.FONT_SIZES = {
            'Extra Small': 10,
            'Small': 12,
            'Medium (Recommended)': 14,
            'Large': 16,
            'Extra Large': 18
        }

        self.main = wl_misc.find_wl_main(parent)

        self.addItems(list(self.FONT_SIZES))

    def set_text(self, font_size):
        for text, val in self.FONT_SIZES.items():
            if val == font_size:
                self.setCurrentText(text)

                break

    def get_val(self):
        return self.FONT_SIZES[self.currentText()]

# Spin Box
class Wl_Spin_Box(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Double_Spin_Box(QDoubleSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Spin_Box_Window(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(-100, 100)

        self.valueChanged.connect(self.value_changed)

    def stepBy(self, steps):
        if self.prefix() == 'L':
            super().stepBy(-steps)
        elif self.prefix() == 'R':
            super().stepBy(steps)

    def value_changed(self):
        if self.value() <= 0:
            if self.prefix() == 'L':
                self.setPrefix('R')
            else:
                self.setPrefix('L')

            self.setValue(-self.value() + 1)

class Wl_Spin_Box_Font_Size(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(8, 72)

# Text Browser
class Wl_Text_Browser(QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setOpenExternalLinks(True)
        self.setContentsMargins(3, 3, 3, 3)
