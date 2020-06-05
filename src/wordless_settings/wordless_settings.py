#
# Wordless: Settings - Settings
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import itertools
import json
import os
import re
import threading
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import wordcloud

from wordless_dialogs import wordless_dialog_misc, wordless_msg_box
from wordless_tagsets import wordless_tagset_universal
from wordless_text import wordless_text_processing, wordless_text_utils
from wordless_utils import wordless_conversion, wordless_misc, wordless_threading
from wordless_widgets import (wordless_box, wordless_button, wordless_label,
                              wordless_layout, wordless_list, wordless_table,
                              wordless_tree, wordless_widgets)

class Wordless_Table_Tags_Pos(wordless_table.Wordless_Table_Tags):
    def reset_table(self):
        super().reset_table()

        for tags in self.main.settings_default['tags']['tags_pos']:
            self.add_item(texts = tags)

class Wordless_Table_Tags_Non_Pos(wordless_table.Wordless_Table_Tags):
    def reset_table(self):
        super().reset_table()

        for tags in self.main.settings_default['tags']['tags_non_pos']:
            self.add_item(texts = tags)

class Wordless_Worker_Preview_Sentence_Tokenizer(wordless_threading.Wordless_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_lang = self.main.settings_custom['sentence_tokenization']['preview_lang']
        preview_samples = self.main.settings_custom['sentence_tokenization']['preview_samples']

        preview_results = wordless_text_processing.wordless_sentence_tokenize(
            self.main,
            text = preview_samples.strip(),
            lang = preview_lang,
            sentence_tokenizer = self.sentence_tokenizer
        )

        self.worker_done.emit(preview_samples, preview_results)

class Wordless_Worker_Preview_Word_Tokenizer(wordless_threading.Wordless_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['word_tokenization']['preview_lang']
        preview_samples = self.main.settings_custom['word_tokenization']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                tokens = wordless_text_processing.wordless_word_tokenize(
                    self.main, line,
                    lang = preview_lang,
                    word_tokenizer = self.word_tokenizer
                )

                # Vietnamese
                if preview_lang == 'vie':
                    tokens = [re.sub(r'\s+', r'_', token) for token in tokens]

                preview_results.append(' '.join(tokens))
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wordless_Worker_Preview_Word_Detokenizer(wordless_threading.Wordless_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['word_detokenization']['preview_lang']
        preview_samples = self.main.settings_custom['word_detokenization']['preview_samples']

        for line in preview_samples.splitlines():
            line = line.strip()

            if line:
                text = wordless_text_processing.wordless_word_detokenize(
                    self.main,
                    tokens = line.split(),
                    lang = preview_lang,
                    word_detokenizer = self.word_detokenizer
                )
                
                preview_results.append(text)
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wordless_Worker_Preview_Pos_Tagger(wordless_threading.Wordless_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['pos_tagging']['preview_lang']
        preview_samples = self.main.settings_custom['pos_tagging']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                tokens = wordless_text_processing.wordless_word_tokenize(
                    self.main, line,
                    lang = preview_lang
                )

                tokens_tagged = wordless_text_processing.wordless_pos_tag(
                    self.main, tokens,
                    lang = preview_lang,
                    pos_tagger = self.pos_tagger,
                    tagset = self.tagset
                )

                preview_results.append(' '.join([f'{token}_{tag}' for token, tag in tokens_tagged]))
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wordless_Worker_Fetch_Data_Tagsets(wordless_threading.Wordless_Worker):
    worker_done = pyqtSignal(list)

    def run(self):
        settings_custom = self.main.settings_custom['tagsets']

        preview_lang = settings_custom['preview_lang']
        preview_pos_tagger = settings_custom['preview_pos_tagger'][preview_lang]
        mappings = settings_custom['mappings'][preview_lang][preview_pos_tagger]

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit(mappings)

class Wordless_Worker_Preview_Lemmatizer(wordless_threading.Wordless_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['lemmatization']['preview_lang']
        preview_samples = self.main.settings_custom['lemmatization']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                tokens = wordless_text_processing.wordless_word_tokenize(
                    self.main, line,
                    lang = preview_lang
                )

                lemmas = wordless_text_processing.wordless_lemmatize(
                    self.main, tokens,
                    lang = preview_lang,
                    lemmatizer = self.lemmatizer
                )

                text = wordless_text_processing.wordless_word_detokenize(
                    self.main, lemmas,
                    lang = preview_lang
                )

                preview_results.append(text)
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wordless_Settings(QDialog):
    wordless_settings_changed = pyqtSignal()

    def __init__(self, main):
        super().__init__(main)

        self.main = main

        self.pos_tag_mappings_loaded = False

        self.preview_processing_sentence_tokenization = False
        self.preview_processing_word_tokenization = False
        self.preview_processing_word_detokenization = False
        self.preview_processing_pos_tagging = False
        self.preview_processing_lemmatization = False

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedSize(800, 550)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('General')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Import')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Export')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Auto-detection')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Data')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Tags')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Sentence Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Word Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Word Detokenization')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('POS Tagging')]))
        self.tree_settings.topLevelItem(9).addChild(QTreeWidgetItem([self.tr('Tagsets')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Lemmatization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Stop Words')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Measures')]))
        self.tree_settings.topLevelItem(12).addChild(QTreeWidgetItem([self.tr('Dispersion')]))
        self.tree_settings.topLevelItem(12).addChild(QTreeWidgetItem([self.tr('Adjusted Frequency')]))
        self.tree_settings.topLevelItem(12).addChild(QTreeWidgetItem([self.tr('Statistical Significance')]))
        self.tree_settings.topLevelItem(12).addChild(QTreeWidgetItem([self.tr('Effect Size')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Figures')]))

        self.tree_settings.itemSelectionChanged.connect(self.selection_changed)

        self.scroll_area_settings = wordless_layout.Wordless_Scroll_Area(self)

        self.stacked_widget_settings = QStackedWidget(self)

        self.init_settings_general()
        self.init_settings_import()
        self.init_settings_export()
        self.init_settings_auto_detection()
        self.init_settings_data()
        self.init_settings_tags()
        self.init_settings_sentence_tokenization()
        self.init_settings_word_tokenization()
        self.init_settings_word_detokenization()

        self.init_settings_pos_tagging()
        self.init_settings_tagsets()

        self.init_settings_lemmatization()
        self.init_settings_stop_words()

        self.init_settings_dispersion()
        self.init_settings_adjusted_freq()
        self.init_settings_statistical_significance()
        self.init_settings_effect_size()

        self.init_settings_figs()

        self.stacked_widget_settings.addWidget(self.settings_general)
        self.stacked_widget_settings.addWidget(self.settings_import)
        self.stacked_widget_settings.addWidget(self.settings_export)
        self.stacked_widget_settings.addWidget(self.settings_auto_detection)
        self.stacked_widget_settings.addWidget(self.settings_data)
        self.stacked_widget_settings.addWidget(self.settings_tags)
        self.stacked_widget_settings.addWidget(self.settings_sentence_tokenization)
        self.stacked_widget_settings.addWidget(self.settings_word_tokenization)
        self.stacked_widget_settings.addWidget(self.settings_word_detokenization)

        self.stacked_widget_settings.addWidget(self.settings_pos_tagging)
        self.stacked_widget_settings.addWidget(self.settings_tagsets)

        self.stacked_widget_settings.addWidget(self.settings_lemmatization)
        self.stacked_widget_settings.addWidget(self.settings_stop_words)

        self.stacked_widget_settings.addWidget(self.settings_dispersion)
        self.stacked_widget_settings.addWidget(self.settings_adjusted_freq)
        self.stacked_widget_settings.addWidget(self.settings_statistical_significance)
        self.stacked_widget_settings.addWidget(self.settings_effect_size)

        self.stacked_widget_settings.addWidget(self.settings_figs)

        self.scroll_area_settings.setWidget(self.stacked_widget_settings)

        button_reset_settings = wordless_button.Wordless_Button_Reset_All_Settings(self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_save.clicked.connect(self.settings_save)
        button_apply.clicked.connect(self.settings_apply)
        button_cancel.clicked.connect(self.reject)

        button_reset_settings.setFixedWidth(150)
        button_save.setFixedWidth(80)
        button_apply.setFixedWidth(80)
        button_cancel.setFixedWidth(80)

        layout_buttons = wordless_layout.Wordless_Layout()
        layout_buttons.addWidget(button_reset_settings, 0, 0)
        layout_buttons.addWidget(button_save, 0, 2)
        layout_buttons.addWidget(button_apply, 0, 3)
        layout_buttons.addWidget(button_cancel, 0, 4)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wordless_layout.Wordless_Layout())
        self.layout().addWidget(self.tree_settings, 0, 0)
        self.layout().addWidget(self.scroll_area_settings, 0, 1)
        self.layout().addLayout(layout_buttons, 1, 0, 1, 2)

        self.tree_settings.item_selected_old = self.tree_settings.topLevelItem(0)
        self.tree_settings.topLevelItem(0).setSelected(True)

    def selection_changed(self):
        settings_cur = None

        if self.tree_settings.selectedItems():
            if self.settings_validate():
                item_selected = self.tree_settings.selectedItems()[0]
                item_selected_text = item_selected.text(0)

                if item_selected_text == self.tr('General'):
                    self.stacked_widget_settings.setCurrentIndex(0)
                elif item_selected_text == self.tr('Import'):
                    self.stacked_widget_settings.setCurrentIndex(1)
                elif item_selected_text == self.tr('Export'):
                    self.stacked_widget_settings.setCurrentIndex(2)
                elif item_selected_text == self.tr('Auto-detection'):
                    self.stacked_widget_settings.setCurrentIndex(3)
                elif item_selected_text == self.tr('Data'):
                    self.stacked_widget_settings.setCurrentIndex(4)
                elif item_selected_text == self.tr('Tags'):
                    self.stacked_widget_settings.setCurrentIndex(5)
                elif item_selected_text == self.tr('Sentence Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(6)
                elif item_selected_text == self.tr('Word Tokenization'):
                    self.stacked_widget_settings.setCurrentIndex(7)
                elif item_selected_text == self.tr('Word Detokenization'):
                    self.stacked_widget_settings.setCurrentIndex(8)

                elif item_selected_text == self.tr('POS Tagging'):
                    self.stacked_widget_settings.setCurrentIndex(9)

                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Tagsets'):
                    self.stacked_widget_settings.setCurrentIndex(10)

                elif item_selected_text == self.tr('Lemmatization'):
                    self.stacked_widget_settings.setCurrentIndex(11)
                elif item_selected_text == self.tr('Stop Words'):
                    self.stacked_widget_settings.setCurrentIndex(12)

                elif item_selected_text == self.tr('Measures'):
                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Dispersion'):
                    self.stacked_widget_settings.setCurrentIndex(13)
                elif item_selected_text == self.tr('Adjusted Frequency'):
                    self.stacked_widget_settings.setCurrentIndex(14)
                elif item_selected_text == self.tr('Statistical Significance'):
                    self.stacked_widget_settings.setCurrentIndex(15)
                elif item_selected_text == self.tr('Effect Size'):
                    self.stacked_widget_settings.setCurrentIndex(16)

                elif item_selected_text == self.tr('Figures'):
                    self.stacked_widget_settings.setCurrentIndex(17)

                self.tree_settings.item_selected_old = item_selected

                # Delay loading of POS tag mappings
                if item_selected_text == self.tr('Tagsets') and not self.pos_tag_mappings_loaded:
                    self.combo_box_tagsets_lang.currentTextChanged.emit(self.combo_box_tagsets_lang.currentText())

                    self.pos_tag_mappings_loaded = True
            else:
                self.tree_settings.blockSignals(True)

                self.tree_settings.clearSelection()
                self.tree_settings.item_selected_old.setSelected(True)

                self.tree_settings.blockSignals(False)

    # General
    def init_settings_general(self):
        self.settings_general = QWidget(self)

        # Font Settings
        group_box_font_settings = QGroupBox(self.tr('Font Settings'), self)

        self.label_font_family = QLabel(self.tr('Font Family:'), self)
        self.combo_box_font_family = wordless_box.Wordless_Combo_Box_Font_Family(self)
        self.label_font_size = QLabel(self.tr('Font Size:'), self)
        self.combo_box_font_size = wordless_box.Wordless_Combo_Box_Font_Size(self)

        group_box_font_settings.setLayout(QGridLayout())
        group_box_font_settings.layout().addWidget(self.label_font_family, 0, 0)
        group_box_font_settings.layout().addWidget(self.combo_box_font_family, 0, 1)
        group_box_font_settings.layout().addWidget(self.label_font_size, 1, 0)
        group_box_font_settings.layout().addWidget(self.combo_box_font_size, 1, 1)

        group_box_font_settings.layout().setColumnStretch(2, 1)

        # Update Settings
        group_box_update_settings = QGroupBox(self.tr('Update Settings'), self)

        self.checkbox_check_updates_on_startup = QCheckBox(self.tr('Check for updates on startup'), self)

        group_box_update_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_update_settings.layout().addWidget(self.checkbox_check_updates_on_startup, 0, 0)

        # Miscellaneous
        group_box_misc = QGroupBox(self.tr('Miscellaneous'), self)

        self.checkbox_confirm_on_exit = QCheckBox(self.tr('Always confirm on exit'), self)

        group_box_misc.setLayout(wordless_layout.Wordless_Layout())
        group_box_misc.layout().addWidget(self.checkbox_confirm_on_exit, 0, 0)

        self.settings_general.setLayout(wordless_layout.Wordless_Layout())
        self.settings_general.layout().addWidget(group_box_font_settings, 0, 0)
        self.settings_general.layout().addWidget(group_box_update_settings, 1, 0)
        self.settings_general.layout().addWidget(group_box_misc, 2, 0)

        self.settings_general.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_general.layout().setRowStretch(3, 1)

    # Import
    def init_settings_import(self):
        def browse_files():
            path_file = QFileDialog.getExistingDirectory(self.main,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['import']['files']['default_path'])

            if path_file:
                self.line_edit_import_files_default_path.setText(wordless_misc.get_normalized_path(path_file))

        def browse_search_terms():
            path_file = QFileDialog.getExistingDirectory(self.main,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['import']['search_terms']['default_path'])

            if path_file:
                self.line_edit_import_search_terms_default_path.setText(wordless_misc.get_normalized_path(path_file))

        def browse_stop_words():
            path_file = QFileDialog.getExistingDirectory(self.main,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['import']['stop_words']['default_path'])

        def browse_temp_files():
            path_file = QFileDialog.getExistingDirectory(self.main,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['import']['temp_files']['default_path'])

            if path_file:
                self.line_edit_import_temp_files_default_path.setText(wordless_misc.get_normalized_path(path_file))

        self.settings_import = QWidget(self)

        # Files
        group_box_import_files = QGroupBox(self.tr('Files'), self)

        self.label_import_files_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_files_default_path = QLineEdit(self)
        self.button_import_files_browse = QPushButton(self.tr('Browse...'), self)

        self.button_import_files_browse.clicked.connect(browse_files)

        group_box_import_files.setLayout(wordless_layout.Wordless_Layout())
        group_box_import_files.layout().addWidget(self.label_import_files_default_path, 0, 0)
        group_box_import_files.layout().addWidget(self.line_edit_import_files_default_path, 0, 1)
        group_box_import_files.layout().addWidget(self.button_import_files_browse, 0, 2)

        # Search Terms
        group_box_import_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_import_search_terms_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_import_search_terms_default_path = QLineEdit(self)
        self.button_import_search_terms_browse = QPushButton(self.tr('Browse'), self)
        self.checkbox_import_search_terms_detect_encodings = QCheckBox(self.tr('Auto-detect encodings'))

        self.button_import_search_terms_browse.clicked.connect(browse_search_terms)

        group_box_import_search_terms.setLayout(wordless_layout.Wordless_Layout())
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

        self.button_import_stop_words_browse.clicked.connect(browse_stop_words)

        group_box_import_stop_words.setLayout(wordless_layout.Wordless_Layout())
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
        self.combo_box_import_temp_files_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self)

        self.button_import_temp_files_browse.clicked.connect(browse_temp_files)

        group_box_import_temp_files.setLayout(wordless_layout.Wordless_Layout())
        group_box_import_temp_files.layout().addWidget(self.label_import_temp_files_default_path, 0, 0)
        group_box_import_temp_files.layout().addWidget(self.line_edit_import_temp_files_default_path, 0, 1)
        group_box_import_temp_files.layout().addWidget(self.button_import_temp_files_browse, 0, 2)
        group_box_import_temp_files.layout().addWidget(self.label_import_temp_files_default_encoding, 1, 0)
        group_box_import_temp_files.layout().addWidget(self.combo_box_import_temp_files_default_encoding, 1, 1, 1, 2)

        self.settings_import.setLayout(wordless_layout.Wordless_Layout())
        self.settings_import.layout().addWidget(group_box_import_files, 0, 0)
        self.settings_import.layout().addWidget(group_box_import_search_terms, 1, 0)
        self.settings_import.layout().addWidget(group_box_import_stop_words, 2, 0)
        self.settings_import.layout().addWidget(group_box_import_temp_files, 3, 0)

        self.settings_import.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_import.layout().setRowStretch(4, 1)

    # Export
    def init_settings_export(self):
        def tables_default_type_changed():
            if self.combo_box_export_tables_default_type.currentText() == self.tr('Excel Workbook (*.xlsx)'):
                self.combo_box_export_tables_default_encoding.setEnabled(False)
            else:
                self.combo_box_export_tables_default_encoding.setEnabled(True)

        def browse_tables():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['export']['tables']['default_path'])

            if path_file:
                self.line_edit_export_tables_default_path.setText(wordless_misc.get_normalized_path(path_file))

        def browse_search_terms():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['export']['search_terms']['default_path'])

            if path_file:
                self.line_edit_export_search_terms_default_path.setText(wordless_misc.get_normalized_path(path_file))

        def browse_stop_words():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['export']['stop_words']['default_path'])

            if path_file:
                self.line_edit_export_stop_words_default_path.setText(wordless_misc.get_normalized_path(path_file))

        self.settings_export = QWidget(self)

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

        self.button_export_tables_default_path.clicked.connect(browse_tables)
        self.combo_box_export_tables_default_type.currentTextChanged.connect(tables_default_type_changed)

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

        self.button_export_search_terms_default_path.clicked.connect(browse_search_terms)

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

        self.button_export_stop_words_default_path.clicked.connect(browse_stop_words)

        group_box_export_stop_words.setLayout(wordless_layout.Wordless_Layout())
        group_box_export_stop_words.layout().addWidget(self.label_export_stop_words_default_path, 0, 0)
        group_box_export_stop_words.layout().addWidget(self.line_edit_export_stop_words_default_path, 0, 1)
        group_box_export_stop_words.layout().addWidget(self.button_export_stop_words_default_path, 0, 2)
        group_box_export_stop_words.layout().addWidget(self.label_export_stop_words_default_encoding, 1, 0)
        group_box_export_stop_words.layout().addWidget(self.combo_box_export_stop_words_default_encoding, 1, 1, 1, 2)

        self.settings_export.setLayout(wordless_layout.Wordless_Layout())
        self.settings_export.layout().addWidget(group_box_export_tables, 0, 0)
        self.settings_export.layout().addWidget(group_box_export_search_terms, 1, 0)
        self.settings_export.layout().addWidget(group_box_export_stop_words, 2, 0)

        self.settings_export.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_export.layout().setRowStretch(3, 1)

        tables_default_type_changed()

    # Auto-detection
    def init_settings_auto_detection(self):
        self.settings_auto_detection = QWidget(self)

        # Detection Settings
        group_box_detection_settings = QGroupBox(self.tr('Detection Settings'), self)

        self.label_auto_detection_number_lines = QLabel(self.tr('Number of lines to scan in each file:'), self)
        (self.spin_box_auto_detection_number_lines,
         self.checkbox_auto_detection_number_lines_no_limit) = wordless_widgets.wordless_widgets_no_limit(self)

        self.spin_box_auto_detection_number_lines.setRange(1, 1000000)

        group_box_detection_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_detection_settings.layout().addWidget(self.label_auto_detection_number_lines, 0, 0)
        group_box_detection_settings.layout().addWidget(self.spin_box_auto_detection_number_lines, 0, 1)
        group_box_detection_settings.layout().addWidget(self.checkbox_auto_detection_number_lines_no_limit, 0, 2)

        group_box_detection_settings.layout().setColumnStretch(3, 1)

        # Default Settings
        group_box_default_settings = QGroupBox(self.tr('Default Settings'), self)

        self.label_auto_detection_default_lang = QLabel(self.tr('Default Language:'), self)
        self.combo_box_auto_detection_default_lang = wordless_box.Wordless_Combo_Box_Lang(self)
        self.label_auto_detection_default_text_type = QLabel(self.tr('Default Text Type:'), self)
        self.combo_box_auto_detection_default_text_type = wordless_box.Wordless_Combo_Box_Text_Type(self)
        self.label_auto_detection_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_auto_detection_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self)

        group_box_default_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_default_settings.layout().addWidget(self.label_auto_detection_default_lang, 0, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_auto_detection_default_lang, 0, 1)
        group_box_default_settings.layout().addWidget(self.label_auto_detection_default_text_type, 1, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_auto_detection_default_text_type, 1, 1)
        group_box_default_settings.layout().addWidget(self.label_auto_detection_default_encoding, 2, 0)
        group_box_default_settings.layout().addWidget(self.combo_box_auto_detection_default_encoding, 2, 1)

        group_box_default_settings.layout().setColumnStretch(3, 1)

        self.settings_auto_detection.setLayout(wordless_layout.Wordless_Layout())
        self.settings_auto_detection.layout().addWidget(group_box_detection_settings, 0, 0)
        self.settings_auto_detection.layout().addWidget(group_box_default_settings, 1, 0)

        self.settings_auto_detection.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_auto_detection.layout().setRowStretch(2, 1)

    # Data
    def init_settings_data(self):
        self.settings_data = QWidget(self)

        # Precision Settings
        group_box_precision_settings = QGroupBox(self.tr('Precision Settings'), self)

        self.label_precision_decimal = QLabel(self.tr('Decimal:'), self)
        self.spin_box_precision_decimal = wordless_box.Wordless_Spin_Box(self)
        self.label_precision_pct = QLabel(self.tr('Percentage:'), self)
        self.spin_box_precision_pct = wordless_box.Wordless_Spin_Box(self)
        self.label_precision_p_value = QLabel(self.tr('p-value:'), self)
        self.spin_box_precision_p_value = wordless_box.Wordless_Spin_Box(self)

        self.spin_box_precision_decimal.setRange(0, 10)
        self.spin_box_precision_pct.setRange(0, 10)
        self.spin_box_precision_p_value.setRange(0, 15)

        group_box_precision_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_precision_settings.layout().addWidget(self.label_precision_decimal, 0, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_decimal, 0, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_pct, 1, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_pct, 1, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_p_value, 2, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_p_value, 2, 1)

        group_box_precision_settings.layout().setColumnStretch(2, 1)

        self.settings_data.setLayout(wordless_layout.Wordless_Layout())
        self.settings_data.layout().addWidget(group_box_precision_settings, 0, 0)

        self.settings_data.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_data.layout().setRowStretch(1, 1)

    # Tags
    def init_settings_tags(self):
        self.settings_tags = QWidget(self)

        # POS Tag Settings
        group_box_pos_tag_settings = QGroupBox(self.tr('POS Tag Settings'), self)

        self.table_tags_pos = Wordless_Table_Tags_Pos(self)

        group_box_pos_tag_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos, 0, 0, 1, 3)
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos.button_add, 1, 0)
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos.button_remove, 1, 1)
        group_box_pos_tag_settings.layout().addWidget(self.table_tags_pos.button_reset, 1, 2)

        # Non-POS Tag Settings
        group_box_non_pos_tag_settings = QGroupBox(self.tr('Non-POS Tag Settings'), self)

        self.table_tags_non_pos = Wordless_Table_Tags_Non_Pos(self)

        group_box_non_pos_tag_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos, 0, 0, 1, 3)
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos.button_add, 1, 0)
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos.button_remove, 1, 1)
        group_box_non_pos_tag_settings.layout().addWidget(self.table_tags_non_pos.button_reset, 1, 2)

        self.settings_tags.setLayout(wordless_layout.Wordless_Layout())
        self.settings_tags.layout().addWidget(group_box_pos_tag_settings, 0, 0)
        self.settings_tags.layout().addWidget(group_box_non_pos_tag_settings, 1, 0)

        self.settings_tags.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_tags.layout().setRowStretch(2, 1)

    # Sentence Tokenization
    def init_settings_sentence_tokenization(self):
        def sentence_tokenizers_changed(lang):
            if lang == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_sentence_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_sentence_tokenization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_sentence_tokenization_preview_results.toPlainText()

        def preview_results_changed():
            if settings_custom['preview_samples']:
                if self.combo_box_sentence_tokenization_preview_lang.isEnabled():
                    self.__dict__[f"combo_box_sentence_tokenizer_{settings_custom['preview_lang']}"].setEnabled(False)
                    self.combo_box_sentence_tokenization_preview_lang.setEnabled(False)

                    self.label_sentence_tokenization_preview_processing.show()

                    sentence_tokenizer = self.__dict__[f"combo_box_sentence_tokenizer_{settings_custom['preview_lang']}"].currentText()

                    worker_preview_sentence_tokenizer = Wordless_Worker_Preview_Sentence_Tokenizer(
                        self.main,
                        update_gui = update_gui,
                        sentence_tokenizer = sentence_tokenizer
                    )

                    self.thread_preview_sentence_tokenizer = wordless_threading.Wordless_Thread_No_Progress(worker_preview_sentence_tokenizer)
                    self.thread_preview_sentence_tokenizer.start_worker()
            else:
                self.text_edit_sentence_tokenization_preview_results.clear()

        def update_gui(preview_samples, preview_results):
            self.label_sentence_tokenization_preview_processing.hide()

            self.__dict__[f"combo_box_sentence_tokenizer_{settings_custom['preview_lang']}"].setEnabled(True)
            self.combo_box_sentence_tokenization_preview_lang.setEnabled(True)

            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_sentence_tokenization_preview_results.setPlainText('\n'.join(preview_results))
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['sentence_tokenizers']
        settings_custom = self.main.settings_custom['sentence_tokenization']

        self.settings_sentence_tokenization = QWidget(self)

        # Sentence Tokenizer Settings
        group_box_sentence_tokenizer_settings = QGroupBox(self.tr('Sentence Tokenizer Settings'), self)

        table_sentence_tokenizers = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Sentence Tokenizers')
            ],
            cols_stretch = [
                self.tr('Sentence Tokenizers')
            ]
        )

        table_sentence_tokenizers.verticalHeader().setHidden(True)

        table_sentence_tokenizers.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            table_sentence_tokenizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_sentence_tokenizer_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_sentence_tokenizer_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_sentence_tokenizer_{lang}'].currentTextChanged.connect(lambda text, lang = lang: sentence_tokenizers_changed(lang))

            table_sentence_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_sentence_tokenizer_{lang}'])

        group_box_sentence_tokenizer_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_sentence_tokenizer_settings.layout().addWidget(table_sentence_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_sentence_tokenization_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_sentence_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_sentence_tokenization_preview_processing = QLabel(self.tr('Processing text ...'))
        self.text_edit_sentence_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_sentence_tokenization_preview_results = QTextEdit(self)

        self.combo_box_sentence_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.label_sentence_tokenization_preview_processing.hide()

        self.text_edit_sentence_tokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_sentence_tokenization_preview_results.setReadOnly(True)

        self.combo_box_sentence_tokenization_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_sentence_tokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_sentence_tokenization_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_sentence_tokenization_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_sentence_tokenization_preview_results.textChanged.connect(preview_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_sentence_tokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_sentence_tokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_sentence_tokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_sentence_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_sentence_tokenization_preview_results, 1, 1)

        self.settings_sentence_tokenization.setLayout(wordless_layout.Wordless_Layout())
        self.settings_sentence_tokenization.layout().addWidget(group_box_sentence_tokenizer_settings, 0, 0)
        self.settings_sentence_tokenization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_sentence_tokenization.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_sentence_tokenization.layout().setRowStretch(0, 3)
        self.settings_sentence_tokenization.layout().setRowStretch(1, 2)

    # Word Tokenization
    def init_settings_word_tokenization(self):
        def word_tokenizers_changed(lang):
            if lang == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_tokenization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_word_tokenization_preview_results.toPlainText()

        def preview_results_changed():
            if settings_custom['preview_samples']:
                if self.combo_box_word_tokenization_preview_lang.isEnabled():
                    self.__dict__[f"combo_box_word_tokenizer_{settings_custom['preview_lang']}"].setEnabled(False)
                    self.combo_box_word_tokenization_preview_lang.setEnabled(False)

                    self.label_word_tokenization_preview_processing.setText(self.tr('Processing text ...'))

                    word_tokenizer = self.__dict__[f"combo_box_word_tokenizer_{settings_custom['preview_lang']}"].currentText()

                    worker_preview_word_tokenizer = Wordless_Worker_Preview_Word_Tokenizer(
                        self.main,
                        update_gui = update_gui,
                        word_tokenizer = word_tokenizer
                    )

                    self.thread_preview_word_tokenizer = wordless_threading.Wordless_Thread_No_Progress(worker_preview_word_tokenizer)
                    self.thread_preview_word_tokenizer.start_worker()
            else:
                self.text_edit_word_tokenization_preview_results.clear()

        def update_gui(preview_samples, preview_results):
            self.label_word_tokenization_preview_processing.setText('')

            self.__dict__[f"combo_box_word_tokenizer_{settings_custom['preview_lang']}"].setEnabled(True)
            self.combo_box_word_tokenization_preview_lang.setEnabled(True)

            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_word_tokenization_preview_results.setPlainText('\n'.join(preview_results))
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['word_tokenizers']
        settings_custom = self.main.settings_custom['word_tokenization']

        self.settings_word_tokenization = QWidget(self)

        # Word Tokenizer Settings
        group_box_word_tokenizer_settings = QGroupBox(self.tr('Word Tokenizer Settings'), self)

        table_word_tokenizers = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Word Tokenizers')
            ],
            cols_stretch = [
                self.tr('Word Tokenizers')
            ]
        )

        table_word_tokenizers.verticalHeader().setHidden(True)

        table_word_tokenizers.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            table_word_tokenizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_word_tokenizer_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_word_tokenizer_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_word_tokenizer_{lang}'].currentTextChanged.connect(lambda text, lang = lang: word_tokenizers_changed(lang))

            table_word_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_word_tokenizer_{lang}'])

        group_box_word_tokenizer_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_word_tokenizer_settings.layout().addWidget(table_word_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_tokenization_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_word_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_word_tokenization_preview_processing = QLabel('', self)
        self.text_edit_word_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_word_tokenization_preview_results = QTextEdit(self)

        self.combo_box_word_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_word_tokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_word_tokenization_preview_results.setReadOnly(True)

        self.combo_box_word_tokenization_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_word_tokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_word_tokenization_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_word_tokenization_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_word_tokenization_preview_results.textChanged.connect(preview_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_word_tokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_word_tokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_word_tokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_results, 1, 1)

        self.settings_word_tokenization.setLayout(wordless_layout.Wordless_Layout())
        self.settings_word_tokenization.layout().addWidget(group_box_word_tokenizer_settings, 0, 0,)
        self.settings_word_tokenization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_word_tokenization.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_word_tokenization.layout().setRowStretch(0, 3)
        self.settings_word_tokenization.layout().setRowStretch(1, 2)

    # Word Detokenization
    def init_settings_word_detokenization(self):
        def word_detokenizers_changed(lang):
            if lang == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_detokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_detokenization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_word_detokenization_preview_results.toPlainText()

        def preview_results_changed():
            if settings_custom['preview_samples']:
                if self.combo_box_word_detokenization_preview_lang.isEnabled():
                    self.__dict__[f"combo_box_word_detokenizer_{settings_custom['preview_lang']}"].setEnabled(False)
                    self.combo_box_word_detokenization_preview_lang.setEnabled(False)

                    self.label_word_detokenization_preview_processing.setText(self.tr('Processing text ...'))

                    word_detokenizer = self.__dict__[f"combo_box_word_detokenizer_{settings_custom['preview_lang']}"].currentText()

                    worker_preview_word_detokenizer = Wordless_Worker_Preview_Word_Detokenizer(
                        self.main,
                        update_gui = update_gui,
                        word_detokenizer = word_detokenizer
                    )

                    self.thread_preview_word_detokenizer = wordless_threading.Wordless_Thread_No_Progress(worker_preview_word_detokenizer)
                    self.thread_preview_word_detokenizer.start_worker()
            else:
                self.text_edit_word_detokenization_preview_results.clear()

        def update_gui(preview_samples, preview_results):
            self.label_word_detokenization_preview_processing.setText('')

            self.__dict__[f"combo_box_word_detokenizer_{settings_custom['preview_lang']}"].setEnabled(True)
            self.combo_box_word_detokenization_preview_lang.setEnabled(True)

            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_word_detokenization_preview_results.setPlainText('\n'.join(preview_results))
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['word_detokenizers']
        settings_custom = self.main.settings_custom['word_detokenization']

        self.settings_word_detokenization = QWidget(self)

        # Word Detokenizer Settings
        group_box_word_detokenizer_settings = QGroupBox(self.tr('Word Detokenizer Settings'), self)

        table_word_detokenizers = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Word Detokenizers')
            ],
            cols_stretch = [
                self.tr('Word Detokenizers')
            ]
        )

        table_word_detokenizers.verticalHeader().setHidden(True)

        table_word_detokenizers.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            table_word_detokenizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_word_detokenizer_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_word_detokenizer_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_word_detokenizer_{lang}'].currentTextChanged.connect(lambda text, lang = lang: word_detokenizers_changed(lang))

            table_word_detokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_word_detokenizer_{lang}'])

        group_box_word_detokenizer_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_word_detokenizer_settings.layout().addWidget(table_word_detokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_detokenization_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_word_detokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_word_detokenization_preview_processing = QLabel('', self)
        self.text_edit_word_detokenization_preview_samples = QTextEdit(self)
        self.text_edit_word_detokenization_preview_results = QTextEdit(self)

        self.combo_box_word_detokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_word_detokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_word_detokenization_preview_results.setReadOnly(True)

        self.combo_box_word_detokenization_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_word_detokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_word_detokenization_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_word_detokenization_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_word_detokenization_preview_results.textChanged.connect(preview_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_word_detokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_word_detokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_word_detokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_word_detokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_detokenization_preview_results, 1, 1)

        self.settings_word_detokenization.setLayout(wordless_layout.Wordless_Layout())
        self.settings_word_detokenization.layout().addWidget(group_box_word_detokenizer_settings, 0, 0,)
        self.settings_word_detokenization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_word_detokenization.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_word_detokenization.layout().setRowStretch(0, 3)
        self.settings_word_detokenization.layout().setRowStretch(1, 2)

    # POS Tagging
    def init_settings_pos_tagging(self):
        def pos_taggers_changed(lang):
            if lang == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_pos_tagging_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_pos_tagging_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_pos_tagging_preview_results.toPlainText()

        def preview_results_changed():
            if settings_custom['preview_samples']:
                if self.combo_box_pos_tagging_preview_lang.isEnabled():
                    self.__dict__[f"combo_box_pos_tagger_{settings_custom['preview_lang']}"].setEnabled(False)
                    self.combo_box_pos_tagging_preview_lang.setEnabled(False)

                    self.label_pos_tagging_preview_processing.setText(self.tr('Processing text ...'))

                    pos_tagger = self.__dict__[f"combo_box_pos_tagger_{settings_custom['preview_lang']}"].currentText()

                    if self.checkbox_to_universal_pos_tags.isChecked():
                        tagset = 'universal'
                    else:
                        tagset = 'default'

                    worker_preview_pos_tagger = Wordless_Worker_Preview_Pos_Tagger(
                        self.main,
                        update_gui = update_gui,
                        pos_tagger = pos_tagger,
                        tagset = tagset
                    )

                    self.thread_preview_pos_tagger = wordless_threading.Wordless_Thread_No_Progress(worker_preview_pos_tagger)
                    self.thread_preview_pos_tagger.start_worker()
            else:
                self.text_edit_pos_tagging_preview_results.clear()

        def update_gui(preview_samples, preview_results):
            self.label_pos_tagging_preview_processing.setText('')

            self.__dict__[f"combo_box_pos_tagger_{settings_custom['preview_lang']}"].setEnabled(True)
            self.combo_box_pos_tagging_preview_lang.setEnabled(True)

            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_pos_tagging_preview_results.setPlainText('\n'.join(preview_results))
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['pos_taggers']
        settings_custom = self.main.settings_custom['pos_tagging']

        self.settings_pos_tagging = QWidget(self)

        # POS Tagger Settings
        group_box_pos_tagger_settings = QGroupBox(self.tr('POS Tagger Settings'), self)

        self.table_pos_taggers = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('POS Taggers')
            ],
            cols_stretch = [
                self.tr('POS Taggers')
            ]
        )

        self.checkbox_to_universal_pos_tags = QCheckBox(self.tr('Convert all POS tags to universal POS tags'))

        self.table_pos_taggers.verticalHeader().setHidden(True)

        self.table_pos_taggers.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            self.table_pos_taggers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_pos_tagger_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_pos_tagger_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_pos_tagger_{lang}'].currentTextChanged.connect(lambda text, lang = lang: pos_taggers_changed(lang))

            self.table_pos_taggers.setCellWidget(i, 1, self.__dict__[f'combo_box_pos_tagger_{lang}'])

        self.checkbox_to_universal_pos_tags.stateChanged.connect(preview_results_changed)

        group_box_pos_tagger_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_pos_tagger_settings.layout().addWidget(self.table_pos_taggers, 0, 0)
        group_box_pos_tagger_settings.layout().addWidget(self.checkbox_to_universal_pos_tags, 1, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_pos_tagging_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_pos_tagging_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_pos_tagging_preview_processing = QLabel('', self)
        self.text_edit_pos_tagging_preview_samples = QTextEdit(self)
        self.text_edit_pos_tagging_preview_results = QTextEdit(self)

        self.combo_box_pos_tagging_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global)))

        self.text_edit_pos_tagging_preview_samples.setAcceptRichText(False)
        self.text_edit_pos_tagging_preview_results.setReadOnly(True)

        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_pos_tagging_preview_results.textChanged.connect(preview_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_pos_tagging_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_pos_tagging_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_pos_tagging_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_results, 1, 1)

        self.settings_pos_tagging.setLayout(wordless_layout.Wordless_Layout())
        self.settings_pos_tagging.layout().addWidget(group_box_pos_tagger_settings, 0, 0)
        self.settings_pos_tagging.layout().addWidget(group_box_preview, 1, 0)

        self.settings_pos_tagging.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_pos_tagging.layout().setRowStretch(0, 3)
        self.settings_pos_tagging.layout().setRowStretch(1, 2)

    # POS Tagging -> Tagsets
    def init_settings_tagsets(self):
        def preview_lang_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(
                self.main,
                self.combo_box_tagsets_lang.currentText()
            )

            preview_lang = settings_custom['preview_lang']

            self.combo_box_tagsets_pos_tagger.blockSignals(True)

            self.combo_box_tagsets_pos_tagger.clear()

            self.combo_box_tagsets_pos_tagger.addItems(settings_global[preview_lang])
            self.combo_box_tagsets_pos_tagger.setCurrentText(settings_custom['preview_pos_tagger'][preview_lang])

            self.combo_box_tagsets_pos_tagger.blockSignals(False)

            self.combo_box_tagsets_pos_tagger.currentTextChanged.emit('')

        def preview_pos_tagger_changed():
            def update_gui(mappings):
                self.table_mappings.hide()
                self.table_mappings.blockSignals(True)
                self.table_mappings.setUpdatesEnabled(False)

                self.table_mappings.clear_table()
                self.table_mappings.setRowCount(len(mappings))

                for i, (tag, tag_universal, description, examples) in enumerate(mappings):
                    combo_box_tag_univsersal = wordless_box.Wordless_Combo_Box(self.main)

                    combo_box_tag_univsersal.addItems([
                        'ADJ',
                        'ADP',
                        'ADV',
                        'AUX',
                        'CONJ', # Coordinating/Subordinating Conjunctions
                        'CCONJ',
                        'SCONJ',
                        'DET',
                        'INTJ',
                        'NOUN',
                        'PROPN',
                        'NUM',
                        'PART',
                        'PRON',
                        'VERB',

                        'PUNCT',
                        'SYM',
                        'X'
                    ])

                    combo_box_tag_univsersal.setCurrentText(tag_universal)
                    combo_box_tag_univsersal.setEditable(True)

                    self.table_mappings.setItem(i, 0, QTableWidgetItem(tag))
                    self.table_mappings.setCellWidget(i, 1, combo_box_tag_univsersal)
                    self.table_mappings.setItem(i, 2, QTableWidgetItem(description))
                    self.table_mappings.setItem(i, 3, QTableWidgetItem(examples))

                self.table_mappings.blockSignals(False)
                self.table_mappings.setUpdatesEnabled(True)
                self.table_mappings.show()

                self.table_mappings.itemChanged.emit(self.table_mappings.item(0, 0))

                # Disable editing if the default tagset is Universal POS tags
                if mappings == wordless_tagset_universal.mappings:
                    for i in range(self.table_mappings.rowCount()):
                        self.table_mappings.cellWidget(i, 1).setEnabled(False)

                self.label_tagsets_num_pos_tags.setText(self.tr(f'Number of POS Tags: {self.table_mappings.rowCount()}'))

                self.combo_box_tagsets_lang.setEnabled(True)
                self.combo_box_tagsets_pos_tagger.setEnabled(True)
                self.button_tagsets_reset.setEnabled(True)
                self.button_tagsets_reset_all.setEnabled(True)

            settings_custom['preview_pos_tagger'][settings_custom['preview_lang']] = self.combo_box_tagsets_pos_tagger.currentText()

            self.combo_box_tagsets_lang.setEnabled(False)
            self.combo_box_tagsets_pos_tagger.setEnabled(False)
            self.button_tagsets_reset.setEnabled(False)
            self.button_tagsets_reset_all.setEnabled(False)

            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Fetch_Data(self.main)

            worker_fetch_data = Wordless_Worker_Fetch_Data_Tagsets(
                self.main,
                dialog_progress = dialog_progress,
                update_gui = update_gui
            )

            thread_fetch_data = wordless_threading.Wordless_Thread(worker_fetch_data)
            thread_fetch_data.start()

            dialog_progress.show()
            dialog_progress.raise_()

            thread_fetch_data.quit()
            thread_fetch_data.wait()

        def reset_currently_shown_table():
            preview_lang = settings_custom['preview_lang']
            preview_pos_tagger = settings_custom['preview_pos_tagger'][preview_lang]
            mappings = copy.deepcopy(self.main.settings_default['tagsets']['mappings'][preview_lang][preview_pos_tagger])

            self.table_mappings.hide()
            self.table_mappings.blockSignals(True)
            self.table_mappings.setUpdatesEnabled(False)

            for i in range(self.table_mappings.rowCount()):
                self.table_mappings.cellWidget(i, 1).setCurrentText(mappings[i][1])

            self.table_mappings.blockSignals(False)
            self.table_mappings.setUpdatesEnabled(True)
            self.table_mappings.show()

            self.table_mappings.itemChanged.emit(self.table_mappings.item(0, 0))

            settings_custom['mappings'][preview_lang][preview_pos_tagger] = mappings

        def reset_mappings():
            if wordless_msg_box.wordless_msg_box_reset_mappings(self.main):
                reset_currently_shown_table()

        def reset_all_mappings():
            if wordless_msg_box.wordless_msg_box_reset_all_mappings(self.main):
                settings_custom['mappings'] = copy.deepcopy(self.main.settings_default['tagsets']['mappings'])

                reset_currently_shown_table()

        settings_global = self.main.settings_global['pos_taggers']
        settings_custom = self.main.settings_custom['tagsets']

        self.settings_tagsets = QWidget(self)

        # Preview Settings
        group_box_preview_settings = QGroupBox(self.tr('Preview Settings:'), self)

        self.label_tagsets_lang = QLabel(self.tr('Language:'), self)
        self.combo_box_tagsets_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_tagsets_pos_tagger = QLabel(self.tr('POS Tagger:'), self)
        self.combo_box_tagsets_pos_tagger = wordless_box.Wordless_Combo_Box_Adjustable(self)

        self.combo_box_tagsets_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global)))

        self.combo_box_tagsets_lang.currentTextChanged.connect(preview_lang_changed)
        self.combo_box_tagsets_pos_tagger.currentTextChanged.connect(preview_pos_tagger_changed)

        group_box_preview_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview_settings.layout().addWidget(self.label_tagsets_lang, 0, 0)
        group_box_preview_settings.layout().addWidget(self.combo_box_tagsets_lang, 0, 1, Qt.AlignLeft)
        group_box_preview_settings.layout().addWidget(self.label_tagsets_pos_tagger, 1, 0)
        group_box_preview_settings.layout().addWidget(self.combo_box_tagsets_pos_tagger, 1, 1, Qt.AlignLeft)

        group_box_preview_settings.layout().setColumnStretch(2, 1)

        # Mapping Settings
        group_box_mapping_settings = QGroupBox(self.tr('Mapping Settings'))

        self.label_tagsets_num_pos_tags = QLabel('', self)
        self.button_tagsets_reset = QPushButton(self.tr('Reset'), self)
        self.button_tagsets_reset_all = QPushButton(self.tr('Reset All'), self)
        self.table_mappings = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('POS Tag'),
                self.tr('Universal POS Tag'),
                self.tr('Description'),
                self.tr('Examples')
            ]
        )

        self.button_tagsets_reset.setFixedWidth(100)
        self.button_tagsets_reset_all.setFixedWidth(100)

        self.button_tagsets_reset.clicked.connect(reset_mappings)
        self.button_tagsets_reset_all.clicked.connect(reset_all_mappings)

        group_box_mapping_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_mapping_settings.layout().addWidget(self.label_tagsets_num_pos_tags, 0, 0)
        group_box_mapping_settings.layout().addWidget(self.button_tagsets_reset, 0, 2)
        group_box_mapping_settings.layout().addWidget(self.button_tagsets_reset_all, 0, 3)
        group_box_mapping_settings.layout().addWidget(self.table_mappings, 1, 0, 1, 4)

        group_box_mapping_settings.layout().setColumnStretch(1, 1)

        self.settings_tagsets.setLayout(wordless_layout.Wordless_Layout())
        self.settings_tagsets.layout().addWidget(group_box_preview_settings, 0, 0)
        self.settings_tagsets.layout().addWidget(group_box_mapping_settings, 1, 0)

        self.settings_tagsets.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_tagsets.layout().setRowStretch(1, 1)

    # Lemmatization
    def init_settings_lemmatization(self):
        def lemmatizers_changed(lang):
            if lang == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_lemmatization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_lemmatization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_lemmatization_preview_results.toPlainText()

        def preview_results_changed():
            if settings_custom['preview_samples']:
                if self.combo_box_lemmatization_preview_lang.isEnabled():
                    self.__dict__[f"combo_box_lemmatizer_{settings_custom['preview_lang']}"].setEnabled(False)
                    self.combo_box_lemmatization_preview_lang.setEnabled(False)

                    self.label_lemmatization_preview_processing.setText(self.tr('Processing text ...'))

                    lemmatizer = self.__dict__[f"combo_box_lemmatizer_{settings_custom['preview_lang']}"].currentText()

                    worker_preview_lemmatizer = Wordless_Worker_Preview_Lemmatizer(
                        self.main,
                        update_gui = update_gui,
                        lemmatizer = lemmatizer
                    )

                    self.thread_preview_lemmatizer = wordless_threading.Wordless_Thread_No_Progress(worker_preview_lemmatizer)
                    self.thread_preview_lemmatizer.start_worker()
            else:
                self.text_edit_lemmatization_preview_results.clear()

        def update_gui(preview_samples, preview_results):
            self.label_lemmatization_preview_processing.setText('')

            self.__dict__[f"combo_box_lemmatizer_{settings_custom['preview_lang']}"].setEnabled(True)
            self.combo_box_lemmatization_preview_lang.setEnabled(True)

            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_lemmatization_preview_results.setPlainText('\n'.join(preview_results))
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['lemmatizers']
        settings_custom = self.main.settings_custom['lemmatization']

        self.settings_lemmatization = QWidget(self)

        # Lemmatizer Settings
        group_box_lemmatizer_settings = QGroupBox(self.tr('Lemmatizer Settings'), self)

        table_lemmatizers = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Lemmatizers')
            ],
            cols_stretch = [
                self.tr('Lemmatizers')
            ]
        )

        table_lemmatizers.verticalHeader().setHidden(True)

        table_lemmatizers.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            table_lemmatizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_lemmatizer_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_lemmatizer_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_lemmatizer_{lang}'].currentTextChanged.connect(lambda text, lang = lang: lemmatizers_changed(lang))

            table_lemmatizers.setCellWidget(i, 1, self.__dict__[f'combo_box_lemmatizer_{lang}'])

        group_box_lemmatizer_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_lemmatizer_settings.layout().addWidget(table_lemmatizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_lemmatization_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_lemmatization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_lemmatization_preview_processing = QLabel('', self)
        self.text_edit_lemmatization_preview_samples = QTextEdit(self)
        self.text_edit_lemmatization_preview_results = QTextEdit(self)

        self.combo_box_lemmatization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_lemmatization_preview_samples.setAcceptRichText(False)
        self.text_edit_lemmatization_preview_results.setReadOnly(True)

        self.combo_box_lemmatization_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_lemmatization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_lemmatization_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_lemmatization_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_lemmatization_preview_results.textChanged.connect(preview_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_lemmatization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_lemmatization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_lemmatization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_results, 1, 1)

        self.settings_lemmatization.setLayout(wordless_layout.Wordless_Layout())
        self.settings_lemmatization.layout().addWidget(group_box_lemmatizer_settings, 0, 0)
        self.settings_lemmatization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_lemmatization.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_lemmatization.layout().setRowStretch(0, 3)
        self.settings_lemmatization.layout().setRowStretch(1, 2)

    # Stop words
    def init_settings_stop_words(self):
        def stop_words_changed(lang):
            if lang == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_stop_words_preview_lang.currentText())

        def preview_results_changed():
            lang = wordless_conversion.to_lang_code(self.main, self.combo_box_stop_words_preview_lang.currentText())
            list_stop_words = self.__dict__[f'combo_box_stop_words_{lang}'].currentText()
            
            stop_words = wordless_text_processing.wordless_get_stop_words(self.main, lang, list_stop_words = list_stop_words)

            self.list_stop_words_preview_results.load_stop_words(stop_words)
            self.label_stop_words_preview_count.setText(self.tr(f'Count of Stop Words: {len(stop_words)}'))

            if list_stop_words == self.tr('Custom List'):
                self.list_stop_words_preview_results.switch_to_custom()

                self.list_stop_words_preview_results.itemChanged.connect(lambda: self.label_stop_words_preview_count.setText(self.tr(f'Count of Stop Words: {self.list_stop_words_preview_results.count()}')))
            else:
                self.list_stop_words_preview_results.switch_to_default()

        settings_global = self.main.settings_global['stop_words']
        settings_custom = self.main.settings_custom['stop_words']

        self.settings_stop_words = QWidget(self)

        # Stop Words Settings
        group_box_stop_words_settings = QGroupBox(self.tr('Stop Words Settings'), self)

        table_stop_words = wordless_table.Wordless_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Lists of Stop Words')
            ],
            cols_stretch = [
                self.tr('Lists of Stop Words')
            ]
        )

        table_stop_words.verticalHeader().setHidden(True)

        table_stop_words.setRowCount(len(settings_global))

        for i, lang in enumerate(settings_global):
            table_stop_words.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_stop_words_{lang}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_stop_words_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_stop_words_{lang}'].currentTextChanged.connect(lambda text, lang = lang: stop_words_changed(lang))

            table_stop_words.setCellWidget(i, 1, self.__dict__[f'combo_box_stop_words_{lang}'])

        group_box_stop_words_settings.setLayout(wordless_layout.Wordless_Layout())
        group_box_stop_words_settings.layout().addWidget(table_stop_words, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_stop_words_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_stop_words_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.combo_box_stop_words_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))
        self.label_stop_words_preview_count = QLabel('', self)

        self.list_stop_words_preview_results = wordless_list.Wordless_List_Stop_Words(self)

        self.combo_box_stop_words_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_stop_words_preview_lang.currentTextChanged.connect(preview_results_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_stop_words_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_stop_words_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_stop_words_preview_count, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 5)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results, 1, 0, 1, 5)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_add, 2, 0)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_remove, 2, 1)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_clear, 2, 2)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_import, 2, 3)
        group_box_preview.layout().addWidget(self.list_stop_words_preview_results.button_export, 2, 4)

        self.settings_stop_words.setLayout(wordless_layout.Wordless_Layout())
        self.settings_stop_words.layout().addWidget(group_box_stop_words_settings, 0, 0)
        self.settings_stop_words.layout().addWidget(group_box_preview, 1, 0)

        self.settings_stop_words.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_stop_words.layout().setRowStretch(0, 3)
        self.settings_stop_words.layout().setRowStretch(1, 2)

        preview_results_changed()

    # Measures -> Dispersion
    def init_settings_dispersion(self):
        self.settings_dispersion = QWidget(self)

        # General
        group_box_general = QGroupBox(self.tr('General'), self)

        (self.label_dispersion_divide,
         self.spin_box_dispersion_number_sections,
         self.label_dispersion_sections) = wordless_widgets.wordless_widgets_number_sections(self)

        group_box_general.setLayout(wordless_layout.Wordless_Layout())
        group_box_general.layout().addWidget(self.label_dispersion_divide, 0, 0)
        group_box_general.layout().addWidget(self.spin_box_dispersion_number_sections, 0, 1)
        group_box_general.layout().addWidget(self.label_dispersion_sections, 0, 2)

        group_box_general.layout().setColumnStretch(3, 1)

        self.settings_dispersion.setLayout(wordless_layout.Wordless_Layout())
        self.settings_dispersion.layout().addWidget(group_box_general, 0, 0)

        self.settings_dispersion.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_dispersion.layout().setRowStretch(1, 1)

    # Measures -> Adjusted Frequency
    def init_settings_adjusted_freq(self):
        def use_same_settings_changed():
            if self.checkbox_use_same_settings_dispersion.isChecked():
                self.spin_box_adjusted_freq_number_sections.setEnabled(False)
            else:
                self.spin_box_adjusted_freq_number_sections.setEnabled(True)

        self.settings_adjusted_freq = QWidget(self)

        # General
        group_box_general = QGroupBox(self.tr('General'), self)

        (self.label_adjusted_freq_divide,
         self.spin_box_adjusted_freq_number_sections,
         self.label_adjusted_freq_sections) = wordless_widgets.wordless_widgets_number_sections(self)
        self.checkbox_use_same_settings_dispersion = QCheckBox(self.tr('Use same settings in "Settings -> Measures -> Dispersion"'), self)

        self.checkbox_use_same_settings_dispersion.stateChanged.connect(use_same_settings_changed)

        group_box_general.setLayout(wordless_layout.Wordless_Layout())
        group_box_general.layout().addWidget(self.label_adjusted_freq_divide, 0, 0)
        group_box_general.layout().addWidget(self.spin_box_adjusted_freq_number_sections, 0, 1)
        group_box_general.layout().addWidget(self.label_adjusted_freq_sections, 0, 2)
        group_box_general.layout().addWidget(self.checkbox_use_same_settings_dispersion, 1, 0, 1, 4)

        group_box_general.layout().setColumnStretch(3, 1)

        self.settings_adjusted_freq.setLayout(wordless_layout.Wordless_Layout())
        self.settings_adjusted_freq.layout().addWidget(group_box_general, 0, 0)

        self.settings_adjusted_freq.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_adjusted_freq.layout().setRowStretch(1, 1)

        use_same_settings_changed()

    # Measures -> Statistical Significance
    def init_settings_statistical_significance(self):
        self.settings_statistical_significance = QWidget(self)

        # z-score
        group_box_z_score = QGroupBox(self.tr('z-score'), self)

        (self.label_z_score_direction,
         self.combo_box_z_score_direction) = wordless_widgets.wordless_widgets_direction_2(self)

        group_box_z_score.setLayout(wordless_layout.Wordless_Layout())
        group_box_z_score.layout().addWidget(self.label_z_score_direction, 0, 0)
        group_box_z_score.layout().addWidget(self.combo_box_z_score_direction, 0, 1)

        group_box_z_score.layout().setColumnStretch(2, 1)

        # Student's t-test (Two-sample)
        group_box_students_t_test_2_sample = QGroupBox(self.tr('Student\'s t-test (Two-sample)'), self)

        (self.label_students_t_test_2_sample_divide,
         self.spin_box_students_t_test_2_sample_number_sections,
         self.label_students_t_test_2_sample_sections) = wordless_widgets.wordless_widgets_number_sections(self)

        (self.label_students_t_test_2_sample_use_data,
         self.combo_box_students_t_test_2_sample_use_data) = wordless_widgets.wordless_widgets_use_data_freq(self)
        self.label_students_t_test_2_sample_variances = QLabel(self.tr('Variances:'), self)
        self.combo_box_students_t_test_2_sample_variances = QComboBox(self)
        self.label_welchs_t_test = wordless_label.Wordless_Label_Hint(
            self.tr('''
                <p>
                    * If variances are set to "Unequal", the Welch\'s t-test will be performed instead.
                </p>
            '''), self)

        self.combo_box_students_t_test_2_sample_variances.addItems([
            self.tr('Equal'),
            self.tr('Unequal')
        ])

        layout_students_t_test_2_sample_number_sections = wordless_layout.Wordless_Layout()
        layout_students_t_test_2_sample_number_sections.addWidget(self.label_students_t_test_2_sample_divide, 0, 0)
        layout_students_t_test_2_sample_number_sections.addWidget(self.spin_box_students_t_test_2_sample_number_sections, 0, 1)
        layout_students_t_test_2_sample_number_sections.addWidget(self.label_students_t_test_2_sample_sections, 0, 2)

        layout_students_t_test_2_sample_number_sections.setColumnStretch(3, 1)

        group_box_students_t_test_2_sample.setLayout(wordless_layout.Wordless_Layout())
        group_box_students_t_test_2_sample.layout().addLayout(layout_students_t_test_2_sample_number_sections, 0, 0, 1, 3)
        group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_use_data, 1, 0)
        group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_use_data, 1, 1)
        group_box_students_t_test_2_sample.layout().addWidget(self.label_students_t_test_2_sample_variances, 2, 0)
        group_box_students_t_test_2_sample.layout().addWidget(self.combo_box_students_t_test_2_sample_variances, 2, 1)
        group_box_students_t_test_2_sample.layout().addWidget(self.label_welchs_t_test, 3, 0, 1, 3)

        group_box_students_t_test_2_sample.layout().setColumnStretch(2, 1)

        # Pearson's Chi-squared Test
        group_box_pearsons_chi_squared_test = QGroupBox(self.tr('Pearson\'s Chi-squared Test'), self)

        self.checkbox_pearsons_chi_squared_test_apply_correction = QCheckBox(self.tr('Apply Yates\'s correction for continuity'))

        group_box_pearsons_chi_squared_test.setLayout(wordless_layout.Wordless_Layout())
        group_box_pearsons_chi_squared_test.layout().addWidget(self.checkbox_pearsons_chi_squared_test_apply_correction, 0, 0)

        # Fisher's Exact Test
        group_box_fishers_exact_test = QGroupBox(self.tr('Fisher\'s Exact Test'), self)

        (self.label_fishers_exact_test_direction,
         self.combo_box_fishers_exact_test_direction) = wordless_widgets.wordless_widgets_direction(self)

        group_box_fishers_exact_test.setLayout(wordless_layout.Wordless_Layout())
        group_box_fishers_exact_test.layout().addWidget(self.label_fishers_exact_test_direction, 0, 0)
        group_box_fishers_exact_test.layout().addWidget(self.combo_box_fishers_exact_test_direction, 0, 1)

        group_box_fishers_exact_test.layout().setColumnStretch(2, 1)

        # Mann-Whitney U Test
        group_box_mann_whitney_u_test = QGroupBox(self.tr('Mann-Whitney U Test'), self)

        (self.label_mann_whitney_u_test_divide,
         self.spin_box_mann_whitney_u_test_number_sections,
         self.label_mann_whitney_u_test_sections) = wordless_widgets.wordless_widgets_number_sections(self)

        (self.label_mann_whitney_u_test_use_data,
         self.combo_box_mann_whitney_u_test_use_data) = wordless_widgets.wordless_widgets_use_data_freq(self)
        (self.label_mann_whitney_u_test_direction,
         self.combo_box_mann_whitney_u_test_direction) = wordless_widgets.wordless_widgets_direction(self)
        self.checkbox_mann_whitney_u_test_apply_correction = QCheckBox(self.tr('Apply continuity correction'), self)

        layout_mann_whitney_u_test_number_sections = wordless_layout.Wordless_Layout()
        layout_mann_whitney_u_test_number_sections.addWidget(self.label_mann_whitney_u_test_divide, 0, 0)
        layout_mann_whitney_u_test_number_sections.addWidget(self.spin_box_mann_whitney_u_test_number_sections, 0, 1)
        layout_mann_whitney_u_test_number_sections.addWidget(self.label_mann_whitney_u_test_sections, 0, 2)

        layout_mann_whitney_u_test_number_sections.setColumnStretch(3, 1)

        group_box_mann_whitney_u_test.setLayout(wordless_layout.Wordless_Layout())
        group_box_mann_whitney_u_test.layout().addLayout(layout_mann_whitney_u_test_number_sections, 0, 0, 1, 3)
        group_box_mann_whitney_u_test.layout().addWidget(self.label_mann_whitney_u_test_use_data, 1, 0)
        group_box_mann_whitney_u_test.layout().addWidget(self.combo_box_mann_whitney_u_test_use_data, 1, 1)
        group_box_mann_whitney_u_test.layout().addWidget(self.label_mann_whitney_u_test_direction, 2, 0)
        group_box_mann_whitney_u_test.layout().addWidget(self.combo_box_mann_whitney_u_test_direction, 2, 1)
        group_box_mann_whitney_u_test.layout().addWidget(self.checkbox_mann_whitney_u_test_apply_correction, 3, 0, 1, 3)

        group_box_mann_whitney_u_test.layout().setColumnStretch(3, 1)

        self.settings_statistical_significance.setLayout(wordless_layout.Wordless_Layout())
        self.settings_statistical_significance.layout().addWidget(group_box_z_score, 0, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_students_t_test_2_sample, 1, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_pearsons_chi_squared_test, 2, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_fishers_exact_test, 3, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_mann_whitney_u_test, 4, 0)

        self.settings_statistical_significance.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_statistical_significance.layout().setRowStretch(5, 1)

    # Measures -> Effect Size
    def init_settings_effect_size(self):
        self.settings_effect_size = QWidget(self)

        # Kilgarriff's Ratio
        group_box_kilgarriffs_ratio = QGroupBox(self.tr('Kilgarriff\'s Ratio'), self)

        self.label_kilgarriffs_ratio_smoothing_param = QLabel(self.tr('Smoothing Parameter:'), self)
        self.spin_box_kilgarriffs_ratio_smoothing_param = wordless_box.Wordless_Double_Spin_Box(self)

        self.spin_box_kilgarriffs_ratio_smoothing_param.setRange(0.01, 10000)

        group_box_kilgarriffs_ratio.setLayout(wordless_layout.Wordless_Layout())
        group_box_kilgarriffs_ratio.layout().addWidget(self.label_kilgarriffs_ratio_smoothing_param, 0, 0)
        group_box_kilgarriffs_ratio.layout().addWidget(self.spin_box_kilgarriffs_ratio_smoothing_param, 0, 1)

        group_box_kilgarriffs_ratio.layout().setColumnStretch(2, 1)

        self.settings_effect_size.setLayout(wordless_layout.Wordless_Layout())
        self.settings_effect_size.layout().addWidget(group_box_kilgarriffs_ratio, 0, 0)

        self.settings_effect_size.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_effect_size.layout().setRowStretch(1, 1)

    # Figures
    def init_settings_figs(self):
        self.settings_figs = QWidget(self)

        # Line Chart
        group_box_figs_line_chart = QGroupBox(self.tr('Line Chart'), self)

        self.label_figs_line_chart_font = QLabel(self.tr('Font:'), self)
        self.combo_box_figs_line_chart_font = wordless_box.Wordless_Combo_Box_Font_Family(self)

        group_box_figs_line_chart.setLayout(wordless_layout.Wordless_Layout())
        group_box_figs_line_chart.layout().addWidget(self.label_figs_line_chart_font, 0, 0)
        group_box_figs_line_chart.layout().addWidget(self.combo_box_figs_line_chart_font, 0, 1)

        group_box_figs_line_chart.layout().setColumnStretch(2, 1)

        # Word Cloud
        group_box_figs_word_cloud = QGroupBox(self.tr('Word Cloud'), self)

        self.label_figs_word_cloud_font = QLabel(self.tr('Font:'), self)
        self.combo_box_figs_word_cloud_font = wordless_box.Wordless_Combo_Box(self)
        self.label_figs_word_cloud_bg_color = QLabel(self.tr('Background Color:'), self)
        (self.label_figs_word_cloud_bg_color_pick,
         self.button_figs_word_cloud_bg_color_pick) = wordless_widgets.wordless_widgets_pick_color(self)

        self.combo_box_figs_word_cloud_font.addItems([
            'DroidSansMono',
            'Code2000',
            'Unifont'
        ])

        group_box_figs_word_cloud.setLayout(wordless_layout.Wordless_Layout())
        group_box_figs_word_cloud.layout().addWidget(self.label_figs_word_cloud_font, 0, 0)
        group_box_figs_word_cloud.layout().addWidget(self.combo_box_figs_word_cloud_font, 0, 1, 1, 2)
        group_box_figs_word_cloud.layout().addWidget(self.label_figs_word_cloud_bg_color, 1, 0)
        group_box_figs_word_cloud.layout().addWidget(self.label_figs_word_cloud_bg_color_pick, 1, 1)
        group_box_figs_word_cloud.layout().addWidget(self.button_figs_word_cloud_bg_color_pick, 1, 2)

        group_box_figs_word_cloud.layout().setColumnStretch(3, 1)

        # Network Graph
        group_box_figs_network_graph = QGroupBox(self.tr('Network Graph'), self)

        self.label_figs_network_graph_layout = QLabel(self.tr('Layout:'), self)
        self.combo_box_figs_network_graph_layout = wordless_box.Wordless_Combo_Box(self)
        self.label_figs_network_graph_node_font = QLabel(self.tr('Node Font:'), self)
        self.combo_box_figs_network_graph_node_font = wordless_box.Wordless_Combo_Box_Font_Family(self)
        self.label_figs_network_graph_node_font_size = QLabel(self.tr('Node Font Size:'), self)
        self.spin_box_figs_network_graph_node_font_size = wordless_box.Wordless_Spin_Box_Font_Size(self)
        self.label_figs_network_graph_edge_font = QLabel(self.tr('Edge Font:'), self)
        self.combo_box_figs_network_graph_edge_font = wordless_box.Wordless_Combo_Box_Font_Family(self)
        self.label_figs_network_graph_edge_font_size = QLabel(self.tr('Edge Font Size:'), self)
        self.spin_box_figs_network_graph_edge_font_size = wordless_box.Wordless_Spin_Box_Font_Size(self)
        self.label_figs_network_graph_edge_color = QLabel(self.tr('Edge Color:'), self)
        (self.label_figs_network_graph_edge_color_pick,
         self.combo_box_figs_network_graph_color_pick) = wordless_widgets.wordless_widgets_pick_color(self)

        self.combo_box_figs_network_graph_layout.addItems([
            self.tr('Circular'),
            self.tr('Kamada-Kawai'),
            self.tr('Planar'),
            self.tr('Random'),
            self.tr('Shell'),
            self.tr('Spring'),
            self.tr('Spectral')
        ])

        group_box_figs_network_graph.setLayout(wordless_layout.Wordless_Layout())
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_layout, 0, 0)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_layout, 0, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_node_font, 1, 0)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_node_font, 1, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_node_font_size, 2, 0)
        group_box_figs_network_graph.layout().addWidget(self.spin_box_figs_network_graph_node_font_size, 2, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_font, 3, 0)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_edge_font, 3, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_font_size, 4, 0)
        group_box_figs_network_graph.layout().addWidget(self.spin_box_figs_network_graph_edge_font_size, 4, 1, 1, 2)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_color, 5, 0)
        group_box_figs_network_graph.layout().addWidget(self.label_figs_network_graph_edge_color_pick, 5, 1)
        group_box_figs_network_graph.layout().addWidget(self.combo_box_figs_network_graph_color_pick, 5, 2)

        group_box_figs_network_graph.layout().setColumnStretch(3, 1)

        self.settings_figs.setLayout(wordless_layout.Wordless_Layout())
        self.settings_figs.layout().addWidget(group_box_figs_line_chart, 0, 0)
        self.settings_figs.layout().addWidget(group_box_figs_word_cloud, 1, 0)
        self.settings_figs.layout().addWidget(group_box_figs_network_graph, 2, 0)

        self.settings_figs.layout().setContentsMargins(6, 4, 6, 4)
        self.settings_figs.layout().setRowStretch(3, 1)

    def change_wordcloud_font(self):
        font_dir = os.path.split(wordcloud.wordcloud.FONT_PATH)[0]

        if self.main.settings_custom['figs']['word_cloud']['font'] == 'DroidSansMono':
            wordcloud.wordcloud.FONT_PATH = os.path.join(font_dir, 'DroidSansMono.ttf')
        elif self.main.settings_custom['figs']['word_cloud']['font'] == 'Code2000':
            wordcloud.wordcloud.FONT_PATH = os.path.join(font_dir, 'Code2000.ttf')
        elif self.main.settings_custom['figs']['word_cloud']['font'] == 'Unifont':
            wordcloud.wordcloud.FONT_PATH = os.path.join(font_dir, 'unifont-12.1.03.ttf')

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        # General
        self.combo_box_font_family.setCurrentFont(QFont(settings['general']['font_settings']['font_family']))
        self.combo_box_font_size.set_text(settings['general']['font_settings']['font_size'])

        self.checkbox_check_updates_on_startup.setChecked(settings['general']['update_settings']['check_updates_on_startup'])

        self.checkbox_confirm_on_exit.setChecked(settings['general']['misc']['confirm_on_exit'])

        # Import
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
        self.combo_box_import_temp_files_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['import']['temp_files']['default_encoding']))

        # Export
        self.line_edit_export_tables_default_path.setText(settings['export']['tables']['default_path'])
        self.combo_box_export_tables_default_type.setCurrentText(settings['export']['tables']['default_type'])
        self.combo_box_export_tables_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['export']['tables']['default_encoding']))

        self.line_edit_export_search_terms_default_path.setText(settings['export']['search_terms']['default_path'])
        self.combo_box_export_search_terms_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['export']['search_terms']['default_encoding']))

        self.line_edit_export_stop_words_default_path.setText(settings['export']['stop_words']['default_path'])
        self.combo_box_export_stop_words_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['export']['stop_words']['default_encoding']))

        # Auto-detection
        self.spin_box_auto_detection_number_lines.setValue(settings['auto_detection']['detection_settings']['number_lines'])
        self.checkbox_auto_detection_number_lines_no_limit.setChecked(settings['auto_detection']['detection_settings']['number_lines_no_limit'])

        self.combo_box_auto_detection_default_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['auto_detection']['default_settings']['default_lang']))
        self.combo_box_auto_detection_default_text_type.setCurrentText(wordless_conversion.to_text_type_text(self.main, settings['auto_detection']['default_settings']['default_text_type']))
        self.combo_box_auto_detection_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['auto_detection']['default_settings']['default_encoding']))

        # Data
        self.spin_box_precision_decimal.setValue(settings['data']['precision_decimal'])
        self.spin_box_precision_pct.setValue(settings['data']['precision_pct'])
        self.spin_box_precision_p_value.setValue(settings['data']['precision_p_value'])

        # Tags
        self.table_tags_pos.clear_table(0)

        for tags in settings['tags']['tags_pos']:
            self.table_tags_pos.add_item(texts = tags)

        self.table_tags_non_pos.clear_table(0)

        for tags in settings['tags']['tags_non_pos']:
            self.table_tags_non_pos.add_item(texts = tags)

        # Tokenization -> Sentence Tokenization
        for lang in settings['sentence_tokenization']['sentence_tokenizers']:
            self.__dict__[f'combo_box_sentence_tokenizer_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_sentence_tokenizer_{lang}'].setCurrentText(settings['sentence_tokenization']['sentence_tokenizers'][lang])

            self.__dict__[f'combo_box_sentence_tokenizer_{lang}'].blockSignals(False)

        if not defaults:
            self.combo_box_sentence_tokenization_preview_lang.blockSignals(True)
            self.text_edit_sentence_tokenization_preview_samples.blockSignals(True)

            self.combo_box_sentence_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['sentence_tokenization']['preview_lang']))
            self.text_edit_sentence_tokenization_preview_samples.setText(settings['sentence_tokenization']['preview_samples'])
            self.text_edit_sentence_tokenization_preview_results.setText(settings['sentence_tokenization']['preview_results'])

            self.combo_box_sentence_tokenization_preview_lang.blockSignals(False)
            self.text_edit_sentence_tokenization_preview_samples.blockSignals(False)

        # Tokenization -> Word Tokenization
        for lang in settings['word_tokenization']['word_tokenizers']:
            self.__dict__[f'combo_box_word_tokenizer_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_word_tokenizer_{lang}'].setCurrentText(settings['word_tokenization']['word_tokenizers'][lang])

            self.__dict__[f'combo_box_word_tokenizer_{lang}'].blockSignals(False)

        if not defaults:
            self.combo_box_word_tokenization_preview_lang.blockSignals(True)
            self.text_edit_word_tokenization_preview_samples.blockSignals(True)

            self.combo_box_word_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['word_tokenization']['preview_lang']))
            self.text_edit_word_tokenization_preview_samples.setText(settings['word_tokenization']['preview_samples'])
            self.text_edit_word_tokenization_preview_results.setText(settings['word_tokenization']['preview_results'])

            self.combo_box_word_tokenization_preview_lang.blockSignals(False)
            self.text_edit_word_tokenization_preview_samples.blockSignals(False)

        # Tokenization -> Word Detokenization
        for lang in settings['word_detokenization']['word_detokenizers']:
            self.__dict__[f'combo_box_word_detokenizer_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_word_detokenizer_{lang}'].setCurrentText(settings['word_detokenization']['word_detokenizers'][lang])

            self.__dict__[f'combo_box_word_detokenizer_{lang}'].blockSignals(False)

        if not defaults:
            self.combo_box_word_detokenization_preview_lang.blockSignals(True)
            self.text_edit_word_detokenization_preview_samples.blockSignals(True)

            self.combo_box_word_detokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['word_detokenization']['preview_lang']))
            self.text_edit_word_detokenization_preview_samples.setText(settings['word_detokenization']['preview_samples'])
            self.text_edit_word_detokenization_preview_results.setText(settings['word_detokenization']['preview_results'])

            self.combo_box_word_detokenization_preview_lang.blockSignals(False)
            self.text_edit_word_detokenization_preview_samples.blockSignals(False)

        # POS Tagging
        for lang in settings['pos_tagging']['pos_taggers']:
            self.__dict__[f'combo_box_pos_tagger_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_pos_tagger_{lang}'].setCurrentText(settings['pos_tagging']['pos_taggers'][lang])

            self.__dict__[f'combo_box_pos_tagger_{lang}'].blockSignals(False)

        self.checkbox_to_universal_pos_tags.blockSignals(True)

        self.checkbox_to_universal_pos_tags.setChecked(settings['pos_tagging']['to_universal_pos_tags'])

        self.checkbox_to_universal_pos_tags.blockSignals(False)

        if not defaults:
            self.combo_box_pos_tagging_preview_lang.blockSignals(True)
            self.text_edit_pos_tagging_preview_samples.blockSignals(True)

            self.combo_box_pos_tagging_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['pos_tagging']['preview_lang']))
            self.text_edit_pos_tagging_preview_samples.setText(settings['pos_tagging']['preview_samples'])
            self.text_edit_pos_tagging_preview_results.setText(settings['pos_tagging']['preview_results'])

            self.combo_box_pos_tagging_preview_lang.blockSignals(False)
            self.text_edit_pos_tagging_preview_samples.blockSignals(False)

        # POS Tagging -> Tagsets
        if not defaults:
            self.combo_box_tagsets_lang.blockSignals(True)
            self.combo_box_tagsets_pos_tagger.blockSignals(True)

            self.combo_box_tagsets_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['tagsets']['preview_lang']))
            self.combo_box_tagsets_pos_tagger.setCurrentText(settings['tagsets']['preview_pos_tagger'][settings['tagsets']['preview_lang']])

            self.combo_box_tagsets_lang.blockSignals(False)
            self.combo_box_tagsets_pos_tagger.blockSignals(False)

        # Lemmatization
        for lang in settings['lemmatization']['lemmatizers']:
            self.__dict__[f'combo_box_lemmatizer_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_lemmatizer_{lang}'].setCurrentText(settings['lemmatization']['lemmatizers'][lang])

            self.__dict__[f'combo_box_lemmatizer_{lang}'].blockSignals(False)

        if not defaults:
            self.combo_box_lemmatization_preview_lang.blockSignals(True)
            self.text_edit_lemmatization_preview_samples.blockSignals(True)

            self.combo_box_lemmatization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['lemmatization']['preview_lang']))
            self.text_edit_lemmatization_preview_samples.setText(settings['lemmatization']['preview_samples'])
            self.text_edit_lemmatization_preview_results.setText(settings['lemmatization']['preview_results'])

            self.combo_box_lemmatization_preview_lang.blockSignals(False)
            self.text_edit_lemmatization_preview_samples.blockSignals(False)

        # Stop Words
        for lang in settings['stop_words']['stop_words']:
            self.__dict__[f'combo_box_stop_words_{lang}'].setCurrentText(settings['stop_words']['stop_words'][lang])

        if not defaults:
            self.combo_box_stop_words_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['stop_words']['preview_lang']))

        if defaults:
            self.main.settings_custom['stop_words']['custom_lists'] = copy.deepcopy(self.main.settings_default['stop_words']['custom_lists'])

        self.combo_box_stop_words_preview_lang.currentTextChanged.emit(self.combo_box_stop_words_preview_lang.currentText())

        # Measures -> Dispersion
        self.spin_box_dispersion_number_sections.setValue(settings['measures']['dispersion']['general']['number_sections'])

        # Measures -> Adjusted Frequency
        self.spin_box_adjusted_freq_number_sections.setValue(settings['measures']['adjusted_freq']['general']['number_sections'])
        self.checkbox_use_same_settings_dispersion.setChecked(settings['measures']['adjusted_freq']['general']['use_same_settings_dispersion'])

        # Measures -> Statistical Significance
        self.combo_box_z_score_direction.setCurrentText(settings['measures']['statistical_significance']['z_score']['direction'])

        self.spin_box_students_t_test_2_sample_number_sections.setValue(settings['measures']['statistical_significance']['students_t_test_2_sample']['number_sections'])
        self.combo_box_students_t_test_2_sample_use_data.setCurrentText(settings['measures']['statistical_significance']['students_t_test_2_sample']['use_data'])
        self.combo_box_students_t_test_2_sample_variances.setCurrentText(settings['measures']['statistical_significance']['students_t_test_2_sample']['variances'])

        self.checkbox_pearsons_chi_squared_test_apply_correction.setChecked(settings['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'])

        self.combo_box_fishers_exact_test_direction.setCurrentText(settings['measures']['statistical_significance']['fishers_exact_test']['direction'])

        self.spin_box_mann_whitney_u_test_number_sections.setValue(settings['measures']['statistical_significance']['mann_whitney_u_test']['number_sections'])
        self.combo_box_mann_whitney_u_test_use_data.setCurrentText(settings['measures']['statistical_significance']['mann_whitney_u_test']['use_data'])
        self.combo_box_mann_whitney_u_test_direction.setCurrentText(settings['measures']['statistical_significance']['mann_whitney_u_test']['direction'])
        self.checkbox_mann_whitney_u_test_apply_correction.setChecked(settings['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction'])

        # Measures -> Effect Size
        self.spin_box_kilgarriffs_ratio_smoothing_param.setValue(settings['measures']['effect_size']['kilgarriffs_ratio']['smoothing_param'])

        # Figures
        self.combo_box_figs_line_chart_font.setCurrentText(settings['figs']['line_chart']['font'])

        self.combo_box_figs_word_cloud_font.setCurrentText(settings['figs']['word_cloud']['font'])
        self.label_figs_word_cloud_bg_color_pick.set_color(settings['figs']['word_cloud']['bg_color'])

        self.combo_box_figs_network_graph_layout.setCurrentText(settings['figs']['network_graph']['layout'])
        self.combo_box_figs_network_graph_node_font.setCurrentText(settings['figs']['network_graph']['node_font'])
        self.spin_box_figs_network_graph_node_font_size.setValue(settings['figs']['network_graph']['node_font_size'])
        self.combo_box_figs_network_graph_edge_font.setCurrentText(settings['figs']['network_graph']['edge_font'])
        self.spin_box_figs_network_graph_edge_font_size.setValue(settings['figs']['network_graph']['edge_font_size'])
        self.label_figs_network_graph_edge_color_pick.set_color(settings['figs']['network_graph']['edge_color'])

        # Change wordcloud's default font
        self.change_wordcloud_font()

    def settings_validate(self):
        def validate_path(line_edit):
            if not os.path.exists(line_edit.text()):
                wordless_msg_box.wordless_msg_box_path_not_exist(self.main, line_edit.text())

                line_edit.setFocus()
                line_edit.selectAll()

                return False
            elif not os.path.isdir(line_edit.text()):
                wordless_msg_box.wordless_msge_box_path_not_dir(self.main, line_edit.text())

                line_edit.setFocus()
                line_edit.selectAll()

                return False
            else:
                return True

        def confirm_path(line_edit):
            if not os.path.exists(line_edit.text()):
                reply = wordless_msg_box.wordless_msg_box_path_not_exist_confirm(self.main, line_edit.text())

                if reply == QMessageBox.Yes:
                    return True
                else:
                    line_edit.setFocus()
                    line_edit.selectAll()

                    return False
            elif not os.path.isdir(line_edit.text()):
                wordless_msg_box.wordless_msg_box_path_not_dir(self.main, line_edit.text())

                line_edit.setFocus()
                line_edit.selectAll()

                return False
            else:
                return True

        if self.tree_settings.item_selected_old.text(0) == self.tr('Import'):
            if (validate_path(self.line_edit_import_files_default_path) and
                validate_path(self.line_edit_import_search_terms_default_path) and
                validate_path(self.line_edit_import_stop_words_default_path) and
                confirm_path(self.line_edit_import_temp_files_default_path)):
                return True
        elif self.tree_settings.item_selected_old.text(0) == self.tr('Export'):
            if (confirm_path(self.line_edit_export_tables_default_path) and
                confirm_path(self.line_edit_export_search_terms_default_path) and
                confirm_path(self.line_edit_export_stop_words_default_path)):
                return True
        else:
            return True

    def settings_save(self):
        if self.settings_apply():
            self.accept()

    def settings_apply(self):
        settings_valid = self.settings_validate()

        if settings_valid:
            settings = self.main.settings_custom

            # Check font settings
            font_old = [
                settings['general']['font_settings']['font_family'],
                settings['general']['font_settings']['font_size']
            ]

            font_new = [
                self.combo_box_font_family.currentFont().family(),
                self.combo_box_font_size.get_val()
            ]

            if font_new == font_old:
                result = 'skip'
            else:
                dialog_restart_required = wordless_dialog_misc.Wordless_Dialog_Restart_Required(self.main)
                result = dialog_restart_required.exec_()

                if result == QDialog.Accepted:
                    result = 'restart'
                elif result == QDialog.Rejected:
                    result = 'cancel'

            if result in ['skip', 'restart']:
                # General
                settings['general']['font_settings']['font_family'] = self.combo_box_font_family.currentFont().family()
                settings['general']['font_settings']['font_size'] = self.combo_box_font_size.get_val()

                settings['general']['update_settings']['check_updates_on_startup'] = self.checkbox_check_updates_on_startup.isChecked()

                settings['general']['misc']['confirm_on_exit'] = self.checkbox_confirm_on_exit.isChecked()

                # Import
                settings['import']['files']['default_path'] = self.line_edit_import_files_default_path.text()

                settings['import']['search_terms']['default_path'] = self.line_edit_import_search_terms_default_path.text()
                settings['import']['search_terms']['detect_encodings'] = self.checkbox_import_search_terms_detect_encodings.isChecked()

                settings['import']['stop_words']['default_path'] = self.line_edit_import_stop_words_default_path.text()
                settings['import']['stop_words']['detect_encodings'] = self.checkbox_import_stop_words_detect_encodings.isChecked()

                settings['import']['temp_files']['default_path'] = self.line_edit_import_temp_files_default_path.text()
                settings['import']['temp_files']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_import_temp_files_default_encoding.currentText())

                # Export
                settings['export']['tables']['default_path'] = self.line_edit_export_tables_default_path.text()
                settings['export']['tables']['default_type'] = self.combo_box_export_tables_default_type.currentText()
                settings['export']['tables']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_tables_default_encoding.currentText())

                settings['export']['search_terms']['default_path'] = self.line_edit_export_search_terms_default_path.text()
                settings['export']['search_terms']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_search_terms_default_encoding.currentText())

                settings['export']['stop_words']['default_path'] = self.line_edit_export_stop_words_default_path.text()
                settings['export']['stop_words']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_stop_words_default_encoding.currentText())

                # Auto-detection
                settings['auto_detection']['detection_settings']['number_lines'] = self.spin_box_auto_detection_number_lines.value()
                settings['auto_detection']['detection_settings']['number_lines_no_limit'] = self.checkbox_auto_detection_number_lines_no_limit.isChecked()

                settings['auto_detection']['default_settings']['default_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_auto_detection_default_lang.currentText())
                settings['auto_detection']['default_settings']['default_text_type'] = wordless_conversion.to_text_type_code(self.main, self.combo_box_auto_detection_default_text_type.currentText())
                settings['auto_detection']['default_settings']['default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_auto_detection_default_encoding.currentText())

                # Data
                settings['data']['precision_decimal'] = self.spin_box_precision_decimal.value()
                settings['data']['precision_pct'] = self.spin_box_precision_pct.value()
                settings['data']['precision_p_value'] = self.spin_box_precision_p_value.value()

                # Tags
                settings['tags']['tags_pos'] = self.table_tags_pos.get_tags()
                settings['tags']['tags_non_pos'] = self.table_tags_non_pos.get_tags()

                # Tokenization -> Sentence Tokenization
                for lang in settings['sentence_tokenization']['sentence_tokenizers']:
                    settings['sentence_tokenization']['sentence_tokenizers'][lang] = self.__dict__[f'combo_box_sentence_tokenizer_{lang}'].currentText()

                # Tokenization -> Word Tokenization
                for lang in settings['word_tokenization']['word_tokenizers']:
                    settings['word_tokenization']['word_tokenizers'][lang] = self.__dict__[f'combo_box_word_tokenizer_{lang}'].currentText()

                # Tokenization -> Word Detokenization
                for lang in settings['word_detokenization']['word_detokenizers']:
                    settings['word_detokenization']['word_detokenizers'][lang] = self.__dict__[f'combo_box_word_detokenizer_{lang}'].currentText()

                # POS Tagging
                for lang in settings['pos_tagging']['pos_taggers']:
                    settings['pos_tagging']['pos_taggers'][lang] = self.__dict__[f'combo_box_pos_tagger_{lang}'].currentText()

                settings['pos_tagging']['to_universal_pos_tags'] = self.checkbox_to_universal_pos_tags.isChecked()

                # POS Tagging -> Tagsets
                if self.pos_tag_mappings_loaded:
                    preview_lang = settings['tagsets']['preview_lang']
                    preview_pos_tagger = settings['tagsets']['preview_pos_tagger'][preview_lang]

                    for i in range(self.table_mappings.rowCount()):
                        settings['tagsets']['mappings'][preview_lang][preview_pos_tagger][i][1] = self.table_mappings.cellWidget(i, 1).currentText()

                # Lemmatization
                for lang in settings['lemmatization']['lemmatizers']:
                    settings['lemmatization']['lemmatizers'][lang] = self.__dict__[f'combo_box_lemmatizer_{lang}'].currentText()

                # Stop Words
                for lang in settings['stop_words']['stop_words']:
                    settings['stop_words']['stop_words'][lang] = self.__dict__[f'combo_box_stop_words_{lang}'].currentText()

                if settings['stop_words']['stop_words'][settings['stop_words']['preview_lang']] == self.tr('Custom List'):
                    settings['stop_words']['custom_lists'][settings['stop_words']['preview_lang']] = self.list_stop_words_preview_results.get_items()

                # Measures -> Dispersion
                settings['measures']['dispersion']['general']['number_sections'] = self.spin_box_dispersion_number_sections.value()

                # Measures -> Adjusted Frequency
                settings['measures']['adjusted_freq']['general']['number_sections'] = self.spin_box_adjusted_freq_number_sections.value()
                settings['measures']['adjusted_freq']['general']['use_same_settings_dispersion'] = self.checkbox_use_same_settings_dispersion.isChecked()

                # Measures -> Statistical Significance
                settings['measures']['statistical_significance']['z_score']['direction'] = self.combo_box_z_score_direction.currentText()

                settings['measures']['statistical_significance']['students_t_test_2_sample']['number_sections'] = self.spin_box_students_t_test_2_sample_number_sections.value()
                settings['measures']['statistical_significance']['students_t_test_2_sample']['use_data'] = self.combo_box_students_t_test_2_sample_use_data.currentText()
                settings['measures']['statistical_significance']['students_t_test_2_sample']['variances'] = self.combo_box_students_t_test_2_sample_variances.currentText()

                settings['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = self.checkbox_pearsons_chi_squared_test_apply_correction.isChecked()

                settings['measures']['statistical_significance']['fishers_exact_test']['direction'] = self.combo_box_fishers_exact_test_direction.currentText()

                settings['measures']['statistical_significance']['mann_whitney_u_test']['number_sections'] = self.spin_box_mann_whitney_u_test_number_sections.value()
                settings['measures']['statistical_significance']['mann_whitney_u_test']['use_data'] = self.combo_box_mann_whitney_u_test_use_data.currentText()
                settings['measures']['statistical_significance']['mann_whitney_u_test']['direction'] = self.combo_box_mann_whitney_u_test_direction.currentText()
                settings['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction'] = self.checkbox_mann_whitney_u_test_apply_correction.isChecked()

                # Measures -> Effect Size
                settings['measures']['effect_size']['kilgarriffs_ratio']['smoothing_param'] = self.spin_box_kilgarriffs_ratio_smoothing_param.value()

                # Figures
                settings['figs']['line_chart']['font'] = self.combo_box_figs_line_chart_font.currentText()

                settings['figs']['word_cloud']['font'] = self.combo_box_figs_word_cloud_font.currentText()
                settings['figs']['word_cloud']['bg_color'] = self.label_figs_word_cloud_bg_color_pick.get_color()

                settings['figs']['network_graph']['layout'] = self.combo_box_figs_network_graph_layout.currentText()
                settings['figs']['network_graph']['node_font'] = self.combo_box_figs_network_graph_node_font.currentText()
                settings['figs']['network_graph']['node_font_size'] = self.spin_box_figs_network_graph_node_font_size.value()
                settings['figs']['network_graph']['edge_font'] = self.combo_box_figs_network_graph_edge_font.currentText()
                settings['figs']['network_graph']['edge_font_size'] = self.spin_box_figs_network_graph_edge_font_size.value()
                settings['figs']['network_graph']['edge_color'] = self.label_figs_network_graph_edge_color_pick.get_color()

                # Change wordcloud's default font
                self.change_wordcloud_font()

                self.wordless_settings_changed.emit()

                if result == 'restart':
                    self.main.restart()

                return True
            elif result == 'cancel':
                return False

    def load(self, tab = None):
        self.load_settings()

        if tab:
            item_selected = self.tree_settings.findItems(tab, Qt.MatchRecursive)[0]

            self.tree_settings.item_selected_old = item_selected

            self.tree_settings.clearSelection()
            item_selected.setSelected(True)

            if not self.tree_settings.findItems(tab, Qt.MatchExactly):
                item_selected.parent().setExpanded(True)

        # Calculate width
        for node in self.tree_settings.get_nodes():
            node.setExpanded(True)

        self.tree_settings.setFixedWidth(self.tree_settings.columnWidth(0) + 10)

        for node in self.tree_settings.get_nodes():
            node.setExpanded(False)

        self.exec_()
