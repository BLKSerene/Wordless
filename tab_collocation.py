#
# Wordless: Collocation
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import collections
import copy
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy

from wordless_measures import *
from wordless_plot import *
from wordless_text import *
from wordless_utils import *
from wordless_widgets import *

class Wordless_Table_Collocation(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Nodes'),
                             main.tr('Collocates'),
                             main.tr('Number of\nFiles Found'),
                         ],
                         headers_num = [
                             main.tr('Rank'),
                             main.tr('Number of\nFiles Found'),
                         ],
                         headers_pct = [
                             main.tr('Number of\nFiles Found')
                         ],
                         sorting_enabled = True)

        dialog_search = wordless_dialog.Wordless_Dialog_Search(self.main,
                                                               tab = 'collocation',
                                                               table = self,
                                                               cols_search = [
                                                                   self.tr('Nodes'),
                                                                   self.tr('Collocates')
                                                               ])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(main.tr('Generate Table'), main)
        self.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

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

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['collocation']['filter_settings']

            text_test_significance = self.settings['collocation']['generation_settings']['test_significance']
            text_measure_effect_size = self.settings['collocation']['generation_settings']['measure_effect_size']

            (col_text_test_stat,
             col_text_p_value,
             col_text_bayes_factor) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
            col_text_effect_size = self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

            if settings['filter_file'] == self.tr('Total'):
                if settings['freq_filter_data'] == self.tr('Total'):
                    col_freq = self.find_col(self.tr('Total\nFrequency'))
                else:
                    col_freq = self.find_col(self.tr(f'Total\n{settings["freq_filter_data"]}'))

                col_test_stat = self.find_col(self.tr(f'Total\n{col_text_test_stat}'))
                col_p_value = self.find_col(self.tr(f'Total\n{col_text_p_value}'))
                col_bayes_factor = self.find_col(self.tr(f'Total\n{col_text_bayes_factor}'))
                col_effect_size = self.find_col(self.tr(f'Total\n{col_text_effect_size}'))
            else:
                if settings['freq_filter_data'] == self.tr('Total'):
                    col_freq = self.find_col(self.tr(f'[{settings["filter_file"]}]\nFrequency'))
                else:
                    col_freq = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{settings["freq_filter_data"]}'))

                col_test_stat = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_test_stat}'))
                col_p_value = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_p_value}'))
                col_bayes_factor = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_bayes_factor}'))
                col_effect_size = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_effect_size}'))

            col_collocates = self.find_col('Collocates')
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

            len_collocate_min = (float('-inf')
                                 if settings['len_collocate_min_no_limit'] else settings['len_collocate_min'])
            len_collocate_max = (float('inf')
                                 if settings['len_collocate_max_no_limit'] else settings['len_collocate_max'])

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

                if col_text_test_stat:
                    if test_stat_min <= self.item(i, col_test_stat).val <= test_stat_max:
                        self.row_filters[i].append(True)
                    else:
                        self.row_filters[i].append(False)

                if p_value_min <= self.item(i, col_p_value).val <= p_value_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if col_text_bayes_factor:
                    if bayes_factor_min <= self.item(i, col_bayes_factor).val <= bayes_factor_max:
                        self.row_filters[i].append(True)
                    else:
                        self.row_filters[i].append(False)

                if effect_size_min <= self.item(i, col_effect_size).val <= effect_size_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if len_collocate_min <= len(self.item(i, col_collocates).text()) <= len_collocate_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if number_files_found_min <= self.item(i, col_number_files_found).val <= number_files_found_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

            self.filter_table()

        wordless_message.wordless_message_filter_table_done(self.main)

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.settings_default['collocation'])
        else:
            settings = copy.deepcopy(main.settings_custom['collocation'])

        # Token Settings
        checkbox_words.setChecked(settings['token_settings']['words'])
        checkbox_lowercase.setChecked(settings['token_settings']['lowercase'])
        checkbox_uppercase.setChecked(settings['token_settings']['uppercase'])
        checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings['token_settings']['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings['token_settings']['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        checkbox_nums.setChecked(settings['token_settings']['nums'])
        checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        # Search Settings
        group_box_search_settings.setChecked(settings['search_settings']['search_settings'])

        checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])
        
        if not defaults:
            line_edit_search_term.setText(settings['search_settings']['search_term'])

            for search_term in settings['search_settings']['search_terms']:
                list_search_terms.add_item(search_term)

        checkbox_ignore_case.setChecked(settings['search_settings']['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings['search_settings']['match_whole_word'])
        checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])

        # Context Settings
        if defaults:
            main.wordless_context_settings_collocation.load_settings(defaults = True)

        # Generation Settings
        checkbox_window_sync.setChecked(settings['generation_settings']['window_sync'])

        if settings['generation_settings']['window_left'] < 0:
            spin_box_window_left.setPrefix('L')
            spin_box_window_left.setValue(-settings['generation_settings']['window_left'])
        else:
            spin_box_window_left.setPrefix('R')
            spin_box_window_left.setValue(settings['generation_settings']['window_left'])

        if settings['generation_settings']['window_right'] < 0:
            spin_box_window_right.setPrefix('L')
            spin_box_window_right.setValue(-settings['generation_settings']['window_right'])
        else:
            spin_box_window_right.setPrefix('R')
            spin_box_window_right.setValue(settings['generation_settings']['window_right'])

        combo_box_test_significance.setCurrentText(settings['generation_settings']['test_significance'])
        combo_box_measure_effect_size.setCurrentText(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        checkbox_show_breakdown_position.setChecked(settings['table_settings']['show_breakdown_position'])
        checkbox_show_breakdown_file.setChecked(settings['table_settings']['show_breakdown_file'])

        # Plot Settings
        combo_box_plot_type.setCurrentText(settings['plot_settings']['plot_type'])
        combo_box_use_file.setCurrentText(settings['plot_settings']['use_file'])
        combo_box_use_data.setCurrentText(settings['plot_settings']['use_data'])
        checkbox_use_pct.setChecked(settings['plot_settings']['use_pct'])
        checkbox_use_cumulative.setChecked(settings['plot_settings']['use_cumulative'])

        spin_box_rank_min.setValue(settings['plot_settings']['rank_min'])
        checkbox_rank_min_no_limit.setChecked(settings['plot_settings']['rank_min_no_limit'])
        spin_box_rank_max.setValue(settings['plot_settings']['rank_max'])
        checkbox_rank_max_no_limit.setChecked(settings['plot_settings']['rank_max_no_limit'])

        # Filter Settings
        combo_box_freq_filter_data.setCurrentText(settings['filter_settings']['freq_filter_data'])
        spin_box_freq_min.setValue(settings['filter_settings']['freq_min'])
        checkbox_freq_min_no_limit.setChecked(settings['filter_settings']['freq_min_no_limit'])
        spin_box_freq_max.setValue(settings['filter_settings']['freq_max'])
        checkbox_freq_max_no_limit.setChecked(settings['filter_settings']['freq_max_no_limit'])

        spin_box_test_stat_min.setValue(settings['filter_settings']['test_stat_min'])
        checkbox_test_stat_min_no_limit.setChecked(settings['filter_settings']['test_stat_min_no_limit'])
        spin_box_test_stat_max.setValue(settings['filter_settings']['test_stat_max'])
        checkbox_test_stat_max_no_limit.setChecked(settings['filter_settings']['test_stat_max_no_limit'])

        spin_box_p_value_min.setValue(settings['filter_settings']['p_value_min'])
        checkbox_p_value_min_no_limit.setChecked(settings['filter_settings']['p_value_min_no_limit'])
        spin_box_p_value_max.setValue(settings['filter_settings']['p_value_max'])
        checkbox_p_value_max_no_limit.setChecked(settings['filter_settings']['p_value_max_no_limit'])

        spin_box_bayes_factor_min.setValue(settings['filter_settings']['bayes_factor_min'])
        checkbox_bayes_factor_min_no_limit.setChecked(settings['filter_settings']['bayes_factor_min_no_limit'])
        spin_box_bayes_factor_max.setValue(settings['filter_settings']['bayes_factor_max'])
        checkbox_bayes_factor_max_no_limit.setChecked(settings['filter_settings']['bayes_factor_max_no_limit'])

        spin_box_effect_size_min.setValue(settings['filter_settings']['effect_size_min'])
        checkbox_effect_size_min_no_limit.setChecked(settings['filter_settings']['effect_size_min_no_limit'])
        spin_box_effect_size_max.setValue(settings['filter_settings']['effect_size_max'])
        checkbox_effect_size_max_no_limit.setChecked(settings['filter_settings']['effect_size_max_no_limit'])

        spin_box_len_collocate_min.setValue(settings['filter_settings']['len_collocate_min'])
        checkbox_len_collocate_min_no_limit.setChecked(settings['filter_settings']['len_collocate_min_no_limit'])
        spin_box_len_collocate_max.setValue(settings['filter_settings']['len_collocate_max'])
        checkbox_len_collocate_max_no_limit.setChecked(settings['filter_settings']['len_collocate_max_no_limit'])

        spin_box_number_files_found_min.setValue(settings['filter_settings']['number_files_found_min'])
        checkbox_number_files_found_min_no_limit.setChecked(settings['filter_settings']['number_files_found_min_no_limit'])
        spin_box_number_files_found_max.setValue(settings['filter_settings']['number_files_found_max'])
        checkbox_number_files_found_max_no_limit.setChecked(settings['filter_settings']['number_files_found_max_no_limit'])

        combo_box_filter_file.setCurrentText(settings['filter_settings']['filter_file'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        measures_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['collocation']['token_settings']

        settings['words'] = checkbox_words.isChecked()
        settings['lowercase'] = checkbox_lowercase.isChecked()
        settings['uppercase'] = checkbox_uppercase.isChecked()
        settings['title_case'] = checkbox_title_case.isChecked()
        settings['treat_as_lowercase'] = checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize'] = checkbox_lemmatize.isChecked()
        settings['filter_stop_words'] = checkbox_filter_stop_words.isChecked()

        settings['nums'] = checkbox_nums.isChecked()
        settings['puncs'] = checkbox_puncs.isChecked()

    def search_settings_changed():
        settings = main.settings_custom['collocation']['search_settings']

        settings['search_settings'] = group_box_search_settings.isChecked()

        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()
        settings['search_term'] = line_edit_search_term.text()
        settings['search_terms'] = list_search_terms.get_items()

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()

    def generation_settings_changed():
        settings = main.settings_custom['collocation']['generation_settings']

        settings['window_sync'] = checkbox_window_sync.isChecked()

        if spin_box_window_left.prefix() == 'L':
            settings['window_left'] = -spin_box_window_left.value()
        else:
            settings['window_left'] = spin_box_window_left.value()

        if spin_box_window_right.prefix() == 'L':
            settings['window_right'] = -spin_box_window_right.value()
        else:
            settings['window_right'] = spin_box_window_right.value()

        settings['test_significance'] = combo_box_test_significance.currentText()
        settings['measure_effect_size'] = combo_box_measure_effect_size.currentText()

    def measures_changed():
        settings = main.settings_custom['collocation']['generation_settings']

        # Use Data
        use_data_old = main.settings_custom['collocation']['plot_settings']['use_data']

        text_test_significance = settings['test_significance']
        text_measure_effect_size = settings['measure_effect_size']

        combo_box_use_data.clear()

        for i in range(settings['window_left'], settings['window_right'] + 1):
            if i < 0:
                combo_box_use_data.addItem(main.tr(f'L{-i}'))
            elif i > 0:
                combo_box_use_data.addItem(main.tr(f'R{i}'))

        combo_box_use_data.addItem(main.tr('Frequency'))

        combo_box_use_data.addItems([col
                                     for col in main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
                                     if col])
        combo_box_use_data.addItem(main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(main.settings_default['collocation']['plot_settings']['use_data'])

    def table_settings_changed():
        settings = main.settings_custom['collocation']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown_position'] = checkbox_show_breakdown_position.isChecked()
        settings['show_breakdown_file'] = checkbox_show_breakdown_file.isChecked()

    def plot_settings_changed():
        settings = main.settings_custom['collocation']['plot_settings']

        settings['plot_type'] = combo_box_plot_type.currentText()
        settings['use_file'] = combo_box_use_file.currentText()
        settings['use_data'] = combo_box_use_data.currentText()
        settings['use_pct'] = checkbox_use_pct.isChecked()
        settings['use_cumulative'] = checkbox_use_cumulative.isChecked()

        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_min_no_limit'] = checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = spin_box_rank_max.value()
        settings['rank_max_no_limit'] = checkbox_rank_max_no_limit.isChecked()

    def filter_settings_changed():
        settings = main.settings_custom['collocation']['filter_settings']

        settings['freq_filter_data'] = combo_box_freq_filter_data.currentText()
        settings['freq_min'] = spin_box_freq_min.value()
        settings['freq_min_no_limit'] = checkbox_freq_min_no_limit.isChecked()
        settings['freq_max'] = spin_box_freq_max.value()
        settings['freq_max_no_limit'] = checkbox_freq_max_no_limit.isChecked()

        settings['test_stat_min'] = spin_box_test_stat_min.value()
        settings['test_stat_min_no_limit'] = checkbox_test_stat_min_no_limit.isChecked()
        settings['test_stat_max'] = spin_box_test_stat_max.value()
        settings['test_stat_max_no_limit'] = checkbox_test_stat_max_no_limit.isChecked()

        settings['p_value_min'] = spin_box_p_value_min.value()
        settings['p_value_min_no_limit'] = checkbox_p_value_min_no_limit.isChecked()
        settings['p_value_max'] = spin_box_p_value_max.value()
        settings['p_value_max_no_limit'] = checkbox_p_value_max_no_limit.isChecked()

        settings['bayes_factor_min'] = spin_box_bayes_factor_min.value()
        settings['bayes_factor_min_no_limit'] = checkbox_bayes_factor_min_no_limit.isChecked()
        settings['bayes_factor_max'] = spin_box_bayes_factor_max.value()
        settings['bayes_factor_max_no_limit'] = checkbox_bayes_factor_max_no_limit.isChecked()

        settings['effect_size_min'] = spin_box_effect_size_min.value()
        settings['effect_size_min_no_limit'] = checkbox_effect_size_min_no_limit.isChecked()
        settings['effect_size_max'] = spin_box_effect_size_max.value()
        settings['effect_size_max_no_limit'] = checkbox_effect_size_max_no_limit.isChecked()

        settings['len_collocate_min'] = spin_box_len_collocate_min.value()
        settings['len_collocate_min_no_limit'] = checkbox_len_collocate_min_no_limit.isChecked()
        settings['len_collocate_max'] = spin_box_len_collocate_max.value()
        settings['len_collocate_max_no_limit'] = checkbox_len_collocate_max_no_limit.isChecked()

        settings['number_files_found_min'] = spin_box_number_files_found_min.value()
        settings['number_files_found_min_no_limit'] = checkbox_number_files_found_min_no_limit.isChecked()
        settings['number_files_found_max'] = spin_box_number_files_found_max.value()
        settings['number_files_found_max_no_limit'] = checkbox_number_files_found_max_no_limit.isChecked()

        settings['filter_file'] = combo_box_filter_file.currentText()

    def table_item_changed():
        settings = table_collocation.settings['collocation']

        # Filter Data (Frequency)
        freq_filter_data_old = settings['filter_settings']['freq_filter_data']

        combo_box_freq_filter_data.clear()

        for i in range(settings['generation_settings']['window_left'], settings['generation_settings']['window_right'] + 1):
            if i < 0:
                combo_box_freq_filter_data.addItem(main.tr(f'L{-i}'))
            elif i > 0:
                combo_box_freq_filter_data.addItem(main.tr(f'R{i}'))

        combo_box_freq_filter_data.addItem(main.tr('Frequency'))

        if combo_box_freq_filter_data.findText(freq_filter_data_old) > -1:
            combo_box_freq_filter_data.setCurrentText(freq_filter_data_old)
        else:
            combo_box_freq_filter_data.setCurrentText(main.settings_default['collocation']['filter_settings']['freq_filter_data'])

        # Filters
        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (col_text_test_stat,
         col_text_p_value,
         col_text_bayes_factor) = main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
        col_text_effect_size =  main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

        if col_text_test_stat:
            label_test_stat.setText(f'{col_text_test_stat}:')

            if not checkbox_test_stat_min_no_limit.isChecked():
                spin_box_test_stat_min.setEnabled(True)
            if not checkbox_test_stat_max_no_limit.isChecked():
                spin_box_test_stat_max.setEnabled(True)

            checkbox_test_stat_min_no_limit.setEnabled(True)
            checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            label_test_stat.setText(main.tr('Test Statistic:'))

            spin_box_test_stat_min.setEnabled(False)
            checkbox_test_stat_min_no_limit.setEnabled(False)
            spin_box_test_stat_max.setEnabled(False)
            checkbox_test_stat_max_no_limit.setEnabled(False)

        if col_text_bayes_factor:
            if not checkbox_bayes_factor_min_no_limit.isChecked():
                spin_box_bayes_factor_min.setEnabled(True)
            if not checkbox_bayes_factor_max_no_limit.isChecked():
                spin_box_bayes_factor_max.setEnabled(True)

            checkbox_bayes_factor_min_no_limit.setEnabled(True)
            checkbox_bayes_factor_max_no_limit.setEnabled(True)
        else:
            spin_box_bayes_factor_min.setEnabled(False)
            checkbox_bayes_factor_min_no_limit.setEnabled(False)
            spin_box_bayes_factor_max.setEnabled(False)
            checkbox_bayes_factor_max_no_limit.setEnabled(False)

        label_effect_size.setText(f'{col_text_effect_size}:')

    tab_collocation = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_collocation = Wordless_Table_Collocation(main)

    tab_collocation.layout_table.addWidget(table_collocation.label_number_results, 0, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_search_results, 0, 4)
    tab_collocation.layout_table.addWidget(table_collocation, 1, 0, 1, 5)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_table, 2, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_plot, 2, 1)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_selected, 2, 2)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_all, 2, 3)
    tab_collocation.layout_table.addWidget(table_collocation.button_clear, 2, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(main.tr('Token Settings'), main)

    (checkbox_words,
     checkbox_lowercase,
     checkbox_uppercase,
     checkbox_title_case,
     checkbox_treat_as_lowercase,
     checkbox_lemmatize,
     checkbox_filter_stop_words,

     checkbox_nums,
     checkbox_puncs) = wordless_widgets.wordless_widgets_token_settings1(main)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_case.stateChanged.connect(token_settings_changed)
    checkbox_treat_as_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_lemmatize.stateChanged.connect(token_settings_changed)
    checkbox_filter_stop_words.stateChanged.connect(token_settings_changed)

    checkbox_nums.stateChanged.connect(token_settings_changed)
    checkbox_puncs.stateChanged.connect(token_settings_changed)

    group_box_token_settings.setLayout(QGridLayout())
    group_box_token_settings.layout().addWidget(checkbox_words, 0, 0)
    group_box_token_settings.layout().addWidget(checkbox_lowercase, 0, 1)
    group_box_token_settings.layout().addWidget(checkbox_uppercase, 1, 0)
    group_box_token_settings.layout().addWidget(checkbox_title_case, 1, 1)
    group_box_token_settings.layout().addWidget(checkbox_treat_as_lowercase, 2, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_lemmatize, 3, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_filter_stop_words, 4, 0, 1, 2)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 5, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_nums, 6, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 6, 1)

    # Search Settings
    group_box_search_settings = QGroupBox(main.tr('Search Settings'), main)

    (label_search_term,
     checkbox_multi_search_mode,
     line_edit_search_term,
     list_search_terms,

     checkbox_ignore_case,
     checkbox_match_inflected_forms,
     checkbox_match_whole_word,
     checkbox_use_regex) = wordless_widgets.wordless_widgets_search_settings(main)

    (label_context_settings,
     button_context_settings) = wordless_widgets.wordless_widgets_context_settings(main, tab = 'collocation')

    group_box_search_settings.setCheckable(True)

    group_box_search_settings.toggled.connect(search_settings_changed)

    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_collocation.button_generate_table.click)
    list_search_terms.itemChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 5, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 4, 1)

    layout_context_settings = QGridLayout()
    layout_context_settings.addWidget(label_context_settings, 0, 0)
    layout_context_settings.addWidget(button_context_settings, 0, 1)

    layout_context_settings.setColumnStretch(1, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addWidget(label_search_term, 0, 0)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 2)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 2)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 3, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 4, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 5, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 6, 0, 1, 2)

    group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 7, 0, 1, 2)

    group_box_search_settings.layout().addLayout(layout_context_settings, 8, 0, 1, 2)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_window = QLabel(main.tr('Collocational Window:'), main)
    (checkbox_window_sync,
     label_window_left,
     spin_box_window_left,
     label_window_right,
     spin_box_window_right) = wordless_widgets.wordless_widgets_window(main)

    (label_test_significance,
     combo_box_test_significance) = wordless_widgets.wordless_widgets_test_significance(main)
    (label_measure_effect_size,
     combo_box_measure_effect_size) = wordless_widgets.wordless_widgets_measure_effect_size(main)

    (label_settings_measures,
     button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(main,
                                                                                     tab = main.tr('Statistical Significance'))

    combo_box_test_significance.addItems(list(main.settings_global['tests_significance']['collocation'].keys()))
    combo_box_measure_effect_size.addItems(list(main.settings_global['measures_effect_size']['collocation'].keys()))

    checkbox_window_sync.stateChanged.connect(generation_settings_changed)
    spin_box_window_left.valueChanged.connect(generation_settings_changed)
    spin_box_window_right.valueChanged.connect(generation_settings_changed)

    combo_box_test_significance.currentTextChanged.connect(generation_settings_changed)
    combo_box_test_significance.currentTextChanged.connect(measures_changed)
    combo_box_measure_effect_size.currentTextChanged.connect(generation_settings_changed)
    combo_box_measure_effect_size.currentTextChanged.connect(measures_changed)

    layout_settings_measures = QGridLayout()
    layout_settings_measures.addWidget(label_settings_measures, 0, 0)
    layout_settings_measures.addWidget(button_settings_measures, 0, 1)

    layout_settings_measures.setColumnStretch(1, 1)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_window, 0, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(checkbox_window_sync, 0, 3, Qt.AlignRight)
    group_box_generation_settings.layout().addWidget(label_window_left, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_window_left, 1, 1)
    group_box_generation_settings.layout().addWidget(label_window_right, 1, 2)
    group_box_generation_settings.layout().addWidget(spin_box_window_right, 1, 3)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 2, 0, 1, 4)

    group_box_generation_settings.layout().addWidget(label_test_significance, 3, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(combo_box_test_significance, 4, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(label_measure_effect_size, 5, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(combo_box_measure_effect_size, 6, 0, 1, 4)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 7, 0, 1, 4)

    group_box_generation_settings.layout().addLayout(layout_settings_measures, 8, 0, 1, 4)

    group_box_generation_settings.layout().setColumnStretch(1, 1)
    group_box_generation_settings.layout().setColumnStretch(3, 1)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown_file) = wordless_widgets.wordless_widgets_table_settings(main, table_collocation)

    checkbox_show_breakdown_file.setText(main.tr('Show Breakdown by File'))
    checkbox_show_breakdown_position = QCheckBox(main.tr('Show Breakdown by Span Position'), main)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_position.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_position.stateChanged.connect(table_collocation.toggle_breakdown)
    checkbox_show_breakdown_file.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_file.stateChanged.connect(table_collocation.toggle_breakdown)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown_position, 2, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown_file, 3, 0)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    (label_plot_type,
     combo_box_plot_type,
     label_use_file,
     combo_box_use_file,
     label_use_data,
     combo_box_use_data,

     checkbox_use_pct,
     checkbox_use_cumulative) = wordless_widgets.wordless_widgets_plot_settings(main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (label_rank_min,
     spin_box_rank_min,
     checkbox_rank_min_no_limit,
     label_rank_max,
     spin_box_rank_max,
     checkbox_rank_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    combo_box_plot_type.currentTextChanged.connect(plot_settings_changed)
    combo_box_use_file.currentTextChanged.connect(plot_settings_changed)
    combo_box_use_data.currentTextChanged.connect(plot_settings_changed)
    checkbox_use_pct.stateChanged.connect(plot_settings_changed)
    checkbox_use_cumulative.stateChanged.connect(plot_settings_changed)

    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    checkbox_rank_min_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)
    checkbox_rank_max_no_limit.stateChanged.connect(plot_settings_changed)

    layout_plot_settings_combo_boxes = QGridLayout()
    layout_plot_settings_combo_boxes.addWidget(label_plot_type, 0, 0)
    layout_plot_settings_combo_boxes.addWidget(combo_box_plot_type, 0, 1)
    layout_plot_settings_combo_boxes.addWidget(label_use_file, 1, 0)
    layout_plot_settings_combo_boxes.addWidget(combo_box_use_file, 1, 1)
    layout_plot_settings_combo_boxes.addWidget(label_use_data, 2, 0)
    layout_plot_settings_combo_boxes.addWidget(combo_box_use_data, 2, 1)

    layout_plot_settings_combo_boxes.setColumnStretch(1, 1)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addLayout(layout_plot_settings_combo_boxes, 0, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_use_pct, 1, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_use_cumulative, 2, 0, 1, 3)
    
    group_box_plot_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 3)

    group_box_plot_settings.layout().addWidget(label_rank, 4, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(label_rank_min, 5, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_min, 5, 1)
    group_box_plot_settings.layout().addWidget(checkbox_rank_min_no_limit, 5, 2)
    group_box_plot_settings.layout().addWidget(label_rank_max, 6, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_max, 6, 1)
    group_box_plot_settings.layout().addWidget(checkbox_rank_max_no_limit, 6, 2)

    group_box_plot_settings.layout().setColumnStretch(1, 1)

    # Filter Settings
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_freq = QLabel(main.tr('Frequency:'), main)
    label_freq_filter_data = QLabel(main.tr('Filter Data:'), main)
    combo_box_freq_filter_data = wordless_box.Wordless_Combo_Box(main)
    (label_freq_min,
     spin_box_freq_min,
     checkbox_freq_min_no_limit,
     label_freq_max,
     spin_box_freq_max,
     checkbox_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_test_stat = QLabel(main.tr('Test Statistic:'), main)
    (label_test_stat_min,
     spin_box_test_stat_min,
     checkbox_test_stat_min_no_limit,
     label_test_stat_max,
     spin_box_test_stat_max,
     checkbox_test_stat_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(main)

    label_p_value = QLabel(main.tr('p-value:'), main)
    (label_p_value_min,
     spin_box_p_value_min,
     checkbox_p_value_min_no_limit,
     label_p_value_max,
     spin_box_p_value_max,
     checkbox_p_value_max_no_limit) = wordless_widgets.wordless_widgets_filter_p_value(main)

    label_bayes_factor = QLabel(main.tr('Bayes Factor:'), main)
    (label_bayes_factor_min,
     spin_box_bayes_factor_min,
     checkbox_bayes_factor_min_no_limit,
     label_bayes_factor_max,
     spin_box_bayes_factor_max,
     checkbox_bayes_factor_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(main)

    label_effect_size = QLabel(main.tr('Effect Size:'), main)
    (label_effect_size_min,
     spin_box_effect_size_min,
     checkbox_effect_size_min_no_limit,
     label_effect_size_max,
     spin_box_effect_size_max,
     checkbox_effect_size_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(main)

    label_len_collocate = QLabel(main.tr('Collocate Length:'), main)
    (label_len_collocate_min,
     spin_box_len_collocate_min,
     checkbox_len_collocate_min_no_limit,
     label_len_collocate_max,
     spin_box_len_collocate_max,
     checkbox_len_collocate_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100)

    label_number_files_found = QLabel(main.tr('Number of Files Found:'), main)
    (label_number_files_found_min,
     spin_box_number_files_found_min,
     checkbox_number_files_found_min_no_limit,
     label_number_files_found_max,
     spin_box_number_files_found_max,
     checkbox_number_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    (label_filter_file,
     combo_box_filter_file,
     button_filter_results) = wordless_widgets.wordless_widgets_filter_results(main, table_collocation)

    combo_box_freq_filter_data.addItem(main.tr('Total'))

    combo_box_freq_filter_data.currentTextChanged.connect(filter_settings_changed)
    spin_box_freq_min.valueChanged.connect(filter_settings_changed)
    checkbox_freq_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_max.valueChanged.connect(filter_settings_changed)
    checkbox_freq_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_test_stat_min.valueChanged.connect(filter_settings_changed)
    checkbox_test_stat_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_test_stat_max.valueChanged.connect(filter_settings_changed)
    checkbox_test_stat_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_p_value_min.valueChanged.connect(filter_settings_changed)
    checkbox_p_value_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_p_value_max.valueChanged.connect(filter_settings_changed)
    checkbox_p_value_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_bayes_factor_min.valueChanged.connect(filter_settings_changed)
    checkbox_bayes_factor_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_bayes_factor_max.valueChanged.connect(filter_settings_changed)
    checkbox_bayes_factor_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_effect_size_min.valueChanged.connect(filter_settings_changed)
    checkbox_effect_size_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_effect_size_max.valueChanged.connect(filter_settings_changed)
    checkbox_effect_size_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_len_collocate_min.valueChanged.connect(filter_settings_changed)
    checkbox_len_collocate_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_collocate_max.valueChanged.connect(filter_settings_changed)
    checkbox_len_collocate_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_number_files_found_min.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_number_files_found_max.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_max_no_limit.stateChanged.connect(filter_settings_changed)

    combo_box_filter_file.currentTextChanged.connect(filter_settings_changed)

    table_collocation.itemChanged.connect(table_item_changed)

    layout_freq_filter_data = QGridLayout()
    layout_freq_filter_data.addWidget(label_freq_filter_data, 0, 0)
    layout_freq_filter_data.addWidget(combo_box_freq_filter_data, 0, 1)

    layout_freq_filter_data.setColumnStretch(1, 1)

    layout_filter_file = QGridLayout()
    layout_filter_file.addWidget(label_filter_file, 0, 0)
    layout_filter_file.addWidget(combo_box_filter_file, 0, 1)

    layout_filter_file.setColumnStretch(1, 1)

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_freq, 0, 0, 1, 3)
    group_box_filter_settings.layout().addLayout(layout_freq_filter_data, 1, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_freq_min, 2, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_min, 2, 1)
    group_box_filter_settings.layout().addWidget(checkbox_freq_min_no_limit, 2, 2)
    group_box_filter_settings.layout().addWidget(label_freq_max, 3, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_max, 3, 1)
    group_box_filter_settings.layout().addWidget(checkbox_freq_max_no_limit, 3, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 4, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_test_stat, 5, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_test_stat_min, 6, 0)
    group_box_filter_settings.layout().addWidget(spin_box_test_stat_min, 6, 1)
    group_box_filter_settings.layout().addWidget(checkbox_test_stat_min_no_limit, 6, 2)
    group_box_filter_settings.layout().addWidget(label_test_stat_max, 7, 0)
    group_box_filter_settings.layout().addWidget(spin_box_test_stat_max, 7, 1)
    group_box_filter_settings.layout().addWidget(checkbox_test_stat_max_no_limit, 7, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 8, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_p_value, 9, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_p_value_min, 10, 0)
    group_box_filter_settings.layout().addWidget(spin_box_p_value_min, 10, 1)
    group_box_filter_settings.layout().addWidget(checkbox_p_value_min_no_limit, 10, 2)
    group_box_filter_settings.layout().addWidget(label_p_value_max, 11, 0)
    group_box_filter_settings.layout().addWidget(spin_box_p_value_max, 11, 1)
    group_box_filter_settings.layout().addWidget(checkbox_p_value_max_no_limit, 11, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 12, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_bayes_factor, 13, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_bayes_factor_min, 14, 0)
    group_box_filter_settings.layout().addWidget(spin_box_bayes_factor_min, 14, 1)
    group_box_filter_settings.layout().addWidget(checkbox_bayes_factor_min_no_limit, 14, 2)
    group_box_filter_settings.layout().addWidget(label_bayes_factor_max, 15, 0)
    group_box_filter_settings.layout().addWidget(spin_box_bayes_factor_max, 15, 1)
    group_box_filter_settings.layout().addWidget(checkbox_bayes_factor_max_no_limit, 15, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 16, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_effect_size, 17, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_effect_size_min, 18, 0)
    group_box_filter_settings.layout().addWidget(spin_box_effect_size_min, 18, 1)
    group_box_filter_settings.layout().addWidget(checkbox_effect_size_min_no_limit, 18, 2)
    group_box_filter_settings.layout().addWidget(label_effect_size_max, 19, 0)
    group_box_filter_settings.layout().addWidget(spin_box_effect_size_max, 19, 1)
    group_box_filter_settings.layout().addWidget(checkbox_effect_size_max_no_limit, 19, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 20, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_len_collocate, 21, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_len_collocate_min, 22, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_collocate_min, 22, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_collocate_min_no_limit, 22, 2)
    group_box_filter_settings.layout().addWidget(label_len_collocate_max, 23, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_collocate_max, 23, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_collocate_max_no_limit, 23, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 24, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_number_files_found, 25, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_number_files_found_min, 26, 0)
    group_box_filter_settings.layout().addWidget(spin_box_number_files_found_min, 26, 1)
    group_box_filter_settings.layout().addWidget(checkbox_number_files_found_min_no_limit, 26, 2)
    group_box_filter_settings.layout().addWidget(label_number_files_found_max, 27, 0)
    group_box_filter_settings.layout().addWidget(spin_box_number_files_found_max, 27, 1)
    group_box_filter_settings.layout().addWidget(checkbox_number_files_found_max_no_limit, 27, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 28, 0, 1, 3)

    group_box_filter_settings.layout().addLayout(layout_filter_file, 29, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(button_filter_results, 30, 0, 1, 3)

    group_box_filter_settings.layout().setColumnStretch(1, 1)

    tab_collocation.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    tab_collocation.layout_settings.setRowStretch(6, 1)

    load_settings()

    return tab_collocation

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

        text.tokens = wordless_text_processing.wordless_preprocess_tokens(main, text.tokens,
                                                                          lang_code = text.lang_code,
                                                                          settings = settings['token_settings'])

        search_terms = wordless_matching.match_search_terms(main, text.tokens,
                                                            lang_code = text.lang_code,
                                                            settings = settings['search_settings'])

        (search_terms_inclusion,
         search_terms_exclusion) = wordless_matching.match_search_terms_context(main, text.tokens,
                                                                                lang_code = text.lang_code,
                                                                                settings = settings['context_settings'])

        if search_terms:
            len_search_term_min = min([len(search_term) for search_term in search_terms])
            len_search_term_max = max([len(search_term) for search_term in search_terms])
        else:
            len_search_term_min = 1
            len_search_term_max = 1

        for ngram_size in range(len_search_term_min, len_search_term_max + 1):
            for i, ngram in enumerate(nltk.ngrams(text.tokens, ngram_size)):
                for j, collocate in enumerate(reversed(text.tokens[max(0, i - window_size_left) : i])):
                    if wordless_text_utils.check_context(i, text.tokens,
                                                         settings = settings['context_settings'],
                                                         search_terms_inclusion = search_terms_inclusion,
                                                         search_terms_exclusion = search_terms_exclusion):
                        if (ngram, collocate) not in collocates_freqs_file:
                            collocates_freqs_file[(ngram, collocate)] = [0] * window_size

                        collocates_freqs_file[(ngram, collocate)][window_size_left - 1 - j] += 1

                for j, collocate in enumerate(text.tokens[i + ngram_size: i + ngram_size + window_size_right]):
                    if wordless_text_utils.check_context(i, text.tokens,
                                                         settings = settings['context_settings'],
                                                         search_terms_inclusion = search_terms_inclusion,
                                                         search_terms_exclusion = search_terms_exclusion):
                        if (ngram, collocate) not in collocates_freqs_file:
                            collocates_freqs_file[(ngram, collocate)] = [0] * window_size

                        collocates_freqs_file[(ngram, collocate)][window_size_left + j] += 1

        collocates_freqs_file = wordless_text_processing.wordless_postprocess_freq_collocation(main, collocates_freqs_file,
                                                                                               lang_code = text.lang_code,
                                                                                               settings = settings['token_settings'])

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
            ngrams_freq_files.append(collections.Counter(nltk.ngrams(text.tokens, i)))

        # Nodes Text
        for (node, collocate) in collocates_freqs_file:
            nodes_text[node] = wordless_text_processing.wordless_word_detokenize(main, node, text.lang_code)

        texts.append(text)

    # Total
    if len(files) > 1:
        collocates_freqs_total = {}

        text_total = wordless_text.Wordless_Text(main, files[0])
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

    # Association
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

    if files:
        if (not settings['search_settings']['search_settings'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            collocates_freqs_files, collocates_stats_files, nodes_text = generate_collocates(main, files)

            if collocates_freqs_files:
                table.clear_table()

                table.settings = main.settings_custom

                text_test_significance = settings['generation_settings']['test_significance']
                text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                (col_text_test_stat,
                 col_text_p_value,
                 col_text_bayes_factor) = main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
                col_text_effect_size =  main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

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

                    if col_text_test_stat:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\n{col_text_test_stat}'),
                                         num = True, breakdown = True)

                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\n{col_text_p_value}'),
                                     num = True, breakdown = True)

                    if col_text_bayes_factor:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\n{col_text_bayes_factor}'),
                                         num = True, breakdown = True)

                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\n{col_text_effect_size}'),
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

                if col_text_test_stat:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total\n{col_text_test_stat}'),
                                     num = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\n{col_text_p_value}'),
                                 num = True)

                if col_text_bayes_factor:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total\n{col_text_bayes_factor}'),
                                     num = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\n{col_text_effect_size}'),
                                 num = True)

                # Sort by p-value of the first file
                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\n{col_text_p_value}')), Qt.AscendingOrder)

                if settings['generation_settings']['window_left'] < 0:  
                    cols_freqs_start = [table.find_col(f'[{file["name"]}]\nL{-settings["generation_settings"]["window_left"]}')
                                        for file in files]
                    cols_freqs_start.append(table.find_col(f'Total\nL{-settings["generation_settings"]["window_left"]}'))
                else:
                    cols_freqs_start = [table.find_col(f'[{file["name"]}]\nR{settings["generation_settings"]["window_left"]}')
                                        for file in files]
                    cols_freqs_start.append(table.find_col(f'Total\nR{settings["generation_settings"]["window_left"]}'))

                cols_freq = table.find_cols(main.tr('\nFrequency'))

                if col_text_test_stat:
                    cols_test_stat = table.find_cols(main.tr(f'\n{col_text_test_stat}'))

                cols_p_value = table.find_cols(main.tr('\np-value'))

                if col_text_bayes_factor:
                    cols_bayes_factor = table.find_cols(main.tr('\nBayes Factor'))

                cols_effect_size = table.find_cols(f'\n{col_text_effect_size}')
                col_number_files_found = table.find_col(main.tr('Number of\nFiles Found'))

                len_files = len(files)

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

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
                        if col_text_test_stat:
                            table.set_item_num_float(i, cols_test_stat[j], test_stat)

                        # p-value
                        table.set_item_num_float(i, cols_p_value[j], p_value)

                        # Bayes Factor
                        if col_text_bayes_factor:
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
            wordless_message_box.wordless_message_box_empty_search_term(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['collocation']

    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['search_settings']['search_settings'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            text_test_significance = settings['generation_settings']['test_significance']
            text_measure_effect_size = settings['generation_settings']['measure_effect_size']

            (col_text_test_stat,
             col_text_p_value,
             col_text_bayes_factor) = main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
            col_text_effect_size =  main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

            collocates_freqs_files, collocates_stats_files, nodes_text = generate_collocates(main, files)

            if collocates_freqs_files:
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

                    if settings['plot_settings']['use_data'] == col_text_test_stat:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 0]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = col_text_test_stat
                    elif settings['plot_settings']['use_data'] == col_text_p_value:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 1]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = col_text_p_value
                    elif settings['plot_settings']['use_data'] == col_text_bayes_factor:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 2]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = col_text_bayes_factor
                    elif settings['plot_settings']['use_data'] == col_text_effect_size:
                        collocates_stat_files = {collocate: numpy.array(stats_files)[:, 3]
                                                 for collocate, stats_files in collocates_stats_files.items()}

                        label_y = col_text_effect_size

                    wordless_plot_stat.wordless_plot_stat(main, collocates_stat_files,
                                                          settings = settings['plot_settings'],
                                                          label_x = main.tr('Collocates'),
                                                          label_y = label_y)

                wordless_message.wordless_message_generate_plot_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_plot(main)

                wordless_message.wordless_message_generate_plot_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_plot_error(main)
