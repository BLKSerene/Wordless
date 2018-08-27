#
# Wordless: Utility Function for GUI Widgets
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.setBackgroundRole(QPalette.Light)

class Wordless_Text_Edit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.document().adjustSize()
        
        self.setFixedHeight(self.document().size().height() + 20)

class Wordless_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setMaxVisibleItems(25)

class Wordless_Combo_Box_Lang(Wordless_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(sorted(parent.file_langs))

class Wordless_Combo_Box_Encoding(Wordless_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(parent.file_encodings)
