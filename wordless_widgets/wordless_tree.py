#
# Wordless: Tree
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_Tree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHeaderHidden(True)
