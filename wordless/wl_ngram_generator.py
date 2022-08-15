# ----------------------------------------------------------------------
# Wordless: N-gram Generator
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

import nltk
import numpy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QGroupBox

from wordless.wl_dialogs import wl_dialogs_errs, wl_dialogs_misc, wl_msg_boxes
from wordless.wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wordless.wl_measures import wl_measures_adjusted_freq, wl_measures_dispersion
from wordless.wl_nlp import wl_matching, wl_texts, wl_token_processing
from wordless.wl_utils import wl_misc, wl_msgs, wl_sorting, wl_threading
from wordless.wl_widgets import wl_boxes, wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

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
            sorting_enabled = True
        )

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_fig.clicked.connect(lambda: generate_fig(self.main))
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())

    def file_changed(self, item): # pylint: disable=unused-argument
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
            self.button_generate_fig.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)
            self.button_generate_fig.setEnabled(False)

class Wrapper_Ngram_Generator(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_ngram_generator = Wl_Table_Ngram_Generator(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_ngram_generator.label_number_results, 0, 0)
        layout_results.addWidget(self.table_ngram_generator.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_ngram_generator.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_exp_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_exp_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_ngram_generator.button_clr, 2, 4)

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

            self.token_checkbox_ignore_tags,
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

        self.token_checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
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

        self.group_box_token_settings.layout().addWidget(self.token_checkbox_ignore_tags, 8, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 8, 1)

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
            main,
            tab = 'ngram_generator'
        )

        self.label_search_term_position = QLabel(self.tr('Search Term Position:'), self)
        (
            self.label_search_term_position_min,
            self.spin_box_search_term_position_min,
            self.checkbox_search_term_position_min_no_limit,
            self.label_search_term_position_max,
            self.spin_box_search_term_position_max,
            self.checkbox_search_term_position_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100
        )

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(
            self,
            tab = 'ngram_generator'
        )

        self.group_box_search_settings.setCheckable(True)

        self.group_box_search_settings.toggled.connect(self.search_settings_changed)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_ngram_generator.button_generate_table.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.search_checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.spin_box_search_term_position_min.valueChanged.connect(self.search_settings_changed)
        self.checkbox_search_term_position_min_no_limit.stateChanged.connect(self.search_settings_changed)
        self.spin_box_search_term_position_max.valueChanged.connect(self.search_settings_changed)
        self.checkbox_search_term_position_max_no_limit.stateChanged.connect(self.search_settings_changed)

        layout_search_term_position = wl_layouts.Wl_Layout()
        layout_search_term_position.addWidget(self.label_search_term_position, 0, 0, 1, 3)
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
        self.group_box_search_settings.layout().addWidget(self.label_separator, 2, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_ignore_case, 3, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_words, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.search_checkbox_ignore_tags, 7, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_search_term_position, 10, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 12, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 13, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        self.label_ngram_size = QLabel(self.tr('N-gram Size:'), self)
        (
            self.checkbox_ngram_size_sync,
            self.label_ngram_size_min,
            self.spin_box_ngram_size_min,
            self.label_ngram_size_max,
            self.spin_box_ngram_size_max
        ) = wl_widgets.wl_widgets_size(self)
        self.checkbox_allow_skipped_tokens = QCheckBox(self.tr('Allow skipped tokens:'), self)
        self.spin_box_allow_skipped_tokens = wl_boxes.Wl_Spin_Box(self)

        (
            self.label_measure_dispersion,
            self.combo_box_measure_dispersion,
            self.label_measure_adjusted_freq,
            self.combo_box_measure_adjusted_freq
        ) = wl_widgets.wl_widgets_measures_wordlist_generator(self)

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
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_ngram_generator]
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
        ) = wl_widgets.wl_widgets_fig_settings(self, tab = 'ngram_generator')

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
        layout_fig_settings_combo_boxes.addWidget(self.checkbox_use_pct, 3, 0, 1, 2)
        layout_fig_settings_combo_boxes.addWidget(self.checkbox_use_cumulative, 4, 0, 1, 2)

        layout_fig_settings_combo_boxes.setColumnStretch(1, 1)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addLayout(layout_fig_settings_combo_boxes, 0, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(self.label_rank, 2, 0, 1, 3)
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

        self.wrapper_settings.layout().setRowStretch(5, 1)

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
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.checkbox_treat_as_all_lowercase.setChecked(settings['token_settings']['treat_as_all_lowercase'])
        self.checkbox_lemmatize_tokens.setChecked(settings['token_settings']['lemmatize_tokens'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.token_checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.group_box_search_settings.setChecked(settings['search_settings']['search_settings'])

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

        self.combo_box_measure_dispersion.setCurrentText(settings['generation_settings']['measure_dispersion'])
        self.combo_box_measure_adjusted_freq.setCurrentText(settings['generation_settings']['measure_adjusted_freq'])

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
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.token_checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        # Check if searching is enabled
        if self.group_box_search_settings.isChecked():
            self.checkbox_match_tags.token_settings_changed()
        else:
            self.group_box_search_settings.setChecked(True)

            self.checkbox_match_tags.token_settings_changed()

            self.group_box_search_settings.setChecked(False)

        self.main.wl_context_settings_ngram_generator.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['search_settings']

        settings['search_settings'] = self.group_box_search_settings.isChecked()

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.model().stringList()

        settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()

        settings['ignore_tags'] = self.search_checkbox_ignore_tags.isChecked()
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

        settings['measure_dispersion'] = self.combo_box_measure_dispersion.currentText()
        settings['measure_adjusted_freq'] = self.combo_box_measure_adjusted_freq.currentText()

        # Keyword Position
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

        # Use Data
        self.combo_box_use_data.measures_changed()

    def table_settings_changed(self):
        settings = self.main.settings_custom['ngram_generator']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

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

                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens_ngram_generator(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                tokens = text.tokens_flat

                # Generate all possible n-grams/skip-grams with the index of their first token
                if allow_skipped_tokens:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        if ngram_size == 1:
                            ngrams = nltk.ngrams(tokens, 1)
                        else:
                            ngrams = nltk.skipgrams(tokens, ngram_size, allow_skipped_tokens_num)

                        ngrams_is.extend(self.get_ngrams_is(ngrams, tokens))

                else:
                    ngrams = nltk.everygrams(tokens, ngram_size_min, ngram_size_max)

                    ngrams_is.extend(self.get_ngrams_is(ngrams, tokens))

                # Remove n-grams with at least 1 empty token
                ngrams_is = [
                    (ngram, ngram_i)
                    for ngram, ngram_i in ngrams_is
                    if all(ngram)
                ]

                # Filter search terms & search term positions
                if settings['search_settings']['search_settings']:
                    ngrams_is_filtered = []

                    search_terms = wl_matching.match_search_terms(
                        self.main, tokens,
                        lang = text.lang,
                        tokenized = text.tokenized,
                        tagged = text.tagged,
                        token_settings = settings['token_settings'],
                        search_settings = settings['search_settings']
                    )

                    (
                        search_terms_inclusion,
                        search_terms_exclusion
                    ) = wl_matching.match_search_terms_context(
                        self.main, tokens,
                        lang = text.lang,
                        tokenized = text.tokenized,
                        tagged = text.tagged,
                        token_settings = settings['token_settings'],
                        context_settings = settings['context_settings']
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
                            context_settings = settings['context_settings'],
                            search_terms_inclusion = search_terms_inclusion,
                            search_terms_exclusion = search_terms_exclusion
                        )
                    )

                self.ngrams_freq_files.append(collections.Counter((
                    ngram
                    for ngram, ngram_i in ngrams_is
                )))

                texts.append(text)

            # Total
            if len(files) > 1:
                text_total = wl_texts.Wl_Text_Blank()
                text_total.tokens_flat = [token for text in texts for token in text.tokens_flat]

                self.ngrams_freq_files.append(sum([
                    collections.Counter(ngrams_freq_file)
                    for ngrams_freq_file in self.ngrams_freq_files
                ], collections.Counter()))

                texts.append(text_total)

            # Dispersion & Adjusted Frequency
            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            measure_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['func']
            measure_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['func']

            ngrams_total = list(self.ngrams_freq_files[-1].keys())

            for text in texts:
                ngrams_lens = {}
                ngrams_stats_file = {}

                if allow_skipped_tokens:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        if ngram_size == 1:
                            ngrams_lens[ngram_size] = list(nltk.ngrams(text.tokens_flat, ngram_size))
                        else:
                            ngrams_lens[ngram_size] = list(nltk.skipgrams(text.tokens_flat, ngram_size, allow_skipped_tokens_num))
                else:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        ngrams_lens[ngram_size] = list(nltk.ngrams(text.tokens_flat, ngram_size))

                # Dispersion
                if measure_dispersion is None:
                    ngrams_stats_file = {ngram: [None] for ngram in ngrams_total}
                else:
                    freqs_sections_ngrams = {}

                    for ngram_size, ngram_list in ngrams_lens.items():
                        ngrams_total_len = [ngram for ngram in ngrams_total if len(ngram) == ngram_size]

                        freqs_sections_ngrams.update(wl_measures_dispersion.to_freq_sections_items(
                            self.main,
                            items_search = ngrams_total_len,
                            items = ngram_list
                        ))

                    for ngram, freqs in freqs_sections_ngrams.items():
                        ngrams_stats_file[ngram] = [measure_dispersion(freqs)]

                # Adjusted Frequency
                if measure_adjusted_freq is None:
                    ngrams_stats_file = {ngram: stats + [None] for ngram, stats in ngrams_stats_file.items()}
                else:
                    freqs_sections_ngrams = {}

                    for ngram_size, ngram_list in ngrams_lens.items():
                        ngrams_total_len = [ngram for ngram in ngrams_total if len(ngram) == ngram_size]

                        freqs_sections_ngrams.update(wl_measures_adjusted_freq.to_freq_sections_items(
                            self.main,
                            items_search = ngrams_total_len,
                            items = ngram_list
                        ))

                    for ngram, freqs in freqs_sections_ngrams.items():
                        ngrams_stats_file[ngram].append(measure_adjusted_freq(freqs))

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

@wl_misc.log_timing
def generate_table(main, table):
    def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
        if not err_msg:
            if ngrams_freq_files:
                try:
                    table.settings = copy.deepcopy(main.settings_custom)

                    text_measure_dispersion = settings['generation_settings']['measure_dispersion']
                    text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                    text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
                    text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

                    table.clr_table()

                    # Insert columns (files)
                    files = list(main.wl_file_area.get_selected_files())

                    for i, file in enumerate(files):
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_ngram_generator', '[{}]\nFrequency').format(file['name']),
                            is_int = True, is_cumulative = True, is_breakdown = True
                        )
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_ngram_generator', '[{}]\nFrequency %').format(file['name']),
                            is_pct = True, is_cumulative = True, is_breakdown = True
                        )

                        if text_dispersion is not None:
                            table.ins_header_hor(
                                table.model().columnCount() - 2,
                                f'[{file["name"]}]\n{text_dispersion}',
                                is_float = True, is_breakdown = True
                            )

                        if text_adjusted_freq is not None:
                            table.ins_header_hor(
                                table.model().columnCount() - 2,
                                f'[{file["name"]}]\n{text_adjusted_freq}',
                                is_float = True, is_breakdown = True
                            )

                    # Insert columns (total)
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_ngram_generator', 'Total\nFrequency'),
                        is_int = True, is_cumulative = True
                    )
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        _tr('wl_ngram_generator', 'Total\nFrequency %'),
                        is_pct = True, is_cumulative = True
                    )

                    if text_dispersion is not None:
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_ngram_generator', 'Total\n') + text_dispersion,
                            is_float = True
                        )

                    if text_adjusted_freq is not None:
                        table.ins_header_hor(
                            table.model().columnCount() - 2,
                            _tr('wl_ngram_generator', 'Total\n') + text_adjusted_freq,
                            is_float = True
                        )

                    # Sort by frequency of the first file
                    table.horizontalHeader().setSortIndicator(
                        table.find_header_hor(_tr('wl_ngram_generator', '[{}]\nFrequency').format(files[0]['name'])),
                        Qt.DescendingOrder
                    )

                    cols_freq = table.find_headers_hor(_tr('wl_ngram_generator', '\nFrequency'))
                    cols_freq_pct = table.find_headers_hor(_tr('wl_ngram_generator', '\nFrequency %'))

                    for col in cols_freq_pct:
                        cols_freq.remove(col)

                    cols_dispersion = table.find_headers_hor(f'\n{text_dispersion}') if text_measure_dispersion else None
                    cols_adjusted_freq = table.find_headers_hor(f'\n{text_adjusted_freq}') if text_measure_adjusted_freq else None
                    col_files_found = table.find_header_hor(_tr('wl_ngram_generator', 'Number of\nFiles Found'))
                    col_files_found_pct = table.find_header_hor(_tr('wl_ngram_generator', 'Number of\nFiles Found %'))

                    freq_totals = numpy.array(list(ngrams_freq_files.values())).sum(axis = 0)
                    len_files = len(files)

                    table.model().setRowCount(len(ngrams_freq_files))

                    table.disable_updates()

                    for i, (ngram, freq_files) in enumerate(wl_sorting.sorted_freq_files_items(ngrams_freq_files)):
                        stats_files = ngrams_stats_files[ngram]

                        # Rank
                        table.set_item_num(i, 0, -1)

                        # N-gram
                        table.model().setItem(i, 1, wl_tables.Wl_Table_Item(' '.join(ngram)))

                        table.model().item(i, 1).text_raw = ngram

                        # Frequency
                        for j, freq in enumerate(freq_files):
                            table.set_item_num(i, cols_freq[j], freq)
                            table.set_item_num(i, cols_freq_pct[j], freq, freq_totals[j])

                        for j, (dispersion, adjusted_freq) in enumerate(stats_files):
                            # Dispersion
                            if dispersion is not None:
                                table.set_item_num(i, cols_dispersion[j], dispersion)

                            # Adjusted Frequency
                            if adjusted_freq is not None:
                                table.set_item_num(i, cols_adjusted_freq[j], adjusted_freq)

                        # Number of Files Found
                        num_files_found = len([freq for freq in freq_files[:-1] if freq])

                        table.set_item_num(i, col_files_found, num_files_found)
                        table.set_item_num(i, col_files_found_pct, num_files_found, len_files)

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

    settings = main.settings_custom['ngram_generator']

    if (
        not settings['search_settings']['search_settings']
        or not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']
        or settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']
    ):
        worker_ngram_generator_table = Wl_Worker_Ngram_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        )
        wl_threading.Wl_Thread(worker_ngram_generator_table).start_worker()
    else:
        wl_msg_boxes.wl_msg_box_missing_search_terms_optional(main)
        wl_msgs.wl_msg_generate_table_error(main)

@wl_misc.log_timing
def generate_fig(main):
    def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
        if not err_msg:
            if ngrams_freq_files:
                try:
                    text_measure_dispersion = settings['generation_settings']['measure_dispersion']
                    text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                    text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
                    text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

                    if settings['fig_settings']['use_data'] == _tr('wl_ngram_generator', 'Frequency'):
                        ngrams_freq_files = {
                            ' '.join(ngram): freqs
                            for ngram, freqs in ngrams_freq_files.items()
                        }

                        wl_figs_freqs.wl_fig_freqs(
                            main, ngrams_freq_files,
                            tab = 'ngram_generator'
                        )
                    else:
                        ngrams_stats_files = {
                            ' '.join(ngram): stats
                            for ngram, stats in ngrams_stats_files.items()
                        }

                        if settings['fig_settings']['use_data'] == text_dispersion:
                            ngrams_stat_files = {
                                ngram: numpy.array(stats_files)[:, 0]
                                for ngram, stats_files in ngrams_stats_files.items()
                            }
                        elif settings['fig_settings']['use_data'] == text_adjusted_freq:
                            ngrams_stat_files = {
                                ngram: numpy.array(stats_files)[:, 1]
                                for ngram, stats_files in ngrams_stats_files.items()
                            }

                        wl_figs_stats.wl_fig_stats(
                            main, ngrams_stat_files,
                            tab = 'ngram_generator'
                        )

                    # Hide the progress dialog early so that the main window will not obscure the generated figure
                    worker_ngram_generator_fig.dialog_progress.accept()
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

    settings = main.settings_custom['ngram_generator']

    if (
        not settings['search_settings']['search_settings']
        or not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']
        or settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']
    ):
        worker_ngram_generator_fig = Wl_Worker_Ngram_Generator_Fig(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        )
        wl_threading.Wl_Thread(worker_ngram_generator_fig).start_worker()
    else:
        wl_msg_boxes.wl_msg_box_missing_search_terms_optional(main)
        wl_msgs.wl_msg_generate_fig_error(main)
