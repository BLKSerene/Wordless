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

    def _new_file(self, file_path):
        file = {}

        file['selected'] = True

        file['path'] = os.path.normpath(file_path)
        file['name'], file['ext_code'] = os.path.splitext(os.path.basename(file['path']))
        file['ext_text'] = wordless_conversion.to_ext_text(self.main, file['ext_code'])

        file['encoding_code'] = wordless_detection.detect_encoding(self.main, file)
        file['encoding_text'] = wordless_conversion.to_encoding_text(self.main, file['encoding_code'])

        file['lang_code'] = wordless_detection.detect_lang(self.main, file)
        file['lang_text'] = wordless_conversion.to_lang_text(self.main, file['lang_code'])

        file['name_old'] = file['name']

        return file

    @ wordless_misc.log_timing
    def add_files(self, file_paths):
        files_nonexistent = []
        files_unsupported = []
        files_empty = []
        files_duplicate = []

        len_files_old = len(self.main.settings_custom['file']['files_open'])

        for file_path in wordless_misc.check_files_by_path(self.main, file_paths):
            new_file = self._new_file(file_path)

            # Check duplicate file name
            if self.find_file_by_name(new_file['name']):
                i = 1

                while True:
                    file_name = f"{new_file['name']} ({i})"

                    if self.find_file_by_name(file_name):
                        i += 1
                    else:
                        new_file['name'] = new_file['name_old'] = file_name

                        break

            self.main.settings_custom['file']['files_open'].append(new_file)

        self.write_table()

        len_files_new = len(self.main.settings_custom['file']['files_open'])

        if len_files_new - len_files_old == 0:
            self.main.status_bar.showMessage('No files are newly opened!')
        elif len_files_new - len_files_old == 1:
            self.main.status_bar.showMessage('1 file has been successfully opened.')
        else:
            self.main.status_bar.showMessage(f'{len_files_new - len_files_old} files have been successfully opened.')

    def remove_files(self, indexes):
        self.main.settings_custom['file']['files_closed'].append([])

        for i in reversed(indexes):
            self.main.settings_custom['file']['files_closed'][-1].append(self.main.settings_custom['file']['files_open'].pop(i))

        self.write_table()

    def write_table(self, check_files = False):
        if check_files:
            files = copy.deepcopy(self.main.settings_custom['file']['files_open'])

            self.main.settings_custom['file']['files_open'].clear()

            for file in wordless_misc.check_files(self.main, files):
                self.main.settings_custom['file']['files_open'].append(file)

        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

        files = self.main.settings_custom['file']['files_open']

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
        self.table.setUpdatesEnabled(True)

        self.table.itemChanged.emit(self.table.item(0, 0))

    def get_selected_files(self):
        files_selected = [file for file in self.main.settings_custom['file']['files_open'] if file['selected']]

        return files_selected

    def find_file_by_name(self, file_name, selected_only = False):
        if selected_only:
            files = self.get_selected_files()
        else:
            files = self.main.settings_custom['file']['files_open']

        for file in files:
            if file['name'] == file_name:
                return file

        return None

    def find_file_by_path(self, file_path, selected_only = False):
        if selected_only:
            files = self.get_selected_files()
        else:
            files = self.main.settings_custom['file']['files_open']
            
        for file in files:
            if file['path'] == file_path:
                return file

        return None

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
        self.cellDoubleClicked.connect(self.cell_double_clicked)

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

        self.file_item_changed()

    def file_item_changed(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            # Check duplicate file name
            for row in range(self.rowCount()):
                file_name = self.item(row, 0).text()
                file_path = self.item(row, 2).text()

                file = self.main.wordless_files.find_file_by_path(file_path)

                if file_name != file['name_old']:
                    if self.main.wordless_files.find_file_by_name(file_name):
                        self.blockSignals(True)

                        self.item(row, 0).setText(file['name_old'])
                        
                        self.blockSignals(False)

                        wordless_message_box.wordless_message_box_duplicate_file_name(self.main)

                        self.closePersistentEditor(self.item(row, 0))
                        self.editItem(self.item(row, 0))

                    break

            self.main.settings_custom['file']['files_open'].clear()

            for row in range(self.rowCount()):
                new_file = {}

                new_file['selected'] = True if self.item(row, 0).checkState() == Qt.Checked else False

                new_file['name'] = new_file['name_old'] = self.item(row, 0).text()

                new_file['lang_text'] = self.cellWidget(row, 1).currentText()
                new_file['lang_code'] = wordless_conversion.to_lang_code(self.main, new_file['lang_text'])

                new_file['path'] = self.item(row, 2).text()

                new_file['ext_text'] = self.item(row, 3).text()
                new_file['ext_code'] = wordless_conversion.to_ext_code(self.main, new_file['ext_text'])

                new_file['encoding_text'] = self.cellWidget(row, 4).currentText()
                new_file['encoding_code'] = wordless_conversion.to_encoding_code(self.main, new_file['encoding_text'])

                self.main.settings_custom['file']['files_open'].append(new_file)

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

    def file_selection_changed(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            if self.selectedIndexes():
                self.button_close_selected.setEnabled(True)
            else:
                self.button_close_selected.setEnabled(False)

    def cell_double_clicked(self, row, col):
        if col == self.find_col(self.tr('File Name')):
            self.editItem(self.item(row, col))

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
        files = self.main.settings_custom['file']['files_closed'].pop()

        self.main.wordless_files.add_files([file['path'] for file in files])

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

    main.wordless_files = Wordless_Files(table_files)
    main.wordless_files.write_table(check_files = True)

    return tab_files
