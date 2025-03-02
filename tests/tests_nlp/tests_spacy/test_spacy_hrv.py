# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Croatian
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

def test_spacy_hrv():
    test_spacy.wl_test_spacy(
        lang = 'hrv',
        results_sentence_tokenize_trf = ['Hrvatski jezik obuhvaća govoreni i pisani hrvatski standardni jezik i sve narodne govore kojima govore i pišu Hrvati.[4]', 'Povijesno, obuhvaća sve govore i sve književne jezike izgrađene na tim govorima, kojima su se služili Hrvati.[5][6]'],
        results_sentence_tokenize_lg = ['Hrvatski jezik obuhvaća govoreni i pisani hrvatski standardni jezik i sve narodne govore kojima govore i pišu Hrvati.[4] Povijesno, obuhvaća sve govore i sve književne jezike izgrađene na tim govorima, kojima su se služili Hrvati.[5][6]'],
        results_word_tokenize = ['Hrvatski', 'jezik', 'obuhvaća', 'govoreni', 'i', 'pisani', 'hrvatski', 'standardni', 'jezik', 'i', 'sve', 'narodne', 'govore', 'kojima', 'govore', 'i', 'pišu', 'Hrvati.[4', ']'],
        results_pos_tag = [('Hrvatski', 'Agpmsny'), ('jezik', 'Ncmsn'), ('obuhvaća', 'Vmr3s'), ('govoreni', 'Agpmpny'), ('i', 'Cc'), ('pisani', 'Appmpny'), ('hrvatski', 'Agpmsny'), ('standardni', 'Agpmsny'), ('jezik', 'Ncmsn'), ('i', 'Cc'), ('sve', 'Agpmpay'), ('narodne', 'Agpmpay'), ('govore', 'Vmr3p'), ('kojima', 'Pi-mpi'), ('govore', 'Vmr3p'), ('i', 'Cc'), ('pišu', 'Vmr3p'), ('Hrvati.[4', 'Npmsd'), (']', 'Z')],
        results_pos_tag_universal = [('Hrvatski', 'ADJ'), ('jezik', 'NOUN'), ('obuhvaća', 'VERB'), ('govoreni', 'ADJ'), ('i', 'CCONJ'), ('pisani', 'ADJ'), ('hrvatski', 'ADJ'), ('standardni', 'ADJ'), ('jezik', 'NOUN'), ('i', 'CCONJ'), ('sve', 'ADJ'), ('narodne', 'ADJ'), ('govore', 'VERB'), ('kojima', 'NOUN'), ('govore', 'VERB'), ('i', 'CCONJ'), ('pišu', 'VERB'), ('Hrvati.[4', 'PROPN'), (']', 'PUNCT')],
        results_lemmatize = ['hrvatski', 'jezik', 'obuhvaćati', 'govoren', 'i', 'pisati', 'hrvatski', 'standardan', 'jezik', 'i', 'sav', 'narodni', 'govoriti', 'koji', 'govoriti', 'i', 'pisati', 'Hrvati.[4', ']'],
        results_dependency_parse = [('Hrvatski', 'jezik', 'amod', 1), ('jezik', 'obuhvaća', 'nsubj', 1), ('obuhvaća', 'obuhvaća', 'ROOT', 0), ('govoreni', 'obuhvaća', 'xcomp', -1), ('i', 'jezik', 'cc', 4), ('pisani', 'jezik', 'amod', 3), ('hrvatski', 'jezik', 'amod', 2), ('standardni', 'jezik', 'amod', 1), ('jezik', 'govoreni', 'conj', -5), ('i', 'sve', 'cc', 1), ('sve', 'jezik', 'conj', -2), ('narodne', 'govore', 'amod', 1), ('govore', 'obuhvaća', 'parataxis', -10), ('kojima', 'govore', 'obj', 1), ('govore', 'govore', 'ccomp', -2), ('i', 'pišu', 'cc', 1), ('pišu', 'govore', 'conj', -2), ('Hrvati.[4', 'pišu', 'nsubj', -1), (']', 'pišu', 'punct', -2)]
    )

if __name__ == '__main__':
    test_spacy_hrv()
