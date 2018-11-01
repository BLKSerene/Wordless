#
# Wordless: Collocation
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk
import numpy

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Collocation(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Keywords'),
                             main.tr('Collocates'),
                             main.tr('Files Found'),
                         ],
                         headers_num = [
                             main.tr('Rank'),
                             main.tr('Files Found'),
                         ],
                         headers_pct = [
                             main.tr('Files Found')
                         ],
                         sorting_enabled = True)

        dialog_search = wordless_dialog.Wordless_Dialog_Search(self.main,
                                                               tab = 'collocation',
                                                               table = self,
                                                               cols_search = [
                                                                   self.tr('Keywords'),
                                                                   self.tr('Collocates')
                                                               ])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(main.tr('Generate Table'), main)
        self.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    def toggle_breakdown(self):
        settings = self.main.settings_custom['collocation']

        self.setUpdatesEnabled(False)

        for col in self.cols_breakdown | self.cols_breakdown_position:
            if col in self.cols_breakdown and col in self.cols_breakdown_position:
                if settings['show_breakdown_file'] and settings['show_breakdown_position']:
                    self.showColumn(col)
                else:
                    self.hideColumn(col)
            elif col in self.cols_breakdown:
                if settings['show_breakdown_file']:
                    self.showColumn(col)
                else:
                    self.hideColumn(col)
            elif col in self.cols_breakdown_position:
                if settings['show_breakdown_position']:
                    self.showColumn(col)
                else:
                    self.hideColumn(col)

        self.setUpdatesEnabled(True)

    def clear_table(self, count = 1):
        super().clear_table(count)

        self.cols_breakdown_position = set()

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['collocation']

            if settings['apply_to'] == self.tr('Total'):
                col_freq_left = self.find_col(self.tr('Total\nFrequency/L'))
                col_freq_right = self.find_col(self.tr('Total\nFrequency/R'))
                col_score_left = self.find_col(self.tr('Total\nScore/L'))
                col_score_right = self.find_col(self.tr('Total\nScore/R'))
            else:
                col_freq_left = self.find_col(self.tr(f'[{settings["apply_to"]}]\nFrequency/L'))
                col_freq_right = self.find_col(self.tr(f'[{settings["apply_to"]}]\nFrequency/R'))
                col_score_left = self.find_col(self.tr(f'[{settings["apply_to"]}]\nScore/L'))
                col_score_right = self.find_col(self.tr(f'[{settings["apply_to"]}]\nScore/R'))

            col_collocates = self.find_col('Collocates')
            col_files_found = self.find_col('Files Found')

            freq_left_min = settings['freq_left_min']
            freq_left_max = settings['freq_left_max'] if not settings['freq_left_no_limit'] else float('inf')
            freq_right_min = settings['freq_right_min']
            freq_right_max = settings['freq_right_max'] if not settings['freq_right_no_limit'] else float('inf')

            score_left_min = settings['score_left_min']
            score_left_max = settings['score_left_max'] if not settings['score_left_no_limit'] else float('inf')
            score_right_min = settings['score_right_min']
            score_right_max = settings['score_right_max'] if not settings['score_right_no_limit'] else float('inf')

            len_min = settings['len_min']
            len_max = settings['len_max'] if not settings['len_no_limit'] else float('inf')

            files_min = settings['files_min']
            files_max = settings['files_max'] if not settings['files_no_limit'] else float('inf')

            self.row_filters = [[] for i in range(self.rowCount())]

            for i in range(self.rowCount()):
                if freq_left_min <= self.item(i, col_freq_left).val_raw <= freq_left_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)
                if freq_right_min <= self.item(i, col_freq_right).val_raw <= freq_right_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if score_left_min <= self.item(i, col_score_left).val <= score_left_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)
                if score_right_min <= self.item(i, col_score_right).val <= score_right_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if len_min <= len(self.item(i, col_collocates).text().replace(' ', '')) <= len_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if files_min <= self.item(i, col_files_found).val <= files_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

            self.filter_table()

        self.main.status_bar.showMessage(self.tr('Filtering completed!'))

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings_loaded = copy.deepcopy(main.settings_default['collocation'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['collocation'])

        checkbox_words.setChecked(settings_loaded['words'])
        checkbox_lowercase.setChecked(settings_loaded['lowercase'])
        checkbox_uppercase.setChecked(settings_loaded['uppercase'])
        checkbox_title_case.setChecked(settings_loaded['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings_loaded['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings_loaded['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings_loaded['filter_stop_words'])

        checkbox_nums.setChecked(settings_loaded['nums'])
        checkbox_puncs.setChecked(settings_loaded['puncs'])

        if not defaults:
            line_edit_search_term.setText(settings_loaded['search_term'])

            for search_term in settings_loaded['search_terms']:
                list_search_terms.add_item(search_term)

        checkbox_ignore_case.setChecked(settings_loaded['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings_loaded['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings_loaded['match_whole_word'])
        checkbox_use_regex.setChecked(settings_loaded['use_regex'])
        checkbox_multi_search_mode.setChecked(settings_loaded['multi_search_mode'])
        checkbox_show_all.setChecked(settings_loaded['show_all'])

        checkbox_window_sync.setChecked(settings_loaded['window_sync'])
        if settings_loaded['window_left'] < 0:
            spin_box_window_left.setPrefix('L')
            spin_box_window_left.setValue(-settings_loaded['window_left'])
        else:
            spin_box_window_left.setPrefix('R')
            spin_box_window_left.setValue(settings_loaded['window_left'])
        if settings_loaded['window_right'] < 0:
            spin_box_window_right.setPrefix('L')
            spin_box_window_right.setValue(-settings_loaded['window_right'])
        else:
            spin_box_window_right.setPrefix('R')
            spin_box_window_right.setValue(settings_loaded['window_right'])
        combo_box_assoc_measure.setCurrentText(settings_loaded['assoc_measure'])

        checkbox_show_pct.setChecked(settings_loaded['show_pct'])
        checkbox_show_cumulative.setChecked(settings_loaded['show_cumulative'])
        checkbox_show_breakdown_position.setChecked(settings_loaded['show_breakdown_position'])
        checkbox_show_breakdown_file.setChecked(settings_loaded['show_breakdown_file'])

        combo_box_use_data.setCurrentText(settings_loaded['use_data'])
        checkbox_use_pct.setChecked(settings_loaded['use_pct'])
        checkbox_use_cumulative.setChecked(settings_loaded['use_cumulative'])

        checkbox_rank_no_limit.setChecked(settings_loaded['rank_no_limit'])
        spin_box_rank_min.setValue(settings_loaded['rank_min'])
        spin_box_rank_max.setValue(settings_loaded['rank_max'])

        combo_box_apply_to.setCurrentText(settings_loaded['apply_to'])

        checkbox_freq_left_no_limit.setChecked(settings_loaded['freq_left_no_limit'])
        spin_box_freq_left_min.setValue(settings_loaded['freq_left_min'])
        spin_box_freq_left_max.setValue(settings_loaded['freq_left_max'])
        checkbox_freq_right_no_limit.setChecked(settings_loaded['freq_right_no_limit'])
        spin_box_freq_right_min.setValue(settings_loaded['freq_right_min'])
        spin_box_freq_right_max.setValue(settings_loaded['freq_right_max'])

        checkbox_score_left_no_limit.setChecked(settings_loaded['score_left_no_limit'])
        spin_box_score_left_min.setValue(settings_loaded['score_left_min'])
        spin_box_score_left_max.setValue(settings_loaded['score_left_max'])
        checkbox_score_right_no_limit.setChecked(settings_loaded['score_right_no_limit'])
        spin_box_score_right_min.setValue(settings_loaded['score_right_min'])
        spin_box_score_right_max.setValue(settings_loaded['score_right_max'])

        checkbox_len_no_limit.setChecked(settings_loaded['len_no_limit'])
        spin_box_len_min.setValue(settings_loaded['len_min'])
        spin_box_len_max.setValue(settings_loaded['len_max'])

        checkbox_files_no_limit.setChecked(settings_loaded['files_no_limit'])
        spin_box_files_min.setValue(settings_loaded['files_min'])
        spin_box_files_max.setValue(settings_loaded['files_max'])

        token_settings_changed()
        search_settings_changed()
        generation_settings_changed()
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
        settings['show_all'] = checkbox_show_all.isChecked()

    def generation_settings_changed():
        settings['window_sync'] = checkbox_window_sync.isChecked()
        if spin_box_window_left.prefix() == 'L':
            settings['window_left'] = -spin_box_window_left.value()
        else:
            settings['window_left'] = spin_box_window_left.value()
        if spin_box_window_right.prefix() == 'L':
            settings['window_right'] = -spin_box_window_right.value()
        else:
            settings['window_right'] = spin_box_window_right.value()
        settings['assoc_measure'] = combo_box_assoc_measure.currentText()

        use_data_old = settings['use_data']

        combo_box_use_data.clear()

        for i in range(settings['window_left'], settings['window_right'] + 1):
            if i < 0:
                combo_box_use_data.addItem(main.tr(f'Frequency (L{-i})'))
            elif i > 0:
                combo_box_use_data.addItem(main.tr(f'Frequency (R{i})'))
        combo_box_use_data.addItems([
                                        main.tr('Frequency (Left)'),
                                        main.tr('Frequency (Right)'),
                                        main.tr('Score (Left)'),
                                        main.tr('Score (Right)')
                                    ])

        for i in range(combo_box_use_data.count()):
            if combo_box_use_data.itemText(i) == use_data_old:
                combo_box_use_data.setCurrentIndex(i)

                break

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown_position'] = checkbox_show_breakdown_position.isChecked()
        settings['show_breakdown_file'] = checkbox_show_breakdown_file.isChecked()

    def plot_settings_changed():
        settings['use_data'] = combo_box_use_data.currentText()
        settings['use_pct'] = checkbox_use_pct.isChecked()
        settings['use_cumulative'] = checkbox_use_cumulative.isChecked()

        settings['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_max'] = spin_box_rank_max.value()

        if settings['use_data'].find('Score') > -1:
            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)
        else:
            checkbox_use_pct.setEnabled(True)
            checkbox_use_cumulative.setEnabled(True)

    def filter_settings_changed():
        settings['apply_to'] = combo_box_apply_to.currentText()

        settings['freq_left_no_limit'] = checkbox_freq_left_no_limit.isChecked()
        settings['freq_left_min'] = spin_box_freq_left_min.value()
        settings['freq_left_max'] = spin_box_freq_left_max.value()
        settings['freq_right_no_limit'] = checkbox_freq_right_no_limit.isChecked()
        settings['freq_right_min'] = spin_box_freq_right_min.value()
        settings['freq_right_max'] = spin_box_freq_right_max.value()

        settings['score_left_no_limit'] = checkbox_score_left_no_limit.isChecked()
        settings['score_left_min'] = spin_box_score_left_min.value()
        settings['score_left_max'] = spin_box_score_left_max.value()
        settings['score_right_no_limit'] = checkbox_score_right_no_limit.isChecked()
        settings['score_right_min'] = spin_box_score_right_min.value()
        settings['score_right_max'] = spin_box_score_right_max.value()

        settings['len_no_limit'] = checkbox_len_no_limit.isChecked()
        settings['len_min'] = spin_box_len_min.value()
        settings['len_max'] = spin_box_len_max.value()

        settings['files_no_limit'] = checkbox_files_no_limit.isChecked()
        settings['files_min'] = spin_box_files_min.value()
        settings['files_max'] = spin_box_files_max.value()

    settings = main.settings_custom['collocation']

    tab_collocation = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_collocation = Wordless_Table_Collocation(main)

    tab_collocation.layout_table.addWidget(table_collocation.label_number_results, 0, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_search_results, 0, 4)
    tab_collocation.layout_table.addWidget(table_collocation, 1, 0, 1, 5)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_table, 2, 0)
    tab_collocation.layout_table.addWidget(table_collocation.button_generate_plot, 2, 1)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_selected, 2, 2)
    tab_collocation.layout_table.addWidget(table_collocation.button_export_all, 2, 3)
    tab_collocation.layout_table.addWidget(table_collocation.button_clear, 2, 4)

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

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_collocation.button_generate_table.click)
    list_search_terms.itemChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    checkbox_show_all.stateChanged.connect(search_settings_changed)

    layout_show_all = QGridLayout()
    layout_show_all.addWidget(label_search_term, 0, 0, Qt.AlignLeft)
    layout_show_all.addWidget(checkbox_show_all, 0, 1, Qt.AlignRight)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addLayout(layout_show_all, 0, 0)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 3, 0)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 4, 0)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 5, 0)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 6, 0)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 7, 0)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_window = QLabel(main.tr('Collocational Window:'), main)
    (checkbox_window_sync,
     label_window_left,
     spin_box_window_left,
     label_window_right,
     spin_box_window_right) = wordless_widgets.wordless_widgets_window(main)

    label_assoc_measure = QLabel(main.tr('Association Measure:'), main)
    combo_box_assoc_measure = QComboBox(main)

    combo_box_assoc_measure.addItems(main.settings_global['assoc_measures'])

    checkbox_window_sync.stateChanged.connect(generation_settings_changed)
    spin_box_window_left.valueChanged.connect(generation_settings_changed)
    spin_box_window_right.valueChanged.connect(generation_settings_changed)
    combo_box_assoc_measure.currentTextChanged.connect(generation_settings_changed)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_window, 0, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(checkbox_window_sync, 0, 3)
    group_box_generation_settings.layout().addWidget(label_window_left, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_window_left, 1, 1)
    group_box_generation_settings.layout().addWidget(label_window_right, 1, 2)
    group_box_generation_settings.layout().addWidget(spin_box_window_right, 1, 3)
    group_box_generation_settings.layout().addWidget(label_assoc_measure, 2, 0, 1, 4)
    group_box_generation_settings.layout().addWidget(combo_box_assoc_measure, 3, 0, 1, 4)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown_file) = wordless_widgets.wordless_widgets_table(main, table_collocation)

    checkbox_show_breakdown_file.setText('Show Breakdown by File')
    checkbox_show_breakdown_position = QCheckBox('Show Breakdown by Span Position', main)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_position.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_position.stateChanged.connect(table_collocation.toggle_breakdown)
    checkbox_show_breakdown_file.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown_file.stateChanged.connect(table_collocation.toggle_breakdown)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown_position, 2, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown_file, 3, 0)

    # Plot Settings
    group_box_plot_settings = QGroupBox(main.tr('Plot Settings'), main)

    label_use_data = QLabel(main.tr('Use Data:'), main)
    combo_box_use_data = wordless_box.Wordless_Combo_Box(main)
    checkbox_use_pct = QCheckBox(main.tr('Use Percentage Data'), main)
    checkbox_use_cumulative = QCheckBox(main.tr('Use Cumulative Data'), main)

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 10000)

    combo_box_use_data.currentTextChanged.connect(plot_settings_changed)
    checkbox_use_pct.stateChanged.connect(plot_settings_changed)
    checkbox_use_cumulative.stateChanged.connect(plot_settings_changed)

    checkbox_rank_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)

    layout_use_data = QGridLayout()
    layout_use_data.addWidget(label_use_data, 0, 0)
    layout_use_data.addWidget(combo_box_use_data, 0, 1)

    layout_use_data.setColumnStretch(1, 10)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addLayout(layout_use_data, 0, 0, 1, 4)
    group_box_plot_settings.layout().addWidget(checkbox_use_pct, 1, 0, 1, 4)
    group_box_plot_settings.layout().addWidget(checkbox_use_cumulative, 2, 0, 1, 4)
    
    group_box_plot_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 4)

    group_box_plot_settings.layout().addWidget(label_rank, 4, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_rank_no_limit, 4, 3)
    group_box_plot_settings.layout().addWidget(label_rank_min, 5, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_min, 5, 1)
    group_box_plot_settings.layout().addWidget(label_rank_max, 5, 2)
    group_box_plot_settings.layout().addWidget(spin_box_rank_max, 5, 3)

    # Filter Settings
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_apply_to = QLabel(main.tr('Apply Following Filters to:'), main)
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_collocation)

    label_freq_left = QLabel(main.tr('Frequency (Left):'), main)
    (checkbox_freq_left_no_limit,
     label_freq_left_min,
     spin_box_freq_left_min,
     label_freq_left_max,
     spin_box_freq_left_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_freq_right = QLabel(main.tr('Frequency (Right):'), main)
    (checkbox_freq_right_no_limit,
     label_freq_right_min,
     spin_box_freq_right_min,
     label_freq_right_max,
     spin_box_freq_right_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_score_left = QLabel(main.tr('Score (Left):'), main)
    (checkbox_score_left_no_limit,
     label_score_left_min,
     spin_box_score_left_min,
     label_score_left_max,
     spin_box_score_left_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0.0, filter_max = 10000.0)

    label_score_right = QLabel(main.tr('Score (Right):'), main)
    (checkbox_score_right_no_limit,
     label_score_right_min,
     spin_box_score_right_min,
     label_score_right_max,
     spin_box_score_right_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0.0, filter_max = 10000.0)

    label_len = QLabel(main.tr('Collocate Length:'), main)
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

    button_filter_results = QPushButton(main.tr('Filter Results'), main)

    combo_box_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_freq_left_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_left_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_left_max.valueChanged.connect(filter_settings_changed)
    checkbox_freq_right_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_right_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_right_max.valueChanged.connect(filter_settings_changed)

    checkbox_score_left_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_score_left_min.valueChanged.connect(filter_settings_changed)
    spin_box_score_left_max.valueChanged.connect(filter_settings_changed)
    checkbox_score_right_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_score_right_min.valueChanged.connect(filter_settings_changed)
    spin_box_score_right_max.valueChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.valueChanged.connect(filter_settings_changed)
    spin_box_len_max.valueChanged.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.valueChanged.connect(filter_settings_changed)
    spin_box_files_max.valueChanged.connect(filter_settings_changed)

    button_filter_results.clicked.connect(lambda: table_collocation.update_filters())

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_apply_to, 0, 0, 1, 4)
    group_box_filter_settings.layout().addWidget(combo_box_apply_to, 1, 0, 1, 4)

    group_box_filter_settings.layout().addWidget(label_freq_left, 2, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_left_no_limit, 2, 3)
    group_box_filter_settings.layout().addWidget(label_freq_left_min, 3, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_left_min, 3, 1)
    group_box_filter_settings.layout().addWidget(label_freq_left_max, 3, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_left_max, 3, 3)

    group_box_filter_settings.layout().addWidget(label_freq_right, 4, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_right_no_limit, 4, 3)
    group_box_filter_settings.layout().addWidget(label_freq_right_min, 5, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_right_min, 5, 1)
    group_box_filter_settings.layout().addWidget(label_freq_right_max, 5, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_right_max, 5, 3)

    group_box_filter_settings.layout().addWidget(label_score_left, 6, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_score_left_no_limit, 6, 3)
    group_box_filter_settings.layout().addWidget(label_score_left_min, 7, 0)
    group_box_filter_settings.layout().addWidget(spin_box_score_left_min, 7, 1)
    group_box_filter_settings.layout().addWidget(label_score_left_max, 7, 2)
    group_box_filter_settings.layout().addWidget(spin_box_score_left_max, 7, 3)

    group_box_filter_settings.layout().addWidget(label_score_right, 8, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_score_right_no_limit, 8, 3)
    group_box_filter_settings.layout().addWidget(label_score_right_min, 9, 0)
    group_box_filter_settings.layout().addWidget(spin_box_score_right_min, 9, 1)
    group_box_filter_settings.layout().addWidget(label_score_right_max, 9, 2)
    group_box_filter_settings.layout().addWidget(spin_box_score_right_max, 9, 3)

    group_box_filter_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 10, 0, 1, 4)

    group_box_filter_settings.layout().addWidget(label_len, 11, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_len_no_limit, 11, 3)
    group_box_filter_settings.layout().addWidget(label_len_min, 12, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_min, 12, 1)
    group_box_filter_settings.layout().addWidget(label_len_max, 12, 2)
    group_box_filter_settings.layout().addWidget(spin_box_len_max, 12, 3)

    group_box_filter_settings.layout().addWidget(label_files, 13, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_files_no_limit, 13, 3)
    group_box_filter_settings.layout().addWidget(label_files_min, 14, 0)
    group_box_filter_settings.layout().addWidget(spin_box_files_min, 14, 1)
    group_box_filter_settings.layout().addWidget(label_files_max, 14, 2)
    group_box_filter_settings.layout().addWidget(spin_box_files_max, 14, 3)

    group_box_filter_settings.layout().addWidget(button_filter_results, 15, 0, 1, 4)

    tab_collocation.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_collocation.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    load_settings()

    return tab_collocation

def generate_collocates(main, files):
    def filter_distribution(distribution):
        if settings['words']:
            if not settings['treat_as_lowercase']:
                if not settings['lowercase']:
                    distribution = {collocate: vals
                                    for collocate, vals in distribution.items()
                                    if not collocate[1].islower()}
                if not settings['uppercase']:
                    distribution = {collocate: vals
                                    for collocate, vals in distribution.items()
                                    if not collocate[1].isupper()}
                if not settings['title_case']:
                    distribution = {collocate: vals
                                    for collocate, vals in distribution.items()
                                    if not collocate[1].istitle()}

            if settings['filter_stop_words']:
                tokens_filtered = wordless_text.wordless_filter_stop_words(main,
                                                                           [collocate[1] for collocate in distribution.keys()],
                                                                           text.lang_code)

                distribution = {collocate: vals
                                for collocate, vals in distribution.items()
                                if collocate[1] in tokens_filtered}
        else:
            distribution = {collocate: vals
                            for collocate, vals in distribution.items()
                            if all([not char.isalpha() for char in collocate[1]])}
        
        if not settings['nums']:
            distribution = {collocate: vals
                            for collocate, vals in distribution.items()
                            if not collocate[1].isnumeric()}

        if not settings['show_all']:
            distribution = {collocate: vals
                            for collocate, vals in distribution.items()
                            if collocate[0] in search_terms_files}

        return distribution

    freq_distributions = []
    score_distributions = []
    search_terms_files = set()
    tokens_files = []

    settings = main.settings_custom['collocation']

    if settings['window_left'] < 0 and settings['window_right'] > 0:
        window_size_left = abs(settings['window_left'])
        window_size_right = abs(settings['window_right'])
    elif settings['window_left'] > 0 and settings['window_right'] > 0:
        window_size_left = 0
        window_size_right = settings['window_right'] - settings['window_left'] + 1
    elif settings['window_left'] < 0 and settings['window_right'] < 0:
        window_size_left = settings['window_right'] - settings['window_left'] + 1
        window_size_right = 0
    window_size = window_size_left + window_size_right

    assoc_measure = main.settings_global['assoc_measures'][settings['assoc_measure']]

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(main, file)

        if settings['words']:
            if settings['treat_as_lowercase']:
                text.tokens = [token.lower() for token in text.tokens]

            if settings['lemmatize']:
                text.tokens = wordless_text.wordless_lemmatize(main, text.tokens, text.lang_code)

        if not settings['puncs']:
            text.tokens = [token for token in text.tokens if token.isalnum()]

        if not settings['show_all']:
            if settings['multi_search_mode']:
                search_terms = settings['search_terms']
            else:
                search_terms = [settings['search_term']]

            search_terms_files |= text.match_tokens(search_terms,
                                                    settings['ignore_case'],
                                                    settings['match_inflected_forms'],
                                                    settings['match_whole_word'],
                                                    settings['use_regex'])

        tokens_files.append(text.tokens)
    tokens_files.append([token for tokens in tokens_files for token in tokens])

    # Frequency distribution
    for tokens in tokens_files[:-1]:
        freq_distribution = {}

        if tokens:
            if window_size_right:
                for ngram in nltk.ngrams(tokens, window_size_right + 1, pad_right = True):
                    w1 = ngram[0]

                    for i, w2 in enumerate(ngram[1:]):
                        if w2 is not None:
                            if (w1, w2) not in freq_distribution:
                                freq_distribution[(w1, w2)] = [0] * window_size

                            freq_distribution[(w1, w2)][window_size_left + i] += 1

            if window_size_left:
                for ngram in nltk.ngrams(tokens, window_size_left + 1, pad_right = True):
                    w1 = ngram[0]

                    for i, w2 in enumerate(ngram[1:]):
                        if w2 is not None:
                            if (w2, w1) not in freq_distribution:
                                freq_distribution[(w2, w1)] = [0] * window_size

                            freq_distribution[(w2, w1)][window_size_left - 1 - i] += 1

        freq_distributions.append(filter_distribution(freq_distribution))

    # Score distribution
    for tokens in tokens_files:
        score_distribution = {}

        if tokens:
            if window_size_right:
                finder_right = nltk.collocations.BigramCollocationFinder.from_words(tokens, window_size = window_size_right + 1)

                for collocate, score in finder_right.score_ngrams(assoc_measure):
                    if collocate not in score_distribution:
                        score_distribution[collocate] = [0, 0]

                    score_distribution[collocate][1] = score

            if window_size_left:
                finder_left = nltk.collocations.BigramCollocationFinder.from_words(tokens, window_size = window_size_left + 1)

                for collocate, score in finder_left.score_ngrams(assoc_measure):
                    collocate_reversed = tuple(reversed(collocate))

                    if collocate_reversed not in score_distribution:
                        score_distribution[collocate_reversed] = [0, 0]

                    score_distribution[collocate_reversed][0] = score

        score_distributions.append(filter_distribution(score_distribution))

    return wordless_misc.merge_dicts(freq_distributions), wordless_misc.merge_dicts(score_distributions)

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['collocation']
    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            if settings['window_left'] < 0 and settings['window_right'] > 0:
                window_size_left = abs(settings['window_left'])
                window_size_right = abs(settings['window_right'])
            elif settings['window_left'] > 0 and settings['window_right'] > 0:
                window_size_left = 0
                window_size_right = settings['window_right'] - settings['window_left'] + 1
            elif settings['window_left'] < 0 and settings['window_right'] < 0:
                window_size_left = settings['window_right'] - settings['window_left'] + 1
                window_size_right = 0
            window_size = window_size_left + window_size_right

            freq_distribution, score_distribution = generate_collocates(main, files)

            if freq_distribution:
                table.clear_table()

                table.settings = main.settings_custom

                # Insert columns
                for i, file in enumerate(files):
                    for i in range(settings['window_left'], settings['window_right'] + 1):
                        if i < 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}]\nL{-i}'),
                                             num = True, pct = True, cumulative = True, breakdown = True)
                        elif i > 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}]\nR{i}'),
                                             num = True, pct = True, cumulative = True, breakdown = True)

                        table.cols_breakdown_position.add(table.columnCount() - 2)

                    if window_size_left:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\nFrequency/L'),
                                         num = True, pct = True, cumulative = True, breakdown = True)
                    if window_size_right:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\nFrequency/R'),
                                         num = True, pct = True, cumulative = True, breakdown = True)
                    if window_size_left:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\nScore/L'),
                                         num = True, breakdown = True)
                    if window_size_right:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}]\nScore/R'),
                                         num = True, breakdown = True)

                for i in range(settings['window_left'], settings['window_right'] + 1):
                    if i < 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total\nL{-i}'),
                                         num = True, pct = True, cumulative = True)
                    elif i > 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total\nR{i}'),
                                         num = True, pct = True, cumulative = True)

                    table.cols_breakdown_position.add(table.columnCount() - 2)

                if window_size_left:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total\nFrequency/L'),
                                     num = True, pct = True, cumulative = True)
                if window_size_right:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total\nFrequency/R'),
                                     num = True, pct = True, cumulative = True)
                if window_size_left:
                    table.insert_col(table.columnCount() - 1, main.tr(f'Total\nScore/L'),
                                     num = True)
                if window_size_right:
                    table.insert_col(table.columnCount() - 1, main.tr(f'Total\nScore/R'),
                                     num = True)

                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\nScore/R')), Qt.DescendingOrder)

                cols_freq = table.find_col([main.tr(f'[{file["name"]}]') for file in files], fuzzy_matching = True)
                cols_freq_left = table.find_col([main.tr(f'[{file["name"]}]\nFrequency/L') for file in files])
                cols_freq_right = table.find_col([main.tr(f'[{file["name"]}]\nFrequency/R') for file in files])
                cols_score_left = table.find_col([main.tr(f'[{file["name"]}]\nScore/L') for file in files])
                cols_score_right = table.find_col([main.tr(f'[{file["name"]}]\nScore/R') for file in files])
                cols_freq_total = table.find_cols(main.tr('Total'))
                col_total_freq_left = table.find_col(main.tr('Total\nFrequency/L'))
                col_total_freq_right = table.find_col(main.tr('Total\nFrequency/R'))
                col_total_score_left = table.find_col(main.tr('Total\nScore/L'))
                col_total_score_right = table.find_col(main.tr('Total\nScore/R'))
                col_files_found = table.find_col(main.tr('Files Found'))

                len_files = len(files)

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

                table.setRowCount(len(freq_distribution))

                for i, ((keyword, collocate), scores) in enumerate(sorted(score_distribution.items(),
                                                                          key = wordless_misc.multi_sorting_score)):
                    # Rank
                    table.set_item_num_int(i, 0, -1)

                    # Keywords
                    table.setItem(i, 1, wordless_table.Wordless_Table_Item(keyword))
                    # Collocates
                    table.setItem(i, 2, wordless_table.Wordless_Table_Item(collocate))

                    # Score
                    for j, (score_left, score_right) in enumerate(scores[:-1]):
                        if window_size_left:
                            table.set_item_num_float(i, cols_score_left[j], score_left)
                        if window_size_right:
                            table.set_item_num_float(i, cols_score_right[j], score_right)

                    # Total Score
                    if window_size_left:
                        table.set_item_num_float(i, col_total_score_left, scores[-1][0])
                    if window_size_right:
                        table.set_item_num_float(i, col_total_score_right, scores[-1][1])

                for i in range(table.rowCount()):
                    freq_files_positions = freq_distribution[(table.item(i, 1).text(), table.item(i, 2).text())]
                    freq_files = numpy.array(freq_files_positions).sum(axis = 1)
                    freq_positions = numpy.array(freq_files_positions).sum(axis = 0)

                    # Frequency
                    for j, freq_file_positions in enumerate(freq_files_positions):
                        for k, freq in enumerate(freq_file_positions):
                            table.set_item_num_cumulative(i, cols_freq[j] + k, freq)

                        if window_size_left:
                            table.set_item_num_cumulative(i, cols_freq_left[j],
                                                          sum(freq_positions[:window_size_left]))
                        if window_size_right:
                            table.set_item_num_cumulative(i, cols_freq_right[j],
                                                          sum(freq_positions[-window_size_right:]))

                    # Total Frequency
                    for j, freq_position in enumerate(freq_positions):
                        table.set_item_num_cumulative(i, cols_freq_total[j], freq_position)

                    if window_size_left:
                        table.set_item_num_cumulative(i, col_total_freq_left,
                                                      sum(freq_positions[:window_size_left]))
                    if window_size_right:
                        table.set_item_num_cumulative(i, col_total_freq_right,
                                                      sum(freq_positions[-window_size_right:]))

                    # Files Found
                    table.set_item_num_pct(i, col_files_found,
                                           len([freq_file for freq_file in freq_files if freq_file]),
                                           len_files)

                table.blockSignals(False)
                table.setSortingEnabled(True)
                table.setUpdatesEnabled(True)

                table.toggle_pct()
                table.toggle_cumulative()
                table.toggle_breakdown()
                table.update_ranks()

                table.update_items_width()

                table.item_changed()
            else:
                wordless_dialog.wordless_message_no_results_table(main)
        else:
            wordless_dialog.wordless_message_empty_search_term(main)

    main.status_bar.showMessage(main.tr('Data generation completed!'))

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['collocation']

    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            if settings['window_left'] < 0 and settings['window_right'] > 0:
                window_size_left = abs(settings['window_left'])
                window_size_right = abs(settings['window_right'])
            elif settings['window_left'] > 0 and settings['window_right'] > 0:
                window_size_left = 0
                window_size_right = settings['window_right'] - settings['window_left'] + 1
            elif settings['window_left'] < 0 and settings['window_right'] < 0:
                window_size_left = settings['window_right'] - settings['window_left'] + 1
                window_size_right = 0

            freq_distribution, score_distribution = generate_collocates(main, files)

            if settings['use_data'].find(main.tr('Frequency')) > - 1 and freq_distribution:
                if settings['use_data'] == main.tr('Frequency (Left)'):
                    freq_distribution = {collocate: numpy.array(freqs)[:, :window_size_left].sum(axis = 1) for collocate, freqs in freq_distribution.items()}
                elif settings['use_data'] == main.tr('Frequency (Right)'):
                    freq_distribution = {collocate: numpy.array(freqs)[:, -window_size_right:].sum(axis = 1) for collocate, freqs in freq_distribution.items()}
                else:
                    dist = int(re.findall(r'[0-9]+', settings['use_data'])[0])

                    if settings['use_data'].find('(L') > -1:
                        freq_distribution = {collocate: numpy.array(freqs)[:, -dist - settings['window_left']] for collocate, freqs in freq_distribution.items()}
                    else:
                        freq_distribution = {collocate: numpy.array(freqs)[:, dist - settings['window_left'] - 1] for collocate, freqs in freq_distribution.items()}

                wordless_plot.wordless_plot_freq(main, freq_distribution,
                                                 rank_min = settings['rank_min'],
                                                 rank_max = settings['rank_max'],
                                                 use_pct = settings['use_pct'],
                                                 use_cumulative = settings['use_cumulative'],
                                                 label_x = main.tr('Collocates'))
            elif settings['use_data'].find(main.tr('Score')) > - 1 and score_distribution:
                if settings['use_data'] == main.tr('Score (Left)'):
                    score_distribution = {collocate: numpy.array(scores)[:, 0] for collocate, scores in score_distribution.items()}
                else:
                    score_distribution = {collocate: numpy.array(scores)[:, 1] for collocate, scores in score_distribution.items()}

                wordless_plot.wordless_plot_score(main, score_distribution,
                                                  rank_min = settings['rank_min'],
                                                  rank_max = settings['rank_max'],
                                                  label_x = main.tr('Collocates'))
            else:
                wordless_dialog.wordless_message_no_results_plot(main)
        else:
            wordless_dialog.wordless_message_empty_search_term(main)

    main.status_bar.showMessage(main.tr('Plot generation completed!'))
