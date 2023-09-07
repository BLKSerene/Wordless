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

TOKENS_100 = ['This', 'is', 'a', 'sentence', '.'] * 20
TOKENS_101 = ['This', 'is', 'a', 'sentence', '.'] * 20 + ['another']
TOKENS_1000 = ['This', 'is', 'a', 'sentence', '.'] * 200

def test_msttr():
    msttr_100 = wl_measures_ttr.msttr(main, TOKENS_101)
    settings['msttr']['num_tokens_in_each_seg'] = 1000
    msttr_1000 = wl_measures_ttr.msttr(main, TOKENS_101)

    assert msttr_100 == 5 / 100
    assert msttr_1000 == 0

def test_mtld():
    mtld_100 = wl_measures_ttr.mtld(main, TOKENS_100)

    assert mtld_100 == 100 / (14 + 0 / 0.28)

def test_mattr():
    mattr_100 = wl_measures_ttr.mattr(main, TOKENS_100)
    mattr_1000 = wl_measures_ttr.mattr(main, TOKENS_1000)

    assert mattr_100 == wl_measures_ttr.ttr(main, TOKENS_100)
    assert mattr_1000 == 5 / 500

def test_ttr():
    ttr = wl_measures_ttr.ttr(main, TOKENS_100)

    assert ttr == 5 / 100

if __name__ == '__main__':
    test_msttr()
    test_mtld()
    test_mattr()
    test_ttr()
