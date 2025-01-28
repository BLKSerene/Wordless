# ----------------------------------------------------------------------
# Wordless: Widgets - Boxes
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

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QSpinBox
)

from wordless.wl_measures import wl_measure_utils
from wordless.wl_utils import wl_misc

_tr = QCoreApplication.translate

# Combo boxes
class Wl_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QComboBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Combo_Box_Adjustable(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

class Wl_Combo_Box_Enums(Wl_Combo_Box):
    def __init__(self, parent, enums):
        super().__init__(parent)

        self._enums = enums

        self.addItems(self._enums)

    def get_val(self):
        return self._enums[self.currentText()]

    def set_val(self, val):
        for val_name, val_code in self._enums.items():
            if val == val_code:
                super().setCurrentText(val_name)

                break

class Wl_Combo_Box_Yes_No(Wl_Combo_Box_Enums):
    def __init__(self, parent):
        super().__init__(parent, enums = {
            _tr('wl_boxes', 'Yes'): True,
            _tr('wl_boxes', 'No'): False
        })

    def get_yes_no(self):
        return super().get_val()

    def set_yes_no(self, yes_no):
        super().set_val(yes_no)

class Wl_Combo_Box_Lang(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['langs']))

class Wl_Combo_Box_Encoding(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(list(self.main.settings_global['encodings']))

class Wl_Combo_Box_Measure(Wl_Combo_Box):
    def __init__(self, parent, measure_type):
        super().__init__(parent)

        self.measure_type = measure_type

        self.addItems(self.main.settings_global['mapping_measures'][self.measure_type])

    def get_measure(self):
        return wl_measure_utils.to_measure_code(self.main, self.measure_type, self.currentText())

    def set_measure(self, measure):
        for i in range(self.count()):
            if wl_measure_utils.to_measure_text(self.main, self.measure_type, measure) == self.itemText(i):
                self.setCurrentIndex(i)

class Wl_Combo_Box_File_To_Filter(Wl_Combo_Box):
    def __init__(self, parent, table):
        super().__init__(parent)

        self.table = table

        self.table.model().itemChanged.connect(self.table_item_changed)

        self.table_item_changed()

    def table_item_changed(self):
        self.blockSignals(True)

        file_to_filter_old = self.currentText()

        self.clear()

        for file in self.table.settings['file_area']['files_open']:
            if file['selected']:
                self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        self.setCurrentText(file_to_filter_old)

        self.blockSignals(False)

        self.currentTextChanged.emit(self.currentText())

class Wl_Combo_Box_File(Wl_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        # Clip long file names
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.addItems(self.main.wl_file_area.get_selected_file_names())

        self.main.wl_file_area.table_files.model().itemChanged.connect(self.wl_files_changed)

        self.wl_files_changed()

    def wl_files_changed(self):
        pass

    def get_file(self):
        return self.main.wl_file_area.find_file_by_name(self.currentText(), selected_only = True)

class Wl_Combo_Box_Font_Family(QFontComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setMaxVisibleItems(20)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QComboBox.wheelEvent(self, event)
        else:
            event.ignore()

# Spin boxes
class Wl_Spin_Box(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Spin_Box_Window(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(-100, 100)

        self.valueChanged.connect(self.value_changed)

    def stepBy(self, steps):
        if self.prefix() == self.tr('L'):
            super().stepBy(-steps)
        elif self.prefix() == self.tr('R'):
            super().stepBy(steps)

    def value_changed(self):
        if self.value() <= 0:
            if self.prefix() == self.tr('L'):
                self.setPrefix(self.tr('R'))
            else:
                self.setPrefix(self.tr('L'))

            self.setValue(-self.value() + 1)

class Wl_Spin_Box_Font_Size(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(6, 20)

class Wl_Spin_Box_Font_Weight(Wl_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(0, 1000)

# Double spin boxes
class Wl_Double_Spin_Box(QDoubleSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setDecimals(2)
        self.setSingleStep(.01)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            QDoubleSpinBox.wheelEvent(self, event)
        else:
            event.ignore()

class Wl_Double_Spin_Box_Alpha(Wl_Double_Spin_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(0, 1)

# Box combinations
def wl_spin_box_no_limit(parent, val_min = 1, val_max = 100, double = False):
    def no_limit_changed():
        if checkbox_no_limit.isChecked():
            spin_box_val.setEnabled(False)
        else:
            spin_box_val.setEnabled(True)

    if double:
        spin_box_val = Wl_Double_Spin_Box(parent)
    else:
        spin_box_val = Wl_Spin_Box(parent)

    checkbox_no_limit = QCheckBox(_tr('wl_boxes', 'No limit'), parent)

    spin_box_val.setRange(val_min, val_max)

    checkbox_no_limit.stateChanged.connect(no_limit_changed)

    no_limit_changed()

    return spin_box_val, checkbox_no_limit

# Defer evaluation of default values of functions until QTranslator is initialized
def wl_spin_boxes_min_max(
    parent,
    label_min = None, label_max = None,
    val_min = 1, val_max = 100,
    double = False
):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    label_min = label_min or _tr('wl_boxes', 'From')
    label_max = label_max or _tr('wl_boxes', 'to')

    label_min = QLabel(label_min, parent)
    label_max = QLabel(label_max, parent)

    if double:
        spin_box_min = Wl_Double_Spin_Box(parent)
        spin_box_max = Wl_Double_Spin_Box(parent)
    else:
        spin_box_min = Wl_Spin_Box(parent)
        spin_box_max = Wl_Spin_Box(parent)

    spin_box_min.setRange(val_min, val_max)
    spin_box_max.setRange(val_min, val_max)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    min_changed()
    max_changed()

    return (
        label_min, spin_box_min,
        label_max, spin_box_max
    )

def wl_spin_boxes_min_max_sync(
    parent,
    label_min = None, label_max = None,
    val_min = 1, val_max = 100,
    double = False
):
    def sync_changed():
        if checkbox_sync.isChecked():
            spin_box_min.setValue(spin_box_max.value())

    def min_changed():
        if checkbox_sync.isChecked() or spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if checkbox_sync.isChecked() or spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    label_min = label_min or _tr('wl_boxes', 'From')
    label_max = label_max or _tr('wl_boxes', 'to')

    checkbox_sync = QCheckBox(_tr('wl_boxes', 'Sync'), parent)

    (
        label_min, spin_box_min,
        label_max, spin_box_max
    ) = wl_spin_boxes_min_max(parent, label_min, label_max, val_min, val_max, double)

    spin_box_min.valueChanged.disconnect()
    spin_box_max.valueChanged.disconnect()

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    checkbox_sync.stateChanged.connect(sync_changed)

    min_changed()
    max_changed()
    sync_changed()

    return (
        checkbox_sync,
        label_min, spin_box_min,
        label_max, spin_box_max
    )

def wl_spin_boxes_min_max_sync_window(parent):
    def sync_changed():
        if checkbox_sync.isChecked():
            spin_box_left.setPrefix(spin_box_right.prefix())
            spin_box_left.setValue(spin_box_right.value())

    def left_changed():
        if (
            checkbox_sync.isChecked()
            or (
                spin_box_left.prefix() == _tr('wl_boxes', 'L')
                and spin_box_right.prefix() == _tr('wl_boxes', 'L')
                and spin_box_left.value() < spin_box_right.value()
            ) or (
                spin_box_left.prefix() == _tr('wl_boxes', 'R')
                and spin_box_right.prefix() == _tr('wl_boxes', 'R')
                and spin_box_left.value() > spin_box_right.value()
            ) or (
                spin_box_left.prefix() == _tr('wl_boxes', 'R')
                and spin_box_right.prefix() == _tr('wl_boxes', 'L')
            )
        ):
            spin_box_right.setPrefix(spin_box_left.prefix())
            spin_box_right.setValue(spin_box_left.value())

    def right_changed():
        if (
            checkbox_sync.isChecked()
            or (
                spin_box_left.prefix() == _tr('wl_boxes', 'L')
                and spin_box_right.prefix() == _tr('wl_boxes', 'L')
                and spin_box_left.value() < spin_box_right.value()
            ) or (
                spin_box_left.prefix() == _tr('wl_boxes', 'R')
                and spin_box_right.prefix() == _tr('wl_boxes', 'R')
                and spin_box_left.value() > spin_box_right.value()
            ) or (
                spin_box_left.prefix() == _tr('wl_boxes', 'R')
                and spin_box_right.prefix() == _tr('wl_boxes', 'L')
            )
        ):
            spin_box_left.setPrefix(spin_box_right.prefix())
            spin_box_left.setValue(spin_box_right.value())

    checkbox_sync = QCheckBox(_tr('wl_boxes', 'Sync'), parent)
    label_left = QLabel(_tr('wl_boxes', 'From'), parent)
    spin_box_left = Wl_Spin_Box_Window(parent)
    label_right = QLabel(_tr('wl_boxes', 'to'), parent)
    spin_box_right = Wl_Spin_Box_Window(parent)

    spin_box_left.setRange(-100, 100)
    spin_box_right.setRange(-100, 100)

    checkbox_sync.stateChanged.connect(sync_changed)
    spin_box_left.valueChanged.connect(left_changed)
    spin_box_right.valueChanged.connect(right_changed)

    sync_changed()
    left_changed()
    right_changed()

    return (
        checkbox_sync,
        label_left, spin_box_left,
        label_right, spin_box_right
    )

def wl_spin_boxes_min_max_no_limit(
    parent,
    label_min = None, label_max = None,
    val_min = 1, val_max = 100,
    double = False, sync = True
):
    def no_limit_min_changed():
        if checkbox_min_no_limit.isChecked():
            spin_box_min.setEnabled(False)
        else:
            spin_box_min.setEnabled(True)

    def no_limit_max_changed():
        if checkbox_max_no_limit.isChecked():
            spin_box_max.setEnabled(False)
        else:
            spin_box_max.setEnabled(True)

    label_min = label_min or _tr('wl_boxes', 'From')
    label_max = label_max or _tr('wl_boxes', 'to')

    (
        checkbox_sync,
        label_min, spin_box_min,
        label_max, spin_box_max
    ) = wl_spin_boxes_min_max_sync(parent, label_min, label_max, val_min, val_max, double)

    checkbox_min_no_limit = QCheckBox(_tr('wl_boxes', 'No limit'), parent)
    checkbox_max_no_limit = QCheckBox(_tr('wl_boxes', 'No limit'), parent)

    checkbox_min_no_limit.stateChanged.connect(no_limit_min_changed)
    checkbox_max_no_limit.stateChanged.connect(no_limit_max_changed)

    if not sync:
        checkbox_sync.setChecked(False)

    no_limit_min_changed()
    no_limit_max_changed()

    if sync:
        return (
            checkbox_sync,
            label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit
        )
    else:
        return (
            label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit
        )
