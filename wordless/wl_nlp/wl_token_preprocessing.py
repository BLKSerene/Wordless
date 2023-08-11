# ----------------------------------------------------------------------
# Wordless: NLP - Token preprocessing
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import wl_lemmatization, wl_pos_tagging, wl_stop_word_lists, wl_syl_tokenization, wl_word_detokenization
from wordless.wl_utils import wl_misc

def wl_preprocess_tokens(main, text, token_settings):
    settings = copy.deepcopy(token_settings)

    if not settings['words']:
        settings['all_lowercase'] = False
        settings['all_uppercase'] = False
        settings['title_case'] = False

    if settings['ignore_tags']:
        settings['use_tags'] = False
    elif settings['use_tags']:
        settings['apply_lemmatization'] = False
        settings['ignore_tags'] = False

    # Remove empty paragraphs
    text.tokens_multilevel = [
        para
        for para in text.tokens_multilevel
        if para
    ]

    # Punctuation marks
    if not settings['punc_marks']:
        i_tokens = 0

        # Mark tokens to be removed
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checks_tokens.is_punc(token):
                            sentence_seg[i] = ''

                            text.tags[i_tokens + i] = ''

                    i_tokens += len(sentence_seg)

        # Remove punctuation marks
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token for token in sentence_seg if token]

        text.tags = [tags for tags in text.tags if tags != '']

    # Assign part-of-speech tags
    if settings['assign_pos_tags'] and not text.tagged:
        tokens_tagged = wl_pos_tagging.wl_pos_tag(
            main,
            inputs = text.get_tokens_flat(),
            lang = text.lang
        )

        text.tags = [[(f'_{tag}' if tag else '')] for _, tag in tokens_tagged]
        # Modify text types
        text.tagged = True

    # Apply lemmatization
    if settings['apply_lemmatization']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = wl_lemmatization.wl_lemmatize(
                        main, sentence_seg,
                        lang = text.lang
                    )

    # Treat as all lowercase
    if settings['treat_as_all_lowercase']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token.lower() for token in sentence_seg]

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
                            if token.islower():
                                sentence_seg[i] = ''
        # Uppercase
        if not settings['all_uppercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token.isupper():
                                sentence_seg[i] = ''
        # Title Case
        if not settings['title_case']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token.istitle():
                                sentence_seg[i] = ''
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checks_tokens.is_word_alphabetic(token):
                            sentence_seg[i] = ''

    # Numerals
    if not settings['nums']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checks_tokens.is_num(token):
                            sentence_seg[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        stop_words = wl_stop_word_lists.wl_get_stop_word_list(main, lang = text.lang)

        i_tag = 0

        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if token in stop_words:
                            sentence_seg[i] = ''
                            text.tags[i_tag + i] = ''

                    i_tag += len(sentence_seg)

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

def wl_preprocess_tokens_profiler(main, text, token_settings):
    # Punctuation marks must be preserved for some readability measures (e.g. Wheeler & Smith's Readability Formula)
    text.tokens_multilevel_with_puncs = copy.deepcopy(text.tokens_multilevel)

    text = wl_preprocess_tokens(main, text, token_settings)

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
    text.syls_tokens = wl_syl_tokenization.wl_syl_tokenize_tokens_no_punc(
        main,
        tokens = list(wl_misc.flatten_list(text.tokens_multilevel)),
        lang = text.lang,
        tagged = text.tagged
    )

    return text

def wl_preprocess_tokens_concordancer(main, text, token_settings, preserve_blank_lines = False):
    settings = copy.deepcopy(token_settings)
    tokens_flat = text.get_tokens_flat()

    # Punctuation marks
    if not settings['punc_marks']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token for token in sentence_seg if not wl_checks_tokens.is_punc(token)]

        text.tokens_flat_punc_marks_merged = []

        for i, token in enumerate(tokens_flat):
            if wl_checks_tokens.is_punc(token) and i > 0:
                text.tokens_flat_punc_marks_merged[-1] = wl_word_detokenization.wl_word_detokenize(
                    main,
                    tokens = [text.tokens_flat_punc_marks_merged[-1], token],
                    lang = text.lang
                )
            else:
                text.tokens_flat_punc_marks_merged.append(token)

        # Check if the first token is a punctuation mark
        if wl_checks_tokens.is_punc(text.tokens_flat_punc_marks_merged[0]):
            text.tokens_multilevel[0][0][0].insert(0, '')
    else:
        text.tokens_flat_punc_marks_merged = tokens_flat

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

    # Assign part-of-speech tags
    if settings['assign_pos_tags'] and not text.tagged:
        tokens_tagged = wl_pos_tagging.wl_pos_tag(
            main,
            inputs = text.get_tokens_flat(),
            lang = text.lang
        )

        text.tags = [[(f'_{tag}' if tag else '')] for _, tag in tokens_tagged]
        # Modify text types
        text.tagged = True

    # Ignore tags
    if settings['ignore_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [(token, []) for token in sentence_seg]

        text.tokens_flat_punc_marks_merged = [
            (token, [])
            for token in text.tokens_flat_punc_marks_merged
        ]
    else:
        i_tags = 0

        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        sentence_seg[i] = (token, text.tags[i_tags + i])

                    i_tags += len(sentence_seg)

        text.tokens_flat_punc_marks_merged = list(zip(text.tokens_flat_punc_marks_merged, text.tags))

    # Use tags only
    if settings['use_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [''.join(tags) for (_, tags) in sentence_seg]

        text.tokens_flat_punc_marks_merged = [
            ''.join(tags)
            for _, tags in text.tokens_flat_punc_marks_merged
        ]
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [f"{token}{''.join(tags)}" for (token, tags) in sentence_seg]

        text.tokens_flat_punc_marks_merged = [
            f"{token}{''.join(tags)}"
            for token, tags in text.tokens_flat_punc_marks_merged
        ]

    return text

def wl_preprocess_tokens_colligation_extractor(main, text, token_settings):
    text = wl_preprocess_tokens(main, text, token_settings)

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
