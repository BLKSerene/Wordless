# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Portuguese
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

def test_stanza_por_pt():
    results_pos_tag = [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'ADJ'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('indo-europeia', 'ADJ'), ('românica', 'ADJ'), ('flexiva', 'ADJ'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('em', 'ADP'), ('o', 'DET'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('em', 'ADP'), ('o', 'DET'), ('Reino', 'PROPN'), ('de', 'ADP'), ('a', 'DET'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('em', 'ADP'), ('o', 'DET'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'por_pt',
        results_sentence_tokenize = ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[8]', 'O português foi usado, naquela época, não somente nas cidades conquistadas pelos portugueses, mas também por muitos governantes locais nos seus contatos com outros estrangeiros poderosos.', 'Especialmente nessa altura a língua portuguesa também influenciou várias línguas.[9]'],
        results_word_tokenize = ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'indo-europeia', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego-português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['o', 'língua', 'português', ',', 'também', 'designar', 'português', ',', 'ser', 'um', 'língua', 'indo-europeu', 'românico', 'flexivo', 'ocidental', 'originar', 'em', 'o', 'galego-português', 'falar', 'em', 'o', 'Reino', 'de', 'o', 'Galiza', 'e', 'em', 'o', 'norte', 'de', 'Portugal', '.'],
        results_dependency_parse = [('A', 'língua', 'det', 1), ('língua', 'língua', 'nsubj', 9), ('portuguesa', 'língua', 'amod', -1), (',', 'designada', 'punct', 2), ('também', 'designada', 'advmod', 1), ('designada', 'língua', 'acl', -4), ('português', 'designada', 'xcomp', -1), (',', 'designada', 'punct', -2), ('é', 'língua', 'cop', 2), ('uma', 'língua', 'det', 1), ('língua', 'língua', 'root', 0), ('indo-europeia', 'língua', 'amod', -1), ('românica', 'língua', 'amod', -2), ('flexiva', 'língua', 'amod', -3), ('ocidental', 'língua', 'amod', -4), ('originada', 'língua', 'acl', -5), ('em', 'galego-português', 'case', 2), ('o', 'galego-português', 'det', 1), ('galego-português', 'originada', 'obl', -3), ('falado', 'galego-português', 'acl', -1), ('em', 'Reino', 'case', 2), ('o', 'Reino', 'det', 1), ('Reino', 'falado', 'obl', -3), ('de', 'Galiza', 'case', 2), ('a', 'Galiza', 'det', 1), ('Galiza', 'Reino', 'nmod', -3), ('e', 'norte', 'cc', 3), ('em', 'norte', 'case', 2), ('o', 'norte', 'det', 1), ('norte', 'Reino', 'conj', -7), ('de', 'Portugal', 'case', 1), ('Portugal', 'norte', 'nmod', -2), ('.', 'língua', 'punct', -22)]
    )

if __name__ == '__main__':
    test_stanza_por_pt()
