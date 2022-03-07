# ----------------------------------------------------------------------
# Wordless: Measures - Statistical Significance
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

import math

import numpy
from PyQt5.QtCore import QCoreApplication
import scipy.stats

from wl_measures import wl_measures_bayes_factor

_tr = QCoreApplication.translate

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

# Overwrite scipy.stats.mannwhitneyu to fix wrong implementation
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
    u2 = n1 * n2 - u1  # remainder is U for y
    T = scipy.stats.tiecorrect(ranked)
    if T == 0:
        raise ValueError('All numbers are identical in mannwhitneyu')
    sd = numpy.sqrt(T * n1 * n2 * (n1 + n2 + 1) / 12.0)

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

# Berry-Rogghe's z-score
# References: Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), The computer and literary studies (pp. 103–112). Edinburgh University Press.
def berry_rogghes_z_score(main, c11, c12, c21, c22, span):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    z = cxx
    fn = c1x
    fc = cx1
    k = c11
    s = span

    p = fc / (z - fn)
    e = p * fn * s

    if math.sqrt(e * (1 - p)) == 0:
        z_score = 0
    else:
        z_score = (k - e) / math.sqrt(e * (1 - p))

    p_value = scipy.stats.distributions.norm.sf(z_score)

    return [z_score, p_value, None]

# Fisher's Exact Test
# References: Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188-200). The South–Central Regional SAS Users' Group.
def fishers_exact_test(main, c11, c12, c21, c22):
    direction = main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction']

    if direction == _tr('fishers_exact_test', 'Two-tailed'):
        alternative = 'two-sided'
    elif direction == _tr('fishers_exact_test', 'Left-tailed'):
        alternative = 'less'
    elif direction == _tr('fishers_exact_test', 'Right-tailed'):
        alternative = 'greater'

    _, p_value = scipy.stats.fisher_exact(
        [[c11, c12], [c21, c22]],
        alternative = alternative
    )

    return [None, p_value, None]

# Log-likelihood Ratio
# References: Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74.
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

    log_likelihood_ratio = 2 * (
        log_likelihood_ratio_11
        + log_likelihood_ratio_12
        + log_likelihood_ratio_21
        + log_likelihood_ratio_22
    )

    p_value = scipy.stats.distributions.chi2.sf(log_likelihood_ratio, 1)

    bayes_factor = wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(log_likelihood_ratio, cxx)

    return [log_likelihood_ratio, p_value, bayes_factor]

# Mann-Whitney U Test
# References: Kilgarriff, A. (2001). Comparing corpora. International Journal of Corpus Linguistics, 6(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil
def mann_whitney_u_test(main, counts_observed, counts_ref):
    direction = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['direction']
    apply_correction = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction']

    if direction == _tr('mann_whitney_u_test', 'Two-tailed'):
        alternative = 'two-sided'
    elif direction == _tr('mann_whitney_u_test', 'Left-tailed'):
        alternative = 'less'
    elif direction == _tr('mann_whitney_u_test', 'Right-tailed'):
        alternative = 'greater'

    u_stat, p_value = mannwhitneyu(
        counts_observed, counts_ref,
        use_continuity = apply_correction,
        alternative = alternative
    )

    return [u_stat, p_value, None]

# Pearson's Chi-squared Test
# References:
#     Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities.
#     Oakes, M. P. (1998). Statistics for Corpus Linguistics. Edinburgh University Press.
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

# Student's t-test (1-sample)
# References: Church, K., Gale, W., Hanks P., & Hindle D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), Lexical acquisition: Exploiting on-line resources to build a lexicon (pp. 115–164). Psychology Press.
def students_t_test_1_sample(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        t_stat = 0
    else:
        t_stat = (c11 - e11) / math.sqrt(c11 * (1 - c11 / cxx))

    p_value = scipy.stats.distributions.t.sf(numpy.abs(t_stat), cxx - 1) * 2

    return [t_stat, p_value, None]

# Student's t-test (2-sample)
# References: Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction. Language and Computers, 68, 247–269.
def students_t_test_2_sample(main, counts_observed, counts_ref):
    variances = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['variances']

    if variances == _tr('students_t_test_2_sample', 'Equal'):
        t_stat, p_value = scipy.stats.ttest_ind(counts_observed, counts_ref, equal_var = True)
    elif variances == _tr('students_t_test_2_sample', 'Unequal'):
        t_stat, p_value = scipy.stats.ttest_ind(counts_observed, counts_ref, equal_var = False)

    bayes_factor = wl_measures_bayes_factor.bayes_factor_t_test(t_stat, len(counts_observed) + len(counts_ref))

    return [t_stat, p_value, bayes_factor]

# z-score
# References: Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), Proceedings of the symposium on statistical association methods for mechanized documentation (pp. 61–148). National Bureau of Standards.
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
