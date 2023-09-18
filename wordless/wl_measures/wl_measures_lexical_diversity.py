# ----------------------------------------------------------------------
# Wordless: Measures - Lexical diversity
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import collections
import random

import numpy
import scipy

from wordless.wl_nlp import wl_nlp_utils

# Corrected TTR
# References:
#     Carroll, J. B. (1964). Language and thought. Prentice-Hall.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 26). Palgrave Macmillan.
def cttr(main, tokens):
    return len(set(tokens)) / numpy.sqrt(2 * len(tokens))

# Fisher's Index of Diversity
# Reference: Fisher, R. A., Steven, A. C., & Williams, C. B. (1943). The relation between the number of species and the number of individuals in a random sample of an animal population. Journal of Animal Ecology, 12(1), 42–58. https://doi.org/10.2307/1411
def fishers_index_of_diversity(main, tokens):
    num_tokens = len(tokens)
    num_types = len(set(tokens))

    alpha = -(
        (num_tokens * num_types)
        / (
            num_tokens
            * scipy.special.lambertw(-(
                numpy.exp(-(num_types / num_tokens))
                * num_types
                / num_tokens
            ), -1)
            + num_types
        )
    )

    return alpha.real

# Herdan's Vₘ
# Reference: Herdan, G. (1955). A new derivation and interpretation of Yule's ‘Characteristic’ K. Zeitschrift für Angewandte Mathematik und Physik (ZAMP), 6(4), 332–339. https://doi.org/10.1007/BF01587632
def herdans_vm(main, tokens):
    num_tokens = len(tokens)
    num_types = len(set(tokens))
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = collections.Counter(types_freqs.values())

    s2 = sum((
        num_types * (freq ** 2)
        for freq, num_types in freqs_nums_types.items()
    ))
    vm = s2 / (num_tokens ** 2) - 1 / num_types

    return vm

# HD-D
# Reference: McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods, 42(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
def hdd(main, tokens):
    sample_size = main.settings_custom['measures']['lexical_diversity']['hdd']['sample_size']

    num_tokens = len(tokens)
    tokens_freqs = collections.Counter(tokens)
    ttrs = numpy.empty(len(list(tokens_freqs)))

    for i, freq in enumerate(tokens_freqs.values()):
        ttrs[i] = scipy.stats.hypergeom.pmf(k = 0, M = num_tokens, n = freq, N = sample_size)

    # The probability that each type appears at least once in the sample
    ttrs = 1 - ttrs
    ttrs *= 1 / sample_size

    return sum(ttrs)

# LogTTR
# Herdan:
#     Herdan, G. (1960). Type-token mathematics: A textbook of mathematical linguistics (p. 28). Mouton.
# Somers:
#     Somers, H. H. (1966). Statistical methods in literary analysis. In J. Leeds (Ed.), The computer and literary style (pp. 128–140). Kent State University Press.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 28). Palgrave Macmillan.
# Rubet:
#     Dugast, D. (1979). Vocabulaire et stylistique: I théâtre et dialogue, travaux de linguistique quantitative. Slatkine.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 28). Palgrave Macmillan.
# Maas:
#     Maas, H.-D. (1972). Über den zusammenhang zwischen wortschatzumfang und länge eines textes. Zeitschrift für Literaturwissenschaft und Linguistik, 2(8), 73–96.
# Dugast:
#     Dugast, D. (1978). Sur quoi se fonde la notion d’étendue théoretique du vocabulaire?. Le Français Moderne, 46, 25–32.
#     Dugast, D. (1979). Vocabulaire et stylistique: I théâtre et dialogue, travaux de linguistique quantitative. Slatkine.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 28). Palgrave Macmillan.
def logttr(main, tokens):
    variant = main.settings_custom['measures']['lexical_diversity']['logttr']['variant']

    num_types = len(set(tokens))
    num_tokens = len(tokens)

    if variant == 'Herdan':
        logttr = numpy.log(num_types) / numpy.log(num_tokens)
    elif variant == 'Somers':
        logttr = numpy.log(numpy.log(num_types)) / numpy.log(numpy.log(num_tokens))
    elif variant == 'Rubet':
        logttr = numpy.log(num_types) / numpy.log(numpy.log(num_tokens))
    elif variant == 'Maas':
        logttr = (numpy.log(num_tokens) - numpy.log(num_types)) / (numpy.log(num_tokens) ** 2)
    elif variant == 'Dugast':
        logttr = (numpy.log(num_tokens) ** 2) / (numpy.log(num_tokens) - numpy.log(num_types))

    return logttr

# Mean Segmental TTR
# References:
#     Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
#     McCarthy, P. M. (2005). An assessment of the range and usefulness of lexical diversity measures and the potential of the measure of textual, lexical diversity (MTLD) [Doctoral dissertation, The University of Memphis] (p. 37). ProQuest Dissertations and Theses Global.
def msttr(main, tokens):
    num_tokens_seg = main.settings_custom['measures']['lexical_diversity']['msttr']['num_tokens_in_each_seg']

    ttrs = [
        len(set(tokens_seg)) / num_tokens_seg
        for tokens_seg in wl_nlp_utils.to_sections_unequal(tokens, num_tokens_seg)
        # Discard the last segment of text if its length is shorter than other segments
        if len(tokens_seg) == num_tokens_seg
    ]

    if ttrs:
        msttr = numpy.mean(ttrs)
    else:
        msttr = 0

    return msttr

# Measure of Textual Lexical Diversity
# References:
#     McCarthy, P. M. (2005). An assessment of the range and usefulness of lexical diversity measures and the potential of the measure of textual, lexical diversity (MTLD) [Doctoral dissertation, The University of Memphis] (pp. 95–96, 99–100). ProQuest Dissertations and Theses Global.
#     McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods, 42(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
def mtld(main, tokens):
    mtlds = numpy.empty(shape = 2)
    factor_size = main.settings_custom['measures']['lexical_diversity']['mtld']['factor_size']
    num_tokens = len(tokens)

    for i in range(2):
        num_factors = 0
        counter = collections.Counter()

        # Backward MTLD
        if i == 1:
            tokens = reversed(tokens)

        for j, token in enumerate(tokens):
            counter[token] += 1
            num_types_counter = len(list(counter))
            ttr = num_types_counter / counter.total()

            if ttr <= factor_size:
                num_factors += 1

                counter.clear()
            # The last incomplete factor
            elif j == num_tokens - 1:
                if factor_size < 1:
                    num_factors += (1 - ttr) / (1 - factor_size)

        mtlds[i] = num_tokens / num_factors

    return numpy.mean(mtlds)

# Moving-average TTR
# Reference: Covington, M. A., & McFall, J. D. (2010). Cutting the Gordian knot: The moving-average type-token ratio (MATTR). Journal of Quantitative Linguistics, 17(2), 94–100. https://doi.org/10.1080/09296171003643098
def mattr(main, tokens):
    window_size = main.settings_custom['measures']['lexical_diversity']['mattr']['window_size']

    num_tokens = len(tokens)
    num_windows = max(1, num_tokens - window_size + 1)
    ttrs = numpy.empty(shape = num_windows)

    counter = collections.Counter(tokens[:window_size])

    ttrs[0] = len(list(counter)) / counter.total()

    if num_windows > 1:
        for i in range(num_windows - 1):
            counter[tokens[window_size + i]] += 1
            counter[tokens[i]] -= 1

            if counter[tokens[i]] == 0:
                counter.pop(tokens[i])

            ttrs[i + 1] = len(list(counter))

        ttrs[1:] /= window_size

    return numpy.mean(ttrs)

# Popescu's R₁
# Reference: Popescu, I.-I. (2009). Word frequency studies (pp. 18, 30, 33). Mouton de Gruyter.
def popescus_r1(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    ranks_freqs = [
        (i + 1, freq)
        for i, freq in enumerate(sorted(types_freqs.values(), reverse = True))
    ]

    h = 0

    for rank, freq in ranks_freqs:
        if rank == freq:
            h = rank

            break

    if not h:
        cs = [1 / (freq - rank) for rank, freq in ranks_freqs]
        c_max = max(cs)
        c_min = min(cs)
        r_max = ranks_freqs[cs.index(c_max)][0]
        r_min = ranks_freqs[cs.index(c_min)][0]
        h = (c_min * r_max - c_max * r_min) / (c_min - c_max)

    f_h = sum((freq for _, freq in ranks_freqs[:int(numpy.floor(h))])) / num_tokens
    r1 = 1 - (f_h - numpy.square(h) / (2 * num_tokens))

    return r1

# Popescu's R₂
# Reference: Popescu, I.-I. (2009). Word frequency studies (pp. 35–36, 38). Mouton de Gruyter.
def popescus_r2(main, tokens):
    num_types_all = len(set(tokens))
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = sorted(collections.Counter(types_freqs.values()).items())

    k = 0

    for freq, num_types in freqs_nums_types:
        if freq == num_types:
            k = freq

            break

    if not k:
        cs = [1 / (num_types - freq) for freq, num_types in freqs_nums_types]
        c_max = max(cs)
        c_min = min(cs)
        freq_max = freqs_nums_types[cs.index(c_max)][0]
        freq_min = freqs_nums_types[cs.index(c_min)][0]
        k = (c_min * freq_max - c_max * freq_min) / (c_min - c_max)

    g_k = sum((num_types for freq, num_types in freqs_nums_types if freq <= numpy.floor(k))) / num_types_all
    r2 = g_k - numpy.square(k) / (2 * num_types_all)

    return r2

# Popescu's R₃
# Reference: Popescu, I.-I. (2009). Word frequency studies (pp. 48–49, 53). Mouton de Gruyter.
def popescus_r3(main, tokens):
    num_tokens = len(tokens)
    num_types = len(set(tokens))
    types_freqs = collections.Counter(tokens)
    ranks_freqs = [
        (i + 1, freq)
        for i, freq in enumerate(sorted(types_freqs.values(), reverse = True))
    ]

    rs_rel = numpy.empty(shape = num_types)
    fs_rel = numpy.empty(shape = num_types)
    freq_cum = 0

    for i, (rank, freq) in enumerate(ranks_freqs):
        freq_cum += freq

        rs_rel[i] = rank
        fs_rel[i] = freq_cum

    rs_rel /= num_types
    fs_rel /= num_tokens

    drs = numpy.sqrt(numpy.square(rs_rel) + numpy.square(1 - fs_rel))
    m = numpy.argmin(drs) + 1 # m refers to rank
    fm = fs_rel[m - 1]
    r3 = 1 - fm

    return r3

# Popescu's R₄
# Reference: Popescu, I.-I. (2009). Word frequency studies (p. 57). Mouton de Gruyter.
def popescus_r4(main, tokens):
    num_tokens = len(tokens)
    num_types = len(set(tokens))
    types_freqs = collections.Counter(tokens)

    ranks = numpy.empty(shape = num_types)
    freqs = numpy.empty(shape = num_types)

    for i, freq in enumerate(sorted(types_freqs.values(), reverse = True)):
        ranks[i] = i + 1
        freqs[i] = freq

    r4 = 1 - (num_types + 1 - 2 / num_tokens * numpy.sum(ranks * freqs)) / num_types

    return r4

# Root TTR
# References:
#     Guiraud, P. (1954). Les caractères statistiques du vocabulaire: Essai de méthodologie. Presses universitaires de France.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 26). Palgrave Macmillan.
def rttr(main, tokens):
    return len(set(tokens)) / numpy.sqrt(len(tokens))

# Simpson's l
# Reference: Simpson, E. H. (1949). Measurement of diversity. Nature, 163, p. 688. https://doi.org/10.1038/163688a0
def simpsons_l(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = collections.Counter(types_freqs.values())

    s2 = sum((
        num_types * (freq ** 2)
        for freq, num_types in freqs_nums_types.items()
    ))
    l = (s2 - num_tokens) / (num_tokens * (num_tokens - 1))

    return l

# Type-token Ratio
# Reference: Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
def ttr(main, tokens):
    return len(set(tokens)) / len(tokens)

# vocd-D
# Reference: Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (pp. 51, 56–57). Palgrave Macmillan.
def vocdd(main, tokens):
    def ttr(n, d):
        return (d / n) * (numpy.sqrt(1 + 2 * n / d) - 1)

    num_tokens = len(tokens)
    ttr_ys = numpy.empty(shape = 16)

    for i, n in enumerate(range(35, 51)):
        ttrs = numpy.empty(shape = 100)

        for j in range(100):
            if n <= num_tokens:
                sample = random.sample(tokens, k = n)
            else:
                sample = tokens

            ttrs[j] = len(set(sample)) / len(sample)

        ttr_ys[i] = numpy.mean(ttrs)

    popt, _ = scipy.optimize.curve_fit( # pylint: disable=unbalanced-tuple-unpacking
        f = ttr,
        xdata = numpy.array(range(35, 51)),
        ydata = ttr_ys
    )

    return popt[0]

# Yule's Characteristic K
# Reference: Yule, G. U. (1944). The statistical study of literary vocabulary (pp. 52–53). Cambridge University Press.
def yules_characteristic_k(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = collections.Counter(types_freqs.values())

    s2 = sum((
        num_types * (freq ** 2)
        for freq, num_types in freqs_nums_types.items()
    ))
    k = 10000 * ((s2 - num_tokens) / (num_tokens ** 2))

    return k

# Yule's Index of Diversity
# Reference: Williams, C. B. (1970). Style and vocabulary: Numerical studies (p. 100). Griffin.
def yules_index_of_diversity(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = collections.Counter(types_freqs.values())

    s2 = sum((
        num_types * (freq ** 2)
        for freq, num_types in freqs_nums_types.items()
    ))
    index_of_diversity = (num_tokens ** 2) / (s2 - num_tokens)

    return index_of_diversity
