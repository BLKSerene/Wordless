#
# Wordless: Keywords
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy

from wordless_checking import *
from wordless_measures import *
from wordless_plot import *
from wordless_text import *
from wordless_utils import *
from wordless_widgets import *

class Wordless_Table_Keywords(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, parent):
        super().__init__(parent,
                         headers = [
                             parent.tr('Rank'),
                             parent.tr('Keywords'),
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

        dialog_search = wordless_dialog.Wordless_Dialog_Search(self.main,
                                                               tab = 'keywords',
                                                               table = self,
                                                               cols_search = [
                                                                   self.tr('Keywords')
                                                               ])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['keywords']['filter_settings']

            text_test_significance = self.settings['keywords']['generation_settings']['test_significance']
            text_measure_effect_size = self.settings['keywords']['generation_settings']['measure_effect_size']

            (text_test_stat,
             text_p_value,
             text_bayes_factor) = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
            text_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

            if settings['filter_file'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total\nFrequency'))
                col_test_stat = self.find_col(self.tr(f'Total\n{text_test_stat}'))
                col_p_value = self.find_col(self.tr(f'Total\n{text_p_value}'))
                col_bayes_factor = self.find_col(self.tr(f'Total\n{text_bayes_factor}'))
                col_effect_size = self.find_col(self.tr(f'Total\n{text_effect_size}'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["filter_file"]}]\nFrequency'))
                col_test_stat = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{text_test_stat}'))
                col_p_value = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{text_p_value}'))
                col_bayes_factor = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{text_bayes_factor}'))
                col_effect_size = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{text_effect_size}'))

            col_keywords = self.find_col('Keywords')
            col_number_files_found = self.find_col('Number of\nFiles Found')

            freq_min = (float('-inf')
                        if settings['freq_min_no_limit'] else settings['freq_min'])
            freq_max = (float('inf')
                        if settings['freq_max_no_limit'] else settings['freq_max'])

            test_stat_min = (float('-inf')
                             if settings['test_stat_min_no_limit'] else settings['test_stat_min'])
            test_stat_max = (float('inf')
                             if settings['test_stat_max_no_limit'] else settings['test_stat_max'])

            p_value_min = (float('-inf')
                           if settings['p_value_min_no_limit'] else settings['p_value_min'])
            p_value_max = (float('inf')
                           if settings['p_value_max_no_limit'] else settings['p_value_max'])

            bayes_factor_min = (float('-inf')
                                if settings['bayes_factor_min_no_limit'] else settings['bayes_factor_min'])
            bayes_factor_max = (float('inf')
                                if settings['bayes_factor_max_no_limit'] else settings['bayes_factor_max'])

            effect_size_min = (float('-inf')
                               if settings['effect_size_min_no_limit'] else settings['effect_size_min'])
            effect_size_max = (float('inf')
                               if settings['effect_size_max_no_limit'] else settings['effect_size_max'])

            len_keyword_min = (float('-inf')
                               if settings['len_keyword_min_no_limit'] else settings['len_keyword_min'])
            len_keyword_max = (float('inf')
                               if settings['len_keyword_max_no_limit'] else settings['len_keyword_max'])

            number_files_found_min = (float('-inf')
                                      if settings['number_files_found_min_no_limit'] else settings['number_files_found_min'])
            number_files_found_max = (float('inf')
                                      if settings['number_files_found_max_no_limit'] else settings['number_files_found_max'])

            self.row_filters = [[] for i in range(self.rowCount())]

            for i in range(self.rowCount()):
                if freq_min <= self.item(i, col_freq).val_raw <= freq_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if text_test_stat:
                    if test_stat_min <= self.item(i, col_test_stat).val <= test_stat_max:
                        self.row_filters[i].append(True)
                    else:
                        self.row_filters[i].append(False)

                if p_value_min <= self.item(i, col_p_value).val <= p_value_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if text_bayes_factor:
                    if bayes_factor_min <= self.item(i, col_bayes_factor).val <= bayes_factor_max:
                        self.row_filters[i].append(True)
                    else:
                        self.row_filters[i].append(False)

                if effect_size_min <= self.item(i, col_effect_size).val <= effect_size_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if len_keyword_min <= len(self.item(i, col_keywords).text()) <= len_keyword_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if number_files_found_min <= self.item(i, col_number_files_found).val <= number_files_found_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

            self.filter_table()

        wordless_message.wordless_message_filter_table_done(self.main)

class Wrapper_Keywords(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_keywords = Wordless_Table_Keywords(self)

        self.wrapper_table.layout().addWidget(self.table_keywords.label_number_results, 0, 0)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_search_results, 0, 4)
        self.wrapper_table.layout().addWidget(self.table_keywords, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_generate_plot, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_export_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_export_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_clear, 2, 4)

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

         self.stacked_widget_ignore_tags,
         self.stacked_widget_ignore_tags_type,
         self.label_ignore_tags,
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

        self.stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

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

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        self.label_ref_file = QLabel(self.tr('Reference File:'), self)
        self.combo_box_ref_file = wordless_box.Wordless_Combo_Box_Ref_File(self)

        (self.label_test_significance,
         self.combo_box_test_significance) = wordless_widgets.wordless_widgets_test_significance(self)
        (self.label_measure_effect_size,
         self.combo_box_measure_effect_size) = wordless_widgets.wordless_widgets_measure_effect_size(self)

        (self.label_settings_measures,
         self.button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(self,
                                                                                              tab = self.tr('Statistical Significance'))

        self.combo_box_test_significance.addItems(list(self.main.settings_global['tests_significance']['keywords'].keys()))
        self.combo_box_measure_effect_size.addItems(list(self.main.settings_global['measures_effect_size']['keywords'].keys()))

        self.combo_box_ref_file.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_test_significance.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_effect_size.currentTextChanged.connect(self.generation_settings_changed)

        layout_settings_measures = QGridLayout()
        layout_settings_measures.addWidget(self.label_settings_measures, 0, 0)
        layout_settings_measures.addWidget(self.button_settings_measures, 0, 1)

        layout_settings_measures.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(QGridLayout())
        self.group_box_generation_settings.layout().addWidget(self.label_ref_file, 0, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_ref_file, 1, 0)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 2, 0)

        self.group_box_generation_settings.layout().addWidget(self.label_test_significance, 3, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_test_significance, 4, 0)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_effect_size, 5, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_effect_size, 6, 0)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 7, 0)

        self.group_box_generation_settings.layout().addLayout(layout_settings_measures, 8, 0)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (self.checkbox_show_pct,
         self.checkbox_show_cumulative,
         self.checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self,
                                                                                          table = self.table_keywords)

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(QGridLayout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

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

        # Filter Settings
        self.group_box_filter_settings = QGroupBox(self.tr('Filter Settings'), self)

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (self.label_freq_min,
         self.spin_box_freq_min,
         self.checkbox_freq_min_no_limit,
         self.label_freq_max,
         self.spin_box_freq_max,
         self.checkbox_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 0,
                                                                                     filter_max = 1000000)

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (self.label_test_stat_min,
         self.spin_box_test_stat_min,
         self.checkbox_test_stat_min_no_limit,
         self.label_test_stat_max,
         self.spin_box_test_stat_max,
         self.checkbox_test_stat_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_p_value = QLabel(self.tr('p-value:'), self)
        (self.label_p_value_min,
         self.spin_box_p_value_min,
         self.checkbox_p_value_min_no_limit,
         self.label_p_value_max,
         self.spin_box_p_value_max,
         self.checkbox_p_value_max_no_limit) = wordless_widgets.wordless_widgets_filter_p_value(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (self.label_bayes_factor_min,
         self.spin_box_bayes_factor_min,
         self.checkbox_bayes_factor_min_no_limit,
         self.label_bayes_factor_max,
         self.spin_box_bayes_factor_max,
         self.checkbox_bayes_factor_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (self.label_effect_size_min,
         self.spin_box_effect_size_min,
         self.checkbox_effect_size_min_no_limit,
         self.label_effect_size_max,
         self.spin_box_effect_size_max,
         self.checkbox_effect_size_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_len_keyword = QLabel(self.tr('Keyword Length:'), self)
        (self.label_len_keyword_min,
         self.spin_box_len_keyword_min,
         self.checkbox_len_keyword_min_no_limit,
         self.label_len_keyword_max,
         self.spin_box_len_keyword_max,
         self.checkbox_len_keyword_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                            filter_min = 1,
                                                                                            filter_max = 100)

        self.label_number_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_number_files_found_min,
         self.spin_box_number_files_found_min,
         self.checkbox_number_files_found_min_no_limit,
         self.label_number_files_found_max,
         self.spin_box_number_files_found_max,
         self.checkbox_number_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                   filter_min = 1,
                                                                                                   filter_max = 100000)

        (self.label_filter_file,
         self.combo_box_filter_file,
         self.button_filter_results) = wordless_widgets.wordless_widgets_filter_results(self,
                                                                                        table = self.table_keywords)

        self.spin_box_freq_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.spin_box_len_keyword_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_len_keyword_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_len_keyword_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_len_keyword_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.spin_box_number_files_found_min.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_number_files_found_min_no_limit.stateChanged.connect(self.filter_settings_changed)
        self.spin_box_number_files_found_max.valueChanged.connect(self.filter_settings_changed)
        self.checkbox_number_files_found_max_no_limit.stateChanged.connect(self.filter_settings_changed)

        self.combo_box_filter_file.currentTextChanged.connect(self.filter_settings_changed)

        self.table_keywords.itemChanged.connect(self.table_item_changed)

        layout_filter_file = QGridLayout()
        layout_filter_file.addWidget(self.label_filter_file, 0, 0)
        layout_filter_file.addWidget(self.combo_box_filter_file, 0, 1)

        layout_filter_file.setColumnStretch(1, 1)

        self.group_box_filter_settings.setLayout(QGridLayout())
        self.group_box_filter_settings.layout().addWidget(self.label_freq, 0, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_freq_min, 1, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_freq_min, 1, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_freq_min_no_limit, 1, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_freq_max, 2, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_freq_max, 2, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_freq_max_no_limit, 2, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 3)

        self.group_box_filter_settings.layout().addWidget(self.label_test_stat, 4, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_test_stat_min, 5, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_test_stat_min, 5, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_test_stat_min_no_limit, 5, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_test_stat_max, 6, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_test_stat_max, 6, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_test_stat_max_no_limit, 6, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 7, 0, 1, 3)

        self.group_box_filter_settings.layout().addWidget(self.label_p_value, 8, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_p_value_min, 9, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_p_value_min, 9, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_p_value_min_no_limit, 9, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_p_value_max, 10, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_p_value_max, 10, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_p_value_max_no_limit, 10, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 11, 0, 1, 3)

        self.group_box_filter_settings.layout().addWidget(self.label_bayes_factor, 12, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_bayes_factor_min, 13, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_bayes_factor_min, 13, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_bayes_factor_min_no_limit, 13, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_bayes_factor_max, 14, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_bayes_factor_max, 14, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_bayes_factor_max_no_limit, 14, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 15, 0, 1, 3)

        self.group_box_filter_settings.layout().addWidget(self.label_effect_size, 16, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_effect_size_min, 17, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_effect_size_min, 17, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_effect_size_min_no_limit, 17, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_effect_size_max, 18, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_effect_size_max, 18, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_effect_size_max_no_limit, 18, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 19, 0, 1, 3)

        self.group_box_filter_settings.layout().addWidget(self.label_len_keyword, 20, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_len_keyword_min, 21, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_len_keyword_min, 21, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_len_keyword_min_no_limit, 21, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_len_keyword_max, 22, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_len_keyword_max, 22, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_len_keyword_max_no_limit, 22, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 23, 0, 1, 3)

        self.group_box_filter_settings.layout().addWidget(self.label_number_files_found, 24, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.label_number_files_found_min, 25, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_number_files_found_min, 25, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_number_files_found_min_no_limit, 25, 2)
        self.group_box_filter_settings.layout().addWidget(self.label_number_files_found_max, 26, 0)
        self.group_box_filter_settings.layout().addWidget(self.spin_box_number_files_found_max, 26, 1)
        self.group_box_filter_settings.layout().addWidget(self.checkbox_number_files_found_max_no_limit, 26, 2)

        self.group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 27, 0, 1, 3)

        self.group_box_filter_settings.layout().addLayout(layout_filter_file, 28, 0, 1, 3)
        self.group_box_filter_settings.layout().addWidget(self.button_filter_results, 29, 0, 1, 3)

        self.group_box_filter_settings.layout().setColumnStretch(1, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_plot_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_filter_settings, 4, 0)

        self.wrapper_settings.layout().setRowStretch(5, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['keywords'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['keywords'])

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

        self.stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Generation Settings
        self.combo_box_ref_file.setCurrentText(settings['generation_settings']['ref_file'])
        self.combo_box_test_significance.setCurrentText(settings['generation_settings']['test_significance'])
        self.combo_box_measure_effect_size.setCurrentText(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

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

        # Filter Settings
        self.spin_box_freq_min.setValue(settings['filter_settings']['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['filter_settings']['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['filter_settings']['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['filter_settings']['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['filter_settings']['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['filter_settings']['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['filter_settings']['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['filter_settings']['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['filter_settings']['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['filter_settings']['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['filter_settings']['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['filter_settings']['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['filter_settings']['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['filter_settings']['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['filter_settings']['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['filter_settings']['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['filter_settings']['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['filter_settings']['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['filter_settings']['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['filter_settings']['effect_size_max_no_limit'])

        self.spin_box_len_keyword_min.setValue(settings['filter_settings']['len_keyword_min'])
        self.checkbox_len_keyword_min_no_limit.setChecked(settings['filter_settings']['len_keyword_min_no_limit'])
        self.spin_box_len_keyword_max.setValue(settings['filter_settings']['len_keyword_max'])
        self.checkbox_len_keyword_max_no_limit.setChecked(settings['filter_settings']['len_keyword_max_no_limit'])

        self.spin_box_number_files_found_min.setValue(settings['filter_settings']['number_files_found_min'])
        self.checkbox_number_files_found_min_no_limit.setChecked(settings['filter_settings']['number_files_found_min_no_limit'])
        self.spin_box_number_files_found_max.setValue(settings['filter_settings']['number_files_found_max'])
        self.checkbox_number_files_found_max_no_limit.setChecked(settings['filter_settings']['number_files_found_max_no_limit'])

        self.combo_box_filter_file.setCurrentText(settings['filter_settings']['filter_file'])

        self.token_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.plot_settings_changed()
        self.filter_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['keywords']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['lowercase'] = self.checkbox_lowercase.isChecked()
        settings['uppercase'] = self.checkbox_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_lowercase'] = self.checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['keywords']['generation_settings']

        if self.combo_box_ref_file.currentText() == self.tr('*** None ***'):
            settings['ref_file'] = ''
        else:
            settings['ref_file'] = self.combo_box_ref_file.currentText()

        settings['test_significance'] = self.combo_box_test_significance.currentText()
        settings['measure_effect_size'] = self.combo_box_measure_effect_size.currentText()

        # Use File
        use_file_old = self.combo_box_use_file.currentText()

        self.combo_box_use_file.wordless_files_changed()

        self.combo_box_use_file.removeItem(self.combo_box_use_file.findText(settings['ref_file']))

        if self.combo_box_use_file.findText(use_file_old) > -1:
            self.combo_box_use_file.setCurrentText(use_file_old)
        else:
            self.combo_box_use_file.setCurrentIndex(0)

        # Use Data
        use_data_old = self.combo_box_use_data.currentText()

        text_test_significance = settings['test_significance']
        text_measure_effect_size = settings['measure_effect_size']

        self.combo_box_use_data.clear()

        self.combo_box_use_data.addItem(self.tr('Frequency'))
        self.combo_box_use_data.addItems([col
                                          for col in self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
                                          if col])
        self.combo_box_use_data.addItem(self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col'])

        if self.combo_box_use_data.findText(use_data_old) > -1:
            self.combo_box_use_data.setCurrentText(use_data_old)
        else:
            self.combo_box_use_data.setCurrentText(self.main.settings_default['keywords']['plot_settings']['use_data'])

    def table_settings_changed(self):
        settings = self.main.settings_custom['keywords']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

    def plot_settings_changed(self):
        settings = self.main.settings_custom['keywords']['plot_settings']

        settings['plot_type'] = self.combo_box_plot_type.currentText()
        settings['use_file'] = self.combo_box_use_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

    def filter_settings_changed(self):
        settings = self.main.settings_custom['keywords']['filter_settings']

        settings['freq_min'] = self.spin_box_freq_min.value()
        settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        settings['freq_max'] = self.spin_box_freq_max.value()
        settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        settings['p_value_min'] = self.spin_box_p_value_min.value()
        settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        settings['p_value_max'] = self.spin_box_p_value_max.value()
        settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        settings['len_keyword_min'] = self.spin_box_len_keyword_min.value()
        settings['len_keyword_min_no_limit'] = self.checkbox_len_keyword_min_no_limit.isChecked()
        settings['len_keyword_max'] = self.spin_box_len_keyword_max.value()
        settings['len_keyword_max_no_limit'] = self.checkbox_len_keyword_max_no_limit.isChecked()

        settings['number_files_found_min'] = self.spin_box_number_files_found_min.value()
        settings['number_files_found_min_no_limit'] = self.checkbox_number_files_found_min_no_limit.isChecked()
        settings['number_files_found_max'] = self.spin_box_number_files_found_max.value()
        settings['number_files_found_max_no_limit'] = self.checkbox_number_files_found_max_no_limit.isChecked()

        settings['filter_file'] = self.combo_box_filter_file.currentText()

    def table_item_changed(self):
        settings = self.table_keywords.settings['keywords']

        ref_file = settings['generation_settings']['ref_file']

        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (text_test_stat,
         text_p_value,
         text_bayes_factor) = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(main.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        if text_bayes_factor:
            if not self.checkbox_bayes_factor_min_no_limit.isChecked():
                self.spin_box_bayes_factor_min.setEnabled(True)
            if not self.checkbox_bayes_factor_max_no_limit.isChecked():
                self.spin_box_bayes_factor_max.setEnabled(True)

            self.checkbox_bayes_factor_min_no_limit.setEnabled(True)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(True)
        else:
            self.spin_box_bayes_factor_min.setEnabled(False)
            self.checkbox_bayes_factor_min_no_limit.setEnabled(False)
            self.spin_box_bayes_factor_max.setEnabled(False)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{col_text_effect_size}:')
        
        self.combo_box_filter_file.removeItem(self.combo_box_filter_file.findText(ref_file))

def generate_keywords(main, files, ref_file):
    texts = []
    keywords_freq_files = []
    keywords_stats_files = []

    settings = main.settings_custom['keywords']

    # Frequency
    for i, file in enumerate([ref_file] + files):
        text = wordless_text.Wordless_Text(main, file)

        tokens = wordless_token_processing.wordless_process_tokens_wordlist(text,
                                                                            token_settings = settings['token_settings'])

        keywords_freq_files.append(collections.Counter(tokens))

        if i > 0:
            texts.append(text)
        else:
            tokens_ref = text.tokens
            len_tokens_ref = len(tokens_ref)

    # Total
    if len(files) > 1:
        text_total = wordless_text.Wordless_Text(main, files[0])
        text_total.tokens = [token for text in texts for token in text.tokens]

        texts.append(text_total)
        keywords_freq_files.append(sum(keywords_freq_files, collections.Counter()))

        keywords_freq_files[0] = {token: freq
                                  for token, freq in keywords_freq_files[0].items()
                                  if token in text_total.tokens}
    else:
        keywords_freq_files[0] = {token: freq
                                  for token, freq in keywords_freq_files[0].items()
                                  if token in keywords_freq_files[1]}

    # Keyness
    text_test_significance = settings['generation_settings']['test_significance']
    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

    test_significance = main.settings_global['tests_significance']['keywords'][text_test_significance]['func']
    measure_effect_size = main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['func']

    keywords_freq_file_observed = keywords_freq_files[-1]
    keywords_freq_file_ref = keywords_freq_files[0]

    for text in texts:
        keywords_stats_file = {}

        tokens_observed = text.tokens
        len_tokens_observed = len(tokens_observed)

        if text_test_significance in [main.tr('Student\'s t-test (Two-sample)'),
                                      main.tr('Mann-Whitney U Test')]:
            # Test Statistic, p-value & Bayes Factor
            if text_test_significance == main.tr('Student\'s t-test (Two-sample)'):
                number_sections = main.settings_custom['measures']['statistical_significance']['students_t_test_two_sample']['number_sections']
                use_data = main.settings_custom['measures']['statistical_significance']['students_t_test_two_sample']['use_data']
            elif text_test_significance == main.tr('Mann-Whitney U Test'):
                number_sections = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['number_sections']
                use_data = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['use_data']

            sections_observed = wordless_text_utils.to_sections(tokens_observed, number_sections)
            sections_ref = wordless_text_utils.to_sections(tokens_ref, number_sections)

            sections_freq_observed = [collections.Counter(section) for section in sections_observed]
            sections_freq_ref = [collections.Counter(section) for section in sections_observed]

            len_sections_observed = [len(section) for section in sections_observed]
            len_sections_ref = [len(section) for section in sections_ref]

            if use_data == main.tr('Absolute Frequency'):
                for token in keywords_freq_file_observed:
                    counts_observed = [section_freq.get(token, 0) for section_freq in sections_freq_observed]
                    counts_ref = [section_freq.get(token, 0) for section_freq in sections_freq_ref]

                    keywords_stats_file[token] = test_significance(main, counts_observed, counts_ref)
            elif use_data == main.tr('Relative Frequency'):
                for token in keywords_freq_file_observed:
                    counts_observed = [section_freq.get(token, 0) / len_sections_observed[i]
                                       for i, section_freq in enumerate(sections_freq_observed)]
                    counts_ref = [section_freq.get(token, 0) / len_sections_ref[i]
                                  for i, section_freq in enumerate(sections_freq_ref)]

                    keywords_stats_file[token] = test_significance(main, counts_observed, counts_ref)

            # Effect Size
            for token in keywords_freq_file_observed:
                c11 = keywords_freq_file_observed.get(token, 0)
                c12 = keywords_freq_file_ref.get(token, 0)
                c21 = len_tokens_observed - c11
                c22 = len_tokens_ref - c12

                keywords_stats_file[token].append(measure_effect_size(main, c11, c12, c21, c22))
        else:
            for token in keywords_freq_file_observed:
                c11 = keywords_freq_file_observed.get(token, 0)
                c12 = keywords_freq_file_ref.get(token, 0)
                c21 = len_tokens_observed - c11
                c22 = len_tokens_ref - c12

                # Test Statistic, p-value & Bayes Factor
                keywords_stats_file[token] = test_significance(main, c11, c12, c21, c22)

                # Effect Size
                keywords_stats_file[token].append(measure_effect_size(main, c11, c12, c21, c22))

        keywords_stats_files.append(keywords_stats_file)

    if len(files) == 1:
        keywords_freq_files.append(keywords_freq_files[1])
        keywords_stats_files *= 2

    return (wordless_misc.merge_dicts(keywords_freq_files),
            wordless_misc.merge_dicts(keywords_stats_files))

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['keywords']

    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if settings['generation_settings']['ref_file']:
            ref_file = main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'],
                                                             selected_only = True)

            files = [file
                     for file in main.wordless_files.get_selected_files()
                     if file != ref_file]

            if files:
                keywords_freq_files, keywords_stats_files = generate_keywords(main, files, ref_file)

                if keywords_freq_files:
                    table.clear_table()

                    table.settings = copy.deepcopy(main.settings_custom)

                    text_test_significance = settings['generation_settings']['test_significance']
                    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                    (text_test_stat,
                     text_p_value,
                     text_bayes_factor) = main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
                    text_effect_size =  main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

                    table.blockSignals(True)
                    table.setSortingEnabled(False)
                    table.setUpdatesEnabled(False)

                    # Insert columns (Files)
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{ref_file["name"]}]\nFrequency'),
                                     num = True, pct = True, cumulative = True)

                    for file in files:
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

                    cols_freq = table.find_cols(main.tr('\nFrequency'))

                    if text_test_stat:
                        cols_test_stat = table.find_cols(main.tr(f'\n{text_test_stat}'))

                    cols_p_value = table.find_cols(main.tr('\np-value'))

                    if text_bayes_factor:
                        cols_bayes_factor = table.find_cols(main.tr('\nBayes Factor'))

                    cols_effect_size = table.find_cols(f'\n{text_effect_size}')
                    col_number_files_found = table.find_col(main.tr('Number of\nFiles Found'))

                    len_files = len(files)

                    table.setRowCount(len(keywords_freq_files))

                    for i, (keyword, stats_files) in enumerate(wordless_sorting.sorted_keywords_stats_files(keywords_stats_files)):
                        keyword_freq_files = keywords_freq_files[keyword]

                        # Rank
                        table.set_item_num_int(i, 0, -1)

                        # Keywords
                        table.setItem(i, 1, wordless_table.Wordless_Table_Item(keyword))

                        # Frequency
                        for j, freq in enumerate(keyword_freq_files):
                            table.set_item_num_cumulative(i, cols_freq[j], freq)

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

                        # Number of Files Found
                        table.set_item_num_pct(i, col_number_files_found,
                                               len([freq for freq in keyword_freq_files[1:-1] if freq]),
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
                wordless_message_box.wordless_message_box_missing_observed_files(main)

                wordless_message.wordless_message_generate_table_error(main)
        else:
            wordless_message_box.wordless_message_box_missing_ref_file(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['keywords']

    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if settings['generation_settings']['ref_file']:
            ref_file = main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'],
                                                             selected_only = True)

            files = [file
                     for file in main.wordless_files.get_selected_files()
                     if file != ref_file]

            if files:
                keywords_freq_files, keywords_stats_files = generate_keywords(main, files, ref_file)

                if keywords_freq_files:
                    text_test_significance = settings['generation_settings']['test_significance']
                    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                    (text_test_stat,
                     text_p_value,
                     text_bayes_factor) = main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
                    text_effect_size =  main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

                    if settings['plot_settings']['use_data'] == main.tr('Frequency'):
                        wordless_plot_freq.wordless_plot_freq_ref(main, keywords_freq_files,
                                                                  ref_file = ref_file,
                                                                  settings = settings['plot_settings'],
                                                                  label_x = main.tr('Keywords'))
                    else:
                        if settings['plot_settings']['use_data'] == text_test_stat:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 0]
                                                   for keyword, stats_files in keywords_stats_files.items()}

                            label_y = text_test_stat
                        elif settings['plot_settings']['use_data'] == text_p_value:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 1]
                                                   for keyword, stats_files in keywords_stats_files.items()}

                            label_y = text_p_value
                        elif settings['plot_settings']['use_data'] == text_bayes_factor:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 2]
                                                   for keyword, stats_files in keywords_stats_files.items()}

                            label_y = text_bayes_factor
                        elif settings['plot_settings']['use_data'] == text_effect_size:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 3]
                                                   for keyword, stats_files in keywords_stats_files.items()}

                            label_y = text_effect_size

                        wordless_plot_stat.wordless_plot_stat_ref(main, keywords_stat_files,
                                                                  ref_file = ref_file,
                                                                  settings = settings['plot_settings'],
                                                                  label_y = label_y)

                    wordless_message.wordless_message_generate_plot_success(main)
                else:
                    wordless_message_box.wordless_message_box_no_results_plot(main)

                    wordless_message.wordless_message_generate_plot_error(main)
            else:
                wordless_message_box.wordless_message_box_missing_observed_files(main)

                wordless_message.wordless_message_generate_plot_error(main)
        else:
            wordless_message_box.wordless_message_box_missing_ref_file(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message.wordless_message_generate_plot_error(main)
