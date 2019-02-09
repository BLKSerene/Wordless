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
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Keywords'),
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
                                                               tab = 'keywords',
                                                               table = self,
                                                               cols_search = [
                                                                   self.tr('Keywords')
                                                               ])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(main.tr('Generate Table'), main)
        self.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['keywords']['filter_settings']

            text_test_significance = self.settings['keywords']['generation_settings']['test_significance']
            text_measure_effect_size = self.settings['keywords']['generation_settings']['measure_effect_size']

            (col_text_test_stat,
             col_text_p_value,
             col_text_bayes_factor) = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
            col_text_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

            if settings['filter_file'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total\nFrequency'))
                col_test_stat = self.find_col(self.tr(f'Total\n{col_text_test_stat}'))
                col_p_value = self.find_col(self.tr(f'Total\n{col_text_p_value}'))
                col_bayes_factor = self.find_col(self.tr(f'Total\n{col_text_bayes_factor}'))
                col_effect_size = self.find_col(self.tr(f'Total\n{col_text_effect_size}'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["filter_file"]}]\nFrequency'))
                col_test_stat = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_test_stat}'))
                col_p_value = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_p_value}'))
                col_bayes_factor = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_bayes_factor}'))
                col_effect_size = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_effect_size}'))

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

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.settings_default['keywords'])
        else:
            settings = copy.deepcopy(main.settings_custom['keywords'])

        # Token Settings
        checkbox_words.setChecked(settings['token_settings']['words'])
        checkbox_lowercase.setChecked(settings['token_settings']['lowercase'])
        checkbox_uppercase.setChecked(settings['token_settings']['uppercase'])
        checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        checkbox_nums.setChecked(settings['token_settings']['nums'])
        checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        checkbox_treat_as_lowercase.setChecked(settings['token_settings']['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings['token_settings']['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        checkbox_ignore_tags_tags_only.setChecked(settings['token_settings']['ignore_tags_tags_only'])
        combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        combo_box_ignore_tags_tags_only.setCurrentText(settings['token_settings']['ignore_tags_type_tags_only'])
        checkbox_tags_only.setChecked(settings['token_settings']['tags_only'])

        # Generation Settings
        combo_box_ref_file.setCurrentText(settings['generation_settings']['ref_file'])
        combo_box_test_significance.setCurrentText(settings['generation_settings']['test_significance'])
        combo_box_measure_effect_size.setCurrentText(settings['generation_settings']['measure_effect_size'])

        # Table Settings
        checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

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

        spin_box_len_keyword_min.setValue(settings['filter_settings']['len_keyword_min'])
        checkbox_len_keyword_min_no_limit.setChecked(settings['filter_settings']['len_keyword_min_no_limit'])
        spin_box_len_keyword_max.setValue(settings['filter_settings']['len_keyword_max'])
        checkbox_len_keyword_max_no_limit.setChecked(settings['filter_settings']['len_keyword_max_no_limit'])

        spin_box_number_files_found_min.setValue(settings['filter_settings']['number_files_found_min'])
        checkbox_number_files_found_min_no_limit.setChecked(settings['filter_settings']['number_files_found_min_no_limit'])
        spin_box_number_files_found_max.setValue(settings['filter_settings']['number_files_found_max'])
        checkbox_number_files_found_max_no_limit.setChecked(settings['filter_settings']['number_files_found_max_no_limit'])

        combo_box_filter_file.setCurrentText(settings['filter_settings']['filter_file'])

        token_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['keywords']['token_settings']

        settings['words'] = checkbox_words.isChecked()
        settings['lowercase'] = checkbox_lowercase.isChecked()
        settings['uppercase'] = checkbox_uppercase.isChecked()
        settings['title_case'] = checkbox_title_case.isChecked()
        settings['nums'] = checkbox_nums.isChecked()
        settings['puncs'] = checkbox_puncs.isChecked()

        settings['treat_as_lowercase'] = checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize'] = checkbox_lemmatize.isChecked()
        settings['filter_stop_words'] = checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags_only'] = checkbox_ignore_tags_tags_only.isChecked()
        settings['ignore_tags_type'] = combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags_only'] = combo_box_ignore_tags_tags_only.currentText()
        settings['tags_only'] = checkbox_tags_only.isChecked()

    def generation_settings_changed():
        settings = main.settings_custom['keywords']['generation_settings']

        if combo_box_ref_file.currentText() == main.tr('*** None ***'):
            settings['ref_file'] = ''
        else:
            settings['ref_file'] = combo_box_ref_file.currentText()

        settings['test_significance'] = combo_box_test_significance.currentText()
        settings['measure_effect_size'] = combo_box_measure_effect_size.currentText()

        # Use File
        use_file_old = combo_box_use_file.currentText()

        combo_box_use_file.wordless_files_changed()

        combo_box_use_file.removeItem(combo_box_use_file.findText(settings['ref_file']))

        if combo_box_use_file.findText(use_file_old) > -1:
            combo_box_use_file.setCurrentText(use_file_old)
        else:
            combo_box_use_file.setCurrentIndex(0)

        # Use Data
        use_data_old = combo_box_use_data.currentText()

        combo_box_use_data.clear()

        combo_box_use_data.addItem(main.tr('Frequency'))
        combo_box_use_data.addItems([col
                                     for col in main.settings_global['tests_significance']['collocation'][settings['test_significance']]['cols']
                                     if col])
        combo_box_use_data.addItem(main.settings_global['measures_effect_size']['keywords'][settings['measure_effect_size']]['col'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(main.settings_default['keywords']['plot_settings']['use_data'])

    def table_settings_changed():
        settings = main.settings_custom['keywords']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        settings = main.settings_custom['keywords']['plot_settings']

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
        settings = main.settings_custom['keywords']['filter_settings']

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

        settings['len_keyword_min'] = spin_box_len_keyword_min.value()
        settings['len_keyword_min_no_limit'] = checkbox_len_keyword_min_no_limit.isChecked()
        settings['len_keyword_max'] = spin_box_len_keyword_max.value()
        settings['len_keyword_max_no_limit'] = checkbox_len_keyword_max_no_limit.isChecked()

        settings['number_files_found_min'] = spin_box_number_files_found_min.value()
        settings['number_files_found_min_no_limit'] = checkbox_number_files_found_min_no_limit.isChecked()
        settings['number_files_found_max'] = spin_box_number_files_found_max.value()
        settings['number_files_found_max_no_limit'] = checkbox_number_files_found_max_no_limit.isChecked()

        settings['filter_file'] = combo_box_filter_file.currentText()

    def table_item_changed():
        settings = table_keywords.settings['keywords']

        ref_file = settings['generation_settings']['ref_file']

        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (col_text_test_stat,
         col_text_p_value,
         col_text_bayes_factor) = main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
        col_text_effect_size =  main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

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
        
        combo_box_filter_file.removeItem(combo_box_filter_file.findText(ref_file))

    tab_keywords = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_keywords = Wordless_Table_Keywords(main)

    tab_keywords.layout_table.addWidget(table_keywords.label_number_results, 0, 0)
    tab_keywords.layout_table.addWidget(table_keywords.button_search_results, 0, 4)
    tab_keywords.layout_table.addWidget(table_keywords, 1, 0, 1, 5)
    tab_keywords.layout_table.addWidget(table_keywords.button_generate_table, 2, 0)
    tab_keywords.layout_table.addWidget(table_keywords.button_generate_plot, 2, 1)
    tab_keywords.layout_table.addWidget(table_keywords.button_export_selected, 2, 2)
    tab_keywords.layout_table.addWidget(table_keywords.button_export_all, 2, 3)
    tab_keywords.layout_table.addWidget(table_keywords.button_clear, 2, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(main.tr('Token Settings'), main)

    (checkbox_words,
     checkbox_lowercase,
     checkbox_uppercase,
     checkbox_title_case,
     checkbox_nums,
     checkbox_puncs,

     checkbox_treat_as_lowercase,
     checkbox_lemmatize,
     checkbox_filter_stop_words,

     checkbox_ignore_tags,
     checkbox_ignore_tags_tags_only,
     combo_box_ignore_tags,
     combo_box_ignore_tags_tags_only,
     label_ignore_tags,
     checkbox_tags_only) = wordless_widgets.wordless_widgets_token_settings(main)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_case.stateChanged.connect(token_settings_changed)
    checkbox_nums.stateChanged.connect(token_settings_changed)
    checkbox_puncs.stateChanged.connect(token_settings_changed)

    checkbox_treat_as_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_lemmatize.stateChanged.connect(token_settings_changed)
    checkbox_filter_stop_words.stateChanged.connect(token_settings_changed)

    checkbox_ignore_tags.stateChanged.connect(token_settings_changed)
    checkbox_ignore_tags_tags_only.stateChanged.connect(token_settings_changed)
    combo_box_ignore_tags.currentTextChanged.connect(token_settings_changed)
    combo_box_ignore_tags_tags_only.currentTextChanged.connect(token_settings_changed)
    checkbox_tags_only.stateChanged.connect(token_settings_changed)

    layout_ignore_tags = QGridLayout()
    layout_ignore_tags.addWidget(checkbox_ignore_tags, 0, 0)
    layout_ignore_tags.addWidget(checkbox_ignore_tags_tags_only, 0, 0)
    layout_ignore_tags.addWidget(combo_box_ignore_tags, 0, 1)
    layout_ignore_tags.addWidget(combo_box_ignore_tags_tags_only, 0, 1)
    layout_ignore_tags.addWidget(label_ignore_tags, 0, 2)

    layout_ignore_tags.setColumnStretch(3, 1)

    group_box_token_settings.setLayout(QGridLayout())
    group_box_token_settings.layout().addWidget(checkbox_words, 0, 0)
    group_box_token_settings.layout().addWidget(checkbox_lowercase, 0, 1)
    group_box_token_settings.layout().addWidget(checkbox_uppercase, 1, 0)
    group_box_token_settings.layout().addWidget(checkbox_title_case, 1, 1)
    group_box_token_settings.layout().addWidget(checkbox_nums, 2, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 2, 1)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_treat_as_lowercase, 4, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_lemmatize, 5, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_filter_stop_words, 6, 0, 1, 2)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 7, 0, 1, 2)

    group_box_token_settings.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_tags_only, 9, 0, 1, 2)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_ref_file = QLabel(main.tr('Reference File:'), main)
    combo_box_ref_file = wordless_box.Wordless_Combo_Box_Ref_File(main)

    (label_test_significance,
     combo_box_test_significance) = wordless_widgets.wordless_widgets_test_significance(main)
    (label_measure_effect_size,
     combo_box_measure_effect_size) = wordless_widgets.wordless_widgets_measure_effect_size(main)

    (label_settings_measures,
     button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(main,
                                                                                     tab = main.tr('Statistical Significance'))

    combo_box_test_significance.addItems(list(main.settings_global['tests_significance']['keywords'].keys()))
    combo_box_measure_effect_size.addItems(list(main.settings_global['measures_effect_size']['keywords'].keys()))

    combo_box_ref_file.currentTextChanged.connect(generation_settings_changed)
    combo_box_test_significance.currentTextChanged.connect(generation_settings_changed)
    combo_box_measure_effect_size.currentTextChanged.connect(generation_settings_changed)

    layout_settings_measures = QGridLayout()
    layout_settings_measures.addWidget(label_settings_measures, 0, 0)
    layout_settings_measures.addWidget(button_settings_measures, 0, 1)

    layout_settings_measures.setColumnStretch(1, 1)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_ref_file, 0, 0)
    group_box_generation_settings.layout().addWidget(combo_box_ref_file, 1, 0)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 2, 0)

    group_box_generation_settings.layout().addWidget(label_test_significance, 3, 0)
    group_box_generation_settings.layout().addWidget(combo_box_test_significance, 4, 0)
    group_box_generation_settings.layout().addWidget(label_measure_effect_size, 5, 0)
    group_box_generation_settings.layout().addWidget(combo_box_measure_effect_size, 6, 0)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 7, 0)

    group_box_generation_settings.layout().addLayout(layout_settings_measures, 8, 0)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_keywords)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown, 2, 0)

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

    label_len_keyword = QLabel(main.tr('Keyword Length:'), main)
    (label_len_keyword_min,
     spin_box_len_keyword_min,
     checkbox_len_keyword_min_no_limit,
     label_len_keyword_max,
     spin_box_len_keyword_max,
     checkbox_len_keyword_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100)

    label_number_files_found = QLabel(main.tr('Number of Files Found:'), main)
    (label_number_files_found_min,
     spin_box_number_files_found_min,
     checkbox_number_files_found_min_no_limit,
     label_number_files_found_max,
     spin_box_number_files_found_max,
     checkbox_number_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    (label_filter_file,
     combo_box_filter_file,
     button_filter_results) = wordless_widgets.wordless_widgets_filter_results(main, table_keywords)

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

    spin_box_len_keyword_min.valueChanged.connect(filter_settings_changed)
    checkbox_len_keyword_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_keyword_max.valueChanged.connect(filter_settings_changed)
    checkbox_len_keyword_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_number_files_found_min.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_number_files_found_max.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_max_no_limit.stateChanged.connect(filter_settings_changed)

    combo_box_filter_file.currentTextChanged.connect(filter_settings_changed)

    table_keywords.itemChanged.connect(table_item_changed)

    layout_filter_file = QGridLayout()
    layout_filter_file.addWidget(label_filter_file, 0, 0)
    layout_filter_file.addWidget(combo_box_filter_file, 0, 1)

    layout_filter_file.setColumnStretch(1, 1)

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_freq, 0, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_freq_min, 1, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_min, 1, 1)
    group_box_filter_settings.layout().addWidget(checkbox_freq_min_no_limit, 1, 2)
    group_box_filter_settings.layout().addWidget(label_freq_max, 2, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_max, 2, 1)
    group_box_filter_settings.layout().addWidget(checkbox_freq_max_no_limit, 2, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_test_stat, 4, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_test_stat_min, 5, 0)
    group_box_filter_settings.layout().addWidget(spin_box_test_stat_min, 5, 1)
    group_box_filter_settings.layout().addWidget(checkbox_test_stat_min_no_limit, 5, 2)
    group_box_filter_settings.layout().addWidget(label_test_stat_max, 6, 0)
    group_box_filter_settings.layout().addWidget(spin_box_test_stat_max, 6, 1)
    group_box_filter_settings.layout().addWidget(checkbox_test_stat_max_no_limit, 6, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 7, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_p_value, 8, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_p_value_min, 9, 0)
    group_box_filter_settings.layout().addWidget(spin_box_p_value_min, 9, 1)
    group_box_filter_settings.layout().addWidget(checkbox_p_value_min_no_limit, 9, 2)
    group_box_filter_settings.layout().addWidget(label_p_value_max, 10, 0)
    group_box_filter_settings.layout().addWidget(spin_box_p_value_max, 10, 1)
    group_box_filter_settings.layout().addWidget(checkbox_p_value_max_no_limit, 10, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 11, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_bayes_factor, 12, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_bayes_factor_min, 13, 0)
    group_box_filter_settings.layout().addWidget(spin_box_bayes_factor_min, 13, 1)
    group_box_filter_settings.layout().addWidget(checkbox_bayes_factor_min_no_limit, 13, 2)
    group_box_filter_settings.layout().addWidget(label_bayes_factor_max, 14, 0)
    group_box_filter_settings.layout().addWidget(spin_box_bayes_factor_max, 14, 1)
    group_box_filter_settings.layout().addWidget(checkbox_bayes_factor_max_no_limit, 14, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 15, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_effect_size, 16, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_effect_size_min, 17, 0)
    group_box_filter_settings.layout().addWidget(spin_box_effect_size_min, 17, 1)
    group_box_filter_settings.layout().addWidget(checkbox_effect_size_min_no_limit, 17, 2)
    group_box_filter_settings.layout().addWidget(label_effect_size_max, 18, 0)
    group_box_filter_settings.layout().addWidget(spin_box_effect_size_max, 18, 1)
    group_box_filter_settings.layout().addWidget(checkbox_effect_size_max_no_limit, 18, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 19, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_len_keyword, 20, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_len_keyword_min, 21, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_keyword_min, 21, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_keyword_min_no_limit, 21, 2)
    group_box_filter_settings.layout().addWidget(label_len_keyword_max, 22, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_keyword_max, 22, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_keyword_max_no_limit, 22, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 23, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_number_files_found, 24, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_number_files_found_min, 25, 0)
    group_box_filter_settings.layout().addWidget(spin_box_number_files_found_min, 25, 1)
    group_box_filter_settings.layout().addWidget(checkbox_number_files_found_min_no_limit, 25, 2)
    group_box_filter_settings.layout().addWidget(label_number_files_found_max, 26, 0)
    group_box_filter_settings.layout().addWidget(spin_box_number_files_found_max, 26, 1)
    group_box_filter_settings.layout().addWidget(checkbox_number_files_found_max_no_limit, 26, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 27, 0, 1, 3)

    group_box_filter_settings.layout().addLayout(layout_filter_file, 28, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(button_filter_results, 29, 0, 1, 3)

    group_box_filter_settings.layout().setColumnStretch(1, 1)

    tab_keywords.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_generation_settings, 1, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_table_settings, 2, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_plot_settings, 3, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_filter_settings, 4, 0, Qt.AlignTop)

    tab_keywords.layout_settings.setRowStretch(5, 1)

    load_settings()

    return tab_keywords

def generate_keywords(main, files, ref_file):
    texts = []
    keywords_freq_files = []
    keywords_stats_files = []

    settings = main.settings_custom['keywords']

    # Frequency
    for i, file in enumerate([ref_file] + files):
        text = wordless_text.Wordless_Text(main, file)

        tokens = wordless_token_processing.wordless_preprocess_tokens_wordlist(text,
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

    text_test_significance = settings['generation_settings']['test_significance']
    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

    (col_text_test_stat,
     col_text_p_value,
     col_text_bayes_factor) = main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
    col_text_effect_size =  main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

    if settings['generation_settings']['ref_file']:
        ref_file = main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'],
                                                         selected_only = True)

        if wordless_checking_file.check_files_loading(main, [ref_file]):
            files = [file
                     for file in wordless_checking_file.check_files_loading(main, main.wordless_files.get_selected_files())
                     if file != ref_file]

            if files:
                keywords_freq_files, keywords_stats_files = generate_keywords(main, files, ref_file)

                if keywords_freq_files:
                    table.clear_table()

                    table.settings = copy.deepcopy(main.settings_custom)

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

                    cols_freq = table.find_cols(main.tr('\nFrequency'))

                    if col_text_test_stat:
                        cols_test_stat = table.find_cols(main.tr(f'\n{col_text_test_stat}'))

                    cols_p_value = table.find_cols(main.tr('\np-value'))

                    if col_text_bayes_factor:
                        cols_bayes_factor = table.find_cols(main.tr('\nBayes Factor'))

                    cols_effect_size = table.find_cols(f'\n{col_text_effect_size}')
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
                            if col_text_test_stat:
                                table.set_item_num_float(i, cols_test_stat[j], test_stat)

                            # p-value
                            table.set_item_num_float(i, cols_p_value[j], p_value)

                            # Bayes Factor
                            if col_text_bayes_factor:
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
            wordless_message_box.wordless_message_box_error_ref_file(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message_box.wordless_message_box_missing_ref_file(main)

        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['keywords']

    if settings['generation_settings']['ref_file']:
        ref_file = main.wordless_files.find_file_by_name(settings['generation_settings']['ref_file'],
                                                         selected_only = True)

        if wordless_checking_file.check_files_loading(main, [ref_file]):
            files = [file
                     for file in wordless_checking_file.check_files_loading(main, main.wordless_files.get_selected_files())
                     if file != ref_file]

            if files:
                keywords_freq_files, keywords_stats_files = generate_keywords(main, files, ref_file)

                if keywords_freq_files:
                    text_test_significance = settings['generation_settings']['test_significance']
                    text_measure_effect_size = settings['generation_settings']['measure_effect_size']

                    (col_text_test_stat,
                     col_text_p_value,
                     col_text_bayes_factor) = main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
                    col_text_effect_size =  main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

                    if settings['plot_settings']['use_data'] == main.tr('Frequency'):
                        wordless_plot_freq.wordless_plot_freq_ref(main, keywords_freq_files,
                                                                  ref_file = ref_file,
                                                                  settings = settings['plot_settings'],
                                                                  label_x = main.tr('Keywords'))
                    else:
                        if settings['plot_settings']['use_data'] == col_text_test_stat:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 0]
                                           for keyword, stats_files in keywords_stats_files.items()}

                            label_y = col_text_test_stat
                        elif settings['plot_settings']['use_data'] == col_text_p_value:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 1]
                                           for keyword, stats_files in keywords_stats_files.items()}

                            label_y = col_text_p_value
                        elif settings['plot_settings']['use_data'] == col_text_bayes_factor:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 2]
                                           for keyword, stats_files in keywords_stats_files.items()}

                            label_y = col_text_bayes_factor
                        elif settings['plot_settings']['use_data'] == col_text_effect_size:
                            keywords_stat_files = {keyword: numpy.array(stats_files)[:, 3]
                                           for keyword, stats_files in keywords_stats_files.items()}

                            label_y = col_text_effect_size

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
            wordless_message_box.wordless_message_box_error_ref_file(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message_box.wordless_message_box_missing_ref_file(main)

        wordless_message.wordless_message_generate_plot_error(main)
