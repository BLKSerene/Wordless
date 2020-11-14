#
# Wordless: Widgets - Label
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_utils import wl_misc

class Wl_Label(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        
        self.main = wl_misc.find_wl_main(parent)

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
    def __init__(self, text, parent):
        main = wl_misc.find_wl_main(parent)

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

class Wl_Label_Dialog_No_Wrap(Wl_Label_Dialog):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setWordWrap(False)

class Wl_Label_Normal(Wl_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet(self.main.settings_global['styles']['style_normal'])

class Wl_Label_Important(Wl_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet(self.main.settings_global['styles']['style_important'])

class Wl_Label_Hint(Wl_Label):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setStyleSheet(self.main.settings_global['styles']['style_hint'])
