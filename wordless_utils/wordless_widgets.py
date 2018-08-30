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

class Wordless_Scroll_Area(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)

        self.setBackgroundRole(QPalette.Light)

class Wordless_Text_Edit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.document().adjustSize()
        
        self.setFixedHeight(self.document().size().height() + 20)

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
    def words_settings_changed():
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

    def case_settings_changed():
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

    checkbox_words.clicked.connect(words_settings_changed)
    checkbox_lowercase.clicked.connect(case_settings_changed)
    checkbox_uppercase.clicked.connect(case_settings_changed)
    checkbox_title_cased.clicked.connect(case_settings_changed)

    words_settings_changed()
    case_settings_changed()

    return [checkbox_words, checkbox_lowercase, checkbox_uppercase, checkbox_title_cased,
            checkbox_numerals, checkbox_punctuations]

def wordless_widgets_search_settings(parent, widgets = list(range(9))):
    def search_settings_changed():
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

    checkbox_multi_search.stateChanged.connect(search_settings_changed)
    checkbox_show_all.stateChanged.connect(search_settings_changed)

    search_settings_changed()

    widgets_all = [
        label_search_term, line_edit_search_term, list_search_terms,
        checkbox_ignore_case, checkbox_lemmatization, checkbox_whole_word, checkbox_regex,
        checkbox_multi_search, checkbox_show_all
    ]

    for i, widget in enumerate(widgets_all):
        if i not in widgets:
            widget.hide()

    return [widgets_all[i] for i in widgets]

def wordless_widgets_display_settings(parent, table):
    def display_settings_changed():
        col_cumulative = [col
                          for col in range(table.columnCount())
                          if table.horizontalHeaderItem(col).text().find(parent.tr('Cumulative')) > -1]

        for col in col_cumulative:
            if checkbox_show_cumulative.isChecked():
                table.showColumn(col)
            else:
                table.hideColumn(col)

        # Search for the end index of breakdown
        for col in col_cumulative:
            if table.horizontalHeaderItem(col).text().find(parent.tr('Total')) > -1:
                col_breakdown = col - 2

                break

        for col in range(2, col_breakdown + 1):
            if checkbox_show_breakdown.isChecked():
                if col not in col_cumulative:
                    table.showColumn(col)
            else:
                table.hideColumn(col)

    checkbox_show_pct = QCheckBox(parent.tr('Show Percentage'), parent)
    checkbox_show_cumulative = QCheckBox(parent.tr('Show Cumulative Data'), parent)
    checkbox_show_breakdown = QCheckBox(parent.tr('Show Breakdown'), parent)

    checkbox_show_cumulative.stateChanged.connect(display_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(display_settings_changed)

    display_settings_changed()

    return [checkbox_show_pct, checkbox_show_cumulative, checkbox_show_breakdown]

def wordless_widgets_filter_settings(parent):
    def filter_settings_changed():
        if checkbox_no_limit.isChecked():
            spin_box_max.setEnabled(False)
        else:
            spin_box_max.setEnabled(True)

    checkbox_no_limit = QCheckBox(parent.tr('No Limit'), parent)
    label_min = QLabel(parent.tr('From'), parent)
    spin_box_min = QSpinBox(parent)
    label_max = QLabel(parent.tr('To'), parent)
    spin_box_max = QSpinBox(parent)

    checkbox_no_limit.stateChanged.connect(filter_settings_changed)

    filter_settings_changed()

    return [checkbox_no_limit, label_min, spin_box_min, label_max, spin_box_max]

def wordless_widgets_collocation(parent, default_assoc_measure):
    def ngram_changed():
        text_old = assoc_measures.currentText()

        assoc_measures.clear()
    
        if ngram.currentText() == parent.tr('Bigrams'):
            assoc_measures.addItems(parent.assoc_measures_bigram)
        elif ngram.currentText() == parent.tr('Trigrams'):
            assoc_measures.addItems(parent.assoc_measures_trigram)
        elif ngram.currentText() == parent.tr('Quadgrams'):
            assoc_measures.addItems(parent.assoc_measures_quadgram)

        for i in range(assoc_measures.count()):
            if assoc_measures.itemText(i) == text_old:
                assoc_measures.setCurrentIndex(i)

                break
            else:
                assoc_measures.setCurrentText(default_assoc_measure)

    ngram = QComboBox(parent)
    assoc_measures = QComboBox(parent)

    ngram.addItems([
        parent.tr('Bigrams'),
        parent.tr('Trigrams'),
        parent.tr('Quadgrams')
    ])

    ngram.currentTextChanged.connect(ngram_changed)

    ngram_changed()

    return ngram, assoc_measures

def wordless_widgets_window(parent):
    def sync_changed():
        if window_sync.isChecked():
            window_left.setPrefix(window_right.prefix())
            window_left.setValue(window_right.value())

    def left_changed():
        if window_sync.isChecked():
            window_right.setPrefix(window_left.prefix())
            window_right.setValue(window_left.value())
        else:
            if (window_left.prefix() == 'L' and window_right.prefix() == 'L' and
                window_left.value() < window_right.value() or
                window_left.prefix() == 'R' and window_right.prefix() == 'R' and
                window_left.value() > window_right.value() or
                window_left.prefix() == 'R' and window_right.prefix() == 'L'):
                window_right.setPrefix(window_left.prefix())
                window_right.setValue(window_left.value())

    def right_changed():
        if window_sync.isChecked():
            window_left.setPrefix(window_right.prefix())
            window_left.setValue(window_right.value())
        else:
            if (window_left.prefix() == 'L' and window_right.prefix() == 'L' and
                window_left.value() < window_right.value() or
                window_left.prefix() == 'R' and window_right.prefix() == 'R' and
                window_left.value() > window_right.value() or
                window_left.prefix() == 'R' and window_right.prefix() == 'L'):
                window_left.setPrefix(window_right.prefix())
                window_left.setValue(window_right.value())

    window_sync = QCheckBox(parent.tr('Sync'), parent)
    window_left = Wordless_Spin_Box_Window(parent)
    window_right = Wordless_Spin_Box_Window(parent)

    window_sync.stateChanged.connect(sync_changed)
    window_left.valueChanged.connect(left_changed)
    window_right.valueChanged.connect(right_changed)

    sync_changed()
    left_changed()
    right_changed()

    return window_sync, window_left, window_right
