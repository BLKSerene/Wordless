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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

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

    def __init__(self, parent):
        super().__init__(parent)

        self.main = parent

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedSize(800, 550)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('General')]))
        self.tree_settings.topLevelItem(0).addChild(QTreeWidgetItem(self.tree_settings.topLevelItem(0), [self.tr('Import')]))
        self.tree_settings.topLevelItem(0).addChild(QTreeWidgetItem(self.tree_settings.topLevelItem(0), [self.tr('Export')]))

        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Sentence Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Word Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Word Detokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('POS Tagging')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Lemmatization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Stop Words')]))

        self.tree_settings.itemSelectionChanged.connect(self.selection_changed)

        self.scroll_area_settings = wordless_layout.Wordless_Scroll_Area(self.main)

        self.wrapper_settings_general = self.init_settings_general()
        self.wrapper_settings_import = self.init_settings_import()
        self.wrapper_settings_export = self.init_settings_export()

        self.wrapper_settings_sentence_tokenization = self.init_settings_sentence_tokenization()
        self.wrapper_settings_word_tokenization = self.init_settings_word_tokenization()
        self.wrapper_settings_word_detokenization = self.init_settings_word_detokenization()
        self.wrapper_settings_pos_tagging = self.init_settings_pos_tagging()
        self.wrapper_settings_lemmatization = self.init_settings_lemmatization()
        self.wrapper_settings_stop_words = self.init_settings_stop_words()

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

    def selection_changed(self):
        if self.settings_validate():
            self.wrapper_settings_general.hide()
            self.wrapper_settings_import.hide()
            self.wrapper_settings_export.hide()

            self.wrapper_settings_sentence_tokenization.hide()
            self.wrapper_settings_word_tokenization.hide()
            self.wrapper_settings_pos_tagging.hide()
            self.wrapper_settings_lemmatization.hide()
            self.wrapper_settings_stop_words.hide()

            self.scroll_area_settings.takeWidget()

            item_selected = self.tree_settings.selectedItems()[0]

            if item_selected.text(0) == self.tr('General'):
                settings_cur = self.wrapper_settings_general
            elif item_selected.text(0) == self.tr('Import'):
                settings_cur = self.wrapper_settings_import
            elif item_selected.text(0) == self.tr('Export'):
                settings_cur = self.wrapper_settings_export

            elif item_selected.text(0) == self.tr('Sentence Tokenization'):
                settings_cur = self.wrapper_settings_sentence_tokenization
            elif item_selected.text(0) == self.tr('Word Tokenization'):
                settings_cur = self.wrapper_settings_word_tokenization
            elif item_selected.text(0) == self.tr('Word Detokenization'):
                settings_cur = self.wrapper_settings_word_detokenization
            elif item_selected.text(0) == self.tr('POS Tagging'):
                settings_cur = self.wrapper_settings_pos_tagging
            elif item_selected.text(0) == self.tr('Lemmatization'):
                settings_cur = self.wrapper_settings_lemmatization
            elif item_selected.text(0) == self.tr('Stop Words'):
                settings_cur = self.wrapper_settings_stop_words

            settings_cur.show()

            self.scroll_area_settings.setWidget(settings_cur)

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

        wrapper_settings_general = QWidget(self)

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

        wrapper_settings_general.setLayout(QGridLayout())
        wrapper_settings_general.layout().addWidget(group_box_file_settings, 0, 0, Qt.AlignTop)
        wrapper_settings_general.layout().addWidget(group_box_precision_settings, 1, 0, Qt.AlignTop)

        wrapper_settings_general.layout().setRowStretch(2, 1)

        return wrapper_settings_general

    def init_settings_import(self):
        def browse_search_terms():
            path_file = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Browse'),
                                                         self.main.settings_custom['import']['search_terms_default_path'])

            if path_file:
                self.line_edit_import_search_terms_default_path.setText(path_file)

        wrapper_settings_import = QWidget(self)

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

        wrapper_settings_import.setLayout(QGridLayout())
        wrapper_settings_import.layout().addWidget(group_box_import_search_terms, 0, 0, Qt.AlignTop)

        return wrapper_settings_import

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

        wrapper_settings_export = QWidget(self)

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

        wrapper_settings_export.setLayout(QGridLayout())
        wrapper_settings_export.layout().addWidget(group_box_export_tables, 0, 0, Qt.AlignTop)
        wrapper_settings_export.layout().addWidget(group_box_export_search_terms, 1, 0, Qt.AlignTop)

        wrapper_settings_export.layout().setRowStretch(2, 1)

        tables_default_type_changed()

        return wrapper_settings_export

    def init_settings_sentence_tokenization(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_sentence_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_sentence_tokenization_preview_samples.toPlainText()

        def preview_results_changed():
            results = []

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_sentence_tokenization_preview_lang.currentText())

                sentence_tokenizer = self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentText()

                if settings_custom['preview_samples']:
                    for line in settings_custom['preview_samples'].splitlines():
                        results.extend(wordless_text.wordless_sentence_tokenize(self.main, line, lang_code,
                                                                                sentence_tokenizer = sentence_tokenizer))

                self.text_edit_sentence_tokenization_preview_results.setPlainText('\n'.join(results))
            else:
                self.text_edit_sentence_tokenization_preview_results.clear()

        settings_global = self.main.settings_global['sentence_tokenizers']
        settings_custom = self.main.settings_custom['sentence_tokenization']

        wrapper_settings_sentence_tokenization = QWidget(self)

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

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_sentence_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'])

        group_box_sentence_tokenizer_settings.setLayout(QGridLayout())
        group_box_sentence_tokenizer_settings.layout().addWidget(table_sentence_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_sentence_tokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_sentence_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_sentence_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_sentence_tokenization_preview_results = QTextEdit(self)

        self.combo_box_sentence_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))


        self.text_edit_sentence_tokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_sentence_tokenization_preview_results.setReadOnly(True)

        self.combo_box_sentence_tokenization_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_sentence_tokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_sentence_tokenization_preview_samples.textChanged.connect(preview_settings_changed)
        self.text_edit_sentence_tokenization_preview_samples.textChanged.connect(preview_results_changed)

        layout_preview_lang = QGridLayout()
        layout_preview_lang.addWidget(self.label_sentence_tokenization_preview_lang, 0, 0)
        layout_preview_lang.addWidget(self.combo_box_sentence_tokenization_preview_lang, 0, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_lang, 0, 0, 1, 2, Qt.AlignLeft)
        group_box_preview.layout().addWidget(self.text_edit_sentence_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_sentence_tokenization_preview_results, 1, 1)

        wrapper_settings_sentence_tokenization.setLayout(QGridLayout())
        wrapper_settings_sentence_tokenization.layout().addWidget(group_box_sentence_tokenizer_settings, 0, 0)
        wrapper_settings_sentence_tokenization.layout().addWidget(group_box_preview, 1, 0)

        wrapper_settings_sentence_tokenization.layout().setRowStretch(0, 2)
        wrapper_settings_sentence_tokenization.layout().setRowStretch(1, 1)

        preview_results_changed()

        return wrapper_settings_sentence_tokenization

    def init_settings_word_tokenization(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_tokenization_preview_samples.toPlainText()

        def preview_results_changed():
            results = []

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())

                word_tokenizer = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()

                for line in settings_custom['preview_samples'].splitlines():
                    sentences = wordless_text.wordless_sentence_tokenize(self.main, line, lang_code)
                    tokens = wordless_text.wordless_word_tokenize(self.main, sentences, lang_code,
                                                                  word_tokenizer = word_tokenizer)
                    
                    results.append(' '.join(tokens))

                self.text_edit_word_tokenization_preview_results.setPlainText('\n'.join(results))
            else:
                self.text_edit_word_tokenization_preview_results.clear()

        settings_global = self.main.settings_global['word_tokenizers']
        settings_custom = self.main.settings_custom['word_tokenization']

        wrapper_settings_word_tokenization = QWidget(self)

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

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self)

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_word_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_word_tokenizer_{lang_code}'])

        group_box_word_tokenizer_settings.setLayout(QGridLayout())
        group_box_word_tokenizer_settings.layout().addWidget(table_word_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_tokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_word_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_word_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_word_tokenization_preview_results = QTextEdit(self)

        self.combo_box_word_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_word_tokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_word_tokenization_preview_results.setReadOnly(True)

        self.combo_box_word_tokenization_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_word_tokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_word_tokenization_preview_samples.textChanged.connect(preview_settings_changed)
        self.text_edit_word_tokenization_preview_samples.textChanged.connect(preview_results_changed)

        layout_preview_lang = QGridLayout()
        layout_preview_lang.addWidget(self.label_word_tokenization_preview_lang, 0, 0)
        layout_preview_lang.addWidget(self.combo_box_word_tokenization_preview_lang, 0, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_lang, 0, 0, 1, 2, Qt.AlignLeft)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_results, 1, 1)

        wrapper_settings_word_tokenization.setLayout(QGridLayout())
        wrapper_settings_word_tokenization.layout().addWidget(group_box_word_tokenizer_settings, 0, 0,)
        wrapper_settings_word_tokenization.layout().addWidget(group_box_preview, 1, 0)

        wrapper_settings_word_tokenization.layout().setRowStretch(0, 2)
        wrapper_settings_word_tokenization.layout().setRowStretch(1, 1)

        preview_results_changed()

        return wrapper_settings_word_tokenization

    def init_settings_word_detokenization(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_detokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_detokenization_preview_samples.toPlainText()

        def preview_results_changed():
            results = []

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_word_detokenization_preview_lang.currentText())

                word_detokenizer = self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].currentText()

                for line in settings_custom['preview_samples'].splitlines():
                    text = wordless_text.wordless_word_detokenize(self.main, line.split(), lang_code,
                                                                  word_detokenizer = word_detokenizer)
                    
                    results.append(text)

                self.text_edit_word_detokenization_preview_results.setPlainText('\n'.join(results))
            else:
                self.text_edit_word_detokenization_preview_results.clear()

        settings_global = self.main.settings_global['word_detokenizers']
        settings_custom = self.main.settings_custom['word_detokenization']

        wrapper_settings_word_detokenization = QWidget(self)

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

            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_word_detokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_word_detokenizer_{lang_code}'])

        group_box_word_detokenizer_settings.setLayout(QGridLayout())
        group_box_word_detokenizer_settings.layout().addWidget(table_word_detokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_detokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_word_detokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_word_detokenization_preview_samples = QTextEdit(self)
        self.text_edit_word_detokenization_preview_results = QTextEdit(self)

        self.combo_box_word_detokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_word_detokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_word_detokenization_preview_results.setReadOnly(True)

        self.combo_box_word_detokenization_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_word_detokenization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_word_detokenization_preview_samples.textChanged.connect(preview_settings_changed)
        self.text_edit_word_detokenization_preview_samples.textChanged.connect(preview_results_changed)

        layout_preview_lang = QGridLayout()
        layout_preview_lang.addWidget(self.label_word_detokenization_preview_lang, 0, 0)
        layout_preview_lang.addWidget(self.combo_box_word_detokenization_preview_lang, 0, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_lang, 0, 0, 1, 2, Qt.AlignLeft)
        group_box_preview.layout().addWidget(self.text_edit_word_detokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_detokenization_preview_results, 1, 1)

        wrapper_settings_word_detokenization.setLayout(QGridLayout())
        wrapper_settings_word_detokenization.layout().addWidget(group_box_word_detokenizer_settings, 0, 0,)
        wrapper_settings_word_detokenization.layout().addWidget(group_box_preview, 1, 0)

        wrapper_settings_word_detokenization.layout().setRowStretch(0, 2)
        wrapper_settings_word_detokenization.layout().setRowStretch(1, 1)

        preview_results_changed()

        return wrapper_settings_word_detokenization

    def init_settings_pos_tagging(self):
        def pos_tagger_changed():
            for i, lang_code in enumerate(settings_global):
                pos_tagger = self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentText()
                tagset_old = self.__dict__[f'combo_box_tagset_{lang_code}'].currentText()

                table_pos_taggers.cellWidget(i, 2).blockSignals(True)

                table_pos_taggers.cellWidget(i, 2).clear()
                table_pos_taggers.cellWidget(i, 2).addItems([self.main.settings_global['pos_taggers'][lang_code][pos_tagger], 'Universal'])

                table_pos_taggers.cellWidget(i, 2).blockSignals(False)

                if tagset_old == 'Universal':
                    self.__dict__[f'combo_box_tagset_{lang_code}'].setCurrentText('Universal')

            preview_results_changed()

        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_pos_tagging_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_pos_tagging_preview_samples.toPlainText()

        def preview_results_changed():
            results = []

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_pos_tagging_preview_lang.currentText())

                pos_tagger = self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentText()
                tagset = self.__dict__[f'combo_box_tagset_{lang_code}'].currentText()

                for sample_line in settings_custom['preview_samples'].splitlines():
                    tokens_tagged = wordless_text.wordless_pos_tag(self.main, sample_line, lang_code,
                                                                   pos_tagger = pos_tagger, tagset = tagset)
                    results.append(' '.join([f'{token}_{tag}' for token, tag in tokens_tagged]))

                self.text_edit_pos_tagging_preview_results.setPlainText('\n'.join(results))
            else:
                self.text_edit_pos_tagging_preview_results.clear()

        settings_global = self.main.settings_global['pos_taggers']
        settings_custom = self.main.settings_custom['pos_tagging']

        wrapper_settings_pos_tagging = QWidget(self)

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

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self)

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].addItems(list(settings_global[lang_code].keys()))

            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentTextChanged.connect(pos_tagger_changed)
            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_pos_taggers.setCellWidget(i, 1, self.__dict__[f'combo_box_pos_tagger_{lang_code}'])

            self.__dict__[f'combo_box_tagset_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_tagset_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_pos_taggers.setCellWidget(i, 2, self.__dict__[f'combo_box_tagset_{lang_code}'])

        group_box_pos_tagger_settings.setLayout(QGridLayout())
        group_box_pos_tagger_settings.layout().addWidget(table_pos_taggers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_pos_tagging_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_pos_tagging_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_pos_tagging_preview_samples = QTextEdit(self)
        self.text_edit_pos_tagging_preview_results = QTextEdit(self)

        self.combo_box_pos_tagging_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_pos_tagging_preview_samples.setAcceptRichText(False)
        self.text_edit_pos_tagging_preview_results.setReadOnly(True)

        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_pos_tagging_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(preview_settings_changed)
        self.text_edit_pos_tagging_preview_samples.textChanged.connect(preview_results_changed)

        layout_preview_lang = QGridLayout()
        layout_preview_lang.addWidget(self.label_pos_tagging_preview_lang, 0, 0)
        layout_preview_lang.addWidget(self.combo_box_pos_tagging_preview_lang, 0, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_lang, 0, 0, 1, 2, Qt.AlignLeft)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_pos_tagging_preview_results, 1, 1)

        wrapper_settings_pos_tagging.setLayout(QGridLayout())
        wrapper_settings_pos_tagging.layout().addWidget(group_box_pos_tagger_settings, 0, 0)
        wrapper_settings_pos_tagging.layout().addWidget(group_box_preview, 1, 0)

        wrapper_settings_pos_tagging.layout().setRowStretch(0, 2)
        wrapper_settings_pos_tagging.layout().setRowStretch(1, 1)

        pos_tagger_changed()

        return wrapper_settings_pos_tagging

    def init_settings_lemmatization(self):
        def preview_settings_changed():
            lang_text = self.combo_box_lemmatization_preview_lang.currentText()

            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, lang_text)
            settings_custom['preview_samples'] = self.text_edit_lemmatization_preview_samples.toPlainText()

        def preview_results_changed():
            results = []

            if settings_custom['preview_samples']:
                lang_text = self.combo_box_lemmatization_preview_lang.currentText()
                lang_code = wordless_conversion.to_lang_code(self.main, lang_text)
                lemmatizer = self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentText()

                for sample_line in settings_custom['preview_samples'].splitlines():
                    samples = wordless_text.wordless_word_tokenize(self.main, sample_line, lang_code)
                    lemmas = wordless_text.wordless_lemmatize(self.main, samples, lang_code, lemmatizer = lemmatizer)

                    results.append(wordless_text.wordless_word_detokenize(self.main, lemmas, lang_code))

                self.text_edit_lemmatization_preview_results.setPlainText('\n'.join(results))
            else:
                self.text_edit_lemmatization_preview_results.clear()

        settings_global = self.main.settings_global['lemmatizers']
        settings_custom = self.main.settings_custom['lemmatization']

        wrapper_settings_lemmatization = QWidget(self)

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

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)

            table_lemmatizers.setCellWidget(i, 1, self.__dict__[f'combo_box_lemmatizer_{lang_code}'])

        group_box_lemmatizer_settings.setLayout(QGridLayout())
        group_box_lemmatizer_settings.layout().addWidget(table_lemmatizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_lemmatization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_lemmatization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_lemmatization_preview_samples = QTextEdit(self)
        self.text_edit_lemmatization_preview_results = QTextEdit(self)

        self.combo_box_lemmatization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_lemmatization_preview_samples.setAcceptRichText(False)
        self.text_edit_lemmatization_preview_results.setReadOnly(True)

        self.combo_box_lemmatization_preview_lang.currentTextChanged.connect(preview_settings_changed)
        self.combo_box_lemmatization_preview_lang.currentTextChanged.connect(preview_results_changed)
        self.text_edit_lemmatization_preview_samples.textChanged.connect(preview_settings_changed)
        self.text_edit_lemmatization_preview_samples.textChanged.connect(preview_results_changed)

        layout_preview_lang = QGridLayout()
        layout_preview_lang.addWidget(self.label_lemmatization_preview_lang, 0, 0)
        layout_preview_lang.addWidget(self.combo_box_lemmatization_preview_lang, 0, 1)

        group_box_preview.setLayout(QGridLayout())
        group_box_preview.layout().addLayout(layout_preview_lang, 0, 0, 1, 2, Qt.AlignLeft)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_results, 1, 1)

        wrapper_settings_lemmatization.setLayout(QGridLayout())
        wrapper_settings_lemmatization.layout().addWidget(group_box_lemmatizer_settings, 0, 0)
        wrapper_settings_lemmatization.layout().addWidget(group_box_preview, 1, 0)

        wrapper_settings_lemmatization.layout().setRowStretch(0, 2)
        wrapper_settings_lemmatization.layout().setRowStretch(1, 1)

        preview_results_changed()

        return wrapper_settings_lemmatization

    def init_settings_stop_words(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_stop_words_preview_lang.currentText())

        def preview_results_changed():
            lang_text = self.combo_box_stop_words_preview_lang.currentText()
            lang_code_639_3 = wordless_conversion.to_lang_code(self.main, lang_text)
            lang_code_639_1 = wordless_conversion.to_iso_639_1(self.main, lang_code_639_3)

            if lang_code_639_1 == 'zh_CN':
                lang_code_639_1 = 'zh'

            word_list = self.__dict__[f'combo_box_stop_words_{lang_code_639_3}'].currentText()

            if word_list == 'NLTK':
                stop_words = nltk.corpus.stopwords.words(lang_text)
            elif word_list == 'Stopwords ISO':
                if lang_code_639_1 == 'zh_TW':
                    with open(r'stop_words/Stopwords ISO/stopwords_zh_TW.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]
                else:
                    with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                        stop_words = json.load(f)[lang_code_639_1]
            elif word_list == 'stopwords-json':
                if lang_code_639_1 == 'zh_TW':
                    with open(r'stop_words/stopwords-json/stopwords_zh_TW.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]
                else:
                    with open(r'stop_words/stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
                        stop_words = json.load(f)[lang_code_639_1]
            elif word_list == 'HanLP':
                if lang_code_639_1 == 'zh_TW':
                    with open(r'stop_words/HanLP/stopwords_zh_TW.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]
                else:
                    with open(r'stop_words/HanLP/stopwords.txt', 'r', encoding = 'utf_8') as f:
                        stop_words = [line.rstrip() for line in f]

            self.label_stop_words_preview_count.setText(self.tr(f'Count of Stop Words: {len(stop_words)}'))
            self.table_stop_words_preview_results.set_items(stop_words)

        settings_global = self.main.settings_global['stop_words']
        settings_custom = self.main.settings_custom['stop_words']

        wrapper_settings_stop_words = QWidget(self)

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

        wrapper_settings_stop_words.setLayout(QGridLayout())
        wrapper_settings_stop_words.layout().addWidget(group_box_stop_words_settings, 0, 0)
        wrapper_settings_stop_words.layout().addWidget(group_box_preview, 1, 0)

        wrapper_settings_stop_words.layout().setRowStretch(0, 2)
        wrapper_settings_stop_words.layout().setRowStretch(1, 1)

        preview_results_changed()

        return wrapper_settings_stop_words

    def load_settings(self, defaults = False):
        if defaults:
            settings_loaded = self.main.settings_default
        else:
            settings_loaded = copy.deepcopy(self.main.settings_custom)

        # General
        self.line_edit_file_default_path.setText(settings_loaded['general']['file_default_path'])
        self.combo_box_file_default_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['general']['file_default_lang']))
        self.combo_box_file_default_encoding.setCurrentText(settings_loaded['general']['file_default_encoding'])

        self.spin_box_precision_decimal.setValue(settings_loaded['general']['precision_decimal'])
        self.spin_box_precision_pct.setValue(settings_loaded['general']['precision_pct'])
        self.spin_box_precision_p_value.setValue(settings_loaded['general']['precision_p_value'])

        # Import
        self.line_edit_import_search_terms_default_path.setText(settings_loaded['import']['search_terms_default_path'])
        self.combo_box_import_search_terms_default_encoding.setCurrentText(settings_loaded['import']['search_terms_default_encoding'])

        # Export
        self.line_edit_export_tables_default_path.setText(settings_loaded['export']['tables_default_path'])
        self.combo_box_export_tables_default_type.setCurrentText(settings_loaded['export']['tables_default_type'])
        self.combo_box_export_tables_default_encoding.setCurrentText(settings_loaded['export']['tables_default_encoding'])

        self.line_edit_export_search_terms_default_path.setText(settings_loaded['export']['search_terms_default_path'])
        self.combo_box_export_search_terms_default_encoding.setCurrentText(settings_loaded['export']['search_terms_default_encoding'])

        # Sentence Tokenization
        for lang_code in settings_loaded['sentence_tokenization']['sentence_tokenizers']:
            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].setCurrentText(settings_loaded['sentence_tokenization']['sentence_tokenizers'][lang_code])

        self.combo_box_sentence_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['sentence_tokenization']['preview_lang']))
        self.text_edit_sentence_tokenization_preview_samples.setText(settings_loaded['sentence_tokenization']['preview_samples'])

        # Word Tokenization
        for lang_code in settings_loaded['word_tokenization']['word_tokenizers']:
            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].setCurrentText(settings_loaded['word_tokenization']['word_tokenizers'][lang_code])

        self.combo_box_word_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['word_tokenization']['preview_lang']))
        self.text_edit_word_tokenization_preview_samples.setText(settings_loaded['word_tokenization']['preview_samples'])

        # Word Detokenization
        for lang_code in settings_loaded['word_detokenization']['word_detokenizers']:
            self.__dict__[f'combo_box_word_detokenizer_{lang_code}'].setCurrentText(settings_loaded['word_detokenization']['word_detokenizers'][lang_code])

        self.combo_box_word_detokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['word_detokenization']['preview_lang']))
        self.text_edit_word_detokenization_preview_samples.setText(settings_loaded['word_detokenization']['preview_samples'])

        # POS Tagging
        for lang_code in settings_loaded['pos_tagging']['pos_taggers']:
            self.__dict__[f'combo_box_pos_tagger_{lang_code}'].setCurrentText(settings_loaded['pos_tagging']['pos_taggers'][lang_code])
            self.__dict__[f'combo_box_tagset_{lang_code}'].setCurrentText(settings_loaded['pos_tagging']['tagsets'][lang_code])

        self.combo_box_pos_tagging_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['pos_tagging']['preview_lang']))
        self.text_edit_pos_tagging_preview_samples.setText(settings_loaded['pos_tagging']['preview_samples'])

        # Lemmatization
        for lang_code in settings_loaded['lemmatization']['lemmatizers']:
            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].setCurrentText(settings_loaded['lemmatization']['lemmatizers'][lang_code])

        self.combo_box_lemmatization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['lemmatization']['preview_lang']))
        self.text_edit_lemmatization_preview_samples.setText(settings_loaded['lemmatization']['preview_samples'])

        # Stop Words
        for lang_code in settings_loaded['stop_words']['stop_words']:
            self.__dict__[f'combo_box_stop_words_{lang_code}'].setCurrentText(settings_loaded['stop_words']['stop_words'][lang_code])

        self.combo_box_stop_words_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['stop_words']['preview_lang']))

    def restore_default_settings(self):
        reply = wordless_message_box.wordless_restore_default_settings(self.main)

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
            settings['general']['file_default_encoding'] = self.combo_box_file_default_encoding.currentText()

            settings['general']['precision_decimal'] = self.spin_box_precision_decimal.value()
            settings['general']['precision_pct'] = self.spin_box_precision_pct.value()
            settings['general']['precision_p_value'] = self.spin_box_precision_p_value.value()

            # Import
            settings['import']['search_terms_default_path'] = self.line_edit_import_search_terms_default_path.text()
            settings['import']['search_terms_default_encoding'] = self.combo_box_import_search_terms_default_encoding.currentText()

            # Export
            settings['export']['tables_default_path'] = self.line_edit_export_tables_default_path.text()
            settings['export']['tables_default_type'] = self.combo_box_export_tables_default_type.currentText()
            settings['export']['tables_default_encoding'] = self.combo_box_export_tables_default_encoding.currentText()

            settings['export']['search_terms_default_path'] = self.line_edit_export_search_terms_default_path.text()
            settings['export']['search_terms_default_encoding'] = self.combo_box_export_search_terms_default_encoding.currentText()

            # Sentence Tokenization
            for lang_code in settings['sentence_tokenization']['sentence_tokenizers']:
                settings['sentence_tokenization']['sentence_tokenizers'][lang_code] = self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentText()

            # Word Tokenization
            for lang_code in settings['word_tokenization']['word_tokenizers']:
                settings['word_tokenization']['word_tokenizers'][lang_code] = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()

            # Word Detokenization
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

            self.wordless_settings_changed.emit()

        return settings_valid

    def load(self):
        self.load_settings()

        if not self.tree_settings.selectedItems():
            self.tree_settings.item_selected_old = self.tree_settings.topLevelItem(0)
            self.tree_settings.topLevelItem(0).setSelected(True)

        self.exec()
