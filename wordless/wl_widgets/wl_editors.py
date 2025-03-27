# ----------------------------------------------------------------------
# Wordless: Widgets - Editors
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

import os
import re

from PyQt5 import QtWidgets

from wordless.wl_checks import wl_checks_misc
from wordless.wl_dialogs import wl_dialogs
from wordless.wl_utils import wl_misc

# Line edits
class Wl_Line_Edit_Nonempty(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)
        self.text_old = ''

        self.editingFinished.connect(self.text_changed)

    def setText(self, text):
        super().setText(text)

        self.text_old = text

    def text_changed(self):
        # Empty text
        if not self.text().strip():
            self.setText(self.text_old)
        else:
            self.text_old = self.text()

    def start_editing(self):
        self.setFocus()
        self.selectAll()

class Wl_Line_Edit_Re(Wl_Line_Edit_Nonempty):
    def __init__(self, parent, re_validation, warning_title, warning_text):
        super().__init__(parent)

        self.RE_VALIDATION = re.compile(re_validation)
        self.warning_title = warning_title
        self.warning_text = warning_text

    def text_changed(self):
        # Empty text
        if not self.text().strip():
            self.setText(self.text_old)
            self.start_editing()
        # Validate text
        elif not self.RE_VALIDATION.search(self.text()):
            wl_dialogs.Wl_Dialog_Info_Simple(
                self,
                title = self.warning_title,
                text = self.warning_text,
                icon = 'critical'
            ).open()

            self.setText(self.text_old)
        else:
            self.text_old = self.text()

class Wl_Line_Edit_Path(Wl_Line_Edit_Nonempty):
    def dialog_path_empty(self):
        wl_dialogs.Wl_Dialog_Info_Simple(
            self,
            title = self.tr('Empty Path'),
            text = self.tr('''
                <div>The path should not be left empty.</div>
            '''),
            icon = 'critical'
        ).open()

    def dialog_path_not_found(self):
        wl_dialogs.Wl_Dialog_Info_Simple(
            self,
            title = self.tr('Path Not Found'),
            text = self.tr('''
                <div>The specified path "{}" cannot be found.</div>
                <br>
                <div>Please check your settings or specify another path.</div>
            ''').format(self.text()),
            icon = 'critical'
        ).open()

class Wl_Line_Edit_Path_File(Wl_Line_Edit_Path):
    def dialog_path_not_file(self):
        wl_dialogs.Wl_Dialog_Info_Simple(
            self,
            title = self.tr('Path Is Not a File'),
            text = self.tr('''
                <div>The specified path "{}" should be a file rather than a folder.</div>
                <br>
                <div>Please check your settings or specify another path.</div>
            ''').format(self.text()),
            icon = 'critical'
        ).open()

    def text_changed(self):
        # Empty text
        if not self.text().strip():
            self.setText(self.text_old)
        # Nonexistent path
        elif not os.path.exists(self.text()):
            self.dialog_path_not_found()

            self.setText(self.text_old)
            self.start_editing()
        # Invalid file path
        elif os.path.isdir(self.text()):
            self.dialog_path_not_file()

            self.setText(self.text_old)
            self.start_editing()
        else:
            self.text_old = self.text()

    def validate(self, default):
        if (
            not self.text().strip()
            or not os.path.exists(self.text())
            or os.path.isdir(self.text())
        ):
            # Empty text
            if not self.text().strip():
                self.dialog_path_empty()
            # Nonexistent path
            elif not os.path.exists(self.text()):
                self.dialog_path_not_found()
            # Invalid file path
            elif os.path.isdir(self.text()):
                self.dialog_path_not_file()

            self.setText(default)
            self.start_editing()

            return False
        else:
            return True

class Wl_Line_Edit_Path_Dir(Wl_Line_Edit_Path):
    def dialog_path_not_dir(self):
        wl_dialogs.Wl_Dialog_Info_Simple(
            self,
            title = self.tr('Path Is Not a Folder'),
            text = self.tr('''
                <div>The specified path "{}" should be a folder rather than a file.</div>
                <br>
                <div>Please check your settings or specify another path.</div>
            ''').format(self.text()),
            icon = 'critical'
        ).open()

    def text_changed(self):
        # Empty text
        if not self.text().strip():
            self.setText(self.text_old)
        # Nonexistent path
        elif not os.path.exists(self.text()):
            self.dialog_path_not_found()

            self.setText(self.text_old)
            self.start_editing()
        # Invalid directory path
        elif not os.path.isdir(self.text()):
            self.dialog_path_not_dir()

            self.setText(self.text_old)
            self.start_editing()
        else:
            self.text_old = self.text()

    def validate(self, default):
        if (
            not self.text().strip()
            or not os.path.exists(self.text())
            or not os.path.isdir(self.text())
        ):
            # Empty text
            if not self.text().strip():
                self.dialog_path_empty()
            # Nonexistent path
            elif not os.path.exists(self.text()):
                self.dialog_path_not_found()
            # Invalid directory path
            elif not os.path.isdir(self.text()):
                self.dialog_path_not_dir()

            self.setText(default)
            self.start_editing()

            return False
        else:
            return True

class Wl_Line_Edit_Path_Dir_Confirm(Wl_Line_Edit_Path_Dir):
    def dialog_path_confirm(self):
        return wl_dialogs.Wl_Dialog_Question(
            self,
            self.tr('Nonexistent Path'),
            self.tr('''
                <div>The specified path "{}" does not exist.</div>
                <br>
                <div>Do you want to create the folder?</div>
            ''').format(self.text()),
        ).exec_()

    def text_changed(self):
        # Empty text
        if not self.text().strip():
            self.setText(self.text_old)
        # Nonexistent path
        elif not os.path.exists(self.text()):
            if self.dialog_path_confirm():
                wl_checks_misc.check_dir(self.text())

                self.text_old = self.text()
            else:
                self.setText(self.text_old)
                self.start_editing()
        # Invalid directory path
        elif not os.path.isdir(self.text()):
            self.dialog_path_not_dir()

            self.setText(self.text_old)
            self.start_editing()
        else:
            self.text_old = self.text()

    def validate(self, default):
        # Empty text
        if not self.text().strip():
            self.dialog_path_empty()

            self.setText(default)
            self.start_editing()

            return False
        # Nonexistent path
        elif not os.path.exists(self.text()):
            if self.dialog_path_confirm():
                wl_checks_misc.check_dir(self.text())

                return True
            else:
                self.setText(default)
                self.start_editing()

                return False
        # Invalid directory path
        elif not os.path.isdir(self.text()):
            self.dialog_path_not_dir()

            self.setText(default)
            self.start_editing()

            return False
        else:
            return True

# Text browsers
class Wl_Text_Browser(QtWidgets.QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setOpenExternalLinks(True)
        self.setContentsMargins(3, 3, 3, 3)
 