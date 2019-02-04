#
# Wordless: Wordlist
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

class Wordless_Table_Wordlist(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Tokens'),
                             main.tr('Number of\nFiles Found')
                         ],
                         headers_num = [
                             main.tr('Rank'),
                             main.tr('Number of\nFiles Found')
                         ],
                         headers_pct = [
                             main.tr('Number of\nFiles Found')
                         ],
                         sorting_enabled = True)

        dialog_search = wordless_dialog.Wordless_Dialog_Search(self.main,
                                                               tab = 'wordlist',
                                                               table = self,
                                                               cols_search = [
                                                                   self.tr('Tokens')
                                                               ])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self.main)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self.main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['wordlist']['filter_settings']

            text_measure_dispersion = self.settings['wordlist']['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = self.settings['wordlist']['generation_settings']['measure_adjusted_freq']

            col_text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
            col_text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

            if settings['filter_file'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total\nFrequency'))
                col_dispersion = self.find_col(self.tr(f'Total\n{col_text_dispersion}'))
                col_adjusted_freq = self.find_col(self.tr(f'Total\n{col_text_adjusted_freq}'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["filter_file"]}]\nFrequency'))
                col_dispersion = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_dispersion}'))
                col_adjusted_freq = self.find_col(self.tr(f'[{settings["filter_file"]}]\n{col_text_adjusted_freq}'))

            col_tokens = self.find_col(self.tr('Tokens'))
            col_number_files_found = self.find_col(self.tr('Number of\nFiles Found'))

            freq_min = (float('-inf')
                        if settings['freq_min_no_limit'] else settings['freq_min'])
            freq_max = (float('inf')
                        if settings['freq_max_no_limit'] else settings['freq_max'])

            dispersion_min = (float('-inf')
                              if settings['dispersion_min_no_limit'] else settings['dispersion_min'])
            dispersion_max = (float('inf')
                              if settings['dispersion_max_no_limit'] else settings['dispersion_max'])

            adjusted_freq_min = (float('-inf')
                                 if settings['adjusted_freq_min_no_limit'] else settings['adjusted_freq_min'])
            adjusted_freq_max = (float('inf')
                                 if settings['adjusted_freq_max_no_limit'] else settings['adjusted_freq_max'])

            len_token_min = (float('-inf')
                             if settings['len_token_min_no_limit'] else settings['len_token_min'])
            len_token_max = (float('inf')
                             if settings['len_token_max_no_limit'] else settings['len_token_max'])

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

                if dispersion_min <= self.item(i, col_dispersion).val <= dispersion_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if adjusted_freq_min <= self.item(i, col_adjusted_freq).val <= adjusted_freq_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if len_token_min <= len(self.item(i, col_tokens).text()) <= len_token_max:
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
            settings = copy.deepcopy(main.settings_default['wordlist'])
        else:
            settings = copy.deepcopy(main.settings_custom['wordlist'])

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
        combo_box_measure_dispersion.setCurrentText(settings['generation_settings']['measure_dispersion'])
        combo_box_measure_adjusted_freq.setCurrentText(settings['generation_settings']['measure_adjusted_freq'])

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

        spin_box_dispersion_min.setValue(settings['filter_settings']['dispersion_min'])
        checkbox_dispersion_min_no_limit.setChecked(settings['filter_settings']['dispersion_min_no_limit'])
        spin_box_dispersion_max.setValue(settings['filter_settings']['dispersion_max'])
        checkbox_dispersion_max_no_limit.setChecked(settings['filter_settings']['dispersion_max_no_limit'])

        spin_box_adjusted_freq_min.setValue(settings['filter_settings']['adjusted_freq_min'])
        checkbox_adjusted_freq_min_no_limit.setChecked(settings['filter_settings']['adjusted_freq_min_no_limit'])
        spin_box_adjusted_freq_max.setValue(settings['filter_settings']['adjusted_freq_max'])
        checkbox_adjusted_freq_max_no_limit.setChecked(settings['filter_settings']['adjusted_freq_max_no_limit'])

        spin_box_len_token_min.setValue(settings['filter_settings']['len_token_min'])
        checkbox_len_token_min_no_limit.setChecked(settings['filter_settings']['len_token_min_no_limit'])
        spin_box_len_token_max.setValue(settings['filter_settings']['len_token_max'])
        checkbox_len_token_max_no_limit.setChecked(settings['filter_settings']['len_token_max_no_limit'])

        spin_box_number_files_found_min.setValue(settings['filter_settings']['number_files_found_min'])
        checkbox_number_files_found_min_no_limit.setChecked(settings['filter_settings']['number_files_found_min_no_limit'])
        spin_box_number_files_found_max.setValue(settings['filter_settings']['number_files_found_max'])
        checkbox_number_files_found_max_no_limit.setChecked(settings['filter_settings']['number_files_found_max_no_limit'])

        combo_box_filter_file.setCurrentText(settings['filter_settings']['filter_file'])

        token_settings_changed()
        generation_settings_changed()
        measures_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['wordlist']['token_settings']

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
        settings = main.settings_custom['wordlist']['generation_settings']

        settings['measure_dispersion'] = combo_box_measure_dispersion.currentText()
        settings['measure_adjusted_freq'] = combo_box_measure_adjusted_freq.currentText()

    def measures_changed():
        settings = main.settings_custom['wordlist']['generation_settings']

        # Use Data
        use_data_old = combo_box_use_data.currentText()

        text_measure_dispersion = settings['measure_dispersion']
        text_measure_adjusted_freq = settings['measure_adjusted_freq']

        combo_box_use_data.clear()

        combo_box_use_data.addItem(main.tr('Frequency'))
        combo_box_use_data.addItem(main.settings_global['measures_dispersion'][text_measure_dispersion]['col'])
        combo_box_use_data.addItem(main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(main.settings_default['wordlist']['plot_settings']['use_data'])

    def table_settings_changed():
        settings = main.settings_custom['wordlist']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        settings = main.settings_custom['wordlist']['plot_settings']

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
        settings = main.settings_custom['wordlist']['filter_settings']

        settings['freq_min'] = spin_box_freq_min.value()
        settings['freq_min_no_limit'] = checkbox_freq_min_no_limit.isChecked()
        settings['freq_max'] = spin_box_freq_max.value()
        settings['freq_max_no_limit'] = checkbox_freq_max_no_limit.isChecked()

        settings['dispersion_min'] = spin_box_dispersion_min.value()
        settings['dispersion_min_no_limit'] = checkbox_dispersion_min_no_limit.isChecked()
        settings['dispersion_max'] = spin_box_dispersion_max.value()
        settings['dispersion_max_no_limit'] = checkbox_dispersion_max_no_limit.isChecked()

        settings['adjusted_freq_min'] = spin_box_adjusted_freq_min.value()
        settings['adjusted_freq_min_no_limit'] = checkbox_adjusted_freq_min_no_limit.isChecked()
        settings['adjusted_freq_max'] = spin_box_adjusted_freq_max.value()
        settings['adjusted_freq_max_no_limit'] = checkbox_adjusted_freq_max_no_limit.isChecked()

        settings['len_token_min'] = spin_box_len_token_min.value()
        settings['len_token_min_no_limit'] = checkbox_len_token_min_no_limit.isChecked()
        settings['len_token_max'] = spin_box_len_token_max.value()
        settings['len_token_max_no_limit'] = checkbox_len_token_max_no_limit.isChecked()

        settings['number_files_found_min'] = spin_box_number_files_found_min.value()
        settings['number_files_found_min_no_limit'] = checkbox_number_files_found_min_no_limit.isChecked()
        settings['number_files_found_max'] = spin_box_number_files_found_max.value()
        settings['number_files_found_max_no_limit'] = checkbox_number_files_found_max_no_limit.isChecked()

        settings['filter_file'] = combo_box_filter_file.currentText()

    def table_item_changed():
        settings = table_wordlist.settings['wordlist']

        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        col_text_adjusted_freq =  main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        label_dispersion.setText(f'{col_text_dispersion}:')
        label_adjusted_freq.setText(f'{col_text_adjusted_freq}:')

    tab_wordlist = wordless_layout.Wordless_Tab(main, load_settings)

    table_wordlist = Wordless_Table_Wordlist(main)

    tab_wordlist.layout_table.addWidget(table_wordlist.label_number_results, 0, 0)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_search_results, 0, 4)
    tab_wordlist.layout_table.addWidget(table_wordlist, 1, 0, 1, 5)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_generate_table, 2, 0)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_generate_plot, 2, 1)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_export_selected, 2, 2)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_export_all, 2, 3)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_clear, 2, 4)

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

    (label_measure_dispersion,
     combo_box_measure_dispersion) = wordless_widgets.wordless_widgets_measure_dispersion(main)
    (label_measure_adjusted_freq,
     combo_box_measure_adjusted_freq) = wordless_widgets.wordless_widgets_measure_adjusted_freq(main)

    (label_settings_measures,
     button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(main,
                                                                                     tab = main.tr('Dispersion'))

    combo_box_measure_dispersion.currentTextChanged.connect(generation_settings_changed)
    combo_box_measure_dispersion.currentTextChanged.connect(measures_changed)
    combo_box_measure_adjusted_freq.currentTextChanged.connect(generation_settings_changed)
    combo_box_measure_adjusted_freq.currentTextChanged.connect(measures_changed)

    layout_settings_measures = QGridLayout()
    layout_settings_measures.addWidget(label_settings_measures, 0, 0)
    layout_settings_measures.addWidget(button_settings_measures, 0, 1)

    layout_settings_measures.setColumnStretch(1, 1)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_measure_dispersion, 0, 0)
    group_box_generation_settings.layout().addWidget(combo_box_measure_dispersion, 1, 0)
    group_box_generation_settings.layout().addWidget(label_measure_adjusted_freq, 2, 0)
    group_box_generation_settings.layout().addWidget(combo_box_measure_adjusted_freq, 3, 0)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 4, 0)

    group_box_generation_settings.layout().addLayout(layout_settings_measures, 5, 0)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_wordlist)

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

    label_dispersion = QLabel(main.tr('Dispersion:'), main)
    (label_dispersion_min,
     spin_box_dispersion_min,
     checkbox_dispersion_min_no_limit,
     label_dispersion_max,
     spin_box_dispersion_max,
     checkbox_dispersion_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(main, filter_min = 0, filter_max = 1)

    label_adjusted_freq = QLabel(main.tr('Adjusted Frequency:'), main)
    (label_adjusted_freq_min,
     spin_box_adjusted_freq_min,
     checkbox_adjusted_freq_min_no_limit,
     label_adjusted_freq_max,
     spin_box_adjusted_freq_max,
     checkbox_adjusted_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_len_token = QLabel(main.tr('Token Length:'), main)
    (label_len_token_min,
     spin_box_len_token_min,
     checkbox_len_token_min_no_limit,
     label_len_token_max,
     spin_box_len_token_max,
     checkbox_len_token_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100)

    label_number_files_found = QLabel(main.tr('Number of Files Found:'), main)
    (label_number_files_found_min,
     spin_box_number_files_found_min,
     checkbox_number_files_found_min_no_limit,
     label_number_files_found_max,
     spin_box_number_files_found_max,
     checkbox_number_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    (label_filter_file,
     combo_box_filter_file,
     button_filter_results) = wordless_widgets.wordless_widgets_filter_results(main, table_wordlist)

    spin_box_freq_min.valueChanged.connect(filter_settings_changed)
    checkbox_freq_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_max.valueChanged.connect(filter_settings_changed)
    checkbox_freq_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_dispersion_min.valueChanged.connect(filter_settings_changed)
    checkbox_dispersion_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_dispersion_max.valueChanged.connect(filter_settings_changed)
    checkbox_dispersion_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_adjusted_freq_min.valueChanged.connect(filter_settings_changed)
    checkbox_adjusted_freq_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_adjusted_freq_max.valueChanged.connect(filter_settings_changed)
    checkbox_adjusted_freq_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_len_token_min.valueChanged.connect(filter_settings_changed)
    checkbox_len_token_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_token_max.valueChanged.connect(filter_settings_changed)
    checkbox_len_token_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_number_files_found_min.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_number_files_found_max.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_max_no_limit.stateChanged.connect(filter_settings_changed)

    combo_box_filter_file.currentTextChanged.connect(filter_settings_changed)

    table_wordlist.itemChanged.connect(table_item_changed)

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

    group_box_filter_settings.layout().addWidget(label_dispersion, 4, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_dispersion_min, 5, 0)
    group_box_filter_settings.layout().addWidget(spin_box_dispersion_min, 5, 1)
    group_box_filter_settings.layout().addWidget(checkbox_dispersion_min_no_limit, 5, 2)
    group_box_filter_settings.layout().addWidget(label_dispersion_max, 6, 0)
    group_box_filter_settings.layout().addWidget(spin_box_dispersion_max, 6, 1)
    group_box_filter_settings.layout().addWidget(checkbox_dispersion_max_no_limit, 6, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 7, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_adjusted_freq, 8, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_adjusted_freq_min, 9, 0)
    group_box_filter_settings.layout().addWidget(spin_box_adjusted_freq_min, 9, 1)
    group_box_filter_settings.layout().addWidget(checkbox_adjusted_freq_min_no_limit, 9, 2)
    group_box_filter_settings.layout().addWidget(label_adjusted_freq_max, 10, 0)
    group_box_filter_settings.layout().addWidget(spin_box_adjusted_freq_max, 10, 1)
    group_box_filter_settings.layout().addWidget(checkbox_adjusted_freq_max_no_limit, 10, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 11, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_len_token, 12, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_len_token_min, 13, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_token_min, 13, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_token_min_no_limit, 13, 2)
    group_box_filter_settings.layout().addWidget(label_len_token_max, 14, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_token_max, 14, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_token_max_no_limit, 14, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 15, 0, 1, 3)

    group_box_filter_settings.layout().addWidget(label_number_files_found, 16, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_number_files_found_min, 17, 0)
    group_box_filter_settings.layout().addWidget(spin_box_number_files_found_min, 17, 1)
    group_box_filter_settings.layout().addWidget(checkbox_number_files_found_min_no_limit, 17, 2)
    group_box_filter_settings.layout().addWidget(label_number_files_found_max, 18, 0)
    group_box_filter_settings.layout().addWidget(spin_box_number_files_found_max, 18, 1)
    group_box_filter_settings.layout().addWidget(checkbox_number_files_found_max_no_limit, 18, 2)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 19, 0, 1, 3)

    group_box_filter_settings.layout().addLayout(layout_filter_file, 20, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(button_filter_results, 21, 0, 1, 3)

    group_box_filter_settings.layout().setColumnStretch(1, 1)

    tab_wordlist.layout_settings.addWidget(group_box_token_settings, 0, 0)
    tab_wordlist.layout_settings.addWidget(group_box_generation_settings, 1, 0)
    tab_wordlist.layout_settings.addWidget(group_box_table_settings, 2, 0)
    tab_wordlist.layout_settings.addWidget(group_box_plot_settings, 3, 0)
    tab_wordlist.layout_settings.addWidget(group_box_filter_settings, 4, 0)

    tab_wordlist.layout_settings.setRowStretch(5, 1)

    load_settings()

    return tab_wordlist

def generate_wordlists(main, files):
    texts = []
    tokens_freq_files = []
    tokens_stats_files = []

    settings = main.settings_custom['wordlist']

    # Frequency
    for file in files:
        text = wordless_text.Wordless_Text(main, file)

        tokens = wordless_token_processing.wordless_preprocess_tokens_wordlist(text,
                                                                               token_settings = settings['token_settings'])

        texts.append(text)
        tokens_freq_files.append(collections.Counter(tokens))

    # Total
    if len(files) > 1:
        text_total = wordless_text.Wordless_Text(main, files[0])
        text_total.tokens = [token for text in texts for token in text.tokens]

        texts.append(text_total)
        tokens_freq_files.append(sum(tokens_freq_files, collections.Counter()))

    # Dispersion & Adjusted Frequency
    text_measure_dispersion = settings['generation_settings']['measure_dispersion']
    text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

    measure_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['func']
    measure_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['func']

    tokens_total = tokens_freq_files[-1].keys()

    for text in texts:
        tokens_stats_file = {}

        # Dispersion
        number_sections = main.settings_custom['measures']['dispersion']['general']['number_sections']

        sections_freq = [collections.Counter(section)
                         for section in wordless_text_utils.to_sections(text.tokens, number_sections)]

        for token in tokens_total:
            counts = [section_freq[token] for section_freq in sections_freq]

            tokens_stats_file[token] = [measure_dispersion(counts)]

        # Adjusted Frequency
        if not main.settings_custom['measures']['adjusted_freq']['general']['use_same_settings_dispersion']:
            number_sections = main.settings_custom['measures']['adjusted_freq']['general']['number_sections']

            sections_freq = [collections.Counter(section)
                             for section in wordless_text_utils.to_sections(text.tokens, number_sections)]

        for token in tokens_total:
            counts = [section_freq[token] for section_freq in sections_freq]

            tokens_stats_file[token].append(measure_adjusted_freq(counts))

        tokens_stats_files.append(tokens_stats_file)

    if len(files) == 1:
        tokens_freq_files *= 2
        tokens_stats_files *= 2

    return (wordless_misc.merge_dicts(tokens_freq_files),
            wordless_misc.merge_dicts(tokens_stats_files))

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['wordlist']

    files = wordless_checking_file.check_files_loading(main, main.wordless_files.get_selected_files())

    if files:
        tokens_freq_files, tokens_stats_files = generate_wordlists(main, files)

        if tokens_freq_files:
            table.clear_table()

            table.settings = copy.deepcopy(main.settings_custom)

            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
            col_text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

            table.blockSignals(True)
            table.setSortingEnabled(False)
            table.setUpdatesEnabled(False)

            if settings['token_settings']['tags_only']:
                table.setHorizontalHeaderLabels([
                    main.tr('Rank'),
                    main.tr('Tags'),
                    main.tr('Number of\nFiles Found')
                ])

            # Insert Columns (Files)
            for file in files:
                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\nFrequency'),
                                 num = True, pct = True, cumulative = True, breakdown = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\n{col_text_dispersion}'),
                                 num = True, breakdown = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\n{col_text_adjusted_freq}'),
                                 num = True, breakdown = True)

            # Insert Columns (Total)
            table.insert_col(table.columnCount() - 1,
                             main.tr('Total\nFrequency'),
                             num = True, pct = True, cumulative = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'Total\n{col_text_dispersion}'),
                             num = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'Total\n{col_text_adjusted_freq}'),
                             num = True)

            # Sort by frequency of the first file
            table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\nFrequency')), Qt.DescendingOrder)

            cols_freq = table.find_cols(main.tr('\nFrequency'))
            cols_dispersion = table.find_cols(main.tr(f'\n{col_text_dispersion}'))
            cols_adjusted_freq = table.find_cols(main.tr(f'\n{col_text_adjusted_freq}'))
            col_files_found = table.find_col(main.tr('Number of\nFiles Found'))

            len_files = len(files)

            table.setRowCount(len(tokens_freq_files))

            for i, (token, freq_files) in enumerate(wordless_sorting.sorted_tokens_freq_files(tokens_freq_files)):
                stats_files = tokens_stats_files[token]

                # Rank
                table.set_item_num_int(i, 0, -1)

                # Tokens
                table.setItem(i, 1, wordless_table.Wordless_Table_Item(token))

                # Frequency
                for j, freq in enumerate(freq_files):
                    table.set_item_num_cumulative(i, cols_freq[j], freq)

                for j, (dispersion, adjusted_freq) in enumerate(stats_files):
                    # Dispersion
                    table.set_item_num_float(i, cols_dispersion[j], dispersion)

                    # Adjusted Frequency
                    table.set_item_num_float(i, cols_adjusted_freq[j], adjusted_freq)

                # Number of Files Found
                table.set_item_num_pct(i, col_files_found,
                                       len([freq for freq in freq_files[:-1] if freq]),
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
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['wordlist']

    files = wordless_checking_file.check_files_loading(main, main.wordless_files.get_selected_files())

    if files:
        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        col_text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']
        
        tokens_freq_files, tokens_stats_files = generate_wordlists(main, files)

        if settings['plot_settings']['use_data'] == main.tr('Frequency'):
            wordless_plot_freq.wordless_plot_freq(main, tokens_freq_files,
                                                  settings = settings['plot_settings'],
                                                  label_x = main.tr('Tokens'))
        else:
            if settings['plot_settings']['use_data'] == col_text_dispersion:
                tokens_stat_files = {token: numpy.array(stats_files)[:, 0]
                                     for token, stats_files in tokens_stats_files.items()}

                label_y = col_text_dispersion
            elif settings['plot_settings']['use_data'] == col_text_adjusted_freq:
                tokens_stat_files = {token: numpy.array(stats_files)[:, 1]
                                     for token, stats_files in tokens_stats_files.items()}

                label_y = col_text_adjusted_freq

            wordless_plot_stat.wordless_plot_stat(main, tokens_stat_files,
                                                  settings = settings['plot_settings'],
                                                  label_x = main.tr('Tokens'),
                                                  label_y = label_y)

        wordless_message.wordless_message_generate_plot_success(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_plot_error(main)
