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

import itertools
import sys

sys.path.append('.')

from wordless_testing import testing_init
from wordless_text import wordless_text_processing, wordless_text_utils
from wordless_utils import wordless_conversion

main = testing_init.Testing_Main()

def testing_word_detokenize(lang, word_detokenizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {word_detokenizer}:')

    wordless_text_utils.check_word_tokenizers(main, lang)

    tokens_sentences = wordless_text_processing.wordless_word_tokenize(main, globals()[f'text_{lang}'],
                                                                       lang = lang)
    tokens = list(itertools.chain.from_iterable(tokens_sentences))

    text = wordless_text_processing.wordless_word_detokenize(main, tokens,
                                                             lang = lang,
                                                             word_detokenizer = word_detokenizer)

    print(f"\t{text}")

text_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。此外，汉语还是联合国官方语文[3]，并被上海合作组织等国际组织采用为官方语言。在中国大陆，汉语通称为“汉语”。在联合国、台湾、香港及澳门，通称为“中文”。在新加坡及马来西亚，通称为“华语”[注 1]。'

text_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to the area of Great Britain that would later take their name, England, both names ultimately deriving from the Anglia peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, particularly Norse (a North Germanic language), as well as by Latin and French.[6]'

text_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。統計によって前後す 173 る場合もあるが、この数は世界の母語話者数で上位10位以内に入る人数である。'

text_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย ภาษาไทยเป็นภ าษาในกลุ่มภาษาไท ซึ่งเป็นกลุ่มย่อยของตระกูลภาษาไท-กะได สันนิษฐานว่า ภาษาในตระกูลนี้มีถิ่นกำเนิดจากทางตอนใต้ของประเทศจีน และนักภาษาศาสตร์บางส่วนเสนอว่า ภาษาไทยน่าจะมีความเชื่อมโยงกับตระกูลภาษาออสโตร-เอเชียติก ตระกูลภาษาออสโตรนีเซียน และตระกูลภาษาจีน-ทิเบต'

testing_word_detokenize(lang = 'zho_cn',
                        word_detokenizer = 'Wordless - Chinese Word Detokenizer')
testing_word_detokenize(lang = 'eng',
                        word_detokenizer = 'NLTK - Penn Treebank Detokenizer')
testing_word_detokenize(lang = 'eng',
                        word_detokenizer = 'SacreMoses - Moses Detokenizer')
testing_word_detokenize(lang = 'jpn',
                        word_detokenizer = 'Wordless - Japanese Word Detokenizer')
testing_word_detokenize(lang = 'tha',
                        word_detokenizer = 'Wordless - Thai Word Detokenizer')
