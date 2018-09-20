#
# Wordless: Wordlist
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

from wordless_utils import *

class Wordless_Table_Wordlist(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Tokens'),
                             main.tr('Total'),
                             main.tr('Total (Cumulative)'),
                             main.tr('Files Found'),
                         ])

    def update_filters(self):
        settings = self.main.settings['wordlist']

        col_freq = self.find_column(settings['freq_apply_to'])
        col_tokens = self.find_column('Tokens')
        col_files_found = self.find_column('Files Found')

        freq_min = settings['freq_min']
        freq_max = settings['freq_max'] if not settings['freq_no_limit'] else float('inf')
        len_min = settings['len_min']
        len_max = settings['len_max'] if not settings['len_no_limit'] else float('inf')
        files_min = settings['files_min']
        files_max = settings['files_max'] if not settings['files_no_limit'] else float('inf')

        self.row_filters = [{} for i in range(self.rowCount())]

        for i in range(self.rowCount()):
            if freq_min <= self.item(i, col_freq).read_data() <= freq_max:
                self.row_filters[i]['Total'] = True
            else:
                self.row_filters[i]['Total'] = False

            if len_min <= len(str(self.item(i, col_tokens).read_data()).replace(' ', '')) <= len_max:
                self.row_filters[i]['Tokens'] = True
            else:
                self.row_filters[i]['Tokens'] = False

            if files_min <= self.item(i, col_files_found).read_data() <= files_max:
                self.row_filters[i]['Files Found'] = True
            else:
                self.row_filters[i]['Files Found'] = False

        self.filter_table()

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.default_settings['wordlist'])
        else:
            settings = copy.deepcopy(main.settings['wordlist'])

        checkbox_words.setChecked(settings['words'])
        checkbox_lowercase.setChecked(settings['lowercase'])
        checkbox_uppercase.setChecked(settings['uppercase'])
        checkbox_title_cased.setChecked(settings['title_cased'])
        checkbox_punctuations.setChecked(settings['punctuations'])
        checkbox_numerals.setChecked(settings['numerals'])

        line_edit_search_term.setText(settings['search_term'])
        list_search_terms.clear()
        for search_term in settings['search_terms']:
            list_search_terms.add_item(search_term)

        checkbox_ignore_case.setChecked(settings['ignore_case'])
        checkbox_lemmatization.setChecked(settings['lemmatization'])
        checkbox_whole_word.setChecked(settings['whole_word'])
        checkbox_regex.setChecked(settings['regex'])
        checkbox_multi_search.setChecked(settings['multi_search'])

        checkbox_generation_ignore_case.setChecked(settings['generation_ignore_case'])
        checkbox_generation_lemmatization.setChecked(settings['generation_lemmatization'])

        checkbox_show_pct.setChecked(settings['show_pct'])
        checkbox_show_cumulative.setChecked(settings['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings['show_breakdown'])

        checkbox_rank_no_limit.setChecked(settings['rank_no_limit'])
        spin_box_rank_min.setValue(settings['rank_min'])
        spin_box_rank_max.setValue(settings['rank_max'])
        checkbox_cumulative.setChecked(settings['cumulative'])

        checkbox_freq_no_limit.setChecked(settings['freq_no_limit'])
        spin_box_freq_min.setValue(settings['freq_min'])
        spin_box_freq_max.setValue(settings['freq_max'])
        combo_box_freq_apply_to.setCurrentText(settings['freq_apply_to'])

        checkbox_len_no_limit.setChecked(settings['len_no_limit'])
        spin_box_len_min.setValue(settings['len_min'])
        spin_box_len_max.setValue(settings['len_max'])

        checkbox_files_no_limit.setChecked(settings['files_no_limit'])
        spin_box_files_min.setValue(settings['files_min'])
        spin_box_files_max.setValue(settings['files_max'])

        token_settings_changed()
        search_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        main.settings['wordlist']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        main.settings['wordlist']['lowercase'] = checkbox_lowercase.isChecked()
        main.settings['wordlist']['uppercase'] = checkbox_uppercase.isChecked()
        main.settings['wordlist']['title_cased'] = checkbox_title_cased.isChecked()
        main.settings['wordlist']['numerals'] = checkbox_numerals.isChecked()
        main.settings['wordlist']['punctuations'] = checkbox_punctuations.isChecked()

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
        main.settings['wordlist']['search_term'] = line_edit_search_term.text()
        main.settings['wordlist']['search_terms'] = list_search_terms.get_items()
        main.settings['wordlist']['ignore_case'] = checkbox_ignore_case.isChecked()
        main.settings['wordlist']['lemmatization'] = checkbox_lemmatization.isChecked()
        main.settings['wordlist']['whole_word'] = checkbox_whole_word.isChecked()
        main.settings['wordlist']['regex'] = checkbox_regex.isChecked()
        main.settings['wordlist']['multi_search'] = checkbox_multi_search.isChecked()

    def generation_settings_changed():
        main.settings['wordlist']['generation_ignore_case'] = checkbox_generation_ignore_case.isChecked()
        main.settings['wordlist']['checkbox_generation_lemmatization'] = checkbox_generation_lemmatization.isChecked()

        if main.settings['wordlist']['generation_ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

    def table_settings_changed():
        main.settings['wordlist']['show_pct'] = checkbox_show_pct.isChecked()
        main.settings['wordlist']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        main.settings['wordlist']['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        main.settings['wordlist']['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        main.settings['wordlist']['rank_min'] = spin_box_rank_min.value()
        main.settings['wordlist']['rank_max'] = spin_box_rank_max.value()

        main.settings['wordlist']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        main.settings['wordlist']['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        main.settings['wordlist']['freq_min'] = spin_box_freq_min.value()
        main.settings['wordlist']['freq_max'] = spin_box_freq_max.value()
        main.settings['wordlist']['freq_apply_to'] = combo_box_freq_apply_to.currentText()

        main.settings['wordlist']['len_no_limit'] = checkbox_len_no_limit.isChecked()
        main.settings['wordlist']['len_min'] = spin_box_len_min.value()
        main.settings['wordlist']['len_max'] = spin_box_len_max.value()

        main.settings['wordlist']['files_no_limit'] = checkbox_files_no_limit.isChecked()
        main.settings['wordlist']['files_min'] = spin_box_files_min.value()
        main.settings['wordlist']['files_max'] = spin_box_files_max.value()

    def restore_defaults():
        reply = QMessageBox.question(main,
                                     main.tr('Restore Defaults'),
                                     main.tr('Do you really want to reset all settings to defaults?'),
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            load_settings(defaults = True)

    tab_wordlist = wordless_tab.Wordless_Tab(main, main.tr('Wordlist'))

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
     checkbox_title_cased,
     checkbox_numerals,
     checkbox_punctuations) = wordless_widgets.wordless_widgets_token_settings(main)

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
    group_box_search_settings = QGroupBox(main.tr('Search Settings'), main)

    (label_search_term,
     line_edit_search_term,
     list_search_terms,
     checkbox_ignore_case,
     checkbox_lemmatization,
     checkbox_whole_word,
     checkbox_regex,
     checkbox_multi_search,
     checkbox_show_all) = wordless_widgets.wordless_widgets_search_settings(main)

    button_find_next = QPushButton(main.tr('Find Next'), main)
    button_find_prev = QPushButton(main.tr('Find Previous'), main)
    button_find_all = QPushButton(main.tr('Find All'), main)
    button_clear_highlights = QPushButton(main.tr('Clear Highlights'), main)

    checkbox_show_all.hide()

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(button_find_next.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)
    checkbox_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search.stateChanged.connect(search_settings_changed)

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

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_search_term, 0, 0, 1, 2)
    layout_search_settings.addWidget(line_edit_search_term, 1, 0, 1, 2)
    layout_search_settings.addLayout(layout_search_terms, 2, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_ignore_case, 5, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_lemmatization, 6, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_whole_word, 7, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_regex, 8, 0, 1, 2)
    layout_search_settings.addWidget(checkbox_multi_search, 9, 0, 1, 2)

    layout_search_settings.addWidget(button_find_next, 3, 0)
    layout_search_settings.addWidget(button_find_prev, 3, 1)
    layout_search_settings.addWidget(button_find_all, 4, 0)
    layout_search_settings.addWidget(button_clear_highlights, 4, 1)

    group_box_search_settings.setLayout(layout_search_settings)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    checkbox_generation_ignore_case = QCheckBox(main.tr('Ignore Case'), main)
    checkbox_generation_lemmatization = QCheckBox(main.tr('Lemmatization'), main)

    checkbox_generation_ignore_case.stateChanged.connect(generation_settings_changed)
    checkbox_generation_lemmatization.stateChanged.connect(generation_settings_changed)

    layout_generation_settings = QGridLayout()
    layout_generation_settings.addWidget(checkbox_generation_ignore_case, 0, 0)
    layout_generation_settings.addWidget(checkbox_generation_lemmatization, 1, 0)

    group_box_generation_settings.setLayout(layout_generation_settings)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_wordlist)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    layout_table_settings = QGridLayout()
    layout_table_settings.addWidget(checkbox_show_pct, 0, 0)
    layout_table_settings.addWidget(checkbox_show_cumulative, 1, 0)
    layout_table_settings.addWidget(checkbox_show_breakdown, 2, 0)

    group_box_table_settings.setLayout(layout_table_settings)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, 1, 10000)
    checkbox_cumulative = QCheckBox(main.tr('Cumulative'), main)

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
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_freq = QLabel(main.tr('Frequency:'), main)
    (checkbox_freq_no_limit,
     label_freq_min,
     spin_box_freq_min,
     label_freq_max,
     spin_box_freq_max,
     label_freq_apply_to,
     combo_box_freq_apply_to) = wordless_widgets.wordless_widgets_filter(main,
                                                                         filter_min = 0,
                                                                         filter_max = 10000,
                                                                         table = table_wordlist,
                                                                         column = 'Total')

    label_len = QLabel(main.tr('Token Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main, table = table_wordlist, column = 'Tokens')

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_wordlist,
                                                                    column = 'Files Found')

    checkbox_freq_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_min.editingFinished.connect(filter_settings_changed)
    spin_box_freq_max.editingFinished.connect(filter_settings_changed)
    combo_box_freq_apply_to.currentTextChanged.connect(filter_settings_changed)

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
    layout_filter_settings.addWidget(combo_box_freq_apply_to, 2, 1, 1, 3)

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
    tab_wordlist.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_wordlist.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    tab_wordlist.button_restore_defaults.clicked.connect(restore_defaults)

    load_settings()

    return tab_wordlist

def generate_freq_distributions(main, files):
    freq_distributions = []

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(main, file)
        
        freq_distributions.append(text.wordlist(main.settings['wordlist']))

    return wordless_distribution.Wordless_Freq_Distribution(wordless_misc.merge_dicts(freq_distributions))

@wordless_misc.check_results_table
def generate_data(main, table):
    table.clear_table()

    files = main.wordless_files.selected_files()

    table.files = files

    for i, file in enumerate(files):
        table.insert_column(table.find_column(main.tr('Total')), file['name'])
        table.insert_column(table.find_column(main.tr('Total')), file['name'] + main.tr(' (Cumulative)'))

    table.sortByColumn(table.find_column('Tokens') + 1, Qt.DescendingOrder)

    freq_distributions = generate_freq_distributions(main, files)

    col_total = table.find_column(main.tr('Total'))
    col_files_found = table.find_column(main.tr('Files Found'))

    freqs_files = [freqs for freqs in zip(*freq_distributions.values())]
    total_files = [sum(freqs) for freqs in freqs_files]
    freqs_total = sum([sum(freqs) for freqs in freqs_files])
    len_files = len(files)

    table.blockSignals(True)
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

    table.blockSignals(False)
    table.setSortingEnabled(True)
    table.setUpdatesEnabled(True)

    table.update_filters()
    
    main.status_bar.showMessage(main.tr('Done!'))

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

        # Scroll to top if no previous items exist
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

    if table.item(0, 0):
        if main.settings['wordlist']['multi_search']:
            search_terms = main.settings['wordlist']['search_terms']
        else:
            if main.settings['wordlist']['search_term']:
                search_terms = [main.settings['wordlist']['search_term']]
            else:
                search_terms = []

        search_terms = wordless_text.Wordless_Text(main, table.files).match_tokens(search_terms,
                                                                                   main.settings['wordlist']['ignore_case'],
                                                                                   main.settings['wordlist']['lemmatization'],
                                                                                   main.settings['wordlist']['whole_word'],
                                                                                   main.settings['wordlist']['regex'])

        for i in range(table.rowCount()):
            item = table.item(i, 1)

            if item.text() in search_terms:
                items_found.append(item)

        clear_highlights(main, table)

        table.hide()
        table.blockSignals(True)

        for item in items_found:
            item.setForeground(QBrush(QColor('#FFF')))
            item.setBackground(QBrush(QColor('#F00')))

        table.blockSignals(False)
        table.show()

        if not items_found:
            QMessageBox.information(main,
                                    main.tr('Empty Results'),
                                    main.tr('There is nothing that could be found in the table.'))
    else:
        QMessageBox.information(main,
                                main.tr('Search Failed'),
                                main.tr('Please generate wordlist(s) first!'))

    main.status_bar.showMessage(main.tr('Found {:,} items.'.format(len(items_found))))

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

def generate_plot(main):
    files = main.wordless_files.selected_files()

    freq_distributions = generate_freq_distributions(main, files)

    freq_distributions.plot(files = files,
                            start = main.settings['wordlist']['rank_min'] - 1,
                            end = main.settings['wordlist']['rank_max'],
                            cumulative = main.settings['wordlist']['cumulative'])

    main.status_bar.showMessage(main.tr('Done!'))
