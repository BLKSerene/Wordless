#
# Wordless: Collocation
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
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy

from wordless_checking import *
from wordless_measures import *
from wordless_plot import *
from wordless_text import *
from wordless_utils import *
from wordless_widgets import *

class Wordless_Table_Collocation(wordless_table.Wordless_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(parent,
                         headers = [
                             parent.tr('Rank'),
                             parent.tr('Nodes'),
                             parent.tr('Collocates'),
                             parent.tr('Number of\nFiles Found'),
                         ],
                         headers_num = [
                             parent.tr('Rank'),
                             parent.tr('Number of\nFiles Found'),
                         ],
                         headers_pct = [
                             parent.tr('Number of\nFiles Found')
                         ],
                         sorting_enabled = True)
        dialog_filter_results = wordless_dialog.Wordless_Dialog_Filter_Results_Collocation(self.main,
                                                                                           tab = 'collocation',
                                                                                           table = self)
        dialog_search_results = wordless_dialog.Wordless_Dialog_Search_Results(self.main,
                                                                               tab = 'collocation',
                                                                               table = self)

        self.button_filter_results.clicked.connect(dialog_filter_results.load)
        self.button_search_results.clicked.connect(dialog_search_results.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    def toggle_breakdown(self):
        settings = self.main.settings_custom['collocation']['table_settings']

        self.setUpdatesEnabled(False)

        for col in self.cols_breakdown | self.cols_breakdown_position:
            if col in self.cols_breakdown and col in self.cols_breakdown_position:
                if settings['show_breakdown_file'] and settings['show_breakdown_position']:
                    self.showColumn(col)
                else:
                    self.hideColumn(col)
            elif col in self.cols_breakdown:
                if settings['show_breakdown_file']:
                    self.showColumn(col)
                else:
                    self.hideColumn(col)
            elif col in self.cols_breakdown_position:
                if settings['show_breakdown_position']:
                    self.showColumn(col)
                else:
                    self.hideColumn(col)

        self.setUpdatesEnabled(True)

    def clear_table(self, count = 1):
        super().clear_table(count)

        self.cols_breakdown_position = set()

class Wrapper_Collocation(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_collocation = Wordless_Table_Collocation(self)

        layout_results = QGridLayout()
        layout_results.addWidget(self.table_collocation.label_number_results, 0, 0)
        layout_results.addWidget(self.table_collocation.button_filter_results, 0, 2)
        layout_results.addWidget(self.table_collocation.button_search_results, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_collocation, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_collocation.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_collocation.button_generate_plot, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_collocation.button_export_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_collocation.button_export_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_collocation.button_clear, 2, 4)

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

         self.token_stacked_ignore_tags,
         self.token_stacked_ignore_tags_type,
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

        self.token_stacked_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.token_stacked_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.token_stacked_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.token_stacked_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.token_stacked_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.token_stacked_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.token_label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        self.group_box_token_settings.setLayout(QGridLayout())
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
         self.line_edit_search_term,
         self.list_search_terms,
         self.label_separator,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_word,
         self.checkbox_use_regex,

         self.search_stacked_widget_ignore_tags,
         self.search_stacked_widget_ignore_tags_type,
         self.search_label_ignore_tags,
         self.checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self,
                                                                                       tab = 'collocation')

        (self.label_context_settings,
         self.button_context_settings) = wordless_widgets.wordless_widgets_context_settings(self,
                                                                                            tab = 'collocation')

        self.group_box_search_settings.setCheckable(True)

        self.group_box_search_settings.toggled.connect(self.search_settings_changed)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_collocation.button_generate_table.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_word.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.search_settings_changed)
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.search_settings_changed)
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        layout_search_terms = QGridLayout()
        layout_search_terms.addWidget(self.list_search_terms, 0, 0, 5, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_add, 0, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_remove, 1, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_clear, 2, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_import, 3, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_export, 4, 1)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.search_label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        layout_context_settings = QGridLayout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(QGridLayout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.line_edit_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_separator, 3, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_ignore_case, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_word, 6, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 7, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 9, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 11, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        self.label_window = QLabel(self.tr('Collocational Window:'), self)
        (self.checkbox_window_sync,
         self.label_window_left,
         self.spin_box_window_left,
         self.label_window_right,
         self.spin_box_window_right) = wordless_widgets.wordless_widgets_window(self)

        (self.label_test_significance,
         self.combo_box_test_significance) = wordless_widgets.wordless_widgets_test_significance(self)
        (self.label_measure_effect_size,
         self.combo_box_measure_effect_size) = wordless_widgets.wordless_widgets_measure_effect_size(self)

        (self.label_settings_measures,
         self.button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(self,
                                                                                              tab = self.tr('Statistical Significance'))

        self.combo_box_test_significance.addItems(list(self.main.settings_global['tests_significance']['collocation'].keys()))
        self.combo_box_measure_effect_size.addItems(list(self.main.settings_global['measures_effect_size']['collocation'].keys()))

        self.checkbox_window_sync.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_window_left.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_window_right.valueChanged.connect(self.generation_settings_changed)

        self.combo_box_test_significance.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_effect_size.currentTextChanged.connect(self.generation_settings_changed)

        layout_settings_measures = QGridLayout()
        layout_settings_measures.addWidget(self.label_settings_measures, 0, 0)
        layout_settings_measures.addWidget(self.button_settings_measures, 0, 1)

        layout_settings_measures.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(QGridLayout())
        self.group_box_generation_settings.layout().addWidget(self.label_window, 0, 0, 1, 3)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_window_sync, 0, 3, Qt.AlignRight)
        self.group_box_generation_settings.layout().addWidget(self.label_window_left, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_window_left, 1, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_window_right, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_window_right, 1, 3)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 2, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(self.label_test_significance, 3, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_test_significance, 4, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_effect_size, 5, 0, 1, 4)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_effect_size, 6, 0, 1, 4)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 7, 0, 1, 4)

        self.group_box_generation_settings.layout().addLayout(layout_settings_measures, 8, 0, 1, 4)

        self.group_box_generation_settings.layout().setColumnStretch(1, 1)
        self.group_box_generation_settings.layout().setColumnStretch(3, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (self.checkbox_show_pct,
         self.checkbox_show_cumulative,
         self.checkbox_show_breakdown_file) = wordless_widgets.wordless_widgets_table_settings(self,
                                                                                               table = self.table_collocation)

        self.checkbox_show_breakdown_file.setText(self.tr('Show Breakdown by File'))
        self.checkbox_show_breakdown_position = QCheckBox(self.tr('Show Breakdown by Span Position'), self)

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_position.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_position.stateChanged.connect(self.table_collocation.toggle_breakdown)
        self.checkbox_show_breakdown_file.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_file.stateChanged.connect(self.table_collocation.toggle_breakdown)

        self.group_box_table_settings.setLayout(QGridLayout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_position, 2, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_file, 3, 0)

        # Plot Settings
        self.group_box_plot_settings = QGroupBox(self.tr('Plot Settings'), self)

        (self.label_plot_type,
         self.combo_box_plot_type,
         self.label_use_file,
         self.combo_box_use_file,
         self.label_use_data,
         self.combo_box_use_data,

         self.checkbox_use_pct,
         self.checkbox_use_cumulative) = wordless_widgets.wordless_widgets_plot_settings(self)

        self.label_rank = QLabel(self.tr('Rank:'), self)
        (self.label_rank_min,
         self.spin_box_rank_min,
         self.checkbox_rank_min_no_limit,
         self.label_rank_max,
         self.spin_box_rank_max,
         self.checkbox_rank_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 1,
                                                                                     filter_max = 100000)

        self.combo_box_plot_type.currentTextChanged.connect(self.plot_settings_changed)
        self.combo_box_use_file.currentTextChanged.connect(self.plot_settings_changed)
        self.combo_box_use_data.currentTextChanged.connect(self.plot_settings_changed)
        self.checkbox_use_pct.stateChanged.connect(self.plot_settings_changed)
        self.checkbox_use_cumulative.stateChanged.connect(self.plot_settings_changed)

        self.spin_box_rank_min.valueChanged.connect(self.plot_settings_changed)
        self.checkbox_rank_min_no_limit.stateChanged.connect(self.plot_settings_changed)
        self.spin_box_rank_max.valueChanged.connect(self.plot_settings_changed)
        self.checkbox_rank_max_no_limit.stateChanged.connect(self.plot_settings_changed)

        layout_plot_settings_combo_boxes = QGridLayout()
        layout_plot_settings_combo_boxes.addWidget(self.label_plot_type, 0, 0)
        layout_plot_settings_combo_boxes.addWidget(self.combo_box_plot_type, 0, 1)
        layout_plot_settings_combo_boxes.addWidget(self.label_use_file, 1, 0)
        layout_plot_settings_combo_boxes.addWidget(self.combo_box_use_file, 1, 1)
        layout_plot_settings_combo_boxes.addWidget(self.label_use_data, 2, 0)
        layout_plot_settings_combo_boxes.addWidget(self.combo_box_use_data, 2, 1)

        layout_plot_settings_combo_boxes.setColumnStretch(1, 1)

        self.group_box_plot_settings.setLayout(QGridLayout())
        self.group_box_plot_settings.layout().addLayout(layout_plot_settings_combo_boxes, 0, 0, 1, 3)
        self.group_box_plot_settings.layout().addWidget(self.checkbox_use_pct, 1, 0, 1, 3)
        self.group_box_plot_settings.layout().addWidget(self.checkbox_use_cumulative, 2, 0, 1, 3)
        
        self.group_box_plot_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 3)

        self.group_box_plot_settings.layout().addWidget(self.label_rank, 4, 0, 1, 3)
        self.group_box_plot_settings.layout().addWidget(self.label_rank_min, 5, 0)
        self.group_box_plot_settings.layout().addWidget(self.spin_box_rank_min, 5, 1)
        self.group_box_plot_settings.layout().addWidget(self.checkbox_rank_min_no_limit, 5, 2)
        self.group_box_plot_settings.layout().addWidget(self.label_rank_max, 6, 0)
        self.group_box_plot_settings.layout().addWidget(self.spin_box_rank_max, 6, 1)
        self.group_box_plot_settings.layout().addWidget(self.checkbox_rank_max_no_limit, 6, 2)

        self.group_box_plot_settings.layout().setColumnStretch(1, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_plot_settings, 4, 0)

        self.wrapper_settings.layout().setRowStretch(5, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['collocation'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['collocation'])

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

        self.token_stacked_ignore_tags.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.token_stacked_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.token_stacked_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.token_stacked_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.group_box_search_settings.setChecked(settings['search_settings']['search_settings'])

        self.checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])
        
        if not defaults:
            self.line_edit_search_term.setText(settings['search_settings']['search_term'])
            self.list_search_terms.load_items(settings['search_settings']['search_terms'])

        self.checkbox_ignore_case.setChecked(settings['search_settings']['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        self.checkbox_match_whole_word.setChecked(settings['search_settings']['match_whole_word'])
        self.checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])

        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['search_settings']['ignore_tags'])
        self.search_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['search_settings']['ignore_tags_tags'])
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['search_settings']['ignore_tags_type'])
        self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['search_settings']['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        # Context Settings
        if defaults:
            self.main.wordless_context_settings_collocation.load_settings(defaults = True)

        # Generation Settings
        self.checkbox_window_sync.setChecked(settings['generation_settings']['window_sync'])

        if settings['generation_settings']['window_left'] < 0:
            self.spin_box_window_left.setPrefix('L')
            self.spin_box_window_left.setValue(-settings['generation_settings']['window_left'])
        else:
            self.spin_box_window_left.setPrefix('R')
            self.spin_box_window_left.setValue(settings['generation_settings']['window_left'])

        if settings['generation_settings']['window_right'] < 0:
            self.spin_box_window_right.setPrefix('L')
            self.spin_box_window_right.setValue(-settings['generation_settings']['window_right'])
        else:
            self.spin_box_window_right.setPrefix('R')
            self.spin_box_window_right.setValue(settings['generation_settings']['window_right'])

        self.combo_box_test_significance.setCurrentText(settings['generation_settings']['test_significance'])
        self.combo_box_measure_effect_size.setCurrentText(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown_position.setChecked(settings['table_settings']['show_breakdown_position'])
        self.checkbox_show_breakdown_file.setChecked(settings['table_settings']['show_breakdown_file'])

        # Plot Settings
        self.combo_box_plot_type.setCurrentText(settings['plot_settings']['plot_type'])
        self.combo_box_use_file.setCurrentText(settings['plot_settings']['use_file'])
        self.combo_box_use_data.setCurrentText(settings['plot_settings']['use_data'])
        self.checkbox_use_pct.setChecked(settings['plot_settings']['use_pct'])
        self.checkbox_use_cumulative.setChecked(settings['plot_settings']['use_cumulative'])

        self.spin_box_rank_min.setValue(settings['plot_settings']['rank_min'])
        self.checkbox_rank_min_no_limit.setChecked(settings['plot_settings']['rank_min_no_limit'])
        self.spin_box_rank_max.setValue(settings['plot_settings']['rank_max'])
        self.checkbox_rank_max_no_limit.setChecked(settings['plot_settings']['rank_max_no_limit'])

        self.token_settings_changed()
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.plot_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['collocation']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['lowercase'] = self.checkbox_lowercase.isChecked()
        settings['uppercase'] = self.checkbox_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_lowercase'] = self.checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.token_stacked_ignore_tags.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.token_stacked_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.token_stacked_ignore_tags_type.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.token_stacked_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        self.checkbox_match_tags.token_settings_changed()
        self.main.wordless_context_settings_collocation.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['collocation']['search_settings']

        settings['search_settings'] = self.group_box_search_settings.isChecked()

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.get_items()

        settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = self.checkbox_match_whole_word.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()

        settings['ignore_tags'] = self.search_stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.search_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.search_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

        if settings['search_settings']:
            self.checkbox_match_tags.token_settings_changed()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['collocation']['generation_settings']

        settings['window_sync'] = self.checkbox_window_sync.isChecked()

        if self.spin_box_window_left.prefix() == 'L':
            settings['window_left'] = - self.spin_box_window_left.value()
        else:
            settings['window_left'] = self.spin_box_window_left.value()

        if self.spin_box_window_right.prefix() == 'L':
            settings['window_right'] = - self.spin_box_window_right.value()
        else:
            settings['window_right'] = self.spin_box_window_right.value()

        settings['test_significance'] = self.combo_box_test_significance.currentText()
        settings['measure_effect_size'] = self.combo_box_measure_effect_size.currentText()

        # Use Data
        use_data_old = self.main.settings_custom['collocation']['plot_settings']['use_data']

        text_test_significance = settings['test_significance']
        text_measure_effect_size = settings['measure_effect_size']

        self.combo_box_use_data.clear()

        for i in range(settings['window_left'], settings['window_right'] + 1):
            if i < 0:
                self.combo_box_use_data.addItem(f'L{-i}')
            elif i > 0:
                self.combo_box_use_data.addItem(f'R{i}')

        self.combo_box_use_data.addItem(self.tr('Frequency'))
        self.combo_box_use_data.addItems([col
                                          for col in self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
                                          if col])
        self.combo_box_use_data.addItem(self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col'])

        if self.combo_box_use_data.findText(use_data_old) > -1:
            self.combo_box_use_data.setCurrentText(use_data_old)
        else:
            self.combo_box_use_data.setCurrentText(self.main.settings_default['collocation']['plot_settings']['use_data'])

    def table_settings_changed(self):
        settings = self.main.settings_custom['collocation']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown_position'] = self.checkbox_show_breakdown_position.isChecked()
        settings['show_breakdown_file'] = self.checkbox_show_breakdown_file.isChecked()

    def plot_settings_changed(self):
        settings = self.main.settings_custom['collocation']['plot_settings']

        settings['plot_type'] = self.combo_box_plot_type.currentText()
        settings['use_file'] = self.combo_box_use_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

def generate_collocates(main, files):
    texts = []
    ngrams_freq_files = []
    collocates_freqs_files = []
    collocates_stats_files = []
    nodes_text = {}

    settings = main.settings_custom['collocation']

    if settings['generation_settings']['window_left'] < 0 and settings['generation_settings']['window_right'] > 0:
        window_size_left = abs(settings['generation_settings']['window_left'])
        window_size_right = abs(settings['generation_settings']['window_right'])
    elif settings['generation_settings']['window_left'] > 0 and settings['generation_settings']['window_right'] > 0:
        window_size_left = 0
        window_size_right = settings['generation_settings']['window_right'] - settings['generation_settings']['window_left'] + 1
    elif settings['generation_settings']['window_left'] < 0 and settings['generation_settings']['window_right'] < 0:
        window_size_left = settings['generation_settings']['window_right'] - settings['generation_settings']['window_left'] + 1
        window_size_right = 0

    window_size = window_size_left + window_size_right

    # Frequency
    for i, file in enumerate(files):
        collocates_freqs_file = {}

        text = wordless_text.Wordless_Text(main, file)

        tokens = wordless_token_processing.wordless_process_tokens_ngrams(text,
                                                                          token_settings = settings['token_settings'])

        search_terms = wordless_matching.match_search_terms(main, tokens,
                                                            lang = text.lang,
                                                            text_type = text.text_type,
                                                            token_settings = settings['token_settings'],
                                                            search_settings = settings['search_settings'])

        (search_terms_inclusion,
         search_terms_exclusion) = wordless_matching.match_search_terms_context(main, tokens,
                                                                                lang = text.lang,
                                                                                text_type = text.text_type,
                                                                                token_settings = settings['token_settings'],
                                                                                context_settings = settings['context_settings'])

        if search_terms:
            len_search_term_min = min([len(search_term) for search_term in search_terms])
            len_search_term_max = max([len(search_term) for search_term in search_terms])
        else:
            len_search_term_min = 1
            len_search_term_max = 1

        for ngram_size in range(len_search_term_min, len_search_term_max + 1):
            for i, ngram in enumerate(nltk.ngrams(tokens, ngram_size)):
                for j, collocate in enumerate(reversed(tokens[max(0, i - window_size_left) : i])):
                    if wordless_matching.check_context(i, tokens,
                                                       context_settings = settings['context_settings'],
                                                       search_terms_inclusion = search_terms_inclusion,
                                                       search_terms_exclusion = search_terms_exclusion):
                        if (ngram, collocate) not in collocates_freqs_file:
                            collocates_freqs_file[(ngram, collocate)] = [0] * window_size

                        collocates_freqs_file[(ngram, collocate)][window_size_left - 1 - j] += 1

                for j, collocate in enumerate(tokens[i + ngram_size: i + ngram_size + window_size_right]):
                    if wordless_matching.check_context(i, tokens,
                                                       context_settings = settings['context_settings'],
                                                       search_terms_inclusion = search_terms_inclusion,
                                                       search_terms_exclusion = search_terms_exclusion):
                        if (ngram, collocate) not in collocates_freqs_file:
                            collocates_freqs_file[(ngram, collocate)] = [0] * window_size

                        collocates_freqs_file[(ngram, collocate)][window_size_left + j] += 1

        collocates_freqs_file = {(ngram, collocate): freqs
                                 for (ngram, collocate), freqs in collocates_freqs_file.items()
                                 if all(ngram) and collocate}

        # Filter search terms
        if settings['search_settings']['search_settings']:
            collocates_freqs_file_filtered = {}

            for search_term in search_terms:
                len_search_term = len(search_term)

                for (node, collocate), freqs in collocates_freqs_file.items():
                    for ngram in nltk.ngrams(node, len_search_term):
                        if ngram == search_term:
                            collocates_freqs_file_filtered[(node, collocate)] = freqs

            collocates_freqs_files.append(collocates_freqs_file_filtered)
        else:
            collocates_freqs_files.append(collocates_freqs_file)

        # Frequency (N-grams)
        for i in {1} | set(range(len_search_term_min, len_search_term_max + 1)):
            ngrams = [ngram
                      for ngram in nltk.ngrams(tokens, i)
                      if all(ngram)]

            ngrams_freq_files.append(collections.Counter(ngrams))

        # Nodes Text
        for (node, collocate) in collocates_freqs_file:
            nodes_text[node] = wordless_text_processing.wordless_word_detokenize(main, node, text.lang)

        texts.append(text)

    # Total
    if len(files) > 1:
        collocates_freqs_total = {}

        text_total = wordless_text.Wordless_Text_Blank()
        text_total.tokens = [token for text in texts for token in text.tokens]

        texts.append(text_total)
        ngrams_freq_files.append(sum(ngrams_freq_files, collections.Counter()))

        for collocates_freqs_file in collocates_freqs_files:
            for collocate, freqs in collocates_freqs_file.items():
                if collocate not in collocates_freqs_total:
                    collocates_freqs_total[collocate] = numpy.array(freqs)
                else:
                    collocates_freqs_total[collocate] += numpy.array(freqs)

        collocates_freqs_files.append(collocates_freqs_total)

    # Statistiscal Significance & Effect Size
    text_test_significance = settings['generation_settings']['test_significance']
    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

    test_significance = main.settings_global['tests_significance']['collocation'][text_test_significance]['func']
    measure_effect_size = main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['func']

    collocates_total = collocates_freqs_files[-1].keys()

    for text, ngrams_freq_file, collocates_freqs_file in zip(texts,
                                                             ngrams_freq_files,
                                                             collocates_freqs_files):
        collocates_stats_file = {}

        len_tokens = len(text.tokens)

        for node, collocate in collocates_total:
            len_node = len(node)

            if (node, collocate) in collocates_freqs_file:
                c11 = sum(collocates_freqs_file[(node, collocate)])
            else:
                c11 = 0

            c12 = max(0, ngrams_freq_file[node] - c11)
            c21 = max(0, ngrams_freq_file[(collocate,)] - c11)
            c22 = len_tokens - c11 - c12 - c21

            collocates_stats_file[(node, collocate)] = test_significance(main, c11, c12, c21, c22)
            collocates_stats_file[(node, collocate)].append(measure_effect_size(main, c11, c12, c21, c22))

        collocates_stats_files.append(collocates_stats_file)

    if len(files) == 1:
        collocates_freqs_files *= 2
        collocates_stats_files *= 2

    return (wordless_misc.merge_dicts(collocates_freqs_files),
            wordless_misc.merge_dicts(collocates_stats_files),
            nodes_text)

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['collocation']

    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['search_settings'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            collocates_freqs_files, collocates_stats_files, nodes_text = generate_collocates(main, files)

            if collocates_freqs_files:
                table.clear_table()

                table.settings = main.settings_custom

                text_test_significance = settings['generation_settings']['test_significance']
                text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                (text_test_stat,
                 text_p_value,
                 text_bayes_factor) = main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
                text_effect_size =  main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

                # Insert columns (Files)
                for i, file in enumerate(files):
                    for i in range(settings['generation_settings']['window_left'],
                                   settings['generation_settings']['window_right'] + 1):
                        if i < 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}]\nL{-i}'),
                                             num = True, pct = True, cumulative = True, breakdown = True)
                        elif i > 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}]\nR{i}'),
                                             num = True, pct = True, cumulative = True, breakdown = True)

                        table.cols_breakdown_position.add(table.columnCount() - 2)

                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\nFrequency'),
                                     num = True, pct = True, cumulative = True, breakdown = True)

                    if text_test_stat:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\n{text_test_stat}'),
                                         num = True, breakdown = True)

                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\n{text_p_value}'),
                                     num = True, breakdown = True)

                    if text_bayes_factor:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\n{text_bayes_factor}'),
                                         num = True, breakdown = True)

                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\n{text_effect_size}'),
                                     num = True, breakdown = True)

                # Insert columns (Total)
                for i in range(settings['generation_settings']['window_left'],
                               settings['generation_settings']['window_right'] + 1):
                    if i < 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total\nL{-i}'),
                                         num = True, pct = True, cumulative = True)
                    elif i > 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total\nR{i}'),
                                         num = True, pct = True, cumulative = True)

                    table.cols_breakdown_position.add(table.columnCount() - 2)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\nFrequency'),
                                 num = True, pct = True, cumulative = True)

                if text_test_stat:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total\n{text_test_stat}'),
                                     num = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\n{text_p_value}'),
                                 num = True)

                if text_bayes_factor:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total\n{text_bayes_factor}'),
                                     num = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\n{text_effect_size}'),
                                 num = True)

                # Sort by p-value of the first file
                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\n{text_p_value}')), Qt.AscendingOrder)

                if settings['generation_settings']['window_left'] < 0:  
                    cols_freqs_start = [table.find_col(f'[{file["name"]}]\nL{-settings["generation_settings"]["window_left"]}')
                                        for file in files]
                    cols_freqs_start.append(table.find_col(f'Total\nL{-settings["generation_settings"]["window_left"]}'))
                else:
                    cols_freqs_start = [table.find_col(f'[{file["name"]}]\nR{settings["generation_settings"]["window_left"]}')
                                        for file in files]
                    cols_freqs_start.append(table.find_col(f'Total\nR{settings["generation_settings"]["window_left"]}'))

                cols_freq = table.find_cols(main.tr('\nFrequency'))

                if text_test_stat:
                    cols_test_stat = table.find_cols(main.tr(f'\n{text_test_stat}'))

                cols_p_value = table.find_cols(main.tr('\np-value'))

                if text_bayes_factor:
                    cols_bayes_factor = table.find_cols(main.tr('\nBayes Factor'))

                cols_effect_size = table.find_cols(f'\n{text_effect_size}')
                col_number_files_found = table.find_col(main.tr('Number of\nFiles Found'))

                len_files = len(files)

                table.setRowCount(len(collocates_freqs_files))

                for i, ((node, collocate), stats_files) in enumerate(wordless_sorting.sorted_collocates_stats_files(collocates_stats_files)):
                    freqs_files = collocates_freqs_files[(node, collocate)]

                    # Rank
                    table.set_item_num_int(i, 0, -1)

                    # Nodes
                    table.setItem(i, 1, wordless_table.Wordless_Table_Item(nodes_text[node]))
                    # Collocates
                    table.setItem(i, 2, wordless_table.Wordless_Table_Item(collocate))

                    # Frequency
                    for j, freqs_file in enumerate(freqs_files):
                        for k, freq in enumerate(freqs_file):
                            table.set_item_num_cumulative(i, cols_freqs_start[j] + k, freq)

                        table.set_item_num_cumulative(i, cols_freq[j], sum(freqs_file))

                    for j, (test_stat, p_value, bayes_factor, effect_size) in enumerate(stats_files):
                        # Test Statistic
                        if text_test_stat:
                            table.set_item_num_float(i, cols_test_stat[j], test_stat)

                        # p-value
                        table.set_item_num_float(i, cols_p_value[j], p_value)

                        # Bayes Factor
                        if text_bayes_factor:
                            table.set_item_num_float(i, cols_bayes_factor[j], bayes_factor)

                        # Effect Size
                        table.set_item_num_float(i, cols_effect_size[j], effect_size)

                    # Files Found
                    table.set_item_num_pct(i, col_number_files_found,
                                           len([freqs_file for freqs_file in freqs_files[:-1] if sum(freqs_file)]),
                                           len_files)

                table.blockSignals(False)
                table.setSortingEnabled(True)
                table.setUpdatesEnabled(True)

                table.toggle_pct()
                table.toggle_cumulative()
                table.toggle_breakdown()
                table.update_ranks()

                table.update_items_width()

                table.itemChanged.emit(table.item(0, 0))

                wordless_message.wordless_message_generate_table_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_table(main)

                wordless_message.wordless_message_generate_table_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term_optional(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['collocation']

    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (settings['search_settings']['search_settings'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            collocates_freqs_files, collocates_stats_files, nodes_text = generate_collocates(main, files)

            if collocates_freqs_files:
                text_test_significance = settings['generation_settings']['test_significance']
                text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                (text_test_stat,
                 text_p_value,
                 text_bayes_factor) = main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
                text_effect_size =  main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

                if re.search(r'^[LR][0-9]+$', settings['plot_settings']['use_data']):
                    span_positions = (list(range(settings['generation_settings']['window_left'], 0)) +
                                      list(range(1, settings['generation_settings']['window_right'] + 1)))

                    if 'L' in settings['plot_settings']['use_data']:
                        span_position = span_positions.index(-int(settings['plot_settings']['use_data'][1:]))
                    else:
                        span_position = span_positions.index(int(settings['plot_settings']['use_data'][1:]))

                    collocates_freq_files = {', '.join([nodes_text[node], collocate]): numpy.array(freqs)[:, span_position]
                                             for (node, collocate), freqs in collocates_freqs_files.items()}

                    wordless_plot_freq.wordless_plot_freq(main, collocates_freq_files,
                                                          settings = settings['plot_settings'],
                                                          label_x = main.tr('Collocates'))
                elif settings['plot_settings']['use_data'] == main.tr('Frequency'):
                    collocates_freq_files = {', '.join([nodes_text[node], collocate]): numpy.array(freqs).sum(axis = 1)
                                             for (node, collocate), freqs in collocates_freqs_files.items()}

                    wordless_plot_freq.wordless_plot_freq(main, collocates_freq_files,
                                                          settings = settings['plot_settings'],
                                                          label_x = main.tr('Collocates'))
                else:
                    collocates_stats_files = {', '.join([nodes_text[node], collocate]): freqs
                                              for (node, collocate), freqs in collocates_stats_files.items()}

                    if settings['plot_settings']['use_data'] == text_test_stat:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 0]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = text_test_stat
                    elif settings['plot_settings']['use_data'] == text_p_value:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 1]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = text_p_value
                    elif settings['plot_settings']['use_data'] == text_bayes_factor:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 2]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = text_bayes_factor
                    elif settings['plot_settings']['use_data'] == text_effect_size:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 3]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = text_effect_size

                    wordless_plot_stat.wordless_plot_stat(main, collocates_stat_files,
                                                          settings = settings['plot_settings'],
                                                          label_x = main.tr('Collocates'),
                                                          label_y = label_y)

                wordless_message.wordless_message_generate_plot_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_plot(main)

                wordless_message.wordless_message_generate_plot_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term_optional(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message.wordless_message_generate_plot_error(main)
