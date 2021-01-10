#
# Wordless: Measures - Effect Size
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

def get_marginals(c11, c12, c21, c22):
    c1x = c11 + c12
    c2x = c21 + c22
    cx1 = c11 + c21
    cx2 = c12 + c22
    cxx = c11 + c12 + c21 + c22

    return (c1x, c2x, cx1, cx2, cxx)

def get_expected(c1x, c2x, cx1, cx2, cxx):
    e11 = c1x * cx1 / cxx
    e12 = c1x * cx2 / cxx
    e21 = c2x * cx1 / cxx
    e22 = c2x * cx2 / cxx

    return (e11, e12, e21, e22)

def pmi(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 / e11, 2)

def md(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 ** 2 / e11, 2)

def lfmd(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        return 0
    elif e11 == 0:
        return math.log(c11, 2)
    else:
        return math.log(c11 ** 2 / e11, 2) + math.log(c11, 2)

def im3(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 ** 3 / e11, 2)

def mi_log_f(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 ** 2 / e11, 2) * math.log(c11 + 1, math.e)

def mi(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        mi11 = 0
    else:
        mi11 = (c11 / cxx) * math.log(c11 / e11, 2)

    if c12 == 0 or e12 == 0:
        mi12 = 0
    else:
        mi12 = (c12 / cxx) * math.log(c12 / e12, 2)

    if c21 == 0 or e21 == 0:
        mi21 = 0
    else:
        mi21 = (c21 / cxx) * math.log(c21 / e21, 2)

    if c22 == 0 or e22 == 0:
        mi22 = 0
    else:
        mi22 = (c22 / cxx) * math.log(c22 / e22, 2)

    return mi11 + mi12 + mi21 + mi22

def squared_phi_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c1x == 0 or cx1 == 0:
        return 0
    else:
        return (c11 * c22 - c12 * c21) ** 2 / (c1x * c2x * cx1 * cx2)

def dices_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c1x + cx1 == 0:
        return 0
    else:
        return 2 * c11 / (c1x + cx1)

def log_dice(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c11 == 0 or c1x + cx1 == 0:
        return 14
    else:
        return 14 + math.log(2 * c11 / (c1x + cx1), 2)

def me(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if cx1 + c1x == 0:
        return 0
    else:
        return c11 * (2 * c11 / (c1x + cx1))

def jaccard_index(main, c11, c12, c21, c22):
    if c11 + c12 + c21 == 0:
        return 0
    else:
        return c11 / (c11 + c12 + c21)

def min_sensitivity(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c1x == 0:
        s1 = 0
    else:
        s1 = c11 / c1x

    if cx1 == 0:
        s2 = 0
    else:
        s2 = c11 / cx1

    return min(s1, s2)

def poisson_collocation_measure(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        log_c11 = 0
    else:
        log_c11 = math.log(c11)

    if e11 == 0:
        log_e11 = 0
    else:
        log_e11 = math.log(e11)

    return (c11 * (log_c11 - log_e11 - 1)) / math.log(cxx)

def kilgarriffs_ratio(main, c11, c12, c21, c22):
    smoothing_param = main.settings_custom['measures']['effect_size']['kilgarriffs_ratio']['smoothing_param']

    if c11 + c21 == 0:
        relative_freq_observed = 0
    else:
        relative_freq_observed = c11 / (c11 + c21) * 1000000

    if c12 + c22 == 0:
        relative_freq_ref = 0
    else:
        relative_freq_ref = c12 / (c12 + c22) * 1000000

    return (relative_freq_observed + smoothing_param) / (relative_freq_ref + smoothing_param)

def odds_ratio(main, c11, c12, c21, c22):
    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return (c11 * c22) / (c12 * c21)

def log_ratio(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return math.log((c11 / cx1) / (c12 / cx2), 2)

def diff_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    return (c11 / cx1 - c12 / cx2) / (c11 / cx1 + c12 / cx2)

def pct_diff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return ((c11 / cx1 - c12 / cx2) * 100) / (c12 / cx2)
