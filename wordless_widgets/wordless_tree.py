#
# Wordless: Tree
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Tree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHeaderHidden(True)
