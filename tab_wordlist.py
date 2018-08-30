#
# Wordless: Wordlist
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_utils import *

class Wordless_Table_Wordlist(wordless_table.Wordless_Table):
    def __init__(self, parent, headers):
        super().__init__(parent, headers)

        self.item_changed()

def init(self):
    def token_settings_changed():
        self.settings['wordlist']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        self.settings['wordlist']['lowercase'] = checkbox_lowercase.isChecked()
        self.settings['wordlist']['uppercase'] = checkbox_uppercase.isChecked()
        self.settings['wordlist']['title_cased'] = checkbox_title_cased.isChecked()
        self.settings['wordlist']['numerals'] = checkbox_numerals.isChecked()
        self.settings['wordlist']['punctuations'] = checkbox_punctuations.isChecked()

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
        self.settings['wordlist']['ignore_case'] = checkbox_ignore_case.isChecked()
        self.settings['wordlist']['lemmatization'] = checkbox_lemmatization.isChecked()

        if self.settings['wordlist']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

    def display_settings_changed():
        self.settings['wordlist']['show_pct'] = checkbox_show_pct.isChecked()
        self.settings['wordlist']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        self.settings['wordlist']['show_breakdown'] = checkbox_show_breakdown.isChecked()

        table_wordlist.show_pct = self.settings['wordlist']['show_pct']

    def plot_settings_changed():
        self.settings['wordlist']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['wordlist']['freq_first_no_limit'] = checkbox_freq_first.isChecked()
        self.settings['wordlist']['freq_first_min'] = spin_box_freq_first_min.value()
        self.settings['wordlist']['freq_first_max'] = (float('inf')
                                                       if checkbox_freq_first.isChecked()
                                                       else spin_box_freq_first_max.value())

        self.settings['wordlist']['freq_total_no_limit'] = checkbox_freq_total.isChecked()
        self.settings['wordlist']['freq_total_min'] = spin_box_freq_total_min.value()
        self.settings['wordlist']['freq_total_max'] = (float('inf')
                                                       if checkbox_freq_total.isChecked()
                                                       else spin_box_freq_total_max.value())

        self.settings['wordlist']['rank_no_limit'] = checkbox_rank.isChecked()
        self.settings['wordlist']['rank_min'] = spin_box_rank_min.value()
        self.settings['wordlist']['rank_max'] = (float('inf')
                                                 if checkbox_rank.isChecked()
                                                 else spin_box_rank_max.value())

        self.settings['wordlist']['len_no_limit'] = checkbox_len.isChecked()
        self.settings['wordlist']['len_min'] = spin_box_len_min.value()
        self.settings['wordlist']['len_max'] = (float('inf')
                                                if checkbox_len.isChecked()
                                                else spin_box_len_max.value())

        self.settings['wordlist']['files_no_limit'] = checkbox_files.isChecked()
        self.settings['wordlist']['files_min'] = spin_box_files_min.value()
        self.settings['wordlist']['files_max'] = (float('inf')
                                                  if checkbox_files.isChecked()
                                                  else spin_box_files_max.value())

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['wordlist']['words'])
        checkbox_lowercase.setChecked(self.default_settings['wordlist']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['wordlist']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['wordlist']['title_cased'])
        checkbox_punctuations.setChecked(self.default_settings['wordlist']['punctuations'])
        checkbox_numerals.setChecked(self.default_settings['wordlist']['numerals'])

        checkbox_ignore_case.setChecked(self.default_settings['wordlist']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['wordlist']['lemmatization'])

        checkbox_show_pct.setChecked(self.default_settings['wordlist']['show_pct'])
        checkbox_show_cumulative.setChecked(self.default_settings['wordlist']['show_cumulative'])
        checkbox_show_breakdown.setChecked(self.default_settings['wordlist']['show_breakdown'])

        checkbox_cumulative.setChecked(self.default_settings['wordlist']['cumulative'])

        checkbox_freq_first.setChecked(self.default_settings['wordlist']['freq_first_no_limit'])
        spin_box_freq_first_min.setValue(self.default_settings['wordlist']['freq_first_min'])
        spin_box_freq_first_max.setValue(self.default_settings['wordlist']['freq_first_max'])
        checkbox_freq_total.setChecked(self.default_settings['wordlist']['freq_total_no_limit'])
        spin_box_freq_total_min.setValue(self.default_settings['wordlist']['freq_total_min'])
        spin_box_freq_total_max.setValue(self.default_settings['wordlist']['freq_total_max'])
        checkbox_rank.setChecked(self.default_settings['wordlist']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['wordlist']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['wordlist']['rank_max'])
        checkbox_len.setChecked(self.default_settings['wordlist']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['wordlist']['len_min'])
        spin_box_len_max.setValue(self.default_settings['wordlist']['len_max'])
        checkbox_files.setChecked(self.default_settings['wordlist']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['wordlist']['files_min'])
        spin_box_files_max.setValue(self.default_settings['wordlist']['files_max'])

        token_settings_changed()
        search_settings_changed()
        display_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_wordlist = QWidget(self)

    table_wordlist = Wordless_Table_Wordlist(self, [
                                                       self.tr('Rank'),
                                                       self.tr('Tokens'),
                                                       self.tr('Total'),
                                                       self.tr('Total (Cumulative)'),
                                                       self.tr('Files Found'),
                                                   ])

    table_wordlist.button_generate_wordlist = QPushButton(self.tr('Generate Wordlist'), self)
    table_wordlist.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_wordlist.button_generate_wordlist.clicked.connect(lambda: generate_wordlist(self, table_wordlist))
    table_wordlist.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    layout_wordlist_left = QGridLayout()
    layout_wordlist_left.addWidget(table_wordlist, 0, 0, 1, 5)
    layout_wordlist_left.addWidget(table_wordlist.button_generate_wordlist, 1, 0)
    layout_wordlist_left.addWidget(table_wordlist.button_generate_plot, 1, 1)
    layout_wordlist_left.addWidget(table_wordlist.button_export_selected, 1, 2)
    layout_wordlist_left.addWidget(table_wordlist.button_export_all, 1, 3)
    layout_wordlist_left.addWidget(table_wordlist.button_clear, 1, 4)

    # Token Settings
    group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

    (checkbox_words,
     checkbox_lowercase,
     checkbox_uppercase,
     checkbox_title_cased,
     checkbox_numerals,
     checkbox_punctuations) = wordless_widgets.wordless_widgets_token_settings(self)

    checkbox_words.clicked.connect(token_settings_changed)
    checkbox_lowercase.clicked.connect(token_settings_changed)
    checkbox_uppercase.clicked.connect(token_settings_changed)
    checkbox_title_cased.clicked.connect(token_settings_changed)
    checkbox_numerals.clicked.connect(token_settings_changed)
    checkbox_punctuations.clicked.connect(token_settings_changed)

    layout_token_settings = QGridLayout()
    layout_token_settings.addWidget(checkbox_words, 0, 0)
    layout_token_settings.addWidget(checkbox_lowercase, 0, 1)
    layout_token_settings.addWidget(checkbox_uppercase, 1, 1)
    layout_token_settings.addWidget(checkbox_title_cased, 2, 1)
    layout_token_settings.addWidget(checkbox_numerals, 1, 0)
    layout_token_settings.addWidget(checkbox_punctuations, 2, 0)

    group_box_token_settings.setLayout(layout_token_settings)

    # Search Settings
    group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

    (checkbox_ignore_case,
     checkbox_lemmatization) = wordless_widgets.wordless_widgets_search_settings(self, widgets = [3, 4])

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(checkbox_ignore_case, 0, 0)
    layout_search_settings.addWidget(checkbox_lemmatization, 1, 0)

    group_box_search_settings.setLayout(layout_search_settings)

    # Display Settings
    group_box_display_settings = QGroupBox(self.tr('Display Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_display_settings(self, table_wordlist)

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
    layout_plot_settings.addWidget(checkbox_cumulative, 0, 0, Qt.AlignTop)

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

    label_len = QLabel(self.tr('Token Length:'), self)
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

    button_advanced_settings.clicked.connect(lambda: self.wordless_settings.settings_load('Wordlist'))
    button_restore_defaults.clicked.connect(restore_defaults)

    layout_wordlist = QGridLayout()
    layout_wordlist.addLayout(layout_wordlist_left, 0, 0, 2, 1)
    layout_wordlist.addWidget(scroll_area_settings, 0, 1, 1, 2)
    layout_wordlist.addWidget(button_advanced_settings, 1, 1)
    layout_wordlist.addWidget(button_restore_defaults, 1, 2)

    layout_wordlist.setColumnStretch(0, 8)
    layout_wordlist.setColumnStretch(1, 1)
    layout_wordlist.setColumnStretch(2, 1)

    tab_wordlist.setLayout(layout_wordlist)

    restore_defaults()

    return tab_wordlist

def generate_wordlist(self, table):
    freq_previous = -1

    table.clear_table(0)

    files = wordless_misc.fetch_files(self)

    for i, file in enumerate(files):
        table.insert_column(table.find_column(self.tr('Total')), file.name)
        table.insert_column(table.find_column(self.tr('Total')), file.name + self.tr(' (Cumulative)'))

    table.setSortingEnabled(False)

    col_total = table.find_column(self.tr('Total'))
    col_total_cumulative = table.find_column(self.tr('Total (Cumulative)'))
    col_files_found = table.find_column(self.tr('Files Found'))

    freq_distributions = wordless_freq.wordless_freq_distributions(self, files, mode = 'wordlist')

    # Calculate the total frequency of all tokens for each file
    freqs_files = [freqs for freqs in zip(*freq_distributions.values())]
    total_files = [sum(freqs) for freqs in freqs_files]

    for i, (token, freqs) in enumerate(freq_distributions.items()):
        table.setRowCount(table.rowCount() + 1)

        # Rank
        table.setItem(i, 0, QTableWidgetItem())
        if freqs[0] == freq_previous:
            table.item(i, 0).setData(Qt.DisplayRole, table.item(i - 1, 0).data(Qt.DisplayRole))
        else:
            table.item(i, 0).setData(Qt.DisplayRole, i + 1)

        # Tokens
        table.setItem(i, 1, QTableWidgetItem(token))

        # Frequency
        for j, freq in enumerate(freqs):
            table.set_item_with_pct(i, 2 + j * 2, freq, total_files[j])
            table.set_item_with_pct(i, 3 + j * 2, sum(freqs_files[j][: i + 1]), total_files[j])

        # Total
        table.set_item_with_pct(i, col_total, sum(freqs), sum(total_files))

        # Total (Cumulative)
        table.set_item_with_pct(i, col_total_cumulative,
                                sum([sum(freqs) for freqs in list(freq_distributions.values())[: i + 1]]),
                                sum(total_files))

        # Files Found
        table.set_item_with_pct(i, col_files_found, len([freq for freq in freqs if freq]), len(files))

        freq_previous = freqs[0]

    if table.rowCount() > 0:
        table.sortByColumn(table.find_column('Tokens') + 1, Qt.DescendingOrder)
    else:
        table.clear_table()

        QMessageBox.information(self,
                                self.tr('No Search Results'),
                                self.tr('There are no results for your search!<br>You might want to change your settings and try it again.'),
                                QMessageBox.Ok)

    table.setSortingEnabled(True)
        
    self.status_bar.showMessage(self.tr('Done!'))

def generate_plot(self):
    freq_distributions = wordless_freq.wordless_freq_distributions(self, wordless_misc.fetch_files(self), mode = 'wordlist')

    freq_distributions.plot(cumulative = self.settings['wordlist']['cumulative'])

    self.status_bar.showMessage(self.tr('Done!'))
