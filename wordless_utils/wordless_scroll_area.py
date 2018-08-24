from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.setBackgroundRole(QPalette.Light)
