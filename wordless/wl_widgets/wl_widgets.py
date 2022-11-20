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

from PyQt5.QtCore import QCoreApplication, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QCheckBox, QColorDialog, QGroupBox, QLabel, QLineEdit,
    QPushButton, QWidget
)

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_utils import wl_misc
from wordless.wl_widgets import wl_boxes, wl_labels, wl_layouts, wl_lists

_tr = QCoreApplication.translate

class Wl_Dialog_Context_Settings(wl_dialogs.Wl_Dialog_Settings):
    def __init__(self, main, tab):
        super().__init__(main, title = _tr('Wl_Dialog_Context_Settings', 'Context Settings'))

        self.tab = tab
        self.settings_custom = self.main.settings_custom[self.tab]['context_settings']
        self.settings_default = self.main.settings_custom[self.tab]['context_settings']

        # Inclusion
        self.incl_group_box = QGroupBox(self.tr('Inclusion'), self)

        self.incl_group_box.setCheckable(True)

        (
            self.incl_label_search_term,
            self.incl_checkbox_multi_search_mode,

            self.incl_stacked_widget_search_term,
            self.incl_line_edit_search_term,
            self.incl_list_search_terms,
            self.incl_label_delimiter,

            self.incl_checkbox_match_case,
            self.incl_checkbox_match_whole_words,
            self.incl_checkbox_match_inflected_forms,
            self.incl_checkbox_use_regex,
            self.incl_checkbox_match_without_tags,
            self.incl_checkbox_match_tags
        ) = wl_widgets_search_settings(self, tab = tab)

        self.incl_label_context_window = QLabel(self.tr('Context Window:'), self)
        (
            self.incl_checkbox_context_window_sync,
            self.incl_label_context_window_left,
            self.incl_spin_box_context_window_left,
            self.incl_label_context_window_right,
            self.incl_spin_box_context_window_right
        ) = wl_widgets_window(self)

        self.incl_checkbox_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)

        incl_layout_multi_search_mode = wl_layouts.Wl_Layout()
        incl_layout_multi_search_mode.addWidget(self.incl_label_search_term, 0, 0)
        incl_layout_multi_search_mode.addWidget(self.incl_checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

        self.incl_group_box.setLayout(wl_layouts.Wl_Layout())
        self.incl_group_box.layout().addLayout(incl_layout_multi_search_mode, 0, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_stacked_widget_search_term, 1, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_label_delimiter, 2, 0, 1, 4)

        self.incl_group_box.layout().addWidget(self.incl_checkbox_match_case, 3, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_checkbox_match_whole_words, 4, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_checkbox_match_inflected_forms, 5, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_checkbox_use_regex, 6, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_checkbox_match_without_tags, 7, 0, 1, 4)
        self.incl_group_box.layout().addWidget(self.incl_checkbox_match_tags, 8, 0, 1, 4)

        self.incl_group_box.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 4)

        self.incl_group_box.layout().addWidget(self.incl_label_context_window, 10, 0, 1, 3)
        self.incl_group_box.layout().addWidget(self.incl_checkbox_context_window_sync, 10, 3, Qt.AlignRight)
        self.incl_group_box.layout().addWidget(self.incl_label_context_window_left, 11, 0)
        self.incl_group_box.layout().addWidget(self.incl_spin_box_context_window_left, 11, 1)
        self.incl_group_box.layout().addWidget(self.incl_label_context_window_right, 11, 2)
        self.incl_group_box.layout().addWidget(self.incl_spin_box_context_window_right, 11, 3)

        self.incl_group_box.layout().setColumnStretch(1, 1)
        self.incl_group_box.layout().setColumnStretch(3, 1)

        # Exclusion
        self.excl_group_box = QGroupBox(self.tr('Exclusion'), self)

        self.excl_group_box.setCheckable(True)

        (
            self.excl_label_search_term,
            self.excl_checkbox_multi_search_mode,

            self.excl_stacked_widget_search_term,
            self.excl_line_edit_search_term,
            self.excl_list_search_terms,
            self.excl_label_delimiter,

            self.excl_checkbox_match_case,
            self.excl_checkbox_match_whole_words,
            self.excl_checkbox_match_inflected_forms,
            self.excl_checkbox_use_regex,
            self.excl_checkbox_match_without_tags,
            self.excl_checkbox_match_tags
        ) = wl_widgets_search_settings(self, tab = tab)

        self.excl_label_context_window = QLabel(self.tr('Context Window:'), self)
        (
            self.excl_checkbox_context_window_sync,
            self.excl_label_context_window_left,
            self.excl_spin_box_context_window_left,
            self.excl_label_context_window_right,
            self.excl_spin_box_context_window_right
        ) = wl_widgets_window(self)

        self.excl_checkbox_multi_search_mode.stateChanged.connect(self.multi_search_mode_changed)

        excl_layout_multi_search_mode = wl_layouts.Wl_Layout()
        excl_layout_multi_search_mode.addWidget(self.excl_label_search_term, 0, 0)
        excl_layout_multi_search_mode.addWidget(self.excl_checkbox_multi_search_mode, 0, 1, Qt.AlignRight)

        self.excl_group_box.setLayout(wl_layouts.Wl_Layout())
        self.excl_group_box.layout().addLayout(excl_layout_multi_search_mode, 0, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_stacked_widget_search_term, 1, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_label_delimiter, 2, 0, 1, 4)

        self.excl_group_box.layout().addWidget(self.excl_checkbox_match_case, 3, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_checkbox_match_whole_words, 4, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_checkbox_match_inflected_forms, 5, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_checkbox_use_regex, 6, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_checkbox_match_without_tags, 7, 0, 1, 4)
        self.excl_group_box.layout().addWidget(self.excl_checkbox_match_tags, 8, 0, 1, 4)

        self.excl_group_box.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 4)

        self.excl_group_box.layout().addWidget(self.excl_label_context_window, 10, 0, 1, 3)
        self.excl_group_box.layout().addWidget(self.excl_checkbox_context_window_sync, 10, 3, Qt.AlignRight)
        self.excl_group_box.layout().addWidget(self.excl_label_context_window_left, 11, 0)
        self.excl_group_box.layout().addWidget(self.excl_spin_box_context_window_left, 11, 1)
        self.excl_group_box.layout().addWidget(self.excl_label_context_window_right, 11, 2)
        self.excl_group_box.layout().addWidget(self.excl_spin_box_context_window_right, 11, 3)

        self.excl_group_box.layout().setColumnStretch(1, 1)
        self.excl_group_box.layout().setColumnStretch(3, 1)

        self.incl_line_edit_search_term.returnPressed.connect(self.button_save.click)
        self.excl_line_edit_search_term.returnPressed.connect(self.button_save.click)

        self.wrapper_settings.layout().addWidget(self.incl_group_box, 0, 0)
        self.wrapper_settings.layout().addWidget(self.excl_group_box, 0, 1)

        self.wrapper_settings.layout().setColumnStretch(0, 1)
        self.wrapper_settings.layout().setColumnStretch(1, 1)

    def multi_search_mode_changed(self):
        if 'size_multi' in self.__dict__:
            if self.incl_checkbox_multi_search_mode.isChecked() or self.excl_checkbox_multi_search_mode.isChecked():
                self.setFixedSize(self.size_multi)
            else:
                self.setFixedSize(self.size_normal)

    def token_settings_changed(self):
        # Check if searching is enabled
        if self.incl_group_box.isChecked():
            self.incl_checkbox_match_tags.token_settings_changed()
        else:
            self.incl_group_box.setChecked(True)

            self.incl_checkbox_match_tags.token_settings_changed()

            self.incl_group_box.setChecked(False)

        if self.excl_group_box.isChecked():
            self.excl_checkbox_match_tags.token_settings_changed()
        else:
            self.excl_group_box.setChecked(True)

            self.excl_checkbox_match_tags.token_settings_changed()

            self.excl_group_box.setChecked(False)

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.settings_default)
        else:
            settings = copy.deepcopy(self.settings_custom)

        # Inclusion
        self.incl_group_box.setChecked(settings['incl']['incl'])

        self.incl_checkbox_multi_search_mode.setChecked(settings['incl']['multi_search_mode'])

        if not defaults:
            self.incl_line_edit_search_term.setText(settings['incl']['search_term'])
            self.incl_list_search_terms.load_items(settings['incl']['search_terms'])

        self.incl_checkbox_match_case.setChecked(settings['incl']['match_case'])
        self.incl_checkbox_match_whole_words.setChecked(settings['incl']['match_whole_words'])
        self.incl_checkbox_match_inflected_forms.setChecked(settings['incl']['match_inflected_forms'])
        self.incl_checkbox_use_regex.setChecked(settings['incl']['use_regex'])
        self.incl_checkbox_match_without_tags.setChecked(settings['incl']['match_without_tags'])
        self.incl_checkbox_match_tags.setChecked(settings['incl']['match_tags'])

        self.incl_checkbox_context_window_sync.setChecked(settings['incl']['context_window_sync'])

        if settings['incl']['context_window_left'] < 0:
            self.incl_spin_box_context_window_left.setPrefix(self.tr('L'))
            self.incl_spin_box_context_window_left.setValue(-settings['incl']['context_window_left'])
        else:
            self.incl_spin_box_context_window_left.setPrefix(self.tr('R'))
            self.incl_spin_box_context_window_left.setValue(settings['incl']['context_window_left'])

        if settings['incl']['context_window_right'] < 0:
            self.incl_spin_box_context_window_right.setPrefix(self.tr('L'))
            self.incl_spin_box_context_window_right.setValue(-settings['incl']['context_window_right'])
        else:
            self.incl_spin_box_context_window_right.setPrefix(self.tr('R'))
            self.incl_spin_box_context_window_right.setValue(settings['incl']['context_window_right'])

        # Exclusion
        self.excl_group_box.setChecked(settings['excl']['excl'])

        self.excl_checkbox_multi_search_mode.setChecked(settings['excl']['multi_search_mode'])

        if not defaults:
            self.excl_line_edit_search_term.setText(settings['excl']['search_term'])
            self.excl_list_search_terms.load_items(settings['excl']['search_terms'])

        self.excl_checkbox_match_case.setChecked(settings['excl']['match_case'])
        self.excl_checkbox_match_whole_words.setChecked(settings['excl']['match_whole_words'])
        self.excl_checkbox_match_inflected_forms.setChecked(settings['excl']['match_inflected_forms'])
        self.excl_checkbox_use_regex.setChecked(settings['excl']['use_regex'])
        self.excl_checkbox_match_without_tags.setChecked(settings['excl']['match_without_tags'])
        self.excl_checkbox_match_tags.setChecked(settings['excl']['match_tags'])

        self.excl_checkbox_context_window_sync.setChecked(settings['excl']['context_window_sync'])

        if settings['excl']['context_window_left'] < 0:
            self.excl_spin_box_context_window_left.setPrefix(self.tr('L'))
            self.excl_spin_box_context_window_left.setValue(-settings['excl']['context_window_left'])
        else:
            self.excl_spin_box_context_window_left.setPrefix(self.tr('R'))
            self.excl_spin_box_context_window_left.setValue(settings['excl']['context_window_left'])

        if settings['excl']['context_window_right'] < 0:
            self.excl_spin_box_context_window_right.setPrefix(self.tr('L'))
            self.excl_spin_box_context_window_right.setValue(-settings['excl']['context_window_right'])
        else:
            self.excl_spin_box_context_window_right.setPrefix(self.tr('R'))
            self.excl_spin_box_context_window_right.setValue(settings['excl']['context_window_right'])

        self.token_settings_changed()

    def save_settings(self):
        # Inclusion
        self.settings_custom['incl']['incl'] = self.incl_group_box.isChecked()

        self.settings_custom['incl']['multi_search_mode'] = self.incl_checkbox_multi_search_mode.isChecked()
        self.settings_custom['incl']['search_term'] = self.incl_line_edit_search_term.text()
        self.settings_custom['incl']['search_terms'] = self.incl_list_search_terms.model().stringList()

        self.settings_custom['incl']['match_case'] = self.incl_checkbox_match_case.isChecked()
        self.settings_custom['incl']['match_whole_words'] = self.incl_checkbox_match_whole_words.isChecked()
        self.settings_custom['incl']['match_inflected_forms'] = self.incl_checkbox_match_inflected_forms.isChecked()
        self.settings_custom['incl']['use_regex'] = self.incl_checkbox_use_regex.isChecked()
        self.settings_custom['incl']['match_without_tags'] = self.incl_checkbox_match_without_tags.isChecked()
        self.settings_custom['incl']['match_tags'] = self.incl_checkbox_match_tags.isChecked()

        self.settings_custom['incl']['context_window_sync'] = self.incl_checkbox_context_window_sync.isChecked()

        if self.incl_spin_box_context_window_left.prefix() == self.tr('L'):
            self.settings_custom['incl']['context_window_left'] = -self.incl_spin_box_context_window_left.value()
        else:
            self.settings_custom['incl']['context_window_left'] = self.incl_spin_box_context_window_left.value()

        if self.incl_spin_box_context_window_right.prefix() == self.tr('L'):
            self.settings_custom['incl']['context_window_right'] = -self.incl_spin_box_context_window_right.value()
        else:
            self.settings_custom['incl']['context_window_right'] = self.incl_spin_box_context_window_right.value()

        # Exclusion
        self.settings_custom['excl']['excl'] = self.excl_group_box.isChecked()

        self.settings_custom['excl']['multi_search_mode'] = self.excl_checkbox_multi_search_mode.isChecked()
        self.settings_custom['excl']['search_term'] = self.excl_line_edit_search_term.text()
        self.settings_custom['excl']['search_terms'] = self.excl_list_search_terms.model().stringList()

        self.settings_custom['excl']['match_case'] = self.excl_checkbox_match_case.isChecked()
        self.settings_custom['excl']['match_whole_words'] = self.excl_checkbox_match_whole_words.isChecked()
        self.settings_custom['excl']['match_inflected_forms'] = self.excl_checkbox_match_inflected_forms.isChecked()
        self.settings_custom['excl']['use_regex'] = self.excl_checkbox_use_regex.isChecked()
        self.settings_custom['excl']['match_without_tags'] = self.excl_checkbox_match_without_tags.isChecked()
        self.settings_custom['excl']['match_tags'] = self.excl_checkbox_match_tags.isChecked()

        self.settings_custom['excl']['context_window_sync'] = self.excl_checkbox_context_window_sync.isChecked()

        if self.excl_spin_box_context_window_left.prefix() == self.tr('L'):
            self.settings_custom['excl']['context_window_left'] = -self.excl_spin_box_context_window_left.value()
        else:
            self.settings_custom['excl']['context_window_left'] = self.excl_spin_box_context_window_left.value()

        if self.excl_spin_box_context_window_right.prefix() == self.tr('L'):
            self.settings_custom['excl']['context_window_right'] = -self.excl_spin_box_context_window_right.value()
        else:
            self.settings_custom['excl']['context_window_right'] = self.excl_spin_box_context_window_right.value()

    def load(self):
        # Calculate size
        if 'size_multi' not in self.__dict__:
            incl_multi_search_mode = self.settings_custom['incl']['multi_search_mode']
            excl_multi_search_mode = self.settings_custom['excl']['multi_search_mode']

            self.incl_checkbox_multi_search_mode.setChecked(False)
            self.excl_checkbox_multi_search_mode.setChecked(False)

            self.incl_group_box.adjustSize()
            self.excl_group_box.adjustSize()
            self.adjustSize()

            self.size_normal = self.size()

            self.incl_checkbox_multi_search_mode.setChecked(True)
            self.excl_checkbox_multi_search_mode.setChecked(True)

            self.incl_group_box.adjustSize()
            self.excl_group_box.adjustSize()
            self.adjustSize()

            self.size_multi = QSize(self.size_normal.width(), self.size().height())

            self.incl_checkbox_multi_search_mode.setChecked(incl_multi_search_mode)
            self.excl_checkbox_multi_search_mode.setChecked(excl_multi_search_mode)

        self.load_settings()
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

    checkbox_no_limit = QCheckBox(_tr('wl_widgets_no_limit', 'No Limit'), parent)

    checkbox_no_limit.stateChanged.connect(no_limit_changed)

    no_limit_changed()

    return spin_box_no_limit, checkbox_no_limit

# Token Settings
def wl_widgets_token_settings(parent):
    def words_changed():
        if checkbox_words.isChecked():
            checkbox_all_lowercase.setEnabled(True)
            checkbox_all_uppercase.setEnabled(True)
            checkbox_title_case.setEnabled(True)
        else:
            checkbox_all_lowercase.setEnabled(False)
            checkbox_all_uppercase.setEnabled(False)
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

    checkbox_words = QCheckBox(_tr('wl_widgets_token_settings', 'Words'), parent)
    checkbox_all_lowercase = QCheckBox(_tr('wl_widgets_token_settings', 'All Lowercase'), parent)
    checkbox_all_uppercase = QCheckBox(_tr('wl_widgets_token_settings', 'All Uppercase'), parent)
    checkbox_title_case = QCheckBox(_tr('wl_widgets_token_settings', 'Title Case'), parent)
    checkbox_nums = QCheckBox(_tr('wl_widgets_token_settings', 'Numerals'), parent)
    checkbox_puncs = QCheckBox(_tr('wl_widgets_token_settings', 'Punctuations'), parent)

    checkbox_treat_as_all_lowercase = QCheckBox(_tr('wl_widgets_token_settings', 'Treat as all lowercase'), parent)
    checkbox_lemmatize_tokens = QCheckBox(_tr('wl_widgets_token_settings', 'Lemmatize all tokens'), parent)
    checkbox_filter_stop_words = QCheckBox(_tr('wl_widgets_token_settings', 'Filter stop words'), parent)

    checkbox_ignore_tags = QCheckBox(_tr('wl_widgets_token_settings', 'Ignore tags'), parent)
    checkbox_use_tags = QCheckBox(_tr('wl_widgets_token_settings', 'Use tags only'), parent)

    checkbox_words.stateChanged.connect(words_changed)
    checkbox_ignore_tags.stateChanged.connect(ignore_tags_changed)
    checkbox_use_tags.stateChanged.connect(use_tags_changed)

    words_changed()
    ignore_tags_changed()
    use_tags_changed()

    return (
        checkbox_words,
        checkbox_all_lowercase,
        checkbox_all_uppercase,
        checkbox_title_case,
        checkbox_nums,
        checkbox_puncs,

        checkbox_treat_as_all_lowercase,
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

    checkbox_puncs = QCheckBox(_tr('wl_widgets_token_settings_concordancer', 'Punctuations'), parent)

    checkbox_ignore_tags = QCheckBox(_tr('wl_widgets_token_settings_concordancer', 'Ignore tags'), parent)
    checkbox_use_tags = QCheckBox(_tr('wl_widgets_token_settings_concordancer', 'Use tags only'), parent)

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
            label_search_term.setText(_tr('wl_widgets_search_settings', 'Search Terms:'))

            if line_edit_search_term.text() and list_search_terms.model().rowCount() == 0:
                list_search_terms.load_items([line_edit_search_term.text()])

            stacked_widget_search_term.setCurrentIndex(1)
        else:
            label_search_term.setText(_tr('wl_widgets_search_settings', 'Search Term:'))

            stacked_widget_search_term.setCurrentIndex(0)

    def token_settings_changed():
        token_settings = main.settings_custom[tab]['token_settings']

        if token_settings['ignore_tags'] or token_settings['use_tags']:
            checkbox_match_without_tags.setEnabled(False)
            checkbox_match_tags.setEnabled(False)
        else:
            if not checkbox_match_tags.isChecked():
                checkbox_match_without_tags.setEnabled(True)

            if not checkbox_match_without_tags.isChecked():
                checkbox_match_tags.setEnabled(True)

        if token_settings['use_tags']:
            checkbox_match_inflected_forms.setEnabled(False)
        elif not token_settings['use_tags'] or token_settings['ignore_tags']:
            checkbox_match_inflected_forms.setEnabled(True)

        if checkbox_match_without_tags.isEnabled():
            match_without_tags_changed()
        if checkbox_match_tags.isEnabled():
            match_tags_changed()

    def match_without_tags_changed():
        if checkbox_match_without_tags.isChecked():
            checkbox_match_tags.setEnabled(False)
        else:
            checkbox_match_tags.setEnabled(True)

    def match_tags_changed():
        if checkbox_match_tags.isChecked():
            checkbox_match_inflected_forms.setEnabled(False)
            checkbox_match_without_tags.setEnabled(False)
        else:
            checkbox_match_inflected_forms.setEnabled(True)
            checkbox_match_without_tags.setEnabled(True)

    main = wl_misc.find_wl_main(parent)

    label_search_term = QLabel(_tr('wl_widgets_search_settings', 'Search Term:'), parent)
    checkbox_multi_search_mode = QCheckBox(_tr('wl_widgets_search_settings', 'Multi-search Mode'), parent)
    line_edit_search_term = QLineEdit(parent)
    list_search_terms = wl_lists.Wl_List_Search_Terms(parent)
    label_delimiter = wl_labels.Wl_Label_Hint(_tr('wl_widgets_search_settings', '* Use whitespace to delimit multiple tokens'), parent)

    checkbox_match_case = QCheckBox(_tr('wl_widgets_search_settings', 'Match case'), parent)
    checkbox_match_whole_words = QCheckBox(_tr('wl_widgets_search_settings', 'Match whole words'), parent)
    checkbox_match_inflected_forms = QCheckBox(_tr('wl_widgets_search_settings', 'Match inflected forms'), parent)
    checkbox_use_regex = QCheckBox(_tr('wl_widgets_search_settings', 'Use regular expressions'), parent)
    checkbox_match_without_tags = QCheckBox(_tr('wl_widgets_search_settings', 'Match without tags'), parent)
    checkbox_match_tags = QCheckBox(_tr('wl_widgets_search_settings', 'Match tags only'), parent)

    wrapper_search_terms = QWidget(parent)

    wrapper_search_terms.setLayout(wl_layouts.Wl_Layout())
    wrapper_search_terms.layout().addWidget(list_search_terms, 0, 0, 6, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_add, 0, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_ins, 1, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_del, 2, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_clr, 3, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_imp, 4, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_exp, 5, 1)

    wrapper_search_terms.layout().setContentsMargins(0, 0, 0, 0)

    stacked_widget_search_term = wl_layouts.Wl_Stacked_Widget(parent)
    stacked_widget_search_term.addWidget(line_edit_search_term)
    stacked_widget_search_term.addWidget(wrapper_search_terms)

    checkbox_match_tags.token_settings_changed = token_settings_changed

    checkbox_multi_search_mode.stateChanged.connect(multi_search_mode_changed)
    checkbox_match_without_tags.stateChanged.connect(match_without_tags_changed)
    checkbox_match_tags.stateChanged.connect(match_tags_changed)

    multi_search_mode_changed()
    token_settings_changed()
    match_without_tags_changed()
    match_tags_changed()

    return (
        label_search_term,
        checkbox_multi_search_mode,

        stacked_widget_search_term,
        line_edit_search_term,
        list_search_terms,
        label_delimiter,

        checkbox_match_case,
        checkbox_match_whole_words,
        checkbox_match_inflected_forms,
        checkbox_use_regex,
        checkbox_match_without_tags,
        checkbox_match_tags
    )

def wl_widgets_search_settings_tokens(parent, tab):
    (
        label_search_term,
        checkbox_multi_search_mode,

        stacked_widget_search_term,
        line_edit_search_term,
        list_search_terms,
        label_delimiter,

        checkbox_match_case,
        checkbox_match_whole_words,
        checkbox_match_inflected_forms,
        checkbox_use_regex,
        checkbox_match_without_tags,
        checkbox_match_tags
    ) = wl_widgets_search_settings(parent, tab)

    label_delimiter.setText(_tr('wl_widgets_search_settings_tokens', '* Only 1 token is allowed in each search term'))

    return (
        label_search_term,
        checkbox_multi_search_mode,

        stacked_widget_search_term,
        line_edit_search_term,
        list_search_terms,
        label_delimiter,

        checkbox_match_case,
        checkbox_match_whole_words,
        checkbox_match_inflected_forms,
        checkbox_use_regex,
        checkbox_match_without_tags,
        checkbox_match_tags
    )

def wl_widgets_context_settings(parent, tab):
    main = wl_misc.find_wl_main(parent)

    label_context_settings = QLabel(_tr('wl_widgets_context_settings', 'Context Settings:'), parent)
    button_context_settings = QPushButton(_tr('wl_widgets_context_settings', 'Settings...'), parent)

    dialog_context_settings = Wl_Dialog_Context_Settings(main, tab = tab)
    main.__dict__[f'wl_context_settings_{tab}'] = dialog_context_settings

    button_context_settings.clicked.connect(lambda: main.__dict__[f'wl_context_settings_{tab}'].load()) # pylint: disable=unnecessary-lambda

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

    checkbox_size_sync = QCheckBox(_tr('wl_widgets_size', 'Sync'), parent)
    label_size_min = QLabel(_tr('wl_widgets_size', 'From'), parent)
    spin_box_size_min = wl_boxes.Wl_Spin_Box(parent)
    label_size_max = QLabel(_tr('wl_widgets_size', 'To'), parent)
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
        if (
            checkbox_window_sync.isChecked()

            or (
                spin_box_window_left.prefix() == _tr('wl_widgets_window', 'L')
                and spin_box_window_right.prefix() == _tr('wl_widgets_window', 'L')
                and spin_box_window_left.value() < spin_box_window_right.value()
            ) or (
                spin_box_window_left.prefix() == _tr('wl_widgets_window', 'R')
                and spin_box_window_right.prefix() == _tr('wl_widgets_window', 'R')
                and spin_box_window_left.value() > spin_box_window_right.value()
            ) or (
                spin_box_window_left.prefix() == _tr('wl_widgets_window', 'R')
                and spin_box_window_right.prefix() == _tr('wl_widgets_window', 'L')
            )
        ):
            spin_box_window_right.setPrefix(spin_box_window_left.prefix())
            spin_box_window_right.setValue(spin_box_window_left.value())

    def window_right_changed():
        if (
            checkbox_window_sync.isChecked()

            or (
                spin_box_window_left.prefix() == _tr('wl_widgets_window', 'L')
                and spin_box_window_right.prefix() == _tr('wl_widgets_window', 'L')
                and spin_box_window_left.value() < spin_box_window_right.value()
            ) or (
                spin_box_window_left.prefix() == _tr('wl_widgets_window', 'R')
                and spin_box_window_right.prefix() == _tr('wl_widgets_window', 'R')
                and spin_box_window_left.value() > spin_box_window_right.value()
            ) or (
                spin_box_window_left.prefix() == _tr('wl_widgets_window', 'R')
                and spin_box_window_right.prefix() == _tr('wl_widgets_window', 'L')
            )
        ):
            spin_box_window_left.setPrefix(spin_box_window_right.prefix())
            spin_box_window_left.setValue(spin_box_window_right.value())

    checkbox_window_sync = QCheckBox(_tr('wl_widgets_window', 'Sync'), parent)
    label_window_left = QLabel(_tr('wl_widgets_window', 'From'), parent)
    spin_box_window_left = wl_boxes.Wl_Spin_Box_Window(parent)
    label_window_right = QLabel(_tr('wl_widgets_window', 'To'), parent)
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

def wl_widgets_measures_wordlist_generator(parent):
    main = wl_misc.find_wl_main(parent)

    label_measure_dispersion = QLabel(_tr('wl_widgets_measures_wordlist_generator', 'Measure of Dispersion:'), parent)
    combo_box_measure_dispersion = wl_boxes.Wl_Combo_Box(parent)
    label_measure_adjusted_freq = QLabel(_tr('wl_widgets_measures_wordlist_generator', 'Measure of Adjusted Frequency:'), parent)
    combo_box_measure_adjusted_freq = wl_boxes.Wl_Combo_Box(parent)

    combo_box_measure_dispersion.addItems(list(main.settings_global['measures_dispersion'].keys()))
    combo_box_measure_adjusted_freq.addItems(list(main.settings_global['measures_adjusted_freq'].keys()))

    return (
        label_measure_dispersion,
        combo_box_measure_dispersion,
        label_measure_adjusted_freq,
        combo_box_measure_adjusted_freq
    )

def wl_widgets_measures_collocation_extractor(parent, tab):
    label_test_statistical_significance = QLabel(_tr('wl_widgets_test_significance', 'Test of Statistical Significance:'), parent)
    combo_box_test_statistical_significance = wl_boxes.Wl_Combo_Box(parent)
    label_measure_bayes_factor = QLabel(_tr('wl_widgets_measure_bayes_factor', 'Measure of Bayes Factor:'), parent)
    combo_box_measure_bayes_factor = wl_boxes.Wl_Combo_Box(parent)
    label_measure_effect_size = QLabel(_tr('wl_widgets_measure_effect_size', 'Measure of Effect Size:'), parent)
    combo_box_measure_effect_size = wl_boxes.Wl_Combo_Box(parent)

    for measure, vals in parent.main.settings_global['tests_statistical_significance'].items():
        if vals[tab]:
            combo_box_test_statistical_significance.addItem(measure)

    for measure, vals in parent.main.settings_global['measures_bayes_factor'].items():
        if vals[tab]:
            combo_box_measure_bayes_factor.addItem(measure)

    combo_box_measure_effect_size.addItems(list(parent.main.settings_global['measures_effect_size'].keys()))

    return (
        label_test_statistical_significance,
        combo_box_test_statistical_significance,
        label_measure_bayes_factor,
        combo_box_measure_bayes_factor,
        label_measure_effect_size,
        combo_box_measure_effect_size
    )

# Table Settings
def wl_widgets_table_settings(parent, tables):
    def show_pct_changed():
        for table in tables:
            table.show_pct = checkbox_show_pct.isChecked()

            if any((table.model().item(0, i) for i in range(table.model().columnCount()))):
                table.toggle_pct()

    def show_cumulative_changed():
        for table in tables:
            table.show_cumulative = checkbox_show_cumulative.isChecked()

            if any((table.model().item(0, i) for i in range(table.model().columnCount()))):
                table.toggle_cumulative()

    def show_breakdown_changed():
        for table in tables:
            table.show_breakdown = checkbox_show_breakdown.isChecked()

            table.toggle_breakdown()

    checkbox_show_pct = QCheckBox(_tr('wl_widgets_table_settings', 'Show percentage data'), parent)
    checkbox_show_cumulative = QCheckBox(_tr('wl_widgets_table_settings', 'Show cumulative data'), parent)
    checkbox_show_breakdown = QCheckBox(_tr('wl_widgets_table_settings', 'Show breakdown by file'), parent)

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

        for file in self.main.wl_file_area.get_selected_files():
            self.addItem(file['name'])

        self.addItem(self.tr('Total'))

        if file_old and self.findText(file_old) > -1:
            self.setCurrentText(file_old)

def wl_widgets_fig_settings(parent, tab):
    def graph_type_changed():
        if combo_box_graph_type.currentText() == _tr('wl_widgets_fig_settings', 'Line Chart'):
            combo_box_sort_by_file.setEnabled(True)

            use_data_changed()
        else:
            combo_box_sort_by_file.setEnabled(True)
            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)

    def use_data_changed():
        if combo_box_graph_type.currentText() == _tr('wl_widgets_fig_settings', 'Line Chart'):
            if combo_box_use_data.currentText() == _tr('wl_widgets_fig_settings', 'Frequency'):
                checkbox_use_pct.setEnabled(True)
                checkbox_use_cumulative.setEnabled(True)
            else:
                checkbox_use_pct.setEnabled(False)
                checkbox_use_cumulative.setEnabled(False)

    def measures_changed_wordlist_generator():
        settings_global = parent.main.settings_global
        settings_default = parent.main.settings_default[tab]
        settings_custom = parent.main.settings_custom[tab]

        use_data_old = settings_custom['fig_settings']['use_data']

        combo_box_use_data.clear()

        combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'Frequency'))

        text_measure_dispersion = settings_custom['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings_custom['generation_settings']['measure_adjusted_freq']

        measure_dispersion = settings_global['measures_dispersion'][text_measure_dispersion]
        measure_adjusted_freq = settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]

        if measure_dispersion['col_text'] is not None:
            combo_box_use_data.addItem(measure_dispersion['col_text'])
        if measure_adjusted_freq['col_text'] is not None:
            combo_box_use_data.addItem(measure_adjusted_freq['col_text'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(settings_default['fig_settings']['use_data'])

    def measures_changed_collocation_extractor():
        settings_global = parent.main.settings_global
        settings_default = parent.main.settings_default[tab]
        settings_custom = parent.main.settings_custom[tab]

        use_data_old = settings_custom['fig_settings']['use_data']

        combo_box_use_data.clear()

        for i in range(settings_custom['generation_settings']['window_left'], settings_custom['generation_settings']['window_right'] + 1):
            if i < 0:
                combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'L') + str(-i))
            elif i > 0:
                combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'R') + str(i))

        combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'Frequency'))

        text_test_statistical_significance = settings_custom['generation_settings']['test_statistical_significance']
        text_measure_bayes_factor = settings_custom['generation_settings']['measure_bayes_factor']
        text_measure_effect_size = settings_custom['generation_settings']['measure_effect_size']

        test_statistical_significance = settings_global['tests_statistical_significance'][text_test_statistical_significance]
        measure_bayes_factor = settings_global['measures_bayes_factor'][text_measure_bayes_factor]
        measure_effect_size = settings_global['measures_effect_size'][text_measure_effect_size]

        if test_statistical_significance['func']:
            if test_statistical_significance['col_text']:
                combo_box_use_data.addItem(test_statistical_significance['col_text'])

            combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'p-value'))

        if measure_bayes_factor['func']:
            combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'Bayes Factor'))

        if measure_effect_size['func']:
            combo_box_use_data.addItem(measure_effect_size['col_text'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(settings_default['fig_settings']['use_data'])

    def measures_changed_keyword_extractor():
        settings_global = parent.main.settings_global
        settings_default = parent.main.settings_default[tab]
        settings_custom = parent.main.settings_custom[tab]

        use_data_old = settings_custom['fig_settings']['use_data']

        combo_box_use_data.clear()

        combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'Frequency'))

        text_test_statistical_significance = settings_custom['generation_settings']['test_statistical_significance']
        text_measure_bayes_factor = settings_custom['generation_settings']['measure_bayes_factor']
        text_measure_effect_size = settings_custom['generation_settings']['measure_effect_size']

        test_statistical_significance = settings_global['tests_statistical_significance'][text_test_statistical_significance]
        measure_bayes_factor = settings_global['measures_bayes_factor'][text_measure_bayes_factor]
        measure_effect_size = settings_global['measures_effect_size'][text_measure_effect_size]

        if test_statistical_significance['func']:
            if test_statistical_significance['col_text']:
                combo_box_use_data.addItem(test_statistical_significance['col_text'])

            combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'p-value'))

        if measure_bayes_factor['func']:
            combo_box_use_data.addItem(_tr('wl_widgets_fig_settings', 'Bayes Factor'))

        if measure_effect_size['func']:
            combo_box_use_data.addItem(measure_effect_size['col_text'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(settings_default['fig_settings']['use_data'])

    label_graph_type = QLabel(_tr('wl_widgets_fig_settings', 'Graph Type:'), parent)
    combo_box_graph_type = wl_boxes.Wl_Combo_Box(parent)
    label_sort_by_file = QLabel(_tr('wl_widgets_fig_settings', 'Sort by File:'), parent)
    combo_box_sort_by_file = Wl_Combo_Box_File_Figure_Settings(parent)
    label_use_data = QLabel(_tr('wl_widgets_fig_settings', 'Use Data:'), parent)
    combo_box_use_data = wl_boxes.Wl_Combo_Box(parent)
    checkbox_use_pct = QCheckBox(_tr('wl_widgets_fig_settings', 'Use percentage data'), parent)
    checkbox_use_cumulative = QCheckBox(_tr('wl_widgets_fig_settings', 'Use cumulative data'), parent)

    combo_box_graph_type.addItems([
        _tr('wl_widgets_fig_settings', 'Line Chart'),
        _tr('wl_widgets_fig_settings', 'Word Cloud')
    ])

    # Network Graph
    if tab in ['collocation_extractor', 'colligation_extractor']:
        combo_box_graph_type.addItem(_tr('wl_widgets_fig_settings', 'Network Graph'))

    if tab in ['wordlist_generator', 'ngram_generator', 'collocation_extractor', 'colligation_extractor', 'keyword_extractor']:
        if tab in ['wordlist_generator', 'ngram_generator']:
            combo_box_use_data.measures_changed = measures_changed_wordlist_generator
        elif tab in ['collocation_extractor', 'colligation_extractor']:
            combo_box_use_data.measures_changed = measures_changed_collocation_extractor
        elif tab == 'keyword_extractor':
            combo_box_use_data.measures_changed = measures_changed_keyword_extractor

        combo_box_use_data.measures_changed()

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

    label_min = QLabel(_tr('wl_widgets_filter', 'From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wl_widgets_no_limit(parent)

    label_max = QLabel(_tr('wl_widgets_filter', 'To'), parent)
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
        precision = main.settings_custom['tables']['precision_settings']['precision_decimals']

        spin_box_min.setDecimals(precision)
        spin_box_max.setDecimals(precision)

        spin_box_min.setSingleStep(0.1 ** precision)
        spin_box_max.setSingleStep(0.1 ** precision)

    main = wl_misc.find_wl_main(parent)

    label_min = QLabel(_tr('wl_widgets_filter_measures', 'From'), parent)
    (spin_box_min,
     checkbox_min_no_limit) = wl_widgets_no_limit(parent, double = True)

    label_max = QLabel(_tr('wl_widgets_filter_measures', 'To'), parent)
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

def wl_widgets_filter_p_val(parent):
    def min_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_max.setValue(spin_box_min.value())

    def max_changed():
        if spin_box_min.value() > spin_box_max.value():
            spin_box_min.setValue(spin_box_max.value())

    def precision_changed():
        precision = main.settings_custom['tables']['precision_settings']['precision_p_vals']

        spin_box_min.setDecimals(precision)
        spin_box_max.setDecimals(precision)

        spin_box_min.setSingleStep(0.1 ** precision)
        spin_box_max.setSingleStep(0.1 ** precision)

    main = wl_misc.find_wl_main(parent)

    label_min = QLabel(_tr('wl_widgets_filter_p_val', 'From'), parent)
    (
        spin_box_min,
        checkbox_min_no_limit
    ) = wl_widgets_no_limit(parent, double = True)

    label_max = QLabel(_tr('wl_widgets_filter_p_val', 'To'), parent)
    (
        spin_box_max,
        checkbox_max_no_limit
    ) = wl_widgets_no_limit(parent, double = True)

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

        combo_box_filter_file.addItem(_tr('wl_widgets_filter_results', 'Total'))

        if combo_box_filter_file.findText(file_old) > -1:
            combo_box_filter_file.setCurrentText(file_old)

    label_filter_file = QLabel(_tr('wl_widgets_filter_results', 'Filter File:'), parent)
    combo_box_filter_file = wl_boxes.Wl_Combo_Box(parent)
    button_filter_results = QPushButton(_tr('wl_widgets_filter_results', 'Filter Results in Table'), parent)

    button_filter_results.clicked.connect(lambda: table.update_filters()) # pylint: disable=unnecessary-lambda

    table.itemChanged.connect(table_item_changed)

    table_item_changed()

    return (label_filter_file, combo_box_filter_file,
            button_filter_results)

# Settings -> Measures
def wl_widgets_num_sub_sections(parent):
    label_divide_each_file_into = QLabel(_tr('wl_widgets_num_sub_sections', 'Divide each file into'), parent)
    spin_box_num_sub_sections = wl_boxes.Wl_Spin_Box(parent)
    label_sub_sections = QLabel(_tr('wl_widgets_num_sub_sections', 'sub-sections'), parent)

    spin_box_num_sub_sections.setRange(2, 1000)

    return label_divide_each_file_into, spin_box_num_sub_sections, label_sub_sections

def wl_widgets_use_data_freq(parent):
    label_use_data = QLabel(_tr('wl_widgets_use_data_freq', 'Use Data:'), parent)
    combo_box_use_data = wl_boxes.Wl_Combo_Box(parent)

    combo_box_use_data.addItems([
        _tr('wl_widgets_use_data_freq', 'Absolute Frequency'),
        _tr('wl_widgets_use_data_freq', 'Relative Frequency')
    ])

    return label_use_data, combo_box_use_data

def wl_widgets_direction(parent):
    label_direction = QLabel(_tr('wl_widgets_direction', 'Direction:'), parent)
    combo_box_direction = wl_boxes.Wl_Combo_Box(parent)

    combo_box_direction.addItems([
        _tr('wl_widgets_direction', 'Two-tailed'),
        _tr('wl_widgets_direction', 'Left-tailed'),
        _tr('wl_widgets_direction', 'Right-tailed')
    ])

    return label_direction, combo_box_direction

# Settings -> Figures
def wl_widgets_pick_color(parent):
    def get_color():
        return re.search(r'#[0-9a-zA-Z]{6}', label_pick_color.text()).group()

    def set_color(color):
        label_pick_color.setText(f'<span style="margin-right: 3px; background-color: {color}; color: {color}">00</span> <span>{color.upper()}</span>')

    def pick_color():
        color_picked = QColorDialog.getColor(QColor(get_color()), parent, _tr('wl_widgets_pick_color', 'Pick Color'))

        if color_picked.isValid():
            label_pick_color.set_color(color_picked.name())

    label_pick_color = wl_labels.Wl_Label_Html('', parent)
    button_pick_color = QPushButton(_tr('wl_widgets_pick_color', 'Pick Color...'), parent)

    label_pick_color.get_color = get_color
    label_pick_color.set_color = set_color

    button_pick_color.clicked.connect(pick_color)

    return label_pick_color, button_pick_color
