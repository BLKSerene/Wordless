# -*- coding: utf-8 -*-

#
# Wordless: Testing - Word Detokenization
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

sys.path.append('.')

from wordless_text import wordless_text_processing
from wordless_settings import init_settings_default, init_settings_global

main = QObject()

init_settings_default.init_settings_default(main)
init_settings_global.init_settings_global(main)

main.settings_custom = main.settings_default

# Chinese (Simplified)
text_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。此外，汉语还是联合国官方语文[3]，并被上海合作组织等国际组织采用为官方语言。在中国大陆，汉语通称为“汉语”。在联合国、台湾、香港及澳门，通称为“中文”。在新加坡及马来西亚，通称为“华语”[注 1]。'

sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_zho_cn, lang = 'zho_cn')
tokens = wordless_text_processing.wordless_word_tokenize(main, sentences, lang = 'zho_cn')

print('Chinese (Simplified) / Wordless - Chinese Word Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens,
												         lang = 'zho_cn',
                                                         word_detokenizer = 'Wordless - Chinese Word Detokenizer')

print(f"\t{text}")

# English
text_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to the area of Great Britain that would later take their name, England, both names ultimately deriving from the Anglia peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, particularly Norse (a North Germanic language), as well as by Latin and French.[6]'

sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_eng, lang = 'eng')
tokens = wordless_text_processing.wordless_word_tokenize(main, sentences, lang = 'eng')

print('English / NLTK - Penn Treebank Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens,
														 lang = 'eng',
                                                         word_detokenizer = 'NLTK - Penn Treebank Detokenizer')

print(f'\t{text}')

print('English / SacreMoses - Moses Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens,
														 lang = 'eng',
                                                         word_detokenizer = 'SacreMoses - Moses Detokenizer')

print(f'\t{text}')

# Japanese
text_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。統計によって前後す 173 る場合もあるが、この数は世界の母語話者数で上位10位以内に入る人数である。'

sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_jpn, lang = 'jpn')
tokens = wordless_text_processing.wordless_word_tokenize(main, sentences, lang = 'jpn')

print('Japanese / Wordless - Japanese Word Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens,
														 lang = 'jpn',
                                                         word_detokenizer = 'Wordless - Japanese Word Detokenizer')

print(f'\t{text}')

# Thai
text_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย ภาษาไทยเป็นภ าษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาไท-กะได สันนิษฐานว่า ภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต'

sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_tha, lang = 'tha')
tokens = wordless_text_processing.wordless_word_tokenize(main, sentences, lang = 'tha')

print('Thai / Wordless - Thai Word Detokenizer:')

text = wordless_text_processing.wordless_word_detokenize(main, tokens,
														 lang = 'tha',
                                                         word_detokenizer = 'Wordless - Thai Word Detokenizer')

print(f'\t{text}')
