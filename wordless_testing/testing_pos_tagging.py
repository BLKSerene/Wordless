#
# Wordless: Testing - POS Tagging
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

def testing_pos_tag(lang, pos_tagger):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {pos_tagger}:')

    wordless_text_utils.check_pos_taggers(main, lang, pos_tagger = pos_tagger)

    tokens_tagged = wordless_text_processing.wordless_pos_tag(main, globals()[f'tokens_{lang}'],
                                                              lang = lang,
                                                              pos_tagger = pos_tagger)
    tokens_tagged_universal = wordless_text_processing.wordless_pos_tag(main, globals()[f'tokens_{lang}'],
                                                                        lang = lang,
                                                                        pos_tagger = pos_tagger,
                                                                        tagset = 'universal')

    print(f"\t{tokens_tagged}")
    print(f"\t{tokens_tagged_universal}")

sentence_zho_cn = '作为语言而言，为世界使用人数最多的语言，目前世界有五分之一人口做为母语。'
sentence_nld = 'Het Nederlands is een West-Germaanse taal en de moedertaal van de meeste inwoners van Nederland, België en Suriname.'
sentence_eng = 'English is a West Germanic language that was first spoken in early medieval England and eventually became a global lingua franca.[4][5]'
sentence_fra = 'Le français est une langue indo-européenne de la famille des langues romanes.'
sentence_deu = 'Die deutsche Sprache bzw. Deutsch ([dɔʏ̯t͡ʃ]; abgekürzt Dt. oder Dtsch.) ist eine westgermanische Sprache.'
sentence_ita = "L'italiano ([itaˈljaːno][Nota 1] ascolta[?·info]) è una lingua romanza parlata principalmente in Italia."
sentence_jpn = '使用人口について正確な統計はないが、日本国内の人口、および日本国外に住む日本人や日系人、日本がかつて統治した地域の一部住民など、約1億3千万人以上と考えられている[7]。'
sentence_por = 'A língua portuguesa, também designada português, é uma língua românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.'
sentence_rus = 'Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — один из восточнославянских языков, национальный язык русского народа.'
sentence_spa = 'El idioma español o castellano es una lengua romance procedente del latín hablado.'
sentence_tha = 'ภาษาไทย หรือ ภาษาไทยกลาง เป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
sentence_bod = '༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །'
sentence_ukr = 'Украї́нська мо́ва (МФА: [ʊkrɐˈjɪɲsʲkɐ ˈmɔwɐ], історичні назви — ру́ська, руси́нська[9][10][11][* 2]) — національна мова українців.'
sentence_vie = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam.'

tokens_zho_cn = ['作为', '语言', '而言', '，', '为', '世界', '使用', '人', '数最多', '的', '语言', '，', '目前', '世界', '有', '五分之一', '人口', '做', '为', '母语', '。']
tokens_nld = ['Het', 'Nederlands', 'is', 'een', 'West', '-', 'Germaanse', 'taal', 'en', 'de', 'moedertaal', 'van', 'de', 'meeste', 'inwoners', 'van', 'Nederland', ',', 'België', 'en', 'Suriname', '.']
tokens_eng = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.']
tokens_fra = ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', '.']
tokens_deu = ['Die', 'deutsche', 'Sprache', 'bzw.', 'Deutsch', '(', '[', 'dɔʏ̯t͡ʃ', ']', ';', 'abgekürzt', 'Dt', '.', 'oder', 'Dtsch', '.', ')', 'ist', 'eine', 'westgermanische', 'Sprache', '.']
tokens_ita = ["L'italiano", '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta[?·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.']
tokens_jpn = ['使用', '人口', 'に', 'つい', 'て', '正確', 'な', '統計', 'は', 'ない', 'が', '、', '日本', '国', '内', 'の', '人口', '、', 'および', '日本', '国', '外', 'に', '住む', '日本', '人', 'や', '日系', '人', '、', '日本', 'が', 'かつて', '統治', 'し', 'た', '地域', 'の', '一部', '住民', 'など', '、', '約', '1', '億', '3千', '万', '人', '以上', 'と', '考え', 'られ', 'て', 'いる', '[', '7', ']', '。']
tokens_por = ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego', '-', 'português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.']
tokens_rus = ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'один', 'из', 'восточнославянских', 'языков', ',', 'национальный', 'язык', 'русского', 'народа', '.']
tokens_spa = ['El', 'idioma', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', '.']
tokens_tha = ['ภาษาไทย', 'หรือ', 'ภาษาไทย', 'กลาง', 'เป็น', 'ภาษาราชการ', 'และ', 'ภาษาประจำชาติ', 'ของ', 'ประเทศไทย']
tokens_bod = ['༄༅། །', 'རྒྱ་གར་', 'སྐད་', 'དུ', '།', 'བོ་དྷི་སཏྭ་', 'ཙརྻ་', 'ཨ་བ་ཏ་ར', '།', 'བོད་སྐད་', 'དུ', '།', 'བྱང་ཆུབ་སེམས་དཔ', 'འི་', 'སྤྱོད་པ་', 'ལ་', 'འཇུག་པ', '། །', 'སངས་རྒྱས་', 'དང་', 'བྱང་ཆུབ་སེམས་དཔའ་', 'ཐམས་ཅད་', 'ལ་', 'ཕྱག་', 'འཚལ་', 'ལོ', '། །', 'བདེ་གཤེགས་', 'ཆོས་', 'ཀྱི་', 'སྐུ་', 'མངའ་', 'སྲས་', 'བཅས་', 'དང༌', '། །', 'ཕྱག་འོས་', 'ཀུན་', 'ལ', 'འང་', 'གུས་པ', 'ར་', 'ཕྱག་', 'འཚལ་', 'ཏེ', '། །', 'བདེ་གཤེགས་', 'སྲས་', 'ཀྱི་', 'སྡོམ་', 'ལ་', 'འཇུག་པ་', 'ནི', '། །', 'ལུང་', 'བཞིན་', 'མདོར་བསྡུས་ན', 'ས་', 'ནི་', 'བརྗོད་པ', 'ར་', 'བྱ', '། །']
tokens_ukr = ['Украї́нська', 'мо́ва', '(', 'МФА', ':', '[', 'ʊkrɐˈjɪɲsʲkɐ', 'ˈmɔwɐ', ']', ',', 'історичні', 'назви', '—', 'ру́ська', ',', 'руси́нська[9][10][11', ']', '[', '*', '2', ']', ')', '—', 'національна', 'мова', 'українців.']
tokens_vie = ['Tiếng', 'Việt', ',', 'còn', 'gọi', 'tiếng', 'Việt_Nam', '[', '5', ']', 'hay', 'Việt_ngữ', ',', 'là', 'ngôn_ngữ', 'của', 'người', 'Việt', '(', 'người', 'Kinh', ')', 'và', 'là', 'ngôn_ngữ', 'chính_thức', 'tại', 'Việt_Nam', '.']

testing_pos_tag(lang = 'zho_cn',
                pos_tagger = 'jieba - Chinese POS Tagger')
testing_pos_tag(lang = 'nld',
                pos_tagger = 'spaCy - Dutch POS Tagger')
testing_pos_tag(lang = 'eng',
                pos_tagger = 'NLTK - Perceptron POS Tagger')
testing_pos_tag(lang = 'eng',
                pos_tagger = 'spaCy - English POS Tagger')
testing_pos_tag(lang = 'fra',
                pos_tagger = 'spaCy - French POS Tagger')
testing_pos_tag(lang = 'deu',
                pos_tagger = 'spaCy - German POS Tagger')
testing_pos_tag(lang = 'ita',
                pos_tagger = 'spaCy - Italian POS Tagger')
testing_pos_tag(lang = 'jpn',
                pos_tagger = 'nagisa - Japanese POS Tagger')
testing_pos_tag(lang = 'por',
                pos_tagger = 'spaCy - Portuguese POS Tagger')
testing_pos_tag(lang = 'rus',
                pos_tagger = 'NLTK - Perceptron POS Tagger')
testing_pos_tag(lang = 'rus',
                pos_tagger = 'pymorphy2 - Morphological Analyzer')
testing_pos_tag(lang = 'spa',
                pos_tagger = 'spaCy - Spanish POS Tagger')
testing_pos_tag(lang = 'tha',
                pos_tagger = 'PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus')
testing_pos_tag(lang = 'tha',
                pos_tagger = 'PyThaiNLP - Perceptron POS Tagger - PUD Corpus')
testing_pos_tag(lang = 'bod',
                pos_tagger = 'pybo - Tibetan POS Tagger')
testing_pos_tag(lang = 'ukr',
                pos_tagger = 'pymorphy2 - Morphological Analyzer')
testing_pos_tag(lang = 'vie',
                pos_tagger = 'Underthesea - Vietnamese POS Tagger')
