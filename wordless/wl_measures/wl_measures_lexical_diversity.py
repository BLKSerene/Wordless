# ----------------------------------------------------------------------
# Wordless: Measures - Lexical diversity
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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
from PyQt5.QtCore import QCoreApplication
import scipy

from wordless.wl_nlp import wl_nlp_utils

_tr = QCoreApplication.translate

# Brunét's Index
# References:
#     Brunét, E. (1978). Le vocabulaire de Jean Giraudoux: Structure et evolution. Slatkine.
#     Bucks, R. S., Singh, S., Cuerden, J. M., & Wilcock, G. K. (2000). Analysis of spontaneous, conversational speech in dementia of Alzheimer type: Evaluation of an objective technique for analysing lexical performance. Aphasiology, 14(1), 71–91. https://doi.org/10.1080/026870300401603
def brunets_index(main, tokens):
    return numpy.power(len(tokens), numpy.power(len(set(tokens)), -0.165))

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

    lambertw_x = -(
        numpy.exp(-(num_types / num_tokens))
        * num_types
        / num_tokens
    )

    if lambertw_x > -numpy.exp(-1):
        alpha = -(
            (num_tokens * num_types)
            / (
                num_tokens
                * scipy.special.lambertw(lambertw_x, -1).real
                + num_types
            )
        )
    else:
        alpha = 0

    return alpha

# Herdan's Vₘ
# Reference: Herdan, G. (1955). A new derivation and interpretation of Yule's ‘Characteristic’ K. Zeitschrift für Angewandte Mathematik und Physik (ZAMP), 6(4), 332–339. https://doi.org/10.1007/BF01587632
def herdans_vm(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    num_types = len(types_freqs)
    freqs_nums_types = collections.Counter(types_freqs.values())

    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))
    s2 = numpy.sum(nums_types * numpy.square(freqs))
    vm = s2 / (num_tokens ** 2) - 1 / num_types

    return vm

# HD-D
# Reference: McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods, 42(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
def hdd(main, tokens):
    sample_size = main.settings_custom['measures']['lexical_diversity']['hdd']['sample_size']

    num_tokens = len(tokens)
    tokens_freqs = collections.Counter(tokens)
    ttrs = numpy.empty(len(list(tokens_freqs)))

    # Short texts
    if num_tokens < sample_size:
        sample_size = num_tokens

    for i, freq in enumerate(tokens_freqs.values()):
        ttrs[i] = scipy.stats.hypergeom.pmf(k = 0, M = num_tokens, n = freq, N = sample_size)

    # The probability that each type appears at least once in the sample
    ttrs = 1 - ttrs
    ttrs *= 1 / sample_size

    return sum(ttrs)

# Honoré's statistic
# References:
#     Honoré, A. (1979). Some simple measures of richness of vocabulary. Association of Literary and Linguistic Computing Bulletin, 7(2), 172–177.
#     Bucks, R. S., Singh, S., Cuerden, J. M., & Wilcock, G. K. (2000). Analysis of spontaneous, conversational speech in dementia of Alzheimer type: Evaluation of an objective technique for analysing lexical performance. Aphasiology, 14(1), 71–91. https://doi.org/10.1080/026870300401603
def honores_stat(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    num_types = len(types_freqs)
    freqs_nums_types = collections.Counter(types_freqs.values())

    if (denominator := 1 - freqs_nums_types[1] / num_types):
        r = 100 * numpy.log(num_tokens / denominator)
    else:
        r = 0

    return r

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

        if num_factors:
            mtlds[i] = num_tokens / num_factors
        else:
            mtlds[i] = 0

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

# Popescu-Mačutek-Altmann's B₁/B₂/B₃/B₄/B₅
# Reference: Popescu I.-I., Mačutek, J, & Altmann, G. (2008). Word frequency and arc length. Glottometrics, 17, 18–42.
def popescu_macutek_altmanns_b1_b2_b3_b4_b5(main, tokens):
    types_freqs = collections.Counter(tokens)
    num_types = len(types_freqs)
    freqs = numpy.array(sorted(types_freqs.values(), reverse = True))
    freqs_nums_types = collections.Counter(types_freqs.values())

    l = numpy.sum(numpy.sqrt(numpy.square(freqs[:-1] - freqs[1:]) + 1))
    l_min = numpy.sqrt(numpy.square(num_types - 1) + numpy.square(freqs[0] - 1))
    l_max = numpy.sqrt(numpy.square(freqs[0] - 1) + 1) + num_types - 2

    b1 = l / l_max

    if (divisor := l_max - l_min):
        b2 = (l - l_min) / divisor
    else:
        b2 = 0

    b3 = (num_types - 1) / l
    b4 = (freqs[0] - 1) / l
    b5 = freqs_nums_types[1] / l

    return b1, b2, b3, b4, b5

# Popescu's R₁
# Reference: Popescu, I.-I. (2009). Word frequency studies (pp. 18, 30, 33). Mouton de Gruyter.
def popescus_r1(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    num_types = len(types_freqs)
    ranks = numpy.empty(shape = num_types)
    freqs = numpy.empty(shape = num_types)

    for i, freq in enumerate(sorted(types_freqs.values(), reverse = True)):
        ranks[i] = i + 1
        freqs[i] = freq

    h = 0

    for rank, freq in zip(ranks, freqs):
        if rank == freq:
            h = rank

            break

    if not h:
        cs = 1 / (freqs - ranks)
        i_max = numpy.argmax(cs)
        i_min = numpy.argmin(cs)
        c_max = cs[i_max]
        c_min = cs[i_min]
        r_max = ranks[i_max]
        r_min = ranks[i_min]
        h = (c_min * r_max - c_max * r_min) / (c_min - c_max)

    f_h = numpy.sum(freqs[:int(numpy.floor(h))]) / num_tokens
    r1 = 1 - (f_h - numpy.square(h) / (2 * num_tokens))

    return r1

# Popescu's R₂
# Reference: Popescu, I.-I. (2009). Word frequency studies (pp. 35–36, 38). Mouton de Gruyter.
def popescus_r2(main, tokens):
    num_types_all = len(set(tokens))
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = sorted(collections.Counter(types_freqs.values()).items())
    freqs = numpy.array([freq for freq, _ in freqs_nums_types])
    nums_types = numpy.array([num_types for _, num_types in freqs_nums_types])

    k = 0

    for freq, num_types in freqs_nums_types:
        if freq == num_types:
            k = freq

            break

    if not k:
        cs = 1 / (nums_types - freqs)
        i_max = numpy.argmax(cs)
        i_min = numpy.argmin(cs)
        c_max = cs[i_max]
        c_min = cs[i_min]
        freq_max = freqs[i_max]
        freq_min = freqs[i_min]

        if (divisor := c_min - c_max):
            k = (c_min * freq_max - c_max * freq_min) / divisor
        else:
            k = 0

    g_k = numpy.sum([num_types for freq, num_types in freqs_nums_types if freq <= numpy.floor(k)]) / num_types_all
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

# Repeat Rate
# Reference: Popescu, I.-I. (2009). Word frequency studies (p. 166). Mouton de Gruyter.
def repeat_rate(main, tokens):
    use_data = main.settings_custom['measures']['lexical_diversity']['repeat_rate']['use_data']

    num_tokens = len(tokens)
    num_types = len(set(tokens))
    types_freqs = collections.Counter(tokens)

    if use_data == _tr('wl_measures_lexical_diversity', 'Rank-frequency distribution'):
        freqs = numpy.array(list(types_freqs.values()))

        rr = numpy.sum(numpy.square(freqs)) / numpy.square(num_tokens)
    elif use_data == _tr('wl_measures_lexical_diversity', 'Frequency spectrum'):
        nums_types = numpy.array(list(collections.Counter(types_freqs.values()).values()))

        rr = numpy.sum(numpy.square(nums_types)) / numpy.square(num_types)

    return rr

# Root TTR
# References:
#     Guiraud, P. (1954). Les caractères statistiques du vocabulaire: Essai de méthodologie. Presses universitaires de France.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 26). Palgrave Macmillan.
def rttr(main, tokens):
    return len(set(tokens)) / numpy.sqrt(len(tokens))

# Shannon Entropy
# Reference: Popescu, I.-I. (2009). Word frequency studies (p. 173). Mouton de Gruyter.
def shannon_entropy(main, tokens):
    use_data = main.settings_custom['measures']['lexical_diversity']['shannon_entropy']['use_data']

    num_tokens = len(tokens)
    num_types = len(set(tokens))
    types_freqs = collections.Counter(tokens)

    if use_data == _tr('wl_measures_lexical_diversity', 'Rank-frequency distribution'):
        freqs = numpy.array(list(types_freqs.values()))
        ps = freqs / num_tokens
    elif use_data == _tr('wl_measures_lexical_diversity', 'Frequency spectrum'):
        nums_types = numpy.array(list(collections.Counter(types_freqs.values()).values()))
        ps = nums_types / num_types

    h = -numpy.sum(ps * numpy.log2(ps))

    return h

# Simpson's l
# Reference: Simpson, E. H. (1949). Measurement of diversity. Nature, 163, p. 688. https://doi.org/10.1038/163688a0
def simpsons_l(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = collections.Counter(types_freqs.values())
    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))

    s2 = numpy.sum(nums_types * numpy.square(freqs))
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
    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))

    s2 = numpy.sum(nums_types * numpy.square(freqs))
    k = 10000 * ((s2 - num_tokens) / (num_tokens ** 2))

    return k

# Yule's Index of Diversity
# Reference: Williams, C. B. (1970). Style and vocabulary: Numerical studies (p. 100). Griffin.
def yules_index_of_diversity(main, tokens):
    num_tokens = len(tokens)
    types_freqs = collections.Counter(tokens)
    freqs_nums_types = collections.Counter(types_freqs.values())
    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))

    s2 = numpy.sum(nums_types * numpy.square(freqs))

    if (divisor := s2 - num_tokens):
        index_of_diversity = (num_tokens ** 2) / divisor
    else:
        index_of_diversity = 0

    return index_of_diversity
