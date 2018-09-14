#
# Wordless: Files
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import *

class Wordless_Files():
    def __init__(self, table):
        self.main = table.main
        self.table = table

    def new_file(self, file_path, auto_detect = True):
        file = {}

        file['selected'] = True

        file['path'] = os.path.normpath(file_path)
        _, file_name = os.path.split(file['path'])
        file['name'], file['ext'] = os.path.splitext(file_name)
        file['ext_text'] = wordless_misc.convert_ext(self.main, file['ext'])

        (file['encoding_code'],
         file['encoding_text']) = wordless_detection.detect_encoding(self.main, file, auto_detect = auto_detect)

        (file['lang_code'],
         file['lang_text'],
         file['word_delimiter']) = wordless_detection.detect_lang(self.main, file, auto_detect = auto_detect)

        return file

    def add_files(self, file_paths):
        count_duplicates = 0

        for file_path in file_paths:
            duplicate = False

            if os.path.splitext(file_path)[1] in self.main.file_exts:
                file = self.new_file(file_path)

                for file_open in self.main.settings['file']['files_open']:
                    if file_path == file_open['path']:
                        duplicate = True

                        break

                if duplicate:
                    count_duplicates += 1
                else:
                    self.main.settings['file']['files_open'].append(file)
        
        self.write_table()

        if count_duplicates > 0:
            QMessageBox.information(self.main,
                                    self.tr('Duplicate Warning'),
                                    self.tr('Skipped {} duplicate files!'.format(count_duplicate)),
                                    QMessageBox.Ok)

    def remove_files(self, indexes):
        self.main.settings['file']['files_closed'].append([])

        for i in reversed(indexes):
            self.main.settings['file']['files_closed'][-1].append(self.main.settings['file']['files_open'].pop(i))

        self.write_table()

    def reopen_files(self):
        paths_nonexistent = []

        for file in self.main.settings['file']['files_closed'].pop():
            if os.path.exists(file.path):
                self.main.settings['file']['files_open'].append(file)
            else:
                paths_nonexistent.append(file.path)

        if paths_nonexistent:
            QMessageBox.warning(self.main,
                                self.tr('Failed while reopening the files'),
                                self.tr('The following files cannot be reopened because they no longer exist. Please check and try again.<br>{}'.format('<br>'.join(paths_nonexistent))))

        self.write_table()

    def write_table(self):
        self.table.clear_table()
        self.table.setRowCount(len(self.main.settings['file']['files_open']))

        for i, file in enumerate(self.main.settings['file']['files_open']):
            checkbox_name = QTableWidgetItem(file['name'])
            combo_box_lang = wordless_widgets.Wordless_Combo_Box_Lang(self.main)
            combo_box_encoding = wordless_widgets.Wordless_Combo_Box_Encoding(self.main)

            if file['selected']:
                checkbox_name.setCheckState(Qt.Checked)
            else:
                checkbox_name.setCheckState(Qt.Unchecked)
            combo_box_lang.setCurrentText(file['lang_text'])
            combo_box_encoding.setCurrentText(file['encoding_text'])

            combo_box_lang.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 2)))
            combo_box_encoding.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 3)))
            
            self.table.setItem(i, 0, checkbox_name)
            self.table.setCellWidget(i, 1, combo_box_lang)
            self.table.setItem(i, 2, QTableWidgetItem(file['path']))
            self.table.setItem(i, 3, QTableWidgetItem(file['ext_text']))
            self.table.setCellWidget(i, 4, combo_box_encoding)

    def selected_files(self):
        selected_files = [file for file in self.main.settings['file']['files_open'] if file['selected']]

        if selected_files == []:
            QMessageBox.warning(self,
                                self.tr('Empty Input'),
                                self.tr('There are no files being currently selected! Please check and try again.'),
                                QMessageBox.Ok)

        return selected_files

class Wordless_Table_Files(wordless_table.Wordless_Table):
    def __init__(self, parent, headers, cols_stretch = []):
        super().__init__(parent, headers, cols_stretch = cols_stretch, drag_drop_enabled = True)

        self.itemClicked.connect(self.file_item_changed)

        self.button_open_files = QPushButton(self.tr('Add Files...'))
        self.button_open_dir = QPushButton(self.tr('Add Folder...'))

        self.button_close_selected = QPushButton(self.tr('Close Selected File(s)'))
        self.button_close_all = QPushButton(self.tr('Close All Files'))
        self.button_reopen = QPushButton(self.tr('Reopen Closed File(s)'))

        self.button_select_all = QPushButton(self.tr('Select All'))
        self.button_inverse = QPushButton(self.tr('Inverse'))
        self.button_deselect_all = QPushButton(self.tr('Deselect All'))

        self.button_clear.hide()
        self.button_export_selected.hide()
        self.button_export_all.hide()

        self.button_open_files.clicked.connect(self.open_files)
        self.button_open_dir.clicked.connect(self.open_dir)
        self.button_close_selected.clicked.connect(self.close_selected)
        self.button_close_all.clicked.connect(self.close_all)
        self.button_reopen.clicked.connect(self.reopen)

        self.button_select_all.clicked.connect(self.select_all)
        self.button_inverse.clicked.connect(self.inverse)
        self.button_deselect_all.clicked.connect(self.deselect_all)

        self.main.__class__.open_files = self.open_files
        self.main.__class__.open_dir = self.open_dir

        self.main.__class__.close_selected = self.close_selected
        self.main.__class__.close_all = self.close_all
        self.main.__class__.reopen = self.reopen

        self.main.wordless_files = Wordless_Files(self)
        self.main.wordless_files.write_table()

        self.file_item_changed()


    def file_item_changed(self):
        for row in range(self.rowCount()):
            if self.cellWidget(row, 4):
                file = self.main.wordless_files.new_file(self.item(row, 2).text(), auto_detect = False)

                file['selected'] = True if self.item(row, 0).checkState() == Qt.Checked else False
                file['lang_text'] = self.cellWidget(row, 1).currentText()
                file['lang_code'] = wordless_misc.convert_lang(self.main, file['lang_text'])
                file['word_delimiter'] = wordless_misc.convert_word_delimiter(file['lang_code'])
                file['encoding_text'] = self.cellWidget(row, 4).currentText()
                file['encoding_code'] = wordless_misc.convert_encoding(self.main, file['encoding_text'])[0]

                self.main.settings['file']['files_open'][row] = file

        if self.item(0, 0):
            self.button_select_all.setEnabled(True)
            self.button_inverse.setEnabled(True)
            self.button_deselect_all.setEnabled(True)

            self.button_close_all.setEnabled(True)
        else:
            self.button_select_all.setEnabled(False)
            self.button_inverse.setEnabled(False)
            self.button_deselect_all.setEnabled(False)

            self.button_close_all.setEnabled(False)

        if self.main.settings['file']['files_closed']:
            self.button_reopen.setEnabled(True)
        else:
            self.button_reopen.setEnabled(False)

        self.file_selection_changed()

    def file_selection_changed(self):
        if self.selectedIndexes() and self.item(0, 0):
            self.button_close_selected.setEnabled(True)
        else:
            self.button_close_selected.setEnabled(False)

    def open_files(self):
        file_paths = QFileDialog.getOpenFileNames(self.main,
                                                  self.tr('Choose multiple files'),
                                                  '.',
                                                  ';;'.join(self.main.file_exts.values()))[0]

        self.main.wordless_files.add_files(file_paths)

    def open_dir(self):
        file_paths = []

        dir_path = QFileDialog.getExistingDirectory(self.main,
                                                    self.tr('Choose a folder'),
                                                    '.')

        if dir_path:
            for walk in os.walk(dir_path):
                dir_name = walk[0]

                for file_name in walk[2]:
                    file_path = os.path.realpath(os.path.join(dir_name, file_name))
                    file_paths.append(file_path)

        self.main.wordless_files.add_files(file_paths)

    def close_selected(self):
        self.main.wordless_files.remove_files(self.selected_rows())

        if self.rowCount() == 0:
            self.setRowCount(1)

        self.file_item_changed()

    def close_all(self):
        self.main.wordless_files.remove_files(list(range(len(self.main.wordless_files.files_open))))

        self.clear_table()

        self.file_item_changed()

    def reopen(self):
        self.main.wordless_files.reopen_files()

        self.file_item_changed()

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

def init(main):
    widget_files = wordless_tab.Wordless_Tab(main, main.tr('File List'))

    table_files = Wordless_Table_Files(main,
                                       headers = [
                                           main.tr('Name'),
                                           main.tr('Language'),
                                           main.tr('Path'),
                                           main.tr('Type'),
                                           main.tr('Encoding')
                                       ],
                                       cols_stretch = ['Path'])

    widget_files.layout_table.addWidget(table_files, 0, 0, 1, 4)
    widget_files.layout_table.addWidget(table_files.button_open_files, 1, 0)
    widget_files.layout_table.addWidget(table_files.button_open_dir, 1, 1)
    widget_files.layout_table.addWidget(table_files.button_close_selected, 1, 2)
    widget_files.layout_table.addWidget(table_files.button_close_all, 1, 3)
    widget_files.layout_table.addWidget(table_files.button_reopen, 2, 0)
    widget_files.layout_table.addWidget(table_files.button_select_all, 2, 1)
    widget_files.layout_table.addWidget(table_files.button_inverse, 2, 2)
    widget_files.layout_table.addWidget(table_files.button_deselect_all, 2, 3)

    # Folder Settings
    group_box_folder_settings = QGroupBox(main.tr('Folder Settings'), main)

    checkbox_subfolders = QCheckBox(main.tr('Subfolders'), main)

    layout_folder_settings = QGridLayout()
    layout_folder_settings.addWidget(checkbox_subfolders, 0, 0)

    group_box_folder_settings.setLayout(layout_folder_settings)

    # Auto-detection Settings
    group_box_auto_detection_settings = QGroupBox(main.tr('Auto-detection Settings'), main)

    checkbox_auto_detect_lang = QCheckBox(main.tr('Language'), main)
    checkbox_auto_detect_encoding = QCheckBox(main.tr('Encoding'), main)

    layout_auto_detection_settings = QGridLayout()
    layout_auto_detection_settings.addWidget(checkbox_auto_detect_lang, 0, 0)
    layout_auto_detection_settings.addWidget(checkbox_auto_detect_encoding, 1, 0)

    group_box_auto_detection_settings.setLayout(layout_auto_detection_settings)

    widget_files.layout_settings.addWidget(group_box_folder_settings, 0, 0, Qt.AlignTop)
    widget_files.layout_settings.addWidget(group_box_auto_detection_settings, 1, 0, Qt.AlignTop)

    widget_files.layout_tab.setColumnStretch(0, 5)

    return widget_files
