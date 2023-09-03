# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Ligurian
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_lij():
    results_pos_tag = [('O', 'DET'), ('baxin', 'NOUN'), ("d'", 'ADP'), ('influensa', 'NOUN'), ('de', 'ADP'), ('i', 'DET'), ('dialetti', 'NOUN'), ('lìguri', 'ADJ'), ('o', 'PRON'), ("l'", 'PART'), ('é', 'VERB'), ('de', 'ADP'), ('çirca', 'NOUN'), ('2', 'ADP'), ('milioìn', 'NOUN'), ('de', 'ADP'), ('personn-e', 'VERB'), ('anche', 'ADV'), ('se', 'PRON'), (',', 'PUNCT'), ('specialmente', 'VERB'), ('inte', 'ADP'), ('i', 'DET'), ('ùrtimi', 'NOUN'), ("çinquant'", 'ADV'), ('anni', 'NOUN'), (',', 'PUNCT'), ('pe', 'ADP'), ('coscì', 'ADV'), ('de', 'ADP'), ('variante', 'NOUN'), ('locali', 'NOUN'), ('se', 'PRON'), ('son', 'AUX'), ('pèrse', 'ADJ'), ('e', 'CCONJ'), ('de', 'ADP'), ('âtre', 'DET'), ('son', 'AUX'), ('a', 'DET'), ('reizego', 'ADJ'), ("tutt'", 'DET'), ('òua', 'NOUN'), (',', 'PUNCT'), ('anche', 'ADV'), ('pe', 'ADP'), ('córpa', 'NOUN'), ('de', 'ADP'), ('a', 'DET'), ('mancansa', 'NOUN'), ('de', 'ADP'), ("'", 'PUNCT'), ('n', 'ADJ'), ('pâ', 'NOUN'), ('de', 'ADP'), ('generaçioin', 'NOUN'), ('inte', 'ADP'), ('a', 'DET'), ('continoasion', 'NOUN'), ('de', 'ADP'), ('a', 'DET'), ('parlâ', 'VERB'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'lij',
        results_sentence_tokenize = ["O baxin d'influensa di dialetti lìguri o l'é de çirca 2 milioìn de personn-e anche se, specialmente inti ùrtimi çinquant'anni, pe coscì de variante locali se son pèrse e de âtre son a reizego tutt'òua, anche pe córpa da mancansa de 'n pâ de generaçioin inta continoasion da parlâ.", "Coscî, ancheu, a popolaçion ch'a conosce a léngoa a l'é ben ben infeiô e ancón meno son quelli che a pàrlan e a scrîvan."],
        results_word_tokenize = ['O', 'baxin', "d'", 'influensa', 'di', 'dialetti', 'lìguri', 'o', "l'", 'é', 'de', 'çirca', '2', 'milioìn', 'de', 'personn-e', 'anche', 'se', ',', 'specialmente', 'inti', 'ùrtimi', "çinquant'", 'anni', ',', 'pe', 'coscì', 'de', 'variante', 'locali', 'se', 'son', 'pèrse', 'e', 'de', 'âtre', 'son', 'a', 'reizego', "tutt'", 'òua', ',', 'anche', 'pe', 'córpa', 'da', 'mancansa', 'de', "'", 'n', 'pâ', 'de', 'generaçioin', 'inta', 'continoasion', 'da', 'parlâ', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['o', 'baxin', 'de', 'influensa', 'de', 'o', 'dialetto', 'lìguri', 'o', "l'", 'ëse', 'de', 'çirca', '2', 'milioìn', 'de', 'personn-e', 'anche', 'se', ',', 'specialmente', 'inte', 'o', 'ùrtimo', 'çinquante', 'anno', ',', 'pe', 'coscì', 'de', 'variante', 'localio', 'se', 'ëse', 'pèrse', 'e', 'de', 'âtro', 'ëse', 'o', 'reizego', 'tutto', 'òua', ',', 'anche', 'pe', 'córpa', 'de', 'o', 'mancansa', 'de', "'", 'n', 'pâ', 'de', 'generaçion', 'inte', 'o', 'continoasion', 'de', 'o', 'parlâ', '.'],
        results_dependency_parse = [('O', 'baxin', 'det', 1), ('baxin', 'é', 'nsubj', 9), ("d'", 'influensa', 'case', 1), ('influensa', 'baxin', 'nmod', -2), ('de', 'i', 'case', 1), ('i', 'dialetti', 'det', 1), ('dialetti', 'baxin', 'nmod', -5), ('lìguri', 'dialetti', 'amod', -1), ('o', 'é', 'expl', 2), ("l'", 'é', 'dep', 1), ('é', 'é', 'root', 0), ('de', 'çirca', 'case', 1), ('çirca', 'é', 'obl', -2), ('2', 'milioìn', 'case', 1), ('milioìn', 'é', 'obl', -4), ('de', 'personn-e', 'case', 1), ('personn-e', 'milioìn', 'acl', -2), ('anche', 'personn-e', 'advmod', -1), ('se', 'personn-e', 'expl:impers', -2), (',', 'specialmente', 'punct', 1), ('specialmente', 'é', 'conj', -10), ('inte', 'ùrtimi', 'case', 2), ('i', 'ùrtimi', 'det', 1), ('ùrtimi', 'specialmente', 'obl', -3), ("çinquant'", 'anni', 'advmod', 1), ('anni', 'ùrtimi', 'nmod', -2), (',', 'pèrse', 'punct', 8), ('pe', 'coscì', 'case', 1), ('coscì', 'pèrse', 'advmod', 6), ('de', 'variante', 'case', 1), ('variante', 'pèrse', 'nsubj', 4), ('locali', 'pèrse', 'nsubj', 3), ('se', 'pèrse', 'expl:impers', 2), ('son', 'pèrse', 'cop', 1), ('pèrse', 'ùrtimi', 'acl:relcl', -11), ('e', 'reizego', 'cc', 5), ('de', 'âtre', 'case', 1), ('âtre', 'reizego', 'det', 3), ('son', 'reizego', 'cop', 2), ('a', 'reizego', 'det', 1), ('reizego', 'pèrse', 'conj', -6), ("tutt'", 'òua', 'det', 1), ('òua', 'reizego', 'nmod', -2), (',', 'córpa', 'punct', 3), ('anche', 'córpa', 'advmod', 2), ('pe', 'córpa', 'case', 1), ('córpa', 'reizego', 'obl', -6), ('de', 'mancansa', 'case', 2), ('a', 'mancansa', 'det', 1), ('mancansa', 'córpa', 'nmod', -3), ('de', 'pâ', 'case', 3), ("'", 'pâ', 'punct', 2), ('n', 'pâ', 'amod', 1), ('pâ', 'mancansa', 'nmod', -4), ('de', 'generaçioin', 'case', 1), ('generaçioin', 'pâ', 'nmod', -2), ('inte', 'continoasion', 'case', 2), ('a', 'continoasion', 'det', 1), ('continoasion', 'pâ', 'obl', -5), ('de', 'parlâ', 'case', 2), ('a', 'parlâ', 'det', 1), ('parlâ', 'continoasion', 'nmod', -3), ('.', 'é', 'punct', -52)]
    )

if __name__ == '__main__':
    test_stanza_lij()
