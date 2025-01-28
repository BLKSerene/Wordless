# ----------------------------------------------------------------------
# Wordless: Measures - Miscellaneous
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

def modes(inputs):
    inputs_modes = []

    inputs = numpy.array(inputs)

    if inputs.size > 0:
        unique, unique_counts = numpy.unique(inputs, return_counts = True)
        unique_counts_max = numpy.max(unique_counts)

        for val, freq in zip(unique, unique_counts):
            if freq == unique_counts_max:
                inputs_modes.append(val)

    return inputs_modes
