#
# Wordless: Utility Function for GUI Widgets
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import nltk

from wordless_utils import wordless_list

# Text Editor
class Wordless_Text_Edit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.document().adjustSize()
        
        self.setFixedHeight(self.document().size().height() + 20)

# Combo Box
class Wordless_Combo_Box(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.setMaxVisibleItems(25)

class Wordless_Combo_Box_Lang(Wordless_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(sorted(parent.file_langs))

class Wordless_Combo_Box_Encoding(Wordless_Combo_Box):
    def __init__(self, parent):
        super().__init__(parent)

        self.addItems(parent.file_encodings)

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

def wordless_widgets_token_settings(parent):
    def words_changed():
        checkbox_words.setTristate(False)

        if checkbox_words.isChecked():
            checkbox_lowercase.setChecked(True)
            checkbox_uppercase.setChecked(True)
            checkbox_title_cased.setChecked(True)

            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_cased.setEnabled(True)
        else:
            checkbox_lowercase.setChecked(False)
            checkbox_uppercase.setChecked(False)
            checkbox_title_cased.setChecked(False)

            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_cased.setEnabled(False)

    def case_changed():
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
        else:
            checkbox_words.setCheckState(Qt.PartiallyChecked)

    checkbox_words = QCheckBox(parent.tr('Words'), parent)
    checkbox_lowercase = QCheckBox(parent.tr('Lowercase'), parent)
    checkbox_uppercase = QCheckBox(parent.tr('Uppercase'), parent)
    checkbox_title_cased = QCheckBox(parent.tr('Title Cased'), parent)
    checkbox_numerals = QCheckBox(parent.tr('Numerals'), parent)
    checkbox_punctuations = QCheckBox(parent.tr('Punctuations'), parent)

    checkbox_words.clicked.connect(words_changed)
    checkbox_lowercase.clicked.connect(case_changed)
    checkbox_uppercase.clicked.connect(case_changed)
    checkbox_title_cased.clicked.connect(case_changed)

    words_changed()
    case_changed()

    return [checkbox_words, checkbox_lowercase, checkbox_uppercase, checkbox_title_cased,
            checkbox_numerals, checkbox_punctuations]

def wordless_widgets_search_settings(parent):
    def multi_search_changed():
        if checkbox_multi_search.isChecked():
            label_search_term.setText(parent.tr('Search Terms:'))

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
            label_search_term.setText(parent.tr('Search Term:'))

            line_edit_search_term.show()

            list_search_terms.hide()
            list_search_terms.button_add.hide()
            list_search_terms.button_insert.hide()
            list_search_terms.button_remove.hide()
            list_search_terms.button_clear.hide()
            list_search_terms.button_import.hide()
            list_search_terms.button_export.hide()

    def show_all_changed():
        if checkbox_show_all.isChecked():
            checkbox_lemmatization.setText(parent.tr('Lemmatization'))

            line_edit_search_term.setEnabled(False)
            list_search_terms.setEnabled(False)

            checkbox_whole_word.setEnabled(False)
            checkbox_regex.setEnabled(False)
            checkbox_multi_search.setEnabled(False)
        else:
            checkbox_lemmatization.setText(parent.tr('Match All Lemmatized Forms'))

            line_edit_search_term.setEnabled(True)
            list_search_terms.setEnabled(True)

            checkbox_whole_word.setEnabled(True)
            checkbox_regex.setEnabled(True)
            checkbox_multi_search.setEnabled(True)

    label_search_term = QLabel(parent.tr('Search Term:'), parent)
    line_edit_search_term = QLineEdit(parent)
    list_search_terms = wordless_list.Wordless_List(parent)

    checkbox_ignore_case = QCheckBox(parent.tr('Ignore Case'), parent)
    checkbox_lemmatization = QCheckBox(parent.tr('Lemmatization'), parent)
    checkbox_whole_word = QCheckBox(parent.tr('Match Whole Word Only'), parent)
    checkbox_regex = QCheckBox(parent.tr('Use Regular Expression'), parent)
    checkbox_multi_search = QCheckBox(parent.tr('Multi-search Mode'), parent)
    checkbox_show_all = QCheckBox(parent.tr('Show All Items'), parent)

    checkbox_show_all.setChecked(True)

    checkbox_multi_search.stateChanged.connect(multi_search_changed)
    checkbox_show_all.stateChanged.connect(show_all_changed)

    multi_search_changed()
    show_all_changed()

    return (label_search_term, line_edit_search_term, list_search_terms,
            checkbox_ignore_case, checkbox_lemmatization, checkbox_whole_word, checkbox_regex,
            checkbox_multi_search, checkbox_show_all)

def wordless_widgets_table_settings(parent, table):
    def show_pct_changed():
        if table.item(0, 0) or table.cellWidget(0, 0):
            cols_cumulative = table.find_columns_cumulative()
            col_files_found = table.find_column(parent.tr('Files Found'))
            show_pct = checkbox_show_pct.isChecked()

            table.hide()
            table.setSortingEnabled(False)

            for col in table.cols_pct:
                if col in cols_cumulative:
                    total = sum([table.item(row, col - 1).raw_value
                                 for row in range(table.rowCount())
                                 if not table.isRowHidden(row)])
                elif col == col_files_found:
                    total = table.item(0, col_files_found).raw_total
                else:
                    total = sum([table.item(row, col).raw_value
                                 for row in range(table.rowCount())
                                 if not table.isRowHidden(row)])

                for row in range(table.rowCount()):
                    value = table.item(row, col).raw_value

                    table.set_item_with_pct(row, col, value, total, show_pct = show_pct)

            table.setSortingEnabled(True)
            table.show()

    def show_cumulative_changed():
        cols_cumulative = table.find_columns_cumulative()
        cols_breakdown = table.find_columns_breakdown()

        table.hide()

        for col in cols_cumulative:
            if checkbox_show_cumulative.isChecked():
                if checkbox_show_breakdown.isChecked() or col not in cols_breakdown:
                    table.showColumn(col)
            else:
                table.hideColumn(col)

        table.show()

    def show_breakdown_changed():
        cols_cumulative = table.find_columns_cumulative()
        cols_breakdown = table.find_columns_breakdown()

        table.hide()

        for col in cols_breakdown:
            if checkbox_show_breakdown.isChecked():
                if checkbox_show_cumulative.isChecked() or col not in cols_cumulative:
                    table.showColumn(col)
            else:
                table.hideColumn(col)

        table.show()

    checkbox_show_pct = QCheckBox(parent.tr('Show Percentage'), parent)
    checkbox_show_cumulative = QCheckBox(parent.tr('Show Cumulative Data'), parent)
    checkbox_show_breakdown = QCheckBox(parent.tr('Show Breakdown'), parent)

    checkbox_show_pct.stateChanged.connect(show_pct_changed)
    checkbox_show_cumulative.stateChanged.connect(show_cumulative_changed)
    checkbox_show_breakdown.stateChanged.connect(show_breakdown_changed)

    show_pct_changed()
    show_cumulative_changed()
    show_breakdown_changed()

    return [checkbox_show_pct, checkbox_show_cumulative, checkbox_show_breakdown]

def wordless_widgets_filter(parent, filter_min = 1, filter_max = 100, table = None, column = ''):
    def filter_changed():
        if checkbox_no_limit.isChecked():
            spin_box_max.setEnabled(False)
        else:
            spin_box_max.setEnabled(True)

        if table and (table.item(0, 0) or table.cellWidget(0, 0)):
            if column == 'Total':
                col_filter = table.find_column(combo_box_apply_to.currentText(), fuzzy_search = True)
            else:
                col_filter = table.find_column(column)

            filter_type = type(table.item(0, col_filter).read_data())
            filter_min = spin_box_min.value()
            filter_max = spin_box_max.value() if not checkbox_no_limit.isChecked() else float('inf')

            table.setUpdatesEnabled(False)

            for i in range(table.rowCount()):
                filter_data = table.item(i, col_filter).read_data()

                if filter_type in [int, float]:
                    if filter_min <= filter_data <= filter_max:
                        table.showRow(i)
                    else:
                        table.hideRow(i)
                elif filter_type == str:
                    if filter_min <= len(filter_data) - filter_data.count(' ') <= filter_max:
                        table.showRow(i)
                    else:
                        table.hideRow(i)

            table.sorting_changed(table.horizontalHeader().sortIndicatorSection(),
                                  table.horizontalHeader().sortIndicatorOrder())

            table.setUpdatesEnabled(True)

    checkbox_no_limit = QCheckBox(parent.tr('No Limit'), parent)
    label_min = QLabel(parent.tr('From'), parent)
    spin_box_min = QSpinBox(parent)
    label_max = QLabel(parent.tr('To'), parent)
    spin_box_max = QSpinBox(parent)

    if column == 'Total':
        label_apply_to = QLabel(parent.tr('Apply to:'), parent)
        combo_box_apply_to = QComboBox(parent)

        combo_box_apply_to.addItem('Total')

        combo_box_apply_to.currentTextChanged.connect(filter_changed)

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    checkbox_no_limit.stateChanged.connect(filter_changed)
    spin_box_min.editingFinished.connect(filter_changed)
    spin_box_max.editingFinished.connect(filter_changed)

    filter_changed()

    if column == 'Total':
        return [checkbox_no_limit, label_min, spin_box_min, label_max, spin_box_max, label_apply_to, combo_box_apply_to]
    else:
        return [checkbox_no_limit, label_min, spin_box_min, label_max, spin_box_max]

def wordless_widgets_size(parent, size_min = 1, size_max = 20):
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
    spin_box_size_min = QSpinBox(parent)
    label_size_max = QLabel(parent.tr('To'), parent)
    spin_box_size_max = QSpinBox(parent)

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

    checkbox_window_sync = QCheckBox(parent.tr('Sync'), parent)
    label_window_left = QLabel(parent.tr('From'), parent)
    spin_box_window_left = Wordless_Spin_Box_Window(parent)
    label_window_right = QLabel(parent.tr('To'), parent)
    spin_box_window_right = Wordless_Spin_Box_Window(parent)

    spin_box_window_left.setRange(-100, 100)
    spin_box_window_right.setRange(-100, 100)

    checkbox_window_sync.stateChanged.connect(window_sync_changed)
    spin_box_window_left.valueChanged.connect(window_left_changed)
    spin_box_window_right.valueChanged.connect(window_right_changed)

    window_sync_changed()
    window_left_changed()
    window_right_changed()

    return [checkbox_window_sync, label_window_left, spin_box_window_left, label_window_right, spin_box_window_right]

def wordless_widgets_collocation(parent, default_assoc_measure):
    def search_for_changed():
        text_old = combobox_assoc_measure.currentText()

        combobox_assoc_measure.clear()
    
        if combo_box_search_for.currentText() == parent.tr('Bigrams'):
            combobox_assoc_measure.addItems(parent.assoc_measures_bigram)
        elif combo_box_search_for.currentText() == parent.tr('Trigrams'):
            combobox_assoc_measure.addItems(parent.assoc_measures_trigram)
        elif combo_box_search_for.currentText() == parent.tr('Quadgrams'):
            combobox_assoc_measure.addItems(parent.assoc_measures_quadgram)

        for i in range(combobox_assoc_measure.count()):
            if combobox_assoc_measure.itemText(i) == text_old:
                combobox_assoc_measure.setCurrentIndex(i)

                break
            else:
                combobox_assoc_measure.setCurrentText(default_assoc_measure)

    label_search_for = QLabel(parent.tr('Search for:'), parent)
    combo_box_search_for = QComboBox(parent)
    label_assoc_measure = QLabel(parent.tr('Association Measure:'), parent)
    combobox_assoc_measure = QComboBox(parent)

    combo_box_search_for.addItems([
        parent.tr('Bigrams'),
        parent.tr('Trigrams'),
        parent.tr('Quadgrams')
    ])

    combo_box_search_for.currentTextChanged.connect(search_for_changed)

    search_for_changed()

    return [label_search_for, combo_box_search_for, label_assoc_measure, combobox_assoc_measure]
