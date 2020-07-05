#
# Wordless: Settings - Word Tokenization
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

from wordless_text import wordless_word_tokenization
from wordless_utils import wordless_conversion, wordless_threading
from wordless_widgets import (wordless_box, wordless_layout, wordless_table,
                              wordless_tree)

class Wordless_Worker_Preview_Word_Tokenizer(wordless_threading.Wordless_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['word_tokenization']['preview_lang']
        preview_samples = self.main.settings_custom['word_tokenization']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                tokens = wordless_word_tokenization.wordless_word_tokenize(
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

class Wordless_Settings_Word_Tokenization(wordless_tree.Wordless_Settings):
    def __init__(self, main):
        super().__init__(main)

        settings_global = self.main.settings_global['word_tokenizers']

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

            self.__dict__[f'combo_box_word_tokenizer_{lang}'].currentTextChanged.connect(lambda text, lang = lang: self.word_tokenizers_changed(lang))

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

        self.combo_box_word_tokenization_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.combo_box_word_tokenization_preview_lang.currentTextChanged.connect(self.preview_results_changed)
        self.text_edit_word_tokenization_preview_samples.textChanged.connect(self.preview_changed)
        self.text_edit_word_tokenization_preview_samples.textChanged.connect(self.preview_results_changed)
        self.text_edit_word_tokenization_preview_results.textChanged.connect(self.preview_changed)

        layout_preview_settings = wordless_layout.Wordless_Layout()
        layout_preview_settings.addWidget(self.label_word_tokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_word_tokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_word_tokenization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wordless_layout.Wordless_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_word_tokenization_preview_results, 1, 1)

        self.setLayout(wordless_layout.Wordless_Layout())
        self.layout().addWidget(group_box_word_tokenizer_settings, 0, 0,)
        self.layout().addWidget(group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 2)

    def word_tokenizers_changed(self, lang):
        settings_custom = self.main.settings_custom['word_tokenization']

        if lang == settings_custom['preview_lang']:
            self.preview_results_changed()

    def preview_changed(self):
        settings_custom = self.main.settings_custom['word_tokenization']

        settings_custom['preview_lang'] = wordless_conversion.to_lang_code(self.main, self.combo_box_word_tokenization_preview_lang.currentText())
        settings_custom['preview_samples'] = self.text_edit_word_tokenization_preview_samples.toPlainText()
        settings_custom['preview_results'] = self.text_edit_word_tokenization_preview_results.toPlainText()

    def preview_results_changed(self):
        settings_custom = self.main.settings_custom['word_tokenization']

        if settings_custom['preview_samples']:
            if self.combo_box_word_tokenization_preview_lang.isEnabled():
                self.__dict__[f"combo_box_word_tokenizer_{settings_custom['preview_lang']}"].setEnabled(False)
                self.combo_box_word_tokenization_preview_lang.setEnabled(False)

                self.label_word_tokenization_preview_processing.setText(self.tr('Processing text ...'))

                word_tokenizer = self.__dict__[f"combo_box_word_tokenizer_{settings_custom['preview_lang']}"].currentText()

                worker_preview_word_tokenizer = Wordless_Worker_Preview_Word_Tokenizer(
                    self.main,
                    update_gui = self.update_gui,
                    word_tokenizer = word_tokenizer
                )

                self.thread_preview_word_tokenizer = wordless_threading.Wordless_Thread_No_Progress(worker_preview_word_tokenizer)
                self.thread_preview_word_tokenizer.start_worker()
        else:
            self.text_edit_word_tokenization_preview_results.clear()

    def update_gui(self, preview_samples, preview_results):
        settings_custom = self.main.settings_custom['word_tokenization']

        self.label_word_tokenization_preview_processing.setText('')

        self.__dict__[f"combo_box_word_tokenizer_{settings_custom['preview_lang']}"].setEnabled(True)
        self.combo_box_word_tokenization_preview_lang.setEnabled(True)

        if preview_samples == settings_custom['preview_samples']:
            self.text_edit_word_tokenization_preview_results.setPlainText('\n'.join(preview_results))
        else:
            self.preview_results_changed()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

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

    def apply_settings(self):
        settings = self.main.settings_custom

        for lang in settings['word_tokenization']['word_tokenizers']:
            settings['word_tokenization']['word_tokenizers'][lang] = self.__dict__[f'combo_box_word_tokenizer_{lang}'].currentText()

        return True
