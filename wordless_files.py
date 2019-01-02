#
# Wordless: Files
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *
from wordless_utils import *

class Wordless_Files():
    def __init__(self, table):
        self.main = table.main
        self.table = table

    def _new_file(self, file_path, detection = True):
        file = {}

        file['selected'] = True

        file['path'] = os.path.normpath(file_path)
        _, file_name = os.path.split(file['path'])
        file['name'], file['ext_code'] = os.path.splitext(file_name)
        file['ext_text'] = wordless_conversion.to_ext_text(self.main, file['ext_code'])

        if detection:
            file['encoding_code'] = wordless_detection.detect_encoding(self.main, file)
            file['encoding_text'] = wordless_conversion.to_encoding_text(self.main, file['encoding_code'])
            file['lang_code'] = wordless_detection.detect_lang(self.main, file)
            file['lang_text'] = wordless_conversion.to_lang_text(self.main, file['lang_code'])

        return file

    @ wordless_misc.log_timing
    def add_files(self, file_paths):
        len_files_old = len(self.main.settings_custom['file']['files_open'])

        for file_path in file_paths:
            if os.path.splitext(file_path)[1] in self.main.settings_global['file_exts']:
                if os.path.getsize(file_path):
                    self.main.settings_custom['file']['files_open'].append(self._new_file(file_path))
                else:
                    wordless_message_box.wordless_message_box_empty_file(self.main, file_path)

        self.write_table()

        len_files_new = len(self.main.settings_custom['file']['files_open'])

        if len_files_new - len_files_old == 0:
            self.main.status_bar.showMessage('No files are newly opened!')
        elif len_files_new - len_files_old == 1:
            self.main.status_bar.showMessage('1 file has been successfully loaded.')
        else:
            self.main.status_bar.showMessage(f'{len_files_new - len_files_old} files have been successfully loaded.')

    def remove_files(self, indexes):
        self.main.settings_custom['file']['files_closed'].append([])

        for i in reversed(indexes):
            self.main.settings_custom['file']['files_closed'][-1].append(self.main.settings_custom['file']['files_open'].pop(i))

        self.write_table()

    def reopen_files(self):
        files = self.main.settings_custom['file']['files_closed'].pop()

        self.main.settings_custom['file']['files_open'].extend(wordless_misc.check_file_existence(self.main, files))

        self.write_table()

    def write_table(self):
        files = wordless_misc.check_file_existence(self.main, self.main.settings_custom['file']['files_open'])

        self.table.blockSignals(True)

        if files:
            self.table.clear_table(len(files))

            for i, file in enumerate(files):
                checkbox_name = QTableWidgetItem(file['name'])
                combo_box_lang = wordless_box.Wordless_Combo_Box_Lang(self.main)
                combo_box_encoding = wordless_box.Wordless_Combo_Box_Encoding(self.main)

                if file['selected']:
                    checkbox_name.setCheckState(Qt.Checked)
                else:
                    checkbox_name.setCheckState(Qt.Unchecked)

                combo_box_lang.setCurrentText(file['lang_text'])
                combo_box_encoding.setCurrentText(file['encoding_text'])

                combo_box_lang.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 1)))
                combo_box_encoding.currentTextChanged.connect(lambda: self.table.itemChanged.emit(self.table.item(i, 4)))
                
                self.table.setItem(i, 0, checkbox_name)
                self.table.setCellWidget(i, 1, combo_box_lang)
                self.table.setItem(i, 2, QTableWidgetItem(file['path']))
                self.table.setItem(i, 3, QTableWidgetItem(file['ext_text']))
                self.table.setCellWidget(i, 4, combo_box_encoding)
        else:
            self.table.clear_table(1)

        self.table.blockSignals(False)

        self.table.itemChanged.emit(self.table.item(0, 0))

    def get_selected_files(self):
        files_selected = [file for file in self.main.settings_custom['file']['files_open'] if file['selected']]

        return files_selected

    def find_selected_file(self, file_name):
        for file in self.get_selected_files():
            if file['name'] == file_name:
                return file

class Wordless_Table_Files(wordless_table.Wordless_Table_Data):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('File Name'),
                             main.tr('Language'),
                             main.tr('Path'),
                             main.tr('Type'),
                             main.tr('Encoding')
                         ],
                         cols_stretch = [main.tr('Path')],
                         drag_drop_enabled = True)

        self.itemChanged.connect(self.file_item_changed)
        self.itemClicked.connect(self.file_item_changed)
        self.itemSelectionChanged.connect(self.file_selection_changed)

        self.button_open_files = QPushButton(self.tr('Add File(s)...'))
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
        self.button_open_dir.clicked.connect(lambda: self.open_dir(self.main.settings_custom['file']['subfolders']))
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

    def file_item_changed(self):
        duplicate_files = 0

        self.main.settings_custom['file']['files_open'].clear()

        if any([self.item(0, i) for i in range(self.columnCount())]):
            for row in reversed(list(range(self.rowCount()))):
                for row_above in range(row):
                    if self.item(row, 2).text() == self.item(row_above, 2).text():
                        self.removeRow(row)

                        duplicate_files += 1

                        break

            for row in range(self.rowCount()):
                file = self.main.wordless_files._new_file(self.item(row, 2).text(), detection = False)

                file['selected'] = True if self.item(row, 0).checkState() == Qt.Checked else False
                file['lang_text'] = self.cellWidget(row, 1).currentText()
                file['lang_code'] = wordless_conversion.to_lang_code(self.main, file['lang_text'])
                file['encoding_text'] = self.cellWidget(row, 4).currentText()
                file['encoding_code'] = wordless_conversion.to_encoding_code(self.main, file['encoding_text'])

                self.main.settings_custom['file']['files_open'].append(file)

        if any([self.item(0, i) for i in range(self.columnCount())]):
            self.button_select_all.setEnabled(True)
            self.button_inverse.setEnabled(True)
            self.button_deselect_all.setEnabled(True)

            self.button_close_all.setEnabled(True)
        else:
            self.button_select_all.setEnabled(False)
            self.button_inverse.setEnabled(False)
            self.button_deselect_all.setEnabled(False)

            self.button_close_all.setEnabled(False)

        if self.main.settings_custom['file']['files_closed']:
            self.button_reopen.setEnabled(True)
        else:
            self.button_reopen.setEnabled(False)

        if self.rowCount() == 0:
            self.setRowCount(1)

        self.file_selection_changed()

        if duplicate_files:
            QMessageBox.information(self.main,
                                    self.tr('Duplicate Files Found'),
                                    self.tr(f'{duplicate_files} duplicate files have been removed.'),
                                    QMessageBox.Ok)

    def file_selection_changed(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            if self.selectedIndexes():
                self.button_close_selected.setEnabled(True)
            else:
                self.button_close_selected.setEnabled(False)

    def open_files(self):
        file_paths = QFileDialog.getOpenFileNames(self.main,
                                                  self.tr('Choose multiple files'),
                                                  self.main.settings_custom['general']['file_default_path'],
                                                  ';;'.join(self.main.settings_global['file_exts'].values()))[0]

        if file_paths:
            self.main.wordless_files.add_files(file_paths)

            self.main.settings_custom['general']['file_default_path'] = os.path.split(file_paths[0])[0]

    def open_dir(self, subfolders = True):
        file_paths = []

        file_dir = QFileDialog.getExistingDirectory(self.main,
                                                     self.tr('Choose a folder'),
                                                     self.main.settings_custom['general']['file_default_path'],)

        if file_dir:
            if subfolders:
                for dir_path, dir_names, file_names in os.walk(file_dir):
                    for file_name in file_names:
                        file_paths.append(os.path.realpath(os.path.join(dir_path, file_name)))
            else:
                file_names = list(os.walk(file_dir))[0][2]

                for file_name in file_names:
                    file_paths.append(os.path.realpath(os.path.join(file_dir, file_name)))

            self.main.wordless_files.add_files(file_paths)

            self.main.settings_custom['general']['file_default_path'] = file_dir

    def reopen(self):
        self.main.wordless_files.reopen_files()

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

    def close_selected(self):
        self.main.wordless_files.remove_files(self.selected_rows())

    def close_all(self):
        self.main.wordless_files.remove_files(list(range(len(self.main.settings_custom['file']['files_open']))))

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings_saved = copy.deepcopy(main.settings_default['file'])
        else:
            settings_saved = copy.deepcopy(main.settings_custom['file'])

        checkbox_subfolders.setChecked(settings_saved['subfolders'])

        checkbox_detect_langs.setChecked(settings_saved['detect_langs'])
        checkbox_detect_encodings.setChecked(settings_saved['detect_encodings'])

        folder_settings_changed()
        auto_detection_settings_changed()

    def folder_settings_changed():
        settings['subfolders'] = checkbox_subfolders.isChecked()

    def auto_detection_settings_changed():
        settings['detect_langs'] = checkbox_detect_langs.isChecked()
        settings['detect_encodings'] = checkbox_detect_encodings.isChecked()

    settings = main.settings_custom['file']

    tab_files = wordless_layout.Wordless_Tab(main, load_settings)

    table_files = Wordless_Table_Files(main)

    tab_files.layout_table.addWidget(table_files, 0, 0, 1, 4)
    tab_files.layout_table.addWidget(table_files.button_open_files, 1, 0)
    tab_files.layout_table.addWidget(table_files.button_open_dir, 1, 1)
    tab_files.layout_table.addWidget(table_files.button_reopen, 1, 2)
    tab_files.layout_table.addWidget(table_files.button_select_all, 2, 0)
    tab_files.layout_table.addWidget(table_files.button_inverse, 2, 1)
    tab_files.layout_table.addWidget(table_files.button_deselect_all, 2, 2)
    tab_files.layout_table.addWidget(table_files.button_close_selected, 1, 3)
    tab_files.layout_table.addWidget(table_files.button_close_all, 2, 3)

    # Folder Settings
    group_box_folder_settings = QGroupBox(main.tr('Folder Settings'), main)

    checkbox_subfolders = QCheckBox(main.tr('Subfolders'), main)

    checkbox_subfolders.stateChanged.connect(folder_settings_changed)

    group_box_folder_settings.setLayout(QGridLayout())
    group_box_folder_settings.layout().addWidget(checkbox_subfolders, 0, 0)

    # Auto-detection Settings
    group_box_auto_detection_settings = QGroupBox(main.tr('Auto-detection Settings'), main)

    checkbox_detect_langs = QCheckBox(main.tr('Detect Languages'), main)
    checkbox_detect_encodings = QCheckBox(main.tr('Detect Encodings'), main)

    checkbox_detect_langs.stateChanged.connect(auto_detection_settings_changed)
    checkbox_detect_encodings.stateChanged.connect(auto_detection_settings_changed)

    group_box_auto_detection_settings.setLayout(QGridLayout())
    group_box_auto_detection_settings.layout().addWidget(checkbox_detect_langs, 0, 0)
    group_box_auto_detection_settings.layout().addWidget(checkbox_detect_encodings, 1, 0)

    tab_files.layout_settings.addWidget(group_box_folder_settings, 0, 0, Qt.AlignTop)
    tab_files.layout_settings.addWidget(group_box_auto_detection_settings, 1, 0, Qt.AlignTop)

    tab_files.layout_settings.setRowStretch(2, 1)

    load_settings()

    return tab_files
