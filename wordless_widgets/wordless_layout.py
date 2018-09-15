#
# Wordless: Layout
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
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
    def __init__(self, parent, load_settings):
        super().__init__(parent)

        self.main = parent
        self.load_settings = load_settings

        wrapper_settings = QWidget(parent)

        self.layout_settings = QGridLayout()

        wrapper_settings.setLayout(self.layout_settings)

        scroll_area_settings = Wordless_Scroll_Area(parent, wrapper_settings)

        button_restore_defaults = QPushButton(self.tr('Restore Defaults'), parent)

        button_restore_defaults.clicked.connect(self.restore_defaults)

        self.layout_table = QGridLayout()

        self.layout_tab = QGridLayout()
        self.layout_tab.addLayout(self.layout_table, 0, 0, 2, 1)
        self.layout_tab.addWidget(scroll_area_settings, 0, 1)
        self.layout_tab.addWidget(button_restore_defaults, 1, 1)

        self.layout_tab.setColumnStretch(0, 4)
        self.layout_tab.setColumnStretch(1, 1)
    
        self.setLayout(self.layout_tab)

    def restore_defaults(self):
        reply = QMessageBox.question(self.main,
                                     self.tr('Restore Defaults'),
                                     self.tr('Do you really want to reset all settings to defaults?'),
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.load_settings(default = True)

class Wordless_Separator(QFrame):
    def __init__(self, main):
        super().__init__(main)

        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet('border-top: 1px solid #D0D0D0;')
