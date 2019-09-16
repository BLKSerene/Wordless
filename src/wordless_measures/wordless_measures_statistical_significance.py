#
# Wordless: Measures - Statistical Significance
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

import numpy
import scipy.stats

from wordless_measures import wordless_measures_bayes_factor

def get_marginals(c11, c12, c21, c22):
    c1x = c11 + c12
    c2x = c21 + c22
    cx1 = c11 + c21
    cx2 = c12 + c22
    cxx = c11 + c12 + c21 + c22

    return (c1x, c2x, cx1, cx2, cxx)

def get_expected(c1x, c2x, cx1, cx2, cxx):
    e11 = c1x * cx1 / cxx
    e12 = c1x * cx2 / cxx
    e21 = c2x * cx1 / cxx
    e22 = c2x * cx2 / cxx

    return (e11, e12, e21, e22)

# Overload scipy.stats.mannwhitneyu to fix wrong implementation
def mannwhitneyu(x, y, use_continuity, alternative):
    # Check if all frequencies are equal
    if all([freq == x[0] for freq in x + y]):
        x[0] += 1e-15
        y[0] += 1e-15

    x = numpy.asarray(x)
    y = numpy.asarray(y)
    n1 = len(x)
    n2 = len(y)
    ranked = scipy.stats.rankdata(numpy.concatenate((x, y)))
    rankx = ranked[0:n1]  # get the x-ranks
    u1 = numpy.sum(rankx, axis = 0) - (n1 * (n1 + 1)) / 2.0 # calc U for x
    u2 = n1*n2 - u1  # remainder is U for y
    T = scipy.stats.tiecorrect(ranked)
    if T == 0:
        raise ValueError('All numbers are identical in mannwhitneyu')
    sd = numpy.sqrt(T * n1 * n2 * (n1+n2+1) / 12.0)

    meanrank = n1 * n2 / 2.0 + 0.5 * use_continuity
    if alternative == 'two-sided':
        bigu = max(u1, u2)
    elif alternative == 'less':
        bigu = u1
    elif alternative == 'greater':
        bigu = u2
    else:
        raise ValueError("alternative should be None, 'less', 'greater' "
                         "or 'two-sided'")

    z = (bigu - meanrank) / sd
    if alternative == 'two-sided':
        p = 2 * scipy.stats.distributions.norm.sf(abs(z))
    else:
        p = scipy.stats.distributions.norm.sf(z)

    u = min(u1, u2)
    return (u, p)

# Reference"
#     Dennis, S. F. "The Construction of a Thesaurus Automatically from a Sample of Text." Proceedings of the Symposium on Statistical Association Methods For Mechanized Documentation, Washington, D.C., 17 March, 1964, edited by Stevens, M. E., et at., National Bureau of Standards, 1965, pp. 61-148.
#     Berry-rogghe, Godelieve L. M. "The Computation of Collocations and their Relevance in Lexical Studies." The computer and literary studies, edited by Aitken, A. J., Edinburgh UP, 1973, pp. 103-112.
def z_score(main, c11, c12, c21, c22):
    direction = main.settings_custom['measures']['statistical_significance']['z_score']['direction']

    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if e11 == 0:
        z_score = 0
    else:
        z_score = (c11 - e11) / math.sqrt(e11 * (1 - e11 / cxx))

    if direction == 'Two-tailed':
        p_value = 2 * scipy.stats.distributions.norm.sf(abs(z_score))
    elif direction == 'One-tailed':
        p_value = scipy.stats.distributions.norm.sf(z_score)

    return [z_score, p_value, None]

# Reference:
#     Church, Kenneth Ward, et al. "Using Statistics in Lexical Analysis." Lexical Acquisition: Exploiting On-Line Resources to Build a Lexicon, edited by Uri Zernik, Psychology Press, 1991, pp. 115-64.
def students_t_test_1_sample(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        t_stat = 0
    else:
        t_stat = (c11 - e11) / math.sqrt(c11 * (1 - c11 / cxx))

    p_value = scipy.stats.distributions.t.sf(numpy.abs(t_stat), cxx - 1) * 2

    return [t_stat, p_value, None]

# Reference:
#     Paquot, Magali, and Yves Bestgen. "Distinctive Words in Academic Writing: A Comparison of Three Statistical Tests for Keyword Extraction." Language and Computers, vol.68, 2009, pp. 247-269.
def students_t_test_2_sample(main, counts_observed, counts_ref):
    variances = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['variances']

    if variances == main.tr('Equal'):
        t_stat, p_value = scipy.stats.ttest_ind(counts_observed, counts_ref, equal_var = True)
    elif variances == main.tr('Unequal'):
        t_stat, p_value = scipy.stats.ttest_ind(counts_observed, counts_ref, equal_var = False)

    bayes_factor = wordless_measures_bayes_factor.bayes_factor_t_test(t_stat, len(counts_observed) + len(counts_ref))

    return [t_stat, p_value, bayes_factor]

# Reference:
#     Hofland, Knut, and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982.
#     Oakes, Michael P. Statistics for Corpus Linguistics. Edinburgh UP, 1998.
def pearsons_chi_squared_test(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction']:
        c11 = c11 + 0.5 if e11 > c11 else c11 - 0.5
        c12 = c12 + 0.5 if e12 > c12 else c12 - 0.5
        c21 = c21 + 0.5 if e21 > c21 else c21 - 0.5
        c22 = c22 + 0.5 if e22 > c22 else c22 - 0.5

    if e11 == 0:
        chi_square_11 = 0
    else:
        chi_square_11 = (c11 - e11) ** 2 / e11

    if e12 == 0:
        chi_square_12 = 0
    else:
        chi_square_12 = (c12 - e12) ** 2 / e12

    if e21 == 0:
        chi_square_21 = 0
    else:
        chi_square_21 = (c21 - e21) ** 2 / e21

    if e22 == 0:
        chi_square_22 = 0
    else:
        chi_square_22 = (c22 - e22) ** 2 / e22

    chi_square = chi_square_11 + chi_square_12 + chi_square_21 + chi_square_22
    p_value = scipy.stats.distributions.chi2.sf(chi_square, 1)

    return [chi_square, p_value, None]

# Reference:
#     Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, pp. 61-74.
def log_likehood_ratio_test(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        log_likelihood_ratio_11 = 0
    else:
        log_likelihood_ratio_11 = c11 * math.log(c11 / e11)

    if c12 == 0 or e12 == 0:
        log_likelihood_ratio_12 = 0
    else:
        log_likelihood_ratio_12 = c12 * math.log(c12 / e12)

    if c21 == 0 or e21 == 0:
        log_likelihood_ratio_21 = 0
    else:
        log_likelihood_ratio_21 = c21 * math.log(c21 / e21)

    if c22 == 0 or e22 == 0:
        log_likelihood_ratio_22 = 0
    else:
        log_likelihood_ratio_22 = c22 * math.log(c22 / e22)

    log_likelihood_ratio = 2 * (log_likelihood_ratio_11 +
                                log_likelihood_ratio_12 +
                                log_likelihood_ratio_21 +
                                log_likelihood_ratio_22)

    p_value = scipy.stats.distributions.chi2.sf(log_likelihood_ratio, 1)

    bayes_factor = wordless_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(log_likelihood_ratio, cxx)

    return [log_likelihood_ratio, p_value, bayes_factor]

# Reference:
#     Pedersen, Ted. “Fishing for Exactness.” Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference, 27-29 Oct. 1996, edited by Tom Winn, The South-Central Regional SAS Users' Group, 1996, pp. 188-200.
def fishers_exact_test(main, c11, c12, c21, c22):
    direction = main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction']

    if direction == main.tr('Two-tailed'):
        alternative = 'two-sided'
    elif direction == main.tr('Left-tailed'):
        alternative = 'less'
    elif direction == main.tr('Right-tailed'):
        alternative = 'greater'

    _, p_value = scipy.stats.fisher_exact([[c11, c12], [c21, c22]],
                                          alternative = alternative)

    return [None, p_value, None]

# Reference:
#     Kilgarriff, Adam. "Comparing Corpora." International Journal of Corpus Linguistics, vol.6, no.1, Nov. 2001, pp. 232-263.
def mann_whitney_u_test(main, counts_observed, counts_ref):
    direction = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['direction']
    apply_correction = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction']

    if direction == main.tr('Two-tailed'):
        alternative = 'two-sided'
    elif direction == main.tr('Left-tailed'):
        alternative = 'less'
    elif direction == main.tr('Right-tailed'):
        alternative = 'greater'

    u_stat, p_value = mannwhitneyu(counts_observed, counts_ref,
                                   use_continuity = apply_correction,
                                   alternative = alternative)

    return [u_stat, p_value, None]
