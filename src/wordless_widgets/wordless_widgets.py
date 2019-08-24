#
# Wordless: Widgets - Widgets
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_dialogs import wordless_dialog_context_settings
from wordless_utils import wordless_misc
from wordless_widgets import (wordless_box, wordless_label, wordless_layout,
                              wordless_list)

def wordless_widgets_no_limit(parent, double = False):
    def no_limit_changed():
        if checkbox_no_limit.isChecked():
            spin_box_no_limit.setEnabled(False)
        else:
            spin_box_no_limit.setEnabled(True)

    if double:
        spin_box_no_limit = wordless_box.Wordless_Double_Spin_Box(parent)
    else:
        spin_box_no_limit = wordless_box.Wordless_Spin_Box(parent)

    checkbox_no_limit = QCheckBox(parent.tr('No Limit'), parent)

    checkbox_no_limit.stateChanged.connect(no_limit_changed)

    no_limit_changed()

    return spin_box_no_limit, checkbox_no_limit

# Token Settings
def wordless_widgets_token_settings(parent):
    def words_changed():
        if checkbox_words.isChecked():
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_case.setEnabled(True)
        else:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_case.setEnabled(False)

    def use_tags_changed():
        if checkbox_use_tags.isChecked():
            checkbox_lemmatize_tokens.setEnabled(False)

            stacked_widget_ignore_tags.setCurrentIndex(1)
            stacked_widget_ignore_tags_type.setCurrentIndex(1)
        else:
            checkbox_lemmatize_tokens.setEnabled(True)

            stacked_widget_ignore_tags.setCurrentIndex(0)
            stacked_widget_ignore_tags_type.setCurrentIndex(0)

    checkbox_words = QCheckBox(parent.tr('Words'), parent)
    checkbox_lowercase = QCheckBox(parent.tr('Lowercase'), parent)
    checkbox_uppercase = QCheckBox(parent.tr('Uppercase'), parent)
    checkbox_title_case = QCheckBox(parent.tr('Title Case'), parent)
    checkbox_nums = QCheckBox(parent.tr('Numerals'), parent)
    checkbox_puncs = QCheckBox(parent.tr('Punctuations'), parent)

    checkbox_treat_as_lowercase = QCheckBox(parent.tr('Treat as all lowercase'), parent)
    checkbox_lemmatize_tokens = QCheckBox(parent.tr('Lemmatize all tokens'), parent)
    checkbox_filter_stop_words = QCheckBox(parent.tr('Filter stop words'), parent)

    checkbox_ignore_tags = QCheckBox(parent.tr('Ignore'), parent)
    checkbox_ignore_tags_tags = QCheckBox(parent.tr('Ignore'), parent)
    combo_box_ignore_tags = wordless_box.Wordless_Combo_Box(parent)
    combo_box_ignore_tags_tags = wordless_box.Wordless_Combo_Box(parent)
    label_ignore_tags = QLabel(parent.tr('tags'), parent)
    checkbox_use_tags = QCheckBox(parent.tr('Use tags only'), parent)

    combo_box_ignore_tags.addItems([
        parent.tr('all'),
        parent.tr('POS'),
        parent.tr('non-POS')
    ])

    combo_box_ignore_tags_tags.addItems([
        parent.tr('POS'),
        parent.tr('non-POS')
    ])

    stacked_widget_ignore_tags = QStackedWidget(parent)
    stacked_widget_ignore_tags.addWidget(checkbox_ignore_tags)
    stacked_widget_ignore_tags.addWidget(checkbox_ignore_tags_tags)

    stacked_widget_ignore_tags_type = QStackedWidget(parent)
    stacked_widget_ignore_tags_type.addWidget(combo_box_ignore_tags)
    stacked_widget_ignore_tags_type.addWidget(combo_box_ignore_tags_tags)

    checkbox_words.stateChanged.connect(words_changed)
    checkbox_use_tags.stateChanged.connect(use_tags_changed)

    words_changed()
    use_tags_changed()

    return (checkbox_words,
            checkbox_lowercase,
            checkbox_uppercase,
            checkbox_title_case,
            checkbox_nums,
            checkbox_puncs,

            checkbox_treat_as_lowercase,
            checkbox_lemmatize_tokens,
            checkbox_filter_stop_words,

            stacked_widget_ignore_tags,
            checkbox_ignore_tags,
            checkbox_ignore_tags_tags,

            stacked_widget_ignore_tags_type,
            combo_box_ignore_tags,
            combo_box_ignore_tags_tags,

            label_ignore_tags,
            checkbox_use_tags)

def wordless_widgets_token_settings_concordancer(parent):
    def use_tags_changed():
        if checkbox_use_tags.isChecked():
            stacked_widget_ignore_tags.setCurrentIndex(1)
            stacked_widget_ignore_tags_type.setCurrentIndex(1)
        else:
            stacked_widget_ignore_tags.setCurrentIndex(0)
            stacked_widget_ignore_tags_type.setCurrentIndex(0)

    checkbox_puncs = QCheckBox(parent.tr('Punctuations'), parent)
    checkbox_ignore_tags = QCheckBox(parent.tr('Ignore'), parent)
    checkbox_ignore_tags_tags = QCheckBox(parent.tr('Ignore'), parent)
    combo_box_ignore_tags = wordless_box.Wordless_Combo_Box(parent)
    combo_box_ignore_tags_tags = wordless_box.Wordless_Combo_Box(parent)

    label_ignore_tags = QLabel(parent.tr('Tags'), parent)
    checkbox_use_tags = QCheckBox(parent.tr('Use tags only'), parent)

    combo_box_ignore_tags.addItems([
        parent.tr('all'),
        parent.tr('POS'),
        parent.tr('non-POS')
    ])

    combo_box_ignore_tags_tags.addItems([
        parent.tr('POS'),
        parent.tr('non-POS')
    ])

    stacked_widget_ignore_tags = QStackedWidget(parent)
    stacked_widget_ignore_tags.addWidget(checkbox_ignore_tags)
    stacked_widget_ignore_tags.addWidget(checkbox_ignore_tags_tags)

    stacked_widget_ignore_tags_type = QStackedWidget(parent)
    stacked_widget_ignore_tags_type.addWidget(combo_box_ignore_tags)
    stacked_widget_ignore_tags_type.addWidget(combo_box_ignore_tags_tags)

    checkbox_use_tags.stateChanged.connect(use_tags_changed)

    use_tags_changed()

    return (checkbox_puncs,

            stacked_widget_ignore_tags,
            checkbox_ignore_tags,
            checkbox_ignore_tags_tags,

            stacked_widget_ignore_tags_type,
            combo_box_ignore_tags,
            combo_box_ignore_tags_tags,

            label_ignore_tags,
            checkbox_use_tags)

# Search Settings
def wordless_widgets_search_settings(parent, tab):
    def multi_search_mode_changed():
        if checkbox_multi_search_mode.isChecked():
            label_search_term.setText(parent.tr('Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.count() == 0:
                list_search_terms.load_items([line_edit_search_term.text()])

            stacked_widget_search_term.setCurrentIndex(1)
        else:
            label_search_term.setText(parent.tr('Search Term:'))

            stacked_widget_search_term.setCurrentIndex(0)

    def match_tags_changed():
        if checkbox_match_tags.isChecked():
            checkbox_match_inflected_forms.setEnabled(False)

            stacked_widget_ignore_tags.setCurrentIndex(1)
            stacked_widget_ignore_tags_type.setCurrentIndex(1)
        else:
            checkbox_match_inflected_forms.setEnabled(True)
            
            stacked_widget_ignore_tags.setCurrentIndex(0)
            stacked_widget_ignore_tags_type.setCurrentIndex(0)

    def token_settings_changed():
        token_settings = main.settings_custom[tab]['token_settings']
        
        if token_settings['use_tags']:
            checkbox_match_tags.setEnabled(False)
            checkbox_match_tags.setChecked(True)

            if token_settings['ignore_tags_tags']:
                stacked_widget_ignore_tags.setEnabled(False)
                stacked_widget_ignore_tags_type.setEnabled(False)
            else:
                stacked_widget_ignore_tags.setEnabled(True)
                stacked_widget_ignore_tags_type.setEnabled(True)
        else:
            checkbox_match_tags.setChecked(False)

            if token_settings['ignore_tags']:
                if token_settings['ignore_tags_type'] == parent.tr('All'):
                    stacked_widget_ignore_tags.setEnabled(False)
                    stacked_widget_ignore_tags_type.setEnabled(False)
                    checkbox_match_tags.setEnabled(False)
                else:
                    if checkbox_match_tags.isChecked():
                        stacked_widget_ignore_tags.setEnabled(False)
                        stacked_widget_ignore_tags_type.setEnabled(False)
                    else:
                        stacked_widget_ignore_tags.setEnabled(True)
                        stacked_widget_ignore_tags_type.setEnabled(True)
                        
                    checkbox_match_tags.setEnabled(True)
            else:
                stacked_widget_ignore_tags.setEnabled(True)
                stacked_widget_ignore_tags_type.setEnabled(True)
                checkbox_match_tags.setEnabled(True)

        match_tags_changed()

    main = wordless_misc.find_wordless_main(parent)

    label_search_term = QLabel(parent.tr('Search Term:'), parent)
    checkbox_multi_search_mode = QCheckBox(parent.tr('Multi-search Mode'), parent)
    line_edit_search_term = QLineEdit(parent)
    list_search_terms = wordless_list.Wordless_List_Search_Terms(parent)
    label_separator = wordless_label.Wordless_Label_Hint(parent.tr('* Use space to separate multiple tokens'), parent)

    checkbox_ignore_case = QCheckBox(parent.tr('Ignore case'), parent)
    checkbox_match_inflected_forms = QCheckBox(parent.tr('Match all inflected forms'), parent)
    checkbox_match_whole_words = QCheckBox(parent.tr('Match whole words only'), parent)
    checkbox_use_regex = QCheckBox(parent.tr('Use regular expression'), parent)

    checkbox_ignore_tags = QCheckBox(parent.tr('Ignore'), parent)
    checkbox_ignore_tags_tags = QCheckBox(parent.tr('Ignore'), parent)
    combo_box_ignore_tags = wordless_box.Wordless_Combo_Box(parent)
    combo_box_ignore_tags_tags = wordless_box.Wordless_Combo_Box(parent)
    label_ignore_tags = QLabel(parent.tr('tags'), parent)
    checkbox_match_tags = QCheckBox(parent.tr('Match tags only'), parent)

    combo_box_ignore_tags.addItems([
        parent.tr('all'),
        parent.tr('POS'),
        parent.tr('non-POS')
    ])

    combo_box_ignore_tags_tags.addItems([
        parent.tr('POS'),
        parent.tr('non-POS')
    ])

    wrapper_search_terms = QWidget(parent)

    wrapper_search_terms.setLayout(wordless_layout.Wordless_Layout())
    wrapper_search_terms.layout().addWidget(list_search_terms, 0, 0, 5, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_add, 0, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_remove, 1, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_clear, 2, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_import, 3, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_export, 4, 1)

    wrapper_search_terms.layout().setContentsMargins(0, 0, 0, 0)

    stacked_widget_search_term = wordless_layout.Wordless_Stacked_Widget(parent)
    stacked_widget_search_term.addWidget(line_edit_search_term)
    stacked_widget_search_term.addWidget(wrapper_search_terms)

    stacked_widget_ignore_tags = wordless_layout.Wordless_Stacked_Widget(parent)
    stacked_widget_ignore_tags.addWidget(checkbox_ignore_tags)
    stacked_widget_ignore_tags.addWidget(checkbox_ignore_tags_tags)

    stacked_widget_ignore_tags_type = wordless_layout.Wordless_Stacked_Widget(parent)
    stacked_widget_ignore_tags_type.addWidget(combo_box_ignore_tags)
    stacked_widget_ignore_tags_type.addWidget(combo_box_ignore_tags_tags)

    checkbox_match_tags.token_settings_changed = token_settings_changed

    checkbox_multi_search_mode.stateChanged.connect(multi_search_mode_changed)
    checkbox_match_tags.stateChanged.connect(match_tags_changed)

    multi_search_mode_changed()
    match_tags_changed()

    return (label_search_term,
            checkbox_multi_search_mode,

            stacked_widget_search_term,
            line_edit_search_term,
            list_search_terms,

            label_separator,

            checkbox_ignore_case,
            checkbox_match_inflected_forms,
            checkbox_match_whole_words,
            checkbox_use_regex,

            stacked_widget_ignore_tags,
            checkbox_ignore_tags,
            checkbox_ignore_tags_tags,

            stacked_widget_ignore_tags_type,
            combo_box_ignore_tags,
            combo_box_ignore_tags_tags,

            label_ignore_tags,
            checkbox_match_tags)

def wordless_widgets_context_settings(parent, tab):
    main = wordless_misc.find_wordless_main(parent)

    label_context_settings = QLabel(parent.tr('Context Settings:'), parent)
    button_context_settings = QPushButton(parent.tr('Settings...'), parent)

    dialog_context_settings = wordless_dialog_context_settings.Wordless_Dialog_Context_Settings(main,
                                                                                                tab = tab)
    main.__dict__[f'wordless_context_settings_{tab}'] = dialog_context_settings

    button_context_settings.clicked.connect(lambda: main.__dict__[f'wordless_context_settings_{tab}'].load())

    return label_context_settings, button_context_settings

# Generation Settings
def wordless_widgets_size(parent, size_min = 1, size_max = 100):
    def size_sync_changed():
        if checkbox_size_sync.isChecked():
            spin_box_size_min.setValue(spin_box_size_max.value())

    def size_min_changed():
        if checkbox_size_sync.isChecked() or spin_box_size_min.value() > spin_box_size_max.value():
            spin_box_size_max.setValue(spin_box_size_min.value())

    def size_max_changed():
        if checkbox_size_sync.isChecked() or spin_box_size_min.value() > spin_box_size_max.value():
            spin_box_size_min.setValue(spin_box_size_max.value())

    checkbox_size_sync = QCheckBox(parent.tr('Sync'), parent)
    label_size_min = QLabel(parent.tr('From'), parent)
    spin_box_size_min = wordless_box.Wordless_Spin_Box(parent)
    label_size_max = QLabel(parent.tr('To'), parent)
    spin_box_size_max = wordless_box.Wordless_Spin_Box(parent)

    spin_box_size_min.setRange(size_min, size_max)
    spin_box_size_max.setRange(size_min, size_max)

    checkbox_size_sync.stateChanged.connect(size_sync_changed)
    spin_box_size_min.valueChanged.connect(size_min_changed)
    spin_box_size_max.valueChanged.connect(size_max_changed)

    size_sync_changed()
    size_min_changed()
    size_max_changed()

    return checkbox_size_sync, label_size_min, spin_box_size_min, label_size_max, spin_box_size_max

def wordless_widgets_window(parent):
    def window_sync_changed():
        if checkbox_window_sync.isChecked():
            spin_box_window_left.setPrefix(spin_box_window_right.prefix())
            spin_box_window_left.setValue(spin_box_window_right.value())

    def window_left_changed():
        if checkbox_window_sync.isChecked():
            spin_box_window_right.setPrefix(spin_box_window_left.prefix())
            spin_box_window_right.setValue(spin_box_window_left.value())
        else:
            if (spin_box_window_left.prefix() == 'L' and spin_box_window_right.prefix() == 'L' and
                spin_box_window_left.value() < spin_box_window_right.value() or
                spin_box_window_left.prefix() == 'R' and spin_box_window_right.prefix() == 'R' and
                spin_box_window_left.value() > spin_box_window_right.value() or
                spin_box_window_left.prefix() == 'R' and spin_box_window_right.prefix() == 'L'):
                spin_box_window_right.setPrefix(spin_box_window_left.prefix())
                spin_box_window_right.setValue(spin_box_window_left.value())

    def window_right_changed():
        if checkbox_window_sync.isChecked():
            spin_box_window_left.setPrefix(spin_box_window_right.prefix())
            spin_box_window_left.setValue(spin_box_window_right.value())
        else:
            if (spin_box_window_left.prefix() == 'L' and spin_box_window_right.prefix() == 'L' and
                spin_box_window_left.value() < spin_box_window_right.value() or
                spin_box_window_left.prefix() == 'R' and spin_box_window_right.prefix() == 'R' and
                spin_box_window_left.value() > spin_box_window_right.value() or
                spin_box_window_left.prefix() == 'R' and spin_box_window_right.prefix() == 'L'):
                spin_box_window_left.setPrefix(spin_box_window_right.prefix())
                spin_box_window_left.setValue(spin_box_window_right.value())

    checkbox_window_sync = QCheckBox(parent.tr('Sync'), parent)
    label_window_left = QLabel(parent.tr('From'), parent)
    spin_box_window_left = wordless_box.Wordless_Spin_Box_Window(parent)
    label_window_right = QLabel(parent.tr('To'), parent)
    spin_box_window_right = wordless_box.Wordless_Spin_Box_Window(parent)

    spin_box_window_left.setRange(-100, 100)
    spin_box_window_right.setRange(-100, 100)

    checkbox_window_sync.stateChanged.connect(window_sync_changed)
    spin_box_window_left.valueChanged.connect(window_left_changed)
    spin_box_window_right.valueChanged.connect(window_right_changed)

    window_sync_changed()
    window_left_changed()
    window_right_changed()

    return checkbox_window_sync, label_window_left, spin_box_window_left, label_window_right, spin_box_window_right

def wordless_widgets_measure_dispersion(parent):
    main = wordless_misc.find_wordless_main(parent)

    label_measure_dispersion = QLabel(parent.tr('Measure of Dispersion:'), parent)
    combo_box_measure_dispersion = wordless_box.Wordless_Combo_Box(parent)

    combo_box_measure_dispersion.addItems(list(main.settings_global['measures_dispersion'].keys()))

    return (label_measure_dispersion,
            combo_box_measure_dispersion)

def wordless_widgets_measure_adjusted_freq(parent):
    main = wordless_misc.find_wordless_main(parent)

    label_measure_adjusted_freq = QLabel(parent.tr('Measure of Adjusted Frequency:'), parent)
    combo_box_measure_adjusted_freq = wordless_box.Wordless_Combo_Box(parent)

    combo_box_measure_adjusted_freq.addItems(list(main.settings_global['measures_adjusted_freq'].keys()))

    return (label_measure_adjusted_freq,
            combo_box_measure_adjusted_freq)

def wordless_widgets_test_significance(parent):
    label_test_significance = QLabel(parent.tr('Test of Statistical Significance:'), parent)
    combo_box_test_significance = wordless_box.Wordless_Combo_Box(parent)

    return (label_test_significance,
            combo_box_test_significance)

def wordless_widgets_measure_effect_size(parent):
    label_measure_effect_size = QLabel(parent.tr('Measure of Effect Size:'), parent)
    combo_box_measure_effect_size = wordless_box.Wordless_Combo_Box(parent)

    return (label_measure_effect_size,
            combo_box_measure_effect_size)

def wordless_widgets_settings_measures(parent, tab):
    main = wordless_misc.find_wordless_main(parent)

    label_settings_measures = QLabel(parent.tr('Advanced Settings:'), parent)
    button_settings_measures = QPushButton(parent.tr('Settings...'), parent)

    button_settings_measures.clicked.connect(lambda: main.wordless_settings.load(tab = tab))

    return label_settings_measures, button_settings_measures

# Table Settings
def wordless_widgets_table_settings(parent, table):
    def show_pct_changed():
        table.show_pct = checkbox_show_pct.isChecked()

        if any([table.item(0, i) for i in range(table.columnCount())]):
            table.toggle_pct()

            table.update_items_width()

    def show_cumulative_changed():
        table.show_cumulative = checkbox_show_cumulative.isChecked()

        if any([table.item(0, i) for i in range(table.columnCount())]):
            table.toggle_cumulative()

            table.update_items_width()

    def show_breakdown_changed():
        table.show_breakdown = checkbox_show_breakdown.isChecked()

        table.toggle_breakdown()

    checkbox_show_pct = QCheckBox(parent.tr('Show percentage data'), parent)
    checkbox_show_cumulative = QCheckBox(parent.tr('Show cumulative data'), parent)
    checkbox_show_breakdown = QCheckBox(parent.tr('Show breakdown by file'), parent)

    checkbox_show_pct.stateChanged.connect(show_pct_changed)
    checkbox_show_cumulative.stateChanged.connect(show_cumulative_changed)
    checkbox_show_breakdown.stateChanged.connect(show_breakdown_changed)

    show_pct_changed()
    show_cumulative_changed()
    show_breakdown_changed()

    return checkbox_show_pct, checkbox_show_cumulative, checkbox_show_breakdown

# Figure Settings
def wordless_widgets_fig_settings(parent, collocation = False):
    def graph_type_changed():
        if combo_box_graph_type.currentText() == parent.tr('Line Chart'):
            combo_box_use_file.setEnabled(False)

            use_data_changed()
        else:
            combo_box_use_file.setEnabled(True)

            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)

    def use_data_changed():
        if combo_box_graph_type.currentText() == parent.tr('Line Chart'):
            if combo_box_use_data.currentText() == parent.tr('Frequency'):
                checkbox_use_pct.setEnabled(True)
                checkbox_use_cumulative.setEnabled(True)
            else:
                checkbox_use_pct.setEnabled(False)
                checkbox_use_cumulative.setEnabled(False)

    def wordless_files_changed():
        if combo_box_use_file.count() == 1:
            use_file_old = ''
        else:
            use_file_old = combo_box_use_file.currentText()

        combo_box_use_file.clear()

        for file in main.wordless_files.get_selected_files():
            combo_box_use_file.addItem(file['name'])

        combo_box_use_file.addItem(parent.tr('Total'))

        if use_file_old and combo_box_use_file.findText(use_file_old) > -1:
            combo_box_use_file.setCurrentText(use_file_old)

    main = wordless_misc.find_wordless_main(parent)

    label_graph_type = QLabel(parent.tr('Graph Type:'), parent)
    combo_box_graph_type = wordless_box.Wordless_Combo_Box(parent)
    label_use_file = QLabel(parent.tr('Use File:'), parent)
    combo_box_use_file = wordless_box.Wordless_Combo_Box(parent)
    label_use_data = QLabel(parent.tr('Use Data:'), parent)
    combo_box_use_data = wordless_box.Wordless_Combo_Box(parent)

    # Clip long file names
    combo_box_use_file.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

    checkbox_use_pct = QCheckBox(parent.tr('Use Percentage Data'), parent)
    checkbox_use_cumulative = QCheckBox(parent.tr('Use Cumulative Data'), parent)

    combo_box_graph_type.addItems([parent.tr('Line Chart'),
                                   parent.tr('Word Cloud')])

    # Collocation & Colligation
    if collocation:
        combo_box_graph_type.addItem(parent.tr('Network Graph'))

    combo_box_graph_type.currentTextChanged.connect(graph_type_changed)
    combo_box_use_data.currentTextChanged.connect(use_data_changed)

    main.wordless_files.table.itemChanged.connect(wordless_files_changed)

    combo_box_use_file.wordless_files_changed = wordless_files_changed

    graph_type_changed()
    use_data_changed()
    wordless_files_changed()

    return (label_graph_type, combo_box_graph_type,
            label_use_file, combo_box_use_file,
            label_use_data, combo_box_use_data,
            checkbox_use_pct, checkbox_use_cumulative)

# Filter Settings
def wordless_widgets_filter(parent, filter_min, filter_max):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    label_min = QLabel(parent.tr('From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wordless_widgets_no_limit(parent)

    label_max = QLabel(parent.tr('To'), parent)
    (spin_box_max,
     checkbox_max_no_limit) = wordless_widgets_no_limit(parent)

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    min_changed()
    max_changed()

    return (label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit)

def wordless_widgets_filter_measures(parent, filter_min = -10000, filter_max = 10000):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    def precision_changed():
        precision = main.settings_custom['data']['precision_decimal']

        spin_box_min.setDecimals(precision)
        spin_box_max.setDecimals(precision)

        spin_box_min.setSingleStep(0.1 ** precision)
        spin_box_max.setSingleStep(0.1 ** precision)

    main = wordless_misc.find_wordless_main(parent)

    label_min = QLabel(parent.tr('From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wordless_widgets_no_limit(parent, double = True)

    label_max = QLabel(parent.tr('To'), parent)
    (spin_box_max,
     checkbox_max_no_limit) = wordless_widgets_no_limit(parent, double = True)

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    main.wordless_settings.wordless_settings_changed.connect(precision_changed)

    min_changed()
    max_changed()
    
    precision_changed()

    return (label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit)

def wordless_widgets_filter_p_value(parent):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    def precision_changed():
        precision = main.settings_custom['data']['precision_p_value']

        spin_box_min.setDecimals(precision)
        spin_box_max.setDecimals(precision)

        spin_box_min.setSingleStep(0.1 ** precision)
        spin_box_max.setSingleStep(0.1 ** precision)

    main = wordless_misc.find_wordless_main(parent)

    label_min = QLabel(parent.tr('From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wordless_widgets_no_limit(parent, double = True)

    label_max = QLabel(parent.tr('To'), parent)
    (spin_box_max,
     checkbox_max_no_limit) = wordless_widgets_no_limit(parent, double = True)

    spin_box_min.setRange(0, 1)
    spin_box_max.setRange(0, 1)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    main.wordless_settings.wordless_settings_changed.connect(precision_changed)

    min_changed()
    max_changed()

    precision_changed()

    return (label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit)

def wordless_widgets_filter_results(parent, table):
    def table_item_changed():
        if combo_box_filter_file.count() == 1:
            file_old = ''
        else:
            file_old = combo_box_filter_file.currentText()

        combo_box_filter_file.clear()

        for file in table.settings['files']['files_open']:
            if file['selected']:
                combo_box_filter_file.addItem(file['name'])

        combo_box_filter_file.addItem(parent.tr('Total'))

        if combo_box_filter_file.findText(file_old) > -1:
            combo_box_filter_file.setCurrentText(file_old)

    label_filter_file = QLabel(parent.tr('Filter File:'), parent)
    combo_box_filter_file = wordless_box.Wordless_Combo_Box(parent)
    button_filter_results = QPushButton(parent.tr('Filter Results in Table'), parent)

    button_filter_results.clicked.connect(lambda: table.update_filters())

    table.itemChanged.connect(table_item_changed)

    table_item_changed()

    return (label_filter_file, combo_box_filter_file,
            button_filter_results)

# Settings -> Measures
def wordless_widgets_number_sections(parent):
    label_divide = QLabel(parent.tr('Divide each text into'), parent)
    spin_box_number_sections = wordless_box.Wordless_Spin_Box(parent)
    label_sections = QLabel(parent.tr('sections'), parent)

    spin_box_number_sections.setRange(2, 1000)

    return label_divide, spin_box_number_sections, label_sections

def wordless_widgets_use_data_freq(parent):
    label_use_data = QLabel(parent.tr('Use Data:'), parent)
    combo_box_use_data = wordless_box.Wordless_Combo_Box(parent)

    combo_box_use_data.addItems([parent.tr('Absolute Frequency'),
                                 parent.tr('Relative Frequency')])

    return label_use_data, combo_box_use_data

def wordless_widgets_direction(parent):
    label_direction = QLabel(parent.tr('Direction:'), parent)
    combo_box_direction = wordless_box.Wordless_Combo_Box(parent)

    combo_box_direction.addItems([parent.tr('Two-tailed'),
                                  parent.tr('Left-tailed'),
                                  parent.tr('Right-tailed')])

    return label_direction, combo_box_direction

def wordless_widgets_direction_2(parent):
    label_direction = QLabel(parent.tr('Direction:'), parent)
    combo_box_direction = wordless_box.Wordless_Combo_Box(parent)

    combo_box_direction.addItems([parent.tr('Two-tailed'),
                                  parent.tr('One-tailed')])

    return label_direction, combo_box_direction

# Settings -> Figures
def wordless_widgets_pick_color(parent):
    def get_color():
        return re.search(r'#[0-9a-zA-Z]{6}', label_pick_color.text()).group()

    def set_color(color):
        label_pick_color.setText(f'<span style="margin-right: 3px; background-color: {color}; color: {color}">00</span> <span>{color.upper()}</span>')

    def pick_color():
        color_picked = QColorDialog.getColor(QColor(get_color()), parent, parent.tr('Pick Color'))

        if color_picked.isValid():
            label_pick_color.set_color(color_picked.name())

    label_pick_color = wordless_label.Wordless_Label_Html('', parent)
    button_pick_color = QPushButton(parent.tr('Pick Color...'), parent)

    label_pick_color.get_color = get_color
    label_pick_color.set_color = set_color

    button_pick_color.clicked.connect(pick_color)

    return label_pick_color, button_pick_color
