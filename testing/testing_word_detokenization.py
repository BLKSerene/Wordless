# -*- coding: utf-8 -*-

#
# Wordless: Testing for Word Detokenization
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

# Chinese (Simplified)
sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。'

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'jieba')

print('Chinese (Simplified) / Wordless - Chinese Word Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'zho_cn',
                                                         word_detokenizer = 'Wordless - Chinese Word Detokenizer')

print(f"\t{text}")

# English
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Penn Treebank Tokenizer')
print('English / NLTK - Penn Treebank Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'eng',
                                                         word_detokenizer = 'NLTK - Penn Treebank Detokenizer')

print(f'\t{text}')

print('English / SacreMoses - Moses Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'eng',
                                                         word_detokenizer = 'SacreMoses - Moses Detokenizer')

print(f'\t{text}')

# Japanese
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_jpn, 'jpn',
                                                         word_tokenizer = 'nagisa')
print('Japanese / Wordless - Japanese Word Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'jpn',
                                                         word_detokenizer = 'Wordless - Japanese Word Detokenizer')

print(f'\t{text}')
