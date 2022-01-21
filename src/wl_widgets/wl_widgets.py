# ----------------------------------------------------------------------
# Wordless: Widgets - Widgets
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialogs
from wl_utils import wl_misc
from wl_widgets import wl_boxes, wl_buttons, wl_labels, wl_layouts, wl_lists, wl_widgets

class Wl_Dialog_Context_Settings(wl_dialogs.Wl_Dialog):
    def __init__(self, main, tab):
        super().__init__(main, main.tr('Context Settings'))

        self.tab = tab

        self.settings = self.main.settings_custom[self.tab]['context_settings']

        # Inclusion
        self.inclusion_group_box = QGroupBox(self.tr('Inclusion'), self)

        self.inclusion_group_box.setCheckable(True)

        (
            self.inclusion_label_search_term,
            self.inclusion_checkbox_multi_search_mode,

            self.inclusion_stacked_widget_search_term,
            self.inclusion_line_edit_search_term,
            self.inclusion_list_search_terms,

            self.inclusion_label_separator,

            self.inclusion_checkbox_ignore_case,
            self.inclusion_checkbox_match_inflected_forms,
            self.inclusion_checkbox_match_whole_words,
            self.inclusion_checkbox_use_regex,

            self.inclusion_checkbox_ignore_tags,
            self.inclusion_checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(self, tab = tab)

        self.inclusion_label_context_window = QLabel(self.tr('Context Window:'), self)
        (
            self.inclusion_checkbox_context_window_sync,
            self.inclusion_label_context_window_left,
            self.inclusion_spin_box_context_window_left,
            self.inclusion_label_context_window_right,
            self.inclusion_spin_box_context_window_right
        ) = wl_widgets.wl_widgets_window(self)

        self.inclusion_group_box.toggled.connect(self.inclusion_changed)

        self.inclusion_checkbox_multi_search_mode.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)
        self.inclusion_line_edit_search_term.textChanged.connect(self.inclusion_changed)
        self.inclusion_list_search_terms.itemChanged.connect(self.inclusion_changed)

        self.inclusion_checkbox_ignore_case.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_match_inflected_forms.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_match_whole_words.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_use_regex.stateChanged.connect(self.inclusion_changed)

        self.inclusion_checkbox_ignore_tags.stateChanged.connect(self.inclusion_changed)
        self.inclusion_checkbox_match_tags.stateChanged.connect(self.inclusion_changed)

        self.inclusion_checkbox_context_window_sync.stateChanged.connect(self.inclusion_changed)
        self.inclusion_spin_box_context_window_left.valueChanged.connect(self.inclusion_changed)
        self.inclusion_spin_box_context_window_right.valueChanged.connect(self.inclusion_changed)

        inclusion_layout_multi_search_mode = wl_layouts.Wl_Layout()
        inclusion_layout_multi_search_mode.addWidget(self.inclusion_label_search_term, 0, 0)
        inclusion_layout_multi_search_mode.addWidget(self.inclusion_checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

        self.inclusion_group_box.setLayout(wl_layouts.Wl_Layout())
        self.inclusion_group_box.layout().addLayout(inclusion_layout_multi_search_mode, 0, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_stacked_widget_search_term, 1, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_label_separator, 2, 0, 1, 4)

        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_ignore_case, 3, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_inflected_forms, 4, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_whole_words, 5, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_use_regex, 6, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_ignore_tags, 7, 0, 1, 4)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_match_tags, 8, 0, 1, 4)

        self.inclusion_group_box.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 4)

        self.inclusion_group_box.layout().addWidget(self.inclusion_label_context_window, 10, 0, 1, 3)
        self.inclusion_group_box.layout().addWidget(self.inclusion_checkbox_context_window_sync, 10, 3, Qt.AlignRight)
        self.inclusion_group_box.layout().addWidget(self.inclusion_label_context_window_left, 11, 0)
        self.inclusion_group_box.layout().addWidget(self.inclusion_spin_box_context_window_left, 11, 1)
        self.inclusion_group_box.layout().addWidget(self.inclusion_label_context_window_right, 11, 2)
        self.inclusion_group_box.layout().addWidget(self.inclusion_spin_box_context_window_right, 11, 3)

        self.inclusion_group_box.layout().setColumnStretch(1, 1)
        self.inclusion_group_box.layout().setColumnStretch(3, 1)

        # Exclusion
        self.exclusion_group_box = QGroupBox(self.tr('Exclusion'), self)

        self.exclusion_group_box.setCheckable(True)

        (   self.exclusion_label_search_term,
            self.exclusion_checkbox_multi_search_mode,

            self.exclusion_stacked_widget_search_term,
            self.exclusion_line_edit_search_term,
            self.exclusion_list_search_terms,

            self.exclusion_label_separator,

            self.exclusion_checkbox_ignore_case,
            self.exclusion_checkbox_match_inflected_forms,
            self.exclusion_checkbox_match_whole_words,
            self.exclusion_checkbox_use_regex,

            self.exclusion_checkbox_ignore_tags,
            self.exclusion_checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(self, tab = tab)

        self.exclusion_label_context_window = QLabel(self.tr('Context Window:'), self)
        (
            self.exclusion_checkbox_context_window_sync,
            self.exclusion_label_context_window_left,
            self.exclusion_spin_box_context_window_left,
            self.exclusion_label_context_window_right,
            self.exclusion_spin_box_context_window_right
        ) = wl_widgets.wl_widgets_window(self)

        self.exclusion_group_box.toggled.connect(self.exclusion_changed)

        self.exclusion_checkbox_multi_search_mode.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)
        self.exclusion_line_edit_search_term.textChanged.connect(self.exclusion_changed)
        self.exclusion_list_search_terms.itemChanged.connect(self.exclusion_changed)

        self.exclusion_checkbox_ignore_case.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_match_inflected_forms.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_match_whole_words.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_use_regex.stateChanged.connect(self.exclusion_changed)

        self.exclusion_checkbox_ignore_tags.stateChanged.connect(self.exclusion_changed)
        self.exclusion_checkbox_match_tags.stateChanged.connect(self.exclusion_changed)

        self.exclusion_checkbox_context_window_sync.stateChanged.connect(self.exclusion_changed)
        self.exclusion_spin_box_context_window_left.valueChanged.connect(self.exclusion_changed)
        self.exclusion_spin_box_context_window_right.valueChanged.connect(self.exclusion_changed)

        exclusion_layout_multi_search_mode = wl_layouts.Wl_Layout()
        exclusion_layout_multi_search_mode.addWidget(self.exclusion_label_search_term, 0, 0)
        exclusion_layout_multi_search_mode.addWidget(self.exclusion_checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

        self.exclusion_group_box.setLayout(wl_layouts.Wl_Layout())
        self.exclusion_group_box.layout().addLayout(exclusion_layout_multi_search_mode, 0, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_stacked_widget_search_term, 1, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_label_separator, 2, 0, 1, 4)

        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_ignore_case, 3, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_inflected_forms, 4, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_whole_words, 5, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_use_regex, 6, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_ignore_tags, 7, 0, 1, 4)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_match_tags, 8, 0, 1, 4)

        self.exclusion_group_box.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 4)

        self.exclusion_group_box.layout().addWidget(self.exclusion_label_context_window, 10, 0, 1, 3)
        self.exclusion_group_box.layout().addWidget(self.exclusion_checkbox_context_window_sync, 10, 3, Qt.AlignRight)
        self.exclusion_group_box.layout().addWidget(self.exclusion_label_context_window_left, 11, 0)
        self.exclusion_group_box.layout().addWidget(self.exclusion_spin_box_context_window_left, 11, 1)
        self.exclusion_group_box.layout().addWidget(self.exclusion_label_context_window_right, 11, 2)
        self.exclusion_group_box.layout().addWidget(self.exclusion_spin_box_context_window_right, 11, 3)

        self.exclusion_group_box.layout().setColumnStretch(1, 1)
        self.exclusion_group_box.layout().setColumnStretch(3, 1)

        self.button_restore_default_settings = wl_buttons.Wl_Button_Restore_Default_Settings(self)
        self.button_close = QPushButton(self.tr('Close'), self)

        self.button_close.clicked.connect(self.accept)

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_default_settings, 0, 0)
        layout_buttons.addWidget(self.button_close, 0, 2)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addWidget(self.inclusion_group_box, 0, 0)
        self.layout().addWidget(self.exclusion_group_box, 0, 1)
        self.layout().addLayout(layout_buttons, 1, 0, 1, 2)

        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 1)

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

        self.inclusion_checkbox_ignore_tags.setChecked(settings['inclusion']['ignore_tags'])
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

        self.inclusion_line_edit_search_term.returnPressed.connect(self.button_close.click)

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

        self.exclusion_checkbox_ignore_tags.setChecked(settings['exclusion']['ignore_tags'])
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

        self.exclusion_line_edit_search_term.returnPressed.connect(self.button_close.click)

        self.inclusion_changed()
        self.exclusion_changed()
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

        self.settings['inclusion']['ignore_tags'] = self.inclusion_checkbox_ignore_tags.isChecked()
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

    def exclusion_changed(self):
        self.settings['exclusion']['exclusion'] = self.exclusion_group_box.isChecked()

        self.settings['exclusion']['multi_search_mode'] = self.exclusion_checkbox_multi_search_mode.isChecked()
        self.settings['exclusion']['search_term'] = self.exclusion_line_edit_search_term.text()
        self.settings['exclusion']['search_terms'] = self.exclusion_list_search_terms.get_items()

        self.settings['exclusion']['ignore_case'] = self.exclusion_checkbox_ignore_case.isChecked()
        self.settings['exclusion']['match_inflected_forms'] = self.exclusion_checkbox_match_inflected_forms.isChecked()
        self.settings['exclusion']['match_whole_words'] = self.exclusion_checkbox_match_whole_words.isChecked()
        self.settings['exclusion']['use_regex'] = self.exclusion_checkbox_use_regex.isChecked()

        self.settings['exclusion']['ignore_tags'] = self.exclusion_checkbox_ignore_tags.isChecked()
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

    def multi_search_mode_changed(self):
        if 'size_multi' in self.__dict__:
            if self.settings['inclusion']['multi_search_mode'] or self.settings['exclusion']['multi_search_mode']:
                self.setFixedSize(self.size_multi)
            else:
                self.setFixedSize(self.size_normal)

    def token_settings_changed(self):
        # Check if searching is enabled
        if self.inclusion_group_box.isChecked():
            self.inclusion_checkbox_match_tags.token_settings_changed()
        else:
            self.inclusion_group_box.setChecked(True)

            self.inclusion_checkbox_match_tags.token_settings_changed()

            self.inclusion_group_box.setChecked(False)

        if self.exclusion_group_box.isChecked():
            self.exclusion_checkbox_match_tags.token_settings_changed()
        else:
            self.exclusion_group_box.setChecked(True)

            self.exclusion_checkbox_match_tags.token_settings_changed()

            self.exclusion_group_box.setChecked(False)

    def load(self):
        # Calculate size
        if 'size_multi' not in self.__dict__:
            inclusion_multi_search_mode = self.settings['inclusion']['multi_search_mode']
            exclusion_multi_search_mode = self.settings['exclusion']['multi_search_mode']

            self.inclusion_checkbox_multi_search_mode.setChecked(False)
            self.exclusion_checkbox_multi_search_mode.setChecked(False)

            self.inclusion_group_box.adjustSize()
            self.exclusion_group_box.adjustSize()
            self.adjustSize()
            
            self.size_normal = self.size()

            self.inclusion_checkbox_multi_search_mode.setChecked(True)
            self.exclusion_checkbox_multi_search_mode.setChecked(True)

            self.inclusion_group_box.adjustSize()
            self.exclusion_group_box.adjustSize()
            self.adjustSize()

            self.size_multi = QSize(self.size_normal.width(), self.size().height())

            self.inclusion_checkbox_multi_search_mode.setChecked(inclusion_multi_search_mode)
            self.exclusion_checkbox_multi_search_mode.setChecked(exclusion_multi_search_mode)

        self.exec_()

def wl_widgets_no_limit(parent, double = False):
    def no_limit_changed():
        if checkbox_no_limit.isChecked():
            spin_box_no_limit.setEnabled(False)
        else:
            spin_box_no_limit.setEnabled(True)

    if double:
        spin_box_no_limit = wl_boxes.Wl_Double_Spin_Box(parent)
    else:
        spin_box_no_limit = wl_boxes.Wl_Spin_Box(parent)

    checkbox_no_limit = QCheckBox(parent.tr('No Limit'), parent)

    checkbox_no_limit.stateChanged.connect(no_limit_changed)

    no_limit_changed()

    return spin_box_no_limit, checkbox_no_limit

# Token Settings
def wl_widgets_token_settings(parent):
    def words_changed():
        if checkbox_words.isChecked():
            checkbox_lowercase.setEnabled(True)
            checkbox_uppercase.setEnabled(True)
            checkbox_title_case.setEnabled(True)
        else:
            checkbox_lowercase.setEnabled(False)
            checkbox_uppercase.setEnabled(False)
            checkbox_title_case.setEnabled(False)

    def ignore_tags_changed():
        if checkbox_ignore_tags.isChecked():
            checkbox_use_tags.setEnabled(False)
        else:
            checkbox_use_tags.setEnabled(True)

    def use_tags_changed():
        if checkbox_use_tags.isChecked():
            checkbox_lemmatize_tokens.setEnabled(False)
            checkbox_ignore_tags.setEnabled(False)
        else:
            checkbox_lemmatize_tokens.setEnabled(True)
            checkbox_ignore_tags.setEnabled(True)

    checkbox_words = QCheckBox(parent.tr('Words'), parent)
    checkbox_lowercase = QCheckBox(parent.tr('Lowercase'), parent)
    checkbox_uppercase = QCheckBox(parent.tr('Uppercase'), parent)
    checkbox_title_case = QCheckBox(parent.tr('Title Case'), parent)
    checkbox_nums = QCheckBox(parent.tr('Numerals'), parent)
    checkbox_puncs = QCheckBox(parent.tr('Punctuations'), parent)

    checkbox_treat_as_lowercase = QCheckBox(parent.tr('Treat as all lowercase'), parent)
    checkbox_lemmatize_tokens = QCheckBox(parent.tr('Lemmatize all tokens'), parent)
    checkbox_filter_stop_words = QCheckBox(parent.tr('Filter stop words'), parent)

    checkbox_ignore_tags = QCheckBox(parent.tr('Ignore tags'), parent)
    checkbox_use_tags = QCheckBox(parent.tr('Use tags only'), parent)

    checkbox_words.stateChanged.connect(words_changed)
    checkbox_ignore_tags.stateChanged.connect(ignore_tags_changed)
    checkbox_use_tags.stateChanged.connect(use_tags_changed)

    words_changed()
    ignore_tags_changed()
    use_tags_changed()

    return (
        checkbox_words,
        checkbox_lowercase,
        checkbox_uppercase,
        checkbox_title_case,
        checkbox_nums,
        checkbox_puncs,

        checkbox_treat_as_lowercase,
        checkbox_lemmatize_tokens,
        checkbox_filter_stop_words,

        checkbox_ignore_tags,
        checkbox_use_tags
    )

def wl_widgets_token_settings_concordancer(parent):
    def ignore_tags_changed():
        if checkbox_ignore_tags.isChecked():
            checkbox_use_tags.setEnabled(False)
        else:
            checkbox_use_tags.setEnabled(True)

    def use_tags_changed():
        if checkbox_use_tags.isChecked():
            checkbox_ignore_tags.setEnabled(False)
        else:
            checkbox_ignore_tags.setEnabled(True)

    checkbox_puncs = QCheckBox(parent.tr('Punctuations'), parent)

    checkbox_ignore_tags = QCheckBox(parent.tr('Ignore tags'), parent)
    checkbox_use_tags = QCheckBox(parent.tr('Use tags only'), parent)

    checkbox_ignore_tags.stateChanged.connect(ignore_tags_changed)
    checkbox_use_tags.stateChanged.connect(use_tags_changed)

    ignore_tags_changed()
    use_tags_changed()

    return (
        checkbox_puncs,

        checkbox_ignore_tags,
        checkbox_use_tags
    )

# Search Settings
def wl_widgets_search_settings(parent, tab):
    def multi_search_mode_changed():
        if checkbox_multi_search_mode.isChecked():
            label_search_term.setText(parent.tr('Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.count() == 0:
                list_search_terms.load_items([line_edit_search_term.text()])

            stacked_widget_search_term.setCurrentIndex(1)
        else:
            label_search_term.setText(parent.tr('Search Term:'))

            stacked_widget_search_term.setCurrentIndex(0)

    def token_settings_changed():
        token_settings = main.settings_custom[tab]['token_settings']

        checkbox_ignore_tags.blockSignals(True)
        checkbox_match_tags.blockSignals(True)

        if token_settings['ignore_tags']:
            checkbox_ignore_tags.setEnabled(False)
            checkbox_match_tags.setEnabled(False)
        else:
            checkbox_ignore_tags.setEnabled(True)
            checkbox_match_tags.setEnabled(True)

        if token_settings['use_tags']:
            checkbox_ignore_tags.setEnabled(False)
            checkbox_match_tags.setEnabled(False)
        else:
            checkbox_ignore_tags.setEnabled(True)
            checkbox_match_tags.setEnabled(True)

        checkbox_ignore_tags.blockSignals(False)
        checkbox_match_tags.blockSignals(False)

    def ignore_tags_changed():
        if checkbox_ignore_tags.isChecked():
            checkbox_match_tags.setEnabled(False)
            checkbox_match_tags.setChecked(False)
        else:
            checkbox_match_tags.setEnabled(True)

    def match_tags_changed():
        if checkbox_match_tags.isChecked():
            checkbox_match_inflected_forms.setEnabled(False)
            checkbox_ignore_tags.setEnabled(False)
            checkbox_ignore_tags.setChecked(False)
        else:
            checkbox_match_inflected_forms.setEnabled(True)
            checkbox_ignore_tags.setEnabled(True)

    main = wl_misc.find_wl_main(parent)

    label_search_term = QLabel(parent.tr('Search Term:'), parent)
    checkbox_multi_search_mode = QCheckBox(parent.tr('Multi-search Mode'), parent)
    line_edit_search_term = QLineEdit(parent)
    list_search_terms = wl_lists.Wl_List_Search_Terms(parent)
    label_separator = wl_labels.Wl_Label_Hint(parent.tr('* Use space to separate multiple tokens'), parent)

    checkbox_ignore_case = QCheckBox(parent.tr('Ignore case'), parent)
    checkbox_match_inflected_forms = QCheckBox(parent.tr('Match all inflected forms'), parent)
    checkbox_match_whole_words = QCheckBox(parent.tr('Match whole words only'), parent)
    checkbox_use_regex = QCheckBox(parent.tr('Use regular expression'), parent)

    checkbox_ignore_tags = QCheckBox(parent.tr('Ignore tags'), parent)
    checkbox_match_tags = QCheckBox(parent.tr('Match tags only'), parent)

    wrapper_search_terms = QWidget(parent)

    wrapper_search_terms.setLayout(wl_layouts.Wl_Layout())
    wrapper_search_terms.layout().addWidget(list_search_terms, 0, 0, 6, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_add, 0, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_insert, 1, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_remove, 2, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_clear, 3, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_import, 4, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_export, 5, 1)

    wrapper_search_terms.layout().setContentsMargins(0, 0, 0, 0)

    stacked_widget_search_term = wl_layouts.Wl_Stacked_Widget(parent)
    stacked_widget_search_term.addWidget(line_edit_search_term)
    stacked_widget_search_term.addWidget(wrapper_search_terms)

    checkbox_match_tags.token_settings_changed = token_settings_changed

    checkbox_multi_search_mode.stateChanged.connect(multi_search_mode_changed)
    checkbox_ignore_tags.stateChanged.connect(ignore_tags_changed)
    checkbox_match_tags.stateChanged.connect(match_tags_changed)

    multi_search_mode_changed()
    token_settings_changed()
    ignore_tags_changed()
    match_tags_changed()

    return (
        label_search_term,
        checkbox_multi_search_mode,

        stacked_widget_search_term,
        line_edit_search_term,
        list_search_terms,

        label_separator,

        checkbox_ignore_case,
        checkbox_match_inflected_forms,
        checkbox_match_whole_words,
        checkbox_use_regex,

        checkbox_ignore_tags,
        checkbox_match_tags
    )

def wl_widgets_context_settings(parent, tab):
    main = wl_misc.find_wl_main(parent)

    label_context_settings = QLabel(parent.tr('Context Settings:'), parent)
    button_context_settings = QPushButton(parent.tr('Settings...'), parent)

    dialog_context_settings = Wl_Dialog_Context_Settings(main, tab = tab)
    main.__dict__[f'wl_context_settings_{tab}'] = dialog_context_settings

    button_context_settings.clicked.connect(lambda: main.__dict__[f'wl_context_settings_{tab}'].load())

    return label_context_settings, button_context_settings

# Generation Settings
def wl_widgets_size(parent, size_min = 1, size_max = 100):
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
    spin_box_size_min = wl_boxes.Wl_Spin_Box(parent)
    label_size_max = QLabel(parent.tr('To'), parent)
    spin_box_size_max = wl_boxes.Wl_Spin_Box(parent)

    spin_box_size_min.setRange(size_min, size_max)
    spin_box_size_max.setRange(size_min, size_max)

    checkbox_size_sync.stateChanged.connect(size_sync_changed)
    spin_box_size_min.valueChanged.connect(size_min_changed)
    spin_box_size_max.valueChanged.connect(size_max_changed)

    size_sync_changed()
    size_min_changed()
    size_max_changed()

    return checkbox_size_sync, label_size_min, spin_box_size_min, label_size_max, spin_box_size_max

def wl_widgets_window(parent):
    def window_sync_changed():
        if checkbox_window_sync.isChecked():
            spin_box_window_left.setPrefix(spin_box_window_right.prefix())
            spin_box_window_left.setValue(spin_box_window_right.value())

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
    spin_box_window_left = wl_boxes.Wl_Spin_Box_Window(parent)
    label_window_right = QLabel(parent.tr('To'), parent)
    spin_box_window_right = wl_boxes.Wl_Spin_Box_Window(parent)

    spin_box_window_left.setRange(-100, 100)
    spin_box_window_right.setRange(-100, 100)

    checkbox_window_sync.stateChanged.connect(window_sync_changed)
    spin_box_window_left.valueChanged.connect(window_left_changed)
    spin_box_window_right.valueChanged.connect(window_right_changed)

    window_sync_changed()
    window_left_changed()
    window_right_changed()

    return checkbox_window_sync, label_window_left, spin_box_window_left, label_window_right, spin_box_window_right

def wl_widgets_measure_dispersion(parent):
    main = wl_misc.find_wl_main(parent)

    label_measure_dispersion = QLabel(parent.tr('Measure of Dispersion:'), parent)
    combo_box_measure_dispersion = wl_boxes.Wl_Combo_Box(parent)

    combo_box_measure_dispersion.addItems(list(main.settings_global['measures_dispersion'].keys()))

    return (label_measure_dispersion,
            combo_box_measure_dispersion)

def wl_widgets_measure_adjusted_freq(parent):
    main = wl_misc.find_wl_main(parent)

    label_measure_adjusted_freq = QLabel(parent.tr('Measure of Adjusted Frequency:'), parent)
    combo_box_measure_adjusted_freq = wl_boxes.Wl_Combo_Box(parent)

    combo_box_measure_adjusted_freq.addItems(list(main.settings_global['measures_adjusted_freq'].keys()))

    return (label_measure_adjusted_freq,
            combo_box_measure_adjusted_freq)

def wl_widgets_test_significance(parent):
    label_test_significance = QLabel(parent.tr('Test of Statistical Significance:'), parent)
    combo_box_test_significance = wl_boxes.Wl_Combo_Box(parent)

    return (label_test_significance,
            combo_box_test_significance)

def wl_widgets_measure_effect_size(parent):
    label_measure_effect_size = QLabel(parent.tr('Measure of Effect Size:'), parent)
    combo_box_measure_effect_size = wl_boxes.Wl_Combo_Box(parent)

    return (label_measure_effect_size,
            combo_box_measure_effect_size)

def wl_widgets_settings_measures(parent, node):
    main = wl_misc.find_wl_main(parent)

    label_settings_measures = QLabel(parent.tr('Advanced Settings:'), parent)
    button_settings_measures = QPushButton(parent.tr('Settings...'), parent)

    button_settings_measures.clicked.connect(lambda: main.wl_settings.load(node = node))

    return label_settings_measures, button_settings_measures

# Table Settings
def wl_widgets_table_settings(parent, tables):
    def show_pct_changed():
        for table in tables:
            table.show_pct = checkbox_show_pct.isChecked()

            if any([table.item(0, i) for i in range(table.columnCount())]):
                table.toggle_pct()

    def show_cumulative_changed():
        for table in tables:
            table.show_cumulative = checkbox_show_cumulative.isChecked()

            if any([table.item(0, i) for i in range(table.columnCount())]):
                table.toggle_cumulative()

    def show_breakdown_changed():
        for table in tables:
            table.show_breakdown = checkbox_show_breakdown.isChecked()

            table.toggle_breakdown()

    checkbox_show_pct = QCheckBox(parent.tr('Show percentage data'), parent)
    checkbox_show_cumulative = QCheckBox(parent.tr('Show cumulative data'), parent)
    checkbox_show_breakdown = QCheckBox(parent.tr('Show breakdown by file'), parent)

    checkbox_show_pct.stateChanged.connect(show_pct_changed)
    checkbox_show_cumulative.stateChanged.connect(show_cumulative_changed)
    checkbox_show_breakdown.stateChanged.connect(show_breakdown_changed)

    show_pct_changed()
    show_cumulative_changed()
    show_breakdown_changed()

    return checkbox_show_pct, checkbox_show_cumulative, checkbox_show_breakdown

# Figure Settings
class Wl_Combo_Box_File_Figure_Settings(wl_boxes.Wl_Combo_Box_File):
    def wl_files_changed(self):
        if self.count() == 1:
            file_old = ''
        else:
            file_old = self.currentText()

        self.clear()

        for file in self.main.wl_files.get_selected_files():
            self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        if file_old and self.findText(file_old) > -1:
            self.setCurrentText(file_old)

def wl_widgets_fig_settings(parent, collocation = False):
    def graph_type_changed():
        if combo_box_graph_type.currentText() == parent.tr('Line Chart'):
            combo_box_sort_by_file.setEnabled(True)

            use_data_changed()
        else:
            combo_box_sort_by_file.setEnabled(True)
            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)

    def use_data_changed():
        if combo_box_graph_type.currentText() == parent.tr('Line Chart'):
            if combo_box_use_data.currentText() == parent.tr('Frequency'):
                checkbox_use_pct.setEnabled(True)
                checkbox_use_cumulative.setEnabled(True)
            else:
                checkbox_use_pct.setEnabled(False)
                checkbox_use_cumulative.setEnabled(False)

    main = wl_misc.find_wl_main(parent)

    label_graph_type = QLabel(parent.tr('Graph Type:'), parent)
    combo_box_graph_type = wl_boxes.Wl_Combo_Box(parent)
    label_sort_by_file = QLabel(parent.tr('Sort by File:'), parent)
    combo_box_sort_by_file = Wl_Combo_Box_File_Figure_Settings(parent)
    label_use_data = QLabel(parent.tr('Use Data:'), parent)
    combo_box_use_data = wl_boxes.Wl_Combo_Box(parent)
    checkbox_use_pct = QCheckBox(parent.tr('Use percentage data'), parent)
    checkbox_use_cumulative = QCheckBox(parent.tr('Use cumulative data'), parent)

    combo_box_graph_type.addItems([parent.tr('Line Chart'),
                                   parent.tr('Word Cloud')])

    # Collocation & Colligation
    if collocation:
        combo_box_graph_type.addItem(parent.tr('Network Graph'))

    combo_box_graph_type.currentTextChanged.connect(graph_type_changed)
    combo_box_use_data.currentTextChanged.connect(use_data_changed)

    graph_type_changed()
    use_data_changed()

    return (
        label_graph_type, combo_box_graph_type,
        label_sort_by_file, combo_box_sort_by_file,
        label_use_data, combo_box_use_data,
        checkbox_use_pct, checkbox_use_cumulative
    )

# Filter Settings
def wl_widgets_filter(parent, filter_min, filter_max):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    label_min = QLabel(parent.tr('From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wl_widgets_no_limit(parent)

    label_max = QLabel(parent.tr('To'), parent)
    (spin_box_max,
     checkbox_max_no_limit) = wl_widgets_no_limit(parent)

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    min_changed()
    max_changed()

    return (label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit)

def wl_widgets_filter_measures(parent, filter_min = -10000, filter_max = 10000):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    def precision_changed():
        precision = main.settings_custom['data']['precision_decimal']

        spin_box_min.setDecimals(precision)
        spin_box_max.setDecimals(precision)

        spin_box_min.setSingleStep(0.1 ** precision)
        spin_box_max.setSingleStep(0.1 ** precision)

    main = wl_misc.find_wl_main(parent)

    label_min = QLabel(parent.tr('From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wl_widgets_no_limit(parent, double = True)

    label_max = QLabel(parent.tr('To'), parent)
    (spin_box_max,
     checkbox_max_no_limit) = wl_widgets_no_limit(parent, double = True)

    spin_box_min.setRange(filter_min, filter_max)
    spin_box_max.setRange(filter_min, filter_max)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    main.wl_settings.wl_settings_changed.connect(precision_changed)

    min_changed()
    max_changed()
    
    precision_changed()

    return (
        label_min, spin_box_min, checkbox_min_no_limit,
        label_max, spin_box_max, checkbox_max_no_limit
    )

def wl_widgets_filter_p_value(parent):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    def precision_changed():
        precision = main.settings_custom['data']['precision_p_value']

        spin_box_min.setDecimals(precision)
        spin_box_max.setDecimals(precision)

        spin_box_min.setSingleStep(0.1 ** precision)
        spin_box_max.setSingleStep(0.1 ** precision)

    main = wl_misc.find_wl_main(parent)

    label_min = QLabel(parent.tr('From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wl_widgets_no_limit(parent, double = True)

    label_max = QLabel(parent.tr('To'), parent)
    (spin_box_max,
     checkbox_max_no_limit) = wl_widgets_no_limit(parent, double = True)

    spin_box_min.setRange(0, 1)
    spin_box_max.setRange(0, 1)

    spin_box_min.valueChanged.connect(min_changed)
    spin_box_max.valueChanged.connect(max_changed)

    main.wl_settings.wl_settings_changed.connect(precision_changed)

    min_changed()
    max_changed()

    precision_changed()

    return (
        label_min, spin_box_min, checkbox_min_no_limit,
        label_max, spin_box_max, checkbox_max_no_limit
    )

def wl_widgets_filter_results(parent, table):
    def table_item_changed():
        if combo_box_filter_file.count() == 1:
            file_old = ''
        else:
            file_old = combo_box_filter_file.currentText()

        combo_box_filter_file.clear()

        for file in table.settings['files']['files_open']:
            if file['selected']:
                combo_box_filter_file.addItem(file['name'])

        combo_box_filter_file.addItem(parent.tr('Total'))

        if combo_box_filter_file.findText(file_old) > -1:
            combo_box_filter_file.setCurrentText(file_old)

    label_filter_file = QLabel(parent.tr('Filter File:'), parent)
    combo_box_filter_file = wl_boxes.Wl_Combo_Box(parent)
    button_filter_results = QPushButton(parent.tr('Filter Results in Table'), parent)

    button_filter_results.clicked.connect(lambda: table.update_filters())

    table.itemChanged.connect(table_item_changed)

    table_item_changed()

    return (label_filter_file, combo_box_filter_file,
            button_filter_results)

# Settings -> Measures
def wl_widgets_number_sections(parent):
    label_divide = QLabel(parent.tr('Divide each text into'), parent)
    spin_box_number_sections = wl_boxes.Wl_Spin_Box(parent)
    label_sections = QLabel(parent.tr('sections'), parent)

    spin_box_number_sections.setRange(2, 1000)

    return label_divide, spin_box_number_sections, label_sections

def wl_widgets_use_data_freq(parent):
    label_use_data = QLabel(parent.tr('Use Data:'), parent)
    combo_box_use_data = wl_boxes.Wl_Combo_Box(parent)

    combo_box_use_data.addItems([
        parent.tr('Absolute Frequency'),
        parent.tr('Relative Frequency')
    ])

    return label_use_data, combo_box_use_data

def wl_widgets_direction(parent):
    label_direction = QLabel(parent.tr('Direction:'), parent)
    combo_box_direction = wl_boxes.Wl_Combo_Box(parent)

    combo_box_direction.addItems([
        parent.tr('Two-tailed'),
        parent.tr('Left-tailed'),
        parent.tr('Right-tailed')
    ])

    return label_direction, combo_box_direction

def wl_widgets_direction_2(parent):
    label_direction = QLabel(parent.tr('Direction:'), parent)
    combo_box_direction = wl_boxes.Wl_Combo_Box(parent)

    combo_box_direction.addItems([
        parent.tr('Two-tailed'),
        parent.tr('One-tailed')
    ])

    return label_direction, combo_box_direction

# Settings -> Figures
def wl_widgets_pick_color(parent):
    def get_color():
        return re.search(r'#[0-9a-zA-Z]{6}', label_pick_color.text()).group()

    def set_color(color):
        label_pick_color.setText(f'<span style="margin-right: 3px; background-color: {color}; color: {color}">00</span> <span>{color.upper()}</span>')

    def pick_color():
        color_picked = QColorDialog.getColor(QColor(get_color()), parent, parent.tr('Pick Color'))

        if color_picked.isValid():
            label_pick_color.set_color(color_picked.name())

    label_pick_color = wl_labels.Wl_Label_Html('', parent)
    button_pick_color = QPushButton(parent.tr('Pick Color...'), parent)

    label_pick_color.get_color = get_color
    label_pick_color.set_color = set_color

    button_pick_color.clicked.connect(pick_color)

    return label_pick_color, button_pick_color
