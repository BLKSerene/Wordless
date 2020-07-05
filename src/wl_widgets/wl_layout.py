#
# Wordless: Widgets - Layout
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import platform

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_utils import wl_misc
from wl_widgets import wl_button

class Wl_Layout(QGridLayout):
    def __init__(self):
        super().__init__()

        if platform.system() == 'Darwin':
            self.setSpacing(5)

class Wl_Wrapper(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setObjectName('wl-wrapper')
        self.setStyleSheet('''
            QWidget#wl-wrapper {
                background-color: #FFF;
            }
        ''')

        self.wrapper_table = QWidget(self)

        self.wrapper_table.setLayout(Wl_Layout())
        self.wrapper_table.layout().setContentsMargins(8, 8, 6, 6)

        self.wrapper_right = QWidget(self)
        self.wrapper_right.setFixedWidth(340)

        self.scroll_area_settings = Wl_Scroll_Area(self)
        self.button_reset_settings = wl_button.Wl_Button_Reset_Settings(self)

        self.wrapper_settings = QWidget(self)
        self.wrapper_settings.setLayout(Wl_Layout())

        self.wrapper_settings.layout().setContentsMargins(6, 4, 6, 4)

        self.scroll_area_settings.setWidget(self.wrapper_settings)

        self.wrapper_right.setLayout(Wl_Layout())
        self.wrapper_right.layout().addWidget(self.scroll_area_settings, 0, 0)
        self.wrapper_right.layout().addWidget(self.button_reset_settings, 1, 0)

        self.wrapper_right.layout().setContentsMargins(0, 8, 8, 6)

        self.setLayout(Wl_Layout())
        self.layout().addWidget(self.wrapper_table, 0, 0)
        self.layout().addWidget(self.wrapper_right, 0, 1)

        self.layout().setContentsMargins(0, 0, 0, 0)

    # If you subclass from QWidget, you need to provide a paintEvent for your custom QWidget as below.
    # See: https://doc.qt.io/qt-5/stylesheet-reference.html#list-of-stylable-widgets - QWidget
    def paintEvent(self, event):
        opt = QStyleOption();
        opt.initFrom(self);
        p = QPainter(self);
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self);
        
    def load_settings(self, defaults = False):
        pass

class Wl_Wrapper_File_Area(Wl_Wrapper):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet('''
            QWidget#wl-wrapper {
                border: 1px solid #D0D0D0;
                background-color: #FFF;
            }
        ''')

class Wl_Splitter(QSplitter):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setHandleWidth(0)
        self.setChildrenCollapsible(False)

class Wl_Scroll_Area(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setWidgetResizable(True)
        self.setBackgroundRole(QPalette.Light)

class Wl_Stacked_Widget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.currentChanged.connect(self.current_changed)

    def current_changed(self, index):
        for i in range(self.count()):
            self.widget(i).setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.widget(i).adjustSize()

        self.widget(index).setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
        self.widget(index).adjustSize()

        self.adjustSize()

    def addWidget(self, widget):
        super().addWidget(widget)

        self.currentChanged.emit(self.currentIndex())

class Wl_Separator(QFrame):
    def __init__(self, parent, orientation = 'Horizontal'):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        if orientation == 'Horizontal':
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)

        self.setStyleSheet('color: #D0D0D0;')
