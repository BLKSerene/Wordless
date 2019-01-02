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
from wordless_utils import wordless_conversion

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
        file_path = QFileDialog.getOpenFileName(self.main,
                                                self.tr('Import Search Terms from File'),
                                                self.main.settings_custom['import']['search_terms_default_path'],
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            encoding_code = self.main.settings_custom['import']['search_terms_default_encoding']
            encoding_text = wordless_conversion.to_encoding_text(self.main, encoding_code)

            try:
                with open(file_path, 'r', encoding = encoding_code) as f:
                    if os.path.getsize(file_path) == 0:
                        wordless_message_box.wordless_message_box_empty_file(self.main, file_path)
                    else:
                        for line in f:
                            if line.strip():
                                self.addItem(line.strip())

                        self.itemChanged.emit(self.item(0))
            except:
                QMessageBox.warning(self.main,
                                    self.tr('Import Failed'),
                                    self.tr(f'''{self.main.settings_global['styles']['style_dialog']}
                                                <body>
                                                    <p>Failed to open the specified file with encoding "{encoding_text}".</p>
                                                    <p>You can change the default file encoding in "Preferences -> Settings -> General -> Import" and try again.</p>
                                                </body>
                                            '''))

            self.main.settings_custom['import']['search_terms_default_path'] = os.path.split(file_path)[0]

    def export_list(self):
        file_path = QFileDialog.getSaveFileName(self.main,
                                                self.tr('Export Search Terms to File'),
                                                self.main.settings_custom['export']['search_terms_default_path'],
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            encoding = self.main.settings_custom['export']['search_terms_default_encoding']

            with open(file_path, 'w', encoding = encoding) as f:
                for item in self.get_items():
                    f.write(item + '\n')

            wordless_message_box.wordless_message_box_export_completed_search_terms(self.main, file_path)

    def get_items(self):
        return [self.item(i).text() for i in range(self.count())]
