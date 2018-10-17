#
# Wordless: Converter of Simplified Chinese Stopwords to Traditional Chinese Stopwords
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import json

import pyhanlp

def stopwords_to_zh_tw():
	# Stopwords ISO
	with open(r'Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
		stop_words = json.load(f)['zh']

	with open(r'Stopwords ISO/stopwords_zh_TW.txt', 'w', encoding = 'utf_8') as f:
		for stop_word in stop_words:
			f.write(f'{pyhanlp.HanLP.convertToTraditionalChinese(stop_word)}\n')

	# stopwords-json
	with open(r'stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
		stop_words = json.load(f)['zh']

	with open(r'stopwords-json/stopwords_zh_TW.txt', 'w', encoding = 'utf_8') as f:
		for stop_word in stop_words:
			f.write(f'{pyhanlp.HanLP.convertToTraditionalChinese(stop_word)}\n')

	# HanLP
	with open(r'HanLP/stopwords.txt', 'r', encoding = 'utf_8') as f:
		stop_words = [line.rstrip() for line in f]

	with open(r'HanLP/stopwords_zh_TW.txt', 'w', encoding = 'utf_8') as f:
		for stop_word in stop_words:
			f.write(f'{pyhanlp.HanLP.convertToTraditionalChinese(stop_word)}\n')

if __name__ == '__main__':
	stopwords_to_zh_tw()