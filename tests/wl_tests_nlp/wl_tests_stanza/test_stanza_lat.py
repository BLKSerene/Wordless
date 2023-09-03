# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Latin
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

def test_stanza_lat():
    test_stanza.wl_test_stanza(
        lang = 'lat',
        results_sentence_tokenize = ['Lingua Latina,[1] sive sermo Latinus,[2] est lingua Indoeuropaea qua primum Latini universi et Romani antiqui in primis loquebantur quamobrem interdum etiam lingua Latia[3] (in Latio enim sueta) et lingua Romana[4] (nam imperii Romani sermo sollemnis) appellatur.', 'Nomen linguae ductum est a terra quam gentes Latine loquentes incolebant, Latium vetus interdum appellata, in paeninsula Italica inter Tiberim, Volscos, Appenninum, et mare Inferum sita.'],
        results_word_tokenize = ['Lingua', 'Latina', ',', '[1', ']', 'sive', 'sermo', 'Latinus', ',', '[2', ']', 'est', 'lingua', 'Indoeuropaea', 'qua', 'primum', 'Latini', 'universi', 'et', 'Romani', 'antiqui', 'in', 'primis', 'loquebantur', 'quamobrem', 'interdum', 'etiam', 'lingua', 'Latia[3]', '(', 'in', 'Latio', 'enim', 'sueta', ')', 'et', 'lingua', 'Romana[4', ']', '(', 'nam', 'imperii', 'Romani', 'sermo', 'sollemnis', ')', 'appellatur', '.'],
        results_pos_tag = [('Lingua', 'A1|grn1|casA|gen2'), ('Latina', 'A1|grn1|casA|gen2'), (',', 'Punc'), ('[1', 'C1|grn1|casA|gen2'), (']', 'Punc'), ('sive', 'O4'), ('sermo', 'C1|grn1|casA|gen1'), ('Latinus', 'B1|grn1|casA|gen1'), (',', 'Punc'), ('[2', '5|grn1|casA|gen1'), (']', '5|grn1|gen2'), ('est', 'N3|modA|tem1|gen6'), ('lingua', 'A1|grn1|casA|gen2'), ('Indoeuropaea', 'A1|grn1|casA|gen2'), ('qua', 'F1|grn1|casF|gen2|varA'), ('primum', 'B1|grn1|casA|gen3'), ('Latini', 'B1|grn1|casJ|gen1'), ('universi', 'B1|grn1|casJ|gen1'), ('et', 'O4'), ('Romani', 'B1|grn1|casJ|gen1'), ('antiqui', 'B1|grn1|casJ|gen1'), ('in', 'S4'), ('primis', 'B1|grn1|casO|gen1'), ('loquebantur', 'L3|modJ|tem2|gen9'), ('quamobrem', 'O4'), ('interdum', 'O4'), ('etiam', 'O4|vgr1'), ('lingua', 'A1|grn1|casA|gen2'), ('Latia[3]', 'G5'), ('(', 'Punc'), ('in', 'S4'), ('Latio', 'B1|grn1|casF|gen3'), ('enim', 'O4'), ('sueta', 'L2|modM|tem4|grp1|casA|gen2'), (')', 'Punc'), ('et', 'O4'), ('lingua', 'A1|grn1|casA|gen2'), ('Romana[4', 'G5'), (']', 'G5'), ('(', 'Punc'), ('nam', 'O4'), ('imperii', 'B1|grn1|casB|gen3'), ('Romani', 'B1|grn1|casB|gen1'), ('sermo', 'C1|grn1|casA|gen1'), ('sollemnis', 'C1|grn1|casA|gen1'), (')', 'Punc'), ('appellatur', 'J3|modJ|tem1|gen6'), ('.', 'Punc')],
        results_pos_tag_universal = [('Lingua', 'NOUN'), ('Latina', 'ADJ'), (',', 'PUNCT'), ('[1', 'NOUN'), (']', 'PUNCT'), ('sive', 'CCONJ'), ('sermo', 'NOUN'), ('Latinus', 'ADJ'), (',', 'PUNCT'), ('[2', 'NOUN'), (']', 'NOUN'), ('est', 'AUX'), ('lingua', 'NOUN'), ('Indoeuropaea', 'ADJ'), ('qua', 'PRON'), ('primum', 'ADJ'), ('Latini', 'NOUN'), ('universi', 'ADJ'), ('et', 'CCONJ'), ('Romani', 'ADJ'), ('antiqui', 'ADJ'), ('in', 'ADP'), ('primis', 'ADJ'), ('loquebantur', 'VERB'), ('quamobrem', 'ADV'), ('interdum', 'ADV'), ('etiam', 'ADV'), ('lingua', 'NOUN'), ('Latia[3]', 'NUM'), ('(', 'PUNCT'), ('in', 'ADP'), ('Latio', 'NOUN'), ('enim', 'ADV'), ('sueta', 'VERB'), (')', 'PUNCT'), ('et', 'CCONJ'), ('lingua', 'NOUN'), ('Romana[4', 'NUM'), (']', 'NUM'), ('(', 'PUNCT'), ('nam', 'ADV'), ('imperii', 'NOUN'), ('Romani', 'ADJ'), ('sermo', 'NOUN'), ('sollemnis', 'ADJ'), (')', 'PUNCT'), ('appellatur', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['Lingua', 'Latina', ',', '[1', ']', 'sive', 'sermo', 'Latinus', ',', '[2', ']', 'sum', 'lingua', 'Indoeuropaea', 'qui', 'primus', 'Latini', 'universi', 'et', 'Romani', 'antiquus', 'in', 'primus', 'loquor', 'quamobrem', 'interdum', 'etiam', 'lingua', 'Latia[3]', '(', 'in', 'Latio', 'enim', 'sueo', ')', 'et', 'lingua', 'Romana[4', ']', '(', 'nam', 'imperium', 'Romani', 'sermo', 'sollemnis', ')', 'appello', '.'],
        results_dependency_parse = [('Lingua', 'Lingua', 'root', 0), ('Latina', 'Lingua', 'amod', -1), (',', '[1', 'punct', 1), ('[1', 'Lingua', 'conj', -3), (']', 'sermo', 'punct', 2), ('sive', 'sermo', 'cc', 1), ('sermo', 'Lingua', 'conj', -6), ('Latinus', 'sermo', 'amod', -1), (',', '[2', 'punct', 1), ('[2', 'Lingua', 'conj', -9), (']', '[2', 'nmod', -1), ('est', 'Lingua', 'cop', -11), ('lingua', 'Lingua', 'conj', -12), ('Indoeuropaea', 'lingua', 'amod', -1), ('qua', 'loquebantur', 'obl', 9), ('primum', 'Latini', 'amod', 1), ('Latini', 'loquebantur', 'nsubj', 7), ('universi', 'Latini', 'amod', -1), ('et', 'Romani', 'cc', 1), ('Romani', 'universi', 'conj', -2), ('antiqui', 'Latini', 'amod', -4), ('in', 'primis', 'case', 1), ('primis', 'loquebantur', 'obl', 1), ('loquebantur', 'lingua', 'acl:relcl', -11), ('quamobrem', 'loquebantur', 'advmod', -1), ('interdum', 'loquebantur', 'advmod', -2), ('etiam', 'lingua', 'advmod:emph', 1), ('lingua', 'loquebantur', 'nsubj', -4), ('Latia[3]', 'lingua', 'nummod', -1), ('(', 'sueta', 'punct', 4), ('in', 'Latio', 'case', 1), ('Latio', 'sueta', 'obl', 2), ('enim', 'sueta', 'advmod', 1), ('sueta', 'loquebantur', 'conj', -10), (')', 'sueta', 'punct', -1), ('et', 'lingua', 'cc', 1), ('lingua', 'sueta', 'conj', -3), ('Romana[4', 'lingua', 'nummod', -1), (']', 'lingua', 'nummod', -2), ('(', 'appellatur', 'punct', 7), ('nam', 'appellatur', 'advmod', 6), ('imperii', 'sermo', 'nmod', 2), ('Romani', 'imperii', 'amod', -1), ('sermo', 'appellatur', 'nsubj:pass', 3), ('sollemnis', 'sermo', 'amod', -1), (')', 'appellatur', 'punct', 1), ('appellatur', 'loquebantur', 'conj', -23), ('.', 'Lingua', 'punct', -47)]
    )

if __name__ == '__main__':
    test_stanza_lat()
