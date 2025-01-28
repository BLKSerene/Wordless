# ----------------------------------------------------------------------
# Wordless: Widgets - Widgets
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget
)

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_measures import wl_measure_utils
from wordless.wl_utils import wl_misc
from wordless.wl_widgets import (
    wl_boxes,
    wl_labels,
    wl_layouts,
    wl_lists
)

_tr = QCoreApplication.translate

class Wl_Dialog_Context_Settings(wl_dialogs.Wl_Dialog_Settings):
    def __init__(self, main, tab):
        super().__init__(main, title = _tr('Wl_Dialog_Context_Settings', 'Context Settings'))

        self.tab = tab
        self.settings_custom = self.main.settings_custom[self.tab]['search_settings']['context_settings']
        self.settings_default = self.main.settings_custom[self.tab]['search_settings']['context_settings']

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

        self.incl_label_context_window = QLabel(self.tr('Context window:'), self)
        (
            self.incl_checkbox_context_window_sync,
            self.incl_label_context_window_left,
            self.incl_spin_box_context_window_left,
            self.incl_label_context_window_right,
            self.incl_spin_box_context_window_right
        ) = wl_boxes.wl_spin_boxes_min_max_sync_window(self)

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

        self.incl_group_box.layout().setRowStretch(12, 1)
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

        self.excl_label_context_window = QLabel(self.tr('Context window:'), self)
        (
            self.excl_checkbox_context_window_sync,
            self.excl_label_context_window_left,
            self.excl_spin_box_context_window_left,
            self.excl_label_context_window_right,
            self.excl_spin_box_context_window_right
        ) = wl_boxes.wl_spin_boxes_min_max_sync_window(self)

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

        self.excl_group_box.layout().setRowStretch(12, 1)
        self.excl_group_box.layout().setColumnStretch(1, 1)
        self.excl_group_box.layout().setColumnStretch(3, 1)

        self.incl_line_edit_search_term.returnPressed.connect(self.button_save.click)
        self.excl_line_edit_search_term.returnPressed.connect(self.button_save.click)

        self.wrapper_settings.layout().addWidget(self.incl_group_box, 0, 0)
        self.wrapper_settings.layout().addWidget(self.excl_group_box, 0, 1)

        self.wrapper_settings.layout().setColumnStretch(0, 1)
        self.wrapper_settings.layout().setColumnStretch(1, 1)

    def multi_search_mode_changed(self):
        self.incl_group_box.adjustSize()
        self.excl_group_box.adjustSize()
        self.wrapper_settings.adjustSize()
        self.adjustSize()

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
        self.load_settings()

        self.exec_()

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

    def assign_pos_tags_changed():
        if checkbox_assign_pos_tags.isChecked():
            checkbox_ignore_tags.setEnabled(False)
        else:
            checkbox_ignore_tags.setEnabled(not checkbox_use_tags.isChecked())

    def ignore_tags_changed():
        if checkbox_ignore_tags.isChecked():
            checkbox_assign_pos_tags.setEnabled(False)
            checkbox_use_tags.setEnabled(False)
        else:
            checkbox_assign_pos_tags.setEnabled(True)
            checkbox_use_tags.setEnabled(True)

    def use_tags_changed():
        if checkbox_use_tags.isChecked():
            checkbox_apply_lemmatization.setEnabled(False)
            checkbox_ignore_tags.setEnabled(False)
        else:
            checkbox_apply_lemmatization.setEnabled(True)
            checkbox_ignore_tags.setEnabled(not checkbox_assign_pos_tags.isChecked())

    checkbox_words = QCheckBox(_tr('wl_widgets', 'Words'), parent)
    checkbox_all_lowercase = QCheckBox(_tr('wl_widgets', 'All lowercase'), parent)
    checkbox_all_uppercase = QCheckBox(_tr('wl_widgets', 'All uppercase'), parent)
    checkbox_title_case = QCheckBox(_tr('wl_widgets', 'Title case'), parent)
    checkbox_nums = QCheckBox(_tr('wl_widgets', 'Numerals'), parent)
    checkbox_punc_marks = QCheckBox(_tr('wl_widgets', 'Punctuation marks'), parent)

    checkbox_treat_as_all_lowercase = QCheckBox(_tr('wl_widgets', 'Treat as all lowercase'), parent)
    checkbox_apply_lemmatization = QCheckBox(_tr('wl_widgets', 'Apply lemmatization'), parent)
    checkbox_filter_stop_words = QCheckBox(_tr('wl_widgets', 'Filter stop words'), parent)

    checkbox_assign_pos_tags = QCheckBox(_tr('wl_widgets', 'Assign part-of-speech tags'), parent)
    checkbox_ignore_tags = QCheckBox(_tr('wl_widgets', 'Ignore tags'), parent)
    checkbox_use_tags = QCheckBox(_tr('wl_widgets', 'Use tags only'), parent)

    checkbox_words.stateChanged.connect(words_changed)
    checkbox_assign_pos_tags.stateChanged.connect(assign_pos_tags_changed)
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
        checkbox_punc_marks,

        checkbox_treat_as_all_lowercase,
        checkbox_apply_lemmatization,
        checkbox_filter_stop_words,

        checkbox_assign_pos_tags,
        checkbox_ignore_tags,
        checkbox_use_tags
    )

def wl_widgets_token_settings_concordancer(parent):
    def assign_pos_tags_changed():
        if checkbox_assign_pos_tags.isChecked():
            checkbox_ignore_tags.setEnabled(False)
        else:
            checkbox_ignore_tags.setEnabled(not checkbox_use_tags.isChecked())

    def ignore_tags_changed():
        if checkbox_ignore_tags.isChecked():
            checkbox_assign_pos_tags.setEnabled(False)
            checkbox_use_tags.setEnabled(False)
        else:
            checkbox_assign_pos_tags.setEnabled(True)
            checkbox_use_tags.setEnabled(True)

    def use_tags_changed():
        if checkbox_use_tags.isChecked():
            checkbox_ignore_tags.setEnabled(False)
        else:
            checkbox_ignore_tags.setEnabled(not checkbox_assign_pos_tags.isChecked())

    checkbox_punc_marks = QCheckBox(_tr('wl_widgets', 'Punctuation marks'), parent)

    checkbox_assign_pos_tags = QCheckBox(_tr('wl_widgets', 'Assign part-of-speech tags'), parent)
    checkbox_ignore_tags = QCheckBox(_tr('wl_widgets', 'Ignore tags'), parent)
    checkbox_use_tags = QCheckBox(_tr('wl_widgets', 'Use tags only'), parent)

    checkbox_assign_pos_tags.stateChanged.connect(assign_pos_tags_changed)
    checkbox_ignore_tags.stateChanged.connect(ignore_tags_changed)
    checkbox_use_tags.stateChanged.connect(use_tags_changed)

    ignore_tags_changed()
    use_tags_changed()

    return (
        checkbox_punc_marks,

        checkbox_assign_pos_tags,
        checkbox_ignore_tags,
        checkbox_use_tags
    )

# Search Settings
def wl_widgets_search_settings(parent, tab):
    def multi_search_mode_changed():
        if checkbox_multi_search_mode.isChecked():
            label_search_term.setText(_tr('wl_widgets', 'Search terms:'))
            search_term = line_edit_search_term.text().strip()

            # Automatically add the non-empty search term
            if search_term and list_search_terms.model().rowCount() == 0:
                list_search_terms.load_items([search_term])

            stacked_widget_search_term.setCurrentIndex(1)
        else:
            label_search_term.setText(_tr('wl_widgets', 'Search term:'))

            stacked_widget_search_term.setCurrentIndex(0)

    def token_settings_changed(token_settings = None):
        if token_settings is None:
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
        checkbox_match_tags.setEnabled(not checkbox_match_without_tags.isChecked())

    def match_tags_changed():
        if checkbox_match_tags.isChecked():
            checkbox_match_inflected_forms.setEnabled(False)
            checkbox_match_without_tags.setEnabled(False)
        else:
            checkbox_match_inflected_forms.setEnabled(True)
            checkbox_match_without_tags.setEnabled(True)

    main = wl_misc.find_wl_main(parent)

    label_search_term = QLabel(_tr('wl_widgets', 'Search term:'), parent)
    checkbox_multi_search_mode = QCheckBox(_tr('wl_widgets', 'Multi-search mode'), parent)
    line_edit_search_term = QLineEdit(parent)
    list_search_terms = wl_lists.Wl_List_Search_Terms(parent)
    label_delimiter = wl_labels.Wl_Label_Hint(_tr('wl_widgets', '* Use whitespace to delimit multiple tokens'), parent)

    checkbox_match_case = QCheckBox(_tr('wl_widgets', 'Match case'), parent)
    checkbox_match_whole_words = QCheckBox(_tr('wl_widgets', 'Match whole words'), parent)
    checkbox_match_inflected_forms = QCheckBox(_tr('wl_widgets', 'Match inflected forms'), parent)
    checkbox_use_regex = QCheckBox(_tr('wl_widgets', 'Use regular expressions'), parent)
    checkbox_match_without_tags = QCheckBox(_tr('wl_widgets', 'Match without tags'), parent)
    checkbox_match_tags = QCheckBox(_tr('wl_widgets', 'Match tags only'), parent)

    wrapper_search_terms = QWidget(parent)

    wrapper_search_terms.setLayout(wl_layouts.Wl_Layout())
    wrapper_search_terms.layout().addWidget(list_search_terms, 0, 0, 7, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_add, 0, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_ins, 1, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_del, 2, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_clr, 3, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_imp, 4, 1)
    wrapper_search_terms.layout().addWidget(list_search_terms.button_exp, 5, 1)

    wrapper_search_terms.layout().setRowStretch(6, 1)
    wrapper_search_terms.layout().setContentsMargins(0, 0, 0, 0)

    stacked_widget_search_term = wl_layouts.Wl_Stacked_Widget_Resizable(parent)
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

    label_delimiter.setText(_tr('wl_widgets', '* Only 1 token is allowed in each search term'))

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

    label_context_settings = QLabel(_tr('wl_widgets', 'Context settings:'), parent)
    button_context_settings = QPushButton(_tr('wl_widgets', 'Settings...'), parent)

    dialog_context_settings = Wl_Dialog_Context_Settings(main, tab = tab)
    main.__dict__[f'wl_context_settings_{tab}'] = dialog_context_settings

    button_context_settings.clicked.connect(lambda: main.__dict__[f'wl_context_settings_{tab}'].load()) # pylint: disable=unnecessary-lambda

    return label_context_settings, button_context_settings

# Generation Settings
def wl_widgets_measures_wordlist_ngram_generation(parent):
    label_measure_dispersion = QLabel(_tr('wl_widgets', 'Measure of dispersion:'), parent)
    combo_box_measure_dispersion = wl_boxes.Wl_Combo_Box_Measure(parent, measure_type = 'dispersion')
    label_measure_adjusted_freq = QLabel(_tr('wl_widgets', 'Measure of adjusted frequency:'), parent)
    combo_box_measure_adjusted_freq = wl_boxes.Wl_Combo_Box_Measure(parent, measure_type = 'adjusted_freq')

    return (
        label_measure_dispersion, combo_box_measure_dispersion,
        label_measure_adjusted_freq, combo_box_measure_adjusted_freq
    )

def wl_widgets_measures_collocation_keyword_extraction(parent, extraction_type):
    main = wl_misc.find_wl_main(parent)

    label_test_statistical_significance = QLabel(_tr('wl_widgets', 'Test of statistical significance:'), parent)
    combo_box_test_statistical_significance = wl_boxes.Wl_Combo_Box_Measure(parent, measure_type = 'statistical_significance')
    label_measure_bayes_factor = QLabel(_tr('wl_widgets', 'Measure of Bayes factor:'), parent)
    combo_box_measure_bayes_factor = wl_boxes.Wl_Combo_Box_Measure(parent, measure_type = 'bayes_factor')
    label_measure_effect_size = QLabel(_tr('wl_widgets', 'Measure of effect size:'), parent)
    combo_box_measure_effect_size = wl_boxes.Wl_Combo_Box_Measure(parent, measure_type = 'effect_size')

    for i in reversed(range(combo_box_test_statistical_significance.count())):
        measure_text = combo_box_test_statistical_significance.itemText(i)
        measure_code = wl_measure_utils.to_measure_code(main, 'statistical_significance', measure_text)

        if not main.settings_global['tests_statistical_significance'][measure_code][extraction_type]:
            combo_box_test_statistical_significance.removeItem(i)

    for i in reversed(range(combo_box_measure_bayes_factor.count())):
        measure_text = combo_box_measure_bayes_factor.itemText(i)
        measure_code = wl_measure_utils.to_measure_code(main, 'bayes_factor', measure_text)

        if not main.settings_global['measures_bayes_factor'][measure_code][extraction_type]:
            combo_box_measure_bayes_factor.removeItem(i)

    for i in reversed(range(combo_box_measure_effect_size.count())):
        measure_text = combo_box_measure_effect_size.itemText(i)
        measure_code = wl_measure_utils.to_measure_code(main, 'effect_size', measure_text)

        if not main.settings_global['measures_effect_size'][measure_code][extraction_type]:
            combo_box_measure_effect_size.removeItem(i)

    return (
        label_test_statistical_significance, combo_box_test_statistical_significance,
        label_measure_bayes_factor, combo_box_measure_bayes_factor,
        label_measure_effect_size, combo_box_measure_effect_size
    )

# Table Settings
def wl_widgets_table_settings(parent, tables):
    def show_pct_data_changed():
        for table in tables:
            table.table_settings['show_pct_data'] = checkbox_show_pct_data.isChecked()

            table.toggle_pct_data()

    def show_cum_data_changed():
        for table in tables:
            table.table_settings['show_cum_data'] = checkbox_show_cum_data.isChecked()

            if not table.is_empty():
                table.toggle_cum_data()

    def show_breakdown_file_changed():
        for table in tables:
            table.table_settings['show_breakdown_file'] = checkbox_show_breakdown_file.isChecked()

            table.toggle_breakdown_file()

    checkbox_show_pct_data = QCheckBox(_tr('wl_widgets', 'Show percentage data'), parent)
    checkbox_show_cum_data = QCheckBox(_tr('wl_widgets', 'Show cumulative data'), parent)
    checkbox_show_breakdown_file = QCheckBox(_tr('wl_widgets', 'Show breakdown by file'), parent)

    checkbox_show_pct_data.stateChanged.connect(show_pct_data_changed)
    checkbox_show_cum_data.stateChanged.connect(show_cum_data_changed)
    checkbox_show_breakdown_file.stateChanged.connect(show_breakdown_file_changed)

    show_pct_data_changed()
    show_cum_data_changed()
    show_breakdown_file_changed()

    return (
        checkbox_show_pct_data,
        checkbox_show_cum_data,
        checkbox_show_breakdown_file
    )

def wl_widgets_table_settings_span_position(parent, tables):
    def show_pct_data_changed():
        for table in tables:
            table.table_settings['show_pct_data'] = checkbox_show_pct_data.isChecked()

            table.toggle_pct_data_span_position()

    def show_cum_data_changed():
        for table in tables:
            table.table_settings['show_cum_data'] = checkbox_show_cum_data.isChecked()

            if not table.is_empty():
                table.toggle_cum_data()

    def show_breakdown_span_position_changed():
        for table in tables:
            table.table_settings['show_breakdown_span_position'] = checkbox_show_breakdown_span_position.isChecked()

            table.toggle_breakdown_span_position()

    def show_breakdown_file_changed():
        for table in tables:
            table.table_settings['show_breakdown_file'] = checkbox_show_breakdown_file.isChecked()

            table.toggle_breakdown_file_span_position()

    checkbox_show_pct_data = QCheckBox(_tr('wl_widgets', 'Show percentage data'), parent)
    checkbox_show_cum_data = QCheckBox(_tr('wl_widgets', 'Show cumulative data'), parent)
    checkbox_show_breakdown_span_position = QCheckBox(_tr('wl_widgets', 'Show breakdown by span position'), parent)
    checkbox_show_breakdown_file = QCheckBox(_tr('wl_widgets', 'Show breakdown by file'), parent)

    checkbox_show_pct_data.stateChanged.connect(show_pct_data_changed)
    checkbox_show_cum_data.stateChanged.connect(show_cum_data_changed)
    checkbox_show_breakdown_span_position.stateChanged.connect(show_breakdown_span_position_changed)
    checkbox_show_breakdown_file.stateChanged.connect(show_breakdown_file_changed)

    show_pct_data_changed()
    show_cum_data_changed()
    show_breakdown_span_position_changed()
    show_breakdown_file_changed()

    return (
        checkbox_show_pct_data,
        checkbox_show_cum_data,
        checkbox_show_breakdown_span_position, checkbox_show_breakdown_file
    )

# Figure Settings
class Wl_Combo_Box_File_Fig_Settings(wl_boxes.Wl_Combo_Box_File):
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
        if combo_box_graph_type.currentText() == _tr('wl_widgets', 'Line chart'):
            combo_box_sort_by_file.setEnabled(True)

            use_data_changed()
        else:
            combo_box_sort_by_file.setEnabled(True)
            checkbox_use_pct.setEnabled(False)
            checkbox_use_cumulative.setEnabled(False)

    def use_data_changed():
        if combo_box_graph_type.currentText() == _tr('wl_widgets', 'Line chart'):
            if combo_box_use_data.currentText() == _tr('wl_widgets', 'Frequency'):
                checkbox_use_pct.setEnabled(True)
                checkbox_use_cumulative.setEnabled(True)
            else:
                checkbox_use_pct.setEnabled(False)
                checkbox_use_cumulative.setEnabled(False)

    def measures_changed_wordlist_generator():
        settings_global = main.settings_global
        settings_default = main.settings_default[tab]
        settings_custom = main.settings_custom[tab]

        use_data_old = settings_custom['fig_settings']['use_data']

        combo_box_use_data.clear()

        combo_box_use_data.addItem(_tr('wl_widgets', 'Frequency'))

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
        settings_global = main.settings_global
        settings_default = main.settings_default[tab]
        settings_custom = main.settings_custom[tab]

        use_data_old = settings_custom['fig_settings']['use_data']

        combo_box_use_data.clear()

        for i in range(settings_custom['generation_settings']['window_left'], settings_custom['generation_settings']['window_right'] + 1):
            if i < 0:
                combo_box_use_data.addItem(_tr('wl_widgets', 'L') + str(-i))
            elif i > 0:
                combo_box_use_data.addItem(_tr('wl_widgets', 'R') + str(i))

        combo_box_use_data.addItem(_tr('wl_widgets', 'Frequency'))

        text_test_statistical_significance = settings_custom['generation_settings']['test_statistical_significance']
        text_measure_bayes_factor = settings_custom['generation_settings']['measure_bayes_factor']
        text_measure_effect_size = settings_custom['generation_settings']['measure_effect_size']

        test_statistical_significance = settings_global['tests_statistical_significance'][text_test_statistical_significance]
        measure_bayes_factor = settings_global['measures_bayes_factor'][text_measure_bayes_factor]
        measure_effect_size = settings_global['measures_effect_size'][text_measure_effect_size]

        if test_statistical_significance['func']:
            if test_statistical_significance['col_text']:
                combo_box_use_data.addItem(test_statistical_significance['col_text'])

            combo_box_use_data.addItem(_tr('wl_widgets', 'p-value'))

        if measure_bayes_factor['func']:
            combo_box_use_data.addItem(_tr('wl_widgets', 'Bayes factor'))

        if measure_effect_size['func']:
            combo_box_use_data.addItem(measure_effect_size['col_text'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(settings_default['fig_settings']['use_data'])

    def measures_changed_keyword_extractor():
        settings_global = main.settings_global
        settings_default = main.settings_default[tab]
        settings_custom = main.settings_custom[tab]

        use_data_old = settings_custom['fig_settings']['use_data']

        combo_box_use_data.clear()

        combo_box_use_data.addItem(_tr('wl_widgets', 'Frequency'))

        text_test_statistical_significance = settings_custom['generation_settings']['test_statistical_significance']
        text_measure_bayes_factor = settings_custom['generation_settings']['measure_bayes_factor']
        text_measure_effect_size = settings_custom['generation_settings']['measure_effect_size']

        test_statistical_significance = settings_global['tests_statistical_significance'][text_test_statistical_significance]
        measure_bayes_factor = settings_global['measures_bayes_factor'][text_measure_bayes_factor]
        measure_effect_size = settings_global['measures_effect_size'][text_measure_effect_size]

        if test_statistical_significance['func']:
            if test_statistical_significance['col_text']:
                combo_box_use_data.addItem(test_statistical_significance['col_text'])

            combo_box_use_data.addItem(_tr('wl_widgets', 'p-value'))

        if measure_bayes_factor['func']:
            combo_box_use_data.addItem(_tr('wl_widgets', 'Bayes factor'))

        if measure_effect_size['func']:
            combo_box_use_data.addItem(measure_effect_size['col_text'])

        if combo_box_use_data.findText(use_data_old) > -1:
            combo_box_use_data.setCurrentText(use_data_old)
        else:
            combo_box_use_data.setCurrentText(settings_default['fig_settings']['use_data'])

    main = wl_misc.find_wl_main(parent)

    label_graph_type = QLabel(_tr('wl_widgets', 'Graph type:'), parent)
    combo_box_graph_type = wl_boxes.Wl_Combo_Box(parent)
    label_sort_by_file = QLabel(_tr('wl_widgets', 'Sort by file:'), parent)
    combo_box_sort_by_file = Wl_Combo_Box_File_Fig_Settings(parent)
    label_use_data = QLabel(_tr('wl_widgets', 'Use data:'), parent)
    combo_box_use_data = wl_boxes.Wl_Combo_Box(parent)
    checkbox_use_pct = QCheckBox(_tr('wl_widgets', 'Use percentage data'), parent)
    checkbox_use_cumulative = QCheckBox(_tr('wl_widgets', 'Use cumulative data'), parent)

    combo_box_graph_type.addItems([
        _tr('wl_widgets', 'Line chart'),
        _tr('wl_widgets', 'Word cloud')
    ])

    # Network Graph
    if tab in ['collocation_extractor', 'colligation_extractor']:
        combo_box_graph_type.addItem(_tr('wl_widgets', 'Network graph'))

    if tab in ['wordlist_generator', 'ngram_generator', 'collocation_extractor', 'colligation_extractor', 'keyword_extractor']:
        match tab:
            case 'wordlist_generator' | 'ngram_generator':
                combo_box_use_data.measures_changed = measures_changed_wordlist_generator
            case 'collocation_extractor' | 'colligation_extractor':
                combo_box_use_data.measures_changed = measures_changed_collocation_extractor
            case 'keyword_extractor':
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

def wl_widgets_fig_settings_dependency_parsing(parent):
    def show_pos_tags_changed():
        if checkbox_show_pos_tags.isChecked():
            combo_box_show_pos_tags.setEnabled(True)
            checkbox_show_lemmas.setEnabled(True)
        else:
            combo_box_show_pos_tags.setEnabled(False)
            checkbox_show_lemmas.setEnabled(False)

    checkbox_show_pos_tags = QCheckBox(_tr('wl_widgets', 'Show'), parent)
    combo_box_show_pos_tags = wl_boxes.Wl_Combo_Box(parent)
    label_show_pos_tags = QLabel(_tr('wl_widgets', 'part-of-speech tags'), parent)
    checkbox_show_lemmas = QCheckBox(_tr('wl_widgets', 'Show lemmas'), parent)
    checkbox_collapse_punc_marks = QCheckBox(_tr('wl_widgets', 'Collapse punctuation marks'), parent)
    checkbox_compact_mode = QCheckBox(_tr('wl_widgets', 'Compact mode'), parent)
    checkbox_show_in_separate_tab = QCheckBox(_tr('wl_widgets', 'Show each sentence in a separate tab'), parent)

    combo_box_show_pos_tags.addItems([
        _tr('wl_widgets', 'coarse-grained'),
        _tr('wl_widgets', 'fine-grained')
    ])

    checkbox_show_pos_tags.stateChanged.connect(show_pos_tags_changed)

    return (
        checkbox_show_pos_tags, combo_box_show_pos_tags, label_show_pos_tags,
        checkbox_show_lemmas,
        checkbox_collapse_punc_marks,
        checkbox_compact_mode,
        checkbox_show_in_separate_tab
    )

# Settings -> Measures
def wl_widgets_num_sub_sections(parent):
    label_divide_each_file_into = QLabel(_tr('wl_widgets', 'Divide each file into'), parent)
    spin_box_num_sub_sections = wl_boxes.Wl_Spin_Box(parent)
    label_sub_sections = QLabel(_tr('wl_widgets', 'sub-sections'), parent)

    spin_box_num_sub_sections.setRange(2, 1000)

    return label_divide_each_file_into, spin_box_num_sub_sections, label_sub_sections

def wl_widgets_use_data_freq(parent):
    label_use_data = QLabel(_tr('wl_widgets', 'Use data:'), parent)
    combo_box_use_data = wl_boxes.Wl_Combo_Box(parent)

    combo_box_use_data.addItems([
        _tr('wl_widgets', 'Absolute frequency'),
        _tr('wl_widgets', 'Relative frequency')
    ])

    return label_use_data, combo_box_use_data

def wl_widgets_direction(parent):
    label_direction = QLabel(_tr('wl_widgets', 'Direction:'), parent)
    combo_box_direction = wl_boxes.Wl_Combo_Box(parent)

    combo_box_direction.addItems([
        _tr('wl_widgets', 'Two-tailed'),
        _tr('wl_widgets', 'Left-tailed'),
        _tr('wl_widgets', 'Right-tailed')
    ])

    return label_direction, combo_box_direction
