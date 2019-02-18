#
# Wordless: Widgets - Button
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
from wordless_widgets import wordless_message_box

class Wordless_Button(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.main = wordless_misc.find_wordless_main(parent)

class Wordless_Button_Reset_Settings(Wordless_Button):
    def __init__(self, parent, load_settings):
        super().__init__(parent.tr('Reset Settings'), parent)

        self.load_settings = load_settings

        self.clicked.connect(self.reset_settings)

    def reset_settings(self):
        reply = wordless_message_box.wordless_message_box_reset_settings(self.main)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)
