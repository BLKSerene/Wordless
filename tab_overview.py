#
# Wordless: Overview
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_text import *
from wordless_utils import *
from wordless_widgets import *

class Wordless_Table_Overview(wordless_table.Wordless_Table_Data):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Types'),
                             main.tr('Count of Characters'),
                             main.tr('Type/Token Ratio'),
                             main.tr('Type/Token Ratio (Standardized)'),
                             main.tr('Average Paragraph Length (in Sentence)'),
                             main.tr('Average Paragraph Length (in Token)'),
                             main.tr('Average Sentence Length (in Token)'),
                             main.tr('Average Token Length (in Character)')
                         ],
                         header_orientation = 'vertical',
                         headers_num = [
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Types'),
                             main.tr('Count of Characters'),
                             main.tr('Type/Token Ratio'),
                             main.tr('Type/Token Ratio (Standardized)'),
                             main.tr('Average Paragraph Length (in Sentence)'),
                             main.tr('Average Paragraph Length (in Token)'),
                             main.tr('Average Sentence Length (in Token)'),
                             main.tr('Average Token Length (in Character)')
                         ],
                         headers_pct = [
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Types'),
                             main.tr('Count of Characters')
                         ],
                         headers_cumulative = [
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Characters')
                         ])

        self.button_generate_table = QPushButton(self.tr('Generate Table'), self.main)

        self.button_generate_table.clicked.connect(lambda: generate_table(self.main, self))

    def clear_table(self, count_headers = 1):
        super().clear_table(0)

        self.insert_col(0, self.tr('Total'))

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings = copy.deepcopy(main.settings_default['overview'])
        else:
            settings = copy.deepcopy(main.settings_custom['overview'])

        # Token Settings
        checkbox_words.setChecked(settings['token_settings']['words'])
        checkbox_lowercase.setChecked(settings['token_settings']['lowercase'])
        checkbox_uppercase.setChecked(settings['token_settings']['uppercase'])
        checkbox_title_case.setChecked(settings['token_settings']['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings['token_settings']['treat_as_lowercase'])

        checkbox_nums.setChecked(settings['token_settings']['nums'])
        checkbox_puncs.setChecked(settings['token_settings']['puncs'])

        checkbox_lemmatize.setChecked(settings['token_settings']['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings['token_settings']['filter_stop_words'])

        checkbox_ignore_tags.setChecked(settings['token_settings']['ignore_tags'])
        combo_box_ignore_tags.setCurrentText(settings['token_settings']['ignore_tags_type'])
        checkbox_tags_only.setChecked(settings['token_settings']['tags_only'])

        # Generation Settings
        spin_box_base_sttr.setValue(settings['generation_settings']['base_sttr'])

        # Table Settings
        checkbox_show_pct.setChecked(settings['table_settings']['show_pct'])
        checkbox_show_cumulative.setChecked(settings['table_settings']['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings['table_settings']['show_breakdown'])

        token_settings_changed()
        generation_settings_changed()
        table_settings_changed()

    def token_settings_changed():
        settings = main.settings_custom['overview']['token_settings']

        settings['words'] = checkbox_words.isChecked()
        settings['lowercase'] = checkbox_lowercase.isChecked()
        settings['uppercase'] = checkbox_uppercase.isChecked()
        settings['title_case'] = checkbox_title_case.isChecked()
        settings['treat_as_lowercase'] = checkbox_treat_as_lowercase.isChecked()

        settings['nums'] = checkbox_nums.isChecked()
        settings['puncs'] = checkbox_puncs.isChecked()

        settings['lemmatize'] = checkbox_lemmatize.isChecked()
        settings['filter_stop_words'] = checkbox_filter_stop_words.isChecked()

        settings['ignore_tags'] = checkbox_ignore_tags.isChecked()
        settings['ignore_tags_type'] = combo_box_ignore_tags.currentText()
        settings['tags_only'] = checkbox_tags_only.isChecked()

    def generation_settings_changed():
        settings = main.settings_custom['overview']['generation_settings']

        settings['base_sttr'] = spin_box_base_sttr.value()

    def table_settings_changed():
        settings = main.settings_custom['overview']['table_settings']

        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    tab_overview = wordless_layout.Wordless_Tab(main, load_settings)

    table_overview = Wordless_Table_Overview(main)

    tab_overview.layout_table.addWidget(table_overview, 0, 0, 1, 4)
    tab_overview.layout_table.addWidget(table_overview.button_generate_table, 1, 0)
    tab_overview.layout_table.addWidget(table_overview.button_export_selected, 1, 1)
    tab_overview.layout_table.addWidget(table_overview.button_export_all, 1, 2)
    tab_overview.layout_table.addWidget(table_overview.button_clear, 1, 3)
    
    # Token Settings
    group_box_token_settings = QGroupBox(main.tr('Token Settings'), main)

    (checkbox_words,
     checkbox_lowercase,
     checkbox_uppercase,
     checkbox_title_case,
     checkbox_treat_as_lowercase,

     checkbox_nums,
     checkbox_puncs,

     checkbox_lemmatize,
     checkbox_filter_stop_words,

     checkbox_ignore_tags,
     combo_box_ignore_tags,
     label_ignore_tags,
     checkbox_tags_only) = wordless_widgets.wordless_widgets_token_settings(main)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_case.stateChanged.connect(token_settings_changed)
    checkbox_treat_as_lowercase.stateChanged.connect(token_settings_changed)

    checkbox_nums.stateChanged.connect(token_settings_changed)
    checkbox_puncs.stateChanged.connect(token_settings_changed)

    checkbox_lemmatize.stateChanged.connect(token_settings_changed)
    checkbox_filter_stop_words.stateChanged.connect(token_settings_changed)

    checkbox_ignore_tags.stateChanged.connect(token_settings_changed)
    combo_box_ignore_tags.currentTextChanged.connect(token_settings_changed)
    checkbox_tags_only.stateChanged.connect(token_settings_changed)

    layout_ignore_tags = QGridLayout()
    layout_ignore_tags.addWidget(checkbox_ignore_tags, 0, 0)
    layout_ignore_tags.addWidget(combo_box_ignore_tags, 0, 1)
    layout_ignore_tags.addWidget(label_ignore_tags, 0, 2)

    layout_ignore_tags.setColumnStretch(3, 1)

    group_box_token_settings.setLayout(QGridLayout())
    group_box_token_settings.layout().addWidget(checkbox_words, 0, 0)
    group_box_token_settings.layout().addWidget(checkbox_lowercase, 0, 1)
    group_box_token_settings.layout().addWidget(checkbox_uppercase, 1, 0)
    group_box_token_settings.layout().addWidget(checkbox_title_case, 1, 1)
    group_box_token_settings.layout().addWidget(checkbox_treat_as_lowercase, 2, 0, 1, 2)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 3, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_nums, 4, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 4, 1)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 5, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_lemmatize, 6, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_filter_stop_words, 7, 0, 1, 2)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 8, 0, 1, 2)

    group_box_token_settings.layout().addLayout(layout_ignore_tags, 9, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_tags_only, 10, 0, 1, 2)

    # Generation Settings
    group_box_generation_settings = QGroupBox(main.tr('Generation Settings'), main)

    label_base_sttr = QLabel(main.tr('Base of Standardized Type/Token Ratio:'), main)
    spin_box_base_sttr = QSpinBox(main)

    spin_box_base_sttr.setRange(100, 10000)

    spin_box_base_sttr.valueChanged.connect(generation_settings_changed)

    group_box_generation_settings.setLayout(QGridLayout())
    group_box_generation_settings.layout().addWidget(label_base_sttr, 0, 0)
    group_box_generation_settings.layout().addWidget(spin_box_base_sttr, 1, 0)

    # Table Settings
    group_box_table_settings = QGroupBox(main.tr('Table Settings'), main)

    (checkbox_show_pct,
     checkbox_show_cumulative,
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table_settings(main, table_overview)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown, 2, 0)

    tab_overview.layout_settings.addWidget(group_box_token_settings, 0, 0)
    tab_overview.layout_settings.addWidget(group_box_generation_settings, 1, 0)
    tab_overview.layout_settings.addWidget(group_box_table_settings, 2, 0)

    tab_overview.layout_settings.setRowStretch(3, 1)

    load_settings()

    return tab_overview

@ wordless_misc.log_timing
def generate_table(main, table):
    texts = []
    len_tokens_files = []

    settings = main.settings_custom['overview']

    files = wordless_checking.check_files_loading(main, main.wordless_files.get_selected_files())

    if files:
        table.clear_table()

        table.settings = copy.deepcopy(main.settings_custom)

        table.blockSignals(True)
        table.setUpdatesEnabled(False)

        for i, file in enumerate(files):
            table.insert_col(table.find_col(main.tr('Total')), file['name'], breakdown = True)

            text = wordless_text.Wordless_Text(main, file)
            text.tokens = wordless_token_processing.wordless_preprocess_tokens_overview(text, settings = settings['token_settings'])
            print(text.tokens)
            texts.append(text)

        if len(files) > 1:
            text_total = wordless_text.Wordless_Text(main, files[0])
            text_total.paras = [para for text in texts for para in text.paras]
            text_total.sentences = [sentence for text in texts for sentence in text.sentences]
            text_total.tokens = [token for text in texts for token in text.tokens]

            texts.append(text_total)
        else:
            texts.append(texts[0])

        base_sttr = settings['generation_settings']['base_sttr']

        for i, text in enumerate(texts):
            count_chars = 0
            ttrs = []

            count_paras = len(text.paras)
            count_sentences = len(text.sentences)

            len_tokens = {len_token + 1: 0
                          for len_token in range(max([len(token) for token in set(text.tokens)]))}

            for token in text.tokens:
                count_chars += len(token)

                len_tokens[len(token)] += 1

            len_tokens_files.append(len_tokens)

            count_tokens = len(text.tokens)
            count_types = len(set(text.tokens))

            ttr = count_types / count_tokens

            if count_tokens <= base_sttr:
                sttr = ttr
            else:
                for j in range(count_tokens // base_sttr):
                    tokens_chunk = text.tokens[base_sttr * j : base_sttr * (j + 1)]

                    ttrs.append(len(set(tokens_chunk)) / len(tokens_chunk))

                sttr = sum(ttrs) / len(ttrs)

            table.set_item_num_cumulative(0, i, count_paras)
            table.set_item_num_cumulative(1, i, count_sentences)
            table.set_item_num_cumulative(2, i, count_tokens)
            table.set_item_num_pct(3, i, count_types)
            table.set_item_num_cumulative(4, i, count_chars)
            table.set_item_num_float(5, i, ttr)
            table.set_item_num_float(6, i, sttr)
            table.set_item_num_float(7, i, count_sentences / count_paras)
            table.set_item_num_float(8, i, count_tokens/ count_paras)
            table.set_item_num_float(9, i, count_tokens/ count_sentences)
            table.set_item_num_float(10, i, count_chars / count_tokens)

        # Count of n-length Tokens
        len_tokens_total = wordless_misc.merge_dicts(len_tokens_files)

        if settings['token_settings']['tags_only']:
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

            for i in range(max(len_tokens_total)):
                table.insert_row(table.rowCount(),
                                 main.tr(f'Count of {i + 1}-length Tags'),
                                 num = True, pct = True, cumulative = True)
        else:
            for i in range(max(len_tokens_total)):
                table.insert_row(table.rowCount(),
                                 main.tr(f'Count of {i + 1}-length Tokens'),
                                 num = True, pct = True, cumulative = True)

        for i, (len_token, freqs) in enumerate(len_tokens_total.items()):
            for j, freq in enumerate(freqs):
                table.set_item_num_cumulative(table.rowCount() - max(len_tokens_total) + i, j, freq)

        table.blockSignals(False)
        table.setUpdatesEnabled(True)

        table.toggle_pct()
        table.toggle_cumulative()
        table.toggle_breakdown()

        table.update_items_width()

        table.item_changed()

        wordless_message.wordless_message_generate_table_success(main)
    else:
        wordless_message_box.wordless_message_box_no_files_selected(main)

        wordless_message.wordless_message_generate_table_error(main)
