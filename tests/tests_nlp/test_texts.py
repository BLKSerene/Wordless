# ----------------------------------------------------------------------
# Tests: NLP - Texts
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

import copy

from tests import wl_test_init
from wordless.wl_nlp import wl_texts

main = wl_test_init.Wl_Test_Main()

wl_token = wl_texts.Wl_Token('test', tag = '_NN')
wl_tokens = [wl_texts.Wl_Token('test', tag = '_NN')]

def test_check_text():
    assert wl_texts.check_text('test') == 'test'
    assert wl_texts.check_text(None) == ''

def test_check_texts():
    assert wl_texts.check_texts(['test', None]) == ['test', '']

def test_wl_token():
    wl_token = wl_texts.Wl_Token('test')
    hash(wl_token)
    assert wl_token == wl_texts.Wl_Token('test')
    wl_token.display_text()
    wl_token.display_text(punc_mark = True)
    wl_token.update_properties(wl_token)

def test_to_tokens():
    assert wl_texts.to_display_texts(wl_texts.to_tokens(['test', None], tags = ['_NN', None])) == ['test_NN', '']

def test_display_texts_to_tokens():
    assert wl_texts.display_texts_to_tokens(main, ['test_NN'])[0].display_text() == 'test_NN'

def test_split_texts_properties():
    texts, token_properties = wl_texts.split_texts_properties(wl_tokens)

    assert texts == ['test']
    assert token_properties == [{
        'lang': 'eng_us',
        'syls': None,
        'tag': '_NN',
        'tag_universal': None,
        'content_function': None,
        'lemma': None,
        'head': None,
        'dependency_relation': None,
        'dependency_len': None,
        'punc_mark': None
    }]

def test_combine_texts_properties():
    wl_texts.combine_texts_properties(['test'], [{}])

def test_to_token_texts():
    assert wl_texts.to_token_texts(wl_tokens) == ['test']

def test_to_display_texts():
    assert wl_texts.to_display_texts(wl_tokens) == ['test_NN']

def test_set_token_text():
    assert wl_texts.set_token_text(wl_token, 'tests').display_text() == 'tests_NN'
    assert wl_texts.set_token_text(wl_token, None).display_text() == '_NN'

def test_set_token_texts():
    wl_tokens_copy = copy.deepcopy(wl_tokens)

    wl_texts.set_token_texts(wl_tokens_copy, ['test1'])
    assert wl_texts.to_display_texts(wl_tokens_copy) == ['test1_NN']

    # If the token property is None, the token text should be set to empty
    wl_texts.set_token_texts(wl_tokens_copy, [None])
    assert wl_texts.to_display_texts(wl_tokens_copy) == ['_NN']

def test_has_token_properties():
    assert wl_texts.has_token_properties(wl_tokens, 'tag')
    assert not wl_texts.has_token_properties(wl_tokens, 'lemma')

def test_get_token_properties():
    assert wl_texts.get_token_properties(wl_tokens, 'tag') == ['_NN']
    assert wl_texts.get_token_properties(wl_tokens, 'lemma') == [None]

def test_set_token_properties():
    wl_tokens_copy = copy.deepcopy(wl_tokens)
    wl_texts.set_token_properties(wl_tokens_copy, 'tag', '_NNS')

    assert wl_tokens_copy[0].tag == '_NNS'

def test_update_token_properties():
    wl_tokens_copy = copy.deepcopy(wl_tokens)
    wl_tokens_copy[0].tag = '_NNS'
    wl_texts.update_token_properties(wl_tokens_copy, wl_tokens)

    assert wl_tokens_copy[0].tag == '_NN'

def test_clean_texts():
    assert wl_texts.clean_texts([' test ', ' ']) == ['test']

def test_wl_text_total():
    text_1 = wl_test_init.Wl_Test_Text(main, tokens_multilevel = [], lang = 'eng_us', tagged = False)
    text_2 = wl_test_init.Wl_Test_Text(main, tokens_multilevel = [], lang = 'eng_gb', tagged = True)

    text_total_1 = wl_texts.Wl_Text_Total(texts = [text_1, text_1])
    text_total_2 = wl_texts.Wl_Text_Total(texts = [text_1, text_2])

    assert text_total_1.lang == 'eng_us'
    assert not text_total_1.tagged
    assert text_total_2.lang == 'other'
    assert text_total_2.tagged

if __name__ == '__main__':
    test_check_text()
    test_check_texts()

    test_wl_token()
    test_to_tokens()
    test_display_texts_to_tokens()
    test_split_texts_properties()
    test_combine_texts_properties()
    test_to_token_texts()
    test_to_display_texts()
    test_set_token_text()
    test_set_token_texts()
    test_has_token_properties()
    test_get_token_properties()
    test_set_token_properties()
    test_update_token_properties()
    test_clean_texts()

    test_wl_text_total()
