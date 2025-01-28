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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from wordless.wl_utils import wl_misc

class Wl_Label(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wl_misc.find_wl_main(parent)

class Wl_Label_Important(Wl_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet('''
            color: #F00;
            font-weight: bold;
        ''')

class Wl_Label_Hint(Wl_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet('''
            color: #777;
        ''')

class Wl_Label_Html(Wl_Label):
    def __init__(self, html, parent):
        super().__init__(html, parent)

        self.setTextFormat(Qt.RichText)
        self.setOpenExternalLinks(True)

class Wl_Label_Html_Centered(Wl_Label_Html):
    def __init__(self, html, parent):
        super().__init__(html, parent)

        self.setAlignment(Qt.AlignCenter)

class Wl_Label_Dialog(Wl_Label_Html):
    def __init__(self, text, parent, word_wrap = True):
        main = wl_misc.find_wl_main(parent)

        super().__init__(
            f'''
                {main.settings_global['styles']['style_dialog']}
                <body align="justify">{text}</body>
            ''',
            parent
        )

        self.setWordWrap(word_wrap)

    def set_text(self, text):
        super().setText(f'''
            {self.main.settings_global['styles']['style_dialog']}
            <body align="justify">{text}</body>
        ''')

class Wl_Label_Dialog_No_Wrap(Wl_Label_Dialog):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setWordWrap(False)
