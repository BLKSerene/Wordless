# ----------------------------------------------------------------------
# Wordless: Work Area - Dependency Parser
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

import bisect
import copy
import traceback

import numpy

from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
from PyQt5.QtWidgets import QCheckBox, QGroupBox

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import (
    wl_dependency_parsing,
    wl_matching,
    wl_texts,
    wl_token_processing,
    wl_nlp_utils
)
from wordless.wl_utils import wl_misc, wl_threading
from wordless.wl_widgets import (
    wl_labels,
    wl_layouts,
    wl_tables,
    wl_widgets
)

_tr = QCoreApplication.translate

class Wrapper_Dependency_Parser(wl_layouts.Wl_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        self.tab = 'dependency_parser'

        # Table
        self.table_dependency_parser = Wl_Table_Dependency_Parser(self)

        layout_results = wl_layouts.Wl_Layout()
        layout_results.addWidget(self.table_dependency_parser.label_num_results, 0, 0)
        layout_results.addWidget(self.table_dependency_parser.button_results_filter, 0, 2)
        layout_results.addWidget(self.table_dependency_parser.button_results_search, 0, 3)

        layout_results.setColumnStretch(1, 1)

        self.wrapper_table.layout().addLayout(layout_results, 0, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser, 1, 0, 1, 5)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_generate_table, 2, 0)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_generate_fig, 2, 1)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_exp_selected_cells, 2, 2)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_exp_all_cells, 2, 3)
        self.wrapper_table.layout().addWidget(self.table_dependency_parser.button_clr_table, 2, 4)

        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (
            self.checkbox_punc_marks,

            self.checkbox_assign_pos_tags,
            self.checkbox_ignore_tags,
            self.checkbox_use_tags
        ) = wl_widgets.wl_widgets_token_settings_concordancer(self)

        self.checkbox_punc_marks.stateChanged.connect(self.token_settings_changed)

        self.checkbox_assign_pos_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        self.group_box_token_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_punc_marks, 0, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 1, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_assign_pos_tags, 2, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_ignore_tags, 3, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 3, 1)

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
        ) = wl_widgets.wl_widgets_search_settings_tokens(self, tab = self.tab)
        self.checkbox_match_dependency_relations = QCheckBox(self.tr('Match dependency relations'), self)

        (
            self.label_context_settings,
            self.button_context_settings
        ) = wl_widgets.wl_widgets_context_settings(self, tab = self.tab)

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
        self.checkbox_match_dependency_relations.stateChanged.connect(self.search_settings_changed)

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
        self.group_box_search_settings.layout().addWidget(self.checkbox_match_dependency_relations, 9, 0, 1, 2)

        self.group_box_search_settings.layout().addWidget(wl_layouts.Wl_Separator(self), 10, 0, 1, 2)

        self.group_box_search_settings.layout().addLayout(layout_context_settings, 11, 0, 1, 2)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (
            self.checkbox_show_pct_data,
            self.checkbox_show_cum_data,
            self.checkbox_show_breakdown_file
        ) = wl_widgets.wl_widgets_table_settings(
            self,
            tables = [self.table_dependency_parser]
        )

        self.checkbox_show_cum_data.hide()
        self.checkbox_show_breakdown_file.hide()

        self.checkbox_show_pct_data.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct_data, 0, 0)

        # Figure Settings
        self.group_box_fig_settings = QGroupBox(self.tr('Figure Settings'), self)

        (
            self.checkbox_show_pos_tags, self.combo_box_show_pos_tags, self.label_show_pos_tags,
            self.checkbox_show_lemmas,
            self.checkbox_collapse_punc_marks,
            self.checkbox_compact_mode,
            self.checkbox_show_in_separate_tab
        ) = wl_widgets.wl_widgets_fig_settings_dependency_parsing(self)

        self.checkbox_collapse_punc_marks.hide()

        self.checkbox_show_pos_tags.stateChanged.connect(self.fig_settings_changed)
        self.combo_box_show_pos_tags.currentTextChanged.connect(self.fig_settings_changed)
        self.checkbox_show_lemmas.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_collapse_punc_marks.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_compact_mode.stateChanged.connect(self.fig_settings_changed)
        self.checkbox_show_in_separate_tab.stateChanged.connect(self.fig_settings_changed)

        self.group_box_fig_settings.setLayout(wl_layouts.Wl_Layout())
        self.group_box_fig_settings.layout().addWidget(self.checkbox_show_pos_tags, 0, 0)
        self.group_box_fig_settings.layout().addWidget(self.combo_box_show_pos_tags, 0, 1)
        self.group_box_fig_settings.layout().addWidget(self.label_show_pos_tags, 0, 2)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_show_lemmas, 1, 0, 1, 4)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_collapse_punc_marks, 2, 0, 1, 4)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_compact_mode, 3, 0, 1, 4)
        self.group_box_fig_settings.layout().addWidget(self.checkbox_show_in_separate_tab, 4, 0, 1, 4)

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
        self.checkbox_punc_marks.setChecked(settings['token_settings']['punc_marks'])

        self.checkbox_assign_pos_tags.setChecked(settings['token_settings']['assign_pos_tags'])
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
        self.checkbox_match_dependency_relations.setChecked(settings['search_settings']['match_dependency_relations'])

        # Context Settings
        if defaults:
            self.main.wl_context_settings_dependency_parser.load_settings(defaults = True)

        # Table Settings
        self.checkbox_show_pct_data.setChecked(settings['table_settings']['show_pct_data'])

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

        self.checkbox_show_pos_tags.stateChanged.emit(self.checkbox_show_pos_tags.checkState())

    def token_settings_changed(self):
        settings = self.main.settings_custom['dependency_parser']['token_settings']

        settings['punc_marks'] = self.checkbox_punc_marks.isChecked()

        settings['assign_pos_tags'] = self.checkbox_assign_pos_tags.isChecked()
        settings['ignore_tags'] = self.checkbox_ignore_tags.isChecked()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        self.checkbox_match_tags.token_settings_changed()

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
        settings['match_dependency_relations'] = self.checkbox_match_dependency_relations.isChecked()

        # Match dependency relations
        if settings['match_dependency_relations']:
            self.checkbox_match_inflected_forms.setEnabled(False)
            self.checkbox_match_without_tags.setEnabled(False)
            self.checkbox_match_tags.setEnabled(False)
        else:
            self.checkbox_match_tags.token_settings_changed()

    def table_settings_changed(self):
        settings = self.main.settings_custom['dependency_parser']['table_settings']

        settings['show_pct_data'] = self.checkbox_show_pct_data.isChecked()

    def fig_settings_changed(self):
        settings = self.main.settings_custom['dependency_parser']['fig_settings']

        settings['show_pos_tags'] = self.checkbox_show_pos_tags.isChecked()

        if self.combo_box_show_pos_tags.currentText() == self.tr('fine-grained'):
            settings['show_fine_grained_pos_tags'] = True
        elif self.combo_box_show_pos_tags.currentText() == self.tr('coarse-grained'):
            settings['show_fine_grained_pos_tags'] = False

        settings['show_lemmas'] = self.checkbox_show_lemmas.isChecked()
        settings['compact_mode'] = self.checkbox_compact_mode.isChecked()
        settings['show_in_separate_tab'] = self.checkbox_show_in_separate_tab.isChecked()

class Wl_Table_Dependency_Parser(wl_tables.Wl_Table_Data_Filter_Search):
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
            enable_sorting = True
        )

        self.selectionModel().selectionChanged.connect(self.selection_changed_generate_fig)

    # Enable the button "Generate figure" when table cells are selected, not when there are files opened
    def selection_changed_generate_fig(self):
        if not self.is_empty() and self.is_visible() and self.is_selected():
            self.button_generate_fig.setEnabled(True)
        else:
            self.button_generate_fig.setEnabled(False)

    def file_changed(self):
        if list(self.main.wl_file_area.get_selected_files()):
            self.button_generate_table.setEnabled(True)
        else:
            self.button_generate_table.setEnabled(False)

    @wl_misc.log_time
    def generate_table(self):
        if wl_checks_work_area.check_search_terms(
            self.main,
            search_settings = self.main.settings_custom['dependency_parser']['search_settings']
        ):
            if self.main.settings_custom['dependency_parser']['token_settings']['assign_pos_tags']:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(
                    self.main,
                    nlp_utils = ['pos_taggers', 'dependency_parsers']
                )
            else:
                nlp_support_ok = wl_checks_work_area.check_nlp_support(
                    self.main,
                    nlp_utils = ['dependency_parsers']
                )

            if nlp_support_ok:
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
                    sentence_tokens_raw, sentence_tokens_fig, sentence_tokens_search,
                    no_sentence, len_sentences, file
                ) in enumerate(results):
                    # Head
                    self.model().setItem(i, 0, wl_tables.Wl_Table_Item(head.display_text()))
                    self.model().item(i, 0).tokens_filter = [head]

                    # Dependent
                    self.model().setItem(i, 1, wl_tables.Wl_Table_Item(dependent.display_text()))
                    self.model().item(i, 1).tokens_filter = [dependent]

                    # Dependency Relation
                    self.model().setItem(i, 2, wl_tables.Wl_Table_Item(dependency_relation))

                    # Dependency Length
                    self.set_item_num(i, 3, dependency_len)
                    self.set_item_num(i, 4, numpy.abs(dependency_len))

                    # Sentence
                    self.setIndexWidget(
                        self.model().index(i, 5),
                        wl_labels.Wl_Label_Html(' '.join(sentence_tokens_raw), self.main)
                    )
                    self.indexWidget(self.model().index(i, 5)).tokens_raw = sentence_tokens_raw
                    self.indexWidget(self.model().index(i, 5)).tokens_fig = sentence_tokens_fig
                    self.indexWidget(self.model().index(i, 5)).tokens_search = sentence_tokens_search

                    # Sentence No.
                    self.set_item_num(i, 6, no_sentence)
                    self.set_item_num(i, 7, no_sentence, len_sentences)

                    # File
                    self.model().setItem(i, 8, wl_tables.Wl_Table_Item(file))

                self.enable_updates()

                self.toggle_pct_data()
            except Exception:
                err_msg = traceback.format_exc()
            finally:
                wl_checks_work_area.check_err_table(self.main, err_msg)

    @wl_misc.log_time
    def generate_fig(self):
        err_msg = ''

        try:
            sentences_rendered = set()
            htmls = []

            fig_settings = self.main.settings_custom['dependency_parser']['fig_settings']

            for row in self.get_selected_rows():
                sentence = tuple(self.indexWidget(self.model().index(row, 5)).tokens_fig)

                if sentence not in sentences_rendered:
                    for file in self.settings['file_area']['files_open']:
                        if file['name'] == self.model().item(row, 8).text():
                            file_selected = file

                    htmls.extend(wl_dependency_parsing.wl_dependency_parse_fig(
                        self.main,
                        inputs = sentence,
                        lang = file_selected['lang'],
                        show_pos_tags = fig_settings['show_pos_tags'],
                        show_fine_grained_pos_tags = fig_settings['show_fine_grained_pos_tags'],
                        show_lemmas = fig_settings['show_pos_tags'] and fig_settings['show_lemmas'],
                        # Handled by Token Settings - Punctuation marks
                        collapse_punc_marks = False,
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

class Wl_Worker_Dependency_Parser(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str, list)

    def run(self):
        err_msg = ''
        results = []

        try:
            settings = self.main.settings_custom['dependency_parser']

            for file in self.main.wl_file_area.get_selected_files():
                text = wl_token_processing.wl_process_tokens_dependency_parser(
                    self.main, file['text'],
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                tokens = text.get_tokens_flat()
                _, offsets_sentences, _ = text.get_offsets()

                search_terms = wl_matching.match_search_terms_tokens(
                    self.main, tokens,
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    search_settings = settings['search_settings']
                )

                (
                    search_terms_incl,
                    search_terms_excl
                ) = wl_matching.match_search_terms_context(
                    self.main, tokens,
                    lang = text.lang,
                    token_settings = settings['token_settings'],
                    context_settings = settings['search_settings']['context_settings']
                )

                len_sentences = len(offsets_sentences)
                i_token = 0

                head_color = self.main.settings_custom['tables']['dependency_parser']['highlight_color_settings']['head_color']
                dependent_color = self.main.settings_custom['tables']['dependency_parser']['highlight_color_settings']['dependent_color']

                for para in text.tokens_multilevel:
                    for sentence in para:
                        sentence = list(wl_misc.flatten_list(sentence))

                        dependencies = [
                            (token, token.head, token.dependency_relation)
                            for token in sentence
                        ]

                        for i, (token, head, dependency_relation) in enumerate(dependencies):
                            j = i_token + i

                            if (
                                (
                                    (
                                        not settings['search_settings']['match_dependency_relations']
                                        and (token in search_terms or head in search_terms)
                                    ) or (
                                        settings['search_settings']['match_dependency_relations']
                                        and dependency_relation in wl_texts.to_display_texts(search_terms)
                                    )
                                ) and (
                                    # Ignore cases where heads are punctuation marks
                                    token.head is not None
                                    and wl_matching.check_context(
                                        j, tokens,
                                        context_settings = settings['search_settings']['context_settings'],
                                        search_terms_incl = search_terms_incl,
                                        search_terms_excl = search_terms_excl
                                    )
                                )
                            ):
                                results.append([])

                                # Sentence No.
                                no_sentence = bisect.bisect(offsets_sentences, j)

                                # Sentence
                                sentence_tokens_raw = []
                                sentence_tokens_fig = []
                                # Calculate dependency length based on modified tokens
                                i_head = -1
                                i_dependent = -1

                                # Highlight heads and dependents
                                for i, sentence_token in enumerate(sentence):
                                    if sentence_token is head:
                                        sentence_tokens_raw.append(f'''
                                            <span style="color: {head_color}; font-weight: bold;">
                                                {wl_nlp_utils.escape_token(sentence_token.display_text(punc_mark = True))}
                                            </span>
                                        ''')

                                        i_head = i

                                        # Roots are both the head and the dependent
                                        if sentence_token is token:
                                            i_dependent = i
                                    elif sentence_token is token:
                                        sentence_tokens_raw.append(f'''
                                            <span style="color: {dependent_color}; font-weight: bold;">
                                                {wl_nlp_utils.escape_token(sentence_token.display_text(punc_mark = True))}
                                            </span>
                                        ''')

                                        i_dependent = i
                                    else:
                                        sentence_tokens_raw.append(
                                            wl_nlp_utils.escape_token(sentence_token.display_text(punc_mark = True))
                                        )

                                    sentence_tokens_fig.append(copy.deepcopy(sentence_token))

                                if settings['token_settings']['punc_marks']:
                                    # Remove empty tokens for searching in results
                                    sentence_tokens_search = [token for token in copy.deepcopy(sentence) if token]
                                # Convert trailing punctuation marks, if any, to separate tokens for searching
                                else:
                                    sentence_tokens_search = []

                                    for sentence_token in copy.deepcopy(sentence):
                                        sentence_tokens_search.append(sentence_token)

                                        if sentence_token.punc_mark:
                                            sentence_tokens_search.append(wl_texts.Wl_Token(
                                                sentence_token.punc_mark,
                                                lang = sentence_token.lang
                                            ))

                                # Head
                                results[-1].append(head)
                                # Dependent
                                results[-1].append(token)
                                # Dependency Relation
                                results[-1].append(dependency_relation)
                                # Dependency Length
                                results[-1].append(i_head - i_dependent)
                                # Sentence
                                results[-1].extend([sentence_tokens_raw, sentence_tokens_fig, sentence_tokens_search])
                                # Sentence No.
                                results[-1].extend([no_sentence, len_sentences])
                                # File
                                results[-1].append(file['name'])

                        i_token += len(sentence)
        except Exception:
            err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Rendering table...'))
        self.worker_done.emit(err_msg, results)
