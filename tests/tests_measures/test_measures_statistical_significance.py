# ----------------------------------------------------------------------
# Tests: Measures - Statistical significance
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

from tests import wl_test_init
from wordless.wl_measures import wl_measures_statistical_significance

main = wl_test_init.Wl_Test_Main()
settings = main.settings_custom['measures']['statistical_significance']

def test_get_freqs_marginal():
    numpy.testing.assert_array_equal(wl_measures_statistical_significance.get_freqs_marginal(
        numpy.array([1, 0, 0]),
        numpy.array([2, 0, 0]),
        numpy.array([3, 1, 0]),
        numpy.array([4, 2, 0])
    ), (
        numpy.array([3, 0, 0]),
        numpy.array([7, 3, 0]),
        numpy.array([4, 1, 0]),
        numpy.array([6, 2, 0])
    ))

def test_get_freqs_expected():
    numpy.testing.assert_array_equal(wl_measures_statistical_significance.get_freqs_expected(
        numpy.array([1, 0, 0]),
        numpy.array([2, 0, 0]),
        numpy.array([3, 1, 0]),
        numpy.array([4, 2, 0])
    ), (
        numpy.array([1.2, 0, 0]),
        numpy.array([1.8, 0, 0]),
        numpy.array([2.8, 1, 0]),
        numpy.array([4.2, 2, 0])
    ))

def test_get_alt():
    assert wl_measures_statistical_significance.get_alt('Two-tailed') == 'two-sided'
    assert wl_measures_statistical_significance.get_alt('Left-tailed') == 'less'
    assert wl_measures_statistical_significance.get_alt('Right-tailed') == 'greater'

# References: Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188–200). The South–Central Regional SAS Users' Group. | p. 10
def test_fishers_exact_test():
    settings['fishers_exact_test']['direction'] = 'Two-tailed'
    test_stats, p_vals = wl_measures_statistical_significance.fishers_exact_test(
        main,
        numpy.array([1] * 2),
        numpy.array([3] * 2),
        numpy.array([3] * 2),
        numpy.array([1] * 2)
    )
    assert test_stats == [None] * 2
    numpy.testing.assert_array_equal(numpy.round(p_vals, 3), numpy.array([0.486] * 2))

    settings['fishers_exact_test']['direction'] = 'Left-tailed'
    test_stats, p_vals = wl_measures_statistical_significance.fishers_exact_test(
        main,
        numpy.array([1] * 2),
        numpy.array([3] * 2),
        numpy.array([3] * 2),
        numpy.array([1] * 2)
    )
    assert test_stats == [None] * 2
    numpy.testing.assert_array_equal(numpy.round(p_vals, 3), numpy.array([0.243] * 2))

    settings['fishers_exact_test']['direction'] = 'Right-tailed'
    test_stats, p_vals = wl_measures_statistical_significance.fishers_exact_test(
        main,
        numpy.array([1] * 2),
        numpy.array([3] * 2),
        numpy.array([3] * 2),
        numpy.array([1] * 2)
    )
    assert test_stats == [None] * 2
    numpy.testing.assert_array_equal(numpy.round(p_vals, 3), numpy.array([0.986] * 2))

    test_stats, p_vals = wl_measures_statistical_significance.fishers_exact_test(
        main,
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2)
    )
    assert test_stats == [None] * 2
    numpy.testing.assert_array_equal(p_vals, numpy.array([1] * 2))

# References: Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74. | p. 72
def test_log_likelihood_ratio_test():
    settings['log_likelihood_ratio_test']['apply_correction'] = False
    gs, _ = wl_measures_statistical_significance.log_likelihood_ratio_test(
        main,
        numpy.array([10] * 2),
        numpy.array([0] * 2),
        numpy.array([3] * 2),
        numpy.array([31764] * 2)
    )
    numpy.testing.assert_array_equal(numpy.round(gs, 2), numpy.array([167.23] * 2))

    main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test']['apply_correction'] = False
    gs, p_vals = wl_measures_statistical_significance.log_likelihood_ratio_test(
        main,
        numpy.array([1, 0]),
        numpy.array([1, 0]),
        numpy.array([1, 0]),
        numpy.array([1, 0])
    )
    numpy.testing.assert_array_equal(gs, numpy.array([0, 0]))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1, 1]))

    main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test']['apply_correction'] = True
    gs, p_vals = wl_measures_statistical_significance.log_likelihood_ratio_test(
        main,
        numpy.array([1, 0]),
        numpy.array([1, 0]),
        numpy.array([1, 0]),
        numpy.array([1, 0])
    )
    numpy.testing.assert_array_equal(gs, numpy.array([0, 0]))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1, 1]))

# References: Kilgarriff, A. (2001). Comparing corpora. International Journal of Corpus Linguistics, 6(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil | p. 238
def test_mann_whitney_u_test():
    u1s, _ = wl_measures_statistical_significance.mann_whitney_u_test(
        main,
        numpy.array([[12, 15, 18, 24, 88]] * 2),
        numpy.array([[3, 3, 13, 27, 33]] * 2)
    )

    numpy.testing.assert_array_equal(5 * (5 + 1) / 2 + u1s, numpy.array([31] * 2))

    main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['direction'] = 'Two-tailed'
    numpy.testing.assert_array_equal(
        wl_measures_statistical_significance.mann_whitney_u_test(
            main,
            numpy.array([[0] * 5] * 2),
            numpy.array([[0] * 5] * 2)
        ),
        (numpy.array([12.5] * 2), numpy.array([1] * 2))
    )

    main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['direction'] = 'Left-tailed'
    numpy.testing.assert_array_equal(
        wl_measures_statistical_significance.mann_whitney_u_test(
            main,
            numpy.array([[0] * 5] * 2),
            numpy.array([[0] * 5] * 2)
        ),
        (numpy.array([12.5] * 2), numpy.array([1] * 2))
    )

    main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['direction'] = 'Right-tailed'
    numpy.testing.assert_array_equal(
        wl_measures_statistical_significance.mann_whitney_u_test(
            main,
            numpy.array([[0] * 5] * 2),
            numpy.array([[0] * 5] * 2)
        ),
        (numpy.array([12.5] * 2), numpy.array([1] * 2))
    )

# References:
#     Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74. | p. 73
#     Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188–200). The South–Central Regional SAS Users' Group. | p. 10
def test_pearsons_chi_squared_test():
    settings['pearsons_chi_squared_test']['apply_correction'] = False
    chi2s, _ = wl_measures_statistical_significance.pearsons_chi_squared_test(
        main,
        numpy.array([3] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([31774] * 2)
    )
    numpy.testing.assert_array_equal(numpy.round(chi2s), numpy.array([31777] * 2))

    settings['pearsons_chi_squared_test']['apply_correction'] = True
    chi2s, p_vals = wl_measures_statistical_significance.pearsons_chi_squared_test(
        main,
        numpy.array([1] * 2),
        numpy.array([3] * 2),
        numpy.array([3] * 2),
        numpy.array([1] * 2)
    )
    numpy.testing.assert_array_equal(chi2s, numpy.array([0.5] * 2))
    numpy.testing.assert_array_equal(numpy.round(p_vals, 2), numpy.array([0.48] * 2))

    chi2s, p_vals = wl_measures_statistical_significance.pearsons_chi_squared_test(
        main,
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2)
    )
    numpy.testing.assert_array_equal(chi2s, numpy.array([0] * 2))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1] * 2))

# Manning, C. D., & Schütze, H. (1999). Foundations of statistical natural language processing. MIT Press. | pp. 164–165
def test_students_t_test_1_sample():
    t_stats, _ = wl_measures_statistical_significance.students_t_test_1_sample(
        main,
        numpy.array([8] * 2),
        numpy.array([15828 - 8] * 2),
        numpy.array([4675 - 8] * 2),
        numpy.array([14307668 - 15828 - 4675 + 8] * 2)
    )
    numpy.testing.assert_array_equal(numpy.round(t_stats, 6), numpy.array([0.999932] * 2))

    main.settings_custom['measures']['statistical_significance']['students_t_test_1_sample']['direction'] = 'Two-tailed'
    t_stats, p_vals = wl_measures_statistical_significance.students_t_test_1_sample(
        main,
        numpy.array([0, 0]),
        numpy.array([1, 1]),
        numpy.array([1, 1]),
        numpy.array([2, 1])
    )
    numpy.testing.assert_array_equal(t_stats, numpy.array([0, 0]))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1, 1]))

    main.settings_custom['measures']['statistical_significance']['students_t_test_1_sample']['direction'] = 'Left-tailed'
    t_stats, p_vals = wl_measures_statistical_significance.students_t_test_1_sample(
        main,
        numpy.array([0, 0]),
        numpy.array([1, 1]),
        numpy.array([1, 1]),
        numpy.array([2, 1])
    )
    numpy.testing.assert_array_equal(t_stats, numpy.array([0, 0]))
    numpy.testing.assert_array_equal(p_vals, numpy.array([0.5, 0.5]))

    main.settings_custom['measures']['statistical_significance']['students_t_test_1_sample']['direction'] = 'Right-tailed'
    t_stats, p_vals = wl_measures_statistical_significance.students_t_test_1_sample(
        main,
        numpy.array([0, 0]),
        numpy.array([1, 1]),
        numpy.array([1, 1]),
        numpy.array([2, 1])
    )
    numpy.testing.assert_array_equal(t_stats, numpy.array([0, 0]))
    numpy.testing.assert_array_equal(p_vals, numpy.array([0.5, 0.5]))

def test_students_t_test_2_sample():
    t_stats, p_vals = wl_measures_statistical_significance.students_t_test_2_sample(
        main,
        numpy.array([[0] * 5] * 2),
        numpy.array([[0] * 5] * 2)
    )

    numpy.testing.assert_array_equal(t_stats, numpy.array([0] * 2))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1] * 2))

def test__z_test_p_val():
    numpy.testing.assert_array_equal(
        wl_measures_statistical_significance._z_test_p_val(numpy.array([0] * 2), 'Two-tailed'),
        numpy.array([1] * 2)
    )
    numpy.testing.assert_array_equal(
        wl_measures_statistical_significance._z_test_p_val(numpy.array([0] * 2), 'Left-tailed'),
        numpy.array([0] * 2)
    )
    numpy.testing.assert_array_equal(
        wl_measures_statistical_significance._z_test_p_val(numpy.array([0] * 2), 'Right-tailed'),
        numpy.array([0] * 2)
    )

def test_z_test():
    z_scores, p_vals = wl_measures_statistical_significance.z_test(
        main,
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2)
    )

    numpy.testing.assert_array_equal(z_scores, numpy.array([0] * 2))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1] * 2))

def test_z_test_berry_rogghe():
    z_scores, p_vals = wl_measures_statistical_significance.z_test_berry_rogghe(
        main,
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        numpy.array([0] * 2),
        span = 5
    )

    numpy.testing.assert_array_equal(z_scores, numpy.array([0] * 2))
    numpy.testing.assert_array_equal(p_vals, numpy.array([1] * 2))

if __name__ == '__main__':
    test_get_freqs_marginal()
    test_get_freqs_expected()
    test_get_alt()

    test_fishers_exact_test()
    test_log_likelihood_ratio_test()
    test_mann_whitney_u_test()
    test_pearsons_chi_squared_test()
    test_students_t_test_1_sample()
    test_students_t_test_2_sample()

    test__z_test_p_val()
    test_z_test()
    test_z_test_berry_rogghe()
