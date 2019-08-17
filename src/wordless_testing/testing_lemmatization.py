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

SENTENCE_AST = "L'asturianu ye una llingua romance propia d'Asturies,[1] perteneciente al subgrupu asturllionés."
SENTENCE_BUL = 'Бъ̀лгарският езѝк е индоевропейски език от групата на южнославянските езици.'
SENTENCE_CAT = "El català (denominació oficial a Catalunya, a les Illes Balears, a Andorra, a la ciutat de l'Alguer i tradicional a Catalunya Nord) o valencià (denominació oficial al País Valencià i tradicional al Carxe) és una llengua romànica parlada per més d'onze milions de persones, a Catalunya, al País Valencià (tret d'algunes comarques i localitats de l'interior), les Illes Balears, Andorra, la Franja de Ponent (a l'Aragó), la ciutat de l'Alguer (a l'illa de Sardenya), la Catalunya del Nord,[8] el Carxe (un petit territori de Múrcia poblat per immigrats valencians),[9][10] i en petites comunitats arreu del món (entre les quals destaca la de l'Argentina, amb 195.000 parlants).[11]"
SENTENCE_CES = 'Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.'
SENTENCE_NLD = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
SENTENCE_ENG = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'
SENTENCE_EST = 'Eesti keel (varasem nimetus: maakeel) on läänemeresoome lõunarühma kuuluv keel.'
SENTENCE_FRA = 'Le français est une langue indo-européenne de la famille des langues romanes.'
SENTENCE_GLG = 'O galego ([ɡaˈleɣo̝]) é unha lingua indoeuropea que pertence á póla de linguas románicas.'
SENTENCE_DEU = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'
SENTENCE_GRC = 'Με τον όρο αρχαία ελληνική γλώσσα εννοείται μια μορφή της ελληνικής γλώσσας, που ομιλούνταν κατά τους αρχαϊκούς χρόνους και την κλασική αρχαιότητα.'
SENTENCE_ELL = 'Η ελληνική γλώσσα είναι μια από τις ινδοευρωπαϊκές γλώσσες[9] και αποτελεί το μοναδικό μέλος ενός ανεξάρτητου κλάδου, αυτής της οικογένειας γλωσσών, ενώ είναι η επίσημη γλώσσα της Ελλάδος και της Κύπρου.'
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
SENTENCE_SPA = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'
SENTENCE_SWE = 'Svenska (svenska (info)) är ett östnordiskt språk som talas av drygt elva miljoner personer[källa behövs] främst i Sverige där språket har en dominant ställning som huvudspråk, men även som det ena nationalspråket i Finland och som enda officiella språk på Åland.'
SENTENCE_BOD = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
SENTENCE_UKR = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
SENTENCE_CYM = "Aelod o'r gangen Frythonaidd o'r ieithoedd Celtaidd a siaredir yn frodorol yng Nghymru, gan Gymry a phobl eraill ar wasgar yn Lloegr, a chan gymuned fechan yn Y Wladfa, yr Ariannin[7] yw'r Gymraeg (hefyd Cymraeg /kəmˈrɑːɨɡ / heb y fannod)."

def testing_lemmatize(lang, lemmatizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {lemmatizer}:')

    tokens_sentences = wordless_text_processing.wordless_word_tokenize(main, globals()[f'SENTENCE_{lang.upper()}'],
                                                                       lang = lang)
    tokens = [token for tokens in tokens_sentences for token in tokens]

    lemmas = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                         lang = lang,
                                                         lemmatizer = lemmatizer)

    print(f"\t{lemmas}")

main = testing_init.Testing_Main()

for lang, lemmatizers in main.settings_global['lemmatizers'].items():
    for lemmatizer in lemmatizers:
        testing_lemmatize(lang = lang,
                          lemmatizer = lemmatizer)
