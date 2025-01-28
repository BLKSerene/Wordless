# ----------------------------------------------------------------------
# Wordless: Settings - Dependency Parsing
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
from PyQt5.QtWidgets import QGroupBox, QLabel, QPushButton, QTextEdit

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_nlp import wl_dependency_parsing, wl_nlp_utils
from wordless.wl_settings import wl_settings
from wordless.wl_utils import wl_conversion, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_item_delegates,
    wl_layouts,
    wl_tables,
    wl_widgets
)

class Wl_Settings_Dependency_Parsing(wl_settings.Wl_Settings_Node):
    def __init__(self, main):
        super().__init__(main)

        self.settings_global = self.main.settings_global['dependency_parsers']
        self.settings_default = self.main.settings_default['dependency_parsing']
        self.settings_custom = self.main.settings_custom['dependency_parsing']

        # Dependency Parser Settings
        self.group_box_dependency_parser_settings = QGroupBox(self.tr('Dependency Parser Settings'), self)

        self.table_dependency_parsers = wl_tables.Wl_Table(
            self,
            headers = [
                self.tr('Language'),
                self.tr('Dependency Parsers')
            ],
            editable = True
        )

        self.table_dependency_parsers.setFixedHeight(370)
        self.table_dependency_parsers.verticalHeader().setHidden(True)
        self.table_dependency_parsers.model().setRowCount(len(self.settings_global))

        self.table_dependency_parsers.disable_updates()

        for i, lang in enumerate(self.settings_global):
            self.table_dependency_parsers.model().setItem(i, 0, QStandardItem(wl_conversion.to_lang_text(self.main, lang)))
            self.table_dependency_parsers.model().setItem(i, 1, QStandardItem())

            self.table_dependency_parsers.setItemDelegateForRow(i, wl_item_delegates.Wl_Item_Delegate_Combo_Box(
                parent = self.table_dependency_parsers,
                items = list(wl_nlp_utils.to_lang_util_texts(
                    self.main,
                    util_type = 'dependency_parsers',
                    util_codes = self.settings_global[lang]
                )),
                col = 1
            ))

        self.table_dependency_parsers.enable_updates()

        self.group_box_dependency_parser_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_dependency_parser_settings.layout().addWidget(self.table_dependency_parsers, 0, 0)

        # Preview
        self.group_box_preview = QGroupBox(self.tr('Preview'), self)

        self.label_preview_lang = QLabel(self.tr('Select language:'), self)
        self.combo_box_preview_lang = wl_boxes.Wl_Combo_Box(self)
        self.button_preview_settings = QPushButton(self.tr('Preview settings'), self)
        self.dialog_preview_settings = Wl_Dialog_Preview_Settings(self.main)
        self.button_show_preview = QPushButton(self.tr('Show preview'), self)
        self.text_edit_preview_samples = QTextEdit(self)

        self.combo_box_preview_lang.addItems(wl_conversion.to_lang_texts(self.main, self.settings_global))

        self.button_preview_settings.setMinimumWidth(140)
        self.button_show_preview.setMinimumWidth(140)
        self.text_edit_preview_samples.setAcceptRichText(False)

        self.combo_box_preview_lang.currentTextChanged.connect(self.preview_changed)
        self.button_preview_settings.clicked.connect(self.dialog_preview_settings.load)
        self.button_show_preview.clicked.connect(self.preview_results_changed)
        self.text_edit_preview_samples.textChanged.connect(self.preview_changed)

        layout_preview_settings = wl_layouts.Wl_Layout()
        layout_preview_settings.addWidget(self.label_preview_lang, 0, 0)
        layout_preview_settings.addWidget(self.combo_box_preview_lang, 0, 1)
        layout_preview_settings.addWidget(self.button_preview_settings, 0, 3)
        layout_preview_settings.addWidget(self.button_show_preview, 0, 4)

        layout_preview_settings.setColumnStretch(2, 1)

        self.group_box_preview.setLayout(wl_layouts.Wl_Layout())
        self.group_box_preview.layout().addLayout(layout_preview_settings, 0, 0)
        self.group_box_preview.layout().addWidget(self.text_edit_preview_samples, 1, 0)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.group_box_dependency_parser_settings, 0, 0)
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

            self.table_dependency_parsers.itemDelegateForRow(row).set_enabled(False)
            self.combo_box_preview_lang.setEnabled(False)
            self.button_show_preview.setEnabled(False)
            self.text_edit_preview_samples.setEnabled(False)

            self.button_show_preview.setText(self.tr('Processing...'))

            dependency_parser = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'dependency_parsers',
                util_text = self.table_dependency_parsers.model().item(row, 1).text()
            )

            if wl_nlp_utils.check_models(
                self.main,
                langs = [self.settings_custom['preview']['preview_lang']],
                lang_utils = [[dependency_parser]]
            ):
                worker_preview_dependency_parser = Wl_Worker_Preview_Dependency_Parser(
                    self.main,
                    update_gui = self.update_gui,
                    dependency_parser = dependency_parser
                )

                self.thread_preview_dependency_parser = wl_threading.Wl_Thread_No_Progress(worker_preview_dependency_parser)
                self.thread_preview_dependency_parser.start_worker()
            else:
                self.update_gui_err()

    def update_gui(self, htmls):
        wl_dependency_parsing.wl_show_dependency_graphs(
            self.main,
            htmls = htmls,
            show_in_separate_tab = self.settings_custom['preview']['preview_settings']['show_in_separate_tab']
        )

        self.update_gui_err()

    def update_gui_err(self):
        self.button_show_preview.setText(self.tr('Show preview'))

        row = list(self.settings_global.keys()).index(self.settings_custom['preview']['preview_lang'])

        self.table_dependency_parsers.itemDelegateForRow(row).set_enabled(True)
        self.combo_box_preview_lang.setEnabled(True)
        self.button_show_preview.setEnabled(True)
        self.text_edit_preview_samples.setEnabled(True)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.table_dependency_parsers.disable_updates()

        for i, lang in enumerate(settings['dependency_parser_settings']):
            self.table_dependency_parsers.model().item(i, 1).setText(wl_nlp_utils.to_lang_util_text(
                self.main,
                util_type = 'dependency_parsers',
                util_code = settings['dependency_parser_settings'][lang]
            ))

        self.table_dependency_parsers.enable_updates()

        if not defaults:
            self.combo_box_preview_lang.blockSignals(True)
            self.text_edit_preview_samples.blockSignals(True)

            self.combo_box_preview_lang.setCurrentText(wl_conversion.to_lang_text(self.main, settings['preview']['preview_lang']))
            self.text_edit_preview_samples.setText(settings['preview']['preview_samples'])

            self.combo_box_preview_lang.blockSignals(False)
            self.text_edit_preview_samples.blockSignals(False)

        self.preview_changed()

    def apply_settings(self):
        for i, lang in enumerate(self.settings_custom['dependency_parser_settings']):
            self.settings_custom['dependency_parser_settings'][lang] = wl_nlp_utils.to_lang_util_code(
                self.main,
                util_type = 'dependency_parsers',
                util_text = self.table_dependency_parsers.model().item(i, 1).text()
            )

        return True

class Wl_Dialog_Preview_Settings(wl_dialogs.Wl_Dialog_Settings):
    def __init__(self, main):
        super().__init__(main, title = 'Preview Settings')

        self.setMinimumWidth(450)

        self.settings_custom = self.main.settings_custom['dependency_parsing']['preview']['preview_settings']
        self.settings_default = self.main.settings_default['dependency_parsing']['preview']['preview_settings']

        (
            self.checkbox_show_pos_tags, self.combo_box_show_pos_tags, self.label_show_pos_tags,
            self.checkbox_show_lemmas,
            self.checkbox_collapse_punc_marks,
            self.checkbox_compact_mode,
            self.checkbox_show_in_separate_tab
        ) = wl_widgets.wl_widgets_fig_settings_dependency_parsing(self)

        self.wrapper_settings.layout().addWidget(self.checkbox_show_pos_tags, 0, 0)
        self.wrapper_settings.layout().addWidget(self.combo_box_show_pos_tags, 0, 1)
        self.wrapper_settings.layout().addWidget(self.label_show_pos_tags, 0, 2)
        self.wrapper_settings.layout().addWidget(self.checkbox_show_lemmas, 1, 0, 1, 4)
        self.wrapper_settings.layout().addWidget(self.checkbox_collapse_punc_marks, 2, 0, 1, 4)
        self.wrapper_settings.layout().addWidget(self.checkbox_compact_mode, 3, 0, 1, 4)
        self.wrapper_settings.layout().addWidget(self.checkbox_show_in_separate_tab, 4, 0, 1, 4)

        self.wrapper_settings.layout().setColumnStretch(3, 1)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        self.checkbox_show_pos_tags.setChecked(settings['show_pos_tags'])

        if settings['show_fine_grained_pos_tags']:
            self.combo_box_show_pos_tags.setCurrentText(self.tr('fine-grained'))
        else:
            self.combo_box_show_pos_tags.setCurrentText(self.tr('coarse-grained'))

        self.checkbox_show_lemmas.setChecked(settings['show_lemmas'])
        self.checkbox_collapse_punc_marks.setChecked(settings['collapse_punc_marks'])
        self.checkbox_compact_mode.setChecked(settings['compact_mode'])
        self.checkbox_show_in_separate_tab.setChecked(settings['show_in_separate_tab'])

        self.checkbox_show_pos_tags.stateChanged.emit(self.checkbox_show_pos_tags.checkState())

    def save_settings(self):
        self.settings_custom['show_pos_tags'] = self.checkbox_show_pos_tags.isChecked()

        if self.combo_box_show_pos_tags.currentText() == self.tr('fine-grained'):
            self.settings_custom['show_fine_grained_pos_tags'] = True
        elif self.combo_box_show_pos_tags.currentText() == self.tr('coarse-grained'):
            self.settings_custom['show_fine_grained_pos_tags'] = False

        self.settings_custom['show_lemmas'] = self.checkbox_show_lemmas.isChecked()
        self.settings_custom['collapse_punc_marks'] = self.checkbox_collapse_punc_marks.isChecked()
        self.settings_custom['compact_mode'] = self.checkbox_compact_mode.isChecked()
        self.settings_custom['show_in_separate_tab'] = self.checkbox_show_in_separate_tab.isChecked()

class Wl_Worker_Preview_Dependency_Parser(wl_threading.Wl_Worker_No_Progress):
    worker_done = pyqtSignal(list)

    def run(self):
        settings = self.main.settings_custom['dependency_parsing']['preview']

        preview_lang = settings['preview_lang']
        preview_samples = settings['preview_samples']

        htmls = wl_dependency_parsing.wl_dependency_parse_fig(
            self.main, preview_samples,
            lang = preview_lang,
            dependency_parser = self.dependency_parser,
            show_pos_tags = settings['preview_settings']['show_pos_tags'],
            show_fine_grained_pos_tags = settings['preview_settings']['show_fine_grained_pos_tags'],
            # "Show lemmas" requires "Show part-of-speech tags"
            show_lemmas = settings['preview_settings']['show_pos_tags'] and settings['preview_settings']['show_lemmas'],
            collapse_punc_marks = settings['preview_settings']['collapse_punc_marks'],
            compact_mode = settings['preview_settings']['compact_mode'],
            show_in_separate_tab = settings['preview_settings']['show_in_separate_tab']
        )

        self.worker_done.emit(htmls)
