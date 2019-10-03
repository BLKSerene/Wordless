#
# Wordless: Tests - Text - Text Processing - Lemmatization
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

LEMMATIZERS = []

SENTENCE_AST = "L'asturianu ye una llingua romance propia d'Asturies,[1] perteneciente al subgrupu asturllionés."
SENTENCE_BUL = 'Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици.'
SENTENCE_CAT = "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l'Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada a Catalunya, el País Valencià (tret d'algunes comarques i localitats de l'interior), les Illes Balears, Andorra, la Franja de Ponent (a l'Aragó), la ciutat de l'Alguer (a l'illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l'Argentina, amb 195.000 parlants).[11]"
SENTENCE_CES = 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
SENTENCE_NLD = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
SENTENCE_ENG = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[5][6]'
SENTENCE_EST = 'Eesti keel (varasem nimetus: maakeel) on läänemeresoome lõunarühma kuuluv keel.'
SENTENCE_FRA = 'Le français est une langue indo-européenne de la famille des langues romanes.'
SENTENCE_GLG = 'O galego ([ɡaˈleɣo̝]) é unha lingua indoeuropea que pertence á póla de linguas románicas.'
SENTENCE_DEU = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt dt. oder dtsch.) ist eine westgermanische Sprache.'
SENTENCE_GRC = 'Με τον όρο αρχαία ελληνική γλώσσα εννοείται μια μορφή της ελληνικής γλώσσας, που ομιλούνταν κατά τους αρχαϊκούς χρόνους και την κλασική αρχαιότητα.'
SENTENCE_ELL = 'Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] και συγκεκριμένα στον ελληνικό κλάδο, μαζί με την τσακωνική, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
SENTENCE_HUN = 'A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.'
SENTENCE_GLE = 'Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann den dtrí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (.i. an Ghaeilge, Gaeilge na hAlban agus Gaeilge Mhanann) go háirithe.'
SENTENCE_ITA = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
SENTENCE_GLV = 'She Gaelg (graït: /gɪlg/) çhengey Ghaelagh Vannin.'
SENTENCE_FAS = 'فارسی یا پارسی یکی از زبان‌های هندواروپایی در شاخهٔ زبان‌های ایرانی جنوب غربی است که در کشورهای ایران، افغانستان،[۳] تاجیکستان[۴] و ازبکستان[۵] به آن سخن می‌گویند.'
SENTENCE_POR = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
SENTENCE_RON = 'Limba română este o limbă indo-europeană, din grupul italic și din subgrupul oriental al limbilor romanice.'
SENTENCE_RUS = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
SENTENCE_GLA = "'S i cànan dùthchasach na h-Alba a th' anns a' Ghàidhlig."
SENTENCE_SLK = 'Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).'
SENTENCE_SLV = 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.'
SENTENCE_SPA = 'El español o castellano es una lengua romance procedente del latín hablado.'
SENTENCE_SWE = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av ungefär tio miljoner personer främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
SENTENCE_BOD = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
SENTENCE_UKR = 'Украї́нська мо́ва (МФА: [ukrɑ̽ˈjɪnʲsʲkɑ̽ ˈmɔwɑ̽], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
SENTENCE_CYM = "Aelod o'r gangen Frythonaidd o'r ieithoedd Celtaidd a siaredir yn frodorol yng Nghymru, gan Gymry a phobl eraill ar wasgar yn Lloegr, a chan gymuned fechan yn Y Wladfa, yr Ariannin[7] yw'r Gymraeg (hefyd Cymraeg heb y fannod)."

main = test_init.Test_Main()

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        # Temporarily disable testing of pybo's lemmatizer due to memory issues
        if lang != 'bod':
            LEMMATIZERS.append((lang, lemmatizer))

@pytest.mark.parametrize('lang, lemmatizer', LEMMATIZERS)
def test_lemmatize(lang, lemmatizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    tokens = wordless_text_processing.wordless_word_tokenize(main, globals()[f'SENTENCE_{lang.upper()}'],
                                                             lang = lang)

    lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                         lang = lang,
                                                         lemmatizer = lemmatizer)

    # print(lemmas)

    if lang == 'ast':
        assert lemmas == ["L'asturianu", 'ser', 'unu', 'llingua', 'romance', 'propiu', "d'Asturies,[1", ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
    elif lang == 'bul':
        assert lemmas == ['Бъ̀лгарският', 'езѝк', 'съм', 'индоевропейски', 'език', 'от', 'група', 'на', 'южнославянските', 'език', '.']
    elif lang == 'cat':
        assert lemmas == ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'ell', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'ell', 'ciutat', 'de', 'ell', 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'ser', 'un', 'llengua', 'romànic', 'parlar', 'a', 'Catalunya', ',', 'ell', 'País', 'Valencià', '(', 'treure', 'de', 'algun', 'comarca', 'i', 'localitat', 'de', 'ell', 'interior', ')', ',', 'ell', 'Illes', 'Balears', ',', 'Andorra', ',', 'ell', 'Franja', 'de', 'Ponent', '(', 'a', 'ell', 'Aragó', ')', ',', 'ell', 'ciutat', 'de', 'ell', 'Alguer', '(', 'a', 'ell', 'illa', 'de', 'Sardenya', ')', ',', 'ell', 'Catalunya', 'del', 'Nord,[8', ']', 'ell', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblar', 'per', 'immigrar', 'valencians),[9][10', ']', 'i', 'en', 'petita', 'comunitat', 'arreu', 'del', 'món', '(', 'entrar', 'ell', 'qual', 'destacar', 'ell', 'de', 'ell', 'Argentina', ',', 'amb', '195.000', 'parlants).[11', ']']
    elif lang == 'ces':
        assert lemmas == ['Čeština', 'neboli', 'český', 'jazyk', 'on', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
    elif lang == 'nld':
        assert lemmas == ['het', 'nederlands', 'is', 'een', 'west-germaanse', 'taal', 'en', 'de', 'moedertaal', 'van', 'de', 'meeste', 'inwoners', 'van', 'nederland', ',', 'belgië', 'en', 'suriname', '.']
    elif lang == 'eng':
        if lemmatizer == 'Lemmatization Lists - English Lemma List':
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'that', 'be', '1', 'speak', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'become', 'a', 'global', 'lingua', 'franca.[5][6', ']']
        elif lemmatizer in ['NLTK - WordNet Lemmatizer',
                            'spaCy - English Lemmatizer']:
            assert lemmas == ['English', 'be', 'a', 'West', 'Germanic', 'language', 'that', 'be', 'first', 'speak', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'become', 'a', 'global', 'lingua', 'franca.[5][6', ']']
    elif lang == 'est':
        assert lemmas == ['Eesti', 'kee', '(', 'varasem', 'nimetu', ':', 'maakeel', ')', 'olema', 'läänemeresoome', 'lõunarühma', 'kuuluma', 'kee', '.']
    elif lang == 'fra':
        if lemmatizer == 'Lemmatization Lists - French Lemma List':
            assert lemmas == ['Le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'un', 'langue', 'roman', '.']
        elif lemmatizer == 'spaCy - French Lemmatizer':
            assert lemmas == ['le', 'français', 'être', 'un', 'langue', 'indo-européenne', 'de', 'le', 'famille', 'un', 'langue', 'roman', '.']
    elif lang == 'glg':
        assert lemmas == ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'á', 'póla', 'de', 'lingua', 'románico', '.']
    elif lang == 'deu':
        if lemmatizer == 'Lemmatization Lists - German Lemma List':
            assert lemmas == ['Die', 'deutsch', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', '.']
        elif lemmatizer == 'spaCy - German Lemmatizer':
            assert lemmas == ['der', 'deutsch', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abkürzen', 'dt', '.', 'oder', 'dtsch', '.', ')', 'sein', 'einen', 'westgermanische', 'Sprache', '.']
    elif lang == 'grc':
        assert lemmas == ['Με', 'τον', 'όρο', 'αρχαία', 'ελληνική', 'γλώσσα', 'εννοείται', 'μια', 'μορφή', 'της', 'ελληνικής', 'γλώσσας', ',', 'πού', 'ομιλούνταν', 'κατά', 'τους', 'αρχαϊκούς', 'χρόνους', 'και', 'την', 'κλασική', 'αρχαιότητα', '.']
    elif lang == 'ell':
        assert lemmas == ['η', 'ελληνικός', 'γλώσσα', 'ανήκω', 'στην', 'ινδοευρωπαϊκός', 'οικογένεια[9', ']', 'και', 'συγκεκριμένα', 'στον', 'ελληνικό', 'κλάδο', ',', 'μαζί', 'με', 'την', 'τσακωνικός', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδος', 'και', 'της', 'Κύπρου', '.']
    elif lang == 'hun':
        assert lemmas == ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tag', ',', 'a', 'finnugor', 'nyelv', 'köz', 'tartozó', 'ugor', 'nyelv', 'egyik', '.']
    elif lang == 'gle':
        assert lemmas == ['Is', 'ceann', 'de', 'na', 'teangach', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'tabhair', 'ar', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'trí', 'ceann', 'de', 'teangach', 'Ceilteacha', 'air', 'a', 'tabhair', 'na', 'teangach', 'Gaelacha', '(', '.i.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'áirithe', '.']
    elif lang == 'ita':
        assert lemmas == ["L'", 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'essere', 'una', 'lingua', 'romanzo', 'parlato', 'principalmente', 'in', 'Italia', '.']
    elif lang == 'glv':
        assert lemmas == ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Gaelagh', 'Mannin', '.']
    elif lang == 'fas':
        assert lemmas == ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان،[۳', ']', 'تاجیکستان[۴', ']', 'را', 'ازبکستان[۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
    elif lang == 'por':
        assert lemmas == ['A', 'língua', 'portuguesar', ',', 'também', 'designar', 'português', ',', 'ser', 'umar', 'língua', 'românico', 'flexivo', 'ocidental', 'originar', 'o', 'galego-português', 'falar', 'o', 'Reino', 'da', 'Galiza', 'e', 'o', 'norte', 'de', 'Portugal', '.']
    elif lang == 'ron':
        assert lemmas == ['Limba', 'român', 'fi', 'vrea', 'limbă', 'indo', '-', 'european', ',', 'din', 'grup', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbă', 'romanice', '.']
    elif lang == 'rus':
        assert lemmas == ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянский', 'язык', ',', 'национальный', 'язык', 'русский', 'народ', '.']
    elif lang == 'gla':
        assert lemmas == ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'Alba', 'a', 'th', "'", 'anns', 'a', "'", 'Ghàidhlig', '.']
    elif lang == 'slk':
        assert lemmas == ['Slovenčina', 'patriť', 'do', 'skupina', 'západoslovanský', 'jazyk', '(', 'spolu', 's', 'čeština', ',', 'poľština', ',', 'horný', 'as', 'dolný', 'lužickou', 'srbčina', 'as', 'kašubčinou', ')', '.']
    elif lang == 'slv':
        assert lemmas == ['Slovenščina', '[', 'slovénščina', ']', '/', '[', 'sloˈʋenʃtʃina', ']', 'onbiti', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govoriti', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govoriti', 'Slovenec', '.']
    elif lang == 'spa':
        assert lemmas == ['El', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablar', '.']
    elif lang == 'swe':
        assert lemmas == ['Svenska', '(', 'svensk', '(', 'info', ')', ')', 'vara', 'en', 'östnordiskt', 'språka', 'som', 'tala', 'av', 'ungefär', 'tio', 'miljon', 'person', 'främst', 'i', 'Sverige', 'där', 'språk', 'hare', 'man', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'mena', 'även', 'som', 'en', 'en', 'nationalspråk', 'i', 'Finland', 'och', 'som', 'enda', 'officiell', 'språka', 'på', 'Åland', '.']
    elif lang == 'bod':
        assert lemmas == ['༄༅། ། ', 'རྒྱ་གར་', 'སྐད་', 'དུ་', ' ། ', 'བོ་', ' དྷི་', ' སཏྭ་', ' ཙརྻ་', 'ཨ་བ་', 'ཏ་', 'ར་', ' ། ', 'བོད་སྐད་', 'དུ་', ' ། ', 'བྱང་ཆུབ་', 'སེམས་དཔའ་', 'གི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ་', ' ། ། ', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་', 'སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ་', ' ། ། ', 'བདེ་གཤེགས་', 'ཆོ་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲ་', 'བཅའ་', 'དང་', ' ། ། ', 'ཕྱག་འོས་', 'ཀུན་', 'ལ་', 'ཀྱང་', 'གུས་པ་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ཏེ་', ' ། ། ', 'བདེ་གཤེགས་', 'སྲ་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི་', ' ། ། ', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་', 'ན་', 'ནི་', 'བརྗོད་པ་', 'ལ་', 'བྱ་', ' ། །']
    elif lang == 'ukr':
        if lemmatizer == 'Lemmatization Lists - Ukrainian Lemma List':
            assert lemmas == ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назвати', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
        elif lemmatizer == 'pymorphy2 - Morphological Analyzer':
            assert lemmas == ['украї́нський', 'мо́вий', '(', 'мфа', ':', '[', 'ukrɑ̽ˈjɪnʲsʲkɑ̽', 'ˈmɔwɑ̽', ']', ',', 'історичний', 'назва', '—', 'ру́ський', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національний', 'мова', 'українець', '.']
    elif lang == 'cym':
        assert lemmas == ['Aelod', "o'r", 'cangen', 'Frythonaidd', "o'r", 'iaith', 'Celtaidd', 'a', 'siarad', 'bod', 'brodorol', 'yn', 'Nghymru', ',', 'can', 'Gymry', 'a', 'pobl', 'arall', 'aredig', 'gwasgar', 'bod', 'Lloegr', ',', 'a', 'can', 'cymuno', 'bechan', 'bod', 'Y', 'Wladfa', ',', 'gwybod', 'Ariannin[7', ']', "yw'r", 'Gymraeg', '(', 'hefyd', 'Cymraeg', 'heb', 'yr', 'bannod', ')', '.']

'''
for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        if lang not in ['bod']:
            test_lemmatize(lang, lemmatizer)
'''
