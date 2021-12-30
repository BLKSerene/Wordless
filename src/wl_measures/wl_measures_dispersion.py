#
# Wordless: Measures - Dispersion
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

import numpy
import scipy.stats

from wl_measures import wl_measures_adjusted_freq

# Carroll's D₂
# Reference: Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def carrolls_d2(freqs):
    h = 0
    freq_total = sum(freqs)

    if freq_total == 0:
        d2 = 0
    else:
        for freq in freqs:
            if freq:
                h += freq * math.log(freq, math.e)

        h = math.log(freq_total, math.e) - h / freq_total

        d2 = h / math.log(len(freqs), math.e)

    return d2

# Gries's DP
# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri
def griess_dp(freqs):
    num_sections = len(freqs)
    freq_total = sum(freqs)

    if freq_total == 0:
        dp = 0
    else:
        dp = sum([abs(freq / freq_total - 1 / num_sections)
                  for freq in freqs]) / 2

    return dp

# Gries's DPnorm
# Reference: Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora”. International Journal of Corpus Linguistics, 17(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij
def griess_dp_norm(freqs):
    return griess_dp(freqs) / (1 - 1 / len(freqs))

# Juilland's D
# Reference: Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of spanish words. Mouton.
def juillands_d(freqs):
    if sum(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
    
        d = 1 - cv / math.sqrt(len(freqs) - 1)

    return max(0, d)

# Lyne's D₃
# Reference: Lyne, A. A. (1985). Dispersion. In The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method (pp. 101–124). Slatkine/Champion.
def lynes_d3(freqs):
    if sum(freqs) == 0:
        d3 = 0
    else:
        d3 = 1 - scipy.stats.chisquare(freqs)[0] / (4 * sum(freqs))

    return max(0, d3)

# Rosengren's S
# Reference: Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127.
def rosengrens_s(freqs):
    if sum(freqs) == 0:
        s = 0
    else:
        kf = wl_measures_adjusted_freq.rosengrens_kf(freqs)
        s = kf / sum(freqs)

    return s

# Zhang's Distributional Consistency
# Reference: Zhang, H., Huang, C., & Yu, S. (2004). Distributional consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), Proceedings of Fourth International Conference on Language Resources and Evaluation (pp. 1119–1122). European Language Resources Association.
def zhangs_distributional_consistency(freqs):
    if sum(freqs) == 0:
        dc = 0
    else:
        num_sections = len(freqs)

        dc = ((sum([math.sqrt(freq) for freq in freqs]) / num_sections) ** 2 /
              (sum(freqs) / num_sections))

    return dc
