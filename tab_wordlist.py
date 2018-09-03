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

    def table_settings_changed():
        self.settings['wordlist']['show_pct'] = checkbox_show_pct.isChecked()
        self.settings['wordlist']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        self.settings['wordlist']['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        self.settings['wordlist']['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        self.settings['wordlist']['rank_min'] = spin_box_rank_min.value()
        self.settings['wordlist']['rank_max'] = (None
                                                 if checkbox_rank_no_limit.isChecked()
                                                 else spin_box_rank_max.value())

        self.settings['wordlist']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['wordlist']['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        self.settings['wordlist']['freq_min'] = spin_box_freq_min.value()
        self.settings['wordlist']['freq_max'] = (float('inf')
                                                 if checkbox_freq_no_limit.isChecked()
                                                 else spin_box_freq_max.value())
        self.settings['wordlist']['freq_apply_to'] = table_wordlist.combo_box_freq_apply_to.currentText()

        self.settings['wordlist']['len_no_limit'] = checkbox_len_no_limit.isChecked()
        self.settings['wordlist']['len_min'] = spin_box_len_min.value()
        self.settings['wordlist']['len_max'] = (float('inf')
                                                if checkbox_len_no_limit.isChecked()
                                                else spin_box_len_max.value())

        self.settings['wordlist']['files_no_limit'] = checkbox_files_no_limit.isChecked()
        self.settings['wordlist']['files_min'] = spin_box_files_min.value()
        self.settings['wordlist']['files_max'] = (float('inf')
                                                  if checkbox_files_no_limit.isChecked()
                                                  else spin_box_files_max.value())

        checkbox_show_pct.stateChanged.emit(self.settings['wordlist']['show_pct'])

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

        checkbox_rank_no_limit.setChecked(self.default_settings['wordlist']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['wordlist']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['wordlist']['rank_max'])
        checkbox_cumulative.setChecked(self.default_settings['wordlist']['cumulative'])

        checkbox_freq_no_limit.setChecked(self.default_settings['wordlist']['freq_no_limit'])
        spin_box_freq_min.setValue(self.default_settings['wordlist']['freq_min'])
        spin_box_freq_max.setValue(self.default_settings['wordlist']['freq_max'])
        table_wordlist.combo_box_freq_apply_to.setCurrentText(self.default_settings['wordlist']['freq_apply_to'])

        checkbox_len_no_limit.setChecked(self.default_settings['wordlist']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['wordlist']['len_min'])
        spin_box_len_max.setValue(self.default_settings['wordlist']['len_max'])

        checkbox_files_no_limit.setChecked(self.default_settings['wordlist']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['wordlist']['files_min'])
        spin_box_files_max.setValue(self.default_settings['wordlist']['files_max'])

        token_settings_changed()
        search_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_wordlist = wordless_tab.Wordless_Tab(self, self.tr('Wordlist'))

    table_wordlist = wordless_table.Wordless_Table(self,
                                                   headers = [
                                                       self.tr('Rank'),
                                                       self.tr('Tokens'),
                                                       self.tr('Total'),
                                                       self.tr('Total (Cumulative)'),
                                                       self.tr('Files Found'),
                                                   ])

    table_wordlist.button_generate_data = QPushButton(self.tr('Generate Wordlist'), self)
    table_wordlist.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_wordlist.button_generate_data.clicked.connect(lambda: generate_data(table_wordlist))
    table_wordlist.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    tab_wordlist.layout_table.addWidget(table_wordlist, 0, 0, 1, 5)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_generate_data, 1, 0)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_generate_plot, 1, 1)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_export_selected, 1, 2)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_export_all, 1, 3)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_clear, 1, 4)

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
    layout_token_settings.addWidget(checkbox_uppercase, 1, 1)
    layout_token_settings.addWidget(checkbox_title_cased, 2, 1)
    layout_token_settings.addWidget(checkbox_numerals, 1, 0)
    layout_token_settings.addWidget(checkbox_punctuations, 2, 0)

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

    label_search_term.hide()
    line_edit_search_term.hide()
    list_search_terms.hide()
    checkbox_whole_word.hide()
    checkbox_regex.hide()
    checkbox_multi_search.hide()
    checkbox_show_all.hide()

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(checkbox_ignore_case, 0, 0)
    layout_search_settings.addWidget(checkbox_lemmatization, 1, 0)

    group_box_search_settings.setLayout(layout_search_settings)

    # Table Settings
    group_box_table_settings = QGroupBox(self.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self, table_wordlist)

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
     table_wordlist.combo_box_freq_apply_to) = wordless_widgets.wordless_widgets_filter(self,
                                                                                        filter_min = 0,
                                                                                        filter_max = 10000,
                                                                                        table = table_wordlist,
                                                                                        column = 'Total')

    label_len = QLabel(self.tr('Token Length:'), self)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(self, table = table_wordlist, column = 'Tokens')

    label_files = QLabel(self.tr('Files Found:'), self)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(self, filter_min = 1, filter_max = 1000,
                                                                    table = table_wordlist, column = 'Files Found')

    checkbox_freq_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_min.editingFinished.connect(filter_settings_changed)
    spin_box_freq_max.editingFinished.connect(filter_settings_changed)
    table_wordlist.combo_box_freq_apply_to.currentTextChanged.connect(filter_settings_changed)

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
    layout_filter_settings.addWidget(table_wordlist.combo_box_freq_apply_to, 2, 1, 1, 3)

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

    tab_wordlist.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_table_settings, 2, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_plot_settings, 3, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_filter_settings, 4, 0, Qt.AlignTop)

    tab_wordlist.button_restore_defaults.clicked.connect(restore_defaults)

    restore_defaults()

    return tab_wordlist

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

    freq_distributions = wordless_distribution.wordless_distributions(self, files, mode = 'wordlist')

    col_total = table.find_column(self.tr('Total'))
    col_files_found = table.find_column(self.tr('Files Found'))

    freqs_files = [freqs for freqs in zip(*freq_distributions.values())]
    total_files = [sum(freqs) for freqs in freqs_files]
    freqs_total = sum([sum(freqs) for freqs in freqs_files])
    len_files = len(files)

    table.setSortingEnabled(False)
    table.setUpdatesEnabled(False)
    table.setRowCount(len(freq_distributions))

    for i, (token, freqs) in enumerate(freq_distributions.items()):
        # Tokens
        table.setItem(i, 1, wordless_table.Wordless_Table_Item(token))

        # Frequency
        for j, freq in enumerate(freqs):
            table.set_item_with_pct(i, 2 + j * 2, freq, total_files[j])

        # Total
        table.set_item_with_pct(i, col_total, sum(freqs), freqs_total)

        # Files Found
        table.set_item_with_pct(i, col_files_found, len([freq for freq in freqs if freq > 0]), len_files)

    table.sortByColumn(table.find_column('Tokens') + 1, Qt.DescendingOrder)

    table.combo_box_freq_apply_to.currentTextChanged.emit('')

    table.setSortingEnabled(True)
    table.setUpdatesEnabled(True)
        
    self.status_bar.showMessage(self.tr('Done!'))

def generate_plot(self):
    files = wordless_misc.fetch_files(self)

    freq_distributions = wordless_distribution.wordless_distributions(self, files, mode = 'wordlist')

    freq_distributions.plot(files = files,
                            start = self.settings['wordlist']['rank_min'] - 1,
                            end = self.settings['wordlist']['rank_max'],
                            cumulative = self.settings['wordlist']['cumulative'])

    self.status_bar.showMessage(self.tr('Done!'))
