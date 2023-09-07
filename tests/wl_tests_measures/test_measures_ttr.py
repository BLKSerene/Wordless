# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Type-token ratio
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

from tests import wl_test_init
from wordless.wl_measures import wl_measures_ttr

main = wl_test_init.Wl_Test_Main()
settings = main.settings_custom['measures']['ttr']

TOKENS_15 = ['This', 'is', 'a', 'sentence', '.', 'This', 'is', 'a', 'sentence', '.', 'This', 'is', 'a', 'sen-tence0', '.']
TOKENS_101 = ['This', 'is', 'a', 'sentence', '.'] * 20 + ['another']

def test_msttr():
    msttr_100 = wl_measures_ttr.msttr(main, TOKENS_101)
    settings['msttr']['num_tokens_in_each_seg'] = 1000
    msttr_1000 = wl_measures_ttr.msttr(main, TOKENS_101)

    assert msttr_100 == (5 / 100 + 1 / 1) / 2
    assert msttr_1000 == 6 / 101

def test_ttr():
    ttr = wl_measures_ttr.ttr(main, TOKENS_15)

    assert ttr == 6 / 15

if __name__ == '__main__':
    test_msttr()
    test_ttr()
