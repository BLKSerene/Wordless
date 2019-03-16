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

sys.path.append('.')

from wordless_testing import testing_init
from wordless_text import wordless_text_processing, wordless_text_utils
from wordless_utils import wordless_conversion

main = testing_init.Testing_Main()

def testing_lemmatize(lang, lemmatizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {lemmatizer}:')

    wordless_text_utils.check_lemmatizers(main, lang, lemmatizer = lemmatizer)

    lemmas = wordless_text_processing.wordless_lemmatize(main, globals()[f'tokens_{lang}'],
                                                         lang = lang,
                                                         lemmatizer = lemmatizer)

    print(f"\t{lemmas}")

sentence_ast = "L'asturianu ye una llingua romance propia d'Asturies,[1] perteneciente al subgrupu asturllionés."
sentence_bul = 'Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици.'
sentence_cat = "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l'Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada per més d'onze milions de persones, a Catalunya, al País Valencià (tret d'algunes comarques i localitats de l'interior), les Illes Balears, Andorra, la Franja de Ponent (a l'Aragó), la ciutat de l'Alguer (a l'illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l'Argentina, amb 195.000 parlants).[11]"
sentence_ces = 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
sentence_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'
sentence_est = 'Eesti keel (varasem nimetus: maakeel) on läänemeresoome lõunarühma kuuluv keel.'
sentence_fra = 'Le français est une langue indo-européenne de la famille des langues romanes.'
sentence_glg = 'O galego ([ɡaˈleɣo̝]) é unha lingua indoeuropea que pertence á póla de linguas románicas.'
sentence_deu = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'
sentence_grc = 'Με τον όρο αρχαία ελληνική γλώσσα εννοείται μια μορφή της ελληνικής γλώσσας, που ομιλούνταν κατά τους αρχαϊκούς χρόνους και την κλασική αρχαιότητα.'
sentence_ell = 'Η ελληνική γλώσσα είναι μια από τις ινδοευρωπαϊκές γλώσσες[9] και αποτελεί το μοναδικό μέλος ενός ανεξάρτητου κλάδου, αυτής της οικογένειας γλωσσών, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
sentence_hun = 'A magyar nyelv az uráli nyelvcsalád tagja, a finnugor nyelvek közé tartozó ugor nyelvek egyike.'
sentence_gle = 'Is ceann de na teangacha Ceilteacha í an Ghaeilge (nó Gaeilge na hÉireann mar a thugtar uirthi corruair), agus ceann den dtrí cinn de theangacha Ceilteacha ar a dtugtar na teangacha Gaelacha (.i. an Ghaeilge, Gaeilge na hAlban agus Gaeilge Mhanann) go háirithe.'
sentence_ita = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
sentence_glv = 'She Gaelg (graït: /gɪlg/) çhengey Ghaelagh Vannin.'
sentence_fas = 'فارسی یا پارسی یکی از زبان‌های هندواروپایی در شاخهٔ زبان‌های ایرانی جنوب غربی است که در کشورهای ایران، افغانستان،[۳] تاجیکستان[۴] و ازبکستان[۵] به آن سخن می‌گویند.'
sentence_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
sentence_ron = 'Limba română este o limbă indo-europeană, din grupul italic și din subgrupul oriental al limbilor romanice.'
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
sentence_gla = "'S i cànan dùthchasach na h-Alba a th' anns a' Ghàidhlig."
sentence_slk = 'Slovenčina patrí do skupiny západoslovanských jazykov (spolu s češtinou, poľštinou, hornou a dolnou lužickou srbčinou a kašubčinou).'
sentence_slv = 'Slovenščina [slovénščina] / [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.'
sentence_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'
sentence_swe = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av drygt elva miljoner personer[källa behövs] främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
sentence_ukr = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
sentence_cym = "Aelod o'r gangen Frythonaidd o'r ieithoedd Celtaidd a siaredir yn frodorol yng Nghymru, gan Gymry a phobl eraill ar wasgar yn Lloegr, a chan gymuned fechan yn Y Wladfa, yr Ariannin[7] yw'r Gymraeg (hefyd Cymraeg /kəmˈrɑːɨɡ / heb y fannod)."

tokens_ast = ["L'asturianu", 'ye', 'una', 'llingua', 'romance', 'propia', "d'Asturies,[1", ']', 'perteneciente', 'al', 'subgrupu', 'asturllionés', '.']
tokens_bul = ['Бъ̀лгарският', 'езѝк', 'е', 'индоевропейски', 'език', 'от', 'групата', 'на', 'южнославянските', 'езици', '.']
tokens_cat = ['El', 'català', '(', 'denominació', 'oficial', 'a', 'Catalunya', ',', 'a', 'les', 'Illes', 'Balears', ',', 'a', 'Andorra', ',', 'a', 'la', 'ciutat', 'de', "l'", 'Alguer', 'i', 'tradicional', 'a', 'Catalunya', 'Nord', ')', 'o', 'valencià', '(', 'denominació', 'oficial', 'al', 'País', 'Valencià', 'i', 'tradicional', 'al', 'Carxe', ')', 'és', 'una', 'llengua', 'romànica', 'parlada', 'per', 'més', "d'", 'onze', 'milions', 'de', 'persones', ',', 'a', 'Catalunya', ',', 'al', 'País', 'Valencià', '(', 'tret', "d'", 'algunes', 'comarques', 'i', 'localitats', 'de', "l'", 'interior', ')', ',', 'les', 'Illes', 'Balears', ',', 'Andorra', ',', 'la', 'Franja', 'de', 'Ponent', '(', 'a', "l'", 'Aragó', ')', ',', 'la', 'ciutat', 'de', "l'", 'Alguer', '(', 'a', "l'", 'illa', 'de', 'Sardenya', ')', ',', 'la', 'Catalunya', 'del', 'Nord,[8', ']', 'el', 'Carxe', '(', 'un', 'petit', 'territori', 'de', 'Múrcia', 'poblat', 'per', 'immigrats', 'valencians),[9][10', ']', 'i', 'en', 'petites', 'comunitats', 'arreu', 'del', 'món', '(', 'entre', 'les', 'quals', 'destaca', 'la', 'de', "l'", 'Argentina', ',', 'amb', '195.000', 'parlants).[11', ']']
tokens_ces = ['Čeština', 'neboli', 'český', 'jazyk', 'je', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.']
tokens_nld = ['Het', 'Nederlands', 'is', 'een', 'West', '-', 'Germaanse', 'taal', 'en', 'de', 'moedertaal', 'van', 'de', 'meeste', 'inwoners', 'van', 'Nederland', ',', 'België', 'en', 'Suriname', '.']
tokens_eng = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.']
tokens_est = ['Eesti', 'keel', '(', 'varasem', 'nimetus', ':', 'maakeel', ')', 'on', 'läänemeresoome', 'lõunarühma', 'kuuluv', 'keel', '.']
tokens_fra = ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', '.']
tokens_glg = ['O', 'galego', '(', '[', 'ɡaˈleɣo̝', ']', ')', 'é', 'unha', 'lingua', 'indoeuropea', 'que', 'pertence', 'á', 'póla', 'de', 'linguas', 'románicas', '.']
tokens_deu = ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abgekürzt', 'Dt', '.', 'oder', 'Dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
tokens_grc = ['Με', 'τον', 'όρο', 'αρχαία', 'ελληνική', 'γλώσσα', 'εννοείται', 'μια', 'μορφή', 'της', 'ελληνικής', 'γλώσσας', ',', 'που', 'ομιλούνταν', 'κατά', 'τους', 'αρχαϊκούς', 'χρόνους', 'και', 'την', 'κλασική', 'αρχαιότητα', '.']
tokens_ell = ['Η', 'ελληνική', 'γλώσσα', 'είναι', 'μια', 'από', 'τις', 'ινδοευρωπαϊκές', 'γλώσσες[9', ']', 'και', 'αποτελεί', 'το', 'μοναδικό', 'μέλος', 'ενός', 'ανεξάρτητου', 'κλάδου', ',', 'αυτής', 'της', 'οικογένειας', 'γλωσσών', ',', 'ενώ', 'είναι', 'η', 'επίσημη', 'γλώσσα', 'της', 'Ελλάδος', 'και', 'της', 'Κύπρου', '.']
tokens_hun = ['A', 'magyar', 'nyelv', 'az', 'uráli', 'nyelvcsalád', 'tagja', ',', 'a', 'finnugor', 'nyelvek', 'közé', 'tartozó', 'ugor', 'nyelvek', 'egyike', '.']
tokens_gle = ['Is', 'ceann', 'de', 'na', 'teangacha', 'Ceilteacha', 'í', 'an', 'Ghaeilge', '(', 'nó', 'Gaeilge', 'na', 'hÉireann', 'mar', 'a', 'thugtar', 'uirthi', 'corruair', ')', ',', 'agus', 'ceann', 'den', 'dtrí', 'cinn', 'de', 'theangacha', 'Ceilteacha', 'ar', 'a', 'dtugtar', 'na', 'teangacha', 'Gaelacha', '(', '.i.', 'an', 'Ghaeilge', ',', 'Gaeilge', 'na', 'hAlban', 'agus', 'Gaeilge', 'Mhanann', ')', 'go', 'háirithe', '.']
tokens_ita = ["L'italiano", '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
tokens_glv = ['She', 'Gaelg', '(', 'graït', ':', '/gɪlg/', ')', 'çhengey', 'Ghaelagh', 'Vannin', '.']
tokens_fas = ['فارسی', 'یا', 'پارسی', 'یکی', 'از', 'زبان\u200cهای', 'هندواروپایی', 'در', 'شاخهٔ', 'زبان\u200cهای', 'ایرانی', 'جنوب', 'غربی', 'است', 'که', 'در', 'کشورهای', 'ایران', '،', 'افغانستان', '،', '[', '۳', ']', 'تاجیکستان[', '۴', ']', 'و', 'ازبکستان[', '۵', ']', 'به', 'آن', 'سخن', 'می\u200cگویند', '.']
tokens_por = ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego', '-', 'português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.']
tokens_ron = ['Limba', 'română', 'este', 'o', 'limbă', 'indo-europeană', ',', 'din', 'grupul', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbilor', 'romanice', '.']
tokens_rus = ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
tokens_gla = ["'S", 'i', 'cànan', 'dùthchasach', 'na', 'h', '-', 'Alba', 'a', 'th', "'", 'anns', 'a', "'", 'Ghàidhlig', '.']
tokens_slk = ['Slovenčina', 'patrí', 'do', 'skupiny', 'západoslovanských', 'jazykov', '(', 'spolu', 's', 'češtinou', ',', 'poľštinou', ',', 'hornou', 'a', 'dolnou', 'lužickou', 'srbčinou', 'a', 'kašubčinou', ')', '.']
tokens_slv = ['Slovenščina', '[', 'slovénščina', ']', '/', '[', 'sloˈʋenʃtʃina', ']', 'je', 'združeni', 'naziv', 'za', 'uradni', 'knjižni', 'jezik', 'Slovencev', 'in', 'skupno', 'ime', 'za', 'narečja', 'in', 'govore', ',', 'ki', 'jih', 'govorijo', 'ali', 'so', 'jih', 'nekoč', 'govorili', 'Slovenci', '.']
tokens_spa = ['El', 'idioma', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', '.']
tokens_swe = ['Svenska', '(', 'svenska', '(', 'info', ')', ')', 'är', 'ett', 'östnordiskt', 'språk', 'som', 'talas', 'av', 'drygt', 'elva', 'miljoner', 'personer', '[', 'källa', 'behövs', ']', 'främst', 'i', 'Sverige', 'där', 'språket', 'har', 'en', 'dominant', 'ställning', 'som', 'huvudspråk', ',', 'men', 'även', 'som', 'det', 'ena', 'nationalspråket', 'i', 'Finland', 'och', 'som', 'enda', 'officiella', 'språk', 'på', 'Åland', '.']
tokens_bod = ['༄༅། །', 'རྒྱ་གར་', 'སྐད་', 'དུ', '།', 'བོ་དྷི་སཏྭ་', 'ཙརྻ་', 'ཨ་བ་ཏ་ར', '།', 'བོད་སྐད་', 'དུ', '།', 'བྱང་ཆུབ་སེམས་དཔ', 'འི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ', '། །', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ', '། །', 'བདེ་གཤེགས་', 'ཆོས་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲས་', 'བཅས་', 'དང༌', '། །', 'ཕྱག་འོས་', 'ཀུན་', 'ལ', 'འང་', 'གུས་པ', 'ར་', 'ཕྱག་', 'འཚལ་', 'ཏེ', '། །', 'བདེ་གཤེགས་', 'སྲས་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི', '། །', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་ན', 'ས་', 'ནི་', 'བརྗོད་པ', 'ར་', 'བྱ', '། །']
tokens_ukr = ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ʊkrɐˈjɪɲsʲkɐ', 'ˈmɔwɐ', ']', ',', 'історичні', 'назви', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національна', 'мова', 'українців.']
tokens_cym = ['Aelod', "o'r", 'gangen', 'Frythonaidd', "o'r", 'ieithoedd', 'Celtaidd', 'a', 'siaredir', 'yn', 'frodorol', 'yng', 'Nghymru', ',', 'gan', 'Gymry', 'a', 'phobl', 'eraill', 'ar', 'wasgar', 'yn', 'Lloegr', ',', 'a', 'chan', 'gymuned', 'fechan', 'yn', 'Y', 'Wladfa', ',', 'yr', 'Ariannin[7', ']', "yw'r", 'Gymraeg', '(', 'hefyd', 'Cymraeg', '/kəmˈrɑːɨɡ', '/', 'heb', 'y', 'fannod', ')', '.']

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        testing_lemmatize(lang = lang,
                          lemmatizer = lemmatizer)
