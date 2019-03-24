#
# Wordless: Widgets - Label
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import wordless_misc

class Wordless_Label(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wordless_misc.find_wordless_main(parent)

class Wordless_Label_Html(Wordless_Label):
    def __init__(self, html, parent):
        super().__init__(html, parent)

        self.setTextFormat(Qt.RichText)
        self.setOpenExternalLinks(True)

class Wordless_Label_Dialog(Wordless_Label_Html):
    def __init__(self, text, parent):
        main = wordless_misc.find_wordless_main(parent)

        super().__init__(
            f'''
                {main.settings_global['styles']['style_dialog']}
                <body>
                    {text}
                </body>
            ''', parent)

        self.setWordWrap(True)

    def set_text(self, text):
        super().setText(
            f'''
                {self.main.settings_global['styles']['style_dialog']}
                <body>
                    {text}
                </body>
            ''')

class Wordless_Label_Hint(Wordless_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet(self.main.settings_global['styles']['style_hints'])
