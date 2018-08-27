#
# Wordless: Files
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#


import csv
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import chardet
import langdetect

from wordless_utils import *

class Wordless_File:
    def __init__(self, parent, table, file_path, auto_detect = True):
        self.parent = parent
        self.table = table

        if auto_detect:
            self.selected = True
            self.path = os.path.normpath(file_path)

            path_name, file = os.path.split(file_path)
            self.name, self.ext = os.path.splitext(file)
            self.ext_text = wordless_misc.convert_ext(self.parent, self.ext)

            with open(self.path, 'rb') as f:
                encoding_detected = chardet.detect(f.read())

                encoding_code = encoding_detected['encoding']
                encoding_lang = encoding_detected.get('language')
                # chardet
                if encoding_code == None:
                    self.encoding_code = 'UTF-8'
                elif encoding_code == 'EUC-TW':
                    self.encoding_code = 'Big5'
                elif encoding_code == 'ISO-2022-CN':
                    self.encoding_code = 'GB2312'
                else:
                    self.encoding_code = encoding_code.lower().replace('-', '_')
                self.encoding_text = wordless_misc.convert_encoding(self.parent, self.encoding_code, encoding_lang)
                print (self.encoding_code, self.encoding_text)

            try:
                with open(self.path, 'r', encoding = self.encoding_code) as f:
                    self.lang_code = langdetect.detect(f.read())
            except UnicodeDecodeError:
                self.lang_code = 'en'
                QMessageBox.warning(self.parent,
                                    'Auto-detection Failure',
                                    'Failed to auto-detect language and encoding for the file "{}", please choose the right language and encoding manually!'.format(self.name),
                                    QMessageBox.Ok)
            finally:
                self.lang_text = wordless_misc.convert_lang(self.parent, self.lang_code)

            if self.lang_code in ['ja', 'ko', 'zh-cn', 'zh-tw']:
                self.delimiter = ''
            else:
                self.delimiter = ' '

    def write(self, row):
        if row > self.table.rowCount() - 1:
            self.table.setRowCount(self.table.rowCount() + 1)

        checkbox_name = QTableWidgetItem(self.name)
        combo_box_lang = wordless_widgets.Wordless_Combo_Box_Lang(self.parent)
        combo_box_encoding = wordless_widgets.Wordless_Combo_Box_Encoding(self.parent)

        if self.selected:
            checkbox_name.setCheckState(Qt.Checked)
        else:
            checkbox_name.setCheckState(Qt.Unchecked)
        combo_box_lang.setCurrentText(self.lang_text)
        combo_box_encoding.setCurrentText(self.encoding_text)

        combo_box_lang.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(row, 2)))
        combo_box_encoding.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(row, 3)))
        
        self.table.setItem(row, 0, checkbox_name)
        self.table.setCellWidget(row, 1, combo_box_lang)
        self.table.setItem(row, 2, QTableWidgetItem(self.path))
        self.table.setItem(row, 3, QTableWidgetItem(self.ext_text))
        self.table.setCellWidget(row, 4, combo_box_encoding)


class Wordless_Table_Files(wordless_table.Wordless_Table):
    def __init__(self, parent, headers, stretch_columns = []):
        super().__init__(parent, headers, stretch_columns = stretch_columns)

        self.itemClicked.connect(self.item_changed)

        self.button_move_up = QPushButton(self.tr('Move Up'))
        self.button_move_down = QPushButton(self.tr('Move Down'))
        self.button_move_to_top = QPushButton(self.tr('Move To Top'))
        self.button_move_to_bottom = QPushButton(self.tr('Move To Bottom'))

        self.button_move_up.clicked.connect(self.move_up)
        self.button_move_down.clicked.connect(self.move_down)
        self.button_move_to_top.clicked.connect(self.move_to_top)
        self.button_move_to_bottom.clicked.connect(self.move_to_bottom)

        style_btn = 'QPushButton {padding: 4px 8px; text-align: left}'

        self.button_move_up.setStyleSheet(style_btn)
        self.button_move_down.setStyleSheet(style_btn)
        self.button_move_to_top.setStyleSheet(style_btn)
        self.button_move_to_bottom.setStyleSheet(style_btn)

        self.button_open_file = QPushButton(self.tr('Add File...'))
        self.button_open_files = QPushButton(self.tr('Add Files...'))
        self.button_open_dir = QPushButton(self.tr('Add Folder...'))
        self.button_close_selected = QPushButton(self.tr('Close Selected File(s)'))
        self.button_close_all = QPushButton(self.tr('Close All Files'))
        self.button_reopen = QPushButton(self.tr('Reopen Closed File(s)'))

        self.button_select_all = QPushButton(self.tr('Select All'))
        self.button_inverse = QPushButton(self.tr('Inverse'))
        self.button_deselect_all = QPushButton(self.tr('Deselect All'))
        self.button_import_list = QPushButton(self.tr('Import List...'))

        self.button_clear.hide()

        self.button_open_file.clicked.connect(self.open_file)
        self.button_open_files.clicked.connect(self.open_files)
        self.button_open_dir.clicked.connect(self.open_dir)
        self.button_close_selected.clicked.connect(self.close_selected)
        self.button_close_all.clicked.connect(self.close_all)
        self.button_reopen.clicked.connect(self.reopen)

        self.button_select_all.clicked.connect(self.select_all)
        self.button_inverse.clicked.connect(self.inverse)
        self.button_deselect_all.clicked.connect(self.deselect_all)
        self.button_import_list.clicked.connect(self.import_list)

        self.parent.__class__.open_file = self.open_file
        self.parent.__class__.open_files = self.open_files
        self.parent.__class__.open_dir = self.open_dir
        self.parent.__class__.close_selected = self.close_selected
        self.parent.__class__.close_all = self.close_all
        self.parent.__class__.reopen = self.reopen

        self.auto_restore()

    def item_changed(self):
        for row in range(self.rowCount()):
            if self.cellWidget(row, 4):
                file = self.parent.files[row]

                file.selected = True if self.item(row, 0).checkState() == Qt.Checked else False
                file.lang_text = self.cellWidget(row, 1).currentText()
                file.lang_code = wordless_misc.convert_lang(self.parent, file.lang_text)
                file.encoding_text = self.cellWidget(row, 4).currentText()
                file.encoding_code = wordless_misc.convert_encoding(self.parent, file.encoding_text)[0]

        if self.item(0, 0):
            self.button_select_all.setEnabled(True)
            self.button_inverse.setEnabled(True)
            self.button_deselect_all.setEnabled(True)
            self.button_close_all.setEnabled(True)
            self.button_export_all.setEnabled(True)
        else:
            self.button_select_all.setEnabled(False)
            self.button_inverse.setEnabled(False)
            self.button_deselect_all.setEnabled(False)
            self.button_close_all.setEnabled(False)
            self.button_export_all.setEnabled(False)

        if self.parent.files_closed:
            self.button_reopen.setEnabled(True)
        else:
            self.button_reopen.setEnabled(False)

        self.selection_changed()
        self.auto_save()

    def selection_changed(self):
        if self.selectedIndexes() and self.item(0, 0):
            self.button_move_up.setEnabled(True)
            self.button_move_down.setEnabled(True)
            self.button_move_to_top.setEnabled(True)
            self.button_move_to_bottom.setEnabled(True)

            self.button_close_selected.setEnabled(True)
            self.button_export_selected.setEnabled(True)
        else:
            self.button_move_up.setEnabled(False)
            self.button_move_down.setEnabled(False)
            self.button_move_to_top.setEnabled(False)
            self.button_move_to_bottom.setEnabled(False)

            self.button_close_selected.setEnabled(False)
            self.button_export_selected.setEnabled(False)

    def _move_file(self, row_from, row_to):
        self.parent.files[row_from], self.parent.files[row_to] = self.parent.files[row_to], self.parent.files[row_from]

        self.clearContents()

        for file in self.parent.files:
            file.write(self.parent.files.index(file))

        self.setRangeSelected(QTableWidgetSelectionRange(row_from, 0, row_from, self.columnCount() - 1), False)
        self.setRangeSelected(QTableWidgetSelectionRange(row_to, 0, row_to, self.columnCount() - 1), True)

    def move_up(self):
        for i, row in enumerate(self.fetch_selected_rows()):
            if row > i:
                self._move_file(row, row - 1)

    def move_down(self):
        for i, row in enumerate(self.fetch_selected_rows(descending = True)):
            if row < self.rowCount() - i - 1:
                self._move_file(row, row + 1)

    def move_to_top(self):
        for i, row in enumerate(self.fetch_selected_rows()):
            self._move_file(row, i)

    def move_to_bottom(self):
        for i, row in enumerate(self.fetch_selected_rows(descending = True)):
            self._move_file(row, self.rowCount() - 1 - i)

    def _append_files(self, file_paths):
        count_duplicate = 0

        for file_path in file_paths:
            if os.path.splitext(file_path)[1] in self.parent.file_exts:
                file = Wordless_File(self.parent, self, file_path)

                duplicate = False

                for file_loaded in self.parent.files:
                    if file_path == file_loaded.path:
                        duplicate = True

                        break

                if duplicate:
                    count_duplicate += 1
                else:
                    self.parent.files.append(file)
                    file.write(self.parent.files.index(file))

        if count_duplicate > 0:
            QMessageBox.information(self,
                                    self.tr('Duplicate Warning'),
                                    self.tr('Skipped {} duplicate files!'.format(count_duplicate)),
                                    QMessageBox.Ok)

        self.item_changed()

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self.parent,
                                                self.tr('Choose a file'),
                                                '.',
                                                ';;'.join(self.parent.file_exts.values()))[0]

        self._append_files([file_path])

    def open_files(self):
        file_paths = QFileDialog.getOpenFileNames(self.parent,
                                                  self.tr('Choose multiple files'),
                                                  '.',
                                                  ';;'.join(self.parent.file_exts.values()))[0]

        self._append_files(file_paths)

    def open_dir(self):
        file_paths = []

        dir_path = QFileDialog.getExistingDirectory(self.parent,
                                                    self.tr('Choose a folder'),
                                                    '.')

        if dir_path:
            for walk in os.walk(dir_path):
                dir_name = walk[0]

                for file_name in walk[2]:
                    file_path = os.path.realpath(os.path.join(dir_name, file_name))
                    file_paths.append(file_path)

        self._append_files(file_paths)

    def close_selected(self):
        files_closed_temp = []

        for row in self.fetch_selected_rows(descending = True):
            files_closed_temp.append(self.parent.files.pop(row))
            self.removeRow(row)

        self.parent.files_closed.append(files_closed_temp)

        if self.rowCount() == 0:
            self.setRowCount(1)

        self.item_changed()

    def close_all(self):
        self.parent.files_closed.append(self.parent.files.copy())
        self.parent.files.clear()

        self.clear_table()

        self.item_changed()

    def reopen(self):
        for file in self.parent.files_closed.pop():
            self.parent.files.append(file)
            file.write(self.parent.files.index(file))

        self.item_changed()

    def select_all(self):
        if self.item(0, 0):
            for i in range(self.rowCount()):
                if self.item(i, 0).checkState() == Qt.Unchecked:
                    self.item(i, 0).setCheckState(Qt.Checked)

    def inverse(self):
        if self.item(0, 0):
            for i in range(self.rowCount()):
                if self.item(i, 0).checkState() == Qt.Checked:
                    self.item(i, 0).setCheckState(Qt.Unchecked)
                else:
                    self.item(i, 0).setCheckState(Qt.Checked)

    def deselect_all(self):
        if self.item(0, 0):
            for i in range(self.rowCount()):
                if self.item(i, 0).checkState() == Qt.Checked:
                    self.item(i, 0).setCheckState(Qt.Unchecked)

    def import_list(self):


        self.item_changed()

    def auto_save(self):
        with open('wordless_files.csv', 'w', encoding = 'UTF-8', newline = '') as f:
            writer = csv.writer(f)

            for file in self.parent.files:
                writer.writerow([file.selected,
                                 file.name,
                                 file.lang_code,
                                 file.lang_text,
                                 file.path,
                                 file.ext,
                                 file.ext_text,
                                 file.encoding_code,
                                 file.encoding_text,
                                 file.delimiter])

    def auto_restore(self):
        if os.path.exists('wordless_files.csv'):
            with open('wordless_files.csv', 'r', encoding = 'UTF-8') as f:
                for i, row in enumerate(csv.reader(f)):
                    file = Wordless_File(self.parent, self, row[2], auto_detect = False)

                    file.selected = True if row[0] == 'True' else False
                    file.name = row[1]
                    file.lang_code = row[2]
                    file.lang_text = row[3]
                    file.path = row[4]
                    file.ext = row[5]
                    file.ext_text = row[6]
                    file.encoding_code = row[7]
                    file.encoding_text = row[8]
                    file.delimiter = row[9]

                    self.parent.files.append(file)
                    file.write(i)

        self.item_changed()

def init(self):
    groupbox_files = QGroupBox(self.tr('File List'), self)

    table_files = Wordless_Table_Files(self,
                                       headers = [
                                                     self.tr('Name'),
                                                     self.tr('Language'),
                                                     self.tr('Path'),
                                                     self.tr('Type'),
                                                     self.tr('Encoding')
                                                 ],
                                       stretch_columns = ['Path'])

    layout_upper = QGridLayout()
    layout_upper.addWidget(table_files, 0, 0, 6, 1)
    layout_upper.addWidget(table_files.button_move_up, 0, 1, 1, 2)
    layout_upper.addWidget(table_files.button_move_down, 1, 1, 1, 2)
    layout_upper.addWidget(table_files.button_move_to_top, 2, 1, 1, 2)
    layout_upper.addWidget(table_files.button_move_to_bottom, 3, 1, 1, 2)

    layout_upper.setColumnStretch(0, 20)
    layout_upper.setColumnStretch(1, 1)

    layout = QGridLayout()
    layout.addLayout(layout_upper, 0, 0, 1, 6)
    layout.addWidget(table_files.button_open_file, 1, 0)
    layout.addWidget(table_files.button_open_files, 1, 1)
    layout.addWidget(table_files.button_open_dir, 1, 2)
    layout.addWidget(table_files.button_close_selected, 1, 3)
    layout.addWidget(table_files.button_close_all, 1, 4)
    layout.addWidget(table_files.button_reopen, 1, 5)
    layout.addWidget(table_files.button_select_all, 2, 0)
    layout.addWidget(table_files.button_inverse, 2, 1)
    layout.addWidget(table_files.button_deselect_all, 2, 2)
    layout.addWidget(table_files.button_import_list, 2, 3)
    layout.addWidget(table_files.button_export_selected, 2, 4)
    layout.addWidget(table_files.button_export_all, 2, 5)
    
    groupbox_files.setLayout(layout)

    return groupbox_files
