# ----------------------------------------------------------------------
# Wordless: Work Area - Keyword Extractor
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

# pylint: disable=broad-exception-caught

import collections
import copy
import traceback

import numpy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtWidgets import QLabel, QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc, wl_msg_boxes
from wordless.wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wordless.wl_measures import wl_measure_utils
from wordless.wl_nlp import wl_texts, wl_token_processing
from wordless.wl_utils import wl_misc, wl_sorting, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_layouts,
    wl_tables,
    wl_widgets
)

_tr = QCoreApplication.translate

class Wrapper_Keyword_Extractor(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.tab = 'keyword_extractor'

        # Table
        self.table_keyword_extractor = Wl_Table_Keyword_Extractor(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_keyword_extractor.label_num_results, 0, 0)
        layout_results.addWidget(self.table_keyword_extractor.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_keyword_extractor.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_exp_selected_cells, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_exp_all_cells, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_keyword_extractor.button_clr_table, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_words,
            self.checkbox_all_lowercase,
            self.checkbox_all_uppercase,
            self.checkbox_title_case,
            self.checkbox_nums,
            self.checkbox_punc_marks,

            self.checkbox_treat_as_all_lowercase,
            self.checkbox_apply_lemmatization,
            self.checkbox_filter_stop_words,

            self.checkbox_assign_pos_tags,
            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_punc_marks.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_apply_lemmatization.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.checkbox_assign_pos_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_punc_marks, 2, 1)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_all_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_apply_lemmatization, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_assign_pos_tags, 8, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 9, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 9, 1)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        (
            self.label_test_statistical_significance,
            self.combo_box_test_statistical_significance,
            self.label_measure_bayes_factor,
            self.combo_box_measure_bayes_factor,
            self.label_measure_effect_size,
            self.combo_box_measure_effect_size
        ) = wl_widgets.wl_widgets_measures_collocation_keyword_extraction(
            self,
            extraction_type = 'keyword'
        )

        self.combo_box_test_statistical_significance.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_bayes_factor.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_effect_size.currentTextChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_test_statistical_significance, 0, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_test_statistical_significance, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_bayes_factor, 2, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_bayes_factor, 3, 0)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_effect_size, 4, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_effect_size, 5, 0)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_keyword_extractor]
        )

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cum_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_file.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cum_data, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_file, 2, 0)

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
        ) = wl_widgets.wl_widgets_fig_settings(self, tab = self.tab)

        self.label_rank = QLabel(self.tr('Rank:'), self)
        (
            self.checkbox_rank_sync,
            self.label_rank_min,
            self.spin_box_rank_min,
            self.checkbox_rank_min_no_limit,
            self.label_rank_max,
            self.spin_box_rank_max,
            self.checkbox_rank_max_no_limit
        ) = wl_boxes.wl_spin_boxes_min_max_no_limit(
            self,
            val_min = 1,
            val_max = 100000
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

        self.group_box_fig_settings.layout().addWidget(self.label_rank, 4, 0, 1, 2)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_sync, 4, 2)
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
        self.checkbox_punc_marks.setChecked(settings['token_settings']['punc_marks'])

        self.checkbox_treat_as_all_lowercase.setChecked(settings['token_settings']['treat_as_all_lowercase'])
        self.checkbox_apply_lemmatization.setChecked(settings['token_settings']['apply_lemmatization'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.checkbox_assign_pos_tags.setChecked(settings['token_settings']['assign_pos_tags'])
        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Generation Settings
        self.combo_box_test_statistical_significance.set_measure(settings['generation_settings']['test_statistical_significance'])
        self.combo_box_measure_bayes_factor.set_measure(settings['generation_settings']['measure_bayes_factor'])
        self.combo_box_measure_effect_size.set_measure(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        self.checkbox_show_pct_data.setChecked(settings['table_settings']['show_pct_data'])
        self.checkbox_show_cum_data.setChecked(settings['table_settings']['show_cum_data'])
        self.checkbox_show_breakdown_file.setChecked(settings['table_settings']['show_breakdown_file'])

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
        settings['punc_marks'] = self.checkbox_punc_marks.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['apply_lemmatization'] = self.checkbox_apply_lemmatization.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['assign_pos_tags'] = self.checkbox_assign_pos_tags.isChecked()
        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['keyword_extractor']['generation_settings']

        settings['test_statistical_significance'] = self.combo_box_test_statistical_significance.get_measure()
        settings['measure_bayes_factor'] = self.combo_box_measure_bayes_factor.get_measure()
        settings['measure_effect_size'] = self.combo_box_measure_effect_size.get_measure()

        # Use data
        self.combo_box_use_data.measures_changed()

    def table_settings_changed(self):
        settings = self.main.settings_custom['keyword_extractor']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()
        settings['show_cum_data'] = self.checkbox_show_cum_data.isChecked()
        settings['show_breakdown_file'] = self.checkbox_show_breakdown_file.isChecked()

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
            enable_sorting = True
        )

        self.main.wl_file_area_ref.table_files.model().itemChanged.connect(self.file_changed)

    # Enable the buttons and prompt the user if there are only observed corpora or only reference corpora
    def file_changed(self):
        if list(self.main.wl_file_area.get_selected_files()) or list(self.main.wl_file_area_ref.get_selected_files()):
            self.button_generate_table.setEnabled(True)
            self.button_generate_fig.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)
            self.button_generate_fig.setEnabled(False)

    def wl_msg_box_missing_corpus_observed(self):
        wl_msg_boxes.Wl_Msg_Box_Warning(
            self.main,
            title = self.tr('Missing Observed Corpus'),
            text = self.tr('''
                <div>You have not specified any observed corpus yet.</div>
            ''')
        ).open()

    def wl_msg_box_missing_corpus_ref(self):
        wl_msg_boxes.Wl_Msg_Box_Warning(
            self.main,
            title = self.tr('Missing Reference Corpus'),
            text = self.tr('''
                <div>You have not specified any reference corpus yet.</div>
            ''')
        ).open()

    def wl_status_bar_msg_missing_corpus_observed(self):
        self.main.statusBar().showMessage(self.tr('Missing observed corpus!'))

    def wl_status_bar_msg_missing_corpus_ref(self):
        self.main.statusBar().showMessage(self.tr('Missing reference corpus!'))

    @wl_misc.log_time
    def generate_table(self):
        files_observed = list(self.main.wl_file_area.get_selected_files())
        files_ref = list(self.main.wl_file_area_ref.get_selected_files())

        if files_observed and files_ref:
            if self.main.settings_custom['keyword_extractor']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(
                    self.main,
                    nlp_utils = ['pos_taggers']
                )
            else:
                nlp_support_ok = True

            if nlp_support_ok:
                worker_keyword_extractor_table = Wl_Worker_Keyword_Extractor_Table(
                    self.main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                    update_gui = self.update_gui_table
                )

                wl_threading.Wl_Thread(worker_keyword_extractor_table).start_worker()
        else:
            if not files_observed:
                self.wl_msg_box_missing_corpus_observed()
                self.wl_status_bar_msg_missing_corpus_observed()
            elif not files_ref:
                self.wl_msg_box_missing_corpus_ref()
                self.wl_status_bar_msg_missing_corpus_ref()

    def update_gui_table(self, err_msg, keywords_freq_files, keywords_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, keywords_freq_files):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                settings = self.settings['keyword_extractor']
                files_observed = list(self.main.wl_file_area.get_selected_files())

                test_statistical_significance = settings['generation_settings']['test_statistical_significance']
                measure_bayes_factor = settings['generation_settings']['measure_bayes_factor']
                measure_effect_size = settings['generation_settings']['measure_effect_size']

                col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
                col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

                self.clr_table()
                self.model().setRowCount(len(keywords_freq_files))

                # Insert columns
                self.ins_header_hor(
                    self.model().columnCount() - 2,
                    self.tr('[Reference Corpora]\nFrequency'),
                    is_int = True, is_cum = True
                )
                self.ins_header_hor(
                    self.model().columnCount() - 2,
                    self.tr('[Reference Corpora]\nFrequency %'),
                    is_pct = True, is_cum = True
                )

                for file in files_observed + [{'name': self.tr('Total')}]:
                    if file['name'] == self.tr('Total'):
                        is_breakdown_file = False
                    else:
                        is_breakdown_file = True

                    self.ins_header_hor(
                        self.model().columnCount() - 2,
                        self.tr('[{}]\nFrequency').format(file['name']),
                        is_int = True, is_cum = True,
                        is_breakdown_file = is_breakdown_file
                    )
                    self.ins_header_hor(
                        self.model().columnCount() - 2,
                        self.tr('[{}]\nFrequency %').format(file['name']),
                        is_pct = True, is_cum = True,
                        is_breakdown_file = is_breakdown_file
                    )

                    if test_statistical_significance != 'none':
                        if col_text_test_stat:
                            self.ins_header_hor(
                                self.model().columnCount() - 2,
                                f"[{file['name']}]\n{col_text_test_stat}",
                                is_float = True,
                                is_breakdown_file = is_breakdown_file
                            )

                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            self.tr('[{}]\np-value').format(file['name']),
                            is_float = True,
                            is_breakdown_file = is_breakdown_file
                        )

                    if measure_bayes_factor != 'none':
                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            self.tr('[{}]\nBayes Factor').format(file['name']),
                            is_float = True,
                            is_breakdown_file = is_breakdown_file
                        )

                    if measure_effect_size != 'none':
                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            f"[{file['name']}]\n{col_text_effect_size}",
                            is_float = True,
                            is_breakdown_file = is_breakdown_file
                        )

                # Sort by p-value of the first observed corpus
                if test_statistical_significance != 'none':
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(self.tr('[{}]\np-value').format(files_observed[0]['name'])),
                        Qt.AscendingOrder
                    )
                # Sort by bayes factor of the first observed corpus
                elif measure_bayes_factor != 'none':
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(self.tr('[{}]\nBayes Factor').format(files_observed[0]['name'])),
                        Qt.DescendingOrder
                    )
                # Sort by effect size of the first observed corpus
                elif measure_effect_size != 'none':
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(f"[{files_observed[0]['name']}]\n{col_text_effect_size}"),
                        Qt.DescendingOrder
                    )
                # Otherwise sort by frequency of the first observed corpus
                else:
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(self.tr('[{}]\nFrequency').format(files_observed[0]['name'])),
                        Qt.DescendingOrder
                    )

                cols_freq = self.find_headers_hor(self.tr('\nFrequency'))
                cols_freq_pct = self.find_headers_hor(self.tr('\nFrequency %'))

                for col in cols_freq_pct:
                    cols_freq.remove(col)

                cols_test_stat = self.find_headers_hor(f'\n{col_text_test_stat}')
                cols_p_val = self.find_headers_hor(self.tr('\np-value'))
                cols_bayes_factor = self.find_headers_hor(self.tr('\nBayes Factor'))
                cols_effect_size = self.find_headers_hor(f'\n{col_text_effect_size}')
                col_files_found = self.find_header_hor(self.tr('Number of\nFiles Found'))
                col_files_found_pct = self.find_header_hor(self.tr('Number of\nFiles Found %'))

                freq_totals = numpy.array(list(keywords_freq_files.values())).sum(axis = 0)
                len_files_observed = len(files_observed)

                self.disable_updates()

                for i, (keyword, stats_files) in enumerate(wl_sorting.sorted_stats_files_items(keywords_stats_files)):
                    freq_files = keywords_freq_files[keyword]

                    # Rank
                    self.set_item_num(i, 0, -1)

                    # Keyword
                    self.model().setItem(i, 1, wl_tables.Wl_Table_Item(keyword.display_text()))
                    self.model().item(i, 1).tokens_filter = [keyword]

                    # Frequency
                    for j, freq in enumerate(freq_files):
                        self.set_item_num(i, cols_freq[j], freq)
                        self.set_item_num(i, cols_freq_pct[j], freq, freq_totals[j])

                    for j, (test_stat, p_val, bayes_factor, effect_size) in enumerate(stats_files):
                        # Test Statistic
                        if test_stat is not None:
                            self.set_item_num(i, cols_test_stat[j], test_stat)

                        # p-value
                        if p_val is not None:
                            self.set_item_p_val(i, cols_p_val[j], p_val)

                        # Bayes Factor
                        if bayes_factor is not None:
                            self.set_item_num(i, cols_bayes_factor[j], bayes_factor)

                        # Effect Size
                        if effect_size is not None:
                            self.set_item_num(i, cols_effect_size[j], effect_size)

                    # Number of Files Found
                    num_files_found = len([freq for freq in freq_files[1:-1] if freq])

                    self.set_item_num(i, col_files_found, num_files_found)
                    self.set_item_num(i, col_files_found_pct, num_files_found, len_files_observed)

                self.enable_updates()

                self.toggle_pct_data()
                self.toggle_cum_data()
                self.toggle_breakdown_file()
                self.update_ranks()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

    @wl_misc.log_time
    def generate_fig(self):
        files_observed = list(self.main.wl_file_area.get_selected_files())
        files_ref = list(self.main.wl_file_area_ref.get_selected_files())

        if files_observed and files_ref:
            if self.main.settings_custom['keyword_extractor']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(
                    self.main,
                    nlp_utils = ['pos_taggers']
                )
            else:
                nlp_support_ok = True

            if nlp_support_ok:
                self.worker_keyword_extractor_fig = Wl_Worker_Keyword_Extractor_Fig(
                    self.main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                    update_gui = self.update_gui_fig
                )

                wl_threading.Wl_Thread(self.worker_keyword_extractor_fig).start_worker()
        else:
            if not files_observed:
                self.wl_msg_box_missing_corpus_observed()
                self.wl_status_bar_msg_missing_corpus_observed()
            elif not files_ref:
                self.wl_msg_box_missing_corpus_ref()
                self.wl_status_bar_msg_missing_corpus_ref()

    def update_gui_fig(self, err_msg, keywords_freq_files, keywords_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, keywords_freq_files):
            try:
                settings = self.main.settings_custom['keyword_extractor']

                test_statistical_significance = settings['generation_settings']['test_statistical_significance']
                measure_effect_size = settings['generation_settings']['measure_effect_size']

                col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
                col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

                if settings['fig_settings']['use_data'] == self.tr('Frequency'):
                    wl_figs_freqs.wl_fig_freqs(
                        self.main, keywords_freq_files,
                        tab = 'keyword_extractor'
                    )
                else:
                    if settings['fig_settings']['use_data'] == col_text_test_stat:
                        keywords_stat_files = {
                            keyword: numpy.array(stats_files)[:, 0]
                            for keyword, stats_files in keywords_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == self.tr('p-value'):
                        keywords_stat_files = {
                            keyword: numpy.array(stats_files)[:, 1]
                            for keyword, stats_files in keywords_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == self.tr('Bayes factor'):
                        keywords_stat_files = {
                            keyword: numpy.array(stats_files)[:, 2]
                            for keyword, stats_files in keywords_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == col_text_effect_size:
                        keywords_stat_files = {
                            keyword: numpy.array(stats_files)[:, 3]
                            for keyword, stats_files in keywords_stats_files.items()
                        }

                    wl_figs_stats.wl_fig_stats(
                        self.main, keywords_stat_files,
                        tab = 'keyword_extractor'
                    )

                # Hide the progress dialog early so that the main window will not obscure the generated figure
                self.worker_keyword_extractor_fig.dialog_progress.accept()
                wl_figs.show_fig()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_fig(self.main, err_msg)

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

            # Frequency (Reference Corpora)
            self.keywords_freq_files.append(collections.Counter())
            tokens_ref = []

            for file_ref in files_ref:
                text = wl_token_processing.wl_process_tokens_ngram_generator(
                    self.main, file_ref['text'],
                    token_settings = settings['token_settings']
                )

                tokens = text.get_tokens_flat()

                # Remove empty tokens
                self.keywords_freq_files[0] += collections.Counter([token for token in tokens if token])

                # Preserve empty tokens for tests of statistical significance and measures of Bayes factor which require that the corpus be segmented into equal-sized sections
                tokens_ref.extend(tokens)

            len_tokens_ref = len(tokens_ref)

            # Frequency (Observed Corpus)
            for file_observed in files_observed:
                text = wl_token_processing.wl_process_tokens_ngram_generator(
                    self.main, file_observed['text'],
                    token_settings = settings['token_settings']
                )

                tokens = text.get_tokens_flat()

                # Remove empty tokens
                self.keywords_freq_files.append(collections.Counter([token for token in tokens if token]))

                # Preserve empty tokens for tests of statistical significance and measures of Bayes factor which require that the corpus be segmented into equal-sized sections
                texts.append(text)

            # Total
            if len(files_observed) > 1:
                texts.append(wl_texts.Wl_Text_Total(texts))

                self.keywords_freq_files.append(sum(self.keywords_freq_files[1:], collections.Counter()))

            # Remove tokens that do not appear in any observed corpus
            self.keywords_freq_files[0] = {
                token: freq
                for token, freq in self.keywords_freq_files[0].items()
                if token in self.keywords_freq_files[-1].keys()
            }

            # Keyness
            test_statistical_significance = settings['generation_settings']['test_statistical_significance']
            measure_bayes_factor = settings['generation_settings']['measure_bayes_factor']
            measure_effect_size = settings['generation_settings']['measure_effect_size']

            func_statistical_significance = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['func']
            func_bayes_factor = self.main.settings_global['measures_bayes_factor'][measure_bayes_factor]['func']
            func_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['func']

            to_sections_statistical_significance = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['to_sections']
            to_sections_bayes_factor = self.main.settings_global['measures_bayes_factor'][measure_bayes_factor]['to_sections']

            keywords_freq_file_ref = self.keywords_freq_files[0]
            keywords_all = self.keywords_freq_files[-1].keys()
            num_keywords_all = len(keywords_all)

            for i, text in enumerate(texts):
                if any((func_statistical_significance, func_bayes_factor, func_effect_size)):
                    keywords_stats_file = {}

                    keywords_freq_file_observed = self.keywords_freq_files[i + 1]
                    tokens_observed = text.get_tokens_flat()

                    if to_sections_statistical_significance:
                        freqs_sections_tokens_statistical_significance = wl_measure_utils.to_freqs_sections_statistical_significance(
                            self.main,
                            items_to_search = keywords_all,
                            items_x1 = tokens_observed,
                            items_x2 = tokens_ref,
                            test_statistical_significance = test_statistical_significance
                        )

                    if to_sections_bayes_factor:
                        freqs_sections_tokens_bayes_factor = wl_measure_utils.to_freqs_sections_bayes_factor(
                            self.main,
                            items_to_search = keywords_all,
                            items_x1 = tokens_observed,
                            items_x2 = tokens_ref,
                            measure_bayes_factor = measure_bayes_factor
                        )

                    o11s = numpy.empty(shape = num_keywords_all, dtype = float)
                    o12s = numpy.empty(shape = num_keywords_all, dtype = float)
                    o21s = numpy.empty(shape = num_keywords_all, dtype = float)
                    o22s = numpy.empty(shape = num_keywords_all, dtype = float)

                    len_tokens_observed = text.num_tokens

                    for i, token in enumerate(keywords_all):
                        o11s[i] = keywords_freq_file_observed.get(token, 0)
                        o12s[i] = keywords_freq_file_ref.get(token, 0)
                        o21s[i] = len_tokens_observed - o11s[i]
                        o22s[i] = len_tokens_ref - o12s[i]

                    if to_sections_statistical_significance:
                        freqs_x1s_statistical_significance = []
                        freqs_x2s_statistical_significance = []

                        for token in keywords_all:
                            freqs_x1, freqs_x2 = freqs_sections_tokens_statistical_significance[token]

                            freqs_x1s_statistical_significance.append(freqs_x1)
                            freqs_x2s_statistical_significance.append(freqs_x2)

                        freqs_x1s_statistical_significance = numpy.array(freqs_x1s_statistical_significance, dtype = float)
                        freqs_x2s_statistical_significance = numpy.array(freqs_x2s_statistical_significance, dtype = float)

                    if to_sections_bayes_factor:
                        freqs_x1s_bayes_factor = []
                        freqs_x2s_bayes_factor = []

                        for token in keywords_all:
                            freqs_x1, freqs_x2 = freqs_sections_tokens_bayes_factor[token]

                            freqs_x1s_bayes_factor.append(freqs_x1)
                            freqs_x2s_bayes_factor.append(freqs_x2)

                        freqs_x1s_bayes_factor = numpy.array(freqs_x1s_bayes_factor, dtype = float)
                        freqs_x2s_bayes_factor = numpy.array(freqs_x2s_bayes_factor, dtype = float)

                    # Test Statistic & p-value
                    if test_statistical_significance == 'none':
                        test_stats = [None] * num_keywords_all
                        p_vals = [None] * num_keywords_all
                    else:
                        if to_sections_statistical_significance:
                            test_stats, p_vals = func_statistical_significance(self.main, freqs_x1s_statistical_significance, freqs_x2s_statistical_significance)
                        else:
                            test_stats, p_vals = func_statistical_significance(self.main, o11s, o12s, o21s, o22s)

                    # Bayes Factor
                    if measure_bayes_factor == 'none':
                        bayes_factors = [None] * num_keywords_all
                    else:
                        if to_sections_bayes_factor:
                            bayes_factors = func_bayes_factor(self.main, freqs_x1s_bayes_factor, freqs_x2s_bayes_factor)
                        else:
                            bayes_factors = func_bayes_factor(self.main, o11s, o12s, o21s, o22s)

                    # Effect Size
                    if measure_effect_size == 'none':
                        effect_sizes = [None] * num_keywords_all
                    else:
                        effect_sizes = func_effect_size(self.main, o11s, o12s, o21s, o22s)

                    for i, token in enumerate(keywords_all):
                        keywords_stats_file[token] = [
                            test_stats[i],
                            p_vals[i],
                            bayes_factors[i],
                            effect_sizes[i]
                        ]
                else:
                    keywords_stats_file = {
                        token: [None] * 4
                        for token in keywords_all
                    }

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
