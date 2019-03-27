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

from wordless_utils import wordless_misc
from wordless_widgets import wordless_layout

class Wordless_Dialog(QDialog):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main)

        self.main = main

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(wordless_misc.get_abs_path('imgs/wordless_icon.ico')))
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def move_to_center(self):
        self.move((self.main.width() - self.width()) / 2,
                  (self.main.height() - self.height()) / 2,)

class Wordless_Dialog_Frameless(Wordless_Dialog):
    def __init__(self, main):
        super().__init__(main, '',
                         width = 460, height = 120)

        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setObjectName('wordless-dialog-frameless')
        self.setStyleSheet('''
            QDialog#wordless-dialog-frameless {
                background-color: #D0D0D0;
            }
        ''')

class Wordless_Dialog_Info(Wordless_Dialog):
    def __init__(self, main, title, width = 0, height = 0, no_button = False):
        super().__init__(main, title, width, height)

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

        self.wrapper_info.setLayout(wordless_layout.Wordless_Layout())
        self.wrapper_info.layout().setContentsMargins(20, 10, 20, 10)

        self.wrapper_buttons = QWidget(self)

        self.wrapper_buttons.setLayout(wordless_layout.Wordless_Layout())
        self.wrapper_buttons.layout().setContentsMargins(11, 0, 11, 11)

        if not no_button:
            self.button_ok = QPushButton(self.tr('OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.setLayout(wordless_layout.Wordless_Layout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)
