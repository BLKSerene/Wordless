# ----------------------------------------------------------------------
# Wordless: Dialogs - Message boxes
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

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

_tr = QCoreApplication.translate

class Wl_Msg_Box(QMessageBox):
    def __init__(self, main, icon, title, text):
        super().__init__(
            icon,
            title,
            f'''
                {main.settings_global['styles']['style_dialog']}
                <body>
                    {text}
                </body>
            ''',
            parent = main
        )

class Wl_Msg_Box_Info(Wl_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(
            main,
            icon = QMessageBox.Information,
            title = title,
            text = text
        )

class Wl_Msg_Box_Warning(Wl_Msg_Box):
    def __init__(self, main, title, text):
        super().__init__(
            main,
            icon = QMessageBox.Warning,
            title = title,
            text = text
        )

def wl_msg_box_question(main, title, text, default_to_yes = False):
    if default_to_yes:
        default_button = QMessageBox.Yes
    else:
        default_button = QMessageBox.No

    reply = QMessageBox.question(
        main,
        title,
        f'''
            {main.settings_global['styles']['style_dialog']}
            <body>
                {text}
            </body>
        ''',
        buttons = QMessageBox.Yes | QMessageBox.No,
        defaultButton = default_button
    )

    return bool(reply == QMessageBox.Yes)
