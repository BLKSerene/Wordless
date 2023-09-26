# ----------------------------------------------------------------------
# Wordless: Tests - NLP - NLP utilities
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

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_nlp_utils

main = wl_test_init.Wl_Test_Main()

settings_lang_utils = main.settings_global['mapping_lang_utils']

def test_to_lang_util_code():
    for util_type, utils in settings_lang_utils.items():
        for util_text, util_code in utils.items():
            lang_util_code = wl_nlp_utils.to_lang_util_code(main, util_type, util_text)

            assert lang_util_code == util_code

def test_to_lang_util_codes():
    for util_type, utils in settings_lang_utils.items():
        lang_util_codes = wl_nlp_utils.to_lang_util_codes(main, util_type, utils.keys())

        assert list(lang_util_codes) == list(utils.values())

def test_to_lang_util_text():
    for util_type, utils in settings_lang_utils.items():
        TO_LANG_UTIL_TEXT = {
            util_code: util_text
            for util_text, util_code in utils.items()
        }

        for util_code in utils.values():
            lang_util_text = wl_nlp_utils.to_lang_util_text(main, util_type, util_code)

            assert lang_util_text == TO_LANG_UTIL_TEXT[util_code]

def test_to_lang_util_texts():
    for util_type, utils in settings_lang_utils.items():
        TO_LANG_UTIL_TEXT = {
            util_code: util_text
            for util_text, util_code in utils.items()
        }

        util_texts = wl_nlp_utils.to_lang_util_texts(main, util_type, utils.values())

        assert list(util_texts) == list(TO_LANG_UTIL_TEXT.values())

def test_check_models():
    assert wl_nlp_utils.check_models(main, langs = ['eng_us', 'eng_gb'])

def test_init_model_spacy():
    wl_nlp_utils.init_model_spacy(main, lang = 'eng_us')
    wl_nlp_utils.init_model_spacy(main, lang = 'eng_gb')
    wl_nlp_utils.init_model_spacy(main, lang = 'other')
    wl_nlp_utils.init_model_spacy(main, lang = 'afr')
    wl_nlp_utils.init_model_spacy(main, lang = 'srp_cyrl')
    wl_nlp_utils.init_model_spacy(main, lang = 'srp_latn')

    wl_nlp_utils.init_model_spacy(main, lang = 'afr', sentencizer_only = True)

    assert 'spacy_nlp_eng' in main.__dict__
    assert 'spacy_nlp_eng_us' not in main.__dict__
    assert 'spacy_nlp_eng_gb' not in main.__dict__
    assert 'spacy_nlp_other' in main.__dict__
    assert 'spacy_nlp_afr' in main.__dict__
    assert 'spacy_nlp_srp' in main.__dict__
    assert 'spacy_nlp_srp_cyrl' not in main.__dict__
    assert 'spacy_nlp_srp_latn' not in main.__dict__

    assert 'spacy_nlp_sentencizer' in main.__dict__

def test_init_model_stanza():
    wl_nlp_utils.init_model_stanza(main, lang = 'eng_us', lang_util = 'sentence_tokenizer')
    wl_nlp_utils.init_model_stanza(main, lang = 'eng_gb', lang_util = 'sentence_tokenizer')
    wl_nlp_utils.init_model_stanza(main, lang = 'other', lang_util = 'sentence_tokenizer')
    wl_nlp_utils.init_model_stanza(main, lang = 'srp_cyrl', lang_util = 'sentence_tokenizer')

    assert 'stanza_nlp_eng' in main.__dict__
    assert 'stanza_nlp_eng_us' not in main.__dict__
    assert 'stanza_nlp_eng_gb' not in main.__dict__
    assert 'stanza_nlp_other' in main.__dict__

    assert 'stanza_nlp_srp_cyrl' not in main.__dict__

def test_init_sudachipy_word_tokenizer():
    wl_nlp_utils.init_sudachipy_word_tokenizer(main)

    assert 'sudachipy_word_tokenizer' in main.__dict__

def test_to_sections():
    tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    token_sections_5 = wl_nlp_utils.to_sections(tokens, num_sections = 5)
    token_sections_1 = wl_nlp_utils.to_sections(tokens, num_sections = 1)
    token_sections_1000 = wl_nlp_utils.to_sections(tokens, num_sections = 1000)

    assert token_sections_5 == [[1, 2, 3], [4, 5, 6], [7, 8], [9, 10], [11, 12]]
    assert token_sections_1 == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
    assert token_sections_1000 == [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]

def test_to_sections_unequal():
    tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    token_sections_5 = list(wl_nlp_utils.to_sections_unequal(tokens, section_size = 5))
    token_sections_1 = list(wl_nlp_utils.to_sections_unequal(tokens, section_size = 1))
    token_sections_1000 = list(wl_nlp_utils.to_sections_unequal(tokens, section_size = 1000))

    assert token_sections_5 == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12]]
    assert token_sections_1 == [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]
    assert token_sections_1000 == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]

def test_split_into_chunks_text():
    text = '\n\n \n 1\n2 \n\n 3 \n \n\n'

    sections_1 = list(wl_nlp_utils.split_into_chunks_text(text, section_size = 1))
    sections_2 = list(wl_nlp_utils.split_into_chunks_text(text, section_size = 2))
    sections_3 = list(wl_nlp_utils.split_into_chunks_text(text, section_size = 3))

    assert sections_1 == ['\n', '\n', ' \n', ' 1\n', '2 \n', '\n', ' 3 \n', ' \n', '\n']
    assert sections_2 == ['\n\n', ' \n 1\n', '2 \n\n', ' 3 \n \n', '\n']
    assert sections_3 == ['\n\n \n', ' 1\n2 \n\n', ' 3 \n \n\n']

def test_split_token_list():
    tokens = ['test'] * 10000

    assert len(list(wl_nlp_utils.split_token_list(main, tokens, nlp_util = 'sudachipy_jpn'))) == 5
    assert len(list(wl_nlp_utils.split_token_list(main, tokens, nlp_util = 'test'))) == 10

def test_srp_cyrl_to_latn():
    tokens_srp_cyrl = wl_test_lang_examples.SENTENCE_SRP_CYRL.split()

    assert ' '.join(wl_nlp_utils.to_srp_latn(tokens_srp_cyrl)) == wl_test_lang_examples.SENTENCE_SRP_LATN

def test_srp_latn_to_cyrl():
    tokens_srp_latn = wl_test_lang_examples.SENTENCE_SRP_LATN.split()

    assert ' '.join(wl_nlp_utils.to_srp_cyrl(tokens_srp_latn)) == wl_test_lang_examples.SENTENCE_SRP_CYRL

def test_ngrams():
    assert list(wl_nlp_utils.ngrams(range(5), 1)) == [(0,), (1,), (2,), (3,), (4,)]
    assert list(wl_nlp_utils.ngrams(range(5), 2)) == [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert list(wl_nlp_utils.ngrams(range(5), 3)) == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
    assert list(wl_nlp_utils.ngrams(range(5), 4)) == [(0, 1, 2, 3), (1, 2, 3, 4)]
    assert list(wl_nlp_utils.ngrams(range(5), 5)) == [(0, 1, 2, 3, 4)]
    assert not list(wl_nlp_utils.ngrams(range(5), 6))

def test_everygrams():
    assert list(wl_nlp_utils.everygrams(range(5), 1, 1)) == list(wl_nlp_utils.ngrams(range(5), 1))
    assert list(wl_nlp_utils.everygrams(range(5), 1, 2)) == [(0,), (0, 1), (1,), (1, 2), (2,), (2, 3), (3,), (3, 4), (4,)]
    assert list(wl_nlp_utils.everygrams(range(5), 2, 2)) == list(wl_nlp_utils.ngrams(range(5), 2))
    assert list(wl_nlp_utils.everygrams(range(5), 2, 3)) == [(0, 1), (0, 1, 2), (1, 2), (1, 2, 3), (2, 3), (2, 3, 4), (3, 4)]
    assert list(wl_nlp_utils.everygrams(range(5), 2, 4)) == [(0, 1), (0, 1, 2), (0, 1, 2, 3), (1, 2), (1, 2, 3), (1, 2, 3, 4), (2, 3), (2, 3, 4), (3, 4)]
    assert list(wl_nlp_utils.everygrams(range(5), 2, 5)) == [(0, 1), (0, 1, 2), (0, 1, 2, 3), (0, 1, 2, 3, 4), (1, 2), (1, 2, 3), (1, 2, 3, 4), (2, 3), (2, 3, 4), (3, 4)]
    assert list(wl_nlp_utils.everygrams(range(5), 6, 6)) == list(wl_nlp_utils.ngrams(range(5), 6))

def test_skipgrams():
    assert list(wl_nlp_utils.skipgrams(range(5), 1, 0)) == list(wl_nlp_utils.ngrams(range(5), 1))
    assert list(wl_nlp_utils.skipgrams(range(5), 1, 9)) == list(wl_nlp_utils.ngrams(range(5), 1))
    assert list(wl_nlp_utils.skipgrams(range(5), 2, 0)) == list(wl_nlp_utils.ngrams(range(5), 2))
    assert list(wl_nlp_utils.skipgrams(range(5), 2, 1)) == [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
    assert list(wl_nlp_utils.skipgrams(range(5), 3, 1)) == [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
    assert list(wl_nlp_utils.skipgrams(range(5), 3, 2)) == [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (0, 3, 4), (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
    assert list(wl_nlp_utils.skipgrams(range(5), 6, 9)) == list(wl_nlp_utils.ngrams(range(5), 6))

def test_escape_text():
    assert wl_nlp_utils.escape_text('<test test="test">') == '&lt;test test=&quot;test&quot;&gt;'

def test_escape_tokens():
    assert wl_nlp_utils.escape_tokens(['<test test="test">'] * 10) == ['&lt;test test=&quot;test&quot;&gt;'] * 10

def test_html_to_text():
    assert wl_nlp_utils.html_to_text('<test>&lt;test test=&quot;test&quot;&gt;</test>') == '<test test="test">'

if __name__ == '__main__':
    test_to_lang_util_code()
    test_to_lang_util_codes()
    test_to_lang_util_text()
    test_to_lang_util_texts()

    test_check_models()
    test_init_model_spacy()
    test_init_model_stanza()
    test_init_sudachipy_word_tokenizer()

    test_to_sections()
    test_to_sections_unequal()
    test_split_token_list()
    test_split_into_chunks_text()

    test_srp_cyrl_to_latn()
    test_srp_latn_to_cyrl()

    test_ngrams()
    test_everygrams()
    test_skipgrams()

    test_escape_text()
    test_escape_tokens()
    test_html_to_text()
