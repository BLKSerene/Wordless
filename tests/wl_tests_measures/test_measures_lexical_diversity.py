# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Lexical diversity
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

import numpy
import scipy

from tests import wl_test_init
from wordless.wl_measures import wl_measures_lexical_diversity

main = wl_test_init.Wl_Test_Main()
settings = main.settings_custom['measures']['lexical_diversity']

TOKENS_10 = ['This', 'is', 'a', 'sentence', '.'] * 2
TOKENS_100 = ['This', 'is', 'a', 'sentence', '.'] * 20
TOKENS_101 = ['This', 'is', 'a', 'sentence', '.'] * 20 + ['another']
TOKENS_1000 = ['This', 'is', 'a', 'sentence', '.'] * 200

def test_cttr():
    cttr = wl_measures_lexical_diversity.cttr(main, TOKENS_100)

    assert cttr == 5 / (2 * 100) ** 0.5

# Reference: Fisher, R. A., Steven, A. C., & Williams, C. B. (1943). The relation between the number of species and the number of individuals in a random sample of an animal population. Journal of Animal Ecology, 12(1), 56. https://doi.org/10.2307/1411
def test_fishers_index_of_diversity():
    tokens = [str(i) for i in range(240)] + ['0'] * (15609 - 240)
    alpha = wl_measures_lexical_diversity.fishers_index_of_diversity(main, tokens)

    assert round(alpha, 3) == 40.247

def test_herdans_vm():
    vm = wl_measures_lexical_diversity.herdans_vm(main, TOKENS_100)

    assert vm == (5 * 20 ** 2) / (100 ** 2) - 1 / 5

def test_hdd():
    hdd_100 = wl_measures_lexical_diversity.hdd(main, TOKENS_100)

    assert hdd_100 == (1 - scipy.stats.hypergeom.pmf(k = 0, M = 100, n = 20, N = 42)) * (1 / 42) * 5

def test_logttr():
    settings['logttr']['variant'] = 'Herdan'
    logttr_herdan = wl_measures_lexical_diversity.logttr(main, TOKENS_100)
    settings['logttr']['variant'] = 'Somers'
    logttr_somers = wl_measures_lexical_diversity.logttr(main, TOKENS_100)
    settings['logttr']['variant'] = 'Rubet'
    logttr_rubet = wl_measures_lexical_diversity.logttr(main, TOKENS_100)
    settings['logttr']['variant'] = 'Maas'
    logttr_maas = wl_measures_lexical_diversity.logttr(main, TOKENS_100)
    settings['logttr']['variant'] = 'Dugast'
    logttr_dugast = wl_measures_lexical_diversity.logttr(main, TOKENS_100)

    num_types = 5
    num_tokens = 100

    assert logttr_herdan == numpy.log(num_types) / numpy.log(num_tokens)
    assert logttr_somers == numpy.log(numpy.log(num_types)) / numpy.log(numpy.log(num_tokens))
    assert logttr_rubet == numpy.log(num_types) / numpy.log(numpy.log(num_tokens))
    assert logttr_maas == (numpy.log(num_tokens) - numpy.log(num_types)) / (numpy.log(num_tokens) ** 2)
    assert logttr_dugast == (numpy.log(num_tokens) ** 2) / (numpy.log(num_tokens) - numpy.log(num_types))

def test_msttr():
    msttr_100 = wl_measures_lexical_diversity.msttr(main, TOKENS_101)
    settings['msttr']['num_tokens_in_each_seg'] = 1000
    msttr_1000 = wl_measures_lexical_diversity.msttr(main, TOKENS_101)

    assert msttr_100 == 5 / 100
    assert msttr_1000 == 0

def test_mtld():
    mtld_100 = wl_measures_lexical_diversity.mtld(main, TOKENS_100)

    assert mtld_100 == 100 / (14 + 0 / 0.28)

def test_mattr():
    mattr_100 = wl_measures_lexical_diversity.mattr(main, TOKENS_100)
    mattr_1000 = wl_measures_lexical_diversity.mattr(main, TOKENS_1000)

    assert mattr_100 == wl_measures_lexical_diversity.ttr(main, TOKENS_100)
    assert mattr_1000 == 5 / 500

def test_rttr():
    rttr = wl_measures_lexical_diversity.rttr(main, TOKENS_100)

    assert rttr == 5 / 100 ** 0.5

def test_simpsons_l():
    l = wl_measures_lexical_diversity.simpsons_l(main, TOKENS_100)

    assert l == (5 * 20 ** 2 - 100) / (100 * (100 - 1))

def test_ttr():
    ttr = wl_measures_lexical_diversity.ttr(main, TOKENS_100)

    assert ttr == 5 / 100

def test_vocdd():
    vocdd_10 = wl_measures_lexical_diversity.vocdd(main, TOKENS_10)
    vocdd_100 = wl_measures_lexical_diversity.vocdd(main, TOKENS_100)
    vocdd_1000 = wl_measures_lexical_diversity.vocdd(main, TOKENS_1000)

    assert vocdd_10 > 0
    assert vocdd_100 > 0
    assert vocdd_1000 > 0

def test_yules_characteristic_k():
    k = wl_measures_lexical_diversity.yules_characteristic_k(main, TOKENS_100)

    assert k == 10000 * ((5 * 20 ** 2 - 100) / (100 ** 2))

def test_yules_index_of_diversity():
    index_of_diversity = wl_measures_lexical_diversity.yules_index_of_diversity(main, TOKENS_100)

    assert index_of_diversity == (100 ** 2) / (5 * 20 ** 2 - 100)

if __name__ == '__main__':
    test_cttr()
    test_fishers_index_of_diversity()
    test_herdans_vm()
    test_hdd()
    test_logttr()
    test_msttr()
    test_mtld()
    test_mattr()
    test_rttr()
    test_ttr()
    test_simpsons_l()
    test_vocdd()
    test_yules_characteristic_k()
    test_yules_index_of_diversity()
