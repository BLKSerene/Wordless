# ----------------------------------------------------------------------
# Wordless: Dependency Parser
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

import bisect
import copy
import traceback

import numpy

from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QLabel, QPushButton

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_dependency_parsing, wl_matching, wl_nlp_utils, wl_token_processing
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import wl_boxes, wl_layouts, wl_tables, wl_widgets

_tr = QCoreApplication.translate

class Wl_Worker_Dependency_Parser(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        results = []

        try:
            settings = self.main.settings_custom['dependency_parser']

            for file in self.main.wl_file_area.get_selected_files():
                text = copy.deepcopy(file['text'])
                text = wl_token_processing.wl_process_tokens_concordancer(
                    self.main, text,
                    token_settings = settings['token_settings']
                )

                tokens = text.get_tokens_flat()
                _, offsets_sentences, _ = text.get_offsets()

                search_terms = wl_matching.match_search_terms_tokens(
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

                len_sentences = len(offsets_sentences)
                i_token = 0

                for para in text.tokens_multilevel:
                    for sentence in para:
                        sentence = list(wl_misc.flatten_list(sentence))

                        if any((token in search_terms for token in sentence)):
                            dependencies = wl_dependency_parsing.wl_dependency_parse(self.main, sentence, lang = text.lang)

                            for i, (token, head, dependency_relation, dependency_len) in enumerate(dependencies):
                                j = i_token + i

                                if (
                                    (token in search_terms or head in search_terms)
                                    and wl_matching.check_context(
                                        j, tokens,
                                        context_settings = settings['context_settings'],
                                        search_terms_incl = search_terms_incl,
                                        search_terms_excl = search_terms_excl
                                    )
                                ):
                                    results.append([])

                                    # Sentence No.
                                    no_sentence = bisect.bisect(offsets_sentences, j) - 1

                                    # Sentence
                                    if no_sentence == len_sentences - 1:
                                        offset_end = None
                                    else:
                                        offset_end = offsets_sentences[no_sentence + 1]

                                    sentence_display = text.tokens_flat_puncs_merged[offsets_sentences[no_sentence]:offset_end]
                                    sentence_display = wl_nlp_utils.escape_tokens(sentence_display)
                                    sentence_search = sentence

                                    # Head
                                    results[-1].append(head)
                                    # Dependant
                                    results[-1].append(token)
                                    # Dependency Relation
                                    results[-1].append(dependency_relation)
                                    # Dependency Distance
                                    results[-1].append(dependency_len)
                                    # Sentence
                                    results[-1].extend([sentence_display, sentence_search])
                                    # Sentence No.
                                    results[-1].extend([no_sentence, len_sentences])
                                    # File
                                    results[-1].append(file['name'])

                        i_token += len(sentence)
        except Exception:
            err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(err_msg, results)

class Wl_Table_Dependency_Parser(wl_tables.Wl_Table_Data_Search):
    def __init__(self, parent):
        super().__init__(
            parent,
            tab = 'dependency_parser',
            headers = [
                _tr('Wl_Table_Dependency_Parser', 'Head'),
                _tr('Wl_Table_Dependency_Parser', 'Dependent'),
                _tr('Wl_Table_Dependency_Parser', 'Dependency Relation'),
                _tr('Wl_Table_Dependency_Parser', 'Dependency Length'),
                _tr('Wl_Table_Dependency_Parser', 'Dependency Length (Absolute)'),
                _tr('Wl_Table_Dependency_Parser', 'Sentence'),
                _tr('Wl_Table_Dependency_Parser', 'Sentence No.'),
                _tr('Wl_Table_Dependency_Parser', 'Sentence No. %'),
                _tr('Wl_Table_Dependency_Parser', 'File')
            ],
            headers_int = [
                _tr('Wl_Table_Dependency_Parser', 'Dependency Length'),
                _tr('Wl_Table_Dependency_Parser', 'Dependency Length (Absolute)'),
                _tr('Wl_Table_Dependency_Parser', 'Sentence No.')
            ],
            headers_pct = [
                _tr('Wl_Table_Dependency_Parser', 'Sentence No. %')
            ],
            sorting_enabled = True
        )

        self.selectionModel().selectionChanged.connect(self.selection_changed_generate_fig)

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)
        self.button_generate_fig = QPushButton(self.tr('Generate Figure'), self)

        self.button_generate_table.clicked.connect(lambda: self.generate_table()) # pylint: disable=unnecessary-lambda
        self.button_generate_fig.clicked.connect(lambda: self.generate_fig()) # pylint: disable=unnecessary-lambda
        self.main.wl_file_area.table_files.model().itemChanged.connect(self.file_changed)

        self.main.wl_file_area.table_files.model().itemChanged.emit(QStandardItem())

    def selection_changed_generate_fig(self, selected, deselected): # pylint: disable=unused-argument
        if not self.is_empty() and self.is_visible() and self.is_selected():
            self.button_generate_fig.setEnabled(True)
        else:
            self.button_generate_fig.setEnabled(False)

    def file_changed(self, item): # pylint: disable=unused-argument
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)

    @wl_misc.log_timing
    def generate_table(self):
        if wl_checks_work_area.check_nlp_support(
            self.main,
            files = self.main.wl_file_area.get_selected_files(),
            nlp_utils = ['dependency_parsers']
        ) and wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['dependency_parser']['search_settings']
        ):
            worker_dependency_parser_table = Wl_Worker_Dependency_Parser(
                self.main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(self.main),
                update_gui = self.update_gui_table
            )

            wl_threading.Wl_Thread(worker_dependency_parser_table).start_worker()

    def update_gui_table(self, err_msg, results):
        if wl_checks_work_area.check_results(self.main, err_msg, results):
            try:
                self.settings = copy.deepcopy(self.main.settings_custom)

                self.clr_table(0)

                self.model().setRowCount(len(results))
                self.disable_updates()

                for i, (
                    head, dependent, dependency_relation, dependency_len,
                    sentence_display, sentence_search,
                    no_sentence, len_sentences, file
                ) in enumerate(results):
                    # Head
                    self.model().setItem(i, 0, QStandardItem(head))
                    # Dependant
                    self.model().setItem(i, 1, QStandardItem(dependent))
                    # Dependency Relation
                    self.model().setItem(i, 2, QStandardItem(dependency_relation))
                    # Dependency Distance
                    self.set_item_num(i, 3, dependency_len)
                    self.set_item_num(i, 4, numpy.abs(dependency_len))
                    # Sentence
                    self.model().setItem(i, 5, QStandardItem(' '.join(sentence_display)))
                    self.model().item(i, 5).text_display = sentence_display
                    self.model().item(i, 5).text_search = sentence_search
                    # Sentence No.
                    self.set_item_num(i, 6, no_sentence)
                    self.set_item_num(i, 7, no_sentence, len_sentences)
                    # File
                    self.model().setItem(i, 8, QStandardItem(file))

                self.enable_updates()

                self.toggle_pct()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

    @wl_misc.log_timing
    def generate_fig(self):
        err_msg = ''

        try:
            sentences_rendered = set()
            htmls = []

            fig_settings = self.main.settings_custom['dependency_parser']['fig_settings']

            for row in self.get_selected_rows():
                sentence = tuple(self.model().item(row, 5).text_display)

                if sentence not in sentences_rendered:
                    for file in self.settings['file_area']['files_open']:
                        if file['selected'] and file['name'] == self.model().item(row, 8).text():
                            file_selected = file

                    htmls.extend(wl_dependency_parsing.wl_dependency_parse_fig(
                        self.main,
                        inputs = sentence,
                        lang = file_selected['lang'],
                        show_pos_tags = fig_settings['show_pos_tags'],
                        show_fine_grained_pos_tags = fig_settings['show_fine_grained_pos_tags'],
                        show_lemmas = fig_settings['show_pos_tags'] and fig_settings['show_lemmas'],
                        collapse_puncs = False,
                        compact_mode = fig_settings['compact_mode'],
                        show_in_separate_tab = fig_settings['show_in_separate_tab'],
                    ))

                    sentences_rendered.add(sentence)

            wl_dependency_parsing.wl_show_dependency_graphs(
                self.main,
                htmls = htmls,
                show_in_separate_tab = fig_settings['show_in_separate_tab']
            )
        except Exception:
            err_msg = traceback.format_exc()
        finally:
            wl_checks_work_area.check_err_fig(self.main, err_msg)

class Wrapper_Dependency_Parser(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.table_dependency_parser = Wl_Table_Dependency_Parser(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_dependency_parser.label_number_results, 0, 0)
        layout_results.addWidget(self.table_dependency_parser.button_results_search, 0, 2)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_exp_selected, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_exp_all, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_clr, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_puncs,

            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings_concordancer(self)

        self.checkbox_puncs.stateChanged.connect(self.token_settings_changed)

        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 0, 0, 1, 2)

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
        ) = wl_widgets.wl_widgets_search_settings_tokens(
            self,
            tab = 'dependency_parser'
        )

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(
            self,
            tab = 'dependency_parser'
        )

        self.checkbox_multi_search_mode.stateChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.textChanged.connect(self.search_settings_changed)
        self.line_edit_search_term.returnPressed.connect(self.table_dependency_parser.button_generate_table.click)
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
            self.checkbox_show_pct,
            self.checkbox_show_cumulative,
            self.checkbox_show_breakdown
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_dependency_parser]
        )

        self.checkbox_show_cumulative.hide()
        self.checkbox_show_breakdown.hide()

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        self.checkbox_show_pos_tags = QCheckBox(self.tr('Show'), self)
        self.combo_box_show_pos_tags = wl_boxes.Wl_Combo_Box(self)
        self.label_show_pos_tags = QLabel(self.tr('part-of-speech tags'), self)
        self.checkbox_show_lemmas = QCheckBox(self.tr('Show lemmas'), self)
        self.checkbox_compact_mode = QCheckBox(self.tr('Compact mode'), self)
        self.checkbox_show_in_separate_tab = QCheckBox(self.tr('Show each sentence in a separate tab'), self)

        self.combo_box_show_pos_tags.addItems([
            self.tr('coarse-grained'),
            self.tr('fine-grained')
        ])

        self.checkbox_show_pos_tags.stateChanged.connect(self.fig_settings_changed)
        self.combo_box_show_pos_tags.currentTextChanged.connect(self.fig_settings_changed)
        self.checkbox_show_lemmas.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_compact_mode.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_show_in_separate_tab.stateChanged.connect(self.fig_settings_changed)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addWidget(self.checkbox_show_pos_tags, 0, 0)
        self.group_box_fig_settings.layout().addWidget(self.combo_box_show_pos_tags, 0, 1)
        self.group_box_fig_settings.layout().addWidget(self.label_show_pos_tags, 0, 2)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_show_lemmas, 1, 0, 1, 4)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_compact_mode, 2, 0, 1, 4)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_show_in_separate_tab, 3, 0, 1, 4)

        self.group_box_fig_settings.layout().setColumnStretch(3, 1)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_search_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_fig_settings, 3, 0)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['dependency_parser'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['dependency_parser'])

        # Token Settings
        self.checkbox_puncs.setChecked(settings['token_settings']['puncs'])

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
            self.main.wl_context_settings_dependency_parser.load_settings(defaults = True)

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])

        # Figure Settings
        self.checkbox_show_pos_tags.setChecked(settings['fig_settings']['show_pos_tags'])

        if settings['fig_settings']['show_fine_grained_pos_tags']:
            self.combo_box_show_pos_tags.setCurrentText(self.tr('fine-grained'))
        else:
            self.combo_box_show_pos_tags.setCurrentText(self.tr('coarse-grained'))

        self.checkbox_show_lemmas.setChecked(settings['fig_settings']['show_lemmas'])
        self.checkbox_compact_mode.setChecked(settings['fig_settings']['compact_mode'])
        self.checkbox_show_in_separate_tab.setChecked(settings['fig_settings']['show_in_separate_tab'])

        self.token_settings_changed()
        self.search_settings_changed()
        self.table_settings_changed()
        self.fig_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['dependency_parser']['token_settings']

        settings['puncs'] = self.checkbox_puncs.isChecked()

        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        self.checkbox_match_tags.token_settings_changed()
        self.main.wl_context_settings_dependency_parser.token_settings_changed()

    def search_settings_changed(self):
        settings = self.main.settings_custom['dependency_parser']['search_settings']

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
        settings = self.main.settings_custom['dependency_parser']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['dependency_parser']['fig_settings']

        # Show part-of-speech tags
        if self.checkbox_show_pos_tags.isChecked():
            self.combo_box_show_pos_tags.setEnabled(True)
            self.checkbox_show_lemmas.setEnabled(True)
        else:
            self.combo_box_show_pos_tags.setEnabled(False)
            self.checkbox_show_lemmas.setEnabled(False)

        settings['show_pos_tags'] = self.checkbox_show_pos_tags.isChecked()

        if self.combo_box_show_pos_tags.currentText() == self.tr('fine-grained'):
            settings['show_fine_grained_pos_tags'] = True
        elif self.combo_box_show_pos_tags.currentText() == self.tr('coarse-grained'):
            settings['show_fine_grained_pos_tags'] = False

        settings['show_lemmas'] = self.checkbox_show_lemmas.isChecked()
        settings['compact_mode'] = self.checkbox_compact_mode.isChecked()
        settings['show_in_separate_tab'] = self.checkbox_show_in_separate_tab.isChecked()
