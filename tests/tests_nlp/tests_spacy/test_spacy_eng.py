# ----------------------------------------------------------------------
# Tests: NLP - spaCy - English
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

from tests.tests_nlp.tests_spacy import test_spacy

results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', '.']

def test_spacy_eng():
    test_spacy.wl_test_spacy(
        lang = 'eng_us',
        results_sentence_tokenize_trf = ['English is a West Germanic language in the Indo-European language family.', 'Originating in early medieval England,[3][4][5] today English is both the most spoken language in the world[6] and the third most spoken native language, after Mandarin Chinese and Spanish.[7]', 'English is the most widely learned second language and is either the official language or one of the official languages in 59 sovereign states.', 'There are more people who have learned English as a second language than there are native speakers.', 'As of 2005, it was estimated that there were over two billion speakers of English.[8]'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'JJ'), ('Germanic', 'JJ'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo', 'JJ'), ('-', 'JJ'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), ('.', '.')],
        results_pos_tag_universal = [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'ADJ'), ('Germanic', 'ADJ'), ('language', 'NOUN'), ('in', 'ADP'), ('the', 'DET'), ('Indo', 'ADJ'), ('-', 'ADJ'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['English', 'be', 'a', 'west', 'germanic', 'language', 'in', 'the', 'indo', '-', 'european', 'language', 'family', '.'],
        results_dependency_parse = [('English', 'is', 'nsubj', 1), ('is', 'is', 'ROOT', 0), ('a', 'language', 'det', 3), ('West', 'Germanic', 'amod', 1), ('Germanic', 'language', 'amod', 1), ('language', 'is', 'attr', -4), ('in', 'language', 'prep', -1), ('the', 'family', 'det', 5), ('Indo', 'language', 'amod', 3), ('-', 'language', 'amod', 2), ('European', 'language', 'amod', 1), ('language', 'family', 'compound', 1), ('family', 'in', 'pobj', -6), ('.', 'is', 'punct', -12)]
    )

def test_spacy_other():
    test_spacy.wl_test_spacy(
        lang = 'other',
        results_sentence_tokenize_trf = ['English is a West Germanic language in the Indo-European language family.', 'Originating in early medieval England,[3][4][5] today English is both the most spoken language in the world[6] and the third most spoken native language, after Mandarin Chinese and Spanish.[7] English is the most widely learned second language and is either the official language or one of the official languages in 59 sovereign states.', 'There are more people who have learned English as a second language than there are native speakers.', 'As of 2005, it was estimated that there were over two billion speakers of English.[8]'],
        results_word_tokenize = results_word_tokenize
    )

if __name__ == '__main__':
    test_spacy_eng()
    test_spacy_other()
