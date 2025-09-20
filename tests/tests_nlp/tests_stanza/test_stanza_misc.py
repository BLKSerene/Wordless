# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Miscellaneous
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

from tests.tests_nlp.tests_stanza import (
    test_stanza,
    test_stanza_eng
)
from tests import wl_test_init
from wordless.wl_nlp import (
    wl_dependency_parsing,
    wl_word_tokenization
)

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'stanza')

def test_stanza_other():
    test_stanza.wl_test_stanza(
        lang = 'other',
        results_sentence_tokenize = test_stanza_eng.results_sentence_tokenize,
        results_word_tokenize = test_stanza_eng.results_word_tokenize
    )

def test_stanza_punc_marks():
    test_sentence = 'Hi, take it!'

    tokens_untokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = test_sentence,
        lang = 'eng_us',
    )
    dds_untokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dd, token.dd_no_punc)
        for token in tokens_untokenized
    ]

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = 'eng_us'
    )

    tokens_tokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = tokens,
        lang = 'eng_us'
    )

    dds_tokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dd, token.dd_no_punc)
        for token in tokens_tokenized
    ]

    print('eng_us / stanza_eng:')
    print(dds_untokenized)
    print(dds_tokenized)

    assert dds_untokenized == dds_tokenized == [('Hi', 'take', 'discourse', 2, 1), (',', 'Hi', 'punct', -1, -1), ('take', 'take', 'root', 0, 0), ('it', 'take', 'obj', -1, -1), ('!', 'take', 'punct', -2, -1)]

if __name__ == '__main__':
    test_stanza_other()

    test_stanza_punc_marks()
