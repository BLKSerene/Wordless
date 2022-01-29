# ----------------------------------------------------------------------
# Wordless: Widgets - Lists
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

import os
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_checking import wl_checking_files, wl_checking_misc
from wl_dialogs import wl_dialogs_errs, wl_msg_boxes
from wl_widgets import wl_boxes
from wl_utils import wl_detection, wl_misc

class Wl_List_Add_Ins_Del_Clr(QListView):
    def __init__(
        self, parent,
        new_item_text = '',
        editable = True, drag_drop = True
    ):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)
        self.new_item_text = new_item_text if new_item_text else self.tr('New item')
        self.items_old = []

        if editable:
            self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        else:
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        if drag_drop:
            self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setModel(QStringListModel(self))

        self.model().dataChanged.connect(self.data_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed)

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_ins = QPushButton(self.tr('Insert'), self)
        self.button_del = QPushButton(self.tr('Remove'), self)
        self.button_clr = QPushButton(self.tr('Clear'), self)

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

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())

        event.accept()

    def data_changed(self, topLeft = None, bottomRight = None):
        if self.model().rowCount():
            self.button_clr.setEnabled(True)
        else:
            self.button_clr.setEnabled(False)

        # Check for duplicate items
        if topLeft:
            item_row = topLeft.row()

            if item_row != -1:
                item_text = self.model().stringList()[item_row]

                if re.search(r'^\s*$', item_text):
                    self.model().stringList()[item_row] = self.items_old[item_row]
                else:
                    for i, text in enumerate(self.model().stringList()):
                        if i != item_row and item_text == text:
                            wl_msg_boxes.Wl_Msg_Box_Warning(
                                self.main,
                                title = self.tr('Duplicates Found'),
                                text = self.tr('''
                                    <div>The item that you have just edited already exists in the list, please specify another one!</div>
                                ''')
                            ).exec_()

                            data = self.model().stringList()
                            data[item_row] = self.items_old[item_row]

                            self.model().setStringList(data)

                            self.setCurrentIndex(topLeft)
                            self.closePersistentEditor(topLeft)
                            self.edit(topLeft)

                            break

                    self.items_old[item_row] = self.model().stringList()[item_row]

        self.selection_changed()

    def selection_changed(self):
        if self.selectionModel().selectedIndexes():
            self.button_ins.setEnabled(True)
            self.button_del.setEnabled(True)
        else:
            self.button_ins.setEnabled(False)
            self.button_del.setEnabled(False)

    def _add_item(self, text = '', row = None):
        if text:
            item_text = wl_checking_misc.check_new_name(text, self.model().stringList())
        else:
            item_text = wl_checking_misc.check_new_name(self.new_item_text, self.model().stringList())

        data = self.model().stringList()

        if row is None:
            data.append(item_text)
            self.items_old.append(item_text)
        else:
            data.insert(row, item_text)
            self.items_old.insert(row, item_text)

        self.model().setStringList(data)

        if row is None:
            self.setCurrentIndex(self.model().index(self.model().rowCount() - 1))
        else:
            self.setCurrentIndex(self.model().index(row))

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())

    def _add_items(self, texts, row = None):
        data = self.model().stringList()
        texts = [wl_checking_misc.check_new_name(text, data) for text in list(dict.fromkeys(texts))]

        if row is None:
            data.extend(texts)
            self.items_old.extend(texts)

            self.model().setStringList(data)
        else:
            data[row:row] = texts
            self.items_old[row:row] = texts

            self.model().setStringList(data)

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())

    def add_item(self, text = ''):
        self._add_item(text = text)

    def add_items(self, texts):
        self._add_items(texts = texts)

    def ins_item(self, text = ''):
        self._add_item(text = text, row = self.selectionModel().selectedRows()[0].row())

    def ins_items(self, texts):
        self._add_items(texts = reversed(texts), row = self.selectionModel().selectedRows()[0].row())

    def del_item(self):
        data = self.model().stringList()

        for row in reversed(self.selectionModel().selectedRows()):
            del data[row.row()]
            del self.items_old[row.row()]

        self.model().setStringList(data)

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())

    def clr_list(self):
        self.model().setStringList([])
        self.items_old = []

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())

    def load_items(self, texts):
        self.clr_list()

        self.add_items(texts)
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

        self.button_imp = QPushButton(self.tr('Import'), self)
        self.button_exp = QPushButton(self.tr('Export'), self)

        self.button_imp.clicked.connect(self.imp_list)
        self.button_exp.clicked.connect(self.exp_list)

    def data_changed(self, topLeft = None, bottomRight = None):
        super().data_changed(topLeft, bottomRight)

        if self.model().rowCount():
            self.button_exp.setEnabled(True)
        else:
            self.button_exp.setEnabled(False)

    def imp_list(self):
        if os.path.exists(self.main.settings_custom['import'][self.settings]['default_path']):
            default_dir = self.main.settings_custom['import'][self.settings]['default_path']
        else:
            default_dir = self.main.settings_default['import'][self.settings]['default_path']

        file_paths = QFileDialog.getOpenFileNames(
            self.main,
            self.tr('Import from Files'),
            default_dir,
            self.tr('Text File (*.txt)')
        )[0]

        if file_paths:
            # Modify default path
            self.main.settings_custom['import'][self.settings]['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            file_paths, file_paths_empty = wl_checking_files.check_file_paths_empty(self.main, file_paths)

            if file_paths_empty:
                dialog_err_files = wl_dialogs_errs.Wl_Dialog_Err_Files(self.main, self.tr('Import Error'))

                dialog_err_files.label_err.set_text(self.tr('''
                    <div>
                        An error occurred during import, please check the following files and try again.
                    </div>
                '''))

                dialog_err_files.table_err_files.model().setRowCount(len(file_paths_empty))

                dialog_err_files.table_err_files.disable_updates()

                for i, file_path in enumerate(file_paths_empty):
                    dialog_err_files.table_err_files.model().setItem(
                        i, 0,
                        QStandardItem(self.tr('Empty File'))
                    )
                    dialog_err_files.table_err_files.model().setItem(
                        i, 1,
                        QStandardItem(file_path)
                    )

                dialog_err_files.table_err_files.enable_updates()

                dialog_err_files.open()

                self.main.statusBar().showMessage(self.tr('An error occured during import!'))
            else:
                # Check duplicate items
                items_to_import = []
                items_cur = self.model().stringList()

                num_prev = len(items_cur)

                for file_path in file_paths:
                    # Detect encodings
                    if self.main.settings_custom['import'][self.settings]['detect_encodings']:
                        encoding = wl_detection.detect_encoding(self.main, file_path)
                    else:
                        encoding = self.main.settings_custom['import'][self.settings]['default_encoding']

                    with open(file_path, 'r', encoding = encoding, errors = 'replace') as f:
                        text = f.read()

                    for line in text.split('\n'):
                        line = line.strip()

                        if line and line not in items_cur:
                            items_to_import.append(line)

                self.add_items(items_to_import)

                num_imported = self.model().rowCount() - num_prev

                if num_imported == 0:
                    self.main.statusBar().showMessage(self.tr('No items were imported into the list.'))
                elif num_imported == 1:
                    self.main.statusBar().showMessage(self.tr('1 item has been successfully imported into the list.'))
                else:
                    self.main.statusBar().showMessage(self.tr(f'{num_imported:,} items have been successfully imported into the list.'))

    def exp_list(self):
        default_dir = self.main.settings_custom['export'][self.settings]['default_path']

        file_path = QFileDialog.getSaveFileName(
            self.main,
            self.tr('Export to File'),
            os.path.join(wl_checking_misc.check_dir(default_dir), self.exp_file_name),
            self.tr('Text File (*.txt)')
        )[0]

        if file_path:
            encoding = self.main.settings_custom['export'][self.settings]['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.model().stringList():
                    f.write(item + '\n')

            wl_msg_boxes.wl_msg_box_export_list(self.main, file_path)

            # Modify default path
            self.main.settings_custom['export'][self.settings]['default_path'] = os.path.normpath(os.path.dirname(file_path))

class Wl_List_Search_Terms(Wl_List_Add_Ins_Del_Clr_Imp_Exp):
    def __init__(self, parent):
        super().__init__(
            parent,
            new_item_text = parent.tr('New search term'),
            settings = 'search_terms',
            exp_file_name = 'wordless_search_terms.txt'
        )

class Wl_List_Stop_Words(Wl_List_Add_Ins_Del_Clr_Imp_Exp):
    def __init__(self, parent):
        super().__init__(
            parent,
            new_item_text = parent.tr('New stop word'),
            settings = 'stop_words',
            exp_file_name = 'wordless_stop_words.txt'
        )

    def data_changed_default(self):
        super().data_changed()

        self.button_clr.setEnabled(False)

    def selection_changed_default(self):
        super().selection_changed()

        self.button_ins.setEnabled(False)
        self.button_del.setEnabled(False)

    def switch_to_custom(self):
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.setDragEnabled(True)

        self.button_add.setEnabled(True)
        self.button_imp.setEnabled(True)

        self.model().dataChanged.disconnect()
        self.selectionModel().selectionChanged.disconnect()

        self.model().dataChanged.connect(self.data_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed)

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())

    def switch_to_default(self):
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(False)

        self.button_add.setEnabled(False)
        self.button_imp.setEnabled(False)

        self.model().dataChanged.disconnect()
        self.selectionModel().selectionChanged.disconnect()

        self.model().dataChanged.connect(self.data_changed)
        self.model().dataChanged.connect(self.data_changed_default)
        self.selectionModel().selectionChanged.connect(self.selection_changed)
        self.selectionModel().selectionChanged.connect(self.selection_changed_default)

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())

class Wl_List_Files(Wl_List_Add_Ins_Del_Clr):
    def __init__(self, parent):
        super().__init__(parent)

        self.setItemDelegate(wl_boxes.Wl_Item_Delegate_Combo_Box_Custom(self, wl_boxes.Wl_Combo_Box_File))

        self.main.wl_files.table.model().itemChanged.connect(self.wl_files_changed_buttons)
        self.main.wl_files.table.model().itemChanged.connect(self.wl_files_changed_items)

    def selection_changed(self):
        super().selection_changed()

        self.wl_files_changed_buttons()

    def wl_files_changed_buttons(self):
        if self.model().rowCount() >= len(self.main.wl_files.get_selected_files()):
            self.button_add.setEnabled(False)
            self.button_ins.setEnabled(False)
        else:
            self.button_add.setEnabled(True)

            if self.selectionModel().selectedIndexes():
                self.button_ins.setEnabled(True)

    def wl_files_changed_items(self):
        data = self.model().stringList()
        rows_selected = [index.row() for index in self.selectionModel().selectedIndexes()]
        file_names_old = self.main.wl_files.file_names_old
        file_names_selected = self.main.wl_files.get_selected_file_names()

        # Files renamed or reordered
        if len(file_names_selected) == len(file_names_old):
            # Files renamed
            if len([
                True
                for file_name_selected, file_name_old in zip(file_names_selected, file_names_old)
                if file_name_selected != file_name_old
            ]) == 1:
                for file_name_selected, file_name_old in zip(file_names_selected, file_names_old):
                    if file_name_selected != file_name_old and file_name_old in data:
                        data[data.index(file_name_old)] = file_name_selected

                        break
        # Files added or removed
        else:
            for i, item in reversed(list(enumerate(data))):
                if item not in file_names_selected:
                    # Adjust current selection
                    for j, row in reversed(list(enumerate(rows_selected))):
                        if row == i:
                            del rows_selected[j]
                        elif row > i:
                            rows_selected[j] -= 1

                    del data[i]
                    del self.items_old[i]

        self.model().setStringList(data)

        for row in rows_selected:
            self.selectionModel().select(self.model().index(row), QItemSelectionModel.Select)

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())

    def _add_item(self, text = '', row = None):
        data = self.model().stringList()

        if text:
            item_text = text
        else:
            file_names = set(data)

            for file_name in self.main.wl_files.get_selected_file_names():
                if file_name not in file_names:
                    item_text = file_name

                    break

        if row is None:
            data.append(item_text)
            self.items_old.append(item_text)
        else:
            data.insert(row, item_text)
            self.items_old.insert(row, item_text)

        self.model().setStringList(data)

        if row is None:
            self.setCurrentIndex(self.model().index(self.model().rowCount() - 1))
        else:
            self.setCurrentIndex(self.model().index(row))

        self.model().dataChanged.emit(QModelIndex(), QModelIndex())
        self.selectionModel().selectionChanged.emit(QItemSelection(), QItemSelection())
