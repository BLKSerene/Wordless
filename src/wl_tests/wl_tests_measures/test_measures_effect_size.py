# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Effect Size
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
from wl_measures import wl_measures_effect_size

main = wl_test_init.Wl_Test_Main()
main.settings_custom['measures']['effect_size'] = {
    'kilgarriffs_ratio': {
        'smoothing_param': 1.00,
    }
}

# Reference: Gabrielatos, C., & Marchi, A. (2012, September 13–14). Keyness: Appropriate metrics and practical issues [Conference session]. CADS International Conference 2012, University of Bologna, Italy. (pp. 21-22)
def test_pct_diff():
    assert round(wl_measures_effect_size.pct_diff(main, 20, 1, 29954 - 20, 23691 - 1), 2) == 1481.83

# Reference: Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. Computational Linguistics, 22(1), pp. 1–38. (p. 13)
def test_dices_coeff():
    assert round(wl_measures_effect_size.dices_coeff(main, 130, 3121 - 130, 143 - 130, -1), 2) == 0.08

# Reference: Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities. (p. 471)
def test_diff_coeff():
    assert round(wl_measures_effect_size.diff_coeff(main, 18, 35, 1000000 - 18, 1000000 - 35), 2) == -0.32

# Reference: Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), Proceedings of the Corpus Linguistics Conference 2009 (p. 171). University of Liverpool.
def test_kilgarriffs_ratio():
    assert round(wl_measures_effect_size.kilgarriffs_ratio(main, 35, 263, 112289776, 1559716979), 4) == 1.1224

# Reference: Hardie, A. (2014, April 28). Log ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.
def test_log_ratio():
    assert wl_measures_effect_size.log_ratio(main, 1, 1, 1000000 - 1, 1000000 - 1) == 0

# Reference: Pedersen, T. (1998). Dependent bigram identification. In Proceedings of the Fifteenth National Conference on Artificial Intelligence (p. 1197). AAAI Press.
def test_min_sensitivity():
    assert round(wl_measures_effect_size.min_sensitivity(main, 17, 240, 1001, 1298742), 3) == 0.017

# Reference: Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. Corpus Linguistics and Lingustic Theory, 15(1), pp. 133–167. https://doi.org/10.1515/cllt-2015-0030 (p. 154)
def test_odds_ratio():
    assert round(wl_measures_effect_size.odds_ratio(main, 16217, 735, 2796938 - 16217, 2087946 - 735), 1) == 16.6

# Reference: Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. Computational Linguistics, 16(1), 22–29. (p. 24)
def test_pmi():
    assert round(wl_measures_effect_size.pmi(main, 8, 1105 - 8, 44 - 8, 15000000 - 1105 - 44 + 8), 1) == 11.3

# Reference: Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.
def test_squared_phi_coeff():
    assert round(wl_measures_effect_size.squared_phi_coeff(main, 31950, 12004, 4793, 848330), 2) == 0.62
