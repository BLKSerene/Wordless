#
# Wordless: Text - Text
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy
import re

import bs4

from wordless_text import wordless_matching, wordless_text_processing, wordless_text_utils

class Wordless_Token(str):
    def __new__(cls, string, *args, **kwargs):
        return super().__new__(cls, string)

    def __init__(self, string, boundary = '', sentence_ending = False):
        self.boundary = boundary
        self.sentence_ending = sentence_ending

class Wordless_Text_Blank():
    pass

class Wordless_Text():
    def __init__(self, main, file, tokens_only = True):
        self.main = main
        self.lang = file['lang']
        self.text_type = file['text_type']

        self.para_offsets = []
        self.sentence_offsets = []
        self.tokens_sentences_paras = []
        self.tokens = []

        self.tags_all = []
        self.tags_pos = []
        self.tags_non_pos = []

        re_tags_all = wordless_matching.get_re_tags(main, tags = 'all')
        re_tags_pos = wordless_matching.get_re_tags(main, tags = 'pos')
        re_tags_non_pos = wordless_matching.get_re_tags(main, tags = 'non_pos')

        if tokens_only:
            keep_sentences = False
        else:
            keep_sentences = True

        with open(file['path'], 'r', encoding = file['encoding']) as f:
            # Untokenized / Untagged
            if self.text_type == ('untokenized', 'untagged'):
                for line in f:
                    text = line.rstrip()

                    if text:
                        tokens_sentences = wordless_text_processing.wordless_word_tokenize(main, text,
                                                                                           lang = self.lang,
                                                                                           keep_sentences = keep_sentences)

                        self.tokens_sentences_paras.append(tokens_sentences)

            # Untokenized / Tagged (Non-POS)
            elif self.text_type == ('untokenized', 'tagged_non_pos'):
                for i, line in enumerate(f):
                    text = line.rstrip()

                    if text:
                        # Replace all tags with a whitespace to ensure no words run together
                        text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                        text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                        tokens_sentences = wordless_text_processing.wordless_word_tokenize(main, text_no_tags,
                                                                                           lang = self.lang,
                                                                                           keep_sentences = keep_sentences)

                        self.tokens_sentences_paras.append(tokens_sentences)

                        # Check if the first token in the text is a tag
                        if i == 0 and re.match(re_tags_non_pos, text):
                            self.tokens_sentences_paras[0][0].insert(0, '')
                            self.tags_non_pos.append([])

                        # Extract tags
                        for tag in re.findall(re_tags_non_pos, text):
                            i_tag = text.index(tag)

                            self.tokenize_text(text[:i_tag])
                            self.tags_non_pos[-1].append(tag)

                            text = text[i_tag + len(tag):]

                        # The last part of the text
                        if text:
                            self.tokenize_text(text)
            # Tokenized / Untagged
            elif self.text_type == ('tokenized', 'untagged'):
                if tokens_only:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_sentences_paras.append([text.split()])
                else:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_sentences_paras.append([])

                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text,
                                                                                                lang = self.lang):
                                self.tokens_sentences_paras[-1].append(sentence.split())
            # Tokenized / Tagged (POS)
            elif self.text_type == ('tokenized', 'tagged_pos'):
                if tokens_only:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_sentences_paras.append([text_no_tags.split()])

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_pos, text):
                                self.tokens_sentences_paras[0][0].insert(0, '')
                                self.tags_pos.append([])

                            # Extract tags
                            for tag in re.findall(re_tags_pos, text):
                                i_tag = text.index(tag)

                                self.split_text(text[:i_tag])
                                self.tags_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.split_text(text)
                else:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            self.tokens_sentences_paras.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                            lang = self.lang)

                            for sentence in sentences:
                                self.tokens_sentences_paras[-1].append(sentence.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_pos, text):
                                self.tokens_sentences_paras[0][0].insert(0, '')
                                self.tags_pos.append([])

                            # Extract tags
                            for tag in re.findall(re_tags_pos, text):
                                i_tag = text.index(tag)

                                self.split_text(text[:i_tag])
                                self.tags_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.split_text(text)
            # Tokenized / Tagged (Non-POS)
            elif self.text_type == ('tokenized', 'tagged_non_pos'):
                if tokens_only:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_sentences_paras.append([text_no_tags.split()])

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_non_pos, text):
                                self.tokens_sentences_paras[0][0].insert(0, '')
                                self.tags_non_pos.append([])

                            # Extract tags
                            for tag in re.findall(re_tags_non_pos, text):
                                i_tag = text.index(tag)

                                self.split_text(text[:i_tag])
                                self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.split_text(text)
                else:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            self.tokens_sentences_paras.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                            lang = self.lang)

                            for sentence in sentences:
                                self.tokens_sentences_paras[-1].append(sentence.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_non_pos, text):
                                self.tokens_sentences_paras[0][0].insert(0, '')
                                self.tags_non_pos.append([])

                            # Extract tags
                            for tag in re.findall(re_tags_non_pos, text):
                                i_tag = text.index(tag)

                                self.split_text(text[:i_tag])
                                self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.split_text(text)
            # Tokenized / Tagged (Both)
            elif self.text_type == ('tokenized', 'tagged_both'):
                if tokens_only:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_all, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_sentences_paras.append([text_no_tags.split()])

                            # Check if the first token in the text is a tag
                            if i == 0 and (re.match(re_tags_pos, text) or re.match(re_tags_non_pos, text)):
                                self.tokens_sentences_paras[0][0].insert(0, '')

                                self.tags_all.append([])
                                self.tags_pos.append([])
                                self.tags_non_pos.append([])

                            # Extract tags
                            while text:
                                tag_pos = re.search(re_tags_pos, text)
                                tag_non_pos = re.search(re_tags_non_pos, text)

                                if tag_pos:
                                    i_tag_pos = text.index(tag_pos.group())

                                if tag_non_pos:
                                    i_tag_non_pos = text.index(tag_non_pos.group())

                                if (tag_pos and tag_non_pos and i_tag_pos < i_tag_non_pos or
                                    tag_pos and not tag_non_pos):
                                    self.split_text(text[:i_tag_pos])

                                    self.tags_pos[-1].append(tag_pos.group())
                                    self.tags_all[-1].append(tag_pos.group())

                                    text = text[i_tag_pos + len(tag_pos.group()):]
                                elif (tag_pos and tag_non_pos and i_tag_pos > i_tag_non_pos or
                                      not tag_pos and tag_non_pos):
                                    self.split_text(text[:i_tag_non_pos])

                                    self.tags_all[-1].append(tag_non_pos.group())
                                    self.tags_non_pos[-1].append(tag_non_pos.group())

                                    text = text[i_tag_non_pos + len(tag_non_pos.group()):]
                                else:
                                    self.split_text(text)

                                    break
                else:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            self.tokens_sentences_paras.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_all, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            sentences = wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                            lang = self.lang)

                            for sentence in sentences:
                                self.tokens_sentences_paras[-1].append(sentence.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and (re.match(re_tags_pos, text) or re.match(re_tags_non_pos, text)):
                                self.tokens_sentences_paras[0][0].insert(0, '')

                                self.tags_all.append([])
                                self.tags_pos.append([])
                                self.tags_non_pos.append([])

                            # Extract tags
                            while text:
                                tag_pos = re.search(re_tags_pos, text)
                                tag_non_pos = re.search(re_tags_non_pos, text)

                                if tag_pos:
                                    i_tag_pos = text.index(tag_pos.group())

                                if tag_non_pos:
                                    i_tag_non_pos = text.index(tag_non_pos.group())

                                if (tag_pos and tag_non_pos and i_tag_pos < i_tag_non_pos or
                                    tag_pos and not tag_non_pos):
                                    self.split_text(text[:i_tag_pos])

                                    self.tags_all[-1].append(tag_pos.group())
                                    self.tags_pos[-1].append(tag_pos.group())

                                    text = text[i_tag_pos + len(tag_pos.group()):]
                                elif (tag_pos and tag_non_pos and i_tag_pos > i_tag_non_pos or
                                      not tag_pos and tag_non_pos):
                                    self.split_text(text[:i_tag_non_pos])

                                    self.tags_all[-1].append(tag_non_pos.group())
                                    self.tags_non_pos[-1].append(tag_non_pos.group())

                                    text = text[i_tag_non_pos + len(tag_non_pos.group()):]
                                else:
                                    self.split_text(text)

                                    break

        # Record paragraph and sentence offsets
        for tokens_sentences in self.tokens_sentences_paras:
            self.para_offsets.append(len(self.tokens))

            for tokens in tokens_sentences:
                self.sentence_offsets.append(len(self.tokens))

                self.tokens.extend(tokens)

        if self.text_type[1] == 'tagged_pos':
            self.tags_non_pos = [[] for i in range(len(self.tokens))]
            self.tags_all = copy.deepcopy(self.tags_pos)
        elif self.text_type[1] == 'tagged_non_pos':
            self.tags_pos = [[] for i in range(len(self.tokens))]
            self.tags_all = copy.deepcopy(self.tags_non_pos)
        elif self.text_type[1] == 'untagged':
            self.tags_all = [[] for i in range(len(self.tokens))]
            self.tags_pos = [[] for i in range(len(self.tokens))]
            self.tags_non_pos = [[] for i in range(len(self.tokens))]

        # Remove whitespace around all tags
        self.tags_all = [[tag.strip() for tag in tags] for tags in self.tags_all]
        self.tags_pos = [[tag.strip() for tag in tags] for tags in self.tags_pos]
        self.tags_non_pos = [[tag.strip() for tag in tags] for tags in self.tags_non_pos]

    def tokenize_text(self, text):
        if text:
            tokens_sentences = wordless_text_processing.wordless_word_tokenize(self.main, text,
                                                                               lang = self.lang,
                                                                               keep_sentences = False)

            for i in range(len([token for tokens in tokens_sentences for token in tokens])):
                self.tags_all.append([])
                self.tags_pos.append([])
                self.tags_non_pos.append([])

    def split_text(self, text):
        if text:
            tokens = text.split()

            for i in range(len(tokens)):
                self.tags_all.append([])
                self.tags_pos.append([])
                self.tags_non_pos.append([])
