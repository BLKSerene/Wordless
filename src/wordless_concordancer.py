#
# Wordless: Concordancer
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
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

import matplotlib
import matplotlib.pyplot
import nltk
import numpy

from wordless_checking import wordless_checking_file
from wordless_dialogs import (wordless_dialog, wordless_dialog_misc, wordless_msg_box)
from wordless_figs import wordless_fig
from wordless_text import (wordless_matching, wordless_text, wordless_text_processing,
                           wordless_text_utils, wordless_token_processing)
from wordless_utils import wordless_misc, wordless_threading
from wordless_widgets import (wordless_box, wordless_label, wordless_layout,
                              wordless_msg, wordless_table, wordless_widgets)

class Wordless_Table_Concordancer(wordless_table.Wordless_Table_Data_Sort_Search):
    def __init__(self, parent):
        super().__init__(parent,
                         tab = 'concordancer',
                         headers = [
                             parent.tr('Left'),
                             parent.tr('Node'),
                             parent.tr('Right'),
                             parent.tr('Token No.'),
                             parent.tr('Clause No.'),
                             parent.tr('Sentence No.'),
                             parent.tr('Paragraph No.'),
                             parent.tr('File')
                         ],
                         headers_num = [
                             parent.tr('Token No.'),
                             parent.tr('Clause No.'),
                             parent.tr('Sentence No.'),
                             parent.tr('Paragraph No.')
                         ],
                         headers_pct = [
                             parent.tr('Token No.'),
                             parent.tr('Clause No.'),
                             parent.tr('Sentence No.'),
                             parent.tr('Paragraph No.')
                         ])

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_fig.clicked.connect(lambda: generate_fig(self.main))

class Wrapper_Concordancer(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.table_concordancer = Wordless_Table_Concordancer(self)

        layout_results = wordless_layout.Wordless_Layout()
        layout_results.addWidget(self.table_concordancer.label_number_results, 0, 0)
        layout_results.addWidget(self.table_concordancer.button_results_sort, 0, 2)
        layout_results.addWidget(self.table_concordancer.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_export_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_export_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_concordancer.button_clear, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (self.checkbox_puncs,

         self.token_stacked_widget_ignore_tags,
         self.token_checkbox_ignore_tags,
         self.token_checkbox_ignore_tags_tags,

         self.token_stacked_widget_ignore_tags_type,
         self.token_combo_box_ignore_tags,
         self.token_combo_box_ignore_tags_tags,

         self.label_ignore_tags,
         self.checkbox_use_tags) = wordless_widgets.wordless_widgets_token_settings_concordancer(self)

        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.token_checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.token_checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.token_combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.token_combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = wordless_layout.Wordless_Layout()
        layout_ignore_tags.addWidget(self.token_stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.token_stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        self.group_box_token_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 0, 0)

        self.group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 1, 0)

        self.group_box_token_settings.layout().addLayout(layout_ignore_tags, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 3, 0)

        # Search Settings
        self.group_box_search_settings = QGroupBox(self.tr('Search Settings'), self)

        (self.label_search_term,
         self.checkbox_multi_search_mode,

         self.stacked_widget_search_term,
         self.line_edit_search_term,
         self.list_search_terms,
         self.label_separator,

         self.checkbox_ignore_case,
         self.checkbox_match_inflected_forms,
         self.checkbox_match_whole_words,
         self.checkbox_use_regex,

         self.search_stacked_widget_ignore_tags,
         self.search_checkbox_ignore_tags,
         self.search_checkbox_ignore_tags_tags,

         self.search_stacked_widget_ignore_tags_type,
         self.search_combo_box_ignore_tags,
         self.search_combo_box_ignore_tags_tags,

         self.search_label_ignore_tags,
         self.checkbox_match_tags) = wordless_widgets.wordless_widgets_search_settings(self,
                                                                                       tab = 'concordancer')

        (self.label_context_settings,
         self.button_context_settings) = wordless_widgets.wordless_widgets_context_settings(self,
                                                                                            tab = 'concordancer')

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_concordancer.button_generate_table.click)
        self.list_search_terms.itemChanged.connect(self.search_settings_changed)

        self.checkbox_ignore_case.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_inflected_forms.stateChanged.connect(self.search_settings_changed)
        self.checkbox_match_whole_words.stateChanged.connect(self.search_settings_changed)
        self.checkbox_use_regex.stateChanged.connect(self.search_settings_changed)

        self.search_checkbox_ignore_tags.stateChanged.connect(self.search_settings_changed)
        self.search_checkbox_ignore_tags_tags.stateChanged.connect(self.search_settings_changed)
        self.search_combo_box_ignore_tags.currentTextChanged.connect(self.search_settings_changed)
        self.search_combo_box_ignore_tags_tags.currentTextChanged.connect(self.search_settings_changed)
        self.checkbox_match_tags.stateChanged.connect(self.search_settings_changed)

        layout_ignore_tags = wordless_layout.Wordless_Layout()
        layout_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.search_stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.search_label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        layout_context_settings = wordless_layout.Wordless_Layout()
        layout_context_settings.addWidget(self.label_context_settings, 0, 0)
        layout_context_settings.addWidget(self.button_context_settings, 0, 1)

        layout_context_settings.setColumnStretch(1, 1)

        self.group_box_search_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_search_settings.layout().addWidget(self.label_search_term, 0, 0)
        self.group_box_search_settings.layout().addWidget(self.checkbox_multi_search_mode, 0, 1, Qt.AlignRight)
        self.group_box_search_settings.layout().addWidget(self.stacked_widget_search_term, 1, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.label_separator, 2, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(self.checkbox_ignore_case, 3, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_inflected_forms, 4, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_whole_words, 5, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_use_regex, 6, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_ignore_tags, 7, 0, 1, 2)
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_tags, 8, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 9, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 10, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'), self)

        self.label_width_left = QLabel(self.tr('Width (Left):'), self)
        self.stacked_widget_width_left = wordless_layout.Wordless_Stacked_Widget(self)
        self.spin_box_width_left_sentence = wordless_box.Wordless_Spin_Box(self)
        self.spin_box_width_left_clause = wordless_box.Wordless_Spin_Box(self)
        self.spin_box_width_left_token = wordless_box.Wordless_Spin_Box(self)
        self.spin_box_width_left_char = wordless_box.Wordless_Spin_Box(self)
        self.label_width_right = QLabel(self.tr('Width (Right):'), self)
        self.stacked_widget_width_right = wordless_layout.Wordless_Stacked_Widget(self)
        self.spin_box_width_right_sentence = wordless_box.Wordless_Spin_Box(self)
        self.spin_box_width_right_clause = wordless_box.Wordless_Spin_Box(self)
        self.spin_box_width_right_token = wordless_box.Wordless_Spin_Box(self)
        self.spin_box_width_right_char = wordless_box.Wordless_Spin_Box(self)
        self.label_width_unit = QLabel(self.tr('Width Unit:'), self)
        self.combo_box_width_unit = wordless_box.Wordless_Combo_Box(self)

        self.label_number_lines = QLabel(self.tr('Limit number of lines in each file:'), self)
        (self.spin_box_number_lines,
         self.checkbox_number_lines) = wordless_widgets.wordless_widgets_no_limit(self)
        self.label_every_nth_line = QLabel(self.tr('Only show every nth line in each file:'), self)
        (self.spin_box_every_nth_line,
         self.checkbox_every_nth_line) = wordless_widgets.wordless_widgets_no_limit(self)

        self.stacked_widget_width_left.addWidget(self.spin_box_width_left_sentence)
        self.stacked_widget_width_left.addWidget(self.spin_box_width_left_clause)
        self.stacked_widget_width_left.addWidget(self.spin_box_width_left_token)
        self.stacked_widget_width_left.addWidget(self.spin_box_width_left_char)
        self.stacked_widget_width_right.addWidget(self.spin_box_width_right_sentence)
        self.stacked_widget_width_right.addWidget(self.spin_box_width_right_clause)
        self.stacked_widget_width_right.addWidget(self.spin_box_width_right_token)
        self.stacked_widget_width_right.addWidget(self.spin_box_width_right_char)

        self.combo_box_width_unit.addItems([
            self.tr('Sentence'),
            self.tr('Clause'),
            self.tr('Token'),
            self.tr('Character')
        ])

        self.spin_box_width_left_sentence.setRange(0, 20)
        self.spin_box_width_left_clause.setRange(0, 50)
        self.spin_box_width_left_token.setRange(0, 100)
        self.spin_box_width_left_char.setRange(0, 500)
        self.spin_box_width_right_sentence.setRange(0, 20)
        self.spin_box_width_right_clause.setRange(0, 50)
        self.spin_box_width_right_token.setRange(0, 100)
        self.spin_box_width_right_char.setRange(0, 500)

        self.spin_box_number_lines.setRange(1, 100000)
        self.spin_box_every_nth_line.setRange(2, 100000)

        self.spin_box_width_left_sentence.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_left_clause.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_left_token.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_left_char.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_right_sentence.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_right_clause.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_right_token.valueChanged.connect(self.generation_settings_changed)
        self.spin_box_width_right_char.valueChanged.connect(self.generation_settings_changed)
        self.combo_box_width_unit.currentTextChanged.connect(self.generation_settings_changed)

        self.spin_box_number_lines.valueChanged.connect(self.generation_settings_changed)
        self.checkbox_number_lines.stateChanged.connect(self.generation_settings_changed)
        self.spin_box_every_nth_line.valueChanged.connect(self.generation_settings_changed)
        self.checkbox_every_nth_line.stateChanged.connect(self.generation_settings_changed)

        layout_width = wordless_layout.Wordless_Layout()
        layout_width.addWidget(self.label_width_left, 0, 0)
        layout_width.addWidget(self.stacked_widget_width_left, 0, 1)
        layout_width.addWidget(self.label_width_right, 1, 0)
        layout_width.addWidget(self.stacked_widget_width_right, 1, 1)
        layout_width.addWidget(self.label_width_unit, 2, 0)
        layout_width.addWidget(self.combo_box_width_unit, 2, 1)

        layout_width.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_generation_settings.layout().addLayout(layout_width, 0, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 1, 0, 1, 2)

        self.group_box_generation_settings.layout().addWidget(self.label_number_lines, 2, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_number_lines, 3, 0)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_number_lines, 3, 1)
        self.group_box_generation_settings.layout().addWidget(self.label_every_nth_line, 4, 0, 1, 2)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_every_nth_line, 5, 0)
        self.group_box_generation_settings.layout().addWidget(self.checkbox_every_nth_line, 5, 1)

        self.group_box_generation_settings.layout().setColumnStretch(0, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (self.checkbox_show_pct,
         self.checkbox_show_cumulative,
         self.checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self,
                                                                                          table = self.table_concordancer)

        self.checkbox_show_cumulative.hide()
        self.checkbox_show_breakdown.hide()

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        self.label_sort_results_by = QLabel(self.tr('Sort Results by:'), self)
        self.combo_box_sort_results_by = wordless_box.Wordless_Combo_Box(self)

        self.combo_box_sort_results_by.addItems([
            self.tr('File'),
            self.tr('Search Term')
        ])

        self.combo_box_sort_results_by.currentTextChanged.connect(self.fig_settings_changed)

        self.group_box_fig_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_fig_settings.layout().addWidget(self.label_sort_results_by, 0, 0)
        self.group_box_fig_settings.layout().addWidget(self.combo_box_sort_results_by, 0, 1)

        self.group_box_fig_settings.layout().setColumnStretch(1, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 3, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 4, 0)

        self.wrapper_settings.layout().setRowStretch(5, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['concordancer'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['concordancer'])

        # Token Settings
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.token_checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.token_checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.token_combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.token_combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Search Settings
        self.checkbox_multi_search_mode.setChecked(settings['search_settings']['multi_search_mode'])

        if not defaults:
            self.line_edit_search_term.setText(settings['search_settings']['search_term'])
            self.list_search_terms.load_items(settings['search_settings']['search_terms'])

        self.checkbox_ignore_case.setChecked(settings['search_settings']['ignore_case'])
        self.checkbox_match_inflected_forms.setChecked(settings['search_settings']['match_inflected_forms'])
        self.checkbox_match_whole_words.setChecked(settings['search_settings']['match_whole_words'])
        self.checkbox_use_regex.setChecked(settings['search_settings']['use_regex'])

        self.search_checkbox_ignore_tags.setChecked(settings['search_settings']['ignore_tags'])
        self.search_checkbox_ignore_tags_tags.setChecked(settings['search_settings']['ignore_tags_tags'])
        self.search_combo_box_ignore_tags.setCurrentText(settings['search_settings']['ignore_tags_type'])
        self.search_combo_box_ignore_tags_tags.setCurrentText(settings['search_settings']['ignore_tags_type_tags'])
        self.checkbox_match_tags.setChecked(settings['search_settings']['match_tags'])

        # Context Settings
        if defaults:
            self.main.wordless_context_settings_concordancer.load_settings(defaults = True)

        # Generation Settings
        self.spin_box_width_left_sentence.setValue(settings['generation_settings']['width_left_sentence'])
        self.spin_box_width_left_clause.setValue(settings['generation_settings']['width_left_clause'])
        self.spin_box_width_left_token.setValue(settings['generation_settings']['width_left_token'])
        self.spin_box_width_left_char.setValue(settings['generation_settings']['width_left_char'])
        self.spin_box_width_right_sentence.setValue(settings['generation_settings']['width_right_sentence'])
        self.spin_box_width_right_clause.setValue(settings['generation_settings']['width_right_clause'])
        self.spin_box_width_right_token.setValue(settings['generation_settings']['width_right_token'])
        self.spin_box_width_right_char.setValue(settings['generation_settings']['width_right_char'])
        self.combo_box_width_unit.setCurrentText(settings['generation_settings']['width_unit'])

        self.spin_box_number_lines.setValue(settings['generation_settings']['number_lines'])
        self.checkbox_number_lines.setChecked(settings['generation_settings']['number_lines_no_limit'])
        self.spin_box_every_nth_line.setValue(settings['generation_settings']['every_nth_line'])
        self.checkbox_every_nth_line.setChecked(settings['generation_settings']['every_nth_line_no_limit'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])

        # Figure Settings
        self.combo_box_sort_results_by.setCurrentText(settings['fig_settings']['sort_results_by'])

        self.token_settings_changed()
        self.search_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['token_settings']

        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['ignore_tags'] = self.token_checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.token_checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.token_combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.token_combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        # Check if searching is enabled
        if self.group_box_search_settings.isChecked():
            self.checkbox_match_tags.token_settings_changed()
        else:
            self.group_box_search_settings.setChecked(True)

            self.checkbox_match_tags.token_settings_changed()

            self.group_box_search_settings.setChecked(False)
        
        self.main.wordless_context_settings_concordancer.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.get_items()

        settings['ignore_case'] = self.checkbox_ignore_case.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()

        settings['ignore_tags'] = self.search_checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.search_checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.search_combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.search_combo_box_ignore_tags_tags.currentText()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['generation_settings']

        settings['width_left_sentence'] = self.spin_box_width_left_sentence.value()
        settings['width_left_clause'] = self.spin_box_width_left_clause.value()
        settings['width_left_token'] = self.spin_box_width_left_token.value()
        settings['width_left_char'] = self.spin_box_width_left_char.value()
        settings['width_right_sentence'] = self.spin_box_width_right_sentence.value()
        settings['width_right_clause'] = self.spin_box_width_right_clause.value()
        settings['width_right_token'] = self.spin_box_width_right_token.value()
        settings['width_right_char'] = self.spin_box_width_right_char.value()
        settings['width_unit'] = self.combo_box_width_unit.currentText()

        settings['number_lines'] = self.spin_box_number_lines.value()
        settings['number_lines_no_limit'] = self.checkbox_number_lines.isChecked()
        settings['every_nth_line'] = self.spin_box_every_nth_line.value()
        settings['every_nth_line_no_limit'] = self.checkbox_every_nth_line.isChecked()

        if settings['width_unit'] == self.tr('Sentence'):
            self.stacked_widget_width_left.setCurrentIndex(0)
            self.stacked_widget_width_right.setCurrentIndex(0)
        elif settings['width_unit'] == self.tr('Clause'):
            self.stacked_widget_width_left.setCurrentIndex(1)
            self.stacked_widget_width_right.setCurrentIndex(1)
        elif settings['width_unit'] == self.tr('Token'):
            self.stacked_widget_width_left.setCurrentIndex(2)
            self.stacked_widget_width_right.setCurrentIndex(2)
        elif settings['width_unit'] == self.tr('Character'):
            self.stacked_widget_width_left.setCurrentIndex(3)
            self.stacked_widget_width_right.setCurrentIndex(3)

    def table_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['concordancer']['fig_settings']

        settings['sort_results_by'] = self.combo_box_sort_results_by.currentText()

class Wordless_Worker_Process_Data_Concordancer_Table(wordless_threading.Wordless_Worker_Process_Data):
    processing_finished = pyqtSignal(list)

    def process_data(self):
        concordance_lines = []

        settings = self.main.settings_custom['concordancer']
        files = self.main.wordless_files.get_selected_files()

        self.progress_updated.emit(self.tr('Searching in text ...'))

        for file in files:
            number_lines = 0
            number_lines_nth = 0

            text = wordless_text.Wordless_Text(self.main, file, flat_tokens = False)

            tokens = wordless_token_processing.wordless_process_tokens_concordancer(text,
                                                                                    token_settings = settings['token_settings'])

            len_paras = len(text.offsets_paras)
            len_sentences = len(text.offsets_sentences)
            len_clauses = len(text.offsets_clauses)
            len_tokens = len(text.tokens_flat)

            search_terms = wordless_matching.match_search_terms(self.main, tokens,
                                                                lang = text.lang,
                                                                text_type = text.text_type,
                                                                token_settings = settings['token_settings'],
                                                                search_settings = settings['search_settings'])

            (search_terms_inclusion,
             search_terms_exclusion) = wordless_matching.match_search_terms_context(self.main, tokens,
                                                                                    lang = text.lang,
                                                                                    text_type = text.text_type,
                                                                                    token_settings = settings['token_settings'],
                                                                                    context_settings = settings['context_settings'])

            if search_terms:
                len_search_term_min = min([len(search_term) for search_term in search_terms])
                len_search_term_max = max([len(search_term) for search_term in search_terms])
            else:
                len_search_term_min = 0
                len_search_term_max = 0

            for len_search_term in range(len_search_term_min, len_search_term_max + 1):
                # Check number of lines
                if not settings['generation_settings']['number_lines_no_limit']:
                    if number_lines >= settings['generation_settings']['number_lines']:
                        break

                for i, ngram in enumerate(nltk.ngrams(tokens, len_search_term)):
                    if (ngram in search_terms and
                        wordless_matching.check_context(i, tokens,
                                                        context_settings = settings['context_settings'],
                                                        search_terms_inclusion = search_terms_inclusion,
                                                        search_terms_exclusion = search_terms_exclusion)):
                        concordance_line = []

                        # Check number of lines
                        if not settings['generation_settings']['number_lines_no_limit']:
                            if number_lines < settings['generation_settings']['number_lines']:
                                number_lines += 1
                            else:
                                break

                        # Check every nth line
                        if not settings['generation_settings']['every_nth_line_no_limit']:
                            number_lines_nth += 1

                            if (number_lines_nth - 1) % settings['generation_settings']['every_nth_line'] > 0:
                                continue

                        # Clause No.
                        if text.offsets_clauses[-1] <= i:
                            no_clause = len_clauses
                        else:
                            for j, i_clause in enumerate(text.offsets_clauses):
                                if i_clause > i:
                                    no_clause = j

                                    break

                        # Sentence No.
                        if text.offsets_sentences[-1] <= i:
                            no_sentence = len_sentences
                        else:
                            for j, i_sentence in enumerate(text.offsets_sentences):
                                if i_sentence > i:
                                    no_sentence = j

                                    break

                        # Paragraph No.
                        if text.offsets_paras[-1] <= i:
                            no_para = len_paras
                        else:
                            for j, i_para in enumerate(text.offsets_paras):
                                if i_para > i:
                                    no_para = j

                                    break

                        # Search in Results
                        text_search = list(ngram)

                        if not settings['token_settings']['puncs']:
                            ngram = text.tokens_flat[i : i + len_search_term]

                        node_text = wordless_text_processing.wordless_word_detokenize(self.main, ngram, text.lang)
                        node_text = wordless_text_utils.text_escape(node_text)

                        # Width Unit (Sentence)
                        if settings['generation_settings']['width_unit'] == self.tr('Sentence'):
                            width_left_sentence = settings['generation_settings']['width_left_sentence']
                            width_right_sentence = settings['generation_settings']['width_right_sentence']

                            sentence_offset_start = text.offsets_sentences[max(0, no_sentence - 1 - width_left_sentence)]

                            if no_sentence + width_right_sentence >= len_sentences:
                                sentence_offset_end = None
                            else:
                                sentence_offset_end = text.offsets_sentences[min(no_sentence + width_right_sentence, len_sentences - 1)]

                            context_left = text.tokens_flat[sentence_offset_start : i]
                            context_right = text.tokens_flat[i + len_search_term : sentence_offset_end]

                            # Search in Results
                            if settings['token_settings']['puncs']:
                                text_search_left = copy.deepcopy(context_left)
                                text_search_right = copy.deepcopy(context_right)
                            else:
                                text_search_left = tokens[sentence_offset_start : i]
                                text_search_right = tokens[i + len_search_term : sentence_offset_end]
                        # Width Unit (Clause)
                        elif settings['generation_settings']['width_unit'] == self.tr('Clause'):
                            width_left_clause = settings['generation_settings']['width_left_clause']
                            width_right_clause = settings['generation_settings']['width_right_clause']

                            clause_offset_start = text.offsets_clauses[max(0, no_clause - 1 - width_left_clause)]

                            if no_clause + width_right_clause >= len_clauses:
                                clause_offset_end = None
                            else:
                                clause_offset_end = text.offsets_clauses[min(no_clause + width_right_clause, len_clauses - 1)]

                            context_left = text.tokens_flat[clause_offset_start : i]
                            context_right = text.tokens_flat[i + len_search_term : clause_offset_end]

                            # Search in Results
                            if settings['token_settings']['puncs']:
                                text_search_left = copy.deepcopy(context_left)
                                text_search_right = copy.deepcopy(context_right)
                            else:
                                text_search_left = tokens[clause_offset_start : i]
                                text_search_right = tokens[i + len_search_term : clause_offset_end]

                        # Width Unit (Token)
                        elif settings['generation_settings']['width_unit'] == self.tr('Token'):
                            width_left_token = settings['generation_settings']['width_left_token']
                            width_right_token = settings['generation_settings']['width_right_token']

                            context_left = text.tokens_flat[max(0, i - width_left_token) : i]
                            context_right = text.tokens_flat[i + len_search_term : i + len_search_term + width_right_token]

                            # Search in Results
                            if settings['token_settings']['puncs']:
                                text_search_left = copy.deepcopy(context_left)
                                text_search_right = copy.deepcopy(context_right)
                            else:
                                text_search_left = tokens[max(0, i - width_left_token) : i]
                                text_search_right = tokens[i + len_search_term : i + len_search_term + width_right_token]
                        # Width Unit (Character)
                        elif settings['generation_settings']['width_unit'] == self.tr('Character'):
                            len_context_left = 0
                            len_context_right = 0

                            context_left = []
                            context_right = []

                            width_left_char = settings['generation_settings']['width_left_char']
                            width_right_char = settings['generation_settings']['width_right_char']

                            while len_context_left < width_left_char:
                                if i - 1 - len(context_left) < 0:
                                    break
                                else:
                                    token_next = tokens[i - 1 - len(context_left)]
                                    len_token_next = len(token_next)

                                if len_context_left + len_token_next > width_left_char:
                                    context_left.insert(0, token_next[-(width_left_char - len_context_left):])
                                else:
                                    context_left.insert(0, token_next)

                                len_context_left += len_token_next

                            while len_context_right < width_right_char:
                                if i + 1 + len(context_right) > len(text.tokens_flat) - 1:
                                    break
                                else:
                                    token_next = tokens[i + len_search_term + len(context_right)]
                                    len_token_next = len(token_next)

                                if len_context_right + len_token_next > width_right_char:
                                    context_right.append(token_next[: width_right_char - len_context_right])
                                else:
                                    context_right.append(token_next)

                                len_context_right += len(token_next)

                            # Search in Results
                            text_search_left = copy.deepcopy(context_left)
                            text_search_right = copy.deepcopy(context_right)

                            if not settings['token_settings']['puncs']:
                                context_left_first_puncs = text.tokens_flat[i - len(context_left)]
                                context_right_last_puncs = text.tokens_flat[i + len_search_term + len(context_right) - 1]
                                context_left_first = ''
                                context_right_last = ''

                                len_context_left_first = 0
                                len_context_right_last = 0

                                while len_context_left_first < len(context_left[0]):
                                    char_next = context_left_first_puncs[-(len(context_left_first) + 1)]

                                    context_left_first = char_next + context_left_first

                                    if char_next.isalnum():
                                        len_context_left_first += 1

                                while len_context_right_last < len(context_right[-1]):
                                    char_next = context_right_last_puncs[len(context_right_last)]

                                    context_right_last += char_next

                                    if char_next.isalnum():
                                        len_context_right_last += 1

                                context_left = ([context_left_first] +
                                                text.tokens_flat[i - len(context_left) + 1: i])
                                context_right = (text.tokens_flat[i + len_search_term : i + len_search_term + len(context_right) - 1] +
                                                 [context_right_last])

                        context_left = wordless_text_utils.text_escape(context_left)
                        context_right = wordless_text_utils.text_escape(context_right)

                        context_left_text = wordless_text_processing.wordless_word_detokenize(self.main, context_left, text.lang)
                        context_right_text = wordless_text_processing.wordless_word_detokenize(self.main, context_right, text.lang)

                        # Left
                        concordance_line.append([context_left_text, context_left, text_search_left])
                        # Node
                        concordance_line.append([node_text, list(ngram), text_search])
                        # Right
                        concordance_line.append([context_right_text, context_right, text_search_right])
                        # Token No.
                        concordance_line.append([i + 1, len_tokens])
                        # Clause No.
                        concordance_line.append([no_clause, len_clauses])
                        # Sentence No.
                        concordance_line.append([no_sentence, len_sentences])
                        # Paragraph No.
                        concordance_line.append([no_para, len_paras])
                        # File
                        concordance_line.append(file['name'])

                        concordance_lines.append(concordance_line)

        self.progress_updated.emit(self.tr('Rendering table ...'))

        time.sleep(0.1)

        self.processing_finished.emit(concordance_lines)

class Wordless_Worker_Process_Data_Concordancer_Fig(wordless_threading.Wordless_Worker_Process_Data):
    processing_finished = pyqtSignal(list, list)

    def process_data(self):
        texts = []
        search_terms_files = []
        search_terms_total = set()
        search_terms_labels = set()

        points = []
        labels = []

        settings = self.main.settings_custom['concordancer']
        files = sorted(self.main.wordless_files.get_selected_files(), key = lambda item: item['name'])

        for file in files:
            text = wordless_text.Wordless_Text(self.main, file)

            wordless_token_processing.wordless_process_tokens_concordancer(text,
                                                                           token_settings = settings['token_settings'])

            search_terms_file = wordless_matching.match_search_terms(self.main, text.tokens_flat,
                                                                     lang = text.lang,
                                                                     text_type = text.text_type,
                                                                     token_settings = settings['token_settings'],
                                                                     search_settings = settings['search_settings'])

            search_terms_files.append(sorted(search_terms_file))

            for search_term in search_terms_file:
                search_terms_total.add(search_term)
                search_terms_labels.add(wordless_text_processing.wordless_word_detokenize(self.main, search_term,
                                                                                          lang = text.lang))

            texts.append(text)

        len_files = len(files)
        len_tokens_total = sum([len(text.tokens_flat) for text in texts])
        len_search_terms_total = len(search_terms_total)

        if settings['fig_settings']['sort_results_by'] == self.tr('File'):
            search_terms_total = sorted(search_terms_total)
            search_terms_labels = sorted(search_terms_labels)

            for i, search_term in enumerate(search_terms_total):
                len_search_term = len(search_term)

                x_start = len_tokens_total * i + 1
                y_start = len_files

                for j, text in enumerate(texts):
                    if search_term in search_terms_files[j]:
                        x_start_total = x_start + sum([len(text.tokens_flat)
                                                       for k, text in enumerate(texts)
                                                       if k < j])
                        len_tokens = len(text.tokens_flat)

                        for k, ngram in enumerate(nltk.ngrams(text.tokens_flat, len_search_term)):
                            if ngram == search_term:
                                points.append([x_start + k / len_tokens * len_tokens_total, y_start - j])
                                # Total
                                points.append([x_start_total + k, 0])
        elif settings['fig_settings']['sort_results_by'] == self.tr('Search Term'):
            search_terms_total = sorted(search_terms_total, reverse = True)
            search_terms_labels = sorted(search_terms_labels, reverse = True)

            for i, search_term in enumerate(search_terms_total):
                len_search_term = len(search_term)

                for j, text in enumerate(texts):
                    if search_term in search_terms_files[j]:
                        x_start = sum([len(text.tokens_flat)
                                       for k, text in enumerate(texts)
                                       if k < j]) + j + 2

                        for k, ngram in enumerate(nltk.ngrams(text.tokens_flat, len_search_term)):
                            if ngram == search_term:
                                points.append([x_start + k, i])

        if points:
            x_ticks = [0]
            x_tick_labels = ['']

            if settings['fig_settings']['sort_results_by'] == self.tr('File'):
                len_tokens_total = sum([len(text.tokens_flat) for text in texts])

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

            elif settings['fig_settings']['sort_results_by'] == self.tr('Search Term'):
                len_search_terms_total = len(search_terms_total)

                for i, text in enumerate(texts):
                    x_tick_start = sum([len(text.tokens_flat)
                                        for j, text in enumerate(texts)
                                        if j < i]) + j + 1

                    # 1/2
                    x_ticks.append(x_tick_start + len(text.tokens_flat) / 2)
                    # Divider
                    x_ticks.append(x_tick_start + len(text.tokens_flat) + 1)

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

        self.progress_updated.emit(self.tr('Rendering figure ...'))

        time.sleep(0.1)

        self.processing_finished.emit(points, labels)

@wordless_misc.log_timing
def generate_table(main, table):
    def data_received(concordance_lines):
        node_color = settings['sort_results']['highlight_colors'][0]

        if concordance_lines:
            table.settings = main.settings_custom

            table.hide()
            table.blockSignals(True)
            table.setUpdatesEnabled(False)

            table.clear_table(0)

            for concordance_line in concordance_lines:
                left_text, left_text_raw, left_text_search = concordance_line[0]
                node_text, node_text_raw, node_text_search = concordance_line[1]
                right_text, right_text_raw, right_text_search = concordance_line[2]

                no_token, len_tokens = concordance_line[3]
                no_clause, len_clauses = concordance_line[4]
                no_sentence, len_sentences = concordance_line[5]
                no_para, len_paras = concordance_line[6]
                file_name = concordance_line[7]

                table.setRowCount(table.rowCount() + 1)

                # Node
                label_node = wordless_label.Wordless_Label_Html(
                    f'''
                        <span style="color: {node_color}; font-weight: bold;">
                            {node_text}
                        </span>
                    ''',
                    main
                )

                table.setCellWidget(table.rowCount() - 1, 1, label_node)

                table.cellWidget(table.rowCount() - 1, 1).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                table.cellWidget(table.rowCount() - 1, 1).text_raw = node_text_raw
                table.cellWidget(table.rowCount() - 1, 1).text_search = node_text_search

                # Left
                table.setCellWidget(table.rowCount() - 1, 0,
                                    wordless_label.Wordless_Label_Html(left_text, main))

                table.cellWidget(table.rowCount() - 1, 0).setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                table.cellWidget(table.rowCount() - 1, 0).text_raw = left_text_raw
                table.cellWidget(table.rowCount() - 1, 0).text_search = left_text_search

                # Right
                table.setCellWidget(table.rowCount() - 1, 2,
                                    wordless_label.Wordless_Label_Html(right_text, main))

                table.cellWidget(table.rowCount() - 1, 2).text_raw = right_text_raw
                table.cellWidget(table.rowCount() - 1, 2).text_search = right_text_search

                # Token No.
                table.set_item_num_pct(table.rowCount() - 1, 3, no_token, len_tokens)
                # Clause No.
                table.set_item_num_pct(table.rowCount() - 1, 4, no_clause, len_clauses)
                # Sentence No.
                table.set_item_num_pct(table.rowCount() - 1, 5, no_sentence, len_sentences)
                # Paragraph No.
                table.set_item_num_pct(table.rowCount() - 1, 6, no_para, len_paras)

                # File
                table.setItem(table.rowCount() - 1, 7, QTableWidgetItem(file_name))

            table.blockSignals(False)
            table.setUpdatesEnabled(True)
            table.show()

            table.toggle_pct()
            table.update_items_width()

            table.itemChanged.emit(table.item(0, 0))

            wordless_msg.wordless_msg_generate_table_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_table_error(main)

        dialog_progress.accept()

    settings = main.settings_custom['concordancer']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']):
            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

            worker_process_data = Wordless_Worker_Process_Data_Concordancer_Table(main, dialog_progress, data_received)
            thread_process_data = wordless_threading.Wordless_Thread_Process_Data(worker_process_data)

            thread_process_data.start()

            dialog_progress.exec_()

            thread_process_data.quit()
            thread_process_data.wait()
        else:
            wordless_msg_box.wordless_msg_box_missing_search_term(main)

            wordless_msg.wordless_msg_generate_table_error(main)
    else:
        wordless_msg.wordless_msg_generate_table_error(main)

@wordless_misc.log_timing
def generate_fig(main):
    def data_received(points, labels):
        if labels:
            x_ticks = labels[0]
            x_tick_labels = labels[1]
            y_ticks = labels[2]
            y_tick_labels = labels[3]
            y_max = labels[4]

        if points:
            if settings['fig_settings']['sort_results_by'] == main.tr('File'):
                matplotlib.pyplot.plot(numpy.array(points)[:, 0],
                                       numpy.array(points)[:, 1],
                                       'b|')

                matplotlib.pyplot.xlabel(main.tr('Search Terms'))
                matplotlib.pyplot.xticks(x_ticks, x_tick_labels, color = 'r')

                matplotlib.pyplot.ylabel(main.tr('Files'))
                matplotlib.pyplot.yticks(y_ticks, y_tick_labels)
                matplotlib.pyplot.ylim(-1, y_max)
            elif settings['fig_settings']['sort_results_by'] == main.tr('Search Term'):
                matplotlib.pyplot.plot(numpy.array(points)[:, 0],
                                       numpy.array(points)[:, 1],
                                       'b|')

                matplotlib.pyplot.xlabel(main.tr('Files'))
                matplotlib.pyplot.xticks(x_ticks, x_tick_labels)

                matplotlib.pyplot.ylabel(main.tr('Search Terms'))
                matplotlib.pyplot.yticks(y_ticks, y_tick_labels, color = 'r')
                matplotlib.pyplot.ylim(-1, y_max)

            matplotlib.pyplot.title(main.tr('Dispersion Plot'))
            matplotlib.pyplot.grid(True, which = 'major', axis = 'x', linestyle = 'dotted')

            wordless_msg.wordless_msg_generate_fig_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_fig_error(main)

        dialog_progress.accept()

        if points:
            wordless_fig.show_fig()

    settings = main.settings_custom['concordancer']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        if (not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term'] or
            settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']):
            dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

            worker_process_data = Wordless_Worker_Process_Data_Concordancer_Fig(main, dialog_progress, data_received)
            thread_process_data = wordless_threading.Wordless_Thread_Process_Data(worker_process_data)

            thread_process_data.start()

            dialog_progress.exec_()

            thread_process_data.quit()
            thread_process_data.wait()
        else:
            wordless_msg_box.wordless_msg_box_missing_search_term(main)

            wordless_msg.wordless_msg_generate_fig_error(main)
    else:
        wordless_msg.wordless_msg_generate_fig_error(main)
