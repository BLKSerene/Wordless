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

from wordless.wl_checking import wl_checking_tokens
from wordless.wl_nlp import wl_nlp_utils, wl_word_tokenization

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

        section_size = main.settings_custom['files']['misc_settings']['read_files_in_chunks']

        if isinstance(inputs, str):
            for line in inputs.splitlines():
                syls_tokens.extend(wl_syl_tokenize_text(main, line, lang, syl_tokenizer))
        else:
            texts = wl_nlp_utils.to_sections_unequal(inputs, section_size = section_size * 50)

            for tokens in texts:
                syls_tokens.extend(wl_syl_tokenize_tokens(main, tokens, lang, syl_tokenizer))
    else:
        if isinstance(inputs, str):
            syls_tokens = [[token] for token in wl_word_tokenization.wl_word_tokenize_flat(main, inputs, lang = lang)]
        else:
            syls_tokens = [[token] for token in inputs]

    # Remove emtpy syllables and whitespace around syllables
    syls_tokens = [
        [syl_clean for syl in syls if (syl_clean := syl.strip())]
        for syls in syls_tokens
        if any(syls)
    ]

    return syls_tokens

def wl_syl_tokenize_text(main, text, lang, syl_tokenizer):
    tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

    return wl_syl_tokenize_tokens(main, tokens, lang, syl_tokenizer)

def wl_syl_tokenize_tokens(main, tokens, lang, syl_tokenizer = 'default'):
    syls_tokens = []

    for token in tokens:
        # NLTK
        if syl_tokenizer == 'nltk_legality':
            nltk_syl_tokenizer_legality = main.__dict__['nltk_syl_tokenizer_legality']

            syls_tokens.append(nltk_syl_tokenizer_legality.tokenize(token))
        elif syl_tokenizer == 'nltk_sonority_sequencing':
            nltk_syl_tokenizer_sonority_sequencing = main.__dict__['nltk_syl_tokenizer_sonority_sequencing']

            syls_tokens.append(nltk_syl_tokenizer_sonority_sequencing.tokenize(token))
        # Pyphen
        elif syl_tokenizer.startswith('pyphen_'):
            pyphen_syl_tokenizer = main.__dict__[f'pyphen_syl_tokenizer_{lang}']
            syls = re.split(r'\-+', pyphen_syl_tokenizer.inserted(token))

            if any(syls):
                syls_tokens.append(syls)
            else:
                syls_tokens.append([token])
        # Thai
        elif syl_tokenizer == 'pythainlp_tha':
            syls_tokens.append(pythainlp.subword_tokenize(token, engine = 'dict'))

    return syls_tokens

# Excluding punctuations
def wl_syl_tokenize_tokens_no_puncs(main, tokens, lang, syl_tokenizer = 'default'):
    syls_tokens = wl_syl_tokenize(main, tokens, lang, syl_tokenizer = syl_tokenizer)

    for i, syls in reversed(list(enumerate(syls_tokens))):
        if len(syls) == 1 and wl_checking_tokens.is_punc(syls[0]):
            del syls_tokens[i]

    return syls_tokens
