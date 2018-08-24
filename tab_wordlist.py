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
    def token_settings_changed(widget_changed = None):
        if widget_changed == checkbox_words:
            checkbox_words.setTristate(False)

            if checkbox_words.checkState() == Qt.Checked:
                checkbox_lowercase.setEnabled(True)
                checkbox_uppercase.setEnabled(True)
                checkbox_title_cased.setEnabled(True)

                checkbox_ignore_case.setEnabled(True)
                checkbox_lemmatization.setEnabled(True)

                checkbox_lowercase.setChecked(True)
                checkbox_uppercase.setChecked(True)
                checkbox_title_cased.setChecked(True)

                search_settings_changed()
            else:
                checkbox_lowercase.setEnabled(False)
                checkbox_uppercase.setEnabled(False)
                checkbox_title_cased.setEnabled(False)

                checkbox_ignore_case.setEnabled(False)
                checkbox_lemmatization.setEnabled(False)

                checkbox_lowercase.setChecked(False)
                checkbox_uppercase.setChecked(False)
                checkbox_title_cased.setChecked(False)
        else:
            if (checkbox_lowercase.isChecked() and
                checkbox_uppercase.isChecked() and
                checkbox_title_cased.isChecked()):
                checkbox_words.setCheckState(Qt.Checked)
            elif (not checkbox_lowercase.isChecked() and
                  not checkbox_uppercase.isChecked() and
                  not checkbox_title_cased.isChecked()):
                checkbox_words.setCheckState(Qt.Unchecked)

                checkbox_lowercase.setEnabled(False)
                checkbox_uppercase.setEnabled(False)
                checkbox_title_cased.setEnabled(False)

                checkbox_ignore_case.setEnabled(False)
                checkbox_lemmatization.setEnabled(False)
            else:
                checkbox_words.setCheckState(Qt.PartiallyChecked)

        self.settings['wordlist']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        self.settings['wordlist']['lowercase'] = checkbox_lowercase.isChecked()
        self.settings['wordlist']['uppercase'] = checkbox_uppercase.isChecked()
        self.settings['wordlist']['title_cased'] = checkbox_title_cased.isChecked()
        self.settings['wordlist']['numerals'] = checkbox_numerals.isChecked()
        self.settings['wordlist']['punctuations'] = checkbox_punctuations.isChecked()

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

        if self.settings['wordlist']['freq_first_no_limit']:
            spin_box_freq_first_max.setEnabled(False)
        else:
            spin_box_freq_first_max.setEnabled(True)

        if self.settings['wordlist']['freq_total_no_limit']:
            spin_box_freq_total_max.setEnabled(False)
        else:
            spin_box_freq_total_max.setEnabled(True)

        if self.settings['wordlist']['rank_no_limit']:
            spin_box_rank_max.setEnabled(False)
        else:
            spin_box_rank_max.setEnabled(True)

        if self.settings['wordlist']['len_no_limit']:
            spin_box_len_max.setEnabled(False)
        else:
            spin_box_len_max.setEnabled(True)

        if self.settings['wordlist']['files_no_limit']:
            spin_box_files_max.setEnabled(False)
        else:
            spin_box_files_max.setEnabled(True)

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['wordlist']['words'])
        checkbox_lowercase.setChecked(self.default_settings['wordlist']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['wordlist']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['wordlist']['title_cased'])
        checkbox_punctuations.setChecked(self.default_settings['wordlist']['punctuations'])
        checkbox_numerals.setChecked(self.default_settings['wordlist']['numerals'])

        checkbox_ignore_case.setChecked(self.default_settings['wordlist']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['wordlist']['lemmatization'])

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
        plot_settings_changed()
        filter_settings_changed()

    tab_wordlist = QWidget(self)

    table_wordlist = Wordless_Table_Wordlist(self, [
                                                       self.tr('Rank'),
                                                       self.tr('Tokens'),
                                                       self.tr('Total'),
                                                       self.tr('Total (%)'),
                                                       self.tr('Cumulative Total'),
                                                       self.tr('Cumulative Total (%)'),
                                                       self.tr('Files Found'),
                                                       self.tr('Files Found (%)')
                                                   ])

    table_wordlist.button_generate_wordlist = QPushButton('Generate Wordlist', self)
    table_wordlist.button_generate_plot = QPushButton('Generate Plot', self)

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
    groupbox_token_settings = QGroupBox('Token Settings', self)

    checkbox_words = QCheckBox('Words', self)
    checkbox_lowercase = QCheckBox('Lowercase', self)
    checkbox_uppercase = QCheckBox('Uppercase', self)
    checkbox_title_cased = QCheckBox('Title Cased', self)
    checkbox_numerals = QCheckBox('Numerals', self)
    checkbox_punctuations = QCheckBox('Punctuations', self)

    checkbox_words.clicked.connect(lambda: token_settings_changed(checkbox_words))
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

    groupbox_token_settings.setLayout(layout_token_settings)

    # Search Settings
    groupbox_search_settings = QGroupBox('Search Settings', self)

    checkbox_ignore_case = QCheckBox('Ignore Case', self)
    checkbox_lemmatization = QCheckBox('Lemmatization', self)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(checkbox_ignore_case, 0, 0)
    layout_search_settings.addWidget(checkbox_lemmatization, 1, 0)

    groupbox_search_settings.setLayout(layout_search_settings)

    # Plot Settings
    groupbox_plot_settings = QGroupBox('Plot Settings', self)

    checkbox_cumulative = QCheckBox('Cumulative', self)

    checkbox_cumulative.stateChanged.connect(plot_settings_changed)

    layout_plot_settings = QGridLayout()
    layout_plot_settings.addWidget(checkbox_cumulative, 0, 0, Qt.AlignTop)

    groupbox_plot_settings.setLayout(layout_plot_settings)

    # Filter Settings
    groupbox_filter_settings = QGroupBox('Filter Settings', self)

    label_freq_first = QLabel('Frequency (First File):', self)
    checkbox_freq_first = QCheckBox('No Limit', self)
    label_freq_first_min = QLabel('From', self)
    spin_box_freq_first_min = QSpinBox(self)
    label_freq_first_max = QLabel('To', self)
    spin_box_freq_first_max = QSpinBox(self)

    label_freq_total = QLabel('Frequency (Total):', self)
    checkbox_freq_total = QCheckBox('No Limit', self)
    label_freq_total_min = QLabel('From', self)
    spin_box_freq_total_min = QSpinBox(self)
    label_freq_total_max = QLabel('To', self)
    spin_box_freq_total_max = QSpinBox(self)

    label_rank = QLabel('Rank:', self)
    checkbox_rank = QCheckBox('No Limit', self)
    label_rank_min = QLabel('From', self)
    spin_box_rank_min = QSpinBox(self)
    label_rank_max = QLabel('To', self)
    spin_box_rank_max = QSpinBox(self)

    label_len = QLabel('Token Length:', self)
    checkbox_len = QCheckBox('No Limit', self)
    label_len_min = QLabel('From', self)
    spin_box_len_min = QSpinBox(self)
    label_len_max = QLabel('To', self)
    spin_box_len_max = QSpinBox(self)

    label_files = QLabel('Files Found:', self)
    checkbox_files = QCheckBox('No Limit', self)
    label_files_min = QLabel('From', self)
    spin_box_files_min = QSpinBox(self)
    label_files_max = QLabel('To', self)
    spin_box_files_max = QSpinBox(self)

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

    groupbox_filter_settings.setLayout(layout_filter_settings)

    # Scroll Area Wrapper
    wrapper_settings = QWidget(self)

    layout_settings = QGridLayout()
    layout_settings.addWidget(groupbox_token_settings, 0, 0, Qt.AlignTop)
    layout_settings.addWidget(groupbox_search_settings, 1, 0, Qt.AlignTop)
    layout_settings.addWidget(groupbox_plot_settings, 2, 0, Qt.AlignTop)
    layout_settings.addWidget(groupbox_filter_settings, 3, 0, Qt.AlignTop)

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
    freq_total = 0

    table.clear_table()
    table.setRowCount(0)

    files = wordless_utils.fetch_files(self)

    for i, file in enumerate(files):
        table.insert_column(table.find_column('Total'), file.name)

    table.setSortingEnabled(False)

    column_total = table.find_column('Total')
    column_total_percentage = table.find_column('Total (%)')
    column_cumulative_total = table.find_column('Cumulative Total')
    column_cumulative_total_percentage = table.find_column('Cumulative Total (%)')
    column_files_found = table.find_column('Files Found')
    column_files_found_percentage = table.find_column('Files Found (%)')

    freq_distributions = wordless_freq.wordless_freq_distributions(self, files, mode = 'wordlist')

    for i, (token, freqs) in enumerate(freq_distributions.items()):
        table.setRowCount(table.rowCount() + 1)

        # Rank
        table.setItem(i, 0, QTableWidgetItem())
        if freqs[0] == freq_previous:
            table.item(i, 0).setData(Qt.DisplayRole, table.item(i - 1, 0).data(Qt.DisplayRole))
        else:
            table.item(i, 0).setData(Qt.DisplayRole, i + 1)

        # Token
        table.setItem(i, 1, QTableWidgetItem(token))
        # Frequency
        for j, freq in enumerate(freqs):
            table.setItem(i, j + 2, QTableWidgetItem())
            table.item(i, j + 2).setData(Qt.DisplayRole, freq)

        # Total
        table.setItem(i, column_total, QTableWidgetItem())
        table.item(i, column_total).setData(Qt.DisplayRole, sum(freqs))

        # Files Found
        table.setItem(i, column_files_found, QTableWidgetItem())
        table.item(i, column_files_found).setData(Qt.DisplayRole, len([freq for freq in freqs if freq]))
        # Files Found (%)
        table.setItem(i, column_files_found_percentage, QTableWidgetItem())
        table.item(i, column_files_found_percentage).setData(Qt.DisplayRole,
                                                             round(table.item(i, column_files_found).data(Qt.DisplayRole) /
                                                                   len(files) * 100,
                                                                   self.settings['general']['precision']))

        freq_previous = freqs[0]
        freq_total += sum(freqs)

    for i in range(table.rowCount()):
        # Total (%)
        table.setItem(i, column_total_percentage, QTableWidgetItem())
        table.item(i, column_total_percentage).setData(Qt.DisplayRole,
                                                       round(table.item(i, column_total).data(Qt.DisplayRole) /
                                                             freq_total * 100,
                                                             self.settings['general']['precision']))

        # Cumulative Total & Cumulative Total (%)
        table.setItem(i, column_cumulative_total, QTableWidgetItem())
        table.setItem(i, column_cumulative_total_percentage, QTableWidgetItem())

        if i == 0:
            table.item(i, column_cumulative_total).setData(Qt.DisplayRole,
                                                           table.item(i, column_total).data(Qt.DisplayRole))
            table.item(i, column_cumulative_total_percentage).setData(Qt.DisplayRole,
                                                                      table.item(i, column_total_percentage).data(Qt.DisplayRole))
        else:
            table.item(i, column_cumulative_total).setData(Qt.DisplayRole,
                                                           round(table.item(i - 1,column_cumulative_total).data(Qt.DisplayRole) +
                                                                 table.item(i, column_total).data(Qt.DisplayRole),
                                                                 self.settings['general']['precision']))
            table.item(i, column_cumulative_total_percentage).setData(Qt.DisplayRole,
                                                                      round(table.item(i, column_cumulative_total).data(Qt.DisplayRole) / freq_total * 100,
                                                                            self.settings['general']['precision']))

    if table.rowCount() > 0:
        table.sortByColumn(table.find_column('Tokens') + 1, Qt.DescendingOrder)
    else:
        table.clear_table()

        QMessageBox.information(self,
                                self.tr('No Search Results'),
                                self.tr('There are no results for your search!<br>You might want to change your settings and try it again.'),
                                QMessageBox.Ok)

    table.setSortingEnabled(True)
        
    self.status_bar.showMessage('Done!')

def generate_plot(self):
    freq_distributions = wordless_freq.wordless_freq_distributions(self, files, mode = 'wordlist')

    if self.settings['wordlist']['rank_max'] < float('inf'):
        freq_distributions.plot(self.settings['wordlist']['rank_max'], cumulative = self.settings['wordlist']['cumulative'])
    else:
        freq_distributions.plot(cumulative = self.settings['wordlist']['cumulative'])

    self.status_bar.showMessage('Done!')
