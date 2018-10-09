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
import nltk

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Collocation(wordless_table.Wordless_Table):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Keywords'),
                             main.tr('Collocates'),
                             main.tr('Files Found'),
                         ],
                         cols_pct = [
                             main.tr('Files Found')
                         ],
                         sorting_enabled = True)

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

    @ wordless_misc.log_timing('Filtering')
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['collocation']

            if settings['apply_to'] == self.tr('Total'):
                col_freq_left = self.find_col(self.tr('Total Freq/L'))
                col_freq_right = self.find_col(self.tr('Total Freq/R'))
                col_score_left = self.find_col(self.tr('Total Score/L'))
                col_score_right = self.find_col(self.tr('Total Score/R'))
            else:
                col_freq_left = self.find_col(self.tr(f'[{settings["freq_left_apply_to"]}] Freq/L'))
                col_freq_right = self.find_col(self.tr(f'[{settings["freq_right_apply_to"]}] Freq/R'))
                col_score_left = self.find_col(self.tr(f'[{settings["score_left_apply_to"]}] Score/L'))
                col_score_right = self.find_col(self.tr(f'[{settings["score_right_apply_to"]}] Score/R'))

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

            self.row_filters = [{} for i in range(self.rowCount())]

            for i in range(self.rowCount()):
                if freq_left_min <= self.item(i, col_freq_left).val_raw <= freq_left_max:
                    self.row_filters[i][self.tr('Freq/L')] = True
                else:
                    self.row_filters[i][self.tr('Freq/L')] = False
                if freq_right_min <= self.item(i, col_freq_right).val_raw <= freq_right_max:
                    self.row_filters[i][self.tr('Freq/R')] = True
                else:
                    self.row_filters[i][self.tr('Freq/R')] = False

                if score_left_min <= self.item(i, col_score_left).val <= score_left_max:
                    self.row_filters[i][self.tr('Score/L')] = True
                else:
                    self.row_filters[i][self.tr('Score/L')] = False
                if score_right_min <= self.item(i, col_score_right).val <= score_right_max:
                    self.row_filters[i][self.tr('Score/R')] = True
                else:
                    self.row_filters[i][self.tr('Score/R')] = False

                if len_min <= len(self.item(i, col_collocates).text().replace(' ', '')) <= len_max:
                    self.row_filters[i][self.tr('Collocates')] = True
                else:
                    self.row_filters[i][self.tr('Collocates')] = False

                if files_min <= self.item(i, col_files_found).val_raw <= files_max:
                    self.row_filters[i][self.tr('Files Found')] = True
                else:
                    self.row_filters[i][self.tr('Files Found')] = False

            self.filter_table()

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

        line_edit_search_term.setText(settings_loaded['search_term'])
        list_search_terms.clear()
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

        checkbox_rank_no_limit.setChecked(settings_loaded['rank_no_limit'])
        spin_box_rank_min.setValue(settings_loaded['rank_min'])
        spin_box_rank_max.setValue(settings_loaded['rank_max'])
        
        checkbox_use_pct.setChecked(settings_loaded['use_pct'])
        checkbox_use_cumulative.setChecked(settings_loaded['use_cumulative'])

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

        combo_box_apply_to.setCurrentText(settings_loaded['apply_to'])

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

        if main.settings_custom['collocation']['show_all']:
            table_collocation.button_generate_data.setText(main.tr('Generate Collocates'))
        else:
            table_collocation.button_generate_data.setText(main.tr('Search Collocates'))

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

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown_position'] = checkbox_show_breakdown_position.isChecked()
        settings['show_breakdown_file'] = checkbox_show_breakdown_file.isChecked()

    def plot_settings_changed():
        settings['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_max'] = spin_box_rank_max.value()

        settings['use_pct'] = checkbox_use_pct.isChecked()
        settings['use_cumulative'] = checkbox_use_cumulative.isChecked()

    def filter_settings_changed():
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

        settings['apply_to'] = combo_box_apply_to.currentText()

        settings['len_no_limit'] = checkbox_len_no_limit.isChecked()
        settings['len_min'] = spin_box_len_min.value()
        settings['len_max'] = spin_box_len_max.value()

        settings['files_no_limit'] = checkbox_files_no_limit.isChecked()
        settings['files_min'] = spin_box_files_min.value()
        settings['files_max'] = spin_box_files_max.value()

    settings = main.settings_custom['collocation']

    tab_collocation = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_collocation = Wordless_Table_Collocation(main)

    table_collocation.button_generate_data = QPushButton(main.tr('Generate Collocates'), main)
    table_collocation.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

    table_collocation.button_generate_data.clicked.connect(lambda: generate_data(main, table_collocation))
    table_collocation.button_generate_plot.clicked.connect(lambda: generate_plot(main))

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

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_collocation.button_generate_data.click)
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
    group_box_search_settings.layout().addLayout(layout_show_all, 0, 0, 1, 4)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 4)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 4)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 3, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 4, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 5, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 6, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_multi_search_mode, 7, 0, 1, 4)

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

    label_rank = QLabel(main.tr('Rank:'), main)
    (checkbox_rank_no_limit,
     label_rank_min,
     spin_box_rank_min,
     label_rank_max,
     spin_box_rank_max) = wordless_widgets.wordless_widgets_filter(main, 1, 10000)
    
    checkbox_use_pct = QCheckBox(main.tr('Use Percentage Data'), main)
    checkbox_use_cumulative = QCheckBox(main.tr('Use Cumulative Data'), main)

    checkbox_rank_no_limit.stateChanged.connect(plot_settings_changed)
    spin_box_rank_min.valueChanged.connect(plot_settings_changed)
    spin_box_rank_max.valueChanged.connect(plot_settings_changed)
    
    checkbox_use_pct.stateChanged.connect(plot_settings_changed)
    checkbox_use_cumulative.stateChanged.connect(plot_settings_changed)

    group_box_plot_settings.setLayout(QGridLayout())
    group_box_plot_settings.layout().addWidget(label_rank, 0, 0, 1, 3)
    group_box_plot_settings.layout().addWidget(checkbox_rank_no_limit, 0, 3)
    group_box_plot_settings.layout().addWidget(label_rank_min, 1, 0)
    group_box_plot_settings.layout().addWidget(spin_box_rank_min, 1, 1)
    group_box_plot_settings.layout().addWidget(label_rank_max, 1, 2)
    group_box_plot_settings.layout().addWidget(spin_box_rank_max, 1, 3)
    
    group_box_plot_settings.layout().addWidget(checkbox_use_pct, 2, 0, 1, 4)
    group_box_plot_settings.layout().addWidget(checkbox_use_cumulative, 3, 0, 1, 4)

    # Filter Settings
    group_box_filter_settings = QGroupBox(main.tr('Filter Settings'), main)

    label_freq_left = QLabel(main.tr('Frequency (Left):'), main)
    (checkbox_freq_left_no_limit,
     label_freq_left_min,
     spin_box_freq_left_min,
     label_freq_left_max,
     spin_box_freq_left_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                        filter_min = 0,
                                                                        filter_max = 10000,
                                                                        table = table_collocation,
                                                                        col = main.tr('Freq/L'))

    label_freq_right = QLabel(main.tr('Frequency (Right):'), main)
    (checkbox_freq_right_no_limit,
     label_freq_right_min,
     spin_box_freq_right_min,
     label_freq_right_max,
     spin_box_freq_right_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                         filter_min = 0,
                                                                         filter_max = 10000,
                                                                         table = table_collocation,
                                                                         col = main.tr('Freq/R'))

    label_score_left = QLabel(main.tr('Score (Left):'), main)
    (checkbox_score_left_no_limit,
     label_score_left_min,
     spin_box_score_left_min,
     label_score_left_max,
     spin_box_score_left_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                         filter_min = 0,
                                                                         filter_max = 10000,
                                                                         table = table_collocation,
                                                                         col = main.tr('Score/L'))

    label_score_right = QLabel(main.tr('Score (Right):'), main)
    (checkbox_score_right_no_limit,
     label_score_right_min,
     spin_box_score_right_min,
     label_score_right_max,
     spin_box_score_right_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                          filter_min = 0,
                                                                          filter_max = 10000,
                                                                          table = table_collocation,
                                                                          col = main.tr('Score/R'))

    label_apply_to = QLabel(main.tr('Apply to:'), main)
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_collocation)
    separator_filter_settings = wordless_layout.Wordless_Separator(main)

    label_len = QLabel(main.tr('N-gram Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                  table = table_collocation,
                                                                  col = main.tr('Collocates'))

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main,
                                                                    filter_min = 1,
                                                                    filter_max = 1000,
                                                                    table = table_collocation,
                                                                    col = main.tr('Files Found'))

    button_filter_results = QPushButton(main.tr('Filter Results'), main)

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

    combo_box_apply_to.currentTextChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.valueChanged.connect(filter_settings_changed)
    spin_box_len_max.valueChanged.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.valueChanged.connect(filter_settings_changed)
    spin_box_files_max.valueChanged.connect(filter_settings_changed)

    button_filter_results.clicked.connect(lambda: table_collocation.update_filters())

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_freq_left, 0, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_left_no_limit, 0, 3)
    group_box_filter_settings.layout().addWidget(label_freq_left_min, 1, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_left_min, 1, 1)
    group_box_filter_settings.layout().addWidget(label_freq_left_max, 1, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_left_max, 1, 3)

    group_box_filter_settings.layout().addWidget(label_freq_right, 2, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_right_no_limit, 2, 3)
    group_box_filter_settings.layout().addWidget(label_freq_right_min, 3, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_right_min, 3, 1)
    group_box_filter_settings.layout().addWidget(label_freq_right_max, 3, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_right_max, 3, 3)

    group_box_filter_settings.layout().addWidget(label_score_left, 4, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_score_left_no_limit, 4, 3)
    group_box_filter_settings.layout().addWidget(label_score_left_min, 5, 0)
    group_box_filter_settings.layout().addWidget(spin_box_score_left_min, 5, 1)
    group_box_filter_settings.layout().addWidget(label_score_left_max, 5, 2)
    group_box_filter_settings.layout().addWidget(spin_box_score_left_max, 5, 3)

    group_box_filter_settings.layout().addWidget(label_score_right, 6, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_score_right_no_limit, 6, 3)
    group_box_filter_settings.layout().addWidget(label_score_right_min, 7, 0)
    group_box_filter_settings.layout().addWidget(spin_box_score_right_min, 7, 1)
    group_box_filter_settings.layout().addWidget(label_score_right_max, 7, 2)
    group_box_filter_settings.layout().addWidget(spin_box_score_right_max, 7, 3)

    group_box_filter_settings.layout().addWidget(label_apply_to, 8, 0)
    group_box_filter_settings.layout().addWidget(combo_box_apply_to, 8, 1, 1, 3)
    group_box_filter_settings.layout().addWidget(separator_filter_settings, 9, 0, 1, 4)

    group_box_filter_settings.layout().addWidget(label_len, 10, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_len_no_limit, 10, 3)
    group_box_filter_settings.layout().addWidget(label_len_min, 11, 0)
    group_box_filter_settings.layout().addWidget(spin_box_len_min, 11, 1)
    group_box_filter_settings.layout().addWidget(label_len_max, 11, 2)
    group_box_filter_settings.layout().addWidget(spin_box_len_max, 11, 3)

    group_box_filter_settings.layout().addWidget(label_files, 12, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_files_no_limit, 12, 3)
    group_box_filter_settings.layout().addWidget(label_files_min, 13, 0)
    group_box_filter_settings.layout().addWidget(spin_box_files_min, 13, 1)
    group_box_filter_settings.layout().addWidget(label_files_max, 13, 2)
    group_box_filter_settings.layout().addWidget(spin_box_files_max, 13, 3)

    group_box_filter_settings.layout().addWidget(button_filter_results, 14, 0, 1, 4)

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
                                                                           text.lang)

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
                            if collocate[0] in search_terms_total}

        return distribution

    freq_distributions = []
    score_distributions = []
    search_terms_total = set()
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

        tokens = text.tokens.copy()

        if settings['words']:
            if settings['treat_as_lowercase']:
                tokens = [token.lower() for token in tokens]

            if settings['lemmatize']:
                tokens = wordless_text.wordless_lemmatize(main, tokens, text.lang)

        if not settings['puncs']:
            tokens = [token for token in tokens if token.isalnum()]

        if not settings['show_all']:
            if settings['multi_search_mode']:
                search_terms = settings['search_terms']
            else:
                if settings['search_term']:
                    search_terms = [settings['search_term']]
                else:
                    search_terms = []

            search_terms_total |= text.match_tokens(search_terms,
                                                    settings['ignore_case'],
                                                    settings['match_inflected_forms'],
                                                    settings['match_whole_word'],
                                                    settings['use_regex'])

        tokens_files.append(tokens)
    tokens_files.append([token for tokens in tokens_files for token in tokens])

    # Frequency distribution
    for tokens in tokens_files[:-1]:
        freq_distribution = {}

        for ngram in nltk.ngrams(tokens, abs(settings['window_right']) + 1, pad_right = True):
            w1 = ngram[0]

            for i, w2 in enumerate(ngram[1:]):
                if w2 is not None:
                    if (w1, w2) not in freq_distribution:
                        freq_distribution[(w1, w2)] = [0] * window_size

                    freq_distribution[(w1, w2)][window_size_left + i] += 1

        for ngram in nltk.ngrams(tokens, abs(settings['window_left']) + 1, pad_right = True):
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

        finder_left = nltk.collocations.BigramCollocationFinder.from_words(tokens, window_size = abs(settings['window_left']) + 1)
        finder_right = nltk.collocations.BigramCollocationFinder.from_words(tokens, window_size = abs(settings['window_right']) + 1)

        for collocate, score in finder_right.score_ngrams(assoc_measure):
            if collocate not in score_distribution:
                score_distribution[collocate] = [0, 0]

            score_distribution[collocate][1] = score

        for collocate, score in finder_left.score_ngrams(assoc_measure):
            collocate_reversed = tuple(reversed(collocate))

            if collocate_reversed not in score_distribution:
                score_distribution[collocate_reversed] = [0, 0]

            score_distribution[collocate_reversed][0] = score

        if not settings['show_all']:
            score_distribution = {collocate: scores
                                  for collocate, scores in score_distribution.items()
                                  if collocate[0] in search_terms_total}

        score_distributions.append(filter_distribution(score_distribution))

    return wordless_misc.merge_dicts(freq_distributions), wordless_misc.merge_dicts(score_distributions)

@ wordless_misc.log_timing('Data generation completed')
def generate_data(main, table):
    settings = main.settings_custom['collocation']
    files = main.wordless_files.selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            table.files = files

            window_left = True if settings['window_left'] < 0 else False
            window_right = True if settings['window_right'] > 0 else False

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

                table.files = files

                # Insert columns
                for i, file in enumerate(files):
                    for i in range(settings['window_left'], settings['window_right'] + 1):
                        if i < 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}] L{-i}'),
                                             pct = True, cumulative = True, breakdown = True)
                        elif i > 0:
                            table.insert_col(table.columnCount() - 1,
                                             main.tr(f'[{file["name"]}] R{i}'),
                                             pct = True, cumulative = True, breakdown = True)

                        table.cols_breakdown_position.add(table.columnCount() - 2)

                    if window_left:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Freq/L'),
                                         pct = True, cumulative = True, breakdown = True)
                    if window_right:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Freq/R'),
                                         pct = True, cumulative = True, breakdown = True)
                    if window_left:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Score/L'),
                                         breakdown = True)
                    if window_right:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'[{file["name"]}] Score/R'),
                                         breakdown = True)

                for i in range(settings['window_left'], settings['window_right'] + 1):
                    if i < 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total L{-i}'),
                                         pct = True, cumulative = True)
                    elif i > 0:
                        table.insert_col(table.columnCount() - 1,
                                         main.tr(f'Total R{i}'),
                                         pct = True, cumulative = True)

                    table.cols_breakdown_position.add(table.columnCount() - 2)

                if window_left:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total Freq/L'),
                                     pct = True, cumulative = True)
                if window_right:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'Total Freq/R'),
                                     pct = True, cumulative = True)
                if window_left:
                    table.insert_col(table.columnCount() - 1, main.tr(f'Total Score/L'))
                if window_right:
                    table.insert_col(table.columnCount() - 1, main.tr(f'Total Score/R'))

                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}] Score/R')), Qt.DescendingOrder)

                col_keywords = table.find_col(main.tr('Keywords'))
                col_collocates = table.find_col(main.tr('Collocates'))
                cols_freq = table.find_col([main.tr(f'[{file["name"]}]') for file in files], fuzzy_matching = True)
                cols_freq_left = table.find_col([main.tr(f'[{file["name"]}] Freq/L') for file in files])
                cols_freq_right = table.find_col([main.tr(f'[{file["name"]}] Freq/R') for file in files])
                cols_score_left = table.find_col([main.tr(f'[{file["name"]}] Score/L') for file in files])
                cols_score_right = table.find_col([main.tr(f'[{file["name"]}] Score/R') for file in files])
                cols_freq_total = table.find_cols(main.tr('Total'))
                col_total_freq_left = table.find_col(main.tr('Total Freq/L'))
                col_total_freq_right = table.find_col(main.tr('Total Freq/R'))
                col_total_score_left = table.find_col(main.tr('Total Score/L'))
                col_total_score_right = table.find_col(main.tr('Total Score/R'))
                col_files_found = table.find_col(main.tr('Files Found'))

                total_freqs_positions = [[sum(freqs_position) for freqs_position in zip(*freqs)] for freqs in zip(*freq_distribution.values())]
                total_freqs = [sum(total_freqs) for total_freqs in zip(*total_freqs_positions)]
                total_freq_left = sum(total_freqs[:window_size_left])
                total_freq_right = sum(total_freqs[window_size_right:])
                total_freq = total_freq_left + total_freq_right

                score_max = [[max(scores_direction) for scores_direction in zip(*scores)] for scores in zip(*score_distribution.values())]
                score_max_left = list(zip(*score_max))[0]
                score_max_right = list(zip(*score_max))[1]

                len_files = len(files)

                table.blockSignals(True)
                table.setSortingEnabled(False)
                table.setUpdatesEnabled(False)

                table.setRowCount(len(freq_distribution))

                for i, ((keyword, collocate), scores) in enumerate(sorted(score_distribution.items(), key = wordless_misc.multi_sorting)):
                    # Rank
                    table.setItem(i, 0, wordless_table.Wordless_Table_Item())

                    # Keywords
                    table.setItem(i, 1, wordless_table.Wordless_Table_Item(keyword))
                    # Collocates
                    table.setItem(i, 2, wordless_table.Wordless_Table_Item(collocate))

                    # Score
                    for j, (score_left, score_right) in enumerate(scores[:-1]):
                        if window_left:
                            table.set_item_num(i, cols_score_left[j], score_left, score_max_left[j])
                        if window_right:
                            table.set_item_num(i, cols_score_right[j], score_right, score_max_right[j])

                    # Total Score
                    table.set_item_num(i, col_total_score_left, scores[-1][0], score_max_left[-1])
                    table.set_item_num(i, col_total_score_right, scores[-1][1], score_max_right[-1])

                for i in range(table.rowCount()):
                    freqs = freq_distribution[(table.item(i, col_keywords).text(), table.item(i, col_collocates).text())]
                    total_freq_positions = [sum(freqs_position) for freqs_position in zip(*freqs)]

                    # Frequency
                    for j, freq_positions in enumerate(freqs):
                        for k, freq_position in enumerate(freq_positions):
                            table.set_item_pct(i, cols_freq[j] + k, freq_position, total_freqs_positions[j][k])

                        if window_left:
                            table.set_item_pct(i, cols_freq_left[j],
                                               sum(freq_positions[:window_size_left]),
                                               sum(total_freqs_positions[j][:window_size_left]))
                        if window_right:
                            table.set_item_pct(i, cols_freq_right[j],
                                               sum(freq_positions[-window_size_right:]),
                                               sum(total_freqs_positions[j][-window_size_right:]))

                    # Total Frequency
                    for j, total_freq in enumerate(total_freq_positions):
                        table.set_item_pct(i, cols_freq_total[j], total_freq, total_freqs[j])

                    if window_left:
                        table.set_item_pct(i, col_total_freq_left,
                                           sum(total_freq_positions[:window_size_left]),
                                           total_freq_left)
                    if window_right:
                        table.set_item_pct(i, col_total_freq_right,
                                           sum(total_freq_positions[window_size_right:]),
                                           total_freq_right)

                    # Files Found
                    table.set_item_pct(i, col_files_found,
                                       len([freqs_position for freqs_position in freqs if any(freqs_position)]), len_files)

                table.blockSignals(False)
                table.setSortingEnabled(True)
                table.setUpdatesEnabled(True)

                table.update_ranks()
                table.toggle_cumulative()
                table.toggle_breakdown()
            else:
                wordless_message.empty_results_table(main)
        else:
            wordless_message.empty_search_term(main)

@ wordless_misc.log_timing('Plot generation completed')
def generate_plot(main):
    pass