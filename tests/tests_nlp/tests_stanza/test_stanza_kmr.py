# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Kurdish (Kurmanji)
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

def test_stanza_kmr():
    test_stanza.wl_test_stanza(
        lang = 'kmr',
        results_sentence_tokenize = ['Kurmancî, Kurdiya jorîn yan jî Kurdiya bakurî yek ji zaravayên zimanê kurdî ye ku ji aliyê kurdan ve tê axaftin.', 'Zaravayê kurmancî li herçar parçeyên Kurdistanê bi awayekî berfireh tê axaftin û rêjeya zêde ya kurdan bi zaravayê kurmancî diaxivin.', 'Kurmancî li henek deverên herêmên Kurdistanê bi navên cuda cuda hatiye binavkirin.', 'Li Rojhilatê Kurdistanê wekî şikakî û li Başurê Kurdistanê jî wek badînî hatiye binavkirin.'],
        results_word_tokenize = ['Kurmancî', ',', 'Kurdiya', 'jorîn', 'yan', 'jî', 'Kurdiya', 'bakurî', 'yek', 'ji', 'zaravayên', 'zimanê', 'kurdî', 'ye', 'ku', 'ji', 'aliyê', 'kurdan', 've', 'tê', 'axaftin', '.'],
        results_pos_tag = [('Kurmancî', 'n'), (',', 'cm'), ('Kurdiya', 'n'), ('jorîn', 'np'), ('yan', 'cnjcoo'), ('jî', 'emph'), ('Kurdiya', 'n'), ('bakurî', 'n'), ('yek', 'num'), ('ji', 'pr'), ('zaravayên', 'n'), ('zimanê', 'n'), ('kurdî', 'adj'), ('ye', 'con'), ('ku', 'cnjsub'), ('ji', 'pr'), ('aliyê', 'n'), ('kurdan', 'n'), ('ve', 'post'), ('tê', 'vblex'), ('axaftin', 'vblex'), ('.', 'sent')],
        results_pos_tag_universal = [('Kurmancî', 'NOUN'), (',', 'PUNCT'), ('Kurdiya', 'NOUN'), ('jorîn', 'PROPN'), ('yan', 'CCONJ'), ('jî', 'PART'), ('Kurdiya', 'NOUN'), ('bakurî', 'NOUN'), ('yek', 'NUM'), ('ji', 'ADP'), ('zaravayên', 'NOUN'), ('zimanê', 'NOUN'), ('kurdî', 'ADJ'), ('ye', 'ADP'), ('ku', 'SCONJ'), ('ji', 'ADP'), ('aliyê', 'NOUN'), ('kurdan', 'NOUN'), ('ve', 'ADP'), ('tê', 'AUX'), ('axaftin', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['kurmancî', ',', 'kurdî', 'jorîn', 'yan', 'jî', 'kurdî', 'bakurî', 'yek', 'ji', 'zarava', 'ziman', 'kurdî', 'yê', 'ku', 'ji', 'alî', 'kurd', 've', 'hatin', 'axaftin', '.'],
        results_dependency_parse = [('Kurmancî', 'yek', 'nsubj', 8), (',', 'Kurmancî', 'punct', -1), ('Kurdiya', 'Kurmancî', 'appos', -2), ('jorîn', 'Kurdiya', 'nmod:poss', -1), ('yan', 'Kurdiya', 'cc', 2), ('jî', 'Kurdiya', 'advmod', 1), ('Kurdiya', 'Kurdiya', 'conj', -4), ('bakurî', 'Kurdiya', 'nmod:poss', -1), ('yek', 'yek', 'root', 0), ('ji', 'zaravayên', 'case', 1), ('zaravayên', 'yek', 'nmod', -2), ('zimanê', 'zaravayên', 'nmod:poss', -1), ('kurdî', 'zimanê', 'amod', -1), ('ye', 'zimanê', 'case', -2), ('ku', 'axaftin', 'mark', 6), ('ji', 'aliyê', 'case', 1), ('aliyê', 'axaftin', 'nmod', 4), ('kurdan', 'aliyê', 'nmod:poss', -1), ('ve', 'aliyê', 'case', -2), ('tê', 'axaftin', 'aux', 1), ('axaftin', 'yek', 'advcl', -12), ('.', 'yek', 'punct', -13)]
    )

if __name__ == '__main__':
    test_stanza_kmr()
