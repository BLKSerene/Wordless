# ----------------------------------------------------------------------
# Wordless: Measures - Dispersion
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
import scipy.stats

from wordless.wl_measures import wl_measures_adjusted_freq

def _get_dists(tokens, search_term):
    positions = numpy.array([i for i, token in enumerate(tokens) if token == search_term])

    if positions.size > 0:
        dists = positions[1:] - positions[:-1]
        # Prepend the distance between the first and last occurrences
        dists = numpy.insert(dists, 0, positions[0] + (len(tokens) - positions[-1]))
    else:
        dists = numpy.array([])

    return dists

# Average logarithmic distance
# Reference: Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. Journal of Quantitative Linguistics, 9(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
def ald(main, tokens, search_term):
    dists = _get_dists(tokens, search_term)

    if dists.size > 0:
        ald = numpy.sum(dists * numpy.log10(dists)) / len(tokens)
    else:
        ald = 0

    return ald

# Average reduced frequency
# Reference: Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. Journal of Quantitative Linguistics, 9(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
def arf(main, tokens, search_term):
    dists = _get_dists(tokens, search_term)

    if dists.size > 0:
        v = len(tokens) / dists.size
        arf = numpy.sum(numpy.minimum(dists, v)) / v
    else:
        arf = 0

    return arf

# Average waiting time
# Reference: Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. Journal of Quantitative Linguistics, 9(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
def awt(main, tokens, search_term):
    dists = _get_dists(tokens, search_term)

    if dists.size > 0:
        awt = 0.5 * (1 + numpy.sum(numpy.square(dists)) / len(tokens))
    else:
        awt = 0

    return awt

# Carroll's D₂
# Reference: Carroll, J. B. (1970). An alternative to Juillands's usage coefficient for lexical frequencies. ETS Research Bulletin Series, 1970(2), i–15. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def carrolls_d2(main, freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        d2 = 0
    else:
        h = numpy.sum(freqs * numpy.log(freqs, out = numpy.zeros_like(freqs, dtype = numpy.float64), where = freqs != 0))
        h = numpy.log(freq_total) - h / freq_total
        d2 = h / numpy.log(len(freqs))

    return d2

# Gries's DP
# References:
#     Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri
#     Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora”. International Journal of Corpus Linguistics, 17(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij
def griess_dp(main, freqs):
    freqs = numpy.array(freqs)
    apply_normalization = main.settings_custom['measures']['dispersion']['griess_dp']['apply_normalization']

    if (freq_total := numpy.sum(freqs)) == 0:
        dp = 0
    else:
        num_sections = len(freqs)

        dp = numpy.sum([
            numpy.abs(freq / freq_total - 1 / num_sections)
            for freq in freqs
        ]) / 2

        if apply_normalization:
            dp /= 1 - 1 / len(freqs)

    return dp

# Juilland's D
# Reference: Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of Spanish words. Mouton. | p. LIII
def juillands_d(main, freqs):
    freqs = numpy.array(freqs)

    if numpy.sum(freqs) == 0 or len(freqs) == 1:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
        d = 1 - cv / numpy.sqrt(len(freqs) - 1)

    return max(0, d)

# Lyne's D₃
# Reference: Lyne, A. A. (1985). The vocabulary of French business correspondence: Word frequencies, collocations, and problems of lexicometric method. Slatkine. | p. 129
def lynes_d3(main, freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        d3 = 0
    else:
        d3 = 1 - scipy.stats.chisquare(freqs)[0] / (4 * freq_total)

    return max(0, d3)

# Rosengren's S
# Reference: Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127.
def rosengrens_s(main, freqs):
    freqs = numpy.array(freqs)

    if (freq_total := numpy.sum(freqs)) == 0:
        s = 0
    else:
        kf = wl_measures_adjusted_freq.rosengrens_kf(main, freqs)
        s = kf / freq_total

    return s

# Zhang's Distributional Consistency
# Reference: Zhang, H., Huang, C., & Yu, S. (2004). Distributional Consistency: As a general method for defining a core lexicon. In M. T. Lino, M. F. Xavier, F. Ferreira, R. Costa, & R. Silva (Eds.), Proceedings of Fourth International Conference on Language Resources and Evaluation (pp. 1119–1122). European Language Resources Association.
def zhangs_distributional_consistency(main, freqs):
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
