# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Nigerian Pidgin
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

def test_stanza_pcm():
    results_pos_tag = [('Naijá', 'PROPN'), ('na', 'AUX'), ('pijin,', 'VERB'), ('a', 'DET'), ('langwej', 'NOUN'), ('for', 'ADP'), ('oda', 'ADJ'), ('langwej.', 'NOUN')]

    test_stanza.wl_test_stanza(
        lang = 'pcm',
        results_sentence_tokenize = ['Naijá na pijin, a langwej for oda langwej. Naijá for Inglish an wey Afrikan langwej.'],
        results_word_tokenize = ['Naijá', 'na', 'pijin,', 'a', 'langwej', 'for', 'oda', 'langwej.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['Naijá', 'na', 'pijin,', 'a', 'langwej', 'for', 'oder', 'langwej.'],
        results_dependency_parse = [('Naijá', 'pijin,', 'nsubj', 2), ('na', 'pijin,', 'cop', 1), ('pijin,', 'pijin,', 'root', 0), ('a', 'langwej', 'det', 1), ('langwej', 'pijin,', 'obj', -2), ('for', 'oda', 'case', 1), ('oda', 'pijin,', 'obl:arg', -4), ('langwej.', 'pijin,', 'dep', -5)]
    )

if __name__ == '__main__':
    test_stanza_pcm()
