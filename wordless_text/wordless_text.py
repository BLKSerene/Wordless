#
# Wordless: Text
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import bs4

from wordless_text import wordless_text_processing

class Wordless_Token(str):
    def __new__(cls, string, *args, **kwargs):
        return super().__new__(cls, string)

    def __init__(self, string, boundary = '', sentence_ending = False):
        self.boundary = boundary
        self.sentence_ending = sentence_ending

class Wordless_Text():
    def __init__(self, main, file):
        self.main = main
        self.lang_code = file['lang_code']

        self.paras = []
        self.para_offsets = []
        self.sentences = []
        self.sentence_offsets = []
        self.tokens = []

        with open(file['path'], 'r', encoding = file['encoding_code']) as f:
            for line in f:
                if file['ext_code'] in ['.txt']:
                    text = line.rstrip()
                elif file['ext_code'] in ['.htm', '.html']:
                    soup = bs4.BeautifulSoup(line.rstrip(), 'lxml')
                    text = soup.get_text()

                if text:
                    self.paras.append(text)
                    self.para_offsets.append(len(self.tokens))

                    for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text, file['lang_code']):
                        self.sentences.append(sentence)
                        self.sentence_offsets.append(len(self.tokens))

                        self.tokens.extend(wordless_text_processing.wordless_word_tokenize(main, sentence, file['lang_code']))
