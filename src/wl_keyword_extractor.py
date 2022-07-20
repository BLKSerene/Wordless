# ----------------------------------------------------------------------
# Wordless: Keyword Extractor
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

import collections
import copy
import traceback

import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialogs_errs, wl_dialogs_misc, wl_msg_boxes
from wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wl_nlp import wl_nlp_utils, wl_texts, wl_token_processing
from wl_utils import wl_misc, wl_msgs, wl_sorting, wl_threading
from wl_widgets import wl_layouts, wl_lists, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wl_Table_Keyword_Extractor(wl_tables.Wl_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'keyword_extractor',
            headers = [
                _tr('Wl_Table_Keyword_Extractor', 'Rank'),
                _tr('Wl_Table_Keyword_Extractor', 'Keyword'),
                _tr('Wl_Table_Keyword_Extractor', 'Number of\nFiles Found'),
                _tr('Wl_Table_Keyword_Extractor', 'Number of\nFiles Found %')
            ],
            headers_int = [
                _tr('Wl_Table_Keyword_Extractor', 'Rank'),
                _tr('Wl_Table_Keyword_Extractor', 'Number of\nFiles Found')
            ],
            headers_pct = [
                _tr('Wl_Table_Keyword_Extractor', 'Number of\nFiles Found %')
            ],
            sorting_enabled = True
        )

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_fig.clicked.connect(lambda: generate_fig(self.main))
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)
        self.main.wl_file_area_ref.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())
        self.main.wl_file_area_ref.table_files.model().itemChanged.emit(QStandardItem())

    def file_changed(self, item):
        # Enable the buttons and prompt the user if there are only observed files or only reference files
        if list(self.main.wl_file_area.get_selected_files()) or list(self.main.wl_file_area_ref.get_selected_files()):
            self.button_generate_table.setEnabled(True)
            self.button_generate_fig.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)
            self.button_generate_fig.setEnabled(False)

class Wrapper_Keyword_Extractor(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_keyword_extractor = Wl_Table_Keyword_Extractor(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_keyword_extractor.label_number_results, 0, 0)
        layout_results.addWidget(self.table_keyword_extractor.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_keyword_extractor.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_exp_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_exp_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_clr, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_words,
            self.checkbox_all_lowercase,
            self.checkbox_all_uppercase,
            self.checkbox_title_case,
            self.checkbox_nums,
            self.checkbox_puncs,

            self.checkbox_treat_as_all_lowercase,
            self.checkbox_lemmatize_tokens,
            self.checkbox_filter_stop_words,

            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lemmatize_tokens.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 2, 1)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_all_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lemmatize_tokens, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 8, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 8, 1)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        (
            self.label_test_significance,
            self.combo_box_test_significance
        ) = wl_widgets.wl_widgets_test_significance(self)
        (
            self.label_measure_effect_size,
            self.combo_box_measure_effect_size
        ) = wl_widgets.wl_widgets_measure_effect_size(self)

        (
            self.label_settings_measures,
            self.button_settings_measures
        ) = wl_widgets.wl_widgets_settings_measures(
            self,
            node = self.tr('Statistical Significance')
        )

        self.combo_box_test_significance.addItems(list(self.main.settings_global['tests_significance']['keyword_extractor'].keys()))
        self.combo_box_measure_effect_size.addItems(list(self.main.settings_global['measures_effect_size']['keyword_extractor'].keys()))

        self.combo_box_test_significance.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_effect_size.currentTextChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_test_significance, 0, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_test_significance, 1, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_effect_size, 2, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_effect_size, 3, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 4, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(self.label_settings_measures, 5, 0)
        self.group_box_generation_settings.layout().addWidget(self.button_settings_measures, 5, 1)

        self.group_box_token_settings.layout().setColumnStretch(1, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_keyword_extractor]
        )

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        (
            self.label_graph_type,
            self.combo_box_graph_type,
            self.label_sort_by_file,
            self.combo_box_sort_by_file,
            self.label_use_data,
            self.combo_box_use_data,
            self.checkbox_use_pct,
            self.checkbox_use_cumulative
        ) = wl_widgets.wl_widgets_fig_settings(self)

        self.label_rank = QLabel(self.tr('Rank:'), self)
        (
            self.label_rank_min,
            self.spin_box_rank_min,
            self.checkbox_rank_min_no_limit,
            self.label_rank_max,
            self.spin_box_rank_max,
            self.checkbox_rank_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        self.combo_box_graph_type.currentTextChanged.connect(self.fig_settings_changed)
        self.combo_box_sort_by_file.currentTextChanged.connect(self.fig_settings_changed)
        self.combo_box_use_data.currentTextChanged.connect(self.fig_settings_changed)
        self.checkbox_use_pct.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_use_cumulative.stateChanged.connect(self.fig_settings_changed)

        self.spin_box_rank_min.valueChanged.connect(self.fig_settings_changed)
        self.checkbox_rank_min_no_limit.stateChanged.connect(self.fig_settings_changed)
        self.spin_box_rank_max.valueChanged.connect(self.fig_settings_changed)
        self.checkbox_rank_max_no_limit.stateChanged.connect(self.fig_settings_changed)

        layout_fig_settings_combo_boxes = wl_layouts.Wl_Layout()
        layout_fig_settings_combo_boxes.addWidget(self.label_graph_type, 0, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_graph_type, 0, 1)
        layout_fig_settings_combo_boxes.addWidget(self.label_sort_by_file, 1, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_sort_by_file, 1, 1)
        layout_fig_settings_combo_boxes.addWidget(self.label_use_data, 2, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_use_data, 2, 1)

        layout_fig_settings_combo_boxes.setColumnStretch(1, 1)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addLayout(layout_fig_settings_combo_boxes, 0, 0, 1, 3)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_use_pct, 1, 0, 1, 3)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_use_cumulative, 2, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(self.label_rank, 4, 0, 1, 3)
        self.group_box_fig_settings.layout().addWidget(self.label_rank_min, 5, 0)
        self.group_box_fig_settings.layout().addWidget(self.spin_box_rank_min, 5, 1)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_min_no_limit, 5, 2)
        self.group_box_fig_settings.layout().addWidget(self.label_rank_max, 6, 0)
        self.group_box_fig_settings.layout().addWidget(self.spin_box_rank_max, 6, 1)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_max_no_limit, 6, 2)

        self.group_box_fig_settings.layout().setColumnStretch(1, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 3, 0)

        self.wrapper_settings.layout().setRowStretch(4, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['keyword_extractor'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['keyword_extractor'])

        # Token Settings
        self.checkbox_words.setChecked(settings['token_settings']['words'])
        self.checkbox_all_lowercase.setChecked(settings['token_settings']['all_lowercase'])
        self.checkbox_all_uppercase.setChecked(settings['token_settings']['all_uppercase'])
        self.checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        self.checkbox_nums.setChecked(settings['token_settings']['nums'])
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.checkbox_treat_as_all_lowercase.setChecked(settings['token_settings']['treat_as_all_lowercase'])
        self.checkbox_lemmatize_tokens.setChecked(settings['token_settings']['lemmatize_tokens'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Generation Settings
        self.combo_box_test_significance.setCurrentText(settings['generation_settings']['test_significance'])
        self.combo_box_measure_effect_size.setCurrentText(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        # Figure Settings
        self.combo_box_graph_type.setCurrentText(settings['fig_settings']['graph_type'])
        self.combo_box_sort_by_file.setCurrentText(settings['fig_settings']['sort_by_file'])
        self.combo_box_use_data.setCurrentText(settings['fig_settings']['use_data'])
        self.checkbox_use_pct.setChecked(settings['fig_settings']['use_pct'])
        self.checkbox_use_cumulative.setChecked(settings['fig_settings']['use_cumulative'])

        self.spin_box_rank_min.setValue(settings['fig_settings']['rank_min'])
        self.checkbox_rank_min_no_limit.setChecked(settings['fig_settings']['rank_min_no_limit'])
        self.spin_box_rank_max.setValue(settings['fig_settings']['rank_max'])
        self.checkbox_rank_max_no_limit.setChecked(settings['fig_settings']['rank_max_no_limit'])

        self.token_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['keyword_extractor']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['all_lowercase'] = self.checkbox_all_lowercase.isChecked()
        settings['all_uppercase'] = self.checkbox_all_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['keyword_extractor']['generation_settings']

        settings['test_significance'] = self.combo_box_test_significance.currentText()
        settings['measure_effect_size'] = self.combo_box_measure_effect_size.currentText()

        # Use Data
        use_data_old = self.combo_box_use_data.currentText()

        text_test_significance = settings['test_significance']
        text_measure_effect_size = settings['measure_effect_size']

        self.combo_box_use_data.clear()

        self.combo_box_use_data.addItem(self.tr('Frequency'))
        self.combo_box_use_data.addItems(
            [col
             for col in self.main.settings_global['tests_significance']['keyword_extractor'][text_test_significance]['cols']
             if col]
        )
        self.combo_box_use_data.addItem(self.main.settings_global['measures_effect_size']['keyword_extractor'][text_measure_effect_size]['col'])

        if self.combo_box_use_data.findText(use_data_old) > -1:
            self.combo_box_use_data.setCurrentText(use_data_old)
        else:
            self.combo_box_use_data.setCurrentText(self.main.settings_default['keyword_extractor']['fig_settings']['use_data'])

    def table_settings_changed(self):
        settings = self.main.settings_custom['keyword_extractor']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['keyword_extractor']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['sort_by_file'] = self.combo_box_sort_by_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

class Wl_Worker_Keyword_Extractor(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, dict, dict)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.keywords_freq_files = []
        self.keywords_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['keyword_extractor']

            files_observed = list(self.main.wl_file_area.get_selected_files())
            files_ref = list(self.main.wl_file_area_ref.get_selected_files())

            # Frequency (Reference files)
            self.keywords_freq_files.append(collections.Counter())
            tokens_ref = []
            len_tokens_ref = 0

            for file_ref in files_ref:
                text = copy.deepcopy(file_ref['text'])
                text = wl_token_processing.wl_process_tokens_keyword_extractor(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                # Remove empty tokens
                tokens = [token for token in text.tokens_flat if token]

                self.keywords_freq_files[0] += collections.Counter(tokens)

                tokens_ref.extend(text.tokens_flat)
                len_tokens_ref += len(tokens_ref)

            # Frequency (Observed files)
            for file_observed in files_observed:
                text = copy.deepcopy(file_observed['text'])
                text = wl_token_processing.wl_process_tokens_keyword_extractor(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                # Remove empty tokens
                tokens = [token for token in text.tokens_flat if token]

                self.keywords_freq_files.append(collections.Counter(tokens))

                texts.append(text)

            # Total
            if len(files_observed) > 1:
                text_total = wl_texts.Wl_Text_Blank()
                text_total.tokens_flat = [token for text in texts for token in text.tokens_flat]

                self.keywords_freq_files.append(sum(self.keywords_freq_files[1:], collections.Counter()))

                texts.append(text_total)

            # Remove tokens that do not appear in any of the observed files
            self.keywords_freq_files[0] = {
                token: freq
                for token, freq in self.keywords_freq_files[0].items()
                if token in self.keywords_freq_files[-1].keys()
            }

            # Keyness
            text_test_significance = settings['generation_settings']['test_significance']
            text_measure_effect_size = settings['generation_settings']['measure_effect_size']

            test_significance = self.main.settings_global['tests_significance']['keyword_extractor'][text_test_significance]['func']
            measure_effect_size = self.main.settings_global['measures_effect_size']['keyword_extractor'][text_measure_effect_size]['func']

            keywords_freq_file_ref = self.keywords_freq_files[0]

            for i, text in enumerate(texts):
                keywords_stats_file = {}

                keywords_freq_file_observed = self.keywords_freq_files[i + 1]
                tokens_observed = text.tokens_flat
                len_tokens_observed = len(tokens_observed)

                if text_test_significance in [
                    _tr('Wl_Worker_Keyword_Extractor', "Student's t-test (2-sample)"),
                    _tr('Wl_Worker_Keyword_Extractor', 'Mann-Whitney U Test')
                ]:
                    # Test Statistic, p-value & Bayes Factor
                    if text_test_significance == _tr('Wl_Worker_Keyword_Extractor', "Student's t-test (2-sample)"):
                        num_sections = self.main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['num_sections']
                        use_data = self.main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['use_data']
                    elif text_test_significance == _tr('Wl_Worker_Keyword_Extractor', 'Mann-Whitney U Test'):
                        num_sections = self.main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['num_sections']
                        use_data = self.main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['use_data']

                    sections_observed = wl_nlp_utils.to_sections(tokens_observed, num_sections)
                    sections_ref = wl_nlp_utils.to_sections(tokens_ref, num_sections)

                    sections_freq_observed = [collections.Counter(section) for section in sections_observed]
                    sections_freq_ref = [collections.Counter(section) for section in sections_ref]

                    len_sections_observed = [len(section) for section in sections_observed]
                    len_sections_ref = [len(section) for section in sections_ref]

                    if use_data == _tr('Wl_Worker_Keyword_Extractor', 'Absolute Frequency'):
                        for token in keywords_freq_file_observed:
                            counts_observed = [
                                section_freq.get(token, 0)
                                for section_freq in sections_freq_observed
                            ]
                            counts_ref = [
                                section_freq.get(token, 0)
                                for section_freq in sections_freq_ref
                            ]

                            keywords_stats_file[token] = test_significance(self.main, counts_observed, counts_ref)
                    elif use_data == _tr('Wl_Worker_Keyword_Extractor', 'Relative Frequency'):
                        for token in keywords_freq_file_observed:
                            counts_observed = [
                                section_freq.get(token, 0) / len_sections_observed[i]
                                for i, section_freq in enumerate(sections_freq_observed)
                            ]
                            counts_ref = [
                                section_freq.get(token, 0) / len_sections_ref[i]
                                for i, section_freq in enumerate(sections_freq_ref)
                            ]

                            keywords_stats_file[token] = test_significance(self.main, counts_observed, counts_ref)

                    # Effect Size
                    for token in keywords_freq_file_observed:
                        c11 = keywords_freq_file_observed[token]
                        c12 = keywords_freq_file_ref.get(token, 0)
                        c21 = len_tokens_observed - c11
                        c22 = len_tokens_ref - c12

                        keywords_stats_file[token].append(measure_effect_size(self.main, c11, c12, c21, c22))
                else:
                    for token in keywords_freq_file_observed:
                        c11 = keywords_freq_file_observed[token]
                        c12 = keywords_freq_file_ref.get(token, 0)
                        c21 = len_tokens_observed - c11
                        c22 = len_tokens_ref - c12

                        # Test Statistic, p-value & Bayes Factor
                        keywords_stats_file[token] = test_significance(self.main, c11, c12, c21, c22)

                        # Effect Size
                        keywords_stats_file[token].append(measure_effect_size(self.main, c11, c12, c21, c22))

                self.keywords_stats_files.append(keywords_stats_file)

            if len(files_observed) == 1:
                self.keywords_freq_files.append(self.keywords_freq_files[1])
                self.keywords_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Keyword_Extractor_Table(Wl_Worker_Keyword_Extractor):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.keywords_freq_files),
            wl_misc.merge_dicts(self.keywords_stats_files)
        )

class Wl_Worker_Keyword_Extractor_Fig(Wl_Worker_Keyword_Extractor):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering figure...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.keywords_freq_files),
            wl_misc.merge_dicts(self.keywords_stats_files)
        )

def wl_msg_box_missing_files_observed(main):
    wl_msg_boxes.Wl_Msg_Box_Warning(
        main,
        title = _tr('wl_msg_box_missing_files_observed', 'Missing Observed Files'),
        text = _tr('wl_msg_box_missing_files_observed', '''
            <div>You have not specified any observed files yet.</div>
        ''')
    ).open()

def wl_msg_box_missing_files_ref(main):
    wl_msg_boxes.Wl_Msg_Box_Warning(
        main,
        title = _tr('wl_msg_box_missing_files_ref', 'Missing Reference Files'),
        text = _tr('wl_msg_box_missing_files_ref', '''
            <div>You have not specified any reference files yet.</div>
        ''')
    ).open()

@wl_misc.log_timing
def generate_table(main, table):
    def update_gui(err_msg, keywords_freq_files, keywords_stats_files):
        if not err_msg:
            if keywords_freq_files:
                try:
                    table.settings = copy.deepcopy(main.settings_custom)

                    text_test_significance = settings['generation_settings']['test_significance']
                    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                    (
                        text_test_stat,
                        text_p_val,
                        text_bayes_factor
                    ) = main.settings_global['tests_significance']['keyword_extractor'][text_test_significance]['cols']
                    text_effect_size = main.settings_global['measures_effect_size']['keyword_extractor'][text_measure_effect_size]['col']

                    table.clr_table()

                    # Insert columns (files)
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_keyword_extractor', '[Reference Files]\nFrequency'),
                        is_int = True, is_cumulative = True
                    )
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_keyword_extractor', '[Reference Files]\nFrequency %'),
                        is_pct = True, is_cumulative = True
                    )

                    for file_observed in files_observed:
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_keyword_extractor', '[{}]\nFrequency').format(file_observed['name']),
                            is_int = True, is_cumulative = True, is_breakdown = True
                        )
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_keyword_extractor', '[{}]\nFrequency %').format(file_observed['name']),
                            is_pct = True, is_cumulative = True, is_breakdown = True
                        )

                        if text_test_stat:
                            table.ins_header_hor(
                                table.model().columnCount() - 2,
                                f'[{file_observed["name"]}]\n{text_test_stat}',
                                is_float = True, is_breakdown = True
                            )

                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            f'[{file_observed["name"]}]\n{text_p_val}',
                            is_float = True, is_breakdown = True
                        )

                        if text_bayes_factor:
                            table.ins_header_hor(
                                table.model().columnCount() - 2,
                                f'[{file_observed["name"]}]\n{text_bayes_factor}',
                                is_float = True, is_breakdown = True
                            )

                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            f'[{file_observed["name"]}]\n{text_effect_size}',
                            is_float = True, is_breakdown = True
                        )

                    # Insert columns (total)
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_keyword_extractor', 'Total\nFrequency'),
                        is_int = True, is_cumulative = True
                    )
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_keyword_extractor', 'Total\nFrequency %'),
                        is_pct = True, is_cumulative = True
                    )

                    if text_test_stat:
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_keyword_extractor', 'Total\n') + text_test_stat,
                            is_float = True
                        )

                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_keyword_extractor', 'Total\n') + text_p_val,
                        is_float = True
                    )

                    if text_bayes_factor:
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_keyword_extractor', 'Total\n') + text_bayes_factor,
                            is_float = True
                        )

                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_keyword_extractor', 'Total\n') + text_effect_size,
                        is_float = True
                    )

                    # Sort by p-value of the first observed file
                    table.horizontalHeader().setSortIndicator(
                        table.find_header_hor(f'[{files_observed[0]["name"]}]\n{text_p_val}'),
                        Qt.AscendingOrder
                    )

                    cols_freq = table.find_headers_hor(_tr('wl_keyword_extractor', '\nFrequency'))
                    cols_freq_pct = table.find_headers_hor(_tr('wl_keyword_extractor', '\nFrequency %'))

                    for col in cols_freq_pct:
                        cols_freq.remove(col)

                    if text_test_stat:
                        cols_test_stat = table.find_headers_hor(f'\n{text_test_stat}')

                    cols_p_val = table.find_headers_hor(_tr('wl_keyword_extractor', '\np-value'))

                    if text_bayes_factor:
                        cols_bayes_factor = table.find_headers_hor(_tr('wl_keyword_extractor', '\nBayes Factor'))

                    cols_effect_size = table.find_headers_hor(f'\n{text_effect_size}')
                    col_files_found = table.find_header_hor(_tr('wl_keyword_extractor', 'Number of\nFiles Found'))
                    col_files_found_pct = table.find_header_hor(_tr('wl_keyword_extractor', 'Number of\nFiles Found %'))

                    freq_totals = numpy.array(list(keywords_freq_files.values())).sum(axis = 0)
                    len_files_observed = len(files_observed)

                    table.model().setRowCount(len(keywords_freq_files))

                    table.disable_updates()

                    for i, (keyword, stats_files) in enumerate(wl_sorting.sorted_keywords_stats_files(keywords_stats_files)):
                        freq_files = keywords_freq_files[keyword]

                        # Rank
                        table.set_item_num(i, 0, -1)

                        # Keyword
                        table.model().setItem(i, 1, wl_tables.Wl_Table_Item(keyword))

                        # Frequency
                        for j, freq in enumerate(freq_files):
                            table.set_item_num(i, cols_freq[j], freq)
                            table.set_item_num(i, cols_freq_pct[j], freq, freq_totals[j])

                        for j, (test_stat, p_val, bayes_factor, effect_size) in enumerate(stats_files):
                            # Test Statistic
                            if text_test_stat:
                                table.set_item_num(i, cols_test_stat[j], test_stat)

                            # p-value
                            table.set_item_p_val(i, cols_p_val[j], p_val)

                            # Bayes Factor
                            if text_bayes_factor:
                                table.set_item_num(i, cols_bayes_factor[j], bayes_factor)

                            # Effect Size
                            table.set_item_num(i, cols_effect_size[j], effect_size)

                        # Number of Files Found
                        num_files_found = len([freq for freq in freq_files[1:-1] if freq])

                        table.set_item_num(i, col_files_found, num_files_found)
                        table.set_item_num(i, col_files_found_pct, num_files_found, len_files_observed)

                    table.enable_updates()

                    table.toggle_pct()
                    table.toggle_cumulative()
                    table.toggle_breakdown()
                    table.update_ranks()

                    wl_msgs.wl_msg_generate_table_success(main)
                except Exception:
                    err_msg = traceback.format_exc()
            else:
                wl_msg_boxes.wl_msg_box_no_results(main)
                wl_msgs.wl_msg_generate_table_error(main)

        if err_msg:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
            wl_msgs.wl_msg_fatal_error(main)

    settings = main.settings_custom['keyword_extractor']

    files_observed = list(main.wl_file_area.get_selected_files())
    files_ref = list(main.wl_file_area_ref.get_selected_files())

    if files_observed and files_ref:
        worker_keyword_extractor_table = Wl_Worker_Keyword_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        )
        wl_threading.Wl_Thread(worker_keyword_extractor_table).start_worker()
    else:
        if not files_observed:
            wl_msg_box_missing_files_observed(main)
        elif not files_ref:
            wl_msg_box_missing_files_ref(main)

        wl_msgs.wl_msg_generate_table_error(main)

@wl_misc.log_timing
def generate_fig(main):
    def update_gui(err_msg, keywords_freq_files, keywords_stats_files):
        if not err_msg:
            if keywords_freq_files:
                try:
                    text_test_significance = settings['generation_settings']['test_significance']
                    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                    (
                        text_test_stat,
                        text_p_val,
                        text_bayes_factor
                    ) = main.settings_global['tests_significance']['keyword_extractor'][text_test_significance]['cols']
                    text_effect_size = main.settings_global['measures_effect_size']['keyword_extractor'][text_measure_effect_size]['col']

                    if settings['fig_settings']['use_data'] == _tr('wl_keyword_extractor', 'Frequency'):
                        wl_figs_freqs.wl_fig_freq_keyword_extractor(
                            main, keywords_freq_files,
                            files_ref = files_ref,
                            settings = settings['fig_settings'],
                            label_x = _tr('wl_keyword_extractor', 'Keyword')
                        )
                    else:
                        if settings['fig_settings']['use_data'] == text_test_stat:
                            keywords_stat_files = {
                                keyword: numpy.array(stats_files)[:, 0]
                                for keyword, stats_files in keywords_stats_files.items()
                            }

                            label_y = text_test_stat
                        elif settings['fig_settings']['use_data'] == text_p_val:
                            keywords_stat_files = {
                                keyword: numpy.array(stats_files)[:, 1]
                                for keyword, stats_files in keywords_stats_files.items()
                            }

                            label_y = text_p_val
                        elif settings['fig_settings']['use_data'] == text_bayes_factor:
                            keywords_stat_files = {
                                keyword: numpy.array(stats_files)[:, 2]
                                for keyword, stats_files in keywords_stats_files.items()
                            }

                            label_y = text_bayes_factor
                        elif settings['fig_settings']['use_data'] == text_effect_size:
                            keywords_stat_files = {
                                keyword: numpy.array(stats_files)[:, 3]
                                for keyword, stats_files in keywords_stats_files.items()
                            }

                            label_y = text_effect_size

                        wl_figs_stats.wl_fig_stat_keyword_extractor(
                            main, keywords_stat_files,
                            files_ref = files_ref,
                            settings = settings['fig_settings'],
                            label_y = label_y
                        )

                    # Hide the progress dialog early so that the main window will not obscure the generated figure
                    worker_keyword_extractor_fig.dialog_progress.accept()
                    wl_figs.show_fig()

                    wl_msgs.wl_msg_generate_fig_success(main)
                except Exception:
                    err_msg = traceback.format_exc()
            else:
                wl_msg_boxes.wl_msg_box_no_results(main)
                wl_msgs.wl_msg_generate_fig_error(main)

        if err_msg:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
            wl_msgs.wl_msg_fatal_error(main)

    settings = main.settings_custom['keyword_extractor']

    files_observed = list(main.wl_file_area.get_selected_files())
    files_ref = list(main.wl_file_area_ref.get_selected_files())

    if files_observed and files_ref:
        worker_keyword_extractor_fig = Wl_Worker_Keyword_Extractor_Fig(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        )
        wl_threading.Wl_Thread(worker_keyword_extractor_fig).start_worker()
    else:
        if not files_observed:
            wl_msg_box_missing_files_observed(main)
        elif not files_ref:
            wl_msg_box_missing_files_ref(main)

        wl_msgs.wl_msg_generate_fig_error(main)
