# ----------------------------------------------------------------------
# Tests: NLP - Stanza - German (Low)
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

results_pos_tag = [('Plattdüütsch', 'NOUN'), (',', 'PUNCT'), ('kort', 'ADJ'), ('Platt', 'INTJ'), (',', 'PUNCT'), ('ook', 'AUX'), ('Nedderdüütsch', 'NOUN'), ('oder', 'ADP'), ('Neddersassisch', 'PROPN'), ('heten', 'VERB'), (',', 'PUNCT'), ('is', 'AUX'), ('ene', 'DET'), ('Regionaalspraak', 'PROPN'), ('un', 'CCONJ'), ('Dialektgrupp', 'NOUN'), (',', 'PUNCT'), ('de', 'DET'), ('rund', 'NOUN'), ('2', 'PUNCT'), ('Minschen', 'PROPN'), ('in', 'ADP'), ('Noorddüütschland', 'PROPN'), ('un', 'CCONJ'), ('an', 'ADP'), ('de', 'DET'), ('2', 'NOUN'), ('Millionen', 'PROPN'), ('Minschen', 'PROPN'), ('in', 'ADP'), ('Oostnedderland', 'NOUN'), ('snackt', 'VERB'), ('.', 'PUNCT')]

def test_stanza_nds():
    test_stanza.wl_test_stanza(
        lang = 'nds',
        results_sentence_tokenize = ['Plattdüütsch, kort Platt, ook Nedderdüütsch oder Neddersassisch heten, is ene Regionaalspraak un Dialektgrupp, de rund 2 Minschen in Noorddüütschland un an de 2 Millionen Minschen in Oostnedderland snackt.', 'Besünners mit dat mennistsche Plautdietsch het sik de Spraak ook weltwied uutbreidt.', 'De Spraak höört to’n Westgermaanschen, het den hoogdüütschen Luudwannel nich mitmaakt un is so ene nedderdüütsche Spraak, de tohoop mit’n Freeschen un Engelschen to de noordseegermaanschen Spraken tellt.'],
        results_word_tokenize = ['Plattdüütsch', ',', 'kort', 'Platt', ',', 'ook', 'Nedderdüütsch', 'oder', 'Neddersassisch', 'heten', ',', 'is', 'ene', 'Regionaalspraak', 'un', 'Dialektgrupp', ',', 'de', 'rund', '2', 'Minschen', 'in', 'Noorddüütschland', 'un', 'an', 'de', '2', 'Millionen', 'Minschen', 'in', 'Oostnedderland', 'snackt', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['plattdüütsch', ',', 'kort', 'platt', ',', 'oikken', 'nedderdüüts', 'öäder', 'Neddersassich', 'heten', ',', 'weasen', 'en', 'Regionaalspraak', 'un', 'dialektgrupp', ',', 'de', 'rund', '2', 'Minschen', 'in', 'Noorddüütschland', 'un', 'an', 'de', '2', 'Millionen', 'Minschen', 'in', 'oostnedderland', 'sninken', '.'],
        results_dependency_parse = [('Plattdüütsch', 'heten', 'discourse', 9), (',', 'kort', 'punct', 1), ('kort', 'Plattdüütsch', 'conj', -2), ('Platt', 'kort', 'advmod', -1), (',', 'kort', 'punct', -2), ('ook', 'heten', 'aux', 4), ('Nedderdüütsch', 'heten', 'nsubj', 3), ('oder', 'Neddersassisch', 'case', 1), ('Neddersassisch', 'heten', 'obl', 1), ('heten', 'heten', 'root', 0), (',', 'heten', 'punct', -1), ('is', 'snackt', 'aux', 20), ('ene', 'Regionaalspraak', 'det', 1), ('Regionaalspraak', 'heten', 'nsubj', -4), ('un', 'Dialektgrupp', 'cc', 1), ('Dialektgrupp', 'Regionaalspraak', 'conj', -2), (',', 'rund', 'punct', 2), ('de', 'rund', 'det', 1), ('rund', 'Regionaalspraak', 'appos', -5), ('2', 'Minschen', 'punct', 1), ('Minschen', 'rund', 'nmod', -2), ('in', 'Noorddüütschland', 'case', 1), ('Noorddüütschland', 'rund', 'nmod', -4), ('un', '2', 'cc', 3), ('an', '2', 'case', 2), ('de', '2', 'det', 1), ('2', 'snackt', 'obl', 5), ('Millionen', '2', 'appos', -1), ('Minschen', '2', 'appos', -2), ('in', 'Oostnedderland', 'case', 1), ('Oostnedderland', 'snackt', 'obl', 1), ('snackt', 'heten', 'conj', -22), ('.', 'heten', 'punct', -23)]
    )

if __name__ == '__main__':
    test_stanza_nds()
