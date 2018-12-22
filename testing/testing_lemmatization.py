# -*- coding: utf-8 -*-

#
# Wordless: Testing for Lemmatization
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import sys

from PyQt5.QtCore import *

sys.path.append('E:/Wordless')

from wordless_text import wordless_text_processing
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

# English
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Penn Treebank Tokenizer')

print('English / NLTK:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens, 'eng',
                                                     lemmatizer = 'NLTK')

print(f"\t{lemmas}")

print('English / Lemmatization Lists:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens, 'eng',
                                                     lemmatizer = 'Lemmatization Lists')

print(f"\t{lemmas}")
