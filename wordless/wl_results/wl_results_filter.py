# ----------------------------------------------------------------------
# Wordless: Results - Filter
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

import copy

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QLabel, QPushButton

from wordless.wl_dialogs import wl_dialogs, wl_dialogs_misc
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_boxes, wl_buttons, wl_layouts, wl_widgets

_tr = QCoreApplication.translate

class Wl_Worker_Results_Filter_Wordlist_Generator(wl_threading.Wl_Worker):
    def run(self):
        text_measure_dispersion = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col_text']
        text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col_text']

        if self.dialog.tab == 'wordlist_generator':
            col_token = self.dialog.table.find_header_hor(self.tr('Token'))
        elif self.dialog.tab == 'ngram_generator':
            col_ngram = self.dialog.table.find_header_hor(self.tr('N-gram'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            col_freq = self.dialog.table.find_header_hor(
                self.tr('Total\nFrequency')
            )
            col_dispersion = self.dialog.table.find_header_hor(
                self.tr('Total\n') + text_dispersion
            )
            col_adjusted_freq = self.dialog.table.find_header_hor(
                self.tr('Total\n') + text_adjusted_freq
            )
        else:
            col_freq = self.dialog.table.find_header_hor(
                self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
            )
            col_dispersion = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{text_dispersion}"
            )
            col_adjusted_freq = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{text_adjusted_freq}"
            )

        col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

        if self.dialog.tab == 'wordlist_generator':
            len_token_min = (
                float('-inf')
                if self.dialog.settings['len_token_min_no_limit']
                else self.dialog.settings['len_token_min']
            )
            len_token_max = (
                float('inf')
                if self.dialog.settings['len_token_max_no_limit']
                else self.dialog.settings['len_token_max']
            )
        elif self.dialog.tab == 'ngram_generator':
            len_ngram_min = (
                float('-inf')
                if self.dialog.settings['len_ngram_min_no_limit']
                else self.dialog.settings['len_ngram_min']
            )
            len_ngram_max = (
                float('inf')
                if self.dialog.settings['len_ngram_max_no_limit']
                else self.dialog.settings['len_ngram_max']
            )

        freq_min = (
            float('-inf')
            if self.dialog.settings['freq_min_no_limit']
            else self.dialog.settings['freq_min']
        )
        freq_max = (
            float('inf')
            if self.dialog.settings['freq_max_no_limit']
            else self.dialog.settings['freq_max']
        )

        dispersion_min = (
            float('-inf')
            if self.dialog.settings['dispersion_min_no_limit']
            else self.dialog.settings['dispersion_min']
        )
        dispersion_max = (
            float('inf')
            if self.dialog.settings['dispersion_max_no_limit']
            else self.dialog.settings['dispersion_max']
        )

        adjusted_freq_min = (
            float('-inf')
            if self.dialog.settings['adjusted_freq_min_no_limit']
            else self.dialog.settings['adjusted_freq_min']
        )
        adjusted_freq_max = (
            float('inf')
            if self.dialog.settings['adjusted_freq_max_no_limit']
            else self.dialog.settings['adjusted_freq_max']
        )

        num_files_found_min = (
            float('-inf')
            if self.dialog.settings['num_files_found_min_no_limit']
            else self.dialog.settings['num_files_found_min']
        )
        num_files_found_max = (
            float('inf')
            if self.dialog.settings['num_files_found_max_no_limit']
            else self.dialog.settings['num_files_found_max']
        )

        self.dialog.table.row_filters = []

        if self.dialog.tab == 'wordlist_generator':
            for i in range(self.dialog.table.model().rowCount()):
                if (
                    len_token_min <= len(self.dialog.table.model().item(i, col_token).text()) <= len_token_max
                    and freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
                    and dispersion_min <= self.dialog.table.model().item(i, col_dispersion).val <= dispersion_max
                    and adjusted_freq_min <= self.dialog.table.model().item(i, col_adjusted_freq).val <= adjusted_freq_max
                    and num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
                ):
                    self.dialog.table.row_filters.append(True)
                else:
                    self.dialog.table.row_filters.append(False)
        elif self.dialog.tab == 'ngram_generator':
            for i in range(self.dialog.table.model().rowCount()):
                if (
                    len_ngram_min <= len(self.dialog.table.model().item(i, col_ngram).text()) <= len_ngram_max
                    and freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
                    and dispersion_min <= self.dialog.table.model().item(i, col_dispersion).val <= dispersion_max
                    and adjusted_freq_min <= self.dialog.table.model().item(i, col_adjusted_freq).val <= adjusted_freq_max
                    and num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
                ):
                    self.dialog.table.row_filters.append(True)
                else:
                    self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit()

class Wl_Worker_Results_Filter_Collocation_Extractor(wl_threading.Wl_Worker):
    def run(self):
        test_statistical_significance = self.dialog.table.settings[self.dialog.tab]['generation_settings']['test_statistical_significance']
        measure_effect_size = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_effect_size']

        text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        col_collocate = self.dialog.table.find_header_hor(self.tr('Collocate'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_header_hor(
                    self.tr('Total\nFrequency')
                )
            else:
                col_freq = self.dialog.table.find_header_hor(
                    self.tr('Total\n') + self.dialog.settings['freq_position']
                )

            if text_test_stat:
                col_test_stat = self.dialog.table.find_header_hor(self.tr('Total\n') + text_test_stat)

            col_p_value = self.dialog.table.find_header_hor(self.tr('Total\np-value'))
            col_bayes_factor = self.dialog.table.find_header_hor(self.tr('Total\nBayes Factor'))
            col_effect_size = self.dialog.table.find_header_hor(self.tr('Total\n') + text_effect_size)
        else:
            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_header_hor(
                    self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
                )
            else:
                col_freq = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.settings['freq_position']}"
                )

            if text_test_stat:
                col_test_stat = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{text_test_stat}"
                )

            col_p_value = self.dialog.table.find_header_hor(
                self.tr('[{}]\np-value').format(self.dialog.settings['file_to_filter'])
            )
            col_bayes_factor = self.dialog.table.find_header_hor(
                self.tr('[{}]\nBayes Factor').format(self.dialog.settings['file_to_filter'])
            )
            col_effect_size = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{text_effect_size}"
            )

        col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

        len_collocate_min = (
            float('-inf')
            if self.dialog.settings['len_collocate_min_no_limit']
            else self.dialog.settings['len_collocate_min']
        )
        len_collocate_max = (
            float('inf')
            if self.dialog.settings['len_collocate_max_no_limit']
            else self.dialog.settings['len_collocate_max']
        )

        freq_min = (
            float('-inf')
            if self.dialog.settings['freq_min_no_limit']
            else self.dialog.settings['freq_min']
        )
        freq_max = (
            float('inf')
            if self.dialog.settings['freq_max_no_limit']
            else self.dialog.settings['freq_max']
        )

        test_stat_min = (
            float('-inf')
            if self.dialog.settings['test_stat_min_no_limit']
            else self.dialog.settings['test_stat_min']
        )
        test_stat_max = (
            float('inf')
            if self.dialog.settings['test_stat_max_no_limit']
            else self.dialog.settings['test_stat_max']
        )

        p_val_min = (
            float('-inf')
            if self.dialog.settings['p_val_min_no_limit']
            else self.dialog.settings['p_val_min']
        )
        p_val_max = (
            float('inf')
            if self.dialog.settings['p_val_max_no_limit']
            else self.dialog.settings['p_val_max']
        )

        bayes_factor_min = (
            float('-inf')
            if self.dialog.settings['bayes_factor_min_no_limit']
            else self.dialog.settings['bayes_factor_min']
        )
        bayes_factor_max = (
            float('inf')
            if self.dialog.settings['bayes_factor_max_no_limit']
            else self.dialog.settings['bayes_factor_max']
        )

        effect_size_min = (
            float('-inf')
            if self.dialog.settings['effect_size_min_no_limit']
            else self.dialog.settings['effect_size_min']
        )
        effect_size_max = (
            float('inf')
            if self.dialog.settings['effect_size_max_no_limit']
            else self.dialog.settings['effect_size_max']
        )

        num_files_found_min = (
            float('-inf')
            if self.dialog.settings['num_files_found_min_no_limit']
            else self.dialog.settings['num_files_found_min']
        )
        num_files_found_max = (
            float('inf')
            if self.dialog.settings['num_files_found_max_no_limit']
            else self.dialog.settings['num_files_found_max']
        )

        self.dialog.table.row_filters = []

        for i in range(self.dialog.table.model().rowCount()):
            if text_test_stat:
                filter_test_stat = test_stat_min <= self.dialog.table.model().item(i, col_test_stat).val <= test_stat_max
            else:
                filter_test_stat = True

            if (
                len_collocate_min <= len(self.dialog.table.model().item(i, col_collocate).text()) <= len_collocate_max
                and freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
                and filter_test_stat
                and p_val_min <= self.dialog.table.model().item(i, col_p_value).val <= p_val_max
                and bayes_factor_min <= self.dialog.table.model().item(i, col_bayes_factor).val <= bayes_factor_max
                and effect_size_min <= self.dialog.table.model().item(i, col_effect_size).val <= effect_size_max
                and num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
            ):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit()

class Wl_Worker_Results_Filter_Keyword_Extractor(wl_threading.Wl_Worker):
    def run(self):
        test_statistical_significance = self.dialog.table.settings['keyword_extractor']['generation_settings']['test_statistical_significance']
        measure_effect_size = self.dialog.table.settings['keyword_extractor']['generation_settings']['measure_effect_size']

        text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        col_keyword = self.dialog.table.find_header_hor(self.tr('Keyword'))

        if self.dialog.settings['file_to_filter'] == self.tr('Total'):
            col_freq = self.dialog.table.find_header_hor(self.tr('Total\nFrequency'))

            if text_test_stat:
                col_test_stat = self.dialog.table.find_header_hor(self.tr('Total\n') + text_test_stat)

            col_p_val = self.dialog.table.find_header_hor(self.tr('Total\np-value'))
            col_bayes_factor = self.dialog.table.find_header_hor(self.tr('Total\nBayes Factor'))
            col_effect_size = self.dialog.table.find_header_hor(self.tr('Total\n') + text_effect_size)
        else:
            col_freq = self.dialog.table.find_header_hor(
                self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
            )

            if text_test_stat:
                col_test_stat = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{text_test_stat}"
                )

            col_p_val = self.dialog.table.find_header_hor(
                self.tr('[{}]\np-value').format(self.dialog.settings['file_to_filter'])
            )
            col_bayes_factor = self.dialog.table.find_header_hor(
                self.tr('[{}]\nBayes Factor').format(self.dialog.settings['file_to_filter'])
            )
            col_effect_size = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{text_effect_size}"
            )

        col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

        len_keyword_min = (
            float('-inf')
            if self.dialog.settings['len_keyword_min_no_limit']
            else self.dialog.settings['len_keyword_min']
        )
        len_keyword_max = (
            float('inf')
            if self.dialog.settings['len_keyword_max_no_limit']
            else self.dialog.settings['len_keyword_max']
        )

        freq_min = (
            float('-inf')
            if self.dialog.settings['freq_min_no_limit']
            else self.dialog.settings['freq_min']
        )
        freq_max = (
            float('inf')
            if self.dialog.settings['freq_max_no_limit']
            else self.dialog.settings['freq_max']
        )

        test_stat_min = (
            float('-inf')
            if self.dialog.settings['test_stat_min_no_limit']
            else self.dialog.settings['test_stat_min']
        )
        test_stat_max = (
            float('inf')
            if self.dialog.settings['test_stat_max_no_limit']
            else self.dialog.settings['test_stat_max']
        )

        p_val_min = (
            float('-inf')
            if self.dialog.settings['p_val_min_no_limit']
            else self.dialog.settings['p_val_min']
        )
        p_val_max = (
            float('inf')
            if self.dialog.settings['p_val_max_no_limit']
            else self.dialog.settings['p_val_max']
        )

        bayes_factor_min = (
            float('-inf')
            if self.dialog.settings['bayes_factor_min_no_limit']
            else self.dialog.settings['bayes_factor_min']
        )
        bayes_factor_max = (
            float('inf')
            if self.dialog.settings['bayes_factor_max_no_limit']
            else self.dialog.settings['bayes_factor_max']
        )

        effect_size_min = (
            float('-inf')
            if self.dialog.settings['effect_size_min_no_limit']
            else self.dialog.settings['effect_size_min']
        )
        effect_size_max = (
            float('inf')
            if self.dialog.settings['effect_size_max_no_limit']
            else self.dialog.settings['effect_size_max']
        )

        num_files_found_min = (
            float('-inf')
            if self.dialog.settings['num_files_found_min_no_limit']
            else self.dialog.settings['num_files_found_min']
        )
        num_files_found_max = (
            float('inf')
            if self.dialog.settings['num_files_found_max_no_limit']
            else self.dialog.settings['num_files_found_max']
        )

        self.dialog.table.row_filters = []

        for i in range(self.dialog.table.model().rowCount()):
            if text_test_stat:
                filter_test_stat = test_stat_min <= self.dialog.table.model().item(i, col_test_stat).val <= test_stat_max
            else:
                filter_test_stat = True

            if (
                len_keyword_min <= len(self.dialog.table.model().item(i, col_keyword).text()) <= len_keyword_max
                and freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
                and filter_test_stat
                and p_val_min <= self.dialog.table.model().item(i, col_p_val).val <= p_val_max
                and bayes_factor_min <= self.dialog.table.model().item(i, col_bayes_factor).val <= bayes_factor_max
                and effect_size_min <= self.dialog.table.model().item(i, col_effect_size).val <= effect_size_max
                and num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
            ):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit()

class Wl_Dialog_Results_Filter(wl_dialogs.Wl_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, _tr('Wl_Dialog_Results_Filter', 'Filter Results'))

        self.tab = tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['filter_results']

        self.main.wl_work_area.currentChanged.connect(self.reject)

        self.label_file_to_filter = QLabel(_tr('Wl_Dialog_Results_Filter', 'File to Filter:'), self)
        self.combo_box_file_to_filter = wl_boxes.Wl_Combo_Box_File_To_Filter(self, self.table)
        self.button_filter = QPushButton(_tr('Wl_Dialog_Results_Filter', 'Filter'), self)

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)
        self.button_close = QPushButton(_tr('Wl_Dialog_Results_Filter', 'Close'), self)

        self.combo_box_file_to_filter.currentTextChanged.connect(self.file_to_filter_changed)
        self.button_filter.clicked.connect(lambda: self.filter_results()) # pylint: disable=unnecessary-lambda
        self.button_close.clicked.connect(self.reject)

        layout_file_to_filter = wl_layouts.Wl_Layout()
        layout_file_to_filter.addWidget(self.label_file_to_filter, 0, 0)
        layout_file_to_filter.addWidget(self.combo_box_file_to_filter, 0, 1)
        layout_file_to_filter.addWidget(self.button_filter, 0, 2)

        layout_file_to_filter.setColumnStretch(1, 1)

        self.layout_filters = wl_layouts.Wl_Layout()

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_defaults, 0, 0)
        layout_buttons.addWidget(self.button_close, 0, 2)

        layout_buttons.setColumnStretch(1, 1)

        self.setLayout(wl_layouts.Wl_Layout())
        self.layout().addLayout(layout_file_to_filter, 0, 0)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0)
        self.layout().addLayout(self.layout_filters, 2, 0)

        self.layout().addWidget(wl_layouts.Wl_Separator(self), 3, 0)
        self.layout().addLayout(layout_buttons, 4, 0)

        self.set_fixed_size()

    def load_settings(self, defaults = False):
        if defaults:
            settings = self.main.settings_default[self.tab]['filter_results']
        else:
            settings = self.settings

        self.combo_box_file_to_filter.setCurrentText(settings['file_to_filter'])

    def file_to_filter_changed(self):
        self.settings['file_to_filter'] = self.combo_box_file_to_filter.currentText()

    @wl_misc.log_timing
    def filter_results(self):
        def update_gui():
            self.table.filter_table()

            self.main.statusBar().showMessage(_tr('Wl_Dialog_Results_Filter', 'The results in the table has been successfully filtered.'))

        worker_filter_results = self.Worker_Filter_Results(
            self.main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = _tr('Wl_Dialog_Results_Filter', 'Filtering results...')),
            update_gui = update_gui,
            dialog = self
        )
        wl_threading.Wl_Thread(worker_filter_results).start_worker()

class Wl_Dialog_Results_Filter_Wordlist_Generator(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Wordlist_Generator

        if self.tab == 'wordlist_generator':
            self.label_len_token = QLabel(self.tr('Token Length:'), self)
            (
                self.label_len_token_min,
                self.spin_box_len_token_min,
                self.checkbox_len_token_min_no_limit,
                self.label_len_token_max,
                self.spin_box_len_token_max,
                self.checkbox_len_token_max_no_limit
            ) = wl_widgets.wl_widgets_filter(
                self,
                filter_min = 1,
                filter_max = 100
            )
        elif self.tab == 'ngram_generator':
            self.label_len_ngram = QLabel(self.tr('N-gram Length:'), self)
            (
                self.label_len_ngram_min,
                self.spin_box_len_ngram_min,
                self.checkbox_len_ngram_min_no_limit,
                self.label_len_ngram_max,
                self.spin_box_len_ngram_max,
                self.checkbox_len_ngram_max_no_limit
            ) = wl_widgets.wl_widgets_filter(
                self,
                filter_min = 1,
                filter_max = 100
            )

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (
            self.label_freq_min,
            self.spin_box_freq_min,
            self.checkbox_freq_min_no_limit,
            self.label_freq_max,
            self.spin_box_freq_max,
            self.checkbox_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_dispersion = QLabel(self.tr('Dispersion:'), self)
        (
            self.label_dispersion_min,
            self.spin_box_dispersion_min,
            self.checkbox_dispersion_min_no_limit,
            self.label_dispersion_max,
            self.spin_box_dispersion_max,
            self.checkbox_dispersion_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(
            self,
            filter_min = 0,
            filter_max = 1
        )

        self.label_adjusted_freq = QLabel(self.tr('Adjusted Frequency:'), self)
        (
            self.label_adjusted_freq_min,
            self.spin_box_adjusted_freq_min,
            self.checkbox_adjusted_freq_min_no_limit,
            self.label_adjusted_freq_max,
            self.spin_box_adjusted_freq_max,
            self.checkbox_adjusted_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (
            self.label_num_files_found_min,
            self.spin_box_num_files_found_min,
            self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max,
            self.spin_box_num_files_found_max,
            self.checkbox_num_files_found_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        if self.tab == 'wordlist_generator':
            self.spin_box_len_token_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_token_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_token_max_no_limit.stateChanged.connect(self.filters_changed)
        elif self.tab == 'ngram_generator':
            self.spin_box_len_ngram_min.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_len_ngram_max.valueChanged.connect(self.filters_changed)
            self.checkbox_len_ngram_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_dispersion_min.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_dispersion_max.valueChanged.connect(self.filters_changed)
        self.checkbox_dispersion_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_adjusted_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_adjusted_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_adjusted_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.model().itemChanged.connect(self.table_item_changed)

        if self.tab == 'wordlist_generator':
            self.layout_filters.addWidget(self.label_len_token, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_token_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_token_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_token_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_token_max_no_limit, 2, 2)
        elif self.tab == 'ngram_generator':
            self.layout_filters.addWidget(self.label_len_ngram, 0, 0, 1, 3)
            self.layout_filters.addWidget(self.label_len_ngram_min, 1, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_min, 1, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_min_no_limit, 1, 2)
            self.layout_filters.addWidget(self.label_len_ngram_max, 2, 0)
            self.layout_filters.addWidget(self.spin_box_len_ngram_max, 2, 1)
            self.layout_filters.addWidget(self.checkbox_len_ngram_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_dispersion, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_dispersion_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_dispersion_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_dispersion_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_dispersion_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_adjusted_freq, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_adjusted_freq_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_adjusted_freq_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_adjusted_freq_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_adjusted_freq_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 8, 2)

        self.layout_filters.addWidget(wl_layouts.Wl_Separator(self, orientation = 'vert'), 0, 3, 9, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        if self.tab == 'wordlist_generator':
            self.spin_box_len_token_min.setValue(settings['len_token_min'])
            self.checkbox_len_token_min_no_limit.setChecked(settings['len_token_min_no_limit'])
            self.spin_box_len_token_max.setValue(settings['len_token_max'])
            self.checkbox_len_token_max_no_limit.setChecked(settings['len_token_max_no_limit'])
        elif self.tab == 'ngram_generator':
            self.spin_box_len_ngram_min.setValue(settings['len_ngram_min'])
            self.checkbox_len_ngram_min_no_limit.setChecked(settings['len_ngram_min_no_limit'])
            self.spin_box_len_ngram_max.setValue(settings['len_ngram_max'])
            self.checkbox_len_ngram_max_no_limit.setChecked(settings['len_ngram_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_dispersion_min.setValue(settings['dispersion_min'])
        self.checkbox_dispersion_min_no_limit.setChecked(settings['dispersion_min_no_limit'])
        self.spin_box_dispersion_max.setValue(settings['dispersion_max'])
        self.checkbox_dispersion_max_no_limit.setChecked(settings['dispersion_max_no_limit'])

        self.spin_box_adjusted_freq_min.setValue(settings['adjusted_freq_min'])
        self.checkbox_adjusted_freq_min_no_limit.setChecked(settings['adjusted_freq_min_no_limit'])
        self.spin_box_adjusted_freq_max.setValue(settings['adjusted_freq_max'])
        self.checkbox_adjusted_freq_max_no_limit.setChecked(settings['adjusted_freq_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        if self.tab == 'wordlist_generator':
            self.settings['len_token_min'] = self.spin_box_len_token_min.value()
            self.settings['len_token_min_no_limit'] = self.checkbox_len_token_min_no_limit.isChecked()
            self.settings['len_token_max'] = self.spin_box_len_token_max.value()
            self.settings['len_token_max_no_limit'] = self.checkbox_len_token_max_no_limit.isChecked()
        elif self.tab == 'ngram_generator':
            self.settings['len_ngram_min'] = self.spin_box_len_ngram_min.value()
            self.settings['len_ngram_min_no_limit'] = self.checkbox_len_ngram_min_no_limit.isChecked()
            self.settings['len_ngram_max'] = self.spin_box_len_ngram_max.value()
            self.settings['len_ngram_max_no_limit'] = self.checkbox_len_ngram_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['dispersion_min'] = self.spin_box_dispersion_min.value()
        self.settings['dispersion_min_no_limit'] = self.checkbox_dispersion_min_no_limit.isChecked()
        self.settings['dispersion_max'] = self.spin_box_dispersion_max.value()
        self.settings['dispersion_max_no_limit'] = self.checkbox_dispersion_max_no_limit.isChecked()

        self.settings['adjusted_freq_min'] = self.spin_box_adjusted_freq_min.value()
        self.settings['adjusted_freq_min_no_limit'] = self.checkbox_adjusted_freq_min_no_limit.isChecked()
        self.settings['adjusted_freq_max'] = self.spin_box_adjusted_freq_max.value()
        self.settings['adjusted_freq_max_no_limit'] = self.checkbox_adjusted_freq_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        text_measure_dispersion = settings['generation_settings']['measure_dispersion']
        text_measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        text_dispersion = self.main.settings_global['measures_dispersion'][text_measure_dispersion]['col_text']
        text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][text_measure_adjusted_freq]['col_text']

        self.label_dispersion.setText(f'{text_dispersion}:')
        self.label_adjusted_freq.setText(f'{text_adjusted_freq}:')

class Wl_Dialog_Results_Filter_Collocation_Extractor(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Collocation_Extractor

        self.label_len_collocate = QLabel(self.tr('Collocate Length:'), self)
        (
            self.label_len_collocate_min,
            self.spin_box_len_collocate_min,
            self.checkbox_len_collocate_min_no_limit,
            self.label_len_collocate_max,
            self.spin_box_len_collocate_max,
            self.checkbox_len_collocate_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100
        )

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        self.combo_box_freq_position = wl_boxes.Wl_Combo_Box(self)
        (
            self.label_freq_min,
            self.spin_box_freq_min,
            self.checkbox_freq_min_no_limit,
            self.label_freq_max,
            self.spin_box_freq_max,
            self.checkbox_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (
            self.label_test_stat_min,
            self.spin_box_test_stat_min,
            self.checkbox_test_stat_min_no_limit,
            self.label_test_stat_max,
            self.spin_box_test_stat_max,
            self.checkbox_test_stat_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_p_val = QLabel(self.tr('p-value:'), self)
        (
            self.label_p_val_min,
            self.spin_box_p_val_min,
            self.checkbox_p_val_min_no_limit,
            self.label_p_val_max,
            self.spin_box_p_val_max,
            self.checkbox_p_val_max_no_limit
        ) = wl_widgets.wl_widgets_filter_p_val(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (
            self.label_bayes_factor_min,
            self.spin_box_bayes_factor_min,
            self.checkbox_bayes_factor_min_no_limit,
            self.label_bayes_factor_max,
            self.spin_box_bayes_factor_max,
            self.checkbox_bayes_factor_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (
            self.label_effect_size_min,
            self.spin_box_effect_size_min,
            self.checkbox_effect_size_min_no_limit,
            self.label_effect_size_max,
            self.spin_box_effect_size_max,
            self.checkbox_effect_size_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (
            self.label_num_files_found_min,
            self.spin_box_num_files_found_min,
            self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max,
            self.spin_box_num_files_found_max,
            self.checkbox_num_files_found_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        self.spin_box_len_collocate_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_collocate_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_collocate_max_no_limit.stateChanged.connect(self.filters_changed)

        self.combo_box_freq_position.currentTextChanged.connect(self.filters_changed)
        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_val_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_val_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_val_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_val_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.model().itemChanged.connect(self.table_item_changed)

        layout_freq_position = wl_layouts.Wl_Layout()
        layout_freq_position.addWidget(self.label_freq, 0, 0)
        layout_freq_position.addWidget(self.combo_box_freq_position, 0, 1, Qt.AlignRight)

        self.layout_filters.addWidget(self.label_len_collocate, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_collocate_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_collocate_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_collocate_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_collocate_max_no_limit, 2, 2)

        self.layout_filters.addLayout(layout_freq_position, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_val, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_val_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_val_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_val_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_val_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_val_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_val_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wl_layouts.Wl_Separator(self, orientation = 'vert'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_collocate_min.setValue(settings['len_collocate_min'])
        self.checkbox_len_collocate_min_no_limit.setChecked(settings['len_collocate_min_no_limit'])
        self.spin_box_len_collocate_max.setValue(settings['len_collocate_max'])
        self.checkbox_len_collocate_max_no_limit.setChecked(settings['len_collocate_max_no_limit'])

        self.combo_box_freq_position.setCurrentText(settings['freq_position'])
        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_val_min.setValue(settings['p_val_min'])
        self.checkbox_p_val_min_no_limit.setChecked(settings['p_val_min_no_limit'])
        self.spin_box_p_val_max.setValue(settings['p_val_max'])
        self.checkbox_p_val_max_no_limit.setChecked(settings['p_val_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_collocate_min'] = self.spin_box_len_collocate_min.value()
        self.settings['len_collocate_min_no_limit'] = self.checkbox_len_collocate_min_no_limit.isChecked()
        self.settings['len_collocate_max'] = self.spin_box_len_collocate_max.value()
        self.settings['len_collocate_max_no_limit'] = self.checkbox_len_collocate_max_no_limit.isChecked()

        self.settings['freq_position'] = self.combo_box_freq_position.currentText()
        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_val_min'] = self.spin_box_p_val_min.value()
        self.settings['p_val_min_no_limit'] = self.checkbox_p_val_min_no_limit.isChecked()
        self.settings['p_val_max'] = self.spin_box_p_val_max.value()
        self.settings['p_val_max_no_limit'] = self.checkbox_p_val_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        # Frequency
        freq_position_old = self.settings['freq_position']

        self.combo_box_freq_position.clear()

        for i in range(settings['generation_settings']['window_left'], settings['generation_settings']['window_right'] + 1):
            if i < 0:
                self.combo_box_freq_position.addItem(self.tr('L') + str(-i))
            elif i > 0:
                self.combo_box_freq_position.addItem(self.tr('R') + str(i))

        self.combo_box_freq_position.addItem(self.tr('Total'))

        if self.combo_box_freq_position.findText(freq_position_old) > -1:
            self.combo_box_freq_position.setCurrentText(freq_position_old)
        else:
            self.combo_box_freq_position.setCurrentText(self.main.settings_default[self.tab]['filter_results']['freq_position'])

        # Filters
        test_statistical_significance = settings['generation_settings']['test_statistical_significance']
        measure_effect_size = settings['generation_settings']['measure_effect_size']

        text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(self.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{text_effect_size}:')

class Wl_Dialog_Results_Filter_Keyword_Extractor(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Keyword_Extractor

        self.label_len_keyword = QLabel(self.tr('Keyword Length:'), self)
        (
            self.label_len_keyword_min,
            self.spin_box_len_keyword_min,
            self.checkbox_len_keyword_min_no_limit,
            self.label_len_keyword_max,
            self.spin_box_len_keyword_max,
            self.checkbox_len_keyword_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100
        )

        self.label_freq = QLabel(self.tr('Frequency:'), self)
        (
            self.label_freq_min,
            self.spin_box_freq_min,
            self.checkbox_freq_min_no_limit,
            self.label_freq_max,
            self.spin_box_freq_max,
            self.checkbox_freq_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 0,
            filter_max = 1000000
        )

        self.label_test_stat = QLabel(self.tr('Test Statistic:'), self)
        (
            self.label_test_stat_min,
            self.spin_box_test_stat_min,
            self.checkbox_test_stat_min_no_limit,
            self.label_test_stat_max,
            self.spin_box_test_stat_max,
            self.checkbox_test_stat_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_p_val = QLabel(self.tr('p-value:'), self)
        (
            self.label_p_val_min,
            self.spin_box_p_val_min,
            self.checkbox_p_val_min_no_limit,
            self.label_p_val_max,
            self.spin_box_p_val_max,
            self.checkbox_p_val_max_no_limit
        ) = wl_widgets.wl_widgets_filter_p_val(self)

        self.label_bayes_factor = QLabel(self.tr('Bayes Factor:'), self)
        (
            self.label_bayes_factor_min,
            self.spin_box_bayes_factor_min,
            self.checkbox_bayes_factor_min_no_limit,
            self.label_bayes_factor_max,
            self.spin_box_bayes_factor_max,
            self.checkbox_bayes_factor_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_effect_size = QLabel(self.tr('Effect Size:'), self)
        (
            self.label_effect_size_min,
            self.spin_box_effect_size_min,
            self.checkbox_effect_size_min_no_limit,
            self.label_effect_size_max,
            self.spin_box_effect_size_max,
            self.checkbox_effect_size_max_no_limit
        ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of Files Found:'), self)
        (
            self.label_num_files_found_min,
            self.spin_box_num_files_found_min,
            self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max,
            self.spin_box_num_files_found_max,
            self.checkbox_num_files_found_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100000
        )

        self.spin_box_len_keyword_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_keyword_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_keyword_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
        self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_p_val_min.valueChanged.connect(self.filters_changed)
        self.checkbox_p_val_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_p_val_max.valueChanged.connect(self.filters_changed)
        self.checkbox_p_val_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
        self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
        self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        self.table.model().itemChanged.connect(self.table_item_changed)

        self.layout_filters.addWidget(self.label_len_keyword, 0, 0, 1, 3)
        self.layout_filters.addWidget(self.label_len_keyword_min, 1, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_min, 1, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_min_no_limit, 1, 2)
        self.layout_filters.addWidget(self.label_len_keyword_max, 2, 0)
        self.layout_filters.addWidget(self.spin_box_len_keyword_max, 2, 1)
        self.layout_filters.addWidget(self.checkbox_len_keyword_max_no_limit, 2, 2)

        self.layout_filters.addWidget(self.label_freq, 0, 4, 1, 3)
        self.layout_filters.addWidget(self.label_freq_min, 1, 4)
        self.layout_filters.addWidget(self.spin_box_freq_min, 1, 5)
        self.layout_filters.addWidget(self.checkbox_freq_min_no_limit, 1, 6)
        self.layout_filters.addWidget(self.label_freq_max, 2, 4)
        self.layout_filters.addWidget(self.spin_box_freq_max, 2, 5)
        self.layout_filters.addWidget(self.checkbox_freq_max_no_limit, 2, 6)

        self.layout_filters.addWidget(self.label_test_stat, 3, 0, 1, 3)
        self.layout_filters.addWidget(self.label_test_stat_min, 4, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_min, 4, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_min_no_limit, 4, 2)
        self.layout_filters.addWidget(self.label_test_stat_max, 5, 0)
        self.layout_filters.addWidget(self.spin_box_test_stat_max, 5, 1)
        self.layout_filters.addWidget(self.checkbox_test_stat_max_no_limit, 5, 2)

        self.layout_filters.addWidget(self.label_p_val, 3, 4, 1, 3)
        self.layout_filters.addWidget(self.label_p_val_min, 4, 4)
        self.layout_filters.addWidget(self.spin_box_p_val_min, 4, 5)
        self.layout_filters.addWidget(self.checkbox_p_val_min_no_limit, 4, 6)
        self.layout_filters.addWidget(self.label_p_val_max, 5, 4)
        self.layout_filters.addWidget(self.spin_box_p_val_max, 5, 5)
        self.layout_filters.addWidget(self.checkbox_p_val_max_no_limit, 5, 6)

        self.layout_filters.addWidget(self.label_bayes_factor, 6, 0, 1, 3)
        self.layout_filters.addWidget(self.label_bayes_factor_min, 7, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_min, 7, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_min_no_limit, 7, 2)
        self.layout_filters.addWidget(self.label_bayes_factor_max, 8, 0)
        self.layout_filters.addWidget(self.spin_box_bayes_factor_max, 8, 1)
        self.layout_filters.addWidget(self.checkbox_bayes_factor_max_no_limit, 8, 2)

        self.layout_filters.addWidget(self.label_effect_size, 6, 4, 1, 3)
        self.layout_filters.addWidget(self.label_effect_size_min, 7, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_min, 7, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_min_no_limit, 7, 6)
        self.layout_filters.addWidget(self.label_effect_size_max, 8, 4)
        self.layout_filters.addWidget(self.spin_box_effect_size_max, 8, 5)
        self.layout_filters.addWidget(self.checkbox_effect_size_max_no_limit, 8, 6)

        self.layout_filters.addWidget(self.label_num_files_found, 9, 0, 1, 3)
        self.layout_filters.addWidget(self.label_num_files_found_min, 10, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_min, 10, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_min_no_limit, 10, 2)
        self.layout_filters.addWidget(self.label_num_files_found_max, 11, 0)
        self.layout_filters.addWidget(self.spin_box_num_files_found_max, 11, 1)
        self.layout_filters.addWidget(self.checkbox_num_files_found_max_no_limit, 11, 2)

        self.layout_filters.addWidget(wl_layouts.Wl_Separator(self, orientation = 'vert'), 0, 3, 12, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_keyword_min.setValue(settings['len_keyword_min'])
        self.checkbox_len_keyword_min_no_limit.setChecked(settings['len_keyword_min_no_limit'])
        self.spin_box_len_keyword_max.setValue(settings['len_keyword_max'])
        self.checkbox_len_keyword_max_no_limit.setChecked(settings['len_keyword_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
        self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
        self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
        self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        self.spin_box_p_val_min.setValue(settings['p_val_min'])
        self.checkbox_p_val_min_no_limit.setChecked(settings['p_val_min_no_limit'])
        self.spin_box_p_val_max.setValue(settings['p_val_max'])
        self.checkbox_p_val_max_no_limit.setChecked(settings['p_val_max_no_limit'])

        self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
        self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
        self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
        self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
        self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
        self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
        self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings['len_keyword_min'] = self.spin_box_len_keyword_min.value()
        self.settings['len_keyword_min_no_limit'] = self.checkbox_len_keyword_min_no_limit.isChecked()
        self.settings['len_keyword_max'] = self.spin_box_len_keyword_max.value()
        self.settings['len_keyword_max_no_limit'] = self.checkbox_len_keyword_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
        self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
        self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
        self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        self.settings['p_val_min'] = self.spin_box_p_val_min.value()
        self.settings['p_val_min_no_limit'] = self.checkbox_p_val_min_no_limit.isChecked()
        self.settings['p_val_max'] = self.spin_box_p_val_max.value()
        self.settings['p_val_max_no_limit'] = self.checkbox_p_val_max_no_limit.isChecked()

        self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
        self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
        self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
        self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
        self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
        self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
        self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

    def table_item_changed(self):
        settings = self.table.settings[self.tab]

        test_statistical_significance = settings['generation_settings']['test_statistical_significance']
        measure_effect_size = settings['generation_settings']['measure_effect_size']

        text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        if text_test_stat:
            self.label_test_stat.setText(f'{text_test_stat}:')

            if not self.checkbox_test_stat_min_no_limit.isChecked():
                self.spin_box_test_stat_min.setEnabled(True)
            if not self.checkbox_test_stat_max_no_limit.isChecked():
                self.spin_box_test_stat_max.setEnabled(True)

            self.checkbox_test_stat_min_no_limit.setEnabled(True)
            self.checkbox_test_stat_max_no_limit.setEnabled(True)
        else:
            self.label_test_stat.setText(self.tr('Test Statistic:'))

            self.spin_box_test_stat_min.setEnabled(False)
            self.checkbox_test_stat_min_no_limit.setEnabled(False)
            self.spin_box_test_stat_max.setEnabled(False)
            self.checkbox_test_stat_max_no_limit.setEnabled(False)

        self.label_effect_size.setText(f'{text_effect_size}:')
