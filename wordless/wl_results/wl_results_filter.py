# ----------------------------------------------------------------------
# Wordless: Results - Filter
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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
import math

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QLabel, QPushButton

from wordless.wl_dialogs import wl_dialogs, wl_dialogs_misc
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_boxes, wl_buttons, wl_layouts, wl_widgets

_tr = QCoreApplication.translate

def add_widgets_filter(parent, widgets_filter, layout):
    num_rows_left = math.ceil(len(widgets_filter) / 2)

    for i, widgets in enumerate(widgets_filter):
        (
            label,
            label_min, spin_box_min, checkbox_min_no_limit,
            label_max, spin_box_max, checkbox_max_no_limit
        ) = widgets

        if i < num_rows_left:
            layout.addWidget(label, i * 3, 0, 1, 3)
            layout.addWidget(label_min, i * 3 + 1, 0)
            layout.addWidget(spin_box_min, i * 3 + 1, 1)
            layout.addWidget(checkbox_min_no_limit, i * 3 + 1, 2)
            layout.addWidget(label_max, i * 3 + 2, 0)
            layout.addWidget(spin_box_max, i * 3 + 2, 1)
            layout.addWidget(checkbox_max_no_limit, i * 3 + 2, 2)
        else:
            layout.addWidget(label, (i - num_rows_left) * 3, 4, 1, 3)
            layout.addWidget(label_min, (i - num_rows_left) * 3 + 1, 4)
            layout.addWidget(spin_box_min, (i - num_rows_left) * 3 + 1, 5)
            layout.addWidget(checkbox_min_no_limit, (i - num_rows_left) * 3 + 1, 6)
            layout.addWidget(label_max, (i - num_rows_left) * 3 + 2, 4)
            layout.addWidget(spin_box_max, (i - num_rows_left) * 3 + 2, 5)
            layout.addWidget(checkbox_max_no_limit, (i - num_rows_left) * 3 + 2, 6)

        layout.addWidget(wl_layouts.Wl_Separator(parent, orientation = 'vert'), 0, 3, num_rows_left * 3, 1)

class Wl_Dialog_Results_Filter(wl_dialogs.Wl_Dialog):
    def __init__(self, main, tab, table):
        super().__init__(main, _tr('wl_results_filter', 'Filter Results'))

        self.tab = tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['filter_results']

        self.main.wl_work_area.currentChanged.connect(self.close)

        self.label_file_to_filter = QLabel(_tr('wl_results_filter', 'File to filter:'), self)
        self.combo_box_file_to_filter = wl_boxes.Wl_Combo_Box_File_To_Filter(self, self.table)
        self.button_filter = QPushButton(_tr('wl_results_filter', 'Filter'), self)

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)
        self.button_close = QPushButton(_tr('wl_results_filter', 'Close'), self)

        self.combo_box_file_to_filter.currentTextChanged.connect(self.file_to_filter_changed)
        self.button_filter.clicked.connect(lambda checked: self.filter_results())
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
        worker_filter_results = self.Worker_Filter_Results(
            self.main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(self.main, text = _tr('wl_results_filter', 'Filtering results...')),
            update_gui = self.update_gui,
            dialog = self
        )
        wl_threading.Wl_Thread(worker_filter_results).start_worker()

    def update_gui(self):
        self.table.filter_table()

        self.main.statusBar().showMessage(_tr('wl_results_filter', 'The results in the table has been successfully filtered.'))

class Wl_Dialog_Results_Filter_Wordlist_Generator(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Wordlist_Generator

        settings = self.table.settings[tab]

        measure_dispersion = settings['generation_settings']['measure_dispersion']
        measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        col_text_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['col_text']
        col_text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col_text']

        self.has_dispersion = measure_dispersion != 'none'
        self.has_adjusted_freq = measure_adjusted_freq != 'none'

        if self.tab == 'wordlist_generator':
            self.label_len_token_ngram = QLabel(self.tr('Token length:'), self)
        elif self.tab == 'ngram_generator':
            self.label_len_token_ngram = QLabel(self.tr('N-gram length:'), self)

        (
            self.label_len_token_ngram_min,
            self.spin_box_len_token_ngram_min,
            self.checkbox_len_token_ngram_min_no_limit,
            self.label_len_token_ngram_max,
            self.spin_box_len_token_ngram_max,
            self.checkbox_len_token_ngram_max_no_limit
        ) = wl_widgets.wl_widgets_filter(
            self,
            filter_min = 1,
            filter_max = 100
        )

        if self.tab == 'wordlist_generator':
            self.label_num_syls = QLabel(self.tr('Number of syllables:'), self)
            (
                self.label_num_syls_min,
                self.spin_box_num_syls_min,
                self.checkbox_num_syls_min_no_limit,
                self.label_num_syls_max,
                self.spin_box_num_syls_max,
                self.checkbox_num_syls_max_no_limit
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

        if self.has_dispersion:
            self.label_dispersion = QLabel(col_text_dispersion, self)
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

        if self.has_adjusted_freq:
            self.label_adjusted_freq = QLabel(col_text_adjusted_freq, self)
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

        self.label_num_files_found = QLabel(self.tr('Number of files found:'), self)
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

        self.spin_box_len_token_ngram_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_token_ngram_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_token_ngram_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_token_ngram_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.tab == 'wordlist_generator':
            self.spin_box_num_syls_min.valueChanged.connect(self.filters_changed)
            self.checkbox_num_syls_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_num_syls_max.valueChanged.connect(self.filters_changed)
            self.checkbox_num_syls_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.has_dispersion:
            self.spin_box_dispersion_min.valueChanged.connect(self.filters_changed)
            self.checkbox_dispersion_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_dispersion_max.valueChanged.connect(self.filters_changed)
            self.checkbox_dispersion_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.has_adjusted_freq:
            self.spin_box_adjusted_freq_min.valueChanged.connect(self.filters_changed)
            self.checkbox_adjusted_freq_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_adjusted_freq_max.valueChanged.connect(self.filters_changed)
            self.checkbox_adjusted_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        # Close the dialog when data in the table are re-generated
        self.table.button_generate_table.clicked.connect(self.close)

        widgets_filter = [[
            self.label_len_token_ngram,
            self.label_len_token_ngram_min, self.spin_box_len_token_ngram_min, self.checkbox_len_token_ngram_min_no_limit,
            self.label_len_token_ngram_max, self.spin_box_len_token_ngram_max, self.checkbox_len_token_ngram_max_no_limit
        ]]

        if self.tab == 'wordlist_generator':
            widgets_filter.append([
                self.label_num_syls,
                self.label_num_syls_min, self.spin_box_num_syls_min, self.checkbox_num_syls_min_no_limit,
                self.label_num_syls_max, self.spin_box_num_syls_max, self.checkbox_num_syls_max_no_limit
            ])

        widgets_filter.append([
            self.label_freq,
            self.label_freq_min, self.spin_box_freq_min, self.checkbox_freq_min_no_limit,
            self.label_freq_max, self.spin_box_freq_max, self.checkbox_freq_max_no_limit
        ])

        if self.has_dispersion:
            widgets_filter.append([
                self.label_dispersion,
                self.label_dispersion_min, self.spin_box_dispersion_min, self.checkbox_dispersion_min_no_limit,
                self.label_dispersion_max, self.spin_box_dispersion_max, self.checkbox_dispersion_max_no_limit
            ])

        if self.has_adjusted_freq:
            widgets_filter.append([
                self.label_adjusted_freq,
                self.label_adjusted_freq_min, self.spin_box_adjusted_freq_min, self.checkbox_adjusted_freq_min_no_limit,
                self.label_adjusted_freq_max, self.spin_box_adjusted_freq_max, self.checkbox_adjusted_freq_max_no_limit
            ])

        widgets_filter.append([
            self.label_num_files_found,
            self.label_num_files_found_min, self.spin_box_num_files_found_min, self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max, self.spin_box_num_files_found_max, self.checkbox_num_files_found_max_no_limit
        ])

        add_widgets_filter(self, widgets_filter = widgets_filter, layout = self.layout_filters)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        if self.tab == 'wordlist_generator':
            len_type = 'token'
        elif self.tab == 'ngram_generator':
            len_type = 'ngram'

        self.spin_box_len_token_ngram_min.setValue(settings[f'len_{len_type}_min'])
        self.checkbox_len_token_ngram_min_no_limit.setChecked(settings[f'len_{len_type}_min_no_limit'])
        self.spin_box_len_token_ngram_max.setValue(settings[f'len_{len_type}_max'])
        self.checkbox_len_token_ngram_max_no_limit.setChecked(settings[f'len_{len_type}_max_no_limit'])

        if self.tab == 'wordlist_generator':
            self.spin_box_num_syls_min.setValue(settings['num_syls_min'])
            self.checkbox_num_syls_min_no_limit.setChecked(settings['num_syls_min_no_limit'])
            self.spin_box_num_syls_max.setValue(settings['num_syls_max'])
            self.checkbox_num_syls_max_no_limit.setChecked(settings['num_syls_max_no_limit'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        if self.has_dispersion:
            self.spin_box_dispersion_min.setValue(settings['dispersion_min'])
            self.checkbox_dispersion_min_no_limit.setChecked(settings['dispersion_min_no_limit'])
            self.spin_box_dispersion_max.setValue(settings['dispersion_max'])
            self.checkbox_dispersion_max_no_limit.setChecked(settings['dispersion_max_no_limit'])

        if self.has_adjusted_freq:
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
            len_type = 'token'
        elif self.tab == 'ngram_generator':
            len_type = 'ngram'

        self.settings[f'len_{len_type}_min'] = self.spin_box_len_token_ngram_min.value()
        self.settings[f'len_{len_type}_min_no_limit'] = self.checkbox_len_token_ngram_min_no_limit.isChecked()
        self.settings[f'len_{len_type}_max'] = self.spin_box_len_token_ngram_max.value()
        self.settings[f'len_{len_type}_max_no_limit'] = self.checkbox_len_token_ngram_max_no_limit.isChecked()

        if self.tab == 'wordlist_generator':
            self.settings['num_syls_min'] = self.spin_box_num_syls_min.value()
            self.settings['num_syls_min_no_limit'] = self.checkbox_num_syls_min_no_limit.isChecked()
            self.settings['num_syls_max'] = self.spin_box_num_syls_max.value()
            self.settings['num_syls_max_no_limit'] = self.checkbox_num_syls_max_no_limit.isChecked()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        if self.has_dispersion:
            self.settings['dispersion_min'] = self.spin_box_dispersion_min.value()
            self.settings['dispersion_min_no_limit'] = self.checkbox_dispersion_min_no_limit.isChecked()
            self.settings['dispersion_max'] = self.spin_box_dispersion_max.value()
            self.settings['dispersion_max_no_limit'] = self.checkbox_dispersion_max_no_limit.isChecked()

        if self.has_adjusted_freq:
            self.settings['adjusted_freq_min'] = self.spin_box_adjusted_freq_min.value()
            self.settings['adjusted_freq_min_no_limit'] = self.checkbox_adjusted_freq_min_no_limit.isChecked()
            self.settings['adjusted_freq_max'] = self.spin_box_adjusted_freq_max.value()
            self.settings['adjusted_freq_max_no_limit'] = self.checkbox_adjusted_freq_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

class Wl_Worker_Results_Filter_Wordlist_Generator(wl_threading.Wl_Worker):
    def run(self):
        measure_dispersion = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_dispersion']
        measure_adjusted_freq = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_adjusted_freq']

        col_text_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['col_text']
        col_text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col_text']

        if self.dialog.tab == 'wordlist_generator':
            col_token_ngram = self.dialog.table.find_header_hor(self.tr('Token'))
            col_num_syls = self.dialog.table.find_header_hor(self.tr('Syllabification'))
        elif self.dialog.tab == 'ngram_generator':
            col_token_ngram = self.dialog.table.find_header_hor(self.tr('N-gram'))

        col_freq = self.dialog.table.find_header_hor(
            self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
        )

        if self.dialog.has_dispersion:
            col_dispersion = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{col_text_dispersion}"
            )

        if self.dialog.has_adjusted_freq:
            col_adjusted_freq = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{col_text_adjusted_freq}"
            )

        col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

        if self.dialog.tab == 'wordlist_generator':
            len_type = 'token'
        elif self.dialog.tab == 'ngram_generator':
            len_type = 'ngram'

        len_token_ngram_min = (
            float('-inf')
            if self.dialog.settings[f'len_{len_type}_min_no_limit']
            else self.dialog.settings[f'len_{len_type}_min']
        )
        len_token_ngram_max = (
            float('inf')
            if self.dialog.settings[f'len_{len_type}_max_no_limit']
            else self.dialog.settings[f'len_{len_type}_max']
        )

        if self.dialog.tab == 'wordlist_generator':
            num_syls_min = (
                float('-inf')
                if self.dialog.settings['num_syls_min_no_limit']
                else self.dialog.settings['num_syls_min']
            )
            num_syls_max = (
                float('inf')
                if self.dialog.settings['num_syls_max_no_limit']
                else self.dialog.settings['num_syls_max']
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

        for i in range(self.dialog.table.model().rowCount()):
            filter_len_token_ngram = (
                len_token_ngram_min <= len(self.dialog.table.model().item(i, col_token_ngram).text()) <= len_token_ngram_max
            )

            if self.dialog.tab == 'wordlist_generator':
                filter_num_syls = False
                syllabification = self.dialog.table.model().item(i, col_num_syls).text()

                for syls in syllabification.split(', '):
                    if num_syls_min <= len(syls.split('-')) <= num_syls_max:
                        filter_num_syls = True

                        break
            else:
                filter_num_syls = True

            filter_freq = (
                freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
            )

            if self.dialog.has_dispersion:
                filter_dispersion = (
                    dispersion_min <= self.dialog.table.model().item(i, col_dispersion).val <= dispersion_max
                )
            else:
                filter_dispersion = True

            if self.dialog.has_adjusted_freq:
                filter_adjusted_freq = (
                    adjusted_freq_min <= self.dialog.table.model().item(i, col_adjusted_freq).val <= adjusted_freq_max
                )
            else:
                filter_adjusted_freq = True

            filter_num_files_found = (
                num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
            )

            if (
                filter_len_token_ngram
                and filter_num_syls
                and filter_freq
                and filter_dispersion
                and filter_adjusted_freq
                and filter_num_files_found
            ):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit()

class Wl_Dialog_Results_Filter_Collocation_Extractor(Wl_Dialog_Results_Filter):
    def __init__(self, main, tab, table):
        super().__init__(main, tab, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Collocation_Extractor

        if tab in ['collocation_extractor', 'colligation_extractor']:
            self.type_node = 'collocate'
        elif tab == 'keyword_extractor':
            self.type_node = 'keyword'

        settings = self.table.settings[self.tab]

        test_statistical_significance = settings['generation_settings']['test_statistical_significance']
        measure_bayes_factor = settings['generation_settings']['measure_bayes_factor']
        measure_effect_size = settings['generation_settings']['measure_effect_size']

        col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        self.has_test_stat = bool(col_text_test_stat)
        self.has_p_val = test_statistical_significance != 'none'
        self.has_bayes_factor = measure_bayes_factor != 'none'
        self.has_effect_size = measure_effect_size != 'none'

        if self.type_node == 'collocate':
            self.label_len_node = QLabel(self.tr('Collocate length:'), self)
        elif self.type_node == 'keyword':
            self.label_len_node = QLabel(self.tr('Keyword length:'), self)

        (
            self.label_len_node_min,
            self.spin_box_len_node_min,
            self.checkbox_len_node_min_no_limit,
            self.label_len_node_max,
            self.spin_box_len_node_max,
            self.checkbox_len_node_max_no_limit
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

        # Frequency position
        if self.type_node == 'collocate':
            self.combo_box_freq_position = wl_boxes.Wl_Combo_Box(self)

            for i in range(
                settings['generation_settings']['window_left'],
                settings['generation_settings']['window_right'] + 1
            ):
                if i < 0:
                    self.combo_box_freq_position.addItem(self.tr('L') + str(-i))
                elif i > 0:
                    self.combo_box_freq_position.addItem(self.tr('R') + str(i))

            self.combo_box_freq_position.addItem(self.tr('Total'))

        if self.has_test_stat:
            self.label_test_stat = QLabel(col_text_test_stat, self)
            (
                self.label_test_stat_min,
                self.spin_box_test_stat_min,
                self.checkbox_test_stat_min_no_limit,
                self.label_test_stat_max,
                self.spin_box_test_stat_max,
                self.checkbox_test_stat_max_no_limit
            ) = wl_widgets.wl_widgets_filter_measures(self)

        if self.has_p_val:
            self.label_p_val = QLabel(self.tr('p-value:'), self)
            (
                self.label_p_val_min,
                self.spin_box_p_val_min,
                self.checkbox_p_val_min_no_limit,
                self.label_p_val_max,
                self.spin_box_p_val_max,
                self.checkbox_p_val_max_no_limit
            ) = wl_widgets.wl_widgets_filter_p_val(self)

        if self.has_bayes_factor:
            self.label_bayes_factor = QLabel(self.tr('Bayes factor:'), self)
            (
                self.label_bayes_factor_min,
                self.spin_box_bayes_factor_min,
                self.checkbox_bayes_factor_min_no_limit,
                self.label_bayes_factor_max,
                self.spin_box_bayes_factor_max,
                self.checkbox_bayes_factor_max_no_limit
            ) = wl_widgets.wl_widgets_filter_measures(self)

        if self.has_effect_size:
            self.label_effect_size = QLabel(col_text_effect_size, self)
            (
                self.label_effect_size_min,
                self.spin_box_effect_size_min,
                self.checkbox_effect_size_min_no_limit,
                self.label_effect_size_max,
                self.spin_box_effect_size_max,
                self.checkbox_effect_size_max_no_limit
            ) = wl_widgets.wl_widgets_filter_measures(self)

        self.label_num_files_found = QLabel(self.tr('Number of files found:'), self)
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

        self.spin_box_len_node_min.valueChanged.connect(self.filters_changed)
        self.checkbox_len_node_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_len_node_max.valueChanged.connect(self.filters_changed)
        self.checkbox_len_node_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.type_node == 'collocate':
            self.combo_box_freq_position.currentTextChanged.connect(self.filters_changed)

        self.spin_box_freq_min.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_freq_max.valueChanged.connect(self.filters_changed)
        self.checkbox_freq_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.has_test_stat:
            self.spin_box_test_stat_min.valueChanged.connect(self.filters_changed)
            self.checkbox_test_stat_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_test_stat_max.valueChanged.connect(self.filters_changed)
            self.checkbox_test_stat_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.has_p_val:
            self.spin_box_p_val_min.valueChanged.connect(self.filters_changed)
            self.checkbox_p_val_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_p_val_max.valueChanged.connect(self.filters_changed)
            self.checkbox_p_val_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.has_bayes_factor:
            self.spin_box_bayes_factor_min.valueChanged.connect(self.filters_changed)
            self.checkbox_bayes_factor_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_bayes_factor_max.valueChanged.connect(self.filters_changed)
            self.checkbox_bayes_factor_max_no_limit.stateChanged.connect(self.filters_changed)

        if self.has_effect_size:
            self.spin_box_effect_size_min.valueChanged.connect(self.filters_changed)
            self.checkbox_effect_size_min_no_limit.stateChanged.connect(self.filters_changed)
            self.spin_box_effect_size_max.valueChanged.connect(self.filters_changed)
            self.checkbox_effect_size_max_no_limit.stateChanged.connect(self.filters_changed)

        self.spin_box_num_files_found_min.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_min_no_limit.stateChanged.connect(self.filters_changed)
        self.spin_box_num_files_found_max.valueChanged.connect(self.filters_changed)
        self.checkbox_num_files_found_max_no_limit.stateChanged.connect(self.filters_changed)

        # Close the dialog when data in the table are re-generated
        self.table.button_generate_table.clicked.connect(self.close)

        widgets_filter = [
            [
                self.label_len_node,
                self.label_len_node_min, self.spin_box_len_node_min, self.checkbox_len_node_min_no_limit,
                self.label_len_node_max, self.spin_box_len_node_max, self.checkbox_len_node_max_no_limit
            ], [
                self.label_freq,
                self.label_freq_min, self.spin_box_freq_min, self.checkbox_freq_min_no_limit,
                self.label_freq_max, self.spin_box_freq_max, self.checkbox_freq_max_no_limit
            ]
        ]

        if self.has_test_stat:
            widgets_filter.append([
                self.label_test_stat,
                self.label_test_stat_min, self.spin_box_test_stat_min, self.checkbox_test_stat_min_no_limit,
                self.label_test_stat_max, self.spin_box_test_stat_max, self.checkbox_test_stat_max_no_limit
            ])

        if self.has_p_val:
            widgets_filter.append([
                self.label_p_val,
                self.label_p_val_min, self.spin_box_p_val_min, self.checkbox_p_val_min_no_limit,
                self.label_p_val_max, self.spin_box_p_val_max, self.checkbox_p_val_max_no_limit
            ])

        if self.has_bayes_factor:
            widgets_filter.append([
                self.label_bayes_factor,
                self.label_bayes_factor_min, self.spin_box_bayes_factor_min, self.checkbox_bayes_factor_min_no_limit,
                self.label_bayes_factor_max, self.spin_box_bayes_factor_max, self.checkbox_bayes_factor_max_no_limit
            ])

        if self.has_effect_size:
            widgets_filter.append([
                self.label_effect_size,
                self.label_effect_size_min, self.spin_box_effect_size_min, self.checkbox_effect_size_min_no_limit,
                self.label_effect_size_max, self.spin_box_effect_size_max, self.checkbox_effect_size_max_no_limit
            ])

        widgets_filter.append([
            self.label_num_files_found,
            self.label_num_files_found_min, self.spin_box_num_files_found_min, self.checkbox_num_files_found_min_no_limit,
            self.label_num_files_found_max, self.spin_box_num_files_found_max, self.checkbox_num_files_found_max_no_limit
        ])

        add_widgets_filter(self, widgets_filter = widgets_filter, layout = self.layout_filters)

        if self.type_node == 'collocate':
            self.layout_filters.removeWidget(self.label_freq)

            layout_freq_position = wl_layouts.Wl_Layout()
            layout_freq_position.addWidget(self.label_freq, 0, 0)
            layout_freq_position.addWidget(self.combo_box_freq_position, 0, 1, Qt.AlignRight)

            self.layout_filters.addLayout(layout_freq_position, 3, 0, 1, 3)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        self.spin_box_len_node_min.setValue(settings[f'len_{self.type_node}_min'])
        self.checkbox_len_node_min_no_limit.setChecked(settings[f'len_{self.type_node}_min_no_limit'])
        self.spin_box_len_node_max.setValue(settings[f'len_{self.type_node}_max'])
        self.checkbox_len_node_max_no_limit.setChecked(settings[f'len_{self.type_node}_max_no_limit'])

        if self.type_node == 'collocate':
            self.combo_box_freq_position.setCurrentText(settings['freq_position'])

        self.spin_box_freq_min.setValue(settings['freq_min'])
        self.checkbox_freq_min_no_limit.setChecked(settings['freq_min_no_limit'])
        self.spin_box_freq_max.setValue(settings['freq_max'])
        self.checkbox_freq_max_no_limit.setChecked(settings['freq_max_no_limit'])

        if self.has_test_stat:
            self.spin_box_test_stat_min.setValue(settings['test_stat_min'])
            self.checkbox_test_stat_min_no_limit.setChecked(settings['test_stat_min_no_limit'])
            self.spin_box_test_stat_max.setValue(settings['test_stat_max'])
            self.checkbox_test_stat_max_no_limit.setChecked(settings['test_stat_max_no_limit'])

        if self.has_p_val:
            self.spin_box_p_val_min.setValue(settings['p_val_min'])
            self.checkbox_p_val_min_no_limit.setChecked(settings['p_val_min_no_limit'])
            self.spin_box_p_val_max.setValue(settings['p_val_max'])
            self.checkbox_p_val_max_no_limit.setChecked(settings['p_val_max_no_limit'])

        if self.has_bayes_factor:
            self.spin_box_bayes_factor_min.setValue(settings['bayes_factor_min'])
            self.checkbox_bayes_factor_min_no_limit.setChecked(settings['bayes_factor_min_no_limit'])
            self.spin_box_bayes_factor_max.setValue(settings['bayes_factor_max'])
            self.checkbox_bayes_factor_max_no_limit.setChecked(settings['bayes_factor_max_no_limit'])

        if self.has_effect_size:
            self.spin_box_effect_size_min.setValue(settings['effect_size_min'])
            self.checkbox_effect_size_min_no_limit.setChecked(settings['effect_size_min_no_limit'])
            self.spin_box_effect_size_max.setValue(settings['effect_size_max'])
            self.checkbox_effect_size_max_no_limit.setChecked(settings['effect_size_max_no_limit'])

        self.spin_box_num_files_found_min.setValue(settings['num_files_found_min'])
        self.checkbox_num_files_found_min_no_limit.setChecked(settings['num_files_found_min_no_limit'])
        self.spin_box_num_files_found_max.setValue(settings['num_files_found_max'])
        self.checkbox_num_files_found_max_no_limit.setChecked(settings['num_files_found_max_no_limit'])

    def filters_changed(self):
        self.settings[f'len_{self.type_node}_min'] = self.spin_box_len_node_min.value()
        self.settings[f'len_{self.type_node}_min_no_limit'] = self.checkbox_len_node_min_no_limit.isChecked()
        self.settings[f'len_{self.type_node}_max'] = self.spin_box_len_node_max.value()
        self.settings[f'len_{self.type_node}_max_no_limit'] = self.checkbox_len_node_max_no_limit.isChecked()

        if self.type_node == 'collocate':
            self.settings['freq_position'] = self.combo_box_freq_position.currentText()

        self.settings['freq_min'] = self.spin_box_freq_min.value()
        self.settings['freq_min_no_limit'] = self.checkbox_freq_min_no_limit.isChecked()
        self.settings['freq_max'] = self.spin_box_freq_max.value()
        self.settings['freq_max_no_limit'] = self.checkbox_freq_max_no_limit.isChecked()

        if self.has_test_stat:
            self.settings['test_stat_min'] = self.spin_box_test_stat_min.value()
            self.settings['test_stat_min_no_limit'] = self.checkbox_test_stat_min_no_limit.isChecked()
            self.settings['test_stat_max'] = self.spin_box_test_stat_max.value()
            self.settings['test_stat_max_no_limit'] = self.checkbox_test_stat_max_no_limit.isChecked()

        if self.has_p_val:
            self.settings['p_val_min'] = self.spin_box_p_val_min.value()
            self.settings['p_val_min_no_limit'] = self.checkbox_p_val_min_no_limit.isChecked()
            self.settings['p_val_max'] = self.spin_box_p_val_max.value()
            self.settings['p_val_max_no_limit'] = self.checkbox_p_val_max_no_limit.isChecked()

        if self.has_bayes_factor:
            self.settings['bayes_factor_min'] = self.spin_box_bayes_factor_min.value()
            self.settings['bayes_factor_min_no_limit'] = self.checkbox_bayes_factor_min_no_limit.isChecked()
            self.settings['bayes_factor_max'] = self.spin_box_bayes_factor_max.value()
            self.settings['bayes_factor_max_no_limit'] = self.checkbox_bayes_factor_max_no_limit.isChecked()

        if self.has_effect_size:
            self.settings['effect_size_min'] = self.spin_box_effect_size_min.value()
            self.settings['effect_size_min_no_limit'] = self.checkbox_effect_size_min_no_limit.isChecked()
            self.settings['effect_size_max'] = self.spin_box_effect_size_max.value()
            self.settings['effect_size_max_no_limit'] = self.checkbox_effect_size_max_no_limit.isChecked()

        self.settings['num_files_found_min'] = self.spin_box_num_files_found_min.value()
        self.settings['num_files_found_min_no_limit'] = self.checkbox_num_files_found_min_no_limit.isChecked()
        self.settings['num_files_found_max'] = self.spin_box_num_files_found_max.value()
        self.settings['num_files_found_max_no_limit'] = self.checkbox_num_files_found_max_no_limit.isChecked()

class Wl_Worker_Results_Filter_Collocation_Extractor(wl_threading.Wl_Worker):
    def run(self):
        test_statistical_significance = self.dialog.table.settings[self.dialog.tab]['generation_settings']['test_statistical_significance']
        measure_effect_size = self.dialog.table.settings[self.dialog.tab]['generation_settings']['measure_effect_size']

        col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        if self.dialog.type_node == 'collocate':
            col_node = self.dialog.table.find_header_hor(self.tr('Collocate'))

            if self.dialog.settings['freq_position'] == self.tr('Total'):
                col_freq = self.dialog.table.find_header_hor(
                    self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
                )
            else:
                col_freq = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.settings['freq_position']}"
                )
        else:
            col_node = self.dialog.table.find_header_hor(self.tr('Keyword'))
            col_freq = self.dialog.table.find_header_hor(
                    self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
                )

        if self.dialog.has_test_stat:
            col_test_stat = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{col_text_test_stat}"
            )

        if self.dialog.has_p_val:
            col_p_value = self.dialog.table.find_header_hor(
                self.tr('[{}]\np-value').format(self.dialog.settings['file_to_filter'])
            )

        if self.dialog.has_bayes_factor:
            col_bayes_factor = self.dialog.table.find_header_hor(
                self.tr('[{}]\nBayes Factor').format(self.dialog.settings['file_to_filter'])
            )

        if self.dialog.has_effect_size:
            col_effect_size = self.dialog.table.find_header_hor(
                f"[{self.dialog.settings['file_to_filter']}]\n{col_text_effect_size}"
            )

        col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

        len_node_min = (
            float('-inf')
            if self.dialog.settings[f'len_{self.dialog.type_node}_min_no_limit']
            else self.dialog.settings[f'len_{self.dialog.type_node}_min']
        )
        len_node_max = (
            float('inf')
            if self.dialog.settings[f'len_{self.dialog.type_node}_max_no_limit']
            else self.dialog.settings[f'len_{self.dialog.type_node}_max']
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
            filter_len_node = (
                len_node_min <= len(self.dialog.table.model().item(i, col_node).text()) <= len_node_max
            )

            filter_freq = (
                freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
            )

            if self.dialog.has_test_stat:
                filter_test_stat = (
                    test_stat_min <= self.dialog.table.model().item(i, col_test_stat).val <= test_stat_max
                )
            else:
                filter_test_stat = True

            if self.dialog.has_p_val:
                filter_p_val = (
                    p_val_min <= self.dialog.table.model().item(i, col_p_value).val <= p_val_max
                )
            else:
                filter_p_val = True

            if self.dialog.has_bayes_factor:
                filter_bayes_factor = (
                    bayes_factor_min <= self.dialog.table.model().item(i, col_bayes_factor).val <= bayes_factor_max
                )
            else:
                filter_bayes_factor = True

            if self.dialog.has_effect_size:
                filter_effect_size = (
                    effect_size_min <= self.dialog.table.model().item(i, col_effect_size).val <= effect_size_max
                )
            else:
                filter_effect_size = True

            filter_num_files_found = (
                num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
            )

            if (
                filter_len_node
                and filter_freq
                and filter_test_stat
                and filter_p_val
                and filter_bayes_factor
                and filter_effect_size
                and filter_num_files_found
            ):
                self.dialog.table.row_filters.append(True)
            else:
                self.dialog.table.row_filters.append(False)

        self.progress_updated.emit(self.tr('Updating table...'))
        self.worker_done.emit()
