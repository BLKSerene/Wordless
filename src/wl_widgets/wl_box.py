#
# Wordless: Widgets - Box
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

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

class Wl_Combo_Box_Lang(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['langs'].keys()))

class Wl_Combo_Box_Text_Type(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['text_types'].keys()))

class Wl_Combo_Box_Encoding(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['file_encodings'].keys()))

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

        for file in self.table.settings['files']['files_open']:
            if file['selected']:
                self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        self.setCurrentText(file_to_filter_old)

        self.blockSignals(False)

        self.currentTextChanged.emit(self.currentText())

class Wl_Combo_Box_Ref_File(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        # Clip long file names
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.main.wl_files.table.itemChanged.connect(self.wl_files_changed)

        self.wl_files_changed()

    def wl_files_changed(self):
        if self.currentText() == self.tr('*** None ***'):
            use_file_old = ''
        else:
            use_file_old = self.currentText()

        self.clear()

        for file in self.main.wl_files.get_selected_files():
            self.addItem(file['name'])

        if self.count() > 0:
            if self.findText(use_file_old) > -1:
                self.setCurrentText(use_file_old)
        else:
            self.addItem(self.tr('*** None ***'))

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
            'Extra Small': 8,
            'Small': 10,
            'Medium (Recommended)': 12,
            'Large': 14,
            'Extra Large': 16
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
