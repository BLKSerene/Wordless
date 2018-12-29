#
# Wordless: Boxes
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import jpype

from wordless_widgets import wordless_message_box

# Combo Boxes
class Wordless_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = parent

        self.setMaxVisibleItems(25)

class Wordless_Combo_Box_Lang(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.addItems(sorted(main.settings_global['langs']))

class Wordless_Combo_Box_Encoding(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.addItems(main.settings_global['file_encodings'])

class Wordless_Combo_Box_Ref_File(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        main.wordless_files.table.itemChanged.connect(self.wordless_files_changed)

        self.wordless_files_changed()

    def wordless_files_changed(self):
        if self.currentText() == self.tr('*** None ***'):
            use_file_old = ''
        else:
            use_file_old = self.currentText()

        self.clear()

        for file in self.main.wordless_files.get_selected_files():
            self.addItem(file['name'])

        if self.count() > 0:
            if self.findText(use_file_old) > -1:
                self.setCurrentText(use_file_old)
        else:
            self.addItem(self.tr('*** None ***'))

# Spin Boxes
class Wordless_Spin_Box_Window(QSpinBox):
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
