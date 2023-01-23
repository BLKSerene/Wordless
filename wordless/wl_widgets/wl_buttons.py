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
from PyQt5.QtGui import QColor
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

class Wl_Button_Html_Multi_Label(Wl_Button):
    def __init__(self, texts, parent = None):
        super().__init__('', parent)

        self._labels = []
        self._num_labels = len(texts)

        for i in range(self._num_labels):
            self._labels.append(QLabel(texts[i], self))

            self._labels[-1].setTextFormat(Qt.RichText)
            self._labels[-1].setAttribute(Qt.WA_TransparentForMouseEvents)
            self._labels[-1].setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding,
            )

        self.setLayout(wl_layouts.Wl_Layout())

        for i, label in enumerate(self._labels):
            self.layout().addWidget(label, 0, i)

        self.layout().setContentsMargins(5, 0, 5, 0)
        self.layout().setSpacing(5)

    def set_text(self, i, text):
        self._labels[i].setText(text)

        self.updateGeometry()

    def set_texts(self, texts):
        for i, text in enumerate(texts):
            self._labels[i].setText(text)

        self.updateGeometry()

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(
            self.contentsMargins().left()
            + sum((label.sizeHint().width() for label in self._labels))
            + self.layout().spacing() * (self._num_labels - 1)
            + self.contentsMargins().right()
            # Right padding
            + self.main.settings_custom['general']['ui_settings']['font_size'] * 1.5
        )

        return size

class Wl_Button_Browse(Wl_Button):
    def __init__(self, parent, line_edit, caption, filters, initial_filter = -1):
        super().__init__(_tr('Wl_Button_Browse', 'Browse...'), parent)

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

class Wl_Button_Color(Wl_Button_Html_Multi_Label):
    def __init__(self, parent):
        super().__init__([''] * 2, parent)

        self.clicked.connect(self.pick_color)

        self._label_color = self._labels[0]
        self._label_hex = self._labels[1]

        self._label_color.setFixedSize(self.size().height() * 0.65, self.size().height() * 0.65)

    def pick_color(self):
        color_picked = QColorDialog.getColor(QColor(self.get_color()), self.main, _tr('wl_buttons', 'Pick Color'))

        if color_picked.isValid():
            self.set_color(color_picked.name())

    def get_color(self):
        return self._label_hex.text().strip()

    def set_color(self, color):
        self._label_color.setStyleSheet(f'background-color: {color};')
        self._label_hex.setText(color.upper())

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
        super().__init__(_tr('Wl_Button_Restore_Defaults', 'Restore defaults'), parent)

        self.parent = parent
        self.load_settings = load_settings

        self.setMinimumWidth(150)

        self.clicked.connect(self.restore_defaults)

    def restore_defaults(self):
        if wl_msg_boxes.wl_msg_box_question(
            main = self.main,
            title = self.tr('Restore defaults'),
            text = self.tr('''
                <div>Are you sure you want to reset all settings to their defaults?</div>
            ''')
        ):
            self.load_settings(defaults = True)

        self.parent.activateWindow()
