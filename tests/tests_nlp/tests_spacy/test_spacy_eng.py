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
from tests import wl_test_init

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'spacy')

results_sentence_tokenize = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6] The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.']
results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain.[4][5][6', ']']

def test_spacy_eng():
    test_spacy.wl_test_spacy(
        lang = 'eng_us',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'JJ'), ('Germanic', 'JJ'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo', 'JJ'), ('-', 'HYPH'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('whose', 'WP$'), ('speakers', 'NNS'), (',', ','), ('called', 'VBN'), ('Anglophones', 'NNPS'), (',', ','), ('originated', 'VBD'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'NN'), ('England', 'NNP'), ('on', 'IN'), ('the', 'DT'), ('island', 'NN'), ('of', 'IN'), ('Great', 'NNP'), ('Britain.[4][5][6', 'CD'), (']', '-RRB-')],
        results_pos_tag_universal = [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'ADJ'), ('Germanic', 'ADJ'), ('language', 'NOUN'), ('in', 'ADP'), ('the', 'DET'), ('Indo', 'ADJ'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('whose', 'DET'), ('speakers', 'NOUN'), (',', 'PUNCT'), ('called', 'VERB'), ('Anglophones', 'PROPN'), (',', 'PUNCT'), ('originated', 'VERB'), ('in', 'ADP'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England', 'PROPN'), ('on', 'ADP'), ('the', 'DET'), ('island', 'NOUN'), ('of', 'ADP'), ('Great', 'PROPN'), ('Britain.[4][5][6', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['English', 'be', 'a', 'west', 'germanic', 'language', 'in', 'the', 'indo', '-', 'european', 'language', 'family', ',', 'whose', 'speaker', ',', 'call', 'Anglophones', ',', 'originate', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'britain.[4][5][6', ']'],
        results_dependency_parse = [('English', 'is', 'nsubj', 1), ('is', 'is', 'ROOT', 0), ('a', 'language', 'det', 3), ('West', 'Germanic', 'amod', 1), ('Germanic', 'language', 'amod', 1), ('language', 'is', 'attr', -4), ('in', 'language', 'prep', -1), ('the', 'family', 'det', 5), ('Indo', 'European', 'amod', 2), ('-', 'European', 'punct', 1), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'in', 'pobj', -6), (',', 'family', 'punct', -1), ('whose', 'speakers', 'poss', 1), ('speakers', 'originated', 'nsubj', 5), (',', 'speakers', 'punct', -1), ('called', 'speakers', 'acl', -2), ('Anglophones', 'called', 'oprd', -1), (',', 'speakers', 'punct', -4), ('originated', 'family', 'relcl', -8), ('in', 'originated', 'prep', -1), ('early', 'medieval', 'amod', 1), ('medieval', 'England', 'compound', 1), ('England', 'in', 'pobj', -3), ('on', 'originated', 'prep', -5), ('the', 'island', 'det', 1), ('island', 'on', 'pobj', -2), ('of', 'island', 'prep', -1), ('Great', 'Britain.[4][5][6', 'compound', 1), ('Britain.[4][5][6', 'of', 'pobj', -2), (']', 'is', 'punct', -30)]
    )

def test_spacy_other():
    test_spacy.wl_test_spacy(
        lang = 'other',
        results_word_tokenize = results_word_tokenize,
    )

if __name__ == '__main__':
    test_spacy_eng()
    test_spacy_other()
