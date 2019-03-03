#
# Wordless: Stop Words - Chinese (Traditional)
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import json

import opencc
import spacy.lang.zh

# spaCy
stop_words = sorted(spacy.lang.zh.STOP_WORDS)

cc = opencc.OpenCC('s2t')

with open(r'spaCy/stop_words_zh_tw.txt', 'w', encoding = 'utf_8') as f:
    for stop_word in stop_words:
        f.write(f'{cc.convert(stop_word)}\n')

# Stopwords ISO
with open(r'Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
    stop_words = json.load(f)['zh']

with open(r'Stopwords ISO/stop_words_zh_tw.txt', 'w', encoding = 'utf_8') as f:
    for stop_word in stop_words:
        f.write(f'{cc.convert(stop_word)}\n')

print('Done!')
