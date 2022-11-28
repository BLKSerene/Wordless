# ----------------------------------------------------------------------
# Wordless: Measures - Adjusted Frequency
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

# pylint: disable=unused-argument

import numpy
import scipy.special

from wordless.wl_measures import wl_measures_dispersion

# Euler-Mascheroni Constant
C = -scipy.special.digamma(1)

def to_freq_sections_items(main, items_search, items):
    num_sub_sections = main.settings_custom['measures']['adjusted_freq']['general_settings']['num_sub_sections']

    return wl_measures_dispersion._to_freq_sections_items(items_search, items, num_sub_sections)

# Carroll's Um
# Reference: Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def carrolls_um(main, freqs):
    freq_total = sum(freqs)

    d2 = wl_measures_dispersion.carrolls_d2(main, freqs)
    um = freq_total * d2 + (1 - d2) * freq_total / len(freqs)

    return um

# Engwall's FM
# Reference: Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University.
def juillands_u(main, freqs):
    d = wl_measures_dispersion.juillands_d(main, freqs)
    u = max(0, d) * sum(freqs)

    return u

# Juilland's U
# Reference: Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of Spanish words. Mouton.
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
