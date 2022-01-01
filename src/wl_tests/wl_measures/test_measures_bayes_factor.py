#
# Wordless: Tests - Measures - Bayes Factor
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wl_tests import wl_test_init
from wl_measures import wl_measures_bayes_factor

main = wl_test_init.Wl_Test_Main()

# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang. (p. 7)
def test_bayes_factor_log_likelihood_ratio_test():
    assert round(wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(22.22, 9611 + 144925), 2) == 10.27
