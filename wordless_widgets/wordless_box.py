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

from wordless_widgets import wordless_dialog

# Combo Box
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

class Wordless_Combo_Box_Use_Data_File(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        main.wordless_files.table.itemChanged.connect(self.wordless_files_changed)

        self.wordless_files_changed()

    def wordless_files_changed(self):
        if self.count() == 1:
            data_file_old = ''
        else:
            data_file_old = self.currentText()

        self.clear()

        for file in self.main.wordless_files.get_selected_files():
            self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        if self.findText(data_file_old) > -1:
            self.setCurrentText(data_file_old)

class Wordless_Combo_Box_Ref_File(Wordless_Combo_Box_Use_Data_File):
    def wordless_files_changed(self):
        super().wordless_files_changed()

        self.removeItem(self.findText(self.tr('Total')))

        if self.count() == 0:
            self.addItem(main.tr('*** None ***'))

class Wordless_Combo_Box_Apply_To(Wordless_Combo_Box):
    def __init__(self, main, table):
        super().__init__(main)

        self.table = table

        self.table.horizontalHeader().sectionCountChanged.connect(self.table_header_changed)

        self.table_header_changed()

    def table_header_changed(self):
        if self.count() == 1:
            file_old = ''
        else:
            file_old = self.currentText()

        self.clear()

        for file in self.table.settings['file']['files_open']:
            if file['selected']:
                self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        if self.findText(file_old) > -1:
            self.setCurrentText(file_old)

class Wordless_Combo_Box_Jre_Required(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.currentTextChanged.connect(self.text_changed)

        self.text_changed()

    def text_changed(self):
        if 'HanLP' in self.currentText():
            try:
                jpype.getDefaultJVMPath()

                import pyhanlp
            except:
                wordless_dialog.wordless_message_jre_not_installed(self.main)

                self.setCurrentText(self.text_old)

        self.text_old = self.currentText()

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
