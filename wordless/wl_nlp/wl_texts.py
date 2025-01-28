# ----------------------------------------------------------------------
# Wordless: NLP - Texts
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import copy
import os
import re

import bs4
from PyQt5.QtCore import QCoreApplication

from wordless.wl_nlp import wl_matching, wl_sentence_tokenization, wl_word_tokenization
from wordless.wl_utils import wl_misc

_tr = QCoreApplication.translate

RE_VIE_TOKENIZED = re.compile(r'(?<!^)_(?!$)')

def check_text(text):
    return (text if text is not None else '')

def check_texts(texts):
    return [check_text(text) for text in texts]

# Tokens
class Wl_Token(str):
    def __new__(cls, text, **kwargs):
        return str.__new__(cls, text)

    def __init__(
        self, text, lang = 'eng_us',
        syls = None,
        tag = None, tag_universal = None, content_function = None,
        lemma = None,
        head = None, dependency_relation = None, dependency_len = None,
        punc_mark = None
    ): # pylint: disable=unused-argument
        self.lang = lang
        self.syls = syls
        self.tag = tag
        self.tag_universal = tag_universal
        self.content_function = content_function
        self.lemma = lemma
        self.head = head
        self.dependency_relation = dependency_relation
        self.dependency_len = dependency_len
        self.punc_mark = punc_mark

    def __hash__(self):
        return hash(self.display_text())

    def __eq__(self, other):
        return self.display_text() == other.display_text()

    def display_text(self, punc_mark = False):
        if punc_mark:
            return f"{self}{(self.punc_mark or '')}{self.tag or ''}"
        else:
            return f"{self}{self.tag or ''}"

    def update_properties(self, token):
        self.lang = token.lang
        self.syls = token.syls
        self.tag = token.tag
        self.tag_universal = token.tag_universal
        self.content_function = token.content_function
        self.lemma = token.lemma
        self.head = token.head
        self.dependency_relation = token.dependency_relation
        self.dependency_len = token.dependency_len
        self.punc_mark = token.punc_mark

def to_tokens(
    texts, lang = 'eng_us',
    syls_tokens = None,
    tags = None, tags_universal = None, content_functions = None,
    lemmas = None,
    heads = None, dependency_relations = None, dependency_lens = None,
    punc_marks = None
):
    num_tokens = len(texts)

    texts = check_texts(texts)
    syls_tokens = syls_tokens or [None] * num_tokens
    tags = tags or [None] * num_tokens
    tags_universal = tags_universal or [None] * num_tokens
    content_functions = content_functions or [None] * num_tokens
    lemmas = lemmas or [None] * num_tokens
    heads = heads or [None] * num_tokens
    dependency_relations = dependency_relations or [None] * num_tokens
    dependency_lens = dependency_lens or [None] * num_tokens
    punc_marks = punc_marks or [None] * num_tokens

    return [
        Wl_Token(
            text, lang = lang,
            syls = syls_tokens[i],
            tag = tags[i], tag_universal = tags_universal[i], content_function = content_functions[i],
            lemma = lemmas[i],
            head = heads[i], dependency_relation = dependency_relations[i], dependency_len = dependency_lens[i],
            punc_mark = punc_marks[i]
        )
        for i, text in enumerate(texts)
    ]

def display_texts_to_tokens(main, display_texts, lang = 'eng_us'):
    re_tags = re.compile(wl_matching.get_re_tags(main, tag_type = 'body'))

    tags = [''.join(re_tags.findall(display_text)) for display_text in display_texts]
    texts = [re_tags.sub('', display_text) for display_text in display_texts]

    return to_tokens(texts, lang = lang, tags = tags)

def split_texts_properties(tokens):
    texts = []
    token_properties = []

    for token in tokens:
        texts.append(str(token))
        token_properties.append({
            'lang': token.lang,
            'syls': token.syls,
            'tag': token.tag,
            'tag_universal': token.tag_universal,
            'content_function': token.content_function,
            'lemma': token.lemma,
            'head': token.head,
            'dependency_relation': token.dependency_relation,
            'dependency_len': token.dependency_len,
            'punc_mark': token.punc_mark
        })

    return texts, token_properties

def combine_texts_properties(texts, token_properties):
    return [Wl_Token(text, **properties) for text, properties in zip(texts, token_properties)]

def to_token_texts(tokens):
    return [str(token) for token in tokens]

def to_display_texts(tokens, punc_mark = False):
    return [token.display_text(punc_mark = punc_mark) for token in tokens]

def set_token_text(token, text):
    tokens = [token]

    set_token_texts(tokens, [text])

    return tokens[0]

def set_token_texts(tokens, texts):
    _, token_properties = split_texts_properties(tokens)
    texts = check_texts(texts)

    for i, token in enumerate(combine_texts_properties(texts, token_properties)):
        tokens[i] = token

def has_token_properties(tokens, name):
    for token in tokens:
        if getattr(token, name) is not None:
            return True

    return False

def get_token_properties(tokens, name, convert_none = False):
    if convert_none:
        return [getattr(token, name) or '' for token in tokens]
    else:
        return [getattr(token, name) for token in tokens]

def set_token_properties(tokens, name, vals):
    if isinstance(vals, str) or vals is None:
        vals = [vals] * len(tokens)

    for token, val in zip(tokens, vals):
        setattr(token, name, val)

def update_token_properties(tokens, tokens_src):
    for token, token_src in zip(tokens, tokens_src):
        token.update_properties(token_src)

def clean_texts(texts):
    return [
        text_clean
        for text in texts
        if (text_clean := text.strip())
    ]

# Texts
class Wl_Text:
    def __init__(self, main, file):
        self.main = main
        self.lang = file['lang']
        self.tokenized = file['tokenized']
        self.tagged = file['tagged']

        self.tokens_multilevel = []
        # Profiler
        self.tokens_multilevel_with_puncs = []
        tags_tokens = []

        file_ext = os.path.splitext(file['path'])[1].lower()
        re_tags = re.compile(wl_matching.get_re_tags(self.main, tag_type = 'body'))

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
                # Replace all tags with a whitespace character to ensure that no words run together
                text_no_tags = re_tags.sub(' ', text)
                # Remove redundant whitespace characters so that sentences are split correctly
                text_no_tags = re.sub(r'\s{2}', ' ', text_no_tags)

                tokens = wl_word_tokenization.wl_word_tokenize(self.main, text_no_tags, lang = self.lang)

                self.tokens_multilevel.extend(tokens)

                # Extract tags
                text = self.check_tags_text_start(text)
                i_tag_end = 0

                for tag in re_tags.finditer(text):
                    tags_tokens = self.add_tags_tokenization(text[i_tag_end:tag.start()], tags_tokens)
                    tags_tokens[-1].append(tag.group())

                    i_tag_end = tag.end()

                # The last part of the text
                if (text := text[i_tag_end:]):
                    tags_tokens = self.add_tags_tokenization(text, tags_tokens)

                # Insert tags at the start of the text
                if self.tags_text_start and tags_tokens:
                    tags_tokens[0] = self.tags_text_start + tags_tokens[0]
            # Tokenized & Untagged
            elif self.tokenized and not self.tagged:
                for para in text.splitlines():
                    self.tokens_multilevel.append([])

                    if para:
                        for sentence in wl_sentence_tokenization.wl_sentence_split(self.main, para):
                            self.tokens_multilevel[-1].append([])

                            for sentence_seg in wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(
                                self.main,
                                sentence.split()
                            ):
                                self.tokens_multilevel[-1][-1].append(sentence_seg)
            # Tokenized & Tagged
            elif self.tokenized and self.tagged:
                text = self.check_tags_text_start(text)

                for para in text.splitlines():
                    self.tokens_multilevel.append([])

                    if para:
                        # Replace all tags with a whitespace to ensure no words run together
                        text_no_tags = re_tags.sub(' ', para)

                        for sentence in wl_sentence_tokenization.wl_sentence_split(self.main, text_no_tags):
                            self.tokens_multilevel[-1].append([])

                            for sentence_seg in wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(
                                self.main,
                                sentence.split()
                            ):
                                self.tokens_multilevel[-1][-1].append(sentence_seg)

                        # Extract tags
                        i_tag_end = 0

                        for tag in re_tags.finditer(para):
                            tags_tokens = self.add_tags_splitting(para[i_tag_end:tag.start()], tags_tokens)
                            tags_tokens[-1].append(tag.group())

                            i_tag_end = tag.end()

                        # The last part of the text
                        if (para := para[i_tag_end:]):
                            tags_tokens = self.add_tags_splitting(para, tags_tokens)

                # Insert tags at the start of the text
                if self.tags_text_start and tags_tokens:
                    tags_tokens[0] = self.tags_text_start + tags_tokens[0]

            # Add empty tags for untagged files
            if not self.tagged:
                tags_tokens.extend([None] * len(self.get_tokens_flat()))
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
                        tokens = wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(self.main, tokens)

                        self.tokens_multilevel[-1].append(tokens)
            # XML files not tokenized or XML tags unfound or XML tags unspecified
            else:
                text = soup.get_text()
                tokens = wl_word_tokenization.wl_word_tokenize(self.main, text, lang = self.lang)

                self.tokens_multilevel.extend(tokens)

            # Add empty tags
            tags_tokens.extend([None] * len(self.get_tokens_flat()))

        # Remove underscores in tokenized Vietnamese files
        if self.lang == 'vie' and self.tokenized:
            for para in self.tokens_multilevel:
                for sentence in para:
                    for i, sentence_seg in enumerate(sentence):
                        sentence[i] = [
                            RE_VIE_TOKENIZED.sub(' ', token)
                            for token in sentence_seg
                        ]

        # Remove whitespace around tags
        tags_tokens = [
            ''.join([tag_clean for tag in tags if (tag_clean := tag.strip())])
            for tags in tags_tokens
            if tags is not None
        ]

        i_tag = 0

        for para in self.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    len_sentence_seg = len(sentence_seg)

                    sentence[i] = to_tokens(
                        sentence_seg, self.lang,
                        tags = tags_tokens[i_tag : i_tag + len_sentence_seg]
                    )

                    i_tag += len_sentence_seg

        # Record number of tokens and types
        self.update_num_tokens()

        # Remove Wl_Main object from the text since it cannot be pickled
        del self.main

    # Check whether there are tags at the start of the text
    def check_tags_text_start(self, text):
        re_tag_text_start = re.compile(fr"\s*({wl_matching.get_re_tags(self.main, tag_type = 'body')})")
        self.tags_text_start = []

        while (re_result := re_tag_text_start.match(text)):
            tag = re_result.group()

            self.tags_text_start.append(tag)
            text = text[len(tag):]

        return text

    def add_tags_tokenization(self, text, tags):
        if (text := text.strip()):
            tokens = wl_word_tokenization.wl_word_tokenize_flat(
                self.main, text,
                lang = self.lang
            )

            tags.extend([[] for _ in tokens])

        return tags

    def add_tags_splitting(self, text, tags):
        if (text := text.strip()):
            tokens = text.split()

            tags.extend([[] for _ in tokens])

        return tags

    def update_num_tokens(self):
        self.num_tokens = len(self.get_tokens_flat())
        self.num_types = len(set(self.get_tokens_flat()))

    def get_tokens_flat(self):
        return list(wl_misc.flatten_list(self.tokens_multilevel))

    def set_tokens(self, tokens):
        i_token = 0

        for para in self.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, _ in enumerate(sentence_seg):
                        sentence_seg[i] = tokens[i_token]

                        i_token += 1

    def to_token_texts(self, flat = False):
        if flat:
            return to_token_texts(self.get_tokens_flat())
        else:
            return [
                [
                    [
                        [str(token) for token in sentence_seg]
                        for sentence_seg in sentence
                    ]
                    for sentence in para
                ]
                for para in self.tokens_multilevel
            ]

    def to_display_texts(self, punc_mark = False, flat = False):
        if flat:
            return to_display_texts(self.get_tokens_flat())
        else:
            return [
                [
                    [
                        [token.display_text(punc_mark = punc_mark) for token in sentence_seg]
                        for sentence_seg in sentence
                    ]
                    for sentence in para
                ]
                for para in self.tokens_multilevel
            ]

    def set_token_texts(self, texts):
        # Calculate head references
        if self.has_token_properties('head'):
            head_refs = []

            for i_para, para in enumerate(self.tokens_multilevel):
                for i_sentence, sentence in enumerate(para):
                    for sentence_seg in sentence:
                        for token in sentence_seg:
                            head = token.head
                            head_ref = None

                            for i_sentence_seg, sentence_seg in enumerate(sentence):
                                for i_token, token in enumerate(sentence_seg):
                                    if head is token:
                                        head_ref = (i_para, i_sentence, i_sentence_seg, i_token)

                                        break

                                if head_ref:
                                    break

                            if head_ref:
                                head_refs.append(head_ref)
                            else:
                                head_refs.append(None)

        tokens = self.get_tokens_flat()
        set_token_texts(tokens, texts)

        self.set_tokens(tokens)

        # Update head references
        if self.has_token_properties('head'):
            i_token = 0

            for para in self.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for token in sentence_seg:
                            refs = head_refs[i_token]

                            if refs is not None:
                                token.head = self.tokens_multilevel[refs[0]][refs[1]][refs[2]][refs[3]]

                            i_token += 1

    def has_token_properties(self, name):
        return has_token_properties(self.get_tokens_flat(), name)

    def get_token_properties(self, name, flat = False):
        if flat:
            return get_token_properties(self.get_tokens_flat(), name)
        else:
            return [
                [
                    [
                        [getattr(token, name) for token in sentence_seg]
                        for sentence_seg in sentence
                    ]
                    for sentence in para
                ]
                for para in self.tokens_multilevel
            ]

    def set_token_properties(self, name, vals):
        if isinstance(vals, str) or vals is None:
            vals = [vals] * self.num_tokens

        i_val = 0

        for para in self.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for token in sentence_seg:
                        setattr(token, name, vals[i_val])

                        i_val += 1

    def update_token_properties(self, tokens):
        i_token = 0

        for para in self.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for token in sentence_seg:
                        token.update_properties(tokens[i_token])

                        i_token += 1

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

class Wl_Text_Ref(Wl_Text):
    def __init__(self, main, file): # pylint: disable=super-init-not-called
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
                text_no_tags = re_tags.sub(' ', text)
                tokens = wl_word_tokenization.wl_word_tokenize_flat(self.main, text_no_tags, lang = self.lang)

                self.tokens_multilevel[0][0][0].extend(tokens)
            # Tokenized & Untagged
            elif self.tokenized and not self.tagged:
                self.tokens_multilevel[0][0][0].extend(text.split())
            # Tokenized & Tagged
            elif self.tokenized and self.tagged:
                # Replace all tags with a whitespace to ensure no words run together
                text_no_tags = re_tags.sub(' ', text)

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
                            RE_VIE_TOKENIZED.sub(' ', token)
                            for token in sentence_seg
                        ]

        # Remove empty tokens and whitespace around tokens
        self.tokens_multilevel[0][0][0] = clean_texts(self.tokens_multilevel[0][0][0])
        self.tokens_multilevel[0][0][0] = to_tokens(self.tokens_multilevel[0][0][0], self.lang)

        self.num_tokens = len(self.get_tokens_flat())

        # Remove Wl_Main object from the text since it cannot be pickled
        del self.main

class Wl_Text_Total(Wl_Text):
    def __init__(self, texts): # pylint: disable=super-init-not-called
        # Set language for the combined text only if all texts are in the same language
        if len({text.lang for text in texts}) == 1:
            self.lang = texts[0].lang
        else:
            self.lang = 'other'

        self.tagged = any((text.tagged for text in texts))

        self.tokens_multilevel = [
            copy.deepcopy(para)
            for text in texts
            for para in text.tokens_multilevel
        ]
        self.tokens_multilevel_with_puncs = [
            copy.deepcopy(para)
            for text in texts
            for para in text.tokens_multilevel_with_puncs
        ]

        self.update_num_tokens()
