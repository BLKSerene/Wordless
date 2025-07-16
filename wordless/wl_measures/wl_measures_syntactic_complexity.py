# ----------------------------------------------------------------------
# Wordless: Measures - Syntactic complexity
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

import numpy

# Mean dependency distance
# Reference: Liu, H., Hudson, R., & Feng, Z. (2009). Using a Chinese treebank to measure dependency distance. *Corpus Linguistics and Linguistic Theory*, *5*(2), 161–175. https://doi.org/10.1515/CLLT.2009.007
def mdd(dds_sentences):
    # Remove roots
    dds_sentences = [
        numpy.array(dds)
        for dds in dds_sentences
    ]
    dds_sentences = [
        dds[dds != 0]
        for dds in dds_sentences
    ]

    # Remove empty arrays
    dds_sentences = [
        dds
        for dds in dds_sentences
        if dds.size
    ]

    # Remove signs
    dds_sentences = [
        numpy.absolute(dds)
        for dds in dds_sentences
    ]

    return numpy.array([
        numpy.mean(dds)
        for dds in dds_sentences
    ])

# Normalized dependency distance
# Reference: Lei, L., & Jockers, M. L. (2018). Normalized dependency distance: Proposing a new measure. Quantitative Linguistics, 27(1), 62–79. https://doi.org/10.1080/09296174.2018.1504615
def ndd(dds_sentences, root_dists):
    mdds = mdd(dds_sentences)

    for i, (dds, _) in reversed(list(enumerate(zip(dds_sentences, root_dists)))):
        if dds in ([], [0]):
            del root_dists[i]

    root_dists = numpy.array(root_dists)

    # Remove roots
    dds_sentences = [
        numpy.array(dds)
        for dds in dds_sentences
    ]
    dds_sentences = [
        dds[dds != 0]
        for dds in dds_sentences
    ]

    # Remove empty arrays
    dds_sentences = [
        dds
        for dds in dds_sentences
        if dds.size
    ]

    len_sentences = numpy.array([dds.size for dds in dds_sentences])

    return numpy.absolute(numpy.log(mdds / (numpy.sqrt(root_dists * len_sentences))))
