# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Ligurian
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

def test_stanza_lij():
    results_pos_tag = [('O', 'DET'), ('baxin', 'NOUN'), ("d'", 'ADP'), ('influensa', 'NOUN'), ('de', 'ADP'), ('i', 'DET'), ('dialetti', 'NOUN'), ('lìguri', 'ADJ'), ('o', 'PRON'), ("l'", 'PART'), ('é', 'VERB'), ('de', 'ADP'), ('çirca', 'NOUN'), ('2', 'ADP'), ('milioìn', 'NOUN'), ('de', 'ADP'), ('personn-e', 'NOUN'), ('anche', 'ADV'), ('se', 'PRON'), (',', 'PUNCT'), ('specialmente', 'ADV'), ('inte', 'ADP'), ('i', 'DET'), ('ùrtimi', 'NOUN'), ("çinquant'", 'NUM'), ('anni', 'NOUN'), (',', 'PUNCT'), ('pe', 'ADP'), ('coscì', 'ADV'), ('de', 'ADP'), ('variante', 'NOUN'), ('locali', 'NOUN'), ('se', 'PRON'), ('son', 'AUX'), ('pèrse', 'VERB'), ('e', 'CCONJ'), ('de', 'ADP'), ('âtre', 'PRON'), ('son', 'AUX'), ('a', 'DET'), ('reizego', 'ADJ'), ("tutt'", 'PRON'), ('òua', 'NOUN'), (',', 'PUNCT'), ('anche', 'ADV'), ('pe', 'ADP'), ('córpa', 'NOUN'), ('de', 'ADP'), ('a', 'DET'), ('mancansa', 'NOUN'), ('de', 'ADP'), ("'", 'DET'), ('n', 'ADP'), ('pâ', 'NOUN'), ('de', 'ADP'), ('generaçioin', 'NOUN'), ('inte', 'ADP'), ('a', 'DET'), ('continoasion', 'NOUN'), ('de', 'ADP'), ('a', 'DET'), ('parlâ', 'VERB'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'lij',
        results_sentence_tokenize = ["O baxin d'influensa di dialetti lìguri o l'é de çirca 2 milioìn de personn-e anche se, specialmente inti ùrtimi çinquant'anni, pe coscì de variante locali se son pèrse e de âtre son a reizego tutt'òua, anche pe córpa da mancansa de 'n pâ de generaçioin inta continoasion da parlâ.", "Coscî, ancheu, a popolaçion ch'a conosce a léngoa a l'é ben ben infeiô e ancón meno son quelli che a pàrlan e a scrîvan."],
        results_word_tokenize = ['O', 'baxin', "d'", 'influensa', 'di', 'dialetti', 'lìguri', 'o', "l'", 'é', 'de', 'çirca', '2', 'milioìn', 'de', 'personn-e', 'anche', 'se', ',', 'specialmente', 'inti', 'ùrtimi', "çinquant'", 'anni', ',', 'pe', 'coscì', 'de', 'variante', 'locali', 'se', 'son', 'pèrse', 'e', 'de', 'âtre', 'son', 'a', 'reizego', "tutt'", 'òua', ',', 'anche', 'pe', 'córpa', 'da', 'mancansa', 'de', "'", 'n', 'pâ', 'de', 'generaçioin', 'inta', 'continoasion', 'da', 'parlâ', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['o', 'baxin', 'de', 'influensa', 'de', 'o', 'dialetto', 'lìguri', 'o', "l'", 'ëse', 'de', 'çirca', '2', 'milioìn', 'de', 'personn-e', 'anche', 'se', ',', 'specialmente', 'inte', 'o', 'ùrtimo', 'çinqu', 'anno', ',', 'pe', 'coscì', 'de', 'variante', 'localo', 'se', 'ëse', 'pèrse', 'e', 'de', 'âtro', 'ëse', 'o', 'reizego', 'tutto', 'òua', ',', 'anche', 'pe', 'córpa', 'de', 'o', 'mancansa', 'de', "'", 'n', 'pâ', 'de', 'generaçion', 'inte', 'o', 'continoasion', 'de', 'o', 'parlâ', '.'],
        results_dependency_parse = [('O', 'baxin', 'det', 1), ('baxin', 'é', 'nsubj', 9), ("d'", 'influensa', 'case', 1), ('influensa', 'baxin', 'nmod', -2), ('de', 'dialetti', 'case', 2), ('i', 'dialetti', 'det', 1), ('dialetti', 'baxin', 'nmod', -5), ('lìguri', 'dialetti', 'amod', -1), ('o', 'é', 'expl', 2), ("l'", 'é', 'dep', 1), ('é', 'é', 'root', 0), ('de', 'çirca', 'case', 1), ('çirca', 'é', 'obl', -2), ('2', 'milioìn', 'case', 1), ('milioìn', 'é', 'obl', -4), ('de', 'personn-e', 'case', 1), ('personn-e', 'milioìn', 'nmod', -2), ('anche', 'personn-e', 'advmod', -1), ('se', 'personn-e', 'amod', -2), (',', 'ùrtimi', 'punct', 4), ('specialmente', 'ùrtimi', 'advmod', 3), ('inte', 'ùrtimi', 'case', 2), ('i', 'ùrtimi', 'det', 1), ('ùrtimi', 'pèrse', 'obl', 11), ("çinquant'", 'anni', 'nummod', 1), ('anni', 'ùrtimi', 'nmod', -2), (',', 'pèrse', 'punct', 8), ('pe', 'coscì', 'case', 1), ('coscì', 'pèrse', 'advmod', 6), ('de', 'variante', 'case', 1), ('variante', 'coscì', 'conj', -2), ('locali', 'pèrse', 'expl', 3), ('se', 'pèrse', 'expl:pv', 2), ('son', 'pèrse', 'aux', 1), ('pèrse', 'é', 'conj', -24), ('e', "tutt'", 'cc', 6), ('de', 'âtre', 'case', 1), ('âtre', "tutt'", 'obl', 4), ('son', "tutt'", 'cop', 3), ('a', "tutt'", 'det', 2), ('reizego', "tutt'", 'amod', 1), ("tutt'", 'pèrse', 'conj', -7), ('òua', "tutt'", 'flat', -1), (',', 'córpa', 'punct', 3), ('anche', 'córpa', 'advmod', 2), ('pe', 'córpa', 'case', 1), ('córpa', 'pèrse', 'obl', -12), ('de', 'mancansa', 'case', 2), ('a', 'mancansa', 'det', 1), ('mancansa', 'córpa', 'nmod', -3), ('de', 'pâ', 'case', 3), ("'", 'pâ', 'det', 2), ('n', 'pâ', 'case', 1), ('pâ', 'mancansa', 'nmod', -4), ('de', 'generaçioin', 'case', 1), ('generaçioin', 'pâ', 'nmod', -2), ('inte', 'continoasion', 'case', 2), ('a', 'continoasion', 'det', 1), ('continoasion', 'generaçioin', 'nmod', -3), ('de', 'parlâ', 'case', 2), ('a', 'parlâ', 'det', 1), ('parlâ', 'continoasion', 'nmod', -3), ('.', 'é', 'punct', -52)]
    )

if __name__ == '__main__':
    test_stanza_lij()
