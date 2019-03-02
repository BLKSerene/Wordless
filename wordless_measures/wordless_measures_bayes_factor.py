#
# Wordless: Measures - Bayes Factor
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

# Reference:
#     Wilson, Andrew. "Embracing Bayes Factors for Key Item Analysis in Corpus Linguistics." New Approaches to the Study of Linguistic Variability, edited by Markus Bieswanger and Amei Koll-Stobbe, Peter Lang, 2013, pp. 3-11.
def bayes_factor_t_test(t_statistic, number_sections):
    return t_statistic ** 2 - math.log(number_sections, math.e)

def bayes_factor_log_likelihood_ratio_test(log_likelihood_ratio, number_tokens):
    return log_likelihood_ratio - math.log(number_tokens, math.e)

# Testing
if __name__ == '__main__':
    # Wilson, Andrew. "Embracing Bayes Factors for Key Item Analysis in Corpus Linguistics." New Approaches to the Study of Linguistic Variability, edited by Markus Bieswanger and Amei Koll-Stobbe, Peter Lang, 2013, p. 7.
    print('Bayes Factor (Log-likelihood Ratio Test):\n    ', end = '')
    print(bayes_factor_log_likelihood_ratio_test(22.22, 9611 + 144925)) # 10.27
