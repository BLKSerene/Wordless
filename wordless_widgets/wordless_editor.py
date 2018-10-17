#
# Wordless: Editor
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Text_Edit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.document().adjustSize()
        
        self.setFixedHeight(self.document().size().height() + 20)
