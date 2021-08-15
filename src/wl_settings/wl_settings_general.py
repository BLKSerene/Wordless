#
# Wordless: Settings - General
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialog_misc
from wl_utils import wl_conversion
from wl_widgets import wl_box, wl_layout, wl_tree

class Wl_Settings_General(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['general']
        self.settings_custom = self.main.settings_custom['general']

        # Font Settings
        group_box_font_settings = QGroupBox(self.tr('Font Settings'), self)

        self.label_font_family = QLabel(self.tr('Font Family:'), self)
        self.combo_box_font_family = wl_box.Wl_Combo_Box_Font_Family(self)
        self.label_font_size = QLabel(self.tr('Font Size:'), self)
        self.combo_box_font_size = wl_box.Wl_Combo_Box_Font_Size(self)

        group_box_font_settings.setLayout(QGridLayout())
        group_box_font_settings.layout().addWidget(self.label_font_family, 0, 0)
        group_box_font_settings.layout().addWidget(self.combo_box_font_family, 0, 1)
        group_box_font_settings.layout().addWidget(self.label_font_size, 1, 0)
        group_box_font_settings.layout().addWidget(self.combo_box_font_size, 1, 1)

        group_box_font_settings.layout().setColumnStretch(2, 1)

        # Update Settings
        group_box_update_settings = QGroupBox(self.tr('Update Settings'), self)

        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)

        group_box_update_settings.setLayout(wl_layout.Wl_Layout())
        group_box_update_settings.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)

        # Miscellaneous
        group_box_misc = QGroupBox(self.tr('Miscellaneous'), self)

        self.checkbox_confirm_on_exit = QCheckBox(self.tr('Always confirm on exit'), self)

        group_box_misc.setLayout(wl_layout.Wl_Layout())
        group_box_misc.layout().addWidget(self.checkbox_confirm_on_exit, 0, 0)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_font_settings, 0, 0)
        self.layout().addWidget(group_box_update_settings, 1, 0)
        self.layout().addWidget(group_box_misc, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.combo_box_font_family.setCurrentFont(QFont(settings['font_settings']['font_family']))
        self.combo_box_font_size.set_text(settings['font_settings']['font_size'])

        self.checkbox_check_updates_on_startup.setChecked(settings['update_settings']['check_updates_on_startup'])

        self.checkbox_confirm_on_exit.setChecked(settings['misc']['confirm_on_exit'])

    def apply_settings(self):
        # Check font settings
        font_old = [
            self.settings_custom['font_settings']['font_family'],
            self.settings_custom['font_settings']['font_size']
        ]

        font_new = [
            self.combo_box_font_family.currentFont().family(),
            self.combo_box_font_size.get_val()
        ]

        if font_new == font_old:
            result = 'skip'
        else:
            dialog_restart_required = wl_dialog_misc.Wl_Dialog_Restart_Required(self.main)
            result = dialog_restart_required.exec_()

            if result == QDialog.Accepted:
                result = 'restart'
            elif result == QDialog.Rejected:
                result = 'cancel'

        if result in ['skip', 'restart']:
            self.settings_custom['font_settings']['font_family'] = self.combo_box_font_family.currentFont().family()
            self.settings_custom['font_settings']['font_size'] = self.combo_box_font_size.get_val()

            self.settings_custom['update_settings']['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

            self.settings_custom['misc']['confirm_on_exit'] = self.checkbox_confirm_on_exit.isChecked()

            if result == 'restart':
                self.main.restart()

            return True
        elif result == 'cancel':
            self.combo_box_font_family.setCurrentFont(QFont(font_old[0]))
            self.combo_box_font_size.set_text(font_old[1])

            return False

class Wl_Settings_Import(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['import']
        self.settings_custom = self.main.settings_custom['import']

        # Files
        group_box_import_files = QGroupBox(self.tr('Files'), self)

        self.label_import_files_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_files_default_path = QLineEdit(self)
        self.button_import_files_browse = QPushButton(self.tr('Browse...'), self)

        self.button_import_files_browse.clicked.connect(self.browse_files)

        group_box_import_files.setLayout(wl_layout.Wl_Layout())
        group_box_import_files.layout().addWidget(self.label_import_files_default_path, 0, 0)
        group_box_import_files.layout().addWidget(self.line_edit_import_files_default_path, 0, 1)
        group_box_import_files.layout().addWidget(self.button_import_files_browse, 0, 2)

        # Search Terms
        group_box_import_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_import_search_terms_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_search_terms_default_path = QLineEdit(self)
        self.button_import_search_terms_browse = QPushButton(self.tr('Browse'), self)
        self.label_import_search_terms_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_import_search_terms_default_encoding = wl_box.Wl_Combo_Box_Encoding(self)
        self.checkbox_import_search_terms_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_import_search_terms_browse.clicked.connect(self.browse_search_terms)
        self.checkbox_import_search_terms_detect_encodings.stateChanged.connect(self.detect_encodings_changed)

        group_box_import_search_terms.setLayout(wl_layout.Wl_Layout())
        group_box_import_search_terms.layout().addWidget(self.label_import_search_terms_default_path, 0, 0)
        group_box_import_search_terms.layout().addWidget(self.line_edit_import_search_terms_default_path, 0, 1)
        group_box_import_search_terms.layout().addWidget(self.button_import_search_terms_browse, 0, 2)
        group_box_import_search_terms.layout().addWidget(self.label_import_search_terms_default_encoding, 1, 0)
        group_box_import_search_terms.layout().addWidget(self.combo_box_import_search_terms_default_encoding, 1, 1, 1, 2)
        group_box_import_search_terms.layout().addWidget(self.checkbox_import_search_terms_detect_encodings, 2, 0, 1, 3)

        # Stop Words
        group_box_import_stop_words = QGroupBox(self.tr('Stop Words'), self)

        self.label_import_stop_words_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_stop_words_default_path = QLineEdit(self)
        self.button_import_stop_words_browse = QPushButton(self.tr('Browse'), self)
        self.label_import_stop_words_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_import_stop_words_default_encoding = wl_box.Wl_Combo_Box_Encoding(self)
        self.checkbox_import_stop_words_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_import_stop_words_browse.clicked.connect(self.browse_stop_words)
        self.checkbox_import_stop_words_detect_encodings.stateChanged.connect(self.detect_encodings_changed)

        group_box_import_stop_words.setLayout(wl_layout.Wl_Layout())
        group_box_import_stop_words.layout().addWidget(self.label_import_stop_words_default_path, 0, 0)
        group_box_import_stop_words.layout().addWidget(self.line_edit_import_stop_words_default_path, 0, 1)
        group_box_import_stop_words.layout().addWidget(self.button_import_stop_words_browse, 0, 2)
        group_box_import_stop_words.layout().addWidget(self.label_import_stop_words_default_encoding, 1, 0)
        group_box_import_stop_words.layout().addWidget(self.combo_box_import_stop_words_default_encoding, 1, 1, 1, 2)
        group_box_import_stop_words.layout().addWidget(self.checkbox_import_stop_words_detect_encodings, 2, 0, 1, 3)

        # Temporary Files
        group_box_import_temp_files = QGroupBox(self.tr('Temporary Files'), self)

        self.label_import_temp_files_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_temp_files_default_path = QLineEdit(self)
        self.button_import_temp_files_browse = QPushButton(self.tr('Browse...'), self)

        self.button_import_temp_files_browse.clicked.connect(self.browse_temp_files)

        group_box_import_temp_files.setLayout(wl_layout.Wl_Layout())
        group_box_import_temp_files.layout().addWidget(self.label_import_temp_files_default_path, 0, 0)
        group_box_import_temp_files.layout().addWidget(self.line_edit_import_temp_files_default_path, 0, 1)
        group_box_import_temp_files.layout().addWidget(self.button_import_temp_files_browse, 0, 2)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_import_files, 0, 0)
        self.layout().addWidget(group_box_import_search_terms, 1, 0)
        self.layout().addWidget(group_box_import_stop_words, 2, 0)
        self.layout().addWidget(group_box_import_temp_files, 3, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(4, 1)

    def browse_files(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['files']['default_path']
        )

        if path_file:
            self.line_edit_import_files_default_path.setText(wl_misc.get_normalized_path(path_file))

    def browse_search_terms(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['search_terms']['default_path']
        )

        if path_file:
            self.line_edit_import_search_terms_default_path.setText(wl_misc.get_normalized_path(path_file))

    def browse_stop_words(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['stop_words']['default_path']
        )

    def browse_temp_files(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.settings_custom['temp_files']['default_path']
        )

        if path_file:
            self.line_edit_import_temp_files_default_path.setText(wl_misc.get_normalized_path(path_file))

    def detect_encodings_changed(self):
        if self.checkbox_import_search_terms_detect_encodings.isChecked():
            self.combo_box_import_search_terms_default_encoding.setEnabled(False)
        else:
            self.combo_box_import_search_terms_default_encoding.setEnabled(True)

        if self.checkbox_import_stop_words_detect_encodings.isChecked():
            self.combo_box_import_stop_words_default_encoding.setEnabled(False)
        else:
            self.combo_box_import_stop_words_default_encoding.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Files
        if os.path.exists(settings['files']['default_path']):
            self.line_edit_import_files_default_path.setText(settings['files']['default_path'])
        else:
            self.line_edit_import_files_default_path.setText(self.main.settings_default['files']['default_path'])

        # Search Terms
        if os.path.exists(settings['search_terms']['default_path']):
            self.line_edit_import_search_terms_default_path.setText(settings['search_terms']['default_path'])
        else:
            self.line_edit_import_search_terms_default_path.setText(self.main.settings_default['search_terms']['default_path'])

        self.combo_box_import_search_terms_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['stop_words']['default_encoding']))
        self.checkbox_import_search_terms_detect_encodings.setChecked(settings['search_terms']['detect_encodings'])

        # Stop Words
        if os.path.exists(settings['stop_words']['default_path']):
            self.line_edit_import_stop_words_default_path.setText(settings['stop_words']['default_path'])
        else:
            self.line_edit_import_stop_words_default_path.setText(self.main.settings_default['stop_words']['default_path'])
        self.combo_box_import_stop_words_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['stop_words']['default_encoding']))
        self.checkbox_import_stop_words_detect_encodings.setChecked(settings['stop_words']['detect_encodings'])

        # Temporary Files
        self.line_edit_import_temp_files_default_path.setText(settings['temp_files']['default_path'])
        
        self.detect_encodings_changed()

    def validate_settings(self):
        if (self.validate_path(self.line_edit_import_files_default_path) and
            self.validate_path(self.line_edit_import_search_terms_default_path) and
            self.validate_path(self.line_edit_import_stop_words_default_path) and
            self.confirm_path(self.line_edit_import_temp_files_default_path)):
            return True
        else:
            return False

    def apply_settings(self):
        # Files
        self.settings_custom['files']['default_path'] = self.line_edit_import_files_default_path.text()

        # Search Terms
        self.settings_custom['search_terms']['default_path'] = self.line_edit_import_search_terms_default_path.text()
        self.settings_custom['search_terms']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_import_search_terms_default_encoding.currentText())
        self.settings_custom['search_terms']['detect_encodings'] = self.checkbox_import_search_terms_detect_encodings.isChecked()

        # Stop Words
        self.settings_custom['stop_words']['default_path'] = self.line_edit_import_stop_words_default_path.text()
        self.settings_custom['stop_words']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_import_stop_words_default_encoding.currentText())
        self.settings_custom['stop_words']['detect_encodings'] = self.checkbox_import_stop_words_detect_encodings.isChecked()

        # Temporary Files
        self.settings_custom['temp_files']['default_path'] = self.line_edit_import_temp_files_default_path.text()

        return True

class Wl_Settings_Export(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_default = self.main.settings_default['export']
        self.settings_custom = self.main.settings_custom['export']

        # Tables
        group_box_export_tables = QGroupBox(self.tr('Tables'), self)

        self.label_export_tables_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_export_tables_default_path = QLineEdit(self)
        self.button_export_tables_default_path = QPushButton(self.tr('Browse'), self)
        self.label_export_tables_default_type = QLabel(self.tr('Default Type:'), self)
        self.combo_box_export_tables_default_type = wl_box.Wl_Combo_Box(self)
        self.label_export_tables_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_export_tables_default_encoding = wl_box.Wl_Combo_Box_Encoding(self.main)

        self.combo_box_export_tables_default_type.addItems(self.main.settings_global['file_types']['export_tables'])

        self.button_export_tables_default_path.clicked.connect(self.browse_tables)
        self.combo_box_export_tables_default_type.currentTextChanged.connect(self.tables_default_type_changed)

        group_box_export_tables.setLayout(wl_layout.Wl_Layout())
        group_box_export_tables.layout().addWidget(self.label_export_tables_default_path, 0, 0)
        group_box_export_tables.layout().addWidget(self.line_edit_export_tables_default_path, 0, 1)
        group_box_export_tables.layout().addWidget(self.button_export_tables_default_path, 0, 2)
        group_box_export_tables.layout().addWidget(self.label_export_tables_default_type, 1, 0)
        group_box_export_tables.layout().addWidget(self.combo_box_export_tables_default_type, 1, 1, 1, 2)
        group_box_export_tables.layout().addWidget(self.label_export_tables_default_encoding, 2, 0)
        group_box_export_tables.layout().addWidget(self.combo_box_export_tables_default_encoding, 2, 1, 1 ,2)

        # Search Terms
        group_box_export_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_export_search_terms_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_export_search_terms_default_path = QLineEdit(self)
        self.button_export_search_terms_default_path = QPushButton(self.tr('Browse'), self)
        self.label_export_search_terms_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_export_search_terms_default_encoding = wl_box.Wl_Combo_Box_Encoding(self)

        self.button_export_search_terms_default_path.clicked.connect(self.browse_search_terms)

        group_box_export_search_terms.setLayout(wl_layout.Wl_Layout())
        group_box_export_search_terms.layout().addWidget(self.label_export_search_terms_default_path, 0, 0)
        group_box_export_search_terms.layout().addWidget(self.line_edit_export_search_terms_default_path, 0, 1)
        group_box_export_search_terms.layout().addWidget(self.button_export_search_terms_default_path, 0, 2)
        group_box_export_search_terms.layout().addWidget(self.label_export_search_terms_default_encoding, 1, 0)
        group_box_export_search_terms.layout().addWidget(self.combo_box_export_search_terms_default_encoding, 1, 1, 1, 2)

        # Stop Words
        group_box_export_stop_words = QGroupBox(self.tr('Stop Words'), self)

        self.label_export_stop_words_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_export_stop_words_default_path = QLineEdit(self)
        self.button_export_stop_words_default_path = QPushButton(self.tr('Browse'), self)
        self.label_export_stop_words_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_export_stop_words_default_encoding = wl_box.Wl_Combo_Box_Encoding(self)

        self.button_export_stop_words_default_path.clicked.connect(self.browse_stop_words)

        group_box_export_stop_words.setLayout(wl_layout.Wl_Layout())
        group_box_export_stop_words.layout().addWidget(self.label_export_stop_words_default_path, 0, 0)
        group_box_export_stop_words.layout().addWidget(self.line_edit_export_stop_words_default_path, 0, 1)
        group_box_export_stop_words.layout().addWidget(self.button_export_stop_words_default_path, 0, 2)
        group_box_export_stop_words.layout().addWidget(self.label_export_stop_words_default_encoding, 1, 0)
        group_box_export_stop_words.layout().addWidget(self.combo_box_export_stop_words_default_encoding, 1, 1, 1, 2)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_export_tables, 0, 0)
        self.layout().addWidget(group_box_export_search_terms, 1, 0)
        self.layout().addWidget(group_box_export_stop_words, 2, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(3, 1)

        self.tables_default_type_changed()

    def tables_default_type_changed(self):
        if self.combo_box_export_tables_default_type.currentText() == self.tr('Excel Workbook (*.xlsx)'):
            self.combo_box_export_tables_default_encoding.setEnabled(False)
        else:
            self.combo_box_export_tables_default_encoding.setEnabled(True)

    def browse_tables(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.settings_custom['tables']['default_path']
        )

        if path_file:
            self.line_edit_export_tables_default_path.setText(wl_misc.get_normalized_path(path_file))

    def browse_search_terms(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.settings_custom['search_terms']['default_path']
        )

        if path_file:
            self.line_edit_export_search_terms_default_path.setText(wl_misc.get_normalized_path(path_file))

    def browse_stop_words(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.settings_custom['stop_words']['default_path']
        )

        if path_file:
            self.line_edit_export_stop_words_default_path.setText(wl_misc.get_normalized_path(path_file))

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.line_edit_export_tables_default_path.setText(settings['tables']['default_path'])
        self.combo_box_export_tables_default_type.setCurrentText(settings['tables']['default_type'])
        self.combo_box_export_tables_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['tables']['default_encoding']))

        self.line_edit_export_search_terms_default_path.setText(settings['search_terms']['default_path'])
        self.combo_box_export_search_terms_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['search_terms']['default_encoding']))

        self.line_edit_export_stop_words_default_path.setText(settings['stop_words']['default_path'])
        self.combo_box_export_stop_words_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['stop_words']['default_encoding']))

    def validate_settings(self):
        if (self.confirm_path(self.line_edit_export_tables_default_path) and
            self.confirm_path(self.line_edit_export_search_terms_default_path) and
            self.confirm_path(self.line_edit_export_stop_words_default_path)):
            return True
        else:
            return False

    def apply_settings(self):
        self.settings_custom['tables']['default_path'] = self.line_edit_export_tables_default_path.text()
        self.settings_custom['tables']['default_type'] = self.combo_box_export_tables_default_type.currentText()
        self.settings_custom['tables']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_export_tables_default_encoding.currentText())

        self.settings_custom['search_terms']['default_path'] = self.line_edit_export_search_terms_default_path.text()
        self.settings_custom['search_terms']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_export_search_terms_default_encoding.currentText())

        self.settings_custom['stop_words']['default_path'] = self.line_edit_export_stop_words_default_path.text()
        self.settings_custom['stop_words']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_export_stop_words_default_encoding.currentText())

        return True
