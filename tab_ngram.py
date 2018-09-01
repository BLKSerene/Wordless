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

class Wordless_Table_Ngram(wordless_table.Wordless_Table):
    def __init__(self, parent, headers, stretch_columns = []):
        super().__init__(parent, headers = headers, stretch_columns = stretch_columns)

        self.item_changed()

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
        self.settings['ngram']['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        self.settings['ngram']['ngram_size_min'] = spin_box_ngram_size_min.value()
        self.settings['ngram']['ngram_size_max'] = spin_box_ngram_size_max.value()

        self.settings['ngram']['search_term_position_left'] = checkbox_search_term_position_left.isChecked()
        self.settings['ngram']['search_term_position_middle'] = checkbox_search_term_position_middle.isChecked()
        self.settings['ngram']['search_term_position_right'] = checkbox_search_term_position_right.isChecked()
        self.settings['ngram']['ignore_case'] = checkbox_ignore_case.isChecked()
        self.settings['ngram']['lemmatization'] = checkbox_lemmatization.isChecked()
        self.settings['ngram']['whole_word'] = checkbox_whole_word.isChecked()
        self.settings['ngram']['regex'] = checkbox_regex.isChecked()
        self.settings['ngram']['multi_search'] = checkbox_multi_search.isChecked()
        self.settings['ngram']['show_all'] = checkbox_show_all.isChecked()

        if self.settings['ngram']['multi_search']:
            list_search_terms.get_items()
        else:
            if line_edit_search_term.text():
                self.settings['ngram']['search_terms'] = [line_edit_search_term.text()]
            else:
                self.settings['ngram']['search_terms'] = []

        if self.settings['ngram']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if self.settings['ngram']['show_all']:
            table_ngram.button_generate_ngrams.setText(self.tr('Generate N-grams'))
            label_ngram_size.setText(self.tr('N-gram Size:'))

            checkbox_search_term_position_left.setEnabled(False)
            checkbox_search_term_position_middle.setEnabled(False)
            checkbox_search_term_position_right.setEnabled(False)
        else:
            table_ngram.button_generate_ngrams.setText(self.tr('Generate Word Clusters'))
            label_ngram_size.setText(self.tr('Cluster Size:'))

            checkbox_search_term_position_left.setEnabled(True)
            checkbox_search_term_position_middle.setEnabled(True)
            checkbox_search_term_position_right.setEnabled(True)

    def display_settings_changed():
        self.settings['ngram']['show_pct'] = checkbox_show_pct.isChecked()
        self.settings['ngram']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        self.settings['ngram']['show_breakdown'] = checkbox_show_breakdown.isChecked()

        table_ngram.show_pct = self.settings['ngram']['show_pct']

    def plot_settings_changed():
        self.settings['ngram']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['ngram']['freq_first_no_limit'] = checkbox_freq_first.isChecked()
        self.settings['ngram']['freq_first_min'] = spin_box_freq_first_min.value()
        self.settings['ngram']['freq_first_max'] = (float('inf')
                                                   if checkbox_freq_first.isChecked()
                                                   else spin_box_freq_first_max.value())

        self.settings['ngram']['freq_total_no_limit'] = checkbox_freq_total.isChecked()
        self.settings['ngram']['freq_total_min'] = spin_box_freq_total_min.value()
        self.settings['ngram']['freq_total_max'] = (float('inf')
                                                   if checkbox_freq_total.isChecked()
                                                   else spin_box_freq_total_max.value())

        self.settings['ngram']['rank_no_limit'] = checkbox_rank.isChecked()
        self.settings['ngram']['rank_min'] = spin_box_rank_min.value()
        self.settings['ngram']['rank_max'] = (float('inf')
                                             if checkbox_rank.isChecked()
                                             else spin_box_rank_max.value())

        self.settings['ngram']['len_no_limit'] = checkbox_len.isChecked()
        self.settings['ngram']['len_min'] = spin_box_len_min.value()
        self.settings['ngram']['len_max'] = (float('inf')
                                            if checkbox_len.isChecked()
                                            else spin_box_len_max.value())

        self.settings['ngram']['files_no_limit'] = checkbox_files.isChecked()
        self.settings['ngram']['files_min'] = spin_box_files_min.value()
        self.settings['ngram']['files_max'] = (float('inf')
                                              if checkbox_files.isChecked()
                                              else spin_box_files_max.value())

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['ngram']['words'])
        checkbox_lowercase.setChecked(self.default_settings['ngram']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['ngram']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['ngram']['title_cased'])
        checkbox_numerals.setChecked(self.default_settings['ngram']['numerals'])
        checkbox_punctuations.setChecked(self.default_settings['ngram']['punctuations'])

        checkbox_ngram_size_sync.setChecked(self.default_settings['ngram']['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(self.default_settings['ngram']['ngram_size_min'])
        spin_box_ngram_size_max.setValue(self.default_settings['ngram']['ngram_size_max'])
        line_edit_search_term.clear()
        list_search_terms.clear()
        checkbox_search_term_position_left.setChecked(self.default_settings['ngram']['search_term_position_left'])
        checkbox_search_term_position_middle.setChecked(self.default_settings['ngram']['search_term_position_middle'])
        checkbox_search_term_position_right.setChecked(self.default_settings['ngram']['search_term_position_right'])
        checkbox_ignore_case.setChecked(self.default_settings['ngram']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['ngram']['lemmatization'])
        checkbox_whole_word.setChecked(self.default_settings['ngram']['whole_word'])
        checkbox_regex.setChecked(self.default_settings['ngram']['regex'])
        checkbox_multi_search.setChecked(self.default_settings['ngram']['multi_search'])
        checkbox_show_all.setChecked(self.default_settings['ngram']['show_all'])

        checkbox_show_pct.setChecked(self.default_settings['ngram']['show_pct'])
        checkbox_show_cumulative.setChecked(self.default_settings['ngram']['show_cumulative'])
        checkbox_show_breakdown.setChecked(self.default_settings['ngram']['show_breakdown'])

        checkbox_cumulative.setChecked(self.default_settings['ngram']['cumulative'])

        checkbox_freq_first.setChecked(self.default_settings['ngram']['freq_first_no_limit'])
        spin_box_freq_first_min.setValue(self.default_settings['ngram']['freq_first_min'])
        spin_box_freq_first_max.setValue(self.default_settings['ngram']['freq_first_max'])
        checkbox_freq_total.setChecked(self.default_settings['ngram']['freq_total_no_limit'])
        spin_box_freq_total_min.setValue(self.default_settings['ngram']['freq_total_min'])
        spin_box_freq_total_max.setValue(self.default_settings['ngram']['freq_total_max'])
        checkbox_rank.setChecked(self.default_settings['ngram']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['ngram']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['ngram']['rank_max'])
        checkbox_len.setChecked(self.default_settings['ngram']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['ngram']['len_min'])
        spin_box_len_max.setValue(self.default_settings['ngram']['len_max'])
        checkbox_files.setChecked(self.default_settings['ngram']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['ngram']['files_min'])
        spin_box_files_max.setValue(self.default_settings['ngram']['files_max'])

        token_settings_changed()
        search_settings_changed()
        display_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_ngram = QWidget(self)
    
    table_ngram = Wordless_Table_Ngram(self,
                                       [
                                           self.tr('Rank'),
                                           self.tr('N-grams'),
                                           self.tr('Total'),
                                           self.tr('Total (Cumulative)'),
                                           self.tr('Files Found'),
                                       ])

    table_ngram.button_generate_ngrams = QPushButton(self.tr('Generate N-grams'), self)
    table_ngram.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_ngram.button_generate_ngrams.clicked.connect(lambda: generate_ngrams(self, table_ngram))
    table_ngram.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    layout_ngram_left = QGridLayout()
    layout_ngram_left.addWidget(table_ngram, 0, 0, 1, 5)
    layout_ngram_left.addWidget(table_ngram.button_generate_ngrams, 1, 0)
    layout_ngram_left.addWidget(table_ngram.button_generate_plot, 1, 1)
    layout_ngram_left.addWidget(table_ngram.button_export_selected, 1, 2)
    layout_ngram_left.addWidget(table_ngram.button_export_all, 1, 3)
    layout_ngram_left.addWidget(table_ngram.button_clear, 1, 4)

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

    label_ngram_size = QLabel(self.tr('N-gram Size:'), self)
    (checkbox_ngram_size_sync,
     label_ngram_size_min,
     spin_box_ngram_size_min,
     label_ngram_size_max,
     spin_box_ngram_size_max) = wordless_widgets.wordless_widgets_size(self)

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

    label_search_term_position = QLabel(self.tr('Search Term Position:'), self)
    checkbox_search_term_position_left = QCheckBox(self.tr('At Left'), self)
    checkbox_search_term_position_middle = QCheckBox(self.tr('In Middle'), self)
    checkbox_search_term_position_right = QCheckBox(self.tr('At Right'), self)

    spin_box_ngram_size_min.setRange(1, 100)
    spin_box_ngram_size_max.setRange(1, 100)

    checkbox_ngram_size_sync.stateChanged.connect(search_settings_changed)
    spin_box_ngram_size_min.valueChanged.connect(search_settings_changed)
    spin_box_ngram_size_max.valueChanged.connect(search_settings_changed)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_ngram.button_generate_ngrams.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_search_term_position_left.stateChanged.connect(search_settings_changed)
    checkbox_search_term_position_middle.stateChanged.connect(search_settings_changed)
    checkbox_search_term_position_right.stateChanged.connect(search_settings_changed)
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

    layout_search_term_position = QGridLayout()
    layout_search_term_position.addWidget(label_search_term_position, 0, 0, 1, 3)
    layout_search_term_position.addWidget(checkbox_search_term_position_left, 1, 0)
    layout_search_term_position.addWidget(checkbox_search_term_position_middle, 1, 1)
    layout_search_term_position.addWidget(checkbox_search_term_position_right, 1, 2)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_ngram_size, 0, 0, 1, 3)
    layout_search_settings.addWidget(checkbox_ngram_size_sync, 0, 3)
    layout_search_settings.addWidget(label_ngram_size_min, 1, 0)
    layout_search_settings.addWidget(spin_box_ngram_size_min, 1, 1)
    layout_search_settings.addWidget(label_ngram_size_max, 1, 2)
    layout_search_settings.addWidget(spin_box_ngram_size_max, 1, 3)

    layout_search_settings.addWidget(label_search_term, 2, 0, 1, 4)
    layout_search_settings.addWidget(line_edit_search_term, 3, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_terms, 4, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_term_position, 5, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_ignore_case, 6, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_lemmatization, 7, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_whole_word, 8, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_regex, 9, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_multi_search, 10, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_show_all, 11, 0, 1, 4)

    group_box_search_settings.setLayout(layout_search_settings)

    # Display Settings
    group_box_display_settings = QGroupBox(self.tr('Display Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_display_settings(self, table_ngram)

    checkbox_show_pct.stateChanged.connect(display_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(display_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(display_settings_changed)

    layout_display_settings = QGridLayout()
    layout_display_settings.addWidget(checkbox_show_pct, 0, 0)
    layout_display_settings.addWidget(checkbox_show_cumulative, 1, 0)
    layout_display_settings.addWidget(checkbox_show_breakdown, 2, 0)

    group_box_display_settings.setLayout(layout_display_settings)

    # Plot Settings
    group_box_plot_settings = QGroupBox(self.tr('Plot Settings'), self)

    checkbox_cumulative = QCheckBox(self.tr('Cumulative'), self)

    checkbox_cumulative.stateChanged.connect(plot_settings_changed)

    layout_plot_settings = QGridLayout()
    layout_plot_settings.addWidget(checkbox_cumulative, 0, 0)

    group_box_plot_settings.setLayout(layout_plot_settings)

    # Filter Settings
    group_box_filter_settings = QGroupBox(self.tr('Filter Settings'), self)

    label_freq_first = QLabel(self.tr('Frequency (First File):'), self)
    (checkbox_freq_first,
     label_freq_first_min,
     spin_box_freq_first_min,
     label_freq_first_max,
     spin_box_freq_first_max) = wordless_widgets.wordless_widgets_filter_settings(self)

    label_freq_total = QLabel(self.tr('Frequency (Total):'), self)
    (checkbox_freq_total,
     label_freq_total_min,
     spin_box_freq_total_min,
     label_freq_total_max,
     spin_box_freq_total_max) = wordless_widgets.wordless_widgets_filter_settings(self)

    label_rank = QLabel(self.tr('Rank:'), self)
    (checkbox_rank,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter_settings(self)

    label_len = QLabel(self.tr('N-gram Length:'), self)
    (checkbox_len,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter_settings(self)

    label_files = QLabel(self.tr('Files Found:'), self)
    (checkbox_files,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter_settings(self)

    spin_box_freq_first_min.setRange(1, 1000000)
    spin_box_freq_first_max.setRange(1, 1000000)
    spin_box_freq_total_min.setRange(1, 1000000)
    spin_box_freq_total_max.setRange(1, 1000000)
    spin_box_rank_min.setRange(1, 1000000)
    spin_box_rank_max.setRange(1, 1000000)
    spin_box_len_min.setRange(1, 100)
    spin_box_len_max.setRange(1, 100)
    spin_box_files_min.setRange(1, 10000)
    spin_box_files_max.setRange(1, 10000)

    checkbox_freq_first.stateChanged.connect(filter_settings_changed)
    spin_box_freq_first_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_first_max.valueChanged.connect(filter_settings_changed)
    checkbox_freq_total.stateChanged.connect(filter_settings_changed)
    spin_box_freq_total_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_total_max.valueChanged.connect(filter_settings_changed)
    checkbox_rank.stateChanged.connect(filter_settings_changed)
    spin_box_rank_min.valueChanged.connect(filter_settings_changed)
    spin_box_rank_max.valueChanged.connect(filter_settings_changed)
    checkbox_len.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.valueChanged.connect(filter_settings_changed)
    spin_box_len_max.valueChanged.connect(filter_settings_changed)
    checkbox_files.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.valueChanged.connect(filter_settings_changed)
    spin_box_files_max.valueChanged.connect(filter_settings_changed)

    layout_filter_settings = QGridLayout()
    layout_filter_settings.addWidget(label_freq_first, 0, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_freq_first, 0, 3)
    layout_filter_settings.addWidget(label_freq_first_min, 1, 0)
    layout_filter_settings.addWidget(spin_box_freq_first_min, 1, 1)
    layout_filter_settings.addWidget(label_freq_first_max, 1, 2)
    layout_filter_settings.addWidget(spin_box_freq_first_max, 1, 3)

    layout_filter_settings.addWidget(label_freq_total, 2, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_freq_total, 2, 3)
    layout_filter_settings.addWidget(label_freq_total_min, 3, 0)
    layout_filter_settings.addWidget(spin_box_freq_total_min, 3, 1)
    layout_filter_settings.addWidget(label_freq_total_max, 3, 2)
    layout_filter_settings.addWidget(spin_box_freq_total_max, 3, 3)

    layout_filter_settings.addWidget(label_rank, 4, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_rank, 4, 3)
    layout_filter_settings.addWidget(label_rank_min, 5, 0)
    layout_filter_settings.addWidget(spin_box_rank_min, 5, 1)
    layout_filter_settings.addWidget(label_rank_max, 5, 2)
    layout_filter_settings.addWidget(spin_box_rank_max, 5, 3)

    layout_filter_settings.addWidget(label_len, 6, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_len, 6, 3)
    layout_filter_settings.addWidget(label_len_min, 7, 0)
    layout_filter_settings.addWidget(spin_box_len_min, 7, 1)
    layout_filter_settings.addWidget(label_len_max, 7, 2)
    layout_filter_settings.addWidget(spin_box_len_max, 7, 3)

    layout_filter_settings.addWidget(label_files, 8, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_files, 8, 3)
    layout_filter_settings.addWidget(label_files_min, 9, 0)
    layout_filter_settings.addWidget(spin_box_files_min, 9, 1)
    layout_filter_settings.addWidget(label_files_max, 9, 2)
    layout_filter_settings.addWidget(spin_box_files_max, 9, 3)

    group_box_filter_settings.setLayout(layout_filter_settings)

    # Scroll Area Wrapper
    wrapper_settings = QWidget(self)

    layout_settings = QGridLayout()
    layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    layout_settings.addWidget(group_box_display_settings, 2, 0, Qt.AlignTop)
    layout_settings.addWidget(group_box_plot_settings, 3, 0, Qt.AlignTop)
    layout_settings.addWidget(group_box_filter_settings, 4, 0, Qt.AlignTop)

    wrapper_settings.setLayout(layout_settings)

    scroll_area_settings = wordless_widgets.Wordless_Scroll_Area(self)
    scroll_area_settings.setWidget(wrapper_settings)

    button_advanced_settings = QPushButton(self.tr('Advanced Settings'), self)
    button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self)

    button_advanced_settings.clicked.connect(lambda: self.wordless_settings.settings_load('N-gram'))
    button_restore_defaults.clicked.connect(restore_defaults)

    layout_ngram = QGridLayout()
    layout_ngram.addLayout(layout_ngram_left, 0, 0, 2, 1)
    layout_ngram.addWidget(scroll_area_settings, 0, 1, 1, 2)
    layout_ngram.addWidget(button_advanced_settings, 1, 1)
    layout_ngram.addWidget(button_restore_defaults, 1, 2)

    layout_ngram.setColumnStretch(0, 8)
    layout_ngram.setColumnStretch(1, 1)
    layout_ngram.setColumnStretch(2, 1)

    tab_ngram.setLayout(layout_ngram)

    restore_defaults()

    return tab_ngram

def generate_ngrams(self, table):
    if (self.settings['ngram']['show_all'] or
        not self.settings['ngram']['show_all'] and self.settings['ngram']['search_terms']):
        freq_previous = -1
        freq_cumulative = 0
        total_cumulative = 0

        table.clear_table()

        files = wordless_misc.fetch_files(self)
        
        for i, file in enumerate(files):
            table.insert_column(table.find_column(self.tr('Total')), file.name)
            table.insert_column(table.find_column(self.tr('Total')), file.name + self.tr(' (Cumulative)'))

        freq_distributions = wordless_freq.wordless_freq_distributions(self, files, mode = 'ngram')

        col_total = table.find_column(self.tr('Total'))
        col_total_cumulative = table.find_column(self.tr('Total (Cumulative)'))
        col_files_found = table.find_column(self.tr('Files Found'))

        freqs_files = [freqs for freqs in zip(*freq_distributions.values())]
        total_files = [sum(freqs) for freqs in freqs_files]
        freqs_total = sum([sum(freqs) for freqs in freqs_files])
        len_files = len(files)

        table.setSortingEnabled(False)
        table.setRowCount(len(freq_distributions))

        for i, (ngram, freqs) in enumerate(freq_distributions.items()):
            # Rank
            table.setItem(i, 0, QTableWidgetItem())
            if freqs[0] == freq_previous:
                table.item(i, 0).setData(Qt.DisplayRole, table.item(i - 1, 0).data(Qt.DisplayRole))
            else:
                table.item(i, 0).setData(Qt.DisplayRole, i + 1)

            # N-gram
            table.setItem(i, 1, QTableWidgetItem(ngram))

            # Frequency
            for j, freq in enumerate(freqs):
                table.set_item_with_pct(i, 2 + j * 2, freq, total_files[j])

                freq_cumulative += freq

                # Frequency (Cumulative)
                table.set_item_with_pct(i, 3 + j * 2, freq_cumulative, total_files[j])

            # Total
            table.set_item_with_pct(i, col_total, sum(freqs), freqs_total)

            total_cumulative += sum(freqs)

            # Total (Cumulative)
            table.set_item_with_pct(i, col_total_cumulative, total_cumulative, total_files[j])

            # Files Found
            table.set_item_with_pct(i, col_files_found, len([freq for freq in freqs if freq]), len_files)

            freq_previous = freqs[0]

        table.setSortingEnabled(True)

        if table.rowCount() > 0:
            table.sortByColumn(table.find_column('N-grams') + 1, Qt.DescendingOrder)
        else:
            table.clear_table()

            QMessageBox.information(self,
                                    self.tr('No Search Results'),
                                    self.tr('There are no results for your search!<br>You might want to change your settings and try it again.'),
                                    QMessageBox.Ok)
    else:
        QMessageBox.warning(self,
                            self.tr('Search Failed'),
                            self.tr('Please enter your search term(s) first!'),
                            QMessageBox.Ok)
        
    self.status_bar.showMessage(self.tr('Done!'))

def generate_plot(self):
    freq_distributions = wordless_freq.wordless_freq_distributions(self, wordless_misc.fetch_files(self), mode = 'ngrams')

    freq_distributions.plot(cumulative = self.settings['ngrams']['cumulative'])

    self.status_bar.showMessage(self.tr('Done!'))
