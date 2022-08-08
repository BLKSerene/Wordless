# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Statistical Significance
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

from wl_measures import wl_measures_statistical_significance
from wl_tests import wl_test_init

main = wl_test_init.Wl_Test_Main()

def test_get_freqs_marginal():
    assert wl_measures_statistical_significance.get_freqs_marginal(1, 2, 3, 4) == (3, 7, 4, 6)
    assert wl_measures_statistical_significance.get_freqs_marginal(0, 0, 1, 2) == (0, 3, 1, 2)
    assert wl_measures_statistical_significance.get_freqs_marginal(0, 0, 0, 0) == (0, 0, 0, 0)

def test_get_freqs_expected():
    assert wl_measures_statistical_significance.get_freqs_expected(1, 2, 3, 4) == (1.2, 1.8, 2.8, 4.2)
    assert wl_measures_statistical_significance.get_freqs_expected(0, 0, 1, 2) == (0, 0, 1, 2)
    assert wl_measures_statistical_significance.get_freqs_expected(0, 0, 0, 0) == (0, 0, 0, 0)

def test_to_freqs_sections_tokens():
    tokens = ['w1', 'w2']
    tokens_x1 = ['w1'] * 7 + ['w2'] * 3
    tokens_x2 = ['w1'] * 6 + ['w2'] * 4

    freqs_sections_tokens = {
        'w1': ([1, 1, 1, .5, 0], [1, 1, 1, 0, 0]),
        'w2': ([0, 0, 0, .5, 1], [0, 0, 0, 1, 1])
    }

    assert wl_measures_statistical_significance.to_freqs_sections_tokens(main, tokens, tokens_x1, tokens_x2, test_statistical_significance = 'Mann-Whitney U Test') == freqs_sections_tokens
    assert wl_measures_statistical_significance.to_freqs_sections_tokens(main, tokens, tokens_x1, tokens_x2, test_statistical_significance = "Student's t-test (2-sample)") == freqs_sections_tokens
    assert wl_measures_statistical_significance.to_freqs_sections_tokens(main, tokens, tokens_x1, tokens_x2, test_statistical_significance = "Welch's t-test") == freqs_sections_tokens

# References: Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188-200). The South–Central Regional SAS Users' Group. (p. 10)
def test_fishers_exact_test():
    # Two-tailed
    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Two-tailed'

    assert round(wl_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1], 3) == 0.486

    # Left-tailed
    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Left-tailed'

    assert round(wl_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1], 3) == 0.243

    # Right-tailed
    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Right-tailed'

    assert round(wl_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1], 3) == 0.986

    assert wl_measures_statistical_significance.fishers_exact_test(main, 0, 0, 0, 0)[1] == 1

# References: Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74. (p. 72)
def test_log_likelihood_ratio_test():
    main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test']['apply_correction'] = False

    assert round(wl_measures_statistical_significance.log_likelihood_ratio_test(main, 10, 0, 3, 31764)[0], 2) == 167.23

    assert wl_measures_statistical_significance.log_likelihood_ratio_test(main, 1, 1, 1, 1) == (0, 1)
    assert wl_measures_statistical_significance.log_likelihood_ratio_test(main, 0, 0, 0, 0) == (0, 1)

# References: Kilgarriff, A. (2001). Comparing corpora. International Journal of Corpus Linguistics, 6(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil (p. 238)
def test_mann_whitney_u_test():
    u1 = wl_measures_statistical_significance.mann_whitney_u_test(
        main,
        [12, 15, 18, 24, 88],
        [3, 3, 13, 27, 33]
    )[0]

    assert 5 * (5 + 1) / 2 + u1 == 31

    assert wl_measures_statistical_significance.mann_whitney_u_test(main, [0] * 5, [0] * 5) == (12.5, 1)

# References:
#     Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74. (p. 73)
#     Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188-200). The South–Central Regional SAS Users' Group. (p. 10)
def test_pearsons_chi_squared_test():
    main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = False

    assert round(wl_measures_statistical_significance.pearsons_chi_squared_test(main, 3, 0, 0, 31774)[0], 0) == 31777

    # With Yates's correction for continuity
    main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = True

    assert wl_measures_statistical_significance.pearsons_chi_squared_test(main, 1, 3, 3, 1)[0] == 0.5
    assert round(wl_measures_statistical_significance.pearsons_chi_squared_test(main, 1, 3, 3, 1)[1], 2) == 0.48

    assert wl_measures_statistical_significance.pearsons_chi_squared_test(main, 0, 0, 0, 0) == (0, 1)

# Manning, C. D., & Schütze, H. (1999). Foundations of statistical natural language processing. MIT Press. (pp. 164-165)
def test_students_t_test_1_sample():
    assert round(wl_measures_statistical_significance.students_t_test_1_sample(main, 8, 15828 - 8, 4675 - 8, 14307668 - 15828 - 4675 + 8)[0], 6) == 0.999932

    assert wl_measures_statistical_significance.students_t_test_1_sample(main, 0, 1, 1, 2) == (0, 1)
    assert wl_measures_statistical_significance.students_t_test_1_sample(main, 0, 0, 0, 0) == (0, 1)

def test_students_t_test_2_sample():
    assert wl_measures_statistical_significance.students_t_test_2_sample(main, [0] * 5, [0] * 5) == (0, 1)

def test_welchs_t_test():
    assert wl_measures_statistical_significance.welchs_t_test(main, [0] * 5, [0] * 5) == (0, 1)

def test_z_score():
    assert wl_measures_statistical_significance.z_score(main, 0, 0, 0, 0) == (0, 1)

def test_z_score_berry_rogghe():
    assert wl_measures_statistical_significance.z_score_berry_rogghe(main, 0, 0, 0, 0, 5) == (0, 1)

if __name__ == '__main__':
    test_get_freqs_marginal()
    test_get_freqs_expected()
    test_to_freqs_sections_tokens()

    test_fishers_exact_test()
    test_log_likelihood_ratio_test()
    test_mann_whitney_u_test()
    test_pearsons_chi_squared_test()
    test_students_t_test_1_sample()
    test_students_t_test_2_sample()
    test_z_score()
    test_z_score_berry_rogghe()
