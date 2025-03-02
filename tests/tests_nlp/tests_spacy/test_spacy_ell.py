# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Greek (Modern)
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

def test_spacy_ell():
    results_pos_tag = [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[9', 'NOUN'), (']', 'NOUN'), ('secεπίσης', 'X'), ('στο', 'ADP'), ('βαλκανικό', 'ADJ'), ('γλωσσικό', 'ADJ'), ('δεσμό', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'ell',
        results_sentence_tokenize_trf = ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] secεπίσης στο βαλκανικό γλωσσικό δεσμό.', 'ελληνική γλώσσα', ', έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..'],
        results_sentence_tokenize_lg = ['Η ελληνική γλώσσα ανήκει στην ινδοευρωπαϊκή οικογένεια[9] secεπίσης στο βαλκανικό γλωσσικό δεσμό.', 'ελληνική γλώσσα, έχουμε γραπτά κείμενα ήδη από τον 15ο αιώνα π.', 'Χ..'],
        results_word_tokenize = ['Η', 'ελληνική', 'γλώσσα', 'ανήκει', 'στην', 'ινδοευρωπαϊκή', 'οικογένεια[9', ']', 'secεπίσης', 'στο', 'βαλκανικό', 'γλωσσικό', 'δεσμό', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['ο', 'ελληνικός', 'γλώσσα', 'ανήκω', 'σε ο', 'ινδοευρωπαϊκός', 'οικογένεια[9', ']', 'secεπίσης', 'σε ο', 'βαλκανικός', 'γλωσσικός', 'δεσμός', '.'],
        results_dependency_parse = [('Η', 'γλώσσα', 'det', 2), ('ελληνική', 'γλώσσα', 'amod', 1), ('γλώσσα', 'ανήκει', 'nsubj', 1), ('ανήκει', 'ανήκει', 'ROOT', 0), ('στην', 'οικογένεια[9', 'case', 2), ('ινδοευρωπαϊκή', 'οικογένεια[9', 'amod', 1), ('οικογένεια[9', 'ανήκει', 'obl', -3), (']', 'ανήκει', 'obl', -4), ('secεπίσης', ']', 'nmod', -1), ('στο', 'δεσμό', 'case', 3), ('βαλκανικό', 'δεσμό', 'amod', 2), ('γλωσσικό', 'δεσμό', 'amod', 1), ('δεσμό', ']', 'nmod', -5), ('.', 'ανήκει', 'punct', -10)]
    )

if __name__ == '__main__':
    test_spacy_ell()
