#
# Wordless: Matching
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import re

import nltk

from wordless_text import wordless_text_processing

def match_ngrams(main, search_terms, tokens, lang_code, settings):
    ngrams_matched = set()

    if settings['use_regex']:
        for ngram_search in search_terms:
            len_ngram_search = len(ngram_search)

            if match_whole_word:
                ngram_search = [fr'(^|\s+){token}(\s+|$)' for token in ngram_search]

            if settings['ignore_case']:
                flags = re.IGNORECASE
            else:
                flags = 0

            for ngram_text in nltk.ngrams(tokens, len_ngram_search):
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

            if settings['match_whole_word']:
                ngram_search = [fr'(^|\s+){token}(\s+|$)' for token in ngram_search]

            if settings['ignore_case']:
                flags = re.IGNORECASE
            else:
                flags = 0

            for ngram_text in nltk.ngrams(tokens, len_ngram_search):
                matched = True

                for token_search, token_text in zip(ngram_search, ngram_text):
                    if not re.search(token_search, token_text, flags = flags):
                        matched = False

                        break

                if matched:
                    ngrams_matched.add(ngram_text)

    if settings['match_inflected_forms']:
        tokens_text_lemma = wordless_text_processing.wordless_lemmatize(main, tokens, lang_code)
        ngrams_matched_lemma = [wordless_text_processing.wordless_lemmatize(main, ngram, lang_code)
                                for ngram in ngrams_matched | set([tuple(search_term) for search_term in search_terms])]

        for ngram_matched_lemma in ngrams_matched_lemma:
            len_ngram_matched_lemma = len(ngram_matched_lemma)

            ngram_matched_lemma = [re.escape(token) for token in ngram_matched_lemma]
            ngram_matched_lemma = [fr'(^|\s+){token}(\s+|$)' for token in ngram_matched_lemma]

            if settings['ignore_case']:
                flags = re.IGNORECASE
            else:
                flags = 0

            for (ngram_text, ngram_text_lemma) in zip(nltk.ngrams(tokens, len_ngram_matched_lemma),
                                                      nltk.ngrams(tokens_text_lemma, len_ngram_matched_lemma)):
                matched = True

                for token_text_lemma, token_matched_lemma in zip(ngram_text_lemma, ngram_matched_lemma):
                    if not re.search(token_matched_lemma, token_text_lemma, flags = flags):
                        matched = False

                        break

                if matched:
                    ngrams_matched.add(ngram_text)

    return ngrams_matched

def match_search_terms(main, tokens, lang_code, settings):
    if settings['multi_search_mode']:
        search_terms = settings['search_terms']
    else:
        search_terms = [settings['search_term']]

    search_terms = [wordless_text_processing.wordless_word_tokenize(main, search_term, lang_code)
                    for search_term in search_terms]

    search_terms = match_ngrams(main, search_terms, tokens, lang_code, settings)

    return search_terms

def match_search_terms_context(main, tokens, lang_code, settings):
    search_terms_inclusion = set()
    search_terms_exclusion = set()

    # Inclusion
    if settings['inclusion']['inclusion']:
        if settings['inclusion']['multi_search_mode']:
            search_terms = settings['search_terms']
        else:
            if settings['inclusion']['search_term']:
                search_terms = [settings['inclusion']['search_term']]
            else:
                search_terms = []

        if search_terms:
            search_terms = [wordless_text_processing.wordless_word_tokenize(main, search_term, lang_code)
                            for search_term in search_terms]

            search_terms_inclusion = match_ngrams(main, search_terms, tokens, lang_code, settings['inclusion'])

            for search_term in search_terms:
                search_terms_inclusion.add(tuple(search_term))

    # Exclusion
    if settings['exclusion']['exclusion']:
        if settings['exclusion']['multi_search_mode']:
            search_terms = settings['exclusion']['search_terms']
        else:
            if settings['exclusion']['search_term']:
                search_terms = [settings['exclusion']['search_term']]
            else:
                search_terms = []

        if search_terms:
            search_terms = [wordless_text_processing.wordless_word_tokenize(main, search_term, lang_code)
                           for search_term in search_terms]

            search_terms_exclusion = match_ngrams(main, search_terms, tokens, lang_code, settings['exclusion'])

            for search_term in search_terms:
                search_terms_exclusion.add(tuple(search_term))

    return search_terms_inclusion, search_terms_exclusion
