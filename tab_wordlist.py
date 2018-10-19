#
# Wordless: Wordlist
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Wordlist(wordless_table.Wordless_Table_Data):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Tokens'),
                             main.tr('Total Freq'),
                             main.tr('Files Found')
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
            settings = self.main.settings_custom['wordlist']

            if settings['apply_to'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total Freq'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["apply_to"]}] Freq'))

            col_tokens = self.find_col(self.tr('Tokens'))
            col_files_found = self.find_col(self.tr('Files Found'))

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

                if len_min <= len(self.item(i, col_tokens).text().replace(' ', '')) <= len_max:
                    self.row_filters[i][self.tr('Tokens')] = True
                else:
                    self.row_filters[i][self.tr('Tokens')] = False

                if files_min <= self.item(i, col_files_found).val_raw <= files_max:
                    self.row_filters[i][self.tr('Files Found')] = True
                else:
                    self.row_filters[i][self.tr('Files Found')] = False

            self.filter_table()

def init(main):
    def load_settings(default = False):
        if default:
            settings_loaded = copy.deepcopy(main.settings_default['wordlist'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['wordlist'])

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

        checkbox_ignore_case.setChecked(settings_loaded['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings_loaded['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings_loaded['match_whole_word'])
        checkbox_use_regex.setChecked(settings_loaded['use_regex'])
        checkbox_multi_search_mode.setChecked(settings_loaded['multi_search_mode'])

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

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()
        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()

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

    settings = main.settings_custom['wordlist']

    tab_wordlist = wordless_layout.Wordless_Tab(main, load_settings)

    table_wordlist = Wordless_Table_Wordlist(main)

    table_wordlist.button_generate_data = QPushButton(main.tr('Generate Wordlist'), main)
    table_wordlist.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

    table_wordlist.button_generate_data.clicked.connect(lambda: generate_data(main, table_wordlist))
    table_wordlist.button_generate_plot.clicked.connect(lambda: generate_plot(main))

    tab_wordlist.layout_table.addWidget(table_wordlist, 0, 0, 1, 5)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_generate_data, 1, 0)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_generate_plot, 1, 1)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_export_selected, 1, 2)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_export_all, 1, 3)
    tab_wordlist.layout_table.addWidget(table_wordlist.button_clear, 1, 4)

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

    checkbox_show_all.hide()

    button_find_next = QPushButton(main.tr('Find Next'), main)
    button_find_prev = QPushButton(main.tr('Find Previous'), main)
    button_find_all = QPushButton(main.tr('Find All'), main)
    button_clear_highlights = QPushButton(main.tr('Clear Highlights'), main)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(button_find_next.click)
    list_search_terms.itemChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)

    button_find_next.clicked.connect(lambda: find_next(main, table_wordlist))
    button_find_prev.clicked.connect(lambda: find_prev(main, table_wordlist))
    button_find_all.clicked.connect(lambda: find_all(main, table_wordlist))
    button_clear_highlights.clicked.connect(lambda: clear_highlights(main, table_wordlist))

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addWidget(label_search_term, 0, 0, 1, 2)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 2)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 2)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 3, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 4, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 5, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 6, 0, 1, 2)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 7, 0, 1, 2)

    group_box_search_settings.layout().addWidget(button_find_next, 8, 0)
    group_box_search_settings.layout().addWidget(button_find_prev, 8, 1)
    group_box_search_settings.layout().addWidget(button_find_all, 9, 0)
    group_box_search_settings.layout().addWidget(button_clear_highlights, 9, 1)

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

    checkbox_use_pct = QCheckBox(main.tr('Use Percentage Data'), main)
    checkbox_use_cumulative = QCheckBox(main.tr('Use Cumulative Data'), main)

    separator_plot_settings = wordless_layout.Wordless_Separator(main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, 1, 10000)

    separator_plot_settings = wordless_layout.Wordless_Separator(main)

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
                                                                   table = table_wordlist,
                                                                   col = main.tr('Freq'))

    label_apply_to = QLabel(main.tr('Apply to:'), main)
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_wordlist)
    separator_filter_settings = wordless_layout.Wordless_Separator(main)

    label_len = QLabel(main.tr('Token Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                  table = table_wordlist,
                                                                  col = main.tr('Tokens'))

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_wordlist,
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

    button_filter_results.clicked.connect(lambda: table_wordlist.update_filters())

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

    tab_wordlist.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_table_settings, 2, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_plot_settings, 3, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_filter_settings, 4, 0, Qt.AlignTop)

    load_settings()

    return tab_wordlist

def generate_wordlists(main, files):
    freq_distributions = []

    settings = main.settings_custom['wordlist']

    for file in files:
        text = wordless_text.Wordless_Text(main, file)
        tokens = text.tokens.copy()

        if settings['words']:
            if settings['treat_as_lowercase']:
                tokens = [token.lower() for token in tokens]

            if settings['lemmatize']:
                tokens = wordless_text.wordless_lemmatize(text.main, tokens, text.lang)

        freq_distribution = nltk.FreqDist(tokens)

        if settings['words']:
            if not settings['treat_as_lowercase']:
                if not settings['lowercase']:
                    freq_distribution = {token: freq
                                         for token, freq in freq_distribution.items()
                                         if not token.islower()}
                if not settings['uppercase']:
                    freq_distribution = {token: freq
                                         for token, freq in freq_distribution.items()
                                         if not token.isupper()}
                if not settings['title_case']:
                    freq_distribution = {token: freq
                                         for token, freq in freq_distribution.items()
                                         if not token.istitle()}

            if settings['filter_stop_words']:
                tokens_filtered = wordless_text.wordless_filter_stop_words(main, list(freq_distribution.keys()), text.lang)

                freq_distribution = {token: freq_distribution[token] for token in tokens_filtered}
        else:
            freq_distribution = {token: freq
                                 for token, freq in freq_distribution.items()
                                 if all([not char.isalpha() for char in token])}
        
        if not settings['nums']:
            freq_distribution = {token: freq
                                 for token, freq in freq_distribution.items()
                                 if not token.isnumeric()}
        if not settings['puncs']:
            freq_distribution = {token: freq
                                 for token, freq in freq_distribution.items()
                                 if any([char.isalnum() for char in token])}

        freq_distributions.append(freq_distribution)

    return wordless_misc.merge_dicts(freq_distributions)

@ wordless_misc.log_timing('Data generation completed')
def generate_data(main, table):
    files = main.wordless_files.selected_files()

    if files:
        freq_distribution = generate_wordlists(main, files)

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

            for i, (token, freqs) in enumerate(sorted(freq_distribution.items(), key = wordless_misc.multi_sorting)):
                # Rank
                table.setItem(i, 0, wordless_table.Wordless_Table_Item())

                # Tokens
                table.setItem(i, 1, wordless_table.Wordless_Table_Item(token))

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
        
def find_next(main, table):
    items_found = find_all(main, table)

    table.hide()
    table.blockSignals(True)

    # Scroll to the next found item
    if items_found:
        selected_rows = table.selected_rows()

        table.clearSelection()

        if selected_rows:
            for item in items_found:
                if item.row() > selected_rows[-1]:
                    table.selectRow(item.row())
                    table.setFocus()

                    table.scrollToItem(item)

                    break
        else:
            table.scrollToItem(items_found[0])
            table.selectRow(items_found[0].row())

        # Scroll to top if no next items exist
        if not table.selectedItems():
            table.scrollToItem(items_found[0])
            table.selectRow(items_found[0].row())

    table.blockSignals(False)
    table.show()

def find_prev(main, table):
    items_found = find_all(main, table)

    table.hide()
    table.blockSignals(True)

    # Scroll to the previous found item
    if items_found:
        selected_rows = table.selected_rows()

        table.clearSelection()

        if selected_rows:
            for item in reversed(items_found):
                if item.row() < selected_rows[0]:
                    table.selectRow(item.row())
                    table.setFocus()

                    table.scrollToItem(item)

                    break
        else:
            table.scrollToItem(items_found[-1])
            table.selectRow(items_found[-1].row())

        # Scroll to top if no next items exist
        if not table.selectedItems():
            table.scrollToItem(items_found[-1])
            table.selectRow(items_found[-1].row())

    table.blockSignals(False)
    table.show()

def find_all(main, table):
    items_found = []

    settings = main.settings_custom['wordlist']

    if table.item(0, 0):
        if (settings['multi_search_mode'] and settings['search_terms'] or
            not settings['multi_search_mode'] and settings['search_term']):
            if settings['multi_search_mode']:
                search_terms = settings['search_terms']
            else:
                if settings['search_term']:
                    search_terms = [settings['search_term']]
                else:
                    search_terms = []

            col_tokens = table.find_col(main.tr('Tokens'))

            for file in table.files:
                search_terms = wordless_text.Wordless_Text(main, file).match_tokens(search_terms,
                                                                                    settings['ignore_case'],
                                                                                    settings['match_inflected_forms'],
                                                                                    settings['match_whole_word'],
                                                                                    settings['use_regex'])

            for i in range(table.rowCount()):
                item = table.item(i, 1)

                if item.text() in search_terms:
                    items_found.append(item)

            if items_found:
                clear_highlights(main, table)

                table.hide()
                table.blockSignals(True)

                for item in items_found:
                    item.setForeground(QBrush(QColor('#FFF')))
                    item.setBackground(QBrush(QColor('#F00')))

                table.blockSignals(False)
                table.show()
            else:
                wordless_dialog.wordless_message_empty_results_table(main)

            main.status_bar.showMessage(main.tr(f'Found {len(items_found):,} item(s).'))
        else:
            wordless_dialog.wordless_message_empty_search_term(main)
    else:
        QMessageBox.information(main,
                                main.tr('Search Failed'),
                                main.tr('Please generate wordlist(s) first!'))

    return items_found

def clear_highlights(main, table):
    table.hide()
    table.blockSignals(True)

    if table.item(0, 0):
        for i in range(table.rowCount()):
            table.item(i, 1).setForeground(QBrush(QColor('#292929')))
            table.item(i, 1).setBackground(QBrush(QColor('#FFF')))

    table.blockSignals(False)
    table.show()

@ wordless_misc.log_timing('Generation completed')
def generate_plot(main):
    settings = main.settings_custom['wordlist']

    files = main.wordless_files.selected_files()

    if files:
        freq_distribution = generate_wordlists(main, files)

        if freq_distribution:
            wordless_plot.wordless_plot_freq(main, freq_distribution,
                                             rank_min = settings['rank_min'],
                                             rank_max = settings['rank_max'],
                                             use_pct = settings['use_pct'],
                                             use_cumulative = settings['use_cumulative'],
                                             label_x = main.tr('Tokens'))
        else:
            wordless_dialog.wordless_message_empty_results_plot(main)
