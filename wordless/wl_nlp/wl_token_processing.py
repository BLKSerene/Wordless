# ----------------------------------------------------------------------
# Wordless: NLP - Token Processing
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

from wordless.wl_checking import wl_checking_tokens
from wordless.wl_nlp import wl_lemmatization, wl_stop_word_lists, wl_syl_tokenization, wl_word_detokenization
from wordless.wl_utils import wl_misc

def wl_process_tokens(main, text, token_settings):
    settings = copy.deepcopy(token_settings)

    if not settings['words']:
        settings['all_lowercase'] = False
        settings['all_uppercase'] = False
        settings['title_case'] = False

    if settings['ignore_tags']:
        settings['use_tags'] = False
    elif settings['use_tags']:
        settings['lemmatize_tokens'] = False
        settings['ignore_tags'] = False

    # Remove empty paragraphs
    text.tokens_multilevel = [
        para
        for para in text.tokens_multilevel
        if para
    ]

    # Punctuations
    if not settings['puncs']:
        i_tokens = 0

        # Mark tokens to be removed
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checking_tokens.is_punc(token):
                            sentence_seg[i] = ''

                            text.tags[i_tokens + i] = ''

                    i_tokens += len(sentence_seg)

        # Remove punctuations
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token for token in sentence_seg if token]

        text.tags = [tags for tags in text.tags if tags != '']

    # Lemmatize all tokens
    if settings['lemmatize_tokens']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    para[i] = wl_lemmatization.wl_lemmatize(
                        main, sentence_seg,
                        lang = text.lang
                    )

    # Treat as all lowercase
    if settings['treat_as_all_lowercase']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    para[i] = [token.lower() for token in sentence_seg]

        text.tags = [
            [tag.lower() for tag in tags]
            for tags in text.tags
        ]

    # Words
    if settings['words']:
        # Lowercase
        if not settings['all_lowercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if wl_checking_tokens.is_word_lowercase(token):
                                sentence_seg[i] = ''
        # Uppercase
        if not settings['all_uppercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if wl_checking_tokens.is_word_uppercase(token):
                                sentence_seg[i] = ''
        # Title Case
        if not settings['title_case']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if wl_checking_tokens.is_word_title_case(token):
                                sentence_seg[i] = ''
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checking_tokens.is_word_alphabetic(token):
                            sentence_seg[i] = ''

    # Numerals
    if not settings['nums']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checking_tokens.is_num(token):
                            sentence_seg[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        stop_words = wl_stop_word_lists.wl_get_stop_word_list(main, lang = text.lang)

        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [
                        token if token not in stop_words else ''
                        for token in sentence_seg
                    ]

    # Ignore tags
    i_token = 0

    if settings['ignore_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        sentence_seg[i] = (token, [])
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        sentence_seg[i] = (token, text.tags[i_token + i])

                    i_token += len(sentence_seg)

    # Use tags only
    if settings['use_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        sentence_seg[i] = sentence_seg[i][1]
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        sentence_seg[i] = f"{sentence_seg[i][0]}{''.join(sentence_seg[i][1])}"

    return text

def wl_process_tokens_profiler(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    # Remove empty tokens, sentence segments, sentences, and paragraphs
    text.tokens_multilevel = [
        [
            [
                [
                    token
                    for token in sentence_seg
                    if token
                ]
                for sentence_seg in sentence
            ]
            for sentence in para
        ]
        for para in text.tokens_multilevel
    ]
    text.tokens_multilevel = [
        [
            [
                sentence_seg
                for sentence_seg in sentence
                if sentence_seg
            ]
            for sentence in para
        ]
        for para in text.tokens_multilevel
    ]
    text.tokens_multilevel = [
        [
            sentence
            for sentence in para
            if sentence
        ]
        for para in text.tokens_multilevel
    ]
    text.tokens_multilevel = [
        para
        for para in text.tokens_multilevel
        if para
    ]

    # Syllable tokenization
    text.syls_tokens = wl_syl_tokenization.wl_syl_tokenize_tokens_no_puncs(
        main,
        tokens = list(wl_misc.flatten_list(text.tokens_multilevel)),
        lang = text.lang
    )

    return text

def wl_process_tokens_concordancer(main, text, token_settings, preserve_blank_lines = False):
    tokens_flat = text.get_tokens_flat()

    settings = copy.deepcopy(token_settings)

    # Punctuations
    if not settings['puncs']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token for token in sentence_seg if not wl_checking_tokens.is_punc(token)]

        text.tokens_flat_puncs_merged = []

        for i, token in enumerate(tokens_flat):
            if wl_checking_tokens.is_punc(token) and i > 0:
                text.tokens_flat_puncs_merged[-1] = wl_word_detokenization.wl_word_detokenize(
                    main,
                    tokens = [text.tokens_flat_puncs_merged[-1], token],
                    lang = text.lang
                )
            else:
                text.tokens_flat_puncs_merged.append(token)

        # Check if the first token is a punctuation mark
        if wl_checking_tokens.is_punc(text.tokens_flat_puncs_merged[0]):
            text.tokens_multilevel[0][0][0].insert(0, '')
    else:
        text.tokens_flat_puncs_merged = tokens_flat

    # Remove empty paragraphs
    if not preserve_blank_lines:
        text.tokens_multilevel = [
            [
                [
                    sentence_seg
                    for sentence_seg in sentence
                    if sentence_seg
                ]
                for sentence in para
            ]
            for para in text.tokens_multilevel
        ]
        text.tokens_multilevel = [
            [
                sentence
                for sentence in para
                if sentence
            ]
            for para in text.tokens_multilevel
        ]
        text.tokens_multilevel = [
            para
            for para in text.tokens_multilevel
            if para
        ]

    # Ignore tags
    if settings['ignore_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [(token, []) for token in sentence_seg]

        text.tokens_flat_puncs_merged = [
            (token, [])
            for token in text.tokens_flat_puncs_merged
        ]
    else:
        i_tags = 0

        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        sentence_seg[i] = (token, text.tags[i_tags + i])

                    i_tags += len(sentence_seg)

        text.tokens_flat_puncs_merged = list(zip(text.tokens_flat_puncs_merged, text.tags))

    # Use tags only
    if settings['use_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [''.join(tags) for (_, tags) in sentence_seg]

        text.tokens_flat_puncs_merged = [
            ''.join(tags)
            for _, tags in text.tokens_flat_puncs_merged
        ]
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [f"{token}{''.join(tags)}" for (token, tags) in sentence_seg]

        text.tokens_flat_puncs_merged = [
            f"{token}{''.join(tags)}"
            for token, tags in text.tokens_flat_puncs_merged
        ]

    return text

def wl_process_tokens_wordlist_generator(main, text, token_settings):
    return wl_process_tokens(main, text, token_settings)

def wl_process_tokens_ngram_generator(main, text, token_settings):
    return wl_process_tokens(main, text, token_settings)

def wl_process_tokens_collocation_extractor(main, text, token_settings):
    return wl_process_tokens(main, text, token_settings)

def wl_process_tokens_colligation_extractor(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    # Use tags Only
    if token_settings['use_tags']:
        text.tags = [
            tag
            for tags in text.tags
            for tag in tags
        ]
    else:
        text.tags = [
            ''.join(tags)
            for tags in text.tags
        ]

    return text

def wl_process_tokens_keyword_extractor(main, text, token_settings):
    return wl_process_tokens(main, text, token_settings)
