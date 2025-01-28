# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Czech
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

def test_stanza_ces():
    test_stanza.wl_test_stanza(
        lang = 'ces',
        results_sentence_tokenize = ['Čeština neboli český jazyk je západoslovanský jazyk, nejbližší slovenštině, poté lužické srbštině a polštině.', 'Patří mezi slovanské jazyky, do rodiny jazyků indoevropských.', 'Čeština se vyvinula ze západních nářečí praslovanštiny na konci 10. století.', 'Je částečně ovlivněná latinou a němčinou.', 'Česky psaná literatura se objevuje od 14. století.', 'První písemné památky jsou však již z 12. století.'],
        results_word_tokenize = ['Čeština', 'neboli', 'český', 'jazyk', 'je', 'západoslovanský', 'jazyk', ',', 'nejbližší', 'slovenštině', ',', 'poté', 'lužické', 'srbštině', 'a', 'polštině', '.'],
        results_pos_tag = [('Čeština', 'NNFS1-----A----'), ('neboli', 'J^-------------'), ('český', 'AAIS1----1A----'), ('jazyk', 'NNIS1-----A----'), ('je', 'VB-S---3P-AAI--'), ('západoslovanský', 'AAIS1----1A----'), ('jazyk', 'NNIS1-----A----'), (',', 'Z:-------------'), ('nejbližší', 'AAFS3----3A----'), ('slovenštině', 'NNFS6-----A----'), (',', 'Z:-------------'), ('poté', 'Db-------------'), ('lužické', 'AAFS6----1A----'), ('srbštině', 'NNFS6-----A----'), ('a', 'J^-------------'), ('polštině', 'NNFS6-----A----'), ('.', 'Z:-------------')],
        results_pos_tag_universal = [('Čeština', 'NOUN'), ('neboli', 'CCONJ'), ('český', 'ADJ'), ('jazyk', 'NOUN'), ('je', 'AUX'), ('západoslovanský', 'ADJ'), ('jazyk', 'NOUN'), (',', 'PUNCT'), ('nejbližší', 'ADJ'), ('slovenštině', 'NOUN'), (',', 'PUNCT'), ('poté', 'ADV'), ('lužické', 'ADJ'), ('srbštině', 'NOUN'), ('a', 'CCONJ'), ('polštině', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['čeština', 'neboli', 'český', 'jazyk', 'být', 'západoslovanský', 'jazyk', ',', 'blízký', 'slovenština', ',', 'poté', 'lužický', 'srbština', 'a', 'polština', '.'],
        results_dependency_parse = [('Čeština', 'jazyk', 'nsubj', 6), ('neboli', 'jazyk', 'cc', 2), ('český', 'jazyk', 'amod', 1), ('jazyk', 'Čeština', 'appos', -3), ('je', 'jazyk', 'cop', 2), ('západoslovanský', 'jazyk', 'amod', 1), ('jazyk', 'jazyk', 'root', 0), (',', 'slovenštině', 'punct', 2), ('nejbližší', 'slovenštině', 'amod', 1), ('slovenštině', 'jazyk', 'conj', -3), (',', 'poté', 'punct', 1), ('poté', 'jazyk', 'conj', -5), ('lužické', 'srbštině', 'amod', 1), ('srbštině', 'poté', 'orphan', -2), ('a', 'polštině', 'cc', 1), ('polštině', 'srbštině', 'conj', -2), ('.', 'jazyk', 'punct', -10)]
    )

if __name__ == '__main__':
    test_stanza_ces()
