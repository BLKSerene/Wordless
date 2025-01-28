# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Pomak
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

def test_stanza_qpm():
    results_pos_tag = [('Kážyjte', 'VERB'), ('nǽko', 'DET'), (',', 'PUNCT'), ('de', 'PART'), ('!', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'qpm',
        results_sentence_tokenize = ['Kážyjte nǽko, de! Še go preskókneme!'],
        results_word_tokenize = ['Kážyjte', 'nǽko', ',', 'de', '!'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['kážom', 'nǽko', ',', 'de', '!'],
        results_dependency_parse = [('Kážyjte', 'Kážyjte', 'root', 0), ('nǽko', 'Kážyjte', 'det', -1), (',', 'de', 'punct', 1), ('de', 'Kážyjte', 'vocative', -3), ('!', 'Kážyjte', 'punct', -4)]
    )

if __name__ == '__main__':
    test_stanza_qpm()
