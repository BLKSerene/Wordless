# -*- coding: utf-8 -*-

#
# Wordless: Testing for Sentence Tokenization
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
text_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。此外，汉语还是联合国官方语文[3]，并被上海合作组织等国际组织采用为官方语言。在中国大陆，汉语通称为“汉语”。在联合国、台湾、香港及澳门，通称为“中文”。在新加坡及马来西亚，通称为“华语”[注 1]。'

print('Chinese (Simplified) / Wordless - Chinese Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_zho_cn, 'zho_cn',
                                                                    sentence_tokenizer = 'Wordless - Chinese Sentence Tokenizer'):
    print(f'\t{sentence}')

# English
text_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to the area of Great Britain that would later take their name, England, both names ultimately deriving from the Anglia peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, particularly Norse (a North Germanic language), as well as by Latin and French.[6]'

print('English / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_eng, 'eng',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

print('English / spaCy - English Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_eng, 'eng',
                                                                    sentence_tokenizer = 'spaCy - English Sentence Tokenizer'):
    print(f'\t{sentence}')

# Japanese
text_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。統計によって前後する場合もあるが、この数は世界の母語話者数で上位10位以内に入る人数である。'

print('Japanese / Wordless - Japanese Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_jpn, 'jpn',
                                                                    sentence_tokenizer = 'Wordless - Japanese Sentence Tokenizer'):
    print(f'\t{sentence}')

# Norwegian Bokmål
text_nob = 'Norsk er et nordisk språk som snakkes som morsmål av rundt 5 millioner mennesker,[1][trenger bedre kilde] først og fremst i Norge, hvor det er offisielt språk. Det snakkes også av over 50 000 norsk-amerikanere i USA, spesielt i Midtvesten. Norsk, svensk og dansk utgjør sammen de fastlandsnordiske språkene, et kontinuum av mer eller mindre innbyrdes forståelige dialekter i Skandinavia.[2] Norsk kan føres tilbake til de vestnordiske dialektene av norrønt, som også islandsk og færøysk har utgått fra, men avstanden til disse øynordiske språkene er i dag langt større enn avstanden til de østnordiske språkene dansk og svensk. Det er vanskelig å avgrense norsk mot svensk og dansk etter rent språklige kriterier; i praksis kan moderne norsk sies å være de skandinaviske dialekter og standardspråk som har geografisk tilknytning til Norge.'

print('Norwegian Bokmål / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_nob, 'nob',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Norwegian Nynorsk
text_nno = 'Norsk er eit germansk språk som høyrer til den nordiske, eller nordgermanske, greina. Norsk blir for det meste snakka i Noreg, men òg i norske utvandrarsamfunn, som blant norsk-amerikanarar i USA. I dei gamle norske provinsane i Sverige — Jemtland, Herjedalen og Båhuslen — har dialektane mange likskapar med norsk, særleg nord i området.[1]'

print('Norwegian Nynorsk / NLTK - Punkt Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_nno, 'nno',
                                                                    sentence_tokenizer = 'NLTK - Punkt Sentence Tokenizer'):
    print(f'\t{sentence}')

# Thai
text_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย ภาษาไทยเป็นภ าษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาไท-กะได สันนิษฐานว่า ภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต'

print('Thai / PyThaiNLP - Thai Sentence Tokenizer:')

for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_tha, 'tha',
                                                                    sentence_tokenizer = 'PyThaiNLP - Thai Sentence Tokenizer'):
    print(f'\t{sentence}')
