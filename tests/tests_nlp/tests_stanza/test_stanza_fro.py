# ----------------------------------------------------------------------
# Tests: NLP - Stanza - French (Old)
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

def test_stanza_fro():
    test_stanza.wl_test_stanza(
        lang = 'fro',
        results_sentence_tokenize = ["Si l'orrat Carles, ki est as porz passant. Je vos plevis, ja returnerunt Franc."],
        results_word_tokenize = ['Si', "l'", 'orrat', 'Carles', ',', 'ki', 'est', 'as', 'porz', 'passant', '.'],
        results_pos_tag = [('Si', 'ADVgen'), ("l'", 'PROper'), ('orrat', 'VERcjg'), ('Carles', 'NOMpro'), (',', 'PONfbl'), ('ki', 'PROrel'), ('est', 'VERcjg'), ('as', 'PRE.DETdef'), ('porz', 'NOMcom'), ('passant', 'VERppa'), ('.', 'PONfrt')],
        results_pos_tag_universal = [('Si', 'ADV'), ("l'", 'PRON'), ('orrat', 'VERB'), ('Carles', 'PROPN'), (',', 'PUNCT'), ('ki', 'PRON'), ('est', 'AUX'), ('as', 'ADP'), ('porz', 'NOUN'), ('passant', 'VERB'), ('.', 'PUNCT')],
        results_lemmatize = ['si', "l'", 'orrat', 'Carles', ',', 'ki', 'est', 'as', 'porz', 'passant', '.'],
        results_dependency_parse = [('Si', 'orrat', 'advmod', 2), ("l'", 'orrat', 'obj', 1), ('orrat', 'orrat', 'root', 0), ('Carles', 'orrat', 'nsubj', -1), (',', 'Carles', 'punct', -1), ('ki', 'passant', 'nsubj', 4), ('est', 'passant', 'aux', 3), ('as', 'porz', 'case:det', 1), ('porz', 'passant', 'obl', 1), ('passant', 'Carles', 'acl:relcl', -6), ('.', 'orrat', 'punct', -8)]
    )

if __name__ == '__main__':
    test_stanza_fro()
