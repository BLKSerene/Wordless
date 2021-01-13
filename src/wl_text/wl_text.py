#
# Wordless: Text - Text
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import re

import bs4

from wl_dialogs import wl_msg_box
from wl_text import wl_matching, wl_sentence_tokenization, wl_text_utils, wl_word_tokenization
from wl_utils import wl_misc

class Wl_Token(str):
    def __new__(cls, string, *args, **kwargs):
        return super().__new__(cls, string)

    def __init__(self, string, boundary = '', sentence_ending = False):
        self.boundary = boundary
        self.sentence_ending = sentence_ending

class Wl_Text_Blank():
    pass

class Wl_Text():
    def __init__(self, main, file):
        self.main = main
        self.lang = file['lang']
        self.tokenized = file['tokenized']
        self.tagged = file['tagged']

        self.offsets_paras = []
        self.offsets_sentences = []

        self.tokens_multilevel = []
        self.tokens_flat = []
        self.tags = []

        re_tags = wl_matching.get_re_tags(main)

        if re.search(r'\.txt', file['path'], flags = re.IGNORECASE):
            with open(file['path'], 'r', encoding = file['encoding']) as f:
                # Untokenized & Untagged
                if self.tokenized == 'No' and self.tagged == 'No':
                    for line in f:
                        text = line.rstrip()

                        if text:
                            tokens = wl_word_tokenization.wl_word_tokenize(main, text, lang = self.lang)

                            self.tokens_multilevel.append(tokens)
                            self.tags.extend([[]] * len(list(wl_misc.flatten_list(tokens))))
                # Untokenized & Tagged
                elif self.tokenized == 'No' and self.tagged == 'Yes':
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            tokens = wl_word_tokenization.wl_word_tokenize(main, text_no_tags, lang = self.lang)

                            self.tokens_multilevel.append(tokens)

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags, text):
                                self.tokens_multilevel[0][0].insert(0, '')
                                self.tags.append([])

                            # Extract tags
                            for tag in re.findall(re_tags, text):
                                i_tag = text.index(tag)

                                self.tokenize_text(text[:i_tag])
                                self.tags[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.tokenize_text(text)
                # Tokenized & Untagged
                elif self.tokenized == 'Yes' and self.tagged == 'No':
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_multilevel.append([])

                            for sentence in wl_sentence_tokenization.wl_sentence_split(main, text):
                                self.tokens_multilevel[-1].append(sentence.split())
                # Tokenized & Tagged
                elif self.tokenized == 'Yes' and self.tagged == 'Yes':
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            self.tokens_multilevel.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wl_sentence_tokenization.wl_sentence_split(main, text_no_tags):
                                self.tokens_multilevel[-1].append(sentence.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags, text):
                                self.tokens_multilevel[0][0].insert(0, '')

                                self.tags.append([])

                            # Extract tags
                            for tag in re.findall(re_tags, text):
                                i_tag = text.index(tag)

                                self.tokenize_text(text[:i_tag])
                                self.tags[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.tokenize_text(text)
        elif re.search(r'\.xml', file['path'], flags = re.IGNORECASE):
            text = ''

            with open(file['path'], 'r', encoding = file['encoding']) as f:
                for line in f:
                    text += line

            soup = bs4.BeautifulSoup(text, features = 'lxml-xml')

            tags_para = []
            tags_sentence = []
            tags_word = []

            for _, level, opening_tag, _ in self.main.settings_custom['tags']['tags_xml']:
                if level == 'Paragraph':
                    tags_para.append(opening_tag[1:-1])
                elif level == 'Sentence':
                    tags_sentence.append(opening_tag[1:-1])
                elif level == 'Word':
                    tags_word.append(opening_tag[1:-1])


            for para in div.select(','.join(tags_para)):
                self.tokens_multilevel.append([])

                for sentence in para.select(','.join(tags_sentence)):
                    self.tokens_multilevel[-1].append([])

                    for word in sentence.select(','.join(tags_word)):
                        self.tokens_multilevel[-1][-1].append(word.get_text())

                        self.tags.append([])

        # Paragraph and sentence offsets
        for para in self.tokens_multilevel:
            self.offsets_paras.append(len(self.tokens_flat))

            for sentence in para:
                self.offsets_sentences.append(len(self.tokens_flat))

                self.tokens_flat.extend(sentence)

        # Remove whitespace around all tags
        self.tags = [[tag.strip() for tag in tags] for tags in self.tags]

    def tokenize_text(self, text):
        if text:
            tokens = wl_word_tokenization.wl_word_tokenize(
                self.main, text,
                lang = self.lang
            )

            self.tags.extend([[]] * len(list(wl_misc.flatten_list(tokens))))

    def split_text(self, text):
        if text:
            tokens = text.split()

            for i in range(len(tokens)):
                self.tags.append([])
