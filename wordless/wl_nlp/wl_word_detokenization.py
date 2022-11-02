# ----------------------------------------------------------------------
# Wordless: NLP - Word Detokenization
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

from wordless.wl_checking import wl_checking_unicode
from wordless.wl_nlp import wl_nlp_utils
from wordless.wl_utils import wl_conversion

def wl_word_detokenize(main, tokens, lang):
    text = ''

    if lang == 'other':
        lang = 'eng_us'

    wl_nlp_utils.init_word_detokenizers(
        main,
        lang = lang
    )

    # Chinese
    if lang.startswith('zho_'):
        non_cjk_start = 0

        for i, token in enumerate(tokens):
            if i >= non_cjk_start:
                if (
                    wl_checking_unicode.has_han(token)
                    or all(map(str.isnumeric, token))
                ):
                    text += token

                    non_cjk_start += 1
                else:
                    # Non-Chinese
                    for j, _ in enumerate(tokens[i:]):
                        if (
                            i + j + 1 == len(tokens)
                            or wl_checking_unicode.has_han(tokens[i + j + 1])
                        ):
                            text += wl_word_detokenize(
                                main,
                                tokens = tokens[non_cjk_start : i + j + 1],
                                lang = 'other'
                            )

                            non_cjk_start = i + j + 1

                            break
    # Japanese
    elif lang == 'jpn':
        non_cjk_start = 0

        for i, token in enumerate(tokens):
            if i < non_cjk_start:
                continue

            if (
                wl_checking_unicode.has_han(token)
                or wl_checking_unicode.has_kana(token)
                or all(map(str.isnumeric, token))
            ):
                text += token

                non_cjk_start = i + 1
            else:
                # Non-Japanese
                for j, _ in enumerate(tokens[i:]):
                    if (
                        i + j + 1 == len(tokens)
                        or wl_checking_unicode.has_han(tokens[i + j + 1])
                        or wl_checking_unicode.has_kana(tokens[i + j + 1])
                    ):
                        text += wl_word_detokenize(
                            main,
                            tokens = tokens[non_cjk_start : i + j + 1],
                            lang = 'other'
                        )

                        non_cjk_start = i + j + 1

                        break
    # Thai
    elif lang == 'tha':
        non_thai_start = 0

        for i, token in enumerate(tokens):
            if i < non_thai_start:
                continue

            if wl_checking_unicode.has_thai(token):
                text += token

                non_thai_start = i + 1
            else:
                # Non-Thai
                for j, _ in enumerate(tokens[i:]):
                    if (
                        i + j + 1 == len(tokens)
                        or wl_checking_unicode.has_thai(tokens[i + j + 1])
                    ):
                        text += wl_word_detokenize(
                            main,
                            tokens = tokens[non_thai_start : i + j + 1],
                            lang = 'other'
                        )

                        non_thai_start = i + j + 1

                        break
    # Tibetan
    elif lang == 'bod':
        non_tibetan_start = 0

        for i, token in enumerate(tokens):
            if i < non_tibetan_start:
                continue

            if wl_checking_unicode.has_tibetan(token):
                # Check for Tibetan Mark Shad
                # See: https://w3c.github.io/tlreq/#section_breaks
                if i > 0 and text[-1] == '།' and token[0] == '།':
                    text += ' ' + token
                else:
                    text += token

                non_tibetan_start = i + 1
            else:
                # Non-Tibetan
                for j, _ in enumerate(tokens[i:]):
                    if (
                        i + j + 1 == len(tokens)
                        or wl_checking_unicode.has_tibetan(tokens[i + j + 1])
                    ):
                        text += wl_word_detokenize(
                            main,
                            tokens = tokens[non_tibetan_start : i + j + 1],
                            lang = 'other'
                        )

                        non_tibetan_start = i + j + 1

                        break
    # Other Languages
    else:
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        text = main.__dict__[f'sacremoses_moses_detokenizer_{lang}'].detokenize(tokens)

    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()
