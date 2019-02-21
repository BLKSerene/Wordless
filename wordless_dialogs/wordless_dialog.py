#
# Wordless: Dialogs - Dialog
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Dialog(QDialog):
    def __init__(self, main, title):
        super().__init__(main)

        self.main = main

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('imgs/wordless_icon.png'))
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def move_to_center(self):
        self.move((self.main.width() - self.width()) / 2,
                  (self.main.height() - self.height()) / 2,)

class Wordless_Dialog_Info(Wordless_Dialog):
    def __init__(self, main, title, width, height, no_button = False):
        super().__init__(main, title)

        self.setFixedSize(width, height)
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.wrapper_info = QWidget(self)

        self.wrapper_info.setObjectName('wrapper-info')
        self.wrapper_info.setStyleSheet('''
            QWidget#wrapper-info {
                border-bottom: 1px solid #B0B0B0;
                background-color: #FFF;
            }
        ''')

        self.wrapper_info.setLayout(QGridLayout())
        self.wrapper_info.layout().setContentsMargins(20, 10, 20, 10)

        self.wrapper_buttons = QWidget(self)

        self.wrapper_buttons.setLayout(QGridLayout())
        self.wrapper_buttons.layout().setContentsMargins(11, 0, 11, 11)

        if not no_button:
            self.button_ok = QPushButton(self.tr('OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)
