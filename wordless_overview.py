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
import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_checking import *
from wordless_dialogs import *
from wordless_text import *
from wordless_utils import *
from wordless_widgets import *

class Wordless_Table_Overview(wordless_table.Wordless_Table_Data):
    def __init__(self, parent):
        super().__init__(parent,
                         headers = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Types'),
                             parent.tr('Count of Characters'),
                             parent.tr('Type/Token Ratio'),
                             parent.tr('Type/Token Ratio (Standardized)'),
                             parent.tr('Average Paragraph Length (in Sentence)'),
                             parent.tr('Average Paragraph Length (in Token)'),
                             parent.tr('Average Sentence Length (in Token)'),
                             parent.tr('Average Token Length (in Character)')
                         ],
                         header_orientation = 'vertical',
                         headers_num = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Types'),
                             parent.tr('Count of Characters'),
                             parent.tr('Type/Token Ratio'),
                             parent.tr('Type/Token Ratio (Standardized)'),
                             parent.tr('Average Paragraph Length (in Sentence)'),
                             parent.tr('Average Paragraph Length (in Token)'),
                             parent.tr('Average Sentence Length (in Token)'),
                             parent.tr('Average Token Length (in Character)')
                         ],
                         headers_pct = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Types'),
                             parent.tr('Count of Characters')
                         ],
                         headers_cumulative = [
                             parent.tr('Count of Paragraphs'),
                             parent.tr('Count of Sentences'),
                             parent.tr('Count of Tokens'),
                             parent.tr('Count of Characters')
                         ])

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
         self.stacked_widget_ignore_tags_type,
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

        self.stacked_widget_ignore_tags.checkbox_ignore_tags.stateChanged.connect(self.token_settings_changed)
        self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.stateChanged.connect(self.token_settings_changed)
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentTextChanged.connect(self.token_settings_changed)
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentTextChanged.connect(self.token_settings_changed)
        self.checkbox_use_tags.stateChanged.connect(self.token_settings_changed)

        layout_ignore_tags = QGridLayout()
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags, 0, 0)
        layout_ignore_tags.addWidget(self.stacked_widget_ignore_tags_type, 0, 1)
        layout_ignore_tags.addWidget(self.label_ignore_tags, 0, 2)

        layout_ignore_tags.setColumnStretch(3, 1)

        self.group_box_token_settings.setLayout(QGridLayout())
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

        self.label_base_sttr = QLabel(self.tr('Base of standardized type/token ratio:'), self)
        self.spin_box_base_sttr = QSpinBox(self)

        self.spin_box_base_sttr.setRange(100, 10000)

        self.spin_box_base_sttr.valueChanged.connect(self.generation_settings_changed)

        self.group_box_generation_settings.setLayout(QGridLayout())
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

        self.group_box_table_settings.setLayout(QGridLayout())
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

        self.stacked_widget_ignore_tags.checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.setChecked(settings['token_settings']['ignore_tags_tags'])
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.setCurrentText(settings['token_settings']['ignore_tags_type_tags'])
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

        settings['ignore_tags'] = self.stacked_widget_ignore_tags.checkbox_ignore_tags.isChecked()
        settings['ignore_tags_tags'] = self.stacked_widget_ignore_tags.checkbox_ignore_tags_tags.isChecked()
        settings['ignore_tags_type'] = self.stacked_widget_ignore_tags_type.combo_box_ignore_tags.currentText()
        settings['ignore_tags_type_tags'] = self.stacked_widget_ignore_tags_type.combo_box_ignore_tags_tags.currentText()
        settings['use_tags'] = self.checkbox_use_tags.isChecked()

    def generation_settings_changed(self):
        settings = self.main.settings_custom['overview']['generation_settings']

        settings['base_sttr'] = self.spin_box_base_sttr.value()

    def table_settings_changed(self):
        settings = self.main.settings_custom['overview']['table_settings']

        settings['show_pct'] = self.checkbox_show_pct.isChecked()
        settings['show_cumulative'] = self.checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = self.checkbox_show_breakdown.isChecked()

@ wordless_misc.log_timing
def generate_table(main, table):
    texts = []
    len_tokens_files = []

    settings = main.settings_custom['overview']

    files = main.wordless_files.get_selected_files()
    len_files = len(files)

    if wordless_checking_file.check_files_on_loading(main, files):
        table.clear_table()

        table.settings = copy.deepcopy(main.settings_custom)

        base_sttr = settings['generation_settings']['base_sttr']

        table.blockSignals(True)
        table.setUpdatesEnabled(False)

        for i, file in enumerate(files):
            table.insert_col(table.find_col(main.tr('Total')), file['name'], breakdown = True)

            text = wordless_text.Wordless_Text(main, file, tokens_only = False)
            text.tokens = wordless_token_processing.wordless_process_tokens_overview(text,
                                                                                     token_settings = settings['token_settings'])

            texts.append(text)

        if len(files) > 1:
            text_total = wordless_text.Wordless_Text_Blank()
            text_total.para_offsets = [offset for text in texts for offset in text.para_offsets]
            text_total.sentence_offsets = [offset for text in texts for offset in text.sentence_offsets]
            text_total.tokens = [token for text in texts for token in text.tokens]

            texts.append(text_total)
        else:
            texts.append(texts[0])

        for i, text in enumerate(texts):
            count_paras = len(text.para_offsets)
            count_sentences = len(text.sentence_offsets)
            count_tokens = len(text.tokens)
            count_types = len(set(text.tokens))

            len_tokens = [len(token) for token in text.tokens]
            len_tokens_files.append(collections.Counter(len_tokens))

            count_chars = sum(len_tokens)
            ttr = count_types / count_tokens

            token_sections = wordless_text_utils.to_sections(text.tokens, math.ceil(count_tokens / base_sttr))

            ttrs = [len(set(token_section)) / len(token_section) for token_section in token_sections]
            sttr = sum(ttrs) / len(ttrs)

            table.set_item_num_cumulative(0, i, count_paras)
            table.set_item_num_cumulative(1, i, count_sentences)
            table.set_item_num_cumulative(2, i, count_tokens)
            table.set_item_num_pct(3, i, count_types)
            table.set_item_num_cumulative(4, i, count_chars)
            table.set_item_num_float(5, i, ttr)
            table.set_item_num_float(6, i, sttr)
            table.set_item_num_float(7, i, count_sentences / count_paras)
            table.set_item_num_float(8, i, count_tokens / count_paras)
            table.set_item_num_float(9, i, count_tokens / count_sentences)
            table.set_item_num_float(10, i, count_chars / count_tokens)

        # Count of n-length Tokens
        len_tokens_total = wordless_misc.merge_dicts(len_tokens_files)
        len_tokens_max = max(len_tokens_total)

        if settings['token_settings']['use_tags']:
            table.setVerticalHeaderLabels([
                main.tr('Count of Paragraphs'),
                main.tr('Count of Sentences'),
                main.tr('Count of Tags'),
                main.tr('Count of Tag Types'),
                main.tr('Count of Characters'),
                main.tr('Type/Tag Ratio'),
                main.tr('Type/Tag Ratio (Standardized)'),
                main.tr('Average Paragraph Length (in Sentence)'),
                main.tr('Average Paragraph Length (in Tag)'),
                main.tr('Average Sentence Length (in Tag)'),
                main.tr('Average Tag Length (in Character)')
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

        table.item_changed()

        wordless_message.wordless_message_generate_table_success(main)
    else:
        wordless_message.wordless_message_generate_table_error(main)
