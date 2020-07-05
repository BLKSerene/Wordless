#
# Wordless: Settings - Export
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import wordless_conversion
from wordless_widgets import wordless_box, wordless_layout, wordless_tree

class Wordless_Settings_Export(wordless_tree.Wordless_Settings):
    def __init__(self, main):
        super().__init__(main)

        # Tables
        group_box_export_tables = QGroupBox(self.tr('Tables'), self)

        self.label_export_tables_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_export_tables_default_path = QLineEdit(self)
        self.button_export_tables_default_path = QPushButton(self.tr('Browse'), self)
        self.label_export_tables_default_type = QLabel(self.tr('Default Type:'), self)
        self.combo_box_export_tables_default_type = wordless_box.Wordless_Combo_Box(self)
        self.label_export_tables_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_export_tables_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        self.combo_box_export_tables_default_type.addItems(self.main.settings_global['file_types']['export_tables'])

        self.button_export_tables_default_path.clicked.connect(self.browse_tables)
        self.combo_box_export_tables_default_type.currentTextChanged.connect(self.tables_default_type_changed)

        group_box_export_tables.setLayout(wordless_layout.Wordless_Layout())
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
        self.combo_box_export_search_terms_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self)

        self.button_export_search_terms_default_path.clicked.connect(self.browse_search_terms)

        group_box_export_search_terms.setLayout(wordless_layout.Wordless_Layout())
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
        self.combo_box_export_stop_words_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self)

        self.button_export_stop_words_default_path.clicked.connect(self.browse_stop_words)

        group_box_export_stop_words.setLayout(wordless_layout.Wordless_Layout())
        group_box_export_stop_words.layout().addWidget(self.label_export_stop_words_default_path, 0, 0)
        group_box_export_stop_words.layout().addWidget(self.line_edit_export_stop_words_default_path, 0, 1)
        group_box_export_stop_words.layout().addWidget(self.button_export_stop_words_default_path, 0, 2)
        group_box_export_stop_words.layout().addWidget(self.label_export_stop_words_default_encoding, 1, 0)
        group_box_export_stop_words.layout().addWidget(self.combo_box_export_stop_words_default_encoding, 1, 1, 1, 2)

        self.setLayout(wordless_layout.Wordless_Layout())
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
            self.main.settings_custom['export']['tables']['default_path']
        )

        if path_file:
            self.line_edit_export_tables_default_path.setText(wordless_misc.get_normalized_path(path_file))

    def browse_search_terms(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.main.settings_custom['export']['search_terms']['default_path']
        )

        if path_file:
            self.line_edit_export_search_terms_default_path.setText(wordless_misc.get_normalized_path(path_file))

    def browse_stop_words(self):
        path_file = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select Folder'),
            self.main.settings_custom['export']['stop_words']['default_path']
        )

        if path_file:
            self.line_edit_export_stop_words_default_path.setText(wordless_misc.get_normalized_path(path_file))

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        self.line_edit_export_tables_default_path.setText(settings['export']['tables']['default_path'])
        self.combo_box_export_tables_default_type.setCurrentText(settings['export']['tables']['default_type'])
        self.combo_box_export_tables_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['export']['tables']['default_encoding']))

        self.line_edit_export_search_terms_default_path.setText(settings['export']['search_terms']['default_path'])
        self.combo_box_export_search_terms_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['export']['search_terms']['default_encoding']))

        self.line_edit_export_stop_words_default_path.setText(settings['export']['stop_words']['default_path'])
        self.combo_box_export_stop_words_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['export']['stop_words']['default_encoding']))

    def validate_settings(self):
        if (self.confirm_path(self.line_edit_export_tables_default_path) and
            self.confirm_path(self.line_edit_export_search_terms_default_path) and
            self.confirm_path(self.line_edit_export_stop_words_default_path)):
            return True
        else:
            return False

    def apply_settings(self):
        settings = self.main.settings_custom

        settings['export']['tables']['default_path'] = self.line_edit_export_tables_default_path.text()
        settings['export']['tables']['default_type'] = self.combo_box_export_tables_default_type.currentText()
        settings['export']['tables']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_tables_default_encoding.currentText())

        settings['export']['search_terms']['default_path'] = self.line_edit_export_search_terms_default_path.text()
        settings['export']['search_terms']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_search_terms_default_encoding.currentText())

        settings['export']['stop_words']['default_path'] = self.line_edit_export_stop_words_default_path.text()
        settings['export']['stop_words']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_stop_words_default_encoding.currentText())

        return True
