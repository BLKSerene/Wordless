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
    def token_settings_changed():
        pass

    def search_settings_changed():
        pass

    def plot_settings_changed():
        pass

    def filter_settings_changed():
        pass

    def restore_defaults():
        pass

    tab_collocation = QWidget(self)
    
    table_collocation = Wordless_Table_Collocation(self,
                                                   [
                                                       self.tr('Rank'),
                                                       self.tr('Collocates'),
                                                       self.tr('Total'),
                                                       self.tr('Total (%)'),
                                                       self.tr('Cumulative Total'),
                                                       self.tr('Cumulative Total (%)'),
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
    checkbox_window_sync = QCheckBox(self.tr('Sync'))
    label_window_left = QLabel(self.tr('From'), self)
    spin_box_window_left = QSpinBox(self)
    label_window_right = QLabel(self.tr('To'), self)
    spin_box_window_right = QSpinBox(self)
    label_window_span = QLabel(self.tr('Window Span:'), self)
    spin_box_window_span = QSpinBox(self)
    label_search_for = QLabel(self.tr('Search for:'), self)
    combo_box_search_for = wordless_widgets.Wordless_Combo_Box_Collocation_Ngram(self)
    label_assoc_measure = QLabel(self.tr('Association Measure:'), self)
    combo_box_assoc_measure = QComboBox(self)

    label_search_term = QLabel(self.tr('Search Term:'), self)
    line_edit_search_term = QLineEdit(self)
    list_search_terms = wordless_list.Wordless_List(self)
    checkbox_ignore_case = QCheckBox(self.tr('Ignore Case'), self)
    checkbox_lemmatization = QCheckBox(self.tr('Match All Lemmatized Forms'), self)
    checkbox_whole_word = QCheckBox(self.tr('Match Whole Word Only'), self)
    checkbox_regex = QCheckBox(self.tr('Use Regular Expression'), self)
    checkbox_multi_search = QCheckBox(self.tr('Multi-search Mode'), self)
    checkbox_show_all_collocates = QCheckBox(self.tr('Show All Collocates'), self)

    spin_box_window_left.setRange(1, 100)
    spin_box_window_right.setRange(1, 100)
    spin_box_window_span.setRange(1, 100)

    checkbox_window_sync.stateChanged.connect(search_settings_changed)
    spin_box_window_left.valueChanged.connect(lambda: search_settings_changed(spin_box_window_left))
    spin_box_window_right.valueChanged.connect(lambda: search_settings_changed(spin_box_window_right))
    spin_box_window_span.valueChanged.connect(search_settings_changed)
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
    layout_search_settings.addWidget(label_window_span, 2, 0, 1, 2)
    layout_search_settings.addWidget(spin_box_window_span, 2, 2, 1, 2)
    layout_search_settings.addWidget(label_search_for, 3, 0, 1, 2)
    layout_search_settings.addWidget(combo_box_search_for, 3, 2, 1, 2)
    layout_search_settings.addWidget(label_assoc_measure, 4, 0, 1, 4)
    layout_search_settings.addWidget(combo_box_assoc_measure, 5, 0, 1, 4)

    layout_search_settings.addWidget(label_search_term, 6, 0, 1, 4)
    layout_search_settings.addWidget(line_edit_search_term, 7, 0, 1, 4)
    layout_search_settings.addLayout(layout_search_terms, 8, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_ignore_case, 9, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_lemmatization, 10, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_whole_word, 11, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_regex, 12, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_multi_search, 13, 0, 1, 4)
    layout_search_settings.addWidget(checkbox_show_all_collocates, 14, 0, 1, 4)

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
