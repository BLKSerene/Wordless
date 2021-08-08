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
import os
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

        file_ext = os.path.splitext(file['path'])[1].lower()
        re_tags = re.compile(wl_matching.get_re_tags(main))
        re_tags_start = re.compile(fr'\s*({wl_matching.get_re_tags(main)})')

        len_sections = self.main.settings_custom['files']['misc']['read_files_in_chunks']
        
        if file_ext == '.txt':
            with open(file['path'], 'r', encoding = file['encoding'], errors = 'replace') as f:
                # Read files in chunks to reduce memory usage
                sections = wl_text_utils.to_sections_unequal(f.readlines(), len_sections)

            for i, section in enumerate(sections):
                text = ''.join(section)

                if text:
                    # Untokenized & Untagged
                    if self.tokenized == 'No' and self.tagged == 'No':
                        tokens = wl_word_tokenization.wl_word_tokenize(main, text, lang = self.lang)

                        self.tokens_multilevel.extend(tokens)
                    # Untokenized & Tagged
                    elif self.tokenized == 'No' and self.tagged == 'Yes':
                        # Replace all tags with a whitespace to ensure no words run together
                        text_no_tags = re.sub(re_tags, ' ', text)

                        tokens = wl_word_tokenization.wl_word_tokenize(main, text_no_tags, lang = self.lang)

                        self.tokens_multilevel.extend(tokens)

                        # Check if the first token in the text is a tag
                        if i == 0 and re.match(re_tags_start, text):
                            # Check if the first paragraph is empty
                            if not self.tokens_multilevel[0]:
                                self.tokens_multilevel[0].append([])

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
                        # Split text into paragraphs excluding the last empty one
                        paras = re.split(r'\n(?=.|\n)', text)

                        for para in paras:
                            self.tokens_multilevel.append([])

                            if para:
                                for sentence in wl_sentence_tokenization.wl_sentence_split(main, para):
                                    self.tokens_multilevel[-1].append(sentence.split())
                    # Tokenized & Tagged
                    elif self.tokenized == 'Yes' and self.tagged == 'Yes':
                        # Split text into paragraphs excluding the last empty one
                        paras = re.split(r'\n(?=.|\n)', text)

                        for j, para in enumerate(paras):
                            self.tokens_multilevel.append([])

                            if para:
                                # Replace all tags with a whitespace to ensure no words run together
                                text_no_tags = re.sub(re_tags, ' ', para)

                                for sentence in wl_sentence_tokenization.wl_sentence_split(main, text_no_tags):
                                    self.tokens_multilevel[-1].append(sentence.split())

                                # Check if the first token in the text is a tag
                                if i == 0 and j == 0 and re.match(re_tags_start, para):
                                    # Check if the first paragraph is empty
                                    if not self.tokens_multilevel[0]:
                                        self.tokens_multilevel[0].append([])

                                    self.tokens_multilevel[0][0].insert(0, '')

                                    self.tags.append([])

                                # Extract tags
                                for tag in re.findall(re_tags, para):
                                    i_tag = para.index(tag)

                                    self.split_text(para[:i_tag])
                                    self.tags[-1].append(tag)

                                    para = para[i_tag + len(tag):]

                                # The last part of the text
                                if para:
                                    self.split_text(para)

            # Add empty tags for untagged files
            if self.tagged == 'No':
                self.tags.extend([[] for i in wl_misc.flatten_list(self.tokens_multilevel)])
        elif file_ext == '.xml':
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

            with open(file['path'], 'r', encoding = file['encoding'], errors = 'replace') as f:
                soup = bs4.BeautifulSoup(f.read(), features = 'lxml-xml')

            tags_para = ','.join(tags_para)
            tags_sentence = ','.join(tags_sentence)
            tags_word = ','.join(tags_word)

            if ((tags_para and tags_sentence and tags_word) and
                (soup.select(tags_para) and soup.select(tags_sentence) and soup.select(tags_word))):
                for para in soup.select(tags_para):
                    self.tokens_multilevel.append([])

                    for sentence in para.select(tags_sentence):
                        self.tokens_multilevel[-1].append([])

                        for word in sentence.select(tags_word):
                            self.tokens_multilevel[-1][-1].append(word.get_text().strip())
            # XML tags unfound or unspecified
            else:
                text = soup.get_text()
                tokens = wl_word_tokenization.wl_word_tokenize(main, text, lang = self.lang)

                self.tokens_multilevel.extend(tokens)

            # Add empty tags
            self.tags.extend([[] for i in wl_misc.flatten_list(self.tokens_multilevel)])

        # Paragraph and sentence offsets
        for para in self.tokens_multilevel:
            self.offsets_paras.append(len(self.tokens_flat))

            for sentence in para:
                self.offsets_sentences.append(len(self.tokens_flat))

                self.tokens_flat.extend(sentence)
        
        # Remove whitespace around all tags
        self.tags = [[tag.strip() for tag in tags] for tags in self.tags]

    def tokenize_text(self, text):
        text = text.strip()

        if text:
            tokens = wl_word_tokenization.wl_word_tokenize(
                self.main, text,
                lang = self.lang
            )

            self.tags.extend([[] for i in wl_misc.flatten_list(tokens)])

    def split_text(self, text):
        text = text.strip()

        if text:
            tokens = text.split()

            self.tags.extend([[] for i in tokens])
