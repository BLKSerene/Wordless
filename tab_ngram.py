#
# Wordless: N-gram
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Ngram(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('N-grams'),
                             main.tr('Total'),
                             main.tr('Total (Cumulative)'),
                             main.tr('Files Found'),
                         ],
                         cols_with_pct = [
                             main.tr('Total'),
                             main.tr('Total (Cumulative)'),
                             main.tr('Files Found')
                         ],
                         sorting_enabled = True)

    def update_filters(self):
        settings = self.main.settings_custom['ngram']

        col_freq = self.find_column(settings['freq_apply_to'])
        col_ngrams = self.find_column('N-grams')
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
                self.row_filters[i][self.tr('Total')] = True
            else:
                self.row_filters[i][self.tr('Total')] = False

            if len_min <= len(str(self.item(i, col_ngrams).read_data()).replace(' ', '')) <= len_max:
                self.row_filters[i][self.tr('N-grams')] = True
            else:
                self.row_filters[i][self.tr('N-grams')] = False

            if files_min <= self.item(i, col_files_found).read_data() <= files_max:
                self.row_filters[i][self.tr('Files Found')] = True
            else:
                self.row_filters[i][self.tr('Files Found')] = False

        self.filter_table()

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.settings_default['ngram'])
        else:
            settings = copy.deepcopy(main.settings_custom['ngram'])

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

        checkbox_keyword_position_no_limit.setChecked(settings['keyword_position_no_limit'])
        spin_box_keyword_position_min.setValue(settings['keyword_position_min'])
        spin_box_keyword_position_max.setValue(settings['keyword_position_max'])
        checkbox_ignore_case.setChecked(settings['ignore_case'])
        checkbox_lemmatization.setChecked(settings['lemmatization'])
        checkbox_whole_word.setChecked(settings['whole_word'])
        checkbox_regex.setChecked(settings['regex'])
        checkbox_multi_search.setChecked(settings['multi_search'])
        checkbox_show_all.setChecked(settings['show_all'])

        checkbox_ngram_size_sync.setChecked(settings['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(settings['ngram_size_min'])
        spin_box_ngram_size_max.setValue(settings['ngram_size_max'])
        spin_box_allow_skipped_tokens.setValue(settings['allow_skipped_tokens'])

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
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    def token_settings_changed():
        main.settings_custom['ngram']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        main.settings_custom['ngram']['lowercase'] = checkbox_lowercase.isChecked()
        main.settings_custom['ngram']['uppercase'] = checkbox_uppercase.isChecked()
        main.settings_custom['ngram']['title_cased'] = checkbox_title_cased.isChecked()
        main.settings_custom['ngram']['numerals'] = checkbox_numerals.isChecked()
        main.settings_custom['ngram']['punctuations'] = checkbox_punctuations.isChecked()

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
        if main.settings_custom['ngram']['multi_search']:
            list_search_terms.get_items()
        else:
            if line_edit_search_term.text():
                main.settings_custom['ngram']['search_terms'] = [line_edit_search_term.text()]
            else:
                main.settings_custom['ngram']['search_terms'] = []

        main.settings_custom['ngram']['keyword_position_no_limit'] = checkbox_keyword_position_no_limit.isChecked()
        main.settings_custom['ngram']['keyword_position_min'] = spin_box_keyword_position_min.value()
        main.settings_custom['ngram']['keyword_position_max'] = spin_box_keyword_position_max.value()
        main.settings_custom['ngram']['ignore_case'] = checkbox_ignore_case.isChecked()
        main.settings_custom['ngram']['lemmatization'] = checkbox_lemmatization.isChecked()
        main.settings_custom['ngram']['whole_word'] = checkbox_whole_word.isChecked()
        main.settings_custom['ngram']['regex'] = checkbox_regex.isChecked()
        main.settings_custom['ngram']['multi_search'] = checkbox_multi_search.isChecked()
        main.settings_custom['ngram']['show_all'] = checkbox_show_all.isChecked()

        if main.settings_custom['ngram']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if main.settings_custom['ngram']['show_all']:
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

            if not main.settings_custom['ngram']['keyword_position_no_limit']:
                spin_box_keyword_position_max.setEnabled(True)

    def generation_settings_changed():
        main.settings_custom['ngram']['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        main.settings_custom['ngram']['ngram_size_min'] = spin_box_ngram_size_min.value()
        main.settings_custom['ngram']['ngram_size_max'] = spin_box_ngram_size_max.value()
        main.settings_custom['ngram']['allow_skipped_tokens'] = spin_box_allow_skipped_tokens.value()

        if (main.settings_custom['ngram']['keyword_position_no_limit'] and
            spin_box_keyword_position_max.value() == spin_box_keyword_position_max.maximum()):
            spin_box_keyword_position_min.setMaximum(main.settings_custom['ngram']['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(main.settings_custom['ngram']['ngram_size_max'])

            spin_box_keyword_position_max.setValue(main.settings_custom['ngram']['ngram_size_max'])
        else:
            spin_box_keyword_position_min.setMaximum(main.settings_custom['ngram']['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(main.settings_custom['ngram']['ngram_size_max'])

    def table_settings_changed():
        main.settings_custom['ngram']['show_pct'] = checkbox_show_pct.isChecked()
        main.settings_custom['ngram']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        main.settings_custom['ngram']['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        main.settings_custom['ngram']['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        main.settings_custom['ngram']['rank_min'] = spin_box_rank_min.value()
        main.settings_custom['ngram']['rank_max'] = spin_box_rank_max.value()

        main.settings_custom['ngram']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        main.settings_custom['ngram']['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        main.settings_custom['ngram']['freq_min'] = spin_box_freq_min.value()
        main.settings_custom['ngram']['freq_max'] = spin_box_freq_max.value()
        main.settings_custom['ngram']['freq_apply_to'] = combo_box_freq_apply_to.currentText()

        main.settings_custom['ngram']['len_no_limit'] = checkbox_len_no_limit.isChecked()
        main.settings_custom['ngram']['len_min'] = spin_box_len_min.value()
        main.settings_custom['ngram']['len_max'] = spin_box_len_max.value()

        main.settings_custom['ngram']['files_no_limit'] = checkbox_files_no_limit.isChecked()
        main.settings_custom['ngram']['files_min'] = spin_box_files_min.value()
        main.settings_custom['ngram']['files_max'] = spin_box_files_max.value()

    tab_ngram = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_ngram = Wordless_Table_Ngram(main)

    table_ngram.button_generate_data = QPushButton(main.tr('Generate N-grams'), main)
    table_ngram.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

    table_ngram.button_generate_data.clicked.connect(lambda: generate_data(main, tab_ngram, table_ngram))
    table_ngram.button_generate_plot.clicked.connect(lambda: generate_plot(main, tab_ngram))

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
     checkbox_title_cased,
     checkbox_ignore_case,
     checkbox_lemmatization,
     checkbox_filter_stopwords,
     checkbox_numerals,
     checkbox_punctuations) = wordless_widgets.wordless_widgets_token(main)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_cased.stateChanged.connect(token_settings_changed)
    checkbox_numerals.stateChanged.connect(token_settings_changed)
    checkbox_punctuations.stateChanged.connect(token_settings_changed)
    checkbox_filter_stopwords.stateChanged.connect(token_settings_changed)

    layout_token_settings = QGridLayout()
    layout_token_settings.addWidget(checkbox_words, 0, 0)
    layout_token_settings.addWidget(checkbox_lowercase, 0, 1)
    layout_token_settings.addWidget(checkbox_numerals, 1, 0)
    layout_token_settings.addWidget(checkbox_uppercase, 1, 1)
    layout_token_settings.addWidget(checkbox_punctuations, 2, 0)
    layout_token_settings.addWidget(checkbox_title_cased, 2, 1)
    layout_token_settings.addWidget(checkbox_filter_stopwords, 3, 0, 1, 2)

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

    checkbox_show_all.setText(main.tr('Show All N-grams'))

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
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_ngram)

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
                                                                         table = table_ngram,
                                                                         col = 'Total')

    label_len = QLabel(main.tr('N-gram Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                  table = table_ngram,
                                                                  col = 'N-grams')

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_ngram,
                                                                    col = 'Files Found')

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

    tab_ngram.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    load_settings()

    return tab_ngram

def generate_freq_distributions(main, files):
    freq_distributions = []

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(main, file)
        
        freq_distributions.append(text.ngram(main.settings_custom['ngram']))

    return wordless_distribution.Wordless_Freq_Distribution(wordless_misc.merge_dicts(freq_distributions))

@wordless_misc.check_search_term
@wordless_misc.check_results_table
def generate_data(main, table):
    table.clear_table()

    files = main.wordless_files.selected_files()

    for i, file in enumerate(files):
        table.insert_column(table.find_column(main.tr('Total')), file['name'], with_pct = True)
        table.insert_column(table.find_column(main.tr('Total')), file['name'] + main.tr(' (Cumulative)'), with_pct = True)

    table.sortByColumn(table.find_column('N-grams') + 1, Qt.DescendingOrder)

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

    table.blockSignals(False)
    table.setSortingEnabled(True)
    table.setUpdatesEnabled(True)

    table.update_filters()

    main.status_bar.showMessage(main.tr('Done!'))

@wordless_misc.check_search_term
def generate_plot(main):
    files = main.wordless_files.selected_files()

    freq_distributions = generate_freq_distributions(main, files)

    freq_distributions.plot(files = files,
                            start = main.settings_custom['ngram']['rank_min'] - 1,
                            end = main.settings_custom['ngram']['rank_max'],
                            cumulative = main.settings_custom['ngram']['cumulative'])

    main.status_bar.showMessage(main.tr('Done!'))
