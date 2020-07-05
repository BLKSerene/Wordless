#
# Wordless: Settings - Lemmatization
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

from wl_text import wl_word_detokenization, wl_lemmatization, wl_word_tokenization
from wl_utils import wl_conversion, wl_threading
from wl_widgets import wl_box, wl_layout, wl_table, wl_tree

class Wl_Worker_Preview_Lemmatizer(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['lemmatization']['preview_lang']
        preview_samples = self.main.settings_custom['lemmatization']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                tokens = wl_word_tokenization.wl_word_tokenize(
                    self.main, line,
                    lang = preview_lang
                )

                lemmas = wl_lemmatization.wl_lemmatize(
                    self.main, tokens,
                    lang = preview_lang,
                    lemmatizer = self.lemmatizer
                )

                text = wl_word_detokenization.wl_word_detokenize(
                    self.main, lemmas,
                    lang = preview_lang
                )

                preview_results.append(text)
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wl_Settings_Lemmatization(wl_tree.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        settings_global = self.main.settings_global['lemmatizers']

        # Lemmatizer Settings
        group_box_lemmatizer_settings = QGroupBox(self.tr('Lemmatizer Settings'), self)

        table_lemmatizers = wl_table.Wl_Table(
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
            table_lemmatizers.setItem(i, 0, QTableWidgetItem(wl_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_lemmatizer_{lang}'] = wl_box.Wl_Combo_Box(self)

            self.__dict__[f'combo_box_lemmatizer_{lang}'].addItems(settings_global[lang])

            self.__dict__[f'combo_box_lemmatizer_{lang}'].currentTextChanged.connect(lambda text, lang = lang: lemmatizers_changed(lang))

            table_lemmatizers.setCellWidget(i, 1, self.__dict__[f'combo_box_lemmatizer_{lang}'])

        group_box_lemmatizer_settings.setLayout(wl_layout.Wl_Layout())
        group_box_lemmatizer_settings.layout().addWidget(table_lemmatizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_lemmatization_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_lemmatization_preview_lang = wl_box.Wl_Combo_Box(self)
        self.label_lemmatization_preview_processing = QLabel('', self)
        self.text_edit_lemmatization_preview_samples = QTextEdit(self)
        self.text_edit_lemmatization_preview_results = QTextEdit(self)

        self.combo_box_lemmatization_preview_lang.addItems(wl_conversion.to_lang_text(self.main, list(settings_global.keys())))

        self.text_edit_lemmatization_preview_samples.setAcceptRichText(False)
        self.text_edit_lemmatization_preview_results.setReadOnly(True)

        self.combo_box_lemmatization_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.combo_box_lemmatization_preview_lang.currentTextChanged.connect(self.preview_results_changed)
        self.text_edit_lemmatization_preview_samples.textChanged.connect(self.preview_changed)
        self.text_edit_lemmatization_preview_samples.textChanged.connect(self.preview_results_changed)
        self.text_edit_lemmatization_preview_results.textChanged.connect(self.preview_changed)

        layout_preview_settings = wl_layout.Wl_Layout()
        layout_preview_settings.addWidget(self.label_lemmatization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_lemmatization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.label_lemmatization_preview_processing, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wl_layout.Wl_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_lemmatization_preview_results, 1, 1)

        self.setLayout(wl_layout.Wl_Layout())
        self.layout().addWidget(group_box_lemmatizer_settings, 0, 0)
        self.layout().addWidget(group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 2)

    def lemmatizers_changed(self, lang):
        settings_custom = self.main.settings_custom['lemmatization']

        if lang == settings_custom['preview_lang']:
            self.preview_results_changed()

    def preview_changed(self):
        settings_custom = self.main.settings_custom['lemmatization']

        settings_custom['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_lemmatization_preview_lang.currentText())
        settings_custom['preview_samples'] = self.text_edit_lemmatization_preview_samples.toPlainText()
        settings_custom['preview_results'] = self.text_edit_lemmatization_preview_results.toPlainText()

    def preview_results_changed(self):
        settings_custom = self.main.settings_custom['lemmatization']

        if settings_custom['preview_samples']:
            if self.combo_box_lemmatization_preview_lang.isEnabled():
                self.__dict__[f"combo_box_lemmatizer_{settings_custom['preview_lang']}"].setEnabled(False)
                self.combo_box_lemmatization_preview_lang.setEnabled(False)

                self.label_lemmatization_preview_processing.setText(self.tr('Processing text ...'))

                lemmatizer = self.__dict__[f"combo_box_lemmatizer_{settings_custom['preview_lang']}"].currentText()

                worker_preview_lemmatizer = Wl_Worker_Preview_Lemmatizer(
                    self.main,
                    update_gui = self.update_gui,
                    lemmatizer = lemmatizer
                )

                self.thread_preview_lemmatizer = wl_threading.Wl_Thread_No_Progress(worker_preview_lemmatizer)
                self.thread_preview_lemmatizer.start_worker()
        else:
            self.text_edit_lemmatization_preview_results.clear()

    def update_gui(self, preview_samples, preview_results):
        settings_custom = self.main.settings_custom['lemmatization']

        self.label_lemmatization_preview_processing.setText('')

        self.__dict__[f"combo_box_lemmatizer_{settings_custom['preview_lang']}"].setEnabled(True)
        self.combo_box_lemmatization_preview_lang.setEnabled(True)

        if preview_samples == settings_custom['preview_samples']:
            self.text_edit_lemmatization_preview_results.setPlainText('\n'.join(preview_results))
        else:
            self.preview_results_changed()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default)
        else:
            settings = copy.deepcopy(self.main.settings_custom)

        for lang in settings['lemmatization']['lemmatizers']:
            self.__dict__[f'combo_box_lemmatizer_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_lemmatizer_{lang}'].setCurrentText(settings['lemmatization']['lemmatizers'][lang])

            self.__dict__[f'combo_box_lemmatizer_{lang}'].blockSignals(False)

        if not defaults:
            self.combo_box_lemmatization_preview_lang.blockSignals(True)
            self.text_edit_lemmatization_preview_samples.blockSignals(True)

            self.combo_box_lemmatization_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['lemmatization']['preview_lang']))
            self.text_edit_lemmatization_preview_samples.setText(settings['lemmatization']['preview_samples'])
            self.text_edit_lemmatization_preview_results.setText(settings['lemmatization']['preview_results'])

            self.combo_box_lemmatization_preview_lang.blockSignals(False)
            self.text_edit_lemmatization_preview_samples.blockSignals(False)

    def apply_settings(self):
        settings = self.main.settings_custom

        for lang in settings['lemmatization']['lemmatizers']:
            settings['lemmatization']['lemmatizers'][lang] = self.__dict__[f'combo_box_lemmatizer_{lang}'].currentText()

        return True
