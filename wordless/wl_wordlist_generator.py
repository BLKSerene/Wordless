# ----------------------------------------------------------------------
# Wordless: Wordlist Generator
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
import traceback

import numpy
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wordless.wl_measures import wl_measures_adjusted_freq, wl_measures_dispersion
from wordless.wl_nlp import wl_texts, wl_token_processing
from wordless.wl_utils import wl_misc, wl_sorting, wl_threading
from wordless.wl_widgets import wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wl_Worker_Wordlist_Generator(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, dict, dict)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.tokens_freq_files = []
        self.tokens_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['wordlist_generator']
            files = list(self.main.wl_file_area.get_selected_files())

            # Frequency
            for file in files:
                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                # Remove empty tokens
                tokens_flat = text.get_tokens_flat()
                tokens = [token for token in tokens_flat if token]

                self.tokens_freq_files.append(collections.Counter(tokens))
                texts.append(text)

            # Total
            if len(files) > 1:
                text_total = wl_texts.Wl_Text_Blank()
                text_total.tokens_multilevel = [
                    copy.deepcopy(para)
                    for text in texts
                    for para in text.tokens_multilevel
                ]

                self.tokens_freq_files.append(sum(self.tokens_freq_files, collections.Counter()))
                texts.append(text_total)

            # Dispersion & Adjusted Frequency
            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            measure_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['func']
            measure_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['func']

            tokens_total = list(self.tokens_freq_files[-1].keys())

            for text in texts:
                tokens_stats_file = {}

                tokens = text.get_tokens_flat()

                # Dispersion
                if measure_dispersion is None:
                    tokens_stats_file = {token: [None] for token in tokens_total}
                else:
                    freqs_sections_tokens = wl_measures_dispersion.to_freq_sections_items(
                        self.main,
                        items_search = tokens_total,
                        items = tokens
                    )

                    for token, freqs in freqs_sections_tokens.items():
                        tokens_stats_file[token] = [measure_dispersion(self.main, freqs)]

                # Adjusted Frequency
                if measure_adjusted_freq is None:
                    tokens_stats_file = {token: stats + [None] for token, stats in tokens_stats_file.items()}
                else:
                    freqs_sections_tokens = wl_measures_adjusted_freq.to_freq_sections_items(
                        self.main,
                        items_search = tokens_total,
                        items = tokens
                    )

                    for token, freqs in freqs_sections_tokens.items():
                        tokens_stats_file[token].append(measure_adjusted_freq(self.main, freqs))

                self.tokens_stats_files.append(tokens_stats_file)

            if len(files) == 1:
                self.tokens_freq_files *= 2
                self.tokens_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Wordlist_Generator_Table(Wl_Worker_Wordlist_Generator):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.tokens_freq_files),
            wl_misc.merge_dicts(self.tokens_stats_files)
        )

class Wl_Worker_Wordlist_Generator_Fig(Wl_Worker_Wordlist_Generator):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering figure...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.tokens_freq_files),
            wl_misc.merge_dicts(self.tokens_stats_files)
        )

class Wl_Table_Wordlist_Generator(wl_tables.Wl_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'wordlist_generator',
            headers = [
                _tr('Wl_Table_Wordlist_Generator', 'Rank'),
                _tr('Wl_Table_Wordlist_Generator', 'Token'),
                _tr('Wl_Table_Wordlist_Generator', 'Number of\nFiles Found'),
                _tr('Wl_Table_Wordlist_Generator', 'Number of\nFiles Found %')
            ],
            headers_int = [
                _tr('Wl_Table_Wordlist_Generator', 'Rank'),
                _tr('Wl_Table_Wordlist_Generator', 'Number of\nFiles Found')
            ],
            headers_pct = [
                _tr('Wl_Table_Wordlist_Generator', 'Number of\nFiles Found %')
            ],
            sorting_enabled = True
        )

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: self.generate_table()) # pylint: disable=unnecessary-lambda
        self.button_generate_fig.clicked.connect(lambda: self.generate_fig()) # pylint: disable=unnecessary-lambda
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())

    def file_changed(self, item): # pylint: disable=unused-argument
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
            self.button_generate_fig.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)
            self.button_generate_fig.setEnabled(False)

    @wl_misc.log_timing
    def generate_table(self):
        worker_wordlist_generator_table = Wl_Worker_Wordlist_Generator_Table(
            self.main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
            update_gui = self.update_gui_table
        )

        wl_threading.Wl_Thread(worker_wordlist_generator_table).start_worker()

    def update_gui_table(self, err_msg, tokens_freq_files, tokens_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, tokens_freq_files):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                settings = self.main.settings_custom['wordlist_generator']

                text_measure_dispersion = settings['generation_settings']['measure_dispersion']
                text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col_text']
                text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col_text']

                self.clr_table()

                # Insert columns (files)
                files = list(self.main.wl_file_area.get_selected_files())

                for file in files:
                    self.ins_header_hor(
                        self.model().columnCount() - 2,
                        _tr('wl_wordlist_generator', '[{}]\nFrequency').format(file['name']),
                        is_int = True, is_cumulative = True, is_breakdown = True
                    )
                    self.ins_header_hor(
                        self.model().columnCount() - 2,
                        _tr('wl_wordlist_generator', '[{}]\nFrequency %').format(file['name']),
                        is_pct = True, is_cumulative = True, is_breakdown = True
                    )

                    if text_dispersion is not None:
                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            f'[{file["name"]}]\n{text_dispersion}',
                            is_float = True, is_breakdown = True
                        )

                    if text_adjusted_freq is not None:
                        self.ins_header_hor(
                            self.model().columnCount() - 2,
                            f'[{file["name"]}]\n{text_adjusted_freq}',
                            is_float = True, is_breakdown = True
                        )

                # Insert columns (total)
                self.ins_header_hor(
                    self.model().columnCount() - 2,
                    _tr('wl_wordlist_generator', 'Total\nFrequency'),
                    is_int = True, is_cumulative = True
                )
                self.ins_header_hor(
                    self.model().columnCount() - 2,
                    _tr('wl_wordlist_generator', 'Total\nFrequency %'),
                    is_pct = True, is_cumulative = True
                )

                if text_dispersion is not None:
                    self.ins_header_hor(
                        self.model().columnCount() - 2,
                        _tr('wl_wordlist_generator', 'Total\n') + text_dispersion,
                        is_float = True
                    )

                if text_adjusted_freq is not None:
                    self.ins_header_hor(
                        self.model().columnCount() - 2,
                        _tr('wl_wordlist_generator', 'Total\n') + text_adjusted_freq,
                        is_float = True
                    )

                # Sort by frequency of the first file
                self.horizontalHeader().setSortIndicator(
                    self.find_header_hor(_tr('wl_wordlist_generator', '[{}]\nFrequency').format(files[0]['name'])),
                    Qt.DescendingOrder
                )

                cols_freq = self.find_headers_hor(_tr('wl_wordlist_generator', '\nFrequency'))
                cols_freq_pct = self.find_headers_hor(_tr('wl_wordlist_generator', '\nFrequency %'))

                for col in cols_freq_pct:
                    cols_freq.remove(col)

                cols_dispersion = self.find_headers_hor(f'\n{text_dispersion}')
                cols_adjusted_freq = self.find_headers_hor(f'\n{text_adjusted_freq}')
                col_files_found = self.find_header_hor(_tr('wl_wordlist_generator', 'Number of\nFiles Found'))
                col_files_found_pct = self.find_header_hor(_tr('wl_wordlist_generator', 'Number of\nFiles Found %'))

                freq_totals = numpy.array(list(tokens_freq_files.values())).sum(axis = 0)
                len_files = len(files)

                self.model().setRowCount(len(tokens_freq_files))
                self.disable_updates()

                for i, (token, freq_files) in enumerate(wl_sorting.sorted_freq_files_items(tokens_freq_files)):
                    stats_files = tokens_stats_files[token]

                    # Rank
                    self.set_item_num(i, 0, -1)

                    # Token
                    self.model().setItem(i, 1, wl_tables.Wl_Table_Item(token))

                    # Frequency
                    for j, freq in enumerate(freq_files):
                        self.set_item_num(i, cols_freq[j], freq)
                        self.set_item_num(i, cols_freq_pct[j], freq, freq_totals[j])

                    for j, (dispersion, adjusted_freq) in enumerate(stats_files):
                        # Dispersion
                        if dispersion is not None:
                            self.set_item_num(i, cols_dispersion[j], dispersion)

                        # Adjusted Frequency
                        if adjusted_freq is not None:
                            self.set_item_num(i, cols_adjusted_freq[j], adjusted_freq)

                    # Number of Files Found
                    num_files_found = len([freq for freq in freq_files[:-1] if freq])

                    self.set_item_num(i, col_files_found, num_files_found)
                    self.set_item_num(i, col_files_found_pct, num_files_found, len_files)

                self.enable_updates()

                self.toggle_pct()
                self.toggle_cumulative()
                self.toggle_breakdown()
                self.update_ranks()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

    @wl_misc.log_timing
    def generate_fig(self):
        self.worker_wordlist_generator_fig = Wl_Worker_Wordlist_Generator_Fig(
            self.main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
            update_gui = self.update_gui_fig
        )

        wl_threading.Wl_Thread(self.worker_wordlist_generator_fig).start_worker()

    def update_gui_fig(self, err_msg, tokens_freq_files, tokens_stats_files):
        if wl_checks_work_area.check_results(self.main, err_msg, tokens_freq_files):
            try:
                settings = self.main.settings_custom['wordlist_generator']

                measure_dispersion = settings['generation_settings']['measure_dispersion']
                measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                col_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['col_text']
                col_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col_text']

                if settings['fig_settings']['use_data'] == _tr('wl_wordlist_generator', 'Frequency'):
                    wl_figs_freqs.wl_fig_freqs(
                        self.main, tokens_freq_files,
                        tab = 'wordlist_generator'
                    )
                else:
                    if settings['fig_settings']['use_data'] == col_dispersion:
                        tokens_stat_files = {
                            token: numpy.array(stats_files)[:, 0]
                            for token, stats_files in tokens_stats_files.items()
                        }
                    elif settings['fig_settings']['use_data'] == col_adjusted_freq:
                        tokens_stat_files = {
                            token: numpy.array(stats_files)[:, 1]
                            for token, stats_files in tokens_stats_files.items()
                        }

                    wl_figs_stats.wl_fig_stats(
                        self.main, tokens_stat_files,
                        tab = 'wordlist_generator'
                    )

                # Hide the progress dialog early so that the main window will not obscure the generated figure
                self.worker_wordlist_generator_fig.dialog_progress.accept()
                wl_figs.show_fig()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_fig(self.main, err_msg)

class Wrapper_Wordlist_Generator(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_wordlist_generator = Wl_Table_Wordlist_Generator(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_wordlist_generator.label_number_results, 0, 0)
        layout_results.addWidget(self.table_wordlist_generator.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_wordlist_generator.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_wordlist_generator, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_wordlist_generator.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_wordlist_generator.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_wordlist_generator.button_exp_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_wordlist_generator.button_exp_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_wordlist_generator.button_clr, 2, 4)

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

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        (
            self.label_measure_dispersion,
            self.combo_box_measure_dispersion,
            self.label_measure_adjusted_freq,
            self.combo_box_measure_adjusted_freq
        ) = wl_widgets.wl_widgets_measures_wordlist_generator(self)

        self.combo_box_measure_dispersion.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_adjusted_freq.currentTextChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_measure_dispersion, 0, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_dispersion, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_adjusted_freq, 2, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_adjusted_freq, 3, 0)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_wordlist_generator]
        )

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        (
            self.label_graph_type,
            self.combo_box_graph_type,
            self.label_sort_by_file,
            self.combo_box_sort_by_file,
            self.label_use_data,
            self.combo_box_use_data,
            self.checkbox_use_pct,
            self.checkbox_use_cumulative
        ) = wl_widgets.wl_widgets_fig_settings(self, tab = 'wordlist_generator')

        self.label_rank = QLabel(self.tr('Rank:'), self)
        (
            self.label_rank_min,
            self.spin_box_rank_min,
            self.checkbox_rank_min_no_limit,
            self.label_rank_max,
            self.spin_box_rank_max,
            self.checkbox_rank_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        self.combo_box_graph_type.currentTextChanged.connect(self.fig_settings_changed)
        self.combo_box_sort_by_file.currentTextChanged.connect(self.fig_settings_changed)
        self.combo_box_use_data.currentTextChanged.connect(self.fig_settings_changed)
        self.checkbox_use_pct.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_use_cumulative.stateChanged.connect(self.fig_settings_changed)

        self.spin_box_rank_min.valueChanged.connect(self.fig_settings_changed)
        self.checkbox_rank_min_no_limit.stateChanged.connect(self.fig_settings_changed)
        self.spin_box_rank_max.valueChanged.connect(self.fig_settings_changed)
        self.checkbox_rank_max_no_limit.stateChanged.connect(self.fig_settings_changed)

        layout_fig_settings_combo_boxes = wl_layouts.Wl_Layout()
        layout_fig_settings_combo_boxes.addWidget(self.label_graph_type, 0, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_graph_type, 0, 1)
        layout_fig_settings_combo_boxes.addWidget(self.label_sort_by_file, 1, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_sort_by_file, 1, 1)
        layout_fig_settings_combo_boxes.addWidget(self.label_use_data, 2, 0)
        layout_fig_settings_combo_boxes.addWidget(self.combo_box_use_data, 2, 1)
        layout_fig_settings_combo_boxes.addWidget(self.checkbox_use_pct, 3, 0, 1, 2)
        layout_fig_settings_combo_boxes.addWidget(self.checkbox_use_cumulative, 4, 0, 1, 2)

        layout_fig_settings_combo_boxes.setColumnStretch(1, 1)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addLayout(layout_fig_settings_combo_boxes, 0, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 3)

        self.group_box_fig_settings.layout().addWidget(self.label_rank, 2, 0, 1, 3)
        self.group_box_fig_settings.layout().addWidget(self.label_rank_min, 3, 0)
        self.group_box_fig_settings.layout().addWidget(self.spin_box_rank_min, 3, 1)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_min_no_limit, 3, 2)
        self.group_box_fig_settings.layout().addWidget(self.label_rank_max, 4, 0)
        self.group_box_fig_settings.layout().addWidget(self.spin_box_rank_max, 4, 1)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_rank_max_no_limit, 4, 2)

        self.group_box_fig_settings.layout().setColumnStretch(1, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 3, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['wordlist_generator'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['wordlist_generator'])

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

        # Generation Settings
        self.combo_box_measure_dispersion.setCurrentText(settings['generation_settings']['measure_dispersion'])
        self.combo_box_measure_adjusted_freq.setCurrentText(settings['generation_settings']['measure_adjusted_freq'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        # Figure Settings
        self.combo_box_graph_type.setCurrentText(settings['fig_settings']['graph_type'])
        self.combo_box_sort_by_file.setCurrentText(settings['fig_settings']['sort_by_file'])
        self.combo_box_use_data.setCurrentText(settings['fig_settings']['use_data'])
        self.checkbox_use_pct.setChecked(settings['fig_settings']['use_pct'])
        self.checkbox_use_cumulative.setChecked(settings['fig_settings']['use_cumulative'])

        self.spin_box_rank_min.setValue(settings['fig_settings']['rank_min'])
        self.checkbox_rank_min_no_limit.setChecked(settings['fig_settings']['rank_min_no_limit'])
        self.spin_box_rank_max.setValue(settings['fig_settings']['rank_max'])
        self.checkbox_rank_max_no_limit.setChecked(settings['fig_settings']['rank_max_no_limit'])

        self.token_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['wordlist_generator']['token_settings']

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

    def generation_settings_changed(self):
        settings = self.main.settings_custom['wordlist_generator']['generation_settings']

        settings['measure_dispersion'] = self.combo_box_measure_dispersion.currentText()
        settings['measure_adjusted_freq'] = self.combo_box_measure_adjusted_freq.currentText()

        # Use Data
        self.combo_box_use_data.measures_changed()

    def table_settings_changed(self):
        settings = self.main.settings_custom['wordlist_generator']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['wordlist_generator']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['sort_by_file'] = self.combo_box_sort_by_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()
