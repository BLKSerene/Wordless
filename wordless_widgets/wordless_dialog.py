#
# Wordless: Dialogs
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import os
import platform

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import wordless_layout, wordless_widgets
from wordless_utils import wordless_text

def wordless_message_jre_not_installed(main):
    sys_bit = platform.architecture()[0][:2]
    if sys_bit == '32':
        sys_bit_x = 'x86'
    else:
        sys_bit_x = 'x64'

    QMessageBox.information(main,
                            main.tr('Java Runtime Environment Not Installed'),
                            main.tr(f'''
                                        <p>The HanLP library requires Java Runtime Environment (JRE) to be installed on your computer.</p>
                                        <p>You can download the latest version of JRE here: <a href="https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html">https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html</a>.</p>
                                        <p>After JRE is properly installed, please try again.</p>
                                        <p>Note: You are running the {sys_bit}-bit version of Wordless, so you should install the {sys_bit_x} version of JRE!</p>
                                    '''),
                            QMessageBox.Ok)

def wordless_message_empty_search_term(main):
    QMessageBox.warning(main,
                        main.tr('Empty Search Term'),
                        main.tr('Please enter your search term(s) first!'),
                        QMessageBox.Ok)

def wordless_message_no_search_results(main):
    QMessageBox.warning(main,
                        main.tr('No Search Results'),
                        main.tr('There is nothing that could be found in the table.'),
                        QMessageBox.Ok)

def wordless_message_empty_results_table(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr('There is nothing to be shown in the table.<br>You might want to change your search term(s) and/or your settings, and then try again.'),
                            QMessageBox.Ok)

def wordless_message_empty_results_plot(main):
    QMessageBox.information(main,
                            main.tr('No Search Results'),
                            main.tr('There is nothing to be shown in the figure.<br>You might want to change your search term(s) and/or your settings, and then try again.'),
                            QMessageBox.Ok)

class Wordless_Dialog(QDialog):
    def __init__(self, main, title):
        super().__init__(main)

        self.main = main

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('images/wordless_icon.png'))

class Wordless_Dialog_Info(Wordless_Dialog):
	def __init__(self, main, title):
		super().__init__(main, title)

		self.wrapper_info = QWidget(self)

		self.button_ok = QPushButton(self.tr('OK'), self)

		self.button_ok.clicked.connect(self.accept)

		self.setLayout(QGridLayout())
		self.layout().addWidget(self.wrapper_info, 0, 0)
		self.layout().addWidget(self.button_ok, 1, 0, Qt.AlignRight)

class Wordless_Dialog_Search(Wordless_Dialog):
    def __init__(self, main, tab, table, cols_search):
        super().__init__(main, main.tr('Search in Results'))

        self.tab = tab
        self.table = table

        if type(cols_search) != list:
            self.cols_search = [cols_search]
        else:
            self.cols_search = cols_search

        self.settings = self.main.settings_custom[self.tab]['search_results']
        self.size_old = self.sizeHint()

        (self.label_search_term,
         self.checkbox_show_all,
         self.line_edit_search_term,
         self.list_search_terms,
         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_word,
         self.checkbox_use_regex,
         self.checkbox_multi_search_mode) = wordless_widgets.wordless_widgets_search(main)

        self.checkbox_show_all.hide()

        self.button_find_next = QPushButton(main.tr('Find Next'), main)
        self.button_find_prev = QPushButton(main.tr('Find Previous'), main)
        self.button_find_all = QPushButton(main.tr('Find All'), main)
        self.button_clear_highlights = QPushButton(main.tr('Clear Highlights'), main)
        
        self.button_restore_defaults = QPushButton(main.tr('Restore Defaults'), main)

        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.button_find_next.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_word.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)
        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)

        self.button_find_next.clicked.connect(self.find_next)
        self.button_find_prev.clicked.connect(self.find_prev)
        self.button_find_all.clicked.connect(self.find_all)
        self.button_clear_highlights.clicked.connect(self.clear_highlights)

        self.button_restore_defaults.clicked.connect(lambda: self.load_settings(defaults = True))

        layout_search_terms = QGridLayout()
        layout_search_terms.addWidget(self.list_search_terms, 0, 0, 6, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_add, 0, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_insert, 1, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_remove, 2, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_clear, 3, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_import, 4, 1)
        layout_search_terms.addWidget(self.list_search_terms.button_export, 5, 1)

        layout_search_buttons = QGridLayout()
        layout_search_buttons.addWidget(self.button_find_next, 0, 0)
        layout_search_buttons.addWidget(self.button_find_prev, 1, 0)
        layout_search_buttons.addWidget(self.button_find_all, 2, 0)
        layout_search_buttons.addWidget(self.button_clear_highlights, 4, 0)

        layout_search_buttons.addWidget(self.button_restore_defaults, 5, 0, Qt.AlignBottom)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.label_search_term, 0, 0)
        self.layout().addWidget(self.line_edit_search_term, 1, 0)
        self.layout().addLayout(layout_search_terms, 2, 0)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0)

        self.layout().addWidget(self.checkbox_ignore_case, 4, 0)
        self.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0)
        self.layout().addWidget(self.checkbox_match_whole_word, 6, 0)
        self.layout().addWidget(self.checkbox_use_regex, 7, 0)
        self.layout().addWidget(self.checkbox_multi_search_mode, 8, 0)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 1, 9, 1)

        self.layout().addLayout(layout_search_buttons, 0, 2, 9, 1)

        self.main.tabs.currentChanged.connect(self.accept)

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
            self.setFixedSize(350, 350)
        else:
            self.setFixedSize(300, 200)

    def find_next(self):
        items_found = self.find_all()

        self.table.hide()
        self.table.blockSignals(True)

        # Scroll to the next found item
        if items_found:
            selected_rows = self.table.selected_rows()

            self.table.clearSelection()

            if selected_rows:
                for item in items_found:
                    if item.row() > selected_rows[-1]:
                        self.table.selectRow(item.row())
                        self.table.setFocus()

                        self.table.scrollToItem(item)

                        break
            else:
                self.table.scrollToItem(items_found[0])
                self.table.selectRow(items_found[0].row())

            # Scroll to top if no next items exist
            if not self.table.selectedItems():
                self.table.scrollToItem(items_found[0])
                self.table.selectRow(items_found[0].row())

        self.table.blockSignals(False)
        self.table.show()

    def find_prev(self):
        items_found = self.find_all()

        self.table.hide()
        self.table.blockSignals(True)

        # Scroll to the previous found item
        if items_found:
            selected_rows = self.table.selected_rows()

            self.table.clearSelection()

            if selected_rows:
                for item in reversed(items_found):
                    if item.row() < selected_rows[0]:
                        self.table.selectRow(item.row())
                        self.table.setFocus()

                        self.table.scrollToItem(item)

                        break
            else:
                self.table.scrollToItem(items_found[-1])
                self.table.selectRow(items_found[-1].row())

            # Scroll to top if no next items exist
            if not self.table.selectedItems():
                self.table.scrollToItem(items_found[-1])
                self.table.selectRow(items_found[-1].row())

        self.table.blockSignals(False)
        self.table.show()

    def find_all(self):
        search_terms_files = set()
        items_found = []

        cols_search = self.table.find_col(self.cols_search)

        if (self.settings['multi_search_mode'] and self.settings['search_terms'] or
            not self.settings['multi_search_mode'] and self.settings['search_term']):
            if self.settings['multi_search_mode']:
                search_terms = self.settings['search_terms']
            else:
                search_terms = [self.settings['search_term']]

            # Create temporary file
            with open('wordless_text_temp.txt', 'w', encoding = 'utf_8') as f:
                for row in range(self.table.rowCount()):
                    for col in cols_search:
                        f.write(f'{self.table.item(row, col).text()}\n')

            file_temp = self.main.wordless_files._new_file('wordless_text_temp.txt', auto_detect = False)
            file_temp_text = wordless_text.Wordless_Text(self.main, file_temp)

            with open('wordless_text_temp.txt', 'r', encoding = 'utf_8') as f:
                file_temp_text.tokens = [line.rstrip().split() for line in f]

            for file in self.table.files:
                file_temp_text.lang = file['lang_code']

                search_terms_files |= file_temp_text.match_tokens(search_terms,
                                                                  self.settings['ignore_case'],
                                                                  self.settings['match_inflected_forms'],
                                                                  self.settings['match_whole_word'],
                                                                  self.settings['use_regex'])

            os.remove('wordless_text_temp.txt')

            for row in range(self.table.rowCount()):
                for col in cols_search:
                    item = self.table.item(row, col)

                    if item.text() in search_terms_files:
                        items_found.append(item)

            if items_found:
                self.clear_highlights()

                self.table.hide()
                self.table.blockSignals(True)

                for item in items_found:
                    item.setForeground(QBrush(QColor('#FFF')))
                    item.setBackground(QBrush(QColor('#F00')))

                self.table.blockSignals(False)
                self.table.show()
            else:
                wordless_message_no_search_results(self.main)

            self.main.status_bar.showMessage(self.tr(f'Found {len(items_found):,} item(s).'))
        else:
            wordless_message_empty_search_term(self.main)

        return items_found

    def clear_highlights(self):
        self.table.hide()
        self.table.blockSignals(True)

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)

                item.setForeground(QBrush(QColor('#292929')))
                item.setBackground(QBrush(QColor('#FFF')))

        self.table.blockSignals(False)
        self.table.show()

    def load(self):
        self.load_settings()

        self.show()
