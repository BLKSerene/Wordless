# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - English
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

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_eng():
    test_stanza.wl_test_stanza(
        lang = 'eng_us',
        results_sentence_tokenize = ['English is a West Germanic language in the Indo-European language family that originated in early medieval England.[3][4][5]', 'It is the most spoken language in the world[6] and the third most spoken native language in the world, after Standard Chinese and Spanish.[7]', 'Today, English is the primary language of the Anglosphere, which is usually defined as the United States, the United Kingdom, Canada, Australia, and New Zealand.', 'English is also the primary language of the Republic of Ireland, although it is not typically included within the Anglosphere.'],
        results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', 'that', 'originated', 'in', 'early', 'medieval', 'England', '.', '[', '3', ']', '[', '4', ']', '[', '5', ']'],
        results_pos_tag = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'JJ'), ('Germanic', 'JJ'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo', 'NNP'), ('-', 'HYPH'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), ('that', 'WDT'), ('originated', 'VBD'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England', 'NNP'), ('.', '.'), ('[', '-LRB-'), ('3', 'CD'), (']', '-RRB-'), ('[', '-LRB-'), ('4', 'CD'), (']', '-RRB-'), ('[', '-LRB-'), ('5', 'CD'), (']', '-RRB-')],
        results_pos_tag_universal = [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'ADJ'), ('Germanic', 'ADJ'), ('language', 'NOUN'), ('in', 'ADP'), ('the', 'DET'), ('Indo', 'PROPN'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), ('that', 'PRON'), ('originated', 'VERB'), ('in', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England', 'PROPN'), ('.', 'PUNCT'), ('[', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('4', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('5', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['English', 'be', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', 'that', 'originate', 'in', 'early', 'medieval', 'England', '.', '[', '3', ']', '[', '4', ']', '[', '5', ']'],
        results_dependency_parse = [('English', 'language', 'nsubj', 5), ('is', 'language', 'cop', 4), ('a', 'language', 'det', 3), ('West', 'Germanic', 'amod', 1), ('Germanic', 'language', 'amod', 1), ('language', 'language', 'root', 0), ('in', 'family', 'case', 6), ('the', 'family', 'det', 5), ('Indo', 'European', 'compound', 2), ('-', 'European', 'punct', 1), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'language', 'nmod', -7), ('that', 'originated', 'nsubj', 1), ('originated', 'family', 'acl:relcl', -2), ('in', 'England', 'case', 3), ('early', 'England', 'amod', 2), ('medieval', 'England', 'amod', 1), ('England', 'originated', 'obl', -4), ('.', 'language', 'punct', -14), ('[', '3', 'punct', 1), ('3', 'language', 'dep', -16), (']', '3', 'punct', -1), ('[', '4', 'punct', 1), ('4', 'language', 'dep', -19), (']', '4', 'punct', -1), ('[', '5', 'punct', 1), ('5', 'language', 'dep', -22), (']', '5', 'punct', -1)]
    )

def test_stanza_other():
    test_stanza.wl_test_stanza(
        lang = 'other',
        results_sentence_tokenize = ['English is a West Germanic language in the Indo-European language family that originated in early medieval England.[3][4][5]', 'It is the most spoken language in the world[6] and the third most spoken native language in the world, after Standard Chinese and Spanish.[7]', 'Today, English is the primary language of the Anglosphere, which is usually defined as the United States, the United Kingdom, Canada, Australia, and New Zealand.', 'English is also the primary language of the Republic of Ireland, although it is not typically included within the Anglosphere.'],
        results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', 'that', 'originated', 'in', 'early', 'medieval', 'England', '.', '[', '3', ']', '[', '4', ']', '[', '5', ']']
    )

if __name__ == '__main__':
    test_stanza_eng()
    test_stanza_other()
