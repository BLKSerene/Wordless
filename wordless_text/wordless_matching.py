#
# Wordless: Matching
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
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
                 tagged, lang_code, search_settings):
    tokens_searched = []
    ngrams_matched = set()

    settings = copy.deepcopy(search_settings)
    search_terms = [search_term.split() for search_term in search_terms]
    re_tags_all = get_re_tags(main, tags = 'all')
    re_tags_pos = get_re_tags(main, tags = 'pos')
    re_tags_non_pos = get_re_tags(main, tags = 'non_pos')

    # Search Settings
    if settings['match_tags']:
        settings['ignore_tags'] = settings['ignore_tags_match_tags']
        settings['ignore_tags_type'] = settings['ignore_tags_type_match_tags']

    # Match Tags Only & Ignore Tags
    if search_settings['match_tags']:
        if search_settings['ignore_tags']:
            if tagged == main.tr('Untagged'):
                tokens_searched = []
            else:
                if search_settings['ignore_tags_type'] == main.tr('POS'):
                    if tagged in [main.tr('Tagged (Both)'), main.tr('Tagged (Non-POS)')]:
                        tokens_searched = [''.join(re.findall(re_tags_non_pos, token)) for token in tokens]
                    elif tagged == main.tr('Tagged (POS)'):
                        tokens_searched = []
                elif search_settings['ignore_tags_type'] == main.tr('Non-POS'):
                    if tagged in [main.tr('Tagged (Both)'), main.tr('Tagged (POS)')]:
                        tokens_searched = [''.join(re.findall(re_tags_pos, token)) for token in tokens]
                    elif tagged == main.tr('Tagged (Non-POS)'):
                        tokens_searched = []
        else:
            if tagged == main.tr('Untagged'):
                tokens_searched = []
            elif tagged == main.tr('Tagged (POS)'):
                tokens_searched = [''.join(re.findall(re_tags_pos, token)) for token in tokens]
            elif tagged == main.tr('Tagged (Non-POS)'):
                tokens_searched = [''.join(re.findall(re_tags_non_pos, token)) for token in tokens]
            elif tagged == main.tr('Tagged (Both)'):
                tokens_searched = [''.join(re.findall(re_tags_all, token)) for token in tokens]
    else:
        if search_settings['ignore_tags']:
            if tagged == main.tr('Untagged'):
                tokens_searched = tokens
            else:
                if search_settings['ignore_tags_type'] == main.tr('All'):
                    if tagged == main.tr('Tagged (Both)'):
                        tokens_searched = [re.sub(re_tags_all, '', token) for token in tokens]
                    elif tagged == main.tr('Tagged (POS)'):
                        tokens_searched = [re.sub(re_tags_pos, '', token) for token in tokens]
                    elif tagged == main.tr('Tagged (Non-POS)'):
                        tokens_searched = [re.sub(re_tags_non_pos, '', token) for token in tokens]
                elif search_settings['ignore_tags_type'] == main.tr('POS'):
                    if tagged in [main.tr('Tagged (Both)'), main.tr('Tagged (POS)')]:
                        tokens_searched = [re.sub(re_tags_pos, '', token) for token in tokens]
                    elif tagged == main.tr('Tagged (Non-POS)'):
                        tokens_searched = tokens
                elif search_settings['ignore_tags_type'] == main.tr('Non-POS'):
                    if tagged in [main.tr('Tagged (Both)'), main.tr('Tagged (Non-POS)')]:
                        tokens_searched = [re.sub(re_tags_non_pos, '', token) for token in tokens]
                    elif tagged == main.tr('Tagged (POS)'):
                        tokens_searched = tokens
        else:
            tokens_searched = tokens

    if tokens_searched:
        if search_settings['use_regex']:
            for ngram_search in search_terms:
                len_ngram_search = len(ngram_search)

                if search_settings['match_whole_word']:
                    ngram_search = [fr'(^|\s+){token}(\s+|$)' for token in ngram_search]

                if search_settings['ignore_case']:
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

                if search_settings['match_whole_word']:
                    ngram_search = [fr'(^|\s+){token}(\s+|$)' for token in ngram_search]

                if search_settings['ignore_case']:
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

        if (not search_settings['match_tags'] and
            (tagged == main.tr('Untagged') or
             tagged == main.tr('Tagged (Both)') and search_settings['ignore_tags_type'] == main.tr('All') or
             tagged == main.tr('Tagged (POS)') and search_settings['ignore_tags_type'] == main.tr('All') or
             tagged == main.tr('Tagged (POS)') and search_settings['ignore_tags_type'] == main.tr('POS') or
             tagged == main.tr('Tagged (Non-POS)') and search_settings['ignore_tags_type'] == main.tr('All') or
             tagged == main.tr('Tagged (Non-POS)') and search_settings['ignore_tags_type'] == main.tr('Non-POS') or
             tagged == main.tr('Untagged')) and
            search_settings['match_inflected_forms']):
            print('test')
            tokens_text_lemma = wordless_text_processing.wordless_lemmatize(main, tokens_searched, lang_code)
            ngrams_matched_lemma = [wordless_text_processing.wordless_lemmatize(main, ngram, lang_code)
                                    for ngram in ngrams_matched | set([tuple(search_term) for search_term in search_terms])]

            for ngram_matched_lemma in ngrams_matched_lemma:
                len_ngram_matched_lemma = len(ngram_matched_lemma)

                ngram_matched_lemma = [re.escape(token) for token in ngram_matched_lemma]
                ngram_matched_lemma = [fr'(^|\s+){token}(\s+|$)' for token in ngram_matched_lemma]

                if search_settings['ignore_case']:
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
                       tagged, lang_code, search_settings):
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
                                    tagged, lang_code, search_settings)

    return search_terms

def match_search_terms_context(main, tokens,
                               tagged, lang_code, context_settings):
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
                                                  tagged, lang_code, context_settings['inclusion'])

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
                                                  tagged, lang_code, context_settings['exclusion'])

            for search_term in search_terms:
                search_terms_exclusion.add(tuple(search_term))

    return search_terms_inclusion, search_terms_exclusion
