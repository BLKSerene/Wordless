#
# Wordless: Collocation
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Collocation(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Collocates'),
                             main.tr('Total Score'),
                             main.tr('Files Found'),
                         ],
                         cols_with_pct = [
                             main.tr('Files Found')
                         ])

    def update_filters(self):
        settings = self.main.settings_custom['collocation']

        col_score = self.find_col(settings['score_apply_to'])
        col_collocates = self.find_col('Collocates')
        col_files_found = self.find_col('Files Found')

        score_min = settings['score_min']
        score_max = settings['score_max'] if not settings['score_no_limit'] else float('inf')
        len_min = settings['len_min']
        len_max = settings['len_max'] if not settings['len_no_limit'] else float('inf')
        files_min = settings['files_min']
        files_max = settings['files_max'] if not settings['files_no_limit'] else float('inf')

        self.row_filters = [{} for i in range(self.rowCount())]

        for i in range(self.rowCount()):
            if score_min <= self.item(i, col_score).read_data() <= score_max:
                self.row_filters[i][self.tr('Total')] = True
            else:
                self.row_filters[i][self.tr('Total')] = False

            if len_min <= len(str(self.item(i, col_collocates).read_data()).replace(' ', '')) <= len_max:
                self.row_filters[i][self.tr('Collocates')] = True
            else:
                self.row_filters[i][self.tr('Collocates')] = False

            print(self.item(i, col_files_found).raw_value)
            if files_min <= self.item(i, col_files_found).read_data() <= files_max:
                self.row_filters[i][self.tr('Files Found')] = True
            else:
                self.row_filters[i][self.tr('Files Found')] = False

        self.filter_table()

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.settings_default['collocation'])
        else:
            settings = copy.deepcopy(main.settings_custom['collocation'])

        checkbox_words.setChecked(settings['words'])
        checkbox_lowercase.setChecked(settings['lowercase'])
        checkbox_uppercase.setChecked(settings['uppercase'])
        checkbox_title_cased.setChecked(settings['title_cased'])
        checkbox_numerals.setChecked(settings['numerals'])
        checkbox_punctuations.setChecked(settings['punctuations'])

        line_edit_search_term.setText(settings['search_term'])
        list_search_terms.clear()
        for search_term in settings['search_terms']:
            list_search_terms.add_item(search_term)

        checkbox_ignore_case.setChecked(settings['ignore_case'])
        checkbox_lemmatization.setChecked(settings['lemmatization'])
        checkbox_whole_word.setChecked(settings['whole_word'])
        checkbox_regex.setChecked(settings['regex'])
        checkbox_multi_search.setChecked(settings['multi_search'])
        checkbox_show_all.setChecked(settings['show_all'])

        checkbox_window_sync.setChecked(settings['window_sync'])
        spin_box_window_left.setPrefix(settings['window_left'][0])
        spin_box_window_left.setValue(settings['window_left'][1])
        spin_box_window_right.setPrefix(settings['window_right'][0])
        spin_box_window_right.setValue(settings['window_right'][1])
        combo_box_search_for.setCurrentText(settings['search_for'])
        combo_box_assoc_measure.setCurrentText(settings['assoc_measure'])

        checkbox_show_pct.setChecked(settings['show_pct'])
        checkbox_show_cumulative.setChecked(settings['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings['show_breakdown'])

        checkbox_rank_no_limit.setChecked(settings['rank_no_limit'])
        spin_box_rank_min.setValue(settings['rank_min'])
        spin_box_rank_max.setValue(settings['rank_max'])
        checkbox_cumulative.setChecked(settings['cumulative'])

        checkbox_score_no_limit.setChecked(settings['score_no_limit'])
        spin_box_score_min.setValue(settings['score_min'])
        spin_box_score_max.setValue(settings['score_max'])
        combo_box_score_apply_to.setCurrentText(settings['score_apply_to'])

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
        main.settings_custom['collocation']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        main.settings_custom['collocation']['lowercase'] = checkbox_lowercase.isChecked()
        main.settings_custom['collocation']['uppercase'] = checkbox_uppercase.isChecked()
        main.settings_custom['collocation']['title_cased'] = checkbox_title_cased.isChecked()
        main.settings_custom['collocation']['numerals'] = checkbox_numerals.isChecked()
        main.settings_custom['collocation']['punctuations'] = checkbox_punctuations.isChecked()

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
        if main.settings_custom['collocation']['multi_search']:
            list_search_terms.get_items()
        else:
            if line_edit_search_term.text():
                main.settings_custom['collocation']['search_terms'] = [line_edit_search_term.text()]
            else:
                main.settings_custom['collocation']['search_terms'] = []

        main.settings_custom['collocation']['ignore_case'] = checkbox_ignore_case.isChecked()
        main.settings_custom['collocation']['lemmatization'] = checkbox_lemmatization.isChecked()
        main.settings_custom['collocation']['whole_word'] = checkbox_whole_word.isChecked()
        main.settings_custom['collocation']['regex'] = checkbox_regex.isChecked()
        main.settings_custom['collocation']['multi_search'] = checkbox_multi_search.isChecked()
        main.settings_custom['collocation']['show_all'] = checkbox_show_all.isChecked()

        if main.settings_custom['collocation']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if main.settings_custom['collocation']['show_all']:
            table_collocation.button_generate_data.setText(main.tr('Generate Collocates'))
        else:
            table_collocation.button_generate_data.setText(main.tr('Begin Search'))

    def generation_settings_changed():
        main.settings_custom['collocation']['window_sync'] = checkbox_window_sync.isChecked()
        main.settings_custom['collocation']['window_left'][0] = spin_box_window_left.prefix()
        main.settings_custom['collocation']['window_left'][1] = spin_box_window_left.value()
        main.settings_custom['collocation']['window_right'][0] = spin_box_window_right.prefix()
        main.settings_custom['collocation']['window_right'][1] = spin_box_window_right.value()
        main.settings_custom['collocation']['search_for'] = combo_box_search_for.currentText()
        main.settings_custom['collocation']['assoc_measure'] = combo_box_assoc_measure.currentText()

    def table_settings_changed():
        main.settings_custom['collocation']['show_pct'] = checkbox_show_pct.isChecked()
        main.settings_custom['collocation']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        main.settings_custom['collocation']['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        main.settings_custom['collocation']['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        main.settings_custom['collocation']['rank_min'] = spin_box_rank_min.value()
        main.settings_custom['collocation']['rank_max'] = spin_box_rank_max.value()

        main.settings_custom['collocation']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        main.settings_custom['collocation']['score_no_limit'] = checkbox_score_no_limit.isChecked()
        main.settings_custom['collocation']['score_min'] = spin_box_score_min.value()
        main.settings_custom['collocation']['score_max'] = spin_box_score_max.value()
        main.settings_custom['collocation']['score_apply_to'] = combo_box_score_apply_to.currentText()

        main.settings_custom['collocation']['len_no_limit'] = checkbox_len_no_limit.isChecked()
        main.settings_custom['collocation']['len_min'] = spin_box_len_min.value()
        main.settings_custom['collocation']['len_max'] = spin_box_len_max.value()

        main.settings_custom['collocation']['files_no_limit'] = checkbox_files_no_limit.isChecked()
        main.settings_custom['collocation']['files_min'] = spin_box_files_min.value()
        main.settings_custom['collocation']['files_max'] = spin_box_files_max.value()

    tab_collocation = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_collocation = Wordless_Table_Collocation(main)

    table_collocation.button_generate_data = QPushButton(main.tr('Generate Collocates'), main)
    table_collocation.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

    table_collocation.button_generate_data.clicked.connect(lambda: generate_data(main, tab_collocation, table_collocation))
    table_collocation.button_generate_plot.clicked.connect(lambda: generate_plot(main, tab_collocation))

    tab_collocation.layout_table.addWidget(table_collocation, 0, 0, 1, 5)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_data, 1, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_plot, 1, 1)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_selected, 1, 2)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_all, 1, 3)
    tab_collocation.layout_table.addWidget(table_collocation.button_clear, 1, 4)

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

    checkbox_show_all.setText(main.tr('Show All Collocates'))

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_collocation.button_generate_data.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
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
    layout_search_settings.addWidget(label_search_term, 0, 0)
    layout_search_settings.addWidget(line_edit_search_term, 1, 0)
    layout_search_settings.addLayout(layout_search_terms, 2, 0)
    layout_search_settings.addWidget(checkbox_ignore_case, 3, 0)
    layout_search_settings.addWidget(checkbox_lemmatization, 4, 0)
    layout_search_settings.addWidget(checkbox_whole_word, 5, 0)
    layout_search_settings.addWidget(checkbox_regex, 6, 0)
    layout_search_settings.addWidget(checkbox_multi_search, 7, 0)
    layout_search_settings.addWidget(checkbox_show_all, 8, 0)

    group_box_search_settings.setLayout(layout_search_settings)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_window = QLabel(main.tr('Collocational Window:'), main)
    (checkbox_window_sync,
     label_window_left,
     spin_box_window_left,
     label_window_right,
     spin_box_window_right) = wordless_widgets.wordless_widgets_window(main)
    (label_search_for,
     combo_box_search_for,
     label_assoc_measure,
     combo_box_assoc_measure) = wordless_widgets.wordless_widgets_collocation(main,
                                                                              main.settings_default['collocation']['assoc_measure'])

    checkbox_window_sync.stateChanged.connect(generation_settings_changed)
    spin_box_window_left.valueChanged.connect(generation_settings_changed)
    spin_box_window_right.valueChanged.connect(generation_settings_changed)
    combo_box_search_for.currentTextChanged.connect(generation_settings_changed)
    combo_box_assoc_measure.currentTextChanged.connect(generation_settings_changed)

    layout_generation_settings = QGridLayout()
    layout_generation_settings.addWidget(label_window, 0, 0, 1, 3)
    layout_generation_settings.addWidget(checkbox_window_sync, 0, 3)
    layout_generation_settings.addWidget(label_window_left, 1, 0)
    layout_generation_settings.addWidget(spin_box_window_left, 1, 1)
    layout_generation_settings.addWidget(label_window_right, 1, 2)
    layout_generation_settings.addWidget(spin_box_window_right, 1, 3)
    layout_generation_settings.addWidget(label_search_for, 2, 0, 1, 2)
    layout_generation_settings.addWidget(combo_box_search_for, 2, 2, 1, 2)
    layout_generation_settings.addWidget(label_assoc_measure, 3, 0, 1, 4)
    layout_generation_settings.addWidget(combo_box_assoc_measure, 4, 0, 1, 4)

    group_box_generation_settings.setLayout(layout_generation_settings)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_collocation)

    checkbox_show_cumulative.hide()

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    layout_table_settings = QGridLayout()
    layout_table_settings.addWidget(checkbox_show_pct, 0, 0)
    layout_table_settings.addWidget(checkbox_show_breakdown, 1, 0)

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

    label_score = QLabel(main.tr('Score:'), main)
    (checkbox_score_no_limit,
     label_score_min,
     spin_box_score_min,
     label_score_max,
     spin_box_score_max,
     label_score_apply_to,
     combo_box_score_apply_to) = wordless_widgets.wordless_widgets_filter(main,
                                                                          filter_min = 0,
                                                                          filter_max = 10000,
                                                                          table = table_collocation,
                                                                          col = 'Total')

    label_len = QLabel(main.tr('N-gram Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                  table = table_collocation,
                                                                  col = 'Collocates')

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_collocation,
                                                                    col = 'Files Found')

    checkbox_score_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_score_min.editingFinished.connect(filter_settings_changed)
    spin_box_score_max.editingFinished.connect(filter_settings_changed)
    combo_box_score_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.editingFinished.connect(filter_settings_changed)
    spin_box_len_max.editingFinished.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.editingFinished.connect(filter_settings_changed)
    spin_box_files_max.editingFinished.connect(filter_settings_changed)

    layout_filter_settings = QGridLayout()
    layout_filter_settings.addWidget(label_score, 0, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_score_no_limit, 0, 3)
    layout_filter_settings.addWidget(label_score_min, 1, 0)
    layout_filter_settings.addWidget(spin_box_score_min, 1, 1)
    layout_filter_settings.addWidget(label_score_max, 1, 2)
    layout_filter_settings.addWidget(spin_box_score_max, 1, 3)
    layout_filter_settings.addWidget(label_score_apply_to, 2, 0)
    layout_filter_settings.addWidget(combo_box_score_apply_to, 2, 1, 1, 3)

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

    tab_collocation.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    load_settings()

    return tab_collocation

def generate_score_distributions(main, files):
    score_distributions = []

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(main, file)
        
        score_distributions.append(text.collocation(main.settings_custom['collocation']))

    score_distributions = wordless_misc.merge_dicts(score_distributions)

    # Calculate the total score of all texts
    text_total = wordless_text.Wordless_Text(main, files)

    score_distribution_total = text_total.collocation(main.settings_custom['collocation'])

    # Append total scores
    for token, score in score_distribution_total.items():
        if token in score_distributions:
            score_distributions[token].append(score)

    return wordless_distribution.Wordless_Freq_Distribution(score_distributions)

@wordless_misc.check_search_term
@wordless_misc.check_results_table
def generate_data(main, table):
    table.clear_table()

    files = main.wordless_files.selected_files()

    for i, file in enumerate(files):
        table.insert_column(table.find_column(main.tr('Total Score')), file['name'])

    table.sortByColumn(table.find_column('Collocates') + 1, Qt.DescendingOrder)

    score_distributions = generate_score_distributions(main, files)

    col_total_score = table.find_column(main.tr('Total Score'))
    col_files_found = table.find_column(main.tr('Files Found'))

    len_files = len(files)

    table.blockSignals(True)
    table.setSortingEnabled(False)
    table.setUpdatesEnabled(False)

    table.setRowCount(len(score_distributions))

    for i, (collocate, scores) in enumerate(score_distributions.items()):
        # Collocates
        table.setItem(i, 1, wordless_table.Wordless_Table_Item(collocate))

        score_files = list(zip(*score_distributions.values()))

        for j, score in enumerate(scores):
            score_max = max(score_files[j])

            # Score
            table.set_item_data(i, 2 + j, score, score_max)

            # Total Score
            if j == len_files - 1:
                table.set_item_data(i, col_total_score, score, score_max)

        # Files Found
        table.set_item_with_pct(i, col_files_found, len([score for score in scores[:-1] if score != 0]), len_files)
    
    table.blockSignals(False)
    table.setSortingEnabled(True)
    table.setUpdatesEnabled(True)

    table.update_filters()
    
    main.status_bar.showMessage('Done!')
