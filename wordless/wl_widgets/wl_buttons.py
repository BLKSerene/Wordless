# ----------------------------------------------------------------------
# Wordless: Widgets - Buttons
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import os

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import (
    QCheckBox, QColorDialog, QFileDialog, QLabel, QPushButton,
    QSizePolicy
)

from wordless.wl_checks import wl_checks_misc
from wordless.wl_dialogs import wl_msg_boxes
from wordless.wl_utils import wl_misc, wl_paths
from wordless.wl_widgets import wl_layouts

_tr = QCoreApplication.translate

class Wl_Button(QPushButton):
    def __init__(self, text, parent = None):
        super().__init__(text, parent)

        self.main = wl_misc.find_wl_main(parent)

# Reference: https://stackoverflow.com/a/62893567
class Wl_Button_Html(Wl_Button):
    def __init__(self, text, parent = None):
        super().__init__('', parent)

        self._label = QLabel(text, self)

        self._label.setTextFormat(Qt.RichText)
        self._label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self._label)

        self.layout().setContentsMargins(0, 0, 0, 0)

    def setText(self, text):
        self._label.setText(text)

        self.updateGeometry()

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(self._label.sizeHint().width())

        return size

class Wl_Button_Browse(Wl_Button):
    def __init__(self, parent, line_edit, caption, filters, initial_filter = -1):
        super().__init__(_tr('wl_buttons', 'Browse...'), parent)

        self.line_edit = line_edit
        self.caption = caption
        self.filters = filters
        self.initial_filter = initial_filter

        self.clicked.connect(self.browse)

    def browse(self):
        path = QFileDialog.getOpenFileName(
            parent = self.main,
            caption = self.caption,
            directory = wl_checks_misc.check_dir(os.path.split(self.line_edit.text())[0]),
            filter = ';;'.join(self.filters),
            initialFilter = self.filters[self.initial_filter]
        )[0]

        if path:
            self.line_edit.setText(wl_paths.get_normalized_path(path))

class Wl_Button_Color(Wl_Button):
    def __init__(self, parent):
        super().__init__('', parent)

        self.clicked.connect(self.pick_color)

    def paintEvent(self, event):
        super().paintEvent(event)

        # A white border within a black border
        painter = QPainter(self)
        painter.setPen(QColor('#000000'))
        painter.setBrush(QBrush(QColor(self.get_color())))

        painter.drawRect(4, 4, 19, 19)

        painter.setPen(QColor('#FFFFFF'))
        painter.drawRect(5, 5, 17, 17)

    def pick_color(self):
        color_picked = QColorDialog.getColor(QColor(self.get_color()), self.main, _tr('wl_buttons', 'Pick Color'))

        if color_picked.isValid():
            self.set_color(color_picked.name().upper())

    def get_color(self):
        return self.text().strip()

    def set_color(self, color):
        self.setText(' ' * 6 + color)

        self.update()

def wl_button_color(parent, allow_transparent = False):
    def transparent_changed():
        if checkbox_transparent.isChecked():
            button_color.setEnabled(False)
        else:
            button_color.setEnabled(True)

    button_color = Wl_Button_Color(parent)

    if allow_transparent:
        checkbox_transparent = QCheckBox(_tr('wl_buttons', 'Transparent'))

        checkbox_transparent.stateChanged.connect(transparent_changed)

        return button_color, checkbox_transparent
    else:
        return button_color

class Wl_Button_Restore_Defaults(Wl_Button):
    def __init__(self, parent, load_settings):
        super().__init__(_tr('wl_buttons', 'Restore defaults'), parent)

        self.parent = parent
        self.load_settings = load_settings

        self.setMinimumWidth(150)

        self.clicked.connect(self.restore_defaults)

    def restore_defaults(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self.main,
            title = self.tr('Restore Defaults'),
            text = self.tr('''
                <div>Are you sure you want to reset all settings to their defaults?</div>
            ''')
        ):
            self.load_settings(defaults = True)

        self.parent.activateWindow()
