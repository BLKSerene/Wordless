# ----------------------------------------------------------------------
# Wordless: NLP - Matching
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

import copy
import itertools
import re

from PyQt5.QtCore import QCoreApplication

from wordless.wl_nlp import wl_lemmatization

_tr = QCoreApplication.translate

# Tags
def split_tag_embedded(tag):
    # e.g. _*
    if (re_tag := re.search(r'^(([^\w\s]|_)+)(\*)$', tag)) is None:
        re_tag = re.search(r'^(([^\w\s]|_)+)(\S*)$', tag)

    tag_start = re_tag.group(1)
    tag_name = re_tag.group(3)

    return tag_start, tag_name

def split_tag_non_embedded(tag):
    # e.g. <*>
    if (re_tag := re.search(r'^(([^\w\s]|_)+)(\*)(([^\w\s]|_)+)$', tag)) is None:
        re_tag = re.search(r'^(([^\w\s]|_)+)(.*?)(([^\w\s]|_)+)$', tag)

    if (tag_name := re_tag.group(3)):
        tag_start = re_tag.group(1)
        tag_end = re_tag.group(4)
    # Empty tag
    else:
        tag_start = tag[:len(tag) // 2]
        tag_end = tag[len(tag) // 2:]

    return tag_start, tag_name, tag_end

def get_re_tags(main, tag_type):
    tags_embedded = []
    tags_non_embedded = []

    for type_, _, opening_tag, _ in main.settings_custom['files']['tags'][f'{tag_type}_tag_settings']:
        if type_ == _tr('get_re_tags', 'Embedded'):
            tag_start, tag_name = split_tag_embedded(opening_tag)
            tag_start = re.escape(tag_start)

            # Wilcards
            if tag_type == 'body' and tag_name == '*':
                tags_embedded.append(fr'{tag_start}\S*(?=\s|$)')
            else:
                tags_embedded.append(fr'{tag_start}{re.escape(tag_name)}(?=\s|$)')
        elif type_ == _tr('get_re_tags', 'Non-embedded'):
            tag_start, tag_name, tag_end = split_tag_non_embedded(opening_tag)
            tag_start = re.escape(tag_start)
            tag_end = re.escape(tag_end)

            # Wilcards
            if tag_type == 'body' and tag_name == '*':
                tags_non_embedded.append(fr'{tag_start}/?.*?{tag_end}')
            else:
                tags_non_embedded.append(fr'{tag_start}/?{re.escape(tag_name)}{tag_end}')

    return '|'.join(tags_embedded + tags_non_embedded)

def get_re_tags_with_tokens(main, tag_type):
    tags_embedded = []
    tags_non_embedded = []

    for type_, _, opening_tag, closing_tag in main.settings_custom['files']['tags'][f'{tag_type}_tag_settings']:
        if type_ == _tr('get_re_tags_with_tokens', 'Embedded'):
            tag_start, tag_name = split_tag_embedded(opening_tag)
            tag_start = re.escape(tag_start)

            # Wilcards
            if tag_type == 'body' and tag_name == '*':
                tags_embedded.append(fr'\S*{tag_start}\S*(?=\s|$)')
            else:
                tags_embedded.append(fr'\S*{tag_start}{re.escape(tag_name)}(?=\s|$)')
        elif type_ == _tr('get_re_tags_with_tokens', 'Non-embedded'):
            tag_start, tag_name, tag_end = split_tag_non_embedded(opening_tag)
            tag_start = re.escape(tag_start)
            tag_end = re.escape(tag_end)
            opening_tag = re.escape(opening_tag)
            closing_tag = re.escape(closing_tag)

            # Wilcards
            if tag_type == 'body' and tag_name == '*':
                tags_non_embedded.append(fr'{tag_start}.*?{tag_end}.*?{tag_start}/.*?{tag_end}')
            else:
                tags_non_embedded.append(fr'{opening_tag}.*{closing_tag}')

    return '|'.join(tags_embedded + tags_non_embedded)

# Search Terms
def match_tokens(
    main, search_terms, tokens,
    lang, tokenized, tagged,
    token_settings, search_settings
):
    search_results = set()

    settings = copy.deepcopy(search_settings)
    re_tags = get_re_tags(main, tag_type = 'body')

    # Search Settings
    if settings['ignore_tags']:
        settings['match_tags'] = False
    elif settings['match_tags']:
        settings['match_inflected_forms'] = False
        settings['ignore_tags'] = False

    # Token Settings
    if token_settings['use_tags']:
        settings['match_inflected_forms'] = False

    if token_settings['ignore_tags'] or token_settings['use_tags']:
        settings['ignore_tags'] = False
        settings['match_tags'] = False

    # Process tokens to search
    tokens_search = tokens.copy()

    if settings['ignore_tags'] and tagged:
        tokens_search = [re.sub(re_tags, '', token) for token in tokens]
    elif settings['match_tags']:
        if tagged:
            tokens_search = [''.join(re.findall(re_tags, token)) for token in tokens]
        else:
            tokens_search = []

    # Match tokens
    if tokens_search:
        if settings['match_whole_words']:
            re_match = re.fullmatch
        else:
            re_match = re.search

        if settings['ignore_case']:
            re_flags = re.IGNORECASE
        else:
            re_flags = 0

        if settings['use_regex']:
            search_terms_regex = search_terms.copy()
        # Prevent special characters from being treated as regex
        else:
            search_terms_regex = [re.escape(search_term) for search_term in search_terms]

        for search_term in search_terms_regex:
            for token, token_search in zip(tokens, tokens_search):
                if re_match(search_term, token_search, flags = re_flags):
                    search_results.add(token)

        # Match inflected forms of search terms and search results
        if settings['match_inflected_forms']:
            lemmas_search = wl_lemmatization.wl_lemmatize(main, tokens_search, lang, tokenized, tagged)
            lemmas_matched = wl_lemmatization.wl_lemmatize(main, search_terms, lang, tokenized, tagged)

            for search_term, lemma_matched in zip([*search_terms, *search_results], lemmas_matched):
                # Always match literal strings
                lemma_matched = re.escape(lemma_matched)

                for token, lemma_search in zip(tokens, lemmas_search):
                    if re_match(lemma_matched, lemma_search, flags = re_flags):
                        search_results.add(token)

    return search_results

def match_ngrams(
    main, search_terms, tokens,
    lang, tokenized, tagged,
    token_settings, search_settings
):
    search_terms_matched = set()

    settings = copy.deepcopy(search_settings)
    re_tags = get_re_tags(main, tag_type = 'body')

    search_term_tokens = [
        search_term_token
        for search_term in search_terms
        for search_term_token in search_term.split()
    ]

    if search_settings['use_regex']:
        regexes_matched = {search_term_token: set() for search_term_token in search_term_tokens}
        tokens_matched = {}
    else:
        tokens_matched = {search_term_token: set() for search_term_token in search_term_tokens}

    # Search Settings
    if settings['ignore_tags']:
        settings['match_tags'] = False
    elif settings['match_tags']:
        settings['match_inflected_forms'] = False
        settings['ignore_tags'] = False

    # Token Settings
    if token_settings['use_tags']:
        settings['match_inflected_forms'] = False

    if token_settings['ignore_tags'] or token_settings['use_tags']:
        settings['ignore_tags'] = False
        settings['match_tags'] = False

    # Match tags only & Ignore tags
    if settings['match_tags']:
        if not tagged:
            tokens_searched = []
        else:
            tokens_searched = [''.join(re.findall(re_tags, token)) for token in tokens]
    else:
        if settings['ignore_tags']:
            if not tagged:
                tokens_searched = tokens
            else:
                if tagged:
                    tokens_searched = [re.sub(re_tags, '', token) for token in tokens]
        else:
            tokens_searched = tokens

    if tokens_searched:
        if settings['use_regex']:
            for search_term_token in search_term_tokens:
                if settings['match_whole_words']:
                    regex = fr'^{search_term_token}$'
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
                    regex = fr'^{regex}$'

                if settings['ignore_case']:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for token, token_searched in zip(tokens, tokens_searched):
                    if re.search(regex, token_searched, flags = flags):
                        tokens_matched[search_term_token].add(token)

        if settings['match_inflected_forms']:
            lemmas_searched = wl_lemmatization.wl_lemmatize(main, tokens_searched, lang, tokenized, tagged)
            lemmas_matched = wl_lemmatization.wl_lemmatize(main, list(tokens_matched), lang, tokenized, tagged)

            for token_matched, lemma_matched in zip(list(tokens_matched), lemmas_matched):
                lemma_matched = re.escape(lemma_matched)
                lemma_matched = fr'^{lemma_matched}$'

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

def check_search_terms(search_settings):
    if (
        'search_settings' in search_settings and search_settings['search_settings']
        or 'search_settings' not in search_settings
    ):
        if search_settings['multi_search_mode']:
            search_terms = search_settings['search_terms']
        else:
            if search_settings['search_term']:
                search_terms = [search_settings['search_term']]
            else:
                search_terms = []
    else:
        search_terms = []

    return search_terms

def match_search_terms_tokens(
    main, tokens,
    lang, tokenized, tagged,
    token_settings, search_settings
):
    search_terms = check_search_terms(search_settings)

    if search_terms:
        search_terms = match_tokens(
            main, search_terms, tokens,
            lang, tokenized, tagged,
            token_settings, search_settings
        )

    return search_terms

def match_search_terms(
    main, tokens,
    lang, tokenized, tagged,
    token_settings, search_settings
):
    if (
        'search_settings' in search_settings and search_settings['search_settings']
        or 'search_settings' not in search_settings
    ):
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
        search_terms = match_ngrams(
            main, search_terms, tokens,
            lang, tokenized, tagged,
            token_settings, search_settings
        )

    return search_terms

def match_search_terms_context(
    main, tokens,
    lang, tokenized, tagged,
    token_settings, context_settings
):
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
            search_terms_inclusion = match_ngrams(
                main, search_terms, tokens,
                lang, tokenized, tagged,
                token_settings, context_settings['inclusion']
            )

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
            search_terms_exclusion = match_ngrams(
                main, search_terms, tokens,
                lang, tokenized, tagged,
                token_settings, context_settings['exclusion']
            )

            for search_term in search_terms:
                search_terms_exclusion.add(tuple(search_term))

    return search_terms_inclusion, search_terms_exclusion

# Context
def check_context(
    i, tokens, context_settings,
    search_terms_inclusion, search_terms_exclusion
):
    if context_settings['inclusion']['inclusion'] or context_settings['exclusion']['exclusion']:
        len_tokens = len(tokens)

        # Inclusion
        if context_settings['inclusion']['inclusion'] and search_terms_inclusion:
            inclusion_matched = False

            for search_term in search_terms_inclusion:
                if inclusion_matched:
                    break

                for j in range(
                    context_settings['inclusion']['context_window_left'],
                    context_settings['inclusion']['context_window_right'] + 1
                ):
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

                for j in range(
                    context_settings['exclusion']['context_window_left'],
                    context_settings['exclusion']['context_window_right'] + 1
                ):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            exclusion_matched = False

                            break

        return bool(inclusion_matched and exclusion_matched)
    else:
        return True
