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
        def selection_changed():
            self.settings_general.hide()
            self.settings_sentence_tokenization.hide()
            self.settings_word_tokenization.hide()
            self.settings_pos_tagging.hide()
            self.settings_lemmatization.hide()
            self.settings_stop_words.hide()

            selected_items = self.tree_settings.selectedItems()
            if not selected_items:
                self.tree_settings.findItems(self.tr('General'), Qt.MatchExactly)[0].setSelected(True)
            else:
                if selected_items[0].text(0) == 'General':
                    self.settings_general.show()
                elif selected_items[0].text(0) == 'Sentence Tokenization':
                    self.settings_sentence_tokenization.show()
                elif selected_items[0].text(0) == 'Word Tokenization':
                    self.settings_word_tokenization.show()
                elif selected_items[0].text(0) == 'POS Tagging':
                    self.settings_pos_tagging.show()
                elif selected_items[0].text(0) == 'Lemmatization':
                    self.settings_lemmatization.show()
                elif selected_items[0].text(0) == 'Stop Words':
                    self.settings_stop_words.show()

        super().__init__(parent)

        self.main = parent

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedSize(800, 600)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('General')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Sentence Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Word Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('POS Tagging')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Lemmatization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Stop Words')]))

        self.tree_settings.itemSelectionChanged.connect(selection_changed)

        wrapper_settings = QWidget()

        wrapper_settings.setLayout(QGridLayout())
        wrapper_settings.layout().addWidget(self.init_settings_general(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_sentence_tokenization(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_word_tokenization(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_pos_tagging(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_lemmatization(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_stop_words(), 0, 0)

        scroll_area_settings = wordless_layout.Wordless_Scroll_Area(self.main, wrapper_settings)

        button_restore_default_settings = QPushButton(self.tr('Restore Default Settings'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_restore_default_settings.clicked.connect(self.restore_default_settings)
        button_save.clicked.connect(self.save)
        button_apply.clicked.connect(self.apply)
        button_cancel.clicked.connect(self.reject)

        layout_buttons_right = QGridLayout()
        layout_buttons_right.addWidget(button_save, 0, 0)
        layout_buttons_right.addWidget(button_apply, 0, 1)
        layout_buttons_right.addWidget(button_cancel, 0, 2)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.tree_settings, 0, 0)
        self.layout().addWidget(scroll_area_settings, 0, 1)
        self.layout().addWidget(button_restore_default_settings, 1, 0)
        self.layout().addLayout(layout_buttons_right, 1, 1, Qt.AlignRight)

        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 3)

        selection_changed()

    def init_settings_general(self):
        def browse_open_files():
            path_open_files = QFileDialog.getExistingDirectory(self,
                                                               self.tr('Browse'),
                                                               self.main.settings_custom['general']['default_paths_open_files'])

            if path_open_files:
                self.line_edit_default_paths_open_files.setText(os.path.realpath(path_open_files))

        def browse_export():
            path_export = QFileDialog.getExistingDirectory(self,
                                                               self.tr('Browse'),
                                                               self.main.settings_custom['general']['default_paths_export'])

            if path_export:
                self.line_edit_default_paths_export.setText(os.path.realpath(path_export))

        self.settings_general = QWidget(self)

        # Default Encodings
        group_box_default_encoding = QGroupBox(self.tr('Default Encodings'), self)

        self.label_default_encoding_input = QLabel(self.tr('Input Encoding:'), self)
        self.combo_box_default_encoding_input = wordless_box.Wordless_Combo_Box_Encoding(self.main)
        self.label_default_encoding_output = QLabel(self.tr('Output Encoding:'), self)
        self.combo_box_default_encoding_output = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        group_box_default_encoding.setLayout(QGridLayout())
        group_box_default_encoding.layout().addWidget(self.label_default_encoding_input, 0, 0)
        group_box_default_encoding.layout().addWidget(self.combo_box_default_encoding_input, 0, 1)
        group_box_default_encoding.layout().addWidget(self.label_default_encoding_output, 1, 0)
        group_box_default_encoding.layout().addWidget(self.combo_box_default_encoding_output, 1, 1)

        # Default Paths
        group_box_default_paths = QGroupBox(self.tr('Default Paths'), self)

        self.label_default_paths_open_files = QLabel(self.tr('Open Files:'), self)
        self.line_edit_default_paths_open_files = QLineEdit(self)
        self.button_default_paths_open_files = QPushButton(self.tr('Browse'), self)
        self.label_default_paths_export = QLabel(self.tr('Export:'), self)
        self.line_edit_default_paths_export = QLineEdit(self)
        self.button_default_paths_export = QPushButton(self.tr('Browse'), self)

        self.button_default_paths_open_files.clicked.connect(browse_open_files)
        self.button_default_paths_export.clicked.connect(browse_export)

        group_box_default_paths.setLayout(QGridLayout())
        group_box_default_paths.layout().addWidget(self.label_default_paths_open_files, 0, 0)
        group_box_default_paths.layout().addWidget(self.line_edit_default_paths_open_files, 0, 1)
        group_box_default_paths.layout().addWidget(self.button_default_paths_open_files, 0, 2)
        group_box_default_paths.layout().addWidget(self.label_default_paths_export, 1, 0)
        group_box_default_paths.layout().addWidget(self.line_edit_default_paths_export, 1, 1)
        group_box_default_paths.layout().addWidget(self.button_default_paths_export, 1, 2)

        # Precision
        group_box_precision = QGroupBox(self.tr('Precision'), self)

        self.label_precision_decimal = QLabel(self.tr('Decimal:'), self)
        self.spin_box_precision_decimal = QSpinBox(self)
        self.label_precision_pct = QLabel(self.tr('Percentage:'), self)
        self.spin_box_precision_pct = QSpinBox(self)
        self.label_precision_p_value = QLabel(self.tr('p-value:'), self)
        self.spin_box_precision_p_value = QSpinBox(self)

        self.spin_box_precision_decimal.setRange(0, 10)
        self.spin_box_precision_pct.setRange(0, 10)
        self.spin_box_precision_p_value.setRange(0, 15)

        group_box_precision.setLayout(QGridLayout())
        group_box_precision.layout().addWidget(self.label_precision_decimal, 0, 0)
        group_box_precision.layout().addWidget(self.spin_box_precision_decimal, 0, 1)
        group_box_precision.layout().addWidget(self.label_precision_pct, 1, 0)
        group_box_precision.layout().addWidget(self.spin_box_precision_pct, 1, 1)
        group_box_precision.layout().addWidget(self.label_precision_p_value, 2, 0)
        group_box_precision.layout().addWidget(self.spin_box_precision_p_value, 2, 1)

        self.settings_general.setLayout(QGridLayout())
        self.settings_general.layout().addWidget(group_box_default_encoding, 0, 0, Qt.AlignTop)
        self.settings_general.layout().addWidget(group_box_default_paths, 1, 0, Qt.AlignTop)
        self.settings_general.layout().addWidget(group_box_precision, 2, 0, Qt.AlignTop)

        return self.settings_general

    def init_settings_sentence_tokenization(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_sentence_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_sentence_tokenization_preview_samples.toPlainText()

        def preview_results_changed():
            self.text_edit_sentence_tokenization_preview_results.clear()

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_sentence_tokenization_preview_lang.currentText())

                sentence_tokenizer = self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentText()

                if settings_custom['preview_samples']:
                    for sample_line in settings_custom['preview_samples'].split('\n'):
                        sentences = wordless_text.wordless_sentence_tokenize(self.main, sample_line, lang_code, sentence_tokenizer = sentence_tokenizer)

                        self.text_edit_sentence_tokenization_preview_results.append('<span style="color: #F00; font-weight: bold;">/</span>'.join(sentences) + '<span style="color: #F00; font-weight: bold;">/</span>')

        settings_global = self.main.settings_global['sentence_tokenizers']
        settings_custom = self.main.settings_custom['sentence_tokenization']

        self.settings_sentence_tokenization = QWidget(self)

        # Sentence Tokenizers
        group_box_sentence_tokenizers = QGroupBox(self.tr('Sentence Tokenizers'), self)
        wrapper_sentence_tokenizers = QWidget(self)

        for lang_code in settings_global:
            self.__dict__[f'label_sentence_tokenizer_{lang_code}'] = QLabel(wordless_conversion.to_lang_text(self.main, lang_code) + ':', self)
            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self)

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)
        wrapper_sentence_tokenizers.setLayout(QGridLayout())

        for i, lang_code in enumerate(settings_global):
            wrapper_sentence_tokenizers.layout().addWidget(self.__dict__[f'label_sentence_tokenizer_{lang_code}'], i, 0)
            wrapper_sentence_tokenizers.layout().addWidget(self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'], i, 1)

        scroll_area_sentence_tokenizers = wordless_layout.Wordless_Scroll_Area(self, wrapper_sentence_tokenizers)
        scroll_area_sentence_tokenizers.setFrameShape(QFrame.NoFrame)

        group_box_sentence_tokenizers.setLayout(QGridLayout())
        group_box_sentence_tokenizers.layout().addWidget(scroll_area_sentence_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_sentence_tokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_sentence_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_sentence_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_sentence_tokenization_preview_results = QTextEdit(self)

        self.combo_box_sentence_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

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

        self.settings_sentence_tokenization.setLayout(QGridLayout())
        self.settings_sentence_tokenization.layout().addWidget(group_box_sentence_tokenizers, 0, 0)
        self.settings_sentence_tokenization.layout().addWidget(group_box_preview, 1, 0)

        preview_results_changed()

        return self.settings_sentence_tokenization

    def init_settings_word_tokenization(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_tokenization_preview_samples.toPlainText()

        def preview_results_changed():
            self.text_edit_word_tokenization_preview_results.clear()

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())

                word_tokenizer = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()

                for sample_line in settings_custom['preview_samples'].split('\n'):
                    tokens = wordless_text.wordless_word_tokenize(self.main, sample_line, lang_code, word_tokenizer = word_tokenizer)

                    self.text_edit_word_tokenization_preview_results.append(' '.join(tokens))

        settings_global = self.main.settings_global['word_tokenizers']
        settings_custom = self.main.settings_custom['word_tokenization']

        self.settings_word_tokenization = QWidget(self)

        # Word Tokenizers
        group_box_word_tokenizers = QGroupBox(self.tr('Word Tokenizers'), self)
        wrapper_word_tokenizers = QWidget(self)

        for lang_code in settings_global:
            self.__dict__[f'label_word_tokenizer_{lang_code}'] = QLabel(wordless_conversion.to_lang_text(self.main, lang_code) + ':', self)
            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'] = wordless_box.Wordless_Combo_Box_Jre_Required(self)

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)
        wrapper_word_tokenizers.setLayout(QGridLayout())

        for i, lang_code in enumerate(settings_global):
            wrapper_word_tokenizers.layout().addWidget(self.__dict__[f'label_word_tokenizer_{lang_code}'], i, 0)
            wrapper_word_tokenizers.layout().addWidget(self.__dict__[f'combo_box_word_tokenizer_{lang_code}'], i, 1)

        scroll_area_word_tokenizers = wordless_layout.Wordless_Scroll_Area(self, wrapper_word_tokenizers)
        scroll_area_word_tokenizers.setFrameShape(QFrame.NoFrame)

        group_box_word_tokenizers.setLayout(QGridLayout())
        group_box_word_tokenizers.layout().addWidget(scroll_area_word_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_word_tokenization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_word_tokenization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_word_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_word_tokenization_preview_results = QTextEdit(self)

        self.combo_box_word_tokenization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

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

        self.settings_word_tokenization.setLayout(QGridLayout())
        self.settings_word_tokenization.layout().addWidget(group_box_word_tokenizers, 0, 0)
        self.settings_word_tokenization.layout().addWidget(group_box_preview, 1, 0)

        preview_results_changed()

        return self.settings_word_tokenization

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
            self.text_edit_pos_tagging_preview_results.clear()

            if settings_custom['preview_samples']:
                lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_pos_tagging_preview_lang.currentText())

                pos_tagger = self.__dict__[f'combo_box_pos_tagger_{lang_code}'].currentText()
                tagset = self.__dict__[f'combo_box_tagset_{lang_code}'].currentText()

                for sample_line in settings_custom['preview_samples'].split('\n'):
                    tokens_tagged = wordless_text.wordless_pos_tag(self.main, sample_line, lang_code,
                                                                   pos_tagger = pos_tagger, tagset = tagset)
                    tokens_tagged = [f'{token}_{tag}' for token, tag in tokens_tagged]

                    self.text_edit_pos_tagging_preview_results.append(' '.join(tokens_tagged))

        settings_global = self.main.settings_global['pos_taggers']
        settings_custom = self.main.settings_custom['pos_tagging']

        self.settings_pos_tagging = QWidget(self)

        # POS Taggers
        group_box_pos_taggers = QGroupBox(self.tr('POS Taggers'), self)
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

        group_box_pos_taggers.setLayout(QGridLayout())
        group_box_pos_taggers.layout().addWidget(table_pos_taggers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_pos_tagging_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_pos_tagging_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_pos_tagging_preview_samples = QTextEdit(self)
        self.text_edit_pos_tagging_preview_results = QTextEdit(self)

        self.combo_box_pos_tagging_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

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

        self.settings_pos_tagging.setLayout(QGridLayout())
        self.settings_pos_tagging.layout().addWidget(group_box_pos_taggers, 0, 0)
        self.settings_pos_tagging.layout().addWidget(group_box_preview, 1, 0)

        self.settings_pos_tagging.layout().setRowStretch(0, 2)
        self.settings_pos_tagging.layout().setRowStretch(1, 1)

        pos_tagger_changed()

        return self.settings_pos_tagging

    def init_settings_lemmatization(self):
        def preview_settings_changed():
            lang_text = self.combo_box_lemmatization_preview_lang.currentText()

            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, lang_text)
            settings_custom['preview_samples'] = self.text_edit_lemmatization_preview_samples.toPlainText()

        def preview_results_changed():
            self.text_edit_lemmatization_preview_results.clear()

            if settings_custom['preview_samples']:
                lang_text = self.combo_box_lemmatization_preview_lang.currentText()
                lang_code = wordless_conversion.to_lang_code(self.main, lang_text)
                lemmatizer = self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentText()

                for sample_line in settings_custom['preview_samples'].split('\n'):
                    samples = wordless_text.wordless_word_tokenize(self.main, sample_line, lang_code)
                    lemmas = wordless_text.wordless_lemmatize(self.main, samples, lang_code, lemmatizer = lemmatizer)

                    self.text_edit_lemmatization_preview_results.append(wordless_conversion.to_word_delimiter(lang_code).join(lemmas))

        settings_global = self.main.settings_global['lemmatizers']
        settings_custom = self.main.settings_custom['lemmatization']

        self.settings_lemmatization = QWidget(self)

        # Lemmatizers
        group_box_lemmatizers = QGroupBox(self.tr('Lemmatizers'), self)
        wrapper_lemmatizers = QWidget(self)

        for lang_code in settings_global:
            self.__dict__[f'label_lemmatizer_{lang_code}'] = QLabel(wordless_conversion.to_lang_text(self.main, lang_code) + ':', self)
            self.__dict__[f'combo_box_lemmatizer_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)

        wrapper_lemmatizers.setLayout(QGridLayout())

        for i, lang_code in enumerate(settings_global):
            wrapper_lemmatizers.layout().addWidget(self.__dict__[f'label_lemmatizer_{lang_code}'], i, 0)
            wrapper_lemmatizers.layout().addWidget(self.__dict__[f'combo_box_lemmatizer_{lang_code}'], i, 1)

        scroll_area_lemmatizers = wordless_layout.Wordless_Scroll_Area(self, wrapper_lemmatizers)
        scroll_area_lemmatizers.setFrameShape(QFrame.NoFrame)

        group_box_lemmatizers.setLayout(QGridLayout())
        group_box_lemmatizers.layout().addWidget(scroll_area_lemmatizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_lemmatization_preview_lang = QLabel(self.tr('Select a Language:'), self)
        self.combo_box_lemmatization_preview_lang = wordless_box.Wordless_Combo_Box(self)
        self.text_edit_lemmatization_preview_samples = QTextEdit(self)
        self.text_edit_lemmatization_preview_results = QTextEdit(self)

        self.combo_box_lemmatization_preview_lang.addItems(wordless_conversion.to_lang_text(self.main, list(settings_global.keys())))

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

        self.settings_lemmatization.setLayout(QGridLayout())
        self.settings_lemmatization.layout().addWidget(group_box_lemmatizers, 0, 0)
        self.settings_lemmatization.layout().addWidget(group_box_preview, 1, 0)

        preview_results_changed()

        return self.settings_lemmatization

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

        self.settings_stop_words = QWidget(self)

        # Stop Words
        group_box_stop_words = QGroupBox(self.tr('Stop Words'), self)
        wrapper_stop_words = QWidget(self)

        for lang_code in settings_global:
            self.__dict__[f'label_stop_words_{lang_code}'] = QLabel(wordless_conversion.to_lang_text(self.main, lang_code) + ':', self)
            self.__dict__[f'combo_box_stop_words_{lang_code}'] = wordless_box.Wordless_Combo_Box(self)

            self.__dict__[f'combo_box_stop_words_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_stop_words_{lang_code}'].currentTextChanged.connect(preview_results_changed)

        wrapper_stop_words.setLayout(QGridLayout())

        for i, lang_code in enumerate(settings_global):
            wrapper_stop_words.layout().addWidget(self.__dict__[f'label_stop_words_{lang_code}'], i, 0)
            wrapper_stop_words.layout().addWidget(self.__dict__[f'combo_box_stop_words_{lang_code}'], i, 1)

        scroll_area_stop_words = wordless_layout.Wordless_Scroll_Area(self, wrapper_stop_words)
        scroll_area_stop_words.setFrameShape(QFrame.NoFrame)

        group_box_stop_words.setLayout(QGridLayout())
        group_box_stop_words.layout().addWidget(scroll_area_stop_words, 0, 0)

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
        self.settings_stop_words.layout().addWidget(group_box_stop_words, 0, 0)
        self.settings_stop_words.layout().addWidget(group_box_preview, 1, 0)

        preview_results_changed()

        return self.settings_stop_words

    def load_settings(self, defaults = False):
        if defaults:
            settings_loaded = self.main.settings_default
        else:
            settings_loaded = copy.deepcopy(self.main.settings_custom)

        # General
        self.combo_box_default_encoding_input.setCurrentText(wordless_conversion.to_encoding_text(self.main, *settings_loaded['general']['encoding_input']))
        self.combo_box_default_encoding_output.setCurrentText(wordless_conversion.to_encoding_text(self.main, *settings_loaded['general']['encoding_output']))

        self.line_edit_default_paths_open_files.setText(os.path.realpath(settings_loaded['general']['default_paths_open_files']))
        self.line_edit_default_paths_export.setText(os.path.realpath(settings_loaded['general']['default_paths_export']))

        self.spin_box_precision_decimal.setValue(settings_loaded['general']['precision_decimal'])
        self.spin_box_precision_pct.setValue(settings_loaded['general']['precision_pct'])
        self.spin_box_precision_p_value.setValue(settings_loaded['general']['precision_p_value'])

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
        reply = wordless_dialog.wordless_restore_default_settings(self)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

    def save(self):
        if self.apply():
            self.accept()

    def apply(self):
        settings = self.main.settings_custom

        # Validation
        if not os.path.exists(self.line_edit_default_paths_open_files.text()):
            wordless_dialog.wordless_message_path_invalid(self, self.line_edit_default_paths_open_files.text())

            self.line_edit_default_paths_open_files.setFocus()
            self.line_edit_default_paths_open_files.selectAll()

            return False

        if not os.path.exists(self.line_edit_default_paths_export.text()):
            reply = wordless_dialog.wordless_message_path_does_not_exist(self, self.line_edit_default_paths_export.text())

            if reply == QMessageBox.No:
                self.line_edit_default_paths_export.setFocus()
                self.line_edit_default_paths_export.selectAll()

                return False

        # General
        settings['general']['encoding_input'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_default_encoding_input.currentText())
        settings['general']['encoding_output'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_default_encoding_output.currentText())

        settings['general']['default_paths_open_files'] = self.line_edit_default_paths_open_files.text()
        settings['general']['default_paths_export'] = self.line_edit_default_paths_export.text()

        settings['general']['precision_decimal'] = self.spin_box_precision_decimal.value()
        settings['general']['precision_pct'] = self.spin_box_precision_pct.value()
        settings['general']['precision_p_value'] = self.spin_box_precision_p_value.value()

        # Sentence Tokenization
        for lang_code in settings['sentence_tokenization']['sentence_tokenizers']:
            settings['sentence_tokenization']['sentence_tokenizers'][lang_code] = self.__dict__[f'combo_box_sentence_tokenizer_{lang_code}'].currentText()

        # Word Tokenization
        for lang_code in settings['word_tokenization']['word_tokenizers']:
            settings['word_tokenization']['word_tokenizers'][lang_code] = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()

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

        return True

    def load(self):
        self.load_settings()

        self.tree_settings.clearSelection()

        self.exec()
