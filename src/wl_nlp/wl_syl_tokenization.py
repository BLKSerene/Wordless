# ----------------------------------------------------------------------
# Wordless: NLP - Syllable Tokenization
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

import re

import pythainlp
import ssg

from wl_checking import wl_checking_token
from wl_nlp import wl_nlp_utils, wl_word_tokenization

def wl_syl_tokenize(main, inputs, lang, syl_tokenizer = 'default'):
    if inputs and lang in main.settings_global['syl_tokenizers']:
        syls_tokens = []

        if syl_tokenizer == 'default':
            syl_tokenizer = main.settings_custom['syl_tokenization']['syl_tokenizers'][lang]

        wl_nlp_utils.init_syl_tokenizers(
            main,
            lang = lang,
            syl_tokenizer = syl_tokenizer
        )

        if type(inputs) == str:
            syls_tokens = wl_syl_tokenize_text(main, inputs, lang, syl_tokenizer)
        else:
            syls_tokens = wl_syl_tokenize_tokens(main, inputs, lang, syl_tokenizer)
    else:
        if type(inputs) == str:
            syls_tokens = [[token] for token in wl_word_tokenization.wl_word_tokenize_flat(main, inputs, lang = lang)]
        else:
            syls_tokens = [[token] for token in inputs]

    return syls_tokens

def wl_syl_tokenize_text(main, text, lang, syl_tokenizer):
    syls_tokens = []

    tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

    for token in tokens:
        # Pyphen
        if syl_tokenizer.startswith('pyphen_'):
            pyphen_syl_tokenizer = main.__dict__[f'pyphen_syl_tokenizer_{lang}']

            syls_tokens.append(re.split(r'\-+', pyphen_syl_tokenizer.inserted(token)))
        # Thai
        elif syl_tokenizer == 'pythainlp_tha':
            syls_tokens.append(pythainlp.syllable_tokenize(token))
        elif syl_tokenizer == 'ssg_tha':
            syls_tokens.append(ssg.syllable_tokenize(token))

    return syls_tokens


def wl_syl_tokenize_tokens(main, tokens, lang, syl_tokenizer = 'default'):
    syls_tokens = []

    for token in tokens:
        # Pyphen
        if syl_tokenizer.startswith('pyphen_'):
            pyphen_syl_tokenizer = main.__dict__[f'pyphen_syl_tokenizer_{lang}']

            syls_tokens.append(re.split(r'\-+', pyphen_syl_tokenizer.inserted(token)))
        # Thai
        elif syl_tokenizer == 'pythainlp_tha':
            syls_tokens.append(pythainlp.syllable_tokenize(token))
        elif syl_tokenizer == 'ssg_tha':
            syls_tokens.append(ssg.syllable_tokenize(token))

    return syls_tokens

# Excluding punctuations
def wl_syl_tokenize_no_puncs(main, tokens, lang, syl_tokenizer = 'default'):
    syls_tokens = wl_syl_tokenize(main, tokens, lang, syl_tokenizer = syl_tokenizer)

    for i, syls in reversed(list(enumerate(syls_tokens))):
        if len(syls) == 1 and wl_checking_token.is_punc(syls[0]):
            del syls_tokens[i]

    return syls_tokens
