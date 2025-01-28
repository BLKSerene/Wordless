# ----------------------------------------------------------------------
# Wordless: Results - Filter results
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

import copy
import math
import traceback

from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QLabel, QPushButton

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs, wl_dialogs_misc
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_boxes, wl_buttons, wl_layouts

_tr = QCoreApplication.translate

def widgets_filter(parent, label, val_min, val_max, settings, filter_name, double = False):
    def load_settings(settings_load):
        checkbox_sync.setChecked(settings_load[f'{filter_name}_sync'])
        spin_box_min.setValue(settings_load[f'{filter_name}_min'])
        checkbox_min_no_limit.setChecked(settings_load[f'{filter_name}_min_no_limit'])
        spin_box_max.setValue(settings_load[f'{filter_name}_max'])
        checkbox_max_no_limit.setChecked(settings_load[f'{filter_name}_max_no_limit'])

    def filter_changed():
        settings[f'{filter_name}_sync'] = checkbox_sync.isChecked()
        settings[f'{filter_name}_min'] = spin_box_min.value()
        settings[f'{filter_name}_min_no_limit'] = checkbox_min_no_limit.isChecked()
        settings[f'{filter_name}_max'] = spin_box_max.value()
        settings[f'{filter_name}_max_no_limit'] = checkbox_max_no_limit.isChecked()

    label = QLabel(label, parent)
    (
        checkbox_sync,
        label_min, spin_box_min, checkbox_min_no_limit,
        label_max, spin_box_max, checkbox_max_no_limit
    ) = wl_boxes.wl_spin_boxes_min_max_no_limit(parent, val_min = val_min, val_max = val_max, double = double)

    checkbox_sync.stateChanged.connect(filter_changed)
    spin_box_min.valueChanged.connect(filter_changed)
    checkbox_min_no_limit.stateChanged.connect(filter_changed)
    spin_box_max.valueChanged.connect(filter_changed)
    checkbox_max_no_limit.stateChanged.connect(filter_changed)

    layout = wl_layouts.Wl_Layout()
    layout.addWidget(label, 0, 0, 1, 2)
    layout.addWidget(checkbox_sync, 0, 2)
    layout.addWidget(label_min, 1, 0)
    layout.addWidget(spin_box_min, 1, 1)
    layout.addWidget(checkbox_min_no_limit, 1, 2)
    layout.addWidget(label_max, 2, 0)
    layout.addWidget(spin_box_max, 2, 1)
    layout.addWidget(checkbox_max_no_limit, 2, 2)

    layout.setColumnStretch(1, 1)

    layout.label = label
    layout.checkbox_sync = checkbox_sync
    layout.label_min = label_min
    layout.spin_box_min = spin_box_min
    layout.checkbox_min_no_limit = checkbox_min_no_limit
    layout.label_max = label_max
    layout.spin_box_max = spin_box_max
    layout.checkbox_max_no_limit = checkbox_max_no_limit
    layout.load_settings = load_settings

    return layout

def widgets_filter_measures(parent, label, settings, filter_name):
    def precision_changed():
        precision = main.settings_custom['tables']['precision_settings']['precision_decimals']

        layout.spin_box_min.setDecimals(precision)
        layout.spin_box_max.setDecimals(precision)

        layout.spin_box_min.setSingleStep(0.1 ** precision)
        layout.spin_box_max.setSingleStep(0.1 ** precision)

    main = wl_misc.find_wl_main(parent)

    layout = widgets_filter(
        parent,
        label = label,
        val_min = -10000, val_max = 10000,
        settings = settings, filter_name = filter_name,
        double = True
    )

    main.wl_settings.wl_settings_changed.connect(precision_changed)

    precision_changed()

    return layout

def widgets_filter_p_val(parent, settings):
    def precision_changed():
        precision = main.settings_custom['tables']['precision_settings']['precision_p_vals']

        layout.spin_box_min.setDecimals(precision)
        layout.spin_box_max.setDecimals(precision)

        layout.spin_box_min.setSingleStep(0.1 ** precision)
        layout.spin_box_max.setSingleStep(0.1 ** precision)

    main = wl_misc.find_wl_main(parent)

    layout = widgets_filter(
        parent,
        label = _tr('wl_results_filter', 'p-value:'),
        val_min = 0, val_max = 1,
        settings = settings, filter_name = 'p_val',
        double = True
    )

    main.wl_settings.wl_settings_changed.connect(precision_changed)

    precision_changed()

    return layout

def add_layouts_filters(parent, layouts_filters, layout_filters):
    num_rows_left = math.ceil(len(layouts_filters) / 2)

    for i, layout in enumerate(layouts_filters):
        if i < num_rows_left:
            layout_filters.addLayout(layout, i, 0)
        else:
            layout_filters.addLayout(layout, i - num_rows_left, 2)

        layout_filters.addWidget(wl_layouts.Wl_Separator(parent, orientation = 'vert'), 0, 1, num_rows_left, 1)

def get_filter_min_max(settings, filter_name):
    filter_min = (
        float('-inf')
        if settings[f'{filter_name}_min_no_limit']
        else settings[f'{filter_name}_min']
    )

    filter_max = (
        float('inf')
        if settings[f'{filter_name}_max_no_limit']
        else settings[f'{filter_name}_max']
    )

    return filter_min, filter_max

# self.tr() does not work in inherited classes
class Wl_Dialog_Results_Filter(wl_dialogs.Wl_Dialog):
    def __init__(self, main, table):
        super().__init__(main, _tr('Wl_Dialog_Results_Filter', 'Filter Results'))

        self.tab = table.tab
        self.table = table
        self.settings = self.main.settings_custom[self.tab]['filter_results']
        self.layouts_filters = []

        self.main.wl_work_area.currentChanged.connect(self.close)

        self.label_file_to_filter = QLabel(_tr('Wl_Dialog_Results_Filter', 'File to filter:'), self)
        self.combo_box_file_to_filter = wl_boxes.Wl_Combo_Box_File_To_Filter(self, self.table)
        self.button_filter = QPushButton(_tr('Wl_Dialog_Results_Filter', 'Filter'), self)

        self.button_restore_defaults = wl_buttons.Wl_Button_Restore_Defaults(self, load_settings = self.load_settings)
        self.button_close = QPushButton(_tr('Wl_Dialog_Results_Filter', 'Close'), self)

        self.combo_box_file_to_filter.currentTextChanged.connect(self.file_to_filter_changed)
        self.button_filter.clicked.connect(lambda checked: self.filter_results())
        self.button_close.clicked.connect(self.reject)

        layout_file_to_filter = wl_layouts.Wl_Layout()
        layout_file_to_filter.addWidget(self.label_file_to_filter, 0, 0)
        layout_file_to_filter.addWidget(self.combo_box_file_to_filter, 0, 1)

        layout_file_to_filter.setColumnStretch(1, 1)

        self.layout_filters = wl_layouts.Wl_Layout()

        layout_buttons = wl_layouts.Wl_Layout()
        layout_buttons.addWidget(self.button_restore_defaults, 0, 0)
        layout_buttons.addWidget(self.button_filter, 0, 2)
        layout_buttons.addWidget(self.button_close, 0, 3)

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

        # Update the setting if saved file to filter no long exists
        self.file_to_filter_changed()

    def file_to_filter_changed(self):
        self.settings['file_to_filter'] = self.combo_box_file_to_filter.currentText()

    @wl_misc.log_time
    def filter_results(self):
        worker_filter_results = self.Worker_Filter_Results(
            self.main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(
                self.main,
                text = _tr('Wl_Dialog_Results_Filter', 'Filtering results...')
            ),
            update_gui = self.update_gui,
            dialog = self
        )
        wl_threading.Wl_Thread(worker_filter_results).start_worker()

    def update_gui(self, err_msg):
        if wl_checks_work_area.check_postprocessing(self.main, err_msg):
            try:
                self.table.filter_table()

                self.main.statusBar().showMessage(_tr('Wl_Dialog_Results_Filter', 'The results in the data table has been successfully filtered.'))
            except Exception:
                wl_checks_work_area.check_err(self.main, traceback.format_exc())

    def show(self):
        super().show()

        # Make column length of filters equal
        widths_label = []

        for layout in self.layouts_filters:
            if 'combo_box_freq_position' in layout.__dict__:
                widths_label.append(layout.label.width() + layout.combo_box_freq_position.width())
            else:
                widths_label.append(layout.label.width())

        max_width = max(widths_label)

        # Only modify the length of the first filter label in each column, as an extra combo box is added after the filter label in Collocation/Colligation extractor
        self.layouts_filters[0].label.setFixedWidth(max_width)
        self.layouts_filters[(len(self.layouts_filters) + 1) // 2].label.setFixedWidth(max_width)

class Wl_Dialog_Results_Filter_Dependency_Parser(Wl_Dialog_Results_Filter):
    def __init__(self, main, table):
        super().__init__(main, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Dependency_Parser

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Head length:'),
            val_min = 1, val_max = 1000,
            settings = self.settings, filter_name = 'len_head'
        ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Dependent length:'),
            val_min = 1, val_max = 1000,
            settings = self.settings, filter_name = 'len_dependent'
        ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Dependency length:'),
            val_min = -1000, val_max = 1000,
            settings = self.settings, filter_name = 'dependency_len'
        ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Dependency length (absolute):'),
            val_min = -1000, val_max = 1000,
            settings = self.settings, filter_name = 'dependency_len_abs'
        ))

        # Close the dialog when data in the table are re-generated
        self.table.button_generate_table.clicked.connect(self.close)

        add_layouts_filters(
            self.main,
            layouts_filters = self.layouts_filters,
            layout_filters = self.layout_filters
        )

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        for layout in self.layouts_filters:
            layout.load_settings(settings)

class Wl_Worker_Results_Filter_Dependency_Parser(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str)

    def run(self):
        err_msg = ''

        try:
            col_head = self.dialog.table.find_header_hor(self.tr('Head'))
            col_dependent = self.dialog.table.find_header_hor(self.tr('Dependent'))
            col_dependency_len = self.dialog.table.find_header_hor(self.tr('Dependency Length'))
            col_dependency_len_abs = self.dialog.table.find_header_hor(self.tr('Dependency Length (Absolute)'))
            col_file = self.dialog.table.find_header_hor(self.tr('File'))

            len_head_min, len_head_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'len_head'
            )
            len_dependent_min, len_dependent_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'len_dependent'
            )
            dependency_len_min, dependency_len_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'dependency_len'
            )
            dependency_len_abs_min, dependency_len_abs_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'dependency_len_abs'
            )

            self.dialog.table.row_filters = []

            for i in range(self.dialog.table.model().rowCount()):
                if (
                    self.dialog.settings['file_to_filter'] == self.tr('Total')
                    or self.dialog.table.model().item(i, col_file).text() == self.dialog.settings['file_to_filter']
                ):
                    filters = []

                    # Only count the length of token texts when filtering tagged tokens
                    len_head = sum((
                        len(str(token))
                        for token in self.dialog.table.model().item(i, col_head).tokens_filter
                    ))
                    filters.append(len_head_min <= len_head <= len_head_max)

                    len_dependent = sum((
                        len(str(token))
                        for token in self.dialog.table.model().item(i, col_dependent).tokens_filter
                    ))
                    filters.append(len_dependent_min <= len_dependent <= len_dependent_max)

                    filters.append(
                        dependency_len_min <= self.dialog.table.model().item(i, col_dependency_len).val <= dependency_len_max
                    )

                    filters.append(
                        dependency_len_abs_min <= self.dialog.table.model().item(i, col_dependency_len_abs).val <= dependency_len_abs_max
                    )

                    self.dialog.table.row_filters.append(all(filters))
                else:
                    self.dialog.table.row_filters.append(True)

            self.progress_updated.emit(self.tr('Updating table...'))
        except Exception:
            err_msg = traceback.format_exc()
        finally:
            self.worker_done.emit(err_msg)

class Wl_Dialog_Results_Filter_Wordlist_Generator(Wl_Dialog_Results_Filter):
    def __init__(self, main, table):
        super().__init__(main, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Wordlist_Generator

        settings = self.table.settings[self.tab]

        measure_dispersion = settings['generation_settings']['measure_dispersion']
        measure_adjusted_freq = settings['generation_settings']['measure_adjusted_freq']

        self.col_text_dispersion = self.main.settings_global['measures_dispersion'][measure_dispersion]['col_text']
        self.col_text_adjusted_freq = self.main.settings_global['measures_adjusted_freq'][measure_adjusted_freq]['col_text']

        if self.tab == 'wordlist_generator':
            self.has_syllabified_forms = settings['generation_settings']['show_syllabified_forms']
        else:
            self.has_syllabified_forms = True

        self.has_dispersion = measure_dispersion != 'none'
        self.has_adjusted_freq = measure_adjusted_freq != 'none'

        if self.tab == 'wordlist_generator':
            label_len_node = self.tr('Token length:')
            self.type_node = 'token'
        elif self.tab == 'ngram_generator':
            label_len_node = self.tr('N-gram length:')
            self.type_node = 'ngram'

        self.layouts_filters.append(widgets_filter(
            self,
            label = label_len_node,
            val_min = 1, val_max = 1000,
            settings = self.settings, filter_name = f'len_{self.type_node}'
        ))

        if self.tab == 'wordlist_generator' and settings['generation_settings']['show_syllabified_forms']:
            self.layouts_filters.append(widgets_filter(
                self,
                label = self.tr('Number of syllables:'),
                val_min = 1, val_max = 1000,
                settings = self.settings, filter_name = 'num_syls'
            ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Frequency:'),
            val_min = 0, val_max = 1000000,
            settings = self.settings, filter_name = 'freq'
        ))

        if self.has_dispersion:
            self.layouts_filters.append(widgets_filter(
                self,
                label = self.col_text_dispersion,
                val_min = 0, val_max = 1,
                settings = self.settings, filter_name = 'dispersion'
            ))

        if self.has_adjusted_freq:
            self.layouts_filters.append(widgets_filter(
                self,
                label = self.col_text_adjusted_freq,
                val_min = 0, val_max = 1000000,
                settings = self.settings, filter_name = 'adjusted_freq'
            ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Number of files found:'),
            val_min = 1, val_max = 100000,
            settings = self.settings, filter_name = 'num_files_found'
        ))

        # Close the dialog when data in the table are re-generated
        self.table.button_generate_table.clicked.connect(self.close)

        add_layouts_filters(
            self.main,
            layouts_filters = self.layouts_filters,
            layout_filters = self.layout_filters
        )

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        for layout in self.layouts_filters:
            layout.load_settings(settings)

class Wl_Worker_Results_Filter_Wordlist_Generator(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str)

    def run(self):
        err_msg = ''

        try:
            if self.dialog.tab == 'wordlist_generator':
                col_node = self.dialog.table.find_header_hor(self.tr('Token'))

                if self.dialog.has_syllabified_forms:
                    col_num_syls = self.dialog.table.find_header_hor(self.tr('Syllabified Form'))
            elif self.dialog.tab == 'ngram_generator':
                col_node = self.dialog.table.find_header_hor(self.tr('N-gram'))

            col_freq = self.dialog.table.find_header_hor(
                self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
            )

            if self.dialog.has_dispersion:
                col_dispersion = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.col_text_dispersion}"
                )

            if self.dialog.has_adjusted_freq:
                col_adjusted_freq = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.col_text_adjusted_freq}"
                )

            col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

            len_node_min, len_node_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = f'len_{self.dialog.type_node}'
            )

            if self.dialog.tab == 'wordlist_generator':
                num_syls_min, num_syls_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'num_syls'
                )

            freq_min, freq_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'freq'
            )

            if self.dialog.has_dispersion:
                dispersion_min, dispersion_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'dispersion'
                )

            if self.dialog.has_adjusted_freq:
                adjusted_freq_min, adjusted_freq_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'adjusted_freq'
                )

            num_files_found_min, num_files_found_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'num_files_found'
            )

            self.dialog.table.row_filters = []

            for i in range(self.dialog.table.model().rowCount()):
                filters = []

                # Only count the length of token texts when filtering tagged tokens
                len_node = sum((
                    len(str(token))
                    for token in self.dialog.table.model().item(i, col_node).tokens_filter
                ))

                # Filter node length only when the node appears at least once in the specified file
                if self.dialog.table.model().item(i, col_freq).val > 0:
                    filters.append(len_node_min <= len_node <= len_node_max)

                if self.dialog.tab == 'wordlist_generator' and self.dialog.has_syllabified_forms:
                    filter_num_syls = False
                    syllabified_form = self.dialog.table.model().item(i, col_num_syls).text()

                    for syls in syllabified_form.split(', '):
                        if num_syls_min <= len(syls.split('-')) <= num_syls_max:
                            filter_num_syls = True

                            break

                    filters.append(filter_num_syls)

                filters.append(
                    freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
                )

                if self.dialog.has_dispersion:
                    filters.append(
                        dispersion_min <= self.dialog.table.model().item(i, col_dispersion).val <= dispersion_max
                    )

                if self.dialog.has_adjusted_freq:
                    filters.append(
                        adjusted_freq_min <= self.dialog.table.model().item(i, col_adjusted_freq).val <= adjusted_freq_max
                    )

                filters.append(
                    num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
                )

                self.dialog.table.row_filters.append(all(filters))

            self.progress_updated.emit(self.tr('Updating table...'))
        except Exception:
            err_msg = traceback.format_exc()
        finally:
            self.worker_done.emit(err_msg)

class Wl_Dialog_Results_Filter_Collocation_Extractor(Wl_Dialog_Results_Filter):
    def __init__(self, main, table):
        super().__init__(main, table)

        self.Worker_Filter_Results = Wl_Worker_Results_Filter_Collocation_Extractor

        settings = self.table.settings[self.tab]

        test_statistical_significance = settings['generation_settings']['test_statistical_significance']
        measure_bayes_factor = settings['generation_settings']['measure_bayes_factor']
        measure_effect_size = settings['generation_settings']['measure_effect_size']

        self.col_text_test_stat = self.main.settings_global['tests_statistical_significance'][test_statistical_significance]['col_text']
        self.col_text_effect_size = self.main.settings_global['measures_effect_size'][measure_effect_size]['col_text']

        self.has_test_stat = bool(self.col_text_test_stat)
        self.has_p_val = test_statistical_significance != 'none'
        self.has_bayes_factor = measure_bayes_factor != 'none'
        self.has_effect_size = measure_effect_size != 'none'

        match self.tab:
            case 'collocation_extractor':
                self.type_node = 'node'
                self.type_collocation = 'collocation'
                label_len_node = self.tr('Node length:')
                label_len_collocation = self.tr('Collocation length:')
            case 'colligation_extractor':
                self.type_node = 'node'
                self.type_collocation = 'colligation'
                label_len_node = self.tr('Node length:')
                label_len_collocation = self.tr('Colligation length:')
            case 'keyword_extractor':
                self.type_node = 'keyword'
                label_len_node = self.tr('Keyword length:')

        self.layouts_filters.append(widgets_filter(
            self,
            label = label_len_node,
            val_min = 1, val_max = 1000,
            settings = self.settings, filter_name = f'len_{self.type_node}'
        ))

        if self.type_node == 'node':
            self.layouts_filters.append(widgets_filter(
                self,
                label = self.tr('Collocate length:'),
                val_min = 1, val_max = 1000,
                settings = self.settings, filter_name = 'len_collocate'
            ))

            self.layouts_filters.append(widgets_filter(
                self,
                label = label_len_collocation,
                val_min = 2, val_max = 2000,
                settings = self.settings, filter_name = f'len_{self.type_collocation}'
            ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Frequency:'),
            val_min = 0, val_max = 1000000,
            settings = self.settings, filter_name = 'freq'
        ))

        # Frequency position
        if self.type_node == 'node':
            self.combo_box_freq_position = wl_boxes.Wl_Combo_Box(self)

            for i in range(
                settings['generation_settings']['window_left'],
                settings['generation_settings']['window_right'] + 1
            ):
                if i < 0:
                    self.combo_box_freq_position.addItem(self.tr('L{}').format(-i))
                elif i > 0:
                    self.combo_box_freq_position.addItem(self.tr('R{}').format(i))

            self.combo_box_freq_position.addItem(self.tr('Total'))

            self.layouts_filters[-1].combo_box_freq_position = self.combo_box_freq_position

        if self.has_test_stat:
            self.layouts_filters.append(widgets_filter_measures(
                self,
                label = self.col_text_test_stat,
                settings = self.settings, filter_name = 'test_stat'
            ))

        if self.has_p_val:
            self.layouts_filters.append(widgets_filter_p_val(
                self,
                settings = self.settings
            ))

        if self.has_bayes_factor:
            self.layouts_filters.append(widgets_filter_measures(
                self,
                label = self.tr('Bayes factor:'),
                settings = self.settings, filter_name = 'bayes_factor'
            ))

        if self.has_effect_size:
            self.layouts_filters.append(widgets_filter_measures(
                self,
                label = self.col_text_effect_size,
                settings = self.settings, filter_name = 'effect_size'
            ))

        self.layouts_filters.append(widgets_filter(
            self,
            label = self.tr('Number of files found:'),
            val_min = 1, val_max = 100000,
            settings = self.settings, filter_name = 'num_files_found'
        ))

        if self.type_node == 'node':
            self.combo_box_freq_position.currentTextChanged.connect(self.filters_changed)

        # Close the dialog when data in the table are re-generated
        self.table.button_generate_table.clicked.connect(self.close)

        add_layouts_filters(
            self.main,
            layouts_filters = self.layouts_filters,
            layout_filters = self.layout_filters
        )

        if self.type_node == 'node':
            self.layouts_filters[3].removeWidget(self.layouts_filters[3].label)

            layout = wl_layouts.Wl_Layout()
            layout.addWidget(self.layouts_filters[3].label, 0, 0)
            layout.addWidget(self.combo_box_freq_position, 0, 1)

            layout.setColumnStretch(1, 1)

            self.layouts_filters[3].addLayout(layout, 0, 0, 1, 2)

        self.load_settings()

    def load_settings(self, defaults = False):
        super().load_settings(defaults)

        if defaults:
            settings = copy.deepcopy(self.main.settings_default[self.tab]['filter_results'])
        else:
            settings = copy.deepcopy(self.settings)

        for layout in self.layouts_filters:
            layout.load_settings(settings)

        if self.type_node == 'node':
            self.combo_box_freq_position.setCurrentText(settings['freq_position'])

    def filters_changed(self):
        if self.type_node == 'node':
            self.settings['freq_position'] = self.combo_box_freq_position.currentText()

class Wl_Worker_Results_Filter_Collocation_Extractor(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str)

    def run(self):
        err_msg = ''

        try:
            if self.dialog.type_node == 'node':
                col_node = self.dialog.table.find_header_hor(self.tr('Node'))
                col_collocate = self.dialog.table.find_header_hor(self.tr('Collocate'))

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

            col_freq_total = self.dialog.table.find_header_hor(
                self.tr('[{}]\nFrequency').format(self.dialog.settings['file_to_filter'])
            )

            if self.dialog.has_test_stat:
                col_test_stat = self.dialog.table.find_header_hor(
                    f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.col_text_test_stat}"
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
                    f"[{self.dialog.settings['file_to_filter']}]\n{self.dialog.col_text_effect_size}"
                )

            col_num_files_found = self.dialog.table.find_header_hor(self.tr('Number of\nFiles Found'))

            len_node_min, len_node_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = f'len_{self.dialog.type_node}'
            )

            if self.dialog.type_node == 'node':
                len_collocate_min, len_collocate_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'len_collocate'
                )

                len_collocation_min, len_collocation_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = f'len_{self.dialog.type_collocation}'
                )

            freq_min, freq_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'freq'
            )

            if self.dialog.has_test_stat:
                test_stat_min, test_stat_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'test_stat'
                )

            if self.dialog.has_p_val:
                p_val_min, p_val_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'p_val'
                )

            if self.dialog.has_bayes_factor:
                bayes_factor_min, bayes_factor_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'bayes_factor'
                )

            if self.dialog.has_effect_size:
                effect_size_min, effect_size_max = get_filter_min_max(
                    settings = self.dialog.settings,
                    filter_name = 'effect_size'
                )

            num_files_found_min, num_files_found_max = get_filter_min_max(
                settings = self.dialog.settings,
                filter_name = 'num_files_found'
            )

            self.dialog.table.row_filters = []

            for i in range(self.dialog.table.model().rowCount()):
                filters = []

                # Only count the length of token texts when filtering tagged tokens
                len_node = sum((
                    len(str(token))
                    for token in self.dialog.table.model().item(i, col_node).tokens_filter
                ))

                # Filter node length only when the collocation/colligation/keyword appears at least once in the specified file
                if self.dialog.table.model().item(i, col_freq_total).val > 0:
                    filters.append(len_node_min <= len_node <= len_node_max)

                if self.dialog.type_node == 'node':
                    len_collocate = sum((
                        len(str(token))
                        for token in self.dialog.table.model().item(i, col_collocate).tokens_filter
                    ))

                    # Filter collocate/collocation/colligation length only when the collocation/colligation/keyword appears at least once in the specified file
                    if self.dialog.table.model().item(i, col_freq_total).val > 0:
                        filters.append(len_collocate_min <= len_collocate <= len_collocate_max)
                        filters.append(len_collocation_min <= len_node + len_collocate <= len_collocation_max)

                filters.append(
                    freq_min <= self.dialog.table.model().item(i, col_freq).val <= freq_max
                )

                if self.dialog.has_test_stat:
                    filters.append(
                        test_stat_min <= self.dialog.table.model().item(i, col_test_stat).val <= test_stat_max
                    )

                if self.dialog.has_p_val:
                    filters.append(
                        p_val_min <= self.dialog.table.model().item(i, col_p_value).val <= p_val_max
                    )

                if self.dialog.has_bayes_factor:
                    filters.append(
                        bayes_factor_min <= self.dialog.table.model().item(i, col_bayes_factor).val <= bayes_factor_max
                    )

                if self.dialog.has_effect_size:
                    filters.append(
                        effect_size_min <= self.dialog.table.model().item(i, col_effect_size).val <= effect_size_max
                    )

                filters.append(
                    num_files_found_min <= self.dialog.table.model().item(i, col_num_files_found).val <= num_files_found_max
                )

                self.dialog.table.row_filters.append(all(filters))

            self.progress_updated.emit(self.tr('Updating table...'))
        except Exception:
            err_msg = traceback.format_exc()
        finally:
            self.worker_done.emit(err_msg)
