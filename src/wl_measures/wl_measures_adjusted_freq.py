#
# Wordless: Measures - Adjusted Frequency
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

import numpy
import scipy.special

from wl_measures import wl_measures_dispersion

# Euler-Mascheroni Constant
C = -scipy.special.digamma(1)

# Carroll's Um
# Reference: Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def carrolls_um(freqs):
    freq_total = sum(freqs)

    d2 = wl_measures_dispersion.carrolls_d2(freqs)
    um = freq_total * d2 + (1 - d2) * freq_total / len(freqs)

    return um

# Engwall's FM
# Reference: Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University.
def juillands_u(freqs):
    d = wl_measures_dispersion.juillands_d(freqs)
    u = max(0, d) * sum(freqs)

    return u

# Juilland's U
# Reference: Juilland, A., & Chang-Rodriguez, E. (1964). Frequency dictionary of spanish words. Mouton.
def rosengrens_kf(freqs):
    return sum([math.sqrt(freq) for freq in freqs]) ** 2 / len(freqs)

# Kromer's UR
# Reference: Kromer, V. (2003). A usage measure based on psychophysical relations. Journal of Quatitative Linguistics, 10(2), 177–186. https://doi.org/10.1076/jqul.10.2.177.16718
def engwalls_fm(freqs):
    return sum(freqs) * len([freq for freq in freqs if freq]) / len(freqs)

# Rosengren's KF
# Reference: Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127.
def kromers_ur(freqs):
    return sum([scipy.special.digamma(freq + 1) + C for freq in freqs])
