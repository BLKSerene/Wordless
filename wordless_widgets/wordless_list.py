#
# Wordless: Lists
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import wordless_message_box
from wordless_utils import wordless_checking, wordless_conversion, wordless_detection

class Wordless_List(QListWidget):
    def __init__(self, main):
        super().__init__(main)

        self.main = main

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.itemChanged.connect(self.item_changed, Qt.QueuedConnection)
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

    def item_changed(self, item = None):
        if self.count():
            self.button_clear.setEnabled(True)
            self.button_export.setEnabled(True)
        else:
            self.button_clear.setEnabled(False)
            self.button_export.setEnabled(False)

        if item:
            if re.search(r'^\s*$', item.text()):
                QMessageBox.warning(self.main,
                                    self.tr('Empty Search Term'),
                                    self.tr('Empty search term is not allowed!'),
                                    QMessageBox.Ok)

                item.setText(item.old_text)
                self.editItem(item)
            else:
                for i in range(self.count()):
                    if self.item(i) != item:
                        if item.text() == self.item(i).text():
                            self.blockSignals(True)

                            item.setForeground(QColor('#F00'))
                            self.item(i).setForeground(QColor('#F00'))

                            self.blockSignals(False)
                            
                            QMessageBox.warning(self.main,
                                                self.tr('Duplicate Search Terms'),
                                                self.tr('Please refrain from searching the same item more than once!'),
                                                QMessageBox.Ok)

                            item.setText(item.old_text)
                            self.editItem(item)

                            item.setForeground(QColor('#292929'))
                            self.item(i).setForeground(QColor('#292929'))

                            break

                item.old_text = item.text()

    def selection_changed(self):
        if self.selectedIndexes():
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def _new_item(self):
        i = 1

        while True:
            if self.findItems(self.tr(f'New Item ({i})'), Qt.MatchExactly):
                i += 1
            else:
                new_item = QListWidgetItem(self.tr('New Item ({})').format(i))

                new_item.old_text = new_item.text()
                new_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled)

                return new_item

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
        files_encoding_error = []

        if os.path.exists(self.main.settings_custom['import']['search_terms']['default_path']):
            default_dir = self.main.settings_custom['import']['search_terms']['default_path']
        else:
            default_dir = self.main.settings_default['import']['search_terms']['default_path']

        file_paths = QFileDialog.getOpenFileNames(self.main,
                                                  self.tr('Import Search Terms from File(s)'),
                                                  default_dir,
                                                  self.tr('Text File (*.txt)'))[0]

        if file_paths:
            self.main.settings_custom['import']['search_terms']['default_path'] = os.path.normpath(os.path.dirname(file_paths[0]))

            file_paths, files_empty = wordless_checking.check_files_empty(self.main, file_paths)

            for file_path in file_paths:
                file_path = os.path.normpath(file_path)

                # Detect encoding
                if self.main.settings_custom['import']['search_terms']['detect_encodings']:
                    encoding_code, _ = wordless_detection.detect_encoding(self.main, file_path)
                else:
                    encoding_code = self.main.settings_custom['encoding_detection']['default_settings']['default_encoding']

                try:
                    with open(file_path, 'r', encoding = encoding_code) as f:
                        for line in f:
                            if line.strip():
                                self.addItem(line.strip())

                        self.itemChanged.emit(self.item(0))
                except:
                    files_encoding_error.append(file_path)

            wordless_message_box.wordless_message_box_error_open_files(self.main,
                                                                       files_empty = files_empty,
                                                                       files_encoding_error = files_encoding_error)

    def export_list(self):
        default_dir = self.main.settings_custom['export']['search_terms']['default_path']

        file_path = QFileDialog.getSaveFileName(self.main,
                                                self.tr('Export Search Terms to File'),
                                                wordless_checking.check_dir(default_dir),
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            encoding = self.main.settings_custom['export']['search_terms']['default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.get_items():
                    f.write(item + '\n')

            wordless_message_box.wordless_message_box_export_completed_search_terms(self.main, file_path)

            self.main.settings_custom['export']['search_terms']['default_path'] = os.path.normpath(os.path.dirname(file_path))

    def get_items(self):
        return [self.item(i).text() for i in range(self.count())]
