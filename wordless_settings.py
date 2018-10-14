#
# Wordless: Settings
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import jpype
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

        self.button_export_selected.hide()
        self.button_export_all.hide()
        self.button_clear.hide()

    def set_items(self, tokens):
        self.clear_table()

        self.setRowCount((len(tokens) - 1) // self.columnCount() + 1) 

        for i, token in enumerate(tokens):
            row = i // self.columnCount()
            col = i % self.columnCount()

            self.setItem(row, col, QTableWidgetItem(token))

class Wordless_Settings(QDialog):
    def __init__(self, parent):
        def selection_changed():
            self.settings_general.hide()
            self.settings_word_tokenization.hide()
            self.settings_lemmatization.hide()
            self.settings_stop_words.hide()

            selected_items = self.tree_settings.selectedItems()
            if not selected_items:
                self.tree_settings.findItems(self.tr('General'), Qt.MatchExactly)[0].setSelected(True)
            else:
                if selected_items[0].text(0) == 'General':
                    self.settings_general.show()
                elif selected_items[0].text(0) == 'Word Tokenization':
                    self.settings_word_tokenization.show()
                elif selected_items[0].text(0) == 'Lemmatization':
                    self.settings_lemmatization.show()
                elif selected_items[0].text(0) == 'Stop Words':
                    self.settings_stop_words.show()

        super().__init__(parent)

        self.main = parent

        self.setWindowTitle(self.tr('Settings'))
        self.setFixedHeight(600)

        self.accepted.connect(self.apply)

        self.tree_settings = wordless_tree.Wordless_Tree(self)

        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('General')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Word Tokenization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Lemmatization')]))
        self.tree_settings.addTopLevelItem(QTreeWidgetItem(self.tree_settings, [self.tr('Stop Words')]))

        self.tree_settings.itemSelectionChanged.connect(selection_changed)

        wrapper_settings = QWidget()

        wrapper_settings.setLayout(QGridLayout())
        wrapper_settings.layout().addWidget(self.init_settings_general(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_word_tokenization(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_lemmatization(), 0, 0)
        wrapper_settings.layout().addWidget(self.init_settings_stop_words(), 0, 0)

        scroll_area_settings = wordless_layout.Wordless_Scroll_Area(self.main, wrapper_settings)

        button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self)
        button_save = QPushButton(self.tr('Save'), self)
        button_apply = QPushButton(self.tr('Apply'), self)
        button_cancel = QPushButton(self.tr('Cancel'), self)

        button_restore_defaults.clicked.connect(lambda: self.load_settings(defaults = True))
        button_save.clicked.connect(self.accept)
        button_apply.clicked.connect(self.apply)
        button_cancel.clicked.connect(self.reject)

        layout_buttons_right = QGridLayout()
        layout_buttons_right.addWidget(button_save, 0, 0)
        layout_buttons_right.addWidget(button_apply, 0, 1)
        layout_buttons_right.addWidget(button_cancel, 0, 2)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.tree_settings, 0, 0)
        self.layout().addWidget(scroll_area_settings, 0, 1)
        self.layout().addWidget(button_restore_defaults, 1, 0, Qt.AlignLeft)
        self.layout().addLayout(layout_buttons_right, 1, 1, Qt.AlignRight)

        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 4)

        selection_changed()

    def init_settings_general(self):
        self.settings_general = QWidget(self)

        group_box_encoding = QGroupBox(self.tr('Default Encodings'), self)

        self.label_encoding_input = QLabel(self.tr('Input Encoding:'), self)
        self.combo_box_encoding_input = wordless_box.Wordless_Combo_Box_Encoding(self.main)
        self.label_encoding_output = QLabel(self.tr('Output Encoding:'), self)
        self.combo_box_encoding_output = wordless_box.Wordless_Combo_Box_Encoding(self.main)

        group_box_encoding.setLayout(QGridLayout())
        group_box_encoding.layout().addWidget(self.label_encoding_input, 0, 0)
        group_box_encoding.layout().addWidget(self.combo_box_encoding_input, 0, 1)
        group_box_encoding.layout().addWidget(self.label_encoding_output, 1, 0)
        group_box_encoding.layout().addWidget(self.combo_box_encoding_output, 1, 1)

        self.label_precision = QLabel(self.tr('Precision:'), self)
        self.spin_box_precision = QSpinBox(self)

        self.spin_box_precision.setRange(0, 10)

        self.settings_general.setLayout(QGridLayout())
        self.settings_general.layout().addWidget(group_box_encoding, 0, 0, 1, 2, Qt.AlignTop)
        self.settings_general.layout().addWidget(self.label_precision, 1, 0, Qt.AlignTop)
        self.settings_general.layout().addWidget(self.spin_box_precision, 1, 1, Qt.AlignTop)

        return self.settings_general

    def init_settings_word_tokenization(self):
        def preview_settings_changed():
            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())
            settings_custom['preview_samples'] = self.text_edit_word_tokenization_preview_samples.toPlainText()

        def preview_results_changed():
            for lang_code in settings_global:
                if self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText() == self.tr('NLTK - Regular-Expression Tokenizer'):
                    self.__dict__[f'label_regex_tokenizer_{lang_code}'].show()
                    self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'].show()
                else:
                    self.__dict__[f'label_regex_tokenizer_{lang_code}'].hide()
                    self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'].hide()

            lang_code = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())

            word_tokenizer = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()

            self.text_edit_word_tokenization_preview_results.clear()

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

            self.__dict__[f'label_regex_tokenizer_{lang_code}'] = QLabel(self.tr('Regular expression for token delimiters:'))
            self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'] = QLineEdit(self)

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].addItems(settings_global[lang_code])

            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentTextChanged.connect(preview_results_changed)
            self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'].editingFinished.connect(preview_results_changed)

        wrapper_word_tokenizers.setLayout(QGridLayout())

        for i, lang_code in enumerate(settings_global):
            wrapper_word_tokenizers.layout().addWidget(self.__dict__[f'label_word_tokenizer_{lang_code}'], i * 2, 0)
            wrapper_word_tokenizers.layout().addWidget(self.__dict__[f'combo_box_word_tokenizer_{lang_code}'], i * 2, 1, 1, 2)

            wrapper_word_tokenizers.layout().addWidget(self.__dict__[f'label_regex_tokenizer_{lang_code}'], i * 2 + 1, 1)
            wrapper_word_tokenizers.layout().addWidget(self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'], i * 2 + 1, 2)

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

    def init_settings_lemmatization(self):
        def preview_settings_changed():
            lang_text = self.combo_box_lemmatization_preview_lang.currentText()

            settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, lang_text)
            settings_custom['preview_samples'] = self.text_edit_lemmatization_preview_samples.toPlainText()

        def preview_results_changed():
            lang_text = self.combo_box_lemmatization_preview_lang.currentText()
            lang_code = wordless_conversion.to_lang_code(self.main, lang_text)
            lemmatizer = self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentText()

            self.text_edit_lemmatization_preview_results.clear()

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

            word_list = self.__dict__[f'combo_box_stop_words_{lang_code_639_3}'].currentText()

            if word_list == 'NLTK':
                stop_words = nltk.corpus.stopwords.words(lang_text)
            elif word_list == 'Stopwords ISO':
                if lang_code_639_1 == 'zh_cn':
                    lang_code_639_1 = 'zh'

                with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                    stop_words = json.load(f)[lang_code_639_1]
            elif word_list == 'stopwords-json':
                if lang_code_639_1 == 'zh_cn':
                    lang_code_639_1 = 'zh'

                with open(r'stop_words/stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
                    stop_words = json.load(f)[lang_code_639_1]

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
        self.combo_box_encoding_input.setCurrentText(wordless_conversion.to_encoding_text(self.main, *settings_loaded['general']['encoding_input']))
        self.combo_box_encoding_output.setCurrentText(wordless_conversion.to_encoding_text(self.main, *settings_loaded['general']['encoding_output']))

        self.spin_box_precision.setValue(settings_loaded['general']['precision'])

        # Word Tokenization
        for lang_code in settings_loaded['word_tokenization']['word_tokenizers']:
            self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].setCurrentText(settings_loaded['word_tokenization']['word_tokenizers'][lang_code])
            self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'].setText(settings_loaded['word_tokenization']['regex_tokenizers'][lang_code])

        self.combo_box_word_tokenization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['word_tokenization']['preview_lang']))
        self.text_edit_word_tokenization_preview_samples.setText(settings_loaded['word_tokenization']['preview_samples'])

        # Lemmatization
        for lang_code in settings_loaded['lemmatization']['lemmatizers']:
            self.__dict__[f'combo_box_lemmatizer_{lang_code}'].setCurrentText(settings_loaded['lemmatization']['lemmatizers'][lang_code])

        self.combo_box_lemmatization_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['lemmatization']['preview_lang']))
        self.text_edit_lemmatization_preview_samples.setText(settings_loaded['lemmatization']['preview_samples'])

        # Stop Words
        for lang_code in settings_loaded['stop_words']['stop_words']:
            self.__dict__[f'combo_box_stop_words_{lang_code}'].setCurrentText(settings_loaded['stop_words']['stop_words'][lang_code])

        self.combo_box_stop_words_preview_lang.setCurrentText(wordless_conversion.to_lang_text(self.main, settings_loaded['stop_words']['preview_lang']))

    def apply(self):
        settings = self.main.settings_custom

        # General
        settings['general']['encoding_input'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_encoding_input.currentText())
        settings['general']['encoding_output'] = wordless_conversion.to_encoding_code(self.main, self.combo_box_encoding_output.currentText())

        settings['general']['precision'] = self.spin_box_precision.value()

        # Word Tokenization
        for lang_code in settings['word_tokenization']['word_tokenizers']:
            settings['word_tokenization']['word_tokenizers'][lang_code] = self.__dict__[f'combo_box_word_tokenizer_{lang_code}'].currentText()
            settings['word_tokenization']['regex_tokenizers'][lang_code] = self.__dict__[f'line_edit_regex_tokenizer_{lang_code}'].text()

        # Lemmatization
        for lang_code in settings['lemmatization']['lemmatizers']:
            settings['lemmatization']['lemmatizers'][lang_code] = self.__dict__[f'combo_box_lemmatizer_{lang_code}'].currentText()

        # Stop Words
        for lang_code in settings['stop_words']['stop_words']:
            settings['stop_words']['stop_words'][lang_code] = self.__dict__[f'combo_box_stop_words_{lang_code}'].currentText()

    def load(self):
        self.load_settings()

        self.tree_settings.clearSelection()

        self.exec()
