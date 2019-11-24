#
# Wordless: Text - Token Processing
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from wordless_checking import wordless_checking_token
from wordless_text import wordless_text, wordless_text_processing, wordless_text_utils

def wordless_process_tokens(text, token_settings):
    main = text.main
    tokens = text.tokens_flat.copy()

    settings = copy.deepcopy(token_settings)

    # Token Settings
    if settings['use_tags']:
        settings['ignore_tags'] = settings['ignore_tags_tags']
        settings['ignore_tags_type'] = settings['ignore_tags_type_tags']

    # Punctuations
    if not settings['puncs']:
        for i, token in reversed(list(enumerate(tokens))):
            if wordless_checking_token.is_token_punc(token):
                del tokens[i]

                del text.tags_pos[i]
                del text.tags_non_pos[i]
                del text.tags_all[i]

    # Lemmatize all tokens
    if not settings['use_tags'] and settings['lemmatize_tokens']:
        tokens = wordless_text_processing.wordless_lemmatize(main, tokens,
                                                             lang = text.lang)

    # Treat as all lowercase
    if settings['treat_as_lowercase']:
        tokens = [token.lower() for token in tokens]

        text.tags_pos = [[tag.lower() for tag in tags] for tags in text.tags_pos]
        text.tags_non_pos = [[tag.lower() for tag in tags] for tags in text.tags_non_pos]
        text.tags_all = [[tag.lower() for tag in tags] for tags in text.tags_all]

    text.tokens_flat = copy.deepcopy(tokens)

    # Words
    if settings['words']:
        # Lowercase
        if not settings['lowercase']:
            for i, token in enumerate(tokens):
                if wordless_checking_token.is_token_word_lowercase(token):
                    tokens[i] = ''
        # Uppercase
        if not settings['uppercase']:
            for i, token in enumerate(tokens):
                if wordless_checking_token.is_token_word_uppercase(token):
                    tokens[i] = ''
        # Title Case
        if not settings['title_case']:
            for i, token in enumerate(tokens):
                if wordless_checking_token.is_token_word_title_case(token):
                    tokens[i] = ''
    else:
        for i, token in enumerate(tokens):
            if wordless_checking_token.is_token_word(token):
                tokens[i] = ''

    # Numerals
    if not settings['nums']:
        for i, token in enumerate(tokens):
            if wordless_checking_token.is_token_num(token):
                tokens[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        tokens_filtered = wordless_text_processing.wordless_filter_stop_words(main, [token for token in tokens],
                                                                              lang = text.lang)

        for i, token in enumerate(tokens):
            if token not in tokens_filtered:
                tokens[i] = ''

    # Ignore tags
    if settings['ignore_tags']:
        # Ignore all tags
        if settings['ignore_tags_type'] == main.tr('all'):
            tokens = [(token, [])
                      for token in tokens]
            text.tokens_flat = [(token, [])
                                for token in text.tokens_flat]
        # Ignore POS tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_non_pos)]
            text.tokens_flat = [(token, tags)
                                for token, tags in zip(text.tokens_flat, text.tags_non_pos)]
        # Ignore non-POS tags
        elif settings['ignore_tags_type'] == main.tr('non-POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_pos)]
            text.tokens_flat = [(token, tags)
                                for token, tags in zip(text.tokens_flat, text.tags_pos)]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags_all)]
        text.tokens_flat = [(token, tags)
                            for token, tags in zip(text.tokens_flat, text.tags_all)]

    return tokens

def wordless_process_tokens_overview(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    text.offsets_paras = []
    text.offsets_sentences = []
    text.offsets_clauses = []
    text.tokens_flat = []

    offset_token = 0

    # Copy tokens
    for i, para in enumerate(text.tokens_hierarchical):
        text.offsets_paras.append(len(text.tokens_flat))

        for j, sentence in enumerate(para):
            text.offsets_sentences.append(len(text.tokens_flat))

            for k, clause in enumerate(sentence):
                text.offsets_clauses.append(len(text.tokens_flat))

                for l, token in enumerate(clause):
                    # Punctuations
                    if wordless_checking_token.is_token_punc(token) and not token_settings['puncs']:
                        text.tokens_hierarchical[i][j][k][l] = ''
                    else:
                        text.tokens_hierarchical[i][j][k][l] = tokens[offset_token][0]

                        if text.tokens_hierarchical[i][j][k][l] != '':
                            text.tokens_flat.append(tokens[offset_token])

                        offset_token += 1

    # Remove duplicate offsets
    text.offsets_paras = sorted(set(text.offsets_paras))
    text.offsets_sentences = sorted(set(text.offsets_sentences))
    text.offsets_clauses = sorted(set(text.offsets_clauses))

    # Use tags only
    if token_settings['use_tags']:
        text.tokens_flat = [tag
                            for _, tags in text.tokens_flat
                            for tag in tags]
    else:
        text.tokens_flat = [f"{token}{''.join(tags)}"
                            for token, tags in text.tokens_flat]

    # Remove empty tokens
    text.tokens_hierarchical = [[[[token
                                   for token in clause
                                   if token]
                                  for clause in sentence]
                                 for sentence in para]
                                for para in text.tokens_hierarchical]

def wordless_process_tokens_wordlist(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    # Use tags only
    if token_settings['use_tags']:
        tokens = [tag
                  for _, tags in tokens
                  for tag in tags]
        text.tokens_flat = [tag
                            for _, tags in text.tokens_flat
                            for tag in tags]
    else:
        tokens = [f"{token}{''.join(tags)}"
                  for token, tags in tokens]
        text.tokens_flat = [f"{token}{''.join(tags)}"
                            for token, tags in text.tokens_flat]

    # Remove empty tokens/tags
    tokens = [token for token in tokens if token]

    return tokens

def wordless_process_tokens_ngram(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    # Use tags only
    if token_settings['use_tags']:
        tokens = [tag
                  for _, tags in tokens
                  for tag in tags]
        text.tokens_flat = [tag
                            for _, tags in text.tokens_flat
                            for tag in tags]
    else:
        tokens = [f"{token}{''.join(tags)}"
                  for token, tags in tokens]
        text.tokens_flat = [f"{token}{''.join(tags)}"
                            for token, tags in text.tokens_flat]

    return tokens

def wordless_process_tokens_colligation(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    # Use tags Only
    if token_settings['use_tags']:
        tokens = [tag
                  for _, tags in tokens
                  for tag in tags]
        text.tokens_flat = [tag
                            for _, tags in text.tokens_flat
                            for tag in tags]

        text.tags_pos = [tag
                         for tags in text.tags_pos
                         for tag in tags]
    else:
        tokens = [f"{token}{''.join(tags)}"
                  for token, tags in tokens]
        text.tokens_flat = [f"{token}{''.join(tags)}"
                            for token, tags in text.tokens_flat]

        text.tags_pos = [''.join(tags)
                         for tags in text.tags_pos]

    return tokens

def wordless_process_tokens_concordancer(text, token_settings):
    main = text.main
    tokens = text.tokens_flat.copy()

    settings = copy.deepcopy(token_settings)

    # Token Settings
    if settings['use_tags']:
        settings['ignore_tags'] = settings['ignore_tags_tags']
        settings['ignore_tags_type'] = settings['ignore_tags_type_tags']

    # Punctuations
    if not settings['puncs']:
        tokens = [token
                  for token in tokens
                  if not wordless_checking_token.is_token_punc(token)]

        text.offsets_paras = []
        text.offsets_sentences = []
        text.offsets_clauses = []
        text.tokens_flat = []

        for para in text.tokens_hierarchical:
            text.offsets_paras.append(len(text.tokens_flat))
            
            for sentence in para:
                text.offsets_sentences.append(len(text.tokens_flat))

                for clause in sentence:
                    text.offsets_clauses.append(len(text.tokens_flat))

                    for token in clause:
                        if text.tokens_flat:
                            if wordless_checking_token.is_token_punc(token):
                                text.tokens_flat[-1] = wordless_text_processing.wordless_word_detokenize(main, [text.tokens_flat[-1], token], lang = text.lang)
                            else:
                                text.tokens_flat.append(token)
                        else:
                            text.tokens_flat.append(token)

        # Remove duplicate offsets
        text.offsets_paras = sorted(set(text.offsets_paras))
        text.offsets_sentences = sorted(set(text.offsets_sentences))
        text.offsets_clauses = sorted(set(text.offsets_clauses))

        # Check if the first token is a punctuation mark
        if wordless_checking_token.is_token_punc(text.tokens_flat[0]):
            tokens.insert(0, [])

    # Ignore tags
    if settings['ignore_tags']:
        # Ignore all tags
        if settings['ignore_tags_type'] == main.tr('all'):
            tokens = [(token, [])
                      for token in tokens]
            text.tokens_flat = [(token, [])
                                for token in text.tokens_flat]
        # Ignore POS tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_non_pos)]
            text.tokens_flat = [(token, tags)
                                for token, tags in zip(text.tokens_flat, text.tags_non_pos)]
        # Ignore non-POS tags
        elif settings['ignore_tags_type'] == main.tr('non-POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_pos)]
            text.tokens_flat = [(token, tags)
                                for token, tags in zip(text.tokens_flat, text.tags_pos)]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags_all)]
        text.tokens_flat = [(token, tags)
                            for token, tags in zip(text.tokens_flat, text.tags_all)]

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
