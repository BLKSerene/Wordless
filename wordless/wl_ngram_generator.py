# ----------------------------------------------------------------------
# Wordless: Work Area - N-gram Generator
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
from PyQt5.QtWidgets import QCheckBox, QLabel, QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wordless.wl_measures import wl_measure_utils
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

class Wrapper_Ngram_Generator(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.tab = 'ngram_generator'

        # Table
        self.table_ngram_generator = Wl_Table_Ngram_Generator(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_ngram_generator.label_num_results, 0, 0)
        layout_results.addWidget(self.table_ngram_generator.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_ngram_generator.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_exp_selected_cells, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_exp_all_cells, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_clr_table, 2, 4)

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
        ) = wl_widgets.wl_widgets_search_settings(main, tab = self.tab)

        self.label_search_term_position = QLabel(self.tr('Search term position:'), self)
        (
            self.checkbox_search_term_position_sync,
            self.label_search_term_position_min,
            self.spin_box_search_term_position_min,
            self.checkbox_search_term_position_min_no_limit,
            self.label_search_term_position_max,
            self.spin_box_search_term_position_max,
            self.checkbox_search_term_position_max_no_limit
        ) = wl_boxes.wl_spin_boxes_min_max_no_limit(
            self,
            val_min = 1,
            val_max = 100
        )

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(self, tab = self.tab)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_ngram_generator.button_generate_table.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_match_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_without_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.spin_box_search_term_position_min.valueChanged.connect(self.search_settings_changed)
        self.checkbox_search_term_position_min_no_limit.stateChanged.connect(self.search_settings_changed)
        self.spin_box_search_term_position_max.valueChanged.connect(self.search_settings_changed)
        self.checkbox_search_term_position_max_no_limit.stateChanged.connect(self.search_settings_changed)

        layout_search_term_position = wl_layouts.Wl_Layout()
        layout_search_term_position.addWidget(self.label_search_term_position, 0, 0, 1, 2)
        layout_search_term_position.addWidget(self.checkbox_search_term_position_sync, 0, 2)
        layout_search_term_position.addWidget(self.label_search_term_position_min, 1, 0)
        layout_search_term_position.addWidget(self.spin_box_search_term_position_min, 1, 1)
        layout_search_term_position.addWidget(self.checkbox_search_term_position_min_no_limit, 1, 2)
        layout_search_term_position.addWidget(self.label_search_term_position_max, 2, 0)
        layout_search_term_position.addWidget(self.spin_box_search_term_position_max, 2, 1)
        layout_search_term_position.addWidget(self.checkbox_search_term_position_max_no_limit, 2, 2)

        layout_search_term_position.setColumnStretch(1, 1)

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

        self.group_box_search_settings.layout().addLayout(layout_search_term_position, 10, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 12, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 13, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        self.label_ngram_size = QLabel(self.tr('N-gram size:'), self)
        (
            self.checkbox_ngram_size_sync,
            self.label_ngram_size_min,
            self.spin_box_ngram_size_min,
            self.label_ngram_size_max,
            self.spin_box_ngram_size_max
        ) = wl_boxes.wl_spin_boxes_min_max_sync(self)
        self.checkbox_allow_skipped_tokens = QCheckBox(self.tr('Allow skipped tokens:'), self)
        self.spin_box_allow_skipped_tokens = wl_boxes.Wl_Spin_Box(self)

        (
            self.label_measure_dispersion,
            self.combo_box_measure_dispersion,
            self.label_measure_adjusted_freq,
            self.combo_box_measure_adjusted_freq
        ) = wl_widgets.wl_widgets_measures_wordlist_ngram_generation(self)

        self.spin_box_allow_skipped_tokens.setRange(1, 20)

        self.checkbox_ngram_size_sync.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_ngram_size_min.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_ngram_size_max.valueChanged.connect(self.generation_settings_changed)
        self.checkbox_allow_skipped_tokens.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_allow_skipped_tokens.valueChanged.connect(self.generation_settings_changed)

        self.combo_box_measure_dispersion.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_adjusted_freq.currentTextChanged.connect(self.generation_settings_changed)

        layout_allow_skipped_tokens = wl_layouts.Wl_Layout()
        layout_allow_skipped_tokens.addWidget(self.checkbox_allow_skipped_tokens, 0, 0)
        layout_allow_skipped_tokens.addWidget(self.spin_box_allow_skipped_tokens, 0, 1)

        layout_allow_skipped_tokens.setColumnStretch(2, 1)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_ngram_size, 0, 0, 1, 3)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_ngram_size_sync, 0, 3, Qt.AlignRight)
        self.group_box_generation_settings.layout().addWidget(self.label_ngram_size_min, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_ngram_size_min, 1, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_ngram_size_max, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_ngram_size_max, 1, 3)
        self.group_box_generation_settings.layout().addLayout(layout_allow_skipped_tokens, 2, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(self.label_measure_dispersion, 4, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_dispersion, 5, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_adjusted_freq, 6, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_adjusted_freq, 7, 0, 1, 4)

        self.group_box_generation_settings.layout().setColumnStretch(1, 1)
        self.group_box_generation_settings.layout().setColumnStretch(3, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_ngram_generator]
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
        layout_fig_settings_combo_boxes.addWidget(self.checkbox_use_pct, 3, 0, 1, 2)
        layout_fig_settings_combo_boxes.addWidget(self.checkbox_use_cumulative, 4, 0, 1, 2)

        layout_fig_settings_combo_boxes.setColumnStretch(1, 1)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addLayout(layout_fig_settings_combo_boxes, 0, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(self.label_rank, 2, 0, 1, 2)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_sync, 2, 2)
        self.group_box_fig_settings.layout().addWidget(self.label_rank_min, 3, 0)
        self.group_box_fig_settings.layout().addWidget(self.spin_box_rank_min, 3, 1)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_min_no_limit, 3, 2)
        self.group_box_fig_settings.layout().addWidget(self.label_rank_max, 4, 0)
        self.group_box_fig_settings.layout().addWidget(self.spin_box_rank_max, 4, 1)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_max_no_limit, 4, 2)

        self.group_box_fig_settings.layout().setColumnStretch(1, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 4, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['ngram_generator'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['ngram_generator'])

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

        self.spin_box_search_term_position_min.setValue(settings['search_settings']['search_term_position_min'])
        self.checkbox_search_term_position_min_no_limit.setChecked(settings['search_settings']['search_term_position_min_no_limit'])
        self.spin_box_search_term_position_max.setValue(settings['search_settings']['search_term_position_max'])
        self.checkbox_search_term_position_max_no_limit.setChecked(settings['search_settings']['search_term_position_max_no_limit'])

        # Context Settings
        if defaults:
            self.main.wl_context_settings_ngram_generator.load_settings(defaults = True)

        # Generation Settings
        self.checkbox_ngram_size_sync.setChecked(settings['generation_settings']['ngram_size_sync'])
        self.spin_box_ngram_size_min.setValue(settings['generation_settings']['ngram_size_min'])
        self.spin_box_ngram_size_max.setValue(settings['generation_settings']['ngram_size_max'])
        self.checkbox_allow_skipped_tokens.setChecked(settings['generation_settings']['allow_skipped_tokens'])
        self.spin_box_allow_skipped_tokens.setValue(settings['generation_settings']['allow_skipped_tokens_num'])

        self.combo_box_measure_dispersion.set_measure(settings['generation_settings']['measure_dispersion'])
        self.combo_box_measure_adjusted_freq.set_measure(settings['generation_settings']['measure_adjusted_freq'])

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
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['token_settings']

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

        self.checkbox_match_tags.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.model().stringList()

        settings['match_case'] = self.checkbox_match_case.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()
        settings['match_without_tags'] = self.checkbox_match_without_tags.isChecked()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

        settings['search_term_position_min'] = self.spin_box_search_term_position_min.value()
        settings['search_term_position_min_no_limit'] = self.checkbox_search_term_position_min_no_limit.isChecked()
        settings['search_term_position_max'] = self.spin_box_search_term_position_max.value()
        settings['search_term_position_max_no_limit'] = self.checkbox_search_term_position_max_no_limit.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['generation_settings']

        settings['ngram_size_sync'] = self.checkbox_ngram_size_sync.isChecked()
        settings['ngram_size_min'] = self.spin_box_ngram_size_min.value()
        settings['ngram_size_max'] = self.spin_box_ngram_size_max.value()
        settings['allow_skipped_tokens'] = self.checkbox_allow_skipped_tokens.isChecked()
        settings['allow_skipped_tokens_num'] = self.spin_box_allow_skipped_tokens.value()

        settings['measure_dispersion'] = self.combo_box_measure_dispersion.get_measure()
        settings['measure_adjusted_freq'] = self.combo_box_measure_adjusted_freq.get_measure()

        # Search term position
        if self.spin_box_search_term_position_max.value() == self.spin_box_search_term_position_max.maximum():
            self.spin_box_search_term_position_min.setMaximum(settings['ngram_size_max'])
            self.spin_box_search_term_position_max.setMaximum(settings['ngram_size_max'])

            self.spin_box_search_term_position_max.setValue(settings['ngram_size_max'])
        else:
            self.spin_box_search_term_position_min.setMaximum(settings['ngram_size_max'])
            self.spin_box_search_term_position_max.setMaximum(settings['ngram_size_max'])

        # Allow skipped tokens
        if settings['allow_skipped_tokens']:
            self.spin_box_allow_skipped_tokens.setEnabled(True)
        else:
            self.spin_box_allow_skipped_tokens.setEnabled(False)

        # Use data
        self.combo_box_use_data.measures_changed()

    def table_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()
        settings['show_cum_data'] = self.checkbox_show_cum_data.isChecked()
        settings['show_breakdown_file'] = self.checkbox_show_breakdown_file.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['sort_by_file'] = self.combo_box_sort_by_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

class Wl_Table_Ngram_Generator(wl_tables.Wl_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'ngram_generator',
            headers = [
                _tr('Wl_Table_Ngram_Generator', 'Rank'),
                _tr('Wl_Table_Ngram_Generator', 'N-gram'),
                _tr('Wl_Table_Ngram_Generator', 'Number of\nFiles Found'),
                _tr('Wl_Table_Ngram_Generator', 'Number of\nFiles Found %'),
            ],
            headers_int = [
                _tr('Wl_Table_Ngram_Generator', 'Rank'),
                _tr('Wl_Table_Ngram_Generator', 'Number of\nFiles Found')
            ],
            headers_pct = [
                _tr('Wl_Table_Ngram_Generator', 'Number of\nFiles Found %')
            ],
            enable_sorting = True
        )

    @wl_misc.log_time
    def generate_table(self):
        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['ngram_generator']['search_settings']
        ):
            if self.main.settings_custom['ngram_generator']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ['pos_taggers'])
            else:
                nlp_support_ok = True

            if nlp_support_ok:
                worker_ngram_generator_table = Wl_Worker_Ngram_Generator_Table(
                    self.main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                    update_gui = self.update_gui_table
                )

                wl_threading.Wl_Thread(worker_ngram_generator_table).start_worker()

    def update_gui_table(self, err_msg, ngrams_freq_files, ngrams_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, ngrams_freq_files):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                settings = self.settings['ngram_generator']

                measure_dispersion = settings['generation_settings']['measure_dispersion']
                measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                col_text_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['col_text']
                col_text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col_text']

                self.clr_table()
                self.model().setRowCount(len(ngrams_freq_files))

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for file in files + [{'name': self.tr('Total')}]:
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

                    if measure_dispersion != 'none':
                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            f'[{file["name"]}]\n{col_text_dispersion}',
                            is_float = True,
                            is_breakdown_file = is_breakdown_file
                        )

                    if measure_adjusted_freq != 'none':
                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            f'[{file["name"]}]\n{col_text_adjusted_freq}',
                            is_float = True,
                            is_breakdown_file = is_breakdown_file
                        )

                # Sort by frequency of the first file
                self.horizontalHeader().setSortIndicator(
                    self.find_header_hor(self.tr('[{}]\nFrequency').format(files[0]['name'])),
                    Qt.DescendingOrder
                )

                cols_freq = self.find_headers_hor(self.tr('\nFrequency'))
                cols_freq_pct = self.find_headers_hor(self.tr('\nFrequency %'))

                for col in cols_freq_pct:
                    cols_freq.remove(col)

                cols_dispersion = self.find_headers_hor(f'\n{col_text_dispersion}')
                cols_adjusted_freq = self.find_headers_hor(f'\n{col_text_adjusted_freq}')
                col_files_found = self.find_header_hor(self.tr('Number of\nFiles Found'))
                col_files_found_pct = self.find_header_hor(self.tr('Number of\nFiles Found %'))

                freq_totals = numpy.array(list(ngrams_freq_files.values())).sum(axis = 0)
                len_files = len(files)

                self.disable_updates()

                for i, (ngram, freq_files) in enumerate(wl_sorting.sorted_freq_files_items(ngrams_freq_files)):
                    stats_files = ngrams_stats_files[ngram]

                    # Rank
                    self.set_item_num(i, 0, -1)

                    # N-gram
                    self.model().setItem(i, 1, wl_tables.Wl_Table_Item(' '.join(wl_texts.to_display_texts(ngram))))
                    self.model().item(i, 1).tokens_search = ngram
                    self.model().item(i, 1).tokens_filter = ngram

                    # Frequency
                    for j, freq in enumerate(freq_files):
                        self.set_item_num(i, cols_freq[j], freq)
                        self.set_item_num(i, cols_freq_pct[j], freq, freq_totals[j])

                    for j, (dispersion, adjusted_freq) in enumerate(stats_files):
                        # Dispersion
                        if dispersion is not None:
                            self.set_item_num(i, cols_dispersion[j], dispersion)

                        # Adjusted Frequency
                        if adjusted_freq is not None:
                            self.set_item_num(i, cols_adjusted_freq[j], adjusted_freq)

                    # Number of Files Found
                    num_files_found = len([freq for freq in freq_files[:-1] if freq])

                    self.set_item_num(i, col_files_found, num_files_found)
                    self.set_item_num(i, col_files_found_pct, num_files_found, len_files)

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
        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['ngram_generator']['search_settings']
        ):
            if self.main.settings_custom['ngram_generator']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ['pos_taggers'])
            else:
                nlp_support_ok = True

            if nlp_support_ok:
                self.worker_ngram_generator_fig = Wl_Worker_Ngram_Generator_Fig(
                    self.main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                    update_gui = self.update_gui_fig
                )

                wl_threading.Wl_Thread(self.worker_ngram_generator_fig).start_worker()

    def update_gui_fig(self, err_msg, ngrams_freq_files, ngrams_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, ngrams_freq_files):
            try:
                settings = self.main.settings_custom['ngram_generator']

                if settings['fig_settings']['use_data'] == self.tr('Frequency'):
                    wl_figs_freqs.wl_fig_freqs(
                        self.main, ngrams_freq_files,
                        tab = 'ngram_generator'
                    )
                else:
                    measure_dispersion = settings['generation_settings']['measure_dispersion']
                    measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                    col_text_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['col_text']
                    col_text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col_text']

                    if settings['fig_settings']['use_data'] == col_text_dispersion:
                        ngrams_stat_files = {
                            ngram: numpy.array(stats_files)[:, 0]
                            for ngram, stats_files in ngrams_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == col_text_adjusted_freq:
                        ngrams_stat_files = {
                            ngram: numpy.array(stats_files)[:, 1]
                            for ngram, stats_files in ngrams_stats_files.items()
                        }

                    wl_figs_stats.wl_fig_stats(
                        self.main, ngrams_stat_files,
                        tab = 'ngram_generator'
                    )

                # Hide the progress dialog early so that the main window will not obscure the generated figure
                self.worker_ngram_generator_fig.dialog_progress.accept()
                wl_figs.show_fig()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_fig(self.main, err_msg)

class Wl_Worker_Ngram_Generator(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, dict, dict)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.ngrams_freq_files = []
        self.ngrams_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['ngram_generator']

            ngram_size_min = settings['generation_settings']['ngram_size_min']
            ngram_size_max = settings['generation_settings']['ngram_size_max']
            allow_skipped_tokens = settings['generation_settings']['allow_skipped_tokens']
            allow_skipped_tokens_num = settings['generation_settings']['allow_skipped_tokens_num']

            files = list(self.main.wl_file_area.get_selected_files())

            # Frequency
            for file in files:
                ngrams_is = []

                text = wl_token_processing.wl_process_tokens_ngram_generator(
                    self.main, file['text'],
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )
                tokens = text.get_tokens_flat()

                # Generate all possible n-grams/skip-grams with the index of their first token
                if allow_skipped_tokens:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        ngrams = wl_nlp_utils.skipgrams(tokens, ngram_size, allow_skipped_tokens_num)
                        ngrams_is.extend(self.get_ngrams_is(ngrams, tokens))

                else:
                    ngrams = wl_nlp_utils.everygrams(tokens, ngram_size_min, ngram_size_max)
                    ngrams_is.extend(self.get_ngrams_is(ngrams, tokens))

                # Remove n-grams with at least 1 empty token
                ngrams_is = [
                    (ngram, ngram_i)
                    for ngram, ngram_i in ngrams_is
                    if all(ngram)
                ]

                # Filter search terms & search term positions
                ngrams_is_filtered = []

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

                if settings['search_settings']['search_term_position_min_no_limit']:
                    search_term_position_min = 0
                else:
                    search_term_position_min = settings['search_settings']['search_term_position_min'] - 1

                if settings['search_settings']['search_term_position_max_no_limit']:
                    search_term_position_max = ngram_size_max - 1
                else:
                    search_term_position_max = settings['search_settings']['search_term_position_max'] - 1

                for search_term in search_terms:
                    len_search_term = len(search_term)

                    for ngram, ngram_i in ngrams_is:
                        for i in range(search_term_position_min, search_term_position_max + 1):
                            if ngram[i : i + len_search_term] == search_term:
                                ngrams_is_filtered.append((ngram, ngram_i))

                # Check context settings
                ngrams_is = (
                    (ngram, ngram_i)
                    for ngram, ngram_i in ngrams_is_filtered
                    if wl_matching.check_context(
                        ngram_i, tokens,
                        context_settings = settings['search_settings']['context_settings'],
                        search_terms_incl = search_terms_incl,
                        search_terms_excl = search_terms_excl
                    )
                )

                self.ngrams_freq_files.append(collections.Counter((
                    ngram
                    for ngram, ngram_i in ngrams_is
                )))

                texts.append(text)

            # Total
            if len(files) > 1:
                texts.append(wl_texts.Wl_Text_Total(texts))

                self.ngrams_freq_files.append(sum([
                    collections.Counter(ngrams_freq_file)
                    for ngrams_freq_file in self.ngrams_freq_files
                ], collections.Counter()))

            # Dispersion & Adjusted Frequency
            measure_dispersion = settings['generation_settings']['measure_dispersion']
            measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            func_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['func']
            func_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['func']

            type_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['type']
            type_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['type']

            ngrams_total = list(self.ngrams_freq_files[-1].keys())

            for text in texts:
                ngrams_lens = {}
                ngrams_stats_file = {}

                tokens = text.get_tokens_flat()

                if allow_skipped_tokens:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        ngrams_lens[ngram_size] = list(wl_nlp_utils.skipgrams(tokens, ngram_size, allow_skipped_tokens_num))
                else:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        ngrams_lens[ngram_size] = list(wl_nlp_utils.ngrams(tokens, ngram_size))

                # Dispersion
                if measure_dispersion == 'none':
                    ngrams_stats_file = {
                        ngram: [None]
                        for ngram in ngrams_total
                    }
                elif type_dispersion == 'parts_based':
                    freqs_sections_ngrams = {}

                    for ngram_size, ngram_list in ngrams_lens.items():
                        ngrams_total_len = [ngram for ngram in ngrams_total if len(ngram) == ngram_size]

                        freqs_sections_ngrams.update(wl_measure_utils.to_freqs_sections_dispersion(
                            self.main,
                            items_to_search = ngrams_total_len,
                            items = ngram_list
                        ))

                    for ngram, freqs in freqs_sections_ngrams.items():
                        ngrams_stats_file[ngram] = [func_dispersion(self.main, freqs)]
                elif type_dispersion == 'dist_based':
                    for ngram_size, ngram_list in ngrams_lens.items():
                        ngrams_total_len = [ngram for ngram in ngrams_total if len(ngram) == ngram_size]

                        for ngram in ngrams_total_len:
                            ngrams_stats_file[ngram] = [func_dispersion(self.main, ngram_list, ngram)]

                # Adjusted Frequency
                if measure_adjusted_freq == 'none':
                    ngrams_stats_file = {
                        ngram: stats + [None]
                        for ngram, stats in ngrams_stats_file.items()
                    }
                elif type_adjusted_freq == 'parts_based':
                    freqs_sections_ngrams = {}

                    for ngram_size, ngram_list in ngrams_lens.items():
                        ngrams_total_len = [ngram for ngram in ngrams_total if len(ngram) == ngram_size]

                        freqs_sections_ngrams.update(wl_measure_utils.to_freqs_sections_adjusted_freq(
                            self.main,
                            items_to_search = ngrams_total_len,
                            items = ngram_list
                        ))

                    for ngram, freqs in freqs_sections_ngrams.items():
                        ngrams_stats_file[ngram].append(func_adjusted_freq(self.main, freqs))
                elif type_adjusted_freq == 'dist_based':
                    for ngram_size, ngram_list in ngrams_lens.items():
                        ngrams_total_len = [ngram for ngram in ngrams_total if len(ngram) == ngram_size]

                        for ngram in ngrams_total_len:
                            ngrams_stats_file[ngram].append(func_adjusted_freq(self.main, ngram_list, ngram))

                self.ngrams_stats_files.append(ngrams_stats_file)

            if len(files) == 1:
                self.ngrams_freq_files *= 2
                self.ngrams_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

    def get_ngrams_is(self, ngrams, tokens):
        ngrams_is = []
        i = 0

        for ngram in ngrams:
            if ngram[0] != tokens[i]:
                i += 1

            ngrams_is.append((ngram, i))

        return ngrams_is

class Wl_Worker_Ngram_Generator_Table(Wl_Worker_Ngram_Generator):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.ngrams_freq_files),
            wl_misc.merge_dicts(self.ngrams_stats_files)
        )

class Wl_Worker_Ngram_Generator_Fig(Wl_Worker_Ngram_Generator):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering figure...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.ngrams_freq_files),
            wl_misc.merge_dicts(self.ngrams_stats_files)
        )
