#
# Wordless: N-gram
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Ngram(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('N-grams'),
                             main.tr('Total Freq'),
                             main.tr('Files Found'),
                         ],
                         cols_pct = [
                             main.tr('Total Freq'),
                             main.tr('Files Found')
                         ],
                         cols_cumulative = [
                             main.tr('Total Freq')
                         ],
                         sorting_enabled = True)

    @ wordless_misc.log_timing('Filtering')
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['ngram']

            if settings['apply_to'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total Freq'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["apply_to"]}] Freq'))

            col_ngrams = self.find_col('N-grams')
            col_files_found = self.find_col('Files Found')

            freq_min = settings['freq_min']
            freq_max = settings['freq_max'] if not settings['freq_no_limit'] else float('inf')
            len_min = settings['len_min']
            len_max = settings['len_max'] if not settings['len_no_limit'] else float('inf')
            files_min = settings['files_min']
            files_max = settings['files_max'] if not settings['files_no_limit'] else float('inf')

            self.row_filters = [{} for i in range(self.rowCount())]

            for i in range(self.rowCount()):
                if freq_min <= self.item(i, col_freq).val_raw <= freq_max:
                    self.row_filters[i][self.tr('Freq')] = True
                else:
                    self.row_filters[i][self.tr('Freq')] = False

                if len_min <= len(self.item(i, col_ngrams).text().replace(' ', '')) <= len_max:
                    self.row_filters[i][self.tr('N-grams')] = True
                else:
                    self.row_filters[i][self.tr('N-grams')] = False

                if files_min <= self.item(i, col_files_found).val_raw <= files_max:
                    self.row_filters[i][self.tr('Files Found')] = True
                else:
                    self.row_filters[i][self.tr('Files Found')] = False

            self.filter_table()

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings_loaded = copy.deepcopy(main.settings_default['ngram'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['ngram'])

        checkbox_words.setChecked(settings_loaded['words'])
        checkbox_lowercase.setChecked(settings_loaded['lowercase'])
        checkbox_uppercase.setChecked(settings_loaded['uppercase'])
        checkbox_title_case.setChecked(settings_loaded['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings_loaded['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings_loaded['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings_loaded['filter_stop_words'])

        checkbox_nums.setChecked(settings_loaded['nums'])
        checkbox_puncs.setChecked(settings_loaded['puncs'])

        line_edit_search_term.setText(settings_loaded['search_term'])
        list_search_terms.clear()
        for search_term in settings_loaded['search_terms']:
            list_search_terms.add_item(search_term)

        checkbox_keyword_position_no_limit.setChecked(settings_loaded['keyword_position_no_limit'])
        spin_box_keyword_position_min.setValue(settings_loaded['keyword_position_min'])
        spin_box_keyword_position_max.setValue(settings_loaded['keyword_position_max'])

        checkbox_ignore_case.setChecked(settings_loaded['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings_loaded['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings_loaded['match_whole_word'])
        checkbox_use_regex.setChecked(settings_loaded['use_regex'])
        checkbox_multi_search_mode.setChecked(settings_loaded['multi_search_mode'])
        checkbox_show_all.setChecked(settings_loaded['show_all'])

        checkbox_ngram_size_sync.setChecked(settings_loaded['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(settings_loaded['ngram_size_min'])
        spin_box_ngram_size_max.setValue(settings_loaded['ngram_size_max'])
        spin_box_allow_skipped_tokens.setValue(settings_loaded['allow_skipped_tokens'])

        checkbox_show_pct.setChecked(settings_loaded['show_pct'])
        checkbox_show_cumulative.setChecked(settings_loaded['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings_loaded['show_breakdown'])

        checkbox_use_pct.setChecked(settings_loaded['use_pct'])
        checkbox_use_cumulative.setChecked(settings_loaded['use_cumulative'])

        checkbox_rank_no_limit.setChecked(settings_loaded['rank_no_limit'])
        spin_box_rank_min.setValue(settings_loaded['rank_min'])
        spin_box_rank_max.setValue(settings_loaded['rank_max'])

        checkbox_freq_no_limit.setChecked(settings_loaded['freq_no_limit'])
        spin_box_freq_min.setValue(settings_loaded['freq_min'])
        spin_box_freq_max.setValue(settings_loaded['freq_max'])

        combo_box_apply_to.setCurrentText(settings_loaded['apply_to'])

        checkbox_len_no_limit.setChecked(settings_loaded['len_no_limit'])
        spin_box_len_min.setValue(settings_loaded['len_min'])
        spin_box_len_max.setValue(settings_loaded['len_max'])

        checkbox_files_no_limit.setChecked(settings_loaded['files_no_limit'])
        spin_box_files_min.setValue(settings_loaded['files_min'])
        spin_box_files_max.setValue(settings_loaded['files_max'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
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
        settings['search_term'] = line_edit_search_term.text()
        settings['search_terms'] = list_search_terms.get_items()
        settings['keyword_position_no_limit'] = checkbox_keyword_position_no_limit.isChecked()
        settings['keyword_position_min'] = spin_box_keyword_position_min.value()
        settings['keyword_position_max'] = spin_box_keyword_position_max.value()

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()
        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()
        settings['show_all'] = checkbox_show_all.isChecked()

        if settings['show_all']:
            table_ngram.button_generate_data.setText(main.tr('Generate N-grams'))
            label_ngram_size.setText(main.tr('N-gram Size:'))

            checkbox_keyword_position_no_limit.setEnabled(False)
            spin_box_keyword_position_min.setEnabled(False)
            spin_box_keyword_position_max.setEnabled(False)
        else:
            table_ngram.button_generate_data.setText(main.tr('Generate Word Clusters'))
            label_ngram_size.setText(main.tr('Cluster Size:'))

            checkbox_keyword_position_no_limit.setEnabled(True)
            spin_box_keyword_position_min.setEnabled(True)

            if not settings['keyword_position_no_limit']:
                spin_box_keyword_position_max.setEnabled(True)

    def generation_settings_changed():
        settings['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        settings['ngram_size_min'] = spin_box_ngram_size_min.value()
        settings['ngram_size_max'] = spin_box_ngram_size_max.value()
        settings['allow_skipped_tokens'] = spin_box_allow_skipped_tokens.value()

        if (main.settings_custom['ngram']['keyword_position_no_limit'] and
            spin_box_keyword_position_max.value() == spin_box_keyword_position_max.maximum()):
            spin_box_keyword_position_min.setMaximum(settings['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(settings['ngram_size_max'])

            spin_box_keyword_position_max.setValue(settings['ngram_size_max'])
        else:
            spin_box_keyword_position_min.setMaximum(settings['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(settings['ngram_size_max'])

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        settings['use_pct'] = checkbox_use_pct.isChecked()
        settings['use_cumulative'] = checkbox_use_cumulative.isChecked()

        settings['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_max'] = spin_box_rank_max.value()

    def filter_settings_changed():
        settings['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        settings['freq_min'] = spin_box_freq_min.value()
        settings['freq_max'] = spin_box_freq_max.value()

        settings['apply_to'] = combo_box_apply_to.currentText()

        settings['len_no_limit'] = checkbox_len_no_limit.isChecked()
        settings['len_min'] = spin_box_len_min.value()
        settings['len_max'] = spin_box_len_max.value()

        settings['files_no_limit'] = checkbox_files_no_limit.isChecked()
        settings['files_min'] = spin_box_files_min.value()
        settings['files_max'] = spin_box_files_max.value()

    settings = main.settings_custom['ngram']

    tab_ngram = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_ngram = Wordless_Table_Ngram(main)

    table_ngram.button_generate_data = QPushButton(main.tr('Generate N-grams'), main)
    table_ngram.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

    table_ngram.button_generate_data.clicked.connect(lambda: generate_data(main, table_ngram))
    table_ngram.button_generate_plot.clicked.connect(lambda: generate_plot(main))

    tab_ngram.layout_table.addWidget(table_ngram, 0, 0, 1, 5)
    tab_ngram.layout_table.addWidget(table_ngram.button_generate_data, 1, 0)
    tab_ngram.layout_table.addWidget(table_ngram.button_generate_plot, 1, 1)
    tab_ngram.layout_table.addWidget(table_ngram.button_export_selected, 1, 2)
    tab_ngram.layout_table.addWidget(table_ngram.button_export_all, 1, 3)
    tab_ngram.layout_table.addWidget(table_ngram.button_clear, 1, 4)

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
     checkbox_puncs) = wordless_widgets.wordless_widgets_token(main)

    separator_token_settings = wordless_layout.Wordless_Separator(main)

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

    group_box_token_settings.layout().addWidget(separator_token_settings, 5, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_nums, 6, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 6, 1)

    # Search Settings
    group_box_search_settings = QGroupBox(main.tr('Search Settings'), main)

    (label_search_term,
     checkbox_show_all,
     line_edit_search_term,
     list_search_terms,
     checkbox_ignore_case,
     checkbox_match_inflected_forms,
     checkbox_match_whole_word,
     checkbox_use_regex,
     checkbox_multi_search_mode) = wordless_widgets.wordless_widgets_search(main)

    label_keyword_position = QLabel(main.tr('Keyword Position:'), main)
    (checkbox_keyword_position_no_limit,
     label_keyword_position_min,
     spin_box_keyword_position_min,
     label_keyword_position_max,
     spin_box_keyword_position_max) = wordless_widgets.wordless_widgets_filter(main)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_ngram.button_generate_data.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_keyword_position_no_limit.stateChanged.connect(search_settings_changed)
    spin_box_keyword_position_min.valueChanged.connect(search_settings_changed)
    spin_box_keyword_position_max.valueChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    checkbox_show_all.stateChanged.connect(search_settings_changed)

    layout_show_all = QGridLayout()
    layout_show_all.addWidget(label_search_term, 0, 0, Qt.AlignLeft)
    layout_show_all.addWidget(checkbox_show_all, 0, 1, Qt.AlignRight)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addLayout(layout_show_all, 0, 0, 1, 4)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 4)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 4)
    group_box_search_settings.layout().addWidget(label_keyword_position, 3, 0, 1, 3)
    group_box_search_settings.layout().addWidget(checkbox_keyword_position_no_limit, 3, 3)
    group_box_search_settings.layout().addWidget(label_keyword_position_min, 4, 0)
    group_box_search_settings.layout().addWidget(spin_box_keyword_position_min, 4, 1)
    group_box_search_settings.layout().addWidget(label_keyword_position_max, 4, 2)
    group_box_search_settings.layout().addWidget(spin_box_keyword_position_max, 4, 3)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 5, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 6, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 7, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 8, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 9, 0, 1, 4)

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

    spin_box_allow_skipped_tokens.setRange(0, 20)

    checkbox_ngram_size_sync.stateChanged.connect(generation_settings_changed)
    spin_box_ngram_size_min.valueChanged.connect(generation_settings_changed)
    spin_box_ngram_size_max.valueChanged.connect(generation_settings_changed)
    spin_box_allow_skipped_tokens.valueChanged.connect(generation_settings_changed)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_ngram_size, 0, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(checkbox_ngram_size_sync, 0, 3)
    group_box_generation_settings.layout().addWidget(label_ngram_size_min, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_ngram_size_min, 1, 1)
    group_box_generation_settings.layout().addWidget(label_ngram_size_max, 1, 2)
    group_box_generation_settings.layout().addWidget(spin_box_ngram_size_max, 1, 3)
    group_box_generation_settings.layout().addWidget(label_allow_skipped_tokens, 2, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(spin_box_allow_skipped_tokens, 2, 3)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table(main, table_ngram)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown, 2, 0)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    checkbox_use_pct = QCheckBox(main.tr('Use Percentage Data'), main)
    checkbox_use_cumulative = QCheckBox(main.tr('Use Cumulative Data'), main)

    separator_plot_settings = wordless_layout.Wordless_Separator(main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, 1, 10000)

    checkbox_use_pct.stateChanged.connect(plot_settings_changed)
    checkbox_use_cumulative.stateChanged.connect(plot_settings_changed)

    checkbox_rank_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addWidget(checkbox_use_pct, 0, 0, 1, 4)
    group_box_plot_settings.layout().addWidget(checkbox_use_cumulative, 1, 0, 1, 4)

    group_box_plot_settings.layout().addWidget(separator_plot_settings, 2, 0, 1, 4)

    group_box_plot_settings.layout().addWidget(label_rank, 3, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_rank_no_limit, 3, 3)
    group_box_plot_settings.layout().addWidget(label_rank_min, 4, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_min, 4, 1)
    group_box_plot_settings.layout().addWidget(label_rank_max, 4, 2)
    group_box_plot_settings.layout().addWidget(spin_box_rank_max, 4, 3)

    # Filter Settings
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_freq = QLabel(main.tr('Frequency:'), main)
    (checkbox_freq_no_limit,
     label_freq_min,
     spin_box_freq_min,
     label_freq_max,
     spin_box_freq_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                   filter_min = 0,
                                                                   filter_max = 10000,
                                                                   table = table_ngram,
                                                                   col = main.tr('Freq'))

    label_apply_to = QLabel(main.tr('Apply to:'), main)
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_ngram)
    separator_filter_settings = wordless_layout.Wordless_Separator(main)

    label_len = QLabel(main.tr('N-gram Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                  table = table_ngram,
                                                                  col = main.tr('N-grams'))

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_ngram,
                                                                    col = main.tr('Files Found'))

    button_filter_results = QPushButton(main.tr('Filter Results'), main)

    checkbox_freq_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_max.valueChanged.connect(filter_settings_changed)

    combo_box_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.valueChanged.connect(filter_settings_changed)
    spin_box_len_max.valueChanged.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.valueChanged.connect(filter_settings_changed)
    spin_box_files_max.valueChanged.connect(filter_settings_changed)

    button_filter_results.clicked.connect(lambda: table_ngram.update_filters())

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_freq, 0, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_no_limit, 0, 3)
    group_box_filter_settings.layout().addWidget(label_freq_min, 1, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_min, 1, 1)
    group_box_filter_settings.layout().addWidget(label_freq_max, 1, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_max, 1, 3)

    group_box_filter_settings.layout().addWidget(label_apply_to, 2, 0)
    group_box_filter_settings.layout().addWidget(combo_box_apply_to, 2, 1, 1, 3)
    group_box_filter_settings.layout().addWidget(separator_filter_settings, 3, 0, 1, 4)

    group_box_filter_settings.layout().addWidget(label_len, 4, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_len_no_limit, 4, 3)
    group_box_filter_settings.layout().addWidget(label_len_min, 5, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_min, 5, 1)
    group_box_filter_settings.layout().addWidget(label_len_max, 5, 2)
    group_box_filter_settings.layout().addWidget(spin_box_len_max, 5, 3)

    group_box_filter_settings.layout().addWidget(label_files, 6, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_files_no_limit, 6, 3)
    group_box_filter_settings.layout().addWidget(label_files_min, 7, 0)
    group_box_filter_settings.layout().addWidget(spin_box_files_min, 7, 1)
    group_box_filter_settings.layout().addWidget(label_files_max, 7, 2)
    group_box_filter_settings.layout().addWidget(spin_box_files_max, 7, 3)

    group_box_filter_settings.layout().addWidget(button_filter_results, 8, 0, 1, 4)

    tab_ngram.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    load_settings()

    return tab_ngram

def generate_ngrams(main, files):
    freq_distributions = []

    settings = main.settings_custom['ngram']

    for file in files:
        ngrams = []

        text = wordless_text.Wordless_Text(main, file)
        tokens = text.tokens.copy()

        if settings['words']:
            if settings['treat_as_lowercase']:
                tokens = [token.lower() for token in tokens]

            if settings['lemmatize']:
                tokens = wordless_text.wordless_lemmatize(main, tokens, text.lang)

        if not settings['puncs']:
            tokens = [token for token in tokens if [char for char in token if char.isalnum()]]

        if settings['allow_skipped_tokens'] == 0:
            ngrams = list(nltk.everygrams(tokens, settings['ngram_size_min'], settings['ngram_size_max']))
        else:
            for i in range(settings['ngram_size_min'], settings['ngram_size_max'] + 1):
                ngrams.extend(list(nltk.skipgrams(tokens, i, settings['allow_skipped_tokens'])))

        freq_distribution = nltk.FreqDist(ngrams)

        if settings['words']:
            if not settings['treat_as_lowercase']:
                if not settings['lowercase']:
                    freq_distribution = {ngram: freq
                                         for ngram, freq in freq_distribution.items()
                                         if not [token for token in ngram if token.islower()]}
                if not settings['uppercase']:
                    freq_distribution = {ngram: freq
                                         for ngram, freq in freq_distribution.items()
                                         if not [token for token in ngram if token.isupper()]}
                if not settings['title_case']:
                    freq_distribution = {ngram: freq
                                         for ngram, freq in freq_distribution.items()
                                         if not [token for token in ngram if token.istitle()]}

            if settings['filter_stop_words']:
                ngrams_filtered = wordless_text.wordless_filter_stop_words(main, list(freq_distribution.keys()), text.lang)
                
                freq_distribution = {ngram: freq_distribution[ngram] for ngram in ngrams_filtered}
        else:
            freq_distribution = {ngram: freq
                                 for ngram, freq in freq_distribution.items()
                                 if not [char for char in ''.join(ngram) if char.isalpha()]}

        if not settings['nums']:
            freq_distribution = {ngram: freq
                                 for ngram, freq in freq_distribution.items()
                                 if [token for token in ngram if not token.isnumeric()]}

        if not settings['show_all']:
            if settings['multi_search_mode']:
                search_terms = settings['search_terms']
            else:
                if settings['search_term']:
                    search_terms = [settings['search_term']]
                else:
                    search_terms = []

            search_terms = text.match_tokens(search_terms,
                                             settings['ignore_case'],
                                             settings['match_inflected_forms'],
                                             settings['match_whole_word'],
                                             settings['use_regex'])

            freq_distribution = {ngram: freq
                                 for ngram, freq in freq_distribution.items()
                                 for search_term in search_terms
                                 if search_term in ngram and
                                    settings['keyword_position_min'] <= ngram.index(search_term) + 1 <= settings['keyword_position_max']}

        freq_distributions.append({text.word_delimiter.join(ngram): freq for ngram, freq in freq_distribution.items()})

    return wordless_misc.merge_dicts(freq_distributions)

@ wordless_misc.log_timing('Data generation completed')
def generate_data(main, table):
    settings = main.settings_custom['ngram']

    files = main.wordless_files.selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            freq_distribution = generate_ngrams(main, files)

            if freq_distribution:
                table.clear_table()

                table.files = files

                for i, file in enumerate(files):
                    table.insert_col(table.columnCount() - 2,
                                     main.tr(f'[{file["name"]}] Freq'),
                                     pct = True, cumulative = True, breakdown = True)

                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}] Freq')), Qt.DescendingOrder)

                col_total_freq = table.find_col(main.tr('Total Freq'))
                col_files_found = table.find_col(main.tr('Files Found'))

                freqs_total_files = numpy.array(list(freq_distribution.values())).sum(axis = 0)
                freqs_total = sum(freqs_total_files)
                len_files = len(files)

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

                table.setRowCount(len(freq_distribution))

                for i, (ngram, freqs) in enumerate(sorted(freq_distribution.items(), key = wordless_misc.multi_sorting)):
                    # Rank
                    table.setItem(i, 0, wordless_table.Wordless_Table_Item())

                    # N-gram
                    table.setItem(i, 1, wordless_table.Wordless_Table_Item(ngram))

                    # Frequency
                    for j, freq in enumerate(freqs):
                        table.set_item_pct(i, 2 + j, freq, freqs_total_files[j])

                    # Total
                    table.set_item_pct(i, col_total_freq, sum(freqs), freqs_total)

                    # Files Found
                    table.set_item_pct(i, col_files_found, len([freq for freq in freqs if freq]), len_files)

                table.blockSignals(False)
                table.setSortingEnabled(True)
                table.setUpdatesEnabled(True)

                table.update_ranks()
                table.toggle_cumulative()
                table.toggle_breakdown()
            else:
                wordless_dialog.wordless_message_empty_results_table(main)
        else:
            wordless_dialog.wordless_message_empty_search_term(main)

@ wordless_misc.log_timing('Plot generation completed')
def generate_plot(main):
    settings = main.settings_custom['ngram']

    files = main.wordless_files.selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            freq_distribution = generate_ngrams(main, files)

            if freq_distribution:
                wordless_plot.wordless_plot_freq(main, freq_distribution,
                                                 rank_min = settings['rank_min'],
                                                 rank_max = settings['rank_max'],
                                                 use_pct = settings['use_pct'],
                                                 use_cumulative = settings['use_cumulative'],
                                                 label_x = main.tr('N-grams'))
            else:
                wordless_dialog.wordless_message_empty_results_plot(main)
        else:
            wordless_dialog.wordless_message_empty_search_term(main)
