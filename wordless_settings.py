#
# Wordless: Settings
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import *

class Wordless_Settings(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setWindowTitle(self.tr('Settings'))

        self.accepted.connect(self.settings_apply)

        self.tabs_settings = QTabWidget(self)

        self.tabs_settings.addTab(self.init_settings_general(), self.tr('General'))
        self.tabs_settings.addTab(self.init_settings_file(), self.tr('File'))
        self.tabs_settings.addTab(self.init_settings_concordancer(), self.tr('Concordancer'))
        self.tabs_settings.addTab(self.init_settings_wordlist(), self.tr('Wordlist'))
        self.tabs_settings.addTab(self.init_settings_ngram(), self.tr('N-gram'))
        self.tabs_settings.addTab(self.init_settings_semantics(), self.tr('Semantics'))

        button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_restore_defaults.setFixedWidth(150)
        button_save.setFixedWidth(100)
        button_cancel.setFixedWidth(100)
        button_apply.setFixedWidth(100)

        button_restore_defaults.clicked.connect(self.restore_defaults)
        button_save.clicked.connect(self.accept)
        button_apply.clicked.connect(self.settings_apply)
        button_cancel.clicked.connect(self.reject)

        layout_settings = QGridLayout()
        layout_settings.addWidget(self.tabs_settings, 0, 0, 1, 6)
        layout_settings.addWidget(button_restore_defaults, 1, 2, Qt.AlignRight)
        layout_settings.addWidget(button_save, 1, 3, Qt.AlignRight)
        layout_settings.addWidget(button_apply, 1, 4, Qt.AlignRight)
        layout_settings.addWidget(button_cancel, 1, 5, Qt.AlignRight)

        self.setLayout(layout_settings)

    def init_settings_general(self):
        self.tab_settings_general = QWidget(self)

        groupbox_encoding = QGroupBox(self.tr('Default Encoding'), self)

        self.label_encoding_input = QLabel(self.tr('Input Encoding:'), self)
        self.combo_box_encoding_input = wordless_widgets.Wordless_Combo_Box_Encoding(self.parent)
        self.label_encoding_output = QLabel(self.tr('Output Encoding:'), self)
        self.combo_box_encoding_output = wordless_widgets.Wordless_Combo_Box_Encoding(self.parent)

        layout_encoding = QGridLayout()
        layout_encoding.addWidget(self.label_encoding_input, 0, 0)
        layout_encoding.addWidget(self.combo_box_encoding_input, 0, 1)
        layout_encoding.addWidget(self.label_encoding_output, 1, 0)
        layout_encoding.addWidget(self.combo_box_encoding_output, 1, 1)

        groupbox_encoding.setLayout(layout_encoding)

        self.label_precision = QLabel(self.tr('Precision:'), self)
        self.spin_box_precision = QSpinBox(self)

        self.spin_box_precision.setRange(0, 10)

        layout_settings_general = QGridLayout()
        layout_settings_general.addWidget(groupbox_encoding, 0, 0, 1, 2, Qt.AlignTop)
        layout_settings_general.addWidget(self.label_precision, 1, 0, Qt.AlignTop)
        layout_settings_general.addWidget(self.spin_box_precision, 1, 1, Qt.AlignTop)
        self.tab_settings_general.setLayout(layout_settings_general)

        return self.tab_settings_general

    def init_settings_file(self):
        self.tab_settings_file = QWidget(self)

        return self.tab_settings_file

    def init_settings_concordancer(self):
        self.tab_settings_concordancer = QWidget(self)

        return self.tab_settings_concordancer

    def init_settings_wordlist(self):
        self.tab_settings_wordlist = QWidget(self)

        return self.tab_settings_wordlist

    def init_settings_ngram(self):
        self.tab_settings_ngram = QWidget(self)

        return self.tab_settings_ngram

    def init_settings_semantics(self):
        self.tab_settings_semantics = QWidget(self)

        return self.tab_settings_semantics

    def settings_load(self, tab = 'General'):
        self.combo_box_encoding_input.setCurrentText(wordless_misc.convert_encoding(self.parent, *self.parent.settings['general']['encoding_input']))
        self.combo_box_encoding_output.setCurrentText(wordless_misc.convert_encoding(self.parent, *self.parent.settings['general']['encoding_output']))

        self.spin_box_precision.setValue(self.parent.settings['general']['precision'])

        for i in range(self.tabs_settings.count()):
            if tab == self.tabs_settings.tabText(i):
                self.tabs_settings.setCurrentIndex(i)

                break

        self.exec()

    def restore_defaults(self):
        self.combo_box_encoding_input.setCurrentText(wordless_misc.convert_encoding(self.parent, *self.parent.default_settings['general']['encoding_input']))
        self.combo_box_encoding_output.setCurrentText(wordless_misc.convert_encoding(self.parent, *self.parent.default_settings['general']['encoding_output']))

        self.spin_box_precision.setValue(self.parent.default_settings['general']['precision'])

    def settings_apply(self):
        self.parent.settings['general']['encoding_input'] = wordless_misc.convert_encoding(self.parent, self.combo_box_encoding_input.currentText())
        self.parent.settings['general']['encoding_output'] = wordless_misc.convert_encoding(self.parent, self.combo_box_encoding_output.currentText())
        self.parent.settings['general']['precision'] = self.spin_box_precision.value()
