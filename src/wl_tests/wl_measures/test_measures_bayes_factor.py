#
# Wordless: Tests - Measures - Bayes Factor
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
from wl_measures import wl_measures_bayes_factor

main = wl_test_init.Wl_Test_Main()

# Wilson, Andrew. "Embracing Bayes Factors for Key Item Analysis in Corpus Linguistics." New Approaches to the Study of Linguistic Variability, edited by Markus Bieswanger and Amei Koll-Stobbe, Peter Lang, 2013, p. 7.
def test_bayes_factor_log_likelihood_ratio_test():
    assert round(wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(22.22, 9611 + 144925), 2) == 10.27
