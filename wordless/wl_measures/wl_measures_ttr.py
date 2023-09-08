# ----------------------------------------------------------------------
# Wordless: Measures - Type-token ratio (TTR)
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

import numpy
import scipy

from wordless.wl_nlp import wl_nlp_utils

# HD-D
# Reference: McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods, 42(2), 381–392. https://doi.org/10.3758/BRM.42.2.381
def hdd(main, tokens):
    sample_size = main.settings_custom['measures']['ttr']['hdd']['sample_size']

    num_tokens = len(tokens)
    tokens_freqs = collections.Counter(tokens)
    ttrs = numpy.empty(len(list(tokens_freqs)))

    for i, freq in enumerate(tokens_freqs.values()):
        ttrs[i] = scipy.stats.hypergeom.pmf(k = 0, M = num_tokens, n = freq, N = sample_size)

    # The probability that each type appears at least once in the sample
    ttrs = 1 - ttrs
    ttrs *= 1 / sample_size

    return sum(ttrs)

# Mean Segmental TTR
# References:
#     Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
#     McCarthy, P. M. (2005). An assessment of the range and usefulness of lexical diversity measures and the potential of the measure of textual, lexical diversity (MTLD) [Doctoral dissertation, The University of Memphis] (p. 37). ProQuest Dissertations and Theses Global.
def msttr(main, tokens):
    num_tokens_seg = main.settings_custom['measures']['ttr']['msttr']['num_tokens_in_each_seg']

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
    factor_size = main.settings_custom['measures']['ttr']['mtld']['factor_size']
    len_tokens = len(tokens)

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
            elif j == len_tokens - 1:
                if factor_size < 1:
                    num_factors += (1 - ttr) / (1 - factor_size)

        mtlds[i] = len_tokens / num_factors

    return numpy.mean(mtlds)

# Moving-average TTR
# Reference: Covington, M. A., & McFall, J. D. (2010). Cutting the Gordian knot: The moving-average type-token ratio (MATTR). Journal of Quantitative Linguistics, 17(2), 94–100. https://doi.org/10.1080/09296171003643098
def mattr(main, tokens):
    window_size = main.settings_custom['measures']['ttr']['mattr']['window_size']

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

# Type-token Ratio
# Reference: Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
def ttr(main, tokens):
    return len(set(tokens)) / len(tokens)
