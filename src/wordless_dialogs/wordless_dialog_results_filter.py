#
# Wordless: Dialogs - Filter Results
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog, wordless_dialog_misc
from wordless_utils import wordless_misc, wordless_threading
from wordless_widgets import (wordless_box, wordless_button, wordless_layout,
                              wordless_msg, wordless_widgets)

class Wordless_Worker_Results_Filter_Wordlist(wordless_threading.Wordless_Worker):
    def run(self):
        text_measure_dispersion = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        if self.dialog.tab == 'wordlist':
            col_token = self.dialog.table.find_col(self.tr('Token'))
        elif self.dialog.tab == 'ngram':
            col_ngram = self.dialog.table.find_col(self.tr('N-gram'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            col_freq = self.dialog.table.find_col(
                self.tr('Total\nFrequency')
            )
            col_dispersion = self.dialog.table.find_col(
                self.tr(f'Total\n{text_dispersion}')
            )
            col_adjusted_freq = self.dialog.table.find_col(
                self.tr(f'Total\n{text_adjusted_freq}')
            )
        else:
            col_freq = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\nFrequency")
            )
            col_dispersion = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_dispersion}")
            )
            col_adjusted_freq = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_adjusted_freq}")
            )

        col_num_files_found = self.dialog.table.find_col(self.tr('Number of\nFiles Found'))

        if self.dialog.tab == 'wordlist':
            len_token_min = (float('-inf')
                             if self.dialog.settings['len_token_min_no_limit']
                             else self.dialog.settings['len_token_min'])
            len_token_max = (float('inf')
                             if self.dialog.settings['len_token_max_no_limit']
                             else self.dialog.settings['len_token_max'])
        elif self.dialog.tab == 'ngram':
            len_ngram_min = (float('-inf')
                             if self.dialog.settings['len_ngram_min_no_limit']
                             else self.dialog.settings['len_ngram_min'])
            len_ngram_max = (float('inf')
                             if self.dialog.settings['len_ngram_max_no_limit']
                             else self.dialog.settings['len_ngram_max'])

        freq_min = (float('-inf')
                    if self.dialog.settings['freq_min_no_limit']
                    else self.dialog.settings['freq_min'])
        freq_max = (float('inf')
                    if self.dialog.settings['freq_max_no_limit']
                    else self.dialog.settings['freq_max'])

        dispersion_min = (float('-inf')
                          if self.dialog.settings['dispersion_min_no_limit']
                          else self.dialog.settings['dispersion_min'])
        dispersion_max = (float('inf')
                          if self.dialog.settings['dispersion_max_no_limit']
                          else self.dialog.settings['dispersion_max'])

        adjusted_freq_min = (float('-inf')
                             if self.dialog.settings['adjusted_freq_min_no_limit']
                             else self.dialog.settings['adjusted_freq_min'])
        adjusted_freq_max = (float('inf')
                             if self.dialog.settings['adjusted_freq_max_no_limit']
                             else self.dialog.settings['adjusted_freq_max'])

        num_files_found_min = (float('-inf')
                               if self.dialog.settings['num_files_found_min_no_limit']
                               else self.dialog.settings['num_files_found_min'])
        num_files_found_max = (float('inf')
                               if self.dialog.settings['num_files_found_max_no_limit']
                               else self.dialog.settings['num_files_found_max'])

        self.dialog.table.row_filters = []

        if self.dialog.tab == 'wordlist':
            for i in range(self.dialog.table.rowCount()):
                if (len_token_min       <= len(self.dialog.table.item(i, col_token).text())   <= len_token_max and
                    freq_min            <= self.dialog.table.item(i, col_freq).val            <= freq_max and
                    dispersion_min      <= self.dialog.table.item(i, col_dispersion).val      <= dispersion_max and
                    adjusted_freq_min   <= self.dialog.table.item(i, col_adjusted_freq).val   <= adjusted_freq_max and
                    num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val <= num_files_found_max):
                    self.dialog.table.row_filters.append(True)
                else:
                    self.dialog.table.row_filters.append(False)
        elif self.dialog.tab == 'ngram':
            for i in range(self.dialog.table.rowCount()):
                if (len_ngram_min       <= len(self.dialog.table.item(i, col_ngram).text())   <= len_ngram_max and
                    freq_min            <= self.dialog.table.item(i, col_freq).val            <= freq_max and
                    dispersion_min      <= self.dialog.table.item(i, col_dispersion).val      <= dispersion_max and
                    adjusted_freq_min   <= self.dialog.table.item(i, col_adjusted_freq).val   <= adjusted_freq_max and
                    num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val <= num_files_found_max):
                    self.dialog.table.row_filters.append(True)
                else:
                    self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wordless_Worker_Results_Filter_Collocation(wordless_threading.Wordless_Worker):
    def run(self):
        text_test_significance = self.dialog.table.settings['collocation']['generation_settings']['test_significance']
        text_measure_effect_size = self.dialog.table.settings['collocation']['generation_settings']['measure_effect_size']

        (text_test_stat,
         text_p_value,
         text_bayes_factor) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

        col_collocate = self.dialog.table.find_col(self.tr('Collocate'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_col(
                    self.tr('Total\nFrequency')
                )
            else:
                col_freq = self.dialog.table.find_col(
                    self.tr(f'Total\n{self.dialog.settings["freq_position"]}')
                )

            col_test_stat = self.dialog.table.find_col(
                self.tr(f'Total\n{text_test_stat}')
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f'Total\n{text_p_value}')
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f'Total\n{text_bayes_factor}')
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f'Total\n{text_effect_size}')
            )
        else:
            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_col(
                    self.tr(f"[{self.dialog.settings['file_to_filter']}]\nFrequency")
                )
            else:
                col_freq = self.dialog.table.find_col(
                    self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.settings['freq_position']}")
                )

            col_test_stat = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_test_stat}")
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_p_value}")
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_bayes_factor}")
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_effect_size}")
            )

        col_num_files_found = self.dialog.table.find_col(self.tr('Number of\nFiles Found'))

        len_collocate_min = (float('-inf')
                             if self.dialog.settings['len_collocate_min_no_limit']
                             else self.dialog.settings['len_collocate_min'])
        len_collocate_max = (float('inf')
                             if self.dialog.settings['len_collocate_max_no_limit']
                             else self.dialog.settings['len_collocate_max'])

        freq_min = (float('-inf')
                    if self.dialog.settings['freq_min_no_limit']
                    else self.dialog.settings['freq_min'])
        freq_max = (float('inf')
                    if self.dialog.settings['freq_max_no_limit']
                    else self.dialog.settings['freq_max'])

        test_stat_min = (float('-inf')
                         if self.dialog.settings['test_stat_min_no_limit']
                         else self.dialog.settings['test_stat_min'])
        test_stat_max = (float('inf')
                         if self.dialog.settings['test_stat_max_no_limit']
                         else self.dialog.settings['test_stat_max'])

        p_value_min = (float('-inf')
                       if self.dialog.settings['p_value_min_no_limit']
                       else self.dialog.settings['p_value_min'])
        p_value_max = (float('inf')
                       if self.dialog.settings['p_value_max_no_limit']
                       else self.dialog.settings['p_value_max'])

        bayes_factor_min = (float('-inf')
                            if self.dialog.settings['bayes_factor_min_no_limit']
                            else self.dialog.settings['bayes_factor_min'])
        bayes_factor_max = (float('inf')
                            if self.dialog.settings['bayes_factor_max_no_limit']
                            else self.dialog.settings['bayes_factor_max'])

        effect_size_min = (float('-inf')
                           if self.dialog.settings['effect_size_min_no_limit']
                           else self.dialog.settings['effect_size_min'])
        effect_size_max = (float('inf')
                           if self.dialog.settings['effect_size_max_no_limit']
                           else self.dialog.settings['effect_size_max'])

        num_files_found_min = (float('-inf')
                               if self.dialog.settings['num_files_found_min_no_limit']
                               else self.dialog.settings['num_files_found_min'])
        num_files_found_max = (float('inf')
                               if self.dialog.settings['num_files_found_max_no_limit']
                               else self.dialog.settings['num_files_found_max'])

        self.dialog.table.row_filters = []

        for i in range(self.dialog.table.rowCount()):
            if text_test_stat:
                filter_test_stat = test_stat_min <= self.dialog.table.item(i, col_test_stat).val <= test_stat_max
            else:
                filter_test_stat = True

            if text_bayes_factor:
                filter_bayes_factor = bayes_factor_min <= self.dialog.table.item(i, col_bayes_factor).val <= bayes_factor_max
            else:
                filter_bayes_factor = True

            if (len_collocate_min   <= len(self.dialog.table.item(i, col_collocate).text())  <= len_collocate_max and
                freq_min            <= self.dialog.table.item(i, col_freq).val               <= freq_max and
                filter_test_stat and
                p_value_min         <= self.dialog.table.item(i, col_p_value).val            <= p_value_max and
                filter_bayes_factor and
                effect_size_min     <= self.dialog.table.item(i, col_effect_size).val        <= effect_size_max and
                num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val    <= num_files_found_max):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wordless_Worker_Results_Filter_Keywords(wordless_threading.Wordless_Worker):
    def run(self):
        text_test_significance = self.dialog.table.settings['keywords']['generation_settings']['test_significance']
        text_measure_effect_size = self.dialog.table.settings['keywords']['generation_settings']['measure_effect_size']

        (text_test_stat,
         text_p_value,
         text_bayes_factor) = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

        col_keywords = self.dialog.table.find_col(self.tr('Keywords'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            col_freq = self.dialog.table.find_col(
                self.tr('Total\nFrequency')
            )
            col_test_stat = self.dialog.table.find_col(
                self.tr(f'Total\n{text_test_stat}')
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f'Total\n{text_p_value}')
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f'Total\n{text_bayes_factor}')
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f'Total\n{text_effect_size}')
            )
        else:
            col_freq = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\nFrequency")
            )
            col_test_stat = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_test_stat}")
            )
            col_p_value = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_p_value}")
            )
            col_bayes_factor = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_bayes_factor}")
            )
            col_effect_size = self.dialog.table.find_col(
                self.tr(f"[{self.dialog.settings['file_to_filter']}]\n{text_effect_size}")
            )

        col_num_files_found = self.dialog.table.find_col(self.tr('Number of\nFiles Found'))

        len_keyword_min = (float('-inf')
                           if self.dialog.settings['len_keyword_min_no_limit']
                           else self.dialog.settings['len_keyword_min'])
        len_keyword_max = (float('inf')
                           if self.dialog.settings['len_keyword_max_no_limit']
                           else self.dialog.settings['len_keyword_max'])

        freq_min = (float('-inf')
                    if self.dialog.settings['freq_min_no_limit']
                    else self.dialog.settings['freq_min'])
        freq_max = (float('inf')
                    if self.dialog.settings['freq_max_no_limit']
                    else self.dialog.settings['freq_max'])

        test_stat_min = (float('-inf')
                         if self.dialog.settings['test_stat_min_no_limit']
                         else self.dialog.settings['test_stat_min'])
        test_stat_max = (float('inf')
                         if self.dialog.settings['test_stat_max_no_limit']
                         else self.dialog.settings['test_stat_max'])

        p_value_min = (float('-inf')
                       if self.dialog.settings['p_value_min_no_limit']
                       else self.dialog.settings['p_value_min'])
        p_value_max = (float('inf')
                       if self.dialog.settings['p_value_max_no_limit']
                       else self.dialog.settings['p_value_max'])

        bayes_factor_min = (float('-inf')
                            if self.dialog.settings['bayes_factor_min_no_limit']
                            else self.dialog.settings['bayes_factor_min'])
        bayes_factor_max = (float('inf')
                            if self.dialog.settings['bayes_factor_max_no_limit']
                            else self.dialog.settings['bayes_factor_max'])

        effect_size_min = (float('-inf')
                           if self.dialog.settings['effect_size_min_no_limit']
                           else self.dialog.settings['effect_size_min'])
        effect_size_max = (float('inf')
                           if self.dialog.settings['effect_size_max_no_limit']
                           else self.dialog.settings['effect_size_max'])

        num_files_found_min = (float('-inf')
                               if self.dialog.settings['num_files_found_min_no_limit']
                               else self.dialog.settings['num_files_found_min'])
        num_files_found_max = (float('inf')
                               if self.dialog.settings['num_files_found_max_no_limit']
                               else self.dialog.settings['nur_files_found_max'])

        self.dialog.table.row_filters = []

        for i in range(self.dialog.table.rowCount()):
            if text_test_stat:
                filter_test_stat = test_stat_min <= self.dialog.table.item(i, col_test_stat).val <= test_stat_max
            else:
                filter_test_stat = True

            if text_bayes_factor:
                filter_bayes_factor = bayes_factor_min <= self.dialog.table.item(i, col_bayes_factor).val <= bayes_factor_max
            else:
                filter_bayes_factor = True

            if (len_keyword_min     <= len(self.dialog.table.item(i, col_keywords).text()) <= len_keyword_max and
                freq_min            <= self.dialog.table.item(i, col_freq).val             <= freq_max and
                filter_test_stat and
                p_value_min         <= self.dialog.table.item(i, col_p_value).val          <= p_value_max and
                filter_bayes_factor and
                effect_size_min     <= self.dialog.table.item(i, col_effect_size).val      <= effect_size_max and
                num_files_found_min <= self.dialog.table.item(i, col_num_files_found).val  <= num_files_found_max):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table ...'))

        time.sleep(0.1)

        self.worker_done.emit()

class Wordless_Dialog_Results_Filter(wordless_dialog.Wordless_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, main.tr('Filter Results'))

        self.tab = tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['filter_results']

        self.label_file_to_filter = QLabel(self.tr('File to Filter:'), self)
        self.combo_box_file_to_filter = wordless_box.Wordless_Combo_Box_File_To_Filter(self, self.table)
        self.button_filter = QPushButton(self.tr('Filter'), self)

        self.button_reset_settings = wordless_button.Wordless_Button_Reset_Settings(self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.button_filter.setFixedWidth(80)
        self.button_reset_settings.setFixedWidth(120)
        self.button_close.setFixedWidth(80)

        self.combo_box_file_to_filter.currentTextChanged.connect(self.file_to_filter_changed)
        self.button_filter.clicked.connect(lambda: self.filter_results())

        self.button_close.clicked.connect(self.reject)

        self.main.wordless_work_area.currentChanged.connect(self.reject)

        layout_file_to_filter = wordless_layout.Wordless_Layout()
        layout_file_to_filter.addWidget(self.label_file_to_filter, 0, 0)
        layout_file_to_filter.addWidget(self.combo_box_file_to_filter, 0, 1)
        layout_file_to_filter.addWidget(self.button_filter, 0, 2)

        layout_file_to_filter.setColumnStretch(1, 1)

        self.layout_filters = wordless_layout.Wordless_Layout()

        layout_buttons = wordless_layout.Wordless_Layout()
        layout_buttons.addWidget(self.button_reset_settings, 0, 0)
        layout_buttons.addWidget(self.button_close, 0, 1, Qt.AlignRight)

        self.setLayout(wordless_layout.Wordless_Layout())
        self.layout().addLayout(layout_file_to_filter, 0, 0)
        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 1, 0)
        self.layout().addLayout(self.layout_filters, 2, 0)
        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0)
        self.layout().addLayout(layout_buttons, 4, 0)

        self.set_fixed_size()

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.settings_default[self.tab]['filter_results']
        else:
            settings = self.settings

        self.combo_box_file_to_filter.setCurrentText(settings['file_to_filter'])

    def file_to_filter_changed(self):
        self.settings['file_to_filter'] = self.combo_box_file_to_filter.currentText()

    def filter_results(self):
        pass

class Wordless_Dialog_Results_Filter_Wordlist(Wordless_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        if self.tab == 'wordlist':
            self.label_len_token = QLabel(self.tr('Token Length:'), self)
            (self.label_len_token_min,
             self.spin_box_len_token_min,
             self.checkbox_len_token_min_no_limit,
             self.label_len_token_max,
             self.spin_box_len_token_max,
             self.checkbox_len_token_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 1,
                                                                                              filter_max = 100)
        elif self.tab == 'ngram':
            self.label_len_ngram = QLabel(self.tr('N-gram Length:'), self)
            (self.label_len_ngram_min,
             self.spin_box_len_ngram_min,
             self.checkbox_len_ngram_min_no_limit,
             self.label_len_ngram_max,
             self.spin_box_len_ngram_max,
             self.checkbox_len_ngram_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 1,
                                                                                              filter_max = 100)

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (self.label_freq_min,
         self.spin_box_freq_min,
         self.checkbox_freq_min_no_limit,
         self.label_freq_max,
         self.spin_box_freq_max,
         self.checkbox_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 0,
                                                                                     filter_max = 1000000)

        self.label_dispersion = QLabel(self.tr('Dispersion:'), self)
        (self.label_dispersion_min,
         self.spin_box_dispersion_min,
         self.checkbox_dispersion_min_no_limit,
         self.label_dispersion_max,
         self.spin_box_dispersion_max,
         self.checkbox_dispersion_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self,
                                                                                                    filter_min = 0,
                                                                                                    filter_max = 1)

        self.label_adjusted_freq = QLabel(self.tr('Adjusted Frequency:'), self)
        (self.label_adjusted_freq_min,
         self.spin_box_adjusted_freq_min,
         self.checkbox_adjusted_freq_min_no_limit,
         self.label_adjusted_freq_max,
         self.spin_box_adjusted_freq_max,
         self.checkbox_adjusted_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 0,
                                                                                              filter_max = 1000000)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_num_files_found_min,
         self.spin_box_num_files_found_min,
         self.checkbox_num_files_found_min_no_limit,
         self.label_num_files_found_max,
         self.spin_box_num_files_found_max,
         self.checkbox_num_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                filter_min = 1,
                                                                                                filter_max = 100000)

        if self.tab == 'wordlist':
            self.spin_box_len_token_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_token_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_max_no_limit.stateChanged.connect(self.filters_changed)
        elif self.tab == 'ngram':
            self.spin_box_len_ngram_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_ngram_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_dispersion_min.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_dispersion_max.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_adjusted_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_adjusted_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        if self.tab == 'wordlist':
            self.layout_filters.addWidget(self.label_len_token, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_token_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_token_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_max_no_limit, 2, 2)
        elif self.tab == 'ngram':
            self.layout_filters.addWidget(self.label_len_ngram, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_ngram_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_ngram_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_dispersion, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_dispersion_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_dispersion_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_adjusted_freq, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_adjusted_freq_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_adjusted_freq_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 8, 2)

        self.layout_filters.addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 3, 9, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        if self.tab == 'wordlist':
            self.spin_box_len_token_min.setValue(settings['len_token_min'])
            self.checkbox_len_token_min_no_limit.setChecked(settings['len_token_min_no_limit'])
            self.spin_box_len_token_max.setValue(settings['len_token_max'])
            self.checkbox_len_token_max_no_limit.setChecked(settings['len_token_max_no_limit'])
        elif self.tab == 'ngram':
            self.spin_box_len_ngram_min.setValue(settings['len_ngram_min'])
            self.checkbox_len_ngram_min_no_limit.setChecked(settings['len_ngram_min_no_limit'])
            self.spin_box_len_ngram_max.setValue(settings['len_ngram_max'])
            self.checkbox_len_ngram_max_no_limit.setChecked(settings['len_ngram_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_dispersion_min.setValue(settings['dispersion_min'])
        self.checkbox_dispersion_min_no_limit.setChecked(settings['dispersion_min_no_limit'])
        self.spin_box_dispersion_max.setValue(settings['dispersion_max'])
        self.checkbox_dispersion_max_no_limit.setChecked(settings['dispersion_max_no_limit'])

        self.spin_box_adjusted_freq_min.setValue(settings['adjusted_freq_min'])
        self.checkbox_adjusted_freq_min_no_limit.setChecked(settings['adjusted_freq_min_no_limit'])
        self.spin_box_adjusted_freq_max.setValue(settings['adjusted_freq_max'])
        self.checkbox_adjusted_freq_max_no_limit.setChecked(settings['adjusted_freq_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        if self.tab == 'wordlist':
            self.settings['len_token_min'] = self.spin_box_len_token_min.value()
            self.settings['len_token_min_no_limit'] = self.checkbox_len_token_min_no_limit.isChecked()
            self.settings['len_token_max'] = self.spin_box_len_token_max.value()
            self.settings['len_token_max_no_limit'] = self.checkbox_len_token_max_no_limit.isChecked()
        elif self.tab == 'ngram':
            self.settings['len_ngram_min'] = self.spin_box_len_ngram_min.value()
            self.settings['len_ngram_min_no_limit'] = self.checkbox_len_ngram_min_no_limit.isChecked()
            self.settings['len_ngram_max'] = self.spin_box_len_ngram_max.value()
            self.settings['len_ngram_max_no_limit'] = self.checkbox_len_ngram_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['dispersion_min'] = self.spin_box_dispersion_min.value()
        self.settings['dispersion_min_no_limit'] = self.checkbox_dispersion_min_no_limit.isChecked()
        self.settings['dispersion_max'] = self.spin_box_dispersion_max.value()
        self.settings['dispersion_max_no_limit'] = self.checkbox_dispersion_max_no_limit.isChecked()

        self.settings['adjusted_freq_min'] = self.spin_box_adjusted_freq_min.value()
        self.settings['adjusted_freq_min_no_limit'] = self.checkbox_adjusted_freq_min_no_limit.isChecked()
        self.settings['adjusted_freq_max'] = self.spin_box_adjusted_freq_max.value()
        self.settings['adjusted_freq_max_no_limit'] = self.checkbox_adjusted_freq_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        self.label_dispersion.setText(f'{text_dispersion}:')
        self.label_adjusted_freq.setText(f'{text_adjusted_freq}:')

    @wordless_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            dialog_progress.accept()

            wordless_msg.wordless_msg_results_filter_success(self.main)

        dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Results_Filter(self.main)

        worker_search_results = Wordless_Worker_Results_Filter_Wordlist(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            dialog = self)
        thread_search_results = wordless_threading.Wordless_Thread(worker_search_results)

        thread_search_results.start()

        dialog_progress.exec_()

        thread_search_results.quit()
        thread_search_results.wait()

class Wordless_Dialog_Results_Filter_Collocation(Wordless_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.label_len_collocate = QLabel(self.tr('Collocate Length:'), self)
        (self.label_len_collocate_min,
         self.spin_box_len_collocate_min,
         self.checkbox_len_collocate_min_no_limit,
         self.label_len_collocate_max,
         self.spin_box_len_collocate_max,
         self.checkbox_len_collocate_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 1,
                                                                                              filter_max = 100)

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        self.combo_box_freq_position = wordless_box.Wordless_Combo_Box(self)
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

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_num_files_found_min,
         self.spin_box_num_files_found_min,
         self.checkbox_num_files_found_min_no_limit,
         self.label_num_files_found_max,
         self.spin_box_num_files_found_max,
         self.checkbox_num_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                filter_min = 1,
                                                                                                filter_max = 100000)

        self.spin_box_len_collocate_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_collocate_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_max_no_limit.stateChanged.connect(self.filters_changed)

        self.combo_box_freq_position.currentTextChanged.connect(self.filters_changed)
        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        layout_freq_position = wordless_layout.Wordless_Layout()
        layout_freq_position.addWidget(self.label_freq, 0, 0)
        layout_freq_position.addWidget(self.combo_box_freq_position, 0, 1, Qt.AlignRight)

        self.layout_filters.addWidget(self.label_len_collocate, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_collocate_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_collocate_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_max_no_limit, 2, 2)

        self.layout_filters.addLayout(layout_freq_position, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_value, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_value_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_value_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_collocate_min.setValue(settings['len_collocate_min'])
        self.checkbox_len_collocate_min_no_limit.setChecked(settings['len_collocate_min_no_limit'])
        self.spin_box_len_collocate_max.setValue(settings['len_collocate_max'])
        self.checkbox_len_collocate_max_no_limit.setChecked(settings['len_collocate_max_no_limit'])

        self.combo_box_freq_position.setCurrentText(settings['freq_position'])
        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_collocate_min'] = self.spin_box_len_collocate_min.value()
        self.settings['len_collocate_min_no_limit'] = self.checkbox_len_collocate_min_no_limit.isChecked()
        self.settings['len_collocate_max'] = self.spin_box_len_collocate_max.value()
        self.settings['len_collocate_max_no_limit'] = self.checkbox_len_collocate_max_no_limit.isChecked()

        self.settings['freq_position'] = self.combo_box_freq_position.currentText()
        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_value_min'] = self.spin_box_p_value_min.value()
        self.settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        self.settings['p_value_max'] = self.spin_box_p_value_max.value()
        self.settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        # Frequency
        freq_position_old = settings['filter_results']['freq_position']

        self.combo_box_freq_position.clear()

        for i in range(settings['generation_settings']['window_left'], settings['generation_settings']['window_right'] + 1):
            if i < 0:
                self.combo_box_freq_position.addItem(f'L{-i}')
            elif i > 0:
                self.combo_box_freq_position.addItem(f'R{i}')

        self.combo_box_freq_position.addItem(self.tr('Total'))

        if self.combo_box_freq_position.findText(freq_position_old) > -1:
            self.combo_box_freq_position.setCurrentText(freq_position_old)
        else:
            self.combo_box_freq_position.setCurrentText(self.main.settings_default['collocation']['filter_results']['freq_position'])

        # Filters
        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (text_test_stat,
         text_p_value,
         text_bayes_factor) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
        text_effect_size =  self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(self.tr('Test Statistic:'))

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

        self.label_effect_size.setText(f'{text_effect_size}:')

    @wordless_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            dialog_progress.accept()

            wordless_msg.wordless_msg_results_filter_success(self.main)

        dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Results_Filter(self.main)

        worker_search_results = Wordless_Worker_Results_Filter_Collocation(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            dialog = self)
        thread_search_results = wordless_threading.Wordless_Thread(worker_search_results)

        thread_search_results.start()

        dialog_progress.exec_()

        thread_search_results.quit()
        thread_search_results.wait()

class Wordless_Dialog_Results_Filter_Keywords(Wordless_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.label_len_keyword = QLabel(self.tr('Keyword Length:'), self)
        (self.label_len_keyword_min,
         self.spin_box_len_keyword_min,
         self.checkbox_len_keyword_min_no_limit,
         self.label_len_keyword_max,
         self.spin_box_len_keyword_max,
         self.checkbox_len_keyword_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                            filter_min = 1,
                                                                                            filter_max = 100)

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

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_num_files_found_min,
         self.spin_box_num_files_found_min,
         self.checkbox_num_files_found_min_no_limit,
         self.label_num_files_found_max,
         self.spin_box_num_files_found_max,
         self.checkbox_num_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                filter_min = 1,
                                                                                                filter_max = 100000)

        self.spin_box_len_keyword_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_keyword_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        self.layout_filters.addWidget(self.label_len_keyword, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_keyword_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_keyword_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_value, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_value_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_value_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_keyword_min.setValue(settings['len_keyword_min'])
        self.checkbox_len_keyword_min_no_limit.setChecked(settings['len_keyword_min_no_limit'])
        self.spin_box_len_keyword_max.setValue(settings['len_keyword_max'])
        self.checkbox_len_keyword_max_no_limit.setChecked(settings['len_keyword_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_keyword_min'] = self.spin_box_len_keyword_min.value()
        self.settings['len_keyword_min_no_limit'] = self.checkbox_len_keyword_min_no_limit.isChecked()
        self.settings['len_keyword_max'] = self.spin_box_len_keyword_max.value()
        self.settings['len_keyword_max_no_limit'] = self.checkbox_len_keyword_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_value_min'] = self.spin_box_p_value_min.value()
        self.settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        self.settings['p_value_max'] = self.spin_box_p_value_max.value()
        self.settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

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
            self.label_test_stat.setText(self.tr('Test Statistic:'))

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

        self.label_effect_size.setText(f'{text_effect_size}:')
        
        self.combo_box_file_to_filter.removeItem(self.combo_box_file_to_filter.findText(ref_file))

    @wordless_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            dialog_progress.accept()

            wordless_msg.wordless_msg_results_filter_success(self.main)

        dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Results_Filter(self.main)

        worker_search_results = Wordless_Worker_Results_Filter_Keywords(
            self.main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            dialog = self)
        thread_search_results = wordless_threading.Wordless_Thread(worker_search_results)

        thread_search_results.start()

        dialog_progress.exec_()

        thread_search_results.quit()
        thread_search_results.wait()
