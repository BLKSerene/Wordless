# ----------------------------------------------------------------------
# Wordless: Concordancer (Parallel Mode)
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
import random
import traceback

import nltk
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox

from wl_dialogs import wl_dialogs_errs, wl_dialogs_misc, wl_msg_boxes
from wl_nlp import wl_matching, wl_nlp_utils, wl_token_processing
from wl_utils import wl_misc, wl_msgs, wl_threading
from wl_widgets import wl_boxes, wl_labels, wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wl_Table_Concordancer_Parallel_Upper(wl_tables.Wl_Table_Data_Sort_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'concordancer_parallel',
            headers = [
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Left'),
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Node'),
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Right'),
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Segment No.'),
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Segment No. %')
            ],
            headers_int = [
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Segment No.')
            ],
            headers_pct = [
                _tr('Wl_Table_Concordancer_Parallel_Upper', 'Segment No. %')
            ]
        )

        self.button_exp_selected.hide()
        self.button_exp_all.hide()
        self.button_clr.hide()

class Wl_Table_Concordancer_Parallel_Lower(wl_tables.Wl_Table_Data):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'concordancer_parallel',
            headers = [
                _tr('Wl_Table_Concordancer_Parallel_Lower', 'Parallel Text'),
                _tr('Wl_Table_Concordancer_Parallel_Lower', 'Segment No.'),
                _tr('Wl_Table_Concordancer_Parallel_Lower', 'Segment No. %')
            ],
            headers_int = [
                _tr('Wl_Table_Concordancer_Parallel_Lower', 'Segment No.')
            ],
            headers_pct = [
                _tr('Wl_Table_Concordancer_Parallel_Lower', 'Segment No. %')
            ]
        )

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_fig.setEnabled(False)

        self.button_generate_table.clicked.connect(lambda: generate_table(
            self.main,
            table_src = parent.table_concordancer_parallel_upper,
            table_tgt = parent.table_concordancer_parallel_lower
        ))
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())

    def file_changed(self, item):
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)

class Wl_Combo_Box_File_Concordancer(wl_boxes.Wl_Combo_Box_File):
    def wl_files_changed(self):
        if self.currentText() == self.tr('*** None ***'):
            file_old = ''
        else:
            file_old = self.currentText()

        self.clear()

        for file in self.main.wl_file_area.get_selected_files():
            self.addItem(file['name'])

        if self.count() > 0:
            if self.findText(file_old) > -1:
                self.setCurrentText(file_old)
        else:
            self.addItem(self.tr('*** None ***'))

class Wrapper_Concordancer_Parallel(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.table_concordancer_parallel_upper = Wl_Table_Concordancer_Parallel_Upper(self)
        self.table_concordancer_parallel_lower = Wl_Table_Concordancer_Parallel_Lower(self)

        self.table_concordancer_parallel_upper.add_tables([self.table_concordancer_parallel_lower])

        self.table_concordancer_parallel_upper.verticalScrollBar().valueChanged.connect(self.table_concordancer_parallel_lower.verticalScrollBar().setValue)
        self.table_concordancer_parallel_lower.verticalScrollBar().valueChanged.connect(self.table_concordancer_parallel_upper.verticalScrollBar().setValue)

        self.table_concordancer_parallel_lower.add_linked_table(self.table_concordancer_parallel_upper)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_concordancer_parallel_upper.label_number_results, 0, 0)
        layout_results.addWidget(self.table_concordancer_parallel_upper.button_results_sort, 0, 3)
        layout_results.addWidget(self.table_concordancer_parallel_upper.button_results_search, 0, 4)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_upper, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_lower, 2, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_lower.button_generate_table, 3, 0)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_lower.button_generate_fig, 3, 1)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_lower.button_exp_selected, 3, 2)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_lower.button_exp_all, 3, 3)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel_lower.button_clr, 3, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_puncs,

            self.token_checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings_concordancer(self)

        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.token_checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 0, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.token_checkbox_ignore_tags, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 2, 1)

        # Search Settings
        self.group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

        (
            self.label_search_term,
            self.checkbox_multi_search_mode,

            self.stacked_widget_search_term,
            self.line_edit_search_term,
            self.list_search_terms,
            self.label_separator,

            self.checkbox_ignore_case,
            self.checkbox_match_inflected_forms,
            self.checkbox_match_whole_words,
            self.checkbox_use_regex,

            self.search_checkbox_ignore_tags,
            self.checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(
            self,
            tab = 'concordancer_parallel'
        )

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(
            self,
            tab = 'concordancer_parallel'
        )

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_concordancer_parallel_lower.button_generate_table.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.search_checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        layout_context_settings = wl_layouts.Wl_Layout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_separator, 2, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_ignore_case, 3, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_words, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.search_checkbox_ignore_tags, 7, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 10, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'), self)

        self.label_src_file = QLabel(self.tr('Source File:'), self)
        self.combo_box_src_file = Wl_Combo_Box_File_Concordancer(self)
        self.label_tgt_file = QLabel(self.tr('Target File:'), self)
        self.combo_box_tgt_file = Wl_Combo_Box_File_Concordancer(self)

        self.combo_box_src_file.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_tgt_file.currentTextChanged.connect(self.generation_settings_changed)

        self.label_sampling_method = QLabel(self.tr('Sampling Method:'), self)
        self.combo_box_sampling_method = wl_boxes.Wl_Combo_Box(self)
        self.stacked_widget_sample_size_text = wl_layouts.Wl_Stacked_Widget(self)
        self.label_sample_size_first_n_lines = QLabel(self.tr('Sample Size:'), self)
        self.label_sample_size_systematic_fixed_interval = QLabel(self.tr('Sampling Interval:'), self)
        self.label_sample_size_systematic_fixed_size = QLabel(self.tr('Sample Size:'), self)
        self.label_sample_size_random = QLabel(self.tr('Sample Size:'), self)
        self.stacked_widget_sample_size_val = wl_layouts.Wl_Stacked_Widget(self)
        self.spin_box_sample_size_first_n_lines = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_sample_size_systematic_fixed_interval = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_sample_size_systematic_fixed_size = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_sample_size_random = wl_boxes.Wl_Spin_Box(self)

        self.stacked_widget_sample_size_text.addWidget(self.label_sample_size_first_n_lines)
        self.stacked_widget_sample_size_text.addWidget(self.label_sample_size_systematic_fixed_interval)
        self.stacked_widget_sample_size_text.addWidget(self.label_sample_size_systematic_fixed_size)
        self.stacked_widget_sample_size_text.addWidget(self.label_sample_size_random)
        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_first_n_lines)
        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_systematic_fixed_interval)
        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_systematic_fixed_size)
        self.stacked_widget_sample_size_val.addWidget(self.spin_box_sample_size_random)

        self.combo_box_sampling_method.addItems([
            self.tr('None'),
            self.tr('First n Lines'),
            self.tr('Systematic (Fixed Interval)'),
            self.tr('Systematic (Fixed Size)'),
            self.tr('Random')
        ])

        self.spin_box_sample_size_first_n_lines.setRange(1, 1000000)
        self.spin_box_sample_size_systematic_fixed_interval.setRange(2, 10000)
        self.spin_box_sample_size_systematic_fixed_size.setRange(1, 10000)
        self.spin_box_sample_size_random.setRange(1, 1000000)

        self.combo_box_sampling_method.currentTextChanged.connect(self.generation_settings_changed)
        self.spin_box_sample_size_first_n_lines.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_sample_size_systematic_fixed_interval.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_sample_size_systematic_fixed_size.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_sample_size_random.valueChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_src_file, 0, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_src_file, 1, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.label_tgt_file, 2, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_tgt_file, 3, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 4, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(self.label_sampling_method, 5, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_sampling_method, 5, 1)
        self.group_box_generation_settings.layout().addWidget(self.stacked_widget_sample_size_text, 6, 0)
        self.group_box_generation_settings.layout().addWidget(self.stacked_widget_sample_size_val, 6, 1)

        self.group_box_generation_settings.layout().setColumnStretch(1, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [
                self.table_concordancer_parallel_upper,
                self.table_concordancer_parallel_lower
            ]
        )

        self.checkbox_show_cumulative.hide()
        self.checkbox_show_breakdown.hide()

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)

        self.wrapper_settings.layout().setRowStretch(4, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['concordancer_parallel'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['concordancer_parallel'])

        # Token Settings
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.token_checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_settings']['search_term'])
            self.list_search_terms.load_items(settings['search_settings']['search_terms'])

        self.checkbox_ignore_case.setChecked(settings['search_settings']['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        self.checkbox_match_whole_words.setChecked(settings['search_settings']['match_whole_words'])
        self.checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])

        self.search_checkbox_ignore_tags.setChecked(settings['search_settings']['ignore_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        # Context Settings
        if defaults:
            self.main.wl_context_settings_concordancer.load_settings(defaults = True)

        # Generation Settings
        self.combo_box_src_file.setCurrentText(settings['generation_settings']['src_file'])
        self.combo_box_tgt_file.setCurrentText(settings['generation_settings']['tgt_file'])

        self.combo_box_sampling_method.setCurrentText(settings['generation_settings']['sampling_method'])
        self.spin_box_sample_size_first_n_lines.setValue(settings['generation_settings']['sample_size_first_n_lines'])
        self.spin_box_sample_size_systematic_fixed_interval.setValue(settings['generation_settings']['sample_size_systematic_fixed_interval'])
        self.spin_box_sample_size_systematic_fixed_size.setValue(settings['generation_settings']['sample_size_systematic_fixed_size'])
        self.spin_box_sample_size_random.setValue(settings['generation_settings']['sample_size_random'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])

        self.token_settings_changed()
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['token_settings']

        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['ignore_tags'] = self.token_checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        # Check if searching is enabled
        if self.group_box_search_settings.isChecked():
            self.checkbox_match_tags.token_settings_changed()
        else:
            self.group_box_search_settings.setChecked(True)

            self.checkbox_match_tags.token_settings_changed()

            self.group_box_search_settings.setChecked(False)

        self.main.wl_context_settings_concordancer.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.model().stringList()

        settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()

        settings['ignore_tags'] = self.search_checkbox_ignore_tags.isChecked()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['generation_settings']

        if self.combo_box_src_file.currentText() == self.tr('*** None ***'):
            settings['src_file'] = ''
        else:
            settings['src_file'] = self.combo_box_src_file.currentText()

        if self.combo_box_tgt_file.currentText() == self.tr('*** None ***'):
            settings['tgt_file'] = ''
        else:
            settings['tgt_file'] = self.combo_box_tgt_file.currentText()

        settings['sampling_method'] = self.combo_box_sampling_method.currentText()
        settings['sample_size_first_n_lines'] = self.spin_box_sample_size_first_n_lines.value()
        settings['sample_size_systematic_fixed_interval'] = self.spin_box_sample_size_systematic_fixed_interval.value()
        settings['sample_size_systematic_fixed_size'] = self.spin_box_sample_size_systematic_fixed_size.value()
        settings['sample_size_random'] = self.spin_box_sample_size_random.value()

        # Sampling Method
        if settings['sampling_method'] == self.tr('None'):
            self.stacked_widget_sample_size_text.hide()
            self.stacked_widget_sample_size_val.hide()
        else:
            self.stacked_widget_sample_size_text.show()
            self.stacked_widget_sample_size_val.show()

            if settings['sampling_method'] == self.tr('First n Lines'):
                self.stacked_widget_sample_size_text.setCurrentIndex(0)
                self.stacked_widget_sample_size_val.setCurrentIndex(0)
            elif settings['sampling_method'] == self.tr('Systematic (Fixed Interval)'):
                self.stacked_widget_sample_size_text.setCurrentIndex(1)
                self.stacked_widget_sample_size_val.setCurrentIndex(1)
            elif settings['sampling_method'] == self.tr('Systematic (Fixed Size)'):
                self.stacked_widget_sample_size_text.setCurrentIndex(2)
                self.stacked_widget_sample_size_val.setCurrentIndex(2)
            elif settings['sampling_method'] == self.tr('Random'):
                self.stacked_widget_sample_size_text.setCurrentIndex(3)
                self.stacked_widget_sample_size_val.setCurrentIndex(3)

    def table_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()

class Wl_Worker_Concordancer_Parallel_Table(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        concordance_lines = []

        try:
            settings = self.main.settings_custom['concordancer_parallel']

            src_file_name = settings['generation_settings']['src_file']
            tgt_file_name = settings['generation_settings']['tgt_file']

            src_file = self.main.wl_file_area.find_file_by_name(src_file_name, selected_only = True)
            tgt_file = self.main.wl_file_area.find_file_by_name(tgt_file_name, selected_only = True)

            text_src = copy.deepcopy(src_file['text'])
            text_tgt = copy.deepcopy(tgt_file['text'])

            len_segs_src = len(text_src.offsets_paras)
            len_segs_tgt = len(text_tgt.offsets_paras)
            len_segs = max([len_segs_src, len_segs_tgt])

            tokens_src = wl_token_processing.wl_process_tokens_concordancer(
                self.main, text_src,
                token_settings = settings['token_settings'],
                preserve_blank_lines = True
            )
            tokens_tgt = wl_token_processing.wl_process_tokens_concordancer(
                self.main, text_tgt,
                token_settings = settings['token_settings'],
                preserve_blank_lines = True
            )

            if (
                not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']
                or settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']
            ):
                search_terms = wl_matching.match_search_terms(
                    self.main, tokens_src,
                    lang = text_src.lang,
                    tokenized = text_src.tokenized,
                    tagged = text_src.tagged,
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                (search_terms_inclusion,
                 search_terms_exclusion) = wl_matching.match_search_terms_context(
                    self.main, tokens_src,
                    lang = text_src.lang,
                    tokenized = text_src.tokenized,
                    tagged = text_src.tagged,
                    token_settings = settings['token_settings'],
                    context_settings = settings['context_settings']
                )

                if search_terms:
                    len_search_term_min = min([len(search_term) for search_term in search_terms])
                    len_search_term_max = max([len(search_term) for search_term in search_terms])
                else:
                    len_search_term_min = 0
                    len_search_term_max = 0

                for len_search_term in range(len_search_term_min, len_search_term_max + 1):
                    for i, ngram in enumerate(nltk.ngrams(tokens_src, len_search_term)):
                        if (
                            ngram in search_terms
                            and wl_matching.check_context(
                                i, tokens_src,
                                context_settings = settings['context_settings'],
                                search_terms_inclusion = search_terms_inclusion,
                                search_terms_exclusion = search_terms_exclusion
                            )
                        ):
                            concordance_line = []

                            # Segment No.
                            if text_src.offsets_paras[-1] <= i:
                                no_seg = len_segs_src
                            else:
                                for j, i_para in enumerate(text_src.offsets_paras):
                                    if i_para > i:
                                        no_seg = j

                                        break

                            # Search in Results (Node)
                            text_search_node = list(ngram)

                            if not settings['token_settings']['puncs']:
                                ngram = text_src.tokens_flat[i : i + len_search_term]

                            node_text = ' '.join(ngram)
                            node_text = wl_nlp_utils.escape_text(node_text)

                            offset_para_start_src = text_src.offsets_paras[max(0, no_seg - 1)]
                            if no_seg <= len_segs_tgt:
                                offset_para_start_tgt = text_tgt.offsets_paras[max(0, no_seg - 1)]
                            # Omission at the end of the source text
                            else:
                                offset_para_start_tgt = None

                            # Left & Right
                                # Last paragraph
                            if no_seg >= len_segs_src:
                                offset_para_end = None
                            else:
                                offset_para_end = text_src.offsets_paras[min(no_seg, len_segs_src - 1)]

                            context_left = text_src.tokens_flat[offset_para_start_src:i]
                            context_right = text_src.tokens_flat[i + len_search_term : offset_para_end]

                            # Search in Results (Left & Right)
                            if settings['token_settings']['puncs']:
                                text_search_left = copy.deepcopy(context_left)
                                text_search_right = copy.deepcopy(context_right)
                            else:
                                text_search_left = tokens_src[offset_para_start_src:i]
                                text_search_right = tokens_src[i + len_search_term : offset_para_end]

                            context_left = wl_nlp_utils.escape_tokens(context_left)
                            context_right = wl_nlp_utils.escape_tokens(context_right)

                            context_left_text = ' '.join(context_left)
                            context_right_text = ' '.join(context_right)

                            # Parallel Text
                            if no_seg <= len_segs_tgt:
                                # Last paragraph
                                if no_seg == len_segs_tgt:
                                    offset_para_end = None
                                else:
                                    offset_para_end = text_tgt.offsets_paras[min(no_seg, len_segs_tgt - 1)]

                                parallel_text = text_tgt.tokens_flat[offset_para_start_tgt:offset_para_end]
                            # Omission at the end of the source text
                            else:
                                parallel_text = []

                            # Search in Results (Parallel Text)
                            if settings['token_settings']['puncs']:
                                text_search_parallel_text = copy.deepcopy(parallel_text)
                            else:
                                text_search_parallel_text = tokens_tgt[offset_para_start_tgt:offset_para_end]

                            parallel_text = wl_nlp_utils.escape_tokens(parallel_text)

                            parallel_text_text = ' '.join(parallel_text)

                            # Left
                            concordance_line.append([context_left_text, context_left, text_search_left])
                            # Node
                            concordance_line.append([node_text, list(ngram), text_search_node])
                            # Right
                            concordance_line.append([context_right_text, context_right, text_search_right])
                            # Segment No.
                            # * The largest count of segments among source and target files should be passed here since there might be addition or omission during translation at the end of the source text
                            concordance_line.append([no_seg, len_segs])

                            # Parallel Text
                            concordance_line.append([parallel_text_text, parallel_text, text_search_parallel_text])

                            concordance_lines.append(concordance_line)
            # Search for additions
            else:
                for i, para_tgt in enumerate(text_tgt.tokens_multilevel):
                    if i <= len_segs_src - 1:
                        para_src = text_src.tokens_multilevel[i]
                    else:
                        para_src = []

                    if para_src == [] and para_tgt:
                        concordance_line = []
                        no_seg = i + 1

                        offset_para_start_tgt = text_tgt.offsets_paras[max(0, no_seg - 1)]

                        # Parallel Text
                        if no_seg == len_segs_tgt:
                            offset_para_end = None
                        else:
                            offset_para_end = text_tgt.offsets_paras[min(no_seg, len_segs_tgt - 1)]

                        parallel_text = text_tgt.tokens_flat[offset_para_start_tgt:offset_para_end]

                        # Search in Results (Parallel Text)
                        if settings['token_settings']['puncs']:
                            text_search_parallel_text = copy.deepcopy(parallel_text)
                        else:
                            text_search_parallel_text = tokens_tgt[offset_para_start_tgt:offset_para_end]

                        parallel_text = wl_nlp_utils.escape_tokens(parallel_text)

                        parallel_text_text = ' '.join(parallel_text)

                        # Left
                        concordance_line.append(['', [], []])
                        # Node
                        concordance_line.append(['', [], []])
                        # Right
                        concordance_line.append(['', [], []])
                        # Segment No.
                        concordance_line.append([no_seg, len_segs])

                        # Parallel Text
                        concordance_line.append([parallel_text_text, parallel_text, text_search_parallel_text])

                        concordance_lines.append(concordance_line)

            # Sampling - First n Lines
            if settings['generation_settings']['sampling_method'] == self.tr('First n Lines'):
                sample_size = settings['generation_settings']['sample_size_first_n_lines']

                concordance_lines = concordance_lines[:sample_size]
            # Sampling - Systematic (Fixed Interval)
            elif settings['generation_settings']['sampling_method'] == self.tr('Systematic (Fixed Interval)'):
                sampling_interval = settings['generation_settings']['sample_size_systematic_fixed_interval']

                concordance_lines = [line
                                     for i, line in enumerate(concordance_lines)
                                     if i % sampling_interval == 0]
            # Sampling - Systematic (Fixed Size)
            elif settings['generation_settings']['sampling_method'] == self.tr('Systematic (Fixed Size)'):
                sample_size = settings['generation_settings']['sample_size_systematic_fixed_size']
                sampling_interval = len(concordance_lines) // sample_size

                if sampling_interval > 0:
                    concordance_lines_sampled = []

                    for i, line in enumerate(concordance_lines):
                        if i % sampling_interval == 0:
                            concordance_lines_sampled.append(line)

                        if len(concordance_lines_sampled) >= sample_size:
                            break

                    concordance_lines = concordance_lines_sampled
            # Sampling - Random
            elif settings['generation_settings']['sampling_method'] == self.tr('Random'):
                sample_size = settings['generation_settings']['sample_size_random']

                if sample_size < len(concordance_lines):
                    concordance_lines_sampled = random.sample(concordance_lines, k = sample_size)

                    concordance_lines = [
                        line
                        for line in concordance_lines
                        if line in concordance_lines_sampled
                    ]
        except Exception:
            err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(err_msg, concordance_lines)

@wl_misc.log_timing
def generate_table(main, table_src, table_tgt):
    def update_gui(err_msg, concordance_lines):
        if not err_msg:
            if concordance_lines:
                try:
                    table_src.settings = copy.deepcopy(main.settings_custom)

                    table_src.clr_table(0)
                    table_tgt.clr_table(0)

                    table_src.model().setRowCount(len(concordance_lines))
                    table_tgt.model().setRowCount(len(concordance_lines))

                    table_src.disable_updates()
                    table_tgt.disable_updates()

                    for i, concordance_line in enumerate(concordance_lines):
                        left_text, left_text_raw, left_text_search = concordance_line[0]
                        node_text, node_text_raw, node_text_search = concordance_line[1]
                        right_text, right_text_raw, right_text_search = concordance_line[2]

                        no_seg, len_segs = concordance_line[3]

                        parallel_text_text, parallel_text_text_raw, parallel_text_text_search = concordance_line[4]

                        # Node
                        label_node = wl_labels.Wl_Label_Html(
                            f'''
                                <span style="color: {settings['sort_results']['highlight_colors'][0]}; font-weight: bold;">
                                    &nbsp;{node_text}&nbsp;
                                </span>
                            ''',
                            main
                        )

                        table_src.setIndexWidget(table_src.model().index(i, 1), label_node)

                        table_src.indexWidget(table_src.model().index(i, 1)).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                        table_src.indexWidget(table_src.model().index(i, 1)).text_raw = node_text_raw
                        table_src.indexWidget(table_src.model().index(i, 1)).text_search = node_text_search

                        # Left
                        table_src.setIndexWidget(
                            table_src.model().index(i, 0),
                            wl_labels.Wl_Label_Html(left_text, main)
                        )

                        table_src.indexWidget(table_src.model().index(i, 0)).setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                        table_src.indexWidget(table_src.model().index(i, 0)).text_raw = left_text_raw
                        table_src.indexWidget(table_src.model().index(i, 0)).text_search = left_text_search

                        # Right
                        table_src.setIndexWidget(
                            table_src.model().index(i, 2),
                            wl_labels.Wl_Label_Html(right_text, main)
                        )

                        table_src.indexWidget(table_src.model().index(i, 2)).text_raw = right_text_raw
                        table_src.indexWidget(table_src.model().index(i, 2)).text_search = right_text_search

                        # Segment No. (Source File)
                        table_src.set_item_num(i, 3, no_seg)
                        table_src.set_item_num(i, 4, no_seg, len_segs)

                        # Parallel Text
                        table_tgt.setIndexWidget(
                            table_tgt.model().index(i, 0),
                            wl_labels.Wl_Label_Html(parallel_text_text, main)
                        )

                        table_tgt.indexWidget(table_tgt.model().index(i, 0)).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                        table_tgt.indexWidget(table_tgt.model().index(i, 0)).text_raw = parallel_text_text_raw
                        table_tgt.indexWidget(table_tgt.model().index(i, 0)).text_search = parallel_text_text_search

                        # Segment No. (Target File)
                        table_tgt.set_item_num(i, 1, no_seg)
                        table_tgt.set_item_num(i, 2, no_seg, len_segs)

                    table_src.enable_updates()
                    table_tgt.enable_updates()

                    table_src.toggle_pct()
                    table_tgt.toggle_pct()

                    wl_msgs.wl_msg_generate_table_success(main)
                except Exception:
                    err_msg = traceback.format_exc()
            else:
                wl_msg_boxes.wl_msg_box_no_results(main)
                wl_msgs.wl_msg_generate_table_error(main)

        if err_msg:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
            wl_msgs.wl_msg_fatal_error(main)

    settings = main.settings_custom['concordancer_parallel']

    # Check for identical source and target files
    if settings['generation_settings']['src_file'] != settings['generation_settings']['tgt_file']:
        # Check for empty search term
        if (
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']
            or settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']
        ):
            search_additions = True
        else:
            search_additions = wl_msg_boxes.wl_msg_box_question(
                main,
                title = _tr('wl_concordancer_parallel', 'Empty Search Terms'),
                text = _tr('wl_concordancer_parallel', '''
                    <div>You have not specified any search terms. Do you want to search for additions in the target file?</div>
                ''')
            )

        # Ask for confirmation
        if search_additions:
            worker_concordancer_parallel_table = Wl_Worker_Concordancer_Parallel_Table(
                main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
                update_gui = update_gui
            )
            wl_threading.Wl_Thread(worker_concordancer_parallel_table).start_worker()
        else:
            wl_msgs.wl_msg_generate_table_error(main)
    else:
        wl_msg_boxes.Wl_Msg_Box_Warning(
            main,
            title = _tr('wl_concordancer_parallel', 'Identical source and target files'),
            text = _tr('wl_concordancer_parallel', '''
                <div>The source and target file you have specified are identical. Please check your settings and try again.</div>
            ''')
        ).open()
        wl_msgs.wl_msg_generate_table_error(main)
