#
# Wordless: Testing - Word Tokenization
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import itertools
import re
import sys

sys.path.append('.')

from wordless_testing import testing_init
from wordless_text import wordless_text_processing, wordless_text_utils
from wordless_utils import wordless_conversion

main = testing_init.Testing_Main()

def testing_word_tokenize(lang, word_tokenizer):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    print(f'{lang_text} / {word_tokenizer}:')

    wordless_text_utils.check_word_tokenizers(main, lang, word_tokenizer = word_tokenizer)

    tokens_sentences = wordless_text_processing.wordless_word_tokenize(main, globals()[f'sentence_{lang}'],
                                                                       lang = lang,
                                                                       word_tokenizer = word_tokenizer)
    tokens = itertools.chain.from_iterable(tokens_sentences)

    print(f"\t{' '.join(tokens)}")

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
sentence_vie = 'Tiếng Việt, còn gọi tiếng Việt Nam[5] hay Việt ngữ, là ngôn ngữ của người Việt (người Kinh) và là ngôn ngữ chính thức tại Việt Nam.'

testing_word_tokenize(lang = 'zho_cn',
                      word_tokenizer = 'jieba - Chinese Word Tokenizer')
testing_word_tokenize(lang = 'zho_cn',
                      word_tokenizer = 'Wordless - Chinese Character Tokenizer')
testing_word_tokenize(lang = 'nld',
                      word_tokenizer = 'spaCy - Dutch Word Tokenizer')
testing_word_tokenize(lang = 'eng',
                      word_tokenizer = 'NLTK - Penn Treebank Tokenizer')
testing_word_tokenize(lang = 'eng',
                      word_tokenizer = 'NLTK - NIST Tokenizer')
testing_word_tokenize(lang = 'eng',
                      word_tokenizer = 'NLTK - Tok-tok Tokenizer')
testing_word_tokenize(lang = 'eng',
                      word_tokenizer = 'NLTK - Twitter Tokenizer')
testing_word_tokenize(lang = 'eng',
                      word_tokenizer = 'SacreMoses - Moses Tokenizer')
testing_word_tokenize(lang = 'eng',
                      word_tokenizer = 'SacreMoses - Penn Treebank Tokenizer')
testing_word_tokenize(lang = 'fra',
                      word_tokenizer = 'spaCy - French Word Tokenizer')
testing_word_tokenize(lang = 'deu',
                      word_tokenizer = 'spaCy - German Word Tokenizer')
testing_word_tokenize(lang = 'ita',
                      word_tokenizer = 'spaCy - Italian Word Tokenizer')
testing_word_tokenize(lang = 'jpn',
                      word_tokenizer = 'nagisa - Japanese Word Tokenizer')
testing_word_tokenize(lang = 'jpn',
                      word_tokenizer = 'Wordless - Japanese Kanji Tokenizer')
testing_word_tokenize(lang = 'por',
                      word_tokenizer = 'spaCy - Portuguese Word Tokenizer')
testing_word_tokenize(lang = 'rus',
                      word_tokenizer = 'spaCy - Russian Word Tokenizer')
testing_word_tokenize(lang = 'spa',
                      word_tokenizer = 'spaCy - Spanish Word Tokenizer')
testing_word_tokenize(lang = 'tha',
                      word_tokenizer = 'PyThaiNLP - Maximum Matching Algorithm + TCC')
testing_word_tokenize(lang = 'tha',
                      word_tokenizer = 'PyThaiNLP - Maximum Matching Algorithm')
testing_word_tokenize(lang = 'tha',
                      word_tokenizer = 'PyThaiNLP - Longest Matching')
testing_word_tokenize(lang = 'bod',
                      word_tokenizer = 'pybo - Tibetan Word Tokenizer')
testing_word_tokenize(lang = 'vie',
                      word_tokenizer = 'Underthesea - Vietnamese Word Tokenizer')
