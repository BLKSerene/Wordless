# -*- coding: utf-8 -*-

#
# Wordless: Testing for Word Tokenization
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import sys

from PyQt5.QtCore import *

import jpype
import pyhanlp

sys.path.append('E:/Wordless')

from wordless_text import wordless_text, wordless_text_processing
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

main.crf_analyzer = jpype.JClass('com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer')()
main.perceptron_analyzer = jpype.JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')()

# Arabic
sentence_ara = 'اللُّغَة العَرَبِيّة هي أكثر اللغات تحدثاً ونطقاً ضمن مجموعة اللغات السامية، وإحدى أكثر اللغات انتشاراً في العالم، يتحدثها أكثر من 467 مليون نسمة،[4](1) ويتوزع متحدثوها في الوطن العربي، بالإضافة إلى العديد من المناطق الأخرى المجاورة كالأحواز وتركيا وتشاد ومالي والسنغال وإرتيريا وإثيوبيا وجنوب السودان وإيران.'

print('Arabic / spaCy - Arabic Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_ara, 'ara',
                                                         word_tokenizer = 'spaCy - Arabic Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Chinese (Simplified)
sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。'

print('Chinese (Simplified) / jieba - Chinese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'jieba - Chinese Word Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - Standard Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - Standard Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - Basic Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - Basic Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - High-speed Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - High-speed Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - URL Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - URL Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - CRF Lexical Analyzer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - CRF Lexical Analyzer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - Perceptron Lexical Analyzer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - Perceptron Lexical Analyzer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - Dijkstra Segmenter:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - Dijkstra Segmenter')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - N-shortest Path Segmenter:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - N-shortest Path Segmenter')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / HanLP - HanLP - Viterbi Segmenter:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'HanLP - Viterbi Segmenter')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / SacreMoses - Moses Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn, 'zho_cn',
                                                         word_tokenizer = 'SacreMoses - Moses Tokenizer')

print(f"\t{' '.join(tokens)}")

# Chinese (Traditional)
sentence_zho_tw = '作為語言而言，為世界使用人數最多的語言，目前世界有五分之一人口做為母語。'

print('Chinese (Traditional) / HanLP - Traditional Chinese Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_tw, 'zho_tw',
                                                         word_tokenizer = 'HanLP - Traditional Chinese Tokenizer')

print(f"\t{' '.join(tokens)}")

# English
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'

print('English / NLTK - Penn Treebank Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Penn Treebank Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / NLTK - NIST Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - NIST Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / NLTK - Tok-tok Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Tok-tok Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / NLTK - Twitter Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'NLTK - Twitter Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / SacreMoses - Moses Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'SacreMoses - Moses Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / SacreMoses - Penn Treebank Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, 'eng',
                                                         word_tokenizer = 'SacreMoses - Penn Treebank Tokenizer')

print(f"\t{' '.join(tokens)}")

# Japanese
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'

print('Japanese / nagisa - Japanese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_jpn, 'jpn',
                                                         word_tokenizer = 'nagisa - Japanese Word Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Japanese / Wordless - Japanese Character Splitter:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_jpn, 'jpn',
                                                         word_tokenizer = 'Wordless - Japanese Character Splitter')

print(f"\t{' '.join(tokens)}")

# Thai
sentence_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'

print('Thai / PyThaiNLP - Maximum Matching Algorithm + TCC:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_tha, 'tha',
                                                         word_tokenizer = 'PyThaiNLP - Maximum Matching Algorithm + TCC')

print(f"\t{' '.join(tokens)}")

print('Thai / PyThaiNLP - Maximum Matching Algorithm:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_tha, 'tha',
                                                         word_tokenizer = 'PyThaiNLP - Maximum Matching Algorithm')

print(f"\t{' '.join(tokens)}")

print('Thai / PyThaiNLP - Longest Matching:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_tha, 'tha',
                                                         word_tokenizer = 'PyThaiNLP - Longest Matching')

print(f"\t{' '.join(tokens)}")

# Vietnamese
sentence_vie = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam.'

print('Vietnamese / Pyvi - Vietnamese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_vie, 'vie',
                                                         word_tokenizer = 'Pyvi - Vietnamese Word Tokenizer')
print(f"\t{' '.join([token.replace(' ', '_') for token in tokens])}")
