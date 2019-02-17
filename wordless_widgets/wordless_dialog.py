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
    def __init__(self, main, title, width, height, no_button = False):
        super().__init__(main, title)

        self.setFixedSize(width, height)
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.wrapper_info = QWidget(self)

        self.wrapper_info.setObjectName('wrapper-info')
        self.wrapper_info.setStyleSheet('''
            QWidget#wrapper-info {
                border-bottom: 1px solid #B0B0B0;
                background-color: #FFF;
            }
        ''')

        self.wrapper_info.setLayout(QGridLayout())
        self.wrapper_info.layout().setContentsMargins(20, 10, 20, 10)

        self.wrapper_buttons = QWidget(self)

        self.wrapper_buttons.setLayout(QGridLayout())
        self.wrapper_buttons.layout().setContentsMargins(11, 0, 11, 11)

        if not no_button:
            self.button_ok = QPushButton(self.tr('OK'), self)

            self.button_ok.clicked.connect(self.accept)

            self.wrapper_buttons.layout().addWidget(self.button_ok, 0, 0, Qt.AlignRight)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.wrapper_info, 0, 0)
        self.layout().addWidget(self.wrapper_buttons, 1, 0)

        self.layout().setRowStretch(0, 1)
        self.layout().setContentsMargins(0, 0, 0, 0)

class Wordless_Dialog_Search(Wordless_Dialog):
    def __init__(self, main, tab, table, cols_search):
        super().__init__(main, main.tr('Search in Results'))

        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.tab = tab
        self.table = table
        self.cols_search = self.table.find_col(cols_search)

        self.settings = self.main.settings_custom[self.tab]['search_results']

        (self.label_search_term,
         self.checkbox_multi_search_mode,
         self.line_edit_search_term,
         self.list_search_terms,
         self.label_separator,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_word,
         self.checkbox_use_regex,

         self.stacked_wdiget_ignore_tags,
         self.stacked_wdiget_ignore_tags_type,
         self.label_ignore_tags,
         self.checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self, self.tab)

        self.button_find_next = QPushButton(self.tr('Find Next'), self)
        self.button_find_prev = QPushButton(self.tr('Find Previous'), self)
        self.button_find_all = QPushButton(self.tr('Find All'), self)
        
        self.button_reset_settings = QPushButton(self.tr('Reset Settings'), self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.button_find_next.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_word.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.stacked_wdiget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.stacked_wdiget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.search_settings_changed)
        self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.search_settings_changed)
        self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.button_find_next.clicked.connect(lambda: self.find_next())
        self.button_find_prev.clicked.connect(lambda: self.find_prev())
        self.button_find_all.clicked.connect(lambda: self.find_all())

        self.button_reset_settings.clicked.connect(lambda: self.load_settings(defaults = True))
        self.button_close.clicked.connect(self.accept)

        layout_search_terms = QGridLayout()
        layout_search_terms.addWidget(self.list_search_terms, 0, 0, 5, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_add, 0, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_remove, 1, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_clear, 2, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_import, 3, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_export, 4, 1)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.stacked_wdiget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.stacked_wdiget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        layout_buttons_right = QGridLayout()
        layout_buttons_right.addWidget(self.button_find_next, 0, 0)
        layout_buttons_right.addWidget(self.button_find_prev, 1, 0)
        layout_buttons_right.addWidget(self.button_find_all, 2, 0)

        layout_buttons_right.setRowStretch(3, 1)

        layout_buttons_bottom = QGridLayout()
        layout_buttons_bottom.addWidget(self.button_reset_settings, 0, 0)
        layout_buttons_bottom.addWidget(self.button_close, 0, 1, Qt.AlignRight)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.label_search_term, 0, 0)
        self.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.line_edit_search_term, 1, 0, 1, 2)
        self.layout().addLayout(layout_search_terms, 2, 0, 1, 2)
        self.layout().addWidget(self.label_separator, 3, 0, 1, 2)

        self.layout().addWidget(self.checkbox_ignore_case, 4, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_whole_word, 6, 0, 1, 2)
        self.layout().addWidget(self.checkbox_use_regex, 7, 0, 1, 2)

        self.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_tags, 9, 0, 1, 2)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 2, 10, 1)

        self.layout().addLayout(layout_buttons_right, 0, 3, 10, 1)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 4)

        self.layout().addLayout(layout_buttons_bottom, 11, 0, 1, 4)

        self.main.wordless_work_area.currentChanged.connect(self.accept)

        self.load_settings()

        self.search_settings_changed()

    def closeEvent(self, event):
        self.clear_highlights()

        event.accept()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['search_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.checkbox_multi_search_mode.setChecked(settings['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_term'])
            self.list_search_terms.load_items(settings['search_terms'])

        self.checkbox_ignore_case.setChecked(settings['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings['match_inflected_forms'])
        self.checkbox_match_whole_word.setChecked(settings['match_whole_word'])
        self.checkbox_use_regex.setChecked(settings['use_regex'])

        self.stacked_wdiget_ignore_tags.checkbox_ignore_tags.setChecked(settings['ignore_tags'])
        self.stacked_wdiget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['ignore_tags_tags'])
        self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['ignore_tags_type'])
        self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['match_tags'])

    def search_settings_changed(self):
        self.settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        self.settings['search_term'] = self.line_edit_search_term.text()
        self.settings['search_terms'] = self.list_search_terms.get_items()

        self.settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        self.settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        self.settings['match_whole_word'] = self.checkbox_match_whole_word.isChecked()
        self.settings['use_regex'] = self.checkbox_use_regex.isChecked()

        self.settings['ignore_tags'] = self.stacked_wdiget_ignore_tags.checkbox_ignore_tags.isChecked()
        self.settings['ignore_tags_tags'] = self.stacked_wdiget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        self.settings['ignore_tags_type'] = self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags.currentText()
        self.settings['ignore_tags_type_tags'] = self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        self.settings['match_tags'] = self.checkbox_match_tags.isChecked()

        if self.settings['multi_search_mode']:
            self.setFixedSize(360, 390)
        else:
            self.setFixedSize(360, 280)

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

            for file in self.table.settings['files']['files_open']:
                if file['selected']:
                    search_terms_file = wordless_matching.match_search_terms(
                        self.main, items,
                        lang = file['lang'],
                        text_type = ('tokenized', 'tagged_both'),
                        token_settings = self.table.settings[self.tab]['token_settings'],
                        search_settings = self.settings)

                    search_terms |= set(search_terms_file)

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
                self.main.statusBar().showMessage(self.tr('No items found.'))
            elif len(indexes_found) == 1:
                self.main.statusBar().showMessage(self.tr('Found 1 item.'))
            else:
                self.main.statusBar().showMessage(self.tr(f'Found {len(indexes_found):,} items.'))
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
        self.inclusion_group_box = QGroupBox(self.tr('Inclusion'), self)

        self.inclusion_group_box.setCheckable(True)

        (self.inclusion_label_search_term,
         self.inclusion_checkbox_multi_search_mode,
         self.inclusion_line_edit_search_term,
         self.inclusion_list_search_terms,
         self.inclusion_label_separator,

         self.inclusion_checkbox_ignore_case,
         self.inclusion_checkbox_match_inflected_forms,
         self.inclusion_checkbox_match_whole_word,
         self.inclusion_checkbox_use_regex,

         self.inclusion_stacked_widget_ignore_tags,
         self.inclusion_stacked_widget_ignore_tags_type,
         self.inclusion_label_ignore_tags,
         self.inclusion_checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self, tab = tab)

        self.inclusion_label_context_window = QLabel(self.tr('Context Window:'), self)
        (self.inclusion_checkbox_context_window_sync,
         self.inclusion_label_context_window_left,
         self.inclusion_spin_box_context_window_left,
         self.inclusion_label_context_window_right,
         self.inclusion_spin_box_context_window_right) = wordless_widgets.wordless_widgets_window(self)

        self.inclusion_group_box.toggled.connect(self.inclusion_changed)

        self.inclusion_checkbox_multi_search_mode.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)
        self.inclusion_line_edit_search_term.textChanged.connect(self.inclusion_changed)
        self.inclusion_list_search_terms.itemChanged.connect(self.inclusion_changed)

        self.inclusion_checkbox_ignore_case.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_match_inflected_forms.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_match_whole_word.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_use_regex.stateChanged.connect(self.inclusion_changed)

        self.inclusion_stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.inclusion_changed)
        self.inclusion_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.inclusion_changed)
        self.inclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.inclusion_changed)
        self.inclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_match_tags.stateChanged.connect(self.inclusion_changed)

        self.inclusion_checkbox_context_window_sync.stateChanged.connect(self.inclusion_changed)
        self.inclusion_spin_box_context_window_left.valueChanged.connect(self.inclusion_changed)
        self.inclusion_spin_box_context_window_right.valueChanged.connect(self.inclusion_changed)

        inclusion_layout_multi_search_mode = QGridLayout()
        inclusion_layout_multi_search_mode.addWidget(self.inclusion_label_search_term, 0, 0)
        inclusion_layout_multi_search_mode.addWidget(self.inclusion_checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

        inclusion_layout_search_terms = QGridLayout()
        inclusion_layout_search_terms.addWidget(self.inclusion_list_search_terms, 0, 0, 5, 1)
        inclusion_layout_search_terms.addWidget(self.inclusion_list_search_terms.button_add, 0, 1)
        inclusion_layout_search_terms.addWidget(self.inclusion_list_search_terms.button_remove, 1, 1)
        inclusion_layout_search_terms.addWidget(self.inclusion_list_search_terms.button_clear, 2, 1)
        inclusion_layout_search_terms.addWidget(self.inclusion_list_search_terms.button_import, 3, 1)
        inclusion_layout_search_terms.addWidget(self.inclusion_list_search_terms.button_export, 4, 1)

        inclusion_layout_ignore_tags = QGridLayout()
        inclusion_layout_ignore_tags.addWidget(self.inclusion_stacked_widget_ignore_tags, 0, 0)
        inclusion_layout_ignore_tags.addWidget(self.inclusion_stacked_widget_ignore_tags_type, 0, 1)
        inclusion_layout_ignore_tags.addWidget(self.inclusion_label_ignore_tags, 0, 2)

        inclusion_layout_ignore_tags.setColumnStretch(3, 1)

        self.inclusion_group_box.setLayout(QGridLayout())
        self.inclusion_group_box.layout().addLayout(inclusion_layout_multi_search_mode, 0, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_line_edit_search_term, 1, 0, 1, 4)
        self.inclusion_group_box.layout().addLayout(inclusion_layout_search_terms, 2, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_label_separator, 3, 0, 1, 4)

        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_ignore_case, 4, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_inflected_forms, 5, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_whole_word, 6, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_use_regex, 7, 0, 1, 4)
        self.inclusion_group_box.layout().addLayout(inclusion_layout_ignore_tags, 8, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_tags, 9, 0, 1, 4)

        self.inclusion_group_box.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 4)

        self.inclusion_group_box.layout().addWidget(self.inclusion_label_context_window, 11, 0, 1, 3)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_context_window_sync, 11, 3, Qt.AlignRight)
        self.inclusion_group_box.layout().addWidget(self.inclusion_label_context_window_left, 12, 0)
        self.inclusion_group_box.layout().addWidget(self.inclusion_spin_box_context_window_left, 12, 1)
        self.inclusion_group_box.layout().addWidget(self.inclusion_label_context_window_right, 12, 2)
        self.inclusion_group_box.layout().addWidget(self.inclusion_spin_box_context_window_right, 12, 3)

        self.inclusion_group_box.layout().setRowStretch(13, 1)
        self.inclusion_group_box.layout().setColumnStretch(1, 1)
        self.inclusion_group_box.layout().setColumnStretch(3, 1)

        # Exclusion
        self.exclusion_group_box = QGroupBox(self.tr('Exclusion'), self)

        self.exclusion_group_box.setCheckable(True)

        (self.exclusion_label_search_term,
         self.exclusion_checkbox_multi_search_mode,
         self.exclusion_line_edit_search_term,
         self.exclusion_list_search_terms,
         self.exclusion_label_separator,

         self.exclusion_checkbox_ignore_case,
         self.exclusion_checkbox_match_inflected_forms,
         self.exclusion_checkbox_match_whole_word,
         self.exclusion_checkbox_use_regex,

         self.exclusion_stacked_widget_ignore_tags,
         self.exclusion_stacked_widget_ignore_tags_type,
         self.exclusion_label_ignore_tags,
         self.exclusion_checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self, tab = tab)

        self.exclusion_label_context_window = QLabel(self.tr('Context Window:'), self)
        (self.exclusion_checkbox_context_window_sync,
         self.exclusion_label_context_window_left,
         self.exclusion_spin_box_context_window_left,
         self.exclusion_label_context_window_right,
         self.exclusion_spin_box_context_window_right) = wordless_widgets.wordless_widgets_window(self)

        self.exclusion_group_box.toggled.connect(self.exclusion_changed)

        self.exclusion_checkbox_multi_search_mode.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)
        self.exclusion_line_edit_search_term.textChanged.connect(self.exclusion_changed)
        self.exclusion_list_search_terms.itemChanged.connect(self.exclusion_changed)

        self.exclusion_checkbox_ignore_case.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_match_inflected_forms.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_match_whole_word.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_use_regex.stateChanged.connect(self.exclusion_changed)

        self.exclusion_stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.exclusion_changed)
        self.exclusion_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.exclusion_changed)
        self.exclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.exclusion_changed)
        self.exclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_match_tags.stateChanged.connect(self.exclusion_changed)

        self.exclusion_checkbox_context_window_sync.stateChanged.connect(self.exclusion_changed)
        self.exclusion_spin_box_context_window_left.valueChanged.connect(self.exclusion_changed)
        self.exclusion_spin_box_context_window_right.valueChanged.connect(self.exclusion_changed)

        exclusion_layout_multi_search_mode = QGridLayout()
        exclusion_layout_multi_search_mode.addWidget(self.exclusion_label_search_term, 0, 0)
        exclusion_layout_multi_search_mode.addWidget(self.exclusion_checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

        exclusion_layout_search_terms = QGridLayout()
        exclusion_layout_search_terms.addWidget(self.exclusion_list_search_terms, 0, 0, 5, 1)
        exclusion_layout_search_terms.addWidget(self.exclusion_list_search_terms.button_add, 0, 1)
        exclusion_layout_search_terms.addWidget(self.exclusion_list_search_terms.button_remove, 1, 1)
        exclusion_layout_search_terms.addWidget(self.exclusion_list_search_terms.button_clear, 2, 1)
        exclusion_layout_search_terms.addWidget(self.exclusion_list_search_terms.button_import, 3, 1)
        exclusion_layout_search_terms.addWidget(self.exclusion_list_search_terms.button_export, 4, 1)

        exclusion_layout_ignore_tags = QGridLayout()
        exclusion_layout_ignore_tags.addWidget(self.exclusion_stacked_widget_ignore_tags, 0, 0)
        exclusion_layout_ignore_tags.addWidget(self.exclusion_stacked_widget_ignore_tags_type, 0, 1)
        exclusion_layout_ignore_tags.addWidget(self.exclusion_label_ignore_tags, 0, 2)

        exclusion_layout_ignore_tags.setColumnStretch(3, 1)

        self.exclusion_group_box.setLayout(QGridLayout())
        self.exclusion_group_box.layout().addLayout(exclusion_layout_multi_search_mode, 0, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_line_edit_search_term, 1, 0, 1, 4)
        self.exclusion_group_box.layout().addLayout(exclusion_layout_search_terms, 2, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_label_separator, 3, 0, 1, 4)

        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_ignore_case, 4, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_inflected_forms, 5, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_whole_word, 6, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_use_regex, 7, 0, 1, 4)
        self.exclusion_group_box.layout().addLayout(exclusion_layout_ignore_tags, 8, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_tags, 9, 0, 1, 4)

        self.exclusion_group_box.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 4)

        self.exclusion_group_box.layout().addWidget(self.exclusion_label_context_window, 11, 0, 1, 3)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_context_window_sync, 11, 3, Qt.AlignRight)
        self.exclusion_group_box.layout().addWidget(self.exclusion_label_context_window_left, 12, 0)
        self.exclusion_group_box.layout().addWidget(self.exclusion_spin_box_context_window_left, 12, 1)
        self.exclusion_group_box.layout().addWidget(self.exclusion_label_context_window_right, 12, 2)
        self.exclusion_group_box.layout().addWidget(self.exclusion_spin_box_context_window_right, 12, 3)

        self.exclusion_group_box.layout().setRowStretch(13, 1)
        self.exclusion_group_box.layout().setColumnStretch(1, 1)
        self.exclusion_group_box.layout().setColumnStretch(3, 1)

        self.button_reset_settings = QPushButton(self.tr('Reset Settings'), self)
        self.button_ok = QPushButton(self.tr('OK'), self)

        self.button_reset_settings.clicked.connect(self.reset_settings)
        self.button_ok.clicked.connect(self.accept)

        self.button_reset_settings.setFixedWidth(150)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.inclusion_group_box, 0, 0, Qt.AlignTop)
        self.layout().addWidget(self.exclusion_group_box, 0, 1, Qt.AlignTop)
        self.layout().addWidget(self.button_reset_settings, 1, 0, Qt.AlignLeft)
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
        self.inclusion_group_box.setChecked(settings['inclusion']['inclusion'])

        self.inclusion_checkbox_multi_search_mode.setChecked(settings['inclusion']['multi_search_mode'])

        if not defaults:
            self.inclusion_line_edit_search_term.setText(settings['inclusion']['search_term'])
            self.inclusion_list_search_terms.load_items(settings['inclusion']['search_terms'])

        self.inclusion_checkbox_ignore_case.setChecked(settings['inclusion']['ignore_case'])
        self.inclusion_checkbox_match_inflected_forms.setChecked(settings['inclusion']['match_inflected_forms'])
        self.inclusion_checkbox_match_whole_word.setChecked(settings['inclusion']['match_whole_word'])
        self.inclusion_checkbox_use_regex.setChecked(settings['inclusion']['use_regex'])

        self.inclusion_stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['inclusion']['ignore_tags'])
        self.inclusion_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['inclusion']['ignore_tags_tags'])
        self.inclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['inclusion']['ignore_tags_type'])
        self.inclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['inclusion']['ignore_tags_type_tags'])
        self.inclusion_checkbox_match_tags.setChecked(settings['inclusion']['match_tags'])

        self.inclusion_checkbox_context_window_sync.setChecked(settings['inclusion']['context_window_sync'])

        if settings['inclusion']['context_window_left'] < 0:
            self.inclusion_spin_box_context_window_left.setPrefix('L')
            self.inclusion_spin_box_context_window_left.setValue(-settings['inclusion']['context_window_left'])
        else:
            self.inclusion_spin_box_context_window_left.setPrefix('R')
            self.inclusion_spin_box_context_window_left.setValue(settings['inclusion']['context_window_left'])

        if settings['inclusion']['context_window_right'] < 0:
            self.inclusion_spin_box_context_window_right.setPrefix('L')
            self.inclusion_spin_box_context_window_right.setValue(-settings['inclusion']['context_window_right'])
        else:
            self.inclusion_spin_box_context_window_right.setPrefix('R')
            self.inclusion_spin_box_context_window_right.setValue(settings['inclusion']['context_window_right'])

        self.inclusion_line_edit_search_term.returnPressed.connect(self.button_ok.click)

        # Exclusion
        self.exclusion_group_box.setChecked(settings['exclusion']['exclusion'])

        self.exclusion_checkbox_multi_search_mode.setChecked(settings['exclusion']['multi_search_mode'])

        if not defaults:
            self.exclusion_line_edit_search_term.setText(settings['exclusion']['search_term'])
            self.exclusion_list_search_terms.load_items(settings['exclusion']['search_terms'])

        self.exclusion_checkbox_ignore_case.setChecked(settings['exclusion']['ignore_case'])
        self.exclusion_checkbox_match_inflected_forms.setChecked(settings['exclusion']['match_inflected_forms'])
        self.exclusion_checkbox_match_whole_word.setChecked(settings['exclusion']['match_whole_word'])
        self.exclusion_checkbox_use_regex.setChecked(settings['exclusion']['use_regex'])

        self.exclusion_stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['exclusion']['ignore_tags'])
        self.exclusion_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['exclusion']['ignore_tags_tags'])
        self.exclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['exclusion']['ignore_tags_type'])
        self.exclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['exclusion']['ignore_tags_type_tags'])
        self.exclusion_checkbox_match_tags.setChecked(settings['exclusion']['match_tags'])

        self.exclusion_checkbox_context_window_sync.setChecked(settings['exclusion']['context_window_sync'])

        if settings['exclusion']['context_window_left'] < 0:
            self.exclusion_spin_box_context_window_left.setPrefix('L')
            self.exclusion_spin_box_context_window_left.setValue(-settings['exclusion']['context_window_left'])
        else:
            self.exclusion_spin_box_context_window_left.setPrefix('R')
            self.exclusion_spin_box_context_window_left.setValue(settings['exclusion']['context_window_left'])
            
        if settings['exclusion']['context_window_right'] < 0:
            self.exclusion_spin_box_context_window_right.setPrefix('L')
            self.exclusion_spin_box_context_window_right.setValue(-settings['exclusion']['context_window_right'])
        else:
            self.exclusion_spin_box_context_window_right.setPrefix('R')
            self.exclusion_spin_box_context_window_right.setValue(settings['exclusion']['context_window_right'])

        self.exclusion_line_edit_search_term.returnPressed.connect(self.button_ok.click)

        self.inclusion_changed()
        self.exclusion_changed()
        self.multi_search_mode_changed()
        self.token_settings_changed()

    def inclusion_changed(self):
        self.settings['inclusion']['inclusion'] = self.inclusion_group_box.isChecked()

        self.settings['inclusion']['multi_search_mode'] = self.inclusion_checkbox_multi_search_mode.isChecked()
        self.settings['inclusion']['search_term'] = self.inclusion_line_edit_search_term.text()
        self.settings['inclusion']['search_terms'] = self.inclusion_list_search_terms.get_items()

        self.settings['inclusion']['ignore_case'] = self.inclusion_checkbox_ignore_case.isChecked()
        self.settings['inclusion']['match_inflected_forms'] = self.inclusion_checkbox_match_inflected_forms.isChecked()
        self.settings['inclusion']['match_whole_word'] = self.inclusion_checkbox_match_whole_word.isChecked()
        self.settings['inclusion']['use_regex'] = self.inclusion_checkbox_use_regex.isChecked()

        self.settings['inclusion']['ignore_tags'] = self.inclusion_stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        self.settings['inclusion']['ignore_tags_tags'] = self.inclusion_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        self.settings['inclusion']['ignore_tags_type'] = self.inclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        self.settings['inclusion']['ignore_tags_type_tags'] = self.inclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        self.settings['inclusion']['match_tags'] = self.inclusion_checkbox_match_tags.isChecked()
        
        self.settings['inclusion']['context_window_sync'] = self.inclusion_checkbox_context_window_sync.isChecked()

        if self.inclusion_spin_box_context_window_left.prefix() == 'L':
            self.settings['inclusion']['context_window_left'] = -self.inclusion_spin_box_context_window_left.value()
        else:
            self.settings['inclusion']['context_window_left'] = self.inclusion_spin_box_context_window_left.value()
            
        if self.inclusion_spin_box_context_window_right.prefix() == 'L':
            self.settings['inclusion']['context_window_right'] = -self.inclusion_spin_box_context_window_right.value()
        else:
            self.settings['inclusion']['context_window_right'] = self.inclusion_spin_box_context_window_right.value()

        if self.settings['inclusion']['inclusion']:
            self.inclusion_checkbox_match_tags.token_settings_changed()

    def exclusion_changed(self):
        self.settings['exclusion']['exclusion'] = self.exclusion_group_box.isChecked()

        self.settings['exclusion']['multi_search_mode'] = self.exclusion_checkbox_multi_search_mode.isChecked()
        self.settings['exclusion']['search_term'] = self.exclusion_line_edit_search_term.text()
        self.settings['exclusion']['search_terms'] = self.exclusion_list_search_terms.get_items()

        self.settings['exclusion']['ignore_case'] = self.exclusion_checkbox_ignore_case.isChecked()
        self.settings['exclusion']['match_inflected_forms'] = self.exclusion_checkbox_match_inflected_forms.isChecked()
        self.settings['exclusion']['match_whole_word'] = self.exclusion_checkbox_match_whole_word.isChecked()
        self.settings['exclusion']['use_regex'] = self.exclusion_checkbox_use_regex.isChecked()

        self.settings['exclusion']['ignore_tags'] = self.exclusion_stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        self.settings['exclusion']['ignore_tags_tags'] = self.exclusion_stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        self.settings['exclusion']['ignore_tags_type'] = self.exclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        self.settings['exclusion']['ignore_tags_type_tags'] = self.exclusion_stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        self.settings['exclusion']['match_tags'] = self.exclusion_checkbox_match_tags.isChecked()
        
        self.settings['exclusion']['context_window_sync'] = self.exclusion_checkbox_context_window_sync.isChecked()
        
        if self.exclusion_spin_box_context_window_left.prefix() == 'L':
            self.settings['exclusion']['context_window_left'] = -self.exclusion_spin_box_context_window_left.value()
        else:
            self.settings['exclusion']['context_window_left'] = self.exclusion_spin_box_context_window_left.value()
            
        if self.exclusion_spin_box_context_window_right.prefix() == 'L':
            self.settings['exclusion']['context_window_right'] = -self.exclusion_spin_box_context_window_right.value()
        else:
            self.settings['exclusion']['context_window_right'] = self.exclusion_spin_box_context_window_right.value()

        if self.settings['exclusion']['exclusion']:
            self.exclusion_checkbox_match_tags.token_settings_changed()

    def multi_search_mode_changed(self):
        if self.settings['inclusion']['multi_search_mode'] or self.settings['exclusion']['multi_search_mode']:
            self.setFixedSize(520, 480)
        else:
            self.setFixedSize(520, 370)

    def token_settings_changed(self):
        self.inclusion_checkbox_match_tags.token_settings_changed()
        self.exclusion_checkbox_match_tags.token_settings_changed()

    def reset_settings(self):
        reply = wordless_message_box.wordless_message_box_reset_settings(self.main)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

    def load(self):
        self.exec_()
