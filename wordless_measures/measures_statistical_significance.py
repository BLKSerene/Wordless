#
# Wordless: Measures - Statistical Significance
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import math

import numpy
import scipy.stats

from wordless_measures import measures_bayes_factor

def get_marginals(c11, c12, c21, c22):
    c1x = c11 + c12
    c2x = c21 + c22
    cx1 = c11 + c21
    cx2 = c12 + c22
    cxx = c11 + c12 + c21 + c22

    return (c1x, c2x, cx1, cx2, cxx)

def get_expected(c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    e11 = c1x * cx1 / cxx
    e12 = c1x * cx2 / cxx
    e21 = c2x * cx1 / cxx
    e22 = c2x * cx2 / cxx

    return (e11, e12, e21, e22)

# Reference"
#     Dennis, S. F. "The Construction of a Thesaurus Automatically from a Sample of Text." Proceedings of the Symposium on Statistical Association Methods For Mechanized Documentation, Washington, D.C., 17 March, 1964, edited by Stevens, M. E., et at., National Bureau of Standards, 1965, pp. 61-148.
#     Berry-rogghe, Godelieve L. M. "The Computation of Collocations and their Relevance in Lexical Studies." The computer and literary studies, edited by Aitken, A. J., Edinburgh UP, 1973, pp. 103-112.
def z_score(main, c11, c12, c21, c22, span_size):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    p = cx1 / (cxx - c1x)
    e = p * c1x * span_size

    return [(c11 - e) / math.sqrt(e * (1 - p)), None, None]

# Reference:
#     Church, Kenneth Ward, et al. "Using Statistics in Lexical Analysis." Lexical Acquisition: Exploiting On-Line Resources to Build a Lexicon, edited by Uri Zernik, Psychology Press, 1991, pp. 115-64.
def students_t_test_one_sample(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c11, c12, c21, c22)

    samples = [1] * c11 + [0] * (cxx - c11)

    t_statistic, p_value = scipy.stats.ttest_1samp(samples, e11 / cxx)

    return [t_statistic, p_value, None]

# Reference:
#     Paquot, Magali and Yves Bestgen. "Distinctive Words in Academic Writing: A Comparison of Three Statistical Tests for Keyword Extraction." Language and Computers, vol.68, 2009, pp. 247-269.
def students_t_test_two_sample(main, counts_observed, counts_ref):
    variances = main.settings_custom['measures']['statistical_significance']['students_t_test_two_sample']['variances']
    if variances == main.tr('Equal'):
        t_stat, p_value = scipy.stats.ttest_ind(counts_observed, counts_ref, equal_var = True)
    elif variances == main.tr('Unequal'):
        t_stat, p_value = scipy.stats.ttest_ind(counts_observed, counts_ref, equal_var = False)

    bayes_factor = measures_bayes_factor.bayes_factor_t_test(t_stat, len(counts_observed) + len(counts_ref))

    return [t_stat, p_value, bayes_factor]

# Reference:
#     Hofland, Knut and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982.
#     Oakes, Michael P. Statistics for Corpus Linguistics. Edinburgh UP, 1998.
def pearsons_chi_squared_test(main, c11, c12, c21, c22):
    apply_correction = main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction']

    chi2, p_value, _, _ = scipy.stats.chi2_contingency([[c11, c12], [c21, c22]],
                                                       correction = apply_correction)

    return [chi2, p_value, None]

# Reference:
#     Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, pp. 61-74.
def log_likehood_ratio_test(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    g_value, p_value, _, _ = scipy.stats.chi2_contingency([[c11, c12], [c21, c22]],
                                                          correction = False,
                                                          lambda_ = 'log-likelihood')

    bayes_factor = measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(g_value, cxx)

    return [g_value, p_value, bayes_factor]

# Reference:
#     Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin.
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
    # Overload scipy.stats.mannwhitneyu to fix wrong implementation
    def mannwhitneyu(x, y, use_continuity, alternative):
        x = numpy.asarray(x)
        y = numpy.asarray(y)
        n1 = len(x)
        n2 = len(y)
        ranked = scipy.stats.rankdata(numpy.concatenate((x, y)))
        rankx = ranked[0:n1]  # get the x-ranks
        u1 = numpy.sum(rankx, axis=0) - (n1*(n1+1))/2.0 # calc U for x
        u2 = n1*n2 - u1  # remainder is U for y
        T = scipy.stats.tiecorrect(ranked)
        if T == 0:
            raise ValueError('All numbers are identical in mannwhitneyu')
        sd = numpy.sqrt(T * n1 * n2 * (n1+n2+1) / 12.0)

        meanrank = n1*n2/2.0 + 0.5 * use_continuity
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

# Testing
if __name__ == '__main__':
    from PyQt5.QtCore import *

    import measures_bayes_factor

    main = QObject()
    main.settings_custom = {
        'measures': {
            'statistical_significance': {
                'students_t_test_two_sample': {
                    'variances': 'Equal'
                },

                'pearsons_chi_squared_test': {},

                'fishers_exact_test': {},

                'mann_whitney_u_test': {
                    'direction': 'Two-tailed',
                    'apply_correction': True
                }
            }
        }
    }

    # Manning, Christopher D. and Hinrich Schütze. Foundations of Statistical Natural Language Processing. MIT Press, May 1999, pp. 164-165.
    print('Student\'s t-test (One Sample):\n\t', end = '')
    print(students_t_test_one_sample(main, 8, 15828 - 8, 4675 - 8, 14307668 - 15828 - 4675 + 8)[0]) # 0.999932

    # Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, p. 73.
    # Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin, p. 10.
    print('Pearson\'s Chi-squared Test:')

    main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = False 

    print(f'\t{pearsons_chi_squared_test(main, 3, 0, 0, 31774)[0]}') # 31777.00

    main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = True 

    print(f'\t{pearsons_chi_squared_test(main, 1, 3, 3, 1)[0:2]} * with Yates\'s correction for continuity') # 0.500, 0.480

    # Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, p. 72.
    print('Log-likelihood Ratio Test:\n\t', end = '')
    print(log_likehood_ratio_test(main, 10, 0, 3, 31764)[0]) # 167.23

    # Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin, p. 10.
    print('Fisher\'s Exact Test:')

    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Two-tailed' 

    print(f'\t{fishers_exact_test(main, 1, 3, 3, 1)[1]} * Two-tailed') # 0.486

    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Left-tailed' 

    print(f'\t{fishers_exact_test(main, 1, 3, 3, 1)[1]} * Left-tailed') # 0.243

    main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Right-tailed' 

    print(f'\t{fishers_exact_test(main, 1, 3, 3, 1)[1]} * Right-tailed') # 0.986

    # Kilgarriff, Adam. "Comparing Corpora." International Journal of Corpus Linguistics, vol.6, no.1, Nov. 2001, p. 238.
    print('Mann-Whiteney U Test:\n\t', end = '')
    print(5 * (5 + 1) / 2 + mann_whitney_u_test(main,
                                                [12, 15, 18, 24, 88],
                                                [3, 3, 13, 27, 33])[0]) # R2: 24
