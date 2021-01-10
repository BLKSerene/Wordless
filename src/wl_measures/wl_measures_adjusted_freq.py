#
# Wordless: Measures - Adjusted Frequency
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
import scipy.special

from wl_measures import wl_measures_dispersion

# Euler-Mascheroni Constant
C = -scipy.special.digamma(1)

def juillands_u(freqs):
    d = wl_measures_dispersion.juillands_d(freqs)
    u = max(0, d) * sum(freqs)

    return u

def carrolls_um(freqs):
    freq_total = sum(freqs)

    d2 = wl_measures_dispersion.carrolls_d2(freqs)
    um = freq_total * d2 + (1 - d2) * freq_total / len(freqs)

    return um

def rosengrens_kf(freqs):
    return sum([math.sqrt(freq) for freq in freqs]) ** 2 / len(freqs)

def engwalls_fm(freqs):
    return sum(freqs) * len([freq for freq in freqs if freq]) / len(freqs)

def kromers_ur(freqs):
    return sum([scipy.special.digamma(freq + 1) + C for freq in freqs])
