# ----------------------------------------------------------------------
# Wordless: Measures - Statistical significance
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

# pylint: disable=unused-argument

import numpy
from PyQt5.QtCore import QCoreApplication
import scipy.stats

from wordless.wl_measures import wl_measure_utils

_tr = QCoreApplication.translate

def get_freqs_marginal(o11s, o12s, o21s, o22s):
    o1xs = o11s + o12s
    o2xs = o21s + o22s
    ox1s = o11s + o21s
    ox2s = o12s + o22s

    return o1xs, o2xs, ox1s, ox2s

def get_freqs_expected(o11s, o12s, o21s, o22s):
    o1xs, o2xs, ox1s, ox2s = get_freqs_marginal(o11s, o12s, o21s, o22s)
    oxxs = o1xs + o2xs

    e11s = wl_measure_utils.numpy_divide(o1xs * ox1s, oxxs)
    e12s = wl_measure_utils.numpy_divide(o1xs * ox2s, oxxs)
    e21s = wl_measure_utils.numpy_divide(o2xs * ox1s, oxxs)
    e22s = wl_measure_utils.numpy_divide(o2xs * ox2s, oxxs)

    return e11s, e12s, e21s, e22s

# Do not over-correct when the difference between observed and expected value is small than 0.5
# Reference: https://github.com/scipy/scipy/issues/13875
def yatess_correction(o11s, o12s, o21s, o22s, e11s, e12s, e21s, e22s):
    e_o_diffs_11 = e11s - o11s
    e_o_diffs_12 = e12s - o12s
    e_o_diffs_21 = e21s - o21s
    e_o_diffs_22 = e22s - o22s

    o11s = numpy.where(numpy.abs(e_o_diffs_11) > 0.5, o11s + 0.5 * numpy.sign(e_o_diffs_11), e11s)
    o12s = numpy.where(numpy.abs(e_o_diffs_12) > 0.5, o12s + 0.5 * numpy.sign(e_o_diffs_12), e12s)
    o21s = numpy.where(numpy.abs(e_o_diffs_21) > 0.5, o21s + 0.5 * numpy.sign(e_o_diffs_21), e21s)
    o22s = numpy.where(numpy.abs(e_o_diffs_22) > 0.5, o22s + 0.5 * numpy.sign(e_o_diffs_22), e22s)

    return o11s, o12s, o21s, o22s

def get_alt(direction):
    if direction == _tr('wl_measures_statistical_significance', 'Two-tailed'):
        alt = 'two-sided'
    elif direction == _tr('wl_measures_statistical_significance', 'Left-tailed'):
        alt = 'less'
    elif direction == _tr('wl_measures_statistical_significance', 'Right-tailed'):
        alt = 'greater'

    return alt

# Fisher's exact test
# References: Pedersen, T. (1996). Fishing for exactness. In T. Winn (Ed.), Proceedings of the Sixth Annual South-Central Regional SAS Users' Group Conference (pp. 188–200). The South–Central Regional SAS Users' Group.
def fishers_exact_test(main, o11s, o12s, o21s, o22s):
    settings = main.settings_custom['measures']['statistical_significance']['fishers_exact_test']

    p_vals = numpy.array([
        scipy.stats.fisher_exact(
            [[o11, o12], [o21, o22]],
            alternative = get_alt(settings['direction'])
        )[1]
        for o11, o12, o21, o22 in zip(o11s, o12s, o21s, o22s)
    ])

    return [None] * len(p_vals), p_vals

# Log-likelihood ratio test
# References: Dunning, T. E. (1993). Accurate methods for the statistics of surprise and coincidence. Computational Linguistics, 19(1), 61–74.
def log_likelihood_ratio_test(main, o11s, o12s, o21s, o22s):
    settings = main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test']

    e11s, e12s, e21s, e22s = get_freqs_expected(o11s, o12s, o21s, o22s)

    if settings['apply_correction']:
        o11s, o12s, o21s, o22s = yatess_correction(o11s, o12s, o21s, o22s, e11s, e12s, e21s, e22s)

    gs_11 = o11s * wl_measure_utils.numpy_log(wl_measure_utils.numpy_divide(o11s, e11s))
    gs_12 = o12s * wl_measure_utils.numpy_log(wl_measure_utils.numpy_divide(o12s, e12s))
    gs_21 = o21s * wl_measure_utils.numpy_log(wl_measure_utils.numpy_divide(o21s, e21s))
    gs_22 = o22s * wl_measure_utils.numpy_log(wl_measure_utils.numpy_divide(o22s, e22s))

    gs = 2 * (gs_11 + gs_12 + gs_21 + gs_22)
    p_vals = numpy.array([
        scipy.stats.distributions.chi2.sf(g, 1)
        for g in gs
    ])

    return gs, p_vals

# Mann-Whitney U test
# References: Kilgarriff, A. (2001). Comparing corpora. International Journal of Corpus Linguistics, 6(1), 232–263. https://doi.org/10.1075/ijcl.6.1.05kil | pp. 103–104
def mann_whitney_u_test(main, freqs_x1s, freqs_x2s):
    settings = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']

    num_types = len(freqs_x1s)
    u1s = numpy.empty(shape = num_types, dtype = numpy.float64)
    p_vals = numpy.empty(shape = num_types, dtype = numpy.float64)

    for i, (freqs_x1, freqs_x2) in enumerate(zip(freqs_x1s, freqs_x2s)):
        u1, p_val = scipy.stats.mannwhitneyu(
            freqs_x1, freqs_x2,
            use_continuity = settings['apply_correction'],
            alternative = get_alt(settings['direction'])
        )

        u1s[i] = u1
        p_vals[i] = p_val

    return u1s, p_vals

# Pearson's chi-squared test
# References:
#     Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities. | p. 12
#     Oakes, M. P. (1998). Statistics for corpus linguistics. Edinburgh University Press. | p. 25
def pearsons_chi_squared_test(main, o11s, o12s, o21s, o22s):
    settings = main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']

    e11s, e12s, e21s, e22s = get_freqs_expected(o11s, o12s, o21s, o22s)

    if settings['apply_correction']:
        o11s, o12s, o21s, o22s = yatess_correction(o11s, o12s, o21s, o22s, e11s, e12s, e21s, e22s)

    chi2s_11 = wl_measure_utils.numpy_divide((o11s - e11s) ** 2, e11s)
    chi2s_12 = wl_measure_utils.numpy_divide((o12s - e12s) ** 2, e12s)
    chi2s_21 = wl_measure_utils.numpy_divide((o21s - e21s) ** 2, e21s)
    chi2s_22 = wl_measure_utils.numpy_divide((o22s - e22s) ** 2, e22s)

    chi2s = chi2s_11 + chi2s_12 + chi2s_21 + chi2s_22
    p_vals = numpy.array([
        scipy.stats.distributions.chi2.sf(chi2, 1)
        for chi2 in chi2s
    ])

    return chi2s, p_vals

# Student's t-test (1-sample)
# References: Church, K., Gale, W., Hanks, P., & Hindle, D. (1991). Using statistics in lexical analysis. In U. Zernik (Ed.), Lexical acquisition: Exploiting on-line resources to build a lexicon (pp. 115–164). Psychology Press. | pp. 120–126
def students_t_test_1_sample(main, o11s, o12s, o21s, o22s):
    settings = main.settings_custom['measures']['statistical_significance']['students_t_test_1_sample']

    oxxs = o11s + o12s + o21s + o22s
    e11s, _, _, _ = get_freqs_expected(o11s, o12s, o21s, o22s)

    t_stats = wl_measure_utils.numpy_divide(o11s - e11s, numpy.sqrt(o11s * (1 - wl_measure_utils.numpy_divide(o11s, oxxs))))
    p_vals = numpy.empty_like(t_stats)

    if settings['direction'] == _tr('wl_measures_statistical_significance', 'Two-tailed'):
        for i, (oxx, t_stat) in enumerate(zip(oxxs, t_stats)):
            p_vals[i] = scipy.stats.distributions.t.sf(numpy.abs(t_stat), oxx - 1) * 2 if oxx > 1 else 1
    elif settings['direction'] == _tr('wl_measures_statistical_significance', 'Left-tailed'):
        for i, (oxx, t_stat) in enumerate(zip(oxxs, t_stats)):
            p_vals[i] = scipy.stats.distributions.t.cdf(t_stat, oxx - 1) if oxx > 1 else 1
    elif settings['direction'] == _tr('wl_measures_statistical_significance', 'Right-tailed'):
        for i, (oxx, t_stat) in enumerate(zip(oxxs, t_stats)):
            p_vals[i] = scipy.stats.distributions.t.sf(t_stat, oxx - 1) if oxx > 1 else 1

    return t_stats, p_vals

# Student's t-test (2-sample)
# References: Paquot, M., & Bestgen, Y. (2009). Distinctive words in academic writing: A comparison of three statistical tests for keyword extraction. Language and Computers, 68, 247–269. | pp. 252–253
def students_t_test_2_sample(main, freqs_x1s, freqs_x2s):
    settings = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']

    num_types = len(freqs_x1s)
    t_stats = numpy.empty(shape = num_types, dtype = numpy.float64)
    p_vals = numpy.empty(shape = num_types, dtype = numpy.float64)

    for i, (freqs_x1, freqs_x2) in enumerate(zip(freqs_x1s, freqs_x2s)):
        if any(freqs_x1) or any(freqs_x2):
            t_stat, p_val = scipy.stats.ttest_ind(
                freqs_x1, freqs_x2,
                equal_var = True,
                alternative = get_alt(settings['direction'])
            )
        else:
            t_stat = 0
            p_val = 1

        t_stats[i] = t_stat
        p_vals[i] = p_val

    return t_stats, p_vals

def _z_test_p_val(z_scores, direction):
    p_vals = numpy.empty_like(z_scores)

    if direction == _tr('wl_measures_statistical_significance', 'Two-tailed'):
        for i, z_score in enumerate(z_scores):
            p_vals[i] = scipy.stats.distributions.norm.sf(numpy.abs(z_score)) * 2
    elif direction == _tr('wl_measures_statistical_significance', 'Left-tailed'):
        for i, z_score in enumerate(z_scores):
            p_vals[i] = scipy.stats.distributions.norm.cdf(z_score)
    elif direction == _tr('wl_measures_statistical_significance', 'Right-tailed'):
        for i, z_score in enumerate(z_scores):
            p_vals[i] = scipy.stats.distributions.norm.sf(z_score)

    return p_vals

# Z-test
# References: Dennis, S. F. (1964). The construction of a thesaurus automatically from a sample of text. In M. E. Stevens, V. E. Giuliano, & L. B. Heilprin (Eds.), Statistical association methods for mechanized documentation: Symposium proceedings (pp. 61–148). National Bureau of Standards. | p. 69
def z_test(main, o11s, o12s, o21s, o22s):
    settings = main.settings_custom['measures']['statistical_significance']['z_test']

    oxxs = o11s + o12s + o21s + o22s
    e11s, _, _, _ = get_freqs_expected(o11s, o12s, o21s, o22s)

    z_scores = wl_measure_utils.numpy_divide(o11s - e11s, numpy.sqrt(e11s * (1 - wl_measure_utils.numpy_divide(e11s, oxxs))))
    p_vals = _z_test_p_val(z_scores, settings['direction'])

    return z_scores, p_vals

# Z-test (Berry-Rogghe)
# References: Berry-Rogghe, G. L. M. (1973). The computation of collocations and their relevance in lexical studies. In A. J. Aiken, R. W. Bailey, & N. Hamilton-Smith (Eds.), The computer and literary studies (pp. 103–112). Edinburgh University Press.
def z_test_berry_rogghe(main, o11s, o12s, o21s, o22s, span):
    settings = main.settings_custom['measures']['statistical_significance']['z_test_berry_rogghe']

    o1xs, o2xs, ox1s, _ = get_freqs_marginal(o11s, o12s, o21s, o22s)

    zs = o1xs + o2xs
    ps = wl_measure_utils.numpy_divide(ox1s, zs - o1xs, default = 1)
    es = ps * o1xs * span

    z_scores = wl_measure_utils.numpy_divide(o11s - es, numpy.sqrt(es * (1 - ps)))
    p_vals = _z_test_p_val(z_scores, settings['direction'])

    return z_scores, p_vals
