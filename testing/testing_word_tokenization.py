#
# Wordless: Testing - Word Tokenization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re
import sys

from PyQt5.QtCore import *

sys.path.append('.')

from wordless_text import wordless_text, wordless_text_processing
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

# Chinese (Simplified)
sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。'

print('Chinese (Simplified) / jieba - Chinese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn,
                                                         lang = 'zho_cn',
                                                         word_tokenizer = 'jieba - Chinese Word Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Chinese (Simplified) / Wordless - Chinese Character Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_zho_cn,
                                                         lang = 'zho_cn',
                                                         word_tokenizer = 'Wordless - Chinese Character Tokenizer')

print(f"\t{' '.join(tokens)}")

# Dutch
sentence_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'

print('Dutch / spaCy - Dutch Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_nld,
                                                         lang = 'nld',
                                                         word_tokenizer = 'spaCy - Dutch Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# English
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'

print('English / NLTK - Penn Treebank Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng,
                                                         lang = 'eng',
                                                         word_tokenizer = 'NLTK - Penn Treebank Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / NLTK - NIST Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng,
                                                         lang = 'eng',
                                                         word_tokenizer = 'NLTK - NIST Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / NLTK - Tok-tok Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng,
                                                         lang = 'eng',
                                                         word_tokenizer = 'NLTK - Tok-tok Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / NLTK - Twitter Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng,
                                                         lang = 'eng',
                                                         word_tokenizer = 'NLTK - Twitter Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / SacreMoses - Moses Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng,
                                                         lang = 'eng',
                                                         word_tokenizer = 'SacreMoses - Moses Tokenizer')

print(f"\t{' '.join(tokens)}")

print('English / SacreMoses - Penn Treebank Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng,
                                                         lang = 'eng',
                                                         word_tokenizer = 'SacreMoses - Penn Treebank Tokenizer')

print(f"\t{' '.join(tokens)}")

# French
sentence_fra = 'Le français est une langue indo-européenne de la famille des langues romanes.'

print('French / spaCy - French Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_fra,
                                                         lang = 'fra',
                                                         word_tokenizer = 'spaCy - French Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# German
sentence_deu = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'

print('German / spaCy - German Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_deu,
                                                         lang = 'deu',
                                                         word_tokenizer = 'spaCy - German Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Italian
sentence_ita = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."

print('Italian / spaCy - Italian Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_ita,
                                                         lang = 'ita',
                                                         word_tokenizer = 'spaCy - Italian Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Japanese
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'

print('Japanese / nagisa - Japanese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_jpn,
                                                         lang = 'jpn',
                                                         word_tokenizer = 'nagisa - Japanese Word Tokenizer')

print(f"\t{' '.join(tokens)}")

print('Japanese / Wordless - Japanese Kanji Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_jpn,
                                                         lang = 'jpn',
                                                         word_tokenizer = 'Wordless - Japanese Kanji Tokenizer')

print(f"\t{' '.join(tokens)}")

# Portuguese
sentence_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'

print('Portuguese / spaCy - Portuguese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_por,
                                                         lang = 'por',
                                                         word_tokenizer = 'spaCy - Portuguese Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Russian
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'

print('Russian / spaCy - Russian Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_rus,
                                                         lang = 'rus',
                                                         word_tokenizer = 'spaCy - Russian Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Spanish
sentence_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'

print('Spanish / spaCy - Spanish Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_spa,
                                                         lang = 'spa',
                                                         word_tokenizer = 'spaCy - Spanish Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Thai
sentence_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'

print('Thai / PyThaiNLP - Maximum Matching Algorithm + TCC:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_tha,
                                                         lang = 'tha',
                                                         word_tokenizer = 'PyThaiNLP - Maximum Matching Algorithm + TCC')

print(f"\t{' '.join(tokens)}")

print('Thai / PyThaiNLP - Maximum Matching Algorithm:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_tha,
                                                         lang = 'tha',
                                                         word_tokenizer = 'PyThaiNLP - Maximum Matching Algorithm')

print(f"\t{' '.join(tokens)}")

print('Thai / PyThaiNLP - Longest Matching:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_tha,
                                                         lang = 'tha',
                                                         word_tokenizer = 'PyThaiNLP - Longest Matching')

print(f"\t{' '.join(tokens)}")

# Tibetan
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

print('Tibetan / pybo - Tibetan Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_bod,
                                                         lang = 'bod',
                                                         word_tokenizer = 'pybo - Tibetan Word Tokenizer')

print(f"\t{' '.join(tokens)}")

# Vietnamese
sentence_vie = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam.'

print('Vietnamese / Underthesea - Vietnamese Word Tokenizer:')

tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_vie,
                                                         lang = 'vie',
                                                         word_tokenizer = 'Underthesea - Vietnamese Word Tokenizer')
tokens = [re.sub(r'\s+', r'_', token) for token in tokens]

print(f"\t{' '.join(tokens)}")
