# ----------------------------------------------------------------------
# Wordless: Widgets - Layout
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

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
        self.wrapper_table.layout().setContentsMargins(0, 0, 0, 0)

        self.scroll_area_settings = Wl_Scroll_Area(self)
        self.button_restore_default_settings = wl_button.Wl_Button_Restore_Default_Settings(self)

        self.scroll_area_settings.setFixedWidth(400)

        self.wrapper_settings_outer = QWidget(self)
        self.wrapper_settings_outer.setLayout(Wl_Layout())

        self.wrapper_settings = QWidget(self)
        self.wrapper_settings.setLayout(Wl_Layout())

        self.wrapper_settings.layout().setContentsMargins(0, 0, 0, 0)

        self.wrapper_settings_outer.layout().addWidget(self.wrapper_settings, 0, 0)
        self.wrapper_settings_outer.layout().addWidget(self.button_restore_default_settings, 1, 0)

        self.wrapper_settings_outer.layout().setContentsMargins(8, 6, 8, 6)

        self.scroll_area_settings.setWidget(self.wrapper_settings_outer)

        self.setLayout(Wl_Layout())
        self.layout().addWidget(self.wrapper_table, 0, 0)
        self.layout().addWidget(self.scroll_area_settings, 0, 1)

        self.layout().setContentsMargins(8, 6, 8, 6)

    # If you subclass from QWidget, you need to provide a paintEvent for your custom QWidget as below.
    # See: https://doc.qt.io/qt-5/stylesheet-reference.html#list-of-stylable-widgets - QWidget
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        
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
