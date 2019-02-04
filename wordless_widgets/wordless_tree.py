#
# Wordless: Widgets - Tree
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

class Wordless_Tree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHeaderHidden(True)
