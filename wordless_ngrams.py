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

class Wordless_Table_Ngrams(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('N-grams'),
                             main.tr('Number of\nFiles Found'),
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
                                                               tab = 'ngrams',
                                                               table = self,
                                                               cols_search = [
                                                                   self.tr('N-grams')
                                                               ])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self.main)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self.main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['ngrams']['filter_settings']

            text_measure_dispersion = self.settings['ngrams']['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = self.settings['ngrams']['generation_settings']['measure_adjusted_freq']

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

            col_ngrams = self.find_col('N-grams')
            col_number_files_found = self.find_col('Number of\nFiles Found')

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

            len_ngram_min = (float('-inf')
                             if settings['len_ngram_min_no_limit'] else settings['len_ngram_min'])
            len_ngram_max = (float('inf')
                             if settings['len_ngram_max_no_limit'] else settings['len_ngram_max'])

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

                if len_ngram_min <= sum([len(token) for token in self.item(i, col_ngrams).text_raw]) <= len_ngram_max:
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
            settings = copy.deepcopy(main.settings_default['ngrams'])
        else:
            settings = copy.deepcopy(main.settings_custom['ngrams'])

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

        checkbox_ignore_tags_search.setChecked(settings['search_settings']['ignore_tags'])
        checkbox_ignore_tags_search_match_tags.setChecked(settings['search_settings']['ignore_tags_match_tags'])
        combo_box_ignore_tags_search.setCurrentText(settings['search_settings']['ignore_tags_type'])
        combo_box_ignore_tags_search_match_tags.setCurrentText(settings['search_settings']['ignore_tags_type_match_tags'])
        checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        spin_box_search_term_position_min.setValue(settings['search_settings']['search_term_position_min'])
        checkbox_search_term_position_min_no_limit.setChecked(settings['search_settings']['search_term_position_min_no_limit'])
        spin_box_search_term_position_max.setValue(settings['search_settings']['search_term_position_max'])
        checkbox_search_term_position_max_no_limit.setChecked(settings['search_settings']['search_term_position_max_no_limit'])
        checkbox_allow_skipped_tokens_within_search_terms.setChecked(settings['search_settings']['allow_skipped_tokens_within_search_terms'])

        # Context Settings
        if defaults:
            main.wordless_context_settings_ngrams.load_settings(defaults = True)

        # Generation Settings
        checkbox_ngram_size_sync.setChecked(settings['generation_settings']['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(settings['generation_settings']['ngram_size_min'])
        spin_box_ngram_size_max.setValue(settings['generation_settings']['ngram_size_max'])
        spin_box_allow_skipped_tokens.setValue(settings['generation_settings']['allow_skipped_tokens'])

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

        spin_box_len_ngram_min.setValue(settings['filter_settings']['len_ngram_min'])
        checkbox_len_ngram_min_no_limit.setChecked(settings['filter_settings']['len_ngram_min_no_limit'])
        spin_box_len_ngram_max.setValue(settings['filter_settings']['len_ngram_max'])
        checkbox_len_ngram_max_no_limit.setChecked(settings['filter_settings']['len_ngram_max_no_limit'])

        spin_box_number_files_found_min.setValue(settings['filter_settings']['number_files_found_min'])
        checkbox_number_files_found_min_no_limit.setChecked(settings['filter_settings']['number_files_found_min_no_limit'])
        spin_box_number_files_found_max.setValue(settings['filter_settings']['number_files_found_max'])
        checkbox_number_files_found_max_no_limit.setChecked(settings['filter_settings']['number_files_found_max_no_limit'])

        combo_box_filter_file.setCurrentText(settings['filter_settings']['filter_file'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['ngrams']['token_settings']

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

        checkbox_match_tags.token_settings_changed()
        main.wordless_context_settings_ngrams.token_settings_changed()

    def search_settings_changed():
        settings = main.settings_custom['ngrams']['search_settings']

        settings['search_settings'] = group_box_search_settings.isChecked()

        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()
        settings['search_term'] = line_edit_search_term.text()
        settings['search_terms'] = list_search_terms.get_items()

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()

        settings['ignore_tags'] = checkbox_ignore_tags_search.isChecked()
        settings['ignore_tags_match_tags'] = checkbox_ignore_tags_search_match_tags.isChecked()
        settings['ignore_tags_type'] = combo_box_ignore_tags_search.currentText()
        settings['ignore_tags_type_match_tags'] = combo_box_ignore_tags_search_match_tags.currentText()
        settings['match_tags'] = checkbox_match_tags.isChecked()

        settings['search_term_position_min'] = spin_box_search_term_position_min.value()
        settings['search_term_position_min_no_limit'] = checkbox_search_term_position_min_no_limit.isChecked()
        settings['search_term_position_max'] = spin_box_search_term_position_max.value()
        settings['search_term_position_max_no_limit'] = checkbox_search_term_position_max_no_limit.isChecked()
        settings['allow_skipped_tokens_within_search_terms'] = checkbox_allow_skipped_tokens_within_search_terms.isChecked()

        if settings['search_settings']:
            checkbox_match_tags.token_settings_changed()

    def generation_settings_changed():
        settings = main.settings_custom['ngrams']['generation_settings']

        settings['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        settings['ngram_size_min'] = spin_box_ngram_size_min.value()
        settings['ngram_size_max'] = spin_box_ngram_size_max.value()
        settings['allow_skipped_tokens'] = spin_box_allow_skipped_tokens.value()

        settings['measure_dispersion'] = combo_box_measure_dispersion.currentText()
        settings['measure_adjusted_freq'] = combo_box_measure_adjusted_freq.currentText()

        # Keyword Position
        if spin_box_search_term_position_max.value() == spin_box_search_term_position_max.maximum():
            spin_box_search_term_position_min.setMaximum(settings['ngram_size_max'])
            spin_box_search_term_position_max.setMaximum(settings['ngram_size_max'])

            spin_box_search_term_position_max.setValue(settings['ngram_size_max'])
        else:
            spin_box_search_term_position_min.setMaximum(settings['ngram_size_max'])
            spin_box_search_term_position_max.setMaximum(settings['ngram_size_max'])

        # Allow skipped tokens within search terms
        if settings['allow_skipped_tokens'] == 0:
            checkbox_allow_skipped_tokens_within_search_terms.setEnabled(False)
        else:
            checkbox_allow_skipped_tokens_within_search_terms.setEnabled(True)

        # Use Data
        use_data_old = combo_box_use_data.currentText()

        combo_box_use_data.clear()

        combo_box_use_data.addItems([
            main.tr('Frequency'),
            main.settings_global['measures_dispersion'][settings['measure_dispersion']]['col'],
            main.settings_global['measures_adjusted_freq'][settings['measure_adjusted_freq']]['col']
        ])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(main.settings_default['ngrams']['plot_settings']['use_data'])

    def table_settings_changed():
        settings = main.settings_custom['ngrams']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        settings = main.settings_custom['ngrams']['plot_settings']

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
        settings = main.settings_custom['ngrams']['filter_settings']

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

        settings['len_ngram_min'] = spin_box_len_ngram_min.value()
        settings['len_ngram_min_no_limit'] = checkbox_len_ngram_min_no_limit.isChecked()
        settings['len_ngram_max'] = spin_box_len_ngram_max.value()
        settings['len_ngram_max_no_limit'] = checkbox_len_ngram_max_no_limit.isChecked()

        settings['number_files_found_min'] = spin_box_number_files_found_min.value()
        settings['number_files_found_min_no_limit'] = checkbox_number_files_found_min_no_limit.isChecked()
        settings['number_files_found_max'] = spin_box_number_files_found_max.value()
        settings['number_files_found_max_no_limit'] = checkbox_number_files_found_max_no_limit.isChecked()

        settings['filter_file'] = combo_box_filter_file.currentText()

    def table_item_changed():
        text_measure_dispersion = table_ngrams.settings['ngrams']['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = table_ngrams.settings['ngrams']['generation_settings']['measure_adjusted_freq']

        col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        col_text_adjusted_freq =  main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        label_dispersion.setText(f'{col_text_dispersion}:')
        label_adjusted_freq.setText(f'{col_text_adjusted_freq}:')

    wrapper_ngrams = wordless_layout.Wordless_Wrapper(main, load_settings)
    
    table_ngrams = Wordless_Table_Ngrams(main)

    wrapper_ngrams.layout_table.addWidget(table_ngrams.label_number_results, 0, 0)
    wrapper_ngrams.layout_table.addWidget(table_ngrams.button_search_results, 0, 4)
    wrapper_ngrams.layout_table.addWidget(table_ngrams, 1, 0, 1, 5)
    wrapper_ngrams.layout_table.addWidget(table_ngrams.button_generate_table, 2, 0)
    wrapper_ngrams.layout_table.addWidget(table_ngrams.button_generate_plot, 2, 1)
    wrapper_ngrams.layout_table.addWidget(table_ngrams.button_export_selected, 2, 2)
    wrapper_ngrams.layout_table.addWidget(table_ngrams.button_export_all, 2, 3)
    wrapper_ngrams.layout_table.addWidget(table_ngrams.button_clear, 2, 4)

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

    # Search Settings
    group_box_search_settings = QGroupBox(main.tr('Search Settings'), main)

    (label_search_term,
     checkbox_multi_search_mode,
     line_edit_search_term,
     list_search_terms,
     label_separator,

     checkbox_ignore_case,
     checkbox_match_inflected_forms,
     checkbox_match_whole_word,
     checkbox_use_regex,

     checkbox_ignore_tags_search,
     checkbox_ignore_tags_search_match_tags,
     combo_box_ignore_tags_search,
     combo_box_ignore_tags_search_match_tags,
     label_ignore_tags_search,
     checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(main, tab = 'ngrams')

    label_search_term_position = QLabel(main.tr('Search Term Position:'), main)
    (label_search_term_position_min,
     spin_box_search_term_position_min,
     checkbox_search_term_position_min_no_limit,
     label_search_term_position_max,
     spin_box_search_term_position_max,
     checkbox_search_term_position_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100)
    checkbox_allow_skipped_tokens_within_search_terms = QCheckBox(main.tr('Allow skipped tokens within search terms'), main)

    (label_context_settings,
     button_context_settings) = wordless_widgets.wordless_widgets_context_settings(main, tab = 'ngrams')

    group_box_search_settings.setCheckable(True)

    group_box_search_settings.toggled.connect(search_settings_changed)

    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_ngrams.button_generate_table.click)
    list_search_terms.itemChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)

    checkbox_ignore_tags_search.stateChanged.connect(search_settings_changed)
    checkbox_ignore_tags_search_match_tags.stateChanged.connect(search_settings_changed)
    combo_box_ignore_tags_search.currentTextChanged.connect(search_settings_changed)
    combo_box_ignore_tags_search_match_tags.currentTextChanged.connect(search_settings_changed)
    checkbox_match_tags.stateChanged.connect(search_settings_changed)

    spin_box_search_term_position_min.valueChanged.connect(search_settings_changed)
    checkbox_search_term_position_min_no_limit.stateChanged.connect(search_settings_changed)
    spin_box_search_term_position_max.valueChanged.connect(search_settings_changed)
    checkbox_search_term_position_max_no_limit.stateChanged.connect(search_settings_changed)
    checkbox_allow_skipped_tokens_within_search_terms.stateChanged.connect(search_settings_changed)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 5, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 4, 1)

    layout_search_term_position = QGridLayout()
    layout_search_term_position.addWidget(label_search_term_position, 0, 0, 1, 3)
    layout_search_term_position.addWidget(label_search_term_position_min, 1, 0)
    layout_search_term_position.addWidget(spin_box_search_term_position_min, 1, 1)
    layout_search_term_position.addWidget(checkbox_search_term_position_min_no_limit, 1, 2)
    layout_search_term_position.addWidget(label_search_term_position_max, 2, 0)
    layout_search_term_position.addWidget(spin_box_search_term_position_max, 2, 1)
    layout_search_term_position.addWidget(checkbox_search_term_position_max_no_limit, 2, 2)

    layout_search_term_position.setColumnStretch(1, 1)

    layout_context_settings = QGridLayout()
    layout_context_settings.addWidget(label_context_settings, 0, 0)
    layout_context_settings.addWidget(button_context_settings, 0, 1)

    layout_context_settings.setColumnStretch(1, 1)

    layout_ignore_tags_search = QGridLayout()
    layout_ignore_tags_search.addWidget(checkbox_ignore_tags_search, 0, 0)
    layout_ignore_tags_search.addWidget(checkbox_ignore_tags_search_match_tags, 0, 0)
    layout_ignore_tags_search.addWidget(combo_box_ignore_tags_search, 0, 1)
    layout_ignore_tags_search.addWidget(combo_box_ignore_tags_search_match_tags, 0, 1)
    layout_ignore_tags_search.addWidget(label_ignore_tags_search, 0, 2)

    layout_ignore_tags_search.setColumnStretch(3, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addWidget(label_search_term, 0, 0)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 2)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 2)
    group_box_search_settings.layout().addWidget(label_separator, 3, 0, 1, 2)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 4, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 5, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 6, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 7, 0, 1, 2)

    group_box_search_settings.layout().addLayout(layout_ignore_tags_search, 8, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_tags, 9, 0, 1, 2)

    group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 10, 0, 1, 2)

    group_box_search_settings.layout().addLayout(layout_search_term_position, 11, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_allow_skipped_tokens_within_search_terms, 12, 0, 1, 2)

    group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 13, 0, 1, 2)

    group_box_search_settings.layout().addLayout(layout_context_settings, 14, 0, 1, 2)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_ngram_size = QLabel(main.tr('N-gram Size:'), main)
    (checkbox_ngram_size_sync,
     label_ngram_size_min,
     spin_box_ngram_size_min,
     label_ngram_size_max,
     spin_box_ngram_size_max) = wordless_widgets.wordless_widgets_size(main)
    label_allow_skipped_tokens = QLabel(main.tr('Allow Skipped Tokens:'), main)
    spin_box_allow_skipped_tokens = QSpinBox(main)

    (label_measure_dispersion,
     combo_box_measure_dispersion) = wordless_widgets.wordless_widgets_measure_dispersion(main)
    (label_measure_adjusted_freq,
     combo_box_measure_adjusted_freq) = wordless_widgets.wordless_widgets_measure_adjusted_freq(main)

    (label_settings_measures,
     button_settings_measures) = wordless_widgets.wordless_widgets_settings_measures(main,
                                                                                     tab = main.tr('Dispersion'))

    spin_box_allow_skipped_tokens.setRange(0, 20)

    checkbox_ngram_size_sync.stateChanged.connect(generation_settings_changed)
    spin_box_ngram_size_min.valueChanged.connect(generation_settings_changed)
    spin_box_ngram_size_max.valueChanged.connect(generation_settings_changed)
    spin_box_allow_skipped_tokens.valueChanged.connect(generation_settings_changed)

    combo_box_measure_dispersion.currentTextChanged.connect(generation_settings_changed)
    combo_box_measure_adjusted_freq.currentTextChanged.connect(generation_settings_changed)

    layout_allow_skipped_tokens = QGridLayout()
    layout_allow_skipped_tokens.addWidget(label_allow_skipped_tokens, 0, 0)
    layout_allow_skipped_tokens.addWidget(spin_box_allow_skipped_tokens, 0, 1)

    layout_allow_skipped_tokens.setColumnStretch(1, 1)

    layout_settings_measures = QGridLayout()
    layout_settings_measures.addWidget(label_settings_measures, 0, 0)
    layout_settings_measures.addWidget(button_settings_measures, 0, 1)

    layout_settings_measures.setColumnStretch(1, 1)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_ngram_size, 0, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(checkbox_ngram_size_sync, 0, 3, Qt.AlignRight)
    group_box_generation_settings.layout().addWidget(label_ngram_size_min, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_ngram_size_min, 1, 1)
    group_box_generation_settings.layout().addWidget(label_ngram_size_max, 1, 2)
    group_box_generation_settings.layout().addWidget(spin_box_ngram_size_max, 1, 3)
    group_box_generation_settings.layout().addLayout(layout_allow_skipped_tokens, 2, 0, 1, 4)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 4)

    group_box_generation_settings.layout().addWidget(label_measure_dispersion, 4, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(combo_box_measure_dispersion, 5, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(label_measure_adjusted_freq, 6, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(combo_box_measure_adjusted_freq, 7, 0, 1, 4)

    group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 8, 0, 1, 4)

    group_box_generation_settings.layout().addLayout(layout_settings_measures, 9, 0, 1, 4)

    group_box_generation_settings.layout().setColumnStretch(1, 1)
    group_box_generation_settings.layout().setColumnStretch(3, 1)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_ngrams)

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

    label_len_ngram = QLabel(main.tr('N-gram Length:'), main)
    (label_len_ngram_min,
     spin_box_len_ngram_min,
     checkbox_len_ngram_min_no_limit,
     label_len_ngram_max,
     spin_box_len_ngram_max,
     checkbox_len_ngram_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100)

    label_number_files_found = QLabel(main.tr('Number of Files Found:'), main)
    (label_number_files_found_min,
     spin_box_number_files_found_min,
     checkbox_number_files_found_min_no_limit,
     label_number_files_found_max,
     spin_box_number_files_found_max,
     checkbox_number_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    (label_filter_file,
     combo_box_filter_file,
     button_filter_results) = wordless_widgets.wordless_widgets_filter_results(main, table_ngrams)

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

    spin_box_len_ngram_min.valueChanged.connect(filter_settings_changed)
    checkbox_len_ngram_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_ngram_max.valueChanged.connect(filter_settings_changed)
    checkbox_len_ngram_max_no_limit.stateChanged.connect(filter_settings_changed)

    spin_box_number_files_found_min.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_min_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_number_files_found_max.valueChanged.connect(filter_settings_changed)
    checkbox_number_files_found_max_no_limit.stateChanged.connect(filter_settings_changed)

    combo_box_filter_file.currentTextChanged.connect(filter_settings_changed)

    table_ngrams.itemChanged.connect(table_item_changed)

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

    group_box_filter_settings.layout().addWidget(label_len_ngram, 12, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(label_len_ngram_min, 13, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_ngram_min, 13, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_ngram_min_no_limit, 13, 2)
    group_box_filter_settings.layout().addWidget(label_len_ngram_max, 14, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_ngram_max, 14, 1)
    group_box_filter_settings.layout().addWidget(checkbox_len_ngram_max_no_limit, 14, 2)

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

    wrapper_ngrams.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    wrapper_ngrams.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    wrapper_ngrams.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    wrapper_ngrams.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    wrapper_ngrams.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    wrapper_ngrams.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    wrapper_ngrams.layout_settings.setRowStretch(6, 1)

    load_settings()

    return wrapper_ngrams

def generate_ngrams(main, files):
    texts = []
    ngrams_freq_files = []
    ngrams_stats_files = []
    ngrams_text = {}

    settings = main.settings_custom['ngrams']

    ngram_size_min = settings['generation_settings']['ngram_size_min']
    ngram_size_max = settings['generation_settings']['ngram_size_max']
    allow_skipped_tokens = settings['generation_settings']['allow_skipped_tokens']

    # Frequency
    for file in files:
        ngrams = []

        text = wordless_text.Wordless_Text(main, file)

        tokens = wordless_token_processing.wordless_preprocess_tokens_ngrams(text,
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
        if allow_skipped_tokens == 0:
            for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                for i, ngram in enumerate(nltk.ngrams(tokens, ngram_size)):
                    if wordless_text_utils.check_context(i, tokens,
                                                         settings = settings['context_settings'],
                                                         search_terms_inclusion = search_terms_inclusion,
                                                         search_terms_exclusion = search_terms_exclusion):
                        ngrams.append(ngram)
            
        else:
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
                                                    if wordless_text_utils.check_context(i + j, tokens,
                                                                                         settings = settings['context_settings'],
                                                                                         search_terms_inclusion = search_terms_inclusion,
                                                                                         search_terms_exclusion = search_terms_exclusion):
                                                        ngrams.append(tuple(ngram_matched))
                            elif len_search_term == ngram_size:
                                for i, ngram in enumerate(nltk.ngrams(tokens, ngram_size)):
                                    if ngram == search_term:
                                        if wordless_text_utils.check_context(i, tokens,
                                                                             settings = settings['context_settings'],
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
                                    if wordless_text_utils.check_context(i + j, tokens,
                                                                         settings = settings['context_settings'],
                                                                         search_terms_inclusion = search_terms_inclusion,
                                                                         search_terms_exclusion = search_terms_exclusion):
                                        ngrams.append((head, skip_tail))

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

            ngrams_freq_files.append(ngrams_freq_file_filtered)
        else:
            ngrams_freq_files.append(ngrams_freq_file)

        # N-grams Text
        for ngram in ngrams_freq_file:
            ngrams_text[ngram] = wordless_text_processing.wordless_word_detokenize(main, ngram, text.lang)

        texts.append(text)

    # Total
    if len(files) > 1:
        text_total = wordless_text.Wordless_Text(main, files[0])
        text_total.tokens = [token for text in texts for token in text.tokens]

        texts.append(text_total)

        ngrams_freq_files.append(sum([collections.Counter(ngrams_freq_file) for ngrams_freq_file in ngrams_freq_files],
                                     collections.Counter()))

    # Dispersion & Adjusted Frequency
    text_measure_dispersion = settings['generation_settings']['measure_dispersion']
    text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

    measure_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['func']
    measure_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['func']

    ngrams_total = ngrams_freq_files[-1].keys()

    for text in texts:
        ngrams_lens = {}
        ngrams_stats_file = {}

        if allow_skipped_tokens == 0:
            for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                ngrams_lens[ngram_size] = list(nltk.ngrams(text.tokens, ngram_size))
        else:
            for ngram_size in range(ngram_size_min, ngram_size_max + 1):
                ngrams_lens[ngram_size] = list(nltk.skipgrams(text.tokens, ngram_size, allow_skipped_tokens))

        # Dispersion
        number_sections = main.settings_custom['measures']['dispersion']['general']['number_sections']

        sections_freq_lens = {}

        for ngram_size, ngram_list in ngrams_lens.items():
            sections_freq_lens[ngram_size] = [collections.Counter(section)
                                              for section in wordless_text_utils.to_sections(ngram_list, number_sections)]

        for ngram in ngrams_total:
            counts = [section_freq[ngram] for section_freq in sections_freq_lens[len(ngram)]]

            ngrams_stats_file[ngram] = [measure_dispersion(counts)]

        # Adjusted Frequency
        if not main.settings_custom['measures']['adjusted_freq']['general']['use_same_settings_dispersion']:
            number_sections = main.settings_custom['measures']['adjusted_freq']['general']['number_sections']

            sections_freq_lens = {}

            for ngram_size, ngrams in ngrams_lens.items():
                sections_freq_lens[ngram_size] = [collections.Counter(section)
                                                  for section in wordless_text_utils.to_sections(ngrams, number_sections)]

        for ngram in ngrams_total:
            counts = [section_freq[ngram] for section_freq in sections_freq_lens[len(ngram)]]

            ngrams_stats_file[ngram].append(measure_adjusted_freq(counts))

        ngrams_stats_files.append(ngrams_stats_file)

    if len(files) == 1:
        ngrams_freq_files *= 2
        ngrams_stats_files *= 2

    return (wordless_misc.merge_dicts(ngrams_freq_files),
            wordless_misc.merge_dicts(ngrams_stats_files),
            ngrams_text)

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['ngrams']

    files = wordless_checking_file.check_files_loading(main, main.wordless_files.get_selected_files())

    if files:
        if (not settings['search_settings']['search_settings'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            ngrams_freq_files, ngrams_stats_files, ngrams_text = generate_ngrams(main, files)

            if ngrams_freq_files:
                table.clear_table()
                
                table.settings = main.settings_custom

                text_measure_dispersion = settings['generation_settings']['measure_dispersion']
                text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
                col_text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

                # Insert Columns (Files)
                for i, file in enumerate(files):
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

                wordless_message.wordless_message_generate_table_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_table(main)

                wordless_message.wordless_message_generate_table_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term_optional(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['ngrams']

    text_measure_dispersion = settings['generation_settings']['measure_dispersion']
    text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

    col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
    col_text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

    files = wordless_checking_file.check_files_loading(main, main.wordless_files.get_selected_files())

    if files:
        if (settings['search_settings']['search_settings'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms'] or
            not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']):
            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            col_text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
            col_text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']
            
            ngrams_freq_files, ngrams_stats_files, ngrams_text = generate_ngrams(main, files)

            if ngrams_freq_files:
                if settings['plot_settings']['use_data'] == main.tr('Frequency'):
                    ngrams_freq_files = {ngrams_text[ngram]: freqs
                                         for ngram, freqs in ngrams_freq_files.items()}

                    wordless_plot_freq.wordless_plot_freq(main, ngrams_freq_files,
                                                          settings = settings['plot_settings'],
                                                          label_x = main.tr('N-grams'))
                else:
                    ngrams_stats_files = {ngrams_text[ngram]: stats
                                          for ngram, stats in ngrams_stats_files.items()}

                    if settings['plot_settings']['use_data'] == col_text_dispersion:
                        ngrams_stat_files = {ngram: numpy.array(stats_files)[:, 0]
                                             for ngram, stats_files in ngrams_stats_files.items()}

                        label_y = col_text_dispersion
                    elif settings['plot_settings']['use_data'] == col_text_adjusted_freq:
                        ngrams_stat_files = {ngram: numpy.array(stats_files)[:, 1]
                                             for ngram, stats_files in ngrams_stats_files.items()}

                        label_y = col_text_adjusted_freq

                    wordless_plot_stat.wordless_plot_stat(main, ngrams_stat_files,
                                                          settings = settings['plot_settings'],
                                                          label_x = main.tr('N-grams'),
                                                          label_y = label_y)

                wordless_message.wordless_message_generate_plot_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_plot(main)

                wordless_message.wordless_message_generate_plot_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term_optional(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_plot_error(main)
