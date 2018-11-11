#
# Wordless: N-gram
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

class Wordless_Table_Ngram(wordless_table.Wordless_Table_Data_Search):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Rank'),
                             main.tr('N-grams'),
                             main.tr('Total\nFrequency'),
                             main.tr('Files Found'),
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
                                                               tab = 'ngram',
                                                               table = self,
                                                               cols_search = self.tr('N-grams'))

        self.button_search_results.clicked.connect(dialog_search.load)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self.main)
        self.button_generate_plot = QPushButton(self.tr('Generate Plot'), self.main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_plot.clicked.connect(lambda: generate_plot(self.main))

    @ wordless_misc.log_timing
    def update_filters(self):
        if any([self.item(0, i) for i in range(self.columnCount())]):
            settings = self.main.settings_custom['ngram']

            if settings['apply_to'] == self.tr('Total'):
                col_freq = self.find_col(self.tr('Total\nFrequency'))
            else:
                col_freq = self.find_col(self.tr(f'[{settings["apply_to"]}]\nFrequency'))

            col_ngrams = self.find_col('N-grams')
            col_files_found = self.find_col('Files Found')

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

                if len_min <= len(self.item(i, col_ngrams).text().replace(' ', '')) <= len_max:
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
    def load_settings(defaults = False):
        if defaults:
            settings_loaded = copy.deepcopy(main.settings_default['ngram'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['ngram'])

        checkbox_words.setChecked(settings_loaded['words'])
        checkbox_lowercase.setChecked(settings_loaded['lowercase'])
        checkbox_uppercase.setChecked(settings_loaded['uppercase'])
        checkbox_title_case.setChecked(settings_loaded['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings_loaded['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings_loaded['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings_loaded['filter_stop_words'])

        checkbox_nums.setChecked(settings_loaded['nums'])
        checkbox_puncs.setChecked(settings_loaded['puncs'])

        group_box_search_settings.setChecked(settings_loaded['search_settings'])
        
        checkbox_multi_search_mode.setChecked(settings_loaded['multi_search_mode'])

        if not defaults:
            line_edit_search_term.setText(settings_loaded['search_term'])

            for search_term in settings_loaded['search_terms']:
                list_search_terms.add_item(search_term)

        checkbox_keyword_position_no_limit.setChecked(settings_loaded['keyword_position_no_limit'])
        spin_box_keyword_position_min.setValue(settings_loaded['keyword_position_min'])
        spin_box_keyword_position_max.setValue(settings_loaded['keyword_position_max'])

        checkbox_ignore_case.setChecked(settings_loaded['ignore_case'])
        checkbox_match_inflected_forms.setChecked(settings_loaded['match_inflected_forms'])
        checkbox_match_whole_word.setChecked(settings_loaded['match_whole_word'])
        checkbox_use_regex.setChecked(settings_loaded['use_regex'])

        checkbox_ngram_size_sync.setChecked(settings_loaded['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(settings_loaded['ngram_size_min'])
        spin_box_ngram_size_max.setValue(settings_loaded['ngram_size_max'])
        spin_box_allow_skipped_tokens.setValue(settings_loaded['allow_skipped_tokens'])

        checkbox_show_pct.setChecked(settings_loaded['show_pct'])
        checkbox_show_cumulative.setChecked(settings_loaded['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings_loaded['show_breakdown'])

        combo_box_plot_type.setCurrentText(settings_loaded['plot_type'])
        combo_box_use_data_file.setCurrentText(settings_loaded['use_data_file'])
        checkbox_use_pct.setChecked(settings_loaded['use_pct'])
        checkbox_use_cumulative.setChecked(settings_loaded['use_cumulative'])

        checkbox_rank_no_limit.setChecked(settings_loaded['rank_no_limit'])
        spin_box_rank_min.setValue(settings_loaded['rank_min'])
        spin_box_rank_max.setValue(settings_loaded['rank_max'])

        combo_box_apply_to.setCurrentText(settings_loaded['apply_to'])

        checkbox_freq_no_limit.setChecked(settings_loaded['freq_no_limit'])
        spin_box_freq_min.setValue(settings_loaded['freq_min'])
        spin_box_freq_max.setValue(settings_loaded['freq_max'])

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
        settings['search_settings'] = group_box_search_settings.isChecked()

        settings['multi_search_mode'] = checkbox_multi_search_mode.isChecked()
        settings['search_term'] = line_edit_search_term.text()
        settings['search_terms'] = list_search_terms.get_items()
        settings['keyword_position_no_limit'] = checkbox_keyword_position_no_limit.isChecked()
        settings['keyword_position_min'] = spin_box_keyword_position_min.value()
        settings['keyword_position_max'] = spin_box_keyword_position_max.value()

        settings['ignore_case'] = checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = checkbox_match_inflected_forms.isChecked()
        settings['match_whole_word'] = checkbox_match_whole_word.isChecked()
        settings['use_regex'] = checkbox_use_regex.isChecked()

        if settings['search_settings']:
            label_ngram_size.setText(main.tr('N-gram Size:'))
        else:
            label_ngram_size.setText(main.tr('Cluster Size:'))

    def generation_settings_changed():
        settings['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        settings['ngram_size_min'] = spin_box_ngram_size_min.value()
        settings['ngram_size_max'] = spin_box_ngram_size_max.value()
        settings['allow_skipped_tokens'] = spin_box_allow_skipped_tokens.value()

        if (settings['keyword_position_no_limit'] and
            spin_box_keyword_position_max.value() == spin_box_keyword_position_max.maximum()):
            spin_box_keyword_position_min.setMaximum(settings['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(settings['ngram_size_max'])

            spin_box_keyword_position_max.setValue(settings['ngram_size_max'])
        else:
            spin_box_keyword_position_min.setMaximum(settings['ngram_size_max'])
            spin_box_keyword_position_max.setMaximum(settings['ngram_size_max'])

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    def plot_settings_changed():
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

    settings = main.settings_custom['ngram']

    tab_ngram = wordless_layout.Wordless_Tab(main, load_settings)
    
    table_ngram = Wordless_Table_Ngram(main)

    tab_ngram.layout_table.addWidget(table_ngram.label_number_results, 0, 0)
    tab_ngram.layout_table.addWidget(table_ngram.button_search_results, 0, 4)
    tab_ngram.layout_table.addWidget(table_ngram, 1, 0, 1, 5)
    tab_ngram.layout_table.addWidget(table_ngram.button_generate_table, 2, 0)
    tab_ngram.layout_table.addWidget(table_ngram.button_generate_plot, 2, 1)
    tab_ngram.layout_table.addWidget(table_ngram.button_export_selected, 2, 2)
    tab_ngram.layout_table.addWidget(table_ngram.button_export_all, 2, 3)
    tab_ngram.layout_table.addWidget(table_ngram.button_clear, 2, 4)

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

    group_box_search_settings.setCheckable(True)

    group_box_search_settings.toggled.connect(search_settings_changed)

    (label_search_term,
     checkbox_multi_search_mode,
     line_edit_search_term,
     list_search_terms,

     checkbox_ignore_case,
     checkbox_match_inflected_forms,
     checkbox_match_whole_word,
     checkbox_use_regex) = wordless_widgets.wordless_widgets_search(main)

    label_keyword_position = QLabel(main.tr('Keyword Position:'), main)
    (checkbox_keyword_position_no_limit,
     label_keyword_position_min,
     spin_box_keyword_position_min,
     label_keyword_position_max,
     spin_box_keyword_position_max) = wordless_widgets.wordless_widgets_filter(main)

    checkbox_multi_search_mode.stateChanged.connect(search_settings_changed)
    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_ngram.button_generate_table.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_keyword_position_no_limit.stateChanged.connect(search_settings_changed)
    spin_box_keyword_position_min.valueChanged.connect(search_settings_changed)
    spin_box_keyword_position_max.valueChanged.connect(search_settings_changed)

    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_match_inflected_forms.stateChanged.connect(search_settings_changed)
    checkbox_match_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_use_regex.stateChanged.connect(search_settings_changed)

    layout_multi_search_mode = QGridLayout()
    layout_multi_search_mode.addWidget(label_search_term, 0, 0)
    layout_multi_search_mode.addWidget(checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    group_box_search_settings.setLayout(QGridLayout())
    group_box_search_settings.layout().addLayout(layout_multi_search_mode, 0, 0, 1, 4)
    group_box_search_settings.layout().addWidget(line_edit_search_term, 1, 0, 1, 4)
    group_box_search_settings.layout().addLayout(layout_search_terms, 2, 0, 1, 4)
    group_box_search_settings.layout().addWidget(label_keyword_position, 3, 0, 1, 3)
    group_box_search_settings.layout().addWidget(checkbox_keyword_position_no_limit, 3, 3)
    group_box_search_settings.layout().addWidget(label_keyword_position_min, 4, 0)
    group_box_search_settings.layout().addWidget(spin_box_keyword_position_min, 4, 1)
    group_box_search_settings.layout().addWidget(label_keyword_position_max, 4, 2)
    group_box_search_settings.layout().addWidget(spin_box_keyword_position_max, 4, 3)

    group_box_search_settings.layout().addWidget(checkbox_ignore_case, 5, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_inflected_forms, 6, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_match_whole_word, 7, 0, 1, 4)
    group_box_search_settings.layout().addWidget(checkbox_use_regex, 8, 0, 1, 4)

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

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_ngram_size, 0, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(checkbox_ngram_size_sync, 0, 3)
    group_box_generation_settings.layout().addWidget(label_ngram_size_min, 1, 0)
    group_box_generation_settings.layout().addWidget(spin_box_ngram_size_min, 1, 1)
    group_box_generation_settings.layout().addWidget(label_ngram_size_max, 1, 2)
    group_box_generation_settings.layout().addWidget(spin_box_ngram_size_max, 1, 3)
    group_box_generation_settings.layout().addWidget(label_allow_skipped_tokens, 2, 0, 1, 3)
    group_box_generation_settings.layout().addWidget(spin_box_allow_skipped_tokens, 2, 3)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'))

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table(main, table_ngram)

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
    combo_box_apply_to = wordless_box.Wordless_Combo_Box_Apply_To(main, table_ngram)

    label_freq = QLabel(main.tr('Frequency:'), main)
    (checkbox_freq_no_limit,
     label_freq_min,
     spin_box_freq_min,
     label_freq_max,
     spin_box_freq_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 0, filter_max = 1000000)

    label_len = QLabel(main.tr('N-gram Length:'), main)
    (checkbox_len_no_limit,
     label_len_min,
     spin_box_len_min,
     label_len_max,
     spin_box_len_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 1000)

    label_files = QLabel(main.tr('Files Found:'), main)
    (checkbox_files_no_limit,
     label_files_min,
     spin_box_files_min,
     label_files_max,
     spin_box_files_max) = wordless_widgets.wordless_widgets_filter(main, filter_min = 1, filter_max = 100000)

    button_filter_table = QPushButton(main.tr('Filter Results in Table'), main)

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

    button_filter_table.clicked.connect(lambda: table_ngram.update_filters())

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

    group_box_filter_settings.layout().addWidget(button_filter_table, 8, 0, 1, 4)

    tab_ngram.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_search_settings, 1, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_generation_settings, 2, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_table_settings, 3, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_plot_settings, 4, 0, Qt.AlignTop)
    tab_ngram.layout_settings.addWidget(group_box_filter_settings, 5, 0, Qt.AlignTop)

    tab_ngram.layout_settings.setRowStretch(6, 1)

    load_settings()

    return tab_ngram

def generate_ngrams(main, files):
    freqs_files = []

    settings = main.settings_custom['ngram']

    for file in files:
        ngrams = []

        text = wordless_text.Wordless_Text(main, file)

        if settings['words']:
            if settings['treat_as_lowercase']:
                text.tokens = [token.lower() for token in text.tokens]

            if settings['lemmatize']:
                text.tokens = wordless_text.wordless_lemmatize(main, text.tokens, text.lang_code)

        if not settings['puncs']:
            text.tokens = [token for token in text.tokens if [char for char in token if char.isalnum()]]

        if settings['allow_skipped_tokens'] == 0:
            ngrams = list(nltk.everygrams(text.tokens, settings['ngram_size_min'], settings['ngram_size_max']))
        else:
            for i in range(settings['ngram_size_min'], settings['ngram_size_max'] + 1):
                ngrams.extend(list(nltk.skipgrams(text.tokens, i, settings['allow_skipped_tokens'])))

        freqs_file = nltk.FreqDist(ngrams)

        if settings['words']:
            if not settings['treat_as_lowercase']:
                if not settings['lowercase']:
                    freqs_file = {ngram: freq
                                  for ngram, freq in freqs_file.items()
                                  if not [token for token in ngram if token.islower()]}
                if not settings['uppercase']:
                    freqs_file = {ngram: freq
                                  for ngram, freq in freqs_file.items()
                                  if not [token for token in ngram if token.isupper()]}
                if not settings['title_case']:
                    freqs_file = {ngram: freq
                                  for ngram, freq in freqs_file.items()
                                  if not [token for token in ngram if token.istitle()]}

            if settings['filter_stop_words']:
                ngrams_filtered = wordless_text.wordless_filter_stop_words(main, list(freqs_file.keys()), text.lang_code)
                
                freqs_file = {ngram: freqs_file[ngram] for ngram in ngrams_filtered}
        else:
            freqs_file = {ngram: freq
                          for ngram, freq in freqs_file.items()
                          if not [char for char in ''.join(ngram) if char.isalpha()]}

        if not settings['nums']:
            freqs_file = {ngram: freq
                          for ngram, freq in freqs_file.items()
                          if [token for token in ngram if not token.isnumeric()]}

        if not settings['show_all']:
            if settings['multi_search_mode']:
                search_terms = settings['search_terms']
            else:
                search_terms = [settings['search_term']]

            search_terms = text.match_search_terms(search_terms,
                                                   settings['ignore_case'],
                                                   settings['match_inflected_forms'],
                                                   settings['match_whole_word'],
                                                   settings['use_regex'])

            freqs_file = {ngram: freq
                          for ngram, freq in freqs_file.items()
                          for search_term in search_terms
                          if (search_term in ngram and
                              settings['keyword_position_min'] <= ngram.index(search_term) + 1 <= settings['keyword_position_max'])}

        freqs_files.append({text.word_divider.join(ngram): freq for ngram, freq in freqs_file.items()})

    return wordless_misc.merge_dicts(freqs_files)

@ wordless_misc.log_timing
def generate_table(main, table):
    settings = main.settings_custom['ngram']

    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            freqs_files = generate_ngrams(main, files)

            if freqs_files:
                table.settings = main.settings_custom

                table.clear_table()

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

                for i, (ngram, freqs) in enumerate(wordless_sorting.sorted_freqs_files(freqs_files)):
                    # Rank
                    table.set_item_num_int(i, 0, -1)

                    # N-gram
                    table.setItem(i, 1, wordless_table.Wordless_Table_Item(ngram))

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
                wordless_message_box.wordless_message_box_no_results_table(main)

                wordless_message.wordless_message_generate_table_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term(main)

            wordless_message.wordless_message_generate_table_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)

@ wordless_misc.log_timing
def generate_plot(main):
    settings = main.settings_custom['ngram']

    files = main.wordless_files.get_selected_files()

    if files:
        if (settings['show_all'] or
            not settings['show_all'] and (settings['multi_search_mode'] and settings['search_terms'] or
                                          not settings['multi_search_mode'] and settings['search_term'])):
            freqs_files = generate_ngrams(main, files)

            if freqs_files:
                wordless_plot.wordless_plot_freq(main, freqs_files,
                                                 plot_type = settings['plot_type'],
                                                 use_data_file = settings['use_data_file'],
                                                 use_pct = settings['use_pct'],
                                                 use_cumulative = settings['use_cumulative'],
                                                 rank_min = settings['rank_min'],
                                                 rank_max = settings['rank_max'],
                                                 label_x = main.tr('N-grams'))

                wordless_message.wordless_message_generate_plot_success(main)
            else:
                wordless_message_box.wordless_message_box_no_results_plot(main)

                wordless_message.wordless_message_generate_plot_error(main)
        else:
            wordless_message_box.wordless_message_box_empty_search_term(main)

            wordless_message.wordless_message_generate_plot_error(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_plot_error(main)
