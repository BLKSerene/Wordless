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
    results_sentence_tokenize = ['Limba română este o limbă indo-europeană din grupul italic și din subgrupul oriental al limbilor romanice.', 'Printre limbile romanice, româna este a cincea după numărul de vorbitori, în urma spaniolei, portughezei, francezei și italienei.', 'Din motive de diferențiere tipologică, româna mai este numită în lingvistica comparată limba dacoromână sau dialectul dacoromân.', 'De asemenea, este limba oficială în România și în Republica Moldova.']

    test_spacy.wl_test_spacy(
        lang = 'ron',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['Limba', 'română', 'este', 'o', 'limbă', 'indo-europeană', 'din', 'grupul', 'italic', 'și', 'din', 'subgrupul', 'oriental', 'al', 'limbilor', 'romanice', '.'],
        results_pos_tag = [('Limba', 'Ncfsry'), ('română', 'Afpfsrn'), ('este', 'Vaip3s'), ('o', 'Tifsr'), ('limbă', 'Ncfsrn'), ('indo-europeană', 'Afpfsrn'), ('din', 'Spsa'), ('grupul', 'Ncmsry'), ('italic', 'Afpms-n'), ('și', 'Crssp'), ('din', 'Spsa'), ('subgrupul', 'Ncmsry'), ('oriental', 'Afpms-n'), ('al', 'Tsms'), ('limbilor', 'Ncfpoy'), ('romanice', 'Afpfp-n'), ('.', 'PERIOD')],
        results_pos_tag_universal = [('Limba', 'NOUN'), ('română', 'ADJ'), ('este', 'AUX'), ('o', 'DET'), ('limbă', 'NOUN'), ('indo-europeană', 'ADJ'), ('din', 'ADP'), ('grupul', 'NOUN'), ('italic', 'ADJ'), ('și', 'CCONJ'), ('din', 'ADP'), ('subgrupul', 'NOUN'), ('oriental', 'ADJ'), ('al', 'DET'), ('limbilor', 'NOUN'), ('romanice', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['limbă', 'român', 'fi', 'un', 'limbă', 'indo-european', 'din', 'grup', 'italic', 'și', 'din', 'subgrup', 'oriental', 'al', 'limbilor', 'romanic', '.'],
        results_dependency_parse = [('Limba', 'limbă', 'nsubj', 4), ('română', 'Limba', 'amod', -1), ('este', 'limbă', 'cop', 2), ('o', 'limbă', 'det', 1), ('limbă', 'limbă', 'ROOT', 0), ('indo-europeană', 'limbă', 'amod', -1), ('din', 'grupul', 'case', 1), ('grupul', 'limbă', 'nmod', -3), ('italic', 'grupul', 'amod', -1), ('și', 'subgrupul', 'cc', 2), ('din', 'subgrupul', 'case', 1), ('subgrupul', 'grupul', 'conj', -4), ('oriental', 'subgrupul', 'amod', -1), ('al', 'limbilor', 'det', 1), ('limbilor', 'subgrupul', 'nmod', -3), ('romanice', 'limbilor', 'amod', -1), ('.', 'limbă', 'punct', -12)]
    )

if __name__ == '__main__':
    test_spacy_ron()
