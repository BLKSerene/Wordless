#
# Wordless: Overview
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *
from wordless_utils import *

class Wordless_Table_Overview(wordless_table.Wordless_Table_Data):
    def __init__(self, main):
        super().__init__(main,
                         headers = [
                             main.tr('Count of Characters'),
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Types'),
                             main.tr('Type/Token Ratio'),
                             main.tr('Type/Token Ratio (Standardized)'),
                             main.tr('Average Paragraph Length (in Sentence)'),
                             main.tr('Average Paragraph Length (in Tokens)'),
                             main.tr('Average Sentence Length (in Tokens)'),
                             main.tr('Average Token Length (in Characters)'),
                             main.tr('Count of Words'),
                             main.tr('Count of Words in Lowercase'),
                             main.tr('Count of Words in Uppercase'),
                             main.tr('Count of Words in Title Case'),
                             main.tr('Count of Numbers'),
                             main.tr('Count of Punctuations')
                         ],
                         orientation = 'vertical',
                         headers_num = [
                             main.tr('Count of Characters'),
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Types'),
                             main.tr('Type/Token Ratio'),
                             main.tr('Type/Token Ratio (Standardized)'),
                             main.tr('Average Paragraph Length (in Sentence)'),
                             main.tr('Average Paragraph Length (in Tokens)'),
                             main.tr('Average Sentence Length (in Tokens)'),
                             main.tr('Average Token Length (in Characters)'),
                             main.tr('Count of Words'),
                             main.tr('Count of Words in Lowercase'),
                             main.tr('Count of Words in Uppercase'),
                             main.tr('Count of Words in Title Case'),
                             main.tr('Count of Numbers'),
                             main.tr('Count of Punctuations')
                         ],
                         headers_pct = [
                             main.tr('Count of Characters'),
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Types'),
                             main.tr('Count of Words'),
                             main.tr('Count of Words in Lowercase'),
                             main.tr('Count of Words in Uppercase'),
                             main.tr('Count of Words in Title Case'),
                             main.tr('Count of Numbers'),
                             main.tr('Count of Punctuations')
                         ],
                         headers_cumulative = [
                             main.tr('Count of Characters'),
                             main.tr('Count of Paragraphs'),
                             main.tr('Count of Sentences'),
                             main.tr('Count of Tokens'),
                             main.tr('Count of Words'),
                             main.tr('Count of Words in Lowercase'),
                             main.tr('Count of Words in Uppercase'),
                             main.tr('Count of Words in Title Case'),
                             main.tr('Count of Numbers'),
                             main.tr('Count of Punctuations')
                         ])

        self.button_generate_stats = QPushButton(self.tr('Generate Statistics'), self.main)

        self.button_generate_stats.clicked.connect(lambda: generate_stats(self.main, self))

    def clear_table(self, count_headers = 1):
        super().clear_table(0)

        self.insert_col(0, self.tr('Total'))

def init(main):
    def load_settings(defaults = False):
        if defaults:
            settings_loaded = copy.deepcopy(main.settings_default['overview'])
        else:
            settings_loaded = copy.deepcopy(main.settings_custom['overview'])

        checkbox_words.setChecked(settings_loaded['words'])
        checkbox_lowercase.setChecked(settings_loaded['lowercase'])
        checkbox_uppercase.setChecked(settings_loaded['uppercase'])
        checkbox_title_case.setChecked(settings_loaded['title_case'])
        checkbox_treat_as_lowercase.setChecked(settings_loaded['treat_as_lowercase'])
        checkbox_lemmatize.setChecked(settings_loaded['lemmatize'])
        checkbox_filter_stop_words.setChecked(settings_loaded['filter_stop_words'])

        checkbox_nums.setChecked(settings_loaded['nums'])
        checkbox_puncs.setChecked(settings_loaded['puncs'])

        spin_box_base_sttr.setValue(settings_loaded['base_sttr'])

        checkbox_show_pct.setChecked(settings_loaded['show_pct'])
        checkbox_show_cumulative.setChecked(settings_loaded['show_cumulative'])
        checkbox_show_breakdown.setChecked(settings_loaded['show_breakdown'])

        token_settings_changed()
        generation_settings_changed()
        table_settings_changed()

    def token_settings_changed():
        settings['words'] = checkbox_words.isChecked()
        settings['lowercase'] = checkbox_lowercase.isChecked()
        settings['uppercase'] = checkbox_uppercase.isChecked()
        settings['title_case'] = checkbox_title_case.isChecked()
        settings['treat_as_lowercase'] = checkbox_treat_as_lowercase.isChecked()
        settings['lemmatize'] = checkbox_lemmatize.isChecked()
        settings['filter_stop_words'] = checkbox_filter_stop_words.isChecked()

        settings['nums'] = checkbox_nums.isChecked()
        settings['puncs'] = checkbox_puncs.isChecked()

    def generation_settings_changed():
        settings['base_sttr'] = spin_box_base_sttr.value()

    def table_settings_changed():
        settings['show_pct'] = checkbox_show_pct.isChecked()
        settings['show_cumulative'] = checkbox_show_cumulative.isChecked()
        settings['show_breakdown'] = checkbox_show_breakdown.isChecked()

    settings = main.settings_custom['overview']

    tab_overview = wordless_layout.Wordless_Tab(main, load_settings)

    table_overview = Wordless_Table_Overview(main)

    tab_overview.layout_table.addWidget(table_overview, 0, 0, 1, 4)
    tab_overview.layout_table.addWidget(table_overview.button_generate_stats, 1, 0)
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
     checkbox_lemmatize,
     checkbox_filter_stop_words,

     checkbox_nums,
     checkbox_puncs) = wordless_widgets.wordless_widgets_token(main)

    checkbox_words.stateChanged.connect(token_settings_changed)
    checkbox_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_uppercase.stateChanged.connect(token_settings_changed)
    checkbox_title_case.stateChanged.connect(token_settings_changed)
    checkbox_treat_as_lowercase.stateChanged.connect(token_settings_changed)
    checkbox_lemmatize.stateChanged.connect(token_settings_changed)
    checkbox_filter_stop_words.stateChanged.connect(token_settings_changed)

    checkbox_nums.stateChanged.connect(token_settings_changed)
    checkbox_puncs.stateChanged.connect(token_settings_changed)

    group_box_token_settings.setLayout(QGridLayout())
    group_box_token_settings.layout().addWidget(checkbox_words, 0, 0)
    group_box_token_settings.layout().addWidget(checkbox_lowercase, 0, 1)
    group_box_token_settings.layout().addWidget(checkbox_uppercase, 1, 0)
    group_box_token_settings.layout().addWidget(checkbox_title_case, 1, 1)
    group_box_token_settings.layout().addWidget(checkbox_treat_as_lowercase, 2, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_lemmatize, 3, 0, 1, 2)
    group_box_token_settings.layout().addWidget(checkbox_filter_stop_words, 4, 0, 1, 2)

    group_box_token_settings.layout().addWidget(wordless_layout.Wordless_Separator(main), 5, 0, 1, 2)

    group_box_token_settings.layout().addWidget(checkbox_nums, 6, 0)
    group_box_token_settings.layout().addWidget(checkbox_puncs, 6, 1)

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
     checkbox_show_breakdown) = wordless_widgets.wordless_widgets_table(main, table_overview)

    checkbox_show_pct.stateChanged.connect(table_settings_changed)
    checkbox_show_cumulative.stateChanged.connect(table_settings_changed)
    checkbox_show_breakdown.stateChanged.connect(table_settings_changed)

    group_box_table_settings.setLayout(QGridLayout())
    group_box_table_settings.layout().addWidget(checkbox_show_pct, 0, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_cumulative, 1, 0)
    group_box_table_settings.layout().addWidget(checkbox_show_breakdown, 2, 0)

    tab_overview.layout_settings.addWidget(group_box_token_settings, 0, 0, Qt.AlignTop)
    tab_overview.layout_settings.addWidget(group_box_generation_settings, 1, 0, Qt.AlignTop)
    tab_overview.layout_settings.addWidget(group_box_table_settings, 2, 0, Qt.AlignTop)

    load_settings()

    return tab_overview

@ wordless_misc.log_timing('Statistics generation completed')
def generate_stats(main, table):
    texts = []

    settings = main.settings_custom['overview']
    files = main.wordless_files.selected_files()

    if files:
        table.clear_table()

        table.blockSignals(True)
        table.setSortingEnabled(False)
        table.setUpdatesEnabled(False)

        for i, file in enumerate(files):
            table.insert_col(table.find_col(main.tr('Total')), file['name'], breakdown = True)

            text = wordless_text.Wordless_Text(main, file)

            text.tokens_filtered = text.tokens.copy()

            if settings['words']:
                if not settings['lowercase']:
                    text.tokens_filtered = [token for token in text.tokens_filtered if not token.islower()]
                if not settings['uppercase']:
                    text.tokens_filtered = [token for token in text.tokens_filtered if not token.isupper()]
                if not settings['title_case']:
                    text.tokens_filtered = [token for token in text.tokens_filtered if not token.istitle()]

                if settings['treat_as_lowercase']:
                    text.tokens_filtered = [token.lower() for token in text.tokens_filtered]

                if settings['lemmatize']:
                    text.tokens_filtered = wordless_text.wordless_lemmatize(text.main, text.tokens_filtered, text.lang_code)

                if settings['filter_stop_words']:
                    text.tokens_filtered = wordless_text.wordless_filter_stop_words(main, text.tokens_filtered, text.lang_code)
            else:
                text.tokens_filtered = [token for token in text.tokens_filtered if not [char for char in token if char.isalpha()]]
            
            if not settings['nums']:
                text.tokens_filtered = [token for token in text.tokens_filtered if not token.isnumeric()]
            if not settings['puncs']:
                text.tokens_filtered = [token for token in text.tokens_filtered if [char for char in token if char.isalnum()]]

            texts.append(text)

        text_total = wordless_text.Wordless_Text(main, files[0])
        text_total.text = '\n'.join([text.text for text in texts])
        text_total.tokens = [token for text in texts for token in text.tokens]
        text_total.tokens_filtered = [token for text in texts for token in text.tokens_filtered]

        texts.append(text_total)

        base_sttr = settings['base_sttr']

        for i, text in enumerate(texts):
            count_chars = 0
            count_paras = 0
            count_sentences = 0
            count_words = 0
            count_words_lowercase = 0
            count_words_uppercase = 0
            count_words_title_case = 0
            count_nums = 0
            count_puncs = 0
            ttrs = []

            for para in text.text.split('\n'):
                if para:
                    count_paras += 1
                    count_sentences += len(wordless_text.wordless_sentence_tokenize(main, para, text.lang_code))

            for token in text.tokens:
                count_chars += len(token)

                if [char for char in token if char.isalpha()]:
                    count_words += 1

                    if token.islower():
                        count_words_lowercase += 1
                    elif token.isupper():
                        count_words_uppercase += 1
                    elif token.istitle():
                        count_words_title_case += 1
                elif token.isnumeric():
                    count_nums += 1
                else:
                    count_puncs += 1

            count_tokens = len(text.tokens_filtered)
            count_types = len(set(text.tokens_filtered))
            ttr = count_types / count_tokens

            if count_tokens <= base_sttr:
                sttr = ttr
            else:
                for j in range(count_tokens // base_sttr):
                    tokens_chunk = text.tokens_filtered[base_sttr * j : base_sttr * (j + 1)]

                    ttrs.append(len(set(tokens_chunk)) / len(tokens_chunk))

                sttr = sum(ttrs) / len(ttrs)

            table.set_item_num_cumulative(0, i, count_chars)
            table.set_item_num_cumulative(1, i, count_paras)
            table.set_item_num_cumulative(2, i, count_sentences)
            table.set_item_num_cumulative(3, i, count_tokens)
            table.set_item_num_pct(4, i, count_types)
            table.set_item_num_float(5, i, ttr)
            table.set_item_num_float(6, i, sttr)
            table.set_item_num_float(7, i, count_sentences / count_paras)
            table.set_item_num_float(8, i, count_tokens/ count_paras)
            table.set_item_num_float(9, i, count_tokens/ count_sentences)
            table.set_item_num_float(10, i, count_chars / count_tokens)
            table.set_item_num_cumulative(11, i, count_words)
            table.set_item_num_cumulative(12, i, count_words_lowercase)
            table.set_item_num_cumulative(13, i, count_words_uppercase)
            table.set_item_num_cumulative(14, i, count_words_title_case)
            table.set_item_num_cumulative(15, i, count_nums)
            table.set_item_num_cumulative(16, i, count_puncs)

        table.blockSignals(False)
        table.setSortingEnabled(True)
        table.setUpdatesEnabled(True)

        table.toggle_pct()
        table.toggle_cumulative()
        table.toggle_breakdown()
        table.update_items_width()

        table.item_changed()
