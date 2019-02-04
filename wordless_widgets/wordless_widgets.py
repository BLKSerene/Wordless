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

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_widgets import wordless_box, wordless_dialog, wordless_label, wordless_list

def wordless_widgets_no_limit(main, double = False):
    def no_limit_changed():
        if checkbox_no_limit.isChecked():
            spin_box_no_limit.setEnabled(False)
        else:
            spin_box_no_limit.setEnabled(True)

    if double:
        spin_box_no_limit = QDoubleSpinBox(main)
    else:
        spin_box_no_limit = QSpinBox(main)

    checkbox_no_limit = QCheckBox(main.tr('No Limit'), main)

    checkbox_no_limit.stateChanged.connect(no_limit_changed)

    no_limit_changed()

    return spin_box_no_limit, checkbox_no_limit

# Token Settings
def wordless_widgets_token_settings(main):
    def words_changed():
        if checkbox_words.isChecked():
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_case.setEnabled(True)
        else:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_case.setEnabled(False)

    def tags_only_changed():
        if checkbox_tags_only.isChecked():
            checkbox_treat_as_lowercase.setChecked(False)
            checkbox_lemmatize.setEnabled(False)

            checkbox_ignore_tags.hide()
            combo_box_ignore_tags.hide()

            checkbox_ignore_tags_tags_only.show()
            combo_box_ignore_tags_tags_only.show()
        else:
            checkbox_treat_as_lowercase.setChecked(True)
            checkbox_lemmatize.setEnabled(True)

            checkbox_ignore_tags_tags_only.hide()
            combo_box_ignore_tags_tags_only.hide()

            checkbox_ignore_tags.show()
            combo_box_ignore_tags.show()

    checkbox_words = QCheckBox(main.tr('Words'), main)
    checkbox_lowercase = QCheckBox(main.tr('Lowercase'), main)
    checkbox_uppercase = QCheckBox(main.tr('Uppercase'), main)
    checkbox_title_case = QCheckBox(main.tr('Title Case'), main)
    checkbox_nums = QCheckBox(main.tr('Numerals'), main)
    checkbox_puncs = QCheckBox(main.tr('Punctuations'), main)

    checkbox_treat_as_lowercase = QCheckBox(main.tr('Treat as All Lowercase'), main)
    checkbox_lemmatize = QCheckBox(main.tr('Lemmatize'), main)
    checkbox_filter_stop_words = QCheckBox(main.tr('Filter Stop Words'), main)

    checkbox_ignore_tags = QCheckBox(main.tr('Ignore'), main)
    checkbox_ignore_tags_tags_only = QCheckBox(main.tr('Ignore'), main)
    combo_box_ignore_tags = wordless_box.Wordless_Combo_Box(main)
    combo_box_ignore_tags_tags_only = wordless_box.Wordless_Combo_Box(main)
    label_ignore_tags = QLabel(main.tr('Tags'), main)
    checkbox_tags_only = QCheckBox(main.tr('Tags Only'), main)

    combo_box_ignore_tags.addItems([
        main.tr('All'),
        main.tr('POS'),
        main.tr('Non-POS')
    ])

    combo_box_ignore_tags_tags_only.addItems([
        main.tr('POS'),
        main.tr('Non-POS')
    ])

    checkbox_words.stateChanged.connect(words_changed)
    checkbox_tags_only.stateChanged.connect(tags_only_changed)

    words_changed()
    tags_only_changed()

    return (checkbox_words,
            checkbox_lowercase,
            checkbox_uppercase,
            checkbox_title_case,
            checkbox_nums,
            checkbox_puncs,

            checkbox_treat_as_lowercase,
            checkbox_lemmatize,
            checkbox_filter_stop_words,

            checkbox_ignore_tags,
            checkbox_ignore_tags_tags_only,
            combo_box_ignore_tags,
            combo_box_ignore_tags_tags_only,
            label_ignore_tags,
            checkbox_tags_only)

def wordless_widgets_token_settings_concordancer(main):
    def tags_only_changed():
        if checkbox_tags_only.isChecked():
            checkbox_ignore_tags.hide()
            combo_box_ignore_tags.hide()

            checkbox_ignore_tags_tags_only.show()
            combo_box_ignore_tags_tags_only.show()
        else:
            checkbox_ignore_tags_tags_only.hide()
            combo_box_ignore_tags_tags_only.hide()

            checkbox_ignore_tags.show()
            combo_box_ignore_tags.show()

    checkbox_puncs = QCheckBox(main.tr('Punctuations'), main)

    checkbox_ignore_tags = QCheckBox(main.tr('Ignore'), main)
    checkbox_ignore_tags_tags_only = QCheckBox(main.tr('Ignore'), main)
    combo_box_ignore_tags = wordless_box.Wordless_Combo_Box(main)
    combo_box_ignore_tags_tags_only = wordless_box.Wordless_Combo_Box(main)
    label_ignore_tags = QLabel(main.tr('Tags'), main)
    checkbox_tags_only = QCheckBox(main.tr('Tags Only'), main)

    combo_box_ignore_tags.addItems([
        main.tr('All'),
        main.tr('POS'),
        main.tr('Non-POS')
    ])

    combo_box_ignore_tags_tags_only.addItems([
        main.tr('POS'),
        main.tr('Non-POS')
    ])

    checkbox_tags_only.stateChanged.connect(tags_only_changed)

    tags_only_changed()

    return (checkbox_puncs,

            checkbox_ignore_tags,
            checkbox_ignore_tags_tags_only,
            combo_box_ignore_tags,
            combo_box_ignore_tags_tags_only,
            label_ignore_tags,
            checkbox_tags_only)

# Search Settings
def wordless_widgets_search_settings1(main):
    def multi_search_mode_changed():
        if checkbox_multi_search_mode.isChecked():
            label_search_term.setText(main.tr('Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.count() == 0:
                list_search_terms.add_item(line_edit_search_term.text())

            line_edit_search_term.hide()

            list_search_terms.show()
            list_search_terms.button_add.show()
            list_search_terms.button_remove.show()
            list_search_terms.button_clear.show()
            list_search_terms.button_import.show()
            list_search_terms.button_export.show()
        else:
            label_search_term.setText(main.tr('Search Term:'))

            line_edit_search_term.show()

            list_search_terms.hide()
            list_search_terms.button_add.hide()
            list_search_terms.button_remove.hide()
            list_search_terms.button_clear.hide()
            list_search_terms.button_import.hide()
            list_search_terms.button_export.hide()

    label_search_term = QLabel(main.tr('Search Term:'), main)
    checkbox_multi_search_mode = QCheckBox(main.tr('Multi-search Mode'), main)
    line_edit_search_term = QLineEdit(main)
    list_search_terms = wordless_list.Wordless_List_Search_Terms(main)

    checkbox_ignore_case = QCheckBox(main.tr('Ignore Case'), main)
    checkbox_match_inflected_forms = QCheckBox(main.tr('Match All Inflected Forms'), main)
    checkbox_match_whole_word = QCheckBox(main.tr('Match Whole Word Only'), main)
    checkbox_use_regex = QCheckBox(main.tr('Use Regular Expression'), main)

    checkbox_multi_search_mode.stateChanged.connect(multi_search_mode_changed)

    multi_search_mode_changed()

    return (label_search_term, checkbox_multi_search_mode, line_edit_search_term, list_search_terms,
            checkbox_ignore_case, checkbox_match_inflected_forms, checkbox_match_whole_word, checkbox_use_regex)

def wordless_widgets_search_settings(main, tab):
    def multi_search_mode_changed():
        if checkbox_multi_search_mode.isChecked():
            label_search_term.setText(main.tr('Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.count() == 0:
                list_search_terms.add_item(line_edit_search_term.text())

            line_edit_search_term.hide()

            list_search_terms.show()
            list_search_terms.button_add.show()
            list_search_terms.button_remove.show()
            list_search_terms.button_clear.show()
            list_search_terms.button_import.show()
            list_search_terms.button_export.show()
        else:
            label_search_term.setText(main.tr('Search Term:'))

            line_edit_search_term.show()

            list_search_terms.hide()
            list_search_terms.button_add.hide()
            list_search_terms.button_remove.hide()
            list_search_terms.button_clear.hide()
            list_search_terms.button_import.hide()
            list_search_terms.button_export.hide()

    def match_tags_changed():
        if checkbox_match_tags.isChecked():
            checkbox_match_inflected_forms.setEnabled(False)

            checkbox_ignore_tags.hide()
            combo_box_ignore_tags.hide()

            checkbox_ignore_tags_match_tags.show()
            combo_box_ignore_tags_match_tags.show()
        else:
            checkbox_match_inflected_forms.setEnabled(True)
            
            checkbox_ignore_tags_match_tags.hide()
            combo_box_ignore_tags_match_tags.hide()

            checkbox_ignore_tags.show()
            combo_box_ignore_tags.show()

    def token_settings_changed():
        token_settings = main.settings_custom[tab]['token_settings']
        
        if line_edit_search_term.isEnabled() == True:
            combo_box_ignore_tags.blockSignals(True)

            combo_box_ignore_tags.clear()

            if token_settings['tags_only']:
                combo_box_ignore_tags.addItems([
                    main.tr('POS'),
                    main.tr('Non-POS')
                ])

                checkbox_match_tags.setEnabled(False)

                if token_settings['ignore_tags_tags_only']:
                    checkbox_ignore_tags.setEnabled(False)
                    checkbox_ignore_tags_match_tags.setEnabled(False)
                    combo_box_ignore_tags.setEnabled(False)
                    combo_box_ignore_tags_match_tags.setEnabled(False)
                else:
                    checkbox_ignore_tags.setEnabled(True)
                    checkbox_ignore_tags_match_tags.setEnabled(True)
                    combo_box_ignore_tags.setEnabled(True)
                    combo_box_ignore_tags_match_tags.setEnabled(True)
            else:
                combo_box_ignore_tags.addItems([
                    main.tr('All'),
                    main.tr('POS'),
                    main.tr('Non-POS')
                ])

                if token_settings['ignore_tags']:
                    if token_settings['ignore_tags_type'] == main.tr('All'):
                        checkbox_ignore_tags.setEnabled(False)
                        checkbox_ignore_tags_match_tags.setEnabled(False)
                        combo_box_ignore_tags.setEnabled(False)
                        combo_box_ignore_tags_match_tags.setEnabled(False)
                        checkbox_match_tags.setEnabled(False)
                    else:
                        if checkbox_match_tags.isChecked():
                            checkbox_ignore_tags.setEnabled(False)
                            checkbox_ignore_tags_match_tags.setEnabled(False)
                            combo_box_ignore_tags.setEnabled(False)
                            combo_box_ignore_tags_match_tags.setEnabled(False)
                        else:
                            checkbox_ignore_tags.setEnabled(True)
                            checkbox_ignore_tags_match_tags.setEnabled(True)
                            combo_box_ignore_tags.setEnabled(True)
                            combo_box_ignore_tags_match_tags.setEnabled(True)
                            
                        checkbox_match_tags.setEnabled(True)
                else:
                    checkbox_ignore_tags.setEnabled(True)
                    checkbox_ignore_tags_match_tags.setEnabled(True)
                    combo_box_ignore_tags.setEnabled(True)
                    combo_box_ignore_tags_match_tags.setEnabled(True)
                    checkbox_match_tags.setEnabled(True)

            combo_box_ignore_tags.blockSignals(False)

            if checkbox_match_tags.isEnabled():
                match_tags_changed()
            else:
                checkbox_match_inflected_forms.setEnabled(False)

    label_search_term = QLabel(main.tr('Search Term:'), main)
    checkbox_multi_search_mode = QCheckBox(main.tr('Multi-search Mode'), main)
    line_edit_search_term = QLineEdit(main)
    list_search_terms = wordless_list.Wordless_List_Search_Terms(main)
    label_separator = wordless_label.Wordless_Label_Hint(main.tr('''
                                                             <p>* Use space to separate multiple tokens</p>
                                                         '''), main)

    checkbox_ignore_case = QCheckBox(main.tr('Ignore Case'), main)
    checkbox_match_inflected_forms = QCheckBox(main.tr('Match All Inflected Forms'), main)
    checkbox_match_whole_word = QCheckBox(main.tr('Match Whole Word Only'), main)
    checkbox_use_regex = QCheckBox(main.tr('Use Regular Expression'), main)

    checkbox_ignore_tags = QCheckBox(main.tr('Ignore'), main)
    checkbox_ignore_tags_match_tags = QCheckBox(main.tr('Ignore'), main)
    combo_box_ignore_tags = wordless_box.Wordless_Combo_Box(main)
    combo_box_ignore_tags_match_tags = wordless_box.Wordless_Combo_Box(main)
    label_ignore_tags = QLabel(main.tr('Tags'), main)
    checkbox_match_tags = QCheckBox(main.tr('Match Tags Only'), main)

    combo_box_ignore_tags.addItems([
        main.tr('All'),
        main.tr('POS'),
        main.tr('Non-POS')
    ])

    combo_box_ignore_tags_match_tags.addItems([
        main.tr('POS'),
        main.tr('Non-POS')
    ])

    checkbox_match_tags.token_settings_changed = token_settings_changed

    checkbox_multi_search_mode.stateChanged.connect(multi_search_mode_changed)
    checkbox_match_tags.stateChanged.connect(match_tags_changed)

    multi_search_mode_changed()
    match_tags_changed()
    #token_settings_changed()

    return (label_search_term,
            checkbox_multi_search_mode,
            line_edit_search_term,
            list_search_terms,
            label_separator,

            checkbox_ignore_case,
            checkbox_match_inflected_forms,
            checkbox_match_whole_word,
            checkbox_use_regex,

            checkbox_ignore_tags,
            checkbox_ignore_tags_match_tags,
            combo_box_ignore_tags,
            combo_box_ignore_tags_match_tags,
            label_ignore_tags,
            checkbox_match_tags)

def wordless_widgets_context_settings1(main, tab):
    label_context_settings = QLabel(main.tr('Context Settings:'), main)
    button_context_settings = QPushButton(main.tr('Settings...'), main)

    return label_context_settings, button_context_settings

def wordless_widgets_context_settings(main, tab):
    label_context_settings = QLabel(main.tr('Context Settings:'), main)
    button_context_settings = QPushButton(main.tr('Settings...'), main)

    main.__dict__[f'wordless_context_settings_{tab}'] = wordless_dialog.Wordless_Dialog_Context_Settings(main, tab = tab)

    button_context_settings.clicked.connect(main.__dict__[f'wordless_context_settings_{tab}'].load)

    return label_context_settings, button_context_settings

# Generation Settings
def wordless_widgets_size(main, size_min = 1, size_max = 100):
    def size_sync_changed():
        if checkbox_size_sync.isChecked():
            spin_box_size_min.setValue(spin_box_size_max.value())

    def size_min_changed():
        if checkbox_size_sync.isChecked() or spin_box_size_min.value() > spin_box_size_max.value():
            spin_box_size_max.setValue(spin_box_size_min.value())

    def size_max_changed():
        if checkbox_size_sync.isChecked() or spin_box_size_min.value() > spin_box_size_max.value():
            spin_box_size_min.setValue(spin_box_size_max.value())

    checkbox_size_sync = QCheckBox(main.tr('Sync'), main)
    label_size_min = QLabel(main.tr('From'), main)
    spin_box_size_min = QSpinBox(main)
    label_size_max = QLabel(main.tr('To'), main)
    spin_box_size_max = QSpinBox(main)

    spin_box_size_min.setRange(size_min, size_max)
    spin_box_size_max.setRange(size_min, size_max)

    checkbox_size_sync.stateChanged.connect(size_sync_changed)
    spin_box_size_min.valueChanged.connect(size_min_changed)
    spin_box_size_max.valueChanged.connect(size_max_changed)

    size_sync_changed()
    size_min_changed()
    size_max_changed()

    return checkbox_size_sync, label_size_min, spin_box_size_min, label_size_max, spin_box_size_max

def wordless_widgets_window(main):
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

    checkbox_window_sync = QCheckBox(main.tr('Sync'), main)
    label_window_left = QLabel(main.tr('From'), main)
    spin_box_window_left = wordless_box.Wordless_Spin_Box_Window(main)
    label_window_right = QLabel(main.tr('To'), main)
    spin_box_window_right = wordless_box.Wordless_Spin_Box_Window(main)

    spin_box_window_left.setRange(-100, 100)
    spin_box_window_right.setRange(-100, 100)

    checkbox_window_sync.stateChanged.connect(window_sync_changed)
    spin_box_window_left.valueChanged.connect(window_left_changed)
    spin_box_window_right.valueChanged.connect(window_right_changed)

    window_sync_changed()
    window_left_changed()
    window_right_changed()

    return checkbox_window_sync, label_window_left, spin_box_window_left, label_window_right, spin_box_window_right

def wordless_widgets_measure_dispersion(main):
    label_measure_dispersion = QLabel(main.tr('Measure of Dispersion:'), main)
    combo_box_measure_dispersion = wordless_box.Wordless_Combo_Box(main)

    combo_box_measure_dispersion.addItems(list(main.settings_global['measures_dispersion'].keys()))

    return (label_measure_dispersion,
            combo_box_measure_dispersion)

def wordless_widgets_measure_adjusted_freq(main):
    label_measure_adjusted_freq = QLabel(main.tr('Measure of Adjusted Frequency:'), main)
    combo_box_measure_adjusted_freq = wordless_box.Wordless_Combo_Box(main)

    combo_box_measure_adjusted_freq.addItems(list(main.settings_global['measures_adjusted_freq'].keys()))

    return (label_measure_adjusted_freq,
            combo_box_measure_adjusted_freq)

def wordless_widgets_test_significance(main):
    label_test_significance = QLabel(main.tr('Test of Statistical Significance:'), main)
    combo_box_test_significance = wordless_box.Wordless_Combo_Box(main)

    return (label_test_significance,
            combo_box_test_significance)

def wordless_widgets_measure_effect_size(main):
    label_measure_effect_size = QLabel(main.tr('Measure of Effect Size:'), main)
    combo_box_measure_effect_size = wordless_box.Wordless_Combo_Box(main)

    return (label_measure_effect_size,
            combo_box_measure_effect_size)

def wordless_widgets_settings_measures(main, tab):
    label_settings_measures = QLabel(main.tr('Advanced Settings:'), main)
    button_settings_measures = QPushButton(main.tr('Settings...'), main)

    button_settings_measures.clicked.connect(lambda: main.wordless_settings.load(tab = tab))

    return label_settings_measures, button_settings_measures

# Table Settings
def wordless_widgets_table_settings(main, table):
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

    checkbox_show_pct = QCheckBox(main.tr('Show Percentage Data'), main)
    checkbox_show_cumulative = QCheckBox(main.tr('Show Cumulative Data'), main)
    checkbox_show_breakdown = QCheckBox(main.tr('Show Breakdown by File'), main)

    checkbox_show_pct.stateChanged.connect(show_pct_changed)
    checkbox_show_cumulative.stateChanged.connect(show_cumulative_changed)
    checkbox_show_breakdown.stateChanged.connect(show_breakdown_changed)

    show_pct_changed()
    show_cumulative_changed()
    show_breakdown_changed()

    return checkbox_show_pct, checkbox_show_cumulative, checkbox_show_breakdown

# Plot Settings
def wordless_widgets_plot_settings(main):
    def plot_type_changed():
        if combo_box_plot_type.currentText() == main.tr('Line Chart'):
            combo_box_use_file.setEnabled(False)

            use_data_changed()
        elif combo_box_plot_type.currentText() == main.tr('Word Cloud'):
            combo_box_use_file.setEnabled(True)

            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)

    def use_data_changed():
        if combo_box_plot_type.currentText() == main.tr('Line Chart'):
            if combo_box_use_data.currentText() == main.tr('Frequency'):
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

        combo_box_use_file.addItem(main.tr('Total'))

        if use_file_old and combo_box_use_file.findText(use_file_old) > -1:
            combo_box_use_file.setCurrentText(use_file_old)

    label_plot_type = QLabel(main.tr('Plot Type:'), main)
    combo_box_plot_type = wordless_box.Wordless_Combo_Box(main)
    label_use_file = QLabel(main.tr('Use File:'), main)
    combo_box_use_file = wordless_box.Wordless_Combo_Box(main)
    label_use_data = QLabel(main.tr('Use Data:'), main)
    combo_box_use_data = wordless_box.Wordless_Combo_Box(main)

    checkbox_use_pct = QCheckBox(main.tr('Use Percentage Data'), main)
    checkbox_use_cumulative = QCheckBox(main.tr('Use Cumulative Data'), main)

    combo_box_plot_type.addItems([main.tr('Line Chart'),
                                  main.tr('Word Cloud')])

    combo_box_plot_type.currentTextChanged.connect(plot_type_changed)
    combo_box_use_data.currentTextChanged.connect(use_data_changed)

    main.wordless_files.table.itemChanged.connect(wordless_files_changed)

    combo_box_use_file.wordless_files_changed = wordless_files_changed

    plot_type_changed()
    use_data_changed()
    wordless_files_changed()

    return (label_plot_type, combo_box_plot_type,
            label_use_file, combo_box_use_file,
            label_use_data, combo_box_use_data,
            checkbox_use_pct, checkbox_use_cumulative)

# Filter Settings
def wordless_widgets_filter(main, filter_min, filter_max):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    label_min = QLabel(main.tr('From'), main)
    (spin_box_min,
     checkbox_min_no_limit) = wordless_widgets_no_limit(main)

    label_max = QLabel(main.tr('To'), main)
    (spin_box_max,
     checkbox_max_no_limit) = wordless_widgets_no_limit(main)

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    min_changed()
    max_changed()

    return (label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit)

def wordless_widgets_filter_measures(main, filter_min = -10000, filter_max = 10000):
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

    label_min = QLabel(main.tr('From'), main)
    (spin_box_min,
     checkbox_min_no_limit) = wordless_widgets_no_limit(main, double = True)

    label_max = QLabel(main.tr('To'), main)
    (spin_box_max,
     checkbox_max_no_limit) = wordless_widgets_no_limit(main, double = True)

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

def wordless_widgets_filter_p_value(main):
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

    label_min = QLabel(main.tr('From'), main)
    (spin_box_min,
     checkbox_min_no_limit) = wordless_widgets_no_limit(main, double = True)

    label_max = QLabel(main.tr('To'), main)
    (spin_box_max,
     checkbox_max_no_limit) = wordless_widgets_no_limit(main, double = True)

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

def wordless_widgets_filter_results(main, table):
    def table_item_changed():
        if combo_box_filter_file.count() == 1:
            file_old = ''
        else:
            file_old = combo_box_filter_file.currentText()

        combo_box_filter_file.clear()

        for file in table.settings['files']['files_open']:
            if file['selected']:
                combo_box_filter_file.addItem(file['name'])

        combo_box_filter_file.addItem(main.tr('Total'))

        if combo_box_filter_file.findText(file_old) > -1:
            combo_box_filter_file.setCurrentText(file_old)

    label_filter_file = QLabel(main.tr('Filter File:'), main)
    combo_box_filter_file = wordless_box.Wordless_Combo_Box(main)
    button_filter_results = QPushButton(main.tr('Filter Results in Table'), main)

    button_filter_results.clicked.connect(lambda: table.update_filters())

    table.itemChanged.connect(table_item_changed)

    table_item_changed()

    return (label_filter_file, combo_box_filter_file,
            button_filter_results)

# Settings -> Measures
def wordless_widgets_number_sections(parent):
    label_divide = QLabel(parent.tr('Divide each text into'), parent)
    spin_box_number_sections = QSpinBox(parent)
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
