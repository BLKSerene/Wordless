#
# Wordless: Settings - Import
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
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

from wl_utils import wl_conversion
from wl_widgets import wl_box, wl_layout, wl_tree

class Wl_Settings_Import(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

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
        self.checkbox_import_search_terms_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_import_search_terms_browse.clicked.connect(self.browse_search_terms)

        group_box_import_search_terms.setLayout(wl_layout.Wl_Layout())
        group_box_import_search_terms.layout().addWidget(self.label_import_search_terms_default_path, 0, 0)
        group_box_import_search_terms.layout().addWidget(self.line_edit_import_search_terms_default_path, 0, 1)
        group_box_import_search_terms.layout().addWidget(self.button_import_search_terms_browse, 0, 2)
        group_box_import_search_terms.layout().addWidget(self.checkbox_import_search_terms_detect_encodings, 1, 0, 1, 3)

        # Stop Words
        group_box_import_stop_words = QGroupBox(self.tr('Stop Words'), self)

        self.label_import_stop_words_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_stop_words_default_path = QLineEdit(self)
        self.button_import_stop_words_browse = QPushButton(self.tr('Browse'), self)
        self.checkbox_import_stop_words_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_import_stop_words_browse.clicked.connect(self.browse_stop_words)

        group_box_import_stop_words.setLayout(wl_layout.Wl_Layout())
        group_box_import_stop_words.layout().addWidget(self.label_import_stop_words_default_path, 0, 0)
        group_box_import_stop_words.layout().addWidget(self.line_edit_import_stop_words_default_path, 0, 1)
        group_box_import_stop_words.layout().addWidget(self.button_import_stop_words_browse, 0, 2)
        group_box_import_stop_words.layout().addWidget(self.checkbox_import_stop_words_detect_encodings, 1, 0, 1, 3)

        # Temporary Files
        group_box_import_temp_files = QGroupBox(self.tr('Temporary Files'), self)

        self.label_import_temp_files_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_temp_files_default_path = QLineEdit(self)
        self.button_import_temp_files_browse = QPushButton(self.tr('Browse...'), self)
        self.label_import_temp_files_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_import_temp_files_default_encoding = wl_box.Wl_Combo_Box_Encoding(self)

        self.button_import_temp_files_browse.clicked.connect(self.browse_temp_files)

        group_box_import_temp_files.setLayout(wl_layout.Wl_Layout())
        group_box_import_temp_files.layout().addWidget(self.label_import_temp_files_default_path, 0, 0)
        group_box_import_temp_files.layout().addWidget(self.line_edit_import_temp_files_default_path, 0, 1)
        group_box_import_temp_files.layout().addWidget(self.button_import_temp_files_browse, 0, 2)
        group_box_import_temp_files.layout().addWidget(self.label_import_temp_files_default_encoding, 1, 0)
        group_box_import_temp_files.layout().addWidget(self.combo_box_import_temp_files_default_encoding, 1, 1, 1, 2)

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
            self.main.settings_custom['import']['files']['default_path']
        )

        if path_file:
            self.line_edit_import_files_default_path.setText(wl_misc.get_normalized_path(path_file))

    def browse_search_terms(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.main.settings_custom['import']['search_terms']['default_path']
        )

        if path_file:
            self.line_edit_import_search_terms_default_path.setText(wl_misc.get_normalized_path(path_file))

    def browse_stop_words(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.main.settings_custom['import']['stop_words']['default_path']
        )

    def browse_temp_files(self):
        path_file = QFileDialog.getExistingDirectory(
            self.main,
            self.tr('Select Folder'),
            self.main.settings_custom['import']['temp_files']['default_path']
        )

        if path_file:
            self.line_edit_import_temp_files_default_path.setText(wl_misc.get_normalized_path(path_file))

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        if os.path.exists(settings['import']['files']['default_path']):
            self.line_edit_import_files_default_path.setText(settings['import']['files']['default_path'])
        else:
            self.line_edit_import_files_default_path.setText(self.main.settings_default['import']['files']['default_path'])

        if os.path.exists(settings['import']['search_terms']['default_path']):
            self.line_edit_import_search_terms_default_path.setText(settings['import']['search_terms']['default_path'])
        else:
            self.line_edit_import_search_terms_default_path.setText(self.main.settings_default['import']['search_terms']['default_path'])

        self.checkbox_import_search_terms_detect_encodings.setChecked(settings['import']['search_terms']['detect_encodings'])

        if os.path.exists(settings['import']['stop_words']['default_path']):
            self.line_edit_import_stop_words_default_path.setText(settings['import']['stop_words']['default_path'])
        else:
            self.line_edit_import_stop_words_default_path.setText(self.main.settings_default['import']['stop_words']['default_path'])

        self.checkbox_import_stop_words_detect_encodings.setChecked(settings['import']['stop_words']['detect_encodings'])

        self.line_edit_import_temp_files_default_path.setText(settings['import']['temp_files']['default_path'])
        self.combo_box_import_temp_files_default_encoding.setCurrentText(wl_conversion.to_encoding_text(self.main, settings['import']['temp_files']['default_encoding']))

    def validate_settings(self):
        if (self.validate_path(self.line_edit_import_files_default_path) and
            self.validate_path(self.line_edit_import_search_terms_default_path) and
            self.validate_path(self.line_edit_import_stop_words_default_path) and
            self.confirm_path(self.line_edit_import_temp_files_default_path)):
            return True
        else:
            return False

    def apply_settings(self):
        settings = self.main.settings_custom

        settings['import']['files']['default_path'] = self.line_edit_import_files_default_path.text()

        settings['import']['search_terms']['default_path'] = self.line_edit_import_search_terms_default_path.text()
        settings['import']['search_terms']['detect_encodings'] = self.checkbox_import_search_terms_detect_encodings.isChecked()

        settings['import']['stop_words']['default_path'] = self.line_edit_import_stop_words_default_path.text()
        settings['import']['stop_words']['detect_encodings'] = self.checkbox_import_stop_words_detect_encodings.isChecked()

        settings['import']['temp_files']['default_path'] = self.line_edit_import_temp_files_default_path.text()
        settings['import']['temp_files']['default_encoding'] = wl_conversion.to_encoding_code(self.main, self.combo_box_import_temp_files_default_encoding.currentText())

        return True
