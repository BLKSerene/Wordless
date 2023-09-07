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

from wordless.wl_nlp import wl_nlp_utils

# Mean Segmental TTR
# Reference: Johnson, W. (1944). Studies in language behavior: I. a program of research. Psychological Monographs, 56(2), 1–15. https://doi.org/10.1037/h0093508
def msttr(main, tokens):
    num_tokens_seg = main.settings_custom['measures']['ttr']['msttr']['num_tokens_in_each_seg']

    ttrs = [
        len(set(tokens_seg)) / len(tokens_seg)
        for tokens_seg in wl_nlp_utils.to_sections_unequal(tokens, num_tokens_seg)
    ]

    return numpy.mean(ttrs)

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
# References:
#     Templin, M. (1957). Certain language skills in children. University of Minnesota Press.
#     Torreulla, J., & Capsada, R. (2013). Lexical statistics and tipological structures: A measure of lexical richness. Procedia - Social and Behavioral Sciences, 95, 447–454.
def ttr(main, tokens):
    return len(set(tokens)) / len(tokens)
