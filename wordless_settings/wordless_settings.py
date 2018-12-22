#
# Wordless: Settings
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import json
import os
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_text import *
from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Stop_Words(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = ['1', '2', '3', '4', '5'],
                         cols_stretch = ['1', '2', '3', '4', '5'])

        self.horizontalHeader().setHidden(True)
        self.verticalHeader().setHidden(True)

        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def set_items(self, tokens):
        self.clear_table()

        self.setRowCount((len(tokens) - 1) // self.columnCount() + 1) 

        for i, token in enumerate(tokens):
            row = i // self.columnCount()
            col = i % self.columnCount()

            self.setItem(row, col, QTableWidgetItem(token))

class Wordless_Settings(QDialog):
    wordless_settings_changed = pyqtSignal()

    preview_results_updated_sentence_tokenization = pyqtSignal(str, list)
    preview_results_updated_word_tokenization = pyqtSignal(str, list)
    preview_results_updated_word_detokenization = pyqtSignal(str, list)
    preview_results_updated_pos_tagging = pyqtSignal(str, list)
    preview_results_updated_lemmatization = pyqtSignal(str, list)

    def __init__(self, parent):
        super().__init__(parent)

        self.main = parent

        self.preview_processing_sentence_tokenization = False
        self.preview_processing_word_tokenization = False
        self.preview_processing_word_detokenization = False
        self.preview_processing_pos_tagging = False
        self.preview_processing_lemmatization = False

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedSize(800, 550)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('General')]))
        self.tree_settings.topLevelItem(0).addChild(QTreeWidgetItem([self.tr('Import')]))
        self.tree_settings.topLevelItem(0).addChild(QTreeWidgetItem([self.tr('Export')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Auto-detection')]))
        self.tree_settings.topLevelItem(1).addChild(QTreeWidgetItem([self.tr('Language Detection')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Tokenization')]))
        self.tree_settings.topLevelItem(2).addChild(QTreeWidgetItem([self.tr('Sentence Tokenization')]))
        self.tree_settings.topLevelItem(2).addChild(QTreeWidgetItem([self.tr('Word Tokenization')]))
        self.tree_settings.topLevelItem(2).addChild(QTreeWidgetItem([self.tr('Word Detokenization')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('POS Tagging')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Lemmatization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Stop Words')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem([self.tr('Measures')]))
        self.tree_settings.topLevelItem(6).addChild(QTreeWidgetItem([self.tr('Dispersion')]))
        self.tree_settings.topLevelItem(6).addChild(QTreeWidgetItem([self.tr('Adjusted Frequency')]))
        self.tree_settings.topLevelItem(6).addChild(QTreeWidgetItem([self.tr('Statistical Significance')]))
        self.tree_settings.topLevelItem(6).addChild(QTreeWidgetItem([self.tr('Effect Size')]))

        self.tree_settings.itemSelectionChanged.connect(self.selection_changed)

        self.scroll_area_settings = wordless_layout.Wordless_Scroll_Area(self.main)

        self.init_settings_general()
        self.init_settings_import()
        self.init_settings_export()

        self.init_settings_lang_detection()

        self.init_settings_sentence_tokenization()
        self.init_settings_word_tokenization()
        self.init_settings_word_detokenization()

        self.init_settings_pos_tagging()
        self.init_settings_lemmatization()
        self.init_settings_stop_words()

        self.init_settings_dispersion()
        self.init_settings_adjusted_freq()
        self.init_settings_statistical_significance()
        self.init_settings_effect_size()

        button_restore_default_settings = QPushButton(self.tr('Restore Default Settings'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_restore_default_settings.clicked.connect(self.restore_default_settings)
        button_save.clicked.connect(self.settings_save)
        button_apply.clicked.connect(self.settings_apply)
        button_cancel.clicked.connect(self.reject)

        layout_buttons_right = QGridLayout()
        layout_buttons_right.addWidget(button_save, 0, 0)
        layout_buttons_right.addWidget(button_apply, 0, 1)
        layout_buttons_right.addWidget(button_cancel, 0, 2)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.tree_settings, 0, 0)
        self.layout().addWidget(self.scroll_area_settings, 0, 1)
        self.layout().addWidget(button_restore_default_settings, 1, 0)
        self.layout().addLayout(layout_buttons_right, 1, 1, Qt.AlignRight)

        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 3)

        self.load_settings()
        
        self.tree_settings.item_selected_old = self.tree_settings.topLevelItem(0)

        self.tree_settings.topLevelItem(0).setSelected(True)

    def selection_changed(self):
        settings_cur = None

        if self.tree_settings.selectedItems():
            if self.settings_validate():
                item_selected = self.tree_settings.selectedItems()[0]
                item_selected_text = item_selected.text(0)

                if item_selected_text == self.tr('General'):
                    item_selected.setExpanded(True)
                    settings_cur = self.settings_general
                elif item_selected_text == self.tr('Import'):
                    settings_cur = self.settings_import
                elif item_selected_text == self.tr('Export'):
                    settings_cur = self.settings_export

                elif item_selected_text == self.tr('Auto-detection'):
                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Language Detection'):
                    settings_cur = self.settings_lang_detection

                elif item_selected_text == self.tr('Tokenization'):
                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Sentence Tokenization'):
                    settings_cur = self.settings_sentence_tokenization
                elif item_selected_text == self.tr('Word Tokenization'):
                    settings_cur = self.settings_word_tokenization
                elif item_selected_text == self.tr('Word Detokenization'):
                    settings_cur = self.settings_word_detokenization

                elif item_selected_text == self.tr('POS Tagging'):
                    settings_cur = self.settings_pos_tagging
                elif item_selected_text == self.tr('Lemmatization'):
                    settings_cur = self.settings_lemmatization
                elif item_selected_text == self.tr('Stop Words'):
                    settings_cur = self.settings_stop_words

                elif item_selected_text == self.tr('Measures'):
                    item_selected.setExpanded(True)
                elif item_selected_text == self.tr('Dispersion'):
                    settings_cur = self.settings_dispersion
                elif item_selected_text == self.tr('Adjusted Frequency'):
                    settings_cur = self.settings_adjusted_freq
                elif item_selected_text == self.tr('Statistical Significance'):
                    settings_cur = self.settings_statistical_significance
                elif item_selected_text == self.tr('Effect Size'):
                    settings_cur = self.settings_effect_size

                if settings_cur:
                    self.settings_general.hide()
                    self.settings_import.hide()
                    self.settings_export.hide()

                    self.settings_lang_detection.hide()

                    self.settings_sentence_tokenization.hide()
                    self.settings_word_tokenization.hide()
                    self.settings_word_detokenization.hide()

                    self.settings_pos_tagging.hide()
                    self.settings_lemmatization.hide()
                    self.settings_stop_words.hide()

                    self.settings_dispersion.hide()
                    self.settings_adjusted_freq.hide()
                    self.settings_statistical_significance.hide()
                    self.settings_effect_size.hide()

                    self.scroll_area_settings.takeWidget()
                    self.scroll_area_settings.setWidget(settings_cur)

                    settings_cur.show()

                self.tree_settings.item_selected_old = item_selected
            else:
                self.tree_settings.blockSignals(True)

                self.tree_settings.clearSelection()
                self.tree_settings.item_selected_old.setSelected(True)

                self.tree_settings.blockSignals(False)

    def init_settings_general(self):
        def browse_file():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['general']['file_default_path'])

            if path_file:
                self.line_edit_file_default_path.setText(path_file)

        self.settings_general = QWidget(self)

        # File Settings
        group_box_file_settings = QGroupBox(self.tr('File Settings'), self)

        self.label_file_default_path = QLabel(self.tr('Default Path:'), self)
        self.line_edit_file_default_path = QLineEdit(self)
        self.button_file_browse = QPushButton(self.tr('Browse'), self)
        self.label_file_default_lang = QLabel(self.tr('Default Language:'), self)
        self.combo_box_file_default_lang = wordless_box.Wordless_Combo_Box_Lang(self.main)
        self.label_file_default_encoding = QLabel(self.tr('Default Encoding:'), self)
        self.combo_box_file_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        self.button_file_browse.clicked.connect(browse_file)

        group_box_file_settings.setLayout(QGridLayout())
        group_box_file_settings.layout().addWidget(self.label_file_default_path, 0, 0)
        group_box_file_settings.layout().addWidget(self.line_edit_file_default_path, 0, 1)
        group_box_file_settings.layout().addWidget(self.button_file_browse, 0, 2)
        group_box_file_settings.layout().addWidget(self.label_file_default_lang, 1, 0)
        group_box_file_settings.layout().addWidget(self.combo_box_file_default_lang, 1, 1, 1, 2)
        group_box_file_settings.layout().addWidget(self.label_file_default_encoding, 2, 0)
        group_box_file_settings.layout().addWidget(self.combo_box_file_default_encoding, 2, 1, 1, 2)

        # Precision Settings
        group_box_precision_settings = QGroupBox(self.tr('Precision Settings'), self)

        self.label_precision_decimal = QLabel(self.tr('Decimal:'), self)
        self.spin_box_precision_decimal = QSpinBox(self)
        self.label_precision_pct = QLabel(self.tr('Percentage:'), self)
        self.spin_box_precision_pct = QSpinBox(self)
        self.label_precision_p_value = QLabel(self.tr('p-value:'), self)
        self.spin_box_precision_p_value = QSpinBox(self)

        self.spin_box_precision_decimal.setRange(0, 10)
        self.spin_box_precision_pct.setRange(0, 10)
        self.spin_box_precision_p_value.setRange(0, 15)

        group_box_precision_settings.setLayout(QGridLayout())
        group_box_precision_settings.layout().addWidget(self.label_precision_decimal, 0, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_decimal, 0, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_pct, 1, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_pct, 1, 1)
        group_box_precision_settings.layout().addWidget(self.label_precision_p_value, 2, 0)
        group_box_precision_settings.layout().addWidget(self.spin_box_precision_p_value, 2, 1)

        self.settings_general.setLayout(QGridLayout())
        self.settings_general.layout().addWidget(group_box_file_settings, 0, 0, Qt.AlignTop)
        self.settings_general.layout().addWidget(group_box_precision_settings, 1, 0, Qt.AlignTop)

        self.settings_general.layout().setRowStretch(2, 1)

    def init_settings_import(self):
        def browse_search_terms():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['import']['search_terms_default_path'])

            if path_file:
                self.line_edit_import_search_terms_default_path.setText(path_file)

        self.settings_import = QWidget(self)

        group_box_import_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_import_search_terms_default_path = QLabel(self.tr('Default File Path:'), self)
        self.line_edit_import_search_terms_default_path = QLineEdit(self)
        self.button_import_search_terms_browse = QPushButton(self.tr('Browse'), self)
        self.label_import_search_terms_default_encoding = QLabel(self.tr('Default File Encoding:'), self)
        self.combo_box_import_search_terms_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        self.button_import_search_terms_browse.clicked.connect(browse_search_terms)

        group_box_import_search_terms.setLayout(QGridLayout())
        group_box_import_search_terms.layout().addWidget(self.label_import_search_terms_default_path, 0, 0)
        group_box_import_search_terms.layout().addWidget(self.line_edit_import_search_terms_default_path, 0, 1)
        group_box_import_search_terms.layout().addWidget(self.button_import_search_terms_browse, 0, 2)
        group_box_import_search_terms.layout().addWidget(self.label_import_search_terms_default_encoding, 1, 0)
        group_box_import_search_terms.layout().addWidget(self.combo_box_import_search_terms_default_encoding, 1, 1, 1, 2)

        self.settings_import.setLayout(QGridLayout())
        self.settings_import.layout().addWidget(group_box_import_search_terms, 0, 0, Qt.AlignTop)

    def init_settings_export(self):
        def tables_default_type_changed():
            if self.combo_box_export_tables_default_type.currentText() == self.tr('Excel Workbook (*.xlsx)'):
                self.combo_box_export_tables_default_encoding.setEnabled(False)
            else:
                self.combo_box_export_tables_default_encoding.setEnabled(True)

        def browse_tables():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['export']['tables_default_path'])

            if path_file:
                self.line_edit_export_tables_default_path.setText(path_file)

        def browse_search_terms():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['export']['search_terms_default_path'])

            if path_file:
                self.line_edit_export_search_terms_default_path.setText(path_file)

        self.settings_export = QWidget(self)

        # Tables
        group_box_export_tables = QGroupBox(self.tr('Tables'), self)

        self.label_export_tables_default_path = QLabel(self.tr('Default File Path:'), self)
        self.line_edit_export_tables_default_path = QLineEdit(self)
        self.button_export_tables_default_path = QPushButton(self.tr('Browse'), self)
        self.label_export_tables_default_type = QLabel(self.tr('Default File Type:'), self)
        self.combo_box_export_tables_default_type = wordless_box.Wordless_Combo_Box(self)
        self.label_export_tables_default_encoding = QLabel(self.tr('Default File Encoding:'), self)
        self.combo_box_export_tables_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        self.combo_box_export_tables_default_type.addItems(self.main.settings_global['file_types']['export_tables'])

        self.button_export_tables_default_path.clicked.connect(browse_tables)
        self.combo_box_export_tables_default_type.currentTextChanged.connect(tables_default_type_changed)

        group_box_export_tables.setLayout(QGridLayout())
        group_box_export_tables.layout().addWidget(self.label_export_tables_default_path, 0, 0)
        group_box_export_tables.layout().addWidget(self.line_edit_export_tables_default_path, 0, 1)
        group_box_export_tables.layout().addWidget(self.button_export_tables_default_path, 0, 2)
        group_box_export_tables.layout().addWidget(self.label_export_tables_default_type, 1, 0)
        group_box_export_tables.layout().addWidget(self.combo_box_export_tables_default_type, 1, 1, 1, 2)
        group_box_export_tables.layout().addWidget(self.label_export_tables_default_encoding, 2, 0)
        group_box_export_tables.layout().addWidget(self.combo_box_export_tables_default_encoding, 2, 1, 1 ,2)

        # Search Terms
        group_box_export_search_terms = QGroupBox(self.tr('Search Terms'), self)

        self.label_export_search_terms_default_path = QLabel(self.tr('Default File Path:'), self)
        self.line_edit_export_search_terms_default_path = QLineEdit(self)
        self.button_export_search_terms_default_path = QPushButton(self.tr('Browse'), self)
        self.label_export_search_terms_default_encoding = QLabel(self.tr('Default File Encoding:'), self)
        self.combo_box_export_search_terms_default_encoding = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        self.button_export_search_terms_default_path.clicked.connect(browse_search_terms)

        group_box_export_search_terms.setLayout(QGridLayout())
        group_box_export_search_terms.layout().addWidget(self.label_export_search_terms_default_path, 0, 0)
        group_box_export_search_terms.layout().addWidget(self.line_edit_export_search_terms_default_path, 0, 1)
        group_box_export_search_terms.layout().addWidget(self.button_export_search_terms_default_path, 0, 2)
        group_box_export_search_terms.layout().addWidget(self.label_export_search_terms_default_encoding, 1, 0)
        group_box_export_search_terms.layout().addWidget(self.combo_box_export_search_terms_default_encoding, 1, 1, 1, 2)

        self.settings_export.setLayout(QGridLayout())
        self.settings_export.layout().addWidget(group_box_export_tables, 0, 0, Qt.AlignTop)
        self.settings_export.layout().addWidget(group_box_export_search_terms, 1, 0, Qt.AlignTop)

        self.settings_export.layout().setRowStretch(2, 1)

        tables_default_type_changed()

    def init_settings_lang_detection(self):
        self.settings_lang_detection = QWidget(self)

        # Detection Settings
        group_box_lang_detection_settings = QGroupBox(self.tr('Detection Settings'), self)

        self.label_lang_detection_engine = QLabel(self.tr('Detection Engine:'), self)
        self.combo_box_lang_detection_engine = wordless_box.Wordless_Combo_Box(self)
        self.label_lang_detection_number_lines = QLabel(self.tr('Number of lines to scan in each file:'), self)
        (self.spin_box_lang_detection_number_lines,
         self.checkbox_lang_detection_number_lines_no_limit) = wordless_widgets.wordless_widgets_no_limit(self.main)

        self.combo_box_lang_detection_engine.addItems(['langid.py',
                                                       'langdetect'])

        self.spin_box_lang_detection_number_lines.setRange(1, 1000000)

        layout_number_lines = QGridLayout()
        layout_number_lines.addWidget(self.label_lang_detection_number_lines, 0, 0)
        layout_number_lines.addWidget(self.spin_box_lang_detection_number_lines, 0, 1)
        layout_number_lines.addWidget(self.checkbox_lang_detection_number_lines_no_limit, 0, 2)

        layout_number_lines.setColumnStretch(3, 1)

        group_box_lang_detection_settings.setLayout(QGridLayout())
        group_box_lang_detection_settings.layout().addWidget(self.label_lang_detection_engine, 0, 0)
        group_box_lang_detection_settings.layout().addWidget(self.combo_box_lang_detection_engine, 0, 1)
        group_box_lang_detection_settings.layout().addLayout(layout_number_lines, 1, 0, 1, 3)

        group_box_lang_detection_settings.layout().setColumnStretch(2, 1)

        self.settings_lang_detection.setLayout(QGridLayout())
        self.settings_lang_detection.layout().addWidget(group_box_lang_detection_settings, 0, 0)

        self.settings_lang_detection.layout().setRowStretch(1, 1)

    def init_settings_sentence_tokenization(self):
        def sentence_tokenizers_changed(lang_code):
            if lang_code == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_sentence_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_sentence_tokenization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_sentence_tokenization_preview_results.toPlainText()

        def preview_results_changed():
            def preview():
                sentence_tokenizer = self.__dict__[f'combo_box_sentence_tokenizer_{settings_custom["preview_lang"]}'].currentText()

                results = wordless_text_processing.wordless_sentence_tokenize(self.main, settings_custom['preview_samples'],
                                                                              lang_code = settings_custom['preview_lang'],
                                                                              sentence_tokenizer = sentence_tokenizer)

                self.preview_results_updated_sentence_tokenization.emit(settings_custom['preview_samples'], results)

                self.preview_processing_sentence_tokenization = False

            if settings_custom['preview_samples']:
                self.label_sentence_tokenization_preview_processing.setText(self.tr('Processing ...'))

                if not self.preview_processing_sentence_tokenization:
                    self.preview_processing_sentence_tokenization = True

                    threading.Thread(target = preview).start()
            else:
                self.text_edit_sentence_tokenization_preview_results.clear()

        def preview_results_updated(preview_samples, results):
            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_sentence_tokenization_preview_results.setPlainText('\n'.join(results))

                self.label_sentence_tokenization_preview_processing.setText('')
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['sentence_tokenizers']
        settings_custom = self.main.settings_custom['sentence_tokenization']

        self.settings_sentence_tokenization = QWidget(self)

        # Sentence Tokenizer Settings
        group_box_sentence_tokenizer_settings = QGroupBox(self.tr('Sentence Tokenizer Settings'), self)

        table_sentence_tokenizers = wordless_table.Wordless_Table(self,
                                                                  headers = [
                                                                      self.tr('Languages'),
                                                                      self.tr('Sentence Tokenizers')
                                                                  ],
                                                                  cols_stretch = [
                                                                      self.tr('Sentence Tokenizers')
                                                                  ])

        table_sentence_tokenizers.verticalHeader().setHidden(True)

        table_sentence_tokenizers.setRowCount(len(settings_global))

        for i, lang_code in enumerate(settings_global):
            table_sentence_tokenizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang_code)))

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self.main)

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentTextChanged.connect(lambda text, lang_code = lang_code: sentence_tokenizers_changed(lang_code))

            table_sentence_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'])

        group_box_sentence_tokenizer_settings.setLayout(QGridLayout())
        group_box_sentence_tokenizer_settings.layout().addWidget(table_sentence_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_sentence_tokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_sentence_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_sentence_tokenization_preview_processing = QLabel()
        self.text_edit_sentence_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_sentence_tokenization_preview_results = QTextEdit(self)

        self.combo_box_sentence_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_sentence_tokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_sentence_tokenization_preview_results.setReadOnly(True)

        self.combo_box_sentence_tokenization_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_sentence_tokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_sentence_tokenization_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_sentence_tokenization_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_sentence_tokenization_preview_results.textChanged.connect(preview_changed)

        self.preview_results_updated_sentence_tokenization.connect(preview_results_updated)

        layout_preview_settings = QGridLayout()
        layout_preview_settings.addWidget(self.label_sentence_tokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_sentence_tokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_sentence_tokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_sentence_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_sentence_tokenization_preview_results, 1, 1)

        self.settings_sentence_tokenization.setLayout(QGridLayout())
        self.settings_sentence_tokenization.layout().addWidget(group_box_sentence_tokenizer_settings, 0, 0)
        self.settings_sentence_tokenization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_sentence_tokenization.layout().setRowStretch(0, 2)
        self.settings_sentence_tokenization.layout().setRowStretch(1, 1)

    def init_settings_word_tokenization(self):
        def word_tokenizers_changed(lang_code):
            if lang_code == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_tokenization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_word_tokenization_preview_results.toPlainText()

        def preview_results_changed():
            def preview():
                results = []

                word_tokenizer = self.__dict__[f'combo_box_word_tokenizer_{settings_custom["preview_lang"]}'].currentText()

                for line in settings_custom['preview_samples'].splitlines():
                    sentences = wordless_text_processing.wordless_sentence_tokenize(self.main, line, lang_code)
                    tokens = wordless_text_processing.wordless_word_tokenize(self.main, sentences,
                                                                             lang_code = settings_custom['preview_lang'],
                                                                             word_tokenizer = word_tokenizer)
                    
                    results.append(' '.join(tokens))

                self.preview_results_updated_word_tokenization.emit(settings_custom['preview_samples'], results)

                self.preview_processing_word_tokenization = False

            if settings_custom['preview_samples']:
                self.label_word_tokenization_preview_processing.setText(self.tr('Processing ...'))

                if not self.preview_processing_word_tokenization:
                    self.preview_processing_word_tokenization = True

                    threading.Thread(target = preview).start()
            else:
                self.text_edit_word_tokenization_preview_results.clear()

        def preview_results_updated(preview_samples, results):
            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_word_tokenization_preview_results.setPlainText('\n'.join(results))

                self.label_word_tokenization_preview_processing.setText('')
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['word_tokenizers']
        settings_custom = self.main.settings_custom['word_tokenization']

        self.settings_word_tokenization = QWidget(self)

        # Word Tokenizer Settings
        group_box_word_tokenizer_settings = QGroupBox(self.tr('Word Tokenizer Settings'), self)

        table_word_tokenizers = wordless_table.Wordless_Table(self,
                                                              headers = [
                                                                  self.tr('Languages'),
                                                                  self.tr('Word Tokenizers')
                                                              ],
                                                              cols_stretch = [
                                                                  self.tr('Word Tokenizers')
                                                              ])

        table_word_tokenizers.verticalHeader().setHidden(True)

        table_word_tokenizers.setRowCount(len(settings_global))

        for i, lang_code in enumerate(settings_global):
            table_word_tokenizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang_code)))

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self.main)

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentTextChanged.connect(lambda text, lang_code = lang_code: word_tokenizers_changed(lang_code))

            table_word_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_word_tokenizer_{lang_code}'])

        group_box_word_tokenizer_settings.setLayout(QGridLayout())
        group_box_word_tokenizer_settings.layout().addWidget(table_word_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_tokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
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

        self.preview_results_updated_word_tokenization.connect(preview_results_updated)

        layout_preview_settings = QGridLayout()
        layout_preview_settings.addWidget(self.label_word_tokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_word_tokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_word_tokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_results, 1, 1)

        self.settings_word_tokenization.setLayout(QGridLayout())
        self.settings_word_tokenization.layout().addWidget(group_box_word_tokenizer_settings, 0, 0,)
        self.settings_word_tokenization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_word_tokenization.layout().setRowStretch(0, 2)
        self.settings_word_tokenization.layout().setRowStretch(1, 1)

    def init_settings_word_detokenization(self):
        def word_detokenizers_changed(lang_code):
            if lang_code == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_detokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_detokenization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_word_detokenization_preview_results.toPlainText()

        def preview_results_changed():
            def preview():
                results = []

                word_detokenizer = self.__dict__[f'combo_box_word_detokenizer_{settings_custom["preview_lang"]}'].currentText()

                for line in settings_custom['preview_samples'].splitlines():
                    text = wordless_text_processing.wordless_word_detokenize(self.main, line.split(),
                                                                             lang_code = settings_custom['preview_lang'],
                                                                             word_detokenizer = word_detokenizer)
                    
                    results.append(text)

                self.preview_results_updated_word_detokenization.emit(settings_custom['preview_samples'], results)

                self.preview_processing_word_detokenization = False

            if settings_custom['preview_samples']:
                self.label_word_detokenization_preview_processing.setText(self.tr('Processing ...'))

                if not self.preview_processing_word_detokenization:
                    self.preview_processing_word_detokenization = True

                    threading.Thread(target = preview).start()
            else:
                self.text_edit_word_detokenization_preview_results.clear()

        def preview_results_updated(preview_samples, results):
            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_word_detokenization_preview_results.setPlainText('\n'.join(results))

                self.label_word_detokenization_preview_processing.setText('')
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['word_detokenizers']
        settings_custom = self.main.settings_custom['word_detokenization']

        self.settings_word_detokenization = QWidget(self)

        # Word Detokenizer Settings
        group_box_word_detokenizer_settings = QGroupBox(self.tr('Word Detokenizer Settings'), self)

        table_word_detokenizers = wordless_table.Wordless_Table(self,
                                                                headers = [
                                                                    self.tr('Languages'),
                                                                    self.tr('Word Detokenizers')
                                                                ],
                                                                cols_stretch = [
                                                                    self.tr('Word Detokenizers')
                                                                ])

        table_word_detokenizers.verticalHeader().setHidden(True)

        table_word_detokenizers.setRowCount(len(settings_global))

        for i, lang_code in enumerate(settings_global):
            table_word_detokenizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang_code)))

            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].currentTextChanged.connect(lambda text, lang_code = lang_code: word_detokenizers_changed(lang_code))

            table_word_detokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_word_detokenizer_{lang_code}'])

        group_box_word_detokenizer_settings.setLayout(QGridLayout())
        group_box_word_detokenizer_settings.layout().addWidget(table_word_detokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_detokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
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

        self.preview_results_updated_word_detokenization.connect(preview_results_updated)

        layout_preview_settings = QGridLayout()
        layout_preview_settings.addWidget(self.label_word_detokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_word_detokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_word_detokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_word_detokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_detokenization_preview_results, 1, 1)

        self.settings_word_detokenization.setLayout(QGridLayout())
        self.settings_word_detokenization.layout().addWidget(group_box_word_detokenizer_settings, 0, 0,)
        self.settings_word_detokenization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_word_detokenization.layout().setRowStretch(0, 2)
        self.settings_word_detokenization.layout().setRowStretch(1, 1)

    def init_settings_pos_tagging(self):
        def pos_taggers_changed(lang_code):
            for i, lang_code_global in enumerate(settings_global):
                pos_tagger = self.__dict__[f'combo_box_pos_tagger_{lang_code_global}'].currentText()
                tagset_old = self.__dict__[f'combo_box_tagset_{lang_code_global}'].currentText()

                table_pos_taggers.cellWidget(i, 2).blockSignals(True)

                table_pos_taggers.cellWidget(i, 2).clear()
                table_pos_taggers.cellWidget(i, 2).addItems([self.main.settings_global['pos_taggers'][lang_code_global][pos_tagger], 'Universal'])

                table_pos_taggers.cellWidget(i, 2).blockSignals(False)

                if tagset_old == 'Universal':
                    self.__dict__[f'combo_box_tagset_{lang_code_global}'].setCurrentText('Universal')

            if lang_code == settings_custom['preview_lang']:
                preview_results_changed()

        def tagsets_changed(lang_code):
            if lang_code == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_pos_tagging_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_pos_tagging_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_pos_tagging_preview_results.toPlainText()

        def preview_results_changed():
            def preview():
                results = []

                pos_tagger = self.__dict__[f'combo_box_pos_tagger_{settings_custom["preview_lang"]}'].currentText()
                tagset = self.__dict__[f'combo_box_tagset_{settings_custom["preview_lang"]}'].currentText()

                for line in settings_custom['preview_samples'].splitlines():
                    sentences = wordless_text_processing.wordless_sentence_tokenize(self.main, line,
                                                                                    lang_code = settings_custom['preview_lang'])

                    tokens_tagged = wordless_text_processing.wordless_pos_tag(self.main, sentences,
                                                                              lang_code = settings_custom['preview_lang'],
                                                                              pos_tagger = pos_tagger,
                                                                              tagset = tagset)

                    results.append(' '.join([f'{token}_{tag}' for token, tag in tokens_tagged]))

                self.preview_results_updated_pos_tagging.emit(settings_custom['preview_samples'], results)

                self.preview_processing_pos_tagging = False

            if settings_custom['preview_samples']:
                self.label_pos_tagging_preview_processing.setText(self.tr('Processing ...'))

                if not self.preview_processing_pos_tagging:
                    self.preview_processing_pos_tagging = True

                    threading.Thread(target = preview).start()
            else:
                self.text_edit_pos_tagging_preview_results.clear()

        def preview_results_updated(preview_samples, results):
            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_pos_tagging_preview_results.setPlainText('\n'.join(results))

                self.label_pos_tagging_preview_processing.setText('')
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['pos_taggers']
        settings_custom = self.main.settings_custom['pos_tagging']

        self.settings_pos_tagging = QWidget(self)

        # POS Taggers
        group_box_pos_tagger_settings = QGroupBox(self.tr('POS Tagger Settings'), self)

        table_pos_taggers = wordless_table.Wordless_Table(self,
                                                          headers = [
                                                              self.tr('Languages'),
                                                              self.tr('POS Taggers'),
                                                              self.tr('Tagsets')
                                                          ],
                                                          cols_stretch = [
                                                              self.tr('POS Taggers')
                                                          ])

        table_pos_taggers.verticalHeader().setHidden(True)

        table_pos_taggers.setRowCount(len(settings_global))

        for i, lang_code in enumerate(settings_global):
            table_pos_taggers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang_code)))

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self.main)

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].addItems(list(settings_global[lang_code].keys()))

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentTextChanged.connect(lambda text, lang_code = lang_code: pos_taggers_changed(lang_code))

            table_pos_taggers.setCellWidget(i, 1, self.__dict__[f'combo_box_pos_tagger_{lang_code}'])

            self.__dict__[f'combo_box_tagset_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_tagset_{lang_code}'].currentTextChanged.connect(lambda text, lang_code = lang_code: tagsets_changed(lang_code))

            table_pos_taggers.setCellWidget(i, 2, self.__dict__[f'combo_box_tagset_{lang_code}'])

        group_box_pos_tagger_settings.setLayout(QGridLayout())
        group_box_pos_tagger_settings.layout().addWidget(table_pos_taggers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_pos_tagging_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_pos_tagging_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.label_pos_tagging_preview_processing = QLabel('', self)
        self.text_edit_pos_tagging_preview_samples = QTextEdit(self)
        self.text_edit_pos_tagging_preview_results = QTextEdit(self)

        self.combo_box_pos_tagging_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_pos_tagging_preview_samples.setAcceptRichText(False)
        self.text_edit_pos_tagging_preview_results.setReadOnly(True)

        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(preview_changed)
        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(preview_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(preview_results_changed)
        self.text_edit_pos_tagging_preview_results.textChanged.connect(preview_changed)

        self.preview_results_updated_pos_tagging.connect(preview_results_updated)

        layout_preview_settings = QGridLayout()
        layout_preview_settings.addWidget(self.label_pos_tagging_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_pos_tagging_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_pos_tagging_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_results, 1, 1)

        self.settings_pos_tagging.setLayout(QGridLayout())
        self.settings_pos_tagging.layout().addWidget(group_box_pos_tagger_settings, 0, 0)
        self.settings_pos_tagging.layout().addWidget(group_box_preview, 1, 0)

        self.settings_pos_tagging.layout().setRowStretch(0, 2)
        self.settings_pos_tagging.layout().setRowStretch(1, 1)

        pos_taggers_changed('')

    def init_settings_lemmatization(self):
        def lemmatizers_changed():
            if lang_code == settings_custom['preview_lang']:
                preview_results_changed()

        def preview_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_lemmatization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_lemmatization_preview_samples.toPlainText()
            settings_custom['preview_results'] = self.text_edit_lemmatization_preview_results.toPlainText()

        def preview_results_changed():
            def preview():
                results = []

                lemmatizer = self.__dict__[f'combo_box_lemmatizer_{settings_custom["preview_lang"]}'].currentText()

                for line in settings_custom['preview_samples'].splitlines():
                    tokens = wordless_text_processing.wordless_word_tokenize(self.main, line, lang_code)
                    lemmas = wordless_text_processing.wordless_lemmatize(self.main, tokens, lang_code,
                                                                         lemmatizer = lemmatizer)

                    results.append(wordless_text_processing.wordless_word_detokenize(self.main, lemmas, lang_code))

                self.preview_results_updated_lemmatization.emit(settings_custom['preview_samples'], results)

                self.preview_processing_lemmatization = False

            if settings_custom['preview_samples']:
                self.label_lemmatization_preview_processing.setText(self.tr('Processing ...'))

                if not self.preview_processing_lemmatization:
                    self.preview_processing_lemmatization = True

                    threading.Thread(target = preview).start()
            else:
                self.text_edit_lemmatization_preview_results.clear()

        def preview_results_updated(preview_samples, results):
            if preview_samples == settings_custom['preview_samples']:
                self.text_edit_lemmatization_preview_results.setPlainText('\n'.join(results))

                self.label_lemmatization_preview_processing.setText('')
            else:
                preview_results_changed()

        settings_global = self.main.settings_global['lemmatizers']
        settings_custom = self.main.settings_custom['lemmatization']

        self.settings_lemmatization = QWidget(self)

        # Lemmatizer Settings
        group_box_lemmatizer_settings = QGroupBox(self.tr('Lemmatizer Settings'), self)

        table_lemmatizers = wordless_table.Wordless_Table(self,
                                                          headers = [
                                                              self.tr('Languages'),
                                                              self.tr('Lemmatizers')
                                                          ],
                                                          cols_stretch = [
                                                              self.tr('Lemmatizers')
                                                          ])

        table_lemmatizers.verticalHeader().setHidden(True)

        table_lemmatizers.setRowCount(len(settings_global))

        for i, lang_code in enumerate(settings_global):
            table_lemmatizers.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang_code)))

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentTextChanged.connect(lemmatizers_changed)

            table_lemmatizers.setCellWidget(i, 1, self.__dict__[f'combo_box_lemmatizer_{lang_code}'])

        group_box_lemmatizer_settings.setLayout(QGridLayout())
        group_box_lemmatizer_settings.layout().addWidget(table_lemmatizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_lemmatization_preview_lang = QLabel(self.tr('Select a Language:'), self)
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

        self.preview_results_updated_lemmatization.connect(preview_results_updated)

        layout_preview_settings = QGridLayout()
        layout_preview_settings.addWidget(self.label_lemmatization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_lemmatization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_lemmatization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_results, 1, 1)

        self.settings_lemmatization.setLayout(QGridLayout())
        self.settings_lemmatization.layout().addWidget(group_box_lemmatizer_settings, 0, 0)
        self.settings_lemmatization.layout().addWidget(group_box_preview, 1, 0)

        self.settings_lemmatization.layout().setRowStretch(0, 2)
        self.settings_lemmatization.layout().setRowStretch(1, 1)

    def init_settings_stop_words(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_stop_words_preview_lang.currentText())

        def preview_results_changed():
            lang_text = self.combo_box_stop_words_preview_lang.currentText()
            lang_code_639_3 = wordless_conversion.to_lang_code(self.main, lang_text)
            lang_code_639_1 = wordless_conversion.to_iso_639_1(self.main, lang_code_639_3)

            if lang_code_639_1 == 'zh_cn':
                lang_code_639_1 = 'zh'

            word_list = self.__dict__[f'combo_box_stop_words_{lang_code_639_3}'].currentText()

            if word_list == 'NLTK':
                stop_words = nltk.corpus.stopwords.words(lang_text)
            elif word_list == 'Stopwords ISO':
                if lang_code_639_1 == 'zh_tw':
                    with open(r'stop_words/Stopwords ISO/stopwords_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]
                else:
                    with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                        stop_words = json.load(f)[lang_code_639_1]
            elif word_list == 'stopwords-json':
                if lang_code_639_1 == 'zh_tw':
                    with open(r'stop_words/stopwords-json/stopwords_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]
                else:
                    with open(r'stop_words/stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
                        stop_words = json.load(f)[lang_code_639_1]
            elif word_list == 'HanLP':
                if lang_code_639_1 == 'zh_tw':
                    with open(r'stop_words/HanLP/stopwords_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]
                else:
                    with open(r'stop_words/HanLP/stopwords.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]

            self.label_stop_words_preview_count.setText(self.tr(f'Count of Stop Words: {len(stop_words)}'))
            self.table_stop_words_preview_results.set_items(stop_words)

        settings_global = self.main.settings_global['stop_words']
        settings_custom = self.main.settings_custom['stop_words']

        self.settings_stop_words = QWidget(self)

        # Stop Words Settings
        group_box_stop_words_settings = QGroupBox(self.tr('Stop Words Settings'), self)

        table_stop_words = wordless_table.Wordless_Table(self,
                                                         headers = [
                                                             self.tr('Languages'),
                                                             self.tr('Stop Words')
                                                         ],
                                                         cols_stretch = [
                                                             self.tr('Stop Words')
                                                         ])

        table_stop_words.verticalHeader().setHidden(True)

        table_stop_words.setRowCount(len(settings_global))

        for i, lang_code in enumerate(settings_global):
            table_stop_words.setItem(i, 0, QTableWidgetItem(wordless_conversion.to_lang_text(self.main, lang_code)))

            self.__dict__[f'combo_box_stop_words_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_stop_words_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_stop_words_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_stop_words.setCellWidget(i, 1, self.__dict__[f'combo_box_stop_words_{lang_code}'])

        group_box_stop_words_settings.setLayout(QGridLayout())
        group_box_stop_words_settings.layout().addWidget(table_stop_words, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_stop_words_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_stop_words_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.combo_box_stop_words_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.combo_box_stop_words_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_stop_words_preview_lang.currentTextChanged.connect(preview_results_changed)

        layout_preview_lang = QGridLayout()
        layout_preview_lang.addWidget(self.label_stop_words_preview_lang, 0, 0)
        layout_preview_lang.addWidget(self.combo_box_stop_words_preview_lang, 0, 1)

        self.label_stop_words_preview_count = QLabel('', self)

        self.table_stop_words_preview_results = Wordless_Table_Stop_Words(self)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_lang, 0, 0, Qt.AlignLeft)
        group_box_preview.layout().addWidget(self.label_stop_words_preview_count, 0, 1, Qt.AlignRight)
        group_box_preview.layout().addWidget(self.table_stop_words_preview_results, 1, 0, 1, 2)

        self.settings_stop_words.setLayout(QGridLayout())
        self.settings_stop_words.layout().addWidget(group_box_stop_words_settings, 0, 0)
        self.settings_stop_words.layout().addWidget(group_box_preview, 1, 0)

        self.settings_stop_words.layout().setRowStretch(0, 2)
        self.settings_stop_words.layout().setRowStretch(1, 1)

        preview_results_changed()

    def init_settings_dispersion(self):
        self.settings_dispersion = QWidget(self)

        # General
        group_box_general = QGroupBox(self.tr('General'), self)

        (self.label_dispersion_divide,
         self.spin_box_dispersion_number_sections,
         self.label_dispersion_sections) = wordless_widgets.wordless_widgets_number_sections(self)

        group_box_general.setLayout(QGridLayout())
        group_box_general.layout().addWidget(self.label_dispersion_divide, 0, 0)
        group_box_general.layout().addWidget(self.spin_box_dispersion_number_sections, 0, 1)
        group_box_general.layout().addWidget(self.label_dispersion_sections, 0, 2)

        group_box_general.layout().setColumnStretch(3, 1)

        self.settings_dispersion.setLayout(QGridLayout())
        self.settings_dispersion.layout().addWidget(group_box_general, 0, 0)

        self.settings_dispersion.layout().setRowStretch(1, 1)

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

        group_box_general.setLayout(QGridLayout())
        group_box_general.layout().addWidget(self.label_adjusted_freq_divide, 0, 0)
        group_box_general.layout().addWidget(self.spin_box_adjusted_freq_number_sections, 0, 1)
        group_box_general.layout().addWidget(self.label_adjusted_freq_sections, 0, 2)
        group_box_general.layout().addWidget(self.checkbox_use_same_settings_dispersion, 1, 0, 1, 4)

        group_box_general.layout().setColumnStretch(3, 1)

        self.settings_adjusted_freq.setLayout(QGridLayout())
        self.settings_adjusted_freq.layout().addWidget(group_box_general, 0, 0)

        self.settings_adjusted_freq.layout().setRowStretch(1, 1)

        use_same_settings_changed()

    def init_settings_statistical_significance(self):
        self.settings_statistical_significance = QWidget(self)

        # z-score
        group_box_z_score = QGroupBox(self.tr('z-score'), self)

        (self.label_z_score_direction,
         self.combo_box_z_score_direction) = wordless_widgets.wordless_widgets_direction_2(self)

        group_box_z_score.setLayout(QGridLayout())
        group_box_z_score.layout().addWidget(self.label_z_score_direction, 0, 0)
        group_box_z_score.layout().addWidget(self.combo_box_z_score_direction, 0, 1)

        group_box_z_score.layout().setColumnStretch(2, 1)

        # Student's t-test (Two-sample)
        group_box_students_t_test_two_sample = QGroupBox(self.tr('Student\'s t-test (Two-sample)'), self)

        (self.label_students_t_test_two_sample_divide,
         self.spin_box_students_t_test_two_sample_number_sections,
         self.label_students_t_test_two_sample_sections) = wordless_widgets.wordless_widgets_number_sections(self)

        (self.label_students_t_test_two_sample_use_data,
         self.combo_box_students_t_test_two_sample_use_data) = wordless_widgets.wordless_widgets_use_data_freq(self)
        self.label_students_t_test_two_sample_variances = QLabel(self.tr('Variances:'), self)
        self.combo_box_students_t_test_two_sample_variances = QComboBox(self)
        self.label_welchs_t_test = QLabel(self.tr(f'''{self.main.settings_global["styles"]["style_hints"]}
                                                      <body>
                                                          <p>
                                                              * If variances are set to "Unequal", the Welch\'s t-test will be performed instead.
                                                          </p>
                                                  '''), self)

        self.combo_box_students_t_test_two_sample_variances.addItems([self.tr('Equal'),
                                                                      self.tr('Unequal')])

        layout_students_t_test_two_sample_number_sections = QGridLayout()
        layout_students_t_test_two_sample_number_sections.addWidget(self.label_students_t_test_two_sample_divide, 0, 0)
        layout_students_t_test_two_sample_number_sections.addWidget(self.spin_box_students_t_test_two_sample_number_sections, 0, 1)
        layout_students_t_test_two_sample_number_sections.addWidget(self.label_students_t_test_two_sample_sections, 0, 2)

        layout_students_t_test_two_sample_number_sections.setColumnStretch(3, 1)

        group_box_students_t_test_two_sample.setLayout(QGridLayout())
        group_box_students_t_test_two_sample.layout().addLayout(layout_students_t_test_two_sample_number_sections, 0, 0, 1, 3)
        group_box_students_t_test_two_sample.layout().addWidget(self.label_students_t_test_two_sample_use_data, 1, 0)
        group_box_students_t_test_two_sample.layout().addWidget(self.combo_box_students_t_test_two_sample_use_data, 1, 1)
        group_box_students_t_test_two_sample.layout().addWidget(self.label_students_t_test_two_sample_variances, 2, 0)
        group_box_students_t_test_two_sample.layout().addWidget(self.combo_box_students_t_test_two_sample_variances, 2, 1)
        group_box_students_t_test_two_sample.layout().addWidget(self.label_welchs_t_test, 3, 0, 1, 3)

        group_box_students_t_test_two_sample.layout().setColumnStretch(2, 1)

        # Pearson's Chi-squared Test
        group_box_pearsons_chi_squared_test = QGroupBox(self.tr('Pearson\'s Chi-squared Test'), self)

        self.checkbox_pearsons_chi_squared_test_apply_correction = QCheckBox(self.tr('Apply Yates\'s correction for continuity'))

        group_box_pearsons_chi_squared_test.setLayout(QGridLayout())
        group_box_pearsons_chi_squared_test.layout().addWidget(self.checkbox_pearsons_chi_squared_test_apply_correction, 0, 0)

        # Fisher's Exact Test
        group_box_fishers_exact_test = QGroupBox(self.tr('Fisher\'s Exact Test'), self)

        (self.label_fishers_exact_test_direction,
         self.combo_box_fishers_exact_test_direction) = wordless_widgets.wordless_widgets_direction(self)

        group_box_fishers_exact_test.setLayout(QGridLayout())
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

        layout_mann_whitney_u_test_number_sections = QGridLayout()
        layout_mann_whitney_u_test_number_sections.addWidget(self.label_mann_whitney_u_test_divide, 0, 0)
        layout_mann_whitney_u_test_number_sections.addWidget(self.spin_box_mann_whitney_u_test_number_sections, 0, 1)
        layout_mann_whitney_u_test_number_sections.addWidget(self.label_mann_whitney_u_test_sections, 0, 2)

        layout_mann_whitney_u_test_number_sections.setColumnStretch(3, 1)

        group_box_mann_whitney_u_test.setLayout(QGridLayout())
        group_box_mann_whitney_u_test.layout().addLayout(layout_mann_whitney_u_test_number_sections, 0, 0, 1, 3)
        group_box_mann_whitney_u_test.layout().addWidget(self.label_mann_whitney_u_test_use_data, 1, 0)
        group_box_mann_whitney_u_test.layout().addWidget(self.combo_box_mann_whitney_u_test_use_data, 1, 1)
        group_box_mann_whitney_u_test.layout().addWidget(self.label_mann_whitney_u_test_direction, 2, 0)
        group_box_mann_whitney_u_test.layout().addWidget(self.combo_box_mann_whitney_u_test_direction, 2, 1)
        group_box_mann_whitney_u_test.layout().addWidget(self.checkbox_mann_whitney_u_test_apply_correction, 3, 0, 1, 3)

        group_box_mann_whitney_u_test.layout().setColumnStretch(3, 1)

        self.settings_statistical_significance.setLayout(QGridLayout())
        self.settings_statistical_significance.layout().addWidget(group_box_z_score, 0, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_students_t_test_two_sample, 1, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_pearsons_chi_squared_test, 2, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_fishers_exact_test, 3, 0)
        self.settings_statistical_significance.layout().addWidget(group_box_mann_whitney_u_test, 4, 0)

        self.settings_statistical_significance.layout().setRowStretch(5, 1)

    def init_settings_effect_size(self):
        self.settings_effect_size = QWidget(self)

        # Kilgarriff's Ratio
        group_box_kilgarriffs_ratio = QGroupBox(self.tr('Kilgarriff\'s Ratio'), self)

        self.label_kilgarriffs_ratio_smoothing_parameter = QLabel(self.tr('Smoothing Parameter'), self)
        self.spin_box_kilgarriffs_ratio_smoothing_parameter = QDoubleSpinBox(self)

        self.spin_box_kilgarriffs_ratio_smoothing_parameter.setRange(0.01, 10000)

        group_box_kilgarriffs_ratio.setLayout(QGridLayout())
        group_box_kilgarriffs_ratio.layout().addWidget(self.label_kilgarriffs_ratio_smoothing_parameter, 0, 0)
        group_box_kilgarriffs_ratio.layout().addWidget(self.spin_box_kilgarriffs_ratio_smoothing_parameter, 0, 1)

        group_box_kilgarriffs_ratio.layout().setColumnStretch(2, 1)

        self.settings_effect_size.setLayout(QGridLayout())
        self.settings_effect_size.layout().addWidget(group_box_kilgarriffs_ratio, 0, 0)

        self.settings_effect_size.layout().setRowStretch(1, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        # General
        if os.path.exists(settings['general']['file_default_path']):
            self.line_edit_file_default_path.setText(settings['general']['file_default_path'])
        else:
            self.line_edit_file_default_path.setText(self.main.settings_default['general']['file_default_path'])

        self.combo_box_file_default_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['general']['file_default_lang']))
        self.combo_box_file_default_encoding.setCurrentText(wordless_conversion.to_encoding_text(self.main, settings['general']['file_default_encoding']))

        self.spin_box_precision_decimal.setValue(settings['general']['precision_decimal'])
        self.spin_box_precision_pct.setValue(settings['general']['precision_pct'])
        self.spin_box_precision_p_value.setValue(settings['general']['precision_p_value'])

        # General -> Import
        if os.path.exists(settings['import']['search_terms_default_path']):
            self.line_edit_import_search_terms_default_path.setText(settings['import']['search_terms_default_path'])
        else:
            self.line_edit_import_search_terms_default_path.setText(self.main.settings_default['import']['search_terms_default_path'])

        self.combo_box_import_search_terms_default_encoding.setCurrentText(settings['import']['search_terms_default_encoding'])

        # General -> Export
        if os.path.exists(settings['export']['tables_default_path']):
            self.line_edit_export_tables_default_path.setText(settings['export']['tables_default_path'])
        else:
            self.line_edit_export_tables_default_path.setText(self.main.settings_default['export']['tables_default_path'])

        self.combo_box_export_tables_default_type.setCurrentText(settings['export']['tables_default_type'])
        self.combo_box_export_tables_default_encoding.setCurrentText(settings['export']['tables_default_encoding'])

        if os.path.exists(settings['export']['search_terms_default_path']):
            self.line_edit_export_search_terms_default_path.setText(settings['export']['search_terms_default_path'])
        else:
            self.line_edit_export_search_terms_default_path.setText(self.main.settings_default['export']['search_terms_default_path'])

        self.combo_box_export_search_terms_default_encoding.setCurrentText(settings['export']['search_terms_default_encoding'])

        # Auto-detection -> Language Detection
        self.combo_box_lang_detection_engine.setCurrentText(settings['lang_detection']['detection_settings']['detection_engine'])
        self.spin_box_lang_detection_number_lines.setValue(settings['lang_detection']['detection_settings']['number_lines'])
        self.checkbox_lang_detection_number_lines_no_limit.setChecked(settings['lang_detection']['detection_settings']['number_lines_no_limit'])

        # Tokenization -> Sentence Tokenization
        for lang_code in settings['sentence_tokenization']['sentence_tokenizers']:
            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].blockSignals(True)

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].setCurrentText(settings['sentence_tokenization']['sentence_tokenizers'][lang_code])

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].blockSignals(False)

        if not defaults:
            self.combo_box_sentence_tokenization_preview_lang.blockSignals(True)
            self.text_edit_sentence_tokenization_preview_samples.blockSignals(True)

            self.combo_box_sentence_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['sentence_tokenization']['preview_lang']))
            self.text_edit_sentence_tokenization_preview_samples.setText(settings['sentence_tokenization']['preview_samples'])
            self.text_edit_sentence_tokenization_preview_results.setText(settings['sentence_tokenization']['preview_results'])

            self.combo_box_sentence_tokenization_preview_lang.blockSignals(False)
            self.text_edit_sentence_tokenization_preview_samples.blockSignals(False)

        # Tokenization -> Word Tokenization
        for lang_code in settings['word_tokenization']['word_tokenizers']:
            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].blockSignals(True)

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].setCurrentText(settings['word_tokenization']['word_tokenizers'][lang_code])

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].blockSignals(False)

        if not defaults:
            self.combo_box_word_tokenization_preview_lang.blockSignals(True)
            self.text_edit_word_tokenization_preview_samples.blockSignals(True)

            self.combo_box_word_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['word_tokenization']['preview_lang']))
            self.text_edit_word_tokenization_preview_samples.setText(settings['word_tokenization']['preview_samples'])
            self.text_edit_word_tokenization_preview_results.setText(settings['word_tokenization']['preview_results'])

            self.combo_box_word_tokenization_preview_lang.blockSignals(False)
            self.text_edit_word_tokenization_preview_samples.blockSignals(False)

        # Tokenization -> Word Detokenization
        for lang_code in settings['word_detokenization']['word_detokenizers']:
            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].blockSignals(True)

            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].setCurrentText(settings['word_detokenization']['word_detokenizers'][lang_code])

            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].blockSignals(False)

        if not defaults:
            self.combo_box_word_detokenization_preview_lang.blockSignals(True)
            self.text_edit_word_detokenization_preview_samples.blockSignals(True)

            self.combo_box_word_detokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['word_detokenization']['preview_lang']))
            self.text_edit_word_detokenization_preview_samples.setText(settings['word_detokenization']['preview_samples'])
            self.text_edit_word_detokenization_preview_results.setText(settings['word_detokenization']['preview_results'])

            self.combo_box_word_detokenization_preview_lang.blockSignals(False)
            self.text_edit_word_detokenization_preview_samples.blockSignals(False)

        # POS Tagging
        for lang_code in settings['pos_tagging']['pos_taggers']:
            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].blockSignals(True)
            self.__dict__[f'combo_box_tagset_{lang_code}'].blockSignals(True)

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].setCurrentText(settings['pos_tagging']['pos_taggers'][lang_code])
            self.__dict__[f'combo_box_tagset_{lang_code}'].setCurrentText(settings['pos_tagging']['tagsets'][lang_code])

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].blockSignals(False)
            self.__dict__[f'combo_box_tagset_{lang_code}'].blockSignals(False)

        if not defaults:
            self.combo_box_pos_tagging_preview_lang.blockSignals(True)
            self.text_edit_pos_tagging_preview_samples.blockSignals(True)

            self.combo_box_pos_tagging_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['pos_tagging']['preview_lang']))
            self.text_edit_pos_tagging_preview_samples.setText(settings['pos_tagging']['preview_samples'])
            self.text_edit_pos_tagging_preview_results.setText(settings['pos_tagging']['preview_results'])

            self.combo_box_pos_tagging_preview_lang.blockSignals(False)
            self.text_edit_pos_tagging_preview_samples.blockSignals(False)

        # Lemmatization
        for lang_code in settings['lemmatization']['lemmatizers']:
            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].blockSignals(True)

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].setCurrentText(settings['lemmatization']['lemmatizers'][lang_code])

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].blockSignals(False)

        if not defaults:
            self.combo_box_lemmatization_preview_lang.blockSignals(True)
            self.text_edit_lemmatization_preview_samples.blockSignals(True)

            self.combo_box_lemmatization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['lemmatization']['preview_lang']))
            self.text_edit_lemmatization_preview_samples.setText(settings['lemmatization']['preview_samples'])
            self.text_edit_lemmatization_preview_results.setText(settings['lemmatization']['preview_results'])

            self.combo_box_lemmatization_preview_lang.blockSignals(False)
            self.text_edit_lemmatization_preview_samples.blockSignals(False)

        # Stop Words
        for lang_code in settings['stop_words']['stop_words']:
            self.__dict__[f'combo_box_stop_words_{lang_code}'].setCurrentText(settings['stop_words']['stop_words'][lang_code])

        if not defaults:
            self.combo_box_stop_words_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings['stop_words']['preview_lang']))

        # Measures -> Dispersion
        self.spin_box_dispersion_number_sections.setValue(settings['measures']['dispersion']['general']['number_sections'])

        # Measures -> Adjusted Frequency
        self.spin_box_adjusted_freq_number_sections.setValue(settings['measures']['adjusted_freq']['general']['number_sections'])
        self.checkbox_use_same_settings_dispersion.setChecked(settings['measures']['adjusted_freq']['general']['use_same_settings_dispersion'])

        # Measures -> Statistical Significance
        self.combo_box_z_score_direction.setCurrentText(settings['measures']['statistical_significance']['z_score']['direction'])

        self.spin_box_students_t_test_two_sample_number_sections.setValue(settings['measures']['statistical_significance']['students_t_test_two_sample']['number_sections'])
        self.combo_box_students_t_test_two_sample_use_data.setCurrentText(settings['measures']['statistical_significance']['students_t_test_two_sample']['use_data'])
        self.combo_box_students_t_test_two_sample_variances.setCurrentText(settings['measures']['statistical_significance']['students_t_test_two_sample']['variances'])

        self.checkbox_pearsons_chi_squared_test_apply_correction.setChecked(settings['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'])

        self.combo_box_fishers_exact_test_direction.setCurrentText(settings['measures']['statistical_significance']['fishers_exact_test']['direction'])

        self.spin_box_mann_whitney_u_test_number_sections.setValue(settings['measures']['statistical_significance']['mann_whitney_u_test']['number_sections'])
        self.combo_box_mann_whitney_u_test_use_data.setCurrentText(settings['measures']['statistical_significance']['mann_whitney_u_test']['use_data'])
        self.combo_box_mann_whitney_u_test_direction.setCurrentText(settings['measures']['statistical_significance']['mann_whitney_u_test']['direction'])
        self.checkbox_mann_whitney_u_test_apply_correction.setChecked(settings['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction'])

        # Measures -> Effect Size
        self.spin_box_kilgarriffs_ratio_smoothing_parameter.setValue(settings['measures']['effect_size']['kilgarriffs_ratio']['smoothing_parameter'])

    def restore_default_settings(self):
        reply = wordless_message_box.wordless_message_box_restore_default_settings(self.main)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

    def settings_validate(self):
        def validate_path(line_edit):
            if not os.path.exists(line_edit.text()):
                wordless_message_box.wordless_message_box_path_not_exist(self.main, line_edit.text())

                line_edit.setFocus()
                line_edit.selectAll()

                return False
            elif not os.path.isdir(line_edit.text()):
                wordless_message_box.wordless_message_box_path_not_dir(self.main, line_edit.text())

                line_edit.setFocus()
                line_edit.selectAll()

                return False
            else:
                return True

        if self.tree_settings.item_selected_old.text(0) == self.tr('General'):
            if validate_path(self.line_edit_file_default_path):
                return True
        elif self.tree_settings.item_selected_old.text(0) == self.tr('Import'):
            if validate_path(self.line_edit_import_search_terms_default_path):
                return True
        elif self.tree_settings.item_selected_old.text(0) == self.tr('Export'):
            if (validate_path(self.line_edit_export_tables_default_path) and
                validate_path(self.line_edit_export_search_terms_default_path)):
                return True
        else:
            return True

    def settings_save(self):
        settings_valid = self.settings_apply()

        if settings_valid:
            self.accept()

    def settings_apply(self):
        settings_valid = self.settings_validate()

        if settings_valid:
            settings = self.main.settings_custom

            # General
            settings['general']['file_default_path'] = self.line_edit_file_default_path.text()
            settings['general']['file_default_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_file_default_lang.currentText())
            settings['general']['file_default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_file_default_encoding.currentText())

            settings['general']['precision_decimal'] = self.spin_box_precision_decimal.value()
            settings['general']['precision_pct'] = self.spin_box_precision_pct.value()
            settings['general']['precision_p_value'] = self.spin_box_precision_p_value.value()

            # General -> Import
            settings['import']['search_terms_default_path'] = self.line_edit_import_search_terms_default_path.text()
            settings['import']['search_terms_default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_import_search_terms_default_encoding.currentText())

            # General -> Export
            settings['export']['tables_default_path'] = self.line_edit_export_tables_default_path.text()
            settings['export']['tables_default_type'] = self.combo_box_export_tables_default_type.currentText()
            settings['export']['tables_default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_tables_default_encoding.currentText())

            settings['export']['search_terms_default_path'] = self.line_edit_export_search_terms_default_path.text()
            settings['export']['search_terms_default_encoding'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_export_search_terms_default_encoding.currentText())

            # Auto-detection -> Language Detection
            settings['lang_detection']['detection_settings']['detection_engine'] = self.combo_box_lang_detection_engine.currentText()
            settings['lang_detection']['detection_settings']['number_lines'] = self.spin_box_lang_detection_number_lines.value()
            settings['lang_detection']['detection_settings']['number_lines_no_limit'] = self.checkbox_lang_detection_number_lines_no_limit.isChecked()

            # Tokenization -> Sentence Tokenization
            for lang_code in settings['sentence_tokenization']['sentence_tokenizers']:
                settings['sentence_tokenization']['sentence_tokenizers'][lang_code] = self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentText()

            # Tokenization -> Word Tokenization
            for lang_code in settings['word_tokenization']['word_tokenizers']:
                settings['word_tokenization']['word_tokenizers'][lang_code] = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()

            # Tokenization -> Word Detokenization
            for lang_code in settings['word_detokenization']['word_detokenizers']:
                settings['word_detokenization']['word_detokenizers'][lang_code] = self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].currentText()

            # POS Tagging
            for lang_code in settings['pos_tagging']['pos_taggers']:
                settings['pos_tagging']['pos_taggers'][lang_code] = self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentText()
                settings['pos_tagging']['tagsets'][lang_code] = self.__dict__[f'combo_box_tagset_{lang_code}'].currentText()

            # Lemmatization
            for lang_code in settings['lemmatization']['lemmatizers']:
                settings['lemmatization']['lemmatizers'][lang_code] = self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentText()

            # Stop Words
            for lang_code in settings['stop_words']['stop_words']:
                settings['stop_words']['stop_words'][lang_code] = self.__dict__[f'combo_box_stop_words_{lang_code}'].currentText()

            # Measures -> Dispersion
            settings['measures']['dispersion']['general']['number_sections'] = self.spin_box_dispersion_number_sections.value()

            # Measures -> Adjusted Frequency
            settings['measures']['adjusted_freq']['general']['number_sections'] = self.spin_box_adjusted_freq_number_sections.value()
            settings['measures']['adjusted_freq']['general']['use_same_settings_dispersion'] = self.checkbox_use_same_settings_dispersion.isChecked()

            # Measures -> Statistical Significance
            settings['measures']['statistical_significance']['z_score']['direction'] = self.combo_box_z_score_direction.currentText()

            settings['measures']['statistical_significance']['students_t_test_two_sample']['number_sections'] = self.spin_box_students_t_test_two_sample_number_sections.value()
            settings['measures']['statistical_significance']['students_t_test_two_sample']['use_data'] = self.combo_box_students_t_test_two_sample_use_data.currentText()
            settings['measures']['statistical_significance']['students_t_test_two_sample']['variances'] = self.combo_box_students_t_test_two_sample_variances.currentText()

            settings['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = self.checkbox_pearsons_chi_squared_test_apply_correction.isChecked()

            settings['measures']['statistical_significance']['fishers_exact_test']['direction'] = self.combo_box_fishers_exact_test_direction.currentText()

            settings['measures']['statistical_significance']['mann_whitney_u_test']['number_sections'] = self.spin_box_mann_whitney_u_test_number_sections.value()
            settings['measures']['statistical_significance']['mann_whitney_u_test']['use_data'] = self.combo_box_mann_whitney_u_test_use_data.currentText()
            settings['measures']['statistical_significance']['mann_whitney_u_test']['direction'] = self.combo_box_mann_whitney_u_test_direction.currentText()
            settings['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction'] = self.checkbox_mann_whitney_u_test_apply_correction.isChecked()

            # Measures -> Effect Size
            settings['measures']['effect_size']['kilgarriffs_ratio']['smoothing_parameter'] = self.spin_box_kilgarriffs_ratio_smoothing_parameter.value()

            self.wordless_settings_changed.emit()

        return settings_valid

    def load(self, tab = None):
        self.load_settings()

        if tab:
            item_selected = self.tree_settings.findItems(tab, Qt.MatchRecursive)[0]

            self.tree_settings.item_selected_old = item_selected

            self.tree_settings.clearSelection()
            item_selected.setSelected(True)

            if not self.tree_settings.findItems(tab, Qt.MatchExactly):
                item_selected.parent().setExpanded(True)

        self.exec()
