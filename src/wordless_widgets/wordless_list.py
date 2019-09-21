#
# Wordless: Widgets - List
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
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

from wordless_checking import wordless_checking_file, wordless_checking_misc
from wordless_dialogs import wordless_dialog_error, wordless_msg_box
from wordless_widgets import wordless_msg
from wordless_utils import wordless_detection, wordless_misc

class Wordless_List(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main = wordless_misc.find_wordless_main(parent)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.itemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.button_add = QPushButton(self.tr('Add'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear = QPushButton(self.tr('Clear'), self)
        self.button_import = QPushButton(self.tr('Import'), self)
        self.button_export = QPushButton(self.tr('Export'), self)

        self.button_add.clicked.connect(self.add_item)
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
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def _new_item(self):
        pass

    def add_item(self):
        new_item = self._new_item()

        self.addItem(new_item)
        self.editItem(new_item)
            
        self.item(self.count() - 1).setSelected(True)

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

        file_paths = QFileDialog.getOpenFileNames(self.main,
                                                  self.tr('Import from File(s)'),
                                                  default_dir,
                                                  self.tr('Text File (*.txt)'))[0]

        if file_paths:
            self.main.settings_custom['import'][settings]['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            # Detect encodings
            if self.main.settings_custom['import'][settings]['detect_encodings']:
                for file_path in file_paths:
                    files.append({
                        'path': wordless_misc.get_abs_path(file_path),
                        'encoding': wordless_detection.detect_encoding(self.main, file_path)[0]
                    })
            else:
                for file_path in file_paths:
                    files.append({
                        'path': wordless_misc.get_abs_path(file_path),
                        'encoding': self.main.settings_custom['auto_detection']['default_settings']['default_encoding']
                    })

            files_ok, files_empty = wordless_checking_file.check_files_empty(self.main, files)
            files_ok, files_decoding_error = wordless_checking_file.check_files_decoding_error(self.main, files_ok)

            # Extract file paths
            files_empty = [file['path'] for file in files_empty]
            files_decoding_error = [file['path'] for file in files_decoding_error]

            if files_empty or files_decoding_error:
                wordless_dialog_error.wordless_dialog_error_import(self.main,
                                                                   files_empty = files_empty,
                                                                   files_decoding_error = files_decoding_error)

                wordless_msg.wordless_msg_import_list_error(self.main)
            else:
                # Check duplicate items
                items_to_import = []
                items_cur = self.get_items()

                num_prev = len(items_cur)

                for file in files_ok:
                    with open(file['path'], 'r', encoding = file['encoding']) as f:
                        for line in f:
                            line = line.strip()

                            if line not in items_cur:
                                items_to_import.append(line)

                self.load_items(collections.OrderedDict.fromkeys(items_to_import))
                self.itemChanged.emit(self.item(0))

                wordless_msg.wordless_msg_import_list_success(self.main, num_prev, len(self.get_items()))

    def export_list(self, settings):
        default_dir = self.main.settings_custom['export'][settings]['default_path']

        file_path = QFileDialog.getSaveFileName(self.main,
                                                self.tr('Export to File'),
                                                wordless_checking_misc.check_dir(default_dir),
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            encoding = self.main.settings_custom['export'][settings]['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.get_items():
                    f.write(item + '\n')

            wordless_msg_box.wordless_msg_box_export_list(self.main, file_path)

            self.main.settings_custom['export'][settings]['default_path'] = os.path.normpath(os.path.dirname(file_path))

    def load_items(self, texts):
        for text in texts:
            new_item = self._new_item()
            new_item.setText(text)

            self.addItem(new_item)

        self.itemChanged.emit(self.item(0))

    def get_items(self):
        return [self.item(i).text() for i in range(self.count())]

class Wordless_List_Search_Terms(Wordless_List):
    def item_changed(self, item = None):
        super().item_changed()

        if item:
            if re.search(r'^\s*$', item.text()):
                item.setText(item.old_text)
            else:
                for i in range(self.count()):
                    if self.item(i) != item:
                        if item.text() == self.item(i).text():
                            wordless_msg_box.wordless_msg_box_duplicate_search_terms(self.main)

                            item.setText(item.old_text)

                            self.closePersistentEditor(item)
                            self.editItem(item)

                            break

                item.old_text = item.text()

    def _new_item(self):
        i = 1

        while True:
            if self.findItems(self.tr(f'New Search Term ({i})'), Qt.MatchExactly):
                i += 1
            else:
                new_item = QListWidgetItem(self.tr('New Search Term ({})').format(i))

                new_item.old_text = new_item.text()
                new_item.setFlags(Qt.ItemIsSelectable |
                                  Qt.ItemIsEditable |
                                  Qt.ItemIsDragEnabled |
                                  Qt.ItemIsEnabled)

                return new_item

    def import_list(self):
        super().import_list(settings = 'search_terms')

    def export_list(self):
        super().export_list(settings = 'search_terms')

class Wordless_List_Stop_Words(Wordless_List):
    def item_changed(self, item = None):
        super().item_changed()

        if item:
            if re.search(r'^\s*$', item.text()):
                item.setText(item.old_text)
            else:
                for i in range(self.count()):
                    if self.item(i) != item:
                        if item.text() == self.item(i).text():
                            wordless_msg_box.wordless_msg_box_duplicate_stop_words(self.main)

                            item.setText(item.old_text)

                            self.closePersistentEditor(item)
                            self.editItem(item)

                            break

                item.old_text = item.text()

    def item_changed_default(self):
        self.button_clear.setEnabled(False)
        self.button_export.setEnabled(True)

    def selection_changed_default(self):
        self.button_remove.setEnabled(False)

    def _new_item(self):
        i = 1

        while True:
            if self.findItems(self.tr(f'New Stop Word ({i})'), Qt.MatchExactly):
                i += 1
            else:
                new_item = QListWidgetItem(self.tr('New Stop Word ({})').format(i))

                new_item.old_text = new_item.text()
                new_item.setFlags(Qt.ItemIsSelectable |
                                  Qt.ItemIsEditable |
                                  Qt.ItemIsDragEnabled |
                                  Qt.ItemIsEnabled)

                return new_item

    def import_list(self):
        super().import_list(settings = 'stop_words')

    def export_list(self):
        super().export_list(settings = 'stop_words')

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
