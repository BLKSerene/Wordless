# ----------------------------------------------------------------------
# Wordless: Dialogs - Error
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialogs
from wl_widgets import wl_label, wl_table

class Wl_Dialog_Err(wl_dialogs.Wl_Dialog_Err):
    def __init__(self, main, title, width = 0, height = 0):
        super().__init__(main, title, width = 560, height = 320, no_buttons = True)

        self.button_export = QPushButton(self.tr('Export'), self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_ok.clicked.connect(self.accept)

        self.wrapper_buttons.layout().addWidget(self.button_export, 0, 0, Qt.AlignLeft)
        self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 1, Qt.AlignRight)

class Wl_Dialog_Err_Fatal(Wl_Dialog_Err):
    def __init__(self, main, err_msg):
        super().__init__(main, main.tr('Fatal Error'))

        self.label_error_msg = wl_label.Wl_Label_Dialog(
            self.tr(f'''
                <div>A fatal error has occurred, please <b>contact the author for support</b> by emailing to {self.main.email_html}!</div>
            '''),
            self
        )
        self.text_edit_error_msg = QTextEdit(self)

        self.text_edit_error_msg.setPlainText(err_msg)
        self.text_edit_error_msg.setReadOnly(True)

        self.wrapper_info.layout().addWidget(self.label_error_msg, 0, 0)
        self.wrapper_info.layout().addWidget(self.text_edit_error_msg, 1, 0)

        self.button_export.hide()

class Wl_Dialog_Err_Files(wl_dialogs.Wl_Dialog_Err):
    def __init__(self, main, title):
        super().__init__(main, title, width = 560, height = 320, no_buttons = True)

        self.label_err = wl_label.Wl_Label_Dialog('', self)
        self.table_err_files = wl_table.Wl_Table_Error(
            self,
            headers = [
                self.tr('Error Type'),
                self.tr('File')
            ]
        )

        self.table_err_files.setFixedHeight(220)
        self.table_err_files.setRowCount(0)

        self.button_export = QPushButton(self.tr('Export'), self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_export.clicked.connect(self.table_err_files.export_all)
        self.button_ok.clicked.connect(self.accept)

        self.wrapper_info.layout().addWidget(self.label_err, 0, 0)
        self.wrapper_info.layout().addWidget(self.table_err_files, 1, 0)

        self.wrapper_buttons.layout().addWidget(self.button_export, 0, 0, Qt.AlignLeft)
        self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 1, Qt.AlignRight)
