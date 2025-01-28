# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Galician
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

def test_stanza_glg():
    test_stanza.wl_test_stanza(
        lang = 'glg',
        results_sentence_tokenize = ['O galego ([ɡaˈleɣo̝][1]) é unha lingua indoeuropea que pertence á póla de linguas románicas.', 'É a lingua propia de Galicia,[5] onde é falada por uns 2,4 millóns de galegos.[6]', 'Á parte de en Galicia, a lingua fálase tamén en territorios limítrofes con esta comunidade, aínda que sen estatuto de oficialidade (agás en casos puntuais, como na Veiga),[7] así como pola diáspora galega que emigrou a outras partes de España, a América Latina, os Estados Unidos, Suíza e outros países de Europa.'],
        results_word_tokenize = ['O', 'galego', '(', '[ɡaˈleɣo̝', ']', '[', '1', ']', ')', 'é', 'unha', 'lingua', 'indoeuropea', 'que', 'pertence', 'á', 'póla', 'de', 'linguas', 'románicas', '.'],
        results_pos_tag = [('O', 'DA0MS0'), ('galego', 'AQ0MS0'), ('(', 'Fpa'), ('[ɡaˈleɣo̝', 'NP00000'), (']', 'Fct'), ('[', 'Fc'), ('1', 'Z'), (']', 'Fct'), (')', 'Fpt'), ('é', 'VSIP3S0'), ('unha', 'DI0FS0'), ('lingua', 'NCFS000'), ('indoeuropea', 'AQ0FS0'), ('que', 'PR0CN000'), ('pertence', 'VMIP3S0'), ('a', 'SPS00'), ('a', 'DA0FS0'), ('póla', 'NCFS000'), ('de', 'SPS00'), ('linguas', 'NCFP000'), ('románicas', 'AQ0FP0'), ('.', 'Fp')],
        results_pos_tag_universal = [('O', 'DET'), ('galego', 'ADJ'), ('(', 'PUNCT'), ('[ɡaˈleɣo̝', 'PROPN'), (']', 'PUNCT'), ('[', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('é', 'AUX'), ('unha', 'DET'), ('lingua', 'NOUN'), ('indoeuropea', 'ADJ'), ('que', 'PRON'), ('pertence', 'VERB'), ('a', 'ADP'), ('a', 'DET'), ('póla', 'NOUN'), ('de', 'ADP'), ('linguas', 'NOUN'), ('románicas', 'ADJ'), ('.', 'PUNCT')],
        results_lemmatize = ['o', 'galego', '(', '[ɡaˈleɣo̝', ']', '[', '1', ']', ')', 'ser', 'un', 'lingua', 'indoeuropeo', 'que', 'pertencer', 'a', 'o', 'póla', 'de', 'lingua', 'románico', '.'],
        results_dependency_parse = [('O', 'galego', 'det', 1), ('galego', 'lingua', 'nsubj', 10), ('(', '[ɡaˈleɣo̝', 'punct', 1), ('[ɡaˈleɣo̝', 'galego', 'nmod', -2), (']', '[ɡaˈleɣo̝', 'punct', -1), ('[', '1', 'punct', 1), ('1', '[ɡaˈleɣo̝', 'nmod', -3), (']', '1', 'punct', -1), (')', '1', 'punct', -2), ('é', 'lingua', 'cop', 2), ('unha', 'lingua', 'det', 1), ('lingua', 'lingua', 'root', 0), ('indoeuropea', 'lingua', 'amod', -1), ('que', 'pertence', 'nsubj', 1), ('pertence', 'lingua', 'ccomp', -3), ('a', 'pertence', 'obj', -1), ('a', 'póla', 'det', 1), ('póla', 'a', 'nmod', -2), ('de', 'linguas', 'case', 1), ('linguas', 'póla', 'nmod', -2), ('románicas', 'linguas', 'amod', -1), ('.', 'lingua', 'punct', -10)]
    )

if __name__ == '__main__':
    test_stanza_glg()
