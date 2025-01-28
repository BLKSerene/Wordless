# ----------------------------------------------------------------------
# Wordless: Dialogs - Dialogs
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QPlainTextEdit,
    QPushButton,
    QTextEdit,
    QWidget
)

from wordless.wl_dialogs import wl_msg_boxes
from wordless.wl_utils import wl_paths, wl_misc
from wordless.wl_widgets import wl_buttons

_tr = QCoreApplication.translate

is_windows, is_macos, is_linux = wl_misc.check_os()

class Wl_Dialog(QDialog):
    def __init__(self, main, title, width = 0, height = 0, resizable = True):
        super().__init__(main)

        self.main = main
        self.fixed_width = width

        # Dialog size
        if resizable:
            if not width:
                width = self.size().width()

            if not height:
                height = self.size().height()

            self.resize(width, height)
        else:
            if width:
                self.setFixedWidth(width)

            if height:
                self.setFixedHeight(height)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(wl_paths.get_path_img('wl_icon.ico')))

        if not resizable:
            self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

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
                background-color: #264E8C;
            }
        ''')

    def adjust_size(self):
        self.adjustSize()

        if self.fixed_width:
            self.resize(self.fixed_width, self.heightForWidth(self.fixed_width))
        else:
            self.resize(self.width(), self.heightForWidth(self.width()))

        if is_windows or is_linux:
            self.move_to_center()

    def move_to_center(self):
        self.move(
            int((QApplication.primaryScreen().size().width() - self.width()) / 2),
            int((QApplication.primaryScreen().size().height() - self.height()) / 2)
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

# self.tr() does not work in inherited classes
class Wl_Dialog_Info(Wl_Dialog):
    def __init__(self, main, title, width = 0, height = 0, resizable = True, icon = True, no_buttons = False):
        # Avoid circular imports
        from wordless.wl_widgets import wl_layouts # pylint: disable=import-outside-toplevel

        super().__init__(main, title, width, height, resizable)

        self.wrapper_info = QWidget(self)

        self.wrapper_info.setObjectName('wrapper-info')
        self.wrapper_info.setStyleSheet('''
            QWidget#wrapper-info {
                border-bottom: 1px solid #B0B0B0;
                background-color: #FFF;
            }
        ''')

        if icon:
            self.layout_info = wl_layouts.Wl_Layout()
            self.wrapper_info.setLayout(wl_layouts.Wl_Layout())
            self.wrapper_info.layout().addWidget(wl_msg_boxes.get_msg_box_icon('information'), 0, 0, Qt.AlignTop)
            self.wrapper_info.layout().addLayout(self.layout_info, 0, 1)

            self.wrapper_info.layout().setHorizontalSpacing(20)
            self.wrapper_info.layout().setColumnStretch(1, 1)
        else:
            self.layout_info = wl_layouts.Wl_Layout()
            self.wrapper_info.setLayout(self.layout_info)

        self.wrapper_info.layout().setContentsMargins(15, 15, 15, 15)

        self.wrapper_buttons = QWidget(self)

        self.layout_buttons = wl_layouts.Wl_Layout()
        self.wrapper_buttons.setLayout(self.layout_buttons)
        self.wrapper_buttons.layout().setContentsMargins(13, 1, 13, 13)

        if not no_buttons:
            self.button_ok = QPushButton(_tr('wl_dialogs', 'OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def adjust_size(self):
        self.wrapper_info.adjustSize()
        self.wrapper_buttons.adjustSize()

        super().adjust_size()

class Wl_Dialog_Info_Copy(Wl_Dialog_Info):
    def __init__(
        self, main,
        title,
        width = 0, height = 0,
        resizable = True, is_plain_text = False
    ):
        super().__init__(
            main, title, width, height, resizable,
            no_buttons = True, icon = False
        )

        self.is_plain_text = is_plain_text

        if is_plain_text:
            self.text_edit_info = QPlainTextEdit(self)
        else:
            self.text_edit_info = QTextEdit(self)

        self.button_copy = QPushButton(_tr('wl_dialogs', 'Copy'), self)
        self.button_close = QPushButton(_tr('wl_dialogs', 'Close'), self)

        self.text_edit_info.setReadOnly(True)

        self.button_copy.clicked.connect(self.copy)
        self.button_close.clicked.connect(self.accept)

        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 1, Qt.AlignLeft)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 2, Qt.AlignRight)

        self.wrapper_buttons.layout().setColumnStretch(0, 1)
        self.wrapper_buttons.layout().setColumnStretch(1, 1)
        self.wrapper_buttons.layout().setColumnStretch(2, 1)
        self.wrapper_buttons.layout().setColumnStretch(3, 1)

    def copy(self):
        self.text_edit_info.setFocus()
        self.text_edit_info.selectAll()
        self.text_edit_info.copy()

    def get_info(self):
        return self.text_edit_info.toPlainText()

    def set_info(self, text):
        if self.is_plain_text:
            self.text_edit_info.setPlainText(text)
        else:
            self.text_edit_info.setHtml(text)

class Wl_Dialog_Settings(Wl_Dialog_Info):
    def __init__(self, main, title, width = 0, height = 0, resizable = True):
        super().__init__(main, title, width, height, resizable, no_buttons = True, icon = False)

        # Alias
        self.wrapper_settings = self.wrapper_info

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)

        self.button_save = QPushButton(_tr('wl_dialogs', 'Save'), self)
        self.button_cancel = QPushButton(_tr('wl_dialogs', 'Cancel'), self)

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
