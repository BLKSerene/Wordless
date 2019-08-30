#
# Wordless: Tests - Measures - Statistical Significance
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wordless_tests import test_init
from wordless_measures import wordless_measures_statistical_significance

main = test_init.Test_Main()
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

# Manning, Christopher D. and Hinrich Schütze. Foundations of Statistical Natural Language Processing. MIT Press, May 1999, pp. 164-165.
def test_students_t_test_1_sample():
    assert round(wordless_measures_statistical_significance.students_t_test_1_sample(main, 8, 15828 - 8, 4675 - 8, 14307668 - 15828 - 4675 + 8)[0], 6) == 0.999932

# Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, p. 73.
# Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin, p. 10.
def test_pearsons_chi_squared_test():
    main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = False 

    assert round(wordless_measures_statistical_significance.pearsons_chi_squared_test(main, 3, 0, 0, 31774)[0], 0) == 31777

    # With Yates's correction for continuity
    main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = True

    assert wordless_measures_statistical_significance.pearsons_chi_squared_test(main, 1, 3, 3, 1)[0] == 0.5
    assert round(wordless_measures_statistical_significance.pearsons_chi_squared_test(main, 1, 3, 3, 1)[1], 2) == 0.48

# Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, p. 72.
def test_log_likehood_ratio_test():
    assert round(wordless_measures_statistical_significance.log_likehood_ratio_test(main, 10, 0, 3, 31764)[0], 2) == 167.23

# Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin, p. 10.
def test_fishers_exact_test():
    # Two-tailed
    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Two-tailed'

    assert round(wordless_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1], 3) == 0.486

    # Left-tailed
    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Left-tailed'

    assert round(wordless_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1], 3) == 0.243

    # Right-tailed
    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Right-tailed'

    assert round(wordless_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1], 3) == 0.986

# Kilgarriff, Adam. "Comparing Corpora." International Journal of Corpus Linguistics, vol.6, no.1, Nov. 2001, p. 238.
def test_mann_whitney_u_test():
    u_stat = wordless_measures_statistical_significance.mann_whitney_u_test(main,
                                                                            [12, 15, 18, 24, 88],
                                                                            [3, 3, 13, 27, 33])[0]

    assert 5 * (5 + 1) / 2 + u_stat == 24
