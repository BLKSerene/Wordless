#
# Wordless: Overview
#
# Copyright (C) 2018-2019  Ye Lei (叶磊))
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import collections
import copy
import itertools
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy

from wordless_checking import wordless_checking_file
from wordless_dialogs import wordless_dialog_misc, wordless_msg_box
from wordless_text import wordless_text, wordless_text_utils, wordless_token_processing
from wordless_utils import wordless_misc, wordless_threading
from wordless_widgets import (wordless_box, wordless_layout, wordless_msg,
                              wordless_table, wordless_widgets)

class Wordless_Table_Overview(wordless_table.Wordless_Table_Data):
    def __init__(self, parent):
        super().__init__(parent,
                         headers = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Clauses'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Types'),
                             parent.tr('Count of Characters'),
                             parent.tr('Type-token Ratio'),
                             parent.tr('Type-token Ratio (Standardized)'),
                             parent.tr('Paragraph Length in Sentence (Mean)'),
                             parent.tr('Paragraph Length in Sentence (Standard Deviation)'),
                             parent.tr('Paragraph Length in Clause (Mean)'),
                             parent.tr('Paragraph Length in Clause (Standard Deviation)'),
                             parent.tr('Paragraph Length in Token (Mean)'),
                             parent.tr('Paragraph Length in Token (Standard Deviation)'),
                             parent.tr('Sentence Length in Token (Mean)'),
                             parent.tr('Sentence Length in Token (Standard Deviation)'),
                             parent.tr('Clause Length in Token (Mean)'),
                             parent.tr('Clause Length in Token (Standard Deviation)'),
                             parent.tr('Token Length in Character (Mean)'),
                             parent.tr('Token Length in Character (Standard Deviation)'),
                             parent.tr('Type Length in Character (Mean)'),
                             parent.tr('Type Length in Character (Standard Deviation)')
                         ],
                         header_orientation = 'vertical',
                         headers_num = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Clauses'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Types'),
                             parent.tr('Count of Characters'),
                             parent.tr('Type-token Ratio'),
                             parent.tr('Type-token Ratio (Standardized)'),
                             parent.tr('Paragraph Length in Sentence (Mean)'),
                             parent.tr('Paragraph Length in Sentence (Standard Deviation)'),
                             parent.tr('Paragraph Length in Clause (Mean)'),
                             parent.tr('Paragraph Length in Clause (Standard Deviation)'),
                             parent.tr('Paragraph Length in Token (Mean)'),
                             parent.tr('Paragraph Length in Token (Standard Deviation)'),
                             parent.tr('Sentence Length in Token (Mean)'),
                             parent.tr('Sentence Length in Token (Standard Deviation)'),
                             parent.tr('Clause Length in Token (Mean)'),
                             parent.tr('Clause Length in Token (Standard Deviation)'),
                             parent.tr('Token Length in Character (Mean)'),
                             parent.tr('Token Length in Character (Standard Deviation)'),
                             parent.tr('Type Length in Character (Mean)'),
                             parent.tr('Type Length in Character (Standard Deviation)')
                         ],
                         headers_pct = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Clauses'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Types'),
                             parent.tr('Count of Characters')
                         ],
                         headers_cumulative = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Clauses'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Characters')
                         ])
        
        self.name = 'overview'

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))

    def clear_table(self, count_headers = 1):
        super().clear_table(0)

        self.insert_col(0, self.tr('Total'))

class Wrapper_Overview(wordless_layout.Wordless_Wrapper):
    def __init__(self, main):
        super().__init__(main)

        # Table
        self.table_overview = Wordless_Table_Overview(self)

        self.wrapper_table.layout().addWidget(self.table_overview, 0, 0, 1, 4)
        self.wrapper_table.layout().addWidget(self.table_overview.button_generate_table, 1, 0)
        self.wrapper_table.layout().addWidget(self.table_overview.button_export_selected, 1, 1)
        self.wrapper_table.layout().addWidget(self.table_overview.button_export_all, 1, 2)
        self.wrapper_table.layout().addWidget(self.table_overview.button_clear, 1, 3)
        
        # Token Settings
        self.group_box_token_settings = QGroupBox(self.tr('Token Settings'), self)

        (self.checkbox_words,
         self.checkbox_lowercase,
         self.checkbox_uppercase,
         self.checkbox_title_case,
         self.checkbox_nums,
         self.checkbox_puncs,

         self.checkbox_treat_as_lowercase,
         self.checkbox_lemmatize_tokens,
         self.checkbox_filter_stop_words,

         self.stacked_widget_ignore_tags,
         self.checkbox_ignore_tags,
         self.checkbox_ignore_tags_tags,

         self.stacked_widget_ignore_tags_type,
         self.combo_box_ignore_tags,
         self.combo_box_ignore_tags_tags,

         self.label_ignore_tags,
         self.checkbox_use_tags) = wordless_widgets.wordless_widgets_token_settings(self)

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
        self.checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = wordless_layout.Wordless_Layout()
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        self.group_box_token_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_token_settings.layout().addWidget(self.checkbox_words, 0, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lowercase, 0, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_uppercase, 1, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_title_case, 1, 1)
        self.group_box_token_settings.layout().addWidget(self.checkbox_nums, 2, 0)
        self.group_box_token_settings.layout().addWidget(self.checkbox_puncs, 2, 1)

        self.group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 3, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(self.checkbox_treat_as_lowercase, 4, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_lemmatize_tokens, 5, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_filter_stop_words, 6, 0, 1, 2)

        self.group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(self), 7, 0, 1, 2)

        self.group_box_token_settings.layout().addLayout(layout_ignore_tags, 8, 0, 1, 2)
        self.group_box_token_settings.layout().addWidget(self.checkbox_use_tags, 9, 0, 1, 2)

        # Generation Settings
        self.group_box_generation_settings = QGroupBox(self.tr('Generation Settings'), self)

        self.label_base_sttr = QLabel(self.tr('Base of standardized type-token ratio:'), self)
        self.spin_box_base_sttr = wordless_box.Wordless_Spin_Box(self)

        self.spin_box_base_sttr.setRange(100, 10000)

        self.spin_box_base_sttr.valueChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_generation_settings.layout().addWidget(self.label_base_sttr, 0, 0)
        self.group_box_generation_settings.layout().addWidget(self.spin_box_base_sttr, 1, 0)

        # Table Settings
        self.group_box_table_settings = QGroupBox(self.tr('Table Settings'), self)

        (self.checkbox_show_pct,
         self.checkbox_show_cumulative,
         self.checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(self,
                                                                                          table = self.table_overview)

        self.checkbox_show_pct.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_cumulative.stateChanged.connect(self.table_settings_changed)
        self.checkbox_show_breakdown.stateChanged.connect(self.table_settings_changed)

        self.group_box_table_settings.setLayout(wordless_layout.Wordless_Layout())
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_pct, 0, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_cumulative, 1, 0)
        self.group_box_table_settings.layout().addWidget(self.checkbox_show_breakdown, 2, 0)

        self.wrapper_settings.layout().addWidget(self.group_box_token_settings, 0, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_generation_settings, 1, 0)
        self.wrapper_settings.layout().addWidget(self.group_box_table_settings, 2, 0)

        self.wrapper_settings.layout().setRowStretch(3, 1)

        self.load_settings()

    def load_settings(self, defaults = False):
        if defaults:
            settings = copy.deepcopy(self.main.settings_default['overview'])
        else:
            settings = copy.deepcopy(self.main.settings_custom['overview'])

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
        self.checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
        self.checkbox_use_tags.setChecked(settings['token_settings']['use_tags'])

        # Generation Settings
        self.spin_box_base_sttr.setValue(settings['generation_settings']['base_sttr'])

        # Table Settings
        self.checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        self.checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        self.checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        self.token_settings_changed()
        self.generation_settings_changed()
        self.table_settings_changed()

    def token_settings_changed(self):
        settings = self.main.settings_custom['overview']['token_settings']

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
        settings['ignore_tags_tags'] = self.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

        if settings['use_tags']:
            self.label_base_sttr.setText(self.tr('Base of standardized type-tag ratio:'))
        else:
            self.label_base_sttr.setText(self.tr('Base of standardized type-token ratio:'))

    def generation_settings_changed(self):
        settings = self.main.settings_custom['overview']['generation_settings']

        settings['base_sttr'] = self.spin_box_base_sttr.value()

    def table_settings_changed(self):
        settings = self.main.settings_custom['overview']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

class Wordless_Worker_Overview(wordless_threading.Wordless_Worker):
    worker_done = pyqtSignal(list)

    def __init__(self, main, dialog_progress, update_gui):
        super().__init__(main, dialog_progress, update_gui)

        self.texts_stats_files = []

    def run(self):
        texts = []

        settings = self.main.settings_custom['overview']
        files = self.main.wordless_files.get_selected_files()

        for i, file in enumerate(files):
            text = wordless_text.Wordless_Text(self.main, file, flat_tokens = False)
            wordless_token_processing.wordless_process_tokens_overview(text,
                                                                       token_settings = settings['token_settings'])

            texts.append(text)

        if len(files) > 1:
            text_total = wordless_text.Wordless_Text_Blank()
            text_total.offsets_paras = [offset
                                        for text in texts
                                        for offset in text.offsets_paras]
            text_total.offsets_sentences = [offset
                                            for text in texts
                                            for offset in text.offsets_sentences]
            text_total.offsets_clauses = [offset
                                          for text in texts
                                          for offset in text.offsets_clauses]
            text_total.tokens_hierarchical = [para
                                              for text in texts
                                              for para in text.tokens_hierarchical]
            text_total.tokens_flat = [token
                                      for text in texts
                                      for token in text.tokens_flat]

            texts.append(text_total)
        else:
            texts.append(texts[0])

        self.progress_updated.emit(self.tr('Processing data ...'))

        base_sttr = settings['generation_settings']['base_sttr']

        for text in texts:
            texts_stats_file = []

            # Paragraph length
            len_paras_in_sentence = [len(para) for para in text.tokens_hierarchical]
            len_paras_in_clause = [sum([len(sentence) for sentence in para])
                                   for para in text.tokens_hierarchical]
            len_paras_in_token = [sum([len(clause) for sentence in para for clause in sentence])
                                  for para in text.tokens_hierarchical]

            # Sentence length
            len_sentences = [sum([len(clause) for clause in sentence])
                             for para in text.tokens_hierarchical
                             for sentence in para]

            # Clause length
            len_clauses = [len(clause)
                           for para in text.tokens_hierarchical
                           for sentence in para
                           for clause in sentence]

            # Token length
            len_tokens = [len(token) for token in text.tokens_flat]
            # Type length
            len_types = [len(token_type) for token_type in set(text.tokens_flat)]

            count_tokens = len(len_tokens)
            count_types = len(len_types)

            # TTR
            if count_tokens == 0:
                ttr = 0
            else:
                ttr = count_types / count_tokens

            # STTR
            if count_tokens < base_sttr:
                sttr = ttr
            else:
                token_sections = wordless_text_utils.to_sections_unequal(text.tokens_flat, base_sttr)

                # Discard the last section if number of tokens in it is smaller than the base of sttr
                if len(token_sections[-1]) < base_sttr:
                    ttrs = [len(set(token_section)) / len(token_section) for token_section in token_sections[:-1]]
                else:
                    ttrs = [len(set(token_section)) / len(token_section) for token_section in token_sections]

                sttr = sum(ttrs) / len(ttrs)

            texts_stats_file.append(len_paras_in_sentence)
            texts_stats_file.append(len_paras_in_clause)
            texts_stats_file.append(len_paras_in_token)
            texts_stats_file.append(len_sentences)
            texts_stats_file.append(len_clauses)
            texts_stats_file.append(len_tokens)
            texts_stats_file.append(len_types)
            texts_stats_file.append(ttr)
            texts_stats_file.append(sttr)

            self.texts_stats_files.append(texts_stats_file)

class Wordless_Worker_Overview_Table(Wordless_Worker_Overview):
    def run(self):
        super().run()

        self.progress_updated.emit(self.tr('Rendering table ...'))

        time.sleep(0.1)

        self.worker_done.emit(self.texts_stats_files)

@wordless_misc.log_timing
def generate_table(main, table):
    def update_gui(texts_stats_files):
        if any(itertools.chain.from_iterable(texts_stats_files)):
            table.settings = copy.deepcopy(main.settings_custom)

            table.blockSignals(True)
            table.setUpdatesEnabled(False)

            table.clear_table()

            len_tokens_files = []

            for i, file in enumerate(files):
                table.insert_col(table.find_col(main.tr('Total')), file['name'], breakdown = True)

            for i, stats in enumerate(texts_stats_files):
                len_paras_in_sentence = stats[0]
                len_paras_in_clause = stats[1]
                len_paras_in_token = stats[2]
                len_sentences = stats[3]
                len_clauses = stats[4]
                len_tokens = stats[5]
                len_types = stats[6]
                ttr = stats[7]
                sttr = stats[8]

                count_paras = len(len_paras_in_token)
                count_sentences = len(len_sentences)
                count_clauses = len(len_clauses)
                count_tokens = len(len_tokens)
                count_types = len(len_types)
                count_chars = sum(len_tokens)

                # Count of Paragraphs
                table.set_item_num_cumulative(0, i, count_paras)
                # Count of Sentences
                table.set_item_num_cumulative(1, i, count_sentences)
                # Count of Clauses
                table.set_item_num_cumulative(2, i, count_clauses)
                # Count of Tokens
                table.set_item_num_cumulative(3, i, count_tokens)
                # Count of Types
                table.set_item_num_pct(4, i, count_types)
                # Count of Characters
                table.set_item_num_cumulative(5, i, count_chars)
                # Type-token Ratio
                table.set_item_num_float(6, i, ttr)
                # Type-token Ratio (Standardized)
                table.set_item_num_float(7, i, sttr)

                # Paragraph Length
                if count_paras == 0:
                    table.set_item_num_float(8, i, 0)
                    table.set_item_num_float(9, i, 0)
                    table.set_item_num_float(10, i, 0)
                    table.set_item_num_float(11, i, 0)
                    table.set_item_num_float(12, i, 0)
                    table.set_item_num_float(13, i, 0)
                else:
                    table.set_item_num_float(8, i, numpy.mean(len_paras_in_sentence))
                    table.set_item_num_float(9, i, numpy.std(len_paras_in_sentence))
                    table.set_item_num_float(10, i, numpy.mean(len_paras_in_clause))
                    table.set_item_num_float(11, i, numpy.std(len_paras_in_clause))
                    table.set_item_num_float(12, i, numpy.mean(len_paras_in_token))
                    table.set_item_num_float(13, i, numpy.std(len_paras_in_token))

                # Sentence Length
                if count_sentences == 0:
                    table.set_item_num_float(14, i, 0)
                    table.set_item_num_float(15, i, 0)
                else:
                    table.set_item_num_float(14, i, numpy.mean(len_sentences))
                    table.set_item_num_float(15, i, numpy.std(len_sentences))

                # Clause Length
                if count_clauses == 0:
                    table.set_item_num_float(16, i, 0)
                    table.set_item_num_float(17, i, 0)
                else:
                    table.set_item_num_float(16, i, numpy.mean(len_clauses))
                    table.set_item_num_float(17, i, numpy.std(len_clauses))

                # Token Length
                if count_tokens == 0:
                    table.set_item_num_float(18, i, 0)
                    table.set_item_num_float(19, i, 0)
                else:
                    table.set_item_num_float(18, i, numpy.mean(len_tokens))
                    table.set_item_num_float(19, i, numpy.std(len_tokens))

                # Type Length
                if count_types == 0:
                    table.set_item_num_float(20, i, 0)
                    table.set_item_num_float(21, i, 0)
                else:
                    table.set_item_num_float(20, i, numpy.mean(len_types))
                    table.set_item_num_float(21, i, numpy.std(len_types))

                len_tokens_files.append(collections.Counter(len_tokens))

            # Count of n-length Tokens
            len_files = len(files)
            len_tokens_total = wordless_misc.merge_dicts(len_tokens_files)
            len_tokens_max = max(len_tokens_total)

            # Use tags only
            if settings['token_settings']['use_tags']:
                table.setVerticalHeaderLabels([
                    main.tr('Count of Paragraphs'),
                    main.tr('Count of Sentences'),
                    main.tr('Count of Clauses'),
                    main.tr('Count of Tags'),
                    main.tr('Count of Tag Types'),
                    main.tr('Count of Characters'),
                    main.tr('Type-tag Ratio'),
                    main.tr('Type-tag Ratio (Standardized)'),
                    main.tr('Paragraph Length in Sentence (Mean)'),
                    main.tr('Paragraph Length in Sentence (Standard Deviation)'),
                    main.tr('Paragraph Length in Sentence (Mean)'),
                    main.tr('Paragraph Length in Sentence (Standard Deviation)'),
                    main.tr('Paragraph Length in Tag (Mean)'),
                    main.tr('Paragraph Length in Tag (Standard Deviation)'),
                    main.tr('Sentence Length in Tag (Mean)'),
                    main.tr('Sentence Length in Tag (Standard Deviation)'),
                    main.tr('Clause Length in Tag (Mean)'),
                    main.tr('Clause Length in Tag (Standard Deviation)'),
                    main.tr('Tag Length in Character (Mean)'),
                    main.tr('Tag Length in Character (Standard Deviation)'),
                    main.tr('Tag Type Length in Character (Mean)'),
                    main.tr('Tag Type Length in Character (Standard Deviation)')
                ])

                for i in range(len_tokens_max):
                    table.insert_row(table.rowCount(),
                                     main.tr(f'Count of {i + 1}-length Tags'),
                                     num = True, pct = True, cumulative = True)
            else:
                for i in range(len_tokens_max):

                    table.insert_row(table.rowCount(),
                                     main.tr(f'Count of {i + 1}-length Tokens'),
                                     num = True, pct = True, cumulative = True)

            for i in range(len_tokens_max):
                freqs = len_tokens_total.get(i + 1, [0] * (len_files + 1))

                for j, freq in enumerate(freqs):
                    table.set_item_num_cumulative(table.rowCount() - len_tokens_max + i, j, freq)

            table.blockSignals(False)
            table.setUpdatesEnabled(True)

            table.toggle_pct()
            table.toggle_cumulative()
            table.toggle_breakdown()
            table.update_items_width()

            table.itemChanged.emit(table.item(0, 0))

            wordless_msg.wordless_msg_generate_table_success(main)
        else:
            wordless_msg_box.wordless_msg_box_no_results(main)

            wordless_msg.wordless_msg_generate_table_error(main)

        dialog_progress.accept()

    settings = main.settings_custom['overview']
    files = main.wordless_files.get_selected_files()

    if wordless_checking_file.check_files_on_loading(main, files):
        dialog_progress = wordless_dialog_misc.Wordless_Dialog_Progress_Process_Data(main)

        worker_overview_table = Wordless_Worker_Overview_Table(main, dialog_progress, update_gui)
        thread_overview_table = wordless_threading.Wordless_Thread(worker_overview_table)

        thread_overview_table.start()

        dialog_progress.exec_()

        thread_overview_table.quit()
        thread_overview_table.wait()
    else:
        wordless_msg.wordless_msg_generate_table_error(main)
