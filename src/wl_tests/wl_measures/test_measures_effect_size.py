#
# Wordless: Tests - Measures - Effect Size
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wl_tests import wl_test_init
from wl_measures import wl_measures_effect_size

main = wl_test_init.Wl_Test_Main()
main.settings_custom['measures']['effect_size'] = {
    'kilgarriffs_ratio': {
        'smoothing_param': 1.00,
    }
}

# Church, Kenneth Ward, and Patrick Hanks. Word Association Norms, Mutual Information, and Lexicography. Computational Linguistics, vol. 16, no. 1, Mar. 1990, p. 24.
def test_pmi():
    assert round(wl_measures_effect_size.pmi(main, 8, 1105 - 8, 44 - 8, 15000000 - 1105 - 44 + 8), 1) == 11.3

# Church, Kenneth Ward, and William A. Gale. "Concordances for Parallel Text." Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, 29 Sept - 1 Oct 1991, UW Centre for the New OED and Text Research, 1991.
def test_squared_phi_coeff():
    assert round(wl_measures_effect_size.squared_phi_coeff(main, 31950, 12004, 4793, 848330), 2) == 0.62

# Smadja, Frank, et al. "Translating Collocations for Bilingual Lexicons: A Statistical Approach." Computational Linguistics, vol. 22, no. 1, 1996, p. 13.
def test_dices_coeff():
    assert round(wl_measures_effect_size.dices_coeff(main, 130, 3121 - 130, 143 - 130, -1), 2) == 0.08

# Pedersen, Ted. "Dependent Bigram Identification." Proceedings of the Fifteenth National Conference on Artificial Intelligence, Madison, 26-30 July 1998, American Association for Artificial Intelligence, 1998, p. 1197.
def test_min_sensitivity():
    assert round(wl_measures_effect_size.min_sensitivity(main, 17, 240, 1001, 1298742), 3) == 0.017

# "Simple maths." Sketch Engine, www.sketchengine.eu/documentation/simple-maths/. Accessed 26 Nov 2018.
def test_kilgarriffs_ratio():
    assert round(wl_measures_effect_size.kilgarriffs_ratio(main, 35, 263, 112289776, 1559716979), 4) == 1.1224

# Pojanapunya, Punjaporn, and Richard Watson Todd. "Log-likelihood and Odds Ratio Keyness Statistics for Different Purposes of Keyword Analysis." Corpus Linguistics and Lingustic Theory, vol. 15, no. 1, Jan. 2016, p 154.
def test_odds_ratio():
    assert round(wl_measures_effect_size.odds_ratio(main, 16217, 735, 2796938 - 16217, 2087946 - 735), 1) == 16.6

# Hardie, Andrew. “Log Ratio: An Informal Introduction.” The Centre for Corpus Approaches to Social Science, 28 Apr. 2014, http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.
def test_log_ratio():
    assert wl_measures_effect_size.log_ratio(main, 1, 1, 1000000 - 1, 1000000 - 1) == 0

# Hofland, Knut, and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982, p. 471.
def test_diff_coeff():
    assert round(wl_measures_effect_size.diff_coeff(main, 18, 35, 1000000 - 18, 1000000 - 35), 2) == -0.32

# Gabrielatos, Costas. "Keyness Analysis: Nature, Metrics and Techniques." Corpus Approaches to Discourse: A Critical Review, edited by Taylor, Charlotte and Anna Marchi, Routledge, 2018, pp. 21-22.
def test_pct_diff():
    assert round(wl_measures_effect_size.pct_diff(main, 20, 1, 29954 - 20, 23691 - 1), 2) == 1481.83
