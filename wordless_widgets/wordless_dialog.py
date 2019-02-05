#
# Wordless: Widgets - Dialog
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import html

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_text import wordless_matching
from wordless_widgets import wordless_layout, wordless_message_box, wordless_table, wordless_widgets
from wordless_utils import wordless_misc, wordless_sorting

class Wordless_Dialog(QDialog):
    def __init__(self, main, title):
        super().__init__(main)

        self.main = main

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('imgs/wordless_icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def move_to_center(self):
        self.move((self.main.width() - self.width()) / 2,
                  (self.main.height() - self.height()) / 2,)

class Wordless_Dialog_Info(Wordless_Dialog):
    def __init__(self, main, title, width, height):
        super().__init__(main, title)

        self.setFixedSize(width, height)

        self.wrapper_info = QWidget(self)

        self.wrapper_info.setObjectName('wrapper-info')
        self.wrapper_info.setStyleSheet('''
            QWidget#wrapper-info {
                border-bottom: 1px solid #BBB;
                background-color: #FFF;
            }
        ''')

        self.wrapper_info.setLayout(QGridLayout())
        self.wrapper_info.layout().setContentsMargins(20, 10, 20, 10)

        self.wrapper_buttons = QWidget(self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_ok.clicked.connect(self.accept)

        self.wrapper_buttons.setLayout(QGridLayout())
        self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.wrapper_buttons.layout().setContentsMargins(11, 6, 11, 11)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)

class Wordless_Dialog_Search(Wordless_Dialog):
    def __init__(self, main, tab, table, cols_search):
        super().__init__(main, main.tr('Search in Results'))

        self.tab = tab
        self.table = table
        self.cols_search = self.table.find_col(cols_search)

        self.settings = self.main.settings_custom[self.tab]['search_results']

        (self.label_search_term,
         self.checkbox_multi_search_mode,
         self.line_edit_search_term,
         self.list_search_terms,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_word,
         self.checkbox_use_regex) = wordless_widgets.wordless_widgets_search_settings1(main)

        self.button_find_next = QPushButton(main.tr('Find Next'), main)
        self.button_find_prev = QPushButton(main.tr('Find Previous'), main)
        self.button_find_all = QPushButton(main.tr('Find All'), main)
        
        self.button_restore_default_settings = QPushButton(main.tr('Restore Default Settings'), main)
        self.button_close = QPushButton(main.tr('Close'), main)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.button_find_next.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_word.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.button_find_next.clicked.connect(lambda: self.find_next())
        self.button_find_prev.clicked.connect(lambda: self.find_prev())
        self.button_find_all.clicked.connect(lambda: self.find_all())

        self.button_restore_default_settings.clicked.connect(lambda: self.load_settings(defaults = True))
        self.button_close.clicked.connect(self.accept)

        layout_search_terms = QGridLayout()
        layout_search_terms.addWidget(self.list_search_terms, 0, 0, 5, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_add, 0, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_remove, 1, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_clear, 2, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_import, 3, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_export, 4, 1)

        layout_buttons_right = QGridLayout()
        layout_buttons_right.addWidget(self.button_find_next, 0, 0)
        layout_buttons_right.addWidget(self.button_find_prev, 1, 0)
        layout_buttons_right.addWidget(self.button_find_all, 2, 0)

        layout_buttons_right.setRowStretch(3, 1)

        layout_buttons_bottom = QGridLayout()
        layout_buttons_bottom.addWidget(self.button_restore_default_settings, 0, 0)
        layout_buttons_bottom.addWidget(self.button_close, 0, 1, Qt.AlignRight)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.label_search_term, 0, 0)
        self.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.line_edit_search_term, 1, 0, 1, 2)
        self.layout().addLayout(layout_search_terms, 2, 0, 1, 2)

        self.layout().addWidget(self.checkbox_ignore_case, 3, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_inflected_forms, 4, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_whole_word, 5, 0, 1, 2)
        self.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 2, 7, 1)

        self.layout().addLayout(layout_buttons_right, 0, 3, 7, 1)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 7, 0, 1, 4)

        self.layout().addLayout(layout_buttons_bottom, 8, 0, 1, 4)

        self.layout().setRowStretch(9, 1)

        self.main.tabs.currentChanged.connect(self.accept)

        self.load_settings()

        self.search_settings_changed()

    def closeEvent(self, event):
        self.clear_highlights()

        event.accept()

    def load_settings(self, defaults = False):
        if defaults:
            settings_loaded = copy.deepcopy(self.main.settings_default[self.tab]['search_results'])
        else:
            settings_loaded = copy.deepcopy(self.settings)

        if not defaults:
            self.line_edit_search_term.setText(settings_loaded['search_term'])

            for search_term in settings_loaded['search_terms']:
                self.list_search_terms.add_item(search_term)

        self.checkbox_ignore_case.setChecked(settings_loaded['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings_loaded['match_inflected_forms'])
        self.checkbox_match_whole_word.setChecked(settings_loaded['match_whole_word'])
        self.checkbox_use_regex.setChecked(settings_loaded['use_regex'])
        self.checkbox_multi_search_mode.setChecked(settings_loaded['multi_search_mode'])

    def search_settings_changed(self):
        self.settings['search_term'] = self.line_edit_search_term.text()
        self.settings['search_terms'] = self.list_search_terms.get_items()

        self.settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        self.settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        self.settings['match_whole_word'] = self.checkbox_match_whole_word.isChecked()
        self.settings['use_regex'] = self.checkbox_use_regex.isChecked()
        self.settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()

        if self.settings['multi_search_mode']:
            self.setFixedSize(345, 320)
        else:
            self.setFixedSize(345, 205)

    @ wordless_misc.log_timing
    def find_next(self):
        indexes_found = self.find_all()

        self.table.hide()
        self.table.blockSignals(True)

        # Scroll to the next found item
        if indexes_found:
            selected_rows = self.table.get_selected_rows()

            self.table.clearSelection()

            if selected_rows:
                for row, _ in indexes_found:
                    if row > selected_rows[-1]:
                        self.table.selectRow(row)
                        self.table.setFocus()

                        self.table.scrollToItem(self.table.item(row, 0))

                        break
            else:
                self.table.scrollToItem(self.table.item(indexes_found[0][0], 0))
                self.table.selectRow(indexes_found[0][0])

            # Scroll to top if this is the last item
            if not self.table.selectedItems():
                self.table.scrollToItem(self.table.item(indexes_found[0][0], 0))
                self.table.selectRow(indexes_found[0][0])

        self.table.blockSignals(False)
        self.table.show()

    @ wordless_misc.log_timing
    def find_prev(self):
        indexes_found = self.find_all()

        self.table.hide()
        self.table.blockSignals(True)

        # Scroll to the previous found item
        if indexes_found:
            selected_rows = self.table.get_selected_rows()

            self.table.clearSelection()

            if selected_rows:
                for row, _ in reversed(indexes_found):
                    if row < selected_rows[0]:
                        self.table.selectRow(row)
                        self.table.setFocus()

                        self.table.scrollToItem(self.table.item(row, 0))

                        break
            else:
                self.table.scrollToItem(self.table.item(indexes_found[-1][0], 0))
                self.table.selectRow(indexes_found[-1][0])

            # Scroll to top if no next items exist
            if not self.table.selectedItems():
                self.table.scrollToItem(self.table.item(indexes_found[-1][0], 0))
                self.table.selectRow(indexes_found[-1][0])

        self.table.blockSignals(False)
        self.table.show()

    @ wordless_misc.log_timing
    def find_all(self):
        search_terms = set()
        indexes_found = []

        if (self.settings['multi_search_mode'] and self.settings['search_terms'] or
            not self.settings['multi_search_mode'] and self.settings['search_term']):
            results = {}

            self.clear_highlights()

            if self.tab == 'concordancer':
                for row in range(self.table.rowCount()):
                    for col in self.cols_search:
                        results[(row, col)] = self.table.cellWidget(row, col).text_search
            else:
                for row in range(self.table.rowCount()):
                    for col in self.cols_search:
                        try:
                            results[(row, col)] = self.table.item(row, col).text_raw
                        except:
                            results[(row, col)] = [self.table.item(row, col).text()]

            items = [token for text in results.values() for token in text]

            for file in self.table.settings['file']['files_open']:
                if file['selected']:
                    search_terms |= wordless_matching.match_search_terms(self.main, items,
                                                                         lang_code = file['lang_code'],
                                                                         settings = self.settings)

            for search_term in search_terms:
                len_search_term = len(search_term)

                for (row, col), text in results.items():
                    for ngram in nltk.ngrams(text, len_search_term):
                        if ngram == search_term:
                            indexes_found.append([row, col])

            if indexes_found:
                self.table.hide()
                self.table.blockSignals(True)
                self.table.setUpdatesEnabled(False)

                if self.tab == 'concordancer':
                    for row, col in indexes_found:
                        self.table.cellWidget(row, col).setStyleSheet('border: 1px solid #E53E3A;')
                else:
                    for row, col in indexes_found:
                        self.table.item(row, col).setForeground(QBrush(QColor('#FFF')))
                        self.table.item(row, col).setBackground(QBrush(QColor('#E53E3A')))

                self.table.blockSignals(False)
                self.table.setUpdatesEnabled(True)
                self.table.show()
            else:
                wordless_message_box.wordless_message_box_no_search_results(self.main)

            if len(indexes_found) == 0:
                self.main.status_bar.showMessage(self.tr('No items found.'))
            elif len(indexes_found) == 1:
                self.main.status_bar.showMessage(self.tr('Found 1 item.'))
            else:
                self.main.status_bar.showMessage(self.tr(f'Found {len(indexes_found):,} items.'))
        else:
            wordless_message_box.wordless_message_box_empty_search_term(self.main)

        return sorted(indexes_found)

    def clear_highlights(self):
        self.table.hide()
        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

        if self.tab == 'concordancer':
            for row in range(self.table.rowCount()):
                for col in self.cols_search:
                    self.table.cellWidget(row, col).setStyleSheet('border: 0')
        else:
            for row in range(self.table.rowCount()):
                for col in self.cols_search:
                    self.table.item(row, col).setForeground(QBrush(QColor('#292929')))
                    self.table.item(row, col).setBackground(QBrush(QColor('#FFF')))

        self.table.blockSignals(False)
        self.table.setUpdatesEnabled(True)
        self.table.show()

    def load(self):
        self.show()

class Wordless_Dialog_Context_Settings(Wordless_Dialog):
    def __init__(self, main, tab):
        super().__init__(main, main.tr('Context Settings'))

        self.tab = tab

        self.settings = self.main.settings_custom[self.tab]['context_settings']

        # Inclusion
        self.group_box_inclusion = QGroupBox(self.tr('Inclusion'), self)

        self.group_box_inclusion.setCheckable(True)

        (self.label_inclusion_search_term,
         self.checkbox_inclusion_multi_search_mode,
         self.line_edit_inclusion_search_term,
         self.list_inclusion_search_terms,
         self.label_inclusion_separator,

         self.checkbox_inclusion_ignore_case,
         self.checkbox_inclusion_match_inflected_forms,
         self.checkbox_inclusion_match_whole_word,
         self.checkbox_inclusion_use_regex,

         self.checkbox_inclusion_ignore_tags,
         self.checkbox_inclusion_ignore_tags_match_tags,
         self.combo_box_inclusion_ignore_tags_type,
         self.combo_box_inclusion_ignore_tags_type_match_tags,
         self.label_inclusion_ignore_tags,
         self.checkbox_inclusion_match_tags) = wordless_widgets.wordless_widgets_search_settings(main, tab = tab)

        self.label_inclusion_context_window = QLabel(self.tr('Context Window:'), self)
        (self.checkbox_inclusion_context_window_sync,
         self.label_inclusion_context_window_left,
         self.spin_box_inclusion_context_window_left,
         self.label_inclusion_context_window_right,
         self.spin_box_inclusion_context_window_right) = wordless_widgets.wordless_widgets_window(main)

        self.group_box_inclusion.toggled.connect(self.inclusion_changed)

        self.checkbox_inclusion_multi_search_mode.stateChanged.connect(self.inclusion_changed)
        self.checkbox_inclusion_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)
        self.line_edit_inclusion_search_term.textChanged.connect(self.inclusion_changed)
        self.list_inclusion_search_terms.itemChanged.connect(self.inclusion_changed)

        self.checkbox_inclusion_ignore_case.stateChanged.connect(self.inclusion_changed)
        self.checkbox_inclusion_match_inflected_forms.stateChanged.connect(self.inclusion_changed)
        self.checkbox_inclusion_match_whole_word.stateChanged.connect(self.inclusion_changed)
        self.checkbox_inclusion_use_regex.stateChanged.connect(self.inclusion_changed)

        self.checkbox_inclusion_ignore_tags.stateChanged.connect(self.inclusion_changed)
        self.checkbox_inclusion_ignore_tags_match_tags.stateChanged.connect(self.inclusion_changed)
        self.combo_box_inclusion_ignore_tags_type.currentTextChanged.connect(self.inclusion_changed)
        self.combo_box_inclusion_ignore_tags_type_match_tags.currentTextChanged.connect(self.inclusion_changed)
        self.checkbox_inclusion_match_tags.stateChanged.connect(self.inclusion_changed)

        self.checkbox_inclusion_context_window_sync.stateChanged.connect(self.inclusion_changed)
        self.spin_box_inclusion_context_window_left.valueChanged.connect(self.inclusion_changed)
        self.spin_box_inclusion_context_window_right.valueChanged.connect(self.inclusion_changed)

        layout_inclusion_multi_search_mode = QGridLayout()
        layout_inclusion_multi_search_mode.addWidget(self.label_inclusion_search_term, 0, 0)
        layout_inclusion_multi_search_mode.addWidget(self.checkbox_inclusion_multi_search_mode, 0, 1, Qt.AlignRight)

        layout_inclusion_search_terms = QGridLayout()
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms, 0, 0, 5, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_add, 0, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_remove, 1, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_clear, 2, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_import, 3, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_export, 4, 1)

        layout_inclusion_ignore_tags = QGridLayout()
        layout_inclusion_ignore_tags.addWidget(self.checkbox_inclusion_ignore_tags, 0, 0)
        layout_inclusion_ignore_tags.addWidget(self.checkbox_inclusion_ignore_tags_match_tags, 0, 0)
        layout_inclusion_ignore_tags.addWidget(self.combo_box_inclusion_ignore_tags_type, 0, 1)
        layout_inclusion_ignore_tags.addWidget(self.combo_box_inclusion_ignore_tags_type_match_tags, 0, 1)
        layout_inclusion_ignore_tags.addWidget(self.label_inclusion_ignore_tags, 0, 2)

        layout_inclusion_ignore_tags.setColumnStretch(3, 1)

        self.group_box_inclusion.setLayout(QGridLayout())
        self.group_box_inclusion.layout().addLayout(layout_inclusion_multi_search_mode, 0, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.line_edit_inclusion_search_term, 1, 0, 1, 4)
        self.group_box_inclusion.layout().addLayout(layout_inclusion_search_terms, 2, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.label_inclusion_separator, 3, 0, 1, 4)

        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_ignore_case, 4, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_match_inflected_forms, 5, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_match_whole_word, 6, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_use_regex, 7, 0, 1, 4)
        self.group_box_inclusion.layout().addLayout(layout_inclusion_ignore_tags, 8, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_match_tags, 9, 0, 1, 4)

        self.group_box_inclusion.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 4)

        self.group_box_inclusion.layout().addWidget(self.label_inclusion_context_window, 11, 0, 1, 3)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_context_window_sync, 11, 3, Qt.AlignRight)
        self.group_box_inclusion.layout().addWidget(self.label_inclusion_context_window_left, 12, 0)
        self.group_box_inclusion.layout().addWidget(self.spin_box_inclusion_context_window_left, 12, 1)
        self.group_box_inclusion.layout().addWidget(self.label_inclusion_context_window_right, 12, 2)
        self.group_box_inclusion.layout().addWidget(self.spin_box_inclusion_context_window_right, 12, 3)

        self.group_box_inclusion.layout().setRowStretch(13, 1)
        self.group_box_inclusion.layout().setColumnStretch(1, 1)
        self.group_box_inclusion.layout().setColumnStretch(3, 1)

        # Exclusion
        self.group_box_exclusion = QGroupBox(self.tr('Exclusion'), self)

        self.group_box_exclusion.setCheckable(True)

        (self.label_exclusion_search_term,
         self.checkbox_exclusion_multi_search_mode,
         self.line_edit_exclusion_search_term,
         self.list_exclusion_search_terms,
         self.label_exclusion_separator,

         self.checkbox_exclusion_ignore_case,
         self.checkbox_exclusion_match_inflected_forms,
         self.checkbox_exclusion_match_whole_word,
         self.checkbox_exclusion_use_regex,

         self.checkbox_exclusion_ignore_tags,
         self.checkbox_exclusion_ignore_tags_match_tags,
         self.combo_box_exclusion_ignore_tags_type,
         self.combo_box_exclusion_ignore_tags_type_match_tags,
         self.label_exclusion_ignore_tags,
         self.checkbox_exclusion_match_tags) = wordless_widgets.wordless_widgets_search_settings(main, tab = tab)

        self.label_exclusion_context_window = QLabel(self.tr('Context Window:'), self)
        (self.checkbox_exclusion_context_window_sync,
         self.label_exclusion_context_window_left,
         self.spin_box_exclusion_context_window_left,
         self.label_exclusion_context_window_right,
         self.spin_box_exclusion_context_window_right) = wordless_widgets.wordless_widgets_window(main)

        self.group_box_exclusion.toggled.connect(self.exclusion_changed)

        self.checkbox_exclusion_multi_search_mode.stateChanged.connect(self.exclusion_changed)
        self.checkbox_exclusion_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)
        self.line_edit_exclusion_search_term.textChanged.connect(self.exclusion_changed)
        self.list_exclusion_search_terms.itemChanged.connect(self.exclusion_changed)

        self.checkbox_exclusion_ignore_case.stateChanged.connect(self.exclusion_changed)
        self.checkbox_exclusion_match_inflected_forms.stateChanged.connect(self.exclusion_changed)
        self.checkbox_exclusion_match_whole_word.stateChanged.connect(self.exclusion_changed)
        self.checkbox_exclusion_use_regex.stateChanged.connect(self.exclusion_changed)

        self.checkbox_exclusion_ignore_tags.stateChanged.connect(self.exclusion_changed)
        self.checkbox_exclusion_ignore_tags_match_tags.stateChanged.connect(self.exclusion_changed)
        self.combo_box_exclusion_ignore_tags_type.currentTextChanged.connect(self.exclusion_changed)
        self.combo_box_exclusion_ignore_tags_type_match_tags.currentTextChanged.connect(self.exclusion_changed)
        self.checkbox_exclusion_match_tags.stateChanged.connect(self.exclusion_changed)

        self.checkbox_exclusion_context_window_sync.stateChanged.connect(self.exclusion_changed)
        self.spin_box_exclusion_context_window_left.valueChanged.connect(self.exclusion_changed)
        self.spin_box_exclusion_context_window_right.valueChanged.connect(self.exclusion_changed)

        layout_exclusion_multi_search_mode = QGridLayout()
        layout_exclusion_multi_search_mode.addWidget(self.label_exclusion_search_term, 0, 0)
        layout_exclusion_multi_search_mode.addWidget(self.checkbox_exclusion_multi_search_mode, 0, 1, Qt.AlignRight)

        layout_exclusion_search_terms = QGridLayout()
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms, 0, 0, 5, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_add, 0, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_remove, 1, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_clear, 2, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_import, 3, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_export, 4, 1)

        layout_exclusion_ignore_tags = QGridLayout()
        layout_exclusion_ignore_tags.addWidget(self.checkbox_exclusion_ignore_tags, 0, 0)
        layout_exclusion_ignore_tags.addWidget(self.checkbox_exclusion_ignore_tags_match_tags, 0, 0)
        layout_exclusion_ignore_tags.addWidget(self.combo_box_exclusion_ignore_tags_type, 0, 1)
        layout_exclusion_ignore_tags.addWidget(self.combo_box_exclusion_ignore_tags_type_match_tags, 0, 1)
        layout_exclusion_ignore_tags.addWidget(self.label_exclusion_ignore_tags, 0, 2)

        layout_exclusion_ignore_tags.setColumnStretch(3, 1)

        self.group_box_exclusion.setLayout(QGridLayout())
        self.group_box_exclusion.layout().addLayout(layout_exclusion_multi_search_mode, 0, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.line_edit_exclusion_search_term, 1, 0, 1, 4)
        self.group_box_exclusion.layout().addLayout(layout_exclusion_search_terms, 2, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.label_exclusion_separator, 3, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_ignore_case, 4, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_inflected_forms, 5, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_whole_word, 6, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_use_regex, 7, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_ignore_case, 4, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_inflected_forms, 5, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_whole_word, 6, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_use_regex, 7, 0, 1, 4)
        self.group_box_exclusion.layout().addLayout(layout_exclusion_ignore_tags, 8, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_tags, 9, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(self.label_exclusion_context_window, 11, 0, 1, 3)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_context_window_sync, 11, 3, Qt.AlignRight)
        self.group_box_exclusion.layout().addWidget(self.label_exclusion_context_window_left, 12, 0)
        self.group_box_exclusion.layout().addWidget(self.spin_box_exclusion_context_window_left, 12, 1)
        self.group_box_exclusion.layout().addWidget(self.label_exclusion_context_window_right, 12, 2)
        self.group_box_exclusion.layout().addWidget(self.spin_box_exclusion_context_window_right, 12, 3)

        self.group_box_exclusion.layout().setRowStretch(13, 1)
        self.group_box_exclusion.layout().setColumnStretch(1, 1)
        self.group_box_exclusion.layout().setColumnStretch(3, 1)

        self.button_restore_default_settings = QPushButton(self.tr('Restore Default Settings'), self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_restore_default_settings.clicked.connect(self.restore_default_settings)
        self.button_ok.clicked.connect(self.accept)

        self.button_restore_default_settings.setFixedWidth(150)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.group_box_inclusion, 0, 0, Qt.AlignTop)
        self.layout().addWidget(self.group_box_exclusion, 0, 1, Qt.AlignTop)
        self.layout().addWidget(self.button_restore_default_settings, 1, 0, Qt.AlignLeft)
        self.layout().addWidget(self.button_ok, 1, 1, Qt.AlignRight)

        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 1)

        self.multi_search_mode_changed()

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['context_settings'])
        else:
            settings = copy.deepcopy(self.settings)

        # Inclusion
        self.group_box_inclusion.setChecked(settings['inclusion']['inclusion'])

        self.checkbox_inclusion_multi_search_mode.setChecked(settings['inclusion']['multi_search_mode'])

        if not defaults:
            self.line_edit_inclusion_search_term.setText(settings['inclusion']['search_term'])

            self.list_inclusion_search_terms.clear()

            for search_term in settings['inclusion']['search_terms']:
                self.list_inclusion_search_terms.add_item(search_term)

        self.checkbox_inclusion_ignore_case.setChecked(settings['inclusion']['ignore_case'])
        self.checkbox_inclusion_match_inflected_forms.setChecked(settings['inclusion']['match_inflected_forms'])
        self.checkbox_inclusion_match_whole_word.setChecked(settings['inclusion']['match_whole_word'])
        self.checkbox_inclusion_use_regex.setChecked(settings['inclusion']['use_regex'])

        self.checkbox_inclusion_ignore_tags.setChecked(settings['inclusion']['ignore_tags'])
        self.checkbox_inclusion_ignore_tags_match_tags.setChecked(settings['inclusion']['ignore_tags_match_tags'])
        self.combo_box_inclusion_ignore_tags_type.setCurrentText(settings['inclusion']['ignore_tags_type'])
        self.combo_box_inclusion_ignore_tags_type_match_tags.setCurrentText(settings['inclusion']['ignore_tags_type_match_tags'])
        self.checkbox_inclusion_match_tags.setChecked(settings['inclusion']['match_tags'])

        self.checkbox_inclusion_context_window_sync.setChecked(settings['inclusion']['context_window_sync'])

        if settings['inclusion']['context_window_left'] < 0:
            self.spin_box_inclusion_context_window_left.setPrefix('L')
            self.spin_box_inclusion_context_window_left.setValue(-settings['inclusion']['context_window_left'])
        else:
            self.spin_box_inclusion_context_window_left.setPrefix('R')
            self.spin_box_inclusion_context_window_left.setValue(settings['inclusion']['context_window_left'])

        if settings['inclusion']['context_window_right'] < 0:
            self.spin_box_inclusion_context_window_right.setPrefix('L')
            self.spin_box_inclusion_context_window_right.setValue(-settings['inclusion']['context_window_right'])
        else:
            self.spin_box_inclusion_context_window_right.setPrefix('R')
            self.spin_box_inclusion_context_window_right.setValue(settings['inclusion']['context_window_right'])

        self.line_edit_inclusion_search_term.returnPressed.connect(self.button_ok.click)

        # Exclusion
        self.group_box_exclusion.setChecked(settings['exclusion']['exclusion'])

        self.checkbox_exclusion_multi_search_mode.setChecked(settings['exclusion']['multi_search_mode'])

        if not defaults:
            self.line_edit_exclusion_search_term.setText(settings['exclusion']['search_term'])

            self.list_exclusion_search_terms.clear()

            for search_term in settings['exclusion']['search_terms']:
                self.list_exclusion_search_terms.add_item(search_term)

        self.checkbox_exclusion_ignore_case.setChecked(settings['exclusion']['ignore_case'])
        self.checkbox_exclusion_match_inflected_forms.setChecked(settings['exclusion']['match_inflected_forms'])
        self.checkbox_exclusion_match_whole_word.setChecked(settings['exclusion']['match_whole_word'])
        self.checkbox_exclusion_use_regex.setChecked(settings['exclusion']['use_regex'])

        self.checkbox_exclusion_ignore_tags.setChecked(settings['exclusion']['ignore_tags'])
        self.checkbox_exclusion_ignore_tags_match_tags.setChecked(settings['exclusion']['ignore_tags_match_tags'])
        self.combo_box_exclusion_ignore_tags_type.setCurrentText(settings['exclusion']['ignore_tags_type'])
        self.combo_box_exclusion_ignore_tags_type_match_tags.setCurrentText(settings['exclusion']['ignore_tags_type_match_tags'])
        self.checkbox_exclusion_match_tags.setChecked(settings['exclusion']['match_tags'])

        self.checkbox_exclusion_context_window_sync.setChecked(settings['exclusion']['context_window_sync'])

        if settings['exclusion']['context_window_left'] < 0:
            self.spin_box_exclusion_context_window_left.setPrefix('L')
            self.spin_box_exclusion_context_window_left.setValue(-settings['exclusion']['context_window_left'])
        else:
            self.spin_box_exclusion_context_window_left.setPrefix('R')
            self.spin_box_exclusion_context_window_left.setValue(settings['exclusion']['context_window_left'])
            
        if settings['exclusion']['context_window_right'] < 0:
            self.spin_box_exclusion_context_window_right.setPrefix('L')
            self.spin_box_exclusion_context_window_right.setValue(-settings['exclusion']['context_window_right'])
        else:
            self.spin_box_exclusion_context_window_right.setPrefix('R')
            self.spin_box_exclusion_context_window_right.setValue(settings['exclusion']['context_window_right'])

        self.line_edit_exclusion_search_term.returnPressed.connect(self.button_ok.click)

        self.inclusion_changed()
        self.exclusion_changed()
        self.multi_search_mode_changed()
        self.token_settings_changed()

    def inclusion_changed(self):
        self.settings['inclusion']['inclusion'] = self.group_box_inclusion.isChecked()

        self.settings['inclusion']['multi_search_mode'] = self.checkbox_inclusion_multi_search_mode.isChecked()
        self.settings['inclusion']['search_term'] = self.line_edit_inclusion_search_term.text()
        self.settings['inclusion']['search_terms'] = self.list_inclusion_search_terms.get_items()

        self.settings['inclusion']['ignore_case'] = self.checkbox_inclusion_ignore_case.isChecked()
        self.settings['inclusion']['match_inflected_forms'] = self.checkbox_inclusion_match_inflected_forms.isChecked()
        self.settings['inclusion']['match_whole_word'] = self.checkbox_inclusion_match_whole_word.isChecked()
        self.settings['inclusion']['use_regex'] = self.checkbox_inclusion_use_regex.isChecked()

        self.settings['inclusion']['ignore_tags'] = self.checkbox_inclusion_ignore_tags.isChecked()
        self.settings['inclusion']['ignore_tags_match_tags'] = self.checkbox_inclusion_ignore_tags_match_tags.isChecked()
        self.settings['inclusion']['ignore_tags_type'] = self.combo_box_inclusion_ignore_tags_type.currentText()
        self.settings['inclusion']['ignore_tags_type_match_tags'] = self.combo_box_inclusion_ignore_tags_type_match_tags.currentText()
        self.settings['inclusion']['match_tags'] = self.checkbox_inclusion_match_tags.isChecked()
        
        self.settings['inclusion']['context_window_sync'] = self.checkbox_inclusion_context_window_sync.isChecked()

        if self.spin_box_inclusion_context_window_left.prefix() == 'L':
            self.settings['inclusion']['context_window_left'] = -self.spin_box_inclusion_context_window_left.value()
        else:
            self.settings['inclusion']['context_window_left'] = self.spin_box_inclusion_context_window_left.value()
            
        if self.spin_box_inclusion_context_window_right.prefix() == 'L':
            self.settings['inclusion']['context_window_right'] = -self.spin_box_inclusion_context_window_right.value()
        else:
            self.settings['inclusion']['context_window_right'] = self.spin_box_inclusion_context_window_right.value()

        if self.settings['inclusion']['inclusion']:
            self.checkbox_inclusion_match_tags.token_settings_changed()

    def exclusion_changed(self):
        self.settings['exclusion']['exclusion'] = self.group_box_exclusion.isChecked()

        self.settings['exclusion']['multi_search_mode'] = self.checkbox_exclusion_multi_search_mode.isChecked()
        self.settings['exclusion']['search_term'] = self.line_edit_exclusion_search_term.text()
        self.settings['exclusion']['search_terms'] = self.list_exclusion_search_terms.get_items()

        self.settings['exclusion']['ignore_case'] = self.checkbox_exclusion_ignore_case.isChecked()
        self.settings['exclusion']['match_inflected_forms'] = self.checkbox_exclusion_match_inflected_forms.isChecked()
        self.settings['exclusion']['match_whole_word'] = self.checkbox_exclusion_match_whole_word.isChecked()
        self.settings['exclusion']['use_regex'] = self.checkbox_exclusion_use_regex.isChecked()

        self.settings['exclusion']['ignore_tags'] = self.checkbox_exclusion_ignore_tags.isChecked()
        self.settings['exclusion']['ignore_tags_match_tags'] = self.checkbox_exclusion_ignore_tags_match_tags.isChecked()
        self.settings['exclusion']['ignore_tags_type'] = self.combo_box_exclusion_ignore_tags_type.currentText()
        self.settings['exclusion']['ignore_tags_type_match_tags'] = self.combo_box_exclusion_ignore_tags_type_match_tags.currentText()
        self.settings['exclusion']['match_tags'] = self.checkbox_exclusion_match_tags.isChecked()
        
        self.settings['exclusion']['context_window_sync'] = self.checkbox_exclusion_context_window_sync.isChecked()
        
        if self.spin_box_exclusion_context_window_left.prefix() == 'L':
            self.settings['exclusion']['context_window_left'] = -self.spin_box_exclusion_context_window_left.value()
        else:
            self.settings['exclusion']['context_window_left'] = self.spin_box_exclusion_context_window_left.value()
            
        if self.spin_box_exclusion_context_window_right.prefix() == 'L':
            self.settings['exclusion']['context_window_right'] = -self.spin_box_exclusion_context_window_right.value()
        else:
            self.settings['exclusion']['context_window_right'] = self.spin_box_exclusion_context_window_right.value()

        if self.settings['exclusion']['exclusion']:
            self.checkbox_exclusion_match_tags.token_settings_changed()

    def multi_search_mode_changed(self):
        if self.settings['inclusion']['multi_search_mode'] or self.settings['exclusion']['multi_search_mode']:
            self.setFixedSize(520, 480)
        else:
            self.setFixedSize(520, 370)

    def token_settings_changed(self):
        self.checkbox_inclusion_match_tags.token_settings_changed()
        self.checkbox_exclusion_match_tags.token_settings_changed()

    def restore_default_settings(self):
        reply = wordless_message_box.wordless_message_box_restore_default_settings(self.main)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

    def load(self):
        self.exec_()
