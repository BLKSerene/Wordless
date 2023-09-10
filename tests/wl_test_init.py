# ----------------------------------------------------------------------
# Wordless: Tests - Initialization
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

import copy
import glob
import os
import pickle
import random
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QStatusBar, QWidget

from wordless import wl_file_area
from wordless.wl_checks import wl_checks_misc
from wordless.wl_settings import wl_settings_default, wl_settings_global

SEARCH_TERMS = ['be']

# An instance of QApplication must be created before any instance of QWidget
wl_app = QApplication(sys.argv)

class Wl_Test_Main(QWidget):
    def __init__(self):
        super().__init__()

        self.app = wl_app

        # Email
        self.email = 'blkserene@gmail.com'
        self.email_html = '<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a>'

        # Default settings
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

        # Global settings
        self.settings_global = wl_settings_global.init_settings_global()

        # Status bar
        self.status_bar = QStatusBar()

        # Files
        self.wl_file_area = QObject()
        self.wl_file_area.main = self
        self.wl_file_area.file_type = 'observed'
        self.wl_file_area.settings_suffix = ''

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

    def height(self):
        return 1080

    def statusBar(self):
        return self.status_bar

class Wl_Exception_Tests_Lang_Skipped(Exception):
    def __init__(self, lang):
        super().__init__(f'Tests for language "{lang}" is skipped!')

class Wl_Exception_Tests_Lang_Util_Skipped(Exception):
    def __init__(self, lang_util):
        super().__init__(f'Tests for language utility "{lang_util}" is skipped!')

# Select files randomly
def select_random_files(main, num_files):
    files = main.settings_custom['file_area']['files_open']

    for file in files:
        file['selected'] = False

    for file in random.sample(files, num_files):
        file['selected'] = True # pylint: disable=unsupported-assignment-operation

def select_random_files_ref(main, num_files):
    files = main.settings_custom['file_area']['files_open_ref']

    for file in files:
        file['selected'] = False

    for file in random.sample(files, num_files):
        file['selected'] = True # pylint: disable=unsupported-assignment-operation

# Clean cached files
def clean_import_caches():
    for file in glob.glob('imports/*.*'):
        os.remove(file)

def change_default_tokenizers(main):
    settings_custom_sentence_tokenization = main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings']
    settings_global_sentence_tokenizers = main.settings_global['sentence_tokenizers']
    settings_custom_word_tokenization = main.settings_custom['word_tokenization']['word_tokenizer_settings']
    settings_global_word_tokenizers = main.settings_global['word_tokenizers']

    for lang in settings_custom_sentence_tokenization:
        for lang_util in settings_global_sentence_tokenizers[lang]:
            if lang_util == 'spacy_sentencizer':
                settings_custom_sentence_tokenization[lang] = lang_util

                break

    for lang in settings_custom_word_tokenization:
        if 'nltk_nltk' in settings_global_word_tokenizers[lang]:
            settings_custom_word_tokenization[lang] = 'nltk_nltk'
        elif 'pkuseg_zho' in settings_global_word_tokenizers[lang]:
            settings_custom_word_tokenization[lang] = 'pkuseg_zho'
        elif 'sudachipy_jpn_split_mode_a' in settings_global_word_tokenizers[lang]:
            settings_custom_word_tokenization[lang] = 'sudachipy_jpn_split_mode_a'
        else:
            for lang_util in settings_global_word_tokenizers[lang]:
                if lang_util.startswith('spacy_'):
                    settings_custom_word_tokenization[lang] = lang_util

                    break

def change_default_lang_utils_stanza(main):
    for settings_custom, settings_global in [
        (
            main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'],
            main.settings_global['sentence_tokenizers']
        ), (
            main.settings_custom['word_tokenization']['word_tokenizer_settings'],
            main.settings_global['word_tokenizers']
        ), (
            main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'],
            main.settings_global['pos_taggers']
        ), (
            main.settings_custom['lemmatization']['lemmatizer_settings'],
            main.settings_global['lemmatizers']
        ), (
            main.settings_custom['dependency_parsing']['dependency_parser_settings'],
            main.settings_global['dependency_parsers']
        ), (
            main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings'],
            main.settings_global['sentiment_analyzers']
        )
    ]:
        for lang in settings_custom:
            for lang_util in settings_global[lang]:
                if lang_util.startswith('stanza_'):
                    settings_custom[lang] = lang_util

                    break
