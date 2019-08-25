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
    tokens = text.tokens.copy()

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

    text.tokens = copy.deepcopy(tokens)

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
            tokens = [(token, []) for token in tokens]
            text.tokens = [(token, []) for token in text.tokens]
        # Ignore POS tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_non_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_non_pos)]
        # Ignore non-POS tags
        elif settings['ignore_tags_type'] == main.tr('non-POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_pos)]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags_all)]
        text.tokens = [(token, tags)
                       for token, tags in zip(text.tokens, text.tags_all)]

    return tokens

def wordless_process_tokens_overview(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    # Use tags only
    if token_settings['use_tags']:
        tokens = [tag for _, tags in tokens for tag in tags]
        text.tokens = [tag for _, tags in text.tokens for tag in tags]
    else:
        tokens = [f"{token}{''.join(tags)}" for token, tags in tokens]
        text.tokens = [f"{token}{''.join(tags)}" for token, tags in text.tokens]

    # Remove empty tokens/tags
    tokens = [token for token in tokens if token]

    return tokens

def wordless_process_tokens_ngrams(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    # Use tags only
    if token_settings['use_tags']:
        tokens = [tag for _, tags in tokens for tag in tags]
        text.tokens = [tag for _, tags in text.tokens for tag in tags]
    else:
        tokens = [f"{token}{''.join(tags)}" for token, tags in tokens]
        text.tokens = [f"{token}{''.join(tags)}" for token, tags in text.tokens]

    return tokens

def wordless_process_tokens_colligation(text, token_settings):
    tokens = wordless_process_tokens(text, token_settings)

    # Use tags Only
    if token_settings['use_tags']:
        tokens = [tag for _, tags in tokens for tag in tags]
        text.tokens = [tag for _, tags in text.tokens for tag in tags]

        text.tags_pos = [tag for tags in text.tags_pos for tag in tags]
    else:
        tokens = [f"{token}{''.join(tags)}" for token, tags in tokens]
        text.tokens = [f"{token}{''.join(tags)}" for token, tags in text.tokens]

        text.tags_pos = [''.join(tags) for tags in text.tags_pos]

    return tokens

def wordless_process_tokens_concordancer(text, token_settings):
    main = text.main
    tokens = text.tokens.copy()

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
        text.tokens = []

        clause_start = 0

        for para in text.tokens_sentences_paras:
            text.offsets_paras.append(len(text.tokens))
            
            for sentence in para:
                # Check if the sentence contains only punctuation marks
                if not all(map(wordless_checking_token.is_token_punc, sentence)):
                    text.offsets_sentences.append(len(text.tokens))

                    for token in sentence:
                        if text.tokens:
                            if wordless_checking_token.is_token_punc(token):
                                text.tokens[-1] = wordless_text_processing.wordless_word_detokenize(main, [text.tokens[-1], token], lang = text.lang)
                            else:
                                text.tokens.append(token)
                        else:
                            text.tokens.append(token)

                    # Clause offset
                    for clause in wordless_text_processing.wordless_clause_tokenize(main, sentence, lang = text.lang):
                        # Check if the clause contains only punctuation marks
                        if not all(map(wordless_checking_token.is_token_punc, clause)):
                            text.offsets_clauses.append(clause_start)

                            clause_start += len([token
                                                 for token in clause
                                                 if not wordless_checking_token.is_token_punc(token)])

        # Check if the first token is a punctuation mark
        if wordless_checking_token.is_token_punc(text.tokens[0]):
            tokens.insert(0, [])

    # Ignore tags
    if settings['ignore_tags']:
        # Ignore all tags
        if settings['ignore_tags_type'] == main.tr('all'):
            tokens = [(token, []) for token in tokens]
            text.tokens = [(token, []) for token in text.tokens]
        # Ignore POS tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_non_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_non_pos)]
        # Ignore non-POS tags
        elif settings['ignore_tags_type'] == main.tr('non-POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_pos)]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags_all)]
        text.tokens = [(token, tags)
                       for token, tags in zip(text.tokens, text.tags_all)]

    # Use tags only
    if settings['use_tags']:
        tokens = [''.join(tags) for _, tags in tokens]
        text.tokens = [''.join(tags) for _, tags in text.tokens]
    else:
        tokens = [f"{token}{''.join(tags)}" for token, tags in tokens]
        text.tokens = [f"{token}{''.join(tags)}" for token, tags in text.tokens]

    return tokens
