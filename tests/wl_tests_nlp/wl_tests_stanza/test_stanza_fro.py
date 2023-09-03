# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - French (Old)
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

def test_stanza_fro():
    test_stanza.wl_test_stanza(
        lang = 'fro',
        results_sentence_tokenize = ["Si l'orrat Carles, ki est as porz passant. Je vos plevis, ja returnerunt Franc."],
        results_word_tokenize = ['Si', "l'orrat", 'Carles,', 'ki', 'est', 'as', 'porz', 'passant.'],
        results_pos_tag = [('Si', 'ADVgen'), ("l'orrat", 'VERcjg'), ('Carles,', 'NOMpro'), ('ki', 'PROrel'), ('est', 'VERcjg'), ('as', 'PRE.DETdef'), ('porz', 'NOMcom'), ('passant.', 'VERppa')],
        results_pos_tag_universal = [('Si', 'ADV'), ("l'orrat", 'VERB'), ('Carles,', 'PROPN'), ('ki', 'PRON'), ('est', 'AUX'), ('as', 'ADP'), ('porz', 'NOUN'), ('passant.', 'VERB')],
        results_dependency_parse = [('Si', "l'orrat", 'advmod', 1), ("l'orrat", "l'orrat", 'root', 0), ('Carles,', "l'orrat", 'nsubj', -1), ('ki', 'passant.', 'nsubj', 4), ('est', 'passant.', 'aux', 3), ('as', 'porz', 'case:det', 1), ('porz', 'passant.', 'obl', 1), ('passant.', 'Carles,', 'acl:relcl', -5)]
    )

if __name__ == '__main__':
    test_stanza_fro()
