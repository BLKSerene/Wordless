# -*- coding: utf-8 -*-

#
# Wordless: Tests - Text - Word Tokenization
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re
import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init, wl_test_lang_examples
from wl_text import wl_word_tokenization
from wl_utils import wl_conversion, wl_misc

test_word_tokenizers = []

main = wl_test_init.Wl_Test_Main()

for lang, word_tokenizers in main.settings_global['word_tokenizers'].items():
    for word_tokenizer in word_tokenizers:
        if lang not in ['other']:
            test_word_tokenizers.append((lang, word_tokenizer))

@pytest.mark.parametrize('lang, word_tokenizer', test_word_tokenizers)
def test_word_tokenize(lang, word_tokenizer, show_results = False):
    lang_text = wl_conversion.to_lang_text(main, lang)

    tokens = wl_word_tokenization.wl_word_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        word_tokenizer = word_tokenizer
    )

    if show_results:
        print(f'{lang} / {word_tokenizer}:')
        print(tokens)

    if lang == 'afr':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['Afrikaans', 'is', 'tipologies', 'gesien', "'n", 'Indo-Europese', ',', 'Wes-Germaanse', ',', 'Nederfrankiese', 'taal', ',', '[', '2', ']', 'wat', 'sy', 'ontstaan', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'gehad', 'het', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'tale', 'en', 'taalgroepe', '.']
        elif word_tokenizer == ['NLTK - NLTK Tokenizer',
                                'NLTK - Twitter Tokenizer']:
            assert tokens == ['Afrikaans', 'is', 'tipologies', 'gesien', "'", 'n', 'Indo-Europese', ',', 'Wes-Germaanse', ',', 'Nederfrankiese', 'taal', ',', '[', '2', ']', 'wat', 'sy', 'ontstaan', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'gehad', 'het', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'tale', 'en', 'taalgroepe', '.']
        elif word_tokenizer == 'spaCy - Afrikaans Word Tokenizer':
            assert tokens == ['Afrikaans', 'is', 'tipologies', 'gesien', "'", 'n', 'Indo', '-', 'Europese', ',', 'Wes', '-', 'Germaanse', ',', 'Nederfrankiese', 'taal,[2', ']', 'wat', 'sy', 'ontstaan', 'aan', 'die', 'suidpunt', 'van', 'Afrika', 'gehad', 'het', 'onder', 'invloed', 'van', 'verskeie', 'ander', 'tale', 'en', 'taalgroepe', '.']
    elif lang == 'sqi':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Gjuha', 'shqipe', '(', 'ose', 'thjeshtë', 'shqipja', ')', 'është', 'gjuhë', 'dhe', 'degë', 'e', 'veçantë', 'e', 'familjes', 'indo-evropiane', 'të', 'folur', 'nga', 'më', 'shumë', 'se', '6', 'milionë', 'njerëz', '[', '4', ']', ',', 'kryesisht', 'në', 'Shqipëri', ',', 'Kosovë', 'dhe', 'Republikën', 'e', 'Maqedonisë', ',', 'por', 'edhe', 'në', 'zona', 'të', 'tjera', 'të', 'Evropës', 'Jugore', 'ku', 'ka', 'një', 'popullsi', 'shqiptare', ',', 'duke', 'përfshirë', 'Malin', 'e', 'Zi', 'dhe', 'Luginën', 'e', 'Preshevës', '.']
        elif word_tokenizer == 'spaCy - Albanian Word Tokenizer':
            assert tokens == ['Gjuha', 'shqipe', '(', 'ose', 'thjeshtë', 'shqipja', ')', 'është', 'gjuhë', 'dhe', 'degë', 'e', 'veçantë', 'e', 'familjes', 'indo', '-', 'evropiane', 'të', 'folur', 'nga', 'më', 'shumë', 'se', '6', 'milionë', 'njerëz[4', ']', ',', 'kryesisht', 'në', 'Shqipëri', ',', 'Kosovë', 'dhe', 'Republikën', 'e', 'Maqedonisë', ',', 'por', 'edhe', 'në', 'zona', 'të', 'tjera', 'të', 'Evropës', 'Jugore', 'ku', 'ka', 'një', 'popullsi', 'shqiptare', ',', 'duke', 'përfshirë', 'Malin', 'e', 'Zi', 'dhe', 'Luginën', 'e', 'Preshevës', '.']
    elif lang == 'ara':
        assert tokens == ['اللُّغَة', 'العَرَبِيّة', 'هي', 'أكثر', 'اللغات', 'تحدثاً', 'ونطقاً', 'ضمن', 'مجموعة', 'اللغات', 'السامية', '،', 'وإحدى', 'أكثر', 'اللغات', 'انتشاراً', 'في', 'العالم', '،', 'يتحدثها', 'أكثر', 'من', '467', 'مليون', 'نسمة،(1', ')', 'ويتوزع', 'متحدثوها', 'في', 'الوطن', 'العربي', '،', 'بالإضافة', 'إلى', 'العديد', 'من', 'المناطق', 'الأخرى', 'المجاورة', 'كالأحواز', 'وتركيا', 'وتشاد', 'ومالي', 'والسنغال', 'وإرتيريا', 'وإثيوبيا', 'وجنوب', 'السودان', 'وإيران', '.']
    elif lang == 'ben':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামগুলোতেও', 'পরিচিত', ')', 'একটি', 'ইন্দো-আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা।']
        elif word_tokenizer == 'NLTK - Twitter Tokenizer':
            assert tokens == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামগুলোতেও', 'পরিচিত', ')', 'একটি', 'ইন্দো-আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
        elif word_tokenizer == 'spaCy - Arabic Word Tokenizer':
            assert tokens == ['বাংলা', 'ভাষা', '(', 'বাঙলা', ',', 'বাঙ্গলা', ',', 'তথা', 'বাঙ্গালা', 'নামগুলোতেও', 'পরিচিত', ')', 'একটি', 'ইন্দো', '-', 'আর্য', 'ভাষা', ',', 'যা', 'দক্ষিণ', 'এশিয়ার', 'বাঙালি', 'জাতির', 'প্রধান', 'কথ্য', 'ও', 'লেখ্য', 'ভাষা', '।']
    elif lang == 'bul':
        assert tokens == ['Бъ̀лгарският', 'езѝк', 'е', 'индоевропейски', 'език', 'от', 'групата', 'на', 'южнославянските', 'езици', '.']
    elif lang == 'cat':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', "l'Alguer", 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', "d'algunes", 'comarques', 'i', 'localitats', 'de', "l'interior", ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', "l'Aragó", ')', ',', 'la', 'ciutat', 'de', "l'Alguer", '(', 'a', "l'illa", 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'del', 'Nord', ',', '[', '8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrats', 'valencians', ')', ',', '[', '9', ']', '[', '10', ']', 'i', 'en', 'petites', 'comunitats', 'arreu', 'del', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', "l'Argentina", ',', 'amb', '195.000', 'parlants', ')', '.', '[', '11', ']']
        elif word_tokenizer == 'NLTK - Twitter Tokenizer':
            assert tokens == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', "l'Alguer", 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', "d'algunes", 'comarques', 'i', 'localitats', 'de', "l'interior", ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', "l'Aragó", ')', ',', 'la', 'ciutat', 'de', "l'Alguer", '(', 'a', "l'illa", 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'del', 'Nord', ',', '[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrats', 'valencians', ')', ',', '[', '9', ']', '[', '10', ']', 'i', 'en', 'petites', 'comunitats', 'arreu', 'del', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', "l'Argentina", ',', 'amb', '195.000', 'parlants', ')', '.', '[', '11', ']']
        elif word_tokenizer == 'Sacremoses - Moses Tokenizer':
            assert tokens == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', 'l', "'", 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', 'd', "'", 'algunes', 'comarques', 'i', 'localitats', 'de', 'l', "'", 'interior', ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', 'l', "'", 'Aragó', ')', ',', 'la', 'ciutat', 'de', 'l', "'", 'Alguer', '(', 'a', 'l', "'", 'illa', 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'del', 'Nord', ',', '[', '8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrats', 'valencians', ')', ',', '[', '9', ']', '[', '10', ']', 'i', 'en', 'petites', 'comunitats', 'arreu', 'del', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', 'l', "'", 'Argentina', ',', 'amb', '195.000', 'parlants', ')', '.', '[', '11', ']']
        elif word_tokenizer == 'spaCy - Catalan Word Tokenizer':
            assert tokens == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', "l'", 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'a', 'Catalunya', ',', 'el', 'País', 'Valencià', '(', 'tret', "d'", 'algunes', 'comarques', 'i', 'localitats', 'de', "l'", 'interior', ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', "l'", 'Aragó', ')', ',', 'la', 'ciutat', 'de', "l'", 'Alguer', '(', 'a', "l'", 'illa', 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'del', 'Nord,[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrats', 'valencians),[9][10', ']', 'i', 'en', 'petites', 'comunitats', 'arreu', 'del', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', "l'", 'Argentina', ',', 'amb', '195.000', 'parlants).[11', ']']
    elif lang == 'zho_cn':
        if word_tokenizer == 'jieba - Chinese Word Tokenizer':
            assert tokens == ['汉语', '，', '又称', '汉文', '、', '中文', '、', '中国', '话', '、', '中国', '语', '、', '华语', '、', '华文', '、', '唐话', '[', '2', ']', '，', '或', '被', '视为', '一个', '语族', '，', '或', '被', '视为', '隶属于', '汉藏语系', '汉语', '族', '之', '一种', '语言', '。']
        elif word_tokenizer == 'Wordless - Chinese Character Tokenizer':
            assert tokens == ['汉', '语', '，', '又', '称', '汉', '文', '、', '中', '文', '、', '中', '国', '话', '、', '中', '国', '语', '、', '华', '语', '、', '华', '文', '、', '唐', '话', '[', '2', ']', '，', '或', '被', '视', '为', '一', '个', '语', '族', '，', '或', '被', '视', '为', '隶', '属', '于', '汉', '藏', '语', '系', '汉', '语', '族', '之', '一', '种', '语', '言', '。']
    elif lang == 'zho_tw':
        if word_tokenizer == 'jieba - Chinese Word Tokenizer':
            assert tokens == ['漢語', '，', '又', '稱漢文', '、', '中文', '、', '中國話', '、', '中國語', '、', '華語', '、', '華文', '、', '唐話', '[', '2', ']', '，', '或', '被', '視為', '一個', '語族', '，', '或', '被', '視為', '隸屬', '於', '漢藏語', '系漢', '語族', '之一', '種語', '言', '。']
        elif word_tokenizer == 'Wordless - Chinese Character Tokenizer':
            assert tokens == ['漢', '語', '，', '又', '稱', '漢', '文', '、', '中', '文', '、', '中', '國', '話', '、', '中', '國', '語', '、', '華', '語', '、', '華', '文', '、', '唐', '話', '[', '2', ']', '，', '或', '被', '視', '為', '一', '個', '語', '族', '，', '或', '被', '視', '為', '隸', '屬', '於', '漢', '藏', '語', '系', '漢', '語', '族', '之', '一', '種', '語', '言', '。']
    elif lang == 'hrv':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'spaCy - Croatian Word Tokenizer']:
            assert tokens == ['Hrvatski', 'jezik', '(', 'ISO', '639', '-', '3', ':', 'hrv', ')', 'skupni', 'je', 'naziv', 'za', 'nacionalni', 'standardni', 'jezik', 'Hrvata', ',', 'te', 'za', 'skup', 'narječja', 'i', 'govora', 'kojima', 'govore', 'ili', 'su', 'nekada', 'govorili', 'Hrvati', '.']
        elif word_tokenizer in ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer',
                                'NLTK - Twitter Tokenizer']:
            assert tokens == ['Hrvatski', 'jezik', '(', 'ISO', '639-3', ':', 'hrv', ')', 'skupni', 'je', 'naziv', 'za', 'nacionalni', 'standardni', 'jezik', 'Hrvata', ',', 'te', 'za', 'skup', 'narječja', 'i', 'govora', 'kojima', 'govore', 'ili', 'su', 'nekada', 'govorili', 'Hrvati', '.']
        
    elif lang == 'ces':
        assert tokens == ['Čeština', 'neboli', 'český', 'jazyk', 'je', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
    elif lang == 'dan':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Dansk', 'er', 'et', 'nordgermansk', 'sprog', 'af', 'den', 'østnordiske', '(', 'kontinentale', ')', 'gruppe', ',', 'der', 'tales', 'af', 'ca', '.', 'seks', 'millioner', 'mennesker', '.']
        elif word_tokenizer in ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer',
                                'spaCy - Danish Word Tokenizer']:
            assert tokens == ['Dansk', 'er', 'et', 'nordgermansk', 'sprog', 'af', 'den', 'østnordiske', '(', 'kontinentale', ')', 'gruppe', ',', 'der', 'tales', 'af', 'ca.', 'seks', 'millioner', 'mennesker', '.']
        
    elif lang == 'nld':
        assert tokens == ['Het', 'Nederlands', 'is', 'een', 'West-Germaanse', 'taal', 'en', 'de', 'moedertaal', 'van', 'de', 'meeste', 'inwoners', 'van', 'Nederland', ',', 'België', 'en', 'Suriname', '.']
    elif lang == 'eng':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - Twitter Tokenizer',
                              'Sacremoses - Moses Tokenizer']:
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', '[', '4', ']', '[', '5', ']']
        elif word_tokenizer in ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer',
                                'syntok - Word Tokenizer']:
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca.', '[', '4', ']', '[', '5', ']']
        elif word_tokenizer == 'NLTK - Tok-tok Tokenizer':
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca.[', '4', ']', '[', '5', ']']
        elif word_tokenizer == 'spaCy - English Word Tokenizer':
            assert tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca.[4][5', ']']
    elif lang == 'fin':
        assert tokens == ['Suomen', 'kieli', '(', 'suomi', ')', 'on', 'uralilaisten', 'kielten', 'itämerensuomalaiseen', 'ryhmään', 'kuuluva', 'kieli', '.']
    elif lang == 'fra':
        assert tokens == ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', '.']
    elif lang == 'deu':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'syntok - Word Tokenizer']:
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw', '.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abgekürzt', 'dt', '.', 'oder', 'dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
        elif word_tokenizer == ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer',
                                'NLTK - Tok-tok Tokenizer']:
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abgekürzt', 'dt.', 'oder', 'dtsch.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
        elif word_tokenizer == 'German / NLTK - Twitter Tokenizer':
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw', '.', 'Deutsch', '(', '[', 'dɔʏ', '̯', 't', '͡', 'ʃ', '];', 'abgekürzt', 'dt', '.', 'oder', 'dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
        elif word_tokenizer == 'Sacremoses - Moses Tokenizer':
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ', '̯', 't', '͡', 'ʃ', ']', ';', 'abgekürzt', 'dt.', 'oder', 'dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
        elif word_tokenizer == 'spaCy - German Word Tokenizer':
            assert tokens == ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abgekürzt', 'dt', '.', 'oder', 'dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
    elif lang == 'ell':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer',
                              'Sacremoses - Moses Tokenizer']:
            assert tokens == ['Η', 'ελληνική', 'γλώσσα', 'ανήκει', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια', '[', '9', ']', 'και', 'συγκεκριμένα', 'στον', 'ελληνικό', 'κλάδο', ',', 'μαζί', 'με', 'την', 'τσακωνική', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδος', 'και', 'της', 'Κύπρου', '.']
        elif word_tokenizer == 'spaCy - Greek (Modern) Word Tokenizer':
            assert tokens == ['Η', 'ελληνική', 'γλώσσα', 'ανήκει', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια[9', ']', 'και', 'συγκεκριμένα', 'στον', 'ελληνικό', 'κλάδο', ',', 'μαζί', 'με', 'την', 'τσακωνική', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδος', 'και', 'της', 'Κύπρου', '.']
    elif lang == 'heb':
        assert tokens == ['עִבְרִית', 'היא', 'שפה', 'שמית', ',', 'ממשפחת', 'השפות', 'האפרו', '-', 'אסיאתיות', ',', 'הידועה', 'כשפתם', 'של', 'היהודים', 'ושל', 'השומרונים', ',', 'אשר', 'ניב', 'מודרני', 'שלה', '(', 'עברית', 'ישראלית', ')', 'הוא', 'שפתה', 'הרשמית', 'של', 'מדינת', 'ישראל', ',', 'מעמד', 'שעוגן', 'בשנת', '2018', 'בחוק', 'יסוד', ':', 'ישראל', '–', 'מדינת', 'הלאום', 'של', 'העם', 'היהודי', '.']
    elif lang == 'hin':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['हिन्दी', 'विश्व', 'की', 'एक', 'प्रमुख', 'भाषा', 'है', 'एवं', 'भारत', 'की', 'राजभाषा', 'है।']
        elif word_tokenizer == ['NLTK - Twitter Tokenizer',
                                'spaCy - Hindi Word Tokenizer']:
            assert tokens == ['हिन्दी', 'विश्व', 'की', 'एक', 'प्रमुख', 'भाषा', 'है', 'एवं', 'भारत', 'की', 'राजभाषा', 'है', '।']
    elif lang == 'hun':
        assert tokens == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tagja', ',', 'a', 'finnugor', 'nyelvek', 'közé', 'tartozó', 'ugor', 'nyelvek', 'egyike', '.']
    elif lang == 'isl':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - Twitter Tokenizer',
                              'Sacremoses - Moses Tokenizer']:
            assert tokens == ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga', '.', '[', '4', ']']
        elif word_tokenizer == ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga.', '[', '4', ']']
        elif word_tokenizer == 'spaCy - Icelandic Word Tokenizer':
            assert tokens == ['Íslenska', 'er', 'vesturnorrænt', ',', 'germanskt', 'og', 'indóevrópskt', 'tungumál', 'sem', 'er', 'einkum', 'talað', 'og', 'ritað', 'á', 'Íslandi', 'og', 'er', 'móðurmál', 'langflestra', 'Íslendinga.[4', ']']
    elif lang == 'ind':
        assert tokens == ['Bahasa', 'Indonesia', 'adalah', 'bahasa', 'Melayu', 'baku', 'yang', 'dijadikan', 'sebagai', 'bahasa', 'resmi', 'Republik', 'Indonesia[1', ']', 'dan', 'bahasa', 'persatuan', 'bangsa', 'Indonesia.[2', ']']
    elif lang == 'gle':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Is', 'ceann', 'de', 'na', 'teangacha', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'dtrí', 'cinn', 'de', 'theangacha', 'Ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'Gaelacha', '(', '.', 'i', '.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'háirithe', '.']
        elif word_tokenizer in ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer',
                                'Sacremoses - Moses Tokenizer',
                                'spaCy - Irish Word Tokenizer']:
            assert tokens == ['Is', 'ceann', 'de', 'na', 'teangacha', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'dtrí', 'cinn', 'de', 'theangacha', 'Ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'Gaelacha', '(', '.i.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'háirithe', '.']
    elif lang == 'ita':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ["L'italiano", '(', '[', 'itaˈljaːno', ']', '[', 'Nota', '1', ']', 'ascolta', '[', '?', '·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
        elif word_tokenizer == 'NLTK - Twitter Tokenizer':
            assert tokens == ["L'italiano", '(', '[', 'itaˈljaːno', ']', '[', 'Nota', '1', ']', 'ascolta', '[', '?', '·', 'info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
        elif word_tokenizer == 'Sacremoses - Moses Tokenizer':
            assert tokens == ["L'", 'italiano', '(', '[', 'itaˈljaːno', ']', '[', 'Nota', '1', ']', 'ascolta', '[', '?', '·', 'info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
        elif word_tokenizer == 'spaCy - Italian Word Tokenizer':
            assert tokens == ["L'", 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
    elif lang == 'jpn':
        if word_tokenizer == 'nagisa - Japanese Word Tokenizer':
            assert tokens == ['日本', '語', '(', 'にほんご', '、', 'にっぽん', 'ご', '[', '注', '1', ']', ')', 'は', '、', '主に', '日本', '国', '内', 'や', '日本', '人', '同士', 'の', '間', 'で', '使用', 'さ', 'れ', 'て', 'いる', '言語', 'で', 'ある', '。']
        elif word_tokenizer == 'Wordless - Japanese Kanji Tokenizer':
            assert tokens == ['日', '本', '語', '（', 'にほんご', '、', 'にっぽん', 'ご', '[', '注', '1', ']', '）', 'は', '、', '主', 'に', '日', '本', '国', '内', 'や', '日', '本', '人', '同', '士', 'の', '間', 'で', '使', '用', 'さ', 'れ', 'て', 'いる', '言', '語', 'で', 'ある', '。']
    elif lang == 'kan':
        assert tokens == ['ದ್ರಾವಿಡ', 'ಭಾಷೆಗಳಲ್ಲಿ', 'ಪ್ರಾಮುಖ್ಯವುಳ್ಳ', 'ಭಾಷೆಯೂ', 'ಭಾರತದ', 'ಪುರಾತನವಾದ', 'ಭಾಷೆಗಳಲ್ಲಿ', 'ಒಂದೂ', 'ಆಗಿರುವ', 'ಕನ್ನಡ', 'ಭಾಷೆಯನ್ನು', 'ಅದರ', 'ವಿವಿಧ', 'ರೂಪಗಳಲ್ಲಿ', 'ಸುಮಾರು', '೪೫', 'ದಶಲಕ್ಷ', 'ಜನರು', 'ಆಡು', 'ನುಡಿಯಾಗಿ', 'ಬಳಸುತ್ತಲಿದ್ದಾರೆ', '.']
    elif lang == 'lav':
        if word_tokenizer == ['NLTK - NIST Tokenizer',
                              'NLTK - Twitter Tokenizer',
                              'Sacremoses - Moses Tokenizer']:
            assert tokens == ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,7', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda', '.', '[', '3', ']']
        elif word_tokenizer == ['NLTK - NLTK Tokenizer',
                                'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['Latviešu', 'valoda', 'ir', 'dzimtā', 'valoda', 'apmēram', '1,7', 'miljoniem', 'cilvēku', ',', 'galvenokārt', 'Latvijā', ',', 'kur', 'tā', 'ir', 'vienīgā', 'valsts', 'valoda.', '[', '3', ']']
    elif lang == 'lit':
        assert tokens == ['Lietuvių', 'kalba', '–', 'iš', 'baltų', 'prokalbės', 'kilusi', 'lietuvių', 'tautos', 'kalba', ',', 'kuri', 'Lietuvoje', 'yra', 'valstybinė', ',', 'o', 'Europos', 'Sąjungoje', '–', 'viena', 'iš', 'oficialiųjų', 'kalbų', '.']
    elif lang == 'ltz':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ["D'Lëtzebuergesch", 'gëtt', 'an', 'der', 'däitscher', 'Dialektologie', 'als', 'ee', 'westgermaneschen', ',', 'mëtteldäitschen', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéiert', '.']
        elif word_tokenizer == 'spaCy - Luxembourgish Word Tokenizer':
            assert tokens == ["D'", 'Lëtzebuergesch', 'gëtt', 'an', 'der', 'däitscher', 'Dialektologie', 'als', 'ee', 'westgermaneschen', ',', 'mëtteldäitschen', 'Dialekt', 'aklasséiert', ',', 'deen', 'zum', 'Muselfränkesche', 'gehéiert', '.']
    elif lang == 'mar':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['मराठीभाषा', 'ही', 'इंडो-युरोपीय', 'भाषाकुलातील', 'एक', 'भाषा', 'आहे', '.']
        elif word_tokenizer == 'spaCy - Marathi Word Tokenizer':
            assert tokens == ['मराठीभाषा', 'ही', 'इंडो', '-', 'युरोपीय', 'भाषाकुलातील', 'एक', 'भाषा', 'आहे', '.']
    elif lang == 'nob':
        assert tokens == ['Bokmål', 'er', 'en', 'varietet', 'av', 'norsk', 'språk', '.']
    elif lang == 'fas':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران،', 'افغانستان،', '[', '۳', ']', 'تاجیکستان', '[', '۴', ']', 'و', 'ازبکستان', '[', '۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif word_tokenizer == 'NLTK - Tok-tok Tokenizer':
            assert tokens == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', '[', '۳', ']', 'تاجیکستان[', '۴', ']', 'و', 'ازبکستان[', '۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif word_tokenizer == 'NLTK - Twitter Tokenizer':
            assert tokens == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', '[', '۳', ']', 'تاجیکستان', '[', '۴', ']', 'و', 'ازبکستان', '[', '۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
        elif word_tokenizer == 'spaCy - Persian Word Tokenizer':
            assert tokens == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'و', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
    elif lang == 'pol':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Język', 'polski', ',', 'polszczyzna', ',', 'skrót', ':', 'pol', '.', '–', 'język', 'naturalny', 'należący', 'do', 'grupy', 'języków', 'zachodniosłowiańskich', '(', 'do', 'której', 'należą', 'również', 'czeski', ',', 'słowacki', ',', 'kaszubski', ',', 'dolnołużycki', ',', 'górnołużycki', 'i', 'wymarły', 'połabski', ')', ',', 'stanowiącej', 'część', 'rodziny', 'języków', 'indoeuropejskich', '.']
        elif word_tokenizer in ['Sacremoses - Moses Tokenizer',
                                'spaCy - Polish Word Tokenizer']:
            assert tokens == ['Język', 'polski', ',', 'polszczyzna', ',', 'skrót', ':', 'pol.', '–', 'język', 'naturalny', 'należący', 'do', 'grupy', 'języków', 'zachodniosłowiańskich', '(', 'do', 'której', 'należą', 'również', 'czeski', ',', 'słowacki', ',', 'kaszubski', ',', 'dolnołużycki', ',', 'górnołużycki', 'i', 'wymarły', 'połabski', ')', ',', 'stanowiącej', 'część', 'rodziny', 'języków', 'indoeuropejskich', '.']
    elif lang == 'por':
        assert tokens == ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego-português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.']
    elif lang == 'ron':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer',
                              'Sacremoses - Moses Tokenizer']:
            assert tokens == ['Limba', 'română', 'este', 'o', 'limbă', 'indo-europeană', ',', 'din', 'grupul', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbilor', 'romanice', '.']
        elif word_tokenizer == 'spaCy - Romanian Word Tokenizer':
            assert tokens == ['Limba', 'română', 'este', 'o', 'limbă', 'indo', '-', 'europeană', ',', 'din', 'grupul', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbilor', 'romanice', '.']
    elif lang == 'rus':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Tok-tok Tokenizer',
                              'NLTK - Twitter Tokenizer',
                              'razdel - Russian Word Tokenizer']:
            assert tokens == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
        elif word_tokenizer == 'Sacremoses - Moses Tokenizer':
            assert tokens == ['Ру', '́', 'сский', 'язы', '́', 'к', '(', '[', 'ˈruskʲɪi', '̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
        elif word_tokenizer == 'spaCy - Russian Word Tokenizer':
            assert tokens == ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать)[~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
    elif lang == 'srp_cyrl':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Српски', 'језик', 'припада', 'словенској', 'групи', 'језика', 'породице', 'индоевропских', 'језика', '.', '[', '12', ']']
        elif word_tokenizer == 'spaCy - Serbian Word Tokenizer':
            assert tokens == ['Српски', 'језик', 'припада', 'словенској', 'групи', 'језика', 'породице', 'индоевропских', 'језика.[12', ']']
    elif lang == 'srp_latn':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Srpski', 'jezik', 'pripada', 'slovenskoj', 'grupi', 'jezika', 'porodice', 'indoevropskih', 'jezika', '.', '[', '12', ']']
        elif word_tokenizer == 'spaCy - Serbian Word Tokenizer':
            assert tokens == ['Srpski', 'jezik', 'pripada', 'slovenskoj', 'grupi', 'jezika', 'porodice', 'indoevropskih', 'jezika.[12', ']']
    elif lang == 'sin':
        assert tokens == ['ශ්\u200dරී', 'ලංකාවේ', 'ප්\u200dරධාන', 'ජාතිය', 'වන', 'සිංහල', 'ජනයාගේ', 'මව්', 'බස', 'සිංහල', 'වෙයි', '.']
    elif lang == 'slk':
        assert tokens == ['Slovenčina', 'patrí', 'do', 'skupiny', 'západoslovanských', 'jazykov', '(', 'spolu', 's', 'češtinou', ',', 'poľštinou', ',', 'hornou', 'a', 'dolnou', 'lužickou', 'srbčinou', 'a', 'kašubčinou', ')', '.']
    elif lang == 'slv':
        assert tokens == ['Slovenščina', '[', 'slovénščina', ']', '/', '[', 'sloˈʋenʃtʃina', ']', 'je', 'združeni', 'naziv', 'za', 'uradni', 'knjižni', 'jezik', 'Slovencev', 'in', 'skupno', 'ime', 'za', 'narečja', 'in', 'govore', ',', 'ki', 'jih', 'govorijo', 'ali', 'so', 'jih', 'nekoč', 'govorili', 'Slovenci', '.']
    elif lang == 'spa':
        assert tokens == ['El', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', '.']
    elif lang == 'swe':
        assert tokens == ['Svenska', '(', 'svenska', '(', 'info', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'ungefär', 'tio', 'miljoner', 'personer', 'främst', 'i', 'Sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'Finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'Åland', '.']
    elif lang == 'tgl':
        assert tokens == ['Ang', 'Wikang', 'Tagalog[2', ']', '(', 'Baybayin', ':', 'ᜏᜒᜃᜅ᜔', 'ᜆᜄᜎᜓᜄ᜔', ')', ',', 'na', 'kilala', 'rin', 'sa', 'payak', 'na', 'pangalang', 'Tagalog', ',', 'ay', 'isa', 'sa', 'mga', 'pangunahing', 'wika', 'ng', 'Pilipinas', 'at', 'sinasabing', 'ito', 'ang', 'de', 'facto', '(', '"', 'sa', 'katunayan', '"', ')', 'ngunit', 'hindî', 'de', 'jure', '(', '"', 'sa', 'batas', '"', ')', 'na', 'batayan', 'na', 'siyang', 'pambansang', 'Wikang', 'Filipino', '(', 'mula', '1961', 'hanggang', '1987', ':', 'Pilipino).[2', ']']
    elif lang == 'tgk':
        assert tokens == ['Забони', 'тоҷикӣ', '—', 'забоне', ',', 'ки', 'дар', 'Эрон', ':', 'форсӣ', ',', 'ва', 'дар', 'Афғонистон', 'дарӣ', 'номида', 'мешавад', ',', 'забони', 'давлатии', 'кишварҳои', 'Тоҷикистон', ',', 'Эрон', 'ва', 'Афғонистон', 'мебошад', '.']
    elif lang == 'tam':
        if word_tokenizer == 'Sacremoses - Moses Tokenizer':
            assert tokens == ['தமிழ', '்', 'மொழி', '(', 'Tamil', 'language', ')', 'தமிழர', '்', 'களினதும', '்', ',', 'தமிழ', '்', 'பேசும', '்', 'பலரதும', '்', 'தாய', '்', 'மொழி', 'ஆகும', '்', '.']
        elif word_tokenizer == 'spaCy - Tamil Word Tokenizer':
            assert tokens == ['தமிழ்', 'மொழி', '(', 'Tamil', 'language', ')', 'தமிழர்களினதும்', ',', 'தமிழ்', 'பேசும்', 'பலரதும்', 'தாய்மொழி', 'ஆகும்', '.']
    elif lang == 'tat':
        assert tokens == ['Татар', 'теле', '—', 'татарларның', 'милли', 'теле', ',', 'Татарстанның', 'дәүләт', 'теле', ',', 'таралышы', 'буенча', 'Русиядә', 'икенче', 'тел', '.']
    elif lang == 'tel':
        tokens == ['ఆంధ్ర', 'ప్రదేశ్', ',', 'తెలంగాణ', 'రాష్ట్రాల', 'అధికార', 'భాష', 'తెలుగు', '.']
    elif lang == 'tha':
        if word_tokenizer in ['PyThaiNLP - Longest Matching',
                              'PyThaiNLP - Maximum Matching + TCC',
                              'PyThaiNLP - Maximum Matching + TCC (Safe Mode)']:
            assert tokens == ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย']
        elif word_tokenizer == 'PyThaiNLP - Maximum Matching':
            assert tokens == ['ภาษาไทย', 'หรือ', 'ภาษาไทยกลาง', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศ', 'ไทย']
    elif lang == 'bod':
        assert tokens == ['བོད་', 'ཀྱི་', 'སྐད་ཡིག་', 'ནི་', 'བོད་ཡུལ་', 'དང་', 'དེ', 'འི་', 'ཉེ་འཁོར་', 'གྱི་', 'ས་ཁུལ་', 'ཏེ', '།']
    elif lang == 'tur':
        assert tokens == ['Türkçe', 'ya', 'da', 'Türk', 'dili', ',', 'batıda', 'Balkanlar’dan', 'başlayıp', 'doğuda', 'Hazar', 'Denizi', 'sahasına', 'kadar', 'konuşulan', 'Türkî', 'diller', 'dil', 'ailesine', 'ait', 'sondan', 'eklemeli', 'bir', 'dil.[12', ']']
    elif lang == 'ukr':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer',
                              'NLTK - Twitter Tokenizer']:
            assert tokens == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичні', 'назви', '—', 'ру́ська', ',', 'руси́нська', '[', '9', ']', '[', '10', ']', '[', '11', ']', '[', '*', '2', ']', ')', '—', 'національна', 'мова', 'українців', '.']
        elif word_tokenizer == 'spaCy - Ukrainian Word Tokenizer':
            assert tokens == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичні', 'назви', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національна', 'мова', 'українців', '.']
    elif lang == 'urd':
        if word_tokenizer in ['NLTK - NIST Tokenizer',
                              'NLTK - NLTK Tokenizer',
                              'NLTK - Penn Treebank Tokenizer']:
            assert tokens == ['اُردُو', 'لشکری', 'زبان', '[', '8', ']', '(', 'یا', 'جدید', 'معیاری', 'اردو', ')', 'برصغیر', 'کی', 'معیاری', 'زبانوں', 'میں', 'سے', 'ایک', 'ہے۔']
        elif word_tokenizer == 'NLTK - Twitter Tokenizer':
            assert tokens == ['اُردُو', 'لشکری', 'زبان', '[8', ']', '(', 'یا', 'جدید', 'معیاری', 'اردو', ')', 'برصغیر', 'کی', 'معیاری', 'زبانوں', 'میں', 'سے', 'ایک', 'ہے', '۔']
        elif word_tokenizer == 'spaCy - Ukrainian Word Tokenizer':
            assert tokens == ['اُردُو', 'لشکری', 'زبان[8', ']', '(', 'یا', 'جدید', 'معیاری', 'اردو', ')', 'برصغیر', 'کی', 'معیاری', 'زبانوں', 'میں', 'سے', 'ایک', 'ہے', '۔']
    elif lang == 'vie':
        if word_tokenizer == 'NLTK - Tok-tok Tokenizer':
            assert tokens == ['Tiếng', 'Việt', ',', 'còn', 'gọi', 'tiếng', 'Việt', 'Nam[', '5', ']', ',', 'tiếng', 'Kinh', 'hay', 'Việt', 'ngữ', ',', 'là', 'ngôn', 'ngữ', 'của', 'người', 'Việt', '(', 'dân', 'tộc', 'Kinh', ')', 'và', 'là', 'ngôn', 'ngữ', 'chính', 'thức', 'tại', 'Việt', 'Nam', '.']
        elif word_tokenizer == 'Underthesea - Vietnamese Word Tokenizer':
            assert tokens == ['Tiếng', 'Việt', ',', 'còn', 'gọi', 'tiếng', 'Việt Nam', '[', '5', ']', ',', 'tiếng Kinh', 'hay', 'Việt ngữ', ',', 'là', 'ngôn ngữ', 'của', 'người', 'Việt', '(', 'dân tộc', 'Kinh', ')', 'và', 'là', 'ngôn ngữ', 'chính thức', 'tại', 'Việt Nam', '.']

if __name__ == '__main__':
    for lang, word_tokenizer in test_word_tokenizers:
        test_word_tokenize(lang, word_tokenizer, show_results = True)
