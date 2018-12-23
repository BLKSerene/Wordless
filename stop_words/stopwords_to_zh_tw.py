#
# Wordless: Converter of Stop Words from Simplified Chinese to Traditional Chinese
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import json
import os
import shutil

import pyhanlp
import spacy.lang.zh

# HanLP
path_pyhanlp = pyhanlp.__path__[0]
shutil.copy(os.path.join(path_pyhanlp, r'static/data/dictionary/stopwords.txt'),
	        r'HanLP/stop_words_zh_cn.txt')

with open(r'HanLP/stop_words_zh_cn.txt', 'r', encoding = 'utf_8') as f:
    stop_words = [line.rstrip() for line in f]

with open(r'HanLP/stop_words_zh_tw.txt', 'w', encoding = 'utf_8') as f:
    for stop_word in stop_words:
        f.write(f'{pyhanlp.HanLP.convertToTraditionalChinese(stop_word)}\n')

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
