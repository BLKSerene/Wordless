#
# Wordless: Overview
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import *
from wordless_utils import *

def init(self):
    tab_overview = QWidget(self)

    table_overview = wordless_table.Wordless_Table_Data(self,
                                                        [
                                                            self.tr('File Name'),
                                                            self.tr('Count of Characters'),
                                                            self.tr('Count of Tokens'),
                                                            self.tr('Count of Types'),
                                                            self.tr('Count of Word Tokens'),
                                                            self.tr('Count of Word Types'),
                                                            self.tr('Lexical Diversity'),
                                                            self.tr('Average Word Length'),
                                                            self.tr('Count of Lowercase Words'),
                                                            self.tr('Count of Uppercase Words'),
                                                            self.tr('Count of Title Cased Words'),
                                                            self.tr('Count of Punctuations'),
                                                            self.tr('Count of Numbers')
                                                        ],
                                                        orientation = 'Vertical')

    button_generate_stats = QPushButton('Generate Statistics', self)

    button_generate_stats.clicked.connect(lambda: generate_stats(self, table_overview))

    layout = QGridLayout()
    layout.addWidget(table_overview, 0, 0, 1, 4)
    layout.addWidget(button_generate_stats, 1, 0)
    layout.addWidget(table_overview.button_export_selected, 1, 1)
    layout.addWidget(table_overview.button_export_all, 1, 2)
    layout.addWidget(table_overview.button_clear, 1, 3)

    tab_overview.setLayout(layout)

    return tab_overview

def generate_stats(self, table):
    table.clear_table()

    for i, file in enumerate(wordless_utils.fetch_files(self)):
        words = []
        punctuatuations = []
        numbers = []

        count_chars = 0
        count_punctuations = 0
        count_numbers = 0
        count_words_lowercase = 0
        count_words_uppercase = 0
        count_words_titlecased = 0

        len_words = 0

        text = wordless_utils.read_file(file)
        for token in text:
            count_chars += len(token)

            if not token.isalnum():
                count_punctuations += 1
            elif token.isdigit():
                count_numbers += 1
            else:
                for char in token:
                    if char.isalpha():
                        words.append(token)

                        break

        for word in words:
            len_words += len(word)

            if word.islower():
                count_words_lowercase += 1
            elif word.isupper():
                count_words_uppercase += 1
            elif word.istitle():
                count_words_titlecased += 1

        count_tokens = len(text)
        count_types = len(set(text))
        count_words = len(words)
        count_word_types = len(set(words))

        if table.item(0, 0):
            table.setColumnCount(table.columnCount() + 1)

        table.setItem(0, i, QTableWidgetItem(file.name))
        table.setItem(1, i, QTableWidgetItem(str(count_chars)))
        table.setItem(2, i, QTableWidgetItem(str(count_tokens)))
        table.setItem(3, i, QTableWidgetItem(str(count_types)))
        table.setItem(4, i, QTableWidgetItem(str(count_words)))
        table.setItem(5, i, QTableWidgetItem(str(count_word_types)))
        if count_word_types:
            table.setItem(6, i, QTableWidgetItem(str(round(count_words / count_word_types, self.settings_custom['general']['precision']))))
        else:
            table.setItem(6, i, QTableWidgetItem(str(0)))
        if count_words:
            table.setItem(7, i, QTableWidgetItem(str(round(len_words / count_words, self.settings_custom['general']['precision']))))
        else:
            table.setItem(7, i, QTableWidgetItem(str(0)))
        table.setItem(8, i, QTableWidgetItem(str(count_words_lowercase)))
        table.setItem(9, i, QTableWidgetItem(str(count_words_uppercase)))
        table.setItem(10, i, QTableWidgetItem(str(count_words_titlecased)))
        table.setItem(11, i, QTableWidgetItem(str(count_punctuations)))
        table.setItem(12, i, QTableWidgetItem(str(count_numbers)))

    self.status_bar.showMessage('Done!')