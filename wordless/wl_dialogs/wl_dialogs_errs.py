# ----------------------------------------------------------------------
# Wordless: Dialogs - Errors
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
from PyQt5.QtWidgets import QApplication, QPushButton

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_widgets import wl_labels, wl_tables

_tr = QCoreApplication.translate

class Wl_Dialog_Err(wl_dialogs.Wl_Dialog_Info):
    def __init__(self, main, title, width = 0, height = 0, resizable = True, no_buttons = False):
        super().__init__(
            main, title,
            width = width, height = height,
            resizable = resizable, icon = False, no_buttons = no_buttons
        )

    def exec_(self):
        super().exec_()

        QApplication.beep()

    def open(self):
        super().open()

        QApplication.beep()

class Wl_Dialog_Err_Info_Copy(wl_dialogs.Wl_Dialog_Info_Copy):
    def __init__(self, main, title, width = 0, height = 0, resizable = True, help_info = '', err_msg = ''):
        super().__init__(
            main, title,
            width = width, height = height, resizable = resizable
        )

        self.label_err_msg = wl_labels.Wl_Label_Dialog(help_info, self)

        self.text_edit_info.setPlainText(err_msg)

        self.layout_info.addWidget(self.label_err_msg, 0, 0)
        self.layout_info.addWidget(self.text_edit_info, 1, 0)

    def exec_(self):
        super().exec_()

        QApplication.beep()

    def open(self):
        super().open()

        QApplication.beep()

class Wl_Dialog_Err_Fatal(Wl_Dialog_Err_Info_Copy):
    def __init__(self, main, err_msg):
        super().__init__(
            main,
            title = _tr('wl_dialogs_errs', 'Fatal Error'),
            width = 600,
            height = 300,
            help_info = _tr('wl_dialogs_errs', '''
                <div>A fatal error has occurred, please <b>send the following error messages</b> to {} in order to <b>contact the author for support</b>!</div>
            ''').format(main.email_html),
            err_msg = err_msg
        )

class Wl_Dialog_Err_Download_Model(Wl_Dialog_Err_Info_Copy):
    def __init__(self, main, err_msg):
        super().__init__(
            main,
            title = _tr('wl_dialogs_errs', 'Network Error'),
            width = 600,
            height = 400,
            help_info = _tr('wl_dialogs_errs', '''
                <div>A network error occurred while downloading the model, please check your internet connections and proxy settings in <b>Menu → Preferences → General → Proxy Settings</b> if you are using a proxy.</div>
                <div>If the network issue persists, please <b>send the following error messages</b> to {} in order to <b>contact the author for support</b>.</div>
            ''').format(main.email_html),
            err_msg = err_msg
        )

class Wl_Dialog_Err_Files(Wl_Dialog_Err):
    def __init__(self, main, title):
        super().__init__(main, title, width = 650, height = 350, no_buttons = True)

        self.label_err = wl_labels.Wl_Label_Dialog('', self)
        self.table_err_files = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Error Type'),
                self.tr('File Path')
            ]
        )

        self.table_err_files.tab = 'err'

        self.table_err_files.model().setRowCount(0)

        self.button_exp_table = QPushButton(' ' * 3 + self.tr('Export table...') + ' ' * 3, self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_exp_table.clicked.connect(self.table_err_files.exp_all_cells)
        self.button_ok.clicked.connect(self.accept)

        self.layout_info.addWidget(self.label_err, 0, 0)
        self.layout_info.addWidget(self.table_err_files, 1, 0)

        self.layout_buttons.addWidget(self.button_exp_table, 0, 0, Qt.AlignLeft)
        self.layout_buttons.addWidget(self.button_ok, 0, 1, Qt.AlignRight)
