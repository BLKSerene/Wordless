#
# Wordless: Text
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import re

import bs4
import nltk

from wordless_text import wordless_text_processing

class Wordless_Text():
    def __init__(self, main, file, merge_puncs = False):
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

    def match_search_terms(self, search_terms, puncs,
                           ignore_case, match_inflected_forms, match_whole_word, use_regex):
        ngrams_matched = set()

        if puncs:
            tokens_text = self.tokens.copy()
        else:
            tokens_text = [token for token in self.tokens if [char for char in token if char.isalnum()]]

        search_terms = [wordless_text_processing.wordless_word_tokenize(self.main, search_term, self.lang_code)
                        for search_term in search_terms]

        if use_regex:
            for ngram_search in search_terms:
                len_ngram_search = len(ngram_search)

                if match_whole_word:
                    ngram_search = [fr'(^|\s){token}(\s|$)' for token in ngram_search]

                if ignore_case:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for ngram_text in nltk.ngrams(tokens_text, len_ngram_search):
                    ngram_matched = True

                    for token_search, token_text in zip(ngram_search, ngram_text):
                        if not re.search(token_search, token_text, flags = flags):
                            ngram_matched = False

                            break

                    if ngram_matched:
                        ngrams_matched.add(ngram_text)
        else:
            for ngram_search in search_terms:
                len_ngram_search = len(ngram_search)

                ngram_search = [re.escape(token) for token in ngram_search]

                if match_whole_word:
                    ngram_search = [fr'(^|\s){token}(\s|$)' for token in ngram_search]

                if ignore_case:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for ngram_text in nltk.ngrams(tokens_text, len_ngram_search):
                    matched = True

                    for token_search, token_text in zip(ngram_search, ngram_text):
                        if not re.search(token_search, token_text, flags = flags):
                            matched = False

                            break

                    if matched:
                        ngrams_matched.add(ngram_text)

        if match_inflected_forms:
            tokens_text_lemma = wordless_text_processing.wordless_lemmatize(self.main, tokens_text, self.lang_code)
            ngrams_matched_lemma = [wordless_text_processing.wordless_lemmatize(self.main, ngram, self.lang_code)
                                    for ngram in ngrams_matched | set([tuple(search_term) for search_term in search_terms])]

            for ngram_matched_lemma in ngrams_matched_lemma:
                len_ngram_matched_lemma = len(ngram_matched_lemma)

                ngram_matched_lemma = [re.escape(token) for token in ngram_matched_lemma]
                ngram_matched_lemma = [fr'(^|\s){token}(\s|$)' for token in ngram_matched_lemma]

                if ignore_case:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for (ngram_text, ngram_text_lemma) in zip(nltk.ngrams(tokens_text, len_ngram_matched_lemma),
                                                          nltk.ngrams(tokens_text_lemma, len_ngram_matched_lemma)):
                    matched = True

                    for token_text_lemma, token_matched_lemma in zip(ngram_text_lemma, ngram_matched_lemma):
                        if not re.search(token_matched_lemma, token_text_lemma, flags = flags):
                            matched = False

                            break

                    if matched:
                        ngrams_matched.add(ngram_text)

        return ngrams_matched
