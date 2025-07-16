# ----------------------------------------------------------------------
# Tests: Measures - Syntactic complexity
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

from wordless.wl_measures import wl_measures_syntactic_complexity

def test_mdd():
    numpy.testing.assert_array_equal(wl_measures_syntactic_complexity.mdd(
        [
            [1, 0, 1, -2, 2, 1, -3, 3, 2, 1, -4],
            [0, -1],
            [0],
            []
        ]
    ), (
        numpy.array([2, 1])
    ))

def test_ndd():
    numpy.testing.assert_array_equal(wl_measures_syntactic_complexity.ndd(
        [
            [1, 0, 1, -2, 2, 1, -3, 3, 2, 1, -4],
            [0, -1],
            [0],
            []
        ],
        [2, 1, 1, 1]
    ), (
        numpy.array([numpy.absolute(numpy.log(2 / numpy.sqrt(20))), 0])
    ))

if __name__ == '__main__':
    test_mdd()
    test_ndd()
