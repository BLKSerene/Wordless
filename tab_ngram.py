#
# Wordless: N-gram
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_utils import *

class Wordless_Table_Ngram(wordless_table.Wordless_Table):
    def __init__(self, parent, headers, stretch_columns = []):
        super().__init__(parent, headers = headers, stretch_columns = stretch_columns)

        self.item_changed()

def init(self):
    def token_settings_changed(widget_changed = None):
        if widget_changed == checkbox_words:
            checkbox_words.setTristate(False)

            if checkbox_words.checkState() == Qt.Checked:
                checkbox_lowercase.setEnabled(True)
                checkbox_uppercase.setEnabled(True)
                checkbox_title_cased.setEnabled(True)

                checkbox_ignore_case.setEnabled(True)
                checkbox_lemmatization.setEnabled(True)

                checkbox_lowercase.setChecked(True)
                checkbox_uppercase.setChecked(True)
                checkbox_title_cased.setChecked(True)

                search_settings_changed()
            else:
                checkbox_lowercase.setEnabled(False)
                checkbox_uppercase.setEnabled(False)
                checkbox_title_cased.setEnabled(False)

                checkbox_ignore_case.setEnabled(False)
                checkbox_lemmatization.setEnabled(False)

                checkbox_lowercase.setChecked(False)
                checkbox_uppercase.setChecked(False)
                checkbox_title_cased.setChecked(False)
        else:
            if (checkbox_lowercase.isChecked() and
                checkbox_uppercase.isChecked() and
                checkbox_title_cased.isChecked()):
                checkbox_words.setCheckState(Qt.Checked)
            elif (not checkbox_lowercase.isChecked() and
                  not checkbox_uppercase.isChecked() and
                  not checkbox_title_cased.isChecked()):
                checkbox_words.setCheckState(Qt.Unchecked)

                checkbox_lowercase.setEnabled(False)
                checkbox_uppercase.setEnabled(False)
                checkbox_title_cased.setEnabled(False)

                checkbox_ignore_case.setEnabled(False)
                checkbox_lemmatization.setEnabled(False)
            else:
                checkbox_words.setCheckState(Qt.PartiallyChecked)

        if checkbox_ignore_case.isEnabled():
            if checkbox_ignore_case.isChecked():
                checkbox_lowercase.setEnabled(False)
                checkbox_uppercase.setEnabled(False)
                checkbox_title_cased.setEnabled(False)
            else:
                checkbox_lowercase.setEnabled(True)
                checkbox_uppercase.setEnabled(True)
                checkbox_title_cased.setEnabled(True)

        self.settings['ngram']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        self.settings['ngram']['lowercase'] = checkbox_lowercase.isChecked()
        self.settings['ngram']['uppercase'] = checkbox_uppercase.isChecked()
        self.settings['ngram']['title_cased'] = checkbox_title_cased.isChecked()
        self.settings['ngram']['numerals'] = checkbox_numerals.isChecked()
        self.settings['ngram']['punctuations'] = checkbox_punctuations.isChecked()

    def search_settings_changed(widget_changed = None):
        self.settings['ngram']['ngram_size_sync'] = checkbox_ngram_size_sync.isChecked()
        self.settings['ngram']['ngram_size_min'] = spin_box_ngram_size_min.value()
        self.settings['ngram']['ngram_size_max'] = spin_box_ngram_size_max.value()

        self.settings['ngram']['search_term_position_left'] = checkbox_search_term_position_left.isChecked()
        self.settings['ngram']['search_term_position_middle'] = checkbox_search_term_position_middle.isChecked()
        self.settings['ngram']['search_term_position_right'] = checkbox_search_term_position_right.isChecked()
        self.settings['ngram']['ignore_case'] = checkbox_ignore_case.isChecked()
        self.settings['ngram']['lemmatization'] = checkbox_lemmatization.isChecked()
        self.settings['ngram']['whole_word'] = checkbox_whole_word.isChecked()
        self.settings['ngram']['regex'] = checkbox_regex.isChecked()
        self.settings['ngram']['multi_search'] = checkbox_multi_search.isChecked()
        self.settings['ngram']['show_all_ngrams'] = checkbox_show_all_ngrams.isChecked()

        if self.settings['ngram']['multi_search']:
            list_search_terms.get_items()
        else:
            if line_edit_search_term.text():
                self.settings['ngram']['search_terms'] = [line_edit_search_term.text()]
            else:
                self.settings['ngram']['search_terms'] = []

        if self.settings['ngram']['ngram_size_sync']:
            if widget_changed == spin_box_ngram_size_min:
                spin_box_ngram_size_max.setValue(spin_box_ngram_size_min.value())
            else:
                spin_box_ngram_size_min.setValue(spin_box_ngram_size_max.value())
        else:
            if (widget_changed == spin_box_ngram_size_min and 
                self.settings['ngram']['ngram_size_min'] > self.settings['ngram']['ngram_size_max']):
                spin_box_ngram_size_max.setValue(self.settings['ngram']['ngram_size_min'])
            elif (widget_changed == spin_box_ngram_size_max and 
                  self.settings['ngram']['ngram_size_max'] < self.settings['ngram']['ngram_size_min']):
                spin_box_ngram_size_min.setValue(self.settings['ngram']['ngram_size_max'])

        if self.settings['ngram']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if self.settings['ngram']['multi_search']:
            label_search_term.setText(self.tr('Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.count() == 0:
                list_search_terms.add_item()
                list_search_terms.item(0).setText(line_edit_search_term.text())

            line_edit_search_term.hide()

            list_search_terms.show()
            list_search_terms.button_add.show()
            list_search_terms.button_insert.show()
            list_search_terms.button_remove.show()
            list_search_terms.button_clear.show()
            list_search_terms.button_import.show()
            list_search_terms.button_export.show()
        else:
            label_search_term.setText(self.tr('Search Term:'))

            line_edit_search_term.show()

            list_search_terms.hide()
            list_search_terms.button_add.hide()
            list_search_terms.button_insert.hide()
            list_search_terms.button_remove.hide()
            list_search_terms.button_clear.hide()
            list_search_terms.button_import.hide()
            list_search_terms.button_export.hide()

        if self.settings['ngram']['show_all_ngrams']:
            table_ngram.button_generate_ngrams.setText(self.tr('Generate N-grams'))
            checkbox_lemmatization.setText(self.tr('Lemmatization'))

            line_edit_search_term.setEnabled(False)
            list_search_terms.setEnabled(False)
            checkbox_search_term_position_left.setEnabled(False)
            checkbox_search_term_position_middle.setEnabled(False)
            checkbox_search_term_position_right.setEnabled(False)
            checkbox_whole_word.setEnabled(False)
            checkbox_regex.setEnabled(False)
            checkbox_multi_search.setEnabled(False)
        else:
            table_ngram.button_generate_ngrams.setText(self.tr('Begin Search'))
            checkbox_lemmatization.setText(self.tr('Match All Lemmatized Forms'))

            line_edit_search_term.setEnabled(True)
            list_search_terms.setEnabled(True)
            checkbox_search_term_position_left.setEnabled(True)
            checkbox_search_term_position_middle.setEnabled(True)
            checkbox_search_term_position_right.setEnabled(True)
            checkbox_whole_word.setEnabled(True)
            checkbox_regex.setEnabled(True)
            checkbox_multi_search.setEnabled(True)

    def plot_settings_changed():
        self.settings['ngram']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['ngram']['freq_first_no_limit'] = checkbox_freq_first.isChecked()
        self.settings['ngram']['freq_first_min'] = spin_box_freq_first_min.value()
        self.settings['ngram']['freq_first_max'] = (float('inf')
                                                   if checkbox_freq_first.isChecked()
                                                   else spin_box_freq_first_max.value())

        self.settings['ngram']['freq_total_no_limit'] = checkbox_freq_total.isChecked()
        self.settings['ngram']['freq_total_min'] = spin_box_freq_total_min.value()
        self.settings['ngram']['freq_total_max'] = (float('inf')
                                                   if checkbox_freq_total.isChecked()
                                                   else spin_box_freq_total_max.value())

        self.settings['ngram']['rank_no_limit'] = checkbox_rank.isChecked()
        self.settings['ngram']['rank_min'] = spin_box_rank_min.value()
        self.settings['ngram']['rank_max'] = (float('inf')
                                             if checkbox_rank.isChecked()
                                             else spin_box_rank_max.value())

        self.settings['ngram']['len_no_limit'] = checkbox_len.isChecked()
        self.settings['ngram']['len_min'] = spin_box_len_min.value()
        self.settings['ngram']['len_max'] = (float('inf')
                                            if checkbox_len.isChecked()
                                            else spin_box_len_max.value())

        self.settings['ngram']['files_no_limit'] = checkbox_files.isChecked()
        self.settings['ngram']['files_min'] = spin_box_files_min.value()
        self.settings['ngram']['files_max'] = (float('inf')
                                              if checkbox_files.isChecked()
                                              else spin_box_files_max.value())

        if self.settings['ngram']['freq_first_no_limit']:
            spin_box_freq_first_max.setEnabled(False)
        else:
            spin_box_freq_first_max.setEnabled(True)

        if self.settings['ngram']['freq_total_no_limit']:
            spin_box_freq_total_max.setEnabled(False)
        else:
            spin_box_freq_total_max.setEnabled(True)

        if self.settings['ngram']['rank_no_limit']:
            spin_box_rank_max.setEnabled(False)
        else:
            spin_box_rank_max.setEnabled(True)

        if self.settings['ngram']['len_no_limit']:
            spin_box_len_max.setEnabled(False)
        else:
            spin_box_len_max.setEnabled(True)

        if self.settings['ngram']['files_no_limit']:
            spin_box_files_max.setEnabled(False)
        else:
            spin_box_files_max.setEnabled(True)

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['ngram']['words'])
        checkbox_lowercase.setChecked(self.default_settings['ngram']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['ngram']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['ngram']['title_cased'])
        checkbox_numerals.setChecked(self.default_settings['ngram']['numerals'])
        checkbox_punctuations.setChecked(self.default_settings['ngram']['punctuations'])

        checkbox_ngram_size_sync.setChecked(self.default_settings['ngram']['ngram_size_sync'])
        spin_box_ngram_size_min.setValue(self.default_settings['ngram']['ngram_size_min'])
        spin_box_ngram_size_max.setValue(self.default_settings['ngram']['ngram_size_max'])
        line_edit_search_term.clear()
        list_search_terms.clear()
        checkbox_search_term_position_left.setChecked(self.default_settings['ngram']['search_term_position_left'])
        checkbox_search_term_position_middle.setChecked(self.default_settings['ngram']['search_term_position_middle'])
        checkbox_search_term_position_right.setChecked(self.default_settings['ngram']['search_term_position_right'])
        checkbox_ignore_case.setChecked(self.default_settings['ngram']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['ngram']['lemmatization'])
        checkbox_whole_word.setChecked(self.default_settings['ngram']['whole_word'])
        checkbox_regex.setChecked(self.default_settings['ngram']['regex'])
        checkbox_multi_search.setChecked(self.default_settings['ngram']['multi_search'])
        checkbox_show_all_ngrams.setChecked(self.default_settings['ngram']['show_all_ngrams'])

        checkbox_cumulative.setChecked(self.default_settings['ngram']['cumulative'])

        checkbox_freq_first.setChecked(self.default_settings['ngram']['freq_first_no_limit'])
        spin_box_freq_first_min.setValue(self.default_settings['ngram']['freq_first_min'])
        spin_box_freq_first_max.setValue(self.default_settings['ngram']['freq_first_max'])
        checkbox_freq_total.setChecked(self.default_settings['ngram']['freq_total_no_limit'])
        spin_box_freq_total_min.setValue(self.default_settings['ngram']['freq_total_min'])
        spin_box_freq_total_max.setValue(self.default_settings['ngram']['freq_total_max'])
        checkbox_rank.setChecked(self.default_settings['ngram']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['ngram']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['ngram']['rank_max'])
        checkbox_len.setChecked(self.default_settings['ngram']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['ngram']['len_min'])
        spin_box_len_max.setValue(self.default_settings['ngram']['len_max'])
        checkbox_files.setChecked(self.default_settings['ngram']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['ngram']['files_min'])
        spin_box_files_max.setValue(self.default_settings['ngram']['files_max'])

        token_settings_changed()
        search_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_ngram = QWidget(self)
    
    table_ngram = Wordless_Table_Ngram(self,
                                       [
                                           self.tr('Rank'),
                                           self.tr('N-grams'),
                                           self.tr('Total'),
                                           self.tr('Total (%)'),
                                           self.tr('Cumulative Total'),
                                           self.tr('Cumulative Total (%)'),
                                           self.tr('Files Found'),
                                           self.tr('Files Found (%)')
                                       ])

    table_ngram.button_generate_ngrams = QPushButton(self.tr('Generate N-grams'), self)
    table_ngram.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_ngram.button_generate_ngrams.clicked.connect(lambda: generate_ngrams(self, table_ngram))
    table_ngram.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    layout_ngram_left = QGridLayout()
    layout_ngram_left.addWidget(table_ngram, 0, 0, 1, 5)
    layout_ngram_left.addWidget(table_ngram.button_generate_ngrams, 1, 0)
    layout_ngram_left.addWidget(table_ngram.button_generate_plot, 1, 1)
    layout_ngram_left.addWidget(table_ngram.button_export_selected, 1, 2)
    layout_ngram_left.addWidget(table_ngram.button_export_all, 1, 3)
    layout_ngram_left.addWidget(table_ngram.button_clear, 1, 4)

    # Token Settings
    groupbox_token_settings = QGroupBox(self.tr('Token Settings'), self)

    checkbox_words = QCheckBox(self.tr('Words'), self)
    checkbox_lowercase = QCheckBox(self.tr('Lowercase'), self)
    checkbox_uppercase = QCheckBox(self.tr('Uppercase'), self)
    checkbox_title_cased = QCheckBox(self.tr('Title Cased'), self)
    checkbox_numerals = QCheckBox(self.tr('Numerals'), self)
    checkbox_punctuations = QCheckBox(self.tr('Punctuations'), self)

    checkbox_words.clicked.connect(lambda: token_settings_changed(checkbox_words))
    checkbox_uppercase.clicked.connect(token_settings_changed)
    checkbox_title_cased.clicked.connect(token_settings_changed)
    checkbox_numerals.clicked.connect(token_settings_changed)
    checkbox_punctuations.clicked.connect(token_settings_changed)

    layout_token_settings = QGridLayout()
    layout_token_settings.addWidget(checkbox_words, 0, 0)
    layout_token_settings.addWidget(checkbox_lowercase, 0, 1)
    layout_token_settings.addWidget(checkbox_numerals, 1, 0)
    layout_token_settings.addWidget(checkbox_uppercase, 1, 1)
    layout_token_settings.addWidget(checkbox_punctuations, 2, 0)
    layout_token_settings.addWidget(checkbox_title_cased, 2, 1)

    groupbox_token_settings.setLayout(layout_token_settings)

    # Search Settings
    groupbox_search_settings = QGroupBox('Search Settings', self)

    label_ngram_size = QLabel(self.tr('N-gram Size:'), self)
    checkbox_ngram_size_sync = QCheckBox(self.tr('Sync'))
    label_ngram_size_min = QLabel(self.tr('From'), self)
    spin_box_ngram_size_min = QSpinBox(self)
    label_ngram_size_max = QLabel(self.tr('To'), self)
    spin_box_ngram_size_max = QSpinBox(self)

    label_search_term = QLabel(self.tr('Search Term:'), self)
    line_edit_search_term = QLineEdit(self)
    list_search_terms = wordless_list.Wordless_List(self)
    label_search_term_position = QLabel(self.tr('Search Term Position:'), self)
    checkbox_search_term_position_left = QCheckBox(self.tr('At Left'), self)
    checkbox_search_term_position_middle = QCheckBox(self.tr('In Middle'), self)
    checkbox_search_term_position_right = QCheckBox(self.tr('At Right'), self)
    checkbox_ignore_case = QCheckBox(self.tr('Ignore Case'), self)
    checkbox_lemmatization = QCheckBox(self.tr('Match All Lemmatized Forms'), self)
    checkbox_whole_word = QCheckBox(self.tr('Match Whole Word Only'), self)
    checkbox_regex = QCheckBox(self.tr('Use Regular Expression'), self)
    checkbox_multi_search = QCheckBox(self.tr('Multi-search Mode'), self)
    checkbox_show_all_ngrams = QCheckBox(self.tr('Show All N-grams'), self)

    spin_box_ngram_size_min.setRange(1, 100)
    spin_box_ngram_size_max.setRange(1, 100)

    checkbox_ngram_size_sync.stateChanged.connect(search_settings_changed)
    spin_box_ngram_size_min.valueChanged.connect(lambda: search_settings_changed(spin_box_ngram_size_min))
    spin_box_ngram_size_max.valueChanged.connect(lambda: search_settings_changed(spin_box_ngram_size_max))

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_ngram.button_generate_ngrams.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_search_term_position_left.stateChanged.connect(search_settings_changed)
    checkbox_search_term_position_middle.stateChanged.connect(search_settings_changed)
    checkbox_search_term_position_right.stateChanged.connect(search_settings_changed)
    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)
    checkbox_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search.stateChanged.connect(search_settings_changed)
    checkbox_show_all_ngrams.stateChanged.connect(search_settings_changed)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    layout_search_term_position = QGridLayout()
    layout_search_term_position.addWidget(label_search_term_position, 0, 0, 1, 3)
    layout_search_term_position.addWidget(checkbox_search_term_position_left, 1, 0)
    layout_search_term_position.addWidget(checkbox_search_term_position_middle, 1, 1)
    layout_search_term_position.addWidget(checkbox_search_term_position_right, 1, 2)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_ngram_size, 0, 0, 1, 3)
    layout_search_settings.addWidget(checkbox_ngram_size_sync, 0, 3)
    layout_search_settings.addWidget(label_ngram_size_min, 1, 0)
    layout_search_settings.addWidget(spin_box_ngram_size_min, 1, 1)
    layout_search_settings.addWidget(label_ngram_size_max, 1, 2)
    layout_search_settings.addWidget(spin_box_ngram_size_max, 1, 3)

    layout_search_settings.addWidget(label_search_term, 2, 0, 1, 4)
    layout_search_settings.addWidget(line_edit_search_term, 3, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_terms, 4, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_term_position, 5, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_ignore_case, 6, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_lemmatization, 7, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_whole_word, 8, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_regex, 9, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_multi_search, 10, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_show_all_ngrams, 11, 0, 1, 4)

    groupbox_search_settings.setLayout(layout_search_settings)

    # Plot Settings
    groupbox_plot_settings = QGroupBox(self.tr('Plot Settings'), self)

    checkbox_cumulative = QCheckBox(self.tr('Cumulative'), self)

    checkbox_cumulative.stateChanged.connect(plot_settings_changed)

    layout_plot_settings = QGridLayout()
    layout_plot_settings.addWidget(checkbox_cumulative, 0, 0)

    groupbox_plot_settings.setLayout(layout_plot_settings)

    # Filter Settings
    groupbox_filter_settings = QGroupBox(self.tr('Filter Settings'), self)

    label_freq_first = QLabel(self.tr('Frequency (First File):'), self)
    checkbox_freq_first = QCheckBox(self.tr('No Limit'), self)
    label_freq_first_min = QLabel(self.tr('From'), self)
    spin_box_freq_first_min = QSpinBox(self)
    label_freq_first_max = QLabel(self.tr('To'), self)
    spin_box_freq_first_max = QSpinBox(self)

    label_freq_total = QLabel(self.tr('Frequency (Total):'), self)
    checkbox_freq_total = QCheckBox(self.tr('No Limit'), self)
    label_freq_total_min = QLabel(self.tr('From'), self)
    spin_box_freq_total_min = QSpinBox(self)
    label_freq_total_max = QLabel(self.tr('To'), self)
    spin_box_freq_total_max = QSpinBox(self)

    label_rank = QLabel(self.tr('Rank:'), self)
    checkbox_rank = QCheckBox(self.tr('No Limit'), self)
    label_rank_min = QLabel(self.tr('From'), self)
    spin_box_rank_min = QSpinBox(self)
    label_rank_max = QLabel(self.tr('To'), self)
    spin_box_rank_max = QSpinBox(self)

    label_len = QLabel(self.tr('N-gram Length:'), self)
    checkbox_len = QCheckBox(self.tr('No Limit'), self)
    label_len_min = QLabel(self.tr('From'), self)
    spin_box_len_min = QSpinBox(self)
    label_len_max = QLabel(self.tr('To'), self)
    spin_box_len_max = QSpinBox(self)

    label_files = QLabel(self.tr('Files Found:'), self)
    checkbox_files = QCheckBox(self.tr('No Limit'), self)
    label_files_min = QLabel(self.tr('From'), self)
    spin_box_files_min = QSpinBox(self)
    label_files_max = QLabel(self.tr('To'), self)
    spin_box_files_max = QSpinBox(self)

    spin_box_freq_first_min.setRange(1, 1000000)
    spin_box_freq_first_max.setRange(1, 1000000)
    spin_box_freq_total_min.setRange(1, 1000000)
    spin_box_freq_total_max.setRange(1, 1000000)
    spin_box_rank_min.setRange(1, 1000000)
    spin_box_rank_max.setRange(1, 1000000)
    spin_box_len_min.setRange(1, 100)
    spin_box_len_max.setRange(1, 100)
    spin_box_files_min.setRange(1, 10000)
    spin_box_files_max.setRange(1, 10000)

    checkbox_freq_first.stateChanged.connect(filter_settings_changed)
    spin_box_freq_first_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_first_max.valueChanged.connect(filter_settings_changed)
    checkbox_freq_total.stateChanged.connect(filter_settings_changed)
    spin_box_freq_total_min.valueChanged.connect(filter_settings_changed)
    spin_box_freq_total_max.valueChanged.connect(filter_settings_changed)
    checkbox_rank.stateChanged.connect(filter_settings_changed)
    spin_box_rank_min.valueChanged.connect(filter_settings_changed)
    spin_box_rank_max.valueChanged.connect(filter_settings_changed)
    checkbox_len.stateChanged.connect(filter_settings_changed)
    spin_box_len_min.valueChanged.connect(filter_settings_changed)
    spin_box_len_max.valueChanged.connect(filter_settings_changed)
    checkbox_files.stateChanged.connect(filter_settings_changed)
    spin_box_files_min.valueChanged.connect(filter_settings_changed)
    spin_box_files_max.valueChanged.connect(filter_settings_changed)

    layout_filter_settings = QGridLayout()
    layout_filter_settings.addWidget(label_freq_first, 0, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_freq_first, 0, 3)
    layout_filter_settings.addWidget(label_freq_first_min, 1, 0)
    layout_filter_settings.addWidget(spin_box_freq_first_min, 1, 1)
    layout_filter_settings.addWidget(label_freq_first_max, 1, 2)
    layout_filter_settings.addWidget(spin_box_freq_first_max, 1, 3)

    layout_filter_settings.addWidget(label_freq_total, 2, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_freq_total, 2, 3)
    layout_filter_settings.addWidget(label_freq_total_min, 3, 0)
    layout_filter_settings.addWidget(spin_box_freq_total_min, 3, 1)
    layout_filter_settings.addWidget(label_freq_total_max, 3, 2)
    layout_filter_settings.addWidget(spin_box_freq_total_max, 3, 3)

    layout_filter_settings.addWidget(label_rank, 4, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_rank, 4, 3)
    layout_filter_settings.addWidget(label_rank_min, 5, 0)
    layout_filter_settings.addWidget(spin_box_rank_min, 5, 1)
    layout_filter_settings.addWidget(label_rank_max, 5, 2)
    layout_filter_settings.addWidget(spin_box_rank_max, 5, 3)

    layout_filter_settings.addWidget(label_len, 6, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_len, 6, 3)
    layout_filter_settings.addWidget(label_len_min, 7, 0)
    layout_filter_settings.addWidget(spin_box_len_min, 7, 1)
    layout_filter_settings.addWidget(label_len_max, 7, 2)
    layout_filter_settings.addWidget(spin_box_len_max, 7, 3)

    layout_filter_settings.addWidget(label_files, 8, 0, 1, 3)
    layout_filter_settings.addWidget(checkbox_files, 8, 3)
    layout_filter_settings.addWidget(label_files_min, 9, 0)
    layout_filter_settings.addWidget(spin_box_files_min, 9, 1)
    layout_filter_settings.addWidget(label_files_max, 9, 2)
    layout_filter_settings.addWidget(spin_box_files_max, 9, 3)

    groupbox_filter_settings.setLayout(layout_filter_settings)

    # Scroll Area Wrapper
    wrapper_settings = QWidget(self)

    layout_settings = QGridLayout()
    layout_settings.addWidget(groupbox_token_settings, 0, 0, Qt.AlignTop)
    layout_settings.addWidget(groupbox_search_settings, 1, 0, Qt.AlignTop)
    layout_settings.addWidget(groupbox_plot_settings, 2, 0, Qt.AlignTop)
    layout_settings.addWidget(groupbox_filter_settings, 3, 0, Qt.AlignTop)

    wrapper_settings.setLayout(layout_settings)

    scroll_area_settings = wordless_widgets.Wordless_Scroll_Area(self)
    scroll_area_settings.setWidget(wrapper_settings)

    button_advanced_settings = QPushButton(self.tr('Advanced Settings'), self)
    button_restore_defaults = QPushButton(self.tr('Restore Defaults'), self)

    button_advanced_settings.clicked.connect(lambda: self.wordless_settings.settings_load('N-gram'))
    button_restore_defaults.clicked.connect(restore_defaults)

    layout_ngram = QGridLayout()
    layout_ngram.addLayout(layout_ngram_left, 0, 0, 2, 1)
    layout_ngram.addWidget(scroll_area_settings, 0, 1, 1, 2)
    layout_ngram.addWidget(button_advanced_settings, 1, 1)
    layout_ngram.addWidget(button_restore_defaults, 1, 2)

    layout_ngram.setColumnStretch(0, 8)
    layout_ngram.setColumnStretch(1, 1)
    layout_ngram.setColumnStretch(2, 1)

    tab_ngram.setLayout(layout_ngram)

    restore_defaults()

    return tab_ngram

def generate_ngrams(self, table):
    if (self.settings['ngram']['show_all_ngrams'] or
        not self.settings['ngram']['show_all_ngrams'] and self.settings['ngram']['search_terms']):
        freq_previous = -1
        freq_total = 0

        table.clear_table()
        table.setRowCount(0)

        files = wordless_misc.fetch_files(self)
        
        for i, file in enumerate(files):
            table.insert_column(table.find_column('Total'), file.name)

        table.setSortingEnabled(False)

        column_total = table.find_column('Total')
        column_total_percentage = table.find_column('Total (%)')
        column_cumulative_total = table.find_column('Cumulative Total')
        column_cumulative_total_percentage = table.find_column('Cumulative Total (%)')
        column_files_found = table.find_column('Files Found')
        column_files_found_percentage = table.find_column('Files Found (%)')

        freq_distributions = wordless_freq.wordless_freq_distributions(self, files, mode = 'ngram')

        for i, (ngram, freqs) in enumerate(freq_distributions.items()):
            table.setRowCount(table.rowCount() + 1)
            
            # Rank
            table.setItem(i, 0, QTableWidgetItem())
            if freqs[0] == freq_previous:
                table.item(i, 0).setData(Qt.DisplayRole, table.item(i - 1, 0).data(Qt.DisplayRole))
            else:
                table.item(i, 0).setData(Qt.DisplayRole, i + 1)

            # N-gram
            table.setItem(i, 1, QTableWidgetItem(ngram))
            # Frequency
            for j, freq in enumerate(freqs):
                table.setItem(i, j + 2, QTableWidgetItem())
                table.item(i, j + 2).setData(Qt.DisplayRole, freq)

            # Total
            table.setItem(i, column_total, QTableWidgetItem())
            table.item(i, column_total).setData(Qt.DisplayRole, sum(freqs))

            # Files Found
            table.setItem(i, column_files_found, QTableWidgetItem())
            table.item(i, column_files_found).setData(Qt.DisplayRole, len([freq for freq in freqs if freq]))
            # Files Found (%)
            table.setItem(i, column_files_found_percentage, QTableWidgetItem())
            table.item(i, column_files_found_percentage).setData(Qt.DisplayRole,
                                                                 round(table.item(i, column_files_found).data(Qt.DisplayRole) /
                                                                       len(files) * 100,
                                                                       self.settings['general']['precision']))

            freq_previous = freqs[0]
            freq_total += sum(freqs)

        for i in range(table.rowCount()):
            # Total (%)
            table.setItem(i, column_total_percentage, QTableWidgetItem())
            table.item(i, column_total_percentage).setData(Qt.DisplayRole,
                                                           round(table.item(i, column_total).data(Qt.DisplayRole) /
                                                                 freq_total * 100,
                                                                 self.settings['general']['precision']))

            # Cumulative Total & Cumulative Total (%)
            table.setItem(i, column_cumulative_total, QTableWidgetItem())
            table.setItem(i, column_cumulative_total_percentage, QTableWidgetItem())

            if i == 0:
                table.item(i, column_cumulative_total).setData(Qt.DisplayRole,
                                                               table.item(i, column_total).data(Qt.DisplayRole))
                table.item(i, column_cumulative_total_percentage).setData(Qt.DisplayRole,
                                                                          table.item(i, column_total_percentage).data(Qt.DisplayRole))
            else:
                table.item(i, column_cumulative_total).setData(Qt.DisplayRole,
                                                               round(table.item(i - 1,column_cumulative_total).data(Qt.DisplayRole) +
                                                                     table.item(i, column_total).data(Qt.DisplayRole),
                                                                     self.settings['general']['precision']))
                table.item(i, column_cumulative_total_percentage).setData(Qt.DisplayRole,
                                                                          round(table.item(i, column_cumulative_total).data(Qt.DisplayRole) / freq_total * 100,
                                                                                self.settings['general']['precision']))

        if table.rowCount() > 0:
            table.sortByColumn(table.find_column('N-grams') + 1, Qt.DescendingOrder)
        else:
            table.clear_table()

            QMessageBox.information(self,
                                    self.tr('No Search Results'),
                                    self.tr('There are no results for your search!<br>You might want to change your settings and try it again.'),
                                    QMessageBox.Ok)

        table.setSortingEnabled(True)
    else:
        QMessageBox.warning(self,
                            self.tr('Search Failed'),
                            self.tr('Please enter your search term(s) first!'),
                            QMessageBox.Ok)
        
    self.status_bar.showMessage('Done!')

def generate_plot(self):
    freq_distributions = wordless_freq.wordless_freq_distributions(self, wordless_misc.fetch_files(self), mode = 'ngrams')

    freq_distributions.plot(cumulative = self.settings['ngrams']['cumulative'])

    self.status_bar.showMessage('Done!')
