import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import *

class Wordless_Settings(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setWindowTitle(self.tr('Settings'))

        self.setStyleSheet('* {font-family: Arial, sans-serif; color: #292929; font-size: 12px}')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.tabs_settings = QTabWidget(self)

        self.tabs_settings.addTab(self.init_settings_general(), self.tr('General'))
        self.tabs_settings.addTab(self.init_settings_file(), self.tr('File'))
        self.tabs_settings.addTab(self.init_settings_concordancer(), self.tr('Concordancer'))
        self.tabs_settings.addTab(self.init_settings_word_cluster(), self.tr('Word Cluster'))
        self.tabs_settings.addTab(self.init_settings_wordlist(), self.tr('Wordlist'))
        self.tabs_settings.addTab(self.init_settings_ngrams(), self.tr('N-grams'))
        self.tabs_settings.addTab(self.init_settings_semantics(), self.tr('Semantics'))

        button_save = QPushButton(self.tr('Save'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)
        button_apply = QPushButton(self.tr('Apply'), self)

        button_save.setFixedWidth(150)
        button_cancel.setFixedWidth(150)
        button_apply.setFixedWidth(150)

        button_save.clicked.connect(self.settings_save)
        button_cancel.clicked.connect(self.settings_cancel)
        button_apply.clicked.connect(self.settings_apply)

        layout_settings = QGridLayout()
        layout_settings.addWidget(self.tabs_settings, 0, 0, 1, 5)
        layout_settings.addWidget(button_save, 1, 2, Qt.AlignRight)
        layout_settings.addWidget(button_cancel, 1, 3, Qt.AlignRight)
        layout_settings.addWidget(button_apply, 1, 4, Qt.AlignRight)
        central_widget.setLayout(layout_settings)

    def init_settings_general(self):
        self.tab_settings_general = QWidget(self)

        label_precision = QLabel(self.tr('Precision:'), self)
        self.spinbox_precision = QSpinBox()

        self.spinbox_precision.setRange(1, 10)

        layout_settings_general = QGridLayout()
        layout_settings_general.addWidget(label_precision, 0, 0, Qt.AlignTop)
        layout_settings_general.addWidget(self.spinbox_precision, 0, 1, Qt.AlignTop)
        self.tab_settings_general.setLayout(layout_settings_general)

        return self.tab_settings_general

    def init_settings_file(self):
        self.tab_settings_file = QWidget(self)

        return self.tab_settings_file

    def init_settings_concordancer(self):
        self.tab_settings_concordancer = QWidget(self)

        return self.tab_settings_concordancer

    def init_settings_word_cluster(self):
        self.tab_settings_word_cluster = QWidget(self)

        return self.tab_settings_word_cluster

    def init_settings_wordlist(self):
        self.tab_settings_wordlist = QWidget(self)

        return self.tab_settings_wordlist

    def init_settings_ngrams(self):
        self.tab_settings_ngrams = QWidget(self)

        return self.tab_settings_ngrams

    def init_settings_semantics(self):
        self.tab_settings_semantics = QWidget(self)

        return self.tab_settings_semantics

    def settings_load(self, tab = 'General'):
        self.spinbox_precision.setValue(self.parent.settings['general']['precision'])

        for i in range(self.tabs_settings.count()):
            if tab == self.tabs_settings.tabText(i):
                self.tabs_settings.setCurrentIndex(i)

                break

        self.show()

    def settings_save(self):
        self.settings_apply()
        self.settings_cancel()

    def settings_cancel(self):
        self.hide()

    def settings_apply(self):
        self.parent.settings['general']['precision'] = self.spinbox_precision.value()
