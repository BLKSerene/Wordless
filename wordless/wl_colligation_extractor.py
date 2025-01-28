# ----------------------------------------------------------------------
# Wordless: Work Area - Colligation Extractor
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

import bisect
import collections
import copy
import operator
import re
import traceback

import numpy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtWidgets import QLabel, QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wordless.wl_nlp import (
    wl_matching,
    wl_nlp_utils,
    wl_texts,
    wl_token_processing
)
from wordless.wl_utils import wl_misc, wl_sorting, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_layouts,
    wl_tables,
    wl_widgets
)

_tr = QCoreApplication.translate

class Wrapper_Colligation_Extractor(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.tab = 'colligation_extractor'

        # Table
        self.table_colligation_extractor = Wl_Table_Colligation_Extractor(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_colligation_extractor.label_num_results, 0, 0)
        layout_results.addWidget(self.table_colligation_extractor.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_colligation_extractor.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_colligation_extractor, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_colligation_extractor.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_colligation_extractor.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_colligation_extractor.button_exp_selected_cells, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_colligation_extractor.button_exp_all_cells, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_colligation_extractor.button_clr_table, 2, 4)

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

        self.checkbox_assign_pos_tags.hide()

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_punc_marks.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_apply_lemmatization.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

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

        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 8, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 8, 1)

        # Search Settings
        self.group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

        (
            self.label_search_term,
            self.checkbox_multi_search_mode,

            self.stacked_widget_search_term,
            self.line_edit_search_term,
            self.list_search_terms,
            self.label_delimiter,

            self.checkbox_match_case,
            self.checkbox_match_whole_words,
            self.checkbox_match_inflected_forms,
            self.checkbox_use_regex,
            self.checkbox_match_without_tags,
            self.checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(self, tab = self.tab)

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(self, tab = self.tab)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_colligation_extractor.button_generate_table.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_match_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.checkbox_match_without_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        layout_context_settings = wl_layouts.Wl_Layout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_delimiter, 2, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_match_case, 3, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_words, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_without_tags, 7, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 10, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        self.label_window = QLabel(self.tr('Collocational window:'), self)
        (
            self.checkbox_window_sync,
            self.label_window_left,
            self.spin_box_window_left,
            self.label_window_right,
            self.spin_box_window_right
        ) = wl_boxes.wl_spin_boxes_min_max_sync_window(self)

        self.label_limit_searching = QLabel(self.tr('Limit searching:'), self)
        self.combo_box_limit_searching = wl_boxes.Wl_Combo_Box(self)

        (
            self.label_test_statistical_significance,
            self.combo_box_test_statistical_significance,
            self.label_measure_bayes_factor,
            self.combo_box_measure_bayes_factor,
            self.label_measure_effect_size,
            self.combo_box_measure_effect_size
        ) = wl_widgets.wl_widgets_measures_collocation_keyword_extraction(
            self,
            extraction_type = 'collocation'
        )

        self.combo_box_limit_searching.addItems([
            self.tr('None'),
            self.tr('Within sentence segments'),
            self.tr('Within sentences'),
            self.tr('Within paragraphs')
        ])

        self.checkbox_window_sync.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_window_left.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_window_right.valueChanged.connect(self.generation_settings_changed)

        self.combo_box_limit_searching.currentTextChanged.connect(self.generation_settings_changed)

        self.combo_box_test_statistical_significance.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_bayes_factor.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_effect_size.currentTextChanged.connect(self.generation_settings_changed)

        layout_settings_limit_searching = wl_layouts.Wl_Layout()
        layout_settings_limit_searching.addWidget(self.label_limit_searching, 0, 0)
        layout_settings_limit_searching.addWidget(self.combo_box_limit_searching, 0, 1)

        layout_settings_limit_searching.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_window, 0, 0, 1, 3)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_window_sync, 0, 3, Qt.AlignRight)
        self.group_box_generation_settings.layout().addWidget(self.label_window_left, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_window_left, 1, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_window_right, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_window_right, 1, 3)
        self.group_box_generation_settings.layout().addLayout(layout_settings_limit_searching, 2, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(self.label_test_statistical_significance, 4, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_test_statistical_significance, 5, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_bayes_factor, 6, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_bayes_factor, 7, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_effect_size, 8, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_effect_size, 9, 0, 1, 4)

        self.group_box_generation_settings.layout().setColumnStretch(1, 1)
        self.group_box_generation_settings.layout().setColumnStretch(3, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_span_position,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings_span_position(
            self,
            tables = [self.table_colligation_extractor]
        )

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cum_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_span_position.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_file.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cum_data, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_span_position, 2, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_file, 3, 0)

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
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 4, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['colligation_extractor'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['colligation_extractor'])

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

        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_settings']['search_term'])
            self.list_search_terms.load_items(settings['search_settings']['search_terms'])

        self.checkbox_match_case.setChecked(settings['search_settings']['match_case'])
        self.checkbox_match_whole_words.setChecked(settings['search_settings']['match_whole_words'])
        self.checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        self.checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])
        self.checkbox_match_without_tags.setChecked(settings['search_settings']['match_without_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        # Context Settings
        if defaults:
            self.main.wl_context_settings_colligation_extractor.load_settings(defaults = True)

        # Generation Settings
        self.checkbox_window_sync.setChecked(settings['generation_settings']['window_sync'])

        if settings['generation_settings']['window_left'] < 0:
            self.spin_box_window_left.setPrefix(self.tr('L'))
            self.spin_box_window_left.setValue(-settings['generation_settings']['window_left'])
        else:
            self.spin_box_window_left.setPrefix(self.tr('R'))
            self.spin_box_window_left.setValue(settings['generation_settings']['window_left'])

        if settings['generation_settings']['window_right'] < 0:
            self.spin_box_window_right.setPrefix(self.tr('L'))
            self.spin_box_window_right.setValue(-settings['generation_settings']['window_right'])
        else:
            self.spin_box_window_right.setPrefix(self.tr('R'))
            self.spin_box_window_right.setValue(settings['generation_settings']['window_right'])

        self.combo_box_limit_searching.setCurrentText(settings['generation_settings']['limit_searching'])

        self.combo_box_test_statistical_significance.set_measure(settings['generation_settings']['test_statistical_significance'])
        self.combo_box_measure_bayes_factor.set_measure(settings['generation_settings']['measure_bayes_factor'])
        self.combo_box_measure_effect_size.set_measure(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        self.checkbox_show_pct_data.setChecked(settings['table_settings']['show_pct_data'])
        self.checkbox_show_cum_data.setChecked(settings['table_settings']['show_cum_data'])
        self.checkbox_show_breakdown_span_position.setChecked(settings['table_settings']['show_breakdown_span_position'])
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
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['colligation_extractor']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['all_lowercase'] = self.checkbox_all_lowercase.isChecked()
        settings['all_uppercase'] = self.checkbox_all_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['punc_marks'] = self.checkbox_punc_marks.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['apply_lemmatization'] = self.checkbox_apply_lemmatization.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        self.checkbox_match_tags.token_settings_changed()
        self.main.wl_context_settings_colligation_extractor.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['colligation_extractor']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.model().stringList()

        settings['match_case'] = self.checkbox_match_case.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()
        settings['match_without_tags'] = self.checkbox_match_without_tags.isChecked()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['colligation_extractor']['generation_settings']

        settings['window_sync'] = self.checkbox_window_sync.isChecked()

        if self.spin_box_window_left.prefix() == self.tr('L'):
            settings['window_left'] = - self.spin_box_window_left.value()
        else:
            settings['window_left'] = self.spin_box_window_left.value()

        if self.spin_box_window_right.prefix() == self.tr('L'):
            settings['window_right'] = - self.spin_box_window_right.value()
        else:
            settings['window_right'] = self.spin_box_window_right.value()

        settings['limit_searching'] = self.combo_box_limit_searching.currentText()

        settings['test_statistical_significance'] = self.combo_box_test_statistical_significance.get_measure()
        settings['measure_bayes_factor'] = self.combo_box_measure_bayes_factor.get_measure()
        settings['measure_effect_size'] = self.combo_box_measure_effect_size.get_measure()

        # Use data
        self.combo_box_use_data.measures_changed()

    def table_settings_changed(self):
        settings = self.main.settings_custom['colligation_extractor']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()
        settings['show_cum_data'] = self.checkbox_show_cum_data.isChecked()
        settings['show_breakdown_span_position'] = self.checkbox_show_breakdown_span_position.isChecked()
        settings['show_breakdown_file'] = self.checkbox_show_breakdown_file.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['colligation_extractor']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['sort_by_file'] = self.combo_box_sort_by_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

class Wl_Table_Colligation_Extractor(wl_tables.Wl_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'colligation_extractor',
            headers = [
                _tr('Wl_Table_Colligation_Extractor', 'Rank'),
                _tr('Wl_Table_Colligation_Extractor', 'Node'),
                _tr('Wl_Table_Colligation_Extractor', 'Collocate'),
                _tr('Wl_Table_Colligation_Extractor', 'Number of\nFiles Found'),
                _tr('Wl_Table_Colligation_Extractor', 'Number of\nFiles Found %')
            ],
            headers_int = [
                _tr('Wl_Table_Colligation_Extractor', 'Rank'),
                _tr('Wl_Table_Colligation_Extractor', 'Number of\nFiles Found')
            ],
            headers_pct = [
                _tr('Wl_Table_Colligation_Extractor', 'Number of\nFiles Found %')
            ],
            enable_sorting = True
        )

        self.wrapper = parent

    @wl_misc.log_time
    def generate_table(self):
        if (
            wl_checks_work_area.check_search_terms(
                self.main,
                search_settings = self.main.settings_custom['colligation_extractor']['search_settings']
            ) and wl_checks_work_area.check_nlp_support(
                self.main,
                nlp_utils = ['pos_taggers']
            )
        ):
            worker_colligation_extractor_table = Wl_Worker_Colligation_Extractor_Table(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                update_gui = self.update_gui_table
            )

            wl_threading.Wl_Thread(worker_colligation_extractor_table).start_worker()

    def update_gui_table(self, err_msg, colligations_freqs_files, colligations_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, colligations_freqs_files):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                settings = self.settings['colligation_extractor']

                test_statistical_significance = settings['generation_settings']['test_statistical_significance']
                measure_bayes_factor = settings['generation_settings']['measure_bayes_factor']
                measure_effect_size = settings['generation_settings']['measure_effect_size']

                col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
                col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

                self.clr_table()
                self.model().setRowCount(len(colligations_freqs_files))

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())
                files_with_total = files + [{'name': self.tr('Total')}]

                for file in files_with_total:
                    if file['name'] == self.tr('Total'):
                        is_breakdown_file = False
                    else:
                        is_breakdown_file = True

                    for i in range(
                        settings['generation_settings']['window_left'],
                        settings['generation_settings']['window_right'] + 1
                    ):
                        if i < 0:
                            self.ins_header_hor(
                                self.model().columnCount() - 2,
                                self.tr('[{}]\nL{}').format(file['name'], -i),
                                is_int = True, is_cum = True,
                                is_breakdown_file = is_breakdown_file, is_breakdown_span_position = True
                            )
                            self.ins_header_hor(
                                self.model().columnCount() - 2,
                                self.tr('[{}]\nL{} %').format(file['name'], -i),
                                is_pct = True, is_cum = True,
                                is_breakdown_file = is_breakdown_file, is_breakdown_span_position = True
                            )
                        elif i > 0:
                            self.ins_header_hor(
                                self.model().columnCount() - 2,
                                self.tr('[{}]\nR{}').format(file['name'], i),
                                is_int = True, is_cum = True,
                                is_breakdown_file = is_breakdown_file, is_breakdown_span_position = True
                            )
                            self.ins_header_hor(
                                self.model().columnCount() - 2,
                                self.tr('[{}]\nR{} %').format(file['name'], i),
                                is_pct = True, is_cum = True,
                                is_breakdown_file = is_breakdown_file, is_breakdown_span_position = True
                            )

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
                                f'[{file["name"]}]\n{col_text_test_stat}',
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
                            f'[{file["name"]}]\n{col_text_effect_size}',
                            is_float = True,
                            is_breakdown_file = is_breakdown_file
                        )

                # Sort by p-value of the first file
                if test_statistical_significance != 'none':
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(self.tr('[{}]\np-value').format(files[0]['name'])),
                        Qt.AscendingOrder
                    )
                # Sort by bayes factor of the first file
                elif measure_bayes_factor != 'none':
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(self.tr('[{}]\nBayes Factor').format(files[0]['name'])),
                        Qt.DescendingOrder
                    )
                # Sort by effect size of the first file
                elif measure_effect_size != 'none':
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(f"[{files[0]['name']}]\n{col_text_effect_size}"),
                        Qt.DescendingOrder
                    )
                # Otherwise sort by frequency of the first file
                else:
                    self.horizontalHeader().setSortIndicator(
                        self.find_header_hor(self.tr('[{}]\nFrequency').format(files[0]['name'])),
                        Qt.DescendingOrder
                    )

                if settings['generation_settings']['window_left'] < 0:
                    cols_freqs_start = [
                        self.find_header_hor(self.tr('[{}]\nL{}').format(file['name'], -settings['generation_settings']['window_left']))
                        for file in files_with_total
                    ]
                else:
                    cols_freqs_start = [
                        self.find_header_hor(self.tr('[{}]\nR{}').format(file['name'], settings['generation_settings']['window_left']))
                        for file in files_with_total
                    ]

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

                freqs_totals = numpy.array(list(colligations_freqs_files.values())).sum(axis = 0)
                freq_totals = numpy.array(list(colligations_freqs_files.values())).sum(axis = 2).sum(axis = 0)
                len_files = len(files)

                self.disable_updates()

                for i, ((node, collocate), stats_files) in enumerate(wl_sorting.sorted_stats_files_items(colligations_stats_files)):
                    freqs_files = colligations_freqs_files[(node, collocate)]

                    # Rank
                    self.set_item_num(i, 0, -1)

                    # Node
                    self.model().setItem(i, 1, wl_tables.Wl_Table_Item(' '.join(wl_texts.to_display_texts(node))))
                    self.model().item(i, 1).tokens_filter = node

                    # Collocate
                    self.model().setItem(i, 2, wl_tables.Wl_Table_Item(collocate.display_text()))
                    self.model().item(i, 2).tokens_filter = [collocate]

                    # Frequency
                    for j, freqs_file in enumerate(freqs_files):
                        for k, freq in enumerate(freqs_file):
                            self.set_item_num(i, cols_freqs_start[j] + k * 2, freq)

                            if freqs_totals[j][k]:
                                self.set_item_num(i, cols_freqs_start[j] + k * 2 + 1, freq / freqs_totals[j][k])
                            else:
                                self.set_item_num(i, cols_freqs_start[j] + k * 2 + 1, 0)

                        self.set_item_num(i, cols_freq[j], sum(freqs_file))

                        if freq_totals[j]:
                            self.set_item_num(i, cols_freq_pct[j], sum(freqs_file) / freq_totals[j])
                        else:
                            self.set_item_num(i, cols_freq_pct[j], 0)

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
                    num_files_found = len([freqs_file for freqs_file in freqs_files[:-1] if sum(freqs_file)])

                    self.set_item_num(i, col_files_found, num_files_found)
                    self.set_item_num(i, col_files_found_pct, num_files_found / len_files)

                self.enable_updates()

                self.toggle_pct_data_span_position()
                self.toggle_cum_data()
                self.toggle_breakdown_span_position()
                self.toggle_breakdown_file_span_position()
                self.update_ranks()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

    @wl_misc.log_time
    def generate_fig(self):
        if (
            wl_checks_work_area.check_search_terms(
                self.main,
                search_settings = self.main.settings_custom['colligation_extractor']['search_settings']
            ) and wl_checks_work_area.check_nlp_support(
                self.main,
                nlp_utils = ['pos_taggers']
            )
        ):
            self.worker_colligation_extractor_fig = Wl_Worker_Colligation_Extractor_Fig(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                update_gui = self.update_gui_fig
            )

            wl_threading.Wl_Thread(self.worker_colligation_extractor_fig).start_worker()

    def update_gui_fig(self, err_msg, colligations_freqs_file, colligations_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, colligations_freqs_file):
            try:
                settings = self.main.settings_custom['colligation_extractor']

                test_statistical_significance = settings['generation_settings']['test_statistical_significance']
                measure_effect_size = settings['generation_settings']['measure_effect_size']

                col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
                col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

                if re.search(self.tr(r'^[LR][0-9]+$'), settings['fig_settings']['use_data']):
                    span_positions = (
                        list(range(settings['generation_settings']['window_left'], 0))
                        + list(range(1, settings['generation_settings']['window_right'] + 1))
                    )

                    if self.tr('L') in settings['fig_settings']['use_data']:
                        span_position = span_positions.index(-int(settings['fig_settings']['use_data'][1:]))
                    else:
                        span_position = span_positions.index(int(settings['fig_settings']['use_data'][1:]))

                    collocates_freq_files = {
                        colligation: numpy.array(freqs)[:, span_position]
                        for colligation, freqs in colligations_freqs_file.items()
                    }

                    wl_figs_freqs.wl_fig_freqs(
                        self.main, collocates_freq_files,
                        tab = 'colligation_extractor'
                    )
                elif settings['fig_settings']['use_data'] == self.tr('Frequency'):
                    collocates_freq_files = {
                        colligation: numpy.array(freqs).sum(axis = 1)
                        for colligation, freqs in colligations_freqs_file.items()
                    }

                    wl_figs_freqs.wl_fig_freqs(
                        self.main, collocates_freq_files,
                        tab = 'colligation_extractor'
                    )
                else:
                    if settings['fig_settings']['use_data'] == col_text_test_stat:
                        collocates_stat_files = {
                            colligation: numpy.array(stats_files)[:, 0]
                            for colligation, stats_files in colligations_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == self.tr('p-value'):
                        collocates_stat_files = {
                            colligation: numpy.array(stats_files)[:, 1]
                            for colligation, stats_files in colligations_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == self.tr('Bayes factor'):
                        collocates_stat_files = {
                            colligation: numpy.array(stats_files)[:, 2]
                            for colligation, stats_files in colligations_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == col_text_effect_size:
                        collocates_stat_files = {
                            colligation: numpy.array(stats_files)[:, 3]
                            for colligation, stats_files in colligations_stats_files.items()
                        }

                    wl_figs_stats.wl_fig_stats(
                        self.main, collocates_stat_files,
                        tab = 'colligation_extractor'
                    )

                # Hide the progress dialog early so that the main window will not obscure the generated figure
                self.worker_colligation_extractor_fig.dialog_progress.accept()
                wl_figs.show_fig()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_fig(self.main, err_msg)

# self.tr() does not work in inherited classes
class Wl_Worker_Colligation_Extractor(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, dict, dict)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.colligations_freqs_files = []
        self.colligations_stats_files = []

    def run(self):
        try:
            colligations_freqs_files_all = []

            settings = self.main.settings_custom['colligation_extractor']
            files = list(self.main.wl_file_area.get_selected_files())

            window_left = settings['generation_settings']['window_left']
            window_right = settings['generation_settings']['window_right']

            # Calculate window size
            if window_left < 0 < window_right:
                window_size = window_right - window_left
            else:
                window_size = window_right - window_left + 1

            # Frequency
            for i, file in enumerate(files):
                colligations_freqs_file = {}
                colligations_freqs_file_all = {}

                text = wl_token_processing.wl_process_tokens_colligation_extractor(
                    self.main, file['text'],
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                tokens = text.get_tokens_flat()
                (
                    offsets_paras,
                    offsets_sentences,
                    offsets_sentence_segs
                ) = text.get_offsets()

                search_terms = wl_matching.match_search_terms_ngrams(
                    self.main, tokens,
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                (
                    search_terms_incl,
                    search_terms_excl
                ) = wl_matching.match_search_terms_context(
                    self.main, tokens,
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    context_settings = settings['search_settings']['context_settings']
                )

                if search_terms:
                    len_search_term_min = min((len(search_term) for search_term in search_terms))
                    len_search_term_max = max((len(search_term) for search_term in search_terms))
                else:
                    len_search_term_min = 1
                    len_search_term_max = 1

                len_paras = len(offsets_paras)
                len_sentences = len(offsets_sentences)
                len_sentence_segs = len(offsets_sentence_segs)

                settings_limit_searching = settings['generation_settings']['limit_searching']

                for ngram_size in range(len_search_term_min, len_search_term_max + 1):
                    colligations_freqs_file_all[ngram_size] = collections.Counter()

                    for i, ngram in enumerate(wl_nlp_utils.ngrams(tokens, ngram_size)):
                        # Limit Searching
                        if settings_limit_searching != _tr('Wl_Worker_Colligation_Extractor', 'None'):
                            if settings_limit_searching == _tr('Wl_Worker_Colligation_Extractor', 'Within sentence segments'):
                                offsets_unit = offsets_sentence_segs
                                len_unit = len_sentence_segs
                            elif settings_limit_searching == _tr('Wl_Worker_Colligation_Extractor', 'Within sentences'):
                                offsets_unit = offsets_sentences
                                len_unit = len_sentences
                            elif settings_limit_searching == _tr('Wl_Worker_Colligation_Extractor', 'Within paragraphs'):
                                offsets_unit = offsets_paras
                                len_unit = len_paras

                            i_unit = bisect.bisect(offsets_unit, i) - 1

                            i_unit_start = offsets_unit[i_unit]
                            i_unit_end = offsets_unit[i_unit + 1] - 1 if i_unit < len_unit - 1 else text.num_tokens - 1

                        # Extract collocates
                        tags_left = []
                        tags_right = []

                        if window_left < 0 < window_right:
                            # Limit Searching
                            if settings_limit_searching == _tr('Wl_Worker_Colligation_Extractor', 'None'):
                                tags_left = text.tags[max(0, i + window_left) : i]
                                tags_right = text.tags[i + ngram_size : i + ngram_size + window_right]
                            else:
                                # Span positions (Left)
                                for position in range(max(0, i + window_left), i):
                                    if i_unit_start <= position <= i_unit_end:
                                        tags_left.append(text.tags[position])

                                # Span positions (Right)
                                for position in range(i + ngram_size, i + ngram_size + window_right):
                                    if i_unit_start <= position <= i_unit_end:
                                        tags_right.append(text.tags[position])

                            for j, collocate in enumerate(reversed(tags_left)):
                                if wl_matching.check_context(
                                    i, tokens,
                                    context_settings = settings['search_settings']['context_settings'],
                                    search_terms_incl = search_terms_incl,
                                    search_terms_excl = search_terms_excl
                                ):
                                    if (ngram, collocate) not in colligations_freqs_file:
                                        colligations_freqs_file[(ngram, collocate)] = [0] * window_size

                                    colligations_freqs_file[(ngram, collocate)][abs(window_left) - 1 - j] += 1

                                colligations_freqs_file_all[ngram_size][(ngram, collocate)] += 1

                            for j, collocate in enumerate(tags_right):
                                if wl_matching.check_context(
                                    i, tokens,
                                    context_settings = settings['search_settings']['context_settings'],
                                    search_terms_incl = search_terms_incl,
                                    search_terms_excl = search_terms_excl
                                ):
                                    if (ngram, collocate) not in colligations_freqs_file:
                                        colligations_freqs_file[(ngram, collocate)] = [0] * window_size

                                    colligations_freqs_file[(ngram, collocate)][abs(window_left) + j] += 1

                                colligations_freqs_file_all[ngram_size][(ngram, collocate)] += 1
                        elif window_left < 0 and window_right < 0:
                            # Limit Searching
                            if settings_limit_searching == _tr('Wl_Worker_Colligation_Extractor', 'None'):
                                tags_left = text.tags[max(0, i + window_left) : max(0, i + window_right + 1)]
                            else:
                                # Span positions (Left)
                                for position in range(max(0, i + window_left), max(0, i + window_right + 1)):
                                    if i_unit_start <= position <= i_unit_end:
                                        tags_left.append(text.tags[position])

                            for j, collocate in enumerate(reversed(tags_left)):
                                if wl_matching.check_context(
                                    i, tokens,
                                    context_settings = settings['search_settings']['context_settings'],
                                    search_terms_incl = search_terms_incl,
                                    search_terms_excl = search_terms_excl
                                ):
                                    if (ngram, collocate) not in colligations_freqs_file:
                                        colligations_freqs_file[(ngram, collocate)] = [0] * window_size

                                    colligations_freqs_file[(ngram, collocate)][window_size - 1 - j] += 1

                                colligations_freqs_file_all[ngram_size][(ngram, collocate)] += 1
                        elif window_left > 0 and window_right > 0:
                            # Limit Searching
                            if settings_limit_searching == _tr('Wl_Worker_Colligation_Extractor', 'None'):
                                tags_right = text.tags[i + ngram_size + window_left - 1 : i + ngram_size + window_right]
                            else:
                                # Span positions (Right)
                                for position in range(i + ngram_size + window_left - 1, i + ngram_size + window_right):
                                    if i_unit_start <= position <= i_unit_end:
                                        tags_right.append(text.tags[position])

                            for j, collocate in enumerate(tags_right):
                                if wl_matching.check_context(
                                    i, tokens,
                                    context_settings = settings['search_settings']['context_settings'],
                                    search_terms_incl = search_terms_incl,
                                    search_terms_excl = search_terms_excl
                                ):
                                    if (ngram, collocate) not in colligations_freqs_file:
                                        colligations_freqs_file[(ngram, collocate)] = [0] * window_size

                                    colligations_freqs_file[(ngram, collocate)][j] += 1

                                colligations_freqs_file_all[ngram_size][(ngram, collocate)] += 1

                colligations_freqs_file = {
                    (ngram, collocate): freqs
                    for (ngram, collocate), freqs in colligations_freqs_file.items()
                    if all(ngram) and collocate
                }

                # Filter search terms
                colligations_freqs_file_filtered = {}

                for search_term in search_terms:
                    len_search_term = len(search_term)

                    for (node, collocate), freqs in colligations_freqs_file.items():
                        for ngram in wl_nlp_utils.ngrams(node, len_search_term):
                            if ngram == search_term:
                                colligations_freqs_file_filtered[(node, collocate)] = freqs

                self.colligations_freqs_files.append(colligations_freqs_file_filtered)

                # Frequency (All)
                colligations_freqs_files_all.append(colligations_freqs_file_all)

            # Total
            if len(files) > 1:
                colligations_freqs_total = {}
                colligations_freqs_total_all = {}

                # Frequency
                for colligations_freqs_file in self.colligations_freqs_files:
                    for colligation, freqs in colligations_freqs_file.items():
                        if colligation not in colligations_freqs_total:
                            colligations_freqs_total[colligation] = freqs
                        else:
                            colligations_freqs_total[colligation] = list(map(operator.add, colligations_freqs_total[colligation], freqs))

                # Frequency (All)
                for colligations_freqs_file_all in colligations_freqs_files_all:
                    for ngram_size, colligations_freqs in colligations_freqs_file_all.items():
                        if ngram_size not in colligations_freqs_total_all:
                            colligations_freqs_total_all[ngram_size] = collections.Counter()

                        colligations_freqs_total_all[ngram_size] += colligations_freqs

                self.colligations_freqs_files.append(colligations_freqs_total)
                colligations_freqs_files_all.append(colligations_freqs_total_all)

            test_statistical_significance = settings['generation_settings']['test_statistical_significance']
            measure_bayes_factor = settings['generation_settings']['measure_bayes_factor']
            measure_effect_size = settings['generation_settings']['measure_effect_size']

            func_statistical_significance = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['func']
            func_bayes_factor = self.main.settings_global['measures_bayes_factor'][measure_bayes_factor]['func']
            func_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['func']

            colligations_all = self.colligations_freqs_files[-1].keys()
            num_colligations_all = len(colligations_all)
            # Used for z-score (Berry-Rogghe)
            span = (abs(window_left) + abs(window_right)) / 2

            for colligations_freqs_file, colligations_freqs_file_all in zip(
                self.colligations_freqs_files,
                colligations_freqs_files_all
            ):
                if any((func_statistical_significance, func_bayes_factor, func_effect_size)):
                    colligations_stats_file = {}
                    o1xs = collections.Counter()
                    ox1s = collections.Counter()
                    oxxs = {}

                    # Total frequencies of the node and collocate
                    for ngram_size, colligations_freqs in colligations_freqs_file_all.items():
                        o1xs[ngram_size] = collections.Counter()
                        ox1s[ngram_size] = collections.Counter()

                        for (node, collocate), freq in colligations_freqs.items():
                            o1xs[ngram_size][node] += freq
                            ox1s[ngram_size][collocate] += freq

                        oxxs[ngram_size] = sum(colligations_freqs.values())

                    # Observed values
                    o11s = numpy.empty(shape = num_colligations_all, dtype = float)
                    o12s = numpy.empty(shape = num_colligations_all, dtype = float)
                    o21s = numpy.empty(shape = num_colligations_all, dtype = float)
                    o22s = numpy.empty(shape = num_colligations_all, dtype = float)

                    for i, (node, collocate) in enumerate(colligations_all):
                        len_node = len(node)

                        o11s[i] = sum(colligations_freqs_file.get((node, collocate), [0]))
                        o12s[i] = o1xs[len_node][node] - o11s[i]
                        o21s[i] = ox1s[len_node][collocate] - o11s[i]
                        o22s[i] = oxxs[len_node] - o11s[i] - o12s[i] - o21s[i]

                    # Test Statistic & p-value
                    if test_statistical_significance == 'none':
                        test_stats = [None] * num_colligations_all
                        p_vals = [None] * num_colligations_all
                    else:
                        if test_statistical_significance == 'z_test_berry_rogghe':
                            test_stats, p_vals = func_statistical_significance(self.main, o11s, o12s, o21s, o22s, span)
                        else:
                            test_stats, p_vals = func_statistical_significance(self.main, o11s, o12s, o21s, o22s)

                    # Bayes Factor
                    if measure_bayes_factor == 'none':
                        bayes_factors = [None] * num_colligations_all
                    else:
                        bayes_factors = func_bayes_factor(self.main, o11s, o12s, o21s, o22s)

                    # Effect Size
                    if measure_effect_size == 'none':
                        effect_sizes = [None] * num_colligations_all
                    else:
                        effect_sizes = func_effect_size(self.main, o11s, o12s, o21s, o22s)

                    for i, (node, collocate) in enumerate(colligations_all):
                        colligations_stats_file[(node, collocate)] = [
                            test_stats[i],
                            p_vals[i],
                            bayes_factors[i],
                            effect_sizes[i]
                        ]
                else:
                    colligations_stats_file = {
                        (node, collocate): [None] * 4
                        for node, collocate in colligations_all
                    }

                self.colligations_stats_files.append(colligations_stats_file)

            if len(files) == 1:
                self.colligations_freqs_files *= 2
                self.colligations_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Colligation_Extractor_Table(Wl_Worker_Colligation_Extractor):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.colligations_freqs_files),
            wl_misc.merge_dicts(self.colligations_stats_files)
        )

class Wl_Worker_Colligation_Extractor_Fig(Wl_Worker_Colligation_Extractor):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering figure...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.colligations_freqs_files),
            wl_misc.merge_dicts(self.colligations_stats_files)
        )
