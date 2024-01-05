# ----------------------------------------------------------------------
# Wordless: NLP - Texts
# Copyright (C) 2018-2024  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import os
import re

import bs4
from PyQt5.QtCore import QCoreApplication

from wordless.wl_nlp import wl_matching, wl_sentence_tokenization, wl_word_tokenization
from wordless.wl_utils import wl_misc

_tr = QCoreApplication.translate

RE_VIE_TOKENIZED = re.compile(r'(?<!^)_(?!$)')

class Wl_Text:
    def __init__(self, main, file):
        self.main = main
        self.lang = file['lang']
        self.tokenized = file['tokenized']
        self.tagged = file['tagged']

        self.tokens_multilevel = []
        self.tags = []

        file_ext = os.path.splitext(file['path'])[1].lower()
        re_tags = re.compile(wl_matching.get_re_tags(self.main, tag_type = 'body'))
        re_tags_start = re.compile(fr"\s*({wl_matching.get_re_tags(self.main, tag_type = 'body')})")

        if (
            file_ext == '.txt'
            # Treat untagged XML files as untagged text files
            or file_ext == '.xml' and not self.tagged
        ):
            with open(file['path'], 'r', encoding = file['encoding'], errors = 'replace') as f:
                text = f.read()

            # Untokenized & Untagged
            if not self.tokenized and not self.tagged:
                tokens = wl_word_tokenization.wl_word_tokenize(self.main, text, lang = self.lang)

                self.tokens_multilevel.extend(tokens)
            # Untokenized & Tagged
            elif not self.tokenized and self.tagged:
                # Replace all tags with a whitespace to ensure no words run together
                text_no_tags = re.sub(re_tags, ' ', text)

                tokens = wl_word_tokenization.wl_word_tokenize(self.main, text_no_tags, lang = self.lang)

                self.tokens_multilevel.extend(tokens)

                # Check if the first token in the text is a tag
                if re.match(re_tags_start, text):
                    # Check if the first paragraph is empty
                    if not self.tokens_multilevel[0]:
                        self.tokens_multilevel[0].append([[]])

                    self.tokens_multilevel[0][0][0].insert(0, '')
                    self.tags.append([])

                # Extract tags
                tag_end = 0

                for tag in re.finditer(re_tags, text):
                    self.add_tags_tokenization(text[tag_end:tag.start()])
                    self.tags[-1].append(tag.group())

                    tag_end = tag.end()

                # The last part of the text
                if (text := text[tag_end:]):
                    self.add_tags_tokenization(text)
            # Tokenized & Untagged
            elif self.tokenized and not self.tagged:
                for para in text.splitlines():
                    self.tokens_multilevel.append([])

                    if para:
                        for sentence in wl_sentence_tokenization.wl_sentence_split(self.main, para):
                            self.tokens_multilevel[-1].append([])

                            for sentence_seg in wl_sentence_tokenization.wl_sentence_seg_split(self.main, sentence):
                                self.tokens_multilevel[-1][-1].append(sentence_seg.split())
            # Tokenized & Tagged
            elif self.tokenized and self.tagged:
                for i, para in enumerate(text.splitlines()):
                    self.tokens_multilevel.append([])

                    if para:
                        # Replace all tags with a whitespace to ensure no words run together
                        text_no_tags = re.sub(re_tags, ' ', para)

                        for sentence in wl_sentence_tokenization.wl_sentence_split(self.main, text_no_tags):
                            self.tokens_multilevel[-1].append([])

                            for sentence_seg in wl_sentence_tokenization.wl_sentence_seg_split(self.main, sentence):
                                self.tokens_multilevel[-1][-1].append(sentence_seg.split())

                        # Check if the first token in the text is a tag
                        if i == 0 and re.match(re_tags_start, para):
                            # Check if the first paragraph is empty
                            if not self.tokens_multilevel[0]:
                                self.tokens_multilevel[0].append([[]])

                            self.tokens_multilevel[0][0][0].insert(0, '')

                            self.tags.append([])

                        # Extract tags
                        tag_end = 0

                        for tag in re.finditer(re_tags, para):
                            self.add_tags_splitting(para[tag_end:tag.start()])
                            self.tags[-1].append(tag.group())

                            tag_end = tag.end()

                        # The last part of the text
                        if (para := para[tag_end:]):
                            self.add_tags_splitting(para)

            # Add empty tags for untagged files
            if not self.tagged:
                self.tags.extend([[] for _ in wl_misc.flatten_list(self.tokens_multilevel)])
        elif file_ext == '.xml' and self.tagged:
            tags_para = []
            tags_sentence = []
            tags_word = []

            for _, level, opening_tag, _ in self.main.settings_custom['files']['tags']['xml_tag_settings']:
                if level == _tr('wl_texts', 'Paragraph'):
                    tags_para.append(opening_tag[1:-1])
                elif level == _tr('wl_texts', 'Sentence'):
                    tags_sentence.append(opening_tag[1:-1])
                elif level == _tr('wl_texts', 'Word'):
                    tags_word.append(opening_tag[1:-1])

            css_para = ','.join(tags_para)
            css_sentence = ','.join(tags_sentence)
            css_word = ','.join(tags_word)

            with open(file['path'], 'r', encoding = file['encoding'], errors = 'replace') as f:
                soup = bs4.BeautifulSoup(f.read(), features = 'lxml-xml')

            if (
                self.tokenized
                and (css_para and css_sentence and css_word)
                and (soup.select_one(css_para) and soup.select_one(css_sentence) and soup.select_one(css_word))
            ):
                for para in soup.select(css_para):
                    self.tokens_multilevel.append([])

                    for sentence in para.select(css_sentence):
                        tokens = [
                            word_clean
                            for word in sentence.select(css_word)
                            if (word_clean := word.get_text().strip())
                        ]

                        self.tokens_multilevel[-1].append(wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(self.main, tokens))
            # XML files not tokenized or XML tags unfound or XML tags unspecified
            else:
                text = soup.get_text()
                tokens = wl_word_tokenization.wl_word_tokenize(self.main, text, lang = self.lang)

                self.tokens_multilevel.extend(tokens)

            # Add empty tags
            self.tags.extend([[] for _ in wl_misc.flatten_list(self.tokens_multilevel)])

        # Remove underscores in tokenized Vietnamese files
        if self.lang == 'vie' and self.tokenized:
            for para in self.tokens_multilevel:
                for sentence in para:
                    for i, sentence_seg in enumerate(sentence):
                        sentence[i] = [
                            re.sub(RE_VIE_TOKENIZED, ' ', token)
                            for token in sentence_seg
                        ]

        # Remove whitespace around all tags
        self.tags = [
            [tag_clean for tag in tags if (tag_clean := tag.strip())]
            for tags in self.tags
        ]

        # Remove Wl_Main object from the text since it cannot be pickled
        del self.main

    def add_tags_tokenization(self, text):
        if (text := text.strip()):
            tokens = wl_word_tokenization.wl_word_tokenize_flat(
                self.main, text,
                lang = self.lang
            )

            self.tags.extend([[] for _ in tokens])

    def add_tags_splitting(self, text):
        if (text := text.strip()):
            tokens = text.split()

            self.tags.extend([[] for _ in tokens])

    def get_tokens_flat(self):
        return list(wl_misc.flatten_list(self.tokens_multilevel))

    def get_offsets(self):
        offsets_paras = []
        offsets_sentences = []
        offsets_sentence_segs = []
        num_tokens = 0

        for para in self.tokens_multilevel:
            offsets_paras.append(num_tokens)

            for sentence in para:
                offsets_sentences.append(num_tokens)

                for sentence_seg in sentence:
                    offsets_sentence_segs.append(num_tokens)

                    num_tokens += len(sentence_seg)

        return offsets_paras, offsets_sentences, offsets_sentence_segs

class Wl_Text_Ref():
    get_tokens_flat = Wl_Text.get_tokens_flat
    get_offsets = Wl_Text.get_offsets

    def __init__(self, main, file):
        self.main = main
        self.lang = file['lang']
        self.tokenized = file['tokenized']
        self.tagged = file['tagged']

        self.tokens_multilevel = [[[[]]]]

        file_ext = os.path.splitext(file['path'])[1].lower()

        if (
            file_ext == '.txt'
            # Treat untagged XML files as untagged text files
            or file_ext == '.xml' and not self.tagged
        ):
            with open(file['path'], 'r', encoding = file['encoding'], errors = 'replace') as f:
                text = f.read()

            re_tags = re.compile(wl_matching.get_re_tags(self.main, tag_type = 'body'))

            # Untokenized & Untagged
            if not self.tokenized and not self.tagged:
                tokens = wl_word_tokenization.wl_word_tokenize_flat(self.main, text, lang = self.lang)

                self.tokens_multilevel[0][0][0].extend(tokens)
            # Untokenized & Tagged
            elif not self.tokenized and self.tagged:
                # Replace all tags with a whitespace to ensure no words run together
                text_no_tags = re.sub(re_tags, ' ', text)
                tokens = wl_word_tokenization.wl_word_tokenize_flat(self.main, text_no_tags, lang = self.lang)

                self.tokens_multilevel[0][0][0].extend(tokens)
            # Tokenized & Untagged
            elif self.tokenized and not self.tagged:
                self.tokens_multilevel[0][0][0].extend(text.split())
            # Tokenized & Tagged
            elif self.tokenized and self.tagged:
                # Replace all tags with a whitespace to ensure no words run together
                text_no_tags = re.sub(re_tags, ' ', text)

                self.tokens_multilevel[0][0][0].extend(text_no_tags.split())
        elif file_ext == '.xml' and self.tagged:
            tags_word = []

            for _, level, opening_tag, _ in self.main.settings_custom['files']['tags']['xml_tag_settings']:
                if level == _tr('wl_texts', 'Word'):
                    tags_word.append(opening_tag[1:-1])

            css_word = ','.join(tags_word)

            with open(file['path'], 'r', encoding = file['encoding'], errors = 'replace') as f:
                soup = bs4.BeautifulSoup(f.read(), features = 'lxml-xml')

            if (
                self.tokenized
                and css_word
                and soup.select_one(css_word)
            ):
                for word in soup.select(css_word):
                    self.tokens_multilevel[0][0][0].append(word.get_text())
            # XML files not tokenized or XML tags unfound or XML tags unspecified
            else:
                text = soup.get_text()
                tokens = wl_word_tokenization.wl_word_tokenize_flat(self.main, text, lang = self.lang)

                self.tokens_multilevel[0][0][0].extend(tokens)

        # Remove underscores in tokenized Vietnamese files
        if self.lang == 'vie' and self.tokenized:
            for para in self.tokens_multilevel:
                for sentence in para:
                    for i, sentence_seg in enumerate(sentence):
                        sentence[i] = [
                            re.sub(RE_VIE_TOKENIZED, ' ', token)
                            for token in sentence_seg
                        ]

        # Remove whitespace around tokens and empty tokens
        self.tokens_multilevel[0][0][0] = [
            token_clean
            for token in self.tokens_multilevel[0][0][0]
            if (token_clean := token.strip())
        ]

        # No need to extract tags
        self.tags = [[] for _ in self.tokens_multilevel[0][0][0]]

        # Remove Wl_Main object from the text since it cannot be pickled
        del self.main

class Wl_Text_Blank():
    get_tokens_flat = Wl_Text.get_tokens_flat
    get_offsets = Wl_Text.get_offsets
