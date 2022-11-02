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
def check_search_terms(search_settings, search_enabled):
    search_terms = set()

    if search_enabled:
        if search_settings['multi_search_mode']:
            search_terms = set(search_settings['search_terms'])
        else:
            if search_settings['search_term']:
                search_terms.add(search_settings['search_term'])

    return search_terms

def check_search_settings(token_settings, search_settings):
    search_settings = copy.deepcopy(search_settings)

    # Search Settings
    if search_settings['match_without_tags']:
        search_settings['match_tags'] = False
    elif search_settings['match_tags']:
        search_settings['match_without_tags'] = False

        if not token_settings['ignore_tags'] and not token_settings['use_tags']:
            search_settings['match_inflected_forms'] = False

    # Token Settings
    if token_settings['ignore_tags'] or token_settings['use_tags']:
        search_settings['match_without_tags'] = False
        search_settings['match_tags'] = False

        if token_settings['use_tags']:
            search_settings['match_inflected_forms'] = False

    return search_settings

def match_tokens(
    main, search_terms, tokens,
    lang, tagged, settings
):
    search_results = set()

    # Process tokens to search
    tokens_search = tokens.copy()
    re_tags = get_re_tags(main, tag_type = 'body')

    if settings['match_without_tags'] and tagged:
        tokens_search = [re.sub(re_tags, '', token) for token in tokens]
    elif settings['match_tags']:
        if tagged:
            tokens_search = [''.join(re.findall(re_tags, token)) for token in tokens]
        else:
            tokens_search = []

    # Match tokens
    if tokens_search:
        re_match = re.fullmatch if settings['match_whole_words'] else re.search
        re_flags = 0 if settings['match_case'] else re.IGNORECASE

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
            lemmas_search = wl_lemmatization.wl_lemmatize(main, tokens_search, lang, tagged = tagged)
            lemmas_matched = wl_lemmatization.wl_lemmatize(main, set([*search_terms, *search_results]), lang, tagged = tagged)

            for lemma_matched in set(lemmas_matched):
                # Always match literal strings
                lemma_matched = re.escape(lemma_matched)

                for token, lemma_search in set(zip(tokens, lemmas_search)):
                    if re_match(lemma_matched, lemma_search, flags = re_flags):
                        search_results.add(token)

    return search_results

def match_ngrams(
    main, search_terms, tokens,
    lang, tagged, settings
):
    search_results = set()

    search_term_tokens = list({
        search_term_token
        for search_term in search_terms
        for search_term_token in search_term.split()
    })

    tokens_matched = {search_term_token: set() for search_term_token in search_term_tokens}

    # Process tokens to search
    tokens_search = tokens.copy()
    re_tags = get_re_tags(main, tag_type = 'body')

    if settings['match_without_tags'] and tagged:
        tokens_search = [re.sub(re_tags, '', token) for token in tokens]
    elif settings['match_tags']:
        if tagged:
            tokens_search = [''.join(re.findall(re_tags, token)) for token in tokens]
        else:
            tokens_search = []

    # Match n-grams
    if tokens_search:
        re_match = re.fullmatch if settings['match_whole_words'] else re.search
        re_flags = 0 if settings['match_case'] else re.IGNORECASE

        if settings['use_regex']:
            search_term_tokens_regex = search_term_tokens.copy()
        # Prevent special characters from being treated as regex
        else:
            search_term_tokens_regex = [re.escape(token) for token in search_term_tokens]

        for search_term_token in search_term_tokens_regex:
            for token, token_search in zip(tokens, tokens_search):
                if re_match(search_term_token, token_search, flags = re_flags):
                    tokens_matched[search_term_token].add(token)

        if settings['match_inflected_forms']:
            lemmas_search = wl_lemmatization.wl_lemmatize(main, tokens_search, lang, tagged = tagged)

            # Search for inflected forms of tokens in search results first
            for search_term_token, search_term_tokens_matched in copy.deepcopy(tokens_matched).items():
                lemmas_matched = wl_lemmatization.wl_lemmatize(main, search_term_tokens_matched, lang, tagged = tagged)

                for token_matched, lemma_matched in zip(search_term_tokens_matched, lemmas_matched):
                    # Always match literal strings
                    lemma_matched = re.escape(lemma_matched)

                    for token, lemma_search in set(zip(tokens, lemmas_search)):
                        if re_match(lemma_matched, lemma_search, flags = re_flags):
                            tokens_matched[search_term_token].add(token)

            lemmas_matched = wl_lemmatization.wl_lemmatize(main, search_term_tokens, lang, tagged = tagged)

            # Search for inflected forms of tokens in search terms
            for token_matched, lemma_matched in zip(search_term_tokens, lemmas_matched):
                # Always match literal strings
                lemma_matched = re.escape(lemma_matched)

                for token, lemma_search in set(zip(tokens, lemmas_search)):
                    if re_match(lemma_matched, lemma_search, flags = re_flags):
                        tokens_matched[token_matched].add(token)

    for search_term in search_terms:
        search_term_tokens_matched = []

        for search_term_token in search_term.split():
            search_term_tokens_matched.append(tokens_matched[search_term_token])

        for item in itertools.product(*search_term_tokens_matched):
            search_results.add(item)

    return search_results

def match_search_terms_tokens(
    main, tokens,
    lang, tagged,
    token_settings, search_settings
):
    search_terms = check_search_terms(search_settings, search_enabled = True)

    if search_terms:
        search_terms = match_tokens(
            main, search_terms, tokens,
            lang, tagged,
            check_search_settings(token_settings, search_settings)
        )

    return search_terms

def match_search_terms_ngrams(
    main, tokens,
    lang, tagged,
    token_settings, search_settings
):
    search_terms = check_search_terms(search_settings, search_enabled = True)

    if search_terms:
        search_terms = match_ngrams(
            main, search_terms, tokens,
            lang, tagged,
            check_search_settings(token_settings, search_settings)
        )

    return search_terms

# Context
def match_search_terms_context(
    main, tokens,
    lang, tagged,
    token_settings, context_settings
):
    # Inclusion
    search_terms_incl = check_search_terms(
        search_settings = context_settings['incl'],
        search_enabled = context_settings['incl']['incl']
    )

    if search_terms_incl:
        search_terms_incl = match_ngrams(
            main, search_terms_incl, tokens,
            lang, tagged,
            check_search_settings(token_settings, context_settings['incl'])
        )

    # Exclusion
    search_terms_excl = check_search_terms(
        search_settings = context_settings['excl'],
        search_enabled = context_settings['excl']['excl']
    )

    if search_terms_excl:
        search_terms_excl = match_ngrams(
            main, search_terms_excl, tokens,
            lang, tagged,
            check_search_settings(token_settings, context_settings['excl'])
        )

    return search_terms_incl, search_terms_excl

def check_context(
    i, tokens, context_settings,
    search_terms_incl, search_terms_excl
):
    if context_settings['incl']['incl'] or context_settings['excl']['excl']:
        len_tokens = len(tokens)

        # Inclusion
        if context_settings['incl']['incl'] and search_terms_incl:
            incl_matched = False

            for search_term in search_terms_incl:
                if incl_matched:
                    break

                for j in range(
                    context_settings['incl']['context_window_left'],
                    context_settings['incl']['context_window_right'] + 1
                ):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            incl_matched = True

                            break
        else:
            incl_matched = True

        # Exclusion
        excl_matched = True

        if context_settings['excl']['excl'] and search_terms_excl:
            for search_term in search_terms_excl:
                if not excl_matched:
                    break

                for j in range(
                    context_settings['excl']['context_window_left'],
                    context_settings['excl']['context_window_right'] + 1
                ):
                    if i + j < 0 or i + j > len_tokens - 1:
                        continue

                    if j != 0:
                        if tuple(tokens[i + j : i + j + len(search_term)]) == tuple(search_term):
                            excl_matched = False

                            break

        return bool(incl_matched and excl_matched)
    else:
        return True
