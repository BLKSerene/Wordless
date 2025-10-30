# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Italian
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

def test_spacy_ita():
    results_sentence_tokenize = ["L'italiano è una lingua romanza parlata principalmente in Italia.", "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino (complessivamente a pari merito, anche se in parametri diversi, con la lingua sarda).[2][3][4][5]"]

    test_spacy.wl_test_spacy(
        lang = 'ita',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = ["L'", 'italiano', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.'],
        results_pos_tag = [("L'", 'RD'), ('italiano', 'S'), ('è', 'V'), ('una', 'RI'), ('lingua', 'S'), ('romanza', 'A'), ('parlata', 'V'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')],
        results_pos_tag_universal = [("L'", 'DET'), ('italiano', 'NOUN'), ('è', 'AUX'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'ADJ'), ('parlata', 'VERB'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['il', 'italiano', 'essere', 'uno', 'lingua', 'romanza', 'parlare', 'principalmente', 'in', 'Italia', '.'],
        results_dependency_parse = [("L'", 'italiano', 'det', 1), ('italiano', 'lingua', 'nsubj', 3), ('è', 'lingua', 'cop', 2), ('una', 'lingua', 'det', 1), ('lingua', 'lingua', 'ROOT', 0), ('romanza', 'lingua', 'amod', -1), ('parlata', 'lingua', 'amod', -2), ('principalmente', 'parlata', 'advmod', -1), ('in', 'Italia', 'case', 1), ('Italia', 'parlata', 'obl', -3), ('.', 'lingua', 'punct', -6)]
    )

if __name__ == '__main__':
    test_spacy_ita()
