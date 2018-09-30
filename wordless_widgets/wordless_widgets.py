#
# Wordless: Widgets
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_widgets import wordless_list

# Combo Box
class Wordless_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setMaxVisibleItems(25)

class Wordless_Combo_Box_Lang(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.addItems(sorted(main.settings_global['langs']))

class Wordless_Combo_Box_Encoding(Wordless_Combo_Box):
    def __init__(self, main):
        super().__init__(main)

        self.addItems(main.settings_global['file_encodings'])

# Spin Box
class Wordless_Spin_Box_Window(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setRange(-100, 100)

        self.valueChanged.connect(self.value_changed)

    def stepBy(self, steps):
        if self.prefix() == 'L':
            super().stepBy(-steps)
        elif self.prefix() == 'R':
            super().stepBy(steps)

    def value_changed(self):
        if self.value() <= 0:
            if self.prefix() == 'L':
                self.setPrefix('R')
            else:
                self.setPrefix('L')

            self.setValue(-self.value() + 1)

def wordless_widgets_token(main):
    def words_changed():
        if checkbox_words.isChecked():
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_case.setEnabled(True)

            checkbox_treat_as_lowercase.setEnabled(True)
            checkbox_lemmatize.setEnabled(True)
            checkbox_filter_stop_words.setEnabled(True)
        else:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_case.setEnabled(False)

            checkbox_treat_as_lowercase.setEnabled(False)
            checkbox_lemmatize.setEnabled(False)
            checkbox_filter_stop_words.setEnabled(False)

        ignore_case_changed()

    def ignore_case_changed():
        if checkbox_treat_as_lowercase.isEnabled():
            if checkbox_treat_as_lowercase.isChecked():
                checkbox_lowercase.setEnabled(False)
                checkbox_uppercase.setEnabled(False)
                checkbox_title_case.setEnabled(False)
            else:
                checkbox_lowercase.setEnabled(True)
                checkbox_uppercase.setEnabled(True)
                checkbox_title_case.setEnabled(True)

    checkbox_words = QCheckBox(main.tr('Words'), main)
    checkbox_lowercase = QCheckBox(main.tr('Lowercase'), main)
    checkbox_uppercase = QCheckBox(main.tr('Uppercase'), main)
    checkbox_title_case = QCheckBox(main.tr('Title Case'), main)
    checkbox_treat_as_lowercase = QCheckBox(main.tr('Treat as All Lowercase'), main)
    checkbox_lemmatize = QCheckBox(main.tr('Lemmatize'), main)
    checkbox_filter_stop_words = QCheckBox(main.tr('Filter Stop Words'), main)

    checkbox_nums = QCheckBox(main.tr('Numerals'), main)
    checkbox_puncs = QCheckBox(main.tr('Punctuations'), main)

    checkbox_words.stateChanged.connect(words_changed)
    checkbox_treat_as_lowercase.stateChanged.connect(ignore_case_changed)

    words_changed()

    return [checkbox_words, checkbox_lowercase, checkbox_uppercase, checkbox_title_case,
            checkbox_treat_as_lowercase, checkbox_lemmatize, checkbox_filter_stop_words,
            checkbox_nums, checkbox_puncs]

def wordless_widgets_search(main):
    def show_all_changed():
        if checkbox_show_all.isChecked():
            line_edit_search_term.setEnabled(False)
            list_search_terms.setEnabled(False)
            list_search_terms.button_add.setEnabled(False)
            list_search_terms.button_insert.setEnabled(False)
            list_search_terms.button_remove.setEnabled(False)
            list_search_terms.button_clear.setEnabled(False)
            list_search_terms.button_import.setEnabled(False)
            list_search_terms.button_export.setEnabled(False)

            checkbox_ignore_case.setEnabled(False)
            checkbox_match_inflected_forms.setEnabled(False)
            checkbox_match_whole_word.setEnabled(False)
            checkbox_use_regex.setEnabled(False)
            checkbox_multi_search_mode.setEnabled(False)
        else:
            line_edit_search_term.setEnabled(True)
            list_search_terms.setEnabled(True)
            list_search_terms.button_add.setEnabled(True)
            list_search_terms.button_insert.setEnabled(True)
            list_search_terms.button_remove.setEnabled(True)
            list_search_terms.button_clear.setEnabled(True)
            list_search_terms.button_import.setEnabled(True)
            list_search_terms.button_export.setEnabled(True)

            checkbox_ignore_case.setEnabled(True)
            checkbox_match_inflected_forms.setEnabled(True)
            checkbox_match_whole_word.setEnabled(True)
            checkbox_use_regex.setEnabled(True)
            checkbox_multi_search_mode.setEnabled(True)

    def multi_search_changed():
        if checkbox_multi_search_mode.isChecked():
            label_search_term.setText(main.tr('Search Terms:'))

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
            label_search_term.setText(main.tr('Search Term:'))

            line_edit_search_term.show()

            list_search_terms.hide()
            list_search_terms.button_add.hide()
            list_search_terms.button_insert.hide()
            list_search_terms.button_remove.hide()
            list_search_terms.button_clear.hide()
            list_search_terms.button_import.hide()
            list_search_terms.button_export.hide()

    label_search_term = QLabel(main.tr('Search Term:'), main)
    checkbox_show_all = QCheckBox(main.tr('Show All Results'), main)
    line_edit_search_term = QLineEdit(main)
    list_search_terms = wordless_list.Wordless_List(main)

    checkbox_ignore_case = QCheckBox(main.tr('Ignore Case'), main)
    checkbox_match_inflected_forms = QCheckBox(main.tr('Match All Inflected Forms'), main)
    checkbox_match_whole_word = QCheckBox(main.tr('Match Whole Word Only'), main)
    checkbox_use_regex = QCheckBox(main.tr('Use Regular Expression'), main)
    checkbox_multi_search_mode = QCheckBox(main.tr('Multi-search Mode'), main)

    checkbox_show_all.stateChanged.connect(show_all_changed)
    checkbox_multi_search_mode.stateChanged.connect(multi_search_changed)

    show_all_changed()
    multi_search_changed()

    return (label_search_term, checkbox_show_all, line_edit_search_term, list_search_terms,
            checkbox_ignore_case, checkbox_match_inflected_forms, checkbox_match_whole_word, checkbox_use_regex,
            checkbox_multi_search_mode)

def wordless_widgets_table(main, table):
    def show_pct_changed():
        table.show_pct = checkbox_show_pct.isChecked()

        table.update_items_pct()

    def show_cumulative_changed():
        table.show_cumulative = checkbox_show_cumulative.isChecked()

        table.update_items_pct()

    def show_breakdown_changed():
        cols_breakdown = table.cols_breakdown

        table.setUpdatesEnabled(False)

        for col in cols_breakdown:
            if checkbox_show_breakdown.isChecked():
                table.showColumn(col)
            else:
                table.hideColumn(col)

        table.setUpdatesEnabled(True)

    checkbox_show_pct = QCheckBox(main.tr('Show Percentage'), main)
    checkbox_show_cumulative = QCheckBox(main.tr('Show Cumulative Data'), main)
    checkbox_show_breakdown = QCheckBox(main.tr('Show Breakdown'), main)

    checkbox_show_pct.stateChanged.connect(show_pct_changed)
    checkbox_show_cumulative.stateChanged.connect(show_cumulative_changed)
    checkbox_show_breakdown.stateChanged.connect(show_breakdown_changed)

    show_pct_changed()
    show_cumulative_changed()
    show_breakdown_changed()

    return [checkbox_show_pct, checkbox_show_cumulative, checkbox_show_breakdown]

def wordless_widgets_filter(main, filter_min = 1, filter_max = 100, table = None, col = '', apply_to = False):
    def filter_no_limit_changed():
        if checkbox_no_limit.isChecked():
            spin_box_max.setEnabled(False)
        else:
            spin_box_max.setEnabled(True)

    def filter_min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def filter_max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    def table_header_changed():
        apply_to_old = combo_box_apply_to.currentText()

        combo_box_apply_to.blockSignals(True)
        combo_box_apply_to.clear()

        for file in table.files:
            combo_box_apply_to.addItem(file['name'])
        combo_box_apply_to.addItem(main.tr('Total'))

        for i in range(combo_box_apply_to.count()):
            if combo_box_apply_to.itemText(i) == apply_to_old:
                combo_box_apply_to.setCurrentIndex(i)

                break

        combo_box_apply_to.blockSignals(False)

    checkbox_no_limit = QCheckBox(main.tr('No Limit'), main)
    label_min = QLabel(main.tr('From'), main)
    spin_box_min = QSpinBox(main)
    label_max = QLabel(main.tr('To'), main)
    spin_box_max = QSpinBox(main)

    if apply_to:
        label_apply_to = QLabel(main.tr('Apply to:'), main)
        combo_box_apply_to = QComboBox(main)

        table.horizontalHeader().sectionCountChanged.connect(table_header_changed)

        table_header_changed()

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    checkbox_no_limit.stateChanged.connect(filter_no_limit_changed)
    spin_box_min.valueChanged.connect(filter_min_changed)
    spin_box_max.valueChanged.connect(filter_max_changed)

    filter_no_limit_changed()
    filter_min_changed()
    filter_max_changed()

    if apply_to:
        return [checkbox_no_limit, label_min, spin_box_min, label_max, spin_box_max, label_apply_to, combo_box_apply_to]
    else:
        return [checkbox_no_limit, label_min, spin_box_min, label_max, spin_box_max]

def wordless_widgets_size(main, size_min = 1, size_max = 20):
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
            spin_box_window_left.setPrefix(window_right.prefix())
            spin_box_window_left.setValue(window_right.value())

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
    spin_box_window_left = Wordless_Spin_Box_Window(main)
    label_window_right = QLabel(main.tr('To'), main)
    spin_box_window_right = Wordless_Spin_Box_Window(main)

    spin_box_window_left.setRange(-100, 100)
    spin_box_window_right.setRange(-100, 100)

    checkbox_window_sync.stateChanged.connect(window_sync_changed)
    spin_box_window_left.valueChanged.connect(window_left_changed)
    spin_box_window_right.valueChanged.connect(window_right_changed)

    window_sync_changed()
    window_left_changed()
    window_right_changed()

    return [checkbox_window_sync, label_window_left, spin_box_window_left, label_window_right, spin_box_window_right]
