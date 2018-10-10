#
# Wordless: Boxes
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Combo Box
class Wordless_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setMaxVisibleItems(25)

class Wordless_Combo_Box_Lang(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.addItems(sorted(main.settings_global['langs']))

class Wordless_Combo_Box_Encoding(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.addItems(main.settings_global['file_encodings'])

class Wordless_Combo_Box_Apply_To(Wordless_Combo_Box):
    def __init__(self, main, table):
        super().__init__(main)

        self.main = main
        self.table = table

        self.table.horizontalHeader().sectionCountChanged.connect(self.table_header_changed)

        self.table_header_changed()

    def table_header_changed(self):
        apply_to_old = self.currentText()

        self.clear()

        for file in self.table.files:
            self.addItem(file['name'])
        self.addItem(self.main.tr('Total'))

        for i in range(self.count()):
            if self.itemText(i) == apply_to_old:
                self.setCurrentIndex(i)

                break

# Spin Box
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
