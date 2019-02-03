#
# Wordless: Text - Token Processing
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy

from wordless_checking import wordless_checking_token
from wordless_text import wordless_text, wordless_text_processing

def wordless_preprocess_tokens(text, token_settings):
    main = text.main
    tokens = text.tokens.copy()

    settings = copy.deepcopy(token_settings)

    # Token Settings
    if settings['tags_only']:
        settings['ignore_tags'] = settings['ignore_tags_tags_only']
        settings['ignore_tags_type'] = settings['ignore_tags_type_tags_only']

    # Ignore Tags
    if settings['ignore_tags']:
        # Ignore All Tags
        if settings['ignore_tags_type'] == main.tr('All'):
            tokens = [(token, []) for token in tokens]
            text.tokens = [(token, []) for token in text.tokens]
        # Ignore POS Tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_non_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_non_pos)]
        # Ignore Non-POS Tags
        elif settings['ignore_tags_type'] == main.tr('Non-POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_pos)]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags_all)]
        text.tokens = [(token, tags)
                       for token, tags in zip(text.tokens, text.tags_all)]

    # Punctuations
    if not settings['puncs']:
        tokens = [(token, tags)
                  for token, tags in tokens
                  if not wordless_checking_token.is_token_punc(token)]

        text.tokens = copy.deepcopy(tokens)

    # Lemmatize
    if not settings['tags_only'] and settings['lemmatize']:
        lemmas = wordless_text_processing.wordless_lemmatize(main, [token for token, _ in tokens],
                                                             lang_code = text.lang_code)

        tokens = [(lemma, tags) for lemma, tags in zip(lemmas, [tags for _, tags in tokens])]

        text.tokens = copy.deepcopy(tokens)

    # Treat as All Lowercase
    if settings['treat_as_lowercase']:
        if settings['tags_only']:
            tokens = [(token, [tag.lower() for tag in tags]) for token, tags in tokens]

            text.tokens = copy.deepcopy(tokens)
        else:
            tokens = [(token.lower(), tags) for token, tags in tokens]

            text.tokens = copy.deepcopy(tokens)
    # Words
    if settings['words']:
        # Lowercase
        if not settings['lowercase']:
            for i, (token, tags) in enumerate(tokens):
                if wordless_checking_token.is_token_lowercase(token):
                    tokens[i] = ('', [])
        # Uppercase
        if not settings['uppercase']:
            for i, (token, tags) in enumerate(tokens):
                if wordless_checking_token.is_token_uppercase(token):
                    tokens[i] = ('', [])
        # Title Case
        if not settings['title_case']:
            for i, (token, tags) in enumerate(tokens):
                if wordless_checking_token.is_token_title_case(token):
                    tokens[i] = ('', [])
    else:
        for i, (token, tags) in enumerate(tokens):
            if wordless_checking_token.is_token_word(token):
                tokens[i] = ('', [])

    # Numerals
    if not settings['nums']:
        for i, (token, tags) in enumerate(tokens):
            if wordless_checking_token.is_token_num(token):
                tokens[i] = ('', [])

    # Filter Stop Words
    if settings['filter_stop_words']:
        tokens_filtered = wordless_text_processing.wordless_filter_stop_words(main, [token for token, _ in tokens],
                                                                              lang_code = text.lang_code)

        for i, (token, tags) in enumerate(tokens):
            if token not in tokens_filtered:
                tokens[i] = ('', [])

    # Tags Only
    if settings['tags_only']:
        tokens = [tags for _, tags in tokens]
        text.tokens = [tags for _, tags in text.tokens]
    else:
        tokens = [f"{token}{''.join(tags)}" for token, tags in tokens]
        text.tokens = [f"{token}{''.join(tags)}" for token, tags in text.tokens]

    return tokens

def wordless_preprocess_tokens_overview(text, token_settings):
    tokens = wordless_preprocess_tokens(text, token_settings)

    tokens = [token for token in tokens if token]

    if token_settings['tags_only']:
        tokens = [tag for tags in tokens for tag in tags]

    # Remove empty tokens/tags
    tokens = [token for token in tokens if token]

    return tokens

def wordless_preprocess_tokens_wordlist(text, token_settings):
    tokens = wordless_preprocess_tokens(text, token_settings)

    tokens = [token for token in tokens if token]
    text.tokens = [token for token in text.tokens if token]

    if token_settings['tags_only']:
        tokens = [''.join(tags) for tags in tokens]
        text.tokens = [''.join(tags) for tags in text.tokens]

    # Remove empty tokens/tags
    tokens = [token for token in tokens if token]

    return tokens

def wordless_preprocess_tokens_ngrams(text, token_settings):
    tokens = wordless_preprocess_tokens(text, token_settings)

    if token_settings['tags_only']:
        tokens = [''.join(tags) for tags in tokens]
        text.tokens = [''.join(tags) for tags in text.tokens]

    return tokens

def wordless_preprocess_tokens_concordancer(text, token_settings):
    main = text.main
    tokens = text.tokens.copy()

    settings = copy.deepcopy(token_settings)

    # Token Settings
    if settings['tags_only']:
        settings['ignore_tags'] = settings['ignore_tags_tags_only']
        settings['ignore_tags_type'] = settings['ignore_tags_type_tags_only']

    # Punctuations
    if not settings['puncs']:
        tokens = [token
                  for token in tokens
                  if not wordless_checking_token.is_token_punc(token)]

        text.para_offsets = []
        text.sentence_offsets = []
        text.tokens = []

        for para in text.paras:
            text.para_offsets.append(len(text.tokens))

            for sentence, sentence_tokens in zip(text.sentences, text.tokens_sentences):
                # Check if the sentence contains punctuation marks only
                if not all(map(wordless_checking_token.is_token_punc, sentence_tokens)):
                    text.sentence_offsets.append(len(text.tokens))

                    for token in sentence_tokens:
                        if text.tokens:
                            if wordless_checking_token.is_token_punc(token):
                                text.tokens[-1] += token
                            else:
                                text.tokens.append(token)
                        else:
                            text.tokens.append(token)

        # Check if the first token is a punctuation mark
        if wordless_checking_token.is_token_punc(text.tokens[0]):
            tokens.insert(0, [])

    # Ignore Tags
    if settings['ignore_tags']:
        # Ignore All Tags
        if settings['ignore_tags_type'] == main.tr('All'):
            tokens = [(token, []) for token in tokens]
            text.tokens = [(token, []) for token in text.tokens]
        # Ignore POS Tags
        elif settings['ignore_tags_type'] == main.tr('POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_non_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_non_pos)]
        # Ignore Non-POS Tags
        elif settings['ignore_tags_type'] == main.tr('Non-POS'):
            tokens = [(token, tags)
                      for token, tags in zip(tokens, text.tags_pos)]
            text.tokens = [(token, tags)
                           for token, tags in zip(text.tokens, text.tags_pos)]
    else:
        tokens = [(token, tags)
                  for token, tags in zip(tokens, text.tags_all)]
        text.tokens = [(token, tags)
                       for token, tags in zip(text.tokens, text.tags_all)]

    # Tags Only
    if settings['tags_only']:
        tokens = [''.join(tags) for _, tags in tokens]
        text.tokens = [''.join(tags) for _, tags in text.tokens]
    else:
        tokens = [f"{token}{''.join(tags)}" for token, tags in tokens]
        text.tokens = [f"{token}{''.join(tags)}" for token, tags in text.tokens]

    return tokens

def wordless_preprocess_tokens_tagged(main, tokens_tagged, lang_code, settings):
    if settings['treat_as_lowercase']:
        tokens_tagged = [(token.lower(), tag) for token, tag in tokens_tagged]

    if settings['lemmatize']:
        tokens_lemmatized = wordless_lemmatize(main, numpy.array(tokens_tagged)[:, 0], lang_code)

        tokens_tagged = [(token, tag)
                         for token, tag in zip(tokens_lemmatized, numpy.array(tokens_tagged)[:, 1])]

    if not settings['puncs']:
        tokens_tagged = [(token, tag)
                         for token, tag in tokens_tagged
                         if [char for char in token if char.isalnum()]]

    return tokens_tagged

def wordless_postprocess_tokens(main, tokens, lang_code, settings):
    if settings['words']:
        if not settings['treat_as_lowercase']:
            if not settings['lowercase']:
                tokens = [token for token in tokens if not token.islower()]
            if not settings['uppercase']:
                tokens = [token for token in tokens if not token.isupper()]
            if not settings['title_case']:
                tokens = [token for token in tokens if not token.istitle()]

        if settings['filter_stop_words']:
            tokens = wordless_filter_stop_words(main, tokens, lang_code)
    else:
        tokens = [token for token in tokens if not [char for char in token if char.isalpha()]]
    
    if not settings['nums']:
        tokens = [token for token in tokens if not token.isnumeric()]

    return tokens

def wordless_postprocess_freq_colligation(main, collocates_freq_file, tokens, lang_code, settings):
    tokens_filtered = wordless_postprocess_tokens(main, tokens, lang_code, settings)

    collocates_freq_file = {collocate: freq_files
                            for (collocate, freq_files), token in zip(collocates_freq_file.items(), tokens_filtered)
                            if token in tokens_filtered}

    return collocates_freq_file
