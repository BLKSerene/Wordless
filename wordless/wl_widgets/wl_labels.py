# ----------------------------------------------------------------------
# Wordless: Widgets - Labels
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
from PyQt5 import QtWidgets

from wordless.wl_utils import wl_misc

class Wl_Label(QtWidgets.QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wl_misc.find_wl_main(parent)

class Wl_Label_Hint(Wl_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet('''
            color: #777;
        ''')

class Wl_Label_Html(Wl_Label):
    def __init__(self, html, parent):
        super().__init__(html, parent)

        self.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.setTextFormat(QtCore.Qt.RichText)
        self.setOpenExternalLinks(True)

class Wl_Label_Html_Centered(Wl_Label_Html):
    def __init__(self, html, parent):
        super().__init__(html, parent)

        self.setAlignment(QtCore.Qt.AlignCenter)

STYLES_DIALOG = '''
    <head><style>
      * {
        margin: 0;
        line-height: 120%;
      }
    </style></head>
'''

class Wl_Label_Dialog(Wl_Label_Html):
    def __init__(self, text, parent, word_wrap = True):
        super().__init__(
            f'''
                {STYLES_DIALOG}
                <body>{text}</body>
            ''',
            parent
        )

        self.setWordWrap(word_wrap)

    def set_text(self, text):
        super().setText(f'''
            {STYLES_DIALOG}
            <body>{text}</body>
        ''')

class Wl_Label_Dialog_No_Wrap(Wl_Label_Dialog):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setWordWrap(False)
