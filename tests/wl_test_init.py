# ----------------------------------------------------------------------
# Tests: Initialization
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

import copy
import glob
import os
import pickle
import re
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTableView,
    QTabWidget
)

from tests import wl_test_file_area
from wordless import wl_file_area
from wordless.wl_checks import wl_checks_misc
from wordless.wl_nlp import wl_texts
from wordless.wl_settings import wl_settings, wl_settings_default, wl_settings_global
from wordless.wl_utils import wl_misc
from wordless.wl_widgets import wl_tables

# English
SEARCH_TERMS = ['take']

# An instance of QApplication must be created before any instance of QWidget
wl_app = QApplication(sys.argv)

class Wl_Test_Main(QMainWindow):
    def __init__(self, switch_lang_utils = 'default'):
        super().__init__()

        self.app = wl_app

        self.threads_check_updates = []
        self.ver = wl_misc.get_wl_ver()
        self.copyright_year = '2000'
        self.email = 'blkserene@gmail.com'
        self.email_html = '<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a>'

        # Global and default settings
        self.settings_global = wl_settings_global.init_settings_global()
        self.settings_default = wl_settings_default.init_settings_default(self)

        # Custom settings
        if os.path.exists('tests/wl_settings.pickle'):
            with open('tests/wl_settings.pickle', 'rb') as f:
                settings_custom = pickle.load(f)

            if wl_checks_misc.check_custom_settings(settings_custom, self.settings_default):
                self.settings_custom = settings_custom
            else:
                self.settings_custom = copy.deepcopy(self.settings_default)
        else:
            self.settings_custom = copy.deepcopy(self.settings_default)

        match switch_lang_utils:
            case 'fast':
                self.switch_lang_utils_fast()
            case 'spacy':
                self.switch_lang_utils_spacy()
            case 'stanza':
                self.switch_lang_utils_stanza()

        # Status bar
        self.status_bar = QStatusBar()

        # Work area
        self.wl_work_area = QTabWidget()

        # File area
        self.wl_file_area = QObject()
        self.wl_file_area.main = self
        self.wl_file_area.file_type = 'observed'
        self.wl_file_area.settings_suffix = ''

        self.wl_file_area.table_files = Wl_Test_Table(self)

        self.wl_file_area.get_files = lambda: wl_file_area.Wrapper_File_Area.get_files(self.wl_file_area)
        self.wl_file_area.get_file_names = lambda: wl_file_area.Wrapper_File_Area.get_file_names(self.wl_file_area)
        self.wl_file_area.get_selected_files = lambda: wl_file_area.Wrapper_File_Area.get_selected_files(self.wl_file_area)
        self.wl_file_area.get_selected_file_names = lambda: wl_file_area.Wrapper_File_Area.get_selected_file_names(self.wl_file_area)
        self.wl_file_area.find_file_by_name = lambda file_name, selected_only = False: wl_file_area.Wrapper_File_Area.find_file_by_name(self.wl_file_area, file_name, selected_only)
        self.wl_file_area.find_files_by_name = lambda file_names, selected_only = False: wl_file_area.Wrapper_File_Area.find_files_by_name(self.wl_file_area, file_names, selected_only)

        self.wl_file_area_ref = QObject()
        self.wl_file_area_ref.main = self
        self.wl_file_area_ref.file_type = 'ref'
        self.wl_file_area_ref.settings_suffix = '_ref'

        self.wl_file_area_ref.get_files = lambda: wl_file_area.Wrapper_File_Area.get_files(self.wl_file_area_ref)
        self.wl_file_area_ref.get_file_names = lambda: wl_file_area.Wrapper_File_Area.get_file_names(self.wl_file_area_ref)
        self.wl_file_area_ref.get_selected_files = lambda: wl_file_area.Wrapper_File_Area.get_selected_files(self.wl_file_area_ref)
        self.wl_file_area_ref.get_selected_file_names = lambda: wl_file_area.Wrapper_File_Area.get_selected_file_names(self.wl_file_area_ref)

        # Settings
        self.wl_settings = wl_settings.Wl_Settings(self)

    def height(self):
        return 1080

    def statusBar(self):
        return self.status_bar

    def switch_lang_utils_fast(self):
        settings_custom_sentence_tokenizers = self.settings_custom['sentence_tokenization']['sentence_tokenizer_settings']
        settings_global_sentence_tokenizers = self.settings_global['sentence_tokenizers']
        settings_custom_word_tokenizers = self.settings_custom['word_tokenization']['word_tokenizer_settings']
        settings_global_word_tokenizers = self.settings_global['word_tokenizers']
        settings_custom_lemmatizers = self.settings_custom['lemmatization']['lemmatizer_settings']
        settings_global_lemmatizers = self.settings_global['lemmatizers']
        settings_custom_sentiment_analyzers = self.settings_custom['sentiment_analysis']['sentiment_analyzer_settings']
        settings_global_sentiment_analyzers = self.settings_global['sentiment_analyzers']

        for lang in settings_custom_sentence_tokenizers:
            if 'spacy_sentencizer' in settings_global_sentence_tokenizers[lang]:
                settings_custom_sentence_tokenizers[lang] = 'spacy_sentencizer'

        for lang in settings_custom_word_tokenizers:
            if 'nltk_nltk' in settings_global_word_tokenizers[lang]:
                settings_custom_word_tokenizers[lang] = 'nltk_nltk'
            elif 'pkuseg_zho' in settings_global_word_tokenizers[lang]:
                settings_custom_word_tokenizers[lang] = 'pkuseg_zho'
            elif 'sudachipy_jpn_split_mode_a' in settings_global_word_tokenizers[lang]:
                settings_custom_word_tokenizers[lang] = 'sudachipy_jpn_split_mode_a'
            else:
                for lang_util in settings_global_word_tokenizers[lang]:
                    if lang_util.startswith('spacy_'):
                        settings_custom_word_tokenizers[lang] = lang_util

                        break

        for lang in settings_custom_lemmatizers:
            for lang_util in settings_global_lemmatizers[lang]:
                if lang_util.startswith('simplemma_'):
                    settings_custom_lemmatizers[lang] = lang_util

                    break

        for lang in settings_custom_sentiment_analyzers:
            for lang_util in settings_global_sentiment_analyzers[lang]:
                if lang_util.startswith('vader_'):
                    settings_custom_sentiment_analyzers[lang] = lang_util

                    break

    def switch_lang_utils_spacy(self):
        settings_custom_sentence_tokenizers = self.settings_custom['sentence_tokenization']['sentence_tokenizer_settings']
        settings_global_sentence_tokenizers = self.settings_global['sentence_tokenizers']

        for lang in settings_custom_sentence_tokenizers:
            if 'spacy_sentencizer' in settings_global_sentence_tokenizers[lang]:
                settings_custom_sentence_tokenizers[lang] = 'spacy_sentencizer'

        for settings_custom, settings_global in [
            (
                self.settings_custom['word_tokenization']['word_tokenizer_settings'],
                self.settings_global['word_tokenizers']
            ), (
                self.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'],
                self.settings_global['pos_taggers']
            ), (
                self.settings_custom['lemmatization']['lemmatizer_settings'],
                self.settings_global['lemmatizers']
            ), (
                self.settings_custom['dependency_parsing']['dependency_parser_settings'],
                self.settings_global['dependency_parsers']
            )
        ]:
            for lang in settings_custom:
                for lang_util in settings_global[lang]:
                    if lang_util.startswith('spacy_'):
                        settings_custom[lang] = lang_util

                        break

    def switch_lang_utils_stanza(self):
        for settings_custom, settings_global in [
            (
                self.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'],
                self.settings_global['sentence_tokenizers']
            ), (
                self.settings_custom['word_tokenization']['word_tokenizer_settings'],
                self.settings_global['word_tokenizers']
            ), (
                self.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'],
                self.settings_global['pos_taggers']
            ), (
                self.settings_custom['lemmatization']['lemmatizer_settings'],
                self.settings_global['lemmatizers']
            ), (
                self.settings_custom['dependency_parsing']['dependency_parser_settings'],
                self.settings_global['dependency_parsers']
            ), (
                self.settings_custom['sentiment_analysis']['sentiment_analyzer_settings'],
                self.settings_global['sentiment_analyzers']
            )
        ]:
            for lang in settings_custom:
                for lang_util in settings_global[lang]:
                    if lang_util.startswith('stanza_'):
                        settings_custom[lang] = lang_util

                        break

class Wl_Test_Table(QTableView):
    def __init__(self, parent, tab = ''):
        super().__init__(parent)

        self.tab = tab
        self.header_orientation = 'hor'

        self.settings_global = wl_settings_global.init_settings_global()
        self.settings = wl_settings_default.init_settings_default(self)

        self.setModel(QStandardItemModel())

        self.button_generate_table = QPushButton(self)

        self.disable_updates = lambda: wl_tables.Wl_Table.disable_updates(self)
        self.enable_updates = lambda emit_signals: wl_tables.Wl_Table.enable_updates(self, emit_signals)
        self.is_empty = lambda: wl_tables.Wl_Table.is_empty(self)

    def set_item(self, row, col, text):
        self.model().setItem(row, col, QStandardItem(text))

    def set_label(self, row, col, text):
        self.set_item(row, col, QStandardItem())
        self.setIndexWidget(self.model().index(row, col), QLabel(text))
        self.indexWidget(self.model().index(row, col)).tokens_raw = [text]

class Wl_Test_Text:
    def __init__(self, main, tokens_multilevel, lang = 'eng_us', tagged = False):
        self.main = main
        self.lang = lang
        self.tagged = tagged

        self.tokens_multilevel = []

        for para in tokens_multilevel:
            self.tokens_multilevel.append([])

            for sentence in para:
                self.tokens_multilevel[-1].append([])

                for sentence_seg in sentence:
                    self.tokens_multilevel[-1][-1].append(wl_texts.to_tokens(sentence_seg, lang = lang))

        self.tokens_multilevel_with_puncs = copy.deepcopy(tokens_multilevel)

        self.get_tokens_flat = lambda: wl_texts.Wl_Text.get_tokens_flat(self)
        self.update_num_tokens = lambda: wl_texts.Wl_Text.update_num_tokens(self)

        self.update_num_tokens()

class Wl_Exception_Tests_Lang_Skipped(Exception):
    def __init__(self, lang):
        super().__init__(f'Tests for language "{lang}" is skipped!')

class Wl_Exception_Tests_Lang_Util_Skipped(Exception):
    def __init__(self, lang_util):
        super().__init__(f'Tests for language utility "{lang_util}" is skipped!')

def wl_test_index(row, col):
    return QStandardItemModel().createIndex(row, col)

# Select files randomly
def select_test_files(main, no_files, ref = False):
    no_files = set(no_files)

    if ref:
        files = main.settings_custom['file_area']['files_open_ref']
    else:
        files = main.settings_custom['file_area']['files_open']

    if not files:
        wl_test_file_area.wl_test_file_area(main)

        if ref:
            files = main.settings_custom['file_area']['files_open_ref']
        else:
            files = main.settings_custom['file_area']['files_open']

    for file in files:
        file['selected'] = False

    for i, file in enumerate(files):
        if i in no_files:
            file['selected'] = True

def get_test_file_names(main, ref = False):
    if ref:
        file_names = [
            re.search(r'(?<= )[^\.]+?$', file_name).group()
            for file_name in main.wl_file_area_ref.get_selected_file_names()
        ]
    else:
        file_names = [
            re.search(r'(?<= )[^\.]+?$', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

    return file_names

# Clean cached files
def clean_import_caches():
    for file in glob.glob('imports/*.*'):
        os.remove(file)
