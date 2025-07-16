# ----------------------------------------------------------------------
# Tests: NLP - Stanza - English
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

from tests.tests_nlp.tests_stanza import test_stanza
from tests import wl_test_init
from wordless.wl_nlp import (
    wl_dependency_parsing,
    wl_word_tokenization
)

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'stanza')

results_sentence_tokenize = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6]', 'The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.']
results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain', '.', '[', '4', ']', '[', '5', ']', '[', '6', ']']

def test_stanza_eng():
    test_stanza.wl_test_stanza(
        lang = 'eng_us',
        results_sentence_tokenize = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'JJ'), ('Germanic', 'JJ'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo', 'JJ'), ('-', 'HYPH'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('whose', 'WP$'), ('speakers', 'NNS'), (',', ','), ('called', 'VBN'), ('Anglophones', 'NNPS'), (',', ','), ('originated', 'VBD'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England', 'NNP'), ('on', 'IN'), ('the', 'DT'), ('island', 'NN'), ('of', 'IN'), ('Great', 'JJ'), ('Britain', 'NNP'), ('.', '.'), ('[', '-LRB-'), ('4', 'CD'), (']', '-RRB-'), ('[', '-LRB-'), ('5', 'CD'), (']', '-RRB-'), ('[', '-LRB-'), ('6', 'CD'), (']', '-RRB-')],
        results_pos_tag_universal = [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'ADJ'), ('Germanic', 'ADJ'), ('language', 'NOUN'), ('in', 'ADP'), ('the', 'DET'), ('Indo', 'ADJ'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('whose', 'PRON'), ('speakers', 'NOUN'), (',', 'PUNCT'), ('called', 'VERB'), ('Anglophones', 'PROPN'), (',', 'PUNCT'), ('originated', 'VERB'), ('in', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England', 'PROPN'), ('on', 'ADP'), ('the', 'DET'), ('island', 'NOUN'), ('of', 'ADP'), ('Great', 'ADJ'), ('Britain', 'PROPN'), ('.', 'PUNCT'), ('[', 'PUNCT'), ('4', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('5', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('6', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['English', 'be', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speaker', ',', 'call', 'Anglophones', ',', 'originate', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'great', 'Britain', '.', '[', '4', ']', '[', '5', ']', '[', '6', ']'],
        results_dependency_parse = [('English', 'language', 'nsubj', 5), ('is', 'language', 'cop', 4), ('a', 'language', 'det', 3), ('West', 'Germanic', 'amod', 1), ('Germanic', 'language', 'amod', 1), ('language', 'language', 'root', 0), ('in', 'family', 'case', 6), ('the', 'family', 'det', 5), ('Indo', 'European', 'amod', 2), ('-', 'Indo', 'punct', -1), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'language', 'nmod', -7), (',', 'originated', 'punct', 7), ('whose', 'speakers', 'nmod:poss', 1), ('speakers', 'originated', 'nsubj', 5), (',', 'called', 'punct', 1), ('called', 'speakers', 'acl', -2), ('Anglophones', 'called', 'xcomp', -1), (',', 'speakers', 'punct', -4), ('originated', 'family', 'acl:relcl', -8), ('in', 'England', 'case', 3), ('early', 'England', 'amod', 2), ('medieval', 'England', 'amod', 1), ('England', 'originated', 'obl', -4), ('on', 'island', 'case', 2), ('the', 'island', 'det', 1), ('island', 'originated', 'obl', -7), ('of', 'Britain', 'case', 2), ('Great', 'Britain', 'amod', 1), ('Britain', 'island', 'nmod', -3), ('.', 'language', 'punct', -26), ('[', '4', 'punct', 1), ('4', 'language', 'dep', -28), (']', '4', 'punct', -1), ('[', '5', 'punct', 1), ('5', 'language', 'dep', -31), (']', '5', 'punct', -1), ('[', '6', 'punct', 1), ('6', 'language', 'dep', -34), (']', '6', 'punct', -1)],
        results_sentiment_analayze = [0]
    )

def test_stanza_other():
    test_stanza.wl_test_stanza(
        lang = 'other',
        results_sentence_tokenize = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize
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
    test_stanza_eng()
    test_stanza_other()
    test_stanza_punc_marks()
