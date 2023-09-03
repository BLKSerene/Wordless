# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Swedish Sign Language
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

def test_stanza_swl():
    test_stanza.wl_test_stanza(
        lang = 'swl',
        results_sentence_tokenize = ['JA@ub', 'STÄMMA', 'PRO1 BLI BÖRJA MED.VARA LEDAMOT INUTI IDROTT^KLUBB TID-FRAMÅT KASSÖR TID-FRAMÅT BLI IDROTT^KLUBB ORDFÖRANDE TID-FRAMÅT SEX ÅR TID-FRAMÅT'],
        results_word_tokenize = ['JA@ub', 'STÄMMA'],
        results_pos_tag = [('JA@ub', 'INTERJ'), ('STÄMMA', 'VB')],
        results_pos_tag_universal = [('JA@ub', 'INTJ'), ('STÄMMA', 'VERB')],
        results_dependency_parse = [('JA@ub', 'JA@ub', 'root', 0), ('STÄMMA', 'STÄMMA', 'root', 0)]
    )

if __name__ == '__main__':
    test_stanza_swl()
