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
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.setBackgroundRole(QPalette.Light)

# Tab
class Wordless_Tab(QWidget):
    def __init__(self, parent, name):
        super().__init__(parent)

        self.parent = parent
        self.name = name

        self.layout_table = QGridLayout()

        wrapper_settings = QWidget(parent)

        self.layout_settings = QGridLayout()
        wrapper_settings.setLayout(self.layout_settings)

        scroll_area_settings = Wordless_Scroll_Area(parent)
        scroll_area_settings.setWidget(wrapper_settings)

        self.button_advanced_settings = QPushButton(self.tr('Advanced Settings'), parent)
        self.button_restore_defaults = QPushButton(self.tr('Restore Defaults'), parent)

        self.button_advanced_settings.clicked.connect(lambda: parent.wordless_settings.settings_load(parent.tr(name)))

        layout_tab = QGridLayout()
        layout_tab.addLayout(self.layout_table, 0, 0, 2, 1)
        layout_tab.addWidget(scroll_area_settings, 0, 1, 1, 2)
        layout_tab.addWidget(self.button_advanced_settings, 1, 1)
        layout_tab.addWidget(self.button_restore_defaults, 1, 2)
    
        layout_tab.setColumnStretch(0, 8)
        layout_tab.setColumnStretch(1, 1)
        layout_tab.setColumnStretch(2, 1)
    
        self.setLayout(layout_tab)
