#
# Wordless: Measures
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import math

import scipy.stats

def contingency_table_totals(c11, c12, c21, c22):
    c1x = c11 + c12
    c2x = c21 + c22
    cx1 = c11 + c21
    cx2 = c12 + c22
    cxx = c11 + c12 + c21 + c22

    return (c1x, c2x, cx1, cx2, cxx)

def contingency_table_expected(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    e11 = c1x * cx1 / cxx
    e12 = c1x * cx2 / cxx
    e21 = c2x * cx1 / cxx
    e22 = c2x * cx2 / cxx

    return (e11, e12, e21, e22)

# Statistical Significance
def raw_freq(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    return [c11 / cxx, None]

def students_t_test(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)
    e11, e12, e21, e22 = contingency_table_expected(c11, c12, c21, c22)

    return [(c11 - e11) / (c11 ** 0.5), 0]

def chi_squared_test(c11, c12, c21, c22):
    chi2, p_value, _, _ = scipy.stats.chi2_contingency([[c11, c12], [c21, c22]], correction = False)

    return [chi2, p_value]

def chi_squared_test_yates(c11, c12, c21, c22):
    chi2, p_value, _, _ = scipy.stats.chi2_contingency([[c11, c12], [c21, c22]], correction = True)

    return [chi2, p_value]

def log_likehood_ratio_test(c11, c12, c21, c22):
    g_value, p_value, _, _ = scipy.stats.chi2_contingency([[c11, c12], [c21, c22]], correction = False, lambda_ = 'log-likelihood')

    return [g_value, p_value]

def fishers_exact_test(c11, c12, c21, c22):
    return [None, scipy.stats.fisher_exact([[c11, c12], [c21, c22]])[1]]

# Reference: Wilson, Andrew. "Embracing Bayes Factors for Key Item Analysis in Corpus Linguistics." New Approaches to the Study of Linguistic Variability, edited by Markus Bieswanger and Amei Koll-Stobbe, Peter Lang, 2013, pp. 3-11.
def bayes_factor(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    return [log_likehood_ratio_test(c11, c12, c21, c22) - math.log(cxx, e), None]

def pmi(c11, c12, c21, c22):
    e11, e12, e21, e22 = contingency_table_expected(c11, c12, c21, c22)

    return [math.log(c11 / e11), None]

def mi(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)
    e11, e12, e21, e22 = contingency_table_expected(c11, c12, c21, c22)

    return [((c11 / cxx) * math.log(c11 / e11) +
             (c12 / cxx) * math.log(c12 / e12) +
             (c21 / cxx) * math.log(c21 / e21) +
             (c22 / cxx) * math.log(c22 / e22)),
            None]

def poisson_stirling(c11, c12, c21, c22):
    e11, e12, e21, e22 = contingency_table_expected(c11, c12, c21, c22)

    return [c11 * (math.log(c11 / e11) - 1), None]

# Effect Size
def phi_coeff(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    return (c11 * c22 - c12 * c21) / math.sqrt(c1x * c2x * cx1 * cx2)

def sorensen_dice_coeff(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    return 2 * c11 / (c1x + cx1) 

def jaccard_index(c11, c12, c21, c22):
    return c11 / (c11 + c12 + c21)

def odds_ratio(c11, c12, c21, c22):
    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return (c11 / c12) / (c21 / c22)

def risk_ratio(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return (c11 / cx1) / (c12 / cx2)

# Reference: Hardie, Andrew. "Log Ratio: An Informal Introduction." The Centre for Corpus Approaches to Social Science, http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/
def log_ratio(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return math.log((c11 / cx1) / (c12 / cx2), 2)

# Reference: Hofland, Knut and Stig Johansson. Word Frequencies in British and American English, Norwegian Computing Centre for the Humanities, 1982.
def diff_coeff(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    return (c11 / cx1 - c12 / cx2) / (c11 / cx1 + c12 / cx2)

# Reference: Gabrielatos, Costas and Anna Marchi. Keyness: Appropriate Metrics and Practical Issues. CADS International Conference 2012. Corpus-assisted Discourse Studies: More than the sum of Discourse Analysis and computing?, U of Bologna, 13-14 Sept. 2012.
def pct_diff(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = contingency_table_totals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return ((c11 / cx1 - c12 / cx2) * 100) / (c12 / cx2)

def yules_q(c11, c12, c21, c22):
    return (c11 * c22 - c12 * c21) / (c11 * c22 + c12 * c21)