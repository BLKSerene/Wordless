# ----------------------------------------------------------------------
# Wordless: Widgets - Layouts
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_utils import wl_misc
from wordless.wl_widgets import wl_buttons

is_macos = wl_misc.check_os()[1]

class Wl_Layout(QtWidgets.QGridLayout):
    def __init__(self):
        super().__init__()

        if is_macos:
            self.setSpacing(8)

class Wl_Wrapper(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setObjectName('wl-wrapper')
        self.setStyleSheet('''
            QWidget#wl-wrapper {
                background-color: #FFF;
            }
        ''')

        self.wrapper_table = QtWidgets.QWidget(self)

        self.wrapper_table.setLayout(Wl_Layout())
        self.wrapper_table.layout().setContentsMargins(0, 0, 0, 0)

        self.scroll_area_settings = Wl_Scroll_Area(self)
        self.button_restore_default_vals = wl_buttons.Wl_Button_Restore_Default_Vals(self, load_settings = self.load_settings)

        self.scroll_area_settings.resize(400, self.scroll_area_settings.size().height())

        self.wrapper_settings_outer = QtWidgets.QWidget(self)
        self.wrapper_settings_outer.setLayout(Wl_Layout())

        self.wrapper_settings = QtWidgets.QWidget(self)
        self.wrapper_settings.setLayout(Wl_Layout())

        self.wrapper_settings.layout().setContentsMargins(0, 0, 0, 0)

        self.wrapper_settings_outer.layout().addWidget(self.wrapper_settings, 0, 0)
        self.wrapper_settings_outer.layout().addWidget(self.button_restore_default_vals, 1, 0)

        self.wrapper_settings_outer.layout().setContentsMargins(8, 6, 8, 6)
        self.wrapper_settings_outer.layout().setRowStretch(2, 1)

        self.scroll_area_settings.setWidget(self.wrapper_settings_outer)

        self.splitter = Wl_Splitter(QtCore.Qt.Horizontal, self)
        self.splitter.addWidget(self.wrapper_table)
        self.splitter.addWidget(self.scroll_area_settings)

        self.splitter.setHandleWidth(5)
        self.splitter.setStretchFactor(0, 1)

        self.splitter.setObjectName('wl-splitter-work-area')
        self.splitter.setStyleSheet('''
            QSplitter#wl-splitter-work-area::handle {
                background-color: #FFF;
            }
        ''')

        self.setLayout(Wl_Layout())
        self.layout().addWidget(self.splitter, 0, 0)

        self.layout().setContentsMargins(8, 6, 8, 6)

    # If you subclass from QWidget, you need to provide a paintEvent for your custom QWidget as below.
    # See: https://doc.qt.io/qt-5/stylesheet-reference.html#list-of-stylable-widgets - QWidget
    def paintEvent(self, event): # pylint: disable=unused-argument
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        p = QtGui.QPainter(self)

        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, p, self)

    def load_settings(self, defaults = False):
        pass

class Wl_Tab_Widget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.tabBar().installEventFilter(self)

    # Disable mouse wheel events for tabs
    def eventFilter(self, obj, event):
        if obj == self.tabBar() and event.type() == QtCore.QEvent.Wheel:
            return True
        else:
            return super().eventFilter(obj, event)

class Wl_Splitter(QtWidgets.QSplitter):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)

        self.main = wl_misc.find_wl_main(parent)

        if is_macos:
            self.setHandleWidth(2)
        else:
            self.setHandleWidth(1)

        self.setChildrenCollapsible(False)

class Wl_Scroll_Area(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setWidgetResizable(True)
        self.setBackgroundRole(QtGui.QPalette.Light)

class Wl_Stacked_Widget_Resizable(QtWidgets.QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.currentChanged.connect(self.current_changed)

    def current_changed(self, index):
        for i in range(self.count()):
            self.widget(i).setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            self.widget(i).adjustSize()

        self.widget(index).setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget(index).adjustSize()

        self.adjustSize()

    def addWidget(self, widget):
        super().addWidget(widget)

        self.currentChanged.emit(self.currentIndex())

class Wl_Separator(QtWidgets.QFrame):
    def __init__(self, parent, orientation = 'hor'):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        match orientation:
            case 'hor':
                self.setFrameShape(QtWidgets.QFrame.HLine)
            case 'vert':
                self.setFrameShape(QtWidgets.QFrame.VLine)

        self.setStyleSheet('color: #D0D0D0;')
