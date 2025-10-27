# ----------------------------------------------------------------------
# Wordless: Widgets - Lists
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

import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_checks import (
    wl_checks_files,
    wl_checks_misc
)
from wordless.wl_dialogs import (
    wl_dialogs,
    wl_dialogs_errs
)
from wordless.wl_utils import (
    wl_detection,
    wl_misc
)

_tr = QtCore.QCoreApplication.translate

is_macos = wl_misc.check_os()[1]

# self.tr() may not work in inherited classes
# See: https://www.riverbankcomputing.com/static/Docs/PyQt5/i18n.html#differences-between-pyqt5-and-qt
class Wl_List_Add_Ins_Del_Clr(QtWidgets.QListView):
    enter_pressed = QtCore.pyqtSignal()

    def __init__(
        self, parent,
        new_item_text = '',
        editable = True,
        drag_drop = True
    ):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)
        self.new_item_text = new_item_text if new_item_text else _tr('wl_lists', 'New item')
        self.items_old = []

        if editable:
            self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.SelectedClicked | QtWidgets.QAbstractItemView.EditKeyPressed)
        else:
            self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        if drag_drop:
            self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.setModel(QtCore.QStringListModel(self))

        self.model().dataChanged.connect(self.data_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed)

        self.button_add = QtWidgets.QPushButton(_tr('wl_lists', 'Add'), self)
        self.button_ins = QtWidgets.QPushButton(_tr('wl_lists', 'Insert'), self)
        self.button_del = QtWidgets.QPushButton(_tr('wl_lists', 'Remove'), self)
        self.button_clr = QtWidgets.QPushButton(_tr('wl_lists', 'Clear'), self)

        self.button_add.clicked.connect(self.add_item)
        self.button_ins.clicked.connect(self.ins_item)
        self.button_del.clicked.connect(self.del_item)
        self.button_clr.clicked.connect(self.clr_list)

    # There seems to be a bug with QAbstractItemView.InternalMove
    # See: https://bugreports.qt.io/browse/QTBUG-87057
    def dropEvent(self, event):
        if self.indexAt(event.pos()).row() == -1:
            row_dropped_on = self.model().rowCount()
        else:
            row_dropped_on = self.indexAt(event.pos()).row()

        data = self.model().stringList()
        items_selected = []

        for row in sorted([index.row() for index in self.selectionModel().selectedRows()]):
            items_selected.append(data[row])
            data[row] = ''

        for item in reversed(items_selected):
            data.insert(row_dropped_on, item)

        self.model().setStringList([datum for datum in data if datum])

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

        event.accept()

    def keyPressEvent(self, event):
        match event.key():
            # Clear the selected item if no item is being edited
            case QtCore.Qt.Key_Backspace:
                if not self.findChild(QtWidgets.QLineEdit) and self.get_selected_rows():
                    self.edit(self.model().index(self.get_selected_rows()[-1]))
                    self.findChild(QtWidgets.QLineEdit).clear()
                else:
                    super().keyPressEvent(event)
            # Start editing after moving up or down if the previously selected item is being edited
            case QtCore.Qt.Key_Up | QtCore.Qt.Key_Down | QtCore.Qt.Key_PageUp | QtCore.Qt.Key_PageDown | QtCore.Qt.Key_Home | QtCore.Qt.Key_End:
                # On OSes other than macOS, home and end keys jump to the first or last item or the start or end of the item being edited
                if (
                    (event.key() not in {QtCore.Qt.Key_Home, QtCore.Qt.Key_End} or is_macos)
                    and self.get_selected_rows()
                ):
                    row_selected_prev = self.get_selected_rows()[-1]
                    editing = self.findChild(QtWidgets.QLineEdit)

                    super().keyPressEvent(event)

                    # No need to start editing if the previously selected item is the first or last item
                    if editing and self.get_selected_rows() and row_selected_prev != self.get_selected_rows()[-1]:
                        self.edit(self.model().index(self.get_selected_rows()[-1]))
                # On macOS, home and end keys always jump to the first or last item
                else:
                    super().keyPressEvent(event)
            # Insert an item if no item is being edited
            case QtCore.Qt.Key_Insert:
                if not self.findChild(QtWidgets.QLineEdit) and self.get_selected_rows():
                    self.ins_item()
                else:
                    super().keyPressEvent(event)
            case QtCore.Qt.Key_Delete:
                self.del_item()
            # Clear the item being edited or whole list
            # Do nothing on OSes other than macOS as there is no clear key
            case QtCore.Qt.Key_Clear:
                if is_macos:
                    if (line_edit := self.findChild(QtWidgets.QLineEdit)):
                        line_edit.clear()
                    else:
                        self.clr_list()
                else:
                    super().keyPressEvent(event)
            # Generate the table if no item is being edited
            # Key_Return is the main key return/enter and Key_Enter is the enter key in the numeric keypad
            case QtCore.Qt.Key_Return | QtCore.Qt.Key_Enter:
                if self.findChild(QtWidgets.QLineEdit):
                    super().keyPressEvent(event)
                else:
                    self.enter_pressed.emit()
            case _:
                super().keyPressEvent(event)

    def data_changed(self, topLeft = None, bottomRight = None): # pylint: disable=unused-argument
        if self.model().rowCount():
            self.button_clr.setEnabled(True)
        else:
            self.button_clr.setEnabled(False)

        if topLeft:
            item_row = topLeft.row()

            # Check for empty and duplicate items
            if item_row != -1:
                item_text = self.model().stringList()[item_row]

                if wl_misc.RE_EMPTY_ITEM.search(item_text):
                    data = self.model().stringList()
                    data[item_row] = self.items_old[item_row]

                    self.model().setStringList(data)
                else:
                    for i, text in enumerate(self.model().stringList()):
                        if i != item_row and item_text == text:
                            # Use exec() instead of open() here to allow editing to be started
                            wl_dialogs.Wl_Dialog_Info_Simple(
                                self.main,
                                title = _tr('wl_lists', 'Duplicate Items'),
                                text = _tr('wl_lists', '''
                                    <div>The item that you have edited already exists in the list.</div>
                                    <br>
                                    <div>Please specify another item.</div>
                                '''),
                                icon = 'warning'
                            ).exec()

                            data = self.model().stringList()
                            data[item_row] = self.items_old[item_row]

                            self.model().setStringList(data)

                            self.edit(topLeft)

                            break

                    self.items_old[item_row] = self.model().stringList()[item_row]

        self.selectionModel().selectionChanged.emit(QtCore.QItemSelection(), QtCore.QItemSelection())

    def selection_changed(self):
        if self.selectionModel().selectedIndexes():
            self.button_ins.setEnabled(True)
            self.button_del.setEnabled(True)
        else:
            self.button_ins.setEnabled(False)
            self.button_del.setEnabled(False)

    def get_selected_rows(self):
        return [index.row() for index in self.selectionModel().selectedIndexes()]

    def _add_item(self, text = '', row = None):
        if text:
            item_text = wl_checks_misc.check_new_name(text, self.model().stringList())
        else:
            item_text = wl_checks_misc.check_new_name(self.new_item_text, self.model().stringList())

        data = self.model().stringList()

        if row is None:
            data.append(item_text)
            self.items_old.append(item_text)
        else:
            data.insert(row, item_text)
            self.items_old.insert(row, item_text)

        self.model().setStringList(data)

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def _add_items(self, texts, row = None):
        data = self.model().stringList()
        texts = [wl_checks_misc.check_new_name(text, data) for text in list(dict.fromkeys(texts))]

        if row is None:
            data.extend(texts)
            self.items_old.extend(texts)

            self.model().setStringList(data)
        else:
            data[row:row] = texts
            self.items_old[row:row] = texts

            self.model().setStringList(data)

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def add_item(self, text = ''):
        self._add_item(text = text)
        self.setCurrentIndex(self.model().index(self.model().rowCount() - 1))

        self.edit(self.model().index(self.model().rowCount() - 1))

    # Insert before the last selected item
    def ins_item(self, text = ''):
        row = self.get_selected_rows()[-1]

        self._add_item(text = text, row = row)
        self.setCurrentIndex(self.model().index(row))

        self.edit(self.model().index(row))

    def del_item(self):
        data = self.model().stringList()

        for row in sorted(self.get_selected_rows(), reverse = True):
            del data[row]
            del self.items_old[row]

        self.model().setStringList(data)

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def clr_list(self):
        self.model().setStringList([])
        self.items_old = []

        self.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def load_items(self, texts):
        self.clr_list()

        self._add_items(texts)
        self.scrollToTop()

class Wl_List_Add_Ins_Del_Clr_Imp_Exp(Wl_List_Add_Ins_Del_Clr):
    def __init__(
        self, parent,
        new_item_text,
        settings, exp_file_name,
        editable = True, drag_drop = True
    ):
        super().__init__(
            parent,
            new_item_text = new_item_text,
            editable = editable,
            drag_drop = drag_drop
        )

        self.settings = settings
        self.exp_file_name = exp_file_name

        self.button_imp = QtWidgets.QPushButton(_tr('wl_lists', 'Import...'), self)
        self.button_exp = QtWidgets.QPushButton(_tr('wl_lists', 'Export...'), self)

        self.button_imp.clicked.connect(self.imp_list)
        self.button_exp.clicked.connect(self.exp_list)

    def data_changed(self, topLeft = None, bottomRight = None):
        if self.model().rowCount():
            self.button_exp.setEnabled(True)
        else:
            self.button_exp.setEnabled(False)

        super().data_changed(topLeft, bottomRight)

    def imp_list(self):
        if os.path.exists(self.main.settings_custom['general']['imp'][self.settings]['default_path']):
            default_dir = self.main.settings_custom['general']['imp'][self.settings]['default_path']
        else:
            default_dir = self.main.settings_default['general']['imp'][self.settings]['default_path']

        file_paths = QtWidgets.QFileDialog.getOpenFileNames(
            parent = self.main,
            caption = _tr('wl_lists', 'Import from Files'),
            directory = default_dir,
            filter = _tr('wl_lists', 'Text files (*.txt)')
        )[0]

        if file_paths:
            # Modify default path
            self.main.settings_custom['general']['imp'][self.settings]['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            file_paths, file_paths_empty = wl_checks_files.check_file_paths_empty(self.main, file_paths)

            if file_paths_empty:
                dialog_err_files = wl_dialogs_errs.Wl_Dialog_Err_Files(self.main, _tr('wl_lists', 'Import Error'))

                dialog_err_files.label_err.set_text(_tr('wl_lists', '''
                    <div>An error occurred during import. Please check the following files and try again.</div>
                '''))

                dialog_err_files.table_err_files.model().setRowCount(len(file_paths_empty))

                dialog_err_files.table_err_files.disable_updates()

                for i, file_path in enumerate(file_paths_empty):
                    dialog_err_files.table_err_files.model().setItem(
                        i, 0,
                        QtGui.QStandardItem(_tr('wl_lists', 'Empty file'))
                    )
                    dialog_err_files.table_err_files.model().setItem(
                        i, 1,
                        QtGui.QStandardItem(file_path)
                    )

                dialog_err_files.table_err_files.enable_updates()

                dialog_err_files.exec()

                self.main.statusBar().showMessage(_tr('wl_lists', 'An error occurred during import!'))
            else:
                # Check duplicate items
                items_to_imp = []
                items_cur = self.model().stringList()

                num_prev = len(items_cur)

                for file_path in file_paths:
                    # Detect encodings
                    if self.main.settings_custom['general']['imp'][self.settings]['detect_encodings']:
                        encoding = wl_detection.detect_encoding(self.main, file_path)
                    else:
                        encoding = self.main.settings_custom['general']['imp'][self.settings]['default_encoding']

                    with open(file_path, 'r', encoding = encoding, errors = 'replace') as f:
                        text = f.read()

                    for line in text.split('\n'):
                        line = line.strip()

                        if line and line not in items_cur:
                            items_to_imp.append(line)

                self._add_items(items_to_imp)

                num_imps = self.model().rowCount() - num_prev
                msg_item = _tr('wl_lists', 'item') if num_imps == 1 else _tr('wl_lists', 'items')

                self.main.statusBar().showMessage(_tr('wl_lists', '{} {} has been successfully imported into the list.').format(num_imps, msg_item))

    def exp_list(self):
        default_dir = self.main.settings_custom['general']['exp'][self.settings]['default_path']

        file_path = QtWidgets.QFileDialog.getSaveFileName(
            parent = self.main,
            caption = _tr('wl_lists', 'Export to File'),
            directory = os.path.join(wl_checks_misc.check_dir(default_dir), self.exp_file_name),
            filter = _tr('wl_lists', 'Text files (*.txt)')
        )[0]

        if file_path:
            encoding = self.main.settings_custom['general']['exp'][self.settings]['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.model().stringList():
                    f.write(item + '\n')

            wl_dialogs.Wl_Dialog_Info_Simple(
                self.parent(),
                title = _tr('wl_lists', 'Export Completed'),
                text = _tr('wl_lists', '''
                    <div>The list has been successfully exported to "{}".</div>
                ''').format(file_path)
            ).open()

            # Modify default path
            self.main.settings_custom['general']['exp'][self.settings]['default_path'] = os.path.normpath(os.path.dirname(file_path))
