# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Italian
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

def test_stanza_ita():
    test_stanza.wl_test_stanza(
        lang = 'ita',
        results_sentence_tokenize = ["L'italiano ([itaˈljaːno][Nota 1] ascolta[?", '·info]) è una lingua romanza parlata principalmente in Italia.', "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino.[2][3][4][Nota 2]"],
        results_word_tokenize = ["L'", 'italiano', '(', '[', 'itaˈljaːno', ']', '[', 'Nota', '1', ']', 'ascolta', '[', '?', '·info', ']', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.'],
        results_pos_tag = [("L'", 'RD'), ('italiano', 'S'), ('(', 'FB'), ('[', 'FB'), ('itaˈljaːno', 'S'), (']', 'FB'), ('[', 'FB'), ('Nota', 'S'), ('1', 'N'), (']', 'FB'), ('ascolta', 'V'), ('[', 'FB'), ('?', 'FS'), ('·info', 'S'), (']', 'FB'), (')', 'FB'), ('è', 'VA'), ('una', 'RI'), ('lingua', 'S'), ('romanza', 'A'), ('parlata', 'V'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')],
        results_pos_tag_universal = [("L'", 'DET'), ('italiano', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('itaˈljaːno', 'NOUN'), (']', 'PUNCT'), ('[', 'PUNCT'), ('Nota', 'NOUN'), ('1', 'NUM'), (']', 'PUNCT'), ('ascolta', 'VERB'), ('[', 'PUNCT'), ('?', 'PUNCT'), ('·info', 'NOUN'), (']', 'PUNCT'), (')', 'PUNCT'), ('è', 'AUX'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'ADJ'), ('parlata', 'VERB'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['il', 'italiano', '(', '[', 'itaˈljaːno', ']', '[', 'nota', '1', ']', 'ascoltare', '[', '?', '·info', ']', ')', 'essere', 'uno', 'lingua', 'romanzo', 'parlato', 'principalmente', 'in', 'Italia', '.'],
        results_dependency_parse = [("L'", 'italiano', 'det', 1), ('italiano', 'ascolta', 'nsubj', 9), ('(', 'itaˈljaːno', 'punct', 2), ('[', 'itaˈljaːno', 'punct', 1), ('itaˈljaːno', 'italiano', 'appos', -3), (']', 'itaˈljaːno', 'punct', -1), ('[', 'Nota', 'punct', 1), ('Nota', 'italiano', 'appos', -6), ('1', 'Nota', 'nummod', -1), (']', 'Nota', 'punct', -2), ('ascolta', 'ascolta', 'root', 0), ('[', 'ascolta', 'punct', -1), ('?', 'ascolta', 'punct', -2), ('·info', 'lingua', 'parataxis', 5), (']', '·info', 'punct', -1), (')', '·info', 'punct', -2), ('è', 'lingua', 'cop', 2), ('una', 'lingua', 'det', 1), ('lingua', 'lingua', 'root', 0), ('romanza', 'lingua', 'amod', -1), ('parlata', 'lingua', 'amod', -2), ('principalmente', 'parlata', 'advmod', -1), ('in', 'Italia', 'case', 1), ('Italia', 'parlata', 'obl', -3), ('.', 'lingua', 'punct', -6)]
    )

if __name__ == '__main__':
    test_stanza_ita()