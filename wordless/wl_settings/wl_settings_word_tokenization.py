# ----------------------------------------------------------------------
# Wordless: Settings - Word Tokenization
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QTextEdit
)

from wordless.wl_nlp import wl_nlp_utils, wl_word_tokenization
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion, wl_misc, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_layouts,
    wl_tables
)

class Wl_Settings_Word_Tokenization(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['word_tokenizers']
        self.settings_default = self.main.settings_default['word_tokenization']
        self.settings_custom = self.main.settings_custom['word_tokenization']

        # Word Tokenizer Settings
        self.group_box_word_tokenizer_settings = QGroupBox(self.tr('Word Tokenizer Settings'), self)

        self.table_word_tokenizers = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Word Tokenizers')
            ],
            editable = True
        )

        self.table_word_tokenizers.setFixedHeight(370)
        self.table_word_tokenizers.verticalHeader().setHidden(True)
        self.table_word_tokenizers.model().setRowCount(len(self.settings_global))

        self.table_word_tokenizers.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_word_tokenizers.model().setItem(i, 0, QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_word_tokenizers.model().setItem(i, 1, QStandardItem())

            self.table_word_tokenizers.setItemDelegateForRow(i, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self.table_word_tokenizers,
                items = list(wl_nlp_utils.to_lang_util_texts(
                    self.main,
                    util_type = 'word_tokenizers',
                    util_codes = self.settings_global[lang]
                )),
                col = 1
            ))

        self.table_word_tokenizers.enable_updates()

        self.group_box_word_tokenizer_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_word_tokenizer_settings.layout().addWidget(self.table_word_tokenizers, 0, 0)

        # Preview
        self.group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.button_show_preview = QPushButton(self.tr('Show preview'), self)
        self.text_edit_preview_samples = QTextEdit(self)
        self.text_edit_preview_results = QTextEdit(self)

        self.combo_box_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))

        self.button_show_preview.setMinimumWidth(140)
        self.text_edit_preview_samples.setAcceptRichText(False)
        self.text_edit_preview_results.setReadOnly(True)

        self.combo_box_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.button_show_preview.clicked.connect(self.preview_results_changed)
        self.text_edit_preview_samples.textChanged.connect(self.preview_changed)
        self.text_edit_preview_results.textChanged.connect(self.preview_changed)

        layout_preview_settings = wl_layouts.Wl_Layout()
        layout_preview_settings.addWidget(self.label_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.button_show_preview, 0, 3)

        layout_preview_settings.setColumnStretch(2, 1)

        self.group_box_preview.setLayout(wl_layouts.Wl_Layout())
        self.group_box_preview.layout().addLayout(layout_preview_settings, 0, 0, 1, 2)
        self.group_box_preview.layout().addWidget(self.text_edit_preview_samples, 1, 0)
        self.group_box_preview.layout().addWidget(self.text_edit_preview_results, 1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_word_tokenizer_settings, 0, 0,)
        self.layout().addWidget(self.group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def preview_changed(self):
        self.settings_custom['preview']['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_preview_lang.currentText())
        self.settings_custom['preview']['preview_samples'] = self.text_edit_preview_samples.toPlainText()
        self.settings_custom['preview']['preview_results'] = self.text_edit_preview_results.toPlainText()

        if self.settings_custom['preview']['preview_samples'].strip():
            self.button_show_preview.setEnabled(True)
        else:
            self.button_show_preview.setEnabled(False)

    def preview_results_changed(self):
        if self.combo_box_preview_lang.isEnabled():
            row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

            self.table_word_tokenizers.itemDelegateForRow(row).set_enabled(False)
            self.combo_box_preview_lang.setEnabled(False)
            self.button_show_preview.setEnabled(False)
            self.text_edit_preview_samples.setEnabled(False)

            self.button_show_preview.setText(self.tr('Processing...'))

            word_tokenizer = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'word_tokenizers',
                util_text = self.table_word_tokenizers.model().item(row, 1).text()
            )

            if wl_nlp_utils.check_models(
                self.main,
                langs = [self.settings_custom['preview']['preview_lang']],
                lang_utils = [['default_sentence_tokenizer', word_tokenizer]]
            ):
                worker_preview_word_tokenizer = Wl_Worker_Preview_Word_Tokenizer(
                    self.main,
                    update_gui = self.update_gui,
                    word_tokenizer = word_tokenizer
                )

                self.thread_preview_word_tokenizer = wl_threading.Wl_Thread_No_Progress(worker_preview_word_tokenizer)
                self.thread_preview_word_tokenizer.start_worker()
            else:
                self.update_gui_err()

    def update_gui(self, preview_results):
        self.text_edit_preview_results.setPlainText('\n'.join(preview_results))

        self.update_gui_err()

    def update_gui_err(self):
        self.button_show_preview.setText(self.tr('Show preview'))

        row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

        self.table_word_tokenizers.itemDelegateForRow(row).set_enabled(True)
        self.combo_box_preview_lang.setEnabled(True)
        self.button_show_preview.setEnabled(True)
        self.text_edit_preview_samples.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_word_tokenizers.disable_updates()

        for i, lang in enumerate(settings['word_tokenizer_settings']):
            self.table_word_tokenizers.model().item(i, 1).setText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'word_tokenizers',
                util_code = settings['word_tokenizer_settings'][lang]
            ))

        self.table_word_tokenizers.enable_updates()

        if not defaults:
            self.combo_box_preview_lang.blockSignals(True)
            self.text_edit_preview_samples.blockSignals(True)

            self.combo_box_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview']['preview_lang']))
            self.text_edit_preview_samples.setText(settings['preview']['preview_samples'])
            self.text_edit_preview_results.setText(settings['preview']['preview_results'])

            self.combo_box_preview_lang.blockSignals(False)
            self.text_edit_preview_samples.blockSignals(False)

        self.preview_changed()

    def apply_settings(self):
        for i, lang in enumerate(self.settings_custom['word_tokenizer_settings']):
            self.settings_custom['word_tokenizer_settings'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'word_tokenizers',
                util_text = self.table_word_tokenizers.model().item(i, 1).text()
            )

        return True

RE_VIE_SPECES_UNDERSCORES = re.compile(r'\s+')

class Wl_Worker_Preview_Word_Tokenizer(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(list)

    def run(self):
        preview_results = []

        preview_lang = self.main.settings_custom['word_tokenization']['preview']['preview_lang']
        preview_samples = self.main.settings_custom['word_tokenization']['preview']['preview_samples']

        tokens_multilevel = wl_word_tokenization.wl_word_tokenize(
            main = self.main,
            text = preview_samples,
            lang = preview_lang,
            word_tokenizer = self.word_tokenizer
        )

        for para in tokens_multilevel:
            tokens = wl_misc.flatten_list(para)

            # Replace spaces with underscores in Vietnamese texts
            if preview_lang == 'vie':
                tokens = [RE_VIE_SPECES_UNDERSCORES.sub(r'_', token) for token in tokens]

            preview_results.append(' '.join(tokens))

        self.worker_done.emit(preview_results)
