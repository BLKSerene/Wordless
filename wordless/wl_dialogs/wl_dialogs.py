# ----------------------------------------------------------------------
# Wordless: Dialogs - Dialogs
# Copyright (C) 2018-2023  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QWidget

from wordless.wl_widgets import wl_buttons

_tr = QCoreApplication.translate

class Wl_Dialog(QDialog):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main)

        self.main = main

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('imgs/wl_icon.ico'))
        # Do not use setWindowFlag, which was added in Qt 5.9 (PyQt 5.8 is used on macOS for compatibility with old macOSes)
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Fix styles of tables inside dialogs
        self.setStyleSheet('''
            QHeaderView::section {
                color: #FFF;
                font-weight: bold;
            }
            QHeaderView::section:horizontal {
                background-color: #5C88C5;
            }
            QHeaderView::section:horizontal:hover {
                background-color: #3265B2;
            }
            QHeaderView::section:horizontal:pressed {
                background-color: #3265B2;
            }
        ''')

    def set_fixed_height(self):
        self.setFixedHeight(self.heightForWidth(self.width()))

    def set_fixed_size(self):
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

    def move_to_center(self):
        self.move(
            (self.main.width() - self.width()) / 2,
            (self.main.height() - self.height()) / 2
        )

class Wl_Dialog_Frameless(Wl_Dialog):
    def __init__(self, main, width = 0, height = 0):
        super().__init__(
            main,
            title = '',
            width = width,
            height = height
        )

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setObjectName('wl-dialog-frameless')
        self.setStyleSheet('''
            QDialog#wl-dialog-frameless {
                background-color: #D0D0D0;
            }
        ''')

class Wl_Dialog_Info(Wl_Dialog):
    def __init__(self, main, title, width = 0, height = 0, no_buttons = False):
        # Avoid circular imports
        from wordless.wl_widgets import wl_layouts

        super().__init__(main, title, width, height)

        self.wrapper_info = QWidget(self)

        self.wrapper_info.setObjectName('wrapper-info')
        self.wrapper_info.setStyleSheet('''
            QWidget#wrapper-info {
                border-bottom: 1px solid #B0B0B0;
                background-color: #FFF;
            }
        ''')

        self.wrapper_info.setLayout(wl_layouts.Wl_Layout())
        self.wrapper_info.layout().setContentsMargins(20, 10, 20, 10)

        self.wrapper_buttons = QWidget(self)

        self.wrapper_buttons.setLayout(wl_layouts.Wl_Layout())
        self.wrapper_buttons.layout().setContentsMargins(11, 0, 11, 11)

        if not no_buttons:
            self.button_ok = QPushButton(self.tr('OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)

class Wl_Dialog_Settings(Wl_Dialog_Info):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main, title, width, height, no_buttons = True)

        # Alias
        self.wrapper_settings = self.wrapper_info

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)
        self.button_save = QPushButton(_tr('Wl_Dialog_Settings', 'Save'), self)
        self.button_cancel = QPushButton(_tr('Wl_Dialog_Settings', 'Cancel'), self)

        self.button_save.clicked.connect(self.save_settings)
        self.button_save.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.wrapper_buttons.layout().addWidget(self.button_restore_defaults, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_save, 0, 2, Qt.AlignRight)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3, Qt.AlignRight)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

    def load_settings(self, defaults = False):
        pass

    def save_settings(self):
        pass

    def load(self):
        self.load_settings()
        self.exec_()

class Wl_Dialog_Err(Wl_Dialog_Info):
    def exec_(self):
        super().exec_()

        QApplication.beep()

    def open(self):
        super().open()

        QApplication.beep()
