# ----------------------------------------------------------------------
# Wordless: Settings - Sentence Tokenization
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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_sentence_tokenization
)
from wordless.wl_settings import wl_settings
from wordless.wl_utils import (
    wl_conversion,
    wl_threading
)
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_layouts,
    wl_tables
)

class Wl_Settings_Sentence_Tokenization(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['sentence_tokenizers']
        self.settings_default = self.main.settings_default['sentence_tokenization']
        self.settings_custom = self.main.settings_custom['sentence_tokenization']

        # Sentence Tokenizer Settings
        self.group_box_sentence_tokenizer_settings = QtWidgets.QGroupBox(self.tr('Sentence Tokenizer Settings'), self)

        self.table_sentence_tokenizers = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Sentence Tokenizers')
            ],
            editable = True
        )

        self.table_sentence_tokenizers.setFixedHeight(370)
        self.table_sentence_tokenizers.verticalHeader().setHidden(True)
        self.table_sentence_tokenizers.model().setRowCount(len(self.settings_global))

        self.table_sentence_tokenizers.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_sentence_tokenizers.model().setItem(i, 0, QtGui.QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_sentence_tokenizers.model().setItem(i, 1, QtGui.QStandardItem())

            self.table_sentence_tokenizers.setItemDelegateForRow(i, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self.table_sentence_tokenizers,
                items = list(wl_nlp_utils.to_lang_util_texts(
                    self.main,
                    util_type = 'sentence_tokenizers',
                    util_codes = self.settings_global[lang]
                )),
                col = 1
            ))

        self.table_sentence_tokenizers.enable_updates()

        self.group_box_sentence_tokenizer_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_sentence_tokenizer_settings.layout().addWidget(self.table_sentence_tokenizers, 0, 0)

        # Preview
        self.group_box_preview = QtWidgets.QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QtWidgets.QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.button_show_preview = QtWidgets.QPushButton(self.tr('Show preview'), self)
        self.text_edit_preview_samples = QtWidgets.QTextEdit(self)
        self.text_edit_preview_results = QtWidgets.QTextEdit(self)

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

        self.layout().addWidget(self.group_box_sentence_tokenizer_settings, 0, 0)
        self.layout().addWidget(self.group_box_preview, 1, 0)

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

            self.table_sentence_tokenizers.itemDelegateForRow(row).set_enabled(False)
            self.combo_box_preview_lang.setEnabled(False)
            self.button_show_preview.setEnabled(False)
            self.text_edit_preview_samples.setEnabled(False)
            self.text_edit_preview_results.setEnabled(False)

            self.button_show_preview.setText(self.tr('Processing...'))

            sentence_tokenizer = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'sentence_tokenizers',
                util_text = self.table_sentence_tokenizers.model().item(row, 1).text()
            )

            if wl_nlp_utils.check_models(
                self,
                langs = [self.settings_custom['preview']['preview_lang']],
                lang_utils = [[sentence_tokenizer]]
            ):
                self.worker_preview_sentence_tokenizer = Wl_Worker_Preview_Sentence_Tokenizer(
                    self.main,
                    sentence_tokenizer = sentence_tokenizer
                )

                self.thread_preview_sentence_tokenizer = QtCore.QThread()
                wl_threading.start_worker_in_thread(
                    self.worker_preview_sentence_tokenizer,
                    self.thread_preview_sentence_tokenizer,
                    self.update_gui
                )
            else:
                self.update_gui_err()

    def update_gui(self, preview_results):
        self.text_edit_preview_results.setPlainText('\n'.join(preview_results))

        self.update_gui_err()

    def update_gui_err(self):
        self.button_show_preview.setText(self.tr('Show preview'))

        row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

        self.table_sentence_tokenizers.itemDelegateForRow(row).set_enabled(True)
        self.combo_box_preview_lang.setEnabled(True)
        self.button_show_preview.setEnabled(True)
        self.text_edit_preview_samples.setEnabled(True)
        self.text_edit_preview_results.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_sentence_tokenizers.disable_updates()

        for i, lang in enumerate(settings['sentence_tokenizer_settings']):
            self.table_sentence_tokenizers.model().item(i, 1).setText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'sentence_tokenizers',
                util_code = settings['sentence_tokenizer_settings'][lang]
            ))

        self.table_sentence_tokenizers.enable_updates()

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
        for i, lang in enumerate(self.settings_custom['sentence_tokenizer_settings']):
            self.settings_custom['sentence_tokenizer_settings'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'sentence_tokenizers',
                util_text = self.table_sentence_tokenizers.model().item(i, 1).text()
            )

        return True

class Wl_Worker_Preview_Sentence_Tokenizer(wl_threading.Wl_Worker_No_Progress):
    finished = QtCore.pyqtSignal(list)

    def run(self):
        preview_lang = self.main.settings_custom['sentence_tokenization']['preview']['preview_lang']
        preview_samples = self.main.settings_custom['sentence_tokenization']['preview']['preview_samples']

        preview_results = wl_sentence_tokenization.wl_sentence_tokenize(
            self.main,
            text = preview_samples.strip(),
            lang = preview_lang,
            sentence_tokenizer = self.sentence_tokenizer
        )

        self.finished.emit(preview_results)
