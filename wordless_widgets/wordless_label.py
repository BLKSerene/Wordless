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

class Wordless_Label_Html(QLabel):
    def __init__(self, html, parent):
        super().__init__(html, parent)

        self.setTextFormat(Qt.RichText)
        self.setOpenExternalLinks(True)

class Wordless_Label_Hint(Wordless_Label_Html):
    def __init__(self, html, main):
        super().__init__(f'''
                             {main.settings_global["styles"]["style_hints"]}
                             <body>
                                 {html}
                             </body>
                         ''', main)
