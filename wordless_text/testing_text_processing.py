# -*- coding: utf-8 -*-

#
# Wordless: Testing for Text Processing
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import sys

from PyQt5.QtCore import *

sys.path.append('E:/Wordless')

import wordless_text_processing
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

# Chinese (Simplified)
text_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。此外，汉语还是联合国官方语文[3]，并被上海合作组织等国际组织采用为官方语言。在中国大陆，汉语通称为“汉语”。在联合国、台湾、香港及澳门，通称为“中文”。在新加坡及马来西亚，通称为“华语”[注 1]。'
sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。'

print('---------- Chinese (Simplified) ---------- ')
print('Sentence Tokenization (Wordless - Chinese Sentence Tokenizer):')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_cn, 'zho_cn',
                                                                    sentence_tokenizer = 'Wordless - Chinese Sentence Tokenizer'):
    print(f'\t{sentence}')

print('Sentence Tokenization (HanLP - Sentence Segmenter):')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_cn, 'zho_cn',
                                                                    sentence_tokenizer = 'HanLP - Sentence Segmenter'):
    print(f'\t{sentence}')

print('Word Tokenization (jieba):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'jieba')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (SacreMoses - Moses Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'SacreMoses - Moses Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Detokenization (Wordless - Chinese Word Detokenizer):')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'zho_cn',
                                                         word_detokenizer = 'Wordless - Chinese Word Detokenizer')

print(f"\t{text}")

# Chinese (Traditional)
text_zho_tw = '作為語言而言，為世界使用人數最多的語言，目前世界有五分之一人口做為母語。漢語有多種分支，當中標準官話最為流行，為中華人民共和國的國家通用語言（又稱為普通話）、以及中華民國的國語。此外，漢語還是聯合國官方語文[3]，並被上海合作組織等國際組織採用為官方語言。在中國大陸，漢語通稱為「漢語」。在聯合國、臺灣、香港及澳門，通稱為「中文」。在新加坡及馬來西亞，通稱為「華語」[註 1]。'
sentence_zho_tw = '作為語言而言，為世界使用人數最多的語言，目前世界有五分之一人口做為母語。漢語有多種分支，當中標準官話最為流行，為中華人民共和國的國家通用語言（又稱為普通話）、以及中華民國的國語。'

print('---------- Chinese (Traditional) ---------- ')
print('Word Tokenization (HanLP - Traditional Chinese Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_tw, 'zho_tw',
                                                         word_tokenizer = 'HanLP - Traditional Chinese Tokenizer')

print(f"\t{' '.join(tokens)}")

# English
text_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to the area of Great Britain that would later take their name, England, both names ultimately deriving from the Anglia peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, particularly Norse (a North Germanic language), as well as by Latin and French.[6]'
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'

print('---------- English ---------- ')
print('Sentence Tokenization (NLTK - Punkt Sentence Tokenizer):')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_eng, 'eng',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

print('Word Tokenization (NLTK - Penn Treebank Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Treebank Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (NLTK - Twitter Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Twitter Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (NLTK - NIST Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - NIST Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (NLTK - NIST Tokenizer (International Mode)):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - NIST Tokenizer (International Mode)')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (NLTK - Tok-tok Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Tok-tok Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (NLTK - Word Punctuation Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Word Punctuation Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (SacreMoses - Moses Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'SacreMoses - Moses Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (SacreMoses - Penn Treebank Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'SacreMoses - Penn Treebank Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Tokenization (PyDelphin - Repp Tokenizer):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'PyDelphin - Repp Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Word Detokenization (NLTK - Penn Treebank Detokenizer):')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'eng',
                                                         word_detokenizer = 'NLTK - Penn Treebank Detokenizer')

print(f'\t{text}')

print('Word Detokenization (SacreMoses - Moses Detokenizer):')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'eng',
                                                         word_detokenizer = 'SacreMoses - Moses Detokenizer')

print(f'\t{text}')

# Japanese
text_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。統計によって前後する場合もあるが、この数は世界の母語話者数で上位10位以内に入る人数である。'
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'

print('---------- Japanese ---------- ')
print('Sentence Tokenization (Wordless - Japanese Sentence Tokenizer):')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_jpn, 'jpn',
                                                                    sentence_tokenizer = 'Wordless - Japanese Sentence Tokenizer'):
    print(f'\t{sentence}')

print('Word Tokenization (Nagisa):')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_jpn, 'jpn',
                                                         word_tokenizer = 'Nagisa')

print(f"\t{' '.join(tokens)}")

print('Word Detokenization (Wordless - Japanese Word Detokenizer):')

text = wordless_text_processing.wordless_word_detokenize(main, tokens, 'jpn',
                                                         word_detokenizer = 'Wordless - Japanese Word Detokenizer')

print(f'\t{text}')
