# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Portuguese
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

def test_spacy_por():
    results_sentence_tokenize = ['A língua portuguesa, também designada português, é uma língua indo-europeia românica flexiva ocidental originada no galego-português falado no Reino da Galiza e no norte de Portugal.', 'Com a criação do Reino de Portugal em 1139 e a expansão para o sul na sequência da Reconquista, deu-se a difusão da língua pelas terras conquistadas e, mais tarde, com as descobertas portuguesas, para o Brasil, África e outras partes do mundo.[9]']
    results_pos_tag = [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'ADJ'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('indo-europeia', 'ADJ'), ('românica', 'ADJ'), ('flexiva', 'NOUN'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('no', 'ADP'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('no', 'ADP'), ('Reino', 'PROPN'), ('da', 'ADP'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('no', 'ADP'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'por_pt',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = ['A', 'língua', 'portuguesa', ',', 'também', 'designada', 'português', ',', 'é', 'uma', 'língua', 'indo-europeia', 'românica', 'flexiva', 'ocidental', 'originada', 'no', 'galego-português', 'falado', 'no', 'Reino', 'da', 'Galiza', 'e', 'no', 'norte', 'de', 'Portugal', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['o', 'língua', 'português', ',', 'também', 'designar', 'português', ',', 'ser', 'um', 'língua', 'indo-europeia', 'românico', 'flexiva', 'ocidental', 'originar', 'em o', 'galego-português', 'falar', 'em o', 'Reino', 'de o', 'Galiza', 'e', 'em o', 'norte', 'de', 'Portugal', '.'],
        results_dependency_parse = [('A', 'língua', 'det', 1), ('língua', 'língua', 'nsubj', 9), ('portuguesa', 'língua', 'amod', -1), (',', 'designada', 'punct', 2), ('também', 'designada', 'advmod', 1), ('designada', 'língua', 'acl', -4), ('português', 'designada', 'amod', -1), (',', 'designada', 'punct', -2), ('é', 'língua', 'cop', 2), ('uma', 'língua', 'det', 1), ('língua', 'flexiva', 'nsubj', 3), ('indo-europeia', 'língua', 'amod', -1), ('românica', 'língua', 'amod', -2), ('flexiva', 'flexiva', 'ROOT', 0), ('ocidental', 'flexiva', 'amod', -1), ('originada', 'flexiva', 'acl', -2), ('no', 'galego-português', 'case', 1), ('galego-português', 'originada', 'obl', -2), ('falado', 'galego-português', 'acl', -1), ('no', 'Reino', 'case', 1), ('Reino', 'falado', 'obl', -2), ('da', 'Galiza', 'case', 1), ('Galiza', 'Reino', 'nmod', -2), ('e', 'norte', 'cc', 2), ('no', 'norte', 'case', 1), ('norte', 'galego-português', 'conj', -8), ('de', 'Portugal', 'case', 1), ('Portugal', 'norte', 'nmod', -2), ('.', 'flexiva', 'punct', -15)]
    )

if __name__ == '__main__':
    test_spacy_por()
