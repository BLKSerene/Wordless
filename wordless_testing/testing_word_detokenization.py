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
from wordless_text import wordless_text
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

sentence_zho_cn = '汉语，又称中文、华文、唐话[2]，或被视为汉藏语系汉语族下之语言，或被视为语族。'
sentence_zho_tw = '漢語，又稱中文、華文、唐話[2]，或被視為漢藏語系漢語族下之語言，或被視為語族。'
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5]'
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'
sentence_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

tokens_zho_cn = ['汉语', '，', '又称', '中文', '、', '华文', '、', '唐话', '[', '2', ']', '，', '或', '被', '视为', '汉藏语系', '汉语', '族', '下', '之', '语言', '，', '或', '被', '视为', '语族', '。']
tokens_zho_tw = ['漢語', '，', '又', '稱', '中文', '、', '華文', '、', '唐話', '[', '2', ']', '，', '或', '被', '視為', '漢藏語', '系漢', '語族', '下', '之', '語言', '，', '或', '被', '視為', '語族', '。']
tokens_eng = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca.[4][5', ']']
tokens_jpn = ['使用', '人口', 'に', 'つい', 'て', '正確', 'な', '統計', 'は', 'ない', 'が', '、', '日本', '国', '内', 'の', '人口', '、', 'および', '日本', '国', '外', 'に', '住む', '日本', '人', 'や', '日系', '人', '、', '日本', 'が', 'かつて', '統治', 'し', 'た', '地域', 'の', '一部', '住民', 'など', '、', '約', '1', '億', '3千', '万', '人', '以上', 'と', '考え', 'られ', 'て', 'いる', '[', '7', ']', '。']
tokens_tha = [wordless_text.Wordless_Token('ภาษาไทย', boundary = ' '), wordless_text.Wordless_Token('หรือ', boundary = ' '), 'ภาษาไทย', wordless_text.Wordless_Token('กลาง', boundary = ' '), 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศไทย']
tokens_bod = ['༄༅། །', 'རྒྱ་གར་','སྐད་', 'དུ', '།', 'བོ་དྷི་སཏྭ་', 'ཙརྻ་', 'ཨ་བ་ཏ་ར', '།', 'བོད་སྐད་', 'དུ', '།', 'བྱང་ཆུབ་སེམས་དཔ', 'འི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ', '། །', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ', '། །', 'བདེ་གཤེགས་', 'ཆོས་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲས་', 'བཅས་', 'དང༌', '། །', 'ཕྱག་འོས་', 'ཀུན་', 'ལ', 'འང་', 'གུས་པ', 'ར་', 'ཕྱག་', 'འཚལ་', 'ཏེ', '། །', 'བདེ་གཤེགས་', 'སྲས་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི', '། །', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་ན', 'ས་', 'ནི་', 'བརྗོད་པ', 'ར་', 'བྱ', '། །']

testing_word_detokenize(lang = 'zho_cn',
                        word_detokenizer = 'Wordless - Chinese Word Detokenizer')
testing_word_detokenize(lang = 'zho_tw',
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
