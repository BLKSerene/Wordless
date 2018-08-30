#
# Wordless: Collocation
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import *

def init(self):
    def token_settings_changed():
        self.settings['collocation']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        self.settings['collocation']['lowercase'] = checkbox_lowercase.isChecked()
        self.settings['collocation']['uppercase'] = checkbox_uppercase.isChecked()
        self.settings['collocation']['title_cased'] = checkbox_title_cased.isChecked()
        self.settings['collocation']['numerals'] = checkbox_numerals.isChecked()
        self.settings['collocation']['punctuations'] = checkbox_punctuations.isChecked()

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
        if self.settings['collocation']['multi_search']:
            list_search_terms.get_items()
        else:
            if line_edit_search_term.text():
                self.settings['collocation']['search_terms'] = [line_edit_search_term.text()]
            else:
                self.settings['collocation']['search_terms'] = []

        self.settings['collocation']['ignore_case'] = checkbox_ignore_case.isChecked()
        self.settings['collocation']['lemmatization'] = checkbox_lemmatization.isChecked()
        self.settings['collocation']['whole_word'] = checkbox_whole_word.isChecked()
        self.settings['collocation']['regex'] = checkbox_regex.isChecked()
        self.settings['collocation']['multi_search'] = checkbox_multi_search.isChecked()
        self.settings['collocation']['show_all'] = checkbox_show_all.isChecked()

        if self.settings['collocation']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if self.settings['collocation']['show_all']:
            table_collocation.button_generate_data.setText(self.tr('Generate Collocates'))
        else:
            table_collocation.button_generate_data.setText(self.tr('Begin Search'))

    def generation_settings_changed():
        self.settings['collocation']['window_sync'] = checkbox_window_sync.isChecked()
        self.settings['collocation']['window_left'][0] = spin_box_window_left.prefix()
        self.settings['collocation']['window_left'][1] = spin_box_window_left.value()
        self.settings['collocation']['window_right'][0] = spin_box_window_right.prefix()
        self.settings['collocation']['window_right'][1] = spin_box_window_right.value()
        self.settings['collocation']['search_for'] = combo_box_search_for.currentText()
        self.settings['collocation']['assoc_measure'] = combo_box_assoc_measure.currentText()

    def table_settings_changed():
        self.settings['collocation']['show_pct'] = checkbox_show_pct.isChecked()
        self.settings['collocation']['show_cumulative'] = checkbox_show_cumulative.isChecked()
        self.settings['collocation']['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        self.settings['collocation']['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        self.settings['collocation']['rank_min'] = spin_box_rank_min.value()
        self.settings['collocation']['rank_max'] = (None
                                              if checkbox_rank_no_limit.isChecked()
                                              else spin_box_rank_max.value())

        self.settings['collocation']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['collocation']['score_no_limit'] = checkbox_score_no_limit.isChecked()
        self.settings['collocation']['score_min'] = spin_box_score_min.value()
        self.settings['collocation']['score_max'] = (float('inf')
                                                     if checkbox_score_no_limit.isChecked()
                                                     else spin_box_score_max.value())
        self.settings['collocation']['score_apply_to'] = table_collocation.combo_box_score_apply_to.currentText()

        self.settings['collocation']['len_no_limit'] = checkbox_len_no_limit.isChecked()
        self.settings['collocation']['len_min'] = spin_box_len_min.value()
        self.settings['collocation']['len_max'] = (float('inf')
                                                   if checkbox_len_no_limit.isChecked()
                                                   else spin_box_len_max.value())

        self.settings['collocation']['files_no_limit'] = checkbox_files_no_limit.isChecked()
        self.settings['collocation']['files_min'] = spin_box_files_min.value()
        self.settings['collocation']['files_max'] = (float('inf')
                                                     if checkbox_files_no_limit.isChecked()
                                                     else spin_box_files_max.value())

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['collocation']['words'])
        checkbox_lowercase.setChecked(self.default_settings['collocation']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['collocation']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['collocation']['title_cased'])
        checkbox_numerals.setChecked(self.default_settings['collocation']['numerals'])
        checkbox_punctuations.setChecked(self.default_settings['collocation']['punctuations'])

        line_edit_search_term.clear()
        list_search_terms.clear()
        checkbox_ignore_case.setChecked(self.default_settings['collocation']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['collocation']['lemmatization'])
        checkbox_whole_word.setChecked(self.default_settings['collocation']['whole_word'])
        checkbox_regex.setChecked(self.default_settings['collocation']['regex'])
        checkbox_multi_search.setChecked(self.default_settings['collocation']['multi_search'])
        checkbox_show_all.setChecked(self.default_settings['collocation']['show_all'])

        checkbox_window_sync.setChecked(self.default_settings['collocation']['window_sync'])
        spin_box_window_left.setPrefix(self.default_settings['collocation']['window_left'][0])
        spin_box_window_left.setValue(self.default_settings['collocation']['window_left'][1])
        spin_box_window_right.setPrefix(self.default_settings['collocation']['window_right'][0])
        spin_box_window_right.setValue(self.default_settings['collocation']['window_right'][1])
        combo_box_search_for.setCurrentText(self.default_settings['collocation']['search_for'])
        combo_box_assoc_measure.setCurrentText(self.default_settings['collocation']['assoc_measure'])

        checkbox_show_pct.setChecked(self.default_settings['collocation']['show_pct'])
        checkbox_show_cumulative.setChecked(self.default_settings['collocation']['show_cumulative'])
        checkbox_show_breakdown.setChecked(self.default_settings['collocation']['show_breakdown'])

        checkbox_rank_no_limit.setChecked(self.default_settings['collocation']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['collocation']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['collocation']['rank_max'])
        checkbox_cumulative.setChecked(self.default_settings['collocation']['cumulative'])

        checkbox_score_no_limit.setChecked(self.default_settings['collocation']['score_no_limit'])
        spin_box_score_min.setValue(self.default_settings['collocation']['score_min'])
        spin_box_score_max.setValue(self.default_settings['collocation']['score_max'])
        table_collocation.combo_box_score_apply_to.setCurrentText(self.default_settings['collocation']['score_apply_to'])

        checkbox_len_no_limit.setChecked(self.default_settings['collocation']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['collocation']['len_min'])
        spin_box_len_max.setValue(self.default_settings['collocation']['len_max'])

        checkbox_files_no_limit.setChecked(self.default_settings['collocation']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['collocation']['files_min'])
        spin_box_files_max.setValue(self.default_settings['collocation']['files_max'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
        table_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_collocation = wordless_tab.Wordless_Tab(self, self.tr('Collocation'))
    
    table_collocation = wordless_table.Wordless_Table(self,
                                                      headers = [
                                                          self.tr('Rank'),
                                                          self.tr('Collocates'),
                                                          self.tr('Total Score'),
                                                          self.tr('Files Found'),
                                                      ])

    table_collocation.button_generate_data = QPushButton(self.tr('Generate Collocates'), self)
    table_collocation.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_collocation.button_generate_data.clicked.connect(lambda: generate_data(tab_collocation, table_collocation))
    table_collocation.button_generate_plot.clicked.connect(lambda: generate_plot(tab_collocation))

    tab_collocation.layout_table.addWidget(table_collocation, 0, 0, 1, 5)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_data, 1, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_plot, 1, 1)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_selected, 1, 2)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_all, 1, 3)
    tab_collocation.layout_table.addWidget(table_collocation.button_clear, 1, 4)

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

    checkbox_show_all.setText(self.tr('Show All Collocates'))

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
    group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

    label_window = QLabel(self.tr('Collocational Window:'), self)
    (checkbox_window_sync,
     label_window_left,
     spin_box_window_left,
     label_window_right,
     spin_box_window_right) = wordless_widgets.wordless_widgets_window(self)
    (label_search_for,
     combo_box_search_for,
     label_assoc_measure,
     combo_box_assoc_measure) = wordless_widgets.wordless_widgets_collocation(self,
                                                                              self.default_settings['collocation']['assoc_measure'])

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
    group_box_table_settings = QGroupBox(self.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self, table_collocation)

    checkbox_show_cumulative.hide()

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    layout_table_settings = QGridLayout()
    layout_table_settings.addWidget(checkbox_show_pct, 0, 0)
    layout_table_settings.addWidget(checkbox_show_breakdown, 1, 0)

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

    label_score = QLabel(self.tr('Score:'), self)
    (checkbox_score_no_limit,
     label_score_min,
     spin_box_score_min,
     label_score_max,
     spin_box_score_max,
     label_score_apply_to,
     table_collocation.combo_box_score_apply_to) = wordless_widgets.wordless_widgets_filter(self,
                                                                                            filter_min = 0,
                                                                                            filter_max = 10000,
                                                                                            table = table_collocation,
                                                                                            column = 'Total')

    label_len = QLabel(self.tr('N-gram Length:'), self)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(self, table = table_collocation, column = 'Collocates')

    label_files = QLabel(self.tr('Files Found:'), self)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(self, filter_min = 1, filter_max = 1000,
                                                                    table = table_collocation, column = 'Files Found')

    checkbox_score_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_score_min.editingFinished.connect(filter_settings_changed)
    spin_box_score_max.editingFinished.connect(filter_settings_changed)
    table_collocation.combo_box_score_apply_to.currentTextChanged.connect(filter_settings_changed)

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
    layout_filter_settings.addWidget(table_collocation.combo_box_score_apply_to, 2, 1, 1, 3)

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

    tab_collocation.button_restore_defaults.clicked.connect(restore_defaults)

    restore_defaults()

    return tab_collocation

@wordless_misc.check_search_term
@wordless_misc.check_results_table
def generate_data(self, table):
    score_previous = -1

    table.clear_table()

    files = wordless_misc.fetch_files(self)

    # Update filter settings
    apply_to_text_old = table.combo_box_freq_apply_to.currentText()
    table.combo_box_freq_apply_to.clear()
    
    for i, file in enumerate(files):
        table.insert_column(table.find_column(self.tr('Total Score')), file.name)

        table.combo_box_freq_apply_to.addItem(file.name)
    table.combo_box_freq_apply_to.addItem('Total')

    if apply_to_text_old == file.name:
        table.combo_box_freq_apply_to.setCurrentText(file.name)

    collocation_scores = wordless_distribution.wordless_distributions(self, files, mode = 'collocation')

    col_total_score = table.find_column(self.tr('Total Score'))
    col_files_found = table.find_column(self.tr('Files Found'))

    len_files = len(files)

    table.setSortingEnabled(False)
    table.setUpdatesEnabled(False)
    table.setRowCount(len(collocation_scores))

    for i, (collocate, scores) in enumerate(collocation_scores.items()):
        # Collocates
        table.setItem(i, 1, wordless_table.Wordless_Table_Item(collocate))

        # Score
        for j, score in enumerate(scores):
            table.setItem(i, 2 + j, wordless_table.Wordless_Table_Item())
            table.item(i, 2 + j).setData(Qt.DisplayRole, score)

        # Files Found
        table.set_item_with_pct(i, col_files_found, len([score for score in scores if score > 0]), len_files)
    
    table.sortByColumn(table.find_column('Collocates') + 1, Qt.DescendingOrder)

    table.combo_box_score_apply_to.currentTextChanged.emit('')

    table.setSortingEnabled(True)
    table.setUpdatesEnabled(True)
    
    self.status_bar.showMessage('Done!')
