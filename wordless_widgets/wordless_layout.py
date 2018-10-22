#
# Wordless: Layout
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent, wrapped_widget):
        super().__init__(parent)

        self.setWidget(wrapped_widget)

        self.setWidgetResizable(True)
        self.setBackgroundRole(QPalette.Light)

class Wordless_Tab(QWidget):
    def __init__(self, main, load_settings):
        super().__init__(main)

        self.main = main
        self.load_settings = load_settings

        wrapper_settings = QWidget(self.main)

        self.layout_settings = QGridLayout()
        wrapper_settings.setLayout(self.layout_settings)

        scroll_area_settings = Wordless_Scroll_Area(self.main, wrapper_settings)

        button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self.main)

        button_restore_defaults.clicked.connect(self.restore_defaults)

        self.layout_table = QGridLayout()

        self.setLayout(QGridLayout())
        self.layout().addLayout(self.layout_table, 0, 0, 2, 1)
        self.layout().addWidget(scroll_area_settings, 0, 1)
        self.layout().addWidget(button_restore_defaults, 1, 1)

        self.layout().setColumnStretch(0, 4)
        self.layout().setColumnStretch(1, 1)
    
    def restore_defaults(self):
        reply = QMessageBox.question(self.main,
                                     self.tr('Restore Defaults'),
                                     self.tr('Do you really want to reset all settings to defaults?'),
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

class Wordless_Separator(QFrame):
    def __init__(self, parent, orientation = 'Horizontal'):
        super().__init__(parent)

        if orientation == 'Horizontal':
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)

        self.setStyleSheet('color: #D0D0D0;')
