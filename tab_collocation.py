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

class Wordless_Table_Collocation(wordless_table.Wordless_Table):
    def __init__(self, parent, headers):
        super().__init__(parent, headers)

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

        self.settings['collocation']['words'] = False if checkbox_words.checkState() == Qt.Unchecked else True
        self.settings['collocation']['lowercase'] = checkbox_lowercase.isChecked()
        self.settings['collocation']['uppercase'] = checkbox_uppercase.isChecked()
        self.settings['collocation']['title_cased'] = checkbox_title_cased.isChecked()
        self.settings['collocation']['numerals'] = checkbox_numerals.isChecked()
        self.settings['collocation']['punctuations'] = checkbox_punctuations.isChecked()

    def search_settings_changed():
        self.settings['collocation']['window_sync'] = checkbox_window_sync.isChecked()
        self.settings['collocation']['window_left'][0] = spin_box_window_left.prefix()
        self.settings['collocation']['window_left'][1] = spin_box_window_left.value()
        self.settings['collocation']['window_right'][0] = spin_box_window_right.prefix()
        self.settings['collocation']['window_right'][1] = spin_box_window_right.value()
        self.settings['collocation']['search_for'] = combo_box_search_for.currentText()
        self.settings['collocation']['assoc_measure'] = combo_box_assoc_measure.currentText()

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
        self.settings['collocation']['show_all_collocates'] = checkbox_show_all_collocates.isChecked()

        if self.settings['collocation']['ignore_case']:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)
        else:
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)

        if self.settings['collocation']['multi_search']:
            label_search_term.setText(self.tr('Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.count() == 0:
                list_search_terms.add_item(line_edit_search_term.text())

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

        if self.settings['collocation']['show_all_collocates']:
            table_collocation.button_generate_collocates.setText(self.tr('Generate Collocates'))
            checkbox_lemmatization.setText(self.tr('Lemmatization'))

            line_edit_search_term.setEnabled(False)
            list_search_terms.setEnabled(False)
            checkbox_whole_word.setEnabled(False)
            checkbox_regex.setEnabled(False)
            checkbox_multi_search.setEnabled(False)
        else:
            table_collocation.button_generate_collocates.setText(self.tr('Begin Search'))
            checkbox_lemmatization.setText(self.tr('Match All Lemmatized Forms'))

            line_edit_search_term.setEnabled(True)
            list_search_terms.setEnabled(True)
            checkbox_whole_word.setEnabled(True)
            checkbox_regex.setEnabled(True)
            checkbox_multi_search.setEnabled(True)

    def plot_settings_changed():
        self.settings['collocation']['cumulative'] = checkbox_cumulative.isChecked()

    def filter_settings_changed():
        self.settings['collocation']['freq_first_no_limit'] = checkbox_freq_first.isChecked()
        self.settings['collocation']['freq_first_min'] = spin_box_freq_first_min.value()
        self.settings['collocation']['freq_first_max'] = (float('inf')
                                                          if checkbox_freq_first.isChecked()
                                                          else spin_box_freq_first_max.value())

        self.settings['collocation']['freq_total_no_limit'] = checkbox_freq_total.isChecked()
        self.settings['collocation']['freq_total_min'] = spin_box_freq_total_min.value()
        self.settings['collocation']['freq_total_max'] = (float('inf')
                                                          if checkbox_freq_total.isChecked()
                                                          else spin_box_freq_total_max.value())

        self.settings['collocation']['rank_no_limit'] = checkbox_rank.isChecked()
        self.settings['collocation']['rank_min'] = spin_box_rank_min.value()
        self.settings['collocation']['rank_max'] = (float('inf')
                                                    if checkbox_rank.isChecked()
                                                    else spin_box_rank_max.value())

        self.settings['collocation']['len_no_limit'] = checkbox_len.isChecked()
        self.settings['collocation']['len_min'] = spin_box_len_min.value()
        self.settings['collocation']['len_max'] = (float('inf')
                                                   if checkbox_len.isChecked()
                                                   else spin_box_len_max.value())

        self.settings['collocation']['files_no_limit'] = checkbox_files.isChecked()
        self.settings['collocation']['files_min'] = spin_box_files_min.value()
        self.settings['collocation']['files_max'] = (float('inf')
                                                     if checkbox_files.isChecked()
                                                     else spin_box_files_max.value())

        if self.settings['collocation']['freq_first_no_limit']:
            spin_box_freq_first_max.setEnabled(False)
        else:
            spin_box_freq_first_max.setEnabled(True)

        if self.settings['collocation']['freq_total_no_limit']:
            spin_box_freq_total_max.setEnabled(False)
        else:
            spin_box_freq_total_max.setEnabled(True)

        if self.settings['collocation']['rank_no_limit']:
            spin_box_rank_max.setEnabled(False)
        else:
            spin_box_rank_max.setEnabled(True)

        if self.settings['collocation']['len_no_limit']:
            spin_box_len_max.setEnabled(False)
        else:
            spin_box_len_max.setEnabled(True)

        if self.settings['collocation']['files_no_limit']:
            spin_box_files_max.setEnabled(False)
        else:
            spin_box_files_max.setEnabled(True)

    def restore_defaults():
        checkbox_words.setChecked(self.default_settings['collocation']['words'])
        checkbox_lowercase.setChecked(self.default_settings['collocation']['lowercase'])
        checkbox_uppercase.setChecked(self.default_settings['collocation']['uppercase'])
        checkbox_title_cased.setChecked(self.default_settings['collocation']['title_cased'])
        checkbox_numerals.setChecked(self.default_settings['collocation']['numerals'])
        checkbox_punctuations.setChecked(self.default_settings['collocation']['punctuations'])

        checkbox_window_sync.setChecked(self.default_settings['collocation']['window_sync'])
        spin_box_window_left.setPrefix(self.default_settings['collocation']['window_left'][0])
        spin_box_window_left.setValue(self.default_settings['collocation']['window_left'][1])
        spin_box_window_right.setPrefix(self.default_settings['collocation']['window_right'][0])
        spin_box_window_right.setValue(self.default_settings['collocation']['window_right'][1])
        combo_box_search_for.setCurrentText(self.default_settings['collocation']['search_for'])
        combo_box_assoc_measure.setCurrentText(self.default_settings['collocation']['assoc_measure'])

        line_edit_search_term.clear()
        list_search_terms.clear()
        checkbox_ignore_case.setChecked(self.default_settings['collocation']['ignore_case'])
        checkbox_lemmatization.setChecked(self.default_settings['collocation']['lemmatization'])
        checkbox_whole_word.setChecked(self.default_settings['collocation']['whole_word'])
        checkbox_regex.setChecked(self.default_settings['collocation']['regex'])
        checkbox_multi_search.setChecked(self.default_settings['collocation']['multi_search'])
        checkbox_show_all_collocates.setChecked(self.default_settings['collocation']['show_all_collocates'])

        checkbox_cumulative.setChecked(self.default_settings['collocation']['cumulative'])

        checkbox_freq_first.setChecked(self.default_settings['collocation']['freq_first_no_limit'])
        spin_box_freq_first_min.setValue(self.default_settings['collocation']['freq_first_min'])
        spin_box_freq_first_max.setValue(self.default_settings['collocation']['freq_first_max'])
        checkbox_freq_total.setChecked(self.default_settings['collocation']['freq_total_no_limit'])
        spin_box_freq_total_min.setValue(self.default_settings['collocation']['freq_total_min'])
        spin_box_freq_total_max.setValue(self.default_settings['collocation']['freq_total_max'])
        checkbox_rank.setChecked(self.default_settings['collocation']['rank_no_limit'])
        spin_box_rank_min.setValue(self.default_settings['collocation']['rank_min'])
        spin_box_rank_max.setValue(self.default_settings['collocation']['rank_max'])
        checkbox_len.setChecked(self.default_settings['collocation']['len_no_limit'])
        spin_box_len_min.setValue(self.default_settings['collocation']['len_min'])
        spin_box_len_max.setValue(self.default_settings['collocation']['len_max'])
        checkbox_files.setChecked(self.default_settings['collocation']['files_no_limit'])
        spin_box_files_min.setValue(self.default_settings['collocation']['files_min'])
        spin_box_files_max.setValue(self.default_settings['collocation']['files_max'])

        token_settings_changed()
        search_settings_changed()
        plot_settings_changed()
        filter_settings_changed()

    tab_collocation = QWidget(self)
    
    table_collocation = Wordless_Table_Collocation(self,
                                                   [
                                                       self.tr('Rank'),
                                                       self.tr('Collocates'),
                                                       self.tr('Total Frequency'),
                                                       self.tr('Total Frequency (%)'),
                                                       self.tr('Cumulative Total Frequency'),
                                                       self.tr('Cumulative Total Frequency (%)'),
                                                       self.tr('Total Score'),
                                                       self.tr('Total Score (%)'),
                                                       self.tr('Cumulative Total Score'),
                                                       self.tr('Cumulative Total Score (%)'),
                                                       self.tr('Files Found'),
                                                       self.tr('Files Found (%)')
                                                   ])

    table_collocation.button_generate_collocates = QPushButton(self.tr('Generate Collocates'), self)
    table_collocation.button_generate_plot = QPushButton(self.tr('Generate Plot'), self)

    table_collocation.button_generate_collocates.clicked.connect(lambda: generate_collocates(self, table_collocation))
    table_collocation.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    layout_collocation_left = QGridLayout()
    layout_collocation_left.addWidget(table_collocation, 0, 0, 1, 5)
    layout_collocation_left.addWidget(table_collocation.button_generate_collocates, 1, 0)
    layout_collocation_left.addWidget(table_collocation.button_generate_plot, 1, 1)
    layout_collocation_left.addWidget(table_collocation.button_export_selected, 1, 2)
    layout_collocation_left.addWidget(table_collocation.button_export_all, 1, 3)
    layout_collocation_left.addWidget(table_collocation.button_clear, 1, 4)

    # Token Settings
    groupbox_token_settings = QGroupBox(self.tr('Token Settings'), self)

    checkbox_words = QCheckBox(self.tr('Words'), self)
    checkbox_lowercase = QCheckBox(self.tr('Lowercase'), self)
    checkbox_uppercase = QCheckBox(self.tr('Uppercase'), self)
    checkbox_title_cased = QCheckBox(self.tr('Title Cased'), self)
    checkbox_numerals = QCheckBox(self.tr('Numerals'), self)
    checkbox_punctuations = QCheckBox(self.tr('Punctuations'), self)

    checkbox_words.clicked.connect(lambda: token_settings_changed(checkbox_words))
    checkbox_lowercase.clicked.connect(token_settings_changed)
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

    label_window = QLabel(self.tr('Collocational Window:'), self)
    label_window_left = QLabel(self.tr('From'), self)
    label_window_right = QLabel(self.tr('To'), self)
    (checkbox_window_sync,
     spin_box_window_left,
     spin_box_window_right) = wordless_widgets.wordless_widgets_window(self)
    label_search_for = QLabel(self.tr('Search for:'), self)
    label_assoc_measure = QLabel(self.tr('Association Measure:'), self)
    (combo_box_search_for,
     combo_box_assoc_measure) = wordless_widgets.wordless_widgets_collocation(self,
                                                                              self.default_settings['collocation']['assoc_measure'])

    label_search_term = QLabel(self.tr('Search Term:'), self)
    line_edit_search_term = QLineEdit(self)
    list_search_terms = wordless_list.Wordless_List(self)
    checkbox_ignore_case = QCheckBox(self.tr('Ignore Case'), self)
    checkbox_lemmatization = QCheckBox(self.tr('Match All Lemmatized Forms'), self)
    checkbox_whole_word = QCheckBox(self.tr('Match Whole Word Only'), self)
    checkbox_regex = QCheckBox(self.tr('Use Regular Expression'), self)
    checkbox_multi_search = QCheckBox(self.tr('Multi-search Mode'), self)
    checkbox_show_all_collocates = QCheckBox(self.tr('Show All Collocates'), self)

    spin_box_window_left.setRange(-100, 100)
    spin_box_window_right.setRange(-100, 100)

    checkbox_window_sync.stateChanged.connect(search_settings_changed)
    spin_box_window_left.valueChanged.connect(search_settings_changed)
    spin_box_window_right.valueChanged.connect(search_settings_changed)
    combo_box_search_for.currentTextChanged.connect(search_settings_changed)
    combo_box_assoc_measure.currentTextChanged.connect(search_settings_changed)

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_collocation.button_generate_collocates.click)
    list_search_terms.itemChanged.connect(search_settings_changed)
    checkbox_ignore_case.stateChanged.connect(search_settings_changed)
    checkbox_lemmatization.stateChanged.connect(search_settings_changed)
    checkbox_whole_word.stateChanged.connect(search_settings_changed)
    checkbox_regex.stateChanged.connect(search_settings_changed)
    checkbox_multi_search.stateChanged.connect(search_settings_changed)
    checkbox_show_all_collocates.stateChanged.connect(search_settings_changed)

    layout_search_terms = QGridLayout()
    layout_search_terms.addWidget(list_search_terms, 0, 0, 6, 1)
    layout_search_terms.addWidget(list_search_terms.button_add, 0, 1)
    layout_search_terms.addWidget(list_search_terms.button_insert, 1, 1)
    layout_search_terms.addWidget(list_search_terms.button_remove, 2, 1)
    layout_search_terms.addWidget(list_search_terms.button_clear, 3, 1)
    layout_search_terms.addWidget(list_search_terms.button_import, 4, 1)
    layout_search_terms.addWidget(list_search_terms.button_export, 5, 1)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_window, 0, 0, 1, 3)
    layout_search_settings.addWidget(checkbox_window_sync, 0, 3)
    layout_search_settings.addWidget(label_window_left, 1, 0)
    layout_search_settings.addWidget(spin_box_window_left, 1, 1)
    layout_search_settings.addWidget(label_window_right, 1, 2)
    layout_search_settings.addWidget(spin_box_window_right, 1, 3)
    layout_search_settings.addWidget(label_search_for, 2, 0, 1, 2)
    layout_search_settings.addWidget(combo_box_search_for, 2, 2, 1, 2)
    layout_search_settings.addWidget(label_assoc_measure, 3, 0, 1, 4)
    layout_search_settings.addWidget(combo_box_assoc_measure, 4, 0, 1, 4)

    layout_search_settings.addWidget(label_search_term, 5, 0, 1, 4)
    layout_search_settings.addWidget(line_edit_search_term, 6, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_terms, 7, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_ignore_case, 8, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_lemmatization, 9, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_whole_word, 10, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_regex, 11, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_multi_search, 12, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_show_all_collocates, 13, 0, 1, 4)

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

    label_len = QLabel(self.tr('Collocate Length:'), self)
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

    button_advanced_settings.clicked.connect(lambda: self.wordless_settings.settings_load('Collocation'))
    button_restore_defaults.clicked.connect(restore_defaults)

    layout_collocation = QGridLayout()
    layout_collocation.addLayout(layout_collocation_left, 0, 0, 2, 1)
    layout_collocation.addWidget(scroll_area_settings, 0, 1, 1, 2)
    layout_collocation.addWidget(button_advanced_settings, 1, 1)
    layout_collocation.addWidget(button_restore_defaults, 1, 2)

    layout_collocation.setColumnStretch(0, 8)
    layout_collocation.setColumnStretch(1, 1)
    layout_collocation.setColumnStretch(2, 1)

    tab_collocation.setLayout(layout_collocation)

    restore_defaults()

    return tab_collocation

def generate_collocates(self, table):
        if (self.settings['collocation']['show_all_collocates'] or
            not self.settings['collocation']['show_all_collocates'] and self.settings['collocation']['search_terms']):
            freq_previous = -1
            freq_total = 0

            table.clear_table()
            table.setRowCount(0)

            files = wordless_misc.fetch_files(self)
            
            for i, file in enumerate(files):
                table.insert_column(table.find_column('Total Frequency'), file.name + '(Frequency)')
                table.insert_column(table.find_column('Total Frequency'), file.name + '(Score)')

            table.setSortingEnabled(False)

            col_total_freq = table.find_column('Total Frequency')
            col_total_freq_pct = table.find_column('Total Frequency (%)')
            col_cumulative_total_freq = table.find_column('Cumulative Total Frequency')
            col_cumulative_total_freq_pct = table.find_column('Cumulative Total Frequency (%)')
            col_total_score = table.find_column('Total Score')
            col_total_score_pct = table.find_column('Total Score (%)')
            col_cumulative_total_score = table.find_column('Cumulative Total Score')
            col_cumulative_total_score_pct = table.find_column('Cumulative Total Score (%)')
            col_files_found = table.find_column('Files Found')
            col_files_found_pct = table.find_column('Files Found (%)')

            freq_distributions = wordless_freq.wordless_freq_distributions(self, files, mode = 'collocation')

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
                table.setItem(i, col_total, QTableWidgetItem())
                table.item(i, col_total).setData(Qt.DisplayRole, sum(freqs))

                # Files Found
                table.setItem(i, col_files_found, QTableWidgetItem())
                table.item(i, col_files_found).setData(Qt.DisplayRole, len([freq for freq in freqs if freq]))
                # Files Found (%)
                table.setItem(i, col_files_found_pct, QTableWidgetItem())
                table.item(i, col_files_found_pct).setData(Qt.DisplayRole,
                                                           round(table.item(i, col_files_found).data(Qt.DisplayRole) / len(files) * 100,
                                                                 self.settings['general']['precision']))

                freq_previous = freqs[0]
                freq_total += sum(freqs)

            for i in range(table.rowCount()):
                # Total (%)
                table.setItem(i, col_total_pct, QTableWidgetItem())
                table.item(i, col_total_pct).setData(Qt.DisplayRole,
                                                     round(table.item(i, col_total).data(Qt.DisplayRole) / freq_total * 100,
                                                           self.settings['general']['precision']))

                # Cumulative Total & Cumulative Total (%)
                table.setItem(i, col_cumulative_total, QTableWidgetItem())
                table.setItem(i, col_cumulative_total_pct, QTableWidgetItem())

                if i == 0:
                    table.item(i, col_cumulative_total).setData(Qt.DisplayRole,
                                                                table.item(i, col_total).data(Qt.DisplayRole))
                    table.item(i, col_cumulative_total_pct).setData(Qt.DisplayRole,
                                                                    table.item(i, col_total_pct).data(Qt.DisplayRole))
                else:
                    table.item(i, col_cumulative_total).setData(Qt.DisplayRole,
                                                                round(table.item(i - 1,col_cumulative_total).data(Qt.DisplayRole) +
                                                                      table.item(i, col_total).data(Qt.DisplayRole),
                                                                      self.settings['general']['precision']))
                    table.item(i, col_cumulative_total_pct).setData(Qt.DisplayRole,
                                                                    round(table.item(i, col_cumulative_total).data(Qt.DisplayRole) /
                                                                          freq_total * 100,
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
