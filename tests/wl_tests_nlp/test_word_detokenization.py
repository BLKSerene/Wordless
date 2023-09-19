# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Word detokenization
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_word_detokenization, wl_word_tokenization
from wordless.wl_utils import wl_misc

_, is_macos, _ = wl_misc.check_os()

main = wl_test_init.Wl_Test_Main()
wl_test_init.change_default_tokenizers(main)

test_langs = (
    ['zho_cn', 'zho_tw', 'eng_us', 'jpn', 'tha']
    + [pytest.param(
        'bod',
        marks = pytest.mark.xfail(is_macos, reason = 'https://github.com/OpenPecha/Botok/issues/76')
    )]
    + ['other']
)
test_langs_local = ['zho_cn', 'zho_tw', 'eng_us', 'jpn', 'tha', 'bod', 'other']

@pytest.mark.parametrize('lang', test_langs)
def test_word_detokenize(lang):
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    text = wl_word_detokenization.wl_word_detokenize(
        main,
        tokens = tokens,
        lang = lang
    )

    print(f'{lang}:')
    print(f'{text}\n')

    if lang == 'zho_cn':
        assert text == '汉语又称中文、华语[6]、唐话[7] ，概指由上古汉语（先秦雅言）发展而来、书面使用汉字的分析语，为汉藏语系最大的一支语族。'
    elif lang == 'zho_tw':
        assert text == '漢語又稱中文、華語[6]、唐話[7] ，概指由上古漢語（先秦雅言）發展而來、書面使用漢字的分析語，為漢藏語系最大的一支語族。'
    elif lang in ['eng_us', 'other']:
        assert text == 'English is a West Germanic language in the Indo-European language family that originated in early medieval England. [3] [4] [5]'
    elif lang == 'jpn':
        assert text == '日本語（にほんご、にっぽんご[注釈2]、英語: Japanese language ）は、日本国内や、かつての日本領だった国、そして国外移民や移住者を含む日本人同士の間で使用されている言語。'
    elif lang == 'tha':
        assert text == 'ภาษาไทยหรือภาษาไทยกลางเป็นภาษาในกลุ่มภาษาไทซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า - ไทและเป็นภาษาราชการและภาษาประจำชาติของประเทศไทย [ 3 ][ 4 ]'
    elif lang == 'bod':
        assert text == 'བོད་ཀྱི་སྐད་ཡིག་ནི་བོད་ཡུལ་དང་ཉེ་འཁོར་གྱི་ས་ཁུལ་བལ་ཡུལ།འབྲུག་དང་འབྲས་ལྗོངས།'
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

if __name__ == '__main__':
    for lang in test_langs_local:
        test_word_detokenize(lang)
