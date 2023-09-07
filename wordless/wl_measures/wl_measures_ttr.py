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

# Type-token Ratio
# References:
#     Templin, M. (1957). Certain language skills in children. University of Minnesota Press.
#     Torreulla, J., & Capsada, R. (2013). Lexical statistics and tipological structures: A measure of lexical richness. Procedia - Social and Behavioral Sciences, 95, 447–454.
def ttr(main, tokens):
    return len(set(tokens)) / len(tokens)
