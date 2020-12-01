#
# Wordless: Text - Text
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import re

import bs4

from wl_text import wl_matching, wl_sentence_tokenization, wl_text_utils, wl_word_tokenization

class Wl_Token(str):
    def __new__(cls, string, *args, **kwargs):
        return super().__new__(cls, string)

    def __init__(self, string, boundary = '', sentence_ending = False):
        self.boundary = boundary
        self.sentence_ending = sentence_ending

class Wl_Text_Blank():
    pass

class Wl_Text():
    def __init__(self, main, file, flat_tokens = True):
        self.main = main
        self.lang = file['lang']
        self.tokenized = file['tokenized']
        self.tagged = file['tagged']

        self.offsets_paras = []
        self.offsets_sentences = []
        self.offsets_clauses = []

        if flat_tokens:
            self.tokens_multilevel = [[[[]]]]
        else:
            self.tokens_multilevel = []

        self.tokens_flat = []
        self.tags = []

        re_tags = wl_matching.get_re_tags(main)

        with open(file['path'], 'r', encoding = file['encoding']) as f:
            # Untokenized & Untagged
            if self.tokenized == 'No' and self.tagged == 'No':
                if flat_tokens:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            tokens = wl_word_tokenization.wl_word_tokenize(
                                main, text,
                                lang = self.lang,
                                flat_tokens = True
                            )

                            self.tokens_multilevel[0][0][0].extend(tokens)
                            self.tags.extend([[]] * len(tokens))
                else:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            tokens = wl_word_tokenization.wl_word_tokenize(
                                main, text,
                                lang = self.lang,
                                flat_tokens = False
                            )

                            self.tokens_multilevel.append(tokens)
                            self.tags.extend([[]] * len(tokens))

            # Untokenized & Tagged
            elif self.tokenized == 'no' and self.tagged == 'Yes':
                if flat_tokens:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            tokens = wl_word_tokenization.wl_word_tokenize(
                                main, text_no_tags,
                                lang = self.lang,
                                flat_tokens = True
                            )

                            self.tokens_multilevel[0][0][0].extend(tokens)

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags, text):
                                self.tokens_multilevel[0][0][0].insert(0, '')
                                self.tags_non_pos.append([])

                            # Extract tags
                            for tag in re.findall(re_tags, text):
                                i_tag = text.index(tag)

                                self.tokenize_text(text[:i_tag])
                                self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.tokenize_text(text)
                else:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            tokens = wl_word_tokenization.wl_word_tokenize(
                                main, text_no_tags,
                                lang = self.lang,
                                flat_tokens = False
                            )

                            self.tokens_multilevel.append(tokens)

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags, text):
                                self.tokens_multilevel[0][0][0].insert(0, '')
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
                if flat_tokens:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_multilevel[0][0][0].extend(text.split())
                else:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_multilevel.append([])

                            for sentence in wl_sentence_tokenization.wl_sentence_split(main, text):
                                self.tokens_multilevel[-1].append([])

                                for clause in wl_sentence_tokenization.wl_clause_split(main, sentence):
                                    self.tokens_multilevel[-1][-1].append(clause.split())
            # Tokenized & Tagged
            elif self.tokenized == 'Yes' and self.tagged == 'Yes':
                if flat_tokens:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_multilevel[0][0][0].extend(text_no_tags.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_Tags, text):
                                self.tokens_multilevel[0][0][0].insert(0, '')

                                self.tags.append([])

                            # Extract tags
                            for tag in re.findall(re_tags, text):
                                i_tag = text.index(tag)

                                self.tokenize_text(text[:i_tag])
                                self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.tokenize_text(text)
                else:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            self.tokens_multilevel.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_all, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wl_sentence_tokenization.wl_sentence_split(main, text_no_tags):
                                self.tokens_multilevel[-1].append([])

                                for clause in wl_sentence_tokenization.wl_clause_split(main, sentence):
                                    self.tokens_multilevel[-1][-1].append(clause.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and (re.match(re_tags_pos, text) or re.match(re_tags_non_pos, text)):
                                self.tokens_multilevel[0][0][0].insert(0, '')

                                self.tags_all.append([])
                                self.tags_pos.append([])
                                self.tags_non_pos.append([])

                            # Extract tags
                            for tag in re.findall(re_tags, text):
                                i_tag = text.index(tag)

                                self.tokenize_text(text[:i_tag])
                                self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.tokenize_text(text)

        # Paragraph, sentence and clause offsets
        for para in self.tokens_multilevel:
            self.offsets_paras.append(len(self.tokens_flat))

            for sentence in para:
                self.offsets_sentences.append(len(self.tokens_flat))

                for clause in sentence:
                    self.offsets_clauses.append(len(self.tokens_flat))

                    self.tokens_flat.extend(clause)

        # Remove whitespace around all tags
        self.tags = [[tag.strip() for tag in tags] for tags in self.tags]

    def tokenize_text(self, text):
        if text:
            tokens = wl_word_tokenization.wl_word_tokenize(
                self.main, text,
                lang = self.lang
            )

            for i in range(len(tokens)):
                self.tags.append([])

    def split_text(self, text):
        if text:
            tokens = text.split()

            for i in range(len(tokens)):
                self.tags.append([])
