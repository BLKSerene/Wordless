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

from wl_nlp import wl_lemmatization

def get_re_tags(main):
    tags_embedded = []
    tags_non_embedded = []

    for tag_type, _, tag_opening in main.settings_custom['tags']['tags_body']:
        if tag_type == main.tr('Embedded'):
            tag_opening = re.escape(tag_opening)

            tags_embedded.append(fr'{tag_opening}[^{tag_opening}]+?(?=\s|$)')
        elif tag_type == main.tr('Non-embedded'):
            tags_opening = re.split(r'[\w*]+', tag_opening)
            tag_opening_start = re.escape(tags_opening[0])
            tag_opening_end = re.escape(tags_opening[-1])

            tags_non_embedded.append(fr'{tag_opening_start}/?[^{tag_opening_end}]*?{tag_opening_end}')

    return '|'.join(tags_embedded + tags_non_embedded)

def get_re_tags_with_tokens(main, tag_type):
    tags_embedded = []
    tags_non_embedded = []

    for tag_type, _, tag_opening in main.settings_custom['tags'][f'tags_{tag_type}']:
        if tag_type == main.tr('Embedded'):
            tag_opening = re.escape(tag_opening)

            tags_embedded.append(fr'(?<=^|\s)[^{tag_opening}]+?{tag_opening}[^{tag_opening}]+?(?=\s|$)')
        elif tag_type == main.tr('Non-embedded'):
            # Closing tags
            re_non_punc = re.search(r'\w|\*', tag_opening)

            if re_non_punc:
                i_non_punc = re_non_punc.start()
            else:
                i_non_punc = 1

            tag_closing = f'{tag_opening[:i_non_punc]}/{tag_opening[i_non_punc:]}'

            tag_opening = re.escape(tag_opening)
            tag_closing = re.escape(tag_closing)

            tags_non_embedded.append(fr'{tag_opening}.*?{tag_closing}')

    return '|'.join(tags_embedded + tags_non_embedded)

# Search Terms
def match_ngrams(
    main, search_terms, tokens,
    lang, tokenized, tagged,
    token_settings, search_settings
):
    search_terms_matched = set()

    settings = copy.deepcopy(search_settings)
    re_tags = get_re_tags(main)

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
    if settings['match_tags']:
        settings['match_inflected_forms'] = False

    # Token Settings
    if token_settings['use_tags']:
        settings['match_inflected_forms'] = False
        settings['match_tags'] = False

    # Match tags only & Ignore tags
    if settings['match_tags']:
        if tagged == 'No':
            tokens_searched = []
        else:
            tokens_searched = [''.join(re.findall(re_tags, token)) for token in tokens]
    else:
        if settings['ignore_tags']:
            if tagged == 'No':
                tokens_searched = tokens
            else:
                if tagged == 'Yes':
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
