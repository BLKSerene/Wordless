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

import os
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_checking import wordless_checking_file, wordless_checking_misc
from wordless_widgets import wordless_message_box
from wordless_utils import wordless_conversion, wordless_detection

class Wordless_List(QListWidget):
    def __init__(self, main):
        super().__init__(main)

        self.main = main

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

    def selection_changed(self):
        if self.selectedIndexes():
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def _new_item(self):
        pass

    def add_item(self, text = None):
        new_item = self._new_item()

        self.addItem(new_item)

        if text:
            self.item(self.count() - 1).setText(text)
        else:
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
        self.selection_changed()

    def import_list(self):
        pass

    def export_list(self):
        pass

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
                            wordless_message_box.wordless_message_box_duplicate_search_terms(self.main)

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
        files = []

        if os.path.exists(self.main.settings_custom['import']['search_terms']['default_path']):
            default_dir = self.main.settings_custom['import']['search_terms']['default_path']
        else:
            default_dir = self.main.settings_default['import']['search_terms']['default_path']

        file_paths = QFileDialog.getOpenFileNames(self.main,
                                                  self.tr('Import from File(s)'),
                                                  default_dir,
                                                  self.tr('Text File (*.txt)'))[0]

        if file_paths:
            self.main.settings_custom['import']['search_terms']['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            file_paths, files_empty = wordless_checking_file.check_files_empty(self.main, file_paths)

            if self.main.settings_custom['import']['search_terms']['detect_encodings']:
                for file_path in file_paths:
                    files.append({
                                     'path': os.path.normpath(file_path),
                                     'encoding_code': wordless_detection.detect_encoding(self.main, file_path)[0]
                                 })
            else:
                for file_path in file_paths:
                    files.append({
                                     'path': os.path.normpath(file_path),
                                     'encoding_code': self.main.settings_custom['auto_detection']['default_settings']['default_encoding']
                                 })

            encoding_codes = [file['encoding_code'] for file in files]

            file_paths, files_encoding_error = wordless_checking_file.check_files_loading_error(self.main, file_paths, encoding_codes)

            for file in files:
                if file['path'] in file_paths:
                    with open(file['path'], 'r', encoding = file['encoding_code']) as f:
                        for line in f:
                            if line.rstrip():
                                self.addItem(line.strip())

                        self.itemChanged.emit(self.item(0))

            wordless_message_box.wordless_message_box_error_files(self.main,
                                                                  files_empty = files_empty,
                                                                  files_encoding_error = files_encoding_error)

    def export_list(self):
        default_dir = self.main.settings_custom['export']['search_terms']['default_path']

        file_path = QFileDialog.getSaveFileName(self.main,
                                                self.tr('Export to File'),
                                                wordless_checking_misc.check_dir(default_dir),
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            encoding = self.main.settings_custom['export']['search_terms']['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.get_items():
                    f.write(item + '\n')

            wordless_message_box.wordless_message_box_export_search_terms(self.main, file_path)

            self.main.settings_custom['export']['search_terms']['default_path'] = os.path.normpath(os.path.dirname(file_path))

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
                            wordless_message_box.wordless_message_box_duplicate_stop_words(self.main)

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
        files = []

        if os.path.exists(self.main.settings_custom['import']['stop_words']['default_path']):
            default_dir = self.main.settings_custom['import']['stop_words']['default_path']
        else:
            default_dir = self.main.settings_default['import']['stop_words']['default_path']

        file_paths = QFileDialog.getOpenFileNames(self.main,
                                                  self.tr('Import from File(s)'),
                                                  default_dir,
                                                  self.tr('Text File (*.txt)'))[0]

        if file_paths:
            self.main.settings_custom['import']['stop_words']['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            file_paths, files_empty = wordless_checking_file.check_files_empty(self.main, file_paths)

            if self.main.settings_custom['import']['stop_words']['detect_encodings']:
                for file_path in file_paths:
                    files.append({
                                     'path': os.path.normpath(file_path),
                                     'encoding_code': wordless_detection.detect_encoding(self.main, file_path)[0]
                                 })
            else:
                for file_path in file_paths:
                    files.append({
                                     'path': os.path.normpath(file_path),
                                     'encoding_code': self.main.settings_custom['auto_detection']['default_settings']['default_encoding']
                                 })

            encoding_codes = [file['encoding_code'] for file in files]

            file_paths, files_encoding_error = wordless_checking_file.check_files_loading_error(self.main, file_paths, encoding_codes)

            for file in files:
                if file['path'] in file_paths:
                    with open(file['path'], 'r', encoding = file['encoding_code']) as f:
                        for line in f:
                            if line.strip():
                                self.addItem(line.strip())

                        self.itemChanged.emit(self.item(0))

            wordless_message_box.wordless_message_box_error_files(self.main,
                                                                  files_empty = files_empty,
                                                                  files_encoding_error = files_encoding_error)

    def export_list(self):
        default_dir = self.main.settings_custom['export']['stop_words']['default_path']

        file_path = QFileDialog.getSaveFileName(self.main,
                                                self.tr('Export to File'),
                                                wordless_checking_misc.check_dir(default_dir),
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            encoding = self.main.settings_custom['export']['stop_words']['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.get_items():
                    f.write(item + '\n')

            wordless_message_box.wordless_message_box_export_stop_words(self.main, file_path)

            self.main.settings_custom['export']['stop_words']['default_path'] = os.path.normpath(os.path.dirname(file_path))

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
