# ----------------------------------------------------------------------
# Wordless: NLP - Matching
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
import itertools
import re

from PyQt5.QtCore import QCoreApplication

from wordless.wl_nlp import wl_lemmatization, wl_texts

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
        if type_ == _tr('wl_matching', 'Embedded'):
            tag_start, tag_name = split_tag_embedded(opening_tag)
            tag_start = re.escape(tag_start)

            # Wilcards
            if tag_type == 'body' and tag_name == '*':
                tags_embedded.append(fr'{tag_start}\S*(?=\s|$)')
            else:
                tags_embedded.append(fr'{tag_start}{re.escape(tag_name)}(?=\s|$)')
        elif type_ == _tr('wl_matching', 'Non-embedded'):
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
        if type_ == _tr('wl_matching', 'Embedded'):
            tag_start, tag_name = split_tag_embedded(opening_tag)
            tag_start = re.escape(tag_start)

            # Wilcards
            if tag_type == 'body' and tag_name == '*':
                tags_embedded.append(fr'\S*{tag_start}\S*(?=\s|$)')
            else:
                tags_embedded.append(fr'\S*{tag_start}{re.escape(tag_name)}(?=\s|$)')
        elif type_ == _tr('wl_matching', 'Non-embedded'):
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
    settings = copy.deepcopy(search_settings)

    # Search Settings
    if settings['match_without_tags']:
        settings['match_tags'] = False
    elif settings['match_tags']:
        settings['match_without_tags'] = False

        if not token_settings['ignore_tags'] and not token_settings['use_tags']:
            settings['match_inflected_forms'] = False

    # Match dependency relations
    if 'match_dependency_relations' in settings and settings['match_dependency_relations']:
        settings['match_inflected_forms'] = False
        settings['match_without_tags'] = False
        settings['match_tags'] = False

    # Token Settings
    if token_settings['ignore_tags'] or token_settings['use_tags']:
        settings['match_without_tags'] = False
        settings['match_tags'] = False

        if token_settings['use_tags']:
            settings['match_inflected_forms'] = False

    return settings

def match_tokens(
    main, search_terms, tokens,
    lang, settings
):
    search_terms = wl_texts.display_texts_to_tokens(main, search_terms, lang)
    search_results = set()

    # Process tokens
    tokens_search = copy.deepcopy(tokens)

    if settings['match_without_tags']:
        wl_texts.set_token_properties(tokens_search, 'tag', '')
    elif settings['match_tags']:
        wl_texts.set_token_texts(tokens_search, wl_texts.get_token_properties(tokens_search, 'tag'))
        wl_texts.set_token_properties(tokens_search, 'tag', '')

    # Match tokens
    if tokens_search:
        re_match = re.fullmatch if settings['match_whole_words'] else re.search
        re_flags = 0 if settings['match_case'] else re.IGNORECASE

        if settings['use_regex']:
            search_terms_regex = [search_term.display_text() for search_term in search_terms]
        # Prevent special characters from being treated as regex
        else:
            search_terms_regex = [re.escape(search_term.display_text()) for search_term in search_terms]

        # Match dependency relations
        if settings['match_dependency_relations']:
            dependency_relations = wl_texts.to_tokens(
                wl_texts.get_token_properties(tokens_search, 'dependency_relation'),
                lang = lang
            )

            for search_term in search_terms_regex:
                for dependency_relation in dependency_relations:
                    if re_match(search_term, dependency_relation.display_text(), flags = re_flags):
                        search_results.add(dependency_relation)
        else:
            for search_term in search_terms_regex:
                for token, token_search in zip(tokens, tokens_search):
                    if re_match(search_term, token_search.display_text(), flags = re_flags):
                        search_results.add(token)

            # Match inflected forms of search terms and search results
            if settings['match_inflected_forms']:
                lemmas_search = tokens_search
                lemmas_matched = list({*search_terms, *search_results})

                # Match both lemmas and tags
                wl_texts.set_token_texts(
                    lemmas_search,
                    wl_texts.get_token_properties(tokens_search, 'lemma', convert_none = True)
                )
                wl_texts.set_token_texts(
                    lemmas_matched,
                    wl_texts.get_token_properties(
                        wl_lemmatization.wl_lemmatize(main, lemmas_matched, lang),
                        'lemma',
                        convert_none = True
                    )
                )

                for lemma_matched in set(lemmas_matched):
                    # Always match literal strings
                    lemma_matched = wl_texts.set_token_text(lemma_matched, re.escape(lemma_matched))

                    for token, lemma_search in set(zip(tokens, lemmas_search)):
                        if re_match(lemma_matched.display_text(), lemma_search.display_text(), flags = re_flags):
                            search_results.add(token)

    return search_results

def match_ngrams(
    main, search_terms, tokens,
    lang, settings
):
    search_results = set()

    search_term_tokens = list({
        search_term_token
        for search_term in search_terms
        for search_term_token in search_term.split()
    })
    search_term_tokens = wl_texts.display_texts_to_tokens(main, search_term_tokens, lang)

    tokens_matched = {search_term_token: set() for search_term_token in search_term_tokens}

    # Process tokens
    tokens_search = copy.deepcopy(tokens)

    if settings['match_without_tags']:
        wl_texts.set_token_properties(tokens_search, 'tag', '')
    elif settings['match_tags']:
        wl_texts.set_token_texts(tokens_search, wl_texts.get_token_properties(tokens_search, 'tag'))
        wl_texts.set_token_properties(tokens_search, 'tag', '')

    # Match n-grams
    if tokens_search:
        re_match = re.fullmatch if settings['match_whole_words'] else re.search
        re_flags = 0 if settings['match_case'] else re.IGNORECASE

        for search_term_token in search_term_tokens:
            if settings['use_regex']:
                search_term_token_regex = search_term_token.display_text()
            # Prevent special characters from being treated as regex
            else:
                search_term_token_regex = re.escape(search_term_token.display_text())

            for token, token_search in zip(tokens, tokens_search):
                if re_match(search_term_token_regex, token_search.display_text(), flags = re_flags):
                    tokens_matched[search_term_token].add(token)

        if settings['match_inflected_forms']:
            lemmas_search = tokens_search

            # Match both lemmas and tags
            wl_texts.set_token_texts(
                lemmas_search,
                wl_texts.get_token_properties(tokens_search, 'lemma', convert_none = True)
            )

            # Search for inflected forms of tokens in search results first
            for search_term_token, search_term_tokens_matched in copy.deepcopy(tokens_matched).items():
                lemmas_matched = list(search_term_tokens_matched)

                wl_texts.set_token_texts(
                    lemmas_matched,
                    wl_texts.get_token_properties(
                        wl_lemmatization.wl_lemmatize(main, search_term_tokens_matched, lang),
                        'lemma',
                        convert_none = True
                    )
                )

                for token_matched, lemma_matched in zip(search_term_tokens_matched, lemmas_matched):
                    # Always match literal strings
                    lemma_matched = wl_texts.set_token_text(lemma_matched, re.escape(lemma_matched))

                    for token, lemma_search in set(zip(tokens, lemmas_search)):
                        if re_match(lemma_matched.display_text(), lemma_search.display_text(), flags = re_flags):
                            tokens_matched[search_term_token].add(token)

            lemmas_matched = copy.deepcopy(search_term_tokens)

            wl_texts.set_token_texts(
                lemmas_matched,
                wl_texts.get_token_properties(
                    wl_lemmatization.wl_lemmatize(main, search_term_tokens, lang),
                    'lemma',
                    convert_none = True
                )
            )

            # Search for inflected forms of tokens in search terms
            for token_matched, lemma_matched in zip(search_term_tokens, lemmas_matched):
                # Always match literal strings
                lemma_matched = wl_texts.set_token_text(lemma_matched, re.escape(lemma_matched))

                for token, lemma_search in set(zip(tokens, lemmas_search)):
                    if re_match(lemma_matched.display_text(), lemma_search.display_text(), flags = re_flags):
                        tokens_matched[token_matched].add(token)

    for search_term in search_terms:
        search_term_tokens_matched = []

        for search_term_token in wl_texts.display_texts_to_tokens(main, search_term.split(), lang):
            search_term_tokens_matched.append(tokens_matched[search_term_token])

        for item in itertools.product(*search_term_tokens_matched):
            search_results.add(item)

    return search_results

def match_search_terms_tokens(
    main, tokens,
    lang, token_settings, search_settings
):
    search_terms = check_search_terms(search_settings, search_enabled = True)

    if search_terms:
        search_terms = match_tokens(
            main, search_terms, tokens,
            lang, check_search_settings(token_settings, search_settings)
        )

    return search_terms

def match_search_terms_ngrams(
    main, tokens,
    lang, token_settings, search_settings
):
    search_terms = check_search_terms(search_settings, search_enabled = True)

    if search_terms:
        search_terms = match_ngrams(
            main, search_terms, tokens,
            lang, check_search_settings(token_settings, search_settings)
        )

    return search_terms

# Context
def match_search_terms_context(
    main, tokens,
    lang, token_settings, context_settings
):
    search_terms_incl = set()
    search_terms_excl = set()

    # Inclusion
    search_terms = check_search_terms(
        search_settings = context_settings['incl'],
        search_enabled = context_settings['incl']['incl']
    )

    if search_terms:
        search_terms_incl = match_ngrams(
            main, search_terms, tokens,
            lang, check_search_settings(token_settings, context_settings['incl'])
        )

    # Exclusion
    search_terms = check_search_terms(
        search_settings = context_settings['excl'],
        search_enabled = context_settings['excl']['excl']
    )

    if search_terms:
        search_terms_excl = match_ngrams(
            main, search_terms, tokens,
            lang, check_search_settings(token_settings, context_settings['excl'])
        )

    return search_terms_incl, search_terms_excl

def check_context(
    i, tokens, context_settings,
    search_terms_incl, search_terms_excl
):
    len_tokens = len(tokens)

    # Inclusion
    search_terms = check_search_terms(
        search_settings = context_settings['incl'],
        search_enabled = context_settings['incl']['incl']
    )

    # Search terms to be included found in texts
    if search_terms and search_terms_incl:
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
    # Search terms to be included not found in texts
    elif search_terms and not search_terms_incl:
        incl_matched = False
    # No search terms to be included
    elif not search_terms:
        incl_matched = True

    # Exclusion
    search_terms = check_search_terms(
        search_settings = context_settings['excl'],
        search_enabled = context_settings['excl']['excl']
    )

    # Search terms to be excluded found in texts
    if search_terms and search_terms_excl:
        excl_matched = True

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
    # Search terms to be excluded not found in texts
    elif search_terms and not search_terms_excl:
        excl_matched = True
    # No search term to be excluded
    elif not search_terms:
        excl_matched = True

    return bool(incl_matched and excl_matched)
