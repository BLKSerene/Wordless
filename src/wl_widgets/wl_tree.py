#
# Wordless: Widgets - Tree
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_msg_box

class Wl_Tree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setHeaderHidden(True)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)

    def get_nodes(self):
        nodes = []

        iterator = QTreeWidgetItemIterator(self)

        while iterator.value():
            nodes.append(iterator.value())

            iterator += 1

        return nodes

class Wl_Settings(QWidget):
    def __init__(self, main):
        super().__init__()

        self.main = main

    def validate_path(self, line_edit):
        if not os.path.exists(line_edit.text()):
            wl_msg_box.wl_msg_box_path_not_exist(self.main, line_edit.text())

            line_edit.setFocus()
            line_edit.selectAll()

            return False
        elif not os.path.isdir(line_edit.text()):
            wl_msg_box.wl_msge_box_path_not_dir(self.main, line_edit.text())

            line_edit.setFocus()
            line_edit.selectAll()

            return False
        else:
            return True

    def confirm_path(self, line_edit):
        if not os.path.exists(line_edit.text()):
            reply = wl_msg_box.wl_msg_box_path_not_exist_confirm(self.main, line_edit.text())

            if reply == QMessageBox.Yes:
                return True
            else:
                line_edit.setFocus()
                line_edit.selectAll()

                return False
        elif not os.path.isdir(line_edit.text()):
            wl_msg_box.wl_msg_box_path_not_dir(self.main, line_edit.text())

            line_edit.setFocus()
            line_edit.selectAll()

            return False
        else:
            return True

    def validate_settings(self):
        return True

    def apply_settings(self):
        return True
