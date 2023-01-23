# ----------------------------------------------------------------------
# Wordless: Widgets - Boxes
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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QFontComboBox, QSpinBox

from wordless.wl_utils import wl_misc

# Combo boxes
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

        self.addItems(list(self.main.settings_global['encodings']))

class Wl_Combo_Box_File_To_Filter(Wl_Combo_Box):
    def __init__(self, parent, table):
        super().__init__(parent)

        self.table = table

        self.table.model().itemChanged.connect(self.table_item_changed)

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

        self.addItems(self.main.wl_file_area.get_selected_file_names())

        self.main.wl_file_area.table_files.model().itemChanged.connect(self.wl_files_changed)

        self.wl_files_changed()

    def wl_files_changed(self):
        pass

    def get_file(self):
        return self.main.wl_file_area.find_file_by_name(self.currentText(), selected_only = True)

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

# Spin boxes
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
            QDoubleSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Spin_Box_Window(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(-100, 100)

        self.valueChanged.connect(self.value_changed)

    def stepBy(self, steps):
        if self.prefix() == self.tr('L'):
            super().stepBy(-steps)
        elif self.prefix() == self.tr('R'):
            super().stepBy(steps)

    def value_changed(self):
        if self.value() <= 0:
            if self.prefix() == self.tr('L'):
                self.setPrefix(self.tr('R'))
            else:
                self.setPrefix(self.tr('L'))

            self.setValue(-self.value() + 1)

class Wl_Spin_Box_Font_Size(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(6, 20)
