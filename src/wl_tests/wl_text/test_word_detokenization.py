# ----------------------------------------------------------------------
# Wordless: Tests - Text - Word Detokenization
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

import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init, wl_test_lang_examples
from wl_text import wl_word_detokenization, wl_word_tokenization
from wl_utils import wl_conversion, wl_misc

main = wl_test_init.Wl_Test_Main()

LANGS_DETOKENIZATION = ['zho_cn', 'zho_tw', 'eng_gb', 'jpn', 'tha', 'bod', 'other']

@pytest.mark.parametrize('lang', LANGS_DETOKENIZATION)
def test_word_detokenize(lang):
    lang_text = wl_conversion.to_lang_text(main, lang)

    print(f'{lang_text} ({lang}):')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f"SENTENCE_{lang.upper() if lang != 'other' else 'ENG_GB'}"),
        lang = lang
    )
    text = wl_word_detokenization.wl_word_detokenize(
        main,
        tokens = tokens,
        lang = lang
    )

    print(text)

    if lang == 'zho_cn':
        assert text == '汉语，又称汉文、中文、中国话、中国语、华语、华文、唐话[2] ，或被视为一个语族，或被视为隶属于汉藏语系汉语族之一种语言。'
    elif lang == 'zho_tw':
        assert text == '漢語，又稱漢文、中文、中國話、中國語、華語、華文、唐話[2] ，或被視為一個語族，或被視為隸屬於漢藏語系漢語族之一種語言。'
    elif lang == 'eng_gb':
        assert text == 'English is a West Germanic language of the Indo - European language family, originally spoken by the inhabitants of early medieval England.[3][4][5]'
    elif lang == 'jpn':
        assert text == '日本語（にほんご、にっぽんご[注2]、英: Japanese ）は、日本国内や、かつての日本領だった国、そして日本人同士の間で使用されている言語。'
    elif lang == 'tha':
        assert text == 'ภาษาไทยหรือภาษาไทยกลางเป็นภาษาราชการและภาษาประจำชาติของประเทศไทย'
    elif lang == 'bod':
        assert text == 'བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་དེའི་ཉེ་འཁོར་གྱི་ས་ཁུལ་ཏེ།'
    elif lang == 'other':
        assert text == 'English is a West Germanic language of the Indo - European language family, originally spoken by the inhabitants of early medieval England.[3][4][5]'
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

if __name__ == '__main__':
    for lang in LANGS_DETOKENIZATION:
        test_word_detokenize(lang)
