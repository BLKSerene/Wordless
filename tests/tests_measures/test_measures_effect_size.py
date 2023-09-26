# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Effect size
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

from tests import wl_test_init
from wordless.wl_measures import wl_measures_effect_size

main = wl_test_init.Wl_Test_Main()

def assert_zeros(func, result = 0):
    numpy.testing.assert_array_equal(
        func(
            main,
            numpy.array([0] * 10),
            numpy.array([0] * 10),
            numpy.array([0] * 10),
            numpy.array([0] * 10)
        ),
        numpy.array([result] * 10)
    )

# Reference: Gabrielatos, C., & Marchi, A. (2012, September 13–14). Keyness: Appropriate metrics and practical issues [Conference session]. CADS International Conference 2012, University of Bologna, Italy. (pp. 21-22)
def test_pct_diff():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.pct_diff(
            main,
            numpy.array([20] * 2),
            numpy.array([1] * 2),
            numpy.array([29954 - 20] * 2),
            numpy.array([23691 - 1] * 2)
        ), 2),
        numpy.array([1481.83] * 2)
    )

    numpy.testing.assert_array_equal(
        wl_measures_effect_size.pct_diff(
            main,
            numpy.array([0, 1, 0]),
            numpy.array([1, 0, 0]),
            numpy.array([0, 0, 0]),
            numpy.array([1, 1, 0])
        ),
        numpy.array([float('-inf'), float('inf'), 0])
    )

def test_im3():
    assert_zeros(wl_measures_effect_size.im3)

# Reference: Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. Computational Linguistics, 22(1), pp. 1–38. (p. 13)
def test_dices_coeff():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.dices_coeff(
            main,
            numpy.array([130] * 2),
            numpy.array([3121 - 130] * 2),
            numpy.array([143 - 130] * 2),
            numpy.array([-1] * 2)
        ), 2),
        numpy.array([0.08] * 2)
    )

    assert_zeros(wl_measures_effect_size.dices_coeff)

# Reference: Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities. (p. 471)
def test_diff_coeff():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.diff_coeff(
            main,
            numpy.array([18] * 2),
            numpy.array([35] * 2),
            numpy.array([1000000 - 18] * 2),
            numpy.array([1000000 - 35] * 2)
        ), 2),
        numpy.array([-0.32] * 2)
    )

    assert_zeros(wl_measures_effect_size.diff_coeff)

def test_jaccard_index():
    assert_zeros(wl_measures_effect_size.jaccard_index)

# Reference: Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), Proceedings of the Corpus Linguistics Conference 2009 (p. 171). University of Liverpool.
def test_kilgarriffs_ratio():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.kilgarriffs_ratio(
            main,
            numpy.array([35] * 2),
            numpy.array([263] * 2),
            numpy.array([112289776] * 2),
            numpy.array([1559716979] * 2)
        ), 4),
        numpy.array([1.1224] * 2)
    )

    assert_zeros(wl_measures_effect_size.kilgarriffs_ratio, result = 1)

# Reference: Hardie, A. (2014, April 28). Log ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.
def test_log_ratio():
    numpy.testing.assert_array_equal(
        wl_measures_effect_size.log_ratio(
            main,
            numpy.array([1] * 2),
            numpy.array([1] * 2),
            numpy.array([1000000 - 1] * 2),
            numpy.array([1000000 - 1] * 2)
        ),
        numpy.array([0] * 2)
    )

    numpy.testing.assert_array_equal(
        wl_measures_effect_size.log_ratio(
            main,
            numpy.array([0, 1, 0]),
            numpy.array([1, 0, 0]),
            numpy.array([0, 0, 0]),
            numpy.array([1, 1, 0])
        ),
        numpy.array([float('-inf'), float('inf'), 0])
    )

def test_lfmd():
    assert_zeros(wl_measures_effect_size.lfmd)

def test_log_dice():
    assert_zeros(wl_measures_effect_size.log_dice, result = 14)

def test_mi_log_f():
    assert_zeros(wl_measures_effect_size.mi_log_f)

# Reference: Pedersen, T. (1998). Dependent bigram identification. In Proceedings of the Fifteenth National Conference on Artificial Intelligence (p. 1197). AAAI Press.
def test_min_sensitivity():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.min_sensitivity(
            main,
            numpy.array([17] * 2),
            numpy.array([240] * 2),
            numpy.array([1001] * 2),
            numpy.array([1298742] * 2)
        ), 3),
        numpy.array([0.017] * 2)
    )

    assert_zeros(wl_measures_effect_size.min_sensitivity)

def test_md():
    assert_zeros(wl_measures_effect_size.md)

def test_me():
    assert_zeros(wl_measures_effect_size.me)

def test_mi():
    assert_zeros(wl_measures_effect_size.mi)

# Reference: Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. Corpus Linguistics and Linguistic Theory, 15(1), pp. 133–167. https://doi.org/10.1515/cllt-2015-0030 (p. 154)
def test_odds_ratio():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.odds_ratio(
            main,
            numpy.array([16217] * 2, dtype = float),
            numpy.array([735] * 2, dtype = float),
            numpy.array([2796938 - 16217] * 2, dtype = float),
            numpy.array([2087946 - 735] * 2, dtype = float)
        ), 1),
        numpy.array([16.6] * 2)
    )

    numpy.testing.assert_array_equal(
        wl_measures_effect_size.odds_ratio(
            main,
            numpy.array([0, 1, 0]),
            numpy.array([1, 0, 0]),
            numpy.array([0, 0, 0]),
            numpy.array([1, 1, 0])
        ),
        numpy.array([float('-inf'), float('inf'), 0])
    )

# Reference: Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. Computational Linguistics, 16(1), 22–29. (p. 24)
def test_pmi():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.pmi(
            main,
            numpy.array([8] * 2),
            numpy.array([1105 - 8] * 2),
            numpy.array([44 - 8] * 2),
            numpy.array([15000000 - 1105 - 44 + 8] * 2)
        ), 1),
        numpy.array([11.3] * 2)
    )

    assert_zeros(wl_measures_effect_size.pmi)

def test_poisson_collocation_measure():
    assert_zeros(wl_measures_effect_size.poisson_collocation_measure)

# Reference: Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.
def test_squared_phi_coeff():
    numpy.testing.assert_array_equal(
        numpy.round(wl_measures_effect_size.squared_phi_coeff(
            main,
            numpy.array([31950] * 2, dtype = float),
            numpy.array([12004] * 2, dtype = float),
            numpy.array([4793] * 2, dtype = float),
            numpy.array([848330] * 2, dtype = float)
        ), 2),
        numpy.array([0.62] * 2)
    )

    assert_zeros(wl_measures_effect_size.squared_phi_coeff)

if __name__ == '__main__':
    test_pct_diff()
    test_im3()
    test_dices_coeff()
    test_diff_coeff()
    test_jaccard_index()
    test_kilgarriffs_ratio()
    test_log_ratio()
    test_lfmd()
    test_log_dice()
    test_mi_log_f()
    test_min_sensitivity()
    test_md()
    test_me()
    test_mi()
    test_odds_ratio()
    test_pmi()
    test_poisson_collocation_measure()
    test_squared_phi_coeff()
