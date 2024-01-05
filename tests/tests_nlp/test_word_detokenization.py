# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Word detokenization
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

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
    if lang.startswith('zho_'):
        text = '英国全称是United Kingdom of Great Britain，由四个部分组成：England、Scotland、Wales和Northern Ireland'
    elif lang == 'jpn':
        text = '''The meaning of "天気がいいから、散歩しましょう。" is: The weather is good so let's take a walk.'''
    elif lang == 'bod':
        text = 'Test this Tibetan string: དུང་དང་འོ་མར་འགྲན་པའི་ལྷག་བསམ་མཐུ། །དམན་ཡང་དཀར་པོའི་བྱས་འབྲས་ཅུང་ཟད་ཅིག །བློ་དང་འདུན་པ་བཟང་བའི་རང་རིགས་ཀུན། །རྒྱལ་ཁའི་འཕྲིན་བཟང་ལས་དོན་འགྲུབ་ཕྱིར་འབད།།. Does detokenization work as expected?'
    else:
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = text,
        lang = lang
    )

    text = wl_word_detokenization.wl_word_detokenize(
        main,
        tokens = tokens,
        lang = lang
    )

    print(f'{lang}:')
    print(f'{text}\n')

    if lang.startswith('zho_'):
        assert text == '英国全称是United Kingdom of Great Britain，由四个部分组成：England、Scotland、Wales和Northern Ireland'
    elif lang in ['eng_us', 'other']:
        assert text == 'English is a West Germanic language in the Indo-European language family.'
    elif lang == 'jpn':
        assert text == '''The meaning of "天気がいいから、散歩しましょう。"is: The weather is good so let 's take a walk.'''
    elif lang == 'tha':
        assert text == 'ภาษาไทยหรือภาษาไทยกลางเป็นภาษาในกลุ่มภาษาไทซึ่งเป็นกลุ่มย่อยของตระกูลภาษาขร้า - ไทและเป็นภาษาราชการและภาษาประจำชาติของประเทศไทย [ 3 ][ 4 ]'
    elif lang == 'bod':
        assert text == 'Test this Tibetan string: དུང་དང་འོ་མར་འགྲན་པའི་ལྷག་བསམ་མཐུ། །དམན་ཡང་དཀར་པོའི་བྱས་འབྲས་ཅུང་ཟད་ཅིག །བློ་དང་འདུན་པ་བཟང་བའི་རང་རིགས་ཀུན། །རྒྱལ་ཁའི་འཕྲིན་བཟང་ལས་དོན་འགྲུབ་ཕྱིར་འབད།།'
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

if __name__ == '__main__':
    for lang in test_langs_local:
        test_word_detokenize(lang)
