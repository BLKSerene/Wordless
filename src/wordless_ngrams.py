#
# Wordless: N-grams
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import collections
import copy
import itertools
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy

from wordless_checking import wordless_checking_file
from wordless_dialogs import wordless_dialog_misc, wordless_msg_box
from wordless_figs import wordless_fig, wordless_fig_freq, wordless_fig_stat
from wordless_text import (wordless_matching, wordless_text, wordless_text_processing,
                           wordless_text_utils, wordless_token_processing)
from wordless_utils import wordless_misc, wordless_sorting, wordless_threading
from wordless_widgets import (wordless_box, wordless_layout, wordless_msg,
                              wordless_table, wordless_widgets)

class Wordless_Table_Ngrams(wordless_table.Wordless_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(parent,
                         tab = 'ngrams',
                         headers = [
                             parent.tr('Rank'),
                             parent.tr('N-grams'),
                             parent.tr('Number of\nFiles Found'),
                         ],
                         headers_num = [
                             parent.tr('Rank'),
                             parent.tr('Number of\nFiles Found')
                         ],
                         headers_pct = [
                             parent.tr('Number of\nFiles Found')
                         ],
                         sorting_enabled = True)

        self.name = 'ngrams'

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_fig.clicked.connect(lambda: generate_fig(self.main))

class Wrapper_Ngrams(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_ngrams = Wordless_Table_Ngrams(self)

        layout_results = wordless_layout.Wordless_Layout()
        layout_results.addWidget(self.table_ngrams.label_number_results, 0, 0)
        layout_results.addWidget(self.table_ngrams.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_ngrams.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_ngrams, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_ngrams.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_ngrams.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_ngrams.button_export_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_ngrams.button_export_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_ngrams.button_clear, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (self.checkbox_words,
         self.checkbox_lowercase,
         self.checkbox_uppercase,
         self.checkbox_title_case,
         self.checkbox_nums,
         self.checkbox_puncs,

         self.checkbox_treat_as_lowercase,
         self.checkbox_lemmatize_tokens,
         self.checkbox_filter_stop_words,

         self.token_stacked_widget_ignore_tags,
         self.token_checkbox_ignore_tags,
         self.token_checkbox_ignore_tags_tags,

         self.token_stacked_widget_ignore_tags_type,
         self.token_combo_box_ignore_tags,
         self.token_combo_box_ignore_tags_tags,

         self.token_label_ignore_tags,
         self.checkbox_use_tags) = wordless_widgets.wordless_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lemmatize_tokens.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.token_checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.token_checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.token_combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.token_combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = wordless_layout.Wordless_Layout()
        layout_ignore_tags.addWidget(self.token_stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.token_stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.token_label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        self.group_box_token_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 2, 1)

        self.group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lemmatize_tokens, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 9, 0, 1, 2)

        # Search Settings
        self.group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

        (self.label_search_term,
         self.checkbox_multi_search_mode,

         self.stacked_widget_search_term,
         self.line_edit_search_term,
         self.list_search_terms,

         self.label_separator,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_words,
         self.checkbox_use_regex,

         self.search_stacked_widget_ignore_tags,
         self.search_checkbox_ignore_tags,
         self.search_checkbox_ignore_tags_tags,

         self.search_stacked_widget_ignore_tags_type,
         self.search_combo_box_ignore_tags,
         self.search_combo_box_ignore_tags_tags,

         self.search_label_ignore_tags,
         self.checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(main,
                                                                                       tab = 'ngrams')

        self.label_search_term_position = QLabel(self.tr('Search Term Position:'), self)
        (self.label_search_term_position_min,
         self.spin_box_search_term_position_min,
         self.checkbox_search_term_position_min_no_limit,
         self.label_search_term_position_max,
         self.spin_box_search_term_position_max,
         self.checkbox_search_term_position_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                     filter_min = 1,
                                                                                                     filter_max = 100)
        self.checkbox_allow_skipped_tokens_within_search_terms = QCheckBox(self.tr('Allow skipped tokens within search terms'), self)

        (self.label_context_settings,
         self.button_context_settings) = wordless_widgets.wordless_widgets_context_settings(self,
                                                                                            tab = 'ngrams')

        self.group_box_search_settings.setCheckable(True)

        self.group_box_search_settings.toggled.connect(self.search_settings_changed)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_ngrams.button_generate_table.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.search_checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.search_checkbox_ignore_tags_tags.stateChanged.connect(self.search_settings_changed)
        self.search_combo_box_ignore_tags.currentTextChanged.connect(self.search_settings_changed)
        self.search_combo_box_ignore_tags_tags.currentTextChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.spin_box_search_term_position_min.valueChanged.connect(self.search_settings_changed)
        self.checkbox_search_term_position_min_no_limit.stateChanged.connect(self.search_settings_changed)
        self.spin_box_search_term_position_max.valueChanged.connect(self.search_settings_changed)
        self.checkbox_search_term_position_max_no_limit.stateChanged.connect(self.search_settings_changed)
        self.checkbox_allow_skipped_tokens_within_search_terms.stateChanged.connect(self.search_settings_changed)

        layout_search_ignore_tags = wordless_layout.Wordless_Layout()
        layout_search_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags, 0, 0)
        layout_search_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags_type, 0, 1)
        layout_search_ignore_tags.addWidget(self.search_label_ignore_tags, 0, 2)

        layout_search_ignore_tags.setColumnStretch(3, 1)

        layout_search_term_position = wordless_layout.Wordless_Layout()
        layout_search_term_position.addWidget(self.label_search_term_position, 0, 0, 1, 3)
        layout_search_term_position.addWidget(self.label_search_term_position_min, 1, 0)
        layout_search_term_position.addWidget(self.spin_box_search_term_position_min, 1, 1)
        layout_search_term_position.addWidget(self.checkbox_search_term_position_min_no_limit, 1, 2)
        layout_search_term_position.addWidget(self.label_search_term_position_max, 2, 0)
        layout_search_term_position.addWidget(self.spin_box_search_term_position_max, 2, 1)
        layout_search_term_position.addWidget(self.checkbox_search_term_position_max_no_limit, 2, 2)

        layout_search_term_position.setColumnStretch(1, 1)

        layout_context_settings = wordless_layout.Wordless_Layout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_separator, 2, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_ignore_case, 3, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_words, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_search_ignore_tags, 7, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 9, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_search_term_position, 10, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_allow_skipped_tokens_within_search_terms, 11, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 12, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 13, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        self.label_ngram_size = QLabel(self.tr('N-gram Size:'), self)
        (self.checkbox_ngram_size_sync,
         self.label_ngram_size_min,
         self.spin_box_ngram_size_min,
         self.label_ngram_size_max,
         self.spin_box_ngram_size_max) = wordless_widgets.wordless_widgets_size(self)
        self.checkbox_allow_skipped_tokens = QCheckBox(self.tr('Allow skipped tokens:'), self)
        self.spin_box_allow_skipped_tokens = wordless_box.Wordless_Spin_Box(self)

        (self.label_measure_dispersion,
         self.combo_box_measure_dispersion) = wordless_widgets.wordless_widgets_measure_dispersion(self)
        (self.label_measure_adjusted_freq,
         self.combo_box_measure_adjusted_freq) = wordless_widgets.wordless_widgets_measure_adjusted_freq(self)

        (self.label_settings_measures,
         self.button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(self,
                                                                                              tab = self.tr('Dispersion'))

        self.spin_box_allow_skipped_tokens.setRange(1, 20)

        self.checkbox_ngram_size_sync.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_ngram_size_min.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_ngram_size_max.valueChanged.connect(self.generation_settings_changed)
        self.checkbox_allow_skipped_tokens.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_allow_skipped_tokens.valueChanged.connect(self.generation_settings_changed)

        self.combo_box_measure_dispersion.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_adjusted_freq.currentTextChanged.connect(self.generation_settings_changed)

        layout_allow_skipped_tokens = wordless_layout.Wordless_Layout()
        layout_allow_skipped_tokens.addWidget(self.checkbox_allow_skipped_tokens, 0, 0)
        layout_allow_skipped_tokens.addWidget(self.spin_box_allow_skipped_tokens, 0, 1)

        layout_allow_skipped_tokens.setColumnStretch(2, 1)

        layout_settings_measures = wordless_layout.Wordless_Layout()
        layout_settings_measures.addWidget(self.label_settings_measures, 0, 0)
        layout_settings_measures.addWidget(self.button_settings_measures, 0, 1)

        layout_settings_measures.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_ngram_size, 0, 0, 1, 3)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_ngram_size_sync, 0, 3, Qt.AlignRight)
        self.group_box_generation_settings.layout().addWidget(self.label_ngram_size_min, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_ngram_size_min, 1, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_ngram_size_max, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_ngram_size_max, 1, 3)
        self.group_box_generation_settings.layout().addLayout(layout_allow_skipped_tokens, 2, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(self.label_measure_dispersion, 4, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_dispersion, 5, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_adjusted_freq, 6, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_adjusted_freq, 7, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 8, 0, 1, 4)

        self.group_box_generation_settings.layout().addLayout(layout_settings_measures, 9, 0, 1, 4)

        self.group_box_generation_settings.layout().setColumnStretch(1, 1)
        self.group_box_generation_settings.layout().setColumnStretch(3, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (self.checkbox_show_pct,
         self.checkbox_show_cumulative,
         self.checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self,
                                                                                          table = self.table_ngrams)

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        (self.label_graph_type,
         self.combo_box_graph_type,
         self.label_use_file,
         self.combo_box_use_file,
         self.label_use_data,
         self.combo_box_use_data,

         self.checkbox_use_pct,
         self.checkbox_use_cumulative) = wordless_widgets.wordless_widgets_fig_settings(self)

        self.label_rank = QLabel(self.tr('Rank:'), self)
        (self.label_rank_min,
         self.spin_box_rank_min,
         self.checkbox_rank_min_no_limit,
         self.label_rank_max,
         self.spin_box_rank_max,
         self.checkbox_rank_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 1,
                                                                                     filter_max = 100000)

        self.combo_box_graph_type.currentTextChanged.connect(self.fig_settings_changed)
        self.combo_box_use_file.currentTextChanged.connect(self.fig_settings_changed)
        self.combo_box_use_data.currentTextChanged.connect(self.fig_settings_changed)
        self.checkbox_use_pct.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_use_cumulative.stateChanged.connect(self.fig_settings_changed)

        self.spin_box_rank_min.valueChanged.connect(self.fig_settings_changed)
        self.checkbox_rank_min_no_limit.stateChanged.connect(self.fig_settings_changed)
        self.spin_box_rank_max.valueChanged.connect(self.fig_settings_changed)
        self.checkbox_rank_max_no_limit.stateChanged.connect(self.fig_settings_changed)

        layout_fig_settings_combo_boxes = wordless_layout.Wordless_Layout()
        layout_fig_settings_combo_boxes.addWidget(self.label_graph_type, 0, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_graph_type, 0, 1)
        layout_fig_settings_combo_boxes.addWidget(self.label_use_file, 1, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_use_file, 1, 1)
        layout_fig_settings_combo_boxes.addWidget(self.label_use_data, 2, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_use_data, 2, 1)

        layout_fig_settings_combo_boxes.setColumnStretch(1, 1)

        self.group_box_fig_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_fig_settings.layout().addLayout(layout_fig_settings_combo_boxes, 0, 0, 1, 3)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_use_pct, 1, 0, 1, 3)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_use_cumulative, 2, 0, 1, 3)
        
        self.group_box_fig_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(self.label_rank, 4, 0, 1, 3)
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

        self.wrapper_settings.layout().setRowStretch(5, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['ngrams'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['ngrams'])

        # Token Settings
        self.checkbox_words.setChecked(settings['token_settings']['words'])
        self.checkbox_lowercase.setChecked(settings['token_settings']['lowercase'])
        self.checkbox_uppercase.setChecked(settings['token_settings']['uppercase'])
        self.checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        self.checkbox_nums.setChecked(settings['token_settings']['nums'])
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.checkbox_treat_as_lowercase.setChecked(settings['token_settings']['treat_as_lowercase'])
        self.checkbox_lemmatize_tokens.setChecked(settings['token_settings']['lemmatize_tokens'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.token_checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.token_checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.token_combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.token_combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
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
        self.search_checkbox_ignore_tags_tags.setChecked(settings['search_settings']['ignore_tags_tags'])
        self.search_combo_box_ignore_tags.setCurrentText(settings['search_settings']['ignore_tags_type'])
        self.search_combo_box_ignore_tags_tags.setCurrentText(settings['search_settings']['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        self.spin_box_search_term_position_min.setValue(settings['search_settings']['search_term_position_min'])
        self.checkbox_search_term_position_min_no_limit.setChecked(settings['search_settings']['search_term_position_min_no_limit'])
        self.spin_box_search_term_position_max.setValue(settings['search_settings']['search_term_position_max'])
        self.checkbox_search_term_position_max_no_limit.setChecked(settings['search_settings']['search_term_position_max_no_limit'])
        self.checkbox_allow_skipped_tokens_within_search_terms.setChecked(settings['search_settings']['allow_skipped_tokens_within_search_terms'])

        # Context Settings
        if defaults:
            self.main.wordless_context_settings_ngrams.load_settings(defaults = True)

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
        self.combo_box_use_file.setCurrentText(settings['fig_settings']['use_file'])
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
        settings = self.main.settings_custom['ngrams']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['lowercase'] = self.checkbox_lowercase.isChecked()
        settings['uppercase'] = self.checkbox_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_lowercase'] = self.checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.token_checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.token_checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.token_combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.token_combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        # Check if searching is enabled
        if self.group_box_search_settings.isChecked():
            self.checkbox_match_tags.token_settings_changed()
        else:
            self.group_box_search_settings.setChecked(True)

            self.checkbox_match_tags.token_settings_changed()

            self.group_box_search_settings.setChecked(False)

        self.main.wordless_context_settings_ngrams.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['ngrams']['search_settings']

        settings['search_settings'] = self.group_box_search_settings.isChecked()

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.get_items()

        settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()

        settings['ignore_tags'] = self.search_checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.search_checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.search_combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.search_combo_box_ignore_tags_tags.currentText()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

        settings['search_term_position_min'] = self.spin_box_search_term_position_min.value()
        settings['search_term_position_min_no_limit'] = self.checkbox_search_term_position_min_no_limit.isChecked()
        settings['search_term_position_max'] = self.spin_box_search_term_position_max.value()
        settings['search_term_position_max_no_limit'] = self.checkbox_search_term_position_max_no_limit.isChecked()
        settings['allow_skipped_tokens_within_search_terms'] = self.checkbox_allow_skipped_tokens_within_search_terms.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['ngrams']['generation_settings']

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

        # Allow skipped tokens within search terms
        if settings['allow_skipped_tokens']:
            self.spin_box_allow_skipped_tokens.setEnabled(True)

            if self.main.settings_custom['ngrams']['search_settings']['search_settings']:
                self.checkbox_allow_skipped_tokens_within_search_terms.setEnabled(True)
        else:
            self.spin_box_allow_skipped_tokens.setEnabled(False)
            self.checkbox_allow_skipped_tokens_within_search_terms.setEnabled(False)

        # Use Data
        use_data_old = self.combo_box_use_data.currentText()

        self.combo_box_use_data.clear()

        self.combo_box_use_data.addItems([
            self.tr('Frequency'),
            self.main.settings_global['measures_dispersion'][settings['measure_dispersion']]['col'],
            self.main.settings_global['measures_adjusted_freq'][settings['measure_adjusted_freq']]['col']
        ])

        if self.combo_box_use_data.findText(use_data_old) > -1:
            self.combo_box_use_data.setCurrentText(use_data_old)
        else:
            self.combo_box_use_data.setCurrentText(self.main.settings_default['ngrams']['fig_settings']['use_data'])

    def table_settings_changed(self):
        settings = self.main.settings_custom['ngrams']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['ngrams']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['use_file'] = self.combo_box_use_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

class Wordless_Worker_Ngrams(wordless_threading.Wordless_Worker):
    worker_done = pyqtSignal(dict, dict, dict)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.ngrams_freq_files = []
        self.ngrams_stats_files = []
        self.ngrams_text = {}

    def run(self):
        texts = []

        settings = self.main.settings_custom['ngrams']

        ngram_size_min = settings['generation_settings']['ngram_size_min']
        ngram_size_max = settings['generation_settings']['ngram_size_max']
        allow_skipped_tokens = settings['generation_settings']['allow_skipped_tokens']
        allow_skipped_tokens_num = settings['generation_settings']['allow_skipped_tokens_num']

        files = self.main.wordless_files.get_selected_files()

        # Frequency
        for file in files:
            ngrams = []

            text = wordless_text.Wordless_Text(self.main, file)

            tokens = wordless_token_processing.wordless_process_tokens_ngrams(text,
                                                                              token_settings = settings['token_settings'])

            search_terms = wordless_matching.match_search_terms(self.main, tokens,
                                                                lang = text.lang,
                                                                text_type = text.text_type,
                                                                token_settings = settings['token_settings'],
                                                                search_settings = settings['search_settings'])

            (search_terms_inclusion,
             search_terms_exclusion) = wordless_matching.match_search_terms_context(self.main, tokens,
                                                                                    lang = text.lang,
                                                                                    text_type = text.text_type,
                                                                                    token_settings = settings['token_settings'],
                                                                                    context_settings = settings['context_settings'])
            if allow_skipped_tokens:
                SENTINEL = object()

                if settings['search_settings']['search_settings']:
                    if settings['search_settings']['allow_skipped_tokens_within_search_terms']:
                        for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                            ngrams.extend(nltk.skipgrams(tokens, ngram_size, allow_skipped_tokens))
                    else:
                        for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                            for search_term in search_terms:
                                len_search_term = len(search_term)

                                if len_search_term < ngram_size:
                                    for i, ngram in enumerate(nltk.ngrams(tokens,
                                                                          ngram_size + allow_skipped_tokens,
                                                                          pad_right = True,
                                                                          right_pad_symbol = SENTINEL)):
                                        for j in range(ngram_size + allow_skipped_tokens - len_search_term + 1):
                                            if ngram[j : j + len_search_term] == search_term:
                                                ngram_cur = list(ngram)
                                                ngram_cur[j : j + len_search_term] = [ngram_cur[j : j + len_search_term]]

                                                head = ngram_cur[0]
                                                tail = ngram_cur[1:]

                                                for skip_tail in itertools.combinations(tail, ngram_size - len_search_term):
                                                    ngram_matched = []

                                                    if type(head) == list:
                                                        ngram_matched.extend(head)
                                                    else:
                                                        ngram_matched.append(head)

                                                    for item in skip_tail:
                                                        if type(item) == list:
                                                            ngram_matched.extend(item)
                                                        else:
                                                            ngram_matched.append(item)

                                                    if skip_tail and skip_tail[-1] != SENTINEL and len(ngram_matched) == ngram_size:
                                                        if wordless_matching.check_context(i + j, tokens,
                                                                                           context_settings = settings['context_settings'],
                                                                                           search_terms_inclusion = search_terms_inclusion,
                                                                                           search_terms_exclusion = search_terms_exclusion):
                                                            ngrams.append(tuple(ngram_matched))
                                elif len_search_term == ngram_size:
                                    for i, ngram in enumerate(nltk.ngrams(tokens, ngram_size)):
                                        if ngram == search_term:
                                            if wordless_matching.check_context(i, tokens,
                                                                               context_settings = settings['context_settings'],
                                                                               search_terms_inclusion = search_terms_inclusion,
                                                                               search_terms_exclusion = search_terms_exclusion):
                                                ngrams.append(ngram)
                else:
                    for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                        for i, ngram in enumerate(nltk.ngrams(tokens,
                                                              ngram_size + allow_skipped_tokens,
                                                              pad_right = True,
                                                              right_pad_symbol = SENTINEL)):
                            for j in range(ngram_size + allow_skipped_tokens):
                                head = ngram[0]
                                tail = ngram[1:]

                                for skip_tail in tail:
                                    if skip_tail != SENTINEL:
                                        if wordless_matching.check_context(i + j, tokens,
                                                                           context_settings = settings['context_settings'],
                                                                           search_terms_inclusion = search_terms_inclusion,
                                                                           search_terms_exclusion = search_terms_exclusion):
                                            ngrams.append((head, skip_tail))
            else:
                for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                    for i, ngram in enumerate(nltk.ngrams(tokens, ngram_size)):
                        if wordless_matching.check_context(i, tokens,
                                                           context_settings = settings['context_settings'],
                                                           search_terms_inclusion = search_terms_inclusion,
                                                           search_terms_exclusion = search_terms_exclusion):
                            ngrams.append(ngram)

            # Remove n-grams with at least 1 empty token
            ngrams_freq_file = collections.Counter([ngram for ngram in ngrams if all(ngram)])

            # Filter search terms & search term positions
            if settings['search_settings']['search_settings']:
                ngrams_freq_file_filtered = {}

                if settings['search_settings']['search_term_position_min_no_limit']:
                    search_term_position_min = 0
                else:
                    search_term_position_min = settings['search_settings']['search_term_position_min'] - 1

                if settings['search_settings']['search_term_position_max_no_limit']:
                    search_term_position_max = ngram_size_max
                else:
                    search_term_position_max = settings['search_settings']['search_term_position_max'] - 1

                for search_term in search_terms:
                    len_search_term = len(search_term)

                    for ngram, freq in ngrams_freq_file.items():
                        for i in range(search_term_position_min, search_term_position_max + 1):
                            if ngram[i : i + len_search_term] == search_term:
                                ngrams_freq_file_filtered[ngram] = freq

                self.ngrams_freq_files.append(ngrams_freq_file_filtered)
            else:
                self.ngrams_freq_files.append(ngrams_freq_file)

            # N-grams Text
            for ngram in ngrams_freq_file:
                self.ngrams_text[ngram] = wordless_text_processing.wordless_word_detokenize(self.main, ngram, text.lang)

            texts.append(text)

        # Total
        if len(files) > 1:
            text_total = wordless_text.Wordless_Text_Blank()
            text_total.tokens_flat = [token for text in texts for token in text.tokens_flat]

            texts.append(text_total)

            self.ngrams_freq_files.append(sum([collections.Counter(ngrams_freq_file) for ngrams_freq_file in self.ngrams_freq_files],
                                         collections.Counter()))

        self.progress_updated.emit(self.tr('Processing data ...'))

        # Dispersion & Adjusted Frequency
        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        measure_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['func']
        measure_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['func']

        ngrams_total = self.ngrams_freq_files[-1].keys()

        for text in texts:
            ngrams_lens = {}
            ngrams_stats_file = {}

            if allow_skipped_tokens == 0:
                for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                    ngrams_lens[ngram_size] = list(nltk.ngrams(text.tokens_flat, ngram_size))
            else:
                for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                    ngrams_lens[ngram_size] = list(nltk.skipgrams(text.tokens_flat, ngram_size, allow_skipped_tokens))

            # Dispersion
            number_sections = self.main.settings_custom['measures']['dispersion']['general']['number_sections']

            sections_freq_lens = {}

            for ngram_size, ngram_list in ngrams_lens.items():
                sections_freq_lens[ngram_size] = [collections.Counter(section)
                                                  for section in wordless_text_utils.to_sections(ngram_list, number_sections)]

            for ngram in ngrams_total:
                counts = [section_freq[ngram] for section_freq in sections_freq_lens[len(ngram)]]

                ngrams_stats_file[ngram] = [measure_dispersion(counts)]

            # Adjusted Frequency
            if not self.main.settings_custom['measures']['adjusted_freq']['general']['use_same_settings_dispersion']:
                number_sections = self.main.settings_custom['measures']['adjusted_freq']['general']['number_sections']

                sections_freq_lens = {}

                for ngram_size, ngrams in ngrams_lens.items():
                    sections_freq_lens[ngram_size] = [collections.Counter(section)
                                                      for section in wordless_text_utils.to_sections(ngrams, number_sections)]

            for ngram in ngrams_total:
                counts = [section_freq[ngram] for
                          section_freq in sections_freq_lens[len(ngram)]]

                ngrams_stats_file[ngram].append(measure_adjusted_freq(counts))

            self.ngrams_stats_files.append(ngrams_stats_file)

        if len(files) == 1:
            self.ngrams_freq_files *= 2
            self.ngrams_stats_files *= 2

class Wordless_Worker_Ngrams_Table(Wordless_Worker_Ngrams):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table ...'))

        time.sleep(0.1)

        self.worker_done.emit(wordless_misc.merge_dicts(self.ngrams_freq_files),
                              wordless_misc.merge_dicts(self.ngrams_stats_files),
                              self.ngrams_text)

class Wordless_Worker_Ngrams_Fig(Wordless_Worker_Ngrams):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering figure ...'))

        time.sleep(0.1)

        self.worker_done.emit(wordless_misc.merge_dicts(self.ngrams_freq_files),
                              wordless_misc.merge_dicts(self.ngrams_stats_files),
                              self.ngrams_text)

@wordless_misc.log_timing
def generate_table(main, table):
    def update_gui(ngrams_freq_files, ngrams_stats_files, ngrams_text):
        if ngrams_freq_files:
            table.clear_table()
            
            table.settings = main.settings_custom

            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
            text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

            table.blockSignals(True)
            table.setSortingEnabled(False)
            table.setUpdatesEnabled(False)

            # Insert Columns (Files)
            for i, file in enumerate(files):
                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\nFrequency'),
                                 num = True, pct = True, cumulative = True, breakdown = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\n{text_dispersion}'),
                                 num = True, breakdown = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\n{text_adjusted_freq}'),
                                 num = True, breakdown = True)

            # Insert Columns (Total)
            table.insert_col(table.columnCount() - 1,
                             main.tr('Total\nFrequency'),
                             num = True, pct = True, cumulative = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'Total\n{text_dispersion}'),
                             num = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'Total\n{text_adjusted_freq}'),
                             num = True)

            # Sort by frequency of the first file
            table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\nFrequency')), Qt.DescendingOrder)

            cols_freq = table.find_cols(main.tr('\nFrequency'))
            cols_dispersion = table.find_cols(main.tr(f'\n{text_dispersion}'))
            cols_adjusted_freq = table.find_cols(main.tr(f'\n{text_adjusted_freq}'))
            col_files_found = table.find_col(main.tr('Number of\nFiles Found'))

            len_files = len(files)

            table.setRowCount(len(ngrams_freq_files))

            for i, (ngram, freqs) in enumerate(wordless_sorting.sorted_tokens_freq_files(ngrams_freq_files)):
                stats_files = ngrams_stats_files[ngram]

                # Rank
                table.set_item_num_int(i, 0, -1)

                # N-grams
                table.setItem(i, 1, wordless_table.Wordless_Table_Item(ngrams_text[ngram]))

                table.item(i, 1).text_raw = ngram

                # Frequency
                for j, freq in enumerate(freqs):
                    table.set_item_num_cumulative(i, cols_freq[j], freq)

                for j, (dispersion, adjusted_freq) in enumerate(stats_files):
                    # Dispersion
                    table.set_item_num_float(i, cols_dispersion[j], dispersion)

                    # Adjusted Frequency
                    table.set_item_num_float(i, cols_adjusted_freq[j], adjusted_freq)

                # Number of Files Found
                table.set_item_num_pct(i, col_files_found, len([freq for freq in freqs[:-1] if freq]), len_files)

            table.blockSignals(False)
            table.setSortingEnabled(True)
            table.setUpdatesEnabled(True)

            table.toggle_pct()
            table.toggle_cumulative()
            table.toggle_breakdown()
            table.update_ranks()
            table.update_items_width()

            table.itemChanged.emit(table.item(0, 0))

            wordless_msg.wordless_msg_generate_table_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_table_error(main)

        dialog_progress.accept()

    settings = main.settings_custom['ngrams']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['search_settings'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']):
            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

            worker_ngrams_table = Wordless_Worker_Ngrams_Table(main, dialog_progress, update_gui)
            thread_ngrams_table = wordless_threading.Wordless_Thread(worker_ngrams_table)

            thread_ngrams_table.start()

            dialog_progress.exec_()

            thread_ngrams_table.quit()
            thread_ngrams_table.wait()
        else:
            wordless_msg_box.wordless_msg_box_missing_search_term_optional(main)

            wordless_msg.wordless_msg_generate_table_error(main)
    else:
        wordless_msg.wordless_msg_generate_table_error(main)

@wordless_misc.log_timing
def generate_fig(main):
    def update_gui(ngrams_freq_files, ngrams_stats_files, ngrams_text):
        if ngrams_freq_files:
            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
            text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']
            
            if settings['fig_settings']['use_data'] == main.tr('Frequency'):
                ngrams_freq_files = {ngrams_text[ngram]: freqs
                                     for ngram, freqs in ngrams_freq_files.items()}

                wordless_fig_freq.wordless_fig_freq(main, ngrams_freq_files,
                                                          settings = settings['fig_settings'],
                                                          label_x = main.tr('N-grams'))
            else:
                ngrams_stats_files = {ngrams_text[ngram]: stats
                                      for ngram, stats in ngrams_stats_files.items()}

                if settings['fig_settings']['use_data'] == text_dispersion:
                    ngrams_stat_files = {ngram: numpy.array(stats_files)[:, 0]
                                         for ngram, stats_files in ngrams_stats_files.items()}

                    label_y = text_dispersion
                elif settings['fig_settings']['use_data'] == text_adjusted_freq:
                    ngrams_stat_files = {ngram: numpy.array(stats_files)[:, 1]
                                         for ngram, stats_files in ngrams_stats_files.items()}

                    label_y = text_adjusted_freq

                wordless_fig_stat.wordless_fig_stat(main, ngrams_stat_files,
                                                          settings = settings['fig_settings'],
                                                          label_x = main.tr('N-grams'),
                                                          label_y = label_y)

            wordless_msg.wordless_msg_generate_fig_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_fig_error(main)

        dialog_progress.accept()

        if ngrams_freq_files:
            wordless_fig.show_fig()

    settings = main.settings_custom['ngrams']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['search_settings'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']):
            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

            worker_ngrams_fig = Wordless_Worker_Ngrams_Fig(main, dialog_progress, update_gui)
            thread_ngrams_fig = wordless_threading.Wordless_Thread(worker_ngrams_fig)

            thread_ngrams_fig.start()

            dialog_progress.exec_()

            thread_ngrams_fig.quit()
            thread_ngrams_fig.wait()
        else:
            wordless_msg_box.wordless_msg_box_missing_search_term_optional(main)

            wordless_msg.wordless_msg_generate_fig_error(main)
    else:
        wordless_msg.wordless_msg_generate_fig_error(main)
