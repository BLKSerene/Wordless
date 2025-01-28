# ----------------------------------------------------------------------
# Wordless: Work Area - Concordancer
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

# pylint: disable=broad-exception-caught

import bisect
import copy
import traceback

import matplotlib
import matplotlib.pyplot
import numpy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QLabel,
    QLineEdit,
    QGroupBox,
    QStackedWidget
)

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_figs import wl_figs
from wordless.wl_nlp import (
    wl_matching,
    wl_nlp_utils,
    wl_texts,
    wl_token_processing,
    wl_sentiment_analysis
)
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import (
    wl_boxes,
    wl_labels,
    wl_layouts,
    wl_tables,
    wl_widgets
)

_tr = QCoreApplication.translate

class Wrapper_Concordancer(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.tab = 'concordancer'

        # Table
        self.table_concordancer = Wl_Table_Concordancer(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_concordancer.label_num_results, 0, 0)
        layout_results.addWidget(self.table_concordancer.button_results_sort, 0, 2)
        layout_results.addWidget(self.table_concordancer.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_exp_selected_cells, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_exp_all_cells, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_clr_table, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_punc_marks,

            self.checkbox_assign_pos_tags,
            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings_concordancer(self)

        self.checkbox_punc_marks.stateChanged.connect(self.token_settings_changed)

        self.checkbox_assign_pos_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_punc_marks, 0, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_assign_pos_tags, 2, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 3, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 3, 1)

        # Search Settings
        self.group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

        (
            self.label_search_term,
            self.checkbox_multi_search_mode,

            self.stacked_widget_search_term,
            self.line_edit_search_term,
            self.list_search_terms,
            self.label_delimiter,

            self.checkbox_match_case,
            self.checkbox_match_whole_words,
            self.checkbox_match_inflected_forms,
            self.checkbox_use_regex,
            self.checkbox_match_without_tags,
            self.checkbox_match_tags
        ) = wl_widgets.wl_widgets_search_settings(self, tab = self.tab)

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(self, tab = self.tab)

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_concordancer.button_generate_table.click)
        self.list_search_terms.model().dataChanged.connect(self.search_settings_changed)

        self.checkbox_match_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_without_tags.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        layout_context_settings = wl_layouts.Wl_Layout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_delimiter, 2, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_match_case, 3, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_words, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_without_tags, 7, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 9, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 10, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'), self)

        self.checkbox_calc_sentiment_scores = QCheckBox(self.tr('Calculate sentiment scores'), self)

        self.label_context_len_left = QLabel(self.tr('Context length (left):'), self)
        self.stacked_widget_context_len_left = QStackedWidget(self)
        self.spin_box_context_len_left_char = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_left_token = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_left_sentence_seg = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_left_sentence = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_left_para = wl_boxes.Wl_Spin_Box(self)
        self.label_context_len_right = QLabel(self.tr('Context length (right):'), self)
        self.stacked_widget_context_len_right = QStackedWidget(self)
        self.spin_box_context_len_right_char = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_right_token = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_right_sentence_seg = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_right_sentence = wl_boxes.Wl_Spin_Box(self)
        self.spin_box_context_len_right_para = wl_boxes.Wl_Spin_Box(self)
        self.label_context_len_unit = QLabel(self.tr('Unit of context length:'), self)
        self.combo_box_context_len_unit = wl_boxes.Wl_Combo_Box(self)

        self.stacked_widget_context_len_left.addWidget(self.spin_box_context_len_left_char)
        self.stacked_widget_context_len_left.addWidget(self.spin_box_context_len_left_token)
        self.stacked_widget_context_len_left.addWidget(self.spin_box_context_len_left_sentence_seg)
        self.stacked_widget_context_len_left.addWidget(self.spin_box_context_len_left_sentence)
        self.stacked_widget_context_len_left.addWidget(self.spin_box_context_len_left_para)
        self.stacked_widget_context_len_right.addWidget(self.spin_box_context_len_right_char)
        self.stacked_widget_context_len_right.addWidget(self.spin_box_context_len_right_token)
        self.stacked_widget_context_len_right.addWidget(self.spin_box_context_len_right_sentence_seg)
        self.stacked_widget_context_len_right.addWidget(self.spin_box_context_len_right_sentence)
        self.stacked_widget_context_len_right.addWidget(self.spin_box_context_len_right_para)

        self.combo_box_context_len_unit.addItems([
            self.tr('Character'),
            self.tr('Token'),
            self.tr('Sentence segment'),
            self.tr('Sentence'),
            self.tr('Paragraph')
        ])

        self.spin_box_context_len_left_char.setRange(0, 100000)
        self.spin_box_context_len_left_token.setRange(0, 10000)
        self.spin_box_context_len_left_sentence_seg.setRange(0, 1000)
        self.spin_box_context_len_left_sentence.setRange(0, 1000)
        self.spin_box_context_len_left_para.setRange(0, 100)
        self.spin_box_context_len_right_char.setRange(0, 100000)
        self.spin_box_context_len_right_token.setRange(0, 10000)
        self.spin_box_context_len_right_sentence_seg.setRange(0, 1000)
        self.spin_box_context_len_right_sentence.setRange(0, 1000)
        self.spin_box_context_len_right_para.setRange(0, 100)

        self.checkbox_calc_sentiment_scores.stateChanged.connect(self.generation_settings_changed)

        self.spin_box_context_len_left_char.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_left_token.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_left_sentence_seg.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_left_sentence.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_left_para.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_right_char.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_right_token.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_right_sentence_seg.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_right_sentence.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_context_len_right_para.valueChanged.connect(self.generation_settings_changed)
        self.combo_box_context_len_unit.currentTextChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.checkbox_calc_sentiment_scores, 0, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(self.label_context_len_left, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.stacked_widget_context_len_left, 1, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_context_len_right, 2, 0)
        self.group_box_generation_settings.layout().addWidget(self.stacked_widget_context_len_right, 2, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_context_len_unit, 3, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_context_len_unit, 3, 1)

        self.group_box_generation_settings.layout().setColumnStretch(1, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_concordancer]
        )

        self.checkbox_show_cum_data.hide()
        self.checkbox_show_breakdown_file.hide()

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        self.label_sort_results_by = QLabel(self.tr('Sort results by:'), self)
        self.combo_box_sort_results_by = wl_boxes.Wl_Combo_Box(self)

        self.combo_box_sort_results_by.addItems([
            self.tr('File'),
            self.tr('Search term')
        ])

        self.combo_box_sort_results_by.currentTextChanged.connect(self.fig_settings_changed)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addWidget(self.label_sort_results_by, 0, 0)
        self.group_box_fig_settings.layout().addWidget(self.combo_box_sort_results_by, 0, 1)

        self.group_box_fig_settings.layout().setColumnStretch(1, 1)

        # Zapping Settings
        self.group_box_zapping_settings = QGroupBox(self.tr('Zapping Settings'), self)

        self.label_replace_keywords_with = QLabel(self.tr('Replace keywords with'), self)
        self.spin_box_replace_keywords_with = wl_boxes.Wl_Spin_Box(self)
        self.line_edit_replace_keywords_with = QLineEdit('_', self)
        self.checkbox_add_line_nums = QCheckBox(self.tr('Add line numbers'), self)
        self.checkbox_randomize_outputs = QCheckBox(self.tr('Randomize outputs'), self)

        self.group_box_zapping_settings.setCheckable(True)
        self.spin_box_replace_keywords_with.setRange(1, 100)

        self.group_box_zapping_settings.clicked.connect(self.zapping_settings_changed)
        self.spin_box_replace_keywords_with.valueChanged.connect(self.zapping_settings_changed)
        self.line_edit_replace_keywords_with.textChanged.connect(self.zapping_settings_changed)
        self.checkbox_add_line_nums.clicked.connect(self.zapping_settings_changed)
        self.checkbox_randomize_outputs.clicked.connect(self.zapping_settings_changed)

        self.group_box_zapping_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_zapping_settings.layout().addWidget(self.label_replace_keywords_with, 0, 0)
        self.group_box_zapping_settings.layout().addWidget(self.spin_box_replace_keywords_with, 0, 1)
        self.group_box_zapping_settings.layout().addWidget(self.line_edit_replace_keywords_with, 0, 2)
        self.group_box_zapping_settings.layout().addWidget(self.checkbox_add_line_nums, 1, 0, 1, 3)
        self.group_box_zapping_settings.layout().addWidget(self.checkbox_randomize_outputs, 2, 0, 1, 3)

        self.group_box_fig_settings.layout().setColumnStretch(3, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 4, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_zapping_settings, 5, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['concordancer'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['concordancer'])

        # Token Settings
        self.checkbox_punc_marks.setChecked(settings['token_settings']['punc_marks'])

        self.checkbox_assign_pos_tags.setChecked(settings['token_settings']['assign_pos_tags'])
        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_settings']['search_term'])
            self.list_search_terms.load_items(settings['search_settings']['search_terms'])

        self.checkbox_match_case.setChecked(settings['search_settings']['match_case'])
        self.checkbox_match_whole_words.setChecked(settings['search_settings']['match_whole_words'])
        self.checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        self.checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])
        self.checkbox_match_without_tags.setChecked(settings['search_settings']['match_without_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        # Context Settings
        if defaults:
            self.main.wl_context_settings_concordancer.load_settings(defaults = True)

        # Generation Settings
        self.checkbox_calc_sentiment_scores.setChecked(settings['generation_settings']['calc_sentiment_scores'])

        self.spin_box_context_len_left_char.setValue(settings['generation_settings']['context_len_left_char'])
        self.spin_box_context_len_left_token.setValue(settings['generation_settings']['context_len_left_token'])
        self.spin_box_context_len_left_sentence_seg.setValue(settings['generation_settings']['context_len_left_sentence_seg'])
        self.spin_box_context_len_left_sentence.setValue(settings['generation_settings']['context_len_left_sentence'])
        self.spin_box_context_len_left_para.setValue(settings['generation_settings']['context_len_left_para'])
        self.spin_box_context_len_right_char.setValue(settings['generation_settings']['context_len_right_char'])
        self.spin_box_context_len_right_token.setValue(settings['generation_settings']['context_len_right_token'])
        self.spin_box_context_len_right_sentence_seg.setValue(settings['generation_settings']['context_len_right_sentence_seg'])
        self.spin_box_context_len_right_sentence.setValue(settings['generation_settings']['context_len_right_sentence'])
        self.spin_box_context_len_right_para.setValue(settings['generation_settings']['context_len_right_para'])
        self.combo_box_context_len_unit.setCurrentText(settings['generation_settings']['context_len_unit'])

        # Table Settings
        self.checkbox_show_pct_data.setChecked(settings['table_settings']['show_pct_data'])

        # Figure Settings
        self.combo_box_sort_results_by.setCurrentText(settings['fig_settings']['sort_results_by'])

        # Zapping Settings
        self.group_box_zapping_settings.setChecked(settings['zapping_settings']['zapping'])
        self.spin_box_replace_keywords_with.setValue(settings['zapping_settings']['replace_keywords_with'])
        self.line_edit_replace_keywords_with.setText(settings['zapping_settings']['placeholder'])
        self.checkbox_add_line_nums.setChecked(settings['zapping_settings']['add_line_nums'])
        self.checkbox_randomize_outputs.setChecked(settings['zapping_settings']['randomize_outputs'])

        self.token_settings_changed()
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()
        self.zapping_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['token_settings']

        settings['punc_marks'] = self.checkbox_punc_marks.isChecked()

        settings['assign_pos_tags'] = self.checkbox_assign_pos_tags.isChecked()
        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        self.checkbox_match_tags.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.model().stringList()

        settings['match_case'] = self.checkbox_match_case.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()
        settings['match_without_tags'] = self.checkbox_match_without_tags.isChecked()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['generation_settings']

        settings['calc_sentiment_scores'] = self.checkbox_calc_sentiment_scores.isChecked()

        settings['context_len_left_char'] = self.spin_box_context_len_left_char.value()
        settings['context_len_left_token'] = self.spin_box_context_len_left_token.value()
        settings['context_len_left_sentence_seg'] = self.spin_box_context_len_left_sentence_seg.value()
        settings['context_len_left_sentence'] = self.spin_box_context_len_left_sentence.value()
        settings['context_len_left_para'] = self.spin_box_context_len_left_para.value()
        settings['context_len_right_char'] = self.spin_box_context_len_right_char.value()
        settings['context_len_right_token'] = self.spin_box_context_len_right_token.value()
        settings['context_len_right_sentence_seg'] = self.spin_box_context_len_right_sentence_seg.value()
        settings['context_len_right_sentence'] = self.spin_box_context_len_right_sentence.value()
        settings['context_len_right_para'] = self.spin_box_context_len_right_para.value()
        settings['context_len_unit'] = self.combo_box_context_len_unit.currentText()

        # Unit of context length
        if settings['context_len_unit'] == self.tr('Character'):
            self.stacked_widget_context_len_left.setCurrentIndex(0)
            self.stacked_widget_context_len_right.setCurrentIndex(0)
        elif settings['context_len_unit'] == self.tr('Token'):
            self.stacked_widget_context_len_left.setCurrentIndex(1)
            self.stacked_widget_context_len_right.setCurrentIndex(1)
        elif settings['context_len_unit'] == self.tr('Sentence segment'):
            self.stacked_widget_context_len_left.setCurrentIndex(2)
            self.stacked_widget_context_len_right.setCurrentIndex(2)
        elif settings['context_len_unit'] == self.tr('Sentence'):
            self.stacked_widget_context_len_left.setCurrentIndex(3)
            self.stacked_widget_context_len_right.setCurrentIndex(3)
        elif settings['context_len_unit'] == self.tr('Paragraph'):
            self.stacked_widget_context_len_left.setCurrentIndex(4)
            self.stacked_widget_context_len_right.setCurrentIndex(4)

    def table_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['fig_settings']

        settings['sort_results_by'] = self.combo_box_sort_results_by.currentText()

    def zapping_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['zapping_settings']

        settings['zapping'] = self.group_box_zapping_settings.isChecked()
        settings['replace_keywords_with'] = self.spin_box_replace_keywords_with.value()
        settings['placeholder'] = self.line_edit_replace_keywords_with.text()
        settings['add_line_nums'] = self.checkbox_add_line_nums.isChecked()
        settings['randomize_outputs'] = self.checkbox_randomize_outputs.isChecked()

class Wl_Table_Concordancer(wl_tables.Wl_Table_Data_Sort_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'concordancer',
            headers = [
                _tr('Wl_Table_Concordancer', 'Left'),
                _tr('Wl_Table_Concordancer', 'Node'),
                _tr('Wl_Table_Concordancer', 'Right'),
                _tr('Wl_Table_Concordancer', 'Token No.'),
                _tr('Wl_Table_Concordancer', 'Token No. %'),
                _tr('Wl_Table_Concordancer', 'Sentence Segment No.'),
                _tr('Wl_Table_Concordancer', 'Sentence Segment No. %'),
                _tr('Wl_Table_Concordancer', 'Sentence No.'),
                _tr('Wl_Table_Concordancer', 'Sentence No. %'),
                _tr('Wl_Table_Concordancer', 'Paragraph No.'),
                _tr('Wl_Table_Concordancer', 'Paragraph No. %'),
                _tr('Wl_Table_Concordancer', 'File')
            ],
            headers_int = [
                _tr('Wl_Table_Concordancer', 'Token No.'),
                _tr('Wl_Table_Concordancer', 'Sentence Segment No.'),
                _tr('Wl_Table_Concordancer', 'Sentence No.'),
                _tr('Wl_Table_Concordancer', 'Paragraph No.')
            ],
            headers_pct = [
                _tr('Wl_Table_Concordancer', 'Token No. %'),
                _tr('Wl_Table_Concordancer', 'Sentence Segment No. %'),
                _tr('Wl_Table_Concordancer', 'Sentence No. %'),
                _tr('Wl_Table_Concordancer', 'Paragraph No. %')
            ]
        )

    @wl_misc.log_time
    def generate_table(self):
        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['concordancer']['search_settings']
        ):
            if self.main.settings_custom['concordancer']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ['pos_taggers'])
            else:
                nlp_support_ok = True

            if nlp_support_ok:
                worker_concordancer_table = Wl_Worker_Concordancer_Table(
                    self.main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                    update_gui = self.update_gui_table
                )

                wl_threading.Wl_Thread(worker_concordancer_table).start_worker()

    def update_gui_table(self, err_msg, concordance_lines):
        if wl_checks_work_area.check_results(self.main, err_msg, concordance_lines):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                settings = self.settings['concordancer']

                self.clr_table(0)
                self.model().setRowCount(len(concordance_lines))

                # Insert columns
                if settings['generation_settings']['calc_sentiment_scores']:
                    self.ins_header_hor(
                        3,
                        self.tr('Sentiment score'),
                        is_float = True
                    )

                self.disable_updates()

                node_color = self.main.settings_custom['tables']['concordancer']['sorting_settings']['highlight_colors']['lvl_1']

                for i, concordance_line in enumerate(concordance_lines):
                    left_tokens_raw, left_tokens_search = concordance_line[0]
                    node_tokens_raw, node_tokens_search = concordance_line[1]
                    right_tokens_raw, right_tokens_search = concordance_line[2]

                    sentiment = concordance_line[3]
                    no_token, len_tokens = concordance_line[4]
                    no_sentence_seg, len_sentence_segs = concordance_line[5]
                    no_sentence, len_sentences = concordance_line[6]
                    no_para, len_paras = concordance_line[7]
                    file_name = concordance_line[8]

                    # Left
                    self.setIndexWidget(
                        self.model().index(i, 0),
                        wl_labels.Wl_Label_Html(' '.join(left_tokens_raw), self.main)
                    )
                    self.indexWidget(self.model().index(i, 0)).setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    self.indexWidget(self.model().index(i, 0)).tokens_raw = left_tokens_raw
                    self.indexWidget(self.model().index(i, 0)).tokens_search = left_tokens_search

                    # Node
                    label_node = wl_labels.Wl_Label_Html(
                        f'''
                            <span style="color: {node_color}; font-weight: bold;">
                                &nbsp;{' '.join(node_tokens_raw)}&nbsp;
                            </span>
                        ''',
                        self.main
                    )

                    self.setIndexWidget(self.model().index(i, 1), label_node)
                    self.indexWidget(self.model().index(i, 1)).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                    self.indexWidget(self.model().index(i, 1)).tokens_raw = node_tokens_raw
                    self.indexWidget(self.model().index(i, 1)).tokens_search = node_tokens_search

                    # Right
                    self.setIndexWidget(
                        self.model().index(i, 2),
                        wl_labels.Wl_Label_Html(' '.join(right_tokens_raw), self.main)
                    )

                    self.indexWidget(self.model().index(i, 2)).tokens_raw = right_tokens_raw
                    self.indexWidget(self.model().index(i, 2)).tokens_search = right_tokens_search

                    # Sentiment
                    if settings['generation_settings']['calc_sentiment_scores']:
                        if not isinstance(sentiment, str):
                            self.set_item_num(i, 3, sentiment)
                        # No language support
                        else:
                            self.set_item_err(i, 3, text = sentiment, alignment_hor = 'right')

                        i_token_no = 4
                    else:
                        i_token_no = 3

                    # Token No.
                    self.set_item_num(i, i_token_no, no_token)
                    self.set_item_num(i, i_token_no + 1, no_token, len_tokens)
                    # Sentence Segment No.
                    self.set_item_num(i, i_token_no + 2, no_sentence_seg)
                    self.set_item_num(i, i_token_no + 3, no_sentence_seg, len_sentence_segs)
                    # Sentence No.
                    self.set_item_num(i, i_token_no + 4, no_sentence)
                    self.set_item_num(i, i_token_no + 5, no_sentence, len_sentences)
                    # Paragraph No.
                    self.set_item_num(i, i_token_no + 6, no_para)
                    self.set_item_num(i, i_token_no + 7, no_para, len_paras)

                    # File
                    self.model().setItem(i, i_token_no + 8, wl_tables.Wl_Table_Item(file_name))

                self.enable_updates()

                self.toggle_pct_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

    @wl_misc.log_time
    def generate_fig(self):
        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['concordancer']['search_settings']
        ):
            if self.main.settings_custom['concordancer']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ['pos_taggers'])
            else:
                nlp_support_ok = True

            if nlp_support_ok:
                self.worker_concordancer_fig = Wl_Worker_Concordancer_Fig(
                    self.main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                    update_gui = self.update_gui_fig
                )

                wl_threading.Wl_Thread(self.worker_concordancer_fig).start_worker()

    def update_gui_fig(self, err_msg, points, labels):
        if wl_checks_work_area.check_results(self.main, err_msg, points):
            try:
                x_ticks = labels[0]
                x_tick_labels = labels[1]
                y_ticks = labels[2]
                y_tick_labels = labels[3]
                y_max = labels[4]

                points = numpy.array(points)
                settings = self.main.settings_custom['concordancer']

                if settings['fig_settings']['sort_results_by'] == self.tr('File'):
                    matplotlib.pyplot.plot(
                        points[:, 0],
                        points[:, 1],
                        'b|'
                    )

                    matplotlib.pyplot.xlabel(self.tr('Search Term'))
                    matplotlib.pyplot.xticks(x_ticks, x_tick_labels, color = 'r', rotation = 90)

                    matplotlib.pyplot.ylabel(self.tr('File'))
                    matplotlib.pyplot.yticks(y_ticks, y_tick_labels)
                    matplotlib.pyplot.ylim(-1, y_max)
                elif settings['fig_settings']['sort_results_by'] == self.tr('Search term'):
                    matplotlib.pyplot.plot(
                        points[:, 0],
                        points[:, 1],
                        'b|'
                    )

                    matplotlib.pyplot.xlabel(self.tr('File'))
                    matplotlib.pyplot.xticks(x_ticks, x_tick_labels, rotation = 90)

                    matplotlib.pyplot.ylabel(self.tr('Search Term'))
                    matplotlib.pyplot.yticks(y_ticks, y_tick_labels, color = 'r')
                    matplotlib.pyplot.ylim(-1, y_max)

                matplotlib.pyplot.title(self.tr('Dispersion Plot'))
                matplotlib.pyplot.grid(True, which = 'major', axis = 'x', linestyle = 'dotted')

                # Hide the progress dialog early so that the main window will not obscure the generated figure
                self.worker_concordancer_fig.dialog_progress.accept()
                wl_figs.show_fig()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_fig(self.main, err_msg)

class Wl_Worker_Concordancer_Table(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        concordance_lines = []

        try:
            settings = self.main.settings_custom['concordancer']

            for file in self.main.wl_file_area.get_selected_files():
                concordance_lines_file = []

                text = wl_token_processing.wl_process_tokens_concordancer(
                    self.main, file['text'],
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                tokens = text.get_tokens_flat()
                (
                    offsets_paras,
                    offsets_sentences,
                    offsets_sentence_segs
                ) = text.get_offsets()

                search_terms = wl_matching.match_search_terms_ngrams(
                    self.main, tokens,
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                (
                    search_terms_incl,
                    search_terms_excl
                ) = wl_matching.match_search_terms_context(
                    self.main, tokens,
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    context_settings = settings['search_settings']['context_settings']
                )

                if search_terms:
                    len_search_term_min = min((len(search_term) for search_term in search_terms))
                    len_search_term_max = max((len(search_term) for search_term in search_terms))
                else:
                    len_search_term_min = 0
                    len_search_term_max = 0

                len_paras = len(offsets_paras)
                len_sentences = len(offsets_sentences)
                len_sentence_segs = len(offsets_sentence_segs)

                sentiment_inputs = []

                for len_search_term in range(len_search_term_min, len_search_term_max + 1):
                    for i, ngram in enumerate(wl_nlp_utils.ngrams(tokens, len_search_term)):
                        if (
                            ngram in search_terms
                            and wl_matching.check_context(
                                i, tokens,
                                context_settings = settings['search_settings']['context_settings'],
                                search_terms_incl = search_terms_incl,
                                search_terms_excl = search_terms_excl
                            )
                        ):
                            concordance_line = []

                            # No.
                            no_sentence_seg = bisect.bisect(offsets_sentence_segs, i)
                            no_sentence = bisect.bisect(offsets_sentences, i)
                            no_para = bisect.bisect(offsets_paras, i)

                            node_tokens_raw = wl_nlp_utils.escape_tokens(wl_texts.to_display_texts(
                                ngram,
                                punc_mark = True
                            ))

                            # Width Unit
                            if settings['generation_settings']['context_len_unit'] == self.tr('Character'):
                                len_context_left = 0
                                len_context_right = 0

                                left_tokens_raw = []
                                right_tokens_raw = []

                                context_len_left_char = settings['generation_settings']['context_len_left_char']
                                context_len_right_char = settings['generation_settings']['context_len_right_char']

                                while len_context_left < context_len_left_char:
                                    if i - 1 - len(left_tokens_raw) < 0:
                                        break
                                    else:
                                        token_next = tokens[i - 1 - len(left_tokens_raw)]
                                        len_token_next = len(token_next)

                                    if len_context_left + len_token_next > context_len_left_char:
                                        left_tokens_raw.insert(0, wl_texts.set_token_text(
                                            token_next,
                                            token_next[-(context_len_left_char - len_context_left):]
                                        ))
                                    else:
                                        left_tokens_raw.insert(0, token_next)

                                    len_context_left += len_token_next

                                while len_context_right < context_len_right_char:
                                    if i + len_search_term + len(right_tokens_raw) > text.num_tokens - 1:
                                        break
                                    else:
                                        token_next = tokens[i + len_search_term + len(right_tokens_raw)]
                                        len_token_next = len(token_next)

                                    if len_context_right + len_token_next > context_len_right_char:
                                        right_tokens_raw.append(wl_texts.set_token_text(
                                            token_next,
                                            token_next[: context_len_right_char - len_context_right]
                                        ))
                                    else:
                                        right_tokens_raw.append(token_next)

                                    len_context_right += len_token_next
                            elif settings['generation_settings']['context_len_unit'] == self.tr('Token'):
                                context_len_left_token = settings['generation_settings']['context_len_left_token']
                                context_len_right_token = settings['generation_settings']['context_len_right_token']

                                left_tokens_raw = tokens[max(0, i - context_len_left_token) : i]
                                right_tokens_raw = tokens[i + len_search_term : i + len_search_term + context_len_right_token]
                            else:
                                if settings['generation_settings']['context_len_unit'] == self.tr('Sentence segment'):
                                    context_len_unit = 'sentence_seg'
                                    offsets_unit = offsets_sentence_segs
                                    no_unit = no_sentence_seg
                                    len_unit = len_sentence_segs
                                elif settings['generation_settings']['context_len_unit'] == self.tr('Sentence'):
                                    context_len_unit = 'sentence'
                                    offsets_unit = offsets_sentences
                                    no_unit = no_sentence
                                    len_unit = len_sentences
                                elif settings['generation_settings']['context_len_unit'] == self.tr('Paragraph'):
                                    context_len_unit = 'para'
                                    offsets_unit = offsets_paras
                                    no_unit = no_para
                                    len_unit = len_paras

                                context_len_left = settings['generation_settings'][f'context_len_left_{context_len_unit}']
                                context_len_right = settings['generation_settings'][f'context_len_right_{context_len_unit}']

                                offset_start = offsets_unit[max(0, no_unit - 1 - context_len_left)]

                                if no_unit + context_len_right > len_unit - 1:
                                    offset_end = None
                                else:
                                    offset_end = offsets_unit[no_unit + context_len_right]

                                left_tokens_raw = tokens[offset_start:i]
                                right_tokens_raw = tokens[i + len_search_term : offset_end]

                            if settings['token_settings']['punc_marks']:
                                node_tokens_search = list(ngram)

                                # Remove empty tokens for searching in results
                                left_tokens_search = [token for token in copy.deepcopy(left_tokens_raw) if token]
                                right_tokens_search = [token for token in copy.deepcopy(right_tokens_raw) if token]
                            # Convert trailing punctuation marks, if any, to separate tokens for searching
                            else:
                                node_tokens_search = []
                                left_tokens_search = []
                                right_tokens_search = []

                                for token in list(ngram):
                                    node_tokens_search.append(token)

                                    if token.punc_mark:
                                        node_tokens_search.append(wl_texts.Wl_Token(token.punc_mark, lang = token.lang))

                                for token in copy.deepcopy(left_tokens_raw):
                                    if token:
                                        left_tokens_search.append(token)

                                        if token.punc_mark:
                                            left_tokens_search.append(wl_texts.Wl_Token(token.punc_mark, lang = token.lang))

                                for token in copy.deepcopy(right_tokens_raw):
                                    if token:
                                        right_tokens_search.append(token)

                                        if token.punc_mark:
                                            right_tokens_search.append(wl_texts.Wl_Token(token.punc_mark, lang = token.lang))

                            left_tokens_raw = wl_nlp_utils.escape_tokens(wl_texts.to_display_texts(
                                left_tokens_raw,
                                punc_mark = True
                            ))
                            right_tokens_raw = wl_nlp_utils.escape_tokens(wl_texts.to_display_texts(
                                right_tokens_raw,
                                punc_mark = True
                            ))

                            # Left
                            concordance_line.append([left_tokens_raw, left_tokens_search])
                            # Node
                            concordance_line.append([node_tokens_raw, node_tokens_search])
                            # Right
                            concordance_line.append([right_tokens_raw, right_tokens_search])

                            # Sentiment
                            if (
                                settings['generation_settings']['calc_sentiment_scores']
                                and text.lang in self.main.settings_global['sentiment_analyzers']
                            ):
                                sentiment_inputs.append(' '.join(
                                    [*left_tokens_search, *node_tokens_search, *right_tokens_search]
                                ))

                            # Token No.
                            concordance_line.append([i + 1, text.num_tokens])
                            # Sentence Segment No.
                            concordance_line.append([no_sentence_seg, len_sentence_segs])
                            # Sentence No.
                            concordance_line.append([no_sentence, len_sentences])
                            # Paragraph No.
                            concordance_line.append([no_para, len_paras])
                            # File
                            concordance_line.append(file['name'])

                            concordance_lines_file.append(concordance_line)

                if settings['generation_settings']['calc_sentiment_scores']:
                    if sentiment_inputs:
                        sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
                            self.main,
                            inputs = sentiment_inputs,
                            lang = text.lang
                        )

                        for concordance_line, sentiment_score in zip(concordance_lines_file, sentiment_scores):
                            concordance_line.insert(3, sentiment_score)
                    else:
                        for concordance_line in concordance_lines_file:
                            concordance_line.insert(3, self.tr('No language support'))
                else:
                    for concordance_line in concordance_lines_file:
                        concordance_line.insert(3, None)

                concordance_lines.extend(concordance_lines_file)
        except Exception:
            err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(err_msg, concordance_lines)

class Wl_Worker_Concordancer_Fig(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list, list)

    def run(self):
        err_msg = ''
        points = []
        labels = []

        try:
            texts = []
            search_terms_files = []
            search_terms_total = set()
            search_terms_labels = set()

            settings = self.main.settings_custom['concordancer']
            files = sorted(self.main.wl_file_area.get_selected_files(), key = lambda item: item['name'])

            for file in files:
                text = wl_token_processing.wl_process_tokens_concordancer(
                    self.main, file['text'],
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                search_terms_file = wl_matching.match_search_terms_ngrams(
                    self.main, text.get_tokens_flat(),
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                search_terms_files.append(sorted(search_terms_file))

                for search_term in search_terms_file:
                    search_terms_total.add(search_term)
                    search_terms_labels.add(' '.join(wl_texts.to_display_texts(search_term)))

                texts.append(text)

            len_files = len(files)
            len_tokens_total = sum((text.num_tokens for text in texts))

            if settings['fig_settings']['sort_results_by'] == self.tr('File'):
                search_terms_total = sorted(search_terms_total)
                search_terms_labels = sorted(search_terms_labels)

                for i, search_term in enumerate(search_terms_total):
                    len_search_term = len(search_term)

                    x_start = len_tokens_total * i + 1
                    y_start = len_files

                    for j, text in enumerate(texts):
                        tokens = text.get_tokens_flat()

                        if search_term in search_terms_files[j]:
                            x_start_total = x_start + sum((
                                text.num_tokens
                                for k, text in enumerate(texts)
                                if k < j
                            ))

                            for k, ngram in enumerate(wl_nlp_utils.ngrams(tokens, len_search_term)):
                                if ngram == search_term:
                                    points.append([x_start + k / text.num_tokens * len_tokens_total, y_start - j])
                                    # Total
                                    points.append([x_start_total + k, 0])
            elif settings['fig_settings']['sort_results_by'] == self.tr('Search term'):
                search_terms_total = sorted(search_terms_total, reverse = True)
                search_terms_labels = sorted(search_terms_labels, reverse = True)

                for i, search_term in enumerate(search_terms_total):
                    len_search_term = len(search_term)

                    for j, text in enumerate(texts):
                        if search_term in search_terms_files[j]:
                            x_start = sum((
                                text.num_tokens
                                for k, text in enumerate(texts)
                                if k < j
                            )) + j + 2

                            for k, ngram in enumerate(wl_nlp_utils.ngrams(text.get_tokens_flat(), len_search_term)):
                                if ngram == search_term:
                                    points.append([x_start + k, i])

            if points:
                x_ticks = [0]
                x_tick_labels = ['']

                if settings['fig_settings']['sort_results_by'] == self.tr('File'):
                    len_tokens_total = sum((text.num_tokens for text in texts))

                    for i, search_term in enumerate(search_terms_total):
                        x_tick_start = len_tokens_total * i + i + 1

                        # 1/2
                        x_ticks.append(x_tick_start + len_tokens_total / 2)
                        # Divider
                        x_ticks.append(x_tick_start + len_tokens_total + 1)

                    for search_term in search_terms_labels:
                        # 1/2
                        x_tick_labels.append(search_term)
                        # Divider
                        x_tick_labels.append('')

                    labels.append(x_ticks)
                    labels.append(x_tick_labels)
                    labels.append(list(range(len(files) + 1)))
                    labels.append([self.tr('Total')] + [file['name'] for file in reversed(files)])
                    labels.append(len(files) + 1)
                elif settings['fig_settings']['sort_results_by'] == self.tr('Search term'):
                    len_search_terms_total = len(search_terms_total)

                    for i, text in enumerate(texts):
                        tokens = text.get_tokens_flat()

                        x_tick_start = sum((
                            text.num_tokens
                            for j, text in enumerate(texts)
                            if j < i
                        )) + j + 1

                        # 1/2
                        x_ticks.append(x_tick_start + text.num_tokens / 2)
                        # Divider
                        x_ticks.append(x_tick_start + text.num_tokens + 1)

                    for file in files:
                        # 1/2
                        x_tick_labels.append(file['name'])
                        # Divider
                        x_tick_labels.append('')

                    labels.append(x_ticks)
                    labels.append(x_tick_labels)
                    labels.append(list(range(len_search_terms_total)))
                    labels.append(search_terms_labels)
                    labels.append(len_search_terms_total)
        except Exception:
            err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Rendering figure...'))
        self.worker_done.emit(err_msg, points, labels)
