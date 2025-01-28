# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Spanish
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_spa():
    test_stanza.wl_test_stanza(
        lang = 'spa',
        results_sentence_tokenize = ['El español o castellano es una lengua romance procedente del latín hablado, perteneciente a la familia de lenguas indoeuropeas.', 'Forma parte del grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica.', 'Se conoce también informalmente como castillan.', '1\u200b33\u200b34\u200b en algunas áreas rurales e indígenas de América,35\u200b pues el español se empezó a enseñar poco después de la incorporación de los nuevos territorios a la Corona de Castilla.36\u200b37\u200b38\u200b39\u200b40\u200b41\u200b'],
        results_word_tokenize = ['El', 'español', 'o', 'castellano', 'es', 'una', 'lengua', 'romance', 'procedente', 'del', 'latín', 'hablado', ',', 'perteneciente', 'a', 'la', 'familia', 'de', 'lenguas', 'indoeuropeas', '.'],
        results_pos_tag = [('El', 'da0ms0'), ('español', 'ncms000'), ('o', 'cc'), ('castellano', 'ncms000'), ('es', 'vsip3s0'), ('una', 'di0fs0'), ('lengua', 'ncfs000'), ('romance', 'aq0cs0'), ('procedente', 'aq0cs0'), ('de', 'spcms'), ('el', 'DET'), ('latín', 'ncms000'), ('hablado', 'aq0msp'), (',', 'fc'), ('perteneciente', 'aq0cs0'), ('a', 'sps00'), ('la', 'da0fs0'), ('familia', 'ncfs000'), ('de', 'sps00'), ('lenguas', 'ncfp000'), ('indoeuropeas', 'aq0fp0'), ('.', 'fp')],
        results_pos_tag_universal = [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'NOUN'), ('romance', 'ADJ'), ('procedente', 'ADJ'), ('de', 'ADP'), ('el', 'DET'), ('latín', 'NOUN'), ('hablado', 'ADJ'), (',', 'PUNCT'), ('perteneciente', 'ADJ'), ('a', 'ADP'), ('la', 'DET'), ('familia', 'NOUN'), ('de', 'ADP'), ('lenguas', 'NOUN'), ('indoeuropeas', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['el', 'español', 'o', 'castellano', 'ser', 'uno', 'lengua', 'romance', 'procedente', 'de', 'el', 'latín', 'hablar', ',', 'perteneciente', 'a', 'el', 'familia', 'de', 'lengua', 'indoeuropeo', '.'],
        results_dependency_parse = [('El', 'español', 'det', 1), ('español', 'lengua', 'nsubj', 5), ('o', 'castellano', 'cc', 1), ('castellano', 'español', 'conj', -2), ('es', 'lengua', 'cop', 2), ('una', 'lengua', 'det', 1), ('lengua', 'lengua', 'root', 0), ('romance', 'lengua', 'amod', -1), ('procedente', 'lengua', 'amod', -2), ('de', 'latín', 'case', 2), ('el', 'latín', 'det', 1), ('latín', 'procedente', 'nmod', -3), ('hablado', 'latín', 'amod', -1), (',', 'perteneciente', 'punct', 1), ('perteneciente', 'latín', 'amod', -3), ('a', 'familia', 'case', 2), ('la', 'familia', 'det', 1), ('familia', 'perteneciente', 'obl:arg', -3), ('de', 'lenguas', 'case', 1), ('lenguas', 'familia', 'nmod', -2), ('indoeuropeas', 'lenguas', 'amod', -1), ('.', 'lengua', 'punct', -15)],
        results_sentiment_analayze = [-1]
    )

if __name__ == '__main__':
    test_stanza_spa()
