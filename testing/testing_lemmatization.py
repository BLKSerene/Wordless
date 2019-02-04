#
# Wordless: Testing - Lemmatization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

from PyQt5.QtCore import *

sys.path.append('..')

from wordless_text import wordless_text_processing
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

# Dutch
sentence_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_nld, lang = 'nld')

print('Dutch / spaCy - Dutch Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'nld',
                                                     lemmatizer = 'spaCy - Dutch Lemmatizer')

print(f"\t{lemmas}")

# English
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_eng, lang = 'eng')

print('English / NLTK - WordNet Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'eng',
                                                     lemmatizer = 'NLTK - WordNet Lemmatizer')

print(f"\t{lemmas}")

print('English / Lemmatization Lists:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'eng',
                                                     lemmatizer = 'Lemmatization Lists')

print(f"\t{lemmas}")

print('English / spaCy - English Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'eng',
                                                     lemmatizer = 'spaCy - English Lemmatizer')

print(f"\t{lemmas}")

# French
sentence_fra = 'Le français est une langue indo-européenne de la famille des langues romanes.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_fra, lang = 'fra')

print('French / spaCy - French Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'fra',
                                                     lemmatizer = 'spaCy - French Lemmatizer')

print(f"\t{lemmas}")

# German
sentence_deu = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_deu, lang = 'deu')

print('German / spaCy - German Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'deu',
                                                     lemmatizer = 'spaCy - German Lemmatizer')

print(f"\t{lemmas}")

# Italian
sentence_ita = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_ita, lang = 'ita')

print('Italian / spaCy - Italian Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'ita',
                                                     lemmatizer = 'spaCy - Italian Lemmatizer')

print(f"\t{lemmas}")

# Portuguese
sentence_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_por, lang = 'por')

print('Portuguese / spaCy - Portuguese Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'por',
                                                     lemmatizer = 'spaCy - Portuguese Lemmatizer')

print(f"\t{lemmas}")

# Russian
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_rus, lang = 'rus')

print('Russian / pymorphy2 - Morphological Analyzer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'rus',
                                                     lemmatizer = 'pymorphy2 - Morphological Analyzer')

print(f"\t{lemmas}")

# Spanish
sentence_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_spa, lang = 'spa')

print('Spanish / spaCy - Spanish Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'spa',
                                                     lemmatizer = 'spaCy - Spanish Lemmatizer')

print(f"\t{lemmas}")

# Tibetan
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_bod, lang = 'bod')

print('Tibetan / pybo - Tibetan Lemmatizer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'bod',
                                                     lemmatizer = 'pybo - Tibetan Lemmatizer')

print(f"\t{lemmas}")

# Ukrainian
sentence_ukr = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
tokens = wordless_text_processing.wordless_word_tokenize(main, sentence_ukr, lang = 'ukr')

print('Ukrainian / pymorphy2 - Morphological Analyzer:')

lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                     lang = 'ukr',
                                                     lemmatizer = 'pymorphy2 - Morphological Analyzer')

print(f"\t{lemmas}")
