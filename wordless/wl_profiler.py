# ----------------------------------------------------------------------
# Wordless: Work Area - Profiler
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
import collections
import copy
import traceback

import numpy
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import scipy

from wordless.wl_checks import (
    wl_checks_tokens,
    wl_checks_work_area
)
from wordless.wl_dialogs import (
    wl_dialogs,
    wl_dialogs_misc
)
from wordless.wl_measures import (
    wl_measures_lexical_density_diversity,
    wl_measures_misc,
    wl_measures_readability,
    wl_measures_syntactic_complexity
)
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_texts,
    wl_token_processing
)
from wordless.wl_utils import (
    wl_excs,
    wl_misc,
    wl_threading
)
from wordless.wl_widgets import (
    wl_layouts,
    wl_tables,
    wl_widgets
)

_tr = QtCore.QCoreApplication.translate

class Wrapper_Profiler(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.tab = 'profiler'

        # Tables
        self.table_profiler_readability = Wl_Table_Profiler_Readability(self)
        self.table_profiler_counts = Wl_Table_Profiler_Counts(self)
        self.table_profiler_lexical_density_diversity = Wl_Table_Profiler_Lexical_Density_Diversity(self)
        self.table_profiler_syntactic_complexity = Wl_Table_Profiler_Syntactic_Complexity(self)
        self.table_profiler_lens = Wl_Table_Profiler_Lens(self)
        self.table_profiler_len_breakdown = Wl_Table_Profiler_Len_Breakdown(self)

        self.tables = (
            self.table_profiler_readability,
            self.table_profiler_counts,
            self.table_profiler_lexical_density_diversity,
            self.table_profiler_syntactic_complexity,
            self.table_profiler_lens,
            self.table_profiler_len_breakdown
        )

        self.stacked_widget_button_generate_table = QtWidgets.QStackedWidget(self)
        self.button_generate_all_tables = QtWidgets.QPushButton(self.tr('Generate all tables'), self)
        self.stacked_widget_button_exp_selected_cells = QtWidgets.QStackedWidget(self)
        self.stacked_widget_button_exp_all_cells = QtWidgets.QStackedWidget(self)
        self.stacked_widget_button_clr_table = QtWidgets.QStackedWidget(self)
        self.button_clr_all_tables = QtWidgets.QPushButton(self.tr('Clear all tables'), self)

        for table in self.tables:
            self.stacked_widget_button_generate_table.addWidget(table.button_generate_table)
            self.stacked_widget_button_exp_selected_cells.addWidget(table.button_exp_selected_cells)
            self.stacked_widget_button_exp_all_cells.addWidget(table.button_exp_all_cells)
            self.stacked_widget_button_clr_table.addWidget(table.button_clr_table)

            table.model().itemChanged.connect(self.item_changed)

        self.button_generate_all_tables.clicked.connect(lambda: self.generate_all_tables()) # pylint: disable=unnecessary-lambda
        self.button_clr_all_tables.clicked.connect(self.clr_all_tables)

        self.tabs_profiler = wl_layouts.Wl_Tab_Widget(self)
        self.tabs_profiler.addTab(self.table_profiler_readability, self.tr('Readability'))
        self.tabs_profiler.addTab(self.table_profiler_counts, self.tr('Counts'))
        self.tabs_profiler.addTab(self.table_profiler_lexical_density_diversity, self.tr('Lexical Density/Diversity'))
        self.tabs_profiler.addTab(self.table_profiler_syntactic_complexity, self.tr('Syntactic Complexity'))
        self.tabs_profiler.addTab(self.table_profiler_lens, self.tr('Lengths'))
        self.tabs_profiler.addTab(self.table_profiler_len_breakdown, self.tr('Length Breakdown'))

        self.tabs_profiler.currentChanged.connect(self.tabs_changed)

        self.tabs_profiler.setObjectName('tab_widget_profiler')
        self.tabs_profiler.setStyleSheet('''
            QTabWidget#tab_widget_profiler::pane {
                border: 0;
            }
        ''')

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
        self.group_box_token_settings = QtWidgets.QGroupBox(self.tr('Token Settings'), self)

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
        self.group_box_table_settings = QtWidgets.QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file,
            self.checkbox_show_total
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = self.tables
        )

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cum_data.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown_file.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_total.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cum_data, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown_file, 2, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_total, 3, 0)

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
            if self.tabs_profiler.widget(i).tab == settings['tab']:
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
        self.checkbox_show_total.setChecked(settings['table_settings']['show_total'])

        self.tabs_changed()
        self.item_changed()
        self.token_settings_changed()
        self.table_settings_changed()

    def tabs_changed(self):
        self.main.settings_custom['profiler']['tab'] = self.tabs_profiler.currentWidget().tab

        i_tab = self.tabs_profiler.currentIndex()

        self.stacked_widget_button_generate_table.setCurrentIndex(i_tab)
        self.stacked_widget_button_exp_selected_cells.setCurrentIndex(i_tab)
        self.stacked_widget_button_exp_all_cells.setCurrentIndex(i_tab)
        self.stacked_widget_button_clr_table.setCurrentIndex(i_tab)

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
        settings['show_total'] = self.checkbox_show_total.isChecked()

    def file_changed(self):
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_all_tables.setEnabled(True)
        else:
            self.button_generate_all_tables.setEnabled(False)

    @wl_misc.log_time
    def generate_all_tables(self):
        if self.main.settings_custom['profiler']['token_settings']['assign_pos_tags']:
            nlp_support = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ('pos_taggers',))
        else:
            nlp_support = True

        if nlp_support:
            self.worker_profiler_table = Wl_Worker_Profiler_Table(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                tab = 'all'
            )

            self.thread_profiler_table = QtCore.QThread()
            wl_threading.start_worker_in_thread(
                self.worker_profiler_table,
                self.thread_profiler_table,
                self.update_gui_table
            )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
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
            confirmed = wl_dialogs.Wl_Dialog_Question(
                self.main,
                title = self.tr('Clear All Tables'),
                text = self.tr('''
                    <div>The results in some of the tables have yet been exported.</div>
                    <br>
                    <div>Do you want to clear the results displayed in all tables?</div>
                ''')
            ).exec()
        else:
            confirmed = True

        if confirmed:
            for table in self.tables:
                if not table.is_empty():
                    table.clr_table()

class Wl_Table_Profiler(wl_tables.Wl_Table_Data):
    def __init__(
        self, parent, headers,
        headers_int = None, headers_float = None, headers_pct = None, headers_cum = None,
        tab = 'all'
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

        self.tab = tab

    def clr_table(self, confirm = False): # pylint: disable=arguments-differ
        if super().clr_table(num_headers = 0, confirm = confirm):
            self.ins_header_hor(0, self.tr('Total'), is_total = True)

    @wl_misc.log_time
    def generate_table(self):
        if self.main.settings_custom['profiler']['token_settings']['assign_pos_tags']:
            nlp_support = wl_checks_work_area.check_nlp_support(self.main, nlp_utils = ('pos_taggers',))
        else:
            nlp_support = True

        if nlp_support:
            self.worker_profiler_table = Wl_Worker_Profiler_Table(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                tab = self.tab
            )

            self.thread_profiler_table = QtCore.QThread()
            wl_threading.start_worker_in_thread(
                self.worker_profiler_table,
                self.thread_profiler_table,
                self.update_gui_table
            )

    def update_gui_table(self, err_msg, text_stats_files):
        raise NotImplementedError

class Wl_Table_Profiler_Readability(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_READABILITY = (
            _tr('Wl_Table_Profiler_Readability', "Al-Heeti's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', 'Automated Arabic Readability Index'),
            _tr('Wl_Table_Profiler_Readability', 'Automated Readability Index'),
            _tr('Wl_Table_Profiler_Readability', "Bormuth's Cloze Mean"),
            _tr('Wl_Table_Profiler_Readability', "Bormuth's Grade Placement"),
            _tr('Wl_Table_Profiler_Readability', 'Coleman-Liau Index'),
            _tr('Wl_Table_Profiler_Readability', "Coleman's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', "Crawford's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', 'Dale-Chall Readability Formula'),
            _tr('Wl_Table_Profiler_Readability', "Danielson-Bryan's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', "Dawood's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', 'Degrees of Reading Power'),
            _tr('Wl_Table_Profiler_Readability', 'Devereaux Readability Index'),
            _tr('Wl_Table_Profiler_Readability', 'Dickes-Steiwer Handformel'),
            _tr('Wl_Table_Profiler_Readability', 'Easy Listening Formula'),
            _tr('Wl_Table_Profiler_Readability', 'Flesch-Kincaid Grade Level'),
            _tr('Wl_Table_Profiler_Readability', 'Flesch Reading Ease'),
            _tr('Wl_Table_Profiler_Readability', 'Flesch Reading Ease (Farr-Jenkins-Paterson)'),
            _tr('Wl_Table_Profiler_Readability', 'FORCAST'),
            _tr('Wl_Table_Profiler_Readability', "Fucks's Stilcharakteristik"),
            _tr('Wl_Table_Profiler_Readability', 'GULPEASE'),
            _tr('Wl_Table_Profiler_Readability', 'Gunning Fog Index'),
            _tr('Wl_Table_Profiler_Readability', "Gutiérrez de Polini's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', 'Legibilidad μ'),
            _tr('Wl_Table_Profiler_Readability', 'Lensear Write Formula'),
            _tr('Wl_Table_Profiler_Readability', 'Lix'),
            _tr('Wl_Table_Profiler_Readability', 'Lorge Readability Index'),
            _tr('Wl_Table_Profiler_Readability', "Luong-Nguyen-Dinh's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', 'McAlpine EFLAW Readability Score'),
            _tr('Wl_Table_Profiler_Readability', 'neue Wiener Literaturformeln'),
            _tr('Wl_Table_Profiler_Readability', 'neue Wiener Sachtextformel'),
            _tr('Wl_Table_Profiler_Readability', 'OSMAN'),
            _tr('Wl_Table_Profiler_Readability', 'Rix'),
            _tr('Wl_Table_Profiler_Readability', 'SMOG Grading'),
            _tr('Wl_Table_Profiler_Readability', 'Spache Readability Formula'),
            _tr('Wl_Table_Profiler_Readability', 'Strain Index'),
            _tr('Wl_Table_Profiler_Readability', "Tränkle-Bailer's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', "Tuldava's Readability Formula"),
            _tr('Wl_Table_Profiler_Readability', "Wheeler-Smith's Readability Formula")
        )

        super().__init__(
            parent,
            headers = HEADERS_READABILITY,
            headers_float = set(HEADERS_READABILITY),
            tab = 'readability'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
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
                    for j, stat in enumerate(stats[0]):
                        if stat == 'no_support':
                            self.set_item_err(j, i, self.tr('No language support'), alignment_hor = 'right')
                        elif stat == 'text_too_short':
                            self.set_item_err(j, i, self.tr('Text is too short'), alignment_hor = 'right')
                        else:
                            self.set_item_num(j, i, stat)

                self.enable_updates()

                self.toggle_headers()
                self.toggle_cum_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Counts(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_COUNTS = (
            _tr('Wl_Table_Profiler_Counts', 'Count of Paragraphs'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Paragraphs %'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Sentences'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Sentences %'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Sentence Segments'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Sentence Segments %'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Tokens'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Tokens %'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Types'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Types %'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Syllables'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Syllables %'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Characters'),
            _tr('Wl_Table_Profiler_Counts', 'Count of Characters %')
        )

        super().__init__(
            parent,
            headers = HEADERS_COUNTS,
            headers_int = {
                HEADERS_COUNTS[i]
                for i in range(0, len(HEADERS_COUNTS), 2)
            },
            headers_pct = {
                HEADERS_COUNTS[i]
                for i in range(1, len(HEADERS_COUNTS), 2)
            },
            # Excluding count of types
            headers_cum = {*HEADERS_COUNTS[:8], *HEADERS_COUNTS[10:]},
            tab = 'counts'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
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
                count_syls_total = len(text_stats_files[-1][10]) if text_stats_files[-1][10] is not None else None
                count_chars_total = sum(text_stats_files[-1][7])

                self.disable_updates()

                for i, stats in enumerate(text_stats_files):
                    len_paras_sentences = numpy.array(stats[1])
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_chars = numpy.array(stats[7])
                    len_types_chars = numpy.array(stats[9])
                    len_syls = numpy.array(stats[10]) if stats[10] is not None else None

                    count_paras = len(len_paras_sentences)
                    count_sentences = len(len_sentences)
                    count_sentence_segs = len(len_sentence_segs)
                    count_tokens = len(len_tokens_chars)
                    count_types = len(len_types_chars)
                    count_syls = len(len_syls) if len_syls is not None else None
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
                    if count_syls is not None:
                        self.set_item_num(10, i, count_syls)

                        if count_syls_total is not None:
                            self.set_item_num(11, i, count_syls, count_syls_total)
                        else:
                            self.set_item_err(11, i, text = self.tr('No language support'), alignment_hor = 'right')
                    else:
                        self.set_item_err(10, i, text = self.tr('No language support'), alignment_hor = 'right')
                        self.set_item_err(11, i, text = self.tr('No language support'), alignment_hor = 'right')

                    # Count of Characters
                    self.set_item_num(12, i, count_chars)
                    self.set_item_num(13, i, count_chars, count_chars_total)

                self.enable_updates()

                self.toggle_headers()
                self.toggle_cum_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Lexical_Density_Diversity(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_LEXICAL_DENSITY_DIVERSITY = (
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Brunet's Index"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Corrected TTR'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Fisher's Index of Diversity"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Herdan's vₘ"),
            'HD-D',
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Honoré's Statistic"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Lexical Density'),
            'LogTTR',
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Mean Segmental TTR'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Measure of Textual Lexical Diversity'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Moving-average TTR'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu-Mačutek-Altmann's B₁"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu-Mačutek-Altmann's B₂"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu-Mačutek-Altmann's B₃"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu-Mačutek-Altmann's B₄"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu-Mačutek-Altmann's B₅"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu's R₁"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu's R₂"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu's R₃"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Popescu's R₄"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Repeat Rate'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Root TTR'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Shannon Entropy'),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Simpson's l"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', 'Type-token Ratio'),
            'vocd-D',
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Yule's Characteristic K"),
            _tr('Wl_Table_Profiler_Lexical_Density_Diversity', "Yule's Index of Diversity")
        )

        super().__init__(
            parent,
            headers = HEADERS_LEXICAL_DENSITY_DIVERSITY,
            headers_float = set(HEADERS_LEXICAL_DENSITY_DIVERSITY),
            tab = 'lexical_density_diversity'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
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
                    for j, stat in enumerate(stats[11]):
                        if stat == 'no_support':
                            self.set_item_err(j, i, self.tr('No language support'), alignment_hor = 'right')
                        else:
                            self.set_item_num(j, i, stat)

                self.enable_updates()

                self.toggle_headers()
                self.toggle_cum_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Syntactic_Complexity(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_DD = (
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Mean)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Variance)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Minimum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (25th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Median)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (75th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Maximum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Range)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Dependency Distance (Modes)')
        )

        HEADERS_ADD = (
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Mean)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Variance)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Minimum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (25th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Median)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (75th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Maximum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Range)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Absolute Dependency Distance (Modes)')
        )

        HEADERS_MDD = (
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Mean)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Variance)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Minimum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (25th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Median)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (75th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Maximum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Range)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Mean Dependency Distance (Interquartile Range)')
        )

        HEADERS_NDD = (
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Mean)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Variance)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Minimum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (25th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Median)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (75th Percentile)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Maximum)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Range)'),
            _tr('Wl_Table_Profiler_Syntactic_Complexity', 'Normalized Dependency Distance (Interquartile Range)')
        )

        HEADERS_SYNTACTIC_COMPLEXITY = (HEADERS_DD, HEADERS_ADD, HEADERS_MDD, HEADERS_NDD)

        super().__init__(
            parent,
            headers = tuple((header for headers in HEADERS_SYNTACTIC_COMPLEXITY for header in headers)),
            # Minimum, Maximum, and Range
            headers_int = set(sum((
                (HEADERS[3], HEADERS[7], HEADERS[8])
                for HEADERS in HEADERS_SYNTACTIC_COMPLEXITY
            ), start = ())),
            # Mean, Standard Deviation, Variance, 25th Percentile, Median, 75th Percentile, and Interquartile Range
            headers_float = set(sum((
                (*HEADERS[0:3], *HEADERS[4:7], HEADERS[9])
                for HEADERS in HEADERS_SYNTACTIC_COMPLEXITY
            ), start = ())),
            tab = 'syntactic_complexity'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
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
                    dds_sentences = stats[12]
                    mdds = stats[13]
                    ndds = stats[14]

                    if dds_sentences == 'no_support':
                        for j in range(42):
                            self.set_item_err(j, i, text = self.tr('No language support'), alignment_hor = 'right')
                    else:
                        # Dependency Distance
                        dds_sentences = numpy.array(list(wl_misc.flatten_list(dds_sentences)))
                        dds_sentences = dds_sentences[dds_sentences != 0]

                        self.set_item_num(0, i, numpy.mean(dds_sentences))
                        self.set_item_num(1, i, numpy.std(dds_sentences))
                        self.set_item_num(2, i, numpy.var(dds_sentences))
                        self.set_item_num(3, i, numpy.min(dds_sentences))
                        self.set_item_num(4, i, numpy.percentile(dds_sentences, 25))
                        self.set_item_num(5, i, numpy.median(dds_sentences))
                        self.set_item_num(6, i, numpy.percentile(dds_sentences, 75))
                        self.set_item_num(7, i, numpy.max(dds_sentences))
                        self.set_item_num(8, i, numpy.ptp(dds_sentences))
                        self.set_item_num(9, i, scipy.stats.iqr(dds_sentences))
                        self.model().setItem(10, i, wl_tables.Wl_Table_Item(', '.join([
                            str(mode) for mode in wl_measures_misc.modes(dds_sentences)
                        ])))

                        # Absolute Dependency Distance
                        adds = numpy.absolute(dds_sentences)

                        self.set_item_num(11, i, numpy.mean(adds))
                        self.set_item_num(12, i, numpy.std(adds))
                        self.set_item_num(13, i, numpy.var(adds))
                        self.set_item_num(14, i, numpy.min(adds))
                        self.set_item_num(15, i, numpy.percentile(adds, 25))
                        self.set_item_num(16, i, numpy.median(adds))
                        self.set_item_num(17, i, numpy.percentile(adds, 75))
                        self.set_item_num(18, i, numpy.max(adds))
                        self.set_item_num(19, i, numpy.ptp(adds))
                        self.set_item_num(20, i, scipy.stats.iqr(adds))
                        self.model().setItem(21, i, wl_tables.Wl_Table_Item(', '.join([
                            str(mode) for mode in wl_measures_misc.modes(adds)
                        ])))

                        # Mean Dependency Distance
                        self.set_item_num(22, i, numpy.mean(mdds))
                        self.set_item_num(23, i, numpy.std(mdds))
                        self.set_item_num(24, i, numpy.var(mdds))
                        self.set_item_num(25, i, numpy.min(mdds))
                        self.set_item_num(26, i, numpy.percentile(mdds, 25))
                        self.set_item_num(27, i, numpy.median(mdds))
                        self.set_item_num(28, i, numpy.percentile(mdds, 75))
                        self.set_item_num(29, i, numpy.max(mdds))
                        self.set_item_num(30, i, numpy.ptp(mdds))
                        self.set_item_num(31, i, scipy.stats.iqr(mdds))

                        # Normalized Dependency Distance
                        self.set_item_num(32, i, numpy.mean(ndds))
                        self.set_item_num(33, i, numpy.std(ndds))
                        self.set_item_num(34, i, numpy.var(ndds))
                        self.set_item_num(35, i, numpy.min(ndds))
                        self.set_item_num(36, i, numpy.percentile(ndds, 25))
                        self.set_item_num(37, i, numpy.median(ndds))
                        self.set_item_num(38, i, numpy.percentile(ndds, 75))
                        self.set_item_num(39, i, numpy.max(ndds))
                        self.set_item_num(40, i, numpy.ptp(ndds))
                        self.set_item_num(41, i, scipy.stats.iqr(ndds))

                self.enable_updates()

                self.toggle_headers()
                self.toggle_cum_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Lens(Wl_Table_Profiler):
    def __init__(self, parent):
        HEADERS_LEN_PARAS_SENTENCES = (
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentences (Modes)')
        )

        HEADERS_LEN_PARAS_SENTENCE_SEGS = (
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Sentence Segments (Modes)')
        )

        HEADERS_LEN_PARAS_TOKENS = (
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Paragraph Length in Tokens (Modes)')
        )

        HEADERS_LEN_SENTENCES_TOKENS = (
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Length in Tokens (Modes)')
        )

        HEADERS_LEN_SENTENCE_SEGS_TOKENS = (
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Sentence Segment Length in Tokens (Modes)')
        )

        HEADERS_LEN_TOKENS_SYLS = (
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Syllables (Modes)')
        )

        HEADERS_LEN_TOKENS_CHARS = (
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Token Length in Characters (Modes)')
        )

        HEADERS_LEN_TYPES_SYLS = (
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Syllables (Modes)')
        )

        HEADERS_LEN_TYPES_CHARS = (
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Type Length in Characters (Modes)')
        )

        HEADERS_LEN_SYLS_CHARS = (
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Mean)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Standard Deviation)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Variance)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Minimum)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (25th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Median)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (75th Percentile)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Maximum)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Interquartile Range)'),
            _tr('Wl_Table_Profiler_Lens', 'Syllable Length in Characters (Modes)')
        )

        HEADERS_LENS = (
            HEADERS_LEN_PARAS_SENTENCES, HEADERS_LEN_PARAS_SENTENCE_SEGS, HEADERS_LEN_PARAS_TOKENS,
            HEADERS_LEN_SENTENCES_TOKENS, HEADERS_LEN_SENTENCE_SEGS_TOKENS,
            HEADERS_LEN_TOKENS_SYLS, HEADERS_LEN_TOKENS_CHARS,
            HEADERS_LEN_TYPES_SYLS, HEADERS_LEN_TYPES_CHARS,
            HEADERS_LEN_SYLS_CHARS
        )

        super().__init__(
            parent,
            headers = tuple((header for headers in HEADERS_LENS for header in headers)),
            # Minimum, Maximum, and Range
            headers_int = set(sum((
                (HEADERS[3], HEADERS[7], HEADERS[8])
                for HEADERS in HEADERS_LENS
            ), start = ())),
            # Mean, Standard Deviation, Variance, 25th Percentile, Median, 75th Percentile, and Interquartile Range
            headers_float = set(sum((
                (*HEADERS[0:3], *HEADERS[4:7], HEADERS[9])
                for HEADERS in HEADERS_LENS
            ), start = ())),
            tab = 'lens'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
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
                    len_paras_sentences = numpy.array(stats[1])
                    len_paras_sentence_segs = numpy.array(stats[2])
                    len_paras_tokens = numpy.array(stats[3])
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_syls = numpy.array(stats[6]) if stats[6] is not None else None
                    len_tokens_chars = numpy.array(stats[7])
                    len_types_syls = numpy.array(stats[8]) if stats[8] is not None else None
                    len_types_chars = numpy.array(stats[9])
                    len_syls = numpy.array(stats[10]) if stats[10] is not None else None

                    # Paragraph Length in Sentences / Sentence Segments / Tokens
                    # Sentence / Sentence Segment Length in Tokens
                    # Token/Type Length in Characters
                    for row, lens in zip(
                        (
                            0, 11, 22,
                            33, 44,
                            66, 88
                        ), (
                            len_paras_sentences, len_paras_sentence_segs, len_paras_tokens,
                            len_sentences, len_sentence_segs,
                            len_tokens_chars, len_types_chars
                        )
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

                        self.model().item(row + 10, i).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

                    # Token/Type Length in Syllables
                    # Syllable Length in Characters
                    for row, lens in zip(
                        (55, 77, 99),
                        (len_tokens_syls, len_types_syls, len_syls)
                    ):
                        if lens is not None:
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

                            self.model().item(row + 10, i).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        else:
                            for j in range(11):
                                self.set_item_err(row + j, i, text = self.tr('No language support'), alignment_hor = 'right')

                self.enable_updates()

                self.toggle_headers()
                self.toggle_cum_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Table_Profiler_Len_Breakdown(Wl_Table_Profiler):
    def __init__(self, parent):
        super().__init__(
            parent,
            headers = (),
            tab = 'len_breakdown'
        )

    def update_gui_table(self, err_msg, text_stats_files):
        # Skip if the text is empty
        len_tokens = text_stats_files[-1][7] if text_stats_files else []

        if wl_checks_work_area.check_results(self.main, err_msg, len_tokens):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table()

                count_sentences_lens = []
                count_sentence_segs_lens = []
                count_tokens_lens_syls = []
                count_tokens_lens_chars = []

                # Insert columns
                files = list(self.main.wl_file_area.get_selected_files())

                for file in files:
                    self.ins_header_hor(
                        self.find_header_hor(self.tr('Total')), file['name'],
                        is_breakdown_file = True
                    )

                self.disable_updates()

                for stats in text_stats_files:
                    len_sentences = numpy.array(stats[4])
                    len_sentence_segs = numpy.array(stats[5])
                    len_tokens_syls = numpy.array(stats[6]) if stats[6] is not None else None
                    len_tokens_chars = numpy.array(stats[7])

                    count_sentences_lens.append(collections.Counter(len_sentences))
                    count_sentence_segs_lens.append(collections.Counter(len_sentence_segs))
                    count_tokens_lens_syls.append(
                        collections.Counter(len_tokens_syls) if len_tokens_syls is not None else None
                    )
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
                        if count_sentences_len:
                            self.add_header_vert(
                                self.tr('Count of {}-token-long Sentences').format(count_sentences_len),
                                is_int = True, is_cum = True
                            )
                            self.add_header_vert(
                                self.tr('Count of {}-token-long Sentences %').format(count_sentences_len),
                                is_pct = True, is_cum = True
                            )

                            counts = count_sentences_lens_files[count_sentences_len]

                            for j, count in enumerate(counts):
                                self.set_item_num(
                                    row = self.model().rowCount() - 2,
                                    col = j,
                                    val = count
                                )
                                self.set_item_num(
                                    row = self.model().rowCount() - 1,
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
                        if count_sentence_segs_len:
                            self.add_header_vert(
                                self.tr('Count of {}-token-long Sentence Segment').format(count_sentence_segs_len),
                                is_int = True, is_cum = True
                            )
                            self.add_header_vert(
                                self.tr('Count of {}-token-long Sentence Segment %').format(count_sentence_segs_len),
                                is_pct = True, is_cum = True
                            )

                            counts = count_sentence_segs_lens_files[count_sentence_segs_len]

                            for j, count in enumerate(counts):
                                self.set_item_num(
                                    row = self.model().rowCount() - 2,
                                    col = j,
                                    val = count
                                )
                                self.set_item_num(
                                    row = self.model().rowCount() - 1,
                                    col = j,
                                    val = count,
                                    total = count_sentence_segs_lens_total[count_sentence_segs_len]
                                )

                # Count of n-syllable-long Tokens
                if len_tokens_syls is not None:
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

                        counts = count_tokens_lens_files[count_tokens_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1,
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

                        counts = count_tokens_lens_files[count_tokens_len]

                        for j, count in enumerate(counts):
                            self.set_item_num(
                                row = self.model().rowCount() - 2,
                                col = j,
                                val = count
                            )
                            self.set_item_num(
                                row = self.model().rowCount() - 1,
                                col = j,
                                val = count,
                                total = count_tokens_lens_total[count_tokens_len]
                            )

                self.enable_updates()

                self.toggle_headers()
                self.toggle_cum_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

        return err_msg

class Wl_Worker_Profiler(wl_threading.Wl_Worker):
    finished = QtCore.pyqtSignal(str, list)

    def __init__(self, main, dialog_progress, tab):
        super().__init__(main, dialog_progress, tab = tab)

        self.err_msg = ''
        self.text_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['profiler']
            files = list(self.main.wl_file_area.get_selected_files())

            for file in files:
                if not self._running:
                    raise wl_excs.Wl_Exc_Aborted(self.main)

                text = wl_token_processing.wl_process_tokens_profiler(
                    self.main, file['text'],
                    token_settings = settings['token_settings'],
                    tab = self.tab
                )

                texts.append(text)

            # Total
            if self._running and len(files) > 1:
                texts.append(wl_texts.Wl_Text_Total(texts))

            for text in texts:
                if not self._running:
                    raise wl_excs.Wl_Exc_Aborted(self.main)

                # Readability
                if self.tab in ('readability', 'all'):
                    stats_readability = [
                        wl_measures_readability.rd(self.main, text),
                        wl_measures_readability.aari(self.main, text),
                        wl_measures_readability.ari(self.main, text),
                        wl_measures_readability.bormuths_cloze_mean(self.main, text),
                        wl_measures_readability.bormuths_gp(self.main, text),
                        wl_measures_readability.coleman_liau_index(self.main, text),
                        wl_measures_readability.colemans_readability_formula(self.main, text),
                        wl_measures_readability.crawfords_readability_formula(self.main, text),
                        wl_measures_readability.x_c50(self.main, text),
                        wl_measures_readability.danielson_bryans_readability_formula(self.main, text),
                        wl_measures_readability.dawoods_readability_formula(self.main, text),
                        wl_measures_readability.drp(self.main, text),
                        wl_measures_readability.devereux_readability_index(self.main, text),
                        wl_measures_readability.dickes_steiwer_handformel(self.main, text),
                        wl_measures_readability.elf(self.main, text),
                        wl_measures_readability.gl(self.main, text),
                        wl_measures_readability.re_flesch(self.main, text),
                        wl_measures_readability.re_farr_jenkins_paterson(self.main, text),
                        wl_measures_readability.rgl(self.main, text),
                        wl_measures_readability.fuckss_stilcharakteristik(self.main, text),
                        wl_measures_readability.gulpease(self.main, text),
                        wl_measures_readability.fog_index(self.main, text),
                        wl_measures_readability.cp(self.main, text),
                        wl_measures_readability.mu(self.main, text),
                        wl_measures_readability.lensear_write_formula(self.main, text),
                        wl_measures_readability.lix(self.main, text),
                        wl_measures_readability.lorge_readability_index(self.main, text),
                        wl_measures_readability.luong_nguyen_dinhs_readability_formula(self.main, text),
                        wl_measures_readability.eflaw(self.main, text),
                        wl_measures_readability.nwl(self.main, text),
                        wl_measures_readability.nws(self.main, text),
                        wl_measures_readability.osman(self.main, text),
                        wl_measures_readability.rix(self.main, text),
                        wl_measures_readability.smog_grading(self.main, text),
                        wl_measures_readability.spache_readability_formula(self.main, text),
                        wl_measures_readability.strain_index(self.main, text),
                        wl_measures_readability.trankle_bailers_readability_formula(self.main, text),
                        wl_measures_readability.td(self.main, text),
                        wl_measures_readability.wheeler_smiths_readability_formula(self.main, text)
                    ]
                else:
                    stats_readability = None

                if not self._running:
                    raise wl_excs.Wl_Exc_Aborted(self.main)

                tokens = text.get_tokens_flat()
                tokens = wl_nlp_utils.add_missing_ending_tshegs(self.main, tokens, tab = 'profiler')

                if self.tab in ('counts', 'lens', 'len_breakdown', 'all'):
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

                    if text.lang in self.main.settings_global['syl_tokenizers']:
                        syls_tokens = text.get_token_properties('syls', flat = True)

                        # Remove punctuation marks
                        for i, syls in enumerate(syls_tokens):
                            syls_tokens[i] = tuple(syl for syl in syls if not wl_checks_tokens.is_punc(syl))

                        syls_tokens = [syls for syls in syls_tokens if syls]

                        # Token length
                        len_tokens_syls = [len(syls) for syls in syls_tokens]
                        # Type length
                        len_types_syls = [len(syls) for syls in set(syls_tokens)]
                        # Syllable length
                        len_syls = [len(syl) for syls in syls_tokens for syl in syls]
                    else:
                        # Token length
                        len_tokens_syls = None
                        # Type length
                        len_types_syls = None
                        # Syllable length
                        len_syls = None

                    # Token length
                    len_tokens_chars = [len(token) for token in tokens]
                    # Type length
                    len_types_chars = [len(token_type) for token_type in set(tokens)]
                else:
                    len_paras_sentences = None
                    len_paras_sentence_segs = None
                    len_paras_tokens = None
                    len_sentences = None
                    len_sentence_segs = None
                    len_tokens_syls = None
                    # For testing if the text is empty
                    len_tokens_chars = [-1] * len(tokens)
                    len_types_syls = None
                    len_types_chars = None
                    len_syls = None

                if not self._running:
                    raise wl_excs.Wl_Exc_Aborted(self.main)

                # Lexical Density/Diversity
                if self.tab in ('lexical_density_diversity', 'all'):
                    if tokens:
                        stats_lexical_density_diversity = [
                            wl_measures_lexical_density_diversity.brunets_index(self.main, text),
                            wl_measures_lexical_density_diversity.cttr(self.main, text),
                            wl_measures_lexical_density_diversity.fishers_index_of_diversity(self.main, text),
                            wl_measures_lexical_density_diversity.herdans_vm(self.main, text),
                            wl_measures_lexical_density_diversity.hdd(self.main, text),
                            wl_measures_lexical_density_diversity.honores_stat(self.main, text),
                            wl_measures_lexical_density_diversity.lexical_density(self.main, text),
                            wl_measures_lexical_density_diversity.logttr(self.main, text),
                            wl_measures_lexical_density_diversity.msttr(self.main, text),
                            wl_measures_lexical_density_diversity.mtld(self.main, text),
                            wl_measures_lexical_density_diversity.mattr(self.main, text),
                            *wl_measures_lexical_density_diversity.popescu_macutek_altmanns_b1_b2_b3_b4_b5(self.main, text),
                            wl_measures_lexical_density_diversity.popescus_r1(self.main, text),
                            wl_measures_lexical_density_diversity.popescus_r2(self.main, text),
                            wl_measures_lexical_density_diversity.popescus_r3(self.main, text),
                            wl_measures_lexical_density_diversity.popescus_r4(self.main, text),
                            wl_measures_lexical_density_diversity.repeat_rate(self.main, text),
                            wl_measures_lexical_density_diversity.rttr(self.main, text),
                            wl_measures_lexical_density_diversity.shannon_entropy(self.main, text),
                            wl_measures_lexical_density_diversity.simpsons_l(self.main, text),
                            wl_measures_lexical_density_diversity.ttr(self.main, text),
                            wl_measures_lexical_density_diversity.vocdd(self.main, text),
                            wl_measures_lexical_density_diversity.yules_characteristic_k(self.main, text),
                            wl_measures_lexical_density_diversity.yules_index_of_diversity(self.main, text)
                        ]
                    else:
                        stats_lexical_density_diversity = [0] * 28
                else:
                    stats_lexical_density_diversity = None

                if not self._running:
                    raise wl_excs.Wl_Exc_Aborted(self.main)

                # Syntactic Complexity
                if self.tab in ('syntactic_complexity', 'all'):
                    if text.lang in self.main.settings_global['dependency_parsers']:
                        if settings['token_settings']['punc_marks']:
                            dds_sentences = text.dds_sentences.copy()
                            root_dists = text.root_dists.copy()
                        else:
                            dds_sentences = text.dds_sentences_no_punc.copy()
                            root_dists = text.root_dists_no_punc.copy()

                        mdds = wl_measures_syntactic_complexity.mdd(dds_sentences)
                        ndds = wl_measures_syntactic_complexity.ndd(dds_sentences, root_dists)
                    else:
                        dds_sentences = 'no_support'
                        mdds = 'no_support'
                        ndds = 'no_support'
                else:
                    dds_sentences = None
                    mdds = None
                    ndds = None

                self.text_stats_files.append([
                    stats_readability,
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
                    stats_lexical_density_diversity,
                    dds_sentences,
                    mdds,
                    ndds
                ])

            if len(files) == 1:
                self.text_stats_files *= 2
        except wl_excs.Wl_Exc_Aborted:
            self.err_msg = 'aborted'
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Profiler_Table(Wl_Worker_Profiler):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.finished.emit(self.err_msg, self.text_stats_files)
