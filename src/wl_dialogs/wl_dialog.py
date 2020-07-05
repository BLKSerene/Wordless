#
# Wordless: Dialogs - Dialog
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_utils import wl_misc
from wl_widgets import wl_layout

class Wl_Dialog(QDialog):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main)

        self.main = main

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(wl_misc.get_normalized_path('imgs/wl_icon.ico')))
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def set_fixed_height(self):
        self.setFixedHeight(self.heightForWidth(self.width()))

    def set_fixed_size(self):
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

    def move_to_center(self):
        self.move((self.main.width() - self.width()) / 2,
                  (self.main.height() - self.height()) / 2,)

class Wl_Dialog_Frameless(Wl_Dialog):
    def __init__(self, main):
        super().__init__(main, '',
                         width = 450)

        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setObjectName('wl-dialog-frameless')
        self.setStyleSheet('''
            QDialog#wl-dialog-frameless {
                background-color: #D0D0D0;
            }
        ''')

class Wl_Dialog_Info(Wl_Dialog):
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

        self.wrapper_info.setLayout(wl_layout.Wl_Layout())
        self.wrapper_info.layout().setContentsMargins(20, 10, 20, 10)

        self.wrapper_buttons = QWidget(self)

        self.wrapper_buttons.setLayout(wl_layout.Wl_Layout())
        self.wrapper_buttons.layout().setContentsMargins(11, 0, 11, 11)

        if not no_button:
            self.button_ok = QPushButton(self.tr('OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)

class Wl_Dialog_Error(Wl_Dialog_Info):
    def __init__(self, main, title, width = 0, height = 0, no_button = False):
        super().__init__(main, title, width, height, no_button)

    def exec_(self):
        super().exec_()

        QApplication.beep()

    def open(self):
        super().open()

        QApplication.beep()
