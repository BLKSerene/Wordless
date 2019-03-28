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
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy

from wordless_checking import wordless_checking_file
from wordless_dialogs import wordless_dialog_misc, wordless_msg_box
from wordless_figs import wordless_fig, wordless_fig_freq, wordless_fig_stat
from wordless_text import wordless_text, wordless_text_utils, wordless_token_processing
from wordless_utils import wordless_misc, wordless_sorting, wordless_threading
from wordless_widgets import (wordless_box, wordless_layout, wordless_msg,
                              wordless_table, wordless_widgets)

class Wordless_Table_Keywords(wordless_table.Wordless_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(parent,
                         tab = 'keywords',
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

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_fig.clicked.connect(lambda: generate_fig(self.main))

class Wrapper_Keywords(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_keywords = Wordless_Table_Keywords(self)

        layout_results = wordless_layout.Wordless_Layout()
        layout_results.addWidget(self.table_keywords.label_number_results, 0, 0)
        layout_results.addWidget(self.table_keywords.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_keywords.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keywords, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_keywords.button_generate_fig, 2, 1)
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
         self.checkbox_ignore_tags,
         self.checkbox_ignore_tags_tags,

         self.stacked_widget_ignore_tags_type,
         self.combo_box_ignore_tags,
         self.combo_box_ignore_tags_tags,

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

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = wordless_layout.Wordless_Layout()
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

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

        layout_settings_measures = wordless_layout.Wordless_Layout()
        layout_settings_measures.addWidget(self.label_settings_measures, 0, 0)
        layout_settings_measures.addWidget(self.button_settings_measures, 0, 1)

        layout_settings_measures.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_ref_file, 0, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_ref_file, 1, 0)
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
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 3, 0)

        self.wrapper_settings.layout().setRowStretch(4, 1)

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

        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Generation Settings
        self.combo_box_ref_file.setCurrentText(settings['generation_settings']['ref_file'])
        self.combo_box_test_significance.setCurrentText(settings['generation_settings']['test_significance'])
        self.combo_box_measure_effect_size.setCurrentText(settings['generation_settings']['measure_effect_size'])

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
        self.generation_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()

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

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.combo_box_ignore_tags_tags.currentText()
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
                                          for col in self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
                                          if col])
        self.combo_box_use_data.addItem(self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col'])

        if self.combo_box_use_data.findText(use_data_old) > -1:
            self.combo_box_use_data.setCurrentText(use_data_old)
        else:
            self.combo_box_use_data.setCurrentText(self.main.settings_default['keywords']['fig_settings']['use_data'])

    def table_settings_changed(self):
        settings = self.main.settings_custom['keywords']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['keywords']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['use_file'] = self.combo_box_use_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

class Wordless_Worker_Process_Data_Keywords(wordless_threading.Wordless_Worker_Process_Data):
    processing_finished = pyqtSignal(dict, dict)

    def __init__(self, main, dialog_progress, data_received):
        super().__init__(main, dialog_progress, data_received)

        self.keywords_freq_files = []
        self.keywords_stats_files = []

    def process_data(self):
        texts = []

        settings = self.main.settings_custom['keywords']
        ref_file = self.main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'], selected_only = True)

        files = [file
                 for file in self.main.wordless_files.get_selected_files()
                 if file != ref_file]

        # Frequency
        for i, file in enumerate([ref_file] + files):
            text = wordless_text.Wordless_Text(self.main, file)

            tokens = wordless_token_processing.wordless_process_tokens_wordlist(text,
                                                                                token_settings = settings['token_settings'])

            self.keywords_freq_files.append(collections.Counter(tokens))

            if i > 0:
                texts.append(text)
            else:
                tokens_ref = text.tokens
                len_tokens_ref = len(tokens_ref)

        # Total
        if len(files) > 1:
            text_total = wordless_text.Wordless_Text_Blank()
            text_total.tokens = [token for text in texts for token in text.tokens]

            texts.append(text_total)
            self.keywords_freq_files.append(sum(self.keywords_freq_files, collections.Counter()))

            self.keywords_freq_files[0] = {token: freq
                                      for token, freq in self.keywords_freq_files[0].items()
                                      if token in text_total.tokens}
        else:
            self.keywords_freq_files[0] = {token: freq
                                      for token, freq in self.keywords_freq_files[0].items()
                                      if token in self.keywords_freq_files[1]}

        self.progress_updated.emit(self.tr('Processing data ...'))

        # Keyness
        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        test_significance = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['func']
        measure_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['func']

        keywords_freq_file_observed = self.keywords_freq_files[-1]
        keywords_freq_file_ref = self.keywords_freq_files[0]

        for text in texts:
            keywords_stats_file = {}

            tokens_observed = text.tokens
            len_tokens_observed = len(tokens_observed)

            if text_test_significance in [self.tr('Student\'s t-test (Two-sample)'),
                                          self.tr('Mann-Whitney U Test')]:
                # Test Statistic, p-value & Bayes Factor
                if text_test_significance == self.tr('Student\'s t-test (Two-sample)'):
                    number_sections = self.main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['number_sections']
                    use_data = self.main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['use_data']
                elif text_test_significance == self.tr('Mann-Whitney U Test'):
                    number_sections = self.main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['number_sections']
                    use_data = self.main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['use_data']

                sections_observed = wordless_text_utils.to_sections(tokens_observed, number_sections)
                sections_ref = wordless_text_utils.to_sections(tokens_ref, number_sections)

                sections_freq_observed = [collections.Counter(section) for section in sections_observed]
                sections_freq_ref = [collections.Counter(section) for section in sections_observed]

                len_sections_observed = [len(section) for section in sections_observed]
                len_sections_ref = [len(section) for section in sections_ref]

                if use_data == self.tr('Absolute Frequency'):
                    for token in keywords_freq_file_observed:
                        counts_observed = [section_freq.get(token, 0) for section_freq in sections_freq_observed]
                        counts_ref = [section_freq.get(token, 0) for section_freq in sections_freq_ref]

                        keywords_stats_file[token] = test_significance(self.main, counts_observed, counts_ref)
                elif use_data == self.tr('Relative Frequency'):
                    for token in keywords_freq_file_observed:
                        counts_observed = [section_freq.get(token, 0) / len_sections_observed[i]
                                           for i, section_freq in enumerate(sections_freq_observed)]
                        counts_ref = [section_freq.get(token, 0) / len_sections_ref[i]
                                      for i, section_freq in enumerate(sections_freq_ref)]

                        keywords_stats_file[token] = test_significance(self.main, counts_observed, counts_ref)

                # Effect Size
                for token in keywords_freq_file_observed:
                    c11 = keywords_freq_file_observed.get(token, 0)
                    c12 = keywords_freq_file_ref.get(token, 0)
                    c21 = len_tokens_observed - c11
                    c22 = len_tokens_ref - c12

                    keywords_stats_file[token].append(measure_effect_size(self.main, c11, c12, c21, c22))
            else:
                for token in keywords_freq_file_observed:
                    c11 = keywords_freq_file_observed.get(token, 0)
                    c12 = keywords_freq_file_ref.get(token, 0)
                    c21 = len_tokens_observed - c11
                    c22 = len_tokens_ref - c12

                    # Test Statistic, p-value & Bayes Factor
                    keywords_stats_file[token] = test_significance(self.main, c11, c12, c21, c22)

                    # Effect Size
                    keywords_stats_file[token].append(measure_effect_size(self.main, c11, c12, c21, c22))

            self.keywords_stats_files.append(keywords_stats_file)

        if len(files) == 1:
            self.keywords_freq_files.append(self.keywords_freq_files[1])
            self.keywords_stats_files *= 2

class Wordless_Worker_Process_Data_Keywords_Table(Wordless_Worker_Process_Data_Keywords):
    def process_data(self):
        super().process_data()

        self.progress_updated.emit(self.tr('Rendering table ...'))

        time.sleep(0.1)

        self.processing_finished.emit(wordless_misc.merge_dicts(self.keywords_freq_files),
                                      wordless_misc.merge_dicts(self.keywords_stats_files))

class Wordless_Worker_Process_Data_Keywords_Fig(Wordless_Worker_Process_Data_Keywords):
    def process_data(self):
        super().process_data()

        self.progress_updated.emit(self.tr('Rendering figure ...'))

        time.sleep(0.1)

        self.processing_finished.emit(wordless_misc.merge_dicts(self.keywords_freq_files),
                                      wordless_misc.merge_dicts(self.keywords_stats_files))

@wordless_misc.log_timing
def generate_table(main, table):
    def data_received(keywords_freq_files, keywords_stats_files):
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

            wordless_msg.wordless_msg_generate_table_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_table_error(main)

        dialog_progress.accept()

    settings = main.settings_custom['keywords']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        ref_file = main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'],
                                                         selected_only = True)

        files = [file
                 for file in main.wordless_files.get_selected_files()
                 if file != ref_file]

        if files:
            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

            worker_process_data = Wordless_Worker_Process_Data_Keywords_Table(main, dialog_progress, data_received)
            thread_process_data = wordless_threading.Wordless_Thread_Process_Data(worker_process_data)

            thread_process_data.start()

            dialog_progress.exec_()

            thread_process_data.quit()
            thread_process_data.wait()
        else:
            wordless_msg_box.wordless_msg_box_missing_observed_file(main)

            wordless_msg.wordless_msg_generate_table_error(main)
    else:
        wordless_msg.wordless_msg_generate_table_error(main)

@wordless_misc.log_timing
def generate_fig(main):
    def data_received(keywords_freq_files, keywords_stats_files):
        if keywords_freq_files:
            text_test_significance = settings['generation_settings']['test_significance']
            text_measure_effect_size = settings['generation_settings']['measure_effect_size']

            (text_test_stat,
             text_p_value,
             text_bayes_factor) = main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
            text_effect_size =  main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

            if settings['fig_settings']['use_data'] == main.tr('Frequency'):
                wordless_fig_freq.wordless_fig_freq_ref(main, keywords_freq_files,
                                                        ref_file = ref_file,
                                                        settings = settings['fig_settings'],
                                                        label_x = main.tr('Keywords'))
            else:
                if settings['fig_settings']['use_data'] == text_test_stat:
                    keywords_stat_files = {keyword: numpy.array(stats_files)[:, 0]
                                           for keyword, stats_files in keywords_stats_files.items()}

                    label_y = text_test_stat
                elif settings['fig_settings']['use_data'] == text_p_value:
                    keywords_stat_files = {keyword: numpy.array(stats_files)[:, 1]
                                           for keyword, stats_files in keywords_stats_files.items()}

                    label_y = text_p_value
                elif settings['fig_settings']['use_data'] == text_bayes_factor:
                    keywords_stat_files = {keyword: numpy.array(stats_files)[:, 2]
                                           for keyword, stats_files in keywords_stats_files.items()}

                    label_y = text_bayes_factor
                elif settings['fig_settings']['use_data'] == text_effect_size:
                    keywords_stat_files = {keyword: numpy.array(stats_files)[:, 3]
                                           for keyword, stats_files in keywords_stats_files.items()}

                    label_y = text_effect_size

                wordless_fig_stat.wordless_fig_stat_ref(main, keywords_stat_files,
                                                        ref_file = ref_file,
                                                        settings = settings['fig_settings'],
                                                        label_y = label_y)

            wordless_msg.wordless_msg_generate_fig_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_fig_error(main)

        dialog_progress.accept()

        if keywords_freq_files:
            wordless_fig.show_fig()

    settings = main.settings_custom['keywords']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        ref_file = main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'],
                                                         selected_only = True)

        files = [file
                 for file in main.wordless_files.get_selected_files()
                 if file != ref_file]

        if files:
            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

            worker_process_data = Wordless_Worker_Process_Data_Keywords_Fig(main, dialog_progress, data_received)
            thread_process_data = wordless_threading.Wordless_Thread_Process_Data(worker_process_data)

            thread_process_data.start()

            dialog_progress.exec_()

            thread_process_data.quit()
            thread_process_data.wait()
        else:
            wordless_msg_box.wordless_msg_box_missing_observed_file(main)

            wordless_msg.wordless_msg_generate_fig_error(main)
    else:
        wordless_msg.wordless_msg_generate_fig_error(main)
