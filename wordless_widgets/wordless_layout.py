#
# Wordless: Widgets - Layout
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

class Wordless_Splitter(QSplitter):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)

        self.setHandleWidth(0)
        self.setChildrenCollapsible(False)

class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setBackgroundRole(QPalette.Light)

class Wordless_Wrapper(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wordless_misc.find_wordless_main(parent)

        self.setObjectName('wordless-wrapper')
        self.setStyleSheet('''
            QWidget#wordless-wrapper {
                border: 1px solid #D0D0D0;
                background-color: #FFF;
            }
        ''')

        self.wrapper_table = QWidget(self)
        self.wrapper_table.setLayout(QGridLayout())

        self.wrapper_right = QWidget(self)
        self.wrapper_right.setFixedWidth(320)

        self.scroll_area_settings = Wordless_Scroll_Area(self)
        self.button_reset_settings = QPushButton(self.tr('Reset Settings'), self)

        self.wrapper_settings = QWidget(self)
        self.wrapper_settings.setLayout(QGridLayout())

        self.wrapper_settings.layout().setContentsMargins(6, 4, 6, 4)

        self.scroll_area_settings.setWidget(self.wrapper_settings)

        self.button_reset_settings.clicked.connect(self.reset_settings)

        self.wrapper_right.setLayout(QGridLayout())
        self.wrapper_right.layout().addWidget(self.scroll_area_settings, 0, 0)
        self.wrapper_right.layout().addWidget(self.button_reset_settings, 1, 0)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.wrapper_table, 0, 0)
        self.layout().addWidget(self.wrapper_right, 0, 1)

        self.layout().setContentsMargins(2, 0, 2, 0)
        self.layout().setSpacing(0)

    # If you subclass from QWidget, you need to provide a paintEvent for your custom QWidget as below.
    # See: https://doc.qt.io/qt-5/stylesheet-reference.html#list-of-stylable-widgets - QWidget
    def paintEvent(self, event):
        opt = QStyleOption();
        opt.initFrom(self);
        p = QPainter(self);
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self);
        
    def load_settings(self, defaults = False):
        pass
        
    def reset_settings(self):
        reply = wordless_message_box.wordless_message_box_reset_settings(self.main)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

class Wordless_Separator(QFrame):
    def __init__(self, parent, orientation = 'Horizontal'):
        super().__init__(parent)

        if orientation == 'Horizontal':
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)

        self.setStyleSheet('color: #D0D0D0;')
