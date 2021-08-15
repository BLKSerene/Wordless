#
# Wordless: Text - Syllable Tokenization
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

from wl_text import wl_text_utils

def wl_syl_tokenize(main, tokens, lang, syl_tokenizer = 'default'):
    syls = []

    if lang not in main.settings_global['syl_tokenizers']:
        lang = 'other'

    if syl_tokenizer == 'default':
        syl_tokenizer = main.settings_custom['syl_tokenization']['syl_tokenizers'][lang]

    wl_text_utils.init_syl_tokenizers(
        main,
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )

    # Pyphen
    if 'Pyphen' in syl_tokenizer:
        pyphen_syl_tokenizer = main.__dict__[f'pyphen_syl_tokenizer_{lang}']

        for token in tokens:
            syls.append(re.split(r'\-+', pyphen_syl_tokenizer.inserted(token)))

    return syls
