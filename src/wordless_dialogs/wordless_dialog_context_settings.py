#
# Wordless: Dialogs - Context Settings
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

from wordless_dialogs import wordless_dialog
from wordless_widgets import wordless_button, wordless_layout, wordless_widgets

class Wordless_Dialog_Context_Settings(wordless_dialog.Wordless_Dialog):
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
         self.inclusion_checkbox_match_whole_words,
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
        self.inclusion_checkbox_match_whole_words.stateChanged.connect(self.inclusion_changed)
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
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_whole_words, 6, 0, 1, 4)
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
         self.exclusion_checkbox_match_whole_words,
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
        self.exclusion_checkbox_match_whole_words.stateChanged.connect(self.exclusion_changed)
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
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_whole_words, 6, 0, 1, 4)
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
        self.inclusion_checkbox_match_whole_words.setChecked(settings['inclusion']['match_whole_words'])
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
        self.exclusion_checkbox_match_whole_words.setChecked(settings['exclusion']['match_whole_words'])
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
        self.settings['inclusion']['match_whole_words'] = self.inclusion_checkbox_match_whole_words.isChecked()
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
        self.settings['exclusion']['match_whole_words'] = self.exclusion_checkbox_match_whole_words.isChecked()
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
