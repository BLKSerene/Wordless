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
import itertools
import re

import nltk

from wordless_text import wordless_text_processing, wordless_text_utils

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

# Search Terms
def match_ngrams(main, search_terms, tokens,
                 lang, text_type, token_settings, search_settings):
    search_terms_matched = set()

    settings = copy.deepcopy(search_settings)

    re_tags_all = get_re_tags(main, tags = 'all')
    re_tags_pos = get_re_tags(main, tags = 'pos')
    re_tags_non_pos = get_re_tags(main, tags = 'non_pos')

    search_term_tokens = [search_term_token
                          for search_term in search_terms
                          for search_term_token in search_term.split()]

    if search_settings['use_regex']:
        regexes_matched = {search_term_token: set() for search_term_token in search_term_tokens}
        tokens_matched = {}
    else:
        tokens_matched = {search_term_token: set() for search_term_token in search_term_tokens}

    # Search Settings
    if settings['match_tags']:
        settings['match_inflected_forms'] = False

        settings['ignore_tags'] = settings['ignore_tags_tags']
        settings['ignore_tags_type'] = settings['ignore_tags_type_tags']

    # Token Settings
    if token_settings['use_tags']:
        settings['match_inflected_forms'] = False
        settings['match_tags'] = False

        if token_settings['ignore_tags_tags']:
            settings['ignore_tags'] = False
    else:
        if token_settings['ignore_tags']:
            if token_settings['ignore_tags_type'] == main.tr('all'):
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
                elif settings['ignore_tags_type'] == main.tr('non-POS'):
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
                if settings['ignore_tags_type'] == main.tr('all'):
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
                elif settings['ignore_tags_type'] == main.tr('non-POS'):
                    if text_type[1] in ['tagged_both', 'tagged_non_pos']:
                        tokens_searched = [re.sub(re_tags_non_pos, '', token) for token in tokens]
                    elif text_type[1] == 'tagged_pos':
                        tokens_searched = tokens
        else:
            tokens_searched = tokens

    if tokens_searched:
        if settings['use_regex']:
            for search_term_token in search_term_tokens:
                if settings['match_whole_words']:
                    regex = fr'(^|\s+){search_term_token}(\s+|$)'
                else:
                    regex = search_term_token

                if settings['ignore_case']:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for token, token_searched in zip(tokens, tokens_searched):
                    if re.search(regex, token_searched, flags = flags):
                        regexes_matched[search_term_token].add(token)
                        tokens_matched[token] = set()
        else:
            for search_term_token in search_term_tokens:
                regex = re.escape(search_term_token)

                if settings['match_whole_words']:
                    regex = fr'(^|\s+){regex}(\s+|$)'

                if settings['ignore_case']:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for token, token_searched in zip(tokens, tokens_searched):
                    if re.search(regex, token_searched, flags = flags):
                        tokens_matched[search_term_token].add(token)

        if settings['match_inflected_forms']:
            wordless_text_utils.check_lemmatizers(main, lang)

            lemmas_searched = wordless_text_processing.wordless_lemmatize(main, tokens_searched, lang, text_type)
            lemmas_matched = wordless_text_processing.wordless_lemmatize(main, list(tokens_matched), lang, text_type)

            for token_matched, lemma_matched in zip(list(tokens_matched), lemmas_matched):
                lemma_matched = re.escape(lemma_matched)
                lemma_matched = fr'(^|\s+){lemma_matched}(\s+|$)'

                if settings['ignore_case']:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for token, lemma_searched in zip(tokens, lemmas_searched):
                    if re.search(lemma_matched, lemma_searched, flags = flags):
                        tokens_matched[token_matched].add(token)

    if search_settings['use_regex']:
        for search_term in search_terms:
            search_term_tokens_matched = []

            for search_term_token in search_term.split():
                search_term_tokens_matched.append(set())

                for regex_matched in regexes_matched[search_term_token]:
                    search_term_tokens_matched[-1].add(regex_matched)
                    search_term_tokens_matched[-1] |= set(tokens_matched[regex_matched])

            for item in itertools.product(*search_term_tokens_matched):
                search_terms_matched.add(item)
    else:
        for search_term in search_terms:
            search_term_tokens_matched = []

            for search_term_token in search_term.split():
                search_term_tokens_matched.append(set(tokens_matched[search_term_token]))

            for item in itertools.product(*search_term_tokens_matched):
                search_terms_matched.add(item)

    return search_terms_matched

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

# Context
def check_context(i, tokens, context_settings,
                  search_terms_inclusion, search_terms_exclusion):
    if context_settings['inclusion']['inclusion'] or context_settings['exclusion']['exclusion']:
        len_tokens = len(tokens)

        # Inclusion
        if context_settings['inclusion']['inclusion'] and search_terms_inclusion:
            inclusion_matched = False

            for search_term in search_terms_inclusion:
                if inclusion_matched:
                    break

                for j in range(context_settings['inclusion']['context_window_left'],
                               context_settings['inclusion']['context_window_right'] + 1):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            inclusion_matched = True

                            break
        else:
            inclusion_matched = True

        # Exclusion
        exclusion_matched = True

        if context_settings['exclusion']['exclusion'] and search_terms_exclusion:
            for search_term in search_terms_exclusion:
                if not exclusion_matched:
                    break

                for j in range(context_settings['exclusion']['context_window_left'],
                               context_settings['exclusion']['context_window_right'] + 1):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            exclusion_matched = False

                            break

        if inclusion_matched and exclusion_matched:
            return True
        else:
            return False
    else:
        return True
