# -*- coding: utf-8 -*-

#
# Wordless: Tests - Text - Text Processing - Word Detokenization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

import pytest

from wordless_tests import test_init
from wordless_text import wordless_text_processing
from wordless_utils import wordless_conversion

WORD_DETOKENIZERS = []

SENTENCE_CAT = "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l'Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada a Catalunya, el País Valencià (tret d'algunes comarques i localitats de l'interior), les Illes Balears, Andorra, la Franja de Ponent (a l'Aragó), la ciutat de l'Alguer (a l'illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l'Argentina, amb 195.000 parlants).[11]"
SENTENCE_ZHO_CN = '汉语，又称汉文、中文、中国话、中国语、华语、华文、唐话[2]，或被视为一个语族，或被视为隶属于汉藏语系汉语族之一种语言。'
SENTENCE_ZHO_TW = '漢語，又稱漢文、中文、中國話、中國語、華語、華文、唐話[2]，或被視為一個語族，或被視為隸屬於漢藏語系漢語族之一種語言。'
SENTENCE_CES = 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
SENTENCE_NLD = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
SENTENCE_ENG = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[5][6]'
SENTENCE_FIN = 'Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli.'
SENTENCE_FRA = 'Le français est une langue indo-européenne de la famille des langues romanes.'
SENTENCE_DEU = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt dt. oder dtsch.) ist eine westgermanische Sprache.'
SENTENCE_ELL = 'Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και συγκεκριμένα στον ελληνικό κλάδο, μαζί με την τσακωνική, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
SENTENCE_HUN = 'A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.'
SENTENCE_ISL = 'Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[4]'
SENTENCE_GLE = 'Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann den dtrí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (.i. an Ghaeilge, Gaeilge na hAlban agus Gaeilge Mhanann) go háirithe.'
SENTENCE_ITA = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
SENTENCE_JPN = '日本語（にほんご、にっぽんご[注 1]）は、主に日本国内や日本人同士の間で使用されている言語である。'
SENTENCE_LAV = 'Latviešu valoda ir dzimtā valoda apmēram 1,7 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda.[3]'
SENTENCE_LIT = 'Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba, kuri Lietuvoje yra valstybinė, o Europos Sąjungoje – viena iš oficialiųjų kalbų.'
SENTENCE_POL = 'Język polski, polszczyzna, skrót: pol. – język naturalny należący do grupy języków zachodniosłowiańskich (do której należą również czeski, słowacki, kaszubski, dolnołużycki, górnołużycki i wymarły połabski), stanowiącej część rodziny języków indoeuropejskich.'
SENTENCE_POR = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
SENTENCE_RON = 'Limba română este o limbă indo-europeană, din grupul italic și din subgrupul oriental al limbilor romanice.'
SENTENCE_RUS = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
SENTENCE_SLK = 'Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).'
SENTENCE_SLV = 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.'
SENTENCE_SPA = 'El español o castellano es una lengua romance procedente del latín hablado.'
SENTENCE_SWE = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
SENTENCE_TAM = 'தமிழ் மொழி (Tamil language) தமிழர்களினதும், தமிழ் பேசும் பலரதும் தாய்மொழி ஆகும்.'
SENTENCE_THA = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
SENTENCE_BOD = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

main = test_init.Test_Main()

for lang, word_detokenizers in main.settings_global['word_detokenizers'].items():
    for word_detokenizer in word_detokenizers:
        # Temporarily disable testing of pybo's word tokenizers due to memory issues
        if lang not in ['bod', 'other']:
            WORD_DETOKENIZERS.append((lang, word_detokenizer))

@pytest.mark.parametrize('lang, word_detokenizer', WORD_DETOKENIZERS)
def test_word_detokenize(lang, word_detokenizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    tokens = wordless_text_processing.wordless_word_tokenize(main, globals()[f'SENTENCE_{lang.upper()}'],
                                                             lang = lang)

    text = wordless_text_processing.wordless_word_detokenize(main, tokens,
                                                             lang = lang,
                                                             word_detokenizer = word_detokenizer)

    # print(text)

    if lang == 'cat':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l' Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada a Catalunya, el País Valencià (tret d' algunes comarques i localitats de l' interior), les Illes Balears, Andorra, la Franja de Ponent (a l' Aragó), la ciutat de l' Alguer (a l' illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l' Argentina, amb 195.000 parlants).[11 ]"
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l' Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada a Catalunya, el País Valencià (tret d' algunes comarques i localitats de l' interior), les Illes Balears, Andorra, la Franja de Ponent (a l' Aragó), la ciutat de l' Alguer (a l' illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l' Argentina, amb 195.000 parlants).[11]"
    elif lang == 'zho_cn':
        assert text == '汉语，又称汉文、中文、中国话、中国语、华语、华文、唐话[2]，或被视为一个语族，或被视为隶属于汉藏语系汉语族之一种语言。'
    elif lang == 'zho_tw':
        assert text == '漢語，又稱漢文、中文、中國話、中國語、華語、華文、唐話[2]，或被視為一個語族，或被視為隸屬於漢藏語系漢語族之一種語言。'
    elif lang == 'ces':
        assert text == 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
    elif lang == 'nld':
        assert text == 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
    elif lang == 'eng':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[5][6 ]'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[5][6]'
    elif lang == 'fin':
        assert text == 'Suomen kieli (suomi) on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli.'
    elif lang == 'fra':
        assert text == 'Le français est une langue indo-européenne de la famille des langues romanes.'
    elif lang == 'deu':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'Die deutsche Sprache bzw. Deutsch ([ dɔʏ̯t͡ʃ]; abgekürzt dt . oder dtsch .) ist eine westgermanische Sprache.'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt dt. oder dtsch.) ist eine westgermanische Sprache.'
    elif lang == 'ell':
        assert text == 'Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και συγκεκριμένα στον ελληνικό κλάδο, μαζί με την τσακωνική, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
    elif lang == 'hun':
        assert text == 'A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.'
    elif lang == 'isl':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[4 ]'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'Íslenska er vesturnorrænt, germanskt og indóevrópskt tungumál sem er einkum talað og ritað á Íslandi og er móðurmál langflestra Íslendinga.[4]'
    elif lang == 'gle':
        assert text == 'Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann den dtrí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (.i. an Ghaeilge, Gaeilge na hAlban agus Gaeilge Mhanann) go háirithe.'
    elif lang == 'ita':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == "L' italiano ([ itaˈljaːno][Nota 1] ascolta[?·info] ) è una lingua romanza parlata principalmente in Italia."
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
    elif lang == 'jpn':
        assert text == '日本語(にほんご、にっぽんご[注1])は、主に日本国内や日本人同士の間で使用されている言語である。'
    elif lang == 'lav':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'Latviešu valoda ir dzimtā valoda apmēram 1,7 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda . [3 ]'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'Latviešu valoda ir dzimtā valoda apmēram 1,7 miljoniem cilvēku, galvenokārt Latvijā, kur tā ir vienīgā valsts valoda. [3]'
    elif lang == 'lit':
        assert text == 'Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba, kuri Lietuvoje yra valstybinė, o Europos Sąjungoje – viena iš oficialiųjų kalbų.'
    elif lang == 'pol':
        assert text == 'Język polski, polszczyzna, skrót: pol. – język naturalny należący do grupy języków zachodniosłowiańskich (do której należą również czeski, słowacki, kaszubski, dolnołużycki, górnołużycki i wymarły połabski), stanowiącej część rodziny języków indoeuropejskich.'
    elif lang == 'por':
        assert text == 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
    elif lang == 'ron':
        assert text == 'Limba română este o limbă indo - europeană, din grupul italic și din subgrupul oriental al limbilor romanice.'
    elif lang == 'rus':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'Ру́сский язы́к ([ ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать) [~ 3] [⇨] — один из восточнославянских языков, национальный язык русского народа.'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать) [~ 3] [⇨] — один из восточнославянских языков, национальный язык русского народа.'
    elif lang == 'slk':
        assert text == 'Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).'
    elif lang == 'slv':
        assert text == 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.'
    elif lang == 'spa':
        assert text == 'El español o castellano es una lengua romance procedente del latín hablado.'
    elif lang == 'swe':
        if word_detokenizer == 'NLTK - Penn Treebank Detokenizer':
            assert text == 'Svenska (svenska (info) ) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
        elif word_detokenizer == 'Sacremoses - Moses Detokenizer':
            assert text == 'Svenska (svenska (info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
    elif lang == 'tam':
        assert text == 'தமிழ் மொழி (Tamil language) தமிழர்களினதும், தமிழ் பேசும் பலரதும் தாய்மொழி ஆகும்.'
    elif lang == 'tha':
        assert text == 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
    elif lang == 'bod':
        assert text == '༄༅། །རྒྱ་གར་སྐད་དུ།བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར།བོད་སྐད་དུ།བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'

'''
for lang, word_detokenizers in main.settings_global['word_detokenizers'].items():
    for word_detokenizer in word_detokenizers:
        if lang not in ['bod', 'other']:
            test_word_detokenize(lang, word_detokenizer)
'''
