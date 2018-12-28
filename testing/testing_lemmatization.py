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
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, lang_code = 'eng')

print('English / NLTK - WordNet Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang_code = 'eng',
                                                     lemmatizer = 'NLTK - WordNet Lemmatizer')

print(f"\t{lemmas}")

print('English / Lemmatization Lists:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang_code = 'eng',
                                                     lemmatizer = 'Lemmatization Lists')

print(f"\t{lemmas}")

# Russian
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_rus, lang_code = 'rus')

print('Russian / pymorphy2 - Morphological Analyzer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang_code = 'rus',
                                                     lemmatizer = 'pymorphy2 - Morphological Analyzer')

print(f"\t{lemmas}")

# Ukrainian
sentence_ukr = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_ukr, lang_code = 'ukr')

print('Ukrainian / pymorphy2 - Morphological Analyzer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang_code = 'ukr',
                                                     lemmatizer = 'pymorphy2 - Morphological Analyzer')

print(f"\t{lemmas}")
