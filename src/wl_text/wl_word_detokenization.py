#
# Wordless: Text - Word Detokenization
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

import nltk
import sacremoses

from wl_checking import wl_checking_unicode
from wl_text import wl_text
from wl_utils import wl_conversion

def wl_word_detokenize(main, tokens, lang, word_detokenizer = 'default'):
    sentence_start = 0
    sentences = []
    text = ''

    if lang not in main.settings_global['word_detokenizers']:
        lang = 'other'

    if word_detokenizer == 'default':
        word_detokenizer = main.settings_custom['word_detokenization']['word_detokenizers'][lang]

    for i, token in enumerate(tokens):
        if type(token) == wl_text.Wl_Token and token.sentence_ending:
            sentences.append(tokens[sentence_start : i + 1])

            sentence_start = i + 1
        elif i == len(tokens) - 1:
            sentences.append(tokens[sentence_start:])

    # English & Other Languages
    if word_detokenizer == main.tr('NLTK - Penn Treebank Detokenizer'):
        treebank_detokenizer = nltk.tokenize.treebank.TreebankWordDetokenizer()

        for sentence in sentences:
            text += treebank_detokenizer.tokenize(tokens)
    elif word_detokenizer == main.tr('Sacremoses - Moses Detokenizer'):
        moses_detokenizer = sacremoses.MosesDetokenizer(lang = wl_conversion.to_iso_639_1(main, lang))

        for sentence in sentences:
            text += moses_detokenizer.detokenize(sentence)
    # Chinese
    elif word_detokenizer == main.tr('Wordless - Chinese Word Detokenizer'):
        non_cjk_start = 0

        for i, token in enumerate(tokens):
            if i >= non_cjk_start:
                if (wl_checking_unicode.has_han(token) or
                    all(map(str.isnumeric, token))):
                    text += token

                    non_cjk_start += 1
                else:
                    # English
                    if wl_checking_unicode.is_eng_token(token):
                        for j, token in enumerate(tokens[i:]):
                            if i + j + 1 == len(tokens) or not wl_checking_unicode.is_eng_token(tokens[i + j + 1]):
                                text += wl_word_detokenize(
                                    main, tokens[non_cjk_start : i + j + 1],
                                    lang = 'eng'
                                )

                                non_cjk_start = i + j + 1

                                break
                    # Other Languages
                    else:
                        for j, token in enumerate(tokens[i:]):
                            if (i + j + 1 == len(tokens) or
                                wl_checking_unicode.has_han(tokens[i + j + 1])):
                                text += wl_word_detokenize(
                                    main, tokens[non_cjk_start : i + j + 1],
                                    lang = 'other'
                                )

                                non_cjk_start = i + j + 1

                                break
    elif word_detokenizer == main.tr('Wordless - Japanese Word Detokenizer'):
        non_cjk_start = 0

        for i, token in enumerate(tokens):
            if i < non_cjk_start:
                continue

            if (wl_checking_unicode.has_han(token) or
                wl_checking_unicode.has_kana(token) or
                all(map(str.isnumeric, token))):
                text += token

                non_cjk_start = i + 1
            else:
                # English
                if wl_checking_unicode.is_eng_token(token):
                    for j, token in enumerate(tokens[i:]):
                        if i + j + 1 == len(tokens) or not wl_checking_unicode.is_eng_token(tokens[i + j + 1]):
                            text += wl_word_detokenize(
                                main, tokens[non_cjk_start : i + j + 1],
                                lang = 'eng'
                            )

                            non_cjk_start = i + j + 1

                            break
                # Other Languages
                else:
                    for j, token in enumerate(tokens[i:]):
                        if (i + j + 1 == len(tokens) or
                            wl_checking_unicode.has_han(tokens[i + j + 1]) or
                            wl_checking_unicode.has_kana(tokens[i + j + 1])):
                            text += wl_word_detokenize(
                                main, tokens[non_cjk_start : i + j + 1],
                                lang = 'other'
                            )

                            non_cjk_start = i + j + 1

                            break
    # Thai
    elif word_detokenizer in main.tr('Wordless - Thai Word Detokenizer'):
        non_thai_start = 0

        for i, token in enumerate(tokens):
            if i < non_thai_start:
                continue

            if wl_checking_unicode.has_thai(token):
                if type(token) == wl_text.Wl_Token:
                    text += token + token.boundary
                else:
                    text += token

                non_thai_start = i + 1
            else:
                # English
                if wl_checking_unicode.is_eng_token(token):
                    for j, token in enumerate(tokens[i:]):
                        if i + j + 1 == len(tokens) or not wl_checking_unicode.is_eng_token(tokens[i + j + 1]):
                            text += wl_word_detokenize(
                                main, tokens[non_thai_start : i + j + 1],
                                lang = 'eng'
                            )

                            non_thai_start = i + j + 1

                            break
                # Other Languages
                else:
                    for j, token in enumerate(tokens[i:]):
                        if (i + j + 1 == len(tokens) or
                            wl_checking_unicode.has_thai(tokens[i + j + 1])):
                            text += wl_word_detokenize(
                                main, tokens[non_thai_start : i + j + 1],
                                lang = 'other'
                            )

                            non_thai_start = i + j + 1

                            break
    # Tibetan
    elif word_detokenizer == main.tr('Wordless - Tibetan Word Detokenizer'):
        non_tibetan_start = 0

        for i, token in enumerate(tokens):
            if i < non_tibetan_start:
                continue

            if wl_checking_unicode.has_tibetan(token):
                # Check for Tibetan Mark Shad
                # See: https://w3c.github.io/tlreq/#section_breaks
                if i > 0 and token[0] == '།':
                    text += token
                else:
                    text += token

                non_tibetan_start = i + 1
            else:
                # English
                if wl_checking_unicode.is_eng_token(token):
                    for j, token in enumerate(tokens[i:]):
                        if i + j + 1 == len(tokens) or not wl_checking_unicode.is_eng_token(tokens[i + j + 1]):
                            text += wl_word_detokenize(
                                main, tokens[non_tibetan_start : i + j + 1],
                                lang = 'eng'
                            )

                            non_tibetan_start = i + j + 1

                            break
                # Other Languages
                else:
                    for j, token in enumerate(tokens[i:]):
                        if (i + j + 1 == len(tokens) or
                            wl_checking_unicode.has_tibetan(tokens[i + j + 1])):
                            text += wl_word_detokenize(
                                main, tokens[non_tibetan_start : i + j + 1],
                                lang = 'other'
                            )

                            non_tibetan_start = i + j + 1

                            break

    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()
