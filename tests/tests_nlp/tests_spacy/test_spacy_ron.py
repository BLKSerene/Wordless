# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Romanian
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

def test_spacy_ron():
    results_sentence_tokenize = ['Limba română ([ˈlimba roˈmɨnə]  ( audio) sau românește [romɨˈneʃte]) este limba oficială și principală a României și a Republicii Moldova.', 'Face parte din subramura orientală a limbilor romanice, un grup lingvistic evoluat din diverse dialecte ale latinei vulgare separate de limbile romanice occidentale între secolele V și VIII.[2]']
    test_spacy.wl_test_spacy(
        lang = 'ron',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['Limba', 'română', '(', '[', 'ˈlimba', 'roˈmɨnə', ']', '(', 'audio', ')', 'sau', 'românește', '[', 'romɨˈneʃte', ']', ')', 'este', 'limba', 'oficială', 'și', 'principală', 'a', 'României', 'și', 'a', 'Republicii', 'Moldova', '.'],
        results_pos_tag = [('Limba', 'Ncfsry'), ('română', 'Afpfsrn'), ('(', 'LPAR'), ('[', 'LSQR'), ('ˈlimba', 'Ncfsry'), ('roˈmɨnə', 'Ncfsry'), (']', 'RSQR'), ('(', 'LPAR'), ('audio', 'Ncms-n'), (')', 'RPAR'), ('sau', 'Ccssp'), ('românește', 'Rgp'), ('[', 'LSQR'), ('romɨˈneʃte', 'Ncms-n'), (']', 'RSQR'), (')', 'RPAR'), ('este', 'Vaip3s'), ('limba', 'Ncfsry'), ('oficială', 'Afpfsrn'), ('și', 'Crssp'), ('principală', 'Afpfsrn'), ('a', 'Tsfs'), ('României', 'Npfsoy'), ('și', 'Crssp'), ('a', 'Tsfs'), ('Republicii', 'Ncfsoy'), ('Moldova', 'Np'), ('.', 'PERIOD')],
        results_pos_tag_universal = [('Limba', 'NOUN'), ('română', 'ADJ'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈlimba', 'NOUN'), ('roˈmɨnə', 'NOUN'), (']', 'PUNCT'), ('(', 'PUNCT'), ('audio', 'NOUN'), (')', 'PUNCT'), ('sau', 'CCONJ'), ('românește', 'ADV'), ('[', 'PUNCT'), ('romɨˈneʃte', 'NOUN'), (']', 'PUNCT'), (')', 'PUNCT'), ('este', 'AUX'), ('limba', 'NOUN'), ('oficială', 'ADJ'), ('și', 'CCONJ'), ('principală', 'ADJ'), ('a', 'DET'), ('României', 'PROPN'), ('și', 'CCONJ'), ('a', 'DET'), ('Republicii', 'NOUN'), ('Moldova', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['limbă', 'român', '(', '[', 'ˈlimbă', 'roˈmɨnə', ']', '(', 'audio', ')', 'sau', 'românește', '[', 'romɨˈneʃte', ']', ')', 'fi', 'limbă', 'oficial', 'și', 'principal', 'al', 'România', 'și', 'al', 'Republicii', 'Moldova', '.'],
        results_dependency_parse = [('Limba', 'limba', 'nsubj', 18), ('română', 'Limba', 'amod', -1), ('(', 'ˈlimba', 'punct', 2), ('[', 'ˈlimba', 'punct', 1), ('ˈlimba', 'limba', 'parataxis', 14), ('roˈmɨnə', 'ˈlimba', 'nmod', -1), (']', 'ˈlimba', 'punct', -2), (' ', ']', 'dep', -1), ('(', 'audio', 'punct', 1), ('audio', 'ˈlimba', 'appos', -5), (')', 'audio', 'punct', -1), ('sau', 'românește', 'cc', 1), ('românește', 'ˈlimba', 'conj', -8), ('[', 'romɨˈneʃte', 'punct', 1), ('romɨˈneʃte', 'românește', 'appos', -2), (']', 'romɨˈneʃte', 'punct', -1), (')', 'ˈlimba', 'punct', -12), ('este', 'limba', 'cop', 1), ('limba', 'limba', 'ROOT', 0), ('oficială', 'limba', 'amod', -1), ('și', 'principală', 'cc', 1), ('principală', 'oficială', 'conj', -2), ('a', 'României', 'det', 1), ('României', 'limba', 'nmod', -5), ('și', 'Republicii', 'cc', 2), ('a', 'Republicii', 'det', 1), ('Republicii', 'României', 'conj', -3), ('Moldova', 'Republicii', 'nmod', -1), ('.', 'limba', 'punct', -10)]
    )

if __name__ == '__main__':
    test_spacy_ron()
