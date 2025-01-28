# ----------------------------------------------------------------------
# Wordless: Widgets - Item delegates
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

import math

from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QStyledItemDelegate

from wordless.wl_utils import wl_misc
from wordless.wl_widgets import wl_boxes

class Wl_Item_Delegate_Uneditable(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        pass

class Wl_Item_Delegate(QStyledItemDelegate):
    def __init__(self, parent, widget = None, row = None, col = None):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.widget = widget
        self.row = row
        self.col = col
        self.enabled = True

    def createEditor(self, parent, option, index): # pylint: disable=unused-argument
        if self.widget:
            widget = self.widget(parent)
            widget.setEnabled(self.enabled)

            return widget

        return None

    def set_enabled(self, enabled):
        self.enabled = enabled

# Combo boxes
class Wl_Item_Delegate_Combo_Box(Wl_Item_Delegate):
    def __init__(self, parent, items = None, row = None, col = None, editable = False):
        super().__init__(parent, row = row, col = col)

        self.items = items or []
        self.editable = editable

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if self.is_editable(index):
            painter.save()

            height = option.rect.height()

            top_right = option.rect.topRight()
            top_right_x = top_right.x()
            top_right_y = top_right.y()

            # Arrows
            painter.setBrush(QBrush(QColor(73, 74, 76)))
            painter.drawLine(
                top_right_x - 7 - 8,
                top_right_y + math.ceil((height - 5) / 2),
                top_right_x - 7 - 4,
                top_right_y + math.ceil((height - 5) / 2) + 4
            )
            painter.drawLine(
                top_right_x - 7 - 4,
                top_right_y + math.ceil((height - 5) / 2) + 4,
                top_right_x - 7,
                top_right_y + math.ceil((height - 5) / 2)
            )

            painter.restore()

    def createEditor(self, parent, option, index):
        if self.is_editable(index):
            combo_box = wl_boxes.Wl_Combo_Box(parent)
            combo_box.addItems(self.items)

            combo_box.setEditable(self.editable)
            combo_box.setEnabled(self.enabled)

            return combo_box
        else:
            return None

    def is_editable(self, index):
        rows_editable = cols_editable = False

        if self.row is None or self.row == index.row():
            rows_editable = True
        if self.col is None or self.col == index.column():
            cols_editable = True

        return rows_editable and cols_editable

class Wl_Item_Delegate_Combo_Box_Custom(Wl_Item_Delegate_Combo_Box):
    def __init__(self, parent, Combo_Box, row = None, col = None):
        super().__init__(parent, row = row, col = col)

        self.Combo_Box = Combo_Box

    def createEditor(self, parent, option, index):
        if self.is_editable(index):
            combo_box = self.Combo_Box(parent)
            combo_box.setEnabled(self.enabled)

            return combo_box
        else:
            return None
