#
# Wordless: Text - Token Processing
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from wl_checking import wl_checking_token
from wl_text import wl_lemmatization, wl_stop_word_lists, wl_text, wl_text_utils, wl_word_detokenization
from wl_utils import wl_misc

def wl_process_tokens(text, token_settings):
    main = text.main
    settings = copy.deepcopy(token_settings)

    # Punctuations
    if not settings['puncs']:
        i_tokens = 0

        # Mark tokens to be removed
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checking_token.is_token_punc(token):
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
    if not settings['use_tags'] and settings['lemmatize_tokens']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = wl_lemmatization.wl_lemmatize(
                        main, sentence_seg,
                        lang = text.lang
                    )

    # Treat as all lowercase
    if settings['treat_as_lowercase']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token.lower() for token in sentence_seg]

        text.tags = [[tag.lower() for tag in tags] for tags in text.tags]

    # Words
    if settings['words']:
        # Lowercase
        if not settings['lowercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if wl_checking_token.is_token_word_lowercase(token):
                                sentence_seg[i] = ''
        # Uppercase
        if not settings['uppercase']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if wl_checking_token.is_token_word_uppercase(token):
                                sentence_seg[i] = ''
        # Title Case
        if not settings['title_case']:
            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if wl_checking_token.is_token_word_title_case(token):
                                sentence_seg[i] = ''
    else:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checking_token.is_token_word(token):
                            sentence_seg[i] = ''

    # Numerals
    if not settings['nums']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checking_token.is_token_num(token):
                            sentence_seg[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        for para in text.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = wl_stop_word_lists.wl_filter_stop_words(
                        main, sentence_seg,
                        lang = text.lang
                    )

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

    text.tokens_flat = list(wl_misc.flatten_list(text.tokens_multilevel))

    return text

def wl_process_tokens_overview(text, token_settings):
    text = wl_process_tokens(text, token_settings)

    # Remove empty tokens
    text.tokens_multilevel = [[[token for token in sentence
                                if token]
                               for sentence in para]
                              for para in text.tokens_multilevel]
    text.tokens_flat = [token for token in text.tokens_flat if token]

    # Update offsets
    i_sentences = 0
    i_tokens = 0

    for i, para in enumerate(text.tokens_multilevel):
        text.offsets_paras[i] = i_tokens

        for j, sentence in enumerate(para):
            text.offsets_sentences[i_sentences + j] = i_tokens

            i_tokens += len(sentence)

        i_sentences += len(para)

    # Remove duplicate offsets
    text.offsets_paras = sorted(set(text.offsets_paras))
    text.offsets_sentences = sorted(set(text.offsets_sentences))

    return text

def wl_process_tokens_concordancer(text, token_settings):
    main = text.main
    tokens = text.tokens_flat.copy()

    settings = copy.deepcopy(token_settings)

    # Punctuations
    if not settings['puncs']:
        tokens = [token
                  for token in tokens
                  if not wl_checking_token.is_token_punc(token)]

        text.offsets_paras = []
        text.offsets_sentences = []
        text.tokens_flat = []

        for para in text.tokens_multilevel:
            text.offsets_paras.append(len(text.tokens_flat))
            
            for sentence in para:
                text.offsets_sentences.append(len(text.tokens_flat))

                for token in sentence:
                    if text.tokens_flat:
                        if wl_checking_token.is_token_punc(token):
                            text.tokens_flat[-1] = wl_word_detokenization.wl_word_detokenize(
                                main, [text.tokens_flat[-1], token],
                                lang = text.lang
                            )
                        else:
                            text.tokens_flat.append(token)
                    else:
                        text.tokens_flat.append(token)

        # Remove duplicate offsets
        text.offsets_paras = sorted(set(text.offsets_paras))
        text.offsets_sentences = sorted(set(text.offsets_sentences))

        # Check if the first token is a punctuation mark
        if wl_checking_token.is_token_punc(text.tokens_flat[0]):
            tokens.insert(0, [])

    # Ignore tags
    if settings['ignore_tags']:
        tokens = [(token, [])
                  for token in tokens]
        text.tokens_flat = [(token, [])
                            for token in text.tokens_flat]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags)]
        text.tokens_flat = [(token, tags)
                            for token, tags in zip(text.tokens_flat, text.tags)]

    # Use tags only
    if settings['use_tags']:
        tokens = [''.join(tags)
                  for _, tags in tokens]
        text.tokens_flat = [''.join(tags)
                            for _, tags in text.tokens_flat]
    else:
        tokens = [f"{token}{''.join(tags)}"
                  for token, tags in tokens]
        text.tokens_flat = [f"{token}{''.join(tags)}"
                            for token, tags in text.tokens_flat]

    return tokens

def wl_process_tokens_wordlist(text, token_settings):
    text = wl_process_tokens(text, token_settings)

    return text

def wl_process_tokens_ngram(text, token_settings):
    text = wl_process_tokens(text, token_settings)

    return text

def wl_process_tokens_collocation(text, token_settings):
    text = wl_process_tokens(text, token_settings)

    return text

def wl_process_tokens_colligation(text, token_settings):
    text = wl_process_tokens(text, token_settings)

    # Use tags Only
    if token_settings['use_tags']:
        text.tags = [tag
                     for tags in text.tags
                     for tag in tags]
    else:
        text.tags = [''.join(tags)
                     for tags in text.tags]

    return text

def wl_process_tokens_keyword(text, token_settings):
    text = wl_process_tokens(text, token_settings)

    return text
