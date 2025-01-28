# ----------------------------------------------------------------------
# Wordless: Settings - Sentiment Analysis
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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QTextEdit
)

from wordless.wl_nlp import wl_nlp_utils, wl_sentiment_analysis
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_layouts,
    wl_tables
)

class Wl_Settings_Sentiment_Analysis(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['sentiment_analyzers']
        self.settings_default = self.main.settings_default['sentiment_analysis']
        self.settings_custom = self.main.settings_custom['sentiment_analysis']

        # Sentiment Analyzer Settings
        self.group_box_sentiment_analyzer_settings = QGroupBox(self.tr('Sentiment Analyzer Settings'), self)

        self.table_sentiment_analyzers = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Sentiment Analyzer')
            ],
            editable = True
        )

        self.table_sentiment_analyzers.setFixedHeight(370)
        self.table_sentiment_analyzers.verticalHeader().setHidden(True)
        self.table_sentiment_analyzers.model().setRowCount(len(self.settings_global))

        self.table_sentiment_analyzers.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_sentiment_analyzers.model().setItem(i, 0, QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_sentiment_analyzers.model().setItem(i, 1, QStandardItem())

            self.table_sentiment_analyzers.setItemDelegateForRow(i, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self.table_sentiment_analyzers,
                items = list(wl_nlp_utils.to_lang_util_texts(
                    self.main,
                    util_type = 'sentiment_analyzers',
                    util_codes = self.settings_global[lang]
                )),
                col = 1
            ))

        self.table_sentiment_analyzers.enable_updates()

        self.group_box_sentiment_analyzer_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_sentiment_analyzer_settings.layout().addWidget(self.table_sentiment_analyzers, 0, 0)

        # Preview
        self.group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.button_show_preview = QPushButton(self.tr('Show preview'), self)
        self.label_preview_sentiment_score = QLabel(self.tr('Sentiment score: '), self)
        self.label_preview_sentiment_score_val = QLabel('', self)
        self.text_edit_preview_samples = QTextEdit(self)

        self.combo_box_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))

        self.button_show_preview.setMinimumWidth(140)
        self.text_edit_preview_samples.setAcceptRichText(False)

        self.combo_box_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.button_show_preview.clicked.connect(self.preview_results_changed)
        self.text_edit_preview_samples.textChanged.connect(self.preview_changed)

        self.group_box_preview.setLayout(wl_layouts.Wl_Layout())
        self.group_box_preview.layout().addWidget(self.label_preview_lang, 0, 0)
        self.group_box_preview.layout().addWidget(self.combo_box_preview_lang, 0, 1)
        self.group_box_preview.layout().addWidget(self.button_show_preview, 0, 2)
        self.group_box_preview.layout().addWidget(self.label_preview_sentiment_score, 0, 4)
        self.group_box_preview.layout().addWidget(self.label_preview_sentiment_score_val, 0, 5)
        self.group_box_preview.layout().addWidget(self.text_edit_preview_samples, 1, 0, 1, 6)

        self.group_box_preview.layout().setColumnStretch(3, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_sentiment_analyzer_settings, 0, 0)
        self.layout().addWidget(self.group_box_preview, 1, 0)

        self.layout().setContentsMargins(6, 4, 6, 4)
        self.layout().setRowStretch(1, 1)

    def preview_changed(self):
        self.settings_custom['preview']['preview_lang'] = wl_conversion.to_lang_code(self.main, self.combo_box_preview_lang.currentText())
        self.settings_custom['preview']['preview_samples'] = self.text_edit_preview_samples.toPlainText()

        if self.settings_custom['preview']['preview_samples'].strip():
            self.button_show_preview.setEnabled(True)
        else:
            self.button_show_preview.setEnabled(False)

    def preview_results_changed(self):
        if self.combo_box_preview_lang.isEnabled():
            row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

            self.table_sentiment_analyzers.itemDelegateForRow(row).set_enabled(False)
            self.combo_box_preview_lang.setEnabled(False)
            self.button_show_preview.setEnabled(False)
            self.text_edit_preview_samples.setEnabled(False)

            self.button_show_preview.setText(self.tr('Processing...'))

            sentiment_analyzer = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'sentiment_analyzers',
                util_text = self.table_sentiment_analyzers.model().item(row, 1).text()
            )

            if wl_nlp_utils.check_models(
                self.main,
                langs = [self.settings_custom['preview']['preview_lang']],
                lang_utils = [[sentiment_analyzer]]
            ):
                worker_preview_sentiment_analyzer = Wl_Worker_Preview_Sentiment_Analyzer(
                    self.main,
                    update_gui = self.update_gui,
                    sentiment_analyzer = sentiment_analyzer
                )

                self.thread_preview_sentiment_analyzer = wl_threading.Wl_Thread_No_Progress(worker_preview_sentiment_analyzer)
                self.thread_preview_sentiment_analyzer.start_worker()
            else:
                self.update_gui_err()

    def update_gui(self, preview_results):
        self.label_preview_sentiment_score_val.setText(str(preview_results))
        self.settings_custom['preview']['preview_sentiment_score'] = self.label_preview_sentiment_score_val.text()

        self.update_gui_err()

    def update_gui_err(self):
        self.button_show_preview.setText(self.tr('Show preview'))

        row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

        self.table_sentiment_analyzers.itemDelegateForRow(row).set_enabled(True)
        self.combo_box_preview_lang.setEnabled(True)
        self.button_show_preview.setEnabled(True)
        self.text_edit_preview_samples.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_sentiment_analyzers.disable_updates()

        for i, lang in enumerate(settings['sentiment_analyzer_settings']):
            self.table_sentiment_analyzers.model().item(i, 1).setText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'sentiment_analyzers',
                util_code = settings['sentiment_analyzer_settings'][lang]
            ))

        self.table_sentiment_analyzers.enable_updates()

        if not defaults:
            self.combo_box_preview_lang.blockSignals(True)
            self.text_edit_preview_samples.blockSignals(True)

            self.combo_box_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview']['preview_lang']))
            self.text_edit_preview_samples.setText(settings['preview']['preview_samples'])
            self.label_preview_sentiment_score_val.setText(settings['preview']['preview_sentiment_score'])

            self.combo_box_preview_lang.blockSignals(False)
            self.text_edit_preview_samples.blockSignals(False)

        self.preview_changed()

    def apply_settings(self):
        for i, lang in enumerate(self.settings_custom['sentiment_analyzer_settings']):
            self.settings_custom['sentiment_analyzer_settings'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'sentiment_analyzers',
                util_text = self.table_sentiment_analyzers.model().item(i, 1).text()
            )

        return True

class Wl_Worker_Preview_Sentiment_Analyzer(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(float)

    def run(self):
        preview_lang = self.main.settings_custom['sentiment_analysis']['preview']['preview_lang']
        preview_samples = self.main.settings_custom['sentiment_analysis']['preview']['preview_samples']

        sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
            self.main,
            inputs = [preview_samples.strip()],
            lang = preview_lang,
            sentiment_analyzer = self.sentiment_analyzer
        )

        self.worker_done.emit(sentiment_scores[0])
