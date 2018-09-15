#
# Wordless: Utility Functions for Tabs
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Scroll Area
class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent, wrapped_widget):
        super().__init__(parent)

        self.setWidget(wrapped_widget)

        self.setWidgetResizable(True)
        self.setBackgroundRole(QPalette.Light)

# Tab
class Wordless_Tab(QWidget):
    def __init__(self, parent, name):
        super().__init__(parent)

        self.main = parent
        self.name = name

        self.layout_table = QGridLayout()

        wrapper_settings = QWidget(parent)

        self.layout_settings = QGridLayout()

        wrapper_settings.setLayout(self.layout_settings)

        scroll_area_settings = Wordless_Scroll_Area(parent, wrapper_settings)

        self.button_restore_defaults = QPushButton(self.tr('Restore Defaults'), parent)

        self.layout_tab = QGridLayout()
        self.layout_tab.addLayout(self.layout_table, 0, 0, 2, 1)
        self.layout_tab.addWidget(scroll_area_settings, 0, 1)
        self.layout_tab.addWidget(self.button_restore_defaults, 1, 1)

        self.layout_tab.setColumnStretch(0, 4)
        self.layout_tab.setColumnStretch(1, 1)
    
        self.setLayout(self.layout_tab)
