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

from wl_checking import wl_checking_tokens
from wl_nlp import wl_lemmatization, wl_stop_word_lists, wl_syl_tokenization, wl_word_detokenization
from wl_utils import wl_misc

def wl_process_tokens(main, text, token_settings):
    settings = copy.deepcopy(token_settings)

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
                for i, token in enumerate(sentence):
                    if wl_checking_tokens.is_punc(token):
                        sentence[i] = ''

                        text.tags[i_tokens + i] = ''

                i_tokens += len(sentence)

        # Remove punctuations
        for para in text.tokens_multilevel:
            for i, sentence in enumerate(para):
                para[i] = [token for token in sentence if token]

        text.tags = [tags for tags in text.tags if tags != '']

        # Update offsets
        i_sentences = 0
        i_tokens = 0

        for i, para in enumerate(text.tokens_multilevel):
            text.offsets_paras[i] = i_tokens

            for j, sentence in enumerate(para):
                text.offsets_sentences[i_sentences + j] = i_tokens

                i_tokens += len(sentence)

            i_sentences += len(para)

    # Lemmatize all tokens
    if not settings['use_tags'] and settings['lemmatize_tokens']:
        for para in text.tokens_multilevel:
            for i, sentence in enumerate(para):
                para[i] = wl_lemmatization.wl_lemmatize(
                    main, sentence,
                    lang = text.lang
                )

    # Treat as all lowercase
    if settings['treat_as_lowercase']:
        for para in text.tokens_multilevel:
            for i, sentence in enumerate(para):
                para[i] = [token.lower() for token in sentence]

        text.tags = [
            [tag.lower() for tag in tags]
            for tags in text.tags
        ]

    # Words
    if settings['words']:
        # Lowercase
        if not settings['lowercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for i, token in enumerate(sentence):
                        if wl_checking_tokens.is_word_lowercase(token):
                            sentence[i] = ''
        # Uppercase
        if not settings['uppercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for i, token in enumerate(sentence):
                        if wl_checking_tokens.is_word_uppercase(token):
                            sentence[i] = ''
        # Title Case
        if not settings['title_case']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for i, token in enumerate(sentence):
                        if wl_checking_tokens.is_word_title_case(token):
                            sentence[i] = ''
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, token in enumerate(sentence):
                    if wl_checking_tokens.is_word_alphabetic(token):
                        sentence[i] = ''

    # Numerals
    if not settings['nums']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, token in enumerate(sentence):
                    if wl_checking_tokens.is_num(token):
                        sentence[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        for para in text.tokens_multilevel:
            for i, sentence in enumerate(para):
                para[i] = wl_stop_word_lists.wl_filter_stop_words(
                    main, sentence,
                    lang = text.lang
                )

    # Ignore tags
    i_token = 0

    if settings['ignore_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, token in enumerate(sentence):
                    sentence[i] = (token, [])
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, token in enumerate(sentence):
                    sentence[i] = (token, text.tags[i_token + i])

                i_token += len(sentence)

    # Use tags only
    if settings['use_tags']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, token in enumerate(sentence):
                    sentence[i] = sentence[i][1]
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, token in enumerate(sentence):
                    sentence[i] = f"{sentence[i][0]}{''.join(sentence[i][1])}"

    text.tokens_flat = list(wl_misc.flatten_list(text.tokens_multilevel))

    return text

def wl_process_tokens_profiler(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    # Remove empty tokens, sentences, and paragraphs
    text.tokens_multilevel = [
        [
            [
                token
                for token in sentence
                if token
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
    text.tokens_flat = [
        token
        for token in text.tokens_flat
        if token
    ]

    # Update offsets
    i_sentences = 0
    i_tokens = 0

    for i, para in enumerate(text.tokens_multilevel):
        text.offsets_paras[i] = i_tokens

        for j, sentence in enumerate(para):
            text.offsets_sentences[i_sentences + j] = i_tokens

            i_tokens += len(sentence)

        i_sentences += len(para)

    # Syllable tokenization
    text.syls_tokens = wl_syl_tokenization.wl_syl_tokenize_no_puncs(main, text.tokens_flat, lang = text.lang)

    return text

def wl_process_tokens_concordancer(main, text, token_settings, preserve_blank_lines = False):
    tokens = text.tokens_flat.copy()

    settings = copy.deepcopy(token_settings)

    # Punctuations
    if not settings['puncs']:
        tokens = [
            token
            for token in tokens
            if not wl_checking_tokens.is_punc(token)
        ]

        # Update offsets
        text.offsets_paras = []
        text.offsets_sentences = []
        text.tokens_flat = []

        for para in text.tokens_multilevel:
            text.offsets_paras.append(len(text.tokens_flat))

            for sentence in para:
                text.offsets_sentences.append(len(text.tokens_flat))

                for token in sentence:
                    if text.tokens_flat:
                        if wl_checking_tokens.is_punc(token):
                            text.tokens_flat[-1] = wl_word_detokenization.wl_word_detokenize(
                                main, [text.tokens_flat[-1], token],
                                lang = text.lang
                            )
                        else:
                            text.tokens_flat.append(token)
                    else:
                        text.tokens_flat.append(token)

        # Remove duplicate offsets
        if not preserve_blank_lines:
            text.offsets_paras = sorted(set(text.offsets_paras))
            text.offsets_sentences = sorted(set(text.offsets_sentences))

        # Check if the first token is a punctuation mark
        if wl_checking_tokens.is_punc(text.tokens_flat[0]):
            tokens.insert(0, [])

    # Ignore tags
    if settings['ignore_tags']:
        tokens = [
            (token, [])
            for token in tokens
        ]
        text.tokens_flat = [
            (token, [])
            for token in text.tokens_flat
        ]
    else:
        tokens = [
            (token, tags)
            for token, tags in zip(tokens, text.tags)
        ]
        text.tokens_flat = [
            (token, tags)
            for token, tags in zip(text.tokens_flat, text.tags)
        ]

    # Use tags only
    if settings['use_tags']:
        tokens = [
            ''.join(tags)
            for _, tags in tokens
        ]
        text.tokens_flat = [
            ''.join(tags)
            for _, tags in text.tokens_flat
        ]
    else:
        tokens = [
            f"{token}{''.join(tags)}"
            for token, tags in tokens
        ]
        text.tokens_flat = [
            f"{token}{''.join(tags)}"
            for token, tags in text.tokens_flat
        ]

    return tokens

def wl_process_tokens_wordlist_generator(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    return text

def wl_process_tokens_ngram_generator(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    return text

def wl_process_tokens_collocation(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    return text

def wl_process_tokens_colligation(main, text, token_settings):
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

def wl_process_tokens_keyword(main, text, token_settings):
    text = wl_process_tokens(main, text, token_settings)

    return text
