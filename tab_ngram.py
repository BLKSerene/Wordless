#
# Wordless: N-gram
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_utils import *

def init(self):
    def token_settings_changed():
        self.settings['ngram']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        self.settings['ngram']['lowercase'] = checkbox_lowercase.isChecked()
        self.settings['ngram']['uppercase'] = checkbox_uppercase.isChecked()
        self.settings['ngram']['title_cased'] = checkbox_title_cased.isChecked()
        self.settings['ngram']['numerals'] = checkbox_numerals.isChecked()
        self.settings['ngram']['punctuations'] = checkbox_punctuations.isChecked()

        if checkbox_words.checkState() == Qt.Unchecked:
            checkbox_ignore_case.setEnabled(False)
            checkbox_lemmatization.setEnabled(False)
        else:
            checkbox_ignore_case.setEnabled(True)
            checkbox_lemmatization.setEnabled(True)

        if (not checkbox_lowercase.isChecked() and
            not checkbox_uppercase.isChecked() and
            not checkbox_title_cased.isChecked()):
            checkbox_ignore_case.setEnabled(False)
            checkbox_lemmatization.setEnabled(False)

    def search_settings_changed():
        if self.settings['ngram']['multi_search']:
            list_search_terms.get_items()
        else:
            if line_edit_search_term.text():
                self.settings['ngram']['search_terms'] = [line_edit_search_term.text()]
            else:
                self.settings['ngram']['search_terms'] = []

        self.settings['ngram']['keyword_position_no_limit'] = checkbox_keyword_position_no_limit.isChecked()
        self.settings['ngram']['keyword_position_min'] = spin_box_keyword_position_min.value()
        self.settings['ngram']['keyword_position_max'] = (float('inf')
                                                          if checkbox_keyword_position_no_limit.isChecked()
                                                          else spin_box_keyword_position_max.value())
        self.settings['ngram']['ignore_case'] = checkbox_ignore_case.isChecked()
        self.settings['ngram']['lemmatization'] = checkbox_lemmatization.isChecked()
        self.settings['ngram']['whole_word'] = checkbox_whole_word.isChecked()
        self.settings['ngram']['regex'] = checkbox_regex.isChecked()
        self.settings['ngram']['multi_search'] = checkbox_multi_search.isChecked()
        self.settings['ngram']['show_all'] = checkbox_show_all.isChecked()

        if self.settings['ngram']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if self.settings['ngram']['show_all']:
            table_ngram.button_generate_data.setText(self.tr('Generate N-grams'))
            label_ngram_size.setText(self.tr('N-gram Size:'))

            checkbox_keyword_position_no_limit.setEnabled(False)
            spin_box_keyword_position_min.setEnabled(False)
            spin_box_keyword_position_max.setEnabled(False)
        else:
            table_ngram.button_generate_data.setText(self.tr('Generate Word Clusters'))
            label_ngram_size.setText(self.tr('Cluster Size:'))

            checkbox_keyword_position_no_limit.setEnabled(True)
            spin_box_keyword_position_min.setEnabled(True)

            if not self.settings['ngram']['keyword_position_no_limit']:
                spin_box_keyword_position_max.setEnabled(True)

    def generation_settings_changed():
        self.settings['ngram']['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        self.settings['ngram']['ngram_size_min'] = spin_box_ngram_size_min.value()
        self.settings['ngram']['ngram_size_max'] = spin_box_ngram_size_max.value()
        self.settings['ngram']['allow_skipped_tokens'] = spin_box_allow_skipped_tokens.value()

        if (self.settings['ngram']['keyword_position_no_limit'] and
            spin_box_keyword_position_max.value() == spin_box_keyword_position_max.maximum()):
            spin_box_keyword_position_min.setMaximum(self.settings['ngram']['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(self.settings['ngram']['ngram_size_max'])

            spin_box_keyword_position_max.setValue(self.settings['ngram']['ngram_size_max'])
        else:
            spin_box_keyword_position_min.setMaximum(self.settings['ngram']['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(self.settings['ngram']['ngram_size_max'])

    def table_settings_changed():
        self.settings['ngram']['show_pct'] = checkbox_show_pct.isChecked()
        self.settings['ngram']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        self.settings['ngram']['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        self.settings['ngram']['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        self.settings['ngram']['rank_min'] = spin_box_rank_min.value()
        self.settings['ngram']['rank_max'] = (None
                                              if checkbox_rank_no_limit.isChecked()
                                              else spin_box_rank_max.value())

        self.settings['ngram']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['ngram']['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        self.settings['ngram']['freq_min'] = spin_box_freq_min.value()
        self.settings['ngram']['freq_max'] = (float('inf')
                                              if checkbox_freq_no_limit.isChecked()
                                              else spin_box_freq_max.value())
        self.settings['ngram']['freq_apply_to'] = table_ngram.combo_box_freq_apply_to.currentText()

        self.settings['ngram']['len_no_limit'] = checkbox_len_no_limit.isChecked()
        self.settings['ngram']['len_min'] = spin_box_len_min.value()
        self.settings['ngram']['len_max'] = (float('inf')
                                             if checkbox_len_no_limit.isChecked()
                                             else spin_box_len_max.value())

        self.settings['ngram']['files_no_limit'] = checkbox_files_no_limit.isChecked()
        self.settings['ngram']['files_min'] = spin_box_files_min.value()
        self.settings['ngram']['files_max'] = (float('inf')
                                               if checkbox_files_no_limit.isChecked()
                                               else spin_box_files_max.value())

        checkbox_show_pct.stateChanged.emit(self.settings['wordlist']['show_pct'])

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['ngram']['words'])
        checkbox_lowercase.setChecked(self.default_settings['ngram']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['ngram']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['ngram']['title_cased'])
        checkbox_numerals.setChecked(self.default_settings['ngram']['numerals'])
        checkbox_punctuations.setChecked(self.default_settings['ngram']['punctuations'])

        line_edit_search_term.clear()
        list_search_terms.clear()
        checkbox_keyword_position_no_limit.setChecked(self.default_settings['ngram']['keyword_position_no_limit'])
        spin_box_keyword_position_min.setValue(self.default_settings['ngram']['keyword_position_min'])
        spin_box_keyword_position_max.setValue(self.default_settings['ngram']['keyword_position_max'])
        checkbox_ignore_case.setChecked(self.default_settings['ngram']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['ngram']['lemmatization'])
        checkbox_whole_word.setChecked(self.default_settings['ngram']['whole_word'])
        checkbox_regex.setChecked(self.default_settings['ngram']['regex'])
        checkbox_multi_search.setChecked(self.default_settings['ngram']['multi_search'])
        checkbox_show_all.setChecked(self.default_settings['ngram']['show_all'])

        checkbox_ngram_size_sync.setChecked(self.default_settings['ngram']['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(self.default_settings['ngram']['ngram_size_min'])
        spin_box_ngram_size_max.setValue(self.default_settings['ngram']['ngram_size_max'])
        spin_box_allow_skipped_tokens.setValue(self.default_settings['ngram']['allow_skipped_tokens'])

        checkbox_show_pct.setChecked(self.default_settings['ngram']['show_pct'])
        checkbox_show_cumulative.setChecked(self.default_settings['ngram']['show_cumulative'])
        checkbox_show_breakdown.setChecked(self.default_settings['ngram']['show_breakdown'])

        checkbox_rank_no_limit.setChecked(self.default_settings['ngram']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['ngram']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['ngram']['rank_max'])
        checkbox_cumulative.setChecked(self.default_settings['ngram']['cumulative'])

        checkbox_freq_no_limit.setChecked(self.default_settings['ngram']['freq_no_limit'])
        spin_box_freq_min.setValue(self.default_settings['ngram']['freq_min'])
        spin_box_freq_max.setValue(self.default_settings['ngram']['freq_max'])
        table_ngram.combo_box_freq_apply_to.setCurrentText(self.default_settings['ngram']['freq_apply_to'])

        checkbox_len_no_limit.setChecked(self.default_settings['ngram']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['ngram']['len_min'])
        spin_box_len_max.setValue(self.default_settings['ngram']['len_max'])

        checkbox_files_no_limit.setChecked(self.default_settings['ngram']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['ngram']['files_min'])
        spin_box_files_max.setValue(self.default_settings['ngram']['files_max'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_ngram = wordless_tab.Wordless_Tab(self, self.tr('N-gram'))
    
    table_ngram = wordless_table.Wordless_Table(self,
                                                headers = [
                                                    self.tr('Rank'),
                                                    self.tr('N-grams'),
                                                    self.tr('Total'),
                                                    self.tr('Total (Cumulative)'),
                                                    self.tr('Files Found'),
                                                ])

    table_ngram.button_generate_data = QPushButton(self.tr('Generate N-grams'), self)
    table_ngram.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_ngram.button_generate_data.clicked.connect(lambda: generate_data(tab_ngram, table_ngram))
    table_ngram.button_generate_plot.clicked.connect(lambda: generate_plot(tab_ngram))

    tab_ngram.layout_table.addWidget(table_ngram, 0, 0, 1, 5)
    tab_ngram.layout_table.addWidget(table_ngram.button_generate_data, 1, 0)
    tab_ngram.layout_table.addWidget(table_ngram.button_generate_plot, 1, 1)
    tab_ngram.layout_table.addWidget(table_ngram.button_export_selected, 1, 2)
    tab_ngram.layout_table.addWidget(table_ngram.button_export_all, 1, 3)
    tab_ngram.layout_table.addWidget(table_ngram.button_clear, 1, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

    (checkbox_words,
     checkbox_lowercase,
     checkbox_uppercase,
     checkbox_title_cased,
     checkbox_numerals,
     checkbox_punctuations) = wordless_widgets.wordless_widgets_token_settings(self)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_cased.stateChanged.connect(token_settings_changed)
    checkbox_numerals.stateChanged.connect(token_settings_changed)
    checkbox_punctuations.stateChanged.connect(token_settings_changed)

    layout_token_settings = QGridLayout()
    layout_token_settings.addWidget(checkbox_words, 0, 0)
    layout_token_settings.addWidget(checkbox_lowercase, 0, 1)
    layout_token_settings.addWidget(checkbox_numerals, 1, 0)
    layout_token_settings.addWidget(checkbox_uppercase, 1, 1)
    layout_token_settings.addWidget(checkbox_punctuations, 2, 0)
    layout_token_settings.addWidget(checkbox_title_cased, 2, 1)

    group_box_token_settings.setLayout(layout_token_settings)

    # Search Settings
    group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

    (label_search_term,
     line_edit_search_term,
     list_search_terms,
     checkbox_ignore_case,
     checkbox_lemmatization,
     checkbox_whole_word,
     checkbox_regex,
     checkbox_multi_search,
     checkbox_show_all) = wordless_widgets.wordless_widgets_search_settings(self)

    checkbox_show_all.setText(self.tr('Show All N-grams'))

    label_keyword_position = QLabel(self.tr('Keyword Position:'), self)
    (checkbox_keyword_position_no_limit,
     label_keyword_position_min,
     spin_box_keyword_position_min,
     label_keyword_position_max,
     spin_box_keyword_position_max) = wordless_widgets.wordless_widgets_filter(self)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_ngram.button_generate_data.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_keyword_position_no_limit.stateChanged.connect(search_settings_changed)
    spin_box_keyword_position_min.valueChanged.connect(search_settings_changed)
    spin_box_keyword_position_max.valueChanged.connect(search_settings_changed)
    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)
    checkbox_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search.stateChanged.connect(search_settings_changed)
    checkbox_show_all.stateChanged.connect(search_settings_changed)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_search_term, 0, 0, 1, 4)
    layout_search_settings.addWidget(line_edit_search_term, 1, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_terms, 2, 0, 1, 4)
    layout_search_settings.addWidget(label_keyword_position, 3, 0, 1, 3)
    layout_search_settings.addWidget(checkbox_keyword_position_no_limit, 3, 3)
    layout_search_settings.addWidget(label_keyword_position_min, 4, 0)
    layout_search_settings.addWidget(spin_box_keyword_position_min, 4, 1)
    layout_search_settings.addWidget(label_keyword_position_max, 4, 2)
    layout_search_settings.addWidget(spin_box_keyword_position_max, 4, 3)
    layout_search_settings.addWidget(checkbox_ignore_case, 5, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_lemmatization, 6, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_whole_word, 7, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_regex, 8, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_multi_search, 9, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_show_all, 10, 0, 1, 4)

    group_box_search_settings.setLayout(layout_search_settings)

    # Generation Settings
    group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

    label_ngram_size = QLabel(self.tr('N-gram Size:'), self)
    (checkbox_ngram_size_sync,
     label_ngram_size_min,
     spin_box_ngram_size_min,
     label_ngram_size_max,
     spin_box_ngram_size_max) = wordless_widgets.wordless_widgets_size(self)
    label_allow_skipped_tokens = QLabel(self.tr('Allow Skipped Tokens:'), self)
    spin_box_allow_skipped_tokens = QSpinBox(self)

    spin_box_allow_skipped_tokens.setRange(0, 20)

    checkbox_ngram_size_sync.stateChanged.connect(generation_settings_changed)
    spin_box_ngram_size_min.valueChanged.connect(generation_settings_changed)
    spin_box_ngram_size_max.valueChanged.connect(generation_settings_changed)
    spin_box_allow_skipped_tokens.valueChanged.connect(generation_settings_changed)

    layout_generation_settings = QGridLayout()
    layout_generation_settings.addWidget(label_ngram_size, 0, 0, 1, 3)
    layout_generation_settings.addWidget(checkbox_ngram_size_sync, 0, 3)
    layout_generation_settings.addWidget(label_ngram_size_min, 1, 0)
    layout_generation_settings.addWidget(spin_box_ngram_size_min, 1, 1)
    layout_generation_settings.addWidget(label_ngram_size_max, 1, 2)
    layout_generation_settings.addWidget(spin_box_ngram_size_max, 1, 3)
    layout_generation_settings.addWidget(label_allow_skipped_tokens, 2, 0, 1, 3)
    layout_generation_settings.addWidget(spin_box_allow_skipped_tokens, 2, 3)

    group_box_generation_settings.setLayout(layout_generation_settings)

    # Table Settings
    group_box_table_settings = QGroupBox(self.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self, table_ngram)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    layout_table_settings = QGridLayout()
    layout_table_settings.addWidget(checkbox_show_pct, 0, 0)
    layout_table_settings.addWidget(checkbox_show_cumulative, 1, 0)
    layout_table_settings.addWidget(checkbox_show_breakdown, 2, 0)

    group_box_table_settings.setLayout(layout_table_settings)

    # Plot Settings
    group_box_plot_settings = QGroupBox(self.tr('Plot Settings'), self)

    label_rank = QLabel(self.tr('Rank:'), self)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(self, 1, 10000)
    checkbox_cumulative = QCheckBox(self.tr('Cumulative'), self)

    checkbox_rank_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)
    checkbox_cumulative.stateChanged.connect(plot_settings_changed)

    layout_plot_settings = QGridLayout()
    layout_plot_settings.addWidget(label_rank, 0, 0, 1, 3)
    layout_plot_settings.addWidget(checkbox_rank_no_limit, 0, 3)
    layout_plot_settings.addWidget(label_rank_min, 1, 0)
    layout_plot_settings.addWidget(spin_box_rank_min, 1, 1)
    layout_plot_settings.addWidget(label_rank_max, 1, 2)
    layout_plot_settings.addWidget(spin_box_rank_max, 1, 3)
    layout_plot_settings.addWidget(checkbox_cumulative, 2, 0, 1, 4)

    group_box_plot_settings.setLayout(layout_plot_settings)

    # Filter Settings
    group_box_filter_settings = QGroupBox(self.tr('Filter Settings'), self)

    label_freq = QLabel(self.tr('Frequency:'), self)
    (checkbox_freq_no_limit,
     label_freq_min,
     spin_box_freq_min,
     label_freq_max,
     spin_box_freq_max,
     label_freq_apply_to,
     table_ngram.combo_box_freq_apply_to) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 0,
                                                                                     filter_max = 10000,
                                                                                     table = table_ngram,
                                                                                     column = 'Total')

    label_len = QLabel(self.tr('N-gram Length:'), self)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(self, table = table_ngram, column = 'N-grams')

    label_files = QLabel(self.tr('Files Found:'), self)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(self, filter_min = 1, filter_max = 1000,
                                                                    table = table_ngram, column = 'Files Found')

    checkbox_freq_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_min.editingFinished.connect(filter_settings_changed)
    spin_box_freq_max.editingFinished.connect(filter_settings_changed)
    table_ngram.combo_box_freq_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.editingFinished.connect(filter_settings_changed)
    spin_box_len_max.editingFinished.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.editingFinished.connect(filter_settings_changed)
    spin_box_files_max.editingFinished.connect(filter_settings_changed)

    layout_filter_settings = QGridLayout()
    layout_filter_settings.addWidget(label_freq, 0, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_freq_no_limit, 0, 3)
    layout_filter_settings.addWidget(label_freq_min, 1, 0)
    layout_filter_settings.addWidget(spin_box_freq_min, 1, 1)
    layout_filter_settings.addWidget(label_freq_max, 1, 2)
    layout_filter_settings.addWidget(spin_box_freq_max, 1, 3)
    layout_filter_settings.addWidget(label_freq_apply_to, 2, 0)
    layout_filter_settings.addWidget(table_ngram.combo_box_freq_apply_to, 2, 1, 1, 3)

    layout_filter_settings.addWidget(label_len, 4, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_len_no_limit, 4, 3)
    layout_filter_settings.addWidget(label_len_min, 5, 0)
    layout_filter_settings.addWidget(spin_box_len_min, 5, 1)
    layout_filter_settings.addWidget(label_len_max, 5, 2)
    layout_filter_settings.addWidget(spin_box_len_max, 5, 3)

    layout_filter_settings.addWidget(label_files, 6, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_files_no_limit, 6, 3)
    layout_filter_settings.addWidget(label_files_min, 7, 0)
    layout_filter_settings.addWidget(spin_box_files_min, 7, 1)
    layout_filter_settings.addWidget(label_files_max, 7, 2)
    layout_filter_settings.addWidget(spin_box_files_max, 7, 3)

    group_box_filter_settings.setLayout(layout_filter_settings)

    tab_ngram.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    tab_ngram.button_restore_defaults.clicked.connect(restore_defaults)

    restore_defaults()

    return tab_ngram

@wordless_misc.check_search_term
@wordless_misc.check_results_table
def generate_data(self, table):
    table.clear_table()

    files = wordless_misc.fetch_files(self)
    
    # Update filter settings
    apply_to_text_old = table.combo_box_freq_apply_to.currentText()
    table.combo_box_freq_apply_to.clear()

    for i, file in enumerate(files):
        table.insert_column(table.find_column(self.tr('Total')), file.name)
        table.insert_column(table.find_column(self.tr('Total')), file.name + self.tr(' (Cumulative)'))

        table.combo_box_freq_apply_to.addItem(file.name)
    table.combo_box_freq_apply_to.addItem('Total')

    if apply_to_text_old == file.name:
        table.combo_box_freq_apply_to.setCurrentText(file.name)

    table.cols_pct = list(range(2, table.columnCount()))

    freq_distributions = wordless_distribution.wordless_freq_distributions(self, files, mode = 'ngram')

    col_total = table.find_column(self.tr('Total'))
    col_files_found = table.find_column(self.tr('Files Found'))

    freqs_files = [freqs for freqs in zip(*freq_distributions.values())]
    total_files = [sum(freqs) for freqs in freqs_files]
    freqs_total = sum([sum(freqs) for freqs in freqs_files])
    len_files = len(files)

    table.setSortingEnabled(False)
    table.setUpdatesEnabled(False)
    table.setRowCount(len(freq_distributions))

    for i, (ngram, freqs) in enumerate(freq_distributions.items()):
        # N-gram
        table.setItem(i, 1, wordless_table.Wordless_Table_Item(ngram))

        # Frequency
        for j, freq in enumerate(freqs):
            table.set_item_with_pct(i, 2 + j * 2, freq, total_files[j])

        # Total
        table.set_item_with_pct(i, col_total, sum(freqs), freqs_total)

        # Files Found
        table.set_item_with_pct(i, col_files_found, len([freq for freq in freqs if freq > 0]), len_files)

    table.sortByColumn(table.find_column('N-grams') + 1, Qt.DescendingOrder)

    table.combo_box_freq_apply_to.currentTextChanged.emit('')

    table.setSortingEnabled(True)
    table.setUpdatesEnabled(True)

    self.status_bar.showMessage(self.tr('Done!'))

@wordless_misc.check_search_term
def generate_plot(self):
    files = wordless_misc.fetch_files(self)

    freq_distributions = wordless_distribution.wordless_freq_distributions(self, files, mode = 'ngram')

    freq_distributions.plot(files = files,
                            start = self.settings['ngram']['rank_min'] - 1,
                            end = self.settings['ngram']['rank_max'],
                            cumulative = self.settings['ngram']['cumulative'])

    self.status_bar.showMessage(self.tr('Done!'))
