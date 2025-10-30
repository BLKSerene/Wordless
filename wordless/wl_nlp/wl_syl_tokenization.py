# ----------------------------------------------------------------------
# Wordless: NLP - Syllable tokenization
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import re

import pythainlp

from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_misc

def wl_syl_tokenize(main, inputs, lang, syl_tokenizer = 'default', force = False):
    if (
        not isinstance(inputs, str)
        and inputs
        and list(inputs)[0].syls is not None
        and not force
    ):
        return inputs
    else:
        if inputs and lang in main.settings_global['syl_tokenizers']:
            if syl_tokenizer == 'default':
                syl_tokenizer = main.settings_custom['syl_tokenization']['syl_tokenizer_settings'][lang]

            wl_nlp_utils.init_syl_tokenizers(
                main,
                lang = lang,
                syl_tokenizer = syl_tokenizer
            )

            # Only for Settings - Syllable Tokenization - Preview
            if isinstance(inputs, str):
                tokens, syls_tokens = wl_syl_tokenize_text(main, inputs, lang, syl_tokenizer)
            else:
                texts, token_properties = wl_texts.split_texts_properties(inputs)

                syls_tokens = wl_syl_tokenize_tokens(main, texts, lang, syl_tokenizer)

            # Remove empty syllables and whitespace around syllables
            syls_tokens = [
                tuple(wl_nlp_utils.clean_texts(syls)) if syls != ('\n',) else syls
                for syls in syls_tokens
            ]

            if isinstance(inputs, str):
                wl_texts.set_token_properties(tokens, 'syls', syls_tokens)

                return tokens
            else:
                tokens = wl_texts.combine_texts_properties(texts, token_properties)
                wl_texts.set_token_properties(tokens, 'syls', syls_tokens)

                wl_texts.update_token_properties(inputs, tokens)

                return inputs
        # Do not set syllable properties if syllable tokenization is not supported
        else:
            if isinstance(inputs, str):
                tokens = wl_word_tokenization.wl_word_tokenize_flat(main, inputs, lang = lang)

                return tokens
            else:
                return inputs

def wl_syl_tokenize_text(main, text, lang, syl_tokenizer):
    tokens = []
    syls_tokens = []

    for para in wl_word_tokenization.wl_word_tokenize(main, text, lang = lang):
        para = list(wl_misc.flatten_list(para))

        if para:
            tokens.extend(para)
            syls_tokens.extend(wl_syl_tokenize_tokens(
                main,
                tokens = wl_texts.to_token_texts(para),
                lang = lang,
                syl_tokenizer = syl_tokenizer
            ))

        tokens.append(wl_texts.Wl_Token('\n'))
        syls_tokens.append(('\n',))

    if tokens:
        del tokens[-1]
        del syls_tokens[-1]

    return tokens, syls_tokens

def wl_syl_tokenize_tokens(main, tokens, lang, syl_tokenizer):
    tokens_syls = {}

    # Only syllabify types as context information is not needed
    for token in set(tokens):
        if token:
            # NLTK
            if syl_tokenizer == 'nltk_legality':
                nltk_syl_tokenizer_legality = main.__dict__['nltk_syl_tokenizer_legality']

                tokens_syls[token] = nltk_syl_tokenizer_legality.tokenize(token)
            elif syl_tokenizer == 'nltk_sonority_sequencing':
                nltk_syl_tokenizer_sonority_sequencing = main.__dict__['nltk_syl_tokenizer_sonority_sequencing']

                tokens_syls[token] = nltk_syl_tokenizer_sonority_sequencing.tokenize(token)
            # Pyphen
            elif syl_tokenizer.startswith('pyphen_'):
                pyphen_syl_tokenizer = main.__dict__[f'pyphen_syl_tokenizer_{lang}']
                syls = re.split(r'\-+', pyphen_syl_tokenizer.inserted(token))

                if any(syls):
                    tokens_syls[token] = syls
                else:
                    tokens_syls[token] = [token]
            # Thai
            elif syl_tokenizer == 'pythainlp_han_solo':
                tokens_syls[token] = pythainlp.tokenize.syllable_tokenize(token, engine = 'han_solo')
            elif syl_tokenizer == 'pythainlp_syl_dict':
                tokens_syls[token] = pythainlp.tokenize.syllable_tokenize(token, engine = 'dict')

    return [tokens_syls[token] if token else [] for token in tokens]
