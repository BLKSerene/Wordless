#
# Wordless: Widgets - List
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import collections
import os
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_checking import wl_checking_file, wl_checking_misc
from wl_dialogs import wl_dialog_error, wl_msg_box
from wl_widgets import wl_box, wl_msg
from wl_utils import wl_detection, wl_misc

class Wl_List(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)
        self.button_import = QPushButton(self.tr('Import'), self)
        self.button_export = QPushButton(self.tr('Export'), self)

        self.button_add.clicked.connect(self.add_item)
        self.button_insert.clicked.connect(self.insert_item)
        self.button_remove.clicked.connect(self.remove_item)
        self.button_clear.clicked.connect(self.clear_list)
        self.button_import.clicked.connect(self.import_list)
        self.button_export.clicked.connect(self.export_list)

        self.clear_list()

    def item_changed(self):
        if self.count():
            self.button_clear.setEnabled(True)
            self.button_export.setEnabled(True)
        else:
            self.button_clear.setEnabled(False)
            self.button_export.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes():
            self.button_insert.setEnabled(True)
            self.button_remove.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)
            self.button_remove.setEnabled(False)

    def _new_item(self):
        pass

    def add_item(self):
        new_item = self._new_item()

        self.addItem(new_item)
        self.editItem(new_item)
        
        self.item(self.count() - 1).setSelected(True)

        self.itemChanged.emit(self.item(0))

    def insert_item(self):
        new_item = self._new_item()
        selected_row_1st = self.selectedIndexes()[0].row()

        self.insertItem(selected_row_1st, new_item)
        self.editItem(new_item)

        self.item(selected_row_1st).setSelected(True)

        self.itemChanged.emit(self.item(0))

    def remove_item(self):
        for index in sorted(self.selectedIndexes(), reverse = True):
            self.takeItem(index.row())

        self.itemChanged.emit(self.item(0))

    def clear_list(self):
        self.clear()

        self.itemChanged.emit(self.item(0))

    def import_list(self, settings):
        files = []

        if os.path.exists(self.main.settings_custom['import'][settings]['default_path']):
            default_dir = self.main.settings_custom['import'][settings]['default_path']
        else:
            default_dir = self.main.settings_default['import'][settings]['default_path']

        file_paths = QFileDialog.getOpenFileNames(
            self.main,
            self.tr('Import from Files'),
            default_dir,
            self.tr('Text File (*.txt)')
        )[0]

        if file_paths:
            self.main.settings_custom['import'][settings]['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            # Detect encodings
            if self.main.settings_custom['import'][settings]['detect_encodings']:
                for file_path in file_paths:
                    files.append({
                        'path': wl_misc.get_normalized_path(file_path),
                        'encoding': wl_detection.detect_encoding(self.main, file_path)
                    })
            else:
                for file_path in file_paths:
                    files.append({
                        'path': wl_misc.get_normalized_path(file_path),
                        'encoding': self.main.settings_custom['files']['default_settings']['encoding']
                    })

            files_pass, files_empty = wl_checking_file.check_files_empty(self.main, files)
            files_pass, files_parsing_error = wl_checking_file.check_files_parsing_error(self.main, files_pass)

            if files_empty or files_parsing_error:
                wl_dialog_error.wl_dialog_error_import(
                    self.main,
                    files_empty = files_empty,
                    files_parsing_error = files_parsing_error
                )

                wl_msg.wl_msg_import_list_error(self.main)
            else:
                # Check duplicate items
                items_to_import = []
                items_cur = self.get_items()

                num_prev = len(items_cur)

                for file in files_pass:
                    with open(file['path'], 'r', encoding = file['encoding']) as f:
                        for line in f:
                            line = line.strip()

                            if line not in items_cur:
                                items_to_import.append(line)

                self.load_items(collections.OrderedDict.fromkeys(items_to_import))
                self.itemChanged.emit(self.item(0))

                wl_msg.wl_msg_import_list_success(self.main, num_prev, len(self.get_items()))

    def export_list(self, settings, default_file_name):
        default_dir = self.main.settings_custom['export'][settings]['default_path']

        file_path = QFileDialog.getSaveFileName(
            self.main,
            self.tr('Export to File'),
            os.path.join(wl_checking_misc.check_dir(default_dir), default_file_name),
            self.tr('Text File (*.txt)')
        )[0]

        if file_path:
            encoding = self.main.settings_custom['export'][settings]['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.get_items():
                    f.write(item + '\n')

            wl_msg_box.wl_msg_box_export_list(self.main, file_path)

            self.main.settings_custom['export'][settings]['default_path'] = os.path.normpath(os.path.dirname(file_path))

    def load_items(self, texts):
        for text in texts:
            new_item = self._new_item()
            new_item.setText(text)

            self.addItem(new_item)

        self.itemChanged.emit(self.item(0))

    def get_items(self):
        return [self.item(i).text() for i in range(self.count())]

class Wl_List_Files(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wl_misc.find_wl_main(parent)

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)

        self.button_add.clicked.connect(self.add_item)
        self.button_insert.clicked.connect(self.insert_item)
        self.button_remove.clicked.connect(self.remove_item)
        self.button_clear.clicked.connect(self.clear_list)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.main.wl_files.table.itemChanged.connect(self.wl_files_changed)

        self.clear_list()

    def item_changed(self):
        if self.count():
            self.button_clear.setEnabled(True)
        else:
            self.button_clear.setEnabled(False)

        self.selection_changed()

    def selection_changed(self):
        if self.selectedIndexes():
            self.button_insert.setEnabled(True)
            self.button_remove.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)
            self.button_remove.setEnabled(False)

        self.wl_files_changed()

    def file_changed(self, combo_box_file):
        for i in range(self.count()):
            combo_box_cur = self.itemWidget(self.item(i))

            if combo_box_file != combo_box_cur and combo_box_file.currentText() == combo_box_cur.currentText():
                QMessageBox.warning(
                    self.main,
                    self.tr('Duplicate Reference Files'),
                    self.tr(f'''
                        {self.main.settings_global['styles']['style_dialog']}
                        <body>
                            <div>Please refrain from specifying two identical reference files!</div>
                        </body>
                    '''),
                    QMessageBox.Ok
                )

                combo_box_file.setCurrentText(combo_box_file.text_old)
                combo_box_file.showPopup()

                return

        combo_box_file.text_old = combo_box_file.currentText()

    def wl_files_changed(self):
        if self.count() >= len(self.main.wl_files.get_selected_files()):
            self.button_add.setEnabled(False)
            self.button_insert.setEnabled(False)
        else:
            self.button_add.setEnabled(True)
            if self.selectedIndexes():
                self.button_insert.setEnabled(True)

    def wl_file_removed(self, combo_box_file):
        for i in reversed(range(self.count())):
            if self.itemWidget(self.item(i)) == combo_box_file:
                self.takeItem(i)

                self.itemChanged.emit(self.item(0))

    def _new_item(self):
        new_item = QListWidgetItem()
        new_item_file = wl_box.Wl_Combo_Box_File_Ref(self.main, self)

        new_item.setFlags(Qt.ItemIsSelectable |
                          Qt.ItemIsEditable |
                          Qt.ItemIsDragEnabled |
                          Qt.ItemIsEnabled)

        file_names = self.get_file_names()

        for i in range(new_item_file.count()):
            if new_item_file.itemText(i) not in file_names:
                new_item_file.setCurrentIndex(i)

                break

        new_item_file.text_old = new_item_file.currentText()

        return new_item, new_item_file

    def add_item(self):
        new_item, new_item_file = self._new_item()

        self.addItem(new_item)
        self.setItemWidget(new_item, new_item_file)

        self.item(self.count() - 1).setSelected(True)

        self.itemChanged.emit(self.item(0))

    def insert_item(self):
        new_item, new_item_file = self._new_item()

        selected_row_1st = self.selectedIndexes()[0].row()

        self.insertItem(selected_row_1st, new_item)
        self.setItemWidget(new_item, new_item_file)

        self.item(selected_row_1st).setSelected(True)

        self.itemChanged.emit(self.item(0))

    def remove_item(self):
        for index in sorted(self.selectedIndexes(), reverse = True):
            self.takeItem(index.row())

        self.itemChanged.emit(self.item(0))

    def clear_list(self):
        self.clear()

        self.itemChanged.emit(self.item(0))

    def load_items(self, texts):
        for text in texts:
            new_item, new_item_file = self._new_item()

            new_item_file.setCurrentText(text)

            self.addItem(new_item)
            self.setItemWidget(new_item, new_item_file)

            new_item.text_old = new_item_file.currentText()

        self.itemChanged.emit(self.item(0))

    def get_file_names(self):
        return [self.itemWidget(self.item(i)).currentText() for i in range(self.count())]

class Wl_List_Search_Terms(Wl_List):
    def item_changed(self, item = None):
        super().item_changed()

        if item:
            if re.search(r'^\s*$', item.text()):
                item.setText(item.text_old)
            else:
                for i in range(self.count()):
                    if self.item(i) != item:
                        if item.text() == self.item(i).text():
                            wl_msg_box.wl_msg_box_duplicate_search_terms(self.main)

                            item.setText(item.text_old)

                            self.closePersistentEditor(item)
                            self.editItem(item)

                            break

                item.text_old = item.text()

    def _new_item(self):
        i = 1

        while True:
            if self.findItems(self.tr(f'New Search Term ({i})'), Qt.MatchExactly):
                i += 1
            else:
                new_item = QListWidgetItem(self.tr('New Search Term ({})').format(i))

                new_item.text_old = new_item.text()
                new_item.setFlags(Qt.ItemIsSelectable |
                                  Qt.ItemIsEditable |
                                  Qt.ItemIsDragEnabled |
                                  Qt.ItemIsEnabled)

                return new_item

    def import_list(self):
        super().import_list(settings = 'search_terms')

    def export_list(self):
        super().export_list(settings = 'search_terms', default_file_name = 'Wordless_search_terms.txt')

class Wl_List_Stop_Words(Wl_List):
    def item_changed(self, item = None):
        super().item_changed()

        if item:
            if re.search(r'^\s*$', item.text()):
                item.setText(item.text_old)
            else:
                for i in range(self.count()):
                    if self.item(i) != item:
                        if item.text() == self.item(i).text():
                            wl_msg_box.wl_msg_box_duplicate_stop_words(self.main)

                            item.setText(item.text_old)

                            self.closePersistentEditor(item)
                            self.editItem(item)

                            break

                item.text_old = item.text()

    def item_changed_default(self):
        self.button_clear.setEnabled(False)
        self.button_export.setEnabled(True)

    def selection_changed_default(self):
        self.button_insert.setEnabled(False)
        self.button_remove.setEnabled(False)

    def _new_item(self):
        i = 1

        while True:
            if self.findItems(self.tr(f'New Stop Word ({i})'), Qt.MatchExactly):
                i += 1
            else:
                new_item = QListWidgetItem(self.tr('New Stop Word ({})').format(i))

                new_item.text_old = new_item.text()
                new_item.setFlags(Qt.ItemIsSelectable |
                                  Qt.ItemIsEditable |
                                  Qt.ItemIsDragEnabled |
                                  Qt.ItemIsEnabled)

                return new_item

    def import_list(self):
        super().import_list(settings = 'stop_words')

    def export_list(self):
        super().export_list(settings = 'stop_words', default_file_name = 'Wordless_stop_words.txt')

    def load_stop_words(self, stop_words):
        self.clear_list()

        self.addItems(sorted(stop_words))

        self.scrollToTop()

    def switch_to_custom(self):
        self.setDragEnabled(True)

        for i in range(self.count()):
            self.item(0).setFlags(Qt.ItemIsSelectable |
                                  Qt.ItemIsEditable |
                                  Qt.ItemIsDragEnabled |
                                  Qt.ItemIsEnabled)

        self.button_add.setEnabled(True)
        self.button_import.setEnabled(True)

        self.itemChanged.disconnect()
        self.itemSelectionChanged.disconnect()

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.item_changed()
        self.selection_changed()

    def switch_to_default(self):
        self.setDragEnabled(False)

        self.button_add.setEnabled(False)
        self.button_import.setEnabled(False)

        self.itemChanged.disconnect()
        self.itemSelectionChanged.disconnect()

        self.itemChanged.connect(self.item_changed)
        self.itemChanged.connect(self.item_changed_default)
        self.itemSelectionChanged.connect(self.selection_changed)
        self.itemSelectionChanged.connect(self.selection_changed_default)

        self.item_changed_default()
        self.selection_changed_default()
