# ----------------------------------------------------------------------
# Wordless: Measures - Adjusted frequency
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
import scipy.special

from wordless.wl_measures import wl_measures_dispersion

# Euler-Mascheroni Constant
C = -scipy.special.digamma(1)

# Average logarithmic distance
# Reference: Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. Journal of Quantitative Linguistics, 9(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
def fald(main, tokens, search_term):
    dists = wl_measures_dispersion._get_dists(tokens, search_term)

    if dists.size > 0:
        len_tokens = len(tokens)
        fald = numpy.exp(-numpy.sum((dists / len_tokens) * numpy.log(dists / len_tokens)))
    else:
        fald = 0

    return fald

# Average reduced frequency
# Reference: Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. Journal of Quantitative Linguistics, 9(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
def farf(main, tokens, search_term):
    return wl_measures_dispersion.arf(main, tokens, search_term)

# Average waiting time
# Reference: Savický, P., & Hlaváčová, J. (2002). Measures of word commonness. Journal of Quantitative Linguistics, 9(3), 215–231. https://doi.org/10.1076/jqul.9.3.215.14124
def fawt(main, tokens, search_term):
    dists = wl_measures_dispersion._get_dists(tokens, search_term)

    if dists.size > 0:
        fawt = len(tokens)**2 / numpy.sum(numpy.square(dists))
    else:
        fawt = 0

    return fawt

# Carroll's Um
# Reference: Carroll, J. B. (1970). An alternative to Juillands's usage coefficient for lexical frequencies. ETS Research Bulletin Series, 1970(2), i–15. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def carrolls_um(main, freqs):
    freq_total = sum(freqs)

    d2 = wl_measures_dispersion.carrolls_d2(main, freqs)
    um = freq_total * d2 + (1 - d2) * freq_total / len(freqs)

    return um

# Engwall's FM
# Reference: Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University. | p. 53
def juillands_u(main, freqs):
    d = wl_measures_dispersion.juillands_d(main, freqs)
    u = max(0, d) * sum(freqs)

    return u

# Juilland's U
# Reference: Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of Spanish words. Mouton. | p. LXVIII
def rosengrens_kf(main, freqs):
    return numpy.sum(numpy.sqrt(freqs)) ** 2 / len(freqs)

# Kromer's UR
# Reference: Kromer, V. (2003). A usage measure based on psychophysical relations. Journal of Quantitative Linguistics, 10(2), 177–186. https://doi.org/10.1076/jqul.10.2.177.16718
def engwalls_fm(main, freqs):
    return sum(freqs) * len([freq for freq in freqs if freq]) / len(freqs)

# Rosengren's KF
# Reference: Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127.
def kromers_ur(main, freqs):
    return sum((scipy.special.digamma(freq + 1) + C for freq in freqs))
