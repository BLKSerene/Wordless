#
# Wordless: Converter of Stop Words from Simplified Chinese to Traditional Chinese
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import json

import pyhanlp
import spacy.lang.zh

# spaCy
stop_words = sorted(spacy.lang.zh.STOP_WORDS)

with open(r'spaCy/stop_words_zh_tw.txt', 'w', encoding = 'utf_8') as f:
    for stop_word in stop_words:
        f.write(f'{pyhanlp.HanLP.convertToTraditionalChinese(stop_word)}\n')

# Stopwords ISO
with open(r'Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
    stop_words = json.load(f)['zh']

with open(r'Stopwords ISO/stop_words_zh_tw.txt', 'w', encoding = 'utf_8') as f:
    for stop_word in stop_words:
        f.write(f'{pyhanlp.HanLP.convertToTraditionalChinese(stop_word)}\n')
