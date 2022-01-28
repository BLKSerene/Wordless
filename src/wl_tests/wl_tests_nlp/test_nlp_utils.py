# ----------------------------------------------------------------------
# Wordless: Tests - NLP - NLP Utilities
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

from wl_nlp import wl_nlp_utils
from wl_tests import wl_test_init

main = wl_test_init.Wl_Test_Main()

SENTENCE_SRP_CYRL = 'Српски језик припада словенској групи језика породице индоевропских језика.[12]'
SENTENCE_SRP_LATN = 'Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12]'

def test_to_sections():
    tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    token_sections = wl_nlp_utils.to_sections(tokens, num_sections = 5)

    assert token_sections == [[1, 2, 3], [4, 5, 6], [7, 8], [9, 10], [11, 12]]

def test_to_sections_unequal():
    tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    token_sections = list(wl_nlp_utils.to_sections_unequal(tokens, section_size = 5))

    assert token_sections == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12]]

def test_srp_cyrl_to_latn():
    tokens_srp_cyrl = SENTENCE_SRP_CYRL.split()

    assert ' '.join(wl_nlp_utils.to_srp_latn(tokens_srp_cyrl)) == SENTENCE_SRP_LATN

def test_srp_latn_to_cyrl():
    tokens_srp_latn = SENTENCE_SRP_LATN.split()

    assert ' '.join(wl_nlp_utils.to_srp_cyrl(tokens_srp_latn)) == SENTENCE_SRP_CYRL

if __name__ == '__main__':
    test_to_sections()
    test_to_sections_unequal()
    test_srp_cyrl_to_latn()
    test_srp_latn_to_cyrl()
