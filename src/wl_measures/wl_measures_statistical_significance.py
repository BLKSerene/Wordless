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

import collections

import numpy
from PyQt5.QtCore import QCoreApplication
import scipy.stats

from wl_nlp import wl_nlp_utils

_tr = QCoreApplication.translate

def get_freqs_marginal(c11, c12, c21, c22):
    freqs = numpy.array([[c11, c12], [c21, c22]], dtype = numpy.int64)
    m1, m2 = scipy.stats.contingency.margins(freqs)

    c1x = int(m1[0][0])
    c2x = int(m1[1][0])
    cx1 = int(m2[0][0])
    cx2 = int(m2[0][1])

    return c1x, c2x, cx1, cx2

def get_freqs_expected(c11, c12, c21, c22):
    freqs = numpy.array([[c11, c12], [c21, c22]], dtype = numpy.int64)

    if numpy.sum(freqs) > 0:
        freqs_expected = scipy.stats.contingency.expected_freq(freqs)
    else:
        freqs_expected = [[0, 0], [0, 0]]

    e11 = float(freqs_expected[0][0])
    e12 = float(freqs_expected[0][1])
    e21 = float(freqs_expected[1][0])
    e22 = float(freqs_expected[1][1])

    return e11, e12, e21, e22

# Do not over-correct when the difference between observed and expected value is small than 0.5
# Reference: https://github.com/scipy/scipy/issues/13875
def yatess_correction(c11, c12, c21, c22, e11, e12, e21, e22):
    c11 = c11 + min(0.5, numpy.abs(e11 - c11)) if e11 > c11 else c11 - min(0.5, numpy.abs(e11 - c11))
    c12 = c12 + min(0.5, numpy.abs(e12 - c12)) if e12 > c12 else c12 - min(0.5, numpy.abs(e12 - c12))
    c21 = c21 + min(0.5, numpy.abs(e21 - c21)) if e21 > c21 else c21 - min(0.5, numpy.abs(e21 - c21))
    c22 = c22 + min(0.5, numpy.abs(e22 - c22)) if e22 > c22 else c22 - min(0.5, numpy.abs(e22 - c22))

    return c11, c12, c21, c22

def to_freqs_sections_tokens(main, tokens, tokens_x1, tokens_x2, test_statistical_significance):
    freqs_sections_tokens = {}

    if test_statistical_significance == _tr('wl_measures_statistical_significance', 'Mann-Whitney U Test'):
        num_sub_sections = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['num_sub_sections']
        use_data = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['use_data']
    elif test_statistical_significance == _tr('wl_measures_statistical_significance', "Student's t-test (2-sample)"):
        num_sub_sections = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['num_sub_sections']
        use_data = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['use_data']
    elif test_statistical_significance == _tr('wl_measures_statistical_significance', "Welch's t-test"):
        num_sub_sections = main.settings_custom['measures']['statistical_significance']['welchs_t_test']['num_sub_sections']
        use_data = main.settings_custom['measures']['statistical_significance']['welchs_t_test']['use_data']

    sections_x1 = wl_nlp_utils.to_sections(tokens_x1, num_sub_sections)
    sections_x2 = wl_nlp_utils.to_sections(tokens_x2, num_sub_sections)

    freqs_sections_x1 = [collections.Counter(section) for section in sections_x1]
    freqs_sections_x2 = [collections.Counter(section) for section in sections_x2]

    if use_data == _tr('wl_measures_statistical_significance', 'Absolute Frequency'):
        for token in tokens:
            freqs_x1 = [
                freqs_section.get(token, 0)
                for freqs_section in freqs_sections_x1
            ]
            freqs_x2 = [
                freqs_section.get(token, 0)
                for freqs_section in freqs_sections_x2
            ]

            freqs_sections_tokens[token] = (freqs_x1, freqs_x2)
    elif use_data == _tr('wl_measures_statistical_significance', 'Relative Frequency'):
        len_sections_x1 = [len(section) for section in sections_x1]
        len_sections_x2 = [len(section) for section in sections_x2]

        for token in tokens:
            freqs_x1 = [
                freqs_section.get(token, 0) / len_section
                for freqs_section, len_section in zip(freqs_sections_x1, len_sections_x1)
            ]
            freqs_x2 = [
                freqs_section.get(token, 0) / len_section
                for freqs_section, len_section in zip(freqs_sections_x2, len_sections_x2)
            ]

            freqs_sections_tokens[token] = (freqs_x1, freqs_x2)

    return freqs_sections_tokens

# Fisher's Exact Test
# References: Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188-200). The South–Central Regional SAS Users' Group.
def fishers_exact_test(main, c11, c12, c21, c22):
    direction = main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction']

    if direction == _tr('wl_measures_statistical_significance', 'Two-tailed'):
        alternative = 'two-sided'
    elif direction == _tr('wl_measures_statistical_significance', 'Left-tailed'):
        alternative = 'less'
    elif direction == _tr('wl_measures_statistical_significance', 'Right-tailed'):
        alternative = 'greater'

    p_val = scipy.stats.fisher_exact([[c11, c12], [c21, c22]], alternative = alternative)[1]

    return None, p_val

# Log-likelihood Ratio
# References: Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74.
def log_likelihood_ratio_test(main, c11, c12, c21, c22):
    apply_correction = main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test']['apply_correction']

    if c11 and c12 and c21 and c22:
        log_likelihood_ratio, p_val, _, _ = scipy.stats.chi2_contingency(
            [[c11, c12], [c21, c22]],
            correction = apply_correction,
            lambda_='log-likelihood'
        )
    else:
        e11, e12, e21, e22 = get_freqs_expected(c11, c12, c21, c22)

        if apply_correction:
            c11, c12, c21, c22 = yatess_correction(c11, c12, c21, c22, e11, e12, e21, e22)

        log_likelihood_ratio_11 = c11 * numpy.log(c11 / e11) if c11 else 0
        log_likelihood_ratio_12 = c12 * numpy.log(c12 / e12) if c12 else 0
        log_likelihood_ratio_21 = c21 * numpy.log(c21 / e21) if c21 else 0
        log_likelihood_ratio_22 = c22 * numpy.log(c22 / e22) if c22 else 0

        log_likelihood_ratio = 2 * (
            log_likelihood_ratio_11
            + log_likelihood_ratio_12
            + log_likelihood_ratio_21
            + log_likelihood_ratio_22
        )
        p_val = scipy.stats.distributions.chi2.sf(log_likelihood_ratio, 1)

    return log_likelihood_ratio, p_val

# Mann-Whitney U Test
# References: Kilgarriff, A. (2001). Comparing corpora. International Journal of Corpus Linguistics, 6(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil
def mann_whitney_u_test(main, freqs_x1, freqs_x2):
    direction = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['direction']
    apply_correction = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['apply_correction']

    if direction == _tr('wl_measures_statistical_significance', 'Two-tailed'):
        alternative = 'two-sided'
    elif direction == _tr('wl_measures_statistical_significance', 'Left-tailed'):
        alternative = 'less'
    elif direction == _tr('wl_measures_statistical_significance', 'Right-tailed'):
        alternative = 'greater'

    u1, p = scipy.stats.mannwhitneyu(
        freqs_x1, freqs_x2,
        use_continuity = apply_correction,
        alternative = alternative
    )

    return u1, p

# Pearson's Chi-squared Test
# References:
#     Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities.
#     Oakes, M. P. (1998). Statistics for Corpus Linguistics. Edinburgh University Press.
def pearsons_chi_squared_test(main, c11, c12, c21, c22):
    apply_correction = main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction']

    if c11 and c12 and c21 and c22:
        chi_squared, p_val, _, _ = scipy.stats.chi2_contingency(
            [[c11, c12], [c21, c22]],
            correction = apply_correction
        )
    else:
        e11, e12, e21, e22 = get_freqs_expected(c11, c12, c21, c22)

        if apply_correction:
            c11, c12, c21, c22 = yatess_correction(c11, c12, c21, c22, e11, e12, e21, e22)

        chi_squared_11 = (c11 - e11) ** 2 / e11 if e11 else 0
        chi_squared_12 = (c12 - e12) ** 2 / e12 if e12 else 0
        chi_squared_21 = (c21 - e21) ** 2 / e21 if e21 else 0
        chi_squared_22 = (c22 - e22) ** 2 / e22 if e22 else 0

        chi_squared = chi_squared_11 + chi_squared_12 + chi_squared_21 + chi_squared_22
        p_val = scipy.stats.distributions.chi2.sf(chi_squared, 1)

    return chi_squared, p_val

# Student's t-test (1-sample)
# References: Church, K., Gale, W., Hanks P., & Hindle D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), Lexical acquisition: Exploiting on-line resources to build a lexicon (pp. 115–164). Psychology Press.
def students_t_test_1_sample(main, c11, c12, c21, c22):
    cxx = c11 + c12 + c21 + c22
    e11, e12, e21, e22 = get_freqs_expected(c11, c12, c21, c22)

    t_stat = (c11 - e11) / numpy.sqrt(c11 * (1 - c11 / cxx)) if c11 else 0
    p_val = scipy.stats.distributions.t.sf(numpy.abs(t_stat), cxx - 1) * 2 if cxx > 0 else 1

    return t_stat, p_val

# Student's t-test (2-sample)
# References: Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction. Language and Computers, 68, 247–269.
def students_t_test_2_sample(main, freqs_x1, freqs_x2):
    if any(freqs_x1) or any(freqs_x2):
        t_stat, p_val = scipy.stats.ttest_ind(freqs_x1, freqs_x2, equal_var = True)
    else:
        t_stat = 0
        p_val = 1

    return t_stat, p_val

def welchs_t_test(main, freqs_x1, freqs_x2):
    if any(freqs_x1) or any(freqs_x2):
        t_stat, p_val = scipy.stats.ttest_ind(freqs_x1, freqs_x2, equal_var = False)
    else:
        t_stat = 0
        p_val = 1

    return t_stat, p_val

def z_test(z_score, direction):
    if direction == _tr('wl_measures_statistical_significance', 'Two-tailed'):
        p_val = scipy.stats.distributions.norm.sf(numpy.abs(z_score)) * 2
    elif direction == _tr('wl_measures_statistical_significance', 'Left-tailed'):
        p_val = scipy.stats.distributions.norm.cdf(z_score)
    elif direction == _tr('wl_measures_statistical_significance', 'Right-tailed'):
        p_val = scipy.stats.distributions.norm.sf(z_score)

    return p_val

# z-score
# References: Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), Proceedings of the symposium on statistical association methods for mechanized documentation (pp. 61–148). National Bureau of Standards.
def z_score(main, c11, c12, c21, c22):
    direction = main.settings_custom['measures']['statistical_significance']['z_score']['direction']

    cxx = c11 + c12 + c21 + c22
    e11, e12, e21, e22 = get_freqs_expected(c11, c12, c21, c22)

    z_score = (c11 - e11) / numpy.sqrt(e11 * (1 - e11 / cxx)) if cxx and e11 and 1 - e11 / cxx else 0
    p_val = z_test(z_score, direction)

    return z_score, p_val

# z-score (Berry-Rogghe)
# References: Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), The computer and literary studies (pp. 103–112). Edinburgh University Press.
def z_score_berry_rogghe(main, c11, c12, c21, c22, span):
    direction = main.settings_custom['measures']['statistical_significance']['z_score_berry_rogghe']['direction']

    c1x, c2x, cx1, cx2 = get_freqs_marginal(c11, c12, c21, c22)

    z = c1x + c2x
    fn = c1x
    fc = cx1
    k = c11
    s = span

    p = fc / (z - fn) if z - fn else 1
    e = p * fn * s

    z_score = (k - e) / numpy.sqrt(e * (1 - p)) if e and 1 - p else 0
    p_val = z_test(z_score, direction)

    return z_score, p_val
