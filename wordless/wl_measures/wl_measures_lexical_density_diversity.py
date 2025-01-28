# ----------------------------------------------------------------------
# Wordless: Measures - Lexical density/diversity
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

import collections
import random

import numpy
from PyQt5.QtCore import QCoreApplication
import scipy

from wordless.wl_nlp import wl_nlp_utils, wl_pos_tagging

_tr = QCoreApplication.translate

# Brunet's index
# Reference: Brunet, E. (1978). Le vocabulaire de Jean Giraudoux: Structure et evolution. Slatkine. | p. 57
def brunets_index(main, text):
    return numpy.power(text.num_tokens, numpy.power(text.num_types, -0.172))

# Corrected TTR
# Reference: Carroll, J. B. (1964). Language and thought. Prentice-Hall. | p. 54
def cttr(main, text):
    return text.num_types / numpy.sqrt(2 * text.num_tokens)

# Fisher's Index of Diversity
# Reference: Fisher, R. A., Steven, A. C., & Williams, C. B. (1943). The relation between the number of species and the number of individuals in a random sample of an animal population. Journal of Animal Ecology, 12(1), 42–58. https://doi.org/10.2307/1411
def fishers_index_of_diversity(main, text):
    lambertw_x = -(
        numpy.exp(-(text.num_types / text.num_tokens))
        * text.num_types
        / text.num_tokens
    )

    if lambertw_x > -numpy.exp(-1):
        alpha = -(
            (text.num_tokens * text.num_types)
            / (
                text.num_tokens
                * scipy.special.lambertw(lambertw_x, -1).real
                + text.num_types
            )
        )
    else:
        alpha = 0

    return alpha

# Herdan's vₘ
# Reference: Herdan, G. (1955). A new derivation and interpretation of Yule's ‘Characteristic’ K. Zeitschrift für Angewandte Mathematik und Physik (ZAMP), 6(4), 332–339. https://doi.org/10.1007/BF01587632
def herdans_vm(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    freqs_nums_types = collections.Counter(types_freqs.values())

    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))
    s2 = numpy.sum(nums_types * numpy.square(freqs))
    vm = s2 / (text.num_tokens ** 2) - 1 / text.num_types

    return vm

# HD-D
# Reference: McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods, 42(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
def hdd(main, text):
    sample_size = main.settings_custom['measures']['lexical_density_diversity']['hdd']['sample_size']

    tokens_freqs = collections.Counter(text.get_tokens_flat())
    ttrs = numpy.empty(len(list(tokens_freqs)))

    # Short texts
    sample_size = min(sample_size, text.num_tokens)

    for i, freq in enumerate(tokens_freqs.values()):
        ttrs[i] = scipy.stats.hypergeom.pmf(k = 0, M = text.num_tokens, n = freq, N = sample_size)

    # The probability that each type appears at least once in the sample
    ttrs = 1 - ttrs
    ttrs *= 1 / sample_size

    return sum(ttrs)

# Honoré's statistic
# References:
#     Honoré, A. (1979). Some simple measures of richness of vocabulary. Association of Literary and Linguistic Computing Bulletin, 7(2), 172–177.
#     Bucks, R. S., Singh, S., Cuerden, J. M., & Wilcock, G. K. (2000). Analysis of spontaneous, conversational speech in dementia of Alzheimer type: Evaluation of an objective technique for analysing lexical performance. Aphasiology, 14(1), 71–91. https://doi.org/10.1080/026870300401603
def honores_stat(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    freqs_nums_types = collections.Counter(types_freqs.values())

    if (denominator := 1 - freqs_nums_types[1] / text.num_types):
        r = 100 * numpy.log(text.num_tokens / denominator)
    else:
        r = 0

    return r

# Lexical density
# Reference: Halliday, M. A. K. (1989). Spoken and written language (2nd ed.). Oxford University Press. | p. 64
def lexical_density(main, text):
    if text.lang in main.settings_global['pos_taggers']:
        wl_pos_tagging.wl_pos_tag_universal(main, text.get_tokens_flat(), lang = text.lang, tagged = text.tagged)

        num_content_words = sum((
            1
            for token in text.get_tokens_flat()
            if token.content_function == _tr('wl_measures_lexical_density_diversity', 'Content words')
        ))
        num_tokens = text.num_tokens

        lexical_density = num_content_words / num_tokens if num_tokens else 0
    else:
        lexical_density = 'no_support'

    return lexical_density

# LogTTR
# Herdan:
#     Herdan, G. (1960). Type-token mathematics: A textbook of mathematical linguistics. Mouton. | p. 28
# Somers:
#     Somers, H. H. (1966). Statistical methods in literary analysis. In J. Leeds (Ed.), The computer and literary style (pp. 128–140). Kent State University Press.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment. Palgrave Macmillan. | p. 28
# Rubet:
#     Dugast, D. (1979). Vocabulaire et stylistique: I théâtre et dialogue, travaux de linguistique quantitative. Slatkine.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment. Palgrave Macmillan. | p. 28
# Maas:
#     Maas, H.-D. (1972). Über den zusammenhang zwischen wortschatzumfang und länge eines textes. Zeitschrift für Literaturwissenschaft und Linguistik, 2(8), 73–96.
# Dugast:
#     Dugast, D. (1978). Sur quoi se fonde la notion d’étendue théoretique du vocabulaire? Le Français Moderne, 46, 25–32.
#     Dugast, D. (1979). Vocabulaire et stylistique: I théâtre et dialogue, travaux de linguistique quantitative. Slatkine.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment. Palgrave Macmillan. | p. 28
def logttr(main, text):
    variant = main.settings_custom['measures']['lexical_density_diversity']['logttr']['variant']

    if variant == 'Herdan':
        logttr = numpy.log(text.num_types) / numpy.log(text.num_tokens)
    elif variant == 'Somers':
        logttr = numpy.log(numpy.log(text.num_types)) / numpy.log(numpy.log(text.num_tokens))
    elif variant == 'Rubet':
        logttr = numpy.log(text.num_types) / numpy.log(numpy.log(text.num_tokens))
    elif variant == 'Maas':
        logttr = (numpy.log(text.num_tokens) - numpy.log(text.num_types)) / (numpy.log(text.num_tokens) ** 2)
    elif variant == 'Dugast':
        logttr = (numpy.log(text.num_tokens) ** 2) / (numpy.log(text.num_tokens) - numpy.log(text.num_types))

    return logttr

# Mean segmental TTR
# References:
#     Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
#     McCarthy, P. M. (2005). An assessment of the range and usefulness of lexical diversity measures and the potential of the measure of textual, lexical diversity (MTLD) (Publication No. 3199485) [Doctoral dissertation, The University of Memphis]. ProQuest Dissertations and Theses Global. | p. 37
def msttr(main, text):
    num_tokens_seg = main.settings_custom['measures']['lexical_density_diversity']['msttr']['num_tokens_in_each_seg']

    ttrs = [
        len(set(tokens_seg)) / num_tokens_seg
        for tokens_seg in wl_nlp_utils.to_sections_unequal(text.get_tokens_flat(), num_tokens_seg)
        # Discard the last segment of text if its length is shorter than other segments
        if len(tokens_seg) == num_tokens_seg
    ]

    if ttrs:
        msttr = numpy.mean(ttrs)
    else:
        msttr = 0

    return msttr

# Measure of textual lexical diversity
# References:
#     McCarthy, P. M. (2005). An assessment of the range and usefulness of lexical diversity measures and the potential of the measure of textual, lexical diversity (MTLD) (Publication No. 3199485) [Doctoral dissertation, The University of Memphis]. ProQuest Dissertations and Theses Global. | pp. 95–96, 99–100
#     McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods, 42(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
def mtld(main, text):
    mtlds = numpy.empty(shape = 2)
    factor_size = main.settings_custom['measures']['lexical_density_diversity']['mtld']['factor_size']
    tokens = text.get_tokens_flat()

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
            elif j == text.num_tokens - 1:
                if factor_size < 1:
                    num_factors += (1 - ttr) / (1 - factor_size)

        if num_factors:
            mtlds[i] = text.num_tokens / num_factors
        else:
            mtlds[i] = 0

    return numpy.mean(mtlds)

# Moving-average TTR
# Reference: Covington, M. A., & McFall, J. D. (2010). Cutting the Gordian knot: The moving-average type-token ratio (MATTR). Journal of Quantitative Linguistics, 17(2), 94–100. https://doi.org/10.1080/09296171003643098
def mattr(main, text):
    window_size = main.settings_custom['measures']['lexical_density_diversity']['mattr']['window_size']

    num_windows = max(1, text.num_tokens - window_size + 1)
    ttrs = numpy.empty(shape = num_windows)
    tokens = text.get_tokens_flat()

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
def popescu_macutek_altmanns_b1_b2_b3_b4_b5(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    freqs = numpy.array(sorted(types_freqs.values(), reverse = True))
    freqs_nums_types = collections.Counter(types_freqs.values())

    l = numpy.sum(numpy.sqrt(numpy.square(freqs[:-1] - freqs[1:]) + 1))
    l_min = numpy.sqrt(numpy.square(text.num_types - 1) + numpy.square(freqs[0] - 1))
    l_max = numpy.sqrt(numpy.square(freqs[0] - 1) + 1) + text.num_types - 2

    b1 = l / l_max

    if (divisor := l_max - l_min):
        b2 = (l - l_min) / divisor
    else:
        b2 = 0

    b3 = (text.num_types - 1) / l
    b4 = (freqs[0] - 1) / l
    b5 = freqs_nums_types[1] / l

    return b1, b2, b3, b4, b5

# Popescu's R₁
# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | pp. 18, 30, 33
def popescus_r1(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    ranks = numpy.empty(shape = text.num_types)
    freqs = numpy.empty(shape = text.num_types)

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

    f_h = numpy.sum(freqs[:int(numpy.floor(h))]) / text.num_tokens
    r1 = 1 - (f_h - numpy.square(h) / (2 * text.num_tokens))

    return r1

# Popescu's R₂
# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | pp. 35–36, 38
def popescus_r2(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
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

    g_k = numpy.sum([num_types for freq, num_types in freqs_nums_types if freq <= numpy.floor(k)]) / text.num_types
    r2 = g_k - numpy.square(k) / (2 * text.num_types)

    return r2

# Popescu's R₃
# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | pp. 48–49, 53
def popescus_r3(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    ranks_freqs = [
        (i + 1, freq)
        for i, freq in enumerate(sorted(types_freqs.values(), reverse = True))
    ]

    rs_rel = numpy.empty(shape = text.num_types)
    fs_rel = numpy.empty(shape = text.num_types)
    freq_cum = 0

    for i, (rank, freq) in enumerate(ranks_freqs):
        freq_cum += freq

        rs_rel[i] = rank
        fs_rel[i] = freq_cum

    rs_rel /= text.num_types
    fs_rel /= text.num_tokens

    drs = numpy.sqrt(numpy.square(rs_rel) + numpy.square(1 - fs_rel))
    m = numpy.argmin(drs) + 1 # m refers to rank
    fm = fs_rel[m - 1]
    r3 = 1 - fm

    return r3

# Popescu's R₄
# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 57
def popescus_r4(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())

    ranks = numpy.empty(shape = text.num_types)
    freqs = numpy.empty(shape = text.num_types)

    for i, freq in enumerate(sorted(types_freqs.values(), reverse = True)):
        ranks[i] = i + 1
        freqs[i] = freq

    r4 = 1 - (text.num_types + 1 - 2 / text.num_tokens * numpy.sum(ranks * freqs)) / text.num_types

    return r4

# Repeat rate
# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 166
def repeat_rate(main, text):
    use_data = main.settings_custom['measures']['lexical_density_diversity']['repeat_rate']['use_data']

    types_freqs = collections.Counter(text.get_tokens_flat())

    if use_data == _tr('wl_measures_lexical_density_diversity', 'Rank-frequency distribution'):
        freqs = numpy.array(list(types_freqs.values()))

        rr = numpy.sum(numpy.square(freqs)) / numpy.square(text.num_tokens)
    elif use_data == _tr('wl_measures_lexical_density_diversity', 'Frequency spectrum'):
        nums_types = numpy.array(list(collections.Counter(types_freqs.values()).values()))

        rr = numpy.sum(numpy.square(nums_types)) / numpy.square(text.num_types)

    return rr

# Root TTR
# References:
#     Guiraud, P. (1954). Les caractères statistiques du vocabulaire: Essai de méthodologie. Presses Universitaires de France.
#     Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment (p. 26). Palgrave Macmillan.
def rttr(main, text):
    return text.num_types / numpy.sqrt(text.num_tokens)

# Shannon entropy
# Reference: Popescu, I.-I. (2009). Word frequency studies. Mouton de Gruyter. | p. 173
def shannon_entropy(main, text):
    use_data = main.settings_custom['measures']['lexical_density_diversity']['shannon_entropy']['use_data']

    types_freqs = collections.Counter(text.get_tokens_flat())

    if use_data == _tr('wl_measures_lexical_density_diversity', 'Rank-frequency distribution'):
        freqs = numpy.array(list(types_freqs.values()))
        ps = freqs / text.num_tokens
    elif use_data == _tr('wl_measures_lexical_density_diversity', 'Frequency spectrum'):
        nums_types = numpy.array(list(collections.Counter(types_freqs.values()).values()))
        ps = nums_types / text.num_types

    h = -numpy.sum(ps * numpy.log2(ps))

    return h

# Simpson's l
# Reference: Simpson, E. H. (1949). Measurement of diversity. Nature, 163, 688. https://doi.org/10.1038/163688a0
def simpsons_l(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    freqs_nums_types = collections.Counter(types_freqs.values())
    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))

    s2 = numpy.sum(nums_types * numpy.square(freqs))
    l = (s2 - text.num_tokens) / (text.num_tokens * (text.num_tokens - 1))

    return l

# Type-token ratio
# Reference: Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
def ttr(main, text):
    return text.num_types / text.num_tokens

# vocd-D
# Reference: Malvern, D., Richards, B., Chipere, N., & Durán, P. (2004). Lexical diversity and language development: Quantification and assessment. Palgrave Macmillan. | pp. 51, 56–57
def vocdd(main, text):
    def ttr(n, d):
        return (d / n) * (numpy.sqrt(1 + 2 * n / d) - 1)

    tokens = text.get_tokens_flat()
    ttr_ys = numpy.empty(shape = 16)

    for i, n in enumerate(range(35, 51)):
        ttrs = numpy.empty(shape = 100)

        for j in range(100):
            if n <= text.num_tokens:
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

# Yule's characteristic K
# Reference: Yule, G. U. (1944). The statistical study of literary vocabulary. Cambridge University Press. | pp. 52–53
def yules_characteristic_k(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    freqs_nums_types = collections.Counter(types_freqs.values())
    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))

    s2 = numpy.sum(nums_types * numpy.square(freqs))
    k = 10000 * ((s2 - text.num_tokens) / (text.num_tokens ** 2))

    return k

# Yule's Index of Diversity
# Reference: Williams, C. B. (1970). Style and vocabulary: Numerical studies. Griffin. | p. 100
def yules_index_of_diversity(main, text):
    types_freqs = collections.Counter(text.get_tokens_flat())
    freqs_nums_types = collections.Counter(types_freqs.values())
    freqs = numpy.array(list(freqs_nums_types))
    nums_types = numpy.array(list(freqs_nums_types.values()))

    s2 = numpy.sum(nums_types * numpy.square(freqs))

    if (divisor := s2 - text.num_tokens):
        index_of_diversity = (text.num_tokens ** 2) / divisor
    else:
        index_of_diversity = 0

    return index_of_diversity
