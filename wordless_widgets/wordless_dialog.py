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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import nltk

from wordless_text import wordless_matching
from wordless_widgets import (wordless_box, wordless_button, wordless_layout,
                              wordless_message, wordless_message_box, wordless_widgets)
from wordless_utils import wordless_misc

class Wordless_Dialog(QDialog):
    def __init__(self, main, title):
        super().__init__(main)

        self.main = main

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('imgs/wordless_icon.png'))
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def move_to_center(self):
        self.move((self.main.width() - self.width()) / 2,
                  (self.main.height() - self.height()) / 2,)

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

        self.button_reset_settings = wordless_button.Wordless_Button_Reset_Settings(self, self.load_settings)
        self.button_ok = QPushButton(self.tr('OK'), self)

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

    def load(self):
        self.exec_()

class Wordless_Dialog_Filter_Results(Wordless_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, main.tr('Filter Results'))

        self.tab = tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['filter_results']

        self.label_file_to_filter = QLabel(self.tr('File to Filter:'), self)
        self.combo_box_file_to_filter = wordless_box.Wordless_Combo_Box_File_To_Filter(self, self.table)
        self.button_filter = QPushButton(self.tr('Filter'), self)

        self.button_reset_settings = wordless_button.Wordless_Button_Reset_Settings(self, self.load_settings)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.button_filter.setFixedWidth(90)
        self.button_reset_settings.setFixedWidth(140)
        self.button_close.setFixedWidth(90)

        self.combo_box_file_to_filter.currentTextChanged.connect(self.file_to_filter_changed)
        self.button_filter.clicked.connect(lambda: self.filter_results())

        self.button_close.clicked.connect(self.reject)

        self.main.wordless_work_area.currentChanged.connect(self.reject)

        layout_file_to_filter = QGridLayout()
        layout_file_to_filter.addWidget(self.label_file_to_filter, 0, 0)
        layout_file_to_filter.addWidget(self.combo_box_file_to_filter, 0, 1)
        layout_file_to_filter.addWidget(self.button_filter, 0, 2)

        layout_file_to_filter.setColumnStretch(1, 1)

        self.layout_filters = QGridLayout()

        layout_buttons = QGridLayout()
        layout_buttons.addWidget(self.button_reset_settings, 0, 0)
        layout_buttons.addWidget(self.button_close, 0, 1, Qt.AlignRight)

        self.setLayout(QGridLayout())
        self.layout().addLayout(layout_file_to_filter, 0, 0)
        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 1, 0)
        self.layout().addLayout(self.layout_filters, 2, 0)
        self.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0)
        self.layout().addLayout(layout_buttons, 4, 0)

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.settings_default[self.tab]['filter_results']
        else:
            settings = self.settings

        self.combo_box_file_to_filter.setCurrentText(settings['file_to_filter'])

    def file_to_filter_changed(self):
        self.settings['file_to_filter'] = self.combo_box_file_to_filter.currentText()

    def filter_results(self):
        pass

    def load(self):
        self.show()

class Wordless_Dialog_Filter_Results_Wordlist(Wordless_Dialog_Filter_Results):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        if self.tab == 'wordlist':
            self.label_len_token = QLabel(self.tr('Token Length:'), self)
            (self.label_len_token_min,
             self.spin_box_len_token_min,
             self.checkbox_len_token_min_no_limit,
             self.label_len_token_max,
             self.spin_box_len_token_max,
             self.checkbox_len_token_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 1,
                                                                                              filter_max = 100)
        elif self.tab == 'ngrams':
            self.label_len_ngram = QLabel(self.tr('N-gram Length:'), self)
            (self.label_len_ngram_min,
             self.spin_box_len_ngram_min,
             self.checkbox_len_ngram_min_no_limit,
             self.label_len_ngram_max,
             self.spin_box_len_ngram_max,
             self.checkbox_len_ngram_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 1,
                                                                                              filter_max = 100)

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (self.label_freq_min,
         self.spin_box_freq_min,
         self.checkbox_freq_min_no_limit,
         self.label_freq_max,
         self.spin_box_freq_max,
         self.checkbox_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 0,
                                                                                     filter_max = 1000000)

        self.label_dispersion = QLabel(self.tr('Dispersion:'), self)
        (self.label_dispersion_min,
         self.spin_box_dispersion_min,
         self.checkbox_dispersion_min_no_limit,
         self.label_dispersion_max,
         self.spin_box_dispersion_max,
         self.checkbox_dispersion_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self,
                                                                                                    filter_min = 0,
                                                                                                    filter_max = 1)

        self.label_adjusted_freq = QLabel(self.tr('Adjusted Frequency:'), self)
        (self.label_adjusted_freq_min,
         self.spin_box_adjusted_freq_min,
         self.checkbox_adjusted_freq_min_no_limit,
         self.label_adjusted_freq_max,
         self.spin_box_adjusted_freq_max,
         self.checkbox_adjusted_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 0,
                                                                                              filter_max = 1000000)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_num_files_found_min,
         self.spin_box_num_files_found_min,
         self.checkbox_num_files_found_min_no_limit,
         self.label_num_files_found_max,
         self.spin_box_num_files_found_max,
         self.checkbox_num_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                filter_min = 1,
                                                                                                filter_max = 100000)

        if self.tab == 'wordlist':
            self.spin_box_len_token_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_token_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_max_no_limit.stateChanged.connect(self.filters_changed)
        elif self.tab == 'ngrams':
            self.spin_box_len_ngram_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_ngram_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_dispersion_min.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_dispersion_max.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_adjusted_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_adjusted_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        if self.tab == 'wordlist':
            self.layout_filters.addWidget(self.label_len_token, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_token_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_token_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_max_no_limit, 2, 2)
        elif self.tab == 'ngrams':
            self.layout_filters.addWidget(self.label_len_ngram, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_ngram_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_ngram_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_dispersion, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_dispersion_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_dispersion_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_adjusted_freq, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_adjusted_freq_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_adjusted_freq_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 8, 2)

        self.layout_filters.addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 3, 9, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        if self.tab == 'wordlist':
            self.spin_box_len_token_min.setValue(settings['len_token_min'])
            self.checkbox_len_token_min_no_limit.setChecked(settings['len_token_min_no_limit'])
            self.spin_box_len_token_max.setValue(settings['len_token_max'])
            self.checkbox_len_token_max_no_limit.setChecked(settings['len_token_max_no_limit'])
        elif self.tab == 'ngrams':
            self.spin_box_len_ngram_min.setValue(settings['len_ngram_min'])
            self.checkbox_len_ngram_min_no_limit.setChecked(settings['len_ngram_min_no_limit'])
            self.spin_box_len_ngram_max.setValue(settings['len_ngram_max'])
            self.checkbox_len_ngram_max_no_limit.setChecked(settings['len_ngram_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_dispersion_min.setValue(settings['dispersion_min'])
        self.checkbox_dispersion_min_no_limit.setChecked(settings['dispersion_min_no_limit'])
        self.spin_box_dispersion_max.setValue(settings['dispersion_max'])
        self.checkbox_dispersion_max_no_limit.setChecked(settings['dispersion_max_no_limit'])

        self.spin_box_adjusted_freq_min.setValue(settings['adjusted_freq_min'])
        self.checkbox_adjusted_freq_min_no_limit.setChecked(settings['adjusted_freq_min_no_limit'])
        self.spin_box_adjusted_freq_max.setValue(settings['adjusted_freq_max'])
        self.checkbox_adjusted_freq_max_no_limit.setChecked(settings['adjusted_freq_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        if self.tab == 'wordlist':
            self.settings['len_token_min'] = self.spin_box_len_token_min.value()
            self.settings['len_token_min_no_limit'] = self.checkbox_len_token_min_no_limit.isChecked()
            self.settings['len_token_max'] = self.spin_box_len_token_max.value()
            self.settings['len_token_max_no_limit'] = self.checkbox_len_token_max_no_limit.isChecked()
        elif self.tab == 'ngrams':
            self.settings['len_ngram_min'] = self.spin_box_len_ngram_min.value()
            self.settings['len_ngram_min_no_limit'] = self.checkbox_len_ngram_min_no_limit.isChecked()
            self.settings['len_ngram_max'] = self.spin_box_len_ngram_max.value()
            self.settings['len_ngram_max_no_limit'] = self.checkbox_len_ngram_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['dispersion_min'] = self.spin_box_dispersion_min.value()
        self.settings['dispersion_min_no_limit'] = self.checkbox_dispersion_min_no_limit.isChecked()
        self.settings['dispersion_max'] = self.spin_box_dispersion_max.value()
        self.settings['dispersion_max_no_limit'] = self.checkbox_dispersion_max_no_limit.isChecked()

        self.settings['adjusted_freq_min'] = self.spin_box_adjusted_freq_min.value()
        self.settings['adjusted_freq_min_no_limit'] = self.checkbox_adjusted_freq_min_no_limit.isChecked()
        self.settings['adjusted_freq_max'] = self.spin_box_adjusted_freq_max.value()
        self.settings['adjusted_freq_max_no_limit'] = self.checkbox_adjusted_freq_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
        text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

        self.label_dispersion.setText(f'{text_dispersion}:')
        self.label_adjusted_freq.setText(f'{text_adjusted_freq}:')

    @wordless_misc.log_timing
    def filter_results(self):
        if any([self.table.item(0, i) for i in range(self.table.columnCount())]):
            text_measure_dispersion = self.table.settings[self.tab]['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = self.table.settings[self.tab]['generation_settings']['measure_adjusted_freq']

            text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
            text_adjusted_freq =  self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

            if self.tab == 'wordlist':
                col_tokens = self.table.find_col(self.tr('Tokens'))
            elif self.tab == 'ngrams':
                col_ngrams = self.table.find_col(self.tr('N-grams'))

            if self.settings['file_to_filter'] == self.tr('Total'):
                col_freq = self.table.find_col(self.tr('Total\nFrequency'))
                col_dispersion = self.table.find_col(self.tr(f'Total\n{text_dispersion}'))
                col_adjusted_freq = self.table.find_col(self.tr(f'Total\n{text_adjusted_freq}'))
            else:
                col_freq = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\nFrequency"))
                col_dispersion = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{text_dispersion}"))
                col_adjusted_freq = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{text_adjusted_freq}"))

            col_num_files_found = self.table.find_col(self.tr('Number of\nFiles Found'))

            if self.tab == 'wordlist':
                len_token_min = (float('-inf')
                                 if self.settings['len_token_min_no_limit'] else self.settings['len_token_min'])
                len_token_max = (float('inf')
                                 if self.settings['len_token_max_no_limit'] else self.settings['len_token_max'])
            elif self.tab == 'ngrams':
                len_ngram_min = (float('-inf')
                                 if self.settings['len_ngram_min_no_limit'] else self.settings['len_ngram_min'])
                len_ngram_max = (float('inf')
                                 if self.settings['len_ngram_max_no_limit'] else self.settings['len_ngram_max'])

            freq_min = (float('-inf')
                        if self.settings['freq_min_no_limit'] else self.settings['freq_min'])
            freq_max = (float('inf')
                        if self.settings['freq_max_no_limit'] else self.settings['freq_max'])

            dispersion_min = (float('-inf')
                              if self.settings['dispersion_min_no_limit'] else self.settings['dispersion_min'])
            dispersion_max = (float('inf')
                              if self.settings['dispersion_max_no_limit'] else self.settings['dispersion_max'])

            adjusted_freq_min = (float('-inf')
                                 if self.settings['adjusted_freq_min_no_limit'] else self.settings['adjusted_freq_min'])
            adjusted_freq_max = (float('inf')
                                 if self.settings['adjusted_freq_max_no_limit'] else self.settings['adjusted_freq_max'])

            num_files_found_min = (float('-inf')
                                   if self.settings['num_files_found_min_no_limit'] else self.settings['num_files_found_min'])
            num_files_found_max = (float('inf')
                                   if self.settings['num_files_found_max_no_limit'] else self.settings['num_files_found_max'])

            self.table.row_filters = []

            if self.tab == 'wordlist':
                for i in range(self.table.rowCount()):
                    if (len_token_min       <= len(self.table.item(i, col_tokens).text())  <= len_token_max and
                        freq_min            <= self.table.item(i, col_freq).val_raw        <= freq_max and
                        dispersion_min      <= self.table.item(i, col_dispersion).val      <= dispersion_max and
                        adjusted_freq_min   <= self.table.item(i, col_adjusted_freq).val   <= adjusted_freq_max and
                        num_files_found_min <= self.table.item(i, col_num_files_found).val <= num_files_found_max):
                        self.table.row_filters.append(True)
                    else:
                        self.table.row_filters.append(False)
            elif self.tab == 'ngrams':
                for i in range(self.table.rowCount()):
                    if (len_ngram_min       <= len(self.table.item(i, col_ngrams).text())  <= len_ngram_max and
                        freq_min            <= self.table.item(i, col_freq).val_raw        <= freq_max and
                        dispersion_min      <= self.table.item(i, col_dispersion).val      <= dispersion_max and
                        adjusted_freq_min   <= self.table.item(i, col_adjusted_freq).val   <= adjusted_freq_max and
                        num_files_found_min <= self.table.item(i, col_num_files_found).val <= num_files_found_max):
                        self.table.row_filters.append(True)
                    else:
                        self.table.row_filters.append(False)

            self.table.filter_table()

        wordless_message.wordless_message_filter_table_done(self.main)

class Wordless_Dialog_Filter_Results_Collocation(Wordless_Dialog_Filter_Results):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.label_len_collocate = QLabel(self.tr('Collocate Length:'), self)
        (self.label_len_collocate_min,
         self.spin_box_len_collocate_min,
         self.checkbox_len_collocate_min_no_limit,
         self.label_len_collocate_max,
         self.spin_box_len_collocate_max,
         self.checkbox_len_collocate_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                              filter_min = 1,
                                                                                              filter_max = 100)

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        self.combo_box_freq_position = wordless_box.Wordless_Combo_Box(self)
        (self.label_freq_min,
         self.spin_box_freq_min,
         self.checkbox_freq_min_no_limit,
         self.label_freq_max,
         self.spin_box_freq_max,
         self.checkbox_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 0,
                                                                                     filter_max = 1000000)

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (self.label_test_stat_min,
         self.spin_box_test_stat_min,
         self.checkbox_test_stat_min_no_limit,
         self.label_test_stat_max,
         self.spin_box_test_stat_max,
         self.checkbox_test_stat_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_p_value = QLabel(self.tr('p-value:'), self)
        (self.label_p_value_min,
         self.spin_box_p_value_min,
         self.checkbox_p_value_min_no_limit,
         self.label_p_value_max,
         self.spin_box_p_value_max,
         self.checkbox_p_value_max_no_limit) = wordless_widgets.wordless_widgets_filter_p_value(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (self.label_bayes_factor_min,
         self.spin_box_bayes_factor_min,
         self.checkbox_bayes_factor_min_no_limit,
         self.label_bayes_factor_max,
         self.spin_box_bayes_factor_max,
         self.checkbox_bayes_factor_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (self.label_effect_size_min,
         self.spin_box_effect_size_min,
         self.checkbox_effect_size_min_no_limit,
         self.label_effect_size_max,
         self.spin_box_effect_size_max,
         self.checkbox_effect_size_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_num_files_found_min,
         self.spin_box_num_files_found_min,
         self.checkbox_num_files_found_min_no_limit,
         self.label_num_files_found_max,
         self.spin_box_num_files_found_max,
         self.checkbox_num_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                filter_min = 1,
                                                                                                filter_max = 100000)

        self.spin_box_len_collocate_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_collocate_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_max_no_limit.stateChanged.connect(self.filters_changed)

        self.combo_box_freq_position.currentTextChanged.connect(self.filters_changed)
        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        layout_freq_position = QGridLayout()
        layout_freq_position.addWidget(self.label_freq, 0, 0)
        layout_freq_position.addWidget(self.combo_box_freq_position, 0, 1, Qt.AlignRight)

        self.layout_filters.addWidget(self.label_len_collocate, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_collocate_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_collocate_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_max_no_limit, 2, 2)

        self.layout_filters.addLayout(layout_freq_position, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_value, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_value_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_value_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_collocate_min.setValue(settings['len_collocate_min'])
        self.checkbox_len_collocate_min_no_limit.setChecked(settings['len_collocate_min_no_limit'])
        self.spin_box_len_collocate_max.setValue(settings['len_collocate_max'])
        self.checkbox_len_collocate_max_no_limit.setChecked(settings['len_collocate_max_no_limit'])

        self.combo_box_freq_position.setCurrentText(settings['freq_position'])
        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_collocate_min'] = self.spin_box_len_collocate_min.value()
        self.settings['len_collocate_min_no_limit'] = self.checkbox_len_collocate_min_no_limit.isChecked()
        self.settings['len_collocate_max'] = self.spin_box_len_collocate_max.value()
        self.settings['len_collocate_max_no_limit'] = self.checkbox_len_collocate_max_no_limit.isChecked()

        self.settings['freq_position'] = self.combo_box_freq_position.currentText()
        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_value_min'] = self.spin_box_p_value_min.value()
        self.settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        self.settings['p_value_max'] = self.spin_box_p_value_max.value()
        self.settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        # Frequency
        freq_position_old = settings['filter_results']['freq_position']

        self.combo_box_freq_position.clear()

        for i in range(settings['generation_settings']['window_left'], settings['generation_settings']['window_right'] + 1):
            if i < 0:
                self.combo_box_freq_position.addItem(f'L{-i}')
            elif i > 0:
                self.combo_box_freq_position.addItem(f'R{i}')

        self.combo_box_freq_position.addItem(self.tr('Total'))

        if self.combo_box_freq_position.findText(freq_position_old) > -1:
            self.combo_box_freq_position.setCurrentText(freq_position_old)
        else:
            self.combo_box_freq_position.setCurrentText(self.main.settings_default['collocation']['filter_results']['freq_position'])

        # Filters
        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (text_test_stat,
         text_p_value,
         text_bayes_factor) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
        text_effect_size =  self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(self.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        if text_bayes_factor:
            if not self.checkbox_bayes_factor_min_no_limit.isChecked():
                self.spin_box_bayes_factor_min.setEnabled(True)
            if not self.checkbox_bayes_factor_max_no_limit.isChecked():
                self.spin_box_bayes_factor_max.setEnabled(True)

            self.checkbox_bayes_factor_min_no_limit.setEnabled(True)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(True)
        else:
            self.spin_box_bayes_factor_min.setEnabled(False)
            self.checkbox_bayes_factor_min_no_limit.setEnabled(False)
            self.spin_box_bayes_factor_max.setEnabled(False)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{text_effect_size}:')

    @wordless_misc.log_timing
    def filter_results(self):
        if any([self.table.item(0, i) for i in range(self.table.columnCount())]):
            text_test_significance = self.table.settings['collocation']['generation_settings']['test_significance']
            text_measure_effect_size = self.table.settings['collocation']['generation_settings']['measure_effect_size']

            (text_test_stat,
             text_p_value,
             text_bayes_factor) = self.main.settings_global['tests_significance']['collocation'][text_test_significance]['cols']
            text_effect_size = self.main.settings_global['measures_effect_size']['collocation'][text_measure_effect_size]['col']

            col_collocates = self.table.find_col('Collocates')

            if self.settings['file_to_filter'] == self.tr('Total'):
                if self.settings['freq_position'] == self.tr('Total'):
                    col_freq = self.table.find_col(self.tr('Total\nFrequency'))
                else:
                    col_freq = self.table.find_col(self.tr(f'Total\n{self.settings["freq_position"]}'))

                col_test_stat = self.table.find_col(self.tr(f'Total\n{text_test_stat}'))
                col_p_value = self.table.find_col(self.tr(f'Total\n{text_p_value}'))
                col_bayes_factor = self.table.find_col(self.tr(f'Total\n{text_bayes_factor}'))
                col_effect_size = self.table.find_col(self.tr(f'Total\n{text_effect_size}'))
            else:
                if self.settings['freq_position'] == self.tr('Total'):
                    col_freq = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\nFrequency"))
                else:
                    col_freq = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{settings['freq_position']}"))

                col_test_stat = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{text_test_stat}"))
                col_p_value = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{text_p_value}"))
                col_bayes_factor = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{text_bayes_factor}"))
                col_effect_size = self.table.find_col(self.tr(f"[{self.settings['file_to_filter']}]\n{text_effect_size}"))

            col_num_files_found = self.table.find_col('Number of\nFiles Found')

            len_collocate_min = (float('-inf')
                                 if self.settings['len_collocate_min_no_limit'] else self.settings['len_collocate_min'])
            len_collocate_max = (float('inf')
                                 if self.settings['len_collocate_max_no_limit'] else self.settings['len_collocate_max'])

            freq_min = (float('-inf')
                        if self.settings['freq_min_no_limit'] else self.settings['freq_min'])
            freq_max = (float('inf')
                        if self.settings['freq_max_no_limit'] else self.settings['freq_max'])

            test_stat_min = (float('-inf')
                             if self.settings['test_stat_min_no_limit'] else self.settings['test_stat_min'])
            test_stat_max = (float('inf')
                             if self.settings['test_stat_max_no_limit'] else self.settings['test_stat_max'])

            p_value_min = (float('-inf')
                           if self.settings['p_value_min_no_limit'] else self.settings['p_value_min'])
            p_value_max = (float('inf')
                           if self.settings['p_value_max_no_limit'] else self.settings['p_value_max'])

            bayes_factor_min = (float('-inf')
                                if self.settings['bayes_factor_min_no_limit'] else self.settings['bayes_factor_min'])
            bayes_factor_max = (float('inf')
                                if self.settings['bayes_factor_max_no_limit'] else self.settings['bayes_factor_max'])

            effect_size_min = (float('-inf')
                               if self.settings['effect_size_min_no_limit'] else self.settings['effect_size_min'])
            effect_size_max = (float('inf')
                               if self.settings['effect_size_max_no_limit'] else self.settings['effect_size_max'])

            num_files_found_min = (float('-inf')
                                   if self.settings['num_files_found_min_no_limit'] else self.settings['num_files_found_min'])
            num_files_found_max = (float('inf')
                                   if self.settings['num_files_found_max_no_limit'] else self.settings['num_files_found_max'])

            self.table.row_filters = []

            for i in range(self.table.rowCount()):
                if text_test_stat:
                    filter_test_stat = test_stat_min <= self.table.item(i, col_test_stat).val <= test_stat_max
                else:
                    filter_test_stat = True

                if text_bayes_factor:
                    filter_bayes_factor = bayes_factor_min <= self.table.item(i, col_bayes_factor).val <= bayes_factor_max
                else:
                    filter_bayes_factor = True

                if (len_collocate_min   <= len(self.table.item(i, col_collocates).text()) <= len_collocate_max and
                    freq_min            <= self.table.item(i, col_freq).val_raw           <= freq_max and
                    filter_test_stat and
                    p_value_min         <= self.table.item(i, col_p_value).val            <= p_value_max and
                    filter_bayes_factor and
                    effect_size_min     <= self.table.item(i, col_effect_size).val        <= effect_size_max and
                    num_files_found_min <= self.table.item(i, col_num_files_found).val    <= num_files_found_max):
                    self.table.row_filters.append(True)
                else:
                    self.table.row_filters.append(False)

            self.table.filter_table()

        wordless_message.wordless_message_filter_table_done(self.main)

class Wordless_Dialog_Filter_Results_Keywords(Wordless_Dialog_Filter_Results):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.label_len_keyword = QLabel(self.tr('Keyword Length:'), self)
        (self.label_len_keyword_min,
         self.spin_box_len_keyword_min,
         self.checkbox_len_keyword_min_no_limit,
         self.label_len_keyword_max,
         self.spin_box_len_keyword_max,
         self.checkbox_len_keyword_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                            filter_min = 1,
                                                                                            filter_max = 100)

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (self.label_freq_min,
         self.spin_box_freq_min,
         self.checkbox_freq_min_no_limit,
         self.label_freq_max,
         self.spin_box_freq_max,
         self.checkbox_freq_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                     filter_min = 0,
                                                                                     filter_max = 1000000)

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (self.label_test_stat_min,
         self.spin_box_test_stat_min,
         self.checkbox_test_stat_min_no_limit,
         self.label_test_stat_max,
         self.spin_box_test_stat_max,
         self.checkbox_test_stat_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_p_value = QLabel(self.tr('p-value:'), self)
        (self.label_p_value_min,
         self.spin_box_p_value_min,
         self.checkbox_p_value_min_no_limit,
         self.label_p_value_max,
         self.spin_box_p_value_max,
         self.checkbox_p_value_max_no_limit) = wordless_widgets.wordless_widgets_filter_p_value(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (self.label_bayes_factor_min,
         self.spin_box_bayes_factor_min,
         self.checkbox_bayes_factor_min_no_limit,
         self.label_bayes_factor_max,
         self.spin_box_bayes_factor_max,
         self.checkbox_bayes_factor_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (self.label_effect_size_min,
         self.spin_box_effect_size_min,
         self.checkbox_effect_size_min_no_limit,
         self.label_effect_size_max,
         self.spin_box_effect_size_max,
         self.checkbox_effect_size_max_no_limit) = wordless_widgets.wordless_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (self.label_num_files_found_min,
         self.spin_box_num_files_found_min,
         self.checkbox_num_files_found_min_no_limit,
         self.label_num_files_found_max,
         self.spin_box_num_files_found_max,
         self.checkbox_num_files_found_max_no_limit) = wordless_widgets.wordless_widgets_filter(self,
                                                                                                filter_min = 1,
                                                                                                filter_max = 100000)

        self.spin_box_len_keyword_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_keyword_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_value_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_value_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_value_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.itemChanged.connect(self.table_item_changed)

        self.layout_filters.addWidget(self.label_len_keyword, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_keyword_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_keyword_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_value, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_value_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_value_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_value_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_value_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wordless_layout.Wordless_Separator(self, orientation = 'Vertical'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_keyword_min.setValue(settings['len_keyword_min'])
        self.checkbox_len_keyword_min_no_limit.setChecked(settings['len_keyword_min_no_limit'])
        self.spin_box_len_keyword_max.setValue(settings['len_keyword_max'])
        self.checkbox_len_keyword_max_no_limit.setChecked(settings['len_keyword_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_value_min.setValue(settings['p_value_min'])
        self.checkbox_p_value_min_no_limit.setChecked(settings['p_value_min_no_limit'])
        self.spin_box_p_value_max.setValue(settings['p_value_max'])
        self.checkbox_p_value_max_no_limit.setChecked(settings['p_value_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_keyword_min'] = self.spin_box_len_keyword_min.value()
        self.settings['len_keyword_min_no_limit'] = self.checkbox_len_keyword_min_no_limit.isChecked()
        self.settings['len_keyword_max'] = self.spin_box_len_keyword_max.value()
        self.settings['len_keyword_max_no_limit'] = self.checkbox_len_keyword_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_value_min'] = self.spin_box_p_value_min.value()
        self.settings['p_value_min_no_limit'] = self.checkbox_p_value_min_no_limit.isChecked()
        self.settings['p_value_max'] = self.spin_box_p_value_max.value()
        self.settings['p_value_max_no_limit'] = self.checkbox_p_value_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        ref_file = settings['generation_settings']['ref_file']

        text_test_significance = settings['generation_settings']['test_significance']
        text_measure_effect_size = settings['generation_settings']['measure_effect_size']

        (text_test_stat,
         text_p_value,
         text_bayes_factor) = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
        text_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(main.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        if text_bayes_factor:
            if not self.checkbox_bayes_factor_min_no_limit.isChecked():
                self.spin_box_bayes_factor_min.setEnabled(True)
            if not self.checkbox_bayes_factor_max_no_limit.isChecked():
                self.spin_box_bayes_factor_max.setEnabled(True)

            self.checkbox_bayes_factor_min_no_limit.setEnabled(True)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(True)
        else:
            self.spin_box_bayes_factor_min.setEnabled(False)
            self.checkbox_bayes_factor_min_no_limit.setEnabled(False)
            self.spin_box_bayes_factor_max.setEnabled(False)
            self.checkbox_bayes_factor_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{text_effect_size}:')
        
        self.combo_box_file_to_filter.removeItem(self.combo_box_file_to_filter.findText(ref_file))

    @wordless_misc.log_timing
    def filter_results(self):
        if any([self.table.item(0, i) for i in range(self.table.columnCount())]):
            text_test_significance = self.table.settings['keywords']['generation_settings']['test_significance']
            text_measure_effect_size = self.table.settings['keywords']['generation_settings']['measure_effect_size']

            (text_test_stat,
             text_p_value,
             text_bayes_factor) = self.main.settings_global['tests_significance']['keywords'][text_test_significance]['cols']
            text_effect_size = self.main.settings_global['measures_effect_size']['keywords'][text_measure_effect_size]['col']

            col_keywords = self.table.find_col('Keywords')

            if self.settings['file_to_filter'] == self.tr('Total'):
                col_freq = self.table.find_col(self.tr('Total\nFrequency'))
                col_test_stat = self.table.find_col(self.tr(f'Total\n{text_test_stat}'))
                col_p_value = self.table.find_col(self.tr(f'Total\n{text_p_value}'))
                col_bayes_factor = self.table.find_col(self.tr(f'Total\n{text_bayes_factor}'))
                col_effect_size = self.table.find_col(self.tr(f'Total\n{text_effect_size}'))
            else:
                col_freq = self.table.find_col(self.tr(f'[{self.settings["file_to_filter"]}]\nFrequency'))
                col_test_stat = self.table.find_col(self.tr(f'[{self.settings["file_to_filter"]}]\n{text_test_stat}'))
                col_p_value = self.table.find_col(self.tr(f'[{self.settings["file_to_filter"]}]\n{text_p_value}'))
                col_bayes_factor = self.table.find_col(self.tr(f'[{self.settings["file_to_filter"]}]\n{text_bayes_factor}'))
                col_effect_size = self.table.find_col(self.tr(f'[{self.settings["file_to_filter"]}]\n{text_effect_size}'))

            col_num_files_found = self.table.find_col('Number of\nFiles Found')

            len_keyword_min = (float('-inf')
                               if self.settings['len_keyword_min_no_limit'] else self.settings['len_keyword_min'])
            len_keyword_max = (float('inf')
                               if self.settings['len_keyword_max_no_limit'] else self.settings['len_keyword_max'])

            freq_min = (float('-inf')
                        if self.settings['freq_min_no_limit'] else self.settings['freq_min'])
            freq_max = (float('inf')
                        if self.settings['freq_max_no_limit'] else self.settings['freq_max'])

            test_stat_min = (float('-inf')
                             if self.settings['test_stat_min_no_limit'] else self.settings['test_stat_min'])
            test_stat_max = (float('inf')
                             if self.settings['test_stat_max_no_limit'] else self.settings['test_stat_max'])

            p_value_min = (float('-inf')
                           if self.settings['p_value_min_no_limit'] else self.settings['p_value_min'])
            p_value_max = (float('inf')
                           if self.settings['p_value_max_no_limit'] else self.settings['p_value_max'])

            bayes_factor_min = (float('-inf')
                                if self.settings['bayes_factor_min_no_limit'] else self.settings['bayes_factor_min'])
            bayes_factor_max = (float('inf')
                                if self.settings['bayes_factor_max_no_limit'] else self.settings['bayes_factor_max'])

            effect_size_min = (float('-inf')
                               if self.settings['effect_size_min_no_limit'] else self.settings['effect_size_min'])
            effect_size_max = (float('inf')
                               if self.settings['effect_size_max_no_limit'] else self.settings['effect_size_max'])

            num_files_found_min = (float('-inf')
                                   if self.settings['num_files_found_min_no_limit'] else self.settings['num_files_found_min'])
            num_files_found_max = (float('inf')
                                   if self.settings['num_files_found_max_no_limit'] else self.settings['nur_files_found_max'])

            self.table.row_filters = []

            for i in range(self.table.rowCount()):
                if text_test_stat:
                    filter_test_stat = test_stat_min <= self.table.item(i, col_test_stat).val <= test_stat_max
                else:
                    filter_test_stat = True

                if text_bayes_factor:
                    filter_bayes_factor = bayes_factor_min <= self.table.item(i, col_bayes_factor).val <= bayes_factor_max
                else:
                    filter_bayes_factor = True

                if (len_keyword_min     <= len(self.table.item(i, col_keywords).text()) <= len_keyword_max and
                    freq_min            <= self.table.item(i, col_freq).val_raw         <= freq_max and
                    filter_test_stat and
                    p_value_min         <= self.table.item(i, col_p_value).val          <= p_value_max and
                    filter_bayes_factor and
                    effect_size_min     <= self.table.item(i, col_effect_size).val      <= effect_size_max and
                    num_files_found_min <= self.table.item(i, col_num_files_found).val  <= num_files_found_max):
                    self.table.row_filters.append(True)
                else:
                    self.table.row_filters.append(False)

            self.table.filter_table()

        wordless_message.wordless_message_filter_table_done(self.main)

class Wordless_Dialog_Search_Results(Wordless_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, main.tr('Search in Results'))

        self.tab = tab
        self.table = table
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
        
        self.button_reset_settings = wordless_button.Wordless_Button_Reset_Settings(self, self.load_settings)
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

        self.button_close.clicked.connect(self.reject)

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
        self.checkbox_match_whole_word.setChecked(settings['match_whole_word'])
        self.checkbox_use_regex.setChecked(settings['use_regex'])

        self.stacked_wdiget_ignore_tags.checkbox_ignore_tags.setChecked(settings['ignore_tags'])
        self.stacked_wdiget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['ignore_tags_tags'])
        self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['ignore_tags_type'])
        self.stacked_wdiget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['match_tags'])

        self.search_settings_changed()

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
        self.table.setUpdatesEnabled(False)

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
        self.table.setUpdatesEnabled(True)
        self.table.show()

    @ wordless_misc.log_timing
    def find_prev(self):
        indexes_found = self.find_all()

        self.table.hide()
        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

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
        self.table.setUpdatesEnabled(True)
        self.table.show()

    @ wordless_misc.log_timing
    def find_all(self):
        search_terms = set()
        indexes_found = []

        if (self.settings['multi_search_mode'] and self.settings['search_terms'] or
            not self.settings['multi_search_mode'] and self.settings['search_term']):
            results = {}

            self.clear_highlights()

            for col in range(self.table.columnCount()):
                if self.table.cellWidget(0, col):
                    for row in range(self.table.rowCount()):
                        results[(row, col)] = self.table.cellWidget(row, col).text_search
                else:
                    for row in range(self.table.rowCount()):
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

                for row, col in indexes_found:
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

            wordless_message.wordless_message_search_results(self.main, indexes_found)
        else:
            wordless_message_box.wordless_message_box_empty_search_term(self.main)

        return sorted(indexes_found)

    def clear_highlights(self):
        self.table.hide()
        self.table.blockSignals(True)
        self.table.setUpdatesEnabled(False)

        for col in range(self.table.columnCount()):
            if self.table.cellWidget(0, col):
                for row in range(self.table.rowCount()):
                    self.table.cellWidget(row, col).setStyleSheet('border: 0')
            else:
                for row in range(self.table.rowCount()):
                    self.table.item(row, col).setForeground(QBrush(QColor('#292929')))
                    self.table.item(row, col).setBackground(QBrush(QColor('#FFF')))

        self.table.blockSignals(False)
        self.table.setUpdatesEnabled(True)
        self.table.show()

    def load(self):
        self.show()

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
