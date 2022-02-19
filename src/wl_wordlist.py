# ----------------------------------------------------------------------
# Wordless: Wordlist
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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_checking import wl_checking_files
from wl_dialogs import wl_dialogs_errs, wl_dialogs_misc, wl_msg_boxes
from wl_figs import wl_figs, wl_figs_freqs, wl_figs_stats
from wl_nlp import wl_nlp_utils, wl_texts, wl_token_processing
from wl_utils import wl_misc, wl_msgs, wl_sorting, wl_threading
from wl_widgets import wl_layouts, wl_tables, wl_widgets

class Wl_Table_Wordlist(wl_tables.Wl_Table_Data_Filter_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'wordlist',
            headers = [
                parent.tr('Rank'),
                parent.tr('Token'),
                parent.tr('Number of\nFiles Found'),
                parent.tr('Number of\nFiles Found %')
            ],
            headers_int = [
                parent.tr('Rank'),
                parent.tr('Number of\nFiles Found')
            ],
            headers_pct = [
                parent.tr('Number of\nFiles Found %')
            ],
            sorting_enabled = True
        )

        self.name = 'wordlist'

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))
        self.button_generate_fig.clicked.connect(lambda: generate_fig(self.main))

class Wrapper_Wordlist(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_wordlist = Wl_Table_Wordlist(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_wordlist.label_number_results, 0, 0)
        layout_results.addWidget(self.table_wordlist.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_wordlist.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_wordlist, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_wordlist.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_wordlist.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_wordlist.button_exp_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_wordlist.button_exp_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_wordlist.button_clr, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_words,
            self.checkbox_lowercase,
            self.checkbox_uppercase,
            self.checkbox_title_case,
            self.checkbox_nums,
            self.checkbox_puncs,

            self.checkbox_treat_as_lowercase,
            self.checkbox_lemmatize_tokens,
            self.checkbox_filter_stop_words,

            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings(self)

        self.checkbox_words.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_uppercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_title_case.stateChanged.connect(self.token_settings_changed)
        self.checkbox_nums.stateChanged.connect(self.token_settings_changed)
        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.checkbox_treat_as_lowercase.stateChanged.connect(self.token_settings_changed)
        self.checkbox_lemmatize_tokens.stateChanged.connect(self.token_settings_changed)
        self.checkbox_filter_stop_words.stateChanged.connect(self.token_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 2, 1)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lemmatize_tokens, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 8, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 8, 1)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'))

        (
            self.label_measure_dispersion,
            self.combo_box_measure_dispersion
        ) = wl_widgets.wl_widgets_measure_dispersion(self)
        (
            self.label_measure_adjusted_freq,
            self.combo_box_measure_adjusted_freq
        ) = wl_widgets.wl_widgets_measure_adjusted_freq(self)

        (
            self.label_settings_measures,
            self.button_settings_measures
        ) = wl_widgets.wl_widgets_settings_measures(
            self,
            node = self.tr('Dispersion')
        )

        self.combo_box_measure_dispersion.currentTextChanged.connect(self.generation_settings_changed)
        self.combo_box_measure_adjusted_freq.currentTextChanged.connect(self.generation_settings_changed)

        layout_settings_measures = wl_layouts.Wl_Layout()
        layout_settings_measures.addWidget(self.label_settings_measures, 0, 0)
        layout_settings_measures.addWidget(self.button_settings_measures, 0, 1)

        layout_settings_measures.setColumnStretch(1, 1)

        self.group_box_generation_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_measure_dispersion, 0, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_dispersion, 1, 0)
        self.group_box_generation_settings.layout().addWidget(self.label_measure_adjusted_freq, 2, 0)
        self.group_box_generation_settings.layout().addWidget(self.combo_box_measure_adjusted_freq, 3, 0)

        self.group_box_generation_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 4, 0)

        self.group_box_generation_settings.layout().addLayout(layout_settings_measures, 5, 0)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'))

        (
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_wordlist]
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
        ) = wl_widgets.wl_widgets_fig_settings(self)

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

        self.wrapper_settings.layout().setRowStretch(4, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['wordlist'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['wordlist'])

        # Token Settings
        self.checkbox_words.setChecked(settings['token_settings']['words'])
        self.checkbox_lowercase.setChecked(settings['token_settings']['lowercase'])
        self.checkbox_uppercase.setChecked(settings['token_settings']['uppercase'])
        self.checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        self.checkbox_nums.setChecked(settings['token_settings']['nums'])
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        self.checkbox_treat_as_lowercase.setChecked(settings['token_settings']['treat_as_lowercase'])
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
        settings = self.main.settings_custom['wordlist']['token_settings']

        settings['words'] = self.checkbox_words.isChecked()
        settings['lowercase'] = self.checkbox_lowercase.isChecked()
        settings['uppercase'] = self.checkbox_uppercase.isChecked()
        settings['title_case'] = self.checkbox_title_case.isChecked()
        settings['nums'] = self.checkbox_nums.isChecked()
        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['treat_as_lowercase'] = self.checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize_tokens'] = self.checkbox_lemmatize_tokens.isChecked()
        settings['filter_stop_words'] = self.checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['wordlist']['generation_settings']

        settings['measure_dispersion'] = self.combo_box_measure_dispersion.currentText()
        settings['measure_adjusted_freq'] = self.combo_box_measure_adjusted_freq.currentText()

        # Use Data
        use_data_old = self.combo_box_use_data.currentText()

        text_measure_dispersion = settings['measure_dispersion']
        text_measure_adjusted_freq = settings['measure_adjusted_freq']

        self.combo_box_use_data.clear()

        self.combo_box_use_data.addItem(self.tr('Frequency'))
        self.combo_box_use_data.addItem(self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col'])
        self.combo_box_use_data.addItem(self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col'])

        if self.combo_box_use_data.findText(use_data_old) > -1:
            self.combo_box_use_data.setCurrentText(use_data_old)
        else:
            self.combo_box_use_data.setCurrentText(self.main.settings_default['wordlist']['fig_settings']['use_data'])

    def table_settings_changed(self):
        settings = self.main.settings_custom['wordlist']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['wordlist']['fig_settings']

        settings['graph_type'] = self.combo_box_graph_type.currentText()
        settings['sort_by_file'] = self.combo_box_sort_by_file.currentText()
        settings['use_data'] = self.combo_box_use_data.currentText()
        settings['use_pct'] = self.checkbox_use_pct.isChecked()
        settings['use_cumulative'] = self.checkbox_use_cumulative.isChecked()

        settings['rank_min'] = self.spin_box_rank_min.value()
        settings['rank_min_no_limit'] = self.checkbox_rank_min_no_limit.isChecked()
        settings['rank_max'] = self.spin_box_rank_max.value()
        settings['rank_max_no_limit'] = self.checkbox_rank_max_no_limit.isChecked()

class Wl_Worker_Wordlist(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, dict, dict)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.err_msg = ''
        self.tokens_freq_files = []
        self.tokens_stats_files = []

    def run(self):
        try:
            texts = []

            settings = self.main.settings_custom['wordlist']
            files = list(self.main.wl_file_area.get_selected_files())

            # Frequency
            for file in files:
                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens_wordlist(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                # Remove empty tokens
                tokens = [token for token in text.tokens_flat if token]

                self.tokens_freq_files.append(collections.Counter(tokens))
                texts.append(text)

            # Total
            if len(files) > 1:
                text_total = wl_texts.Wl_Text_Blank()
                text_total.tokens_flat = [token for text in texts for token in text.tokens_flat]

                self.tokens_freq_files.append(sum(self.tokens_freq_files, collections.Counter()))
                texts.append(text_total)

            # Dispersion & Adjusted Frequency
            text_measure_dispersion = settings['generation_settings']['measure_dispersion']
            text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

            measure_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['func']
            measure_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['func']

            tokens_total = self.tokens_freq_files[-1].keys()

            for text in texts:
                tokens_stats_file = {}

                # Dispersion
                number_sections = self.main.settings_custom['measures']['dispersion']['general']['number_sections']

                sections_freq = [
                    collections.Counter(section)
                    for section in wl_nlp_utils.to_sections(text.tokens_flat, number_sections)
                ]

                for token in tokens_total:
                    counts = [section_freq[token] for section_freq in sections_freq]

                    tokens_stats_file[token] = [measure_dispersion(counts)]

                # Adjusted Frequency
                if not self.main.settings_custom['measures']['adjusted_freq']['general']['use_same_settings_dispersion']:
                    number_sections = self.main.settings_custom['measures']['adjusted_freq']['general']['number_sections']

                    sections_freq = [
                        collections.Counter(section)
                        for section in wl_nlp_utils.to_sections(text.tokens_flat, number_sections)
                    ]

                for token in tokens_total:
                    counts = [section_freq[token] for section_freq in sections_freq]

                    tokens_stats_file[token].append(measure_adjusted_freq(counts))

                self.tokens_stats_files.append(tokens_stats_file)

            if len(files) == 1:
                self.tokens_freq_files *= 2
                self.tokens_stats_files *= 2
        except Exception:
            self.err_msg = traceback.format_exc()

class Wl_Worker_Wordlist_Table(Wl_Worker_Wordlist):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.tokens_freq_files),
            wl_misc.merge_dicts(self.tokens_stats_files)
        )

class Wl_Worker_Wordlist_Fig(Wl_Worker_Wordlist):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering figure...'))
        self.worker_done.emit(
            self.err_msg,
            wl_misc.merge_dicts(self.tokens_freq_files),
            wl_misc.merge_dicts(self.tokens_stats_files)
        )

@wl_misc.log_timing
def generate_table(main, table):
    def update_gui(err_msg, tokens_freq_files, tokens_stats_files):
        if not err_msg:
            if tokens_freq_files:
                table.settings = copy.deepcopy(main.settings_custom)

                text_measure_dispersion = settings['generation_settings']['measure_dispersion']
                text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                text_dispersion = main.settings_global['measures_dispersion'][text_measure_dispersion]['col']
                text_adjusted_freq = main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col']

                if settings['token_settings']['use_tags']:
                    table.horizontalHeaderItem(1).setText(main.tr('Tag'))

                table.clr_table()

                # Insert columns (files)
                for file in files:
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        main.tr(f'[{file["name"]}]\nFrequency'),
                        is_int = True, is_cumulative = True, is_breakdown = True
                    )
                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        main.tr(f'[{file["name"]}]\nFrequency %'),
                        is_pct = True, is_cumulative = True, is_breakdown = True
                    )

                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        main.tr(f'[{file["name"]}]\n{text_dispersion}'),
                        is_float = True, is_breakdown = True
                    )

                    table.ins_header_hor(
                        table.model().columnCount() - 2,
                        main.tr(f'[{file["name"]}]\n{text_adjusted_freq}'),
                        is_float = True, is_breakdown = True
                    )

                # Insert columns (total)
                table.ins_header_hor(
                    table.model().columnCount() - 2,
                    main.tr('Total\nFrequency'),
                    is_int = True, is_cumulative = True
                )
                table.ins_header_hor(
                    table.model().columnCount() - 2,
                    main.tr('Total\nFrequency %'),
                    is_pct = True, is_cumulative = True
                )

                table.ins_header_hor(
                    table.model().columnCount() - 2,
                    main.tr(f'Total\n{text_dispersion}'),
                    is_float = True
                )

                table.ins_header_hor(
                    table.model().columnCount() - 2,
                    main.tr(f'Total\n{text_adjusted_freq}'),
                    is_float = True
                )

                # Sort by frequency of the first file
                table.horizontalHeader().setSortIndicator(
                    table.find_header_hor(main.tr(f'[{files[0]["name"]}]\nFrequency')),
                    Qt.DescendingOrder
                )

                cols_freq = table.find_headers_hor(main.tr('\nFrequency'))
                cols_freq_pct = table.find_headers_hor(main.tr('\nFrequency %'))

                for col in cols_freq_pct:
                    cols_freq.remove(col)

                cols_dispersion = table.find_headers_hor(main.tr(f'\n{text_dispersion}'))
                cols_adjusted_freq = table.find_headers_hor(main.tr(f'\n{text_adjusted_freq}'))
                col_files_found = table.find_header_hor(main.tr('Number of\nFiles Found'))
                col_files_found_pct = table.find_header_hor(main.tr('Number of\nFiles Found %'))

                freq_totals = numpy.array(list(tokens_freq_files.values())).sum(axis = 0)
                len_files = len(files)

                table.model().setRowCount(len(tokens_freq_files))

                table.disable_updates()

                for i, (token, freq_files) in enumerate(wl_sorting.sorted_tokens_freq_files(tokens_freq_files)):
                    stats_files = tokens_stats_files[token]

                    # Rank
                    table.set_item_num(i, 0, -1)

                    # Token
                    table.model().setItem(i, 1, wl_tables.Wl_Table_Item(token))

                    # Frequency
                    for j, freq in enumerate(freq_files):
                        table.set_item_num(i, cols_freq[j], freq)
                        table.set_item_num(i, cols_freq_pct[j], freq, freq_totals[j])

                    for j, (dispersion, adjusted_freq) in enumerate(stats_files):
                        # Dispersion
                        table.set_item_num(i, cols_dispersion[j], dispersion)

                        # Adjusted Frequency
                        table.set_item_num(i, cols_adjusted_freq[j], adjusted_freq)

                    # Number of Files Found
                    num_files_found = len([freq for freq in freq_files[:-1] if freq])

                    table.set_item_num(i, col_files_found, num_files_found)
                    table.set_item_num(i, col_files_found_pct, num_files_found, len_files)

                table.enable_updates()

                table.toggle_pct()
                table.toggle_cumulative()
                table.toggle_breakdown()
                table.update_ranks()

                wl_msgs.wl_msg_generate_table_success(main)
            else:
                wl_msg_boxes.wl_msg_box_no_results(main)

                wl_msgs.wl_msg_generate_table_error(main)
        else:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()

            wl_msgs.wl_msg_fatal_error(main)

    settings = main.settings_custom['wordlist']
    files = list(main.wl_file_area.get_selected_files())

    if wl_checking_files.check_files_on_loading(main, files):
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main)

        worker_wordlist_table = Wl_Worker_Wordlist_Table(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui
        )

        thread_wordlist_table = wl_threading.Wl_Thread(worker_wordlist_table)
        thread_wordlist_table.start_worker()
    else:
        wl_msgs.wl_msg_generate_table_error(main)

@wl_misc.log_timing
def generate_fig(main):
    def update_gui(err_msg, tokens_freq_files, tokens_stats_files):
        if not err_msg:
            if tokens_freq_files:
                measure_dispersion = settings['generation_settings']['measure_dispersion']
                measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

                col_dispersion = main.settings_global['measures_dispersion'][measure_dispersion]['col']
                col_adjusted_freq = main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col']

                if settings['fig_settings']['use_data'] == main.tr('Frequency'):
                    wl_figs_freqs.wl_fig_freq(
                        main, tokens_freq_files,
                        settings = settings['fig_settings'],
                        label_x = main.tr('Token')
                    )
                else:
                    if settings['fig_settings']['use_data'] == col_dispersion:
                        tokens_stat_files = {
                            token: numpy.array(stats_files)[:, 0]
                            for token, stats_files in tokens_stats_files.items()
                        }

                        label_y = col_dispersion
                    elif settings['fig_settings']['use_data'] == col_adjusted_freq:
                        tokens_stat_files = {
                            token: numpy.array(stats_files)[:, 1]
                            for token, stats_files in tokens_stats_files.items()
                        }

                        label_y = col_adjusted_freq

                    wl_figs_stats.wl_fig_stat(
                        main, tokens_stat_files,
                        settings = settings['fig_settings'],
                        label_x = main.tr('Token'),
                        label_y = label_y
                    )

                wl_msgs.wl_msg_generate_fig_success(main)
            else:
                wl_msg_boxes.wl_msg_box_no_results(main)

                wl_msgs.wl_msg_generate_fig_error(main)
        else:
            wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).open()

            wl_msgs.wl_msg_fatal_error(main)

        dialog_progress.accept()

        if tokens_freq_files:
            wl_figs.show_fig()

    settings = main.settings_custom['wordlist']
    files = list(main.wl_file_area.get_selected_files())

    if wl_checking_files.check_files_on_loading(main, files):
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main)

        worker_wordlist_fig = Wl_Worker_Wordlist_Fig(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui
        )

        thread_wordlist_fig = wl_threading.Wl_Thread(worker_wordlist_fig)
        thread_wordlist_fig.start_worker()
    else:
        wl_msgs.wl_msg_generate_table_error(main)
