#
# Wordless: Dialogs
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_text import *
from wordless_widgets import wordless_layout, wordless_message_box, wordless_widgets
from wordless_utils import *

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

        (self.label_search_term,
         self.checkbox_multi_search_mode,
         self.line_edit_search_term,
         self.list_search_terms,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_word,
         self.checkbox_use_regex) = wordless_widgets.wordless_widgets_search_settings(main)

        self.button_find_next = QPushButton(main.tr('Find Next'), main)
        self.button_find_prev = QPushButton(main.tr('Find Previous'), main)
        self.button_find_all = QPushButton(main.tr('Find All'), main)
        self.button_clear_highlights = QPushButton(main.tr('Clear Highlights'), main)
        
        self.button_restore_default_settings = QPushButton(main.tr('Restore Default Settings'), main)

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
        self.button_clear_highlights.clicked.connect(lambda: self.clear_highlights())

        self.button_restore_default_settings.clicked.connect(lambda: self.load_settings(defaults = True))

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

        layout_search_buttons.addWidget(self.button_restore_default_settings, 5, 0, Qt.AlignBottom)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.label_search_term, 0, 0)
        self.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.layout().addWidget(self.line_edit_search_term, 1, 0, 1, 2)
        self.layout().addLayout(layout_search_terms, 2, 0, 1, 2)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 2)

        self.layout().addWidget(self.checkbox_ignore_case, 4, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.layout().addWidget(self.checkbox_match_whole_word, 6, 0, 1, 2)
        self.layout().addWidget(self.checkbox_use_regex, 7, 0, 1, 2)

        self.layout().addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 2, 8, 1)

        self.layout().addLayout(layout_search_buttons, 0, 3, 8, 1)

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

    @ wordless_misc.log_timing
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

    @ wordless_misc.log_timing
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

    @ wordless_misc.log_timing
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

            for file in self.table.settings['file']['files_open']:
                if file['selected']:
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
                    item.setBackground(QBrush(QColor('#E53E3A')))

                self.table.blockSignals(False)
                self.table.show()
            else:
                wordless_message_box.wordless_message_box_no_search_results(self.main)

            if len(items_found) == 0:
                self.main.status_bar.showMessage(self.tr('No items found.'))
            elif len(items_found) == 1:
                self.main.status_bar.showMessage(self.tr('Found 1 item.'))
            else:
                self.main.status_bar.showMessage(self.tr(f'Found {len(items_found):,} items.'))
        else:
            wordless_message_box.wordless_message_box_empty_search_term(self.main)

        return items_found

    @ wordless_misc.log_timing
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

        self.main.status_bar.showMessage(self.tr('Highlights Cleared!'))

    def load(self):
        self.load_settings()

        self.search_settings_changed()

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

         self.checkbox_inclusion_ignore_case,
         self.checkbox_inclusion_match_inflected_forms,
         self.checkbox_inclusion_match_whole_word,
         self.checkbox_inclusion_use_regex) = wordless_widgets.wordless_widgets_search_settings(main)

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

        self.checkbox_inclusion_context_window_sync.stateChanged.connect(self.inclusion_changed)
        self.spin_box_inclusion_context_window_left.valueChanged.connect(self.inclusion_changed)
        self.spin_box_inclusion_context_window_right.valueChanged.connect(self.inclusion_changed)

        layout_inclusion_multi_search_mode = QGridLayout()
        layout_inclusion_multi_search_mode.addWidget(self.label_inclusion_search_term, 0, 0)
        layout_inclusion_multi_search_mode.addWidget(self.checkbox_inclusion_multi_search_mode, 0, 1, Qt.AlignRight)

        layout_inclusion_search_terms = QGridLayout()
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms, 0, 0, 6, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_add, 0, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_insert, 1, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_remove, 2, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_clear, 3, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_import, 4, 1)
        layout_inclusion_search_terms.addWidget(self.list_inclusion_search_terms.button_export, 5, 1)

        self.group_box_inclusion.setLayout(QGridLayout())
        self.group_box_inclusion.layout().addLayout(layout_inclusion_multi_search_mode, 0, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.line_edit_inclusion_search_term, 1, 0, 1, 4)
        self.group_box_inclusion.layout().addLayout(layout_inclusion_search_terms, 2, 0, 1, 4)

        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_ignore_case, 4, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_match_inflected_forms, 5, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_match_whole_word, 6, 0, 1, 4)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_use_regex, 7, 0, 1, 4)

        self.group_box_inclusion.layout().addWidget(wordless_layout.Wordless_Separator(self), 8, 0, 1, 4)

        self.group_box_inclusion.layout().addWidget(self.label_inclusion_context_window, 9, 0, 1, 3)
        self.group_box_inclusion.layout().addWidget(self.checkbox_inclusion_context_window_sync, 9, 3, Qt.AlignRight)
        self.group_box_inclusion.layout().addWidget(self.label_inclusion_context_window_left, 10, 0)
        self.group_box_inclusion.layout().addWidget(self.spin_box_inclusion_context_window_left, 10, 1)
        self.group_box_inclusion.layout().addWidget(self.label_inclusion_context_window_right, 10, 2)
        self.group_box_inclusion.layout().addWidget(self.spin_box_inclusion_context_window_right, 10, 3)

        self.group_box_inclusion.layout().setRowStretch(11, 1)
        self.group_box_inclusion.layout().setColumnStretch(1, 1)
        self.group_box_inclusion.layout().setColumnStretch(3, 1)

        # Exclusion
        self.group_box_exclusion = QGroupBox(self.tr('Exclusion'), self)

        self.group_box_exclusion.setCheckable(True)

        (self.label_exclusion_search_term,
         self.checkbox_exclusion_multi_search_mode,
         self.line_edit_exclusion_search_term,
         self.list_exclusion_search_terms,

         self.checkbox_exclusion_ignore_case,
         self.checkbox_exclusion_match_inflected_forms,
         self.checkbox_exclusion_match_whole_word,
         self.checkbox_exclusion_use_regex) = wordless_widgets.wordless_widgets_search_settings(main)

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

        self.checkbox_exclusion_context_window_sync.stateChanged.connect(self.exclusion_changed)
        self.spin_box_exclusion_context_window_left.valueChanged.connect(self.exclusion_changed)
        self.spin_box_exclusion_context_window_right.valueChanged.connect(self.exclusion_changed)

        layout_exclusion_multi_search_mode = QGridLayout()
        layout_exclusion_multi_search_mode.addWidget(self.label_exclusion_search_term, 0, 0)
        layout_exclusion_multi_search_mode.addWidget(self.checkbox_exclusion_multi_search_mode, 0, 1, Qt.AlignRight)

        layout_exclusion_search_terms = QGridLayout()
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms, 0, 0, 6, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_add, 0, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_insert, 1, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_remove, 2, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_clear, 3, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_import, 4, 1)
        layout_exclusion_search_terms.addWidget(self.list_exclusion_search_terms.button_export, 5, 1)

        self.group_box_exclusion.setLayout(QGridLayout())
        self.group_box_exclusion.layout().addLayout(layout_exclusion_multi_search_mode, 0, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.line_edit_exclusion_search_term, 1, 0, 1, 4)
        self.group_box_exclusion.layout().addLayout(layout_exclusion_search_terms, 2, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_ignore_case, 4, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_inflected_forms, 5, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_match_whole_word, 6, 0, 1, 4)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_use_regex, 7, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(wordless_layout.Wordless_Separator(self), 8, 0, 1, 4)

        self.group_box_exclusion.layout().addWidget(self.label_exclusion_context_window, 9, 0, 1, 3)
        self.group_box_exclusion.layout().addWidget(self.checkbox_exclusion_context_window_sync, 9, 3, Qt.AlignRight)
        self.group_box_exclusion.layout().addWidget(self.label_exclusion_context_window_left, 10, 0)
        self.group_box_exclusion.layout().addWidget(self.spin_box_exclusion_context_window_left, 10, 1)
        self.group_box_exclusion.layout().addWidget(self.label_exclusion_context_window_right, 10, 2)
        self.group_box_exclusion.layout().addWidget(self.spin_box_exclusion_context_window_right, 10, 3)

        self.group_box_exclusion.layout().setRowStretch(11, 1)
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

        self.line_edit_inclusion_search_term.setText(settings['inclusion']['search_term'])

        self.list_inclusion_search_terms.clear()

        for search_term in settings['inclusion']['search_terms']:
            self.list_inclusion_search_terms.add_item(search_term)

        self.checkbox_inclusion_ignore_case.setChecked(settings['inclusion']['ignore_case'])
        self.checkbox_inclusion_match_inflected_forms.setChecked(settings['inclusion']['match_inflected_forms'])
        self.checkbox_inclusion_match_whole_word.setChecked(settings['inclusion']['match_whole_word'])
        self.checkbox_inclusion_use_regex.setChecked(settings['inclusion']['use_regex'])

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

        self.line_edit_exclusion_search_term.setText(settings['exclusion']['search_term'])

        self.list_exclusion_search_terms.clear()

        for search_term in settings['exclusion']['search_terms']:
            self.list_exclusion_search_terms.add_item(search_term)

        self.checkbox_exclusion_ignore_case.setChecked(settings['exclusion']['ignore_case'])
        self.checkbox_exclusion_match_inflected_forms.setChecked(settings['exclusion']['match_inflected_forms'])
        self.checkbox_exclusion_match_whole_word.setChecked(settings['exclusion']['match_whole_word'])
        self.checkbox_exclusion_use_regex.setChecked(settings['exclusion']['use_regex'])

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

    def inclusion_changed(self):
        self.settings['inclusion']['inclusion'] = self.group_box_inclusion.isChecked()

        self.settings['inclusion']['multi_search_mode'] = self.checkbox_inclusion_multi_search_mode.isChecked()
        self.settings['inclusion']['search_term'] = self.line_edit_inclusion_search_term.text()
        self.settings['inclusion']['search_terms'] = self.list_inclusion_search_terms.get_items()

        self.settings['inclusion']['ignore_case'] = self.checkbox_inclusion_ignore_case.isChecked()
        self.settings['inclusion']['match_inflected_forms'] = self.checkbox_inclusion_match_inflected_forms.isChecked()
        self.settings['inclusion']['match_whole_word'] = self.checkbox_inclusion_match_whole_word.isChecked()
        self.settings['inclusion']['use_regex'] = self.checkbox_inclusion_use_regex.isChecked()
        
        self.settings['inclusion']['context_window_sync'] = self.checkbox_inclusion_context_window_sync.isChecked()

        if self.spin_box_inclusion_context_window_left.prefix() == 'L':
            self.settings['inclusion']['context_window_left'] = -self.spin_box_inclusion_context_window_left.value()
        else:
            self.settings['inclusion']['context_window_left'] = self.spin_box_inclusion_context_window_left.value()
            
        if self.spin_box_inclusion_context_window_right.prefix() == 'L':
            self.settings['inclusion']['context_window_right'] = -self.spin_box_inclusion_context_window_right.value()
        else:
            self.settings['inclusion']['context_window_right'] = self.spin_box_inclusion_context_window_right.value()

    def exclusion_changed(self):
        self.settings['exclusion']['exclusion'] = self.group_box_exclusion.isChecked()

        self.settings['exclusion']['multi_search_mode'] = self.checkbox_exclusion_multi_search_mode.isChecked()
        self.settings['exclusion']['search_term'] = self.line_edit_exclusion_search_term.text()
        self.settings['exclusion']['search_terms'] = self.list_exclusion_search_terms.get_items()

        self.settings['exclusion']['ignore_case'] = self.checkbox_exclusion_ignore_case.isChecked()
        self.settings['exclusion']['match_inflected_forms'] = self.checkbox_exclusion_match_inflected_forms.isChecked()
        self.settings['exclusion']['match_whole_word'] = self.checkbox_exclusion_match_whole_word.isChecked()
        self.settings['exclusion']['use_regex'] = self.checkbox_exclusion_use_regex.isChecked()
        
        self.settings['exclusion']['context_window_sync'] = self.checkbox_exclusion_context_window_sync.isChecked()
        
        if self.spin_box_exclusion_context_window_left.prefix() == 'L':
            self.settings['exclusion']['context_window_left'] = -self.spin_box_exclusion_context_window_left.value()
        else:
            self.settings['exclusion']['context_window_left'] = self.spin_box_exclusion_context_window_left.value()
            
        if self.spin_box_exclusion_context_window_right.prefix() == 'L':
            self.settings['exclusion']['context_window_right'] = -self.spin_box_exclusion_context_window_right.value()
        else:
            self.settings['exclusion']['context_window_right'] = self.spin_box_exclusion_context_window_right.value()

    def multi_search_mode_changed(self):
        if self.settings['inclusion']['multi_search_mode'] or self.settings['exclusion']['multi_search_mode']:
            self.setFixedSize(500, 440)
        else:
            self.setFixedSize(500, 290)

    def restore_default_settings(self):
        reply = wordless_message_box.wordless_message_box_restore_default_settings(self.main)

        if reply == QMessageBox.Yes:
            self.load_settings(defaults = True)

    def load(self):
        self.exec_()
