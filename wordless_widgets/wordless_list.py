#
# Wordless: List
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Wordless_List(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.itemChanged.connect(self.item_changed, Qt.QueuedConnection)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.button_add    = QPushButton(self.tr('Add'), self)
        self.button_insert = QPushButton(self.tr('Insert'), self)
        self.button_remove = QPushButton(self.tr('Remove'), self)
        self.button_clear  = QPushButton(self.tr('Clear'), self)
        self.button_import = QPushButton(self.tr('Import'), self)
        self.button_export = QPushButton(self.tr('Export'), self)

        self.button_add.clicked.connect(self.add_item)
        self.button_insert.clicked.connect(self.insert_item)
        self.button_remove.clicked.connect(self.remove_item)
        self.button_clear.clicked.connect(self.clear_list)
        self.button_import.clicked.connect(self.import_list)
        self.button_export.clicked.connect(self.export_list)

        self.item_changed()
        self.selection_changed()

    def item_changed(self, item = None):
        if self.count():
            self.button_clear.setEnabled(True)
            self.button_export.setEnabled(True)
        else:
            self.button_clear.setEnabled(False)
            self.button_export.setEnabled(False)

        if item:
            if re.search(r'^\s*$', item.text()):
                QMessageBox.warning(self.parent,
                                    self.tr('Empty Search Term'),
                                    self.tr('Please enter your search term!'),
                                    QMessageBox.Ok)

                self.editItem(item)
                item.setText(item.old_text)
            else:
                for i in range(self.count()):
                    if i != self.row(item):
                        if item.text() == self.item(i).text():
                            item.setForeground(QColor('#F00'))
                            self.item(i).setForeground(QColor('#F00'))
                            
                            QMessageBox.warning(self.parent,
                                                self.tr('Duplicate Search Terms'),
                                                self.tr('Please refrain from searching the same item more than once!'),
                                                QMessageBox.Ok)

                            self.editItem(item)
                            item.setText(item.old_text)

                            break

                    item.old_text = item.text()

    def selection_changed(self):
        if self.selectedIndexes():
            self.button_insert.setEnabled(True)
            self.button_remove.setEnabled(True)
        else:
            self.button_insert.setEnabled(False)
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

        self.item_changed()

    def insert_item(self):
        i = self.selectedIndexes()[0].row()
        new_item = self._new_item()

        self.insertItem(i, new_item)
        self.editItem(new_item)
        self.item(i).setSelected(True)

        self.item_changed()

    def remove_item(self):
        for index in sorted(self.selectedIndexes(), reverse = True):
            self.takeItem(index.row())

        self.item_changed()

    def clear_list(self):
        self.clear()

        self.item_changed()

    def import_list(self):
        file_path = QFileDialog.getOpenFileName(self.parent,
                                                self.tr('Import word list from file'),
                                                '.',
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            with open(file_path, 'r', encoding = 'UTF-8') as f:
                for line in f:
                    self.addItem(line.rstrip())

            self.item_changed()

    def export_list(self):
        file_path = QFileDialog.getSaveFileName(self.parent,
                                                self.tr('Export word list to file'),
                                                '.',
                                                self.tr('Text File (*.txt)'))[0]

        if file_path:
            with open(file_path, 'w', encoding = 'UTF-8') as f:
                for item in self.get_items():
                    f.write(item + '\n')

    def get_items(self):
        return list(set([self.item(i).text() for i in range(self.count())]))
