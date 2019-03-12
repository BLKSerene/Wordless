#
# Wordless: Measures - Adjusted Frequency
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

import numpy
import scipy.special

from wordless_measures import wordless_measures_dispersion

# Euler-Mascheroni Constant
C = -scipy.special.digamma(1)

# Reference:
#     Juilland, Alphonse and Eugenio Chang-Rodriguez. Frequency Dictionary of Spanish Words, Mouton, 1964.
def juillands_u(freqs):
    d = wordless_measures_dispersion.juillands_d(freqs)
    u = max(0, d) * sum(freqs)

    return u

# Reference:
#     Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
def carrolls_um(freqs):
    freq_total = sum(freqs)

    d2 = wordless_measures_dispersion.carrolls_d2(freqs)
    um = freq_total * d2 + (1 - d2) * freq_total / len(freqs)

    return um

# Reference:
#     Rosengren, Inger. "The Quantitative Concept of Language and Its Relation to The Structure of Frequency Dictionaries." Études De Linguistique Appliquée, n.s.1, 1971, pp. 103-27.
def rosengrens_kf(freqs):
    return sum([math.sqrt(freq) for freq in freqs]) ** 2 / len(freqs)

# Reference:
#     Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français." Dissertation, Stockholm University, 1974.
def engwalls_fm(freqs):
    return sum(freqs) * len([freq for freq in freqs if freq]) / len(freqs)

# Reference:
#     Kromer, Victor. "A Usage Measure Based on Psychophysical Relations." Journal of Quatitative Linguistics, vol. 10, no. 2, 2003, pp. 177-186.
def kromers_ur(freqs):
    return sum([scipy.special.digamma(freq + 1) + C for freq in freqs])
