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

def juillands_d(freqs):
    if sum(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
    
        d = 1 - cv / math.sqrt(len(freqs) - 1)

    return max(0, d)

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

def lynes_d3(freqs):
    if sum(freqs) == 0:
        d3 = 0
    else:
        d3 = 1 - scipy.stats.chisquare(freqs)[0] / (4 * sum(freqs))

    return max(0, d3)

def rosengrens_s(freqs):
    if sum(freqs) == 0:
        s = 0
    else:
        kf = wl_measures_adjusted_freq.rosengrens_kf(freqs)
        s = kf / sum(freqs)

    return s

def zhangs_distributional_consistency(freqs):
    if sum(freqs) == 0:
        dc = 0
    else:
        num_sections = len(freqs)

        dc = ((sum([math.sqrt(freq) for freq in freqs]) / num_sections) ** 2 /
              (sum(freqs) / num_sections))

    return dc

def griess_dp(freqs):
    num_sections = len(freqs)
    freq_total = sum(freqs)

    if freq_total == 0:
        dp = 0
    else:
        dp = sum([abs(freq / freq_total - 1 / num_sections)
                  for freq in freqs]) / 2

    return dp

def griess_dp_norm(freqs):
    return griess_dp(freqs) / (1 - 1 / len(freqs))
