#
# Wordless: Text - Matching
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

import nltk

from wordless_text import wordless_text_processing

def get_re_tags(main, tags):
    re_tags = []

    if tags == 'all':
        tags = main.settings_custom['tags']['tags_pos'] + main.settings_custom['tags']['tags_non_pos']
    elif tags == 'pos':
        tags = main.settings_custom['tags']['tags_pos']
    elif tags == 'non_pos':
        tags = main.settings_custom['tags']['tags_non_pos']

    tags_opening = [re.escape(tag_opening[0])
                    for tag_opening, _ in (main.settings_custom['tags']['tags_pos'] +
                                           main.settings_custom['tags']['tags_non_pos'])]

    for tag_opening, tag_closing in tags:
        tag_opening = re.escape(tag_opening)
        tag_closing = re.escape(tag_closing)

        tag_opening_first = re.escape(tag_opening[0])
        tag_closing_last = re.escape(tag_opening[-1])

        if tag_closing:
            re_tags.append(fr'\s*{tag_opening}[^{tag_opening_first}{tag_closing_last}]+?{tag_closing}')
        else:
            re_tags.append(fr"\s*{tag_opening}[^{tag_opening_first}]+?(?=\s+|$|{'|'.join(tags_opening)})")

    return '|'.join(re_tags)

def match_ngrams(main, search_terms, tokens,
                 lang, text_type, token_settings, search_settings):
    tokens_searched = []
    ngrams_matched = set()

    settings = copy.deepcopy(search_settings)
    search_terms = [search_term.split() for search_term in search_terms]
    re_tags_all = get_re_tags(main, tags = 'all')
    re_tags_pos = get_re_tags(main, tags = 'pos')
    re_tags_non_pos = get_re_tags(main, tags = 'non_pos')

    # Search Settings
    if settings['match_tags']:
        settings['match_inflected_forms'] = False

        settings['ignore_tags'] = settings['ignore_tags_match_tags']
        settings['ignore_tags_type'] = settings['ignore_tags_type_match_tags']

    # Token Settings
    if token_settings['tags_only']:
        settings['match_inflected_forms'] = False
        settings['match_tags'] = False

        if token_settings['ignore_tags_tags_only']:
            settings['ignore_tags'] = False
    else:
        if token_settings['ignore_tags']:
            if token_settings['ignore_tags_type'] == main.tr('All'):
                settings['ignore_tags'] = False
                settings['match_tags'] = False

    # Match Tags Only & Ignore Tags
    if settings['match_tags']:
        if settings['ignore_tags']:
            if text_type[1] == 'untagged':
                tokens_searched = []
            else:
                if settings['ignore_tags_type'] == main.tr('POS'):
                    if text_type[1] in ['tagged_both', 'tagged_non_pos']:
                        tokens_searched = [''.join(re.findall(re_tags_non_pos, token)) for token in tokens]
                    elif text_type[1] == 'tagged_pos':
                        tokens_searched = []
                elif settings['ignore_tags_type'] == main.tr('Non-POS'):
                    if text_type[1] in ['tagged_both', 'tagged_pos']:
                        tokens_searched = [''.join(re.findall(re_tags_pos, token)) for token in tokens]
                    elif text_type[1] == 'tagged_non_pos':
                        tokens_searched = []
        else:
            if text_type[1] == 'untagged':
                tokens_searched = []
            elif text_type[1] == 'tagged_pos':
                tokens_searched = [''.join(re.findall(re_tags_pos, token)) for token in tokens]
            elif text_type[1] == 'tagged_non_pos':
                tokens_searched = [''.join(re.findall(re_tags_non_pos, token)) for token in tokens]
            elif text_type[1] == 'tagged_both':
                tokens_searched = [''.join(re.findall(re_tags_all, token)) for token in tokens]
    else:
        if settings['ignore_tags']:
            if text_type[1] == 'untagged':
                tokens_searched = tokens
            else:
                if settings['ignore_tags_type'] == main.tr('All'):
                    if text_type[1] == 'tagged_both':
                        tokens_searched = [re.sub(re_tags_all, '', token) for token in tokens]
                    elif text_type[1] == 'tagged_pos':
                        tokens_searched = [re.sub(re_tags_pos, '', token) for token in tokens]
                    elif text_type[1] == 'tagged_non_pos':
                        tokens_searched = [re.sub(re_tags_non_pos, '', token) for token in tokens]
                elif settings['ignore_tags_type'] == main.tr('POS'):
                    if text_type[1] in ['tagged_both', 'tagged_pos']:
                        tokens_searched = [re.sub(re_tags_pos, '', token) for token in tokens]
                    elif text_type[1] == 'tagged_non_pos':
                        tokens_searched = tokens
                elif settings['ignore_tags_type'] == main.tr('Non-POS'):
                    if text_type[1] in ['tagged_both', 'tagged_non_pos']:
                        tokens_searched = [re.sub(re_tags_non_pos, '', token) for token in tokens]
                    elif text_type[1] == 'tagged_pos':
                        tokens_searched = tokens
        else:
            tokens_searched = tokens

    if tokens_searched:
        if settings['use_regex']:
            for ngram_search in search_terms:
                len_ngram_search = len(ngram_search)

                if settings['match_whole_word']:
                    ngram_search = [fr'(^|\s+){token}(\s+|$)' for token in ngram_search]

                if settings['ignore_case']:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for ngram_text, ngram_text_searched in zip(nltk.ngrams(tokens, len_ngram_search),
                                                           nltk.ngrams(tokens_searched, len_ngram_search)):
                    ngram_matched = True

                    for token_search, token_text in zip(ngram_search, ngram_text_searched):
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

                for ngram_text, ngram_text_searched in zip(nltk.ngrams(tokens, len_ngram_search),
                                                           nltk.ngrams(tokens_searched, len_ngram_search)):
                    matched = True

                    for token_search, token_text in zip(ngram_search, ngram_text_searched):
                        if not re.search(token_search, token_text, flags = flags):
                            matched = False

                            break

                    if matched:
                        ngrams_matched.add(ngram_text)

        if settings['match_inflected_forms']:
            tokens_text_lemma = wordless_text_processing.wordless_lemmatize(main, tokens_searched, lang, text_type)
            ngrams_matched_lemma = [wordless_text_processing.wordless_lemmatize(main, ngram, lang, text_type)
                                    for ngram in ngrams_matched | set([tuple(search_term) for search_term in search_terms])]

            for ngram_matched_lemma in ngrams_matched_lemma:
                len_ngram_matched_lemma = len(ngram_matched_lemma)

                ngram_matched_lemma = [re.escape(token) for token in ngram_matched_lemma]
                ngram_matched_lemma = [fr'(^|\s+){token}(\s+|$)' for token in ngram_matched_lemma]

                if settings['ignore_case']:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for (ngram_text, ngram_text_searched, ngram_text_lemma) in zip(nltk.ngrams(tokens, len_ngram_matched_lemma),
                                                                               nltk.ngrams(tokens_searched, len_ngram_matched_lemma),
                                                                               nltk.ngrams(tokens_text_lemma, len_ngram_matched_lemma)):
                    matched = True

                    for token_text_lemma, token_matched_lemma in zip(ngram_text_lemma, ngram_matched_lemma):
                        if not re.search(token_matched_lemma, token_text_lemma, flags = flags):
                            matched = False

                            break

                    if matched:
                        ngrams_matched.add(ngram_text)

    return ngrams_matched

def match_search_terms(main, tokens,
                       lang, text_type, token_settings, search_settings):
    if ('search_settings' in search_settings and search_settings['search_settings'] or
        'search_settings' not in search_settings):
        if search_settings['multi_search_mode']:
            search_terms = search_settings['search_terms']
        else:
            if search_settings['search_term']:
                search_terms = [search_settings['search_term']]
            else:
                search_terms = []
    else:
        search_terms = []

    if search_terms:
        search_terms = match_ngrams(main, search_terms, tokens,
                                    lang, text_type, token_settings, search_settings)

    return search_terms

def match_search_terms_context(main, tokens,
                               lang, text_type, token_settings, context_settings):
    search_terms_inclusion = set()
    search_terms_exclusion = set()

    # Inclusion
    if context_settings['inclusion']['inclusion']:
        if context_settings['inclusion']['multi_search_mode']:
            search_terms = context_settings['search_terms']
        else:
            if context_settings['inclusion']['search_term']:
                search_terms = [context_settings['inclusion']['search_term']]
            else:
                search_terms = []

        if search_terms:
            search_terms_inclusion = match_ngrams(main, search_terms, tokens,
                                                  lang, text_type, token_settings, context_settings['inclusion'])

            for search_term in search_terms:
                search_terms_inclusion.add(tuple(search_term))

    # Exclusion
    if context_settings['exclusion']['exclusion']:
        if context_settings['exclusion']['multi_search_mode']:
            search_terms = context_settings['exclusion']['search_terms']
        else:
            if context_settings['exclusion']['search_term']:
                search_terms = [context_settings['exclusion']['search_term']]
            else:
                search_terms = []

        if search_terms:
            search_terms_exclusion = match_ngrams(main, search_terms, tokens,
                                                  lang, text_type, token_settings, context_settings['exclusion'])

            for search_term in search_terms:
                search_terms_exclusion.add(tuple(search_term))

    return search_terms_inclusion, search_terms_exclusion
