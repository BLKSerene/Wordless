#
# Wordless: Keywords
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import collections
import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Keywords(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('Keywords'),
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
                                                               tab = 'keywords',
                                                               table = self,
                                                               cols_search = [self.tr('Keywords')])

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(main.tr('Generate Table'), main)
        self.button_generate_plot = QPushButton(main.tr('Generate Plot'), main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['keywords']

            (col_text_test_stats,
             col_text_p_value) = self.main.settings_global['significance_tests'][settings['significance_test']]['cols']
            col_text_effect_size =  self.main.settings_global['effect_size_measures'][settings['effect_size_measure']]['col']

            if settings['apply_to'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total\nFrequency'))
                col_test_stats = self.find_col(self.tr(f'Total\n{col_text_test_stats}'))
                col_p_value = self.find_col(self.tr(f'Total\n{col_text_p_value}'))
                col_effect_size = self.find_col(self.tr(f'Total\n{col_text_effect_size}'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["apply_to"]}]\nFrequency'))
                col_test_stats = self.find_col(self.tr(f'[{settings["apply_to"]}]\n{col_text_test_stats}'))
                col_p_value = self.find_col(self.tr(f'[{settings["apply_to"]}]\n{col_text_p_value}'))
                col_effect_size = self.find_col(self.tr(f'[{settings["apply_to"]}]\n{col_text_effect_size}'))

            col_keywords = self.find_col('Keywords')
            col_files_found = self.find_col('Files Found')

            freq_min = settings['freq_min']
            freq_max = settings['freq_max'] if not settings['freq_no_limit'] else float('inf')

            test_stats_min = settings['test_stats_min']
            test_stats_max = settings['test_stats_max'] if not settings['test_stats_no_limit'] else float('inf')

            p_value_min = settings['p_value_min']
            p_value_max = settings['p_value_max'] if not settings['p_value_no_limit'] else float('inf')

            effect_size_min = settings['effect_size_min']
            effect_size_max = settings['effect_size_max'] if not settings['effect_size_no_limit'] else float('inf')

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

                if col_text_test_stats:
                    if test_stats_min <= self.item(i, col_test_stats).val <= test_stats_max:
                        self.row_filters[i].append(True)
                    else:
                        self.row_filters[i].append(False)

                if col_text_p_value:
                    if p_value_min <= self.item(i, col_p_value).val <= p_value_max:
                        self.row_filters[i].append(True)
                    else:
                        self.row_filters[i].append(False)

                if effect_size_min <= self.item(i, col_effect_size).val <= effect_size_max:
                    self.row_filters[i].append(True)
                else:
                    self.row_filters[i].append(False)

                if len_min <= len(self.item(i, col_keywords).text().replace(' ', '')) <= len_max:
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
            settings_loaded = copy.deepcopy(main.settings_default['keywords'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['keywords'])

        checkbox_words.setChecked(settings_loaded['words'])
        checkbox_lowercase.setChecked(settings_loaded['lowercase'])
        checkbox_uppercase.setChecked(settings_loaded['uppercase'])
        checkbox_title_case.setChecked(settings_loaded['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings_loaded['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings_loaded['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings_loaded['filter_stop_words'])

        checkbox_nums.setChecked(settings_loaded['nums'])
        checkbox_puncs.setChecked(settings_loaded['puncs'])

        combo_box_significance_test.setCurrentText(settings_loaded['significance_test'])
        combo_box_effect_size_measure.setCurrentText(settings_loaded['effect_size_measure'])

        checkbox_show_pct.setChecked(settings_loaded['show_pct'])
        checkbox_show_cumulative.setChecked(settings_loaded['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings_loaded['show_breakdown'])

        combo_box_use_data.setCurrentText(settings_loaded['use_data'])
        checkbox_use_pct.setChecked(settings_loaded['use_pct'])
        checkbox_use_cumulative.setChecked(settings_loaded['use_cumulative'])

        checkbox_rank_no_limit.setChecked(settings_loaded['rank_no_limit'])
        spin_box_rank_min.setValue(settings_loaded['rank_min'])
        spin_box_rank_max.setValue(settings_loaded['rank_max'])

        combo_box_apply_to.setCurrentText(settings_loaded['apply_to'])

        checkbox_freq_no_limit.setChecked(settings_loaded['freq_no_limit'])
        spin_box_freq_min.setValue(settings_loaded['freq_min'])
        spin_box_freq_max.setValue(settings_loaded['freq_max'])

        checkbox_test_stats_no_limit.setChecked(settings_loaded['test_stats_no_limit'])
        spin_box_test_stats_min.setValue(settings_loaded['test_stats_min'])
        spin_box_test_stats_max.setValue(settings_loaded['test_stats_max'])

        checkbox_effect_size_no_limit.setChecked(settings_loaded['effect_size_no_limit'])
        spin_box_effect_size_min.setValue(settings_loaded['effect_size_min'])
        spin_box_effect_size_max.setValue(settings_loaded['effect_size_max'])

        checkbox_len_no_limit.setChecked(settings_loaded['len_no_limit'])
        spin_box_len_min.setValue(settings_loaded['len_min'])
        spin_box_len_max.setValue(settings_loaded['len_max'])

        checkbox_files_no_limit.setChecked(settings_loaded['files_no_limit'])
        spin_box_files_min.setValue(settings_loaded['files_min'])
        spin_box_files_max.setValue(settings_loaded['files_max'])

        token_settings_changed()
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

    def generation_settings_changed():
        ref_file_old = combo_box_ref_file.currentText()

        combo_box_ref_file.blockSignals(True)

        combo_box_ref_file.clear()
        combo_box_ref_file.addItems([file['name'] for file in main.settings_custom['file']['files_open']])

        if combo_box_ref_file.findText(ref_file_old) > -1:
            combo_box_ref_file.setCurrentIndex(combo_box_ref_file.findText(ref_file_old))

        combo_box_ref_file.blockSignals(False)

        settings['ref_file'] = combo_box_ref_file.currentText()
        settings['significance_test'] = combo_box_significance_test.currentText()
        settings['effect_size_measure'] = combo_box_effect_size_measure.currentText()

        # Use Data
        use_data_old = combo_box_use_data.currentIndex()

        combo_box_use_data.clear()

        combo_box_use_data.addItem(main.tr('Frequency'))

        for col in main.settings_global['significance_tests'][settings['significance_test']]['cols']:
            if col:
                combo_box_use_data.addItem(col)

        combo_box_use_data.addItem(main.settings_global['effect_size_measures'][settings['effect_size_measure']]['col'])

        if use_data_old > -1:
            combo_box_use_data.setCurrentIndex(use_data_old)

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
        settings['use_data'] = combo_box_use_data.currentText()
        settings['use_pct'] = checkbox_use_pct.isChecked()
        settings['use_cumulative'] = checkbox_use_cumulative.isChecked()

        settings['rank_no_limit'] = checkbox_rank_no_limit.isChecked()
        settings['rank_min'] = spin_box_rank_min.value()
        settings['rank_max'] = spin_box_rank_max.value()

        if settings['use_data'] in [main.tr('Test Statistics'), main.tr('Effect Size')]:
            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)
        else:
            checkbox_use_pct.setEnabled(True)
            checkbox_use_cumulative.setEnabled(True)

    def filter_settings_changed():
        if combo_box_apply_to.findText(settings['ref_file']) > -1:
            combo_box_apply_to.removeItem(combo_box_apply_to.findText(settings['ref_file']))

        settings['apply_to'] = combo_box_apply_to.currentText()

        settings['freq_no_limit'] = checkbox_freq_no_limit.isChecked()
        settings['freq_min'] = spin_box_freq_min.value()
        settings['freq_max'] = spin_box_freq_max.value()

        settings['test_stats_no_limit'] = checkbox_test_stats_no_limit.isChecked()
        settings['test_stats_min'] = spin_box_test_stats_min.value()
        settings['test_stats_max'] = spin_box_test_stats_max.value()

        settings['effect_size_no_limit'] = checkbox_effect_size_no_limit.isChecked()
        settings['effect_size_min'] = spin_box_effect_size_min.value()
        settings['effect_size_max'] = spin_box_effect_size_max.value()

        settings['len_no_limit'] = checkbox_len_no_limit.isChecked()
        settings['len_min'] = spin_box_len_min.value()
        settings['len_max'] = spin_box_len_max.value()

        settings['files_no_limit'] = checkbox_files_no_limit.isChecked()
        settings['files_min'] = spin_box_files_min.value()
        settings['files_max'] = spin_box_files_max.value()

    settings = main.settings_custom['keywords']

    tab_keywords = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_keywords = Wordless_Table_Keywords(main)

    tab_keywords.layout_table.addWidget(table_keywords.label_number_results, 0, 0)
    tab_keywords.layout_table.addWidget(table_keywords.button_search_results, 0, 4)
    tab_keywords.layout_table.addWidget(table_keywords, 1, 0, 1, 5)
    tab_keywords.layout_table.addWidget(table_keywords.button_generate_table, 2, 0)
    tab_keywords.layout_table.addWidget(table_keywords.button_generate_plot, 2, 1)
    tab_keywords.layout_table.addWidget(table_keywords.button_export_selected, 2, 2)
    tab_keywords.layout_table.addWidget(table_keywords.button_export_all, 2, 3)
    tab_keywords.layout_table.addWidget(table_keywords.button_clear, 2, 4)

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

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'))

    label_ref_file = QLabel(main.tr('Reference File:'), main)
    combo_box_ref_file = wordless_box.Wordless_Combo_Box(main)

    label_significance_test = QLabel(main.tr('Significance Test:'), main)
    combo_box_significance_test = wordless_box.Wordless_Combo_Box(main)
    label_effect_size_measure = QLabel(main.tr('Effect Size Measure:'), main)
    combo_box_effect_size_measure = wordless_box.Wordless_Combo_Box(main)

    combo_box_significance_test.addItems(list(main.settings_global['significance_tests'].keys())[2:4])
    combo_box_significance_test.addItem(list(main.settings_global['significance_tests'].keys())[5])
    combo_box_effect_size_measure.addItems(list(main.settings_global['effect_size_measures'].keys()))

    main.wordless_files.table.itemChanged.connect(lambda: generation_settings_changed())
    combo_box_ref_file.currentTextChanged.connect(generation_settings_changed)

    combo_box_significance_test.currentTextChanged.connect(generation_settings_changed)
    combo_box_effect_size_measure.currentTextChanged.connect(generation_settings_changed)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_ref_file, 0, 0)
    group_box_generation_settings.layout().addWidget(combo_box_ref_file, 1, 0)

    group_box_generation_settings.layout().addWidget(label_significance_test, 2, 0)
    group_box_generation_settings.layout().addWidget(combo_box_significance_test, 3, 0)
    group_box_generation_settings.layout().addWidget(label_effect_size_measure, 4, 0)
    group_box_generation_settings.layout().addWidget(combo_box_effect_size_measure, 5, 0)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table(main, table_keywords)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown, 2, 0)

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
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_keywords)

    label_freq = QLabel(main.tr('Frequency:'), main)
    (checkbox_freq_no_limit,
     label_freq_min,
     spin_box_freq_min,
     label_freq_max,
     spin_box_freq_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_test_stats = QLabel(main.tr('Test Statistics:'), main)
    (checkbox_test_stats_no_limit,
     label_test_stats_min,
     spin_box_test_stats_min,
     label_test_stats_max,
     spin_box_test_stats_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0.0, filter_max = 10000.0)

    label_p_value = QLabel(main.tr('p-value:'), main)
    (checkbox_p_value_no_limit,
     label_p_value_min,
     spin_box_p_value_min,
     label_p_value_max,
     spin_box_p_value_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0.0, filter_max = 1.0)

    label_effect_size = QLabel(main.tr('Effect Size:'), main)
    (checkbox_effect_size_no_limit,
     label_effect_size_min,
     spin_box_effect_size_min,
     label_effect_size_max,
     spin_box_effect_size_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0.0, filter_max = 10000.0)

    label_len = QLabel(main.tr('Keyword Length:'), main)
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

    checkbox_freq_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_freq_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_max.valueChanged.connect(filter_settings_changed)

    checkbox_test_stats_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_test_stats_min.valueChanged.connect(filter_settings_changed)
    spin_box_test_stats_max.valueChanged.connect(filter_settings_changed)

    checkbox_p_value_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_p_value_min.valueChanged.connect(filter_settings_changed)
    spin_box_p_value_max.valueChanged.connect(filter_settings_changed)

    checkbox_effect_size_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_effect_size_min.valueChanged.connect(filter_settings_changed)
    spin_box_effect_size_max.valueChanged.connect(filter_settings_changed)

    checkbox_len_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.valueChanged.connect(filter_settings_changed)
    spin_box_len_max.valueChanged.connect(filter_settings_changed)

    checkbox_files_no_limit.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.valueChanged.connect(filter_settings_changed)
    spin_box_files_max.valueChanged.connect(filter_settings_changed)

    button_filter_results.clicked.connect(lambda: table_keywords.update_filters())

    group_box_filter_settings.setLayout(QGridLayout())
    group_box_filter_settings.layout().addWidget(label_apply_to, 0, 0, 1, 4)
    group_box_filter_settings.layout().addWidget(combo_box_apply_to, 1, 0, 1, 4)

    group_box_filter_settings.layout().addWidget(label_freq, 2, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_freq_no_limit, 2, 3)
    group_box_filter_settings.layout().addWidget(label_freq_min, 3, 0)
    group_box_filter_settings.layout().addWidget(spin_box_freq_min, 3, 1)
    group_box_filter_settings.layout().addWidget(label_freq_max, 3, 2)
    group_box_filter_settings.layout().addWidget(spin_box_freq_max, 3, 3)

    group_box_filter_settings.layout().addWidget(label_test_stats, 4, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_test_stats_no_limit, 4, 3)
    group_box_filter_settings.layout().addWidget(label_test_stats_min, 5, 0)
    group_box_filter_settings.layout().addWidget(spin_box_test_stats_min, 5, 1)
    group_box_filter_settings.layout().addWidget(label_test_stats_max, 5, 2)
    group_box_filter_settings.layout().addWidget(spin_box_test_stats_max, 5, 3)

    group_box_filter_settings.layout().addWidget(label_p_value, 6, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_p_value_no_limit, 6, 3)
    group_box_filter_settings.layout().addWidget(label_p_value_min, 7, 0)
    group_box_filter_settings.layout().addWidget(spin_box_p_value_min, 7, 1)
    group_box_filter_settings.layout().addWidget(label_p_value_max, 7, 2)
    group_box_filter_settings.layout().addWidget(spin_box_p_value_max, 7, 3)

    group_box_filter_settings.layout().addWidget(label_effect_size, 8, 0, 1, 3)
    group_box_filter_settings.layout().addWidget(checkbox_effect_size_no_limit, 8, 3)
    group_box_filter_settings.layout().addWidget(label_effect_size_min, 9, 0)
    group_box_filter_settings.layout().addWidget(spin_box_effect_size_min, 9, 1)
    group_box_filter_settings.layout().addWidget(label_effect_size_max, 9, 2)
    group_box_filter_settings.layout().addWidget(spin_box_effect_size_max, 9, 3)

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

    tab_keywords.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_generation_settings, 1, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_table_settings, 2, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_plot_settings, 3, 0, Qt.AlignTop)
    tab_keywords.layout_settings.addWidget(group_box_filter_settings, 4, 0, Qt.AlignTop)

    load_settings()

    return tab_keywords

def generate_keywords(main, files, ref_file):
    texts = []
    keywords_freq = []
    keywords_keyness = []

    settings = main.settings_custom['keywords']

    # Frequency
    for i, file in enumerate(files + [ref_file]):
        text = wordless_text.Wordless_Text(main, file)

        if settings['words']:
            if not settings['lowercase']:
                text.tokens = [token for token in text.tokens if not token.islower()]
            if not settings['uppercase']:
                text.tokens = [token for token in text.tokens if not token.isupper()]
            if not settings['title_case']:
                text.tokens = [token for token in text.tokens if not token.istitle()]

            if settings['treat_as_lowercase']:
                text.tokens = [token.lower() for token in text.tokens]

            if settings['lemmatize']:
                text.tokens = wordless_text.wordless_lemmatize(text.main, text.tokens, text.lang_code)

            if settings['filter_stop_words']:
                text.tokens = wordless_text.wordless_filter_stop_words(main, text.tokens, text.lang_code)
        else:
            text.tokens = [token for token in text.tokens if not [char for char in token if char.isalpha()]]
        
        if not settings['nums']:
            text.tokens = [token for token in text.tokens if not token.isnumeric()]
        if not settings['puncs']:
            text.tokens = [token for token in text.tokens if [char for char in token if char.isalnum()]]

        keywords_freq.append(collections.Counter(text.tokens))

        if i < len(files):
            texts.append(text)

        if i == len(files):
            len_tokens_ref = len(text.tokens)

    text_total = wordless_text.Wordless_Text(main, files[0])
    text_total.tokens = [token for text in texts for token in text.tokens]
    keywords_freq.insert(-1, collections.Counter(text_total.tokens))

    text_total_types = set(text_total.tokens)

    keywords_freq[-1] = {token: freq
                         for token, freq in keywords_freq[-1].items()
                         if token in text_total_types}

    # Test Statistics & Effect Size
    significance_test = main.settings_global['significance_tests'][settings['significance_test']]['func']
    effect_size_measure = main.settings_global['effect_size_measures'][settings['effect_size_measure']]['func']

    for i, text in enumerate(texts + [text_total]):
        keyness = {}

        len_tokens = len(text.tokens)

        for token in set(text.tokens):
            c11 = keywords_freq[i][token]
            c12 = keywords_freq[-1].get(token, 0)
            c21 = len_tokens - c11
            c22 = len_tokens_ref - c12

            keyness[token] = significance_test(c11, c12, c21, c22) + [effect_size_measure(c11, c12, c21, c22)]

        keywords_keyness.append(keyness)

    return (wordless_misc.merge_dicts(keywords_freq),
            wordless_misc.merge_dicts(keywords_keyness))

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['keywords']

    if settings['ref_file']:
        files = [file for file in main.wordless_files.get_selected_files(warning = False) if file['name'] != settings['ref_file']]

        if files:
            table.clear_table()

            table.settings = main.settings_custom

            for file in main.settings_custom['file']['files_open']:
                if file['name'] == settings['ref_file']:
                    ref_file = file

                    break

            (col_text_test_stats,
             col_text_p_value) = main.settings_global['significance_tests'][settings['significance_test']]['cols']
            col_text_effect_size =  main.settings_global['effect_size_measures'][settings['effect_size_measure']]['col']

            # Insert columns
            for file in files:
                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\nFrequency'),
                                 num = True, pct = True, cumulative = True, breakdown = True)

                if col_text_test_stats:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\n{col_text_test_stats}'),
                                     num = True, breakdown = True)
                if col_text_p_value:
                    table.insert_col(table.columnCount() - 1,
                                     main.tr(f'[{file["name"]}]\n{col_text_p_value}'),
                                     num = True, breakdown = True)

                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'[{file["name"]}]\n{col_text_effect_size}'),
                                 num = True, breakdown = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'Total\nFrequency'),
                             num = True, pct = True, cumulative = True)

            if col_text_test_stats:
                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\n{col_text_test_stats}'),
                                 num = True)
            if col_text_p_value:
                table.insert_col(table.columnCount() - 1,
                                 main.tr(f'Total\n{col_text_p_value}'),
                                 num = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'Total\n{col_text_effect_size}'),
                             num = True)

            table.insert_col(table.columnCount() - 1,
                             main.tr(f'[{ref_file["name"]}]\nFrequency'),
                             num = True, pct = True, cumulative = True)

            if col_text_p_value:
                # p-value
                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\n{col_text_p_value}')),
                                   Qt.AscendingOrder)
            else:
                # Test Statistics
                table.sortByColumn(table.find_col(main.tr(f'[{files[0]["name"]}]\n{col_text_test_stats}')),
                                   Qt.DescendingOrder)

            cols_freq = table.find_cols(main.tr('Frequency'))

            if col_text_test_stats and col_text_p_value:
                cols_test_stats = [col + 1 for col in cols_freq[:-1]]
                cols_p_value = [col + 2 for col in cols_freq[:-1]]
            elif col_text_test_stats:
                cols_test_stats = [col + 1 for col in cols_freq[:-1]]
            elif col_text_p_value:
                cols_p_value = [col + 1 for col in cols_freq[:-1]]

            cols_effect_size = table.find_cols(col_text_effect_size)
            col_files_found = table.find_col(main.tr('Files Found'))

            len_files = len(files)

            table.blockSignals(True)
            table.setSortingEnabled(False)
            table.setUpdatesEnabled(False)

            keywords_freq, keywords_keyness = generate_keywords(main, files, ref_file)

            table.setRowCount(len(keywords_freq))

            for i, (keyword, keyness_files) in enumerate(sorted(keywords_keyness.items(),
                                                                key = wordless_misc.multi_sorting_keyness)):
                # Rank
                table.set_item_num_int(i, 0, -1)

                # Keywords
                table.setItem(i, 1, wordless_table.Wordless_Table_Item(keyword))

                for j, (test_stat, p_value, effect_size) in enumerate(keyness_files):
                    if test_stat != None:
                        table.set_item_num_float(i, cols_test_stats[j], test_stat)
                    if p_value != None:
                        table.set_item_num_float(i, cols_p_value[j], p_value)
                    table.set_item_num_float(i, cols_effect_size[j], effect_size)

            for i in range(table.rowCount()):
                freq_files = keywords_freq[table.item(i, 1).text()]

                # Frequency
                for j, freq in enumerate(freq_files):
                    table.set_item_num_cumulative(i, cols_freq[j], freq)

                # Files Found
                table.set_item_num_pct(i, col_files_found, len([freq for freq in freq_files[:-2] if freq]), len_files)

            table.blockSignals(False)
            table.setSortingEnabled(True)
            table.setUpdatesEnabled(True)

            table.toggle_pct()
            table.toggle_cumulative()
            table.toggle_breakdown()
            table.update_ranks()

            table.update_items_width()

            table.item_changed()

            main.status_bar.showMessage(main.tr('Data generation completed!'))
        else:
            QMessageBox.warning(main,
                                main.tr('Missing Observed File(s)'),
                                main.tr('There are no files other than the reference file being currently selected!'),
                                QMessageBox.Ok)
    else:
        QMessageBox.warning(main,
                            main.tr('Missing Reference File'),
                            main.tr('Please open and select your reference file first!'),
                            QMessageBox.Ok)

def generate_plot(main):
    pass
