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

from wordless_widgets import wordless_message_box

class Wordless_Splitter(QSplitter):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)

        self.setHandleWidth(1)
        self.setChildrenCollapsible(False)

class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent, wrapped_widget = None):
        super().__init__(parent)

        if wrapped_widget:
            self.setWidget(wrapped_widget)

        self.setWidgetResizable(True)
        self.setBackgroundRole(QPalette.Light)

class Wordless_Wrapper(Wordless_Splitter):
    def __init__(self, main, load_settings):
        super().__init__(Qt.Horizontal, main)

        self.main = main
        self.load_settings = load_settings

        self.setObjectName('wordless-wrapper')
        self.setStyleSheet('''
            QWidget#wordless-wrapper {
                border: 1px solid #D0D0D0;
                background-color: #FFF;
            }
        ''')

        self.wrapper_left = QWidget(self)

        self.wrapper_left.setLayout(QGridLayout())

        self.wrapper_right = QWidget(self)

        wrapper_settings = QWidget(self)
        wrapper_settings.setLayout(QGridLayout())

        self.scroll_area_settings = Wordless_Scroll_Area(self.main, wrapper_settings)
        button_restore_default_settings = QPushButton(self.tr('Restore Default Settings'), self.main)

        button_restore_default_settings.clicked.connect(self.restore_default_settings)

        self.wrapper_right.setLayout(QGridLayout())
        self.wrapper_right.layout().addWidget(self.scroll_area_settings, 0, 0)
        self.wrapper_right.layout().addWidget(button_restore_default_settings, 1, 0)

        self.addWidget(self.wrapper_left)
        self.addWidget(self.wrapper_right)

        self.layout_table = self.wrapper_left.layout()
        self.layout_settings = wrapper_settings.layout()

        self.layout_settings.setContentsMargins(6, 4, 6, 4)

    # If you subclass from QWidget, you need to provide a paintEvent for your custom QWidget as below.
    # See: https://doc.qt.io/qt-5/stylesheet-reference.html#list-of-stylable-widgets - QWidget
    def paintEvent(self, event):
        opt = QStyleOption();
        opt.initFrom(self);
        p = QPainter(self);
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self);
        
    def restore_default_settings(self):
        reply = wordless_message_box.wordless_message_box_restore_default_settings(self.main)

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
