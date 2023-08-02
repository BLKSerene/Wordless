# ----------------------------------------------------------------------
# Wordless: Profiler
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

# pylint: disable=broad-exception-caught

import collections
import copy
import traceback

import numpy
import scipy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtWidgets import QDialog, QGroupBox, QPushButton, QStackedWidget, QTabWidget

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_measures import wl_measures_misc, wl_measures_readability
from wordless.wl_nlp import wl_nlp_utils, wl_texts, wl_token_preprocessing
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wrapper_Profiler(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_profiler_readability = Wl_Table_Profiler_Readability(self)
        self.table_profiler_counts = Wl_Table_Profiler_Counts(self)
        self.table_profiler_ttrs = Wl_Table_Profiler_Ttrs(self)
        self.table_profiler_lens = Wl_Table_Profiler_Lens(self)
        self.table_profiler_len_breakdown = Wl_Table_Profiler_Len_Breakdown(self)

        self.tables = [
            self.table_profiler_readability,
            self.table_profiler_counts,
            self.table_profiler_ttrs,
            self.table_profiler_lens,
            self.table_profiler_len_breakdown
        ]

        self.stacked_widget_button_generate_table = QStackedWidget(self)
        self.button_generate_all_tables = QPushButton(self.tr('Generate all tables'), self)
        self.stacked_widget_button_exp_selected_cells = QStackedWidget(self)
        self.stacked_widget_button_exp_all_cells = QStackedWidget(self)
        self.stacked_widget_button_clr_table = QStackedWidget(self)
        self.button_clr_all_tables = QPushButton(self.tr('Clear all tables'), self)

        for table in self.tables:
            self.stacked_widget_button_generate_table.addWidget(table.button_generate_table)
            self.stacked_widget_button_exp_selected_cells.addWidget(table.button_exp_selected_cells)
            self.stacked_widget_button_exp_all_cells.addWidget(table.button_exp_all_cells)
            self.stacked_widget_button_clr_table.addWidget(table.button_clr_table)

            table.model().itemChanged.connect(self.item_changed)

        self.button_generate_all_tables.clicked.connect(lambda: self.generate_all_tables()) # pylint: disable=unnecessary-lambda
        self.button_clr_all_tables.clicked.connect(self.clr_all_tables)

        self.tabs_profiler = QTabWidget(self)
        self.tabs_profiler.addTab(self.table_profiler_readability, self.tr('Readability'))
        self.tabs_profiler.addTab(self.table_profiler_counts, self.tr('Counts'))
        self.tabs_profiler.addTab(self.table_profiler_ttrs, self.tr('Type-token Ratios'))
        self.tabs_profiler.addTab(self.table_profiler_lens, self.tr('Lengths'))
        self.tabs_profiler.addTab(self.table_profiler_len_breakdown, self.tr('Length Breakdown'))

        self.tabs_profiler.currentChanged.connect(self.tabs_changed)

        self.wrapper_table.layout().addWidget(self.tabs_profiler, 0, 0, 1, 6)
        self.wrapper_table.layout().addWidget(self.stacked_widget_button_generate_table, 1, 0)
        self.wrapper_table.layout().addWidget(self.button_generate_all_tables, 1, 1)
        self.wrapper_table.layout().addWidget(self.stacked_widget_button_exp_selected_cells, 1, 2)
        self.wrapper_table.layout().addWidget(self.stacked_widget_button_exp_all_cells, 1, 3)
        self.wrapper_table.layout().addWidget(self.stacked_widget_button_clr_table, 1, 4)
        self.wrapper_table.layout().addWidget(self.button_clr_all_tables, 1, 5)

        self.wrapper_table.layout().setRowStretch(0, 1)
        self.wrapper_table.layout().setColumnStretch(0, 1)
        self.wrapper_table.layout().setColumnStretch(1, 1)
        self.wrapper_table.layout().setColumnStretch(2, 1)
        self.wrapper_table.layout().setColumnStretch(3, 1)
        self.wrapper_table.layout().setColumnStretch(4, 1)
        self.wrapper_table.layout().setColumnStretch(5, 1)

        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.file_changed()

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_words,
            self.checkbox_all_lowercase,
            self.checkbox_all_uppercase,
            self.checkbox_title_case,
            self.checkbox_nums,
            self.checkbox_punc_marks,

            self.checkbox_treat_as_all_lowercase,
            self.checkbox_apply_lemmatization,
            self.checkbox_filter_stop_words,

            self.checkbox_assign_pos_tags,
            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_all_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_punc_marks.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_all_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_apply_lemmatization.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.checkbox_assign_pos_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_all_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_punc_marks, 2, 1)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_all_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_apply_lemmatization, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_assign_pos_tags, 8, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 9, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 9, 1)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = self.tables
        )

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cum_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_file.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cum_data, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_file, 2, 0)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 1, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['profiler'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['profiler'])

        # Tab
        for i in range(self.tabs_profiler.count()):
            if self.tabs_profiler.tabText(i) == settings['tab']:
                self.tabs_profiler.setCurrentIndex(i)

        # Token Settings
        self.checkbox_words.setChecked(settings['token_settings']['words'])
        self.checkbox_all_lowercase.setChecked(settings['token_settings']['all_lowercase'])
        self.checkbox_all_uppercase.setChecked(settings['token_settings']['all_uppercase'])
        self.checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        self.checkbox_nums.setChecked(settings['token_settings']['nums'])
        self.checkbox_punc_marks.setChecked(settings['token_settings']['punc_marks'])

        self.checkbox_treat_as_all_lowercase.setChecked(settings['token_settings']['treat_as_all_lowercase'])
        self.checkbox_apply_lemmatization.setChecked(settings['token_settings']['apply_lemmatization'])
        self.checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        self.checkbox_assign_pos_tags.setChecked(settings['token_settings']['assign_pos_tags'])
        self.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Table Settings
        self.checkbox_show_pct_data.setChecked(settings['table_settings']['show_pct_data'])
        self.checkbox_show_cum_data.setChecked(settings['table_settings']['show_cum_data'])
        self.checkbox_show_breakdown_file.setChecked(settings['table_settings']['show_breakdown_file'])

        self.tabs_changed()
        self.item_changed()
        self.token_settings_changed()
        self.table_settings_changed()

    def tabs_changed(self):
        i_tabs = self.tabs_profiler.currentIndex()

        self.main.settings_custom['profiler']['tab'] = self.tabs_profiler.tabText(i_tabs)

        self.stacked_widget_button_generate_table.setCurrentIndex(i_tabs)
        self.stacked_widget_button_exp_selected_cells.setCurrentIndex(i_tabs)
        self.stacked_widget_button_exp_all_cells.setCurrentIndex(i_tabs)
        self.stacked_widget_button_clr_table.setCurrentIndex(i_tabs)

    def item_changed(self):
        if any((not table.is_empty() for table in self.tables)):
            self.button_clr_all_tables.setEnabled(True)
        else:
            self.button_clr_all_tables.setEnabled(False)

    def token_settings_changed(self):
        settings = self.main.settings_custom['profiler']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['all_lowercase'] = self.checkbox_all_lowercase.isChecked()
        settings['all_uppercase'] = self.checkbox_all_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['punc_marks'] = self.checkbox_punc_marks.isChecked()

        settings['treat_as_all_lowercase'] = self.checkbox_treat_as_all_lowercase.isChecked()
        settings['apply_lemmatization'] = self.checkbox_apply_lemmatization.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['assign_pos_tags'] = self.checkbox_assign_pos_tags.isChecked()
        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def table_settings_changed(self):
        settings = self.main.settings_custom['profiler']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()
        settings['show_cum_data'] = self.checkbox_show_cum_data.isChecked()
        settings['show_breakdown_file'] = self.checkbox_show_breakdown_file.isChecked()

    def file_changed(self):
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_all_tables.setEnabled(True)
        else:
            self.button_generate_all_tables.setEnabled(False)

    @wl_misc.log_timing
    def generate_all_tables(self):
        if self.main.settings_custom['profiler']['token_settings']['assign_pos_tags']:
            nlp_support = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ['pos_taggers'])
        else:
            nlp_support = True

        if nlp_support:
            worker_profiler_table = Wl_Worker_Profiler_Table(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                update_gui = self.update_gui_table,
                profiler_tab = 'all'
            )

            wl_threading.Wl_Thread(worker_profiler_table).start_worker()

    def update_gui_table(self, err_msg, text_stats_files):
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats_files):
            for table in self.tables:
                err_msg = table.update_gui_table(err_msg, text_stats_files)

                # Stop if error occurs when generating any of the tables
                if err_msg:
                    break

    def clr_all_tables(self):
        # Confirm if any of the tables are not empty and has yet to be exported
        needs_confirm = any((not table.is_empty() and not table.results_saved for table in self.tables))

        # Ask for confirmation if results have not been exported
        if needs_confirm:
            dialog_clr_table = wl_dialogs_misc.Wl_Dialog_Clr_All_Tables(self.main)
            result = dialog_clr_table.exec_()

            confirmed = bool(result == QDialog.Accepted)

        if confirmed:
            for table in self.tables:
                table.clr_table()

class Wl_Table_Profiler(wl_tables.Wl_Table_Data):
    def __init__(
        self, parent, headers,
        headers_int = None, headers_float = None, headers_pct = None, headers_cum = None,
        profiler_tab = 'all'
    ):
        super().__init__(
            parent,
            tab = 'profiler',
            headers = headers,
            header_orientation = 'vert',
            headers_int = headers_int,
            headers_float = headers_float,
            headers_pct = headers_pct,
            headers_cum = headers_cum,
            generate_fig = False
        )

        self.profiler_tab = profiler_tab

    def clr_table(self, confirm = False): # pylint: disable=arguments-differ
        if super().clr_table(num_headers = 0, confirm = confirm):
            self.ins_header_hor(0, self.tr('Total'))

    @wl_misc.log_timing
    def generate_table(self):
        if self.main.settings_custom['profiler']['token_settings']['assign_pos_tags']:
            nlp_support = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ['pos_taggers'])
        else:
            nlp_support = True

        if nlp_support:
            worker_profiler_table = Wl_Worker_Profiler_Table(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                update_gui = self.update_gui_table,
                profiler_tab = self.profiler_tab
            )

            wl_threading.Wl_Thread(worker_profiler_table).start_worker()

    def update_gui_table(self, err_msg, text_stats_files):
        raise NotImplementedError

class Wl_Table_Profiler_Readability(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_READABILITY = [
            _tr('wl_profiler', 'Automated Arabic Readability Index'),
            _tr('wl_profiler', 'Automated Readability Index'),
            _tr('wl_profiler', "Bormuth's Cloze Mean"),
            _tr('wl_profiler', "Bormuth's Grade Placement"),
            _tr('wl_profiler', 'Coleman-Liau Index'),
            _tr('wl_profiler', "Coleman's Readability Formula"),
            _tr('wl_profiler', 'Dale-Chall Readability Formula'),
            _tr('wl_profiler', 'Dale-Chall Readability Formula (New)'),
            _tr('wl_profiler', "Danielson-Bryan's Readability Formula"),
            _tr('wl_profiler', 'Degrees of Reading Power'),
            _tr('wl_profiler', 'Devereaux Readability Index'),
            _tr('wl_profiler', 'Easy Listening Formula'),
            _tr('wl_profiler', 'Flesch-Kincaid Grade Level'),
            _tr('wl_profiler', 'Flesch Reading Ease'),
            _tr('wl_profiler', 'Flesch Reading Ease (Simplified)'),
            _tr('wl_profiler', 'FORCAST Grade Level'),
            _tr('wl_profiler', 'Fórmula de Comprensibilidad de Gutiérrez de Polini'),
            _tr('wl_profiler', 'Fórmula de Crawford'),
            _tr('wl_profiler', 'Gulpease Index'),
            _tr('wl_profiler', 'Gunning Fog Index'),
            _tr('wl_profiler', 'Legibilidad μ'),
            _tr('wl_profiler', 'Lensear Write'),
            _tr('wl_profiler', 'Lix'),
            _tr('wl_profiler', 'McAlpine EFLAW Readability Score'),
            _tr('wl_profiler', 'OSMAN'),
            _tr('wl_profiler', 'Rix'),
            _tr('wl_profiler', 'SMOG Grade'),
            _tr('wl_profiler', 'Spache Grade Level'),
            _tr('wl_profiler', 'Wiener Sachtextformel')
        ]

        super().__init__(
            parent,
            headers = HEADERS_READABILITY,
            headers_float = HEADERS_READABILITY,
            profiler_tab = 'readability'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats_files):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for i, file in enumerate(files):
                    self.ins_header_hor(
                        self.find_header_hor(self.tr('Total')), file['name'],
                        is_breakdown_file = True
                    )

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    readability_stats = stats[0]

                    # Readability
                    for j, statistic in enumerate(readability_stats):
                        if statistic == 'no_support':
                            self.set_item_err(j, i, self.tr('No language support'), alignment_hor = 'right')
                        elif statistic == 'text_too_short':
                            self.set_item_err(j, i, self.tr('Text is too short'), alignment_hor = 'right')
                        else:
                            self.set_item_num(j, i, statistic)

                self.enable_updates()

                self.toggle_pct_data()
                self.toggle_cum_data()
                self.toggle_breakdown_file()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Counts(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_COUNTS = [
            _tr('wl_profiler', 'Count of Paragraphs'),
            _tr('wl_profiler', 'Count of Paragraphs %'),
            _tr('wl_profiler', 'Count of Sentences'),
            _tr('wl_profiler', 'Count of Sentences %'),
            _tr('wl_profiler', 'Count of Sentence Segments'),
            _tr('wl_profiler', 'Count of Sentence Segments %'),
            _tr('wl_profiler', 'Count of Tokens'),
            _tr('wl_profiler', 'Count of Tokens %'),
            _tr('wl_profiler', 'Count of Types'),
            _tr('wl_profiler', 'Count of Types %'),
            _tr('wl_profiler', 'Count of Syllables'),
            _tr('wl_profiler', 'Count of Syllables %'),
            _tr('wl_profiler', 'Count of Characters'),
            _tr('wl_profiler', 'Count of Characters %')
        ]

        super().__init__(
            parent,
            headers = HEADERS_COUNTS,
            headers_int = [
                HEADERS_COUNTS[i]
                for i in range(0, len(HEADERS_COUNTS), 2)
            ],
            headers_pct = [
                HEADERS_COUNTS[i]
                for i in range(1, len(HEADERS_COUNTS), 2)
            ],
            # Excluding count of types
            headers_cum = HEADERS_COUNTS[:8] + HEADERS_COUNTS[10:],
            profiler_tab = 'counts'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if all statistics except readability measures are 0 or empty
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats[1:]]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for i, file in enumerate(files):
                    self.ins_header_hor(
                        self.find_header_hor(self.tr('Total')), file['name'],
                        is_breakdown_file = True
                    )

                count_paras_total = len(text_stats_files[-1][1])
                count_sentences_total = len(text_stats_files[-1][4])
                count_sentence_segs_total = len(text_stats_files[-1][5])
                count_tokens_total = len(text_stats_files[-1][7])
                count_types_total = len(text_stats_files[-1][9])
                count_syls_total = len(text_stats_files[-1][10])
                count_chars_total = sum(text_stats_files[-1][7])

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    if i < len(files):
                        file_lang = files[i]['lang']
                    # Total
                    else:
                        if len({file['lang'] for file in files}) == 1:
                            file_lang = files[0]['lang']
                        else:
                            file_lang = 'other'

                    len_paras_sentences = numpy.array(stats[1])
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_chars = numpy.array(stats[7])
                    len_types_chars = numpy.array(stats[9])
                    len_syls = numpy.array(stats[10])

                    count_paras = len(len_paras_sentences)
                    count_sentences = len(len_sentences)
                    count_sentence_segs = len(len_sentence_segs)
                    count_tokens = len(len_tokens_chars)
                    count_types = len(len_types_chars)
                    count_syls = len(len_syls)
                    count_chars = numpy.sum(len_tokens_chars)

                    # Count of Paragraphs
                    self.set_item_num(0, i, count_paras)
                    self.set_item_num(1, i, count_paras, count_paras_total)

                    # Count of Sentences
                    self.set_item_num(2, i, count_sentences)
                    self.set_item_num(3, i, count_sentences, count_sentences_total)

                    # Count of Sentence Segments
                    self.set_item_num(4, i, count_sentence_segs)
                    self.set_item_num(5, i, count_sentence_segs, count_sentence_segs_total)

                    # Count of Tokens
                    self.set_item_num(6, i, count_tokens)
                    self.set_item_num(7, i, count_tokens, count_tokens_total)

                    # Count of Types
                    self.set_item_num(8, i, count_types)
                    self.set_item_num(9, i, count_types, count_types_total)

                    # Count of Syllables
                    if file_lang in self.main.settings_global['syl_tokenizers']:
                        self.set_item_num(10, i, count_syls)
                        self.set_item_num(11, i, count_syls, count_syls_total)
                    else:
                        self.set_item_err(10, i, text = self.tr('No language support'), alignment_hor = 'right')
                        self.set_item_err(11, i, text = self.tr('No language support'), alignment_hor = 'right')

                    # Count of Characters
                    self.set_item_num(12, i, count_chars)
                    self.set_item_num(13, i, count_chars, count_chars_total)

                self.enable_updates()

                self.toggle_pct_data()
                self.toggle_cum_data()
                self.toggle_breakdown_file()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Ttrs(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_TTRS = [
            _tr('wl_profiler', 'Type-token Ratio'),
            _tr('wl_profiler', 'Type-token Ratio (Standardized)')
        ]

        super().__init__(
            parent,
            headers = HEADERS_TTRS,
            headers_float = HEADERS_TTRS,
            profiler_tab = 'ttrs'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if all statistics except readability measures are 0 or empty
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats[1:]]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for i, file in enumerate(files):
                    self.ins_header_hor(
                        self.find_header_hor(self.tr('Total')), file['name'],
                        is_breakdown_file = True
                    )

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    ttr = stats[11]
                    sttr = stats[12]

                    # Type-token Ratio
                    self.set_item_num(0, i, ttr)
                    # Type-token Ratio (Standardized)
                    self.set_item_num(1, i, sttr)

                self.enable_updates()

                self.toggle_pct_data()
                self.toggle_cum_data()
                self.toggle_breakdown_file()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Lens(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_LEN_PARAS_SENTENCES = [
            _tr('wl_profiler', 'Paragraph Length in Sentences (Mean)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Standard Deviation)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Variance)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Minimum)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (25th Percentile)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Median)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (75th Percentile)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Maximum)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Range)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Interquartile Range)'),
            _tr('wl_profiler', 'Paragraph Length in Sentences (Modes)')
        ]

        HEADERS_LEN_PARAS_SENTENCE_SEGS = [
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Mean)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Standard Deviation)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Variance)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Minimum)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (25th Percentile)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Median)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (75th Percentile)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Maximum)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Range)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Interquartile Range)'),
            _tr('wl_profiler', 'Paragraph Length in Sentence Segments (Modes)')
        ]

        HEADERS_LEN_PARAS_TOKENS = [
            _tr('wl_profiler', 'Paragraph Length in Tokens (Mean)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Standard Deviation)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Variance)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Minimum)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (25th Percentile)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Median)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (75th Percentile)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Maximum)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Range)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Interquartile Range)'),
            _tr('wl_profiler', 'Paragraph Length in Tokens (Modes)')
        ]

        HEADERS_LEN_SENTENCES_TOKENS = [
            _tr('wl_profiler', 'Sentence Length in Tokens (Mean)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Standard Deviation)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Variance)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Minimum)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (25th Percentile)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Median)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (75th Percentile)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Maximum)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Range)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Interquartile Range)'),
            _tr('wl_profiler', 'Sentence Length in Tokens (Modes)')
        ]

        HEADERS_LEN_SENTENCE_SEGS_TOKENS = [
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Mean)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Standard Deviation)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Variance)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Minimum)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (25th Percentile)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Median)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (75th Percentile)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Maximum)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Range)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Interquartile Range)'),
            _tr('wl_profiler', 'Sentence Segment Length in Tokens (Modes)')
        ]

        HEADERS_LEN_TOKENS_SYLS = [
            _tr('wl_profiler', 'Token Length in Syllables (Mean)'),
            _tr('wl_profiler', 'Token Length in Syllables (Standard Deviation)'),
            _tr('wl_profiler', 'Token Length in Syllables (Variance)'),
            _tr('wl_profiler', 'Token Length in Syllables (Minimum)'),
            _tr('wl_profiler', 'Token Length in Syllables (25th Percentile)'),
            _tr('wl_profiler', 'Token Length in Syllables (Median)'),
            _tr('wl_profiler', 'Token Length in Syllables (75th Percentile)'),
            _tr('wl_profiler', 'Token Length in Syllables (Maximum)'),
            _tr('wl_profiler', 'Token Length in Syllables (Range)'),
            _tr('wl_profiler', 'Token Length in Syllables (Interquartile Range)'),
            _tr('wl_profiler', 'Token Length in Syllables (Modes)')
        ]

        HEADERS_LEN_TOKENS_CHARS = [
            _tr('wl_profiler', 'Token Length in Characters (Mean)'),
            _tr('wl_profiler', 'Token Length in Characters (Standard Deviation)'),
            _tr('wl_profiler', 'Token Length in Characters (Variance)'),
            _tr('wl_profiler', 'Token Length in Characters (Minimum)'),
            _tr('wl_profiler', 'Token Length in Characters (25th Percentile)'),
            _tr('wl_profiler', 'Token Length in Characters (Median)'),
            _tr('wl_profiler', 'Token Length in Characters (75th Percentile)'),
            _tr('wl_profiler', 'Token Length in Characters (Maximum)'),
            _tr('wl_profiler', 'Token Length in Characters (Range)'),
            _tr('wl_profiler', 'Token Length in Characters (Interquartile Range)'),
            _tr('wl_profiler', 'Token Length in Characters (Modes)')
        ]

        HEADERS_LEN_TYPES_SYLS = [
            _tr('wl_profiler', 'Type Length in Syllables (Mean)'),
            _tr('wl_profiler', 'Type Length in Syllables (Standard Deviation)'),
            _tr('wl_profiler', 'Type Length in Syllables (Variance)'),
            _tr('wl_profiler', 'Type Length in Syllables (Minimum)'),
            _tr('wl_profiler', 'Type Length in Syllables (25th Percentile)'),
            _tr('wl_profiler', 'Type Length in Syllables (Median)'),
            _tr('wl_profiler', 'Type Length in Syllables (75th Percentile)'),
            _tr('wl_profiler', 'Type Length in Syllables (Maximum)'),
            _tr('wl_profiler', 'Type Length in Syllables (Range)'),
            _tr('wl_profiler', 'Type Length in Syllables (Interquartile Range)'),
            _tr('wl_profiler', 'Type Length in Syllables (Modes)')
        ]

        HEADERS_LEN_TYPES_CHARS = [
            _tr('wl_profiler', 'Type Length in Characters (Mean)'),
            _tr('wl_profiler', 'Type Length in Characters (Standard Deviation)'),
            _tr('wl_profiler', 'Type Length in Characters (Variance)'),
            _tr('wl_profiler', 'Type Length in Characters (Minimum)'),
            _tr('wl_profiler', 'Type Length in Characters (25th Percentile)'),
            _tr('wl_profiler', 'Type Length in Characters (Median)'),
            _tr('wl_profiler', 'Type Length in Characters (75th Percentile)'),
            _tr('wl_profiler', 'Type Length in Characters (Maximum)'),
            _tr('wl_profiler', 'Type Length in Characters (Range)'),
            _tr('wl_profiler', 'Type Length in Characters (Interquartile Range)'),
            _tr('wl_profiler', 'Type Length in Characters (Modes)')
        ]

        HEADERS_LEN_SYLS_CHARS = [
            _tr('wl_profiler', 'Syllable Length in Characters (Mean)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Standard Deviation)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Variance)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Minimum)'),
            _tr('wl_profiler', 'Syllable Length in Characters (25th Percentile)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Median)'),
            _tr('wl_profiler', 'Syllable Length in Characters (75th Percentile)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Maximum)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Range)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Interquartile Range)'),
            _tr('wl_profiler', 'Syllable Length in Characters (Modes)')
        ]

        HEADERS_LENS = [
            HEADERS_LEN_PARAS_SENTENCES, HEADERS_LEN_PARAS_SENTENCE_SEGS, HEADERS_LEN_PARAS_TOKENS,
            HEADERS_LEN_SENTENCES_TOKENS, HEADERS_LEN_SENTENCE_SEGS_TOKENS,
            HEADERS_LEN_TOKENS_SYLS, HEADERS_LEN_TOKENS_CHARS,
            HEADERS_LEN_TYPES_SYLS, HEADERS_LEN_TYPES_CHARS,
            HEADERS_LEN_SYLS_CHARS
        ]

        super().__init__(
            parent,
            headers = [header for headers in HEADERS_LENS for header in headers],
            # Minimum, Maximum, and Range
            headers_int = sum((
                [HEADERS[3], HEADERS[7], HEADERS[8]]
                for HEADERS in HEADERS_LENS
            ), start = []),
            # Mean, Standard Deviation, Variance, 25th Percentile, Median, 75th Percentile, and Interquartile Range
            headers_float = sum((
                [*HEADERS[0:3], *HEADERS[4:7], HEADERS[9]]
                for HEADERS in HEADERS_LENS
            ), start = []),
            profiler_tab = 'lens'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if all statistics except readability measures are 0 or empty
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats[1:]]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for i, file in enumerate(files):
                    self.ins_header_hor(
                        self.find_header_hor(self.tr('Total')), file['name'],
                        is_breakdown_file = True
                    )

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    if i < len(files):
                        file_lang = files[i]['lang']
                    # Total
                    else:
                        if len({file['lang'] for file in files}) == 1:
                            file_lang = files[0]['lang']
                        else:
                            file_lang = 'other'

                    len_paras_sentences = numpy.array(stats[1])
                    len_paras_sentence_segs = numpy.array(stats[2])
                    len_paras_tokens = numpy.array(stats[3])
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_syls = numpy.array(stats[6])
                    len_tokens_chars = numpy.array(stats[7])
                    len_types_syls = numpy.array(stats[8])
                    len_types_chars = numpy.array(stats[9])
                    len_syls = numpy.array(stats[10])

                    # Paragraph Length in Sentences / Sentence Segments / Tokens
                    # Sentence / Sentence Segment Length in Tokens
                    # Token/Type Length in Characters
                    for row, lens in zip(
                        [
                            0, 11, 22,
                            33, 44,
                            55, 66
                        ], [
                            len_paras_sentences, len_paras_sentence_segs, len_paras_tokens,
                            len_sentences, len_sentence_segs,
                            len_tokens_chars, len_types_chars
                        ]
                    ):
                        if lens.any():
                            self.set_item_num(row, i, numpy.mean(lens))
                            self.set_item_num(row + 1, i, numpy.std(lens))
                            self.set_item_num(row + 2, i, numpy.var(lens))
                            self.set_item_num(row + 3, i, numpy.min(lens))
                            self.set_item_num(row + 4, i, numpy.percentile(lens, 25))
                            self.set_item_num(row + 5, i, numpy.median(lens))
                            self.set_item_num(row + 6, i, numpy.percentile(lens, 75))
                            self.set_item_num(row + 7, i, numpy.max(lens))
                            self.set_item_num(row + 8, i, numpy.ptp(lens))
                            self.set_item_num(row + 9, i, scipy.stats.iqr(lens))
                            self.model().setItem(row + 10, i, wl_tables.Wl_Table_Item(', '.join([
                                str(mode) for mode in wl_measures_misc.modes(lens)
                            ])))
                        else:
                            for j in range(10):
                                self.set_item_num(row + j, i, 0)

                            self.model().setItem(row + 10, i, wl_tables.Wl_Table_Item('0'))

                        self.model().item(row + 10, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    # Token/Type Length in Syllables
                    # Syllable Length in Characters
                    for row, lens in zip(
                        [
                            77, 88,
                            99
                        ], [
                            len_tokens_syls, len_types_syls,
                            len_syls
                        ]
                    ):
                        if file_lang in self.main.settings_global['syl_tokenizers']:
                            if lens.any():
                                self.set_item_num(row, i, numpy.mean(lens))
                                self.set_item_num(row + 1, i, numpy.std(lens))
                                self.set_item_num(row + 2, i, numpy.var(lens))
                                self.set_item_num(row + 3, i, numpy.min(lens))
                                self.set_item_num(row + 4, i, numpy.percentile(lens, 25))
                                self.set_item_num(row + 5, i, numpy.median(lens))
                                self.set_item_num(row + 6, i, numpy.percentile(lens, 75))
                                self.set_item_num(row + 7, i, numpy.max(lens))
                                self.set_item_num(row + 8, i, numpy.ptp(lens))
                                self.set_item_num(row + 9, i, scipy.stats.iqr(lens))
                                self.model().setItem(row + 10, i, wl_tables.Wl_Table_Item(', '.join([
                                    str(mode) for mode in wl_measures_misc.modes(lens)
                                ])))
                            else:
                                for j in range(10):
                                    self.set_item_num(row + j, i, 0)

                                self.model().setItem(row + 10, i, wl_tables.Wl_Table_Item('0'))

                            self.model().item(row + 10, i).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        else:
                            for j in range(11):
                                self.set_item_err(row + j, i, text = self.tr('No language support'), alignment_hor = 'right')

                self.enable_updates()

                self.toggle_pct_data()
                self.toggle_cum_data()
                self.toggle_breakdown_file()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Len_Breakdown(Wl_Table_Profiler):
    def __init__(self, parent):
        super().__init__(
            parent,
            headers = [],
            profiler_tab = 'len_breakdown'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if all statistics except readability measures are 0 or empty
        text_stats = [stat for text_stats in text_stats_files for stat in text_stats[1:]]

        if wl_checks_work_area.check_results(self.main, err_msg, text_stats):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                count_sentences_lens = []
                count_sentence_segs_lens = []
                count_tokens_lens_syls = []
                count_tokens_lens_chars = []

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for i, file in enumerate(files):
                    self.ins_header_hor(
                        self.find_header_hor(self.tr('Total')), file['name'],
                        is_breakdown_file = True
                    )

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_syls = numpy.array(stats[6])
                    len_tokens_chars = numpy.array(stats[7])

                    count_sentences_lens.append(collections.Counter(len_sentences))
                    count_sentence_segs_lens.append(collections.Counter(len_sentence_segs))
                    count_tokens_lens_syls.append(collections.Counter(len_tokens_syls))
                    count_tokens_lens_chars.append(collections.Counter(len_tokens_chars))

                # Count of n-token-long Sentences
                if any(count_sentences_lens):
                    count_sentences_lens_files = wl_misc.merge_dicts(count_sentences_lens)
                    count_sentences_lens_total = {
                        len_sentence: count_sentences_files[-1]
                        for len_sentence, count_sentences_files in count_sentences_lens_files.items()
                    }
                    count_sentences_lens = sorted(count_sentences_lens_files.keys())

                    # Append vertical headers
                    for count_sentences_len in count_sentences_lens:
                        self.add_header_vert(
                            self.tr('Count of {}-token-long Sentences').format(count_sentences_len),
                            is_int = True, is_cum = True
                        )
                        self.add_header_vert(
                            self.tr('Count of {}-token-long Sentences %').format(count_sentences_len),
                            is_pct = True, is_cum = True
                        )

                    for i, count_sentences_len in enumerate(reversed(count_sentences_lens)):
                        counts = count_sentences_lens_files[count_sentences_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_sentences_lens_total[count_sentences_len]
                            )

                # Count of n-token-long Sentence Segments
                if any(count_sentence_segs_lens):
                    count_sentence_segs_lens_files = wl_misc.merge_dicts(count_sentence_segs_lens)
                    count_sentence_segs_lens_total = {
                        len_sentence_seg: count_sentence_segs_files[-1]
                        for len_sentence_seg, count_sentence_segs_files in count_sentence_segs_lens_files.items()
                    }
                    count_sentence_segs_lens = sorted(count_sentence_segs_lens_files.keys())

                    # Append vertical headers
                    for count_sentence_segs_len in count_sentence_segs_lens:
                        self.add_header_vert(
                            self.tr('Count of {}-token-long Sentence Segment').format(count_sentence_segs_len),
                            is_int = True, is_cum = True
                        )
                        self.add_header_vert(
                            self.tr('Count of {}-token-long Sentence Segment %').format(count_sentence_segs_len),
                            is_pct = True, is_cum = True
                        )

                    for i, count_sentence_segs_len in enumerate(reversed(count_sentence_segs_lens)):
                        counts = count_sentence_segs_lens_files[count_sentence_segs_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_sentence_segs_lens_total[count_sentence_segs_len]
                            )

                # Count of n-syllable-long Tokens
                if any(count_tokens_lens_syls):
                    count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens_syls)
                    count_tokens_lens_total = {
                        len_token: count_tokens_files[-1]
                        for len_token, count_tokens_files in count_tokens_lens_files.items()
                    }
                    count_tokens_lens_syls = sorted(count_tokens_lens_files.keys())

                    # Append vertical headers
                    for count_tokens_len in count_tokens_lens_syls:
                        self.add_header_vert(
                            self.tr('Count of {}-syllables-long Tokens').format(count_tokens_len),
                            is_int = True, is_cum = True
                        )
                        self.add_header_vert(
                            self.tr('Count of {}-syllables-long Tokens %').format(count_tokens_len),
                            is_pct = True, is_cum = True
                        )

                    for i, count_tokens_len in enumerate(reversed(count_tokens_lens_syls)):
                        counts = count_tokens_lens_files[count_tokens_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_tokens_lens_total[count_tokens_len]
                            )

                # Count of n-character-long Tokens
                if any(count_tokens_lens_chars):
                    count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens_chars)
                    count_tokens_lens_total = {
                        len_token: count_tokens_files[-1]
                        for len_token, count_tokens_files in count_tokens_lens_files.items()
                    }
                    count_tokens_lens_chars = sorted(count_tokens_lens_files.keys())

                    # Append vertical headers
                    for count_tokens_len in count_tokens_lens_chars:
                        self.add_header_vert(
                            self.tr('Count of {}-character-long Tokens').format(count_tokens_len),
                            is_int = True, is_cum = True
                        )
                        self.add_header_vert(
                            self.tr('Count of {}-character-long Tokens %').format(count_tokens_len),
                            is_pct = True, is_cum = True
                        )

                    for i, count_tokens_len in enumerate(reversed(count_tokens_lens_chars)):
                        counts = count_tokens_lens_files[count_tokens_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2 - i * 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1 - i * 2,
                                col = j,
                                val = count,
                                total = count_tokens_lens_total[count_tokens_len]
                            )

                self.enable_updates()

                self.toggle_pct_data()
                self.toggle_cum_data()
                self.toggle_breakdown_file()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Worker_Profiler(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def __init__(self, main, dialog_progress, update_gui, profiler_tab):
        super().__init__(main, dialog_progress, update_gui, profiler_tab = profiler_tab)

        self.err_msg = ''
        self.text_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['profiler']
            files = list(self.main.wl_file_area.get_selected_files())

            for file in files:
                text = copy.deepcopy(file['text'])
                text = wl_token_preprocessing.wl_preprocess_tokens_profiler(
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

                text_total.tokens_multilevel = [
                    copy.deepcopy(para)
                    for text in texts
                    for para in text.tokens_multilevel
                ]
                text_total.syls_tokens = [
                    syls
                    for text in texts
                    for syls in text.syls_tokens
                ]

                texts.append(text_total)

            num_tokens_section_sttr = self.main.settings_custom['tables']['profiler']['general_settings']['num_tokens_section_sttr']

            for text in texts:
                tokens = text.get_tokens_flat()

                # Readability
                if self.profiler_tab in ['readability', 'all']:
                    readability_stats = [
                        wl_measures_readability.aari(self.main, text),
                        wl_measures_readability.ari(self.main, text),
                        wl_measures_readability.bormuths_cloze_mean(self.main, text),
                        wl_measures_readability.bormuths_gp(self.main, text),
                        wl_measures_readability.coleman_liau_index(self.main, text),
                        wl_measures_readability.colemans_readability_formula(self.main, text),
                        wl_measures_readability.dale_chall_readability_formula(self.main, text),
                        wl_measures_readability.dale_chall_readability_formula_new(self.main, text),
                        wl_measures_readability.danielson_bryans_readability_formula(self.main, text),
                        wl_measures_readability.drp(self.main, text),
                        wl_measures_readability.devereux_readability_index(self.main, text),
                        wl_measures_readability.elf(self.main, text),
                        wl_measures_readability.gl(self.main, text),
                        wl_measures_readability.re_flesch(self.main, text),
                        wl_measures_readability.re_simplified(self.main, text),
                        wl_measures_readability.rgl(self.main, text),
                        wl_measures_readability.cp(self.main, text),
                        wl_measures_readability.formula_de_crawford(self.main, text),
                        wl_measures_readability.gulpease_index(self.main, text),
                        wl_measures_readability.fog_index(self.main, text),
                        wl_measures_readability.mu(self.main, text),
                        wl_measures_readability.lensear_write(self.main, text),
                        wl_measures_readability.lix(self.main, text),
                        wl_measures_readability.eflaw(self.main, text),
                        wl_measures_readability.osman(self.main, text),
                        wl_measures_readability.rix(self.main, text),
                        wl_measures_readability.smog_grade(self.main, text),
                        wl_measures_readability.spache_grade_level(self.main, text),
                        wl_measures_readability.wstf(self.main, text)
                    ]
                else:
                    readability_stats = None

                if self.profiler_tab in ['ttrs', 'counts', 'lens', 'len_breakdown', 'all']:
                    # Paragraph length
                    len_paras_sentences = [
                        len(para)
                        for para in text.tokens_multilevel
                    ]
                    len_paras_sentence_segs = [
                        sum((len(sentence) for sentence in para))
                        for para in text.tokens_multilevel
                    ]
                    len_paras_tokens = [
                        sum((len(sentence_seg) for sentence in para for sentence_seg in sentence))
                        for para in text.tokens_multilevel
                    ]

                    # Sentence length
                    len_sentences = [
                        sum((len(sentence_seg) for sentence_seg in sentence))
                        for para in text.tokens_multilevel
                        for sentence in para
                    ]
                    len_sentence_segs = [
                        len(sentence_seg)
                        for para in text.tokens_multilevel
                        for sentence in para
                        for sentence_seg in sentence
                    ]

                    # Token length
                    len_tokens_syls = [len(syls) for syls in text.syls_tokens]
                    len_tokens_chars = [len(token) for token in tokens]
                    # Type length
                    len_types_syls = [len(syls) for syls in {tuple(syls) for syls in text.syls_tokens}]
                    len_types_chars = [len(token_type) for token_type in set(tokens)]
                    # Syllable length
                    len_syls = [len(syl) for syls in text.syls_tokens for syl in syls]
                else:
                    len_paras_sentences = len_paras_sentence_segs = len_paras_tokens = None
                    len_sentences = len_sentence_segs = None
                    len_tokens_syls = len_tokens_chars = None
                    len_types_syls = len_types_chars = None
                    len_syls = None

                # TTR & STTR (weighted average)
                if self.profiler_tab in ['ttrs', 'all']:
                    count_tokens = len(len_tokens_chars)
                    count_types = len(len_types_chars)

                    if count_tokens:
                        ttr = count_types / count_tokens

                        ttrs = [
                            len(set(token_section))
                            for token_section in wl_nlp_utils.to_sections_unequal(tokens, num_tokens_section_sttr)
                        ]
                        sttr = numpy.sum(ttrs) / count_tokens
                    else:
                        ttr = sttr = 0
                else:
                    ttr = sttr = None

                self.text_stats_files.append([
                    readability_stats,
                    len_paras_sentences,
                    len_paras_sentence_segs,
                    len_paras_tokens,
                    len_sentences,
                    len_sentence_segs,
                    len_tokens_syls,
                    len_tokens_chars,
                    len_types_syls,
                    len_types_chars,
                    len_syls,
                    ttr,
                    sttr
                ])

            if len(files) == 1:
                self.text_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Profiler_Table(Wl_Worker_Profiler):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(self.err_msg, self.text_stats_files)
