# ----------------------------------------------------------------------
# Wordless: NLP - Word detokenization
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

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import wl_nlp_utils, wl_texts
from wordless.wl_utils import wl_conversion

def wl_word_detokenize(main, tokens, lang):
    text = ''
    tokens = wl_texts.clean_texts(tokens)

    if lang == 'other':
        lang = 'eng_us'

    wl_nlp_utils.init_word_detokenizers(
        main,
        lang = lang
    )

    # Chinese
    if lang.startswith('zho_'):
        text_temp = []

        for token in tokens:
            if wl_checks_tokens.has_han(token):
                if text_temp:
                    text += wl_word_detokenize(
                        main, text_temp,
                        lang = 'other'
                    )

                    text_temp.clear()

                text += token
            # Other languages
            else:
                text_temp.append(token)

        if text_temp:
            text += wl_word_detokenize(
                main, text_temp,
                lang = 'other'
            )
    # Japanese
    elif lang == 'jpn':
        text_temp = []

        for token in tokens:
            if (
                wl_checks_tokens.has_han(token)
                or wl_checks_tokens.has_kana(token)
            ):
                if text_temp:
                    text += wl_word_detokenize(
                        main, text_temp,
                        lang = 'other'
                    )

                    text_temp.clear()

                text += token
            else:
                text_temp.append(token)

        if text_temp:
            text += wl_word_detokenize(
                main, text_temp,
                lang = 'other'
            )
    # Thai
    elif lang == 'tha':
        text = pythainlp.tokenize.word_detokenize(pythainlp.tokenize.clause_tokenize(tokens))
    # Tibetan
    elif lang == 'bod':
        text_temp = []

        for token in tokens:
            if wl_checks_tokens.has_tibetan(token):
                if text_temp:
                    text += ' ' + wl_word_detokenize(
                        main, text_temp,
                        lang = 'other'
                    ) + ' '

                    text_temp.clear()

                # See: https://w3c.github.io/tlreq/#whitespace
                if (
                    token[0] == '།'
                    and text
                    and text[-1] in ['།', 'ཀ', 'ག']
                ):
                    text += ' ' + token
                elif (
                    token[0] != '།'
                    and text
                    and text[-1] in ['།', '༎']
                    and (len(text) < 3 or text[-3] not in ['།', 'ཀ', 'ག'])
                ):
                    text += ' ' + token
                else:
                    text += token
            # Other languages
            else:
                text_temp.append(token)

        if text_temp:
            text += wl_word_detokenize(
                main, text_temp,
                lang = 'other'
            )
    # Other languages
    else:
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        text = main.__dict__[f'sacremoses_moses_detokenizer_{lang}'].detokenize(tokens)

    text = re.sub(r'\s{2,}', ' ', text).strip()

    return text
