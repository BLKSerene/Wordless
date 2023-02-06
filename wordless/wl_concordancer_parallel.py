# ----------------------------------------------------------------------
# Wordless: Parallel Concordancer
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

import bisect
import copy
import traceback

from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtWidgets import QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc, wl_msg_boxes
from wordless.wl_nlp import wl_matching, wl_nlp_utils, wl_token_processing
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_labels, wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wrapper_Concordancer_Parallel(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.table_concordancer_parallel = Wl_Table_Concordancer_Parallel(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_concordancer_parallel.label_number_results, 0, 0)
        layout_results.addWidget(self.table_concordancer_parallel.button_results_search, 0, 4)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 4)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel, 1, 0, 1, 4)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel.button_exp_selected_cells, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel.button_exp_all_cells, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_concordancer_parallel.button_clr_table, 2, 3)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_punc_marks,

            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings_concordancer(self)

        self.checkbox_punc_marks.stateChanged.connect(self.token_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_punc_marks, 0, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 2, 1)

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
        ) = wl_widgets.wl_widgets_search_settings(
            self,
            tab = 'concordancer_parallel'
        )

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(
            self,
            tab = 'concordancer_parallel'
        )

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_concordancer_parallel.button_generate_table.click)
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

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_concordancer_parallel]
        )

        self.checkbox_show_cum_data.hide()
        self.checkbox_show_breakdown_file.hide()

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['concordancer_parallel'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['concordancer_parallel'])

        # Token Settings
        self.checkbox_punc_marks.setChecked(settings['token_settings']['punc_marks'])

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

        # Table Settings
        self.checkbox_show_pct_data.setChecked(settings['table_settings']['show_pct_data'])

        self.token_settings_changed()
        self.search_settings_changed()
        self.table_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['token_settings']

        settings['punc_marks'] = self.checkbox_punc_marks.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        # Check if searching is enabled
        if self.group_box_search_settings.isChecked():
            self.checkbox_match_tags.token_settings_changed()
        else:
            self.group_box_search_settings.setChecked(True)

            self.checkbox_match_tags.token_settings_changed()

            self.group_box_search_settings.setChecked(False)

        self.main.wl_context_settings_concordancer.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['search_settings']

        settings['multi_search_mode'] = self.checkbox_multi_search_mode.isChecked()
        settings['search_term'] = self.line_edit_search_term.text()
        settings['search_terms'] = self.list_search_terms.model().stringList()

        settings['match_case'] = self.checkbox_match_case.isChecked()
        settings['match_whole_words'] = self.checkbox_match_whole_words.isChecked()
        settings['match_inflected_forms'] = self.checkbox_match_inflected_forms.isChecked()
        settings['use_regex'] = self.checkbox_use_regex.isChecked()
        settings['match_without_tags'] = self.checkbox_match_without_tags.isChecked()
        settings['match_tags'] = self.checkbox_match_tags.isChecked()

    def table_settings_changed(self):
        settings = self.main.settings_custom['concordancer_parallel']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()

class Wl_Table_Concordancer_Parallel(wl_tables.Wl_Table_Data_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'concordancer_parallel',
            headers = [
                _tr('Wl_Table_Concordancer_Parallel', 'Parallel Unit No.'),
                _tr('Wl_Table_Concordancer_Parallel', 'Parallel Unit No. %')
            ],
            headers_int = [
                _tr('Wl_Table_Concordancer_Parallel', 'Parallel Unit No.')
            ],
            headers_pct = [
                _tr('Wl_Table_Concordancer_Parallel', 'Parallel Unit No. %')
            ],
            generate_fig = False
        )

    @wl_misc.log_timing
    def generate_table(self):
        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['concordancer_parallel']['search_settings'],
            show_warning = False
        ):
            search_additions_deletions = True
        else:
            # Check whether the user has simply forgotten to enter search terms
            search_additions_deletions = wl_msg_boxes.wl_msg_box_question(
                self.main,
                title = self.tr('Missing Search Terms'),
                text = self.tr('''
                    <div>You have not specified any search terms. Do you want to search for additions and deletions?</div>
                ''')
            )

        if search_additions_deletions:
            worker_concordancer_parallel_table = Wl_Worker_Concordancer_Parallel_Table(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                update_gui = self.update_gui_table
            )

            wl_threading.Wl_Thread(worker_concordancer_parallel_table).start_worker()
        else:
            wl_checks_work_area.wl_status_bar_msg_missing_search_terms(self.main)

    def update_gui_table(self, err_msg, concordance_lines):
        if wl_checks_work_area.check_results(self.main, err_msg, concordance_lines):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table(0)

                for file_name in self.main.wl_file_area.get_selected_file_names():
                    self.ins_header_hor(
                        self.model().columnCount(),
                        file_name
                    )

                self.model().setRowCount(len(concordance_lines))
                self.disable_updates()

                for i, concordance_line in enumerate(concordance_lines):
                    parallel_unit_no, len_parallel_units = concordance_line[0]

                    self.set_item_num(i, 0, parallel_unit_no)
                    self.set_item_num(i, 1, parallel_unit_no, len_parallel_units)

                    for j, (parallel_unit_raw, parallel_unit_search) in enumerate(concordance_line[1]):
                        label_parallel_unit = wl_labels.Wl_Label_Html(' '.join(parallel_unit_raw), self.main)
                        label_parallel_unit.text_raw = parallel_unit_raw
                        label_parallel_unit.text_search = parallel_unit_search

                        self.setIndexWidget(self.model().index(i, 2 + j), label_parallel_unit)
                        self.indexWidget(self.model().index(i, 2 + j)).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                self.enable_updates()

                self.toggle_pct_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

class Wl_Worker_Concordancer_Parallel_Table(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        texts = []
        parallel_units = {}
        offsets_paras_files = []

        try:
            settings = self.main.settings_custom['concordancer_parallel']

            files = list(self.main.wl_file_area.get_selected_files())
            len_files = len(files)

            # Parallel Unit No.
            for i, file in enumerate(files):
                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens_concordancer(
                    self.main, text,
                    token_settings = settings['token_settings'],
                    preserve_blank_lines = True
                )
                tokens = text.get_tokens_flat()
                offsets_paras, _, _ = text.get_offsets()

                offsets_paras_files.append(offsets_paras)

                # Save text
                texts.append(text)

                if (
                    not settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_term']
                    or settings['search_settings']['multi_search_mode'] and settings['search_settings']['search_terms']
                ):
                    search_terms = wl_matching.match_search_terms_ngrams(
                        self.main, tokens,
                        lang = text.lang,
                        tagged = text.tagged,
                        token_settings = settings['token_settings'],
                        search_settings = settings['search_settings']
                    )

                    (
                        search_terms_incl,
                        search_terms_excl
                    ) = wl_matching.match_search_terms_context(
                        self.main, tokens,
                        lang = text.lang,
                        tagged = text.tagged,
                        token_settings = settings['token_settings'],
                        context_settings = settings['context_settings']
                    )

                    if search_terms:
                        len_search_term_min = min((len(search_term) for search_term in search_terms))
                        len_search_term_max = max((len(search_term) for search_term in search_terms))
                    else:
                        len_search_term_min = 0
                        len_search_term_max = 0

                    for len_search_term in range(len_search_term_min, len_search_term_max + 1):
                        for j, ngram in enumerate(wl_nlp_utils.ngrams(tokens, len_search_term)):
                            if (
                                ngram in search_terms
                                and wl_matching.check_context(
                                    i, tokens,
                                    context_settings = settings['context_settings'],
                                    search_terms_incl = search_terms_incl,
                                    search_terms_excl = search_terms_excl
                                )
                            ):
                                parallel_unit_no = bisect.bisect(offsets_paras, j)

                                if parallel_unit_no not in parallel_units:
                                    parallel_units[parallel_unit_no] = [[] for _ in range(len_files)]

                                parallel_units[parallel_unit_no][i] = ngram
                # Search for additions & deletions
                else:
                    for i, para in enumerate(text.tokens_multilevel):
                        if para == []:
                            parallel_units[i] = [[] for _ in range(len_files)]

            len_max_parallel_units = max((len(offsets) for offsets in offsets_paras_files))

            for i, (text, offsets_paras) in enumerate(zip(texts, offsets_paras_files)):
                len_parallel_units = len(offsets_paras)

                for parallel_unit_no, parallel_unit_nodes in parallel_units.items():
                    node = parallel_unit_nodes[i]

                    if parallel_unit_no <= len_parallel_units:
                        # Search in Results
                        if settings['token_settings']['punc_marks']:
                            parallel_unit_raw = list(wl_misc.flatten_list(text.tokens_multilevel[parallel_unit_no - 1]))
                        else:
                            offset_para_start = offsets_paras[parallel_unit_no - 1]

                            if parallel_unit_no == len_parallel_units:
                                offset_para_end = None
                            else:
                                offset_para_end = offsets_paras[parallel_unit_no]

                            parallel_unit_raw = text.tokens_flat_punc_marks_merged[offset_para_start:offset_para_end]

                        parallel_unit_raw = wl_nlp_utils.escape_tokens(parallel_unit_raw)
                        parallel_unit_search = list(wl_misc.flatten_list(text.tokens_multilevel[parallel_unit_no - 1]))

                        # Highlight node if found
                        if node:
                            len_node = len(node)
                            len_parallel_unit_raw = len(parallel_unit_raw)
                            j = 0

                            while j < len_parallel_unit_raw:
                                if parallel_unit_raw[j : j + len_node] == list(node):
                                    parallel_unit_raw[j] = '<span style="color: red; font-weight: bold;">' + parallel_unit_raw[j]
                                    parallel_unit_raw[j + len_node - 1] += '</span>'

                                    j += len_node
                                else:
                                    j += 1
                    else:
                        parallel_unit_raw = []
                        parallel_unit_search = []

                    parallel_unit_nodes[i] = [parallel_unit_raw, parallel_unit_search]

            # Remove empty concordance lines
            for parallel_unit_no, parallel_units_files in parallel_units.copy().items():
                if not any(wl_misc.flatten_list(parallel_units_files)):
                    del parallel_units[parallel_unit_no]

            # Sort by Parallel Unit No.
            concordance_lines = sorted(parallel_units.items())

            for i, concordance_line in enumerate(concordance_lines):
                concordance_line = list(concordance_line)
                concordance_line[0] = [concordance_line[0], len_max_parallel_units]

                concordance_lines[i] = concordance_line
        except Exception:
            err_msg = traceback.format_exc()
            print(err_msg)

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(err_msg, concordance_lines)
