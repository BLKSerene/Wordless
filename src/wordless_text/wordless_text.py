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
    def __init__(self, main, file, flat_tokens = True):
        self.main = main
        self.lang = file['lang']
        self.text_type = file['text_type']

        self.offsets_paras = []
        self.offsets_sentences = []
        self.offsets_clauses = []

        if flat_tokens:
            self.tokens_hierarchical = [[[[]]]]
        else:
            self.tokens_hierarchical = []

        self.tokens_flat = []

        self.tags_all = []
        self.tags_pos = []
        self.tags_non_pos = []

        re_tags_all = wordless_matching.get_re_tags(main, tags = 'all')
        re_tags_pos = wordless_matching.get_re_tags(main, tags = 'pos')
        re_tags_non_pos = wordless_matching.get_re_tags(main, tags = 'non_pos')

        with open(file['path'], 'r', encoding = file['encoding']) as f:
            # Untokenized / Untagged
            if self.text_type == ('untokenized', 'untagged'):
                if flat_tokens:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            tokens = wordless_text_processing.wordless_word_tokenize(
                                main, text,
                                lang = self.lang,
                                flat_tokens = True
                            )

                            self.tokens_hierarchical[0][0][0].extend(tokens)
                else:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            tokens = wordless_text_processing.wordless_word_tokenize(
                                main, text,
                                lang = self.lang,
                                flat_tokens = False
                            )

                            self.tokens_hierarchical.append(tokens)

            # Untokenized / Tagged (Non-POS)
            elif self.text_type == ('untokenized', 'tagged_non_pos'):
                if flat_tokens:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            tokens = wordless_text_processing.wordless_word_tokenize(
                                main, text_no_tags,
                                lang = self.lang,
                                flat_tokens = True
                            )

                            self.tokens_hierarchical[0][0][0].extend(tokens)

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_non_pos, text):
                                self.tokens_hierarchical[0][0][0].insert(0, '')
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
                else:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            tokens = wordless_text_processing.wordless_word_tokenize(
                                main, text_no_tags,
                                lang = self.lang,
                                flat_tokens = False
                            )

                            self.tokens_hierarchical.append(tokens)

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_non_pos, text):
                                self.tokens_hierarchical[0][0][0].insert(0, '')
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
                if flat_tokens:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_hierarchical[0][0][0].extend(text.split())
                else:
                    for line in f:
                        text = line.rstrip()

                        if text:
                            self.tokens_hierarchical.append([])

                            for sentence in wordless_text_processing.wordless_sentence_split(main, text):
                                self.tokens_hierarchical[-1].append([])

                                for clause in wordless_text_processing.wordless_clause_split(main, sentence):
                                    self.tokens_hierarchical[-1][-1].append(clause.split())
            # Tokenized / Tagged (POS)
            elif self.text_type == ('tokenized', 'tagged_pos'):
                if flat_tokens:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_hierarchical[0][0][0].extend(text_no_tags.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_pos, text):
                                self.tokens_hierarchical[0][0][0].insert(0, '')
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
                            self.tokens_hierarchical.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_split(main, text_no_tags):
                                self.tokens_hierarchical[-1].append([])

                                for clause in wordless_text_processing.wordless_clause_split(main, sentence):
                                    self.tokens_hierarchical[-1][-1].append(clause.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_pos, text):
                                self.tokens_hierarchical[0][0][0].insert(0, '')
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
                if flat_tokens:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_hierarchical[0][0][0].extend(text_no_tags.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_non_pos, text):
                                self.tokens_hierarchical[0][0][0].insert(0, '')
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
                            self.tokens_hierarchical.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_non_pos, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_split(main, text_no_tags):
                                self.tokens_hierarchical[-1].append([])

                                for clause in wordless_text_processing.wordless_clause_split(main, sentence):
                                    self.tokens_hierarchical[-1][-1].append(clause.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and re.match(re_tags_non_pos, text):
                                self.tokens_hierarchical[0][0][0].insert(0, '')
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
                if flat_tokens:
                    for i, line in enumerate(f):
                        text = line.rstrip()

                        if text:
                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_all, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            self.tokens_hierarchical[0][0][0].extend(text_no_tags.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and (re.match(re_tags_pos, text) or re.match(re_tags_non_pos, text)):
                                self.tokens_hierarchical[0][0][0].insert(0, '')

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
                            self.tokens_hierarchical.append([])

                            # Replace all tags with a whitespace to ensure no words run together
                            text_no_tags = re.sub(re_tags_all, ' ', text)
                            text_no_tags = re.sub(r'\s+', ' ', text_no_tags)

                            for sentence in wordless_text_processing.wordless_sentence_split(main, text_no_tags):
                                self.tokens_hierarchical[-1].append([])

                                for clause in wordless_text_processing.wordless_clause_split(main, sentence):
                                    self.tokens_hierarchical[-1][-1].append(clause.split())

                            # Check if the first token in the text is a tag
                            if i == 0 and (re.match(re_tags_pos, text) or re.match(re_tags_non_pos, text)):
                                self.tokens_hierarchical[0][0][0].insert(0, '')

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

        # Paragraph, sentence and clause offsets
        for para in self.tokens_hierarchical:
            self.offsets_paras.append(len(self.tokens_flat))

            for sentence in para:
                self.offsets_sentences.append(len(self.tokens_flat))

                for clause in sentence:
                    self.offsets_clauses.append(len(self.tokens_flat))

                    self.tokens_flat.extend(clause)

        # Tags
        if self.text_type[1] == 'tagged_pos':
            self.tags_non_pos = [[] for i in range(len(self.tokens_flat))]
            self.tags_all = copy.deepcopy(self.tags_pos)
        elif self.text_type[1] == 'tagged_non_pos':
            self.tags_pos = [[] for i in range(len(self.tokens_flat))]
            self.tags_all = copy.deepcopy(self.tags_non_pos)
        elif self.text_type[1] == 'untagged':
            self.tags_all = [[] for i in range(len(self.tokens_flat))]
            self.tags_pos = [[] for i in range(len(self.tokens_flat))]
            self.tags_non_pos = [[] for i in range(len(self.tokens_flat))]

        # Remove whitespace around all tags
        self.tags_all = [[tag.strip() for tag in tags] for tags in self.tags_all]
        self.tags_pos = [[tag.strip() for tag in tags] for tags in self.tags_pos]
        self.tags_non_pos = [[tag.strip() for tag in tags] for tags in self.tags_non_pos]

    def tokenize_text(self, text):
        if text:
            tokens = wordless_text_processing.wordless_word_tokenize(self.main, text,
                                                                     lang = self.lang)

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
