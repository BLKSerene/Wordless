# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Spanish
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

def test_spacy_spa():
    results_pos_tag = [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'NOUN'), ('romance', 'ADJ'), ('procedente', 'ADJ'), ('del', 'ADP'), ('latín', 'NOUN'), ('hablado', 'ADJ'), (',', 'PUNCT'), ('perteneciente', 'ADJ'), ('a', 'ADP'), ('la', 'DET'), ('familia', 'NOUN'), ('de', 'ADP'), ('lenguas', 'NOUN'), ('indoeuropeas', 'ADJ'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'spa',
        results_sentence_tokenize_trf = ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.', 'Se conoce también informalmente como castillan.', '1\u200b33\u200b34\u200b en algunas áreas rurales e indígenas de América,35\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.36\u200b37\u200b38\u200b39\u200b40\u200b41\u200b'],
        results_word_tokenize = ['El', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'la', 'familia', 'de', 'lenguas', 'indoeuropeas', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropea', '.'],
        results_dependency_parse = [('El', 'español', 'det', 1), ('español', 'lengua', 'nsubj', 5), ('o', 'castellano', 'cc', 1), ('castellano', 'español', 'conj', -2), ('es', 'lengua', 'cop', 2), ('una', 'lengua', 'det', 1), ('lengua', 'lengua', 'ROOT', 0), ('romance', 'lengua', 'amod', -1), ('procedente', 'lengua', 'amod', -2), ('del', 'latín', 'case', 1), ('latín', 'procedente', 'nmod', -2), ('hablado', 'latín', 'amod', -1), (',', 'perteneciente', 'punct', 1), ('perteneciente', 'lengua', 'amod', -7), ('a', 'familia', 'case', 2), ('la', 'familia', 'det', 1), ('familia', 'perteneciente', 'nmod', -3), ('de', 'lenguas', 'case', 1), ('lenguas', 'familia', 'nmod', -2), ('indoeuropeas', 'lenguas', 'amod', -1), ('.', 'lengua', 'punct', -14)]
    )

if __name__ == '__main__':
    test_spacy_spa()
