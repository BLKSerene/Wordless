# ----------------------------------------------------------------------
# Wordless: Profiler
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

import collections
import copy
import itertools
import traceback

import numpy
import scipy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QPushButton, QGroupBox

from wordless.wl_dialogs import wl_dialogs_errs, wl_dialogs_misc, wl_msg_boxes
from wordless.wl_measures import wl_measures_misc, wl_measures_readability
from wordless.wl_nlp import wl_nlp_utils, wl_texts, wl_token_processing
from wordless.wl_utils import wl_misc, wl_msgs, wl_threading
from wordless.wl_widgets import wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wl_Table_Profiler(wl_tables.Wl_Table_Data):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'profiler',
            headers = [
                # Readability
                _tr('Wl_Table_Profiler', 'Automated Readability Index'),
                _tr('Wl_Table_Profiler', 'Coleman-Liau Index'),
                _tr('Wl_Table_Profiler', 'Dale-Chall Readability Score'),
                _tr('Wl_Table_Profiler', 'Devereaux Readability Index'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease (Simplified)'),
                _tr('Wl_Table_Profiler', 'Flesch-Kincaid Grade Level'),
                _tr('Wl_Table_Profiler', 'FORCAST Grade Level'),
                _tr('Wl_Table_Profiler', 'Gunning Fog Index'),
                _tr('Wl_Table_Profiler', 'SMOG Grade'),
                _tr('Wl_Table_Profiler', 'Spache Grade Level'),
                _tr('Wl_Table_Profiler', 'Write Score'),
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs'),
                _tr('Wl_Table_Profiler', 'Count of Paragraphs %'),
                _tr('Wl_Table_Profiler', 'Count of Sentences'),
                _tr('Wl_Table_Profiler', 'Count of Sentences %'),
                _tr('Wl_Table_Profiler', 'Count of Tokens'),
                _tr('Wl_Table_Profiler', 'Count of Tokens %'),
                _tr('Wl_Table_Profiler', 'Count of Types'),
                _tr('Wl_Table_Profiler', 'Count of Types %'),
                _tr('Wl_Table_Profiler', 'Count of Syllables'),
                _tr('Wl_Table_Profiler', 'Count of Syllables %'),
                _tr('Wl_Table_Profiler', 'Count of Characters'),
                _tr('Wl_Table_Profiler', 'Count of Characters %'),
                # TTR
                _tr('Wl_Table_Profiler', 'Type-token Ratio'),
                _tr('Wl_Table_Profiler', 'Type-token Ratio (Standardized)'),
                # Paragraph length
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Modes)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Modes)'),
                # Sentence length
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Range)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Modes)'),
                # Token length
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Modes)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Modes)'),
                # Type length
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Modes)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Modes)'),
                # Syllable length
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Range)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Modes)')
            ],
            header_orientation = 'vert',
            headers_int = [
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs'),
                _tr('Wl_Table_Profiler', 'Count of Sentences'),
                _tr('Wl_Table_Profiler', 'Count of Tokens'),
                _tr('Wl_Table_Profiler', 'Count of Types'),
                _tr('Wl_Table_Profiler', 'Count of Syllables'),
                _tr('Wl_Table_Profiler', 'Count of Characters'),
                # Paragraph length
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Range)'),
                # Sentence length
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Minimum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Maximum)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Range)'),
                # Token length
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Range)'),
                # Type length
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Range)'),
                # Syllable length
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Minimum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Maximum)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Range)')
            ],
            headers_float = [
                # Readability
                _tr('Wl_Table_Profiler', 'Automated Readability Index'),
                _tr('Wl_Table_Profiler', 'Coleman-Liau Index'),
                _tr('Wl_Table_Profiler', 'Dale-Chall Readability Score'),
                _tr('Wl_Table_Profiler', 'Devereaux Readability Index'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease'),
                _tr('Wl_Table_Profiler', 'Flesch Reading Ease (Simplified)'),
                _tr('Wl_Table_Profiler', 'Flesch-Kincaid Grade Level'),
                _tr('Wl_Table_Profiler', 'FORCAST Grade Level'),
                _tr('Wl_Table_Profiler', 'Gunning Fog Index'),
                _tr('Wl_Table_Profiler', 'SMOG Grade'),
                _tr('Wl_Table_Profiler', 'Spache Grade Level'),
                _tr('Wl_Table_Profiler', 'Write Score'),
                # TTR
                _tr('Wl_Table_Profiler', 'Type-token Ratio'),
                _tr('Wl_Table_Profiler', 'Type-token Ratio (Standardized)'),
                # Paragraph length
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Sentences (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Paragraph Length in Tokens (Interquartile Range)'),
                # Sentence length
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Mean)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Variance)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Median)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Sentence Length in Tokens (Interquartile Range)'),
                # Token length
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Token Length in Characters (Interquartile Range)'),
                # Type length
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Syllables (Interquartile Range)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Type Length in Characters (Interquartile Range)'),
                # Syllable length
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Mean)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Standard Deviation)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Variance)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (25th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Median)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (75th Percentile)'),
                _tr('Wl_Table_Profiler', 'Syllable Length in Characters (Interquartile Range)')
            ],
            headers_pct = [
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs %'),
                _tr('Wl_Table_Profiler', 'Count of Sentences %'),
                _tr('Wl_Table_Profiler', 'Count of Tokens %'),
                _tr('Wl_Table_Profiler', 'Count of Types %'),
                _tr('Wl_Table_Profiler', 'Count of Syllables %'),
                _tr('Wl_Table_Profiler', 'Count of Characters %')
            ],
            headers_cumulative = [
                # Counts
                _tr('Wl_Table_Profiler', 'Count of Paragraphs'),
                _tr('Wl_Table_Profiler', 'Count of Paragraphs %'),
                _tr('Wl_Table_Profiler', 'Count of Sentences'),
                _tr('Wl_Table_Profiler', 'Count of Sentences %'),
                _tr('Wl_Table_Profiler', 'Count of Tokens'),
                _tr('Wl_Table_Profiler', 'Count of Tokens %'),
                _tr('Wl_Table_Profiler', 'Count of Types'),
                _tr('Wl_Table_Profiler', 'Count of Types %'),
                _tr('Wl_Table_Profiler', 'Count of Syllables'),
                _tr('Wl_Table_Profiler', 'Count of Syllables %'),
                _tr('Wl_Table_Profiler', 'Count of Characters'),
                _tr('Wl_Table_Profiler', 'Count of Characters %')
            ]
        )

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())

    def file_changed(self, item): # pylint: disable=unused-argument
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)

    def clr_table(self, num_headers = 1, confirm = False):
        if super().clr_table(num_headers = 0, confirm = confirm):
            self.ins_header_hor(0, self.tr('Total'))

class Wrapper_Profiler(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_profiler = Wl_Table_Profiler(self)

        self.wrapper_table.layout().addWidget(self.table_profiler, 0, 0, 1, 4)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_generate_table, 1, 0)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_exp_selected, 1, 1)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_exp_all, 1, 2)
        self.wrapper_table.layout().addWidget(self.table_profiler.button_clr, 1, 3)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_words,
            self.checkbox_all_lowercase,
            self.checkbox_all_uppercase,
            self.checkbox_title_case,
            self.checkbox_nums,
            self.checkbox_puncs,

            self.checkbox_treat_as_all_lowercase,
            self.checkbox_lemmatize_tokens,
            self.checkbox_filter_stop_words,

            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lemmatize_tokens.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 2, 1)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_all_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lemmatize_tokens, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 8, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 8, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_profiler]
        )

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 1, 0)

        self.wrapper_settings.layout().setRowStretch(2, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['profiler'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['profiler'])

        # Token Settings
        self.checkbox_words.setChecked(settings['token_settings']['words'])
        self.checkbox_all_lowercase.setChecked(settings['token_settings']['all_lowercase'])
        self.checkbox_all_uppercase.setChecked(settings['token_settings']['all_uppercase'])
        self.checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        self.checkbox_nums.setChecked(settings['token_settings']['nums'])
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.checkbox_treat_as_all_lowercase.setChecked(settings['token_settings']['treat_as_all_lowercase'])
        self.checkbox_lemmatize_tokens.setChecked(settings['token_settings']['lemmatize_tokens'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        self.token_settings_changed()
        self.table_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['profiler']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['all_lowercase'] = self.checkbox_all_lowercase.isChecked()
        settings['all_uppercase'] = self.checkbox_all_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def table_settings_changed(self):
        settings = self.main.settings_custom['profiler']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

class Wl_Worker_Profiler(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.texts_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['profiler']
            files = list(self.main.wl_file_area.get_selected_files())

            for file in files:
                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens_profiler(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                texts.append(text)

            # Total
            if len(files) > 1:
                text_total = wl_texts.Wl_Text_Blank()

                # Set language for the combined text only if all texts are in the same language
                if len({text.lang for text in texts}) == 1:
                    text_total.lang = texts[0].lang
                else:
                    text_total.lang = 'other'

                text_total.offsets_paras = [
                    offset
                    for text in texts
                    for offset in text.offsets_paras
                ]
                text_total.offsets_sentences = [
                    offset
                    for text in texts
                    for offset in text.offsets_sentences
                ]
                text_total.tokens_multilevel = [
                    para
                    for text in texts
                    for para in text.tokens_multilevel
                ]
                text_total.tokens_flat = [
                    token
                    for text in texts
                    for token in text.tokens_flat
                ]
                text_total.syls_tokens = [
                    syls
                    for text in texts
                    for syls in text.syls_tokens
                ]

                texts.append(text_total)

            num_tokens_section_sttr = self.main.settings_custom['tables']['profiler']['general_settings']['num_tokens_section_sttr']

            for text in texts:
                texts_stats_file = []

                # Readability
                readability_statistics = [
                    wl_measures_readability.automated_readability_index(self.main, text),
                    wl_measures_readability.coleman_liau_index(self.main, text),
                    wl_measures_readability.dale_chall_readability_score(self.main, text),
                    wl_measures_readability.devereux_readability_index(self.main, text),
                    wl_measures_readability.flesch_reading_ease(self.main, text),
                    wl_measures_readability.flesch_reading_ease_simplified(self.main, text),
                    wl_measures_readability.flesch_kincaid_grade_level(self.main, text),
                    wl_measures_readability.forcast_grade_level(self.main, text),
                    wl_measures_readability.gunning_fog_index(self.main, text),
                    wl_measures_readability.smog_grade(self.main, text),
                    wl_measures_readability.spache_grade_level(self.main, text),
                    wl_measures_readability.write_score(self.main, text)
                ]

                # Paragraph length
                len_paras_sentences = [len(para) for para in text.tokens_multilevel]
                len_paras_tokens = [
                    sum((len(sentence) for sentence in para))
                    for para in text.tokens_multilevel
                ]

                # Sentence length
                len_sentences = [
                    len(sentence)
                    for para in text.tokens_multilevel
                    for sentence in para
                ]

                # Token length
                len_tokens_syls = [len(syls) for syls in text.syls_tokens]
                len_tokens_chars = [len(token) for token in text.tokens_flat]
                # Type length
                len_types_syls = [len(syls) for syls in {tuple(syls) for syls in text.syls_tokens}]
                len_types_chars = [len(token_type) for token_type in set(text.tokens_flat)]
                # Syllable length
                len_syls = [len(syl) for syls in text.syls_tokens for syl in syls]

                count_tokens = len(len_tokens_chars)
                count_types = len(len_types_chars)

                # TTR & STTR (weighted average)
                if count_tokens:
                    ttr = count_types / count_tokens

                    ttrs = [
                        len(set(token_section))
                        for token_section in wl_nlp_utils.to_sections_unequal(text.tokens_flat, num_tokens_section_sttr)
                    ]
                    sttr = numpy.sum(ttrs) / count_tokens
                else:
                    ttr = sttr = 0

                texts_stats_file.append(readability_statistics)
                texts_stats_file.append(len_paras_sentences)
                texts_stats_file.append(len_paras_tokens)
                texts_stats_file.append(len_sentences)
                texts_stats_file.append(len_tokens_syls)
                texts_stats_file.append(len_tokens_chars)
                texts_stats_file.append(len_types_syls)
                texts_stats_file.append(len_types_chars)
                texts_stats_file.append(len_syls)
                texts_stats_file.append(ttr)
                texts_stats_file.append(sttr)

                self.texts_stats_files.append(texts_stats_file)

            if len(files) == 1:
                self.texts_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Profiler_Table(Wl_Worker_Profiler):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(self.err_msg, self.texts_stats_files)

@wl_misc.log_timing
def generate_table(main, table):
    def update_gui(err_msg, texts_stats_files):
        if not err_msg:
            if any(itertools.chain.from_iterable(texts_stats_files)):
                try:
                    table.settings = copy.deepcopy(main.settings_custom)

                    table.clr_table()

                    count_tokens_lens = []
                    count_sentences_lens = []

                    # Insert column (total)
                    files = list(main.wl_file_area.get_selected_files())

                    for i, file in enumerate(files):
                        table.ins_header_hor(
                            table.find_header_hor(_tr('wl_profiler', 'Total')), file['name'],
                            is_breakdown = True
                        )

                    count_paras_total = len(texts_stats_files[-1][1])
                    count_sentences_total = len(texts_stats_files[-1][3])
                    count_tokens_total = len(texts_stats_files[-1][5])
                    count_types_total = len(texts_stats_files[-1][7])
                    count_syls_total = len(texts_stats_files[-1][8])
                    count_chars_total = sum(texts_stats_files[-1][5])

                    table.disable_updates()

                    for i, stats in enumerate(texts_stats_files):
                        if i < len(files):
                            file_lang = files[i]['lang']
                        # Total
                        else:
                            if len({file['lang'] for file in files}) == 1:
                                file_lang = files[0]['lang']
                            else:
                                file_lang = 'other'

                        readability_statistics = stats[0]
                        len_paras_sentences = stats[1]
                        len_paras_tokens = stats[2]
                        len_sentences = stats[3]
                        len_tokens_syls = stats[4]
                        len_tokens_chars = stats[5]
                        len_types_syls = stats[6]
                        len_types_chars = stats[7]
                        len_syls = stats[8]
                        ttr = stats[9]
                        sttr = stats[10]

                        len_paras_sentences = numpy.array(len_paras_sentences)
                        len_paras_tokens = numpy.array(len_paras_tokens)
                        len_sentences = numpy.array(len_sentences)
                        len_tokens_syls = numpy.array(len_tokens_syls)
                        len_tokens_chars = numpy.array(len_tokens_chars)
                        len_types_syls = numpy.array(len_types_syls)
                        len_types_chars = numpy.array(len_types_chars)
                        len_syls = numpy.array(len_syls)

                        count_paras = len(len_paras_sentences)
                        count_sentences = len(len_sentences)
                        count_tokens = len(len_tokens_chars)
                        count_types = len(len_types_chars)
                        count_syls = len(len_syls)
                        count_chars = numpy.sum(len_tokens_chars)

                        # Readibility
                        for j, statistic in enumerate(readability_statistics):
                            if statistic not in [
                                wl_measures_readability.TEXT_TOO_SHORT,
                                wl_measures_readability.NO_SUPPORT
                            ]:
                                table.set_item_num(j, i, statistic)
                            else:
                                table.set_item_error(j, i, statistic)

                        # Count of Paragraphs
                        table.set_item_num(12, i, count_paras)
                        table.set_item_num(13, i, count_paras, count_paras_total)

                        # Count of Sentences
                        table.set_item_num(14, i, count_sentences)
                        table.set_item_num(15, i, count_sentences, count_sentences_total)

                        # Count of Tokens
                        table.set_item_num(16, i, count_tokens)
                        table.set_item_num(17, i, count_tokens, count_tokens_total)

                        # Count of Types
                        table.set_item_num(18, i, count_types)
                        table.set_item_num(19, i, count_types, count_types_total)

                        # Count of Syllables
                        if file_lang in main.settings_global['syl_tokenizers']:
                            table.set_item_num(20, i, count_syls)
                            table.set_item_num(21, i, count_syls, count_syls_total)
                        else:
                            table.set_item_error(20, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(21, i, text = _tr('wl_profiler', 'No Support'))

                        # Count of Characters
                        table.set_item_num(22, i, count_chars)
                        table.set_item_num(23, i, count_chars, count_chars_total)

                        # Type-token Ratio
                        table.set_item_num(24, i, ttr)
                        # Type-token Ratio (Standardized)
                        table.set_item_num(25, i, sttr)

                        # Paragraph Length
                        if len_paras_sentences.any():
                            table.set_item_num(26, i, numpy.mean(len_paras_sentences))
                            table.set_item_num(27, i, numpy.std(len_paras_sentences))
                            table.set_item_num(28, i, numpy.var(len_paras_sentences))
                            table.set_item_num(29, i, numpy.min(len_paras_sentences))
                            table.set_item_num(30, i, numpy.percentile(len_paras_sentences, 25))
                            table.set_item_num(31, i, numpy.median(len_paras_sentences))
                            table.set_item_num(32, i, numpy.percentile(len_paras_sentences, 75))
                            table.set_item_num(33, i, numpy.max(len_paras_sentences))
                            table.set_item_num(34, i, numpy.ptp(len_paras_sentences))
                            table.set_item_num(35, i, scipy.stats.iqr(len_paras_sentences))
                            table.model().setItem(36, i, QStandardItem(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(len_paras_sentences)
                            ])))
                            table.set_item_num(37, i, numpy.mean(len_paras_tokens))
                            table.set_item_num(38, i, numpy.std(len_paras_tokens))
                            table.set_item_num(39, i, numpy.var(len_paras_tokens))
                            table.set_item_num(40, i, numpy.min(len_paras_tokens))
                            table.set_item_num(41, i, numpy.percentile(len_paras_tokens, 25))
                            table.set_item_num(42, i, numpy.median(len_paras_tokens))
                            table.set_item_num(43, i, numpy.percentile(len_paras_tokens, 75))
                            table.set_item_num(44, i, numpy.max(len_paras_tokens))
                            table.set_item_num(45, i, numpy.ptp(len_paras_tokens))
                            table.set_item_num(46, i, scipy.stats.iqr(len_paras_tokens))
                            table.model().setItem(47, i, QStandardItem(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(len_paras_tokens)
                            ])))
                        else:
                            table.set_item_num(26, i, 0)
                            table.set_item_num(27, i, 0)
                            table.set_item_num(28, i, 0)
                            table.set_item_num(29, i, 0)
                            table.set_item_num(30, i, 0)
                            table.set_item_num(31, i, 0)
                            table.set_item_num(32, i, 0)
                            table.set_item_num(33, i, 0)
                            table.set_item_num(34, i, 0)
                            table.set_item_num(35, i, 0)
                            table.model().setItem(36, i, QStandardItem('0'))
                            table.set_item_num(37, i, 0)
                            table.set_item_num(38, i, 0)
                            table.set_item_num(39, i, 0)
                            table.set_item_num(40, i, 0)
                            table.set_item_num(41, i, 0)
                            table.set_item_num(42, i, 0)
                            table.set_item_num(43, i, 0)
                            table.set_item_num(44, i, 0)
                            table.set_item_num(45, i, 0)
                            table.set_item_num(46, i, 0)
                            table.model().setItem(47, i, QStandardItem('0'))

                        table.model().item(36, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        table.model().item(47, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                        # Sentence Length
                        if len_sentences.any():
                            table.set_item_num(48, i, numpy.mean(len_sentences))
                            table.set_item_num(49, i, numpy.std(len_sentences))
                            table.set_item_num(50, i, numpy.var(len_sentences))
                            table.set_item_num(51, i, numpy.min(len_sentences))
                            table.set_item_num(52, i, numpy.percentile(len_sentences, 25))
                            table.set_item_num(53, i, numpy.median(len_sentences))
                            table.set_item_num(54, i, numpy.percentile(len_sentences, 75))
                            table.set_item_num(55, i, numpy.max(len_sentences))
                            table.set_item_num(56, i, numpy.ptp(len_sentences))
                            table.set_item_num(57, i, scipy.stats.iqr(len_sentences))
                            table.model().setItem(58, i, QStandardItem(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(len_sentences)
                            ])))
                        else:
                            table.set_item_num(48, i, 0)
                            table.set_item_num(49, i, 0)
                            table.set_item_num(50, i, 0)
                            table.set_item_num(51, i, 0)
                            table.set_item_num(52, i, 0)
                            table.set_item_num(53, i, 0)
                            table.set_item_num(54, i, 0)
                            table.set_item_num(55, i, 0)
                            table.set_item_num(56, i, 0)
                            table.set_item_num(57, i, 0)
                            table.model().setItem(58, i, QStandardItem('0'))

                        table.model().item(58, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                        # Token Length
                        if file_lang in main.settings_global['syl_tokenizers']:
                            if len_tokens_syls.any():
                                table.set_item_num(59, i, numpy.mean(len_tokens_syls))
                                table.set_item_num(60, i, numpy.std(len_tokens_syls))
                                table.set_item_num(61, i, numpy.var(len_tokens_syls))
                                table.set_item_num(62, i, numpy.min(len_tokens_syls))
                                table.set_item_num(63, i, numpy.percentile(len_tokens_syls, 25))
                                table.set_item_num(64, i, numpy.median(len_tokens_syls))
                                table.set_item_num(65, i, numpy.percentile(len_tokens_syls, 75))
                                table.set_item_num(66, i, numpy.max(len_tokens_syls))
                                table.set_item_num(67, i, numpy.ptp(len_tokens_syls))
                                table.set_item_num(68, i, scipy.stats.iqr(len_tokens_syls))
                                table.model().setItem(69, i, QStandardItem(', '.join([
                                    str(mode) for mode in wl_measures_misc.modes(len_tokens_syls)
                                ])))
                            else:
                                table.set_item_num(59, i, 0)
                                table.set_item_num(60, i, 0)
                                table.set_item_num(61, i, 0)
                                table.set_item_num(62, i, 0)
                                table.set_item_num(63, i, 0)
                                table.set_item_num(64, i, 0)
                                table.set_item_num(65, i, 0)
                                table.set_item_num(66, i, 0)
                                table.set_item_num(67, i, 0)
                                table.set_item_num(68, i, 0)
                                table.model().setItem(69, i, QStandardItem('0'))

                            table.model().item(69, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        else:
                            table.set_item_error(59, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(60, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(61, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(62, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(63, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(64, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(65, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(66, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(67, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(68, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(69, i, text = _tr('wl_profiler', 'No Support'))

                        if len_tokens_chars.any():
                            table.set_item_num(70, i, numpy.mean(len_tokens_chars))
                            table.set_item_num(71, i, numpy.std(len_tokens_chars))
                            table.set_item_num(72, i, numpy.var(len_tokens_chars))
                            table.set_item_num(73, i, numpy.min(len_tokens_chars))
                            table.set_item_num(74, i, numpy.percentile(len_tokens_chars, 25))
                            table.set_item_num(75, i, numpy.median(len_tokens_chars))
                            table.set_item_num(76, i, numpy.percentile(len_tokens_chars, 75))
                            table.set_item_num(77, i, numpy.max(len_tokens_chars))
                            table.set_item_num(78, i, numpy.ptp(len_tokens_chars))
                            table.set_item_num(79, i, scipy.stats.iqr(len_tokens_chars))
                            table.model().setItem(80, i, QStandardItem(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(len_tokens_chars)
                            ])))
                        else:
                            table.set_item_num(70, i, 0)
                            table.set_item_num(71, i, 0)
                            table.set_item_num(72, i, 0)
                            table.set_item_num(73, i, 0)
                            table.set_item_num(74, i, 0)
                            table.set_item_num(75, i, 0)
                            table.set_item_num(76, i, 0)
                            table.set_item_num(77, i, 0)
                            table.set_item_num(78, i, 0)
                            table.set_item_num(79, i, 0)
                            table.model().setItem(80, i, QStandardItem('0'))

                        table.model().item(80, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                        # Type Length
                        if file_lang in main.settings_global['syl_tokenizers']:
                            if len_types_syls.any():
                                table.set_item_num(81, i, numpy.mean(len_types_syls))
                                table.set_item_num(82, i, numpy.std(len_types_syls))
                                table.set_item_num(83, i, numpy.var(len_types_syls))
                                table.set_item_num(84, i, numpy.min(len_types_syls))
                                table.set_item_num(85, i, numpy.percentile(len_types_syls, 25))
                                table.set_item_num(86, i, numpy.median(len_types_syls))
                                table.set_item_num(87, i, numpy.percentile(len_types_syls, 75))
                                table.set_item_num(88, i, numpy.max(len_types_syls))
                                table.set_item_num(89, i, numpy.ptp(len_types_syls))
                                table.set_item_num(90, i, scipy.stats.iqr(len_types_syls))
                                table.model().setItem(91, i, QStandardItem(', '.join([
                                    str(mode) for mode in wl_measures_misc.modes(len_types_syls)
                                ])))
                            else:
                                table.set_item_num(81, i, 0)
                                table.set_item_num(82, i, 0)
                                table.set_item_num(83, i, 0)
                                table.set_item_num(84, i, 0)
                                table.set_item_num(85, i, 0)
                                table.set_item_num(86, i, 0)
                                table.set_item_num(87, i, 0)
                                table.set_item_num(88, i, 0)
                                table.set_item_num(89, i, 0)
                                table.set_item_num(90, i, 0)
                                table.model().setItem(91, i, QStandardItem('0'))

                            table.model().item(91, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        else:
                            table.set_item_error(81, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(82, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(83, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(84, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(85, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(86, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(87, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(88, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(89, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(90, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(91, i, text = _tr('wl_profiler', 'No Support'))

                        if len_types_chars.any():
                            table.set_item_num(92, i, numpy.mean(len_types_chars))
                            table.set_item_num(93, i, numpy.std(len_types_chars))
                            table.set_item_num(94, i, numpy.var(len_types_chars))
                            table.set_item_num(95, i, numpy.min(len_types_chars))
                            table.set_item_num(96, i, numpy.percentile(len_types_chars, 25))
                            table.set_item_num(97, i, numpy.median(len_types_chars))
                            table.set_item_num(98, i, numpy.percentile(len_types_chars, 75))
                            table.set_item_num(99, i, numpy.max(len_types_chars))
                            table.set_item_num(100, i, numpy.ptp(len_types_chars))
                            table.set_item_num(101, i, scipy.stats.iqr(len_types_chars))
                            table.model().setItem(102, i, QStandardItem(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(len_types_chars)
                            ])))
                        else:
                            table.set_item_num(92, i, 0)
                            table.set_item_num(93, i, 0)
                            table.set_item_num(94, i, 0)
                            table.set_item_num(95, i, 0)
                            table.set_item_num(96, i, 0)
                            table.set_item_num(97, i, 0)
                            table.set_item_num(98, i, 0)
                            table.set_item_num(99, i, 0)
                            table.set_item_num(100, i, 0)
                            table.set_item_num(101, i, 0)
                            table.model().setItem(102, i, QStandardItem('0'))

                        table.model().item(102, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                        # Syllable Length
                        if file_lang in main.settings_global['syl_tokenizers']:
                            if len_syls.any():
                                table.set_item_num(103, i, numpy.mean(len_syls))
                                table.set_item_num(104, i, numpy.std(len_syls))
                                table.set_item_num(105, i, numpy.var(len_syls))
                                table.set_item_num(106, i, numpy.min(len_syls))
                                table.set_item_num(107, i, numpy.percentile(len_syls, 25))
                                table.set_item_num(108, i, numpy.median(len_syls))
                                table.set_item_num(109, i, numpy.percentile(len_syls, 75))
                                table.set_item_num(110, i, numpy.max(len_syls))
                                table.set_item_num(111, i, numpy.ptp(len_syls))
                                table.set_item_num(112, i, scipy.stats.iqr(len_syls))
                                table.model().setItem(113, i, QStandardItem(', '.join([
                                    str(mode) for mode in wl_measures_misc.modes(len_syls)
                                ])))
                            else:
                                table.set_item_num(103, i, 0)
                                table.set_item_num(104, i, 0)
                                table.set_item_num(105, i, 0)
                                table.set_item_num(106, i, 0)
                                table.set_item_num(107, i, 0)
                                table.set_item_num(108, i, 0)
                                table.set_item_num(109, i, 0)
                                table.set_item_num(110, i, 0)
                                table.set_item_num(111, i, 0)
                                table.set_item_num(112, i, 0)
                                table.model().setItem(113, i, QStandardItem('0'))

                            table.model().item(113, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        else:
                            table.set_item_error(103, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(104, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(105, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(106, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(107, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(108, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(109, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(110, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(111, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(112, i, text = _tr('wl_profiler', 'No Support'))
                            table.set_item_error(113, i, text = _tr('wl_profiler', 'No Support'))

                        count_tokens_lens.append(collections.Counter(len_tokens_chars))
                        count_sentences_lens.append(collections.Counter(len_sentences))

                    # Count of n-length Sentences
                    if any(count_sentences_lens):
                        count_sentences_lens_files = wl_misc.merge_dicts(count_sentences_lens)
                        count_sentences_lens_total = {
                            len_sentence: count_sentences_files[-1]
                            for len_sentence, count_sentences_files in count_sentences_lens_files.items()
                        }
                        count_sentences_lens = sorted(count_sentences_lens_files.keys())

                        # Append vertical headers
                        for count_sentences_len in count_sentences_lens:
                            table.add_header_vert(
                                _tr('wl_profiler', 'Count of {}-length Sentences').format(count_sentences_len),
                                is_int = True, is_cumulative = True
                            )
                            table.add_header_vert(
                                _tr('wl_profiler', 'Count of {}-length Sentences %').format(count_sentences_len),
                                is_pct = True, is_cumulative = True
                            )

                        for i, count_sentences_len in enumerate(reversed(count_sentences_lens)):
                            counts = count_sentences_lens_files[count_sentences_len]

                            for j, count in enumerate(counts):
                                table.set_item_num(
                                    row = table.model().rowCount() - 2 - i * 2,
                                    col = j,
                                    val = count
                                )
                                table.set_item_num(
                                    row = table.model().rowCount() - 1 - i * 2,
                                    col = j,
                                    val = count,
                                    total = count_sentences_lens_total[count_sentences_len]
                                )

                    # Count of n-length Tokens
                    if any(count_tokens_lens):
                        count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens)
                        count_tokens_lens_total = {
                            len_token: count_tokens_files[-1]
                            for len_token, count_tokens_files in count_tokens_lens_files.items()
                        }
                        count_tokens_lens = sorted(count_tokens_lens_files.keys())

                        # Append vertical headers
                        for count_tokens_len in count_tokens_lens:
                            table.add_header_vert(
                                _tr('wl_profiler', 'Count of {}-Length Tokens').format(count_tokens_len),
                                is_int = True, is_cumulative = True
                            )
                            table.add_header_vert(
                                _tr('wl_profiler', 'Count of {}-Length Tokens %').format(count_tokens_len),
                                is_pct = True, is_cumulative = True
                            )

                        for i, count_tokens_len in enumerate(reversed(count_tokens_lens)):
                            counts = count_tokens_lens_files[count_tokens_len]

                            for j, count in enumerate(counts):
                                table.set_item_num(
                                    row = table.model().rowCount() - 2 - i * 2,
                                    col = j,
                                    val = count
                                )
                                table.set_item_num(
                                    row = table.model().rowCount() - 1 - i * 2,
                                    col = j,
                                    val = count,
                                    total = count_tokens_lens_total[count_tokens_len]
                                )

                    table.enable_updates()

                    table.toggle_pct()
                    table.toggle_cumulative()
                    table.toggle_breakdown()

                    wl_msgs.wl_msg_generate_table_success(main)
                except Exception:
                    err_msg = traceback.format_exc()
            else:
                wl_msg_boxes.wl_msg_box_no_results(main)
                wl_msgs.wl_msg_generate_table_error(main)

        if err_msg:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()
            wl_msgs.wl_msg_fatal_error(main)

    worker_profiler_table = Wl_Worker_Profiler_Table(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
        update_gui = update_gui
    )
    wl_threading.Wl_Thread(worker_profiler_table).start_worker()
