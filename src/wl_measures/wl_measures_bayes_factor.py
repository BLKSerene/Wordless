#
# Wordless: Measures - Bayes Factor
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

# Log-likelihood Ratio
# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang.
def bayes_factor_t_test(t_statistic, number_sections):
    return t_statistic ** 2 - math.log(number_sections, math.e)

# Student's t-test (2-sample)
# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang.
def bayes_factor_log_likelihood_ratio_test(log_likelihood_ratio, number_tokens):
    return log_likelihood_ratio - math.log(number_tokens, math.e)
