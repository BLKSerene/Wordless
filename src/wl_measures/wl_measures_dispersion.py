# ----------------------------------------------------------------------
# Wordless: Measures - Dispersion
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
import scipy.stats

from wl_measures import wl_measures_adjusted_freq
from wl_nlp import wl_nlp_utils

def to_freqs_sections_tokens(main, tokens, tokens_all):
    freqs_sections_tokens = {}

    num_sub_sections = main.settings_custom['measures']['dispersion']['general_settings']['num_sub_sections']

    freqs_sections = [
        collections.Counter(section)
        for section in wl_nlp_utils.to_sections(tokens_all, num_sub_sections)
    ]

    for token in tokens:
        freqs_sections_tokens[token] = [
            freqs_section.get(token, 0)
            for freqs_section in freqs_sections
        ]

    return freqs_sections_tokens

# Carroll's D₂
# Reference: Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def carrolls_d2(freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        d2 = 0
    else:
        h = numpy.sum(freqs * numpy.log(freqs, out = numpy.zeros_like(freqs, dtype = numpy.float64), where = (freqs != 0)))
        h = numpy.log(freq_total) - h / freq_total
        d2 = h / numpy.log(len(freqs))

    return d2

# Gries's DP
# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri
def griess_dp(freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        dp = 0
    else:
        num_sections = len(freqs)

        dp = numpy.sum([
            numpy.abs(freq / freq_total - 1 / num_sections)
            for freq in freqs
        ]) / 2

    return dp

# Gries's DPnorm
# Reference: Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora”. International Journal of Corpus Linguistics, 17(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij
def griess_dp_norm(freqs):
    return griess_dp(freqs) / (1 - 1 / len(freqs))

# Juilland's D
# Reference: Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of spanish words. Mouton.
def juillands_d(freqs):
    freqs = numpy.array(freqs)

    if numpy.sum(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
        d = 1 - cv / numpy.sqrt(len(freqs) - 1)

    return max(0, d)

# Lyne's D₃
# Reference: Lyne, A. A. (1985). Dispersion. In The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method (pp. 101–124). Slatkine/Champion.
def lynes_d3(freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        d3 = 0
    else:
        d3 = 1 - scipy.stats.chisquare(freqs)[0] / (4 * freq_total)

    return max(0, d3)

# Rosengren's S
# Reference: Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127.
def rosengrens_s(freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        s = 0
    else:
        kf = wl_measures_adjusted_freq.rosengrens_kf(freqs)
        s = kf / freq_total

    return s

# Zhang's Distributional Consistency
# Reference: Zhang, H., Huang, C., & Yu, S. (2004). Distributional consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), Proceedings of Fourth International Conference on Language Resources and Evaluation (pp. 1119–1122). European Language Resources Association.
def zhangs_distributional_consistency(freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        dc = 0
    else:
        num_sections = len(freqs)

        dc = (
            numpy.sum(numpy.sqrt(freqs) / num_sections) ** 2
            / (freq_total / num_sections)
        )

    return dc
