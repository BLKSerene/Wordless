#
# Wordless: Text - Token Processing
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import copy

from wordless_checking import wordless_checking_token
from wordless_text import (wordless_stop_words, wordless_text, wordless_text_processing,
                           wordless_text_utils)
from wordless_utils import wordless_misc

def wordless_process_tokens(text, token_settings):
    main = text.main
    settings = copy.deepcopy(token_settings)

    # Token Settings
    if settings['use_tags']:
        settings['ignore_tags'] = settings['ignore_tags_tags']
        settings['ignore_tags_type'] = settings['ignore_tags_type_tags']

    # Punctuations
    if not settings['puncs']:
        i_tokens = 0

        # Mark tokens to be removed
        for para in text.tokens_hierarchical:
            for sentence in para:
                for clause in sentence:
                    for i, token in enumerate(clause):
                        if wordless_checking_token.is_token_punc(token):
                            clause[i] = ''

                            text.tags_pos[i_tokens + i] = ''
                            text.tags_non_pos[i_tokens + i] = ''
                            text.tags_all[i_tokens + i] = ''

                    i_tokens += len(clause)

        # Remove punctuations
        for para in text.tokens_hierarchical:
            for sentence in para:
                for i, clause in enumerate(sentence):
                    sentence[i] = [token for token in clause if token]

        text.tags_pos = [tags for tags in text.tags_pos if tags != '']
        text.tags_non_pos = [tags for tags in text.tags_pos if tags != '']
        text.tags_all = [tags for tags in text.tags_pos if tags != '']

    # Lemmatize all tokens
    if not settings['use_tags'] and settings['lemmatize_tokens']:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for i, clause in enumerate(sentence):
                    sentence[i] = wordless_text_processing.wordless_lemmatize(
                        main, clause,
                        lang = text.lang
                    )

    # Treat as all lowercase
    if settings['treat_as_lowercase']:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for i, clause in enumerate(sentence):
                    sentence[i] = [token.lower() for token in clause]

        text.tags_pos = [[tag.lower() for tag in tags] for tags in text.tags_pos]
        text.tags_non_pos = [[tag.lower() for tag in tags] for tags in text.tags_non_pos]
        text.tags_all = [[tag.lower() for tag in tags] for tags in text.tags_all]

    # Words
    if settings['words']:
        # Lowercase
        if not settings['lowercase']:
            for para in text.tokens_hierarchical:
                for sentence in para:
                    for clause in sentence:
                        for i, token in enumerate(clause):
                            if wordless_checking_token.is_token_word_lowercase(token):
                                clause[i] = ''
        # Uppercase
        if not settings['uppercase']:
            for para in text.tokens_hierarchical:
                for sentence in para:
                    for clause in sentence:
                        for i, token in enumerate(clause):
                            if wordless_checking_token.is_token_word_uppercase(token):
                                clause[i] = ''
        # Title Case
        if not settings['title_case']:
            for para in text.tokens_hierarchical:
                for sentence in para:
                    for clause in sentence:
                        for i, token in enumerate(clause):
                            if wordless_checking_token.is_token_word_title_case(token):
                                clause[i] = ''
    else:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for clause in sentence:
                    for i, token in enumerate(clause):
                        if wordless_checking_token.is_token_word(token):
                            clause[i] = ''

    # Numerals
    if not settings['nums']:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for clause in sentence:
                    for i, token in enumerate(clause):
                        if wordless_checking_token.is_token_num(token):
                            clause[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for i, clause in enumerate(sentence):
                    sentence[i] = wordless_stop_words.wordless_filter_stop_words(
                        main, clause,
                        lang = text.lang
                    )

    # Ignore tags
    i_token = 0

    if settings['ignore_tags']:
        # Ignore all tags
        if settings['ignore_tags_type'] == main.tr('all'):
            for para in text.tokens_hierarchical:
                for sentence in para:
                    for clause in sentence:
                        for i, token in enumerate(clause):
                            clause[i] = (token, [])
        # Ignore POS tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            for para in text.tokens_hierarchical:
                for sentence in para:
                    for clause in sentence:
                        for i, token in enumerate(clause):
                            clause[i] = (token, text.tags_non_pos[i_token + i])

                        i_token += len(clause)

        # Ignore non-POS tags
        elif settings['ignore_tags_type'] == main.tr('non-POS'):
            for para in text.tokens_hierarchical:
                for sentence in para:
                    for clause in sentence:
                        for i, token in enumerate(clause):
                            clause[i] = (token, text.tags_pos[i_token + i])

                        i_token += len(clause)
    else:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for clause in sentence:
                    for i, token in enumerate(clause):
                        clause[i] = (token, text.tags_all[i_token + i])

                    i_token += len(clause)

    # Use tags only
    if settings['use_tags']:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for clause in sentence:
                    for i, token in enumerate(clause):
                        clause[i] = clause[i][1]
    else:
        for para in text.tokens_hierarchical:
            for sentence in para:
                for clause in sentence:
                    for i, token in enumerate(clause):
                        clause[i] = f"{clause[i][0]}{''.join(clause[i][1])}"

    text.tokens_flat = list(wordless_misc.flatten_list(text.tokens_hierarchical))

    return text

def wordless_process_tokens_overview(text, token_settings):
    text = wordless_process_tokens(text, token_settings)

    # Remove empty tokens
    text.tokens_hierarchical = [[[[token
                                   for token in clause
                                   if token]
                                  for clause in sentence]
                                 for sentence in para]
                                for para in text.tokens_hierarchical]
    text.tokens_flat = [token for token in text.tokens_flat if token]

    # Update offsets
    i_sentences = 0
    i_clauses = 0
    i_tokens = 0

    for i, para in enumerate(text.tokens_hierarchical):
        text.offsets_paras[i] = i_tokens

        for j, sentence in enumerate(para):
            text.offsets_sentences[i_sentences + j] = i_tokens

            for k, clause in enumerate(sentence):
                text.offsets_clauses[i_clauses + k] = i_tokens

                i_tokens += len(clause)

            i_clauses += len(sentence)

        i_sentences += len(para)

    # Remove duplicate offsets
    text.offsets_paras = sorted(set(text.offsets_paras))
    text.offsets_sentences = sorted(set(text.offsets_sentences))
    text.offsets_clauses = sorted(set(text.offsets_clauses))

    return text

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

def wordless_process_tokens_wordlist(text, token_settings):
    text = wordless_process_tokens(text, token_settings)

    return text

def wordless_process_tokens_ngram(text, token_settings):
    text = wordless_process_tokens(text, token_settings)

    return text

def wordless_process_tokens_collocation(text, token_settings):
    text = wordless_process_tokens(text, token_settings)

    return text

def wordless_process_tokens_colligation(text, token_settings):
    text = wordless_process_tokens(text, token_settings)

    # Use tags Only
    if token_settings['use_tags']:
        text.tags_pos = [tag
                         for tags in text.tags_pos
                         for tag in tags]
    else:
        text.tags_pos = [''.join(tags)
                         for tags in text.tags_pos]

    return text

def wordless_process_tokens_keyword(text, token_settings):
    text = wordless_process_tokens(text, token_settings)

    return text
