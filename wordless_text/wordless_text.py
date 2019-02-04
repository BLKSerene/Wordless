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

from wordless_text import wordless_matching, wordless_text_processing

class Wordless_Token(str):
    def __new__(cls, string, *args, **kwargs):
        return super().__new__(cls, string)

    def __init__(self, string, boundary = '', sentence_ending = False):
        self.boundary = boundary
        self.sentence_ending = sentence_ending

class Wordless_Text():
    def __init__(self, main, file):
        self.main = main
        self.lang = file['lang']
        self.text_type = file['text_type']

        self.paras = []
        self.sentences = []
        self.tokens_sentences = []
        self.tokens = []

        self.para_offsets = []
        self.sentence_offsets = []

        self.tags_all = []
        self.tags_pos = []
        self.tags_non_pos = []

        re_tags_all = wordless_matching.get_re_tags(main, tags = 'all')
        re_tags_pos = wordless_matching.get_re_tags(main, tags = 'pos')
        re_tags_non_pos = wordless_matching.get_re_tags(main, tags = 'non_pos')

        with open(file['path'], 'r', encoding = file['encoding']) as f:
            for i, line in enumerate(f):
                text = line.rstrip()

                if text:
                    self.paras.append(text)
                    self.para_offsets.append(len(self.tokens))

                    sentences = wordless_text_processing.wordless_sentence_tokenize(main, text,
                                                                                    lang = self.lang)

                    if self.text_type[0] == 'untokenized':
                        # Untokenized / Untagged
                        if self.text_type[1] == 'untagged':
                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text,
                                                                                                lang = self.lang):
                                self.tokenize_sentence(sentence)
                        # Untokenized / Tagged (Non-POS)
                        elif self.text_type[1] == 'tagged_non_pos':
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                                lang = self.lang):
                                self.tokenize_sentence(sentence)

                            for tag in re.findall(re_tags_non_pos, text):
                                i_tag = text.index(tag)

                                if i == 0 and i_tag == 0 and not self.tags_non_pos:
                                    self.tokens.insert(0, '')

                                    self.tags_non_pos.append([tag])
                                else:
                                    self.tokenize_text(text[:i_tag])

                                    self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.tokenize_text(text)
                    elif self.text_type[0] == 'tokenized':
                        # Tokenized / Untagged
                        if self.text_type[1] == 'untagged':
                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text,
                                                                                                lang = self.lang):
                                self.split_sentence(sentence)
                        # Tokenized / Tagged (POS)
                        elif self.text_type[1] == 'tagged_pos':
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                                lang = self.lang):
                                self.split_sentence(sentence)

                            for tag in re.findall(re_tags_pos, text):
                                i_tag = text.index(tag)

                                if i == 0 and i_tag == 0 and not self.tags_pos:
                                    self.tokens.insert(0, '')

                                    self.tags_pos.append([tag])
                                else:
                                    self.split_text(text[:i_tag])

                                    self.tags_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.split_text(text)
                        # Tokenized / Tagged (Non-POS)
                        elif self.text_type[1] == 'tagged_non_pos':
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                                lang = self.lang):
                                self.split_sentence(sentence)

                            for tag in re.findall(re_tags_non_pos, text):
                                i_tag = text.index(tag)

                                if i == 0 and i_tag == 0 and not self.tags_non_pos:
                                    self.tokens.insert(0, '')

                                    self.tags_non_pos.append([tag])
                                else:
                                    self.split_text(text[:i_tag])

                                    self.tags_non_pos[-1].append(tag)

                                text = text[i_tag + len(tag):]

                            # The last part of the text
                            if text:
                                self.split_text(text)
                        # Tokenized / Tagged (Both)
                        elif self.text_type[1] == 'tagged_both':
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_all, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_tokenize(main, text_no_tags,
                                                                                                lang = self.lang):
                                self.split_sentence(sentence)

                            while text:
                                tag_pos = re.search(re_tags_pos, text)
                                tag_non_pos = re.search(re_tags_non_pos, text)

                                if tag_pos:
                                    i_tag_pos = text.index(tag_pos.group())

                                if tag_non_pos:
                                    i_tag_non_pos = text.index(tag_non_pos.group())

                                if (tag_pos and tag_non_pos and i_tag_pos < i_tag_non_pos or
                                    tag_pos and not tag_non_pos):
                                    if i == 0 and i_tag_pos == 0 and not self.tags_all:
                                        self.tokens.insert(0, '')

                                        self.tags_all.append([tag_pos.group()])
                                        self.tags_pos.append([tag_pos.group()])
                                        self.tags_non_pos.append([])
                                    else:
                                        self.split_text(text[:i_tag_pos])

                                        self.tags_pos[-1].append(tag_pos.group())
                                        self.tags_all[-1].append(tag_pos.group())

                                    text = text[i_tag_pos + len(tag_pos.group()):]
                                elif (tag_pos and tag_non_pos and i_tag_pos > i_tag_non_pos or
                                      not tag_pos and tag_non_pos):
                                    if i == 0 and i_tag_non_pos == 0 and not self.tags_all:
                                        self.tokens.insert(0, '')

                                        self.tags_all.append([tag_non_pos.group()])
                                        self.tags_pos.append([])
                                        self.tags_non_pos.append([tag_non_pos.group()])
                                    else:
                                        self.split_text(text[:i_tag_non_pos])

                                        self.tags_all[-1].append(tag_non_pos.group())
                                        self.tags_non_pos[-1].append(tag_non_pos.group())

                                    text = text[i_tag_non_pos + len(tag_non_pos.group()):]
                                else:
                                    self.split_text(text)

                                    break

                    # Check if the first token is empty
                    if self.tokens[0] == '':
                        self.tokens_sentences[0].insert(0, '')

                    if self.text_type[1] == 'tagged_pos':
                        self.tags_all = copy.deepcopy(self.tags_pos)
                    elif self.text_type[1] == 'tagged_non_pos':
                        self.tags_all = copy.deepcopy(self.tags_non_pos)
                    elif self.text_type[1] == 'untagged':
                        self.tags_all = [[] for i in range(len(self.tokens))]
                        self.tags_pos = [[] for i in range(len(self.tokens))]
                        self.tags_non_pos = [[] for i in range(len(self.tokens))]

                    # Remove whitespace around all tags
                    self.tags_all = [[tag.strip() for tag in tags] for tags in self.tags_all]
                    self.tags_pos = [[tag.strip() for tag in tags] for tags in self.tags_pos]
                    self.tags_non_pos = [[tag.strip() for tag in tags] for tags in self.tags_non_pos]

    def tokenize_sentence(self, sentence):
        tokens = wordless_text_processing.wordless_word_tokenize(self.main, sentence, self.lang_code)

        self.sentences.append(sentence)
        self.sentence_offsets.append(len(self.tokens))

        self.tokens_sentences.append(tokens)
        self.tokens.extend(tokens)

    def split_sentence(self, sentence):
        tokens = sentence.split()

        self.sentences.append(sentence)
        self.sentence_offsets.append(len(self.tokens))

        self.tokens_sentences.append(tokens)
        self.tokens.extend(tokens)

    def tokenize_text(self, text):
        if text:
            tokens = wordless_text_processing.wordless_word_tokenize(self.main, text, self.lang_code)

            for i in range(len(tokens)):
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
