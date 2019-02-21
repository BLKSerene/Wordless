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

    text = wordless_text_processing.wordless_word_detokenize(main, globals()[f'tokens_{lang}'],
                                                             lang = lang,
                                                             word_detokenizer = word_detokenizer)

    print(f"\t{text}")

sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。汉语有多种分支，当中标准官话最为流行，为中华人民共和国的国家通用语言（又称为普通话）、以及中华民国的国语。'
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5]'
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'
sentence_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

tokens_zho_cn = ['作为', '语言', '而言', '，', '为', '世界', '使用', '人', '数最多', '的', '语言', '，', '目前', '世界', '有', '五分之一', '人口', '做', '为', '母语', '。', '汉语', '有', '多种', '分支', '，', '当中', '标准', '官话', '最为', '流行', '，', '为', '中华人民共和国', '的', '国家', '通用', '语言', '（', '又', '称为', '普通话', '）', '、', '以及', '中华民国', '的', '国语', '。']
tokens_eng = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca.[4][5', ']']
tokens_jpn = ['使用', '人口', 'に', 'つい', 'て', '正確', 'な', '統計', 'は', 'ない', 'が', '、', '日本', '国', '内', 'の', '人口', '、', 'および', '日本', '国', '外', 'に', '住む', '日本', '人', 'や', '日系', '人', '、', '日本', 'が', 'かつて', '統治', 'し', 'た', '地域', 'の', '一部', '住民', 'など', '、', '約', '1', '億', '3千', '万', '人', '以上', 'と', '考え', 'られ', 'て', 'いる', '[', '7', ']', '。']
tokens_tha = ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศไทย']
tokens_bod = ['༄༅། །', 'རྒྱ་གར་', 'སྐད་', 'དུ', '།', 'བོ་དྷི་སཏྭ་', 'ཙརྻ་', 'ཨ་བ་ཏ་ར', '།', 'བོད་སྐད་', 'དུ', '།', 'བྱང་ཆུབ་སེམས་དཔ', 'འི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ', '། །', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ', '། །', 'བདེ་གཤེགས་', 'ཆོས་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲས་', 'བཅས་', 'དང༌', '། །', 'ཕྱག་འོས་', 'ཀུན་', 'ལ', 'འང་', 'གུས་པ', 'ར་', 'ཕྱག་', 'འཚལ་', 'ཏེ', '། །', 'བདེ་གཤེགས་', 'སྲས་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི', '། །', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་ན', 'ས་', 'ནི་', 'བརྗོད་པ', 'ར་', 'བྱ', '། །']

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
testing_word_detokenize(lang = 'bod',
                        word_detokenizer = 'Wordless - Tibetan Word Detokenizer')
