# ----------------------------------------------------------------------
# Wordless: Settings - Syllable Tokenization
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_nlp import wl_nlp_utils, wl_syl_tokenization, wl_word_detokenization
from wl_utils import wl_conversion, wl_threading
from wl_widgets import wl_boxes, wl_layouts, wl_tables, wl_trees

class Wl_Worker_Preview_Syl_Tokenizer(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(str, list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['syl_tokenization']['preview_lang']
        preview_samples = self.main.settings_custom['syl_tokenization']['preview_samples']

        for line in preview_samples.split('\n'):
            line = line.strip()

            if line:
                syls = wl_syl_tokenization.wl_syl_tokenize(
                    self.main, line,
                    lang = preview_lang,
                    syl_tokenizer = self.syl_tokenizer
                )

                if preview_lang == 'tha':
                    text = ' '.join(['-'.join(syl) for syl in syls])
                else:
                    text = wl_word_detokenization.wl_word_detokenize(
                        self.main, ['-'.join(syl) for syl in syls],
                        lang = preview_lang
                    )

                preview_results.append(text)
            else:
                preview_results.append('')

        self.worker_done.emit(preview_samples, preview_results)

class Wl_Settings_Syl_Tokenization(wl_trees.Wl_Settings):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['syl_tokenizers']
        self.settings_default = self.main.settings_default['syl_tokenization']
        self.settings_custom = self.main.settings_custom['syl_tokenization']

        # Syllable Tokenizer Settings
        group_box_syl_tokenizer_settings = QGroupBox(self.tr('Syllable Tokenizer Settings'), self)

        table_syl_tokenizers = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Syllable Tokenizers')
            ],
            cols_stretch = [
                self.tr('Syllable Tokenizers')
            ]
        )

        table_syl_tokenizers.verticalHeader().setHidden(True)
        table_syl_tokenizers.setRowCount(len(self.settings_global))

        for i, lang in enumerate(self.settings_global):
            table_syl_tokenizers.setItem(i, 0, QTableWidgetItem(wl_conversion.to_lang_text(self.main, lang)))

            self.__dict__[f'combo_box_syl_tokenizer_{lang}'] = wl_boxes.Wl_Combo_Box(self)
            self.__dict__[f'combo_box_syl_tokenizer_{lang}'].addItems(wl_nlp_utils.to_lang_util_texts(
                self.main,
                util_type = 'syl_tokenizers',
                util_codes = self.settings_global[lang]
            ))

            table_syl_tokenizers.setCellWidget(i, 1, self.__dict__[f'combo_box_syl_tokenizer_{lang}'])

        group_box_syl_tokenizer_settings.setLayout(wl_layouts.Wl_Layout())
        group_box_syl_tokenizer_settings.layout().addWidget(table_syl_tokenizers, 0, 0)

        # Preview
        group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_syl_tokenization_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_syl_tokenization_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.button_syl_tokenization_show_preview = QPushButton(self.tr('Show preview'), self)
        self.text_edit_syl_tokenization_preview_samples = QTextEdit(self)
        self.text_edit_syl_tokenization_preview_results = QTextEdit(self)

        self.combo_box_syl_tokenization_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))

        self.button_syl_tokenization_show_preview.setFixedWidth(130)
        self.text_edit_syl_tokenization_preview_samples.setAcceptRichText(False)
        self.text_edit_syl_tokenization_preview_results.setReadOnly(True)

        self.combo_box_syl_tokenization_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.button_syl_tokenization_show_preview.clicked.connect(self.preview_results_changed)
        self.text_edit_syl_tokenization_preview_samples.textChanged.connect(self.preview_changed)
        self.text_edit_syl_tokenization_preview_results.textChanged.connect(self.preview_changed)

        layout_preview_settings = wl_layouts.Wl_Layout()
        layout_preview_settings.addWidget(self.label_syl_tokenization_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_syl_tokenization_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.button_syl_tokenization_show_preview, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        group_box_preview.setLayout(wl_layouts.Wl_Layout())
        group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        group_box_preview.layout().addWidget(self.text_edit_syl_tokenization_preview_samples, 1, 0)
        group_box_preview.layout().addWidget(self.text_edit_syl_tokenization_preview_results, 1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(group_box_syl_tokenizer_settings, 0, 0)
        self.layout().addWidget(group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 2)

    def preview_changed(self):
        self.settings_custom['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_syl_tokenization_preview_lang.currentText())
        self.settings_custom['preview_samples'] = self.text_edit_syl_tokenization_preview_samples.toPlainText()
        self.settings_custom['preview_results'] = self.text_edit_syl_tokenization_preview_results.toPlainText()

    def preview_results_changed(self):
        if self.settings_custom['preview_samples']:
            if self.combo_box_syl_tokenization_preview_lang.isEnabled():
                self.__dict__[f"combo_box_syl_tokenizer_{self.settings_custom['preview_lang']}"].setEnabled(False)
                self.combo_box_syl_tokenization_preview_lang.setEnabled(False)
                self.button_syl_tokenization_show_preview.setEnabled(False)
                self.text_edit_syl_tokenization_preview_samples.setEnabled(False)

                self.button_syl_tokenization_show_preview.setText(self.tr('Processing ...'))

                syl_tokenizer = wl_nlp_utils.to_lang_util_code(
                    self.main,
                    util_type = 'syl_tokenizers',
                    util_text = self.__dict__[f"combo_box_syl_tokenizer_{self.settings_custom['preview_lang']}"].currentText()
                )

                worker_preview_syl_tokenizer = Wl_Worker_Preview_Syl_Tokenizer(
                    self.main,
                    update_gui = self.update_gui,
                    syl_tokenizer = syl_tokenizer
                )

                self.thread_preview_syl_tokenizer = wl_threading.Wl_Thread_No_Progress(worker_preview_syl_tokenizer)
                self.thread_preview_syl_tokenizer.start_worker()
        else:
            self.text_edit_syl_tokenization_preview_results.clear()

    def update_gui(self, preview_samples, preview_results):
        self.__dict__[f"combo_box_syl_tokenizer_{self.settings_custom['preview_lang']}"].setEnabled(True)
        self.combo_box_syl_tokenization_preview_lang.setEnabled(True)
        self.button_syl_tokenization_show_preview.setEnabled(True)
        self.text_edit_syl_tokenization_preview_samples.setEnabled(True)

        self.button_syl_tokenization_show_preview.setText(self.tr('Show preview'))
        self.text_edit_syl_tokenization_preview_results.setPlainText('\n'.join(preview_results))

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        for lang in settings['syl_tokenizers']:
            self.__dict__[f'combo_box_syl_tokenizer_{lang}'].blockSignals(True)

            self.__dict__[f'combo_box_syl_tokenizer_{lang}'].setCurrentText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'syl_tokenizers',
                util_code = settings['syl_tokenizers'][lang]
            ))

            self.__dict__[f'combo_box_syl_tokenizer_{lang}'].blockSignals(False)

        if not defaults:
            self.combo_box_syl_tokenization_preview_lang.blockSignals(True)
            self.text_edit_syl_tokenization_preview_samples.blockSignals(True)

            self.combo_box_syl_tokenization_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview_lang']))
            self.text_edit_syl_tokenization_preview_samples.setText(settings['preview_samples'])
            self.text_edit_syl_tokenization_preview_results.setText(settings['preview_results'])

            self.combo_box_syl_tokenization_preview_lang.blockSignals(False)
            self.text_edit_syl_tokenization_preview_samples.blockSignals(False)

    def apply_settings(self):
        for lang in self.settings_custom['syl_tokenizers']:
            self.settings_custom['syl_tokenizers'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'syl_tokenizers',
                util_text = self.__dict__[f'combo_box_syl_tokenizer_{lang}'].currentText()
            )

        return True
