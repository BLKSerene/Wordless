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
    results_sentence_tokenize = ["L'italiano ([itaˈljaːno][Nota 1] ascoltaⓘ) è una lingua romanza parlata principalmente in Italia.", "Per ragioni storiche e geografiche, l'italiano è la lingua romanza meno divergente dal latino.[2][3][4][Nota 2]"]

    test_spacy.wl_test_spacy(
        lang = 'ita',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ["L'", 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascolta', 'ⓘ', ')', 'è', 'una', 'lingua', 'romanza', 'parlata', 'principalmente', 'in', 'Italia', '.'],
        results_pos_tag = [("L'", 'RD'), ('italiano', 'S'), ('(', 'FB'), ('[', 'FB'), ('itaˈljaːno][Nota', 'A'), ('1', 'N'), (']', 'FB'), ('ascolta', 'V'), ('ⓘ', 'X'), (')', 'FB'), ('è', 'V'), ('una', 'RI'), ('lingua', 'S'), ('romanza', 'S'), ('parlata', 'A'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')],
        results_pos_tag_universal = [("L'", 'DET'), ('italiano', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('itaˈljaːno][Nota', 'ADJ'), ('1', 'NUM'), (']', 'PUNCT'), ('ascolta', 'VERB'), ('ⓘ', 'SYM'), (')', 'PUNCT'), ('è', 'AUX'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'NOUN'), ('parlata', 'ADJ'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['il', 'italiano', '(', '[', 'itaˈljaːno][Nota', '1', ']', 'ascoltare', 'ⓘ', ')', 'essere', 'uno', 'lingua', 'romanza', 'parlato', 'principalmente', 'in', 'Italia', '.'],
        results_dependency_parse = [("L'", 'italiano', 'det', 1), ('italiano', 'lingua', 'nsubj', 11), ('(', 'ascolta', 'punct', 5), ('[', 'itaˈljaːno][Nota', 'punct', 1), ('itaˈljaːno][Nota', 'ascolta', 'amod', 3), ('1', 'itaˈljaːno][Nota', 'nummod', -1), (']', 'itaˈljaːno][Nota', 'punct', -2), ('ascolta', 'italiano', 'advcl', -6), ('ⓘ', 'ascolta', 'punct', -1), (')', 'ascolta', 'punct', -2), ('è', 'lingua', 'cop', 2), ('una', 'lingua', 'det', 1), ('lingua', 'lingua', 'ROOT', 0), ('romanza', 'lingua', 'compound', -1), ('parlata', 'lingua', 'amod', -2), ('principalmente', 'parlata', 'advmod', -1), ('in', 'Italia', 'case', 1), ('Italia', 'parlata', 'obl', -3), ('.', 'lingua', 'punct', -6)]
    )

if __name__ == '__main__':
    test_spacy_ita()
