#
# Wordless: Measures - Dispersion
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

import numpy
import scipy.stats

from wordless_measures import wordless_measures_adjusted_freq

# Reference:
#     Juilland, Alphonse, and Eugenio Chang-Rodriguez. Frequency Dictionary of Spanish Words, Mouton, 1964.
def juillands_d(freqs):
    if sum(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
    
        d = 1 - cv / math.sqrt(len(freqs) - 1)

    return max(0, d)

# Reference:
#     Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
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

# Reference:
#     Lyne, Anthony A. “Dispersion.” The Vocabulary of French Business Correspondence: Word Frequencies, Collocations, and Problems of Lexicometric Method. Slatkine/Champion, 1985, pp. 101-24.
def lynes_d3(freqs):
    if sum(freqs) == 0:
        d3 = 0
    else:
        d3 = 1 - scipy.stats.chisquare(freqs)[0] / (4 * sum(freqs))

    return max(0, d3)

# Reference:
#     Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, pp. 103-27.
def rosengrens_s(freqs):
    if sum(freqs) == 0:
        s = 0
    else:
        kf = wordless_measures_adjusted_freq.rosengrens_kf(freqs)
        s = kf / sum(freqs)

    return s

# Reference:
#     Zhang Huarui, et al. “Distributional Consistency: As a General Method for Defining a Core Lexicon.” Proceedings of Fourth International Conference on Language Resources and Evaluation, 26-28 May 2004, edited by Maria Teresa Lino et al., European Language Resources Association, 2004, pp. 1119-22.
def zhangs_distributional_consistency(freqs):
    if sum(freqs) == 0:
        dc = 0
    else:
        num_sections = len(freqs)

        dc = ((sum([math.sqrt(freq) for freq in freqs]) / num_sections) ** 2 /
              (sum(freqs) / num_sections))

    return dc

# Reference:
#     Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, pp. 403-37.
def griess_dp(freqs):
    num_sections = len(freqs)
    freq_total = sum(freqs)

    if freq_total == 0:
        dp = 0
    else:
        dp = sum([abs(freq / freq_total - 1 / num_sections)
                  for freq in freqs]) / 2

    return dp

# Reference:
#     Lijffijt, Jefrey, and Stefan Th. Gries. "Correction to Stefan Th. Gries’ “Dispersions and adjusted frequencies in corpora”" International Journal of Corpus Linguistics, vol. 17, no. 1, 2012, pp. 147-49.
def griess_dp_norm(freqs):
    return griess_dp(freqs) / (1 - 1 / len(freqs))
