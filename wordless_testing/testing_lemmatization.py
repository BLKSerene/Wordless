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

sentence_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.'
sentence_fra = 'Le français est une langue indo-européenne de la famille des langues romanes.'
sentence_deu = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'
sentence_ita = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
sentence_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
sentence_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
sentence_ukr = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'

tokens_nld = ['Het', 'Nederlands', 'is', 'een', 'West', '-', 'Germaanse', 'taal', 'en', 'de', 'moedertaal', 'van', 'de', 'meeste', 'inwoners', 'van', 'Nederland', ',', 'België', 'en', 'Suriname', '.']
tokens_eng = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.']
tokens_fra = ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', '.']
tokens_deu = ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abgekürzt', 'Dt', '.', 'oder', 'Dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
tokens_ita = ["L'italiano", '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
tokens_por = ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego', '-', 'português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.']
tokens_rus = ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
tokens_spa = ['El', 'idioma', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', '.']
tokens_bod = ['༄༅། །', 'རྒྱ་གར་', 'སྐད་', 'དུ', '།', 'བོ་དྷི་སཏྭ་', 'ཙརྻ་', 'ཨ་བ་ཏ་ར', '།', 'བོད་སྐད་', 'དུ', '།', 'བྱང་ཆུབ་སེམས་དཔ', 'འི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ', '། །', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ', '། །', 'བདེ་གཤེགས་', 'ཆོས་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲས་', 'བཅས་', 'དང༌', '། །', 'ཕྱག་འོས་', 'ཀུན་', 'ལ', 'འང་', 'གུས་པ', 'ར་', 'ཕྱག་', 'འཚལ་', 'ཏེ', '། །', 'བདེ་གཤེགས་', 'སྲས་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི', '། །', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་ན', 'ས་', 'ནི་', 'བརྗོད་པ', 'ར་', 'བྱ', '། །']
tokens_ukr = ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ʊkrɐˈjɪɲsʲkɐ', 'ˈmɔwɐ', ']', ',', 'історичні', 'назви', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національна', 'мова', 'українців.']

testing_lemmatize(lang = 'nld',
                  lemmatizer = 'spaCy - Dutch Lemmatizer')
testing_lemmatize(lang = 'eng',
                  lemmatizer = 'NLTK - WordNet Lemmatizer')
testing_lemmatize(lang = 'eng',
                  lemmatizer = 'Lemmatization Lists - English Lemma List')
testing_lemmatize(lang = 'eng',
                  lemmatizer = 'spaCy - English Lemmatizer')
testing_lemmatize(lang = 'fra',
                  lemmatizer = 'spaCy - French Lemmatizer')
testing_lemmatize(lang = 'deu',
                  lemmatizer = 'spaCy - German Lemmatizer')
testing_lemmatize(lang = 'ita',
                  lemmatizer = 'spaCy - Italian Lemmatizer')
testing_lemmatize(lang = 'por',
                  lemmatizer = 'spaCy - Portuguese Lemmatizer')
testing_lemmatize(lang = 'rus',
                  lemmatizer = 'pymorphy2 - Morphological Analyzer')
testing_lemmatize(lang = 'spa',
                  lemmatizer = 'spaCy - Spanish Lemmatizer')
testing_lemmatize(lang = 'bod',
                  lemmatizer = 'pybo - Tibetan Lemmatizer')
testing_lemmatize(lang = 'ukr',
                  lemmatizer = 'pymorphy2 - Morphological Analyzer')
