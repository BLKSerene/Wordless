#
# Wordless: Testing - POS Tagging
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

# Chinese (Simplified)
sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。'

print('Chinese / jieba - Chinese POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_zho_cn,
                                                          lang = 'zho_cn',
                                                          pos_tagger = 'jieba - Chinese POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_zho_cn,
                                                                    lang = 'zho_cn',
                                                                    pos_tagger = 'jieba - Chinese POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Dutch
sentence_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'

print('Dutch / spaCy - Dutch POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_nld,
                                                          lang = 'nld',
                                                          pos_tagger = 'spaCy - Dutch POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_nld,
                                                                    lang = 'nld',
                                                                    pos_tagger = 'spaCy - Dutch POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# English
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'

print('English / NLTK - Perceptron POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_eng,
                                                          lang = 'eng',
                                                          pos_tagger = 'NLTK - Perceptron POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_eng,
                                                                    lang = 'eng',
                                                                    pos_tagger = 'NLTK - Perceptron POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

print('English / spaCy - English POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_eng,
                                                          lang = 'eng',
                                                          pos_tagger = 'spaCy - English POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_eng,
                                                                    lang = 'eng',
                                                                    pos_tagger = 'spaCy - English POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# French
sentence_fra = 'Le français est une langue indo-européenne de la famille des langues romanes.'

print('French / spaCy - French POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_fra,
                                                          lang = 'fra',
                                                          pos_tagger = 'spaCy - French POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_fra,
                                                                    lang = 'fra',
                                                                    pos_tagger = 'spaCy - French POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# German
sentence_deu = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'

print('German / spaCy - German POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_deu,
                                                          lang = 'deu',
                                                          pos_tagger = 'spaCy - German POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_deu,
                                                                    lang = 'deu',
                                                                    pos_tagger = 'spaCy - German POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Italian
sentence_ita = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."

print('Italian / spaCy - Italian POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_ita,
                                                          lang = 'ita',
                                                          pos_tagger = 'spaCy - Italian POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_ita,
                                                                    lang = 'ita',
                                                                    pos_tagger = 'spaCy - Italian POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Japanese
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'

print('Japanese / nagisa - Japanese POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_jpn,
                                                          lang = 'jpn',
                                                          pos_tagger = 'nagisa - Japanese POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_jpn,
                                                                    lang = 'jpn',
                                                                    pos_tagger = 'nagisa - Japanese POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Portuguese
sentence_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'

print('Portuguese / spaCy - Portuguese POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_por,
                                                          lang = 'por',
                                                          pos_tagger = 'spaCy - Portuguese POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_por,
                                                                    lang = 'por',
                                                                    pos_tagger = 'spaCy - Portuguese POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Russian
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'

print('Russian / NLTK - Perceptron POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_rus,
                                                          lang = 'rus',
                                                          pos_tagger = 'NLTK - Perceptron POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_rus,
                                                                    lang = 'rus',
                                                                    pos_tagger = 'NLTK - Perceptron POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

print('Russian / pymorphy2 - Morphological Analyzer:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_rus,
                                                          lang = 'rus',
                                                          pos_tagger = 'pymorphy2 - Morphological Analyzer')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_rus,
                                                                    lang = 'rus',
                                                                    pos_tagger = 'pymorphy2 - Morphological Analyzer',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Spanish
sentence_tha = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'

print('Spanish / spaCy - Spanish POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_tha,
                                                          lang = 'spa',
                                                          pos_tagger = 'spaCy - Spanish POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_tha,
                                                                    lang = 'spa',
                                                                    pos_tagger = 'spaCy - Spanish POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Thai
sentence_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'

print('Thai / PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_tha,
                                                          lang = 'tha',
                                                          pos_tagger = 'PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_tha,
                                                                    lang = 'tha',
                                                                    pos_tagger = 'PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

print('Thai / PyThaiNLP - Perceptron POS Tagger - PUD Corpus:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_tha,
                                                          lang = 'tha',
                                                          pos_tagger = 'PyThaiNLP - Perceptron POS Tagger - PUD Corpus')

print(f"\t{tokens_tagged}")

# Tibetan
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

print('Tibetan / pybo - Tibetan POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_bod,
                                                          lang = 'bod',
                                                          pos_tagger = 'pybo - Tibetan POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_bod,
                                                                    lang = 'bod',
                                                                    pos_tagger = 'pybo - Tibetan POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Ukrainian
sentence_ukr = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'

print('Ukrainian / pymorphy2 - Morphological Analyzer:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_ukr,
                                                          lang = 'ukr',
                                                          pos_tagger = 'pymorphy2 - Morphological Analyzer')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_ukr,
                                                                    lang = 'ukr',
                                                                    pos_tagger = 'pymorphy2 - Morphological Analyzer',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")

# Vietnamese
sentence_vie = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam.'

print('Vietnamese / Underthesea - Vietnamese POS Tagger:')

tokens_tagged = wordless_text_processing.wordless_pos_tag(main, sentence_vie,
                                                          lang = 'vie',
                                                          pos_tagger = 'Underthesea - Vietnamese POS Tagger')
tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, sentence_vie,
                                                                    lang = 'vie',
                                                                    pos_tagger = 'Underthesea - Vietnamese POS Tagger',
                                                                    tagset = 'universal')

print(f"\t{tokens_tagged}")
print(f"\t{tokens_tagged_universal}")
