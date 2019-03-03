#
# Wordless: Dialogs - Search in Results
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_dialogs import wordless_dialog, wordless_dialog_misc, wordless_message_box
from wordless_text import wordless_matching
from wordless_widgets import wordless_button, wordless_layout, wordless_message, wordless_widgets
from wordless_utils import wordless_misc, wordless_threading

class Wordless_Worker_Search_Results(wordless_threading.Wordless_Worker):
    searching_finished = pyqtSignal()

    def __init__(self, main, dialog_search_results):
        super().__init__(main)

        self.dialog = dialog_search_results

    def search_results(self):
        results = {}
        search_terms = set()

        for col in range(self.dialog.table.columnCount()):
            if self.dialog.table.cellWidget(0, col):
                for row in range(self.dialog.table.rowCount()):
                    results[(row, col)] = self.dialog.table.cellWidget(row, col).text_search
            else:
                for row in range(self.dialog.table.rowCount()):
                    try:
                        results[(row, col)] = self.dialog.table.item(row, col).text_raw
                    except:
                        results[(row, col)] = [self.dialog.table.item(row, col).text()]

        items = [token for text in results.values() for token in text]

        for file in self.dialog.table.settings['files']['files_open']:
            if file['selected']:
                search_terms_file = wordless_matching.match_search_terms(
                    self.main, items,
                    lang = file['lang'],
                    text_type = ('tokenized', 'tagged_both'),
                    token_settings = self.dialog.table.settings[self.dialog.tab]['token_settings'],
                    search_settings = self.dialog.settings)

                search_terms |= set(search_terms_file)

        for search_term in search_terms:
            len_search_term = len(search_term)

            for (row, col), text in results.items():
                for ngram in nltk.ngrams(text, len_search_term):
                    if ngram == search_term:
                        self.dialog.items_found.append([row, col])

        self.dialog.items_found = sorted(self.dialog.items_found)

        self.progress_updated.emit(self.tr('Highlighting items ...'))

        time.sleep(0.1)

        self.searching_finished.emit()

class Wordless_Dialog_Search_Results(wordless_dialog.Wordless_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, main.tr('Search in Results'))

        self.tab = tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['search_results']
        self.items_found = []

        (self.label_search_term,
         self.checkbox_multi_search_mode,
         self.line_edit_search_term,
         self.list_search_terms,
         self.label_separator,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_words,
         self.checkbox_use_regex,

         self.stacked_widget_ignore_tags,
         self.stacked_widget_ignore_tags_type,
         self.label_ignore_tags,
         self.checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self, self.tab)

        self.button_find_next = QPushButton(self.tr('Find Next'), self)
        self.button_find_prev = QPushButton(self.tr('Find Previous'), self)
        self.button_find_all = QPushButton(self.tr('Find All'), self)
        
        self.button_reset_settings = wordless_button.Wordless_Button_Reset_Settings(self, self.load_settings)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.button_find_next.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.search_settings_changed)
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.search_settings_changed)
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        self.button_find_next.clicked.connect(lambda: self.find_next())
        self.button_find_prev.clicked.connect(lambda: self.find_prev())
        self.button_find_all.clicked.connect(lambda: self.find_all())

        self.button_close.clicked.connect(self.reject)

        layout_search_terms = QGridLayout()
        layout_search_terms.addWidget(self.list_search_terms, 0, 0, 5, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_add, 0, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_remove, 1, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_clear, 2, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_import, 3, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_export, 4, 1)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags_type, 0, 1)
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
        self.layout().addWidget(self.checkbox_match_whole_words, 6, 0, 1, 2)
        self.layout().addWidget(self.checkbox_use_regex, 7, 0, 1, 2)

        self.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_tags, 9, 0, 1, 2)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 2, 10, 1)

        self.layout().addLayout(layout_buttons_right, 0, 3, 10, 1)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 10, 0, 1, 4)

        self.layout().addLayout(layout_buttons_bottom, 11, 0, 1, 4)

        self.main.wordless_work_area.currentChanged.connect(self.reject)

        self.load_settings()

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
        self.checkbox_match_whole_words.setChecked(settings['match_whole_words'])
        self.checkbox_use_regex.setChecked(settings['use_regex'])

        self.stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['ignore_tags'])
        self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['ignore_tags_tags'])
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['ignore_tags_type'])
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['match_tags'])

        self.search_settings_changed()

    def search_settings_changed(self):
        self.settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        self.settings['search_term'] = self.line_edit_search_term.text()
        self.settings['search_terms'] = self.list_search_terms.get_items()

        self.settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        self.settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        self.settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        self.settings['use_regex'] = self.checkbox_use_regex.isChecked()

        self.settings['ignore_tags'] = self.stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        self.settings['ignore_tags_tags'] = self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        self.settings['ignore_tags_type'] = self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        self.settings['ignore_tags_type_tags'] = self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        self.settings['match_tags'] = self.checkbox_match_tags.isChecked()

        if self.settings['multi_search_mode']:
            self.setFixedSize(360, 390)
        else:
            self.setFixedSize(360, 280)

    @wordless_misc.log_timing
    def find_next(self):
        self.find_all()

        self.table.hide()
        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

        # Scroll to the next found item
        if self.items_found:
            selected_rows = self.table.get_selected_rows()

            self.table.clearSelection()

            if selected_rows:
                for row, _ in self.items_found:
                    if row > selected_rows[-1]:
                        self.table.selectRow(row)
                        self.table.setFocus()

                        self.table.scrollToItem(self.table.item(row, 0))

                        break
            else:
                self.table.scrollToItem(self.table.item(self.items_found[0][0], 0))
                self.table.selectRow(self.items_found[0][0])

            # Scroll to top if this is the last item
            if not self.table.selectedItems():
                self.table.scrollToItem(self.table.item(self.items_found[0][0], 0))
                self.table.selectRow(self.items_found[0][0])

        self.table.blockSignals(False)
        self.table.setUpdatesEnabled(True)
        self.table.show()

    @wordless_misc.log_timing
    def find_prev(self):
        self.find_all()

        self.table.hide()
        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

        # Scroll to the previous found item
        if self.items_found:
            selected_rows = self.table.get_selected_rows()

            self.table.clearSelection()

            if selected_rows:
                for row, _ in reversed(self.items_found):
                    if row < selected_rows[0]:
                        self.table.selectRow(row)
                        self.table.setFocus()

                        self.table.scrollToItem(self.table.item(row, 0))

                        break
            else:
                self.table.scrollToItem(self.table.item(self.items_found[-1][0], 0))
                self.table.selectRow(self.items_found[-1][0])

            # Scroll to top if no next items exist
            if not self.table.selectedItems():
                self.table.scrollToItem(self.table.item(indexes_found[-1][0], 0))
                self.table.selectRow(indexes_found[-1][0])

        self.table.blockSignals(False)
        self.table.setUpdatesEnabled(True)
        self.table.show()

    @wordless_misc.log_timing
    def find_all(self):
        def data_received():
            if self.items_found:
                self.table.hide()
                self.table.blockSignals(True)
                self.table.setUpdatesEnabled(False)

                for row, col in self.items_found:
                    if self.table.cellWidget(row, col):
                        self.table.cellWidget(row, col).setStyleSheet('border: 1px solid #E53E3A;')
                    else:
                        self.table.item(row, col).setForeground(QBrush(QColor('#FFF')))
                        self.table.item(row, col).setBackground(QBrush(QColor('#E53E3A')))

                self.table.blockSignals(False)
                self.table.setUpdatesEnabled(True)
                self.table.show()
            else:
                wordless_message_box.wordless_message_box_no_search_results(self.main)

            wordless_message.wordless_message_search_results_success(self.main, self.items_found)

            dialog_progress.accept()

        if (not self.settings['multi_search_mode'] and self.settings['search_term'] or
            self.settings['multi_search_mode'] and self.settings['search_terms']):
            self.clear_highlights()

            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Search_Results(self.main)

            worker_search_results = Wordless_Worker_Search_Results(self.main, self)
            thread_search_results = wordless_threading.Wordless_Thread_Search_Results(worker_search_results)

            worker_search_results.progress_updated.connect(dialog_progress.update_progress)
            worker_search_results.searching_finished.connect(data_received)

            thread_search_results.start()

            dialog_progress.exec_()

            thread_search_results.quit()
            thread_search_results.wait()
        else:
            wordless_message_box.wordless_message_box_missing_search_term(self.main)

            wordless_message.wordless_message_search_results_error(self.main)

    def clear_highlights(self):
        if self.items_found:
            self.table.hide()
            self.table.blockSignals(True)
            self.table.setUpdatesEnabled(False)

            for row, col in self.items_found:
                if self.table.cellWidget(row, col):
                    self.table.cellWidget(row, col).setStyleSheet('border: 0')
                else:
                    self.table.item(row, col).setForeground(QBrush(QColor('#292929')))
                    self.table.item(row, col).setBackground(QBrush(QColor('#FFF')))

            self.table.blockSignals(False)
            self.table.setUpdatesEnabled(True)
            self.table.show()

            self.items_found.clear()

    def load(self):
        self.show()
