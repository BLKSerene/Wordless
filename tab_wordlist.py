#
# Wordless: Wordlist
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Wordlist(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Tokens'),
                             main.tr('Total\nFrequency'),
                             main.tr('Files Found')
                         ],
                         headers_num = [
                             main.tr('Rank'),
                             main.tr('Total\nFrequency'),
                             main.tr('Files Found')
                         ],
                         headers_pct = [
                             main.tr('Total\nFrequency'),
                             main.tr('Files Found')
                         ],
                         headers_cumulative = [
                             main.tr('Total\nFrequency')
                         ],
                         sorting_enabled = True)

        dialog_search = wordless_dialog.Wordless_Dialog_Search(self.main,
                                                               tab = 'wordlist',
                                                               table = self,
                                                               cols_search = self.tr('Tokens'))

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self.main)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self.main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['wordlist']

            if settings['apply_to'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total\nFrequency'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["apply_to"]}]\nFrequency'))

            col_tokens = self.find_col(self.tr('Tokens'))
            col_files_found = self.find_col(self.tr('Files Found'))

            freq_min = settings['freq_min']
            freq_max = settings['freq_max'] if not settings['freq_no_limit'] else float('inf')

            len_min = settings['len_min']
            len_max = settings['len_max'] if not settings['len_no_limit'] else float('inf')

            files_min = settings['files_min']
            files_max = settings['files_max'] if not settings['files_no_limit'] else float('inf')

            self.row_filters = [[] for i in range(self.rowCount())]

            for i in range(self.rowCount()):
                if freq_min <= self.item(i, col_freq).val_raw <= freq_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if len_min <= len(self.item(i, col_tokens).text().replace(' ', '')) <= len_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if files_min <= self.item(i, col_files_found).val <= files_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

            self.filter_table()

        wordless_message.wordless_message_filter_table_done(self.main)

def init(main):
    def load_settings(default = False):
        if default:
            settings = copy.deepcopy(main.settings_default['wordlist'])
        else:
            settings = copy.deepcopy(main.settings_custom['wordlist'])

        # Token Settings
        checkbox_words.setChecked(settings['token_settings']['words'])
        checkbox_lowercase.setChecked(settings['token_settings']['lowercase'])
        checkbox_uppercase.setChecked(settings['token_settings']['uppercase'])
        checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings['token_settings']['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings['token_settings']['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        checkbox_nums.setChecked(settings['token_settings']['nums'])
        checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        # Table Settings
        checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        # Plot Settings
        combo_box_plot_type.setCurrentText(settings['plot_settings']['plot_type'])
        combo_box_use_data_file.setCurrentText(settings['plot_settings']['use_data_file'])
        checkbox_use_pct.setChecked(settings['plot_settings']['use_pct'])
        checkbox_use_cumulative.setChecked(settings['plot_settings']['use_cumulative'])

        checkbox_rank_no_limit.setChecked(settings['plot_settings']['rank_no_limit'])
        spin_box_rank_min.setValue(settings['plot_settings']['rank_min'])
        spin_box_rank_max.setValue(settings['plot_settings']['rank_max'])

        # Filter Settings
        combo_box_apply_to.setCurrentText(settings['filter_settings']['apply_to'])

        checkbox_freq_no_limit.setChecked(settings['filter_settings']['freq_no_limit'])
        spin_box_freq_min.setValue(settings['filter_settings']['freq_min'])
        spin_box_freq_max.setValue(settings['filter_settings']['freq_max'])

        checkbox_len_no_limit.setChecked(settings['filter_settings']['len_no_limit'])
        spin_box_len_min.setValue(settings['filter_settings']['len_min'])
        spin_box_len_max.setValue(settings['filter_settings']['len_max'])

        checkbox_files_no_limit.setChecked(settings['filter_settings']['files_no_limit'])
        spin_box_files_min.setValue(settings['filter_settings']['files_min'])
        spin_box_files_max.setValue(settings['filter_settings']['files_max'])

        token_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['wordlist']['token_settings']

        settings['words'] = checkbox_words.isChecked()
        settings['lowercase'] = checkbox_lowercase.isChecked()
        settings['uppercase'] = checkbox_uppercase.isChecked()
        settings['title_case'] = checkbox_title_case.isChecked()
        settings['treat_as_lowercase'] = checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize'] = checkbox_lemmatize.isChecked()
        settings['filter_stop_words'] = checkbox_filter_stop_words.isChecked()

        settings['nums'] = checkbox_nums.isChecked()
        settings['puncs'] = checkbox_puncs.isChecked()

    def table_settings_changed():
        settings = main.settings_custom['wordlist']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        settings = main.settings_custom['wordlist']['plot_settings']

        settings['plot_type'] = combo_box_plot_type.currentText()
        settings['use_data_file'] = combo_box_use_data_file.currentText()
        settings['use_pct'] = checkbox_use_pct.isChecked()
        settings['use_cumulative'] = checkbox_use_cumulative.isChecked()

        settings['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_max'] = spin_box_rank_max.value()

        if settings['plot_type'] == main.tr('Line Chart'):
            combo_box_use_data_file.setEnabled(False)

            checkbox_use_pct.setEnabled(True)
            checkbox_use_cumulative.setEnabled(True)
        elif settings['plot_type'] == main.tr('Word Cloud'):
            combo_box_use_data_file.setEnabled(True)

            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)

    def filter_settings_changed():
        settings = main.settings_custom['wordlist']['filter_settings']

        settings['apply_to'] = combo_box_apply_to.currentText()

        settings['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        settings['freq_min'] = spin_box_freq_min.value()
        settings['freq_max'] = spin_box_freq_max.value()

        settings['len_no_limit'] = checkbox_len_no_limit.isChecked()
        settings['len_min'] = spin_box_len_min.value()
        settings['len_max'] = spin_box_len_max.value()

        settings['files_no_limit'] = checkbox_files_no_limit.isChecked()
        settings['files_min'] = spin_box_files_min.value()
        settings['files_max'] = spin_box_files_max.value()

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
     checkbox_treat_as_lowercase,
     checkbox_lemmatize,
     checkbox_filter_stop_words,

     checkbox_nums,
     checkbox_puncs) = wordless_widgets.wordless_widgets_token(main)

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

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 5, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_nums, 6, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 6, 1)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table(main, table_wordlist)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown, 2, 0)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    label_plot_type = QLabel(main.tr('Plot Type:'), main)
    combo_box_plot_type = wordless_box.Wordless_Combo_Box(main)
    label_use_data_file = QLabel(main.tr('Use Data File:'), main)
    combo_box_use_data_file = wordless_box.Wordless_Combo_Box_Use_Data_File(main)
    checkbox_use_pct = QCheckBox(main.tr('Use Percentage Data'), main)
    checkbox_use_cumulative = QCheckBox(main.tr('Use Cumulative Data'), main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 10000)

    combo_box_plot_type.addItems([main.tr('Line Chart'),
                                  main.tr('Word Cloud')])

    combo_box_plot_type.currentTextChanged.connect(plot_settings_changed)
    combo_box_use_data_file.currentTextChanged.connect(plot_settings_changed)
    checkbox_use_pct.stateChanged.connect(plot_settings_changed)
    checkbox_use_cumulative.stateChanged.connect(plot_settings_changed)

    checkbox_rank_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)

    layout_plot_type = QGridLayout()
    layout_plot_type.addWidget(label_plot_type, 0, 0)
    layout_plot_type.addWidget(combo_box_plot_type, 0, 1)

    layout_plot_type.setColumnStretch(1, 1)

    layout_use_data_file = QGridLayout()
    layout_use_data_file.addWidget(label_use_data_file, 0, 0)
    layout_use_data_file.addWidget(combo_box_use_data_file, 0, 1)

    layout_use_data_file.setColumnStretch(1, 1)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addLayout(layout_plot_type, 0, 0, 1, 4)
    group_box_plot_settings.layout().addLayout(layout_use_data_file, 1, 0, 1, 4)
    group_box_plot_settings.layout().addWidget(checkbox_use_pct, 2, 0, 1, 4)
    group_box_plot_settings.layout().addWidget(checkbox_use_cumulative, 3, 0, 1, 4)

    group_box_plot_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 4, 0, 1, 4)

    group_box_plot_settings.layout().addWidget(label_rank, 5, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_rank_no_limit, 5, 3)
    group_box_plot_settings.layout().addWidget(label_rank_min, 6, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_min, 6, 1)
    group_box_plot_settings.layout().addWidget(label_rank_max, 6, 2)
    group_box_plot_settings.layout().addWidget(spin_box_rank_max, 6, 3)

    # Filter Settings
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_apply_to = QLabel(main.tr('Apply Filter to:'), main)
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_wordlist)

    label_freq = QLabel(main.tr('Frequency:'), main)
    (checkbox_freq_no_limit,
     label_freq_min,
     spin_box_freq_min,
     label_freq_max,
     spin_box_freq_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_len = QLabel(main.tr('Token Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100)

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    button_filter_results = QPushButton(main.tr('Filter Results in Table'), main)

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

    button_filter_results.clicked.connect(lambda: table_wordlist.update_filters())

    layout_apply_to = QGridLayout()
    layout_apply_to.addWidget(label_apply_to, 0, 0)
    layout_apply_to.addWidget(combo_box_apply_to, 0, 1)

    layout_apply_to.setColumnStretch(1, 1)

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addLayout(layout_apply_to, 0, 0, 1, 4)

    group_box_filter_settings.layout().addWidget(label_freq, 1, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_no_limit, 1, 3)
    group_box_filter_settings.layout().addWidget(label_freq_min, 2, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_min, 2, 1)
    group_box_filter_settings.layout().addWidget(label_freq_max, 2, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_max, 2, 3)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 4)

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

    tab_wordlist.layout_settings.addWidget(group_box_token_settings, 0, 0)
    tab_wordlist.layout_settings.addWidget(group_box_table_settings, 1, 0)
    tab_wordlist.layout_settings.addWidget(group_box_plot_settings, 2, 0)
    tab_wordlist.layout_settings.addWidget(group_box_filter_settings, 3, 0)

    tab_wordlist.layout_settings.setRowStretch(4, 1)

    load_settings()

    return tab_wordlist

def generate_wordlists(main, files):
    freqs_files = []

    settings = main.settings_custom['wordlist']

    for file in files:
        text = wordless_text.Wordless_Text(main, file)
        tokens = text.tokens.copy()

        if settings['token_settings']['words']:
            if settings['token_settings']['treat_as_lowercase']:
                tokens = [token.lower() for token in tokens]

            if settings['token_settings']['lemmatize']:
                tokens = wordless_text.wordless_lemmatize(text.main, tokens, text.lang_code)

        freqs_file = nltk.FreqDist(tokens)

        if settings['token_settings']['words']:
            if not settings['token_settings']['treat_as_lowercase']:
                if not settings['token_settings']['lowercase']:
                    freqs_file = {token: freq
                                  for token, freq in freqs_file.items()
                                  if not token.islower()}
                if not settings['token_settings']['uppercase']:
                    freqs_file = {token: freq
                                  for token, freq in freqs_file.items()
                                  if not token.isupper()}
                if not settings['token_settings']['title_case']:
                    freqs_file = {token: freq
                                  for token, freq in freqs_file.items()
                                  if not token.istitle()}

            if settings['token_settings']['filter_stop_words']:
                tokens_filtered = wordless_text.wordless_filter_stop_words(main, list(freqs_file.keys()), text.lang_code)

                freqs_file = {token: freqs_file[token] for token in tokens_filtered}
        else:
            freqs_file = {token: freq
                          for token, freq in freqs_file.items()
                          if not [char for char in token if char.isalpha()]}
        
        if not settings['token_settings']['nums']:
            freqs_file = {token: freq
                          for token, freq in freqs_file.items()
                          if not token.isnumeric()}
        if not settings['token_settings']['puncs']:
            freqs_file = {token: freq
                          for token, freq in freqs_file.items()
                          if [char for char in token if char.isalnum()]}

        freqs_files.append(freqs_file)

    return wordless_misc.merge_dicts(freqs_files)

@ wordless_misc.log_timing
def generate_table(main, table):
    files = main.wordless_files.get_selected_files()

    if files:
        table.settings = main.settings_custom

        table.clear_table()

        freqs_files = generate_wordlists(main, files)

        for i, file in enumerate(files):
            table.insert_col(table.columnCount() - 2,
                             main.tr(f'[{file["name"]}]\nFrequency'),
                             num = True, pct = True, cumulative = True, breakdown = True)

        table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\nFrequency')), Qt.DescendingOrder)

        col_total_freq = table.find_col(main.tr('Total\nFrequency'))
        col_files_found = table.find_col(main.tr('Files Found'))

        len_files = len(files)

        table.blockSignals(True)
        table.setSortingEnabled(False)
        table.setUpdatesEnabled(False)

        table.setRowCount(len(freqs_files))

        for i, (token, freqs) in enumerate(wordless_sorting.sorted_freqs_files(freqs_files)):
            # Rank
            table.set_item_num_int(i, 0, -1)

            # Tokens
            table.setItem(i, 1, wordless_table.Wordless_Table_Item(token))

            # Frequency
            for j, freq in enumerate(freqs):
                table.set_item_num_cumulative(i, 2 + j, freq)

            # Total
            table.set_item_num_cumulative(i, col_total_freq, sum(freqs))

            # Files Found
            table.set_item_num_pct(i, col_files_found, len([freq for freq in freqs if freq]), len_files)

        table.blockSignals(False)
        table.setSortingEnabled(True)
        table.setUpdatesEnabled(True)

        table.toggle_pct()
        table.toggle_cumulative()
        table.toggle_breakdown()
        table.update_ranks()

        table.update_items_width()

        table.item_changed()

        wordless_message.wordless_message_generate_table_success(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['wordlist']

    files = main.wordless_files.get_selected_files()

    if files:
        freqs_files = generate_wordlists(main, files)

        wordless_plot.wordless_plot_freq(main, freqs_files,
                                         plot_type = settings['plot_settings']['plot_type'],
                                         use_data_file = settings['plot_settings']['use_data_file'],
                                         use_pct = settings['plot_settings']['use_pct'],
                                         use_cumulative = settings['plot_settings']['use_cumulative'],
                                         rank_min = settings['plot_settings']['rank_min'],
                                         rank_max = settings['plot_settings']['rank_max'],
                                         label_x = main.tr('Tokens'))

        wordless_message.wordless_message_generate_plot_success(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_plot_error(main)
