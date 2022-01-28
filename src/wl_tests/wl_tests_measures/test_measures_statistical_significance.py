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

from wl_tests import wl_test_init
from wl_measures import wl_measures_statistical_significance

main = wl_test_init.Wl_Test_Main()
main.settings_custom['measures']['statistical_significance'] = {
    'students_t_test_2_sample': {
        'variances': 'Equal'
    },

    'pearsons_chi_squared_test': {},

    'fishers_exact_test': {},

    'mann_whitney_u_test': {
        'direction': 'Two-tailed',
        'apply_correction': True
    }
}

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

# References: Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74. (p. 72)
def test_log_likehood_ratio_test():
    assert round(wl_measures_statistical_significance.log_likehood_ratio_test(main, 10, 0, 3, 31764)[0], 2) == 167.23

# References: Kilgarriff, A. (2001). Comparing corpora. International Journal of Corpus Linguistics, 6(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil (p. 238)
def test_mann_whitney_u_test():
    u_stat = wl_measures_statistical_significance.mann_whitney_u_test(
        main,
        [12, 15, 18, 24, 88],
        [3, 3, 13, 27, 33]
    )[0]

    assert 5 * (5 + 1) / 2 + u_stat == 24

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

# Manning, C. D., & Schütze, H. (1999). Foundations of statistical natural language processing. MIT Press. (pp. 164-165)
def test_students_t_test_1_sample():
    assert round(wl_measures_statistical_significance.students_t_test_1_sample(main, 8, 15828 - 8, 4675 - 8, 14307668 - 15828 - 4675 + 8)[0], 6) == 0.999932
