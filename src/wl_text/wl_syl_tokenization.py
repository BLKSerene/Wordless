#
# Wordless: Text - Syllable Tokenization
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

import pythainlp
import ssg

from wl_checking import wl_checking_token
from wl_text import wl_text_utils

def wl_syl_tokenize(main, tokens, lang, syl_tokenizer = 'default'):
    syls_tokens = []

    if lang in main.settings_global['syl_tokenizers']:
        if syl_tokenizer == 'default':
            syl_tokenizer = main.settings_custom['syl_tokenization']['syl_tokenizers'][lang]

        wl_text_utils.init_syl_tokenizers(
            main,
            lang = lang,
            syl_tokenizer = syl_tokenizer
        )

        for token in tokens:
            # Pyphen
            if 'pyphen' in syl_tokenizer:
                pyphen_syl_tokenizer = main.__dict__[f'pyphen_syl_tokenizer_{lang}']

                syls_tokens.append(re.split(r'\-+', pyphen_syl_tokenizer.inserted(token)))
            # Thai
            elif syl_tokenizer == 'pythainlp_tha':
                syls_tokens.append(pythainlp.syllable_tokenize(token))
            elif syl_tokenizer == 'ssg_tha':
                syls_tokens.append(ssg.syllable_tokenize(token))

    return syls_tokens

# Syllable tokenization excluding punctuations
def wl_syl_tokenize_no_puncs(main, tokens, lang, syl_tokenizer = 'default'):
    syls_tokens = wl_syl_tokenize(main, tokens, lang, syl_tokenizer = syl_tokenizer)

    for i, syls in reversed(list(enumerate(syls_tokens))):
        if len(syls) == 1 and wl_checking_token.is_punc(syls[0]):
            del syls_tokens[i]

    return syls_tokens
