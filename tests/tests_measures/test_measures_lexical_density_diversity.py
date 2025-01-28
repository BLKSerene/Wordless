# ----------------------------------------------------------------------
# Tests: Measures - Lexical density/diversity
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

import numpy
import scipy

from tests import wl_test_init
from wordless.wl_measures import wl_measures_lexical_density_diversity

main = wl_test_init.Wl_Test_Main()
settings = main.settings_custom['measures']['lexical_density_diversity']

TOKENS_10 = ['This', 'is', 'a', 'sentence', '.'] * 2
TOKENS_100 = ['This', 'is', 'a', 'sentence', '.'] * 20
TOKENS_101 = ['This', 'is', 'a', 'sentence', '.'] * 20 + ['another']
TOKENS_1000 = ['This', 'is', 'a', 'sentence', '.'] * 200

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 26
TOKENS_225 = [1] * 11 + [2, 3] * 9 + [4] * 7 + [5, 6] * 6 + [7, 8] * 5 + list(range(9, 16)) * 4 + list(range(16, 22)) * 3 + list(range(22, 40)) * 2 + list(range(40, 125))

def get_test_text(tokens):
    return wl_test_init.Wl_Test_Text(main, [[[tokens]]])

text_tokens_10 = get_test_text(TOKENS_10)
text_tokens_100 = get_test_text(TOKENS_100)
text_tokens_101 = get_test_text(TOKENS_101)
text_tokens_1000 = get_test_text(TOKENS_1000)
text_tokens_225 = get_test_text(TOKENS_225)

def test_brunets_index():
    w = wl_measures_lexical_density_diversity.brunets_index(main, text_tokens_100)

    assert w == numpy.power(100, numpy.power(5, -0.172))

def test_cttr():
    cttr = wl_measures_lexical_density_diversity.cttr(main, text_tokens_100)

    assert cttr == 5 / (2 * 100) ** 0.5

# Reference: Fisher, R. A., Steven, A. C., & Williams, C. B. (1943). The relation between the number of species and the number of individuals in a random sample of an animal population. Journal of Animal Ecology, 12(1), 56. https://doi.org/10.2307/1411
def test_fishers_index_of_diversity():
    tokens = [str(i) for i in range(240)] + ['0'] * (15609 - 240)
    alpha = wl_measures_lexical_density_diversity.fishers_index_of_diversity(main, get_test_text(tokens))

    assert round(alpha, 3) == 40.247

def test_herdans_vm():
    vm = wl_measures_lexical_density_diversity.herdans_vm(main, text_tokens_100)

    assert vm == (5 * 20 ** 2) / (100 ** 2) - 1 / 5

def test_hdd():
    hdd_100 = wl_measures_lexical_density_diversity.hdd(main, text_tokens_100)

    assert hdd_100 == (1 - scipy.stats.hypergeom.pmf(k = 0, M = 100, n = 20, N = 42)) * (1 / 42) * 5

def test_honores_stat():
    r = wl_measures_lexical_density_diversity.honores_stat(main, text_tokens_100)

    assert r == 100 * numpy.log(100 / (1 - 0 / 5))

def test_lexical_density():
    lexical_density = wl_measures_lexical_density_diversity.lexical_density(main, text_tokens_100)

    assert lexical_density == 20 / 100

def test_logttr():
    settings['logttr']['variant'] = 'Herdan'
    logttr_herdan = wl_measures_lexical_density_diversity.logttr(main, text_tokens_100)
    settings['logttr']['variant'] = 'Somers'
    logttr_somers = wl_measures_lexical_density_diversity.logttr(main, text_tokens_100)
    settings['logttr']['variant'] = 'Rubet'
    logttr_rubet = wl_measures_lexical_density_diversity.logttr(main, text_tokens_100)
    settings['logttr']['variant'] = 'Maas'
    logttr_maas = wl_measures_lexical_density_diversity.logttr(main, text_tokens_100)
    settings['logttr']['variant'] = 'Dugast'
    logttr_dugast = wl_measures_lexical_density_diversity.logttr(main, text_tokens_100)

    num_types = 5
    num_tokens = 100

    assert logttr_herdan == numpy.log(num_types) / numpy.log(num_tokens)
    assert logttr_somers == numpy.log(numpy.log(num_types)) / numpy.log(numpy.log(num_tokens))
    assert logttr_rubet == numpy.log(num_types) / numpy.log(numpy.log(num_tokens))
    assert logttr_maas == (numpy.log(num_tokens) - numpy.log(num_types)) / (numpy.log(num_tokens) ** 2)
    assert logttr_dugast == (numpy.log(num_tokens) ** 2) / (numpy.log(num_tokens) - numpy.log(num_types))

def test_msttr():
    msttr_100 = wl_measures_lexical_density_diversity.msttr(main, text_tokens_101)
    settings['msttr']['num_tokens_in_each_seg'] = 1000
    msttr_1000 = wl_measures_lexical_density_diversity.msttr(main, text_tokens_101)

    assert msttr_100 == 5 / 100
    assert msttr_1000 == 0

def test_mtld():
    mtld_100 = wl_measures_lexical_density_diversity.mtld(main, text_tokens_100)

    assert mtld_100 == 100 / (14 + 0 / 0.28)

def test_mattr():
    mattr_100 = wl_measures_lexical_density_diversity.mattr(main, text_tokens_100)
    mattr_1000 = wl_measures_lexical_density_diversity.mattr(main, text_tokens_1000)

    assert mattr_100 == wl_measures_lexical_density_diversity.ttr(main, text_tokens_100)
    assert mattr_1000 == 5 / 500

# Reference: Popescu I.-I., Mačutek, J, & Altmann, G. (2008). Word frequency and arc length. Glottometrics, 17, 21, 33.
def test_popescu_macutek_altmanns_b1_b2_b3_b4_b5():
    b1, b2, b3, b4, b5 = wl_measures_lexical_density_diversity.popescu_macutek_altmanns_b1_b2_b3_b4_b5(main, text_tokens_225)

    assert round(b1, 3) == 0.969
    assert round(b2, 3) == 0.527
    assert round(b3, 3) == 0.961
    assert round(b4, 3) == 0.078
    assert round(b5, 3) == 0.664

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 30
def test_popescus_r1():
    r1 = wl_measures_lexical_density_diversity.popescus_r1(main, text_tokens_225)

    assert round(r1, 4) == 0.8667

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 39
def test_popescus_r2():
    r2 = wl_measures_lexical_density_diversity.popescus_r2(main, text_tokens_225)

    assert round(r2, 3) == 0.871

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 51
def test_popescus_r3():
    r3 = wl_measures_lexical_density_diversity.popescus_r3(main, text_tokens_225)

    assert round(r3, 4) == 0.3778

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 59
def test_popescus_r4():
    r4 = wl_measures_lexical_density_diversity.popescus_r4(main, text_tokens_225)

    assert round(r4, 4) == 0.6344

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | pp. 170, 172
def test_repeat_rate():
    settings['repeat_rate']['use_data'] = 'Rank-frequency distribution'
    rr_distribution = wl_measures_lexical_density_diversity.repeat_rate(main, text_tokens_225)
    settings['repeat_rate']['use_data'] = 'Frequency spectrum'
    rr_spectrum = wl_measures_lexical_density_diversity.repeat_rate(main, text_tokens_225)

    assert round(rr_distribution, 4) == 0.0153
    assert round(rr_spectrum, 4) == 0.4974

def test_rttr():
    rttr = wl_measures_lexical_density_diversity.rttr(main, text_tokens_100)

    assert rttr == 5 / 100 ** 0.5

# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | pp. 176, 178
def test_shannon_entropy():
    settings['shannon_entropy']['use_data'] = 'Rank-frequency distribution'
    h_distribution = wl_measures_lexical_density_diversity.shannon_entropy(main, text_tokens_225)
    settings['shannon_entropy']['use_data'] = 'Frequency spectrum'
    h_spectrum = wl_measures_lexical_density_diversity.shannon_entropy(main, text_tokens_225)

    assert round(h_distribution, 4) == 6.5270
    assert round(h_spectrum, 4) == 1.6234

def test_simpsons_l():
    l = wl_measures_lexical_density_diversity.simpsons_l(main, text_tokens_100)

    assert l == (5 * 20 ** 2 - 100) / (100 * (100 - 1))

def test_ttr():
    ttr = wl_measures_lexical_density_diversity.ttr(main, text_tokens_100)

    assert ttr == 5 / 100

def test_vocdd():
    vocdd_10 = wl_measures_lexical_density_diversity.vocdd(main, text_tokens_10)
    vocdd_100 = wl_measures_lexical_density_diversity.vocdd(main, text_tokens_100)
    vocdd_1000 = wl_measures_lexical_density_diversity.vocdd(main, text_tokens_1000)

    assert vocdd_10 > 0
    assert vocdd_100 > 0
    assert vocdd_1000 > 0

def test_yules_characteristic_k():
    k = wl_measures_lexical_density_diversity.yules_characteristic_k(main, text_tokens_100)

    assert k == 10000 * ((5 * 20 ** 2 - 100) / (100 ** 2))

def test_yules_index_of_diversity():
    index_of_diversity = wl_measures_lexical_density_diversity.yules_index_of_diversity(main, text_tokens_100)

    assert index_of_diversity == (100 ** 2) / (5 * 20 ** 2 - 100)

if __name__ == '__main__':
    test_brunets_index()
    test_cttr()
    test_fishers_index_of_diversity()
    test_herdans_vm()
    test_hdd()
    test_honores_stat()
    test_lexical_density()
    test_logttr()
    test_msttr()
    test_mtld()
    test_mattr()
    test_popescu_macutek_altmanns_b1_b2_b3_b4_b5()
    test_popescus_r1()
    test_popescus_r2()
    test_popescus_r3()
    test_popescus_r4()
    test_repeat_rate()
    test_rttr()
    test_shannon_entropy()
    test_simpsons_l()
    test_ttr()
    test_vocdd()
    test_yules_characteristic_k()
    test_yules_index_of_diversity()
