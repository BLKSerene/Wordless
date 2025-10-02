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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_utils import (
    wl_paths,
    wl_misc
)
from wordless.wl_widgets import (
    wl_buttons,
    wl_labels
)

_tr = QtCore.QCoreApplication.translate

is_macos = wl_misc.check_os()[1]

def get_msg_box_icon(icon_type = 'info'):
    style = QtWidgets.QApplication.style()
    size = style.pixelMetric(QtWidgets.QStyle.PM_MessageBoxIconSize, None, None)

    match icon_type:
        case 'info':
            icon = style.standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation, None, None)
        case 'warning':
            icon = style.standardIcon(QtWidgets.QStyle.SP_MessageBoxWarning, None, None)
        case 'critical':
            icon = style.standardIcon(QtWidgets.QStyle.SP_MessageBoxCritical, None, None)
        case 'question':
            icon = style.standardIcon(QtWidgets.QStyle.SP_MessageBoxQuestion, None, None)

    label = QtWidgets.QLabel('')
    label.setPixmap(icon.pixmap(size, size))

    return label

class Wl_Dialog(QtWidgets.QDialog):
    def __init__(self, parent, title, width = 0, height = 0, resizable = True, beep = False):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)
        self.fixed_width = width
        self.beep = beep

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
        self.setWindowIcon(QtGui.QIcon(wl_paths.get_path_img('wl_icon.ico')))

        if not resizable:
            self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint, True)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

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

        if not is_macos:
            self.move_to_center()

    def move_to_center(self):
        self.move(
            int((QtWidgets.QApplication.primaryScreen().size().width() - self.width()) / 2),
            int((QtWidgets.QApplication.primaryScreen().size().height() - self.height()) / 2)
        )

    def exec(self):
        if self.beep:
            QtWidgets.QApplication.beep()

        return super().exec()

    def open(self):
        if self.beep:
            QtWidgets.QApplication.beep()

        return super().open()

class Wl_Dialog_Frameless(Wl_Dialog):
    def __init__(self, parent, width = 0, height = 0, beep = False):
        super().__init__(
            parent,
            title = '',
            width = width, height = height,
            resizable = False, beep = beep
        )

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setObjectName('wl-dialog-frameless')
        self.setStyleSheet('''
            QDialog#wl-dialog-frameless {
                background-color: #D0D0D0;
            }
        ''')

# self.tr() may not work in inherited classes
# See: https://www.riverbankcomputing.com/static/Docs/PyQt5/i18n.html#differences-between-pyqt5-and-qt
class Wl_Dialog_Info(Wl_Dialog):
    def __init__(
        self, parent,
        title,
        width = 0, height = 0,
        resizable = True, icon = '', no_buttons = False
    ):
        # Avoid circular imports
        from wordless.wl_widgets import wl_layouts # pylint: disable=import-outside-toplevel

        beep = icon in ('warning', 'critical', 'question')

        super().__init__(parent, title, width, height, resizable, beep)

        self.wrapper_info = QtWidgets.QWidget(self)

        self.wrapper_info.setObjectName('wrapper-info')
        self.wrapper_info.setStyleSheet('''
            QWidget#wrapper-info {
                border-bottom: 1px solid #B0B0B0;
                background-color: #FFF;
            }
        ''')

        self.wrapper_info.setLayout(wl_layouts.Wl_Layout())
        self.layout_info = wl_layouts.Wl_Layout()

        if icon:
            layout_icon_info = wl_layouts.Wl_Layout()
            layout_icon_info.addWidget(get_msg_box_icon(icon), 0, 0, QtCore.Qt.AlignTop)
            layout_icon_info.addLayout(self.layout_info, 0, 1)

            layout_icon_info.setColumnStretch(1, 1)
            layout_icon_info.setHorizontalSpacing(20)

            self.wrapper_info.layout().addLayout(layout_icon_info, 0, 0)
        else:
            self.wrapper_info.layout().addLayout(self.layout_info, 0, 0)

        self.wrapper_info.layout().setContentsMargins(15, 15, 15, 15)

        self.wrapper_buttons = QtWidgets.QWidget(self)

        self.layout_buttons = wl_layouts.Wl_Layout()
        self.wrapper_buttons.setLayout(self.layout_buttons)
        self.wrapper_buttons.layout().setContentsMargins(13, 1, 13, 13)

        if not no_buttons:
            self.button_ok = QtWidgets.QPushButton(_tr('wl_dialogs', 'OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, QtCore.Qt.AlignRight)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def adjust_size(self):
        self.wrapper_info.adjustSize()
        self.wrapper_buttons.adjustSize()

        super().adjust_size()

class Wl_Dialog_Info_Simple(Wl_Dialog_Info):
    def __init__(
        self, parent,
        title, text,
        width = 500, height = 0,
        resizable = True, icon = 'info'
    ):
        super().__init__(parent, title, width, height, resizable, icon)

        self.label_info = wl_labels.Wl_Label_Dialog(text, self)

        self.layout_info.addWidget(self.label_info, 0, 0)

class Wl_Dialog_Info_Copy(Wl_Dialog_Info):
    def __init__(
        self, parent,
        title,
        width = 0, height = 0,
        resizable = True, icon = '', is_plain_text = False
    ):
        super().__init__(
            parent, title,
            width, height,
            resizable, no_buttons = True, icon = icon
        )

        self.is_plain_text = is_plain_text

        if is_plain_text:
            self.text_edit_info = QtWidgets.QPlainTextEdit(self)
        else:
            self.text_edit_info = QtWidgets.QTextEdit(self)

        self.text_edit_info.setReadOnly(True)

        self.wrapper_info.layout().addWidget(self.text_edit_info, 1, 0, 1, 2)

        self.button_copy = QtWidgets.QPushButton(_tr('wl_dialogs', 'Copy'), self)
        self.button_close = QtWidgets.QPushButton(_tr('wl_dialogs', 'Close'), self)

        self.button_copy.clicked.connect(self.copy)
        self.button_close.clicked.connect(self.accept)

        self.wrapper_buttons.layout().addWidget(self.button_copy, 0, 1, QtCore.Qt.AlignLeft)
        self.wrapper_buttons.layout().addWidget(self.button_close, 0, 2, QtCore.Qt.AlignRight)

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

class Wl_Dialog_Question(Wl_Dialog_Info):
    def __init__(
        self, parent,
        title, text,
        width = 500, height = 0,
        resizable = True, default_to_yes = False
    ):
        super().__init__(
            parent, title, width, height, resizable,
            icon = 'question', no_buttons = True
        )

        self.label_info = wl_labels.Wl_Label_Dialog(text, self)

        self.button_yes = QtWidgets.QPushButton(_tr('wl_dialogs', 'Yes'), self)
        self.button_no = QtWidgets.QPushButton(_tr('wl_dialogs', 'No'), self)

        self.button_yes.clicked.connect(self.accept)
        self.button_no.clicked.connect(self.reject)

        self.layout_info.addWidget(self.label_info, 0, 0)

        self.layout_buttons.addWidget(self.button_yes, 0, 1)
        self.layout_buttons.addWidget(self.button_no, 0, 2)

        self.layout_buttons.setColumnStretch(0, 1)

        if default_to_yes:
            self.button_yes.setFocus(True)
        else:
            self.button_no.setFocus(True)

class Wl_Dialog_Settings(Wl_Dialog_Info):
    def __init__(self, parent, title, width = 0, height = 0, resizable = True):
        super().__init__(
            parent, title, width, height, resizable,
            icon = '', no_buttons = True
        )

        # Alias
        self.wrapper_settings = self.wrapper_info

        self.button_restore_default_vals = wl_buttons.Wl_Button_Restore_Default_Vals(self, load_settings = self.load_settings)

        self.button_save = QtWidgets.QPushButton(_tr('wl_dialogs', 'Save'), self)
        self.button_cancel = QtWidgets.QPushButton(_tr('wl_dialogs', 'Cancel'), self)

        self.button_save.clicked.connect(self.save_settings)
        self.button_save.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

        self.wrapper_buttons.layout().addWidget(self.button_restore_default_vals, 0, 0)
        self.wrapper_buttons.layout().addWidget(self.button_save, 0, 2, QtCore.Qt.AlignRight)
        self.wrapper_buttons.layout().addWidget(self.button_cancel, 0, 3, QtCore.Qt.AlignRight)

        self.wrapper_buttons.layout().setColumnStretch(1, 1)

    def load_settings(self, defaults = False):
        pass

    def save_settings(self):
        pass

    def load(self):
        self.load_settings()

        # Results code
        return self.exec()
