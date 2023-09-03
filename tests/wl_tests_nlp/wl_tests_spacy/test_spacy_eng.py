# ----------------------------------------------------------------------
# Wordless: Tests - NLP - spaCy - English
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

from tests.wl_tests_nlp.wl_tests_spacy import test_spacy

def test_spacy_eng():
    test_spacy.wl_test_spacy(
        lang = 'eng_us',
        results_sentence_tokenize_trf = ['English is a West Germanic language in the Indo-European language family that originated in early medieval England.[3][4][5]', 'It is the most spoken language in the world[6] and the third most spoken native language in the world, after Standard Chinese and Spanish.[7]', 'Today, English is the primary language of the Anglosphere, which is usually defined as the United States, the United Kingdom, Canada, Australia, and New Zealand.', 'English is also the primary language of the Republic of Ireland, although it is not typically included within the Anglosphere.'],
        results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', 'that', 'originated', 'in', 'early', 'medieval', 'England.[3][4][5', ']'],
        results_pos_tag = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'JJ'), ('Germanic', 'JJ'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo', 'JJ'), ('-', 'JJ'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), ('that', 'WDT'), ('originated', 'VBD'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England.[3][4][5', 'CD'), (']', '-RRB-')],
        results_pos_tag_universal = [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'ADJ'), ('Germanic', 'ADJ'), ('language', 'NOUN'), ('in', 'ADP'), ('the', 'DET'), ('Indo', 'ADJ'), ('-', 'ADJ'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), ('that', 'PRON'), ('originated', 'VERB'), ('in', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England.[3][4][5', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['English', 'be', 'a', 'west', 'germanic', 'language', 'in', 'the', 'indo', '-', 'european', 'language', 'family', 'that', 'originate', 'in', 'early', 'medieval', 'england.[3][4][5', ']'],
        results_dependency_parse = [('English', 'is', 'nsubj', 1), ('is', 'is', 'ROOT', 0), ('a', 'language', 'det', 3), ('West', 'Germanic', 'amod', 1), ('Germanic', 'language', 'amod', 1), ('language', 'is', 'attr', -4), ('in', 'language', 'prep', -1), ('the', 'family', 'det', 5), ('Indo', 'family', 'amod', 4), ('-', 'family', 'amod', 3), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'in', 'pobj', -6), ('that', 'originated', 'nsubj', 1), ('originated', 'family', 'relcl', -2), ('in', 'originated', 'prep', -1), ('early', 'medieval', 'amod', 1), ('medieval', 'England.[3][4][5', 'amod', 1), ('England.[3][4][5', 'in', 'pobj', -3), (']', 'is', 'punct', -18)]
    )

def test_spacy_other():
    test_spacy.wl_test_spacy(
        lang = 'other',
        results_sentence_tokenize_trf = ['English is a West Germanic language in the Indo-European language family that originated in early medieval England.[3][4][5] It is the most spoken language in the world[6] and the third most spoken native language in the world, after Standard Chinese and Spanish.[7] Today, English is the primary language of the Anglosphere, which is usually defined as the United States, the United Kingdom, Canada, Australia, and New Zealand.', 'English is also the primary language of the Republic of Ireland, although it is not typically included within the Anglosphere.'],
        results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', 'that', 'originated', 'in', 'early', 'medieval', 'England.[3][4][5', ']']
    )

if __name__ == '__main__':
    test_spacy_eng()
    test_spacy_other()
