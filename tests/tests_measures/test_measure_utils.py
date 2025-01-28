# ----------------------------------------------------------------------
# Tests: Measures - Measure Utilities
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

from tests import wl_test_init
from wordless.wl_measures import wl_measure_utils

main = wl_test_init.Wl_Test_Main()

ITEMS_TO_SEARCH = ['w1', 'w2']

ITEMS = ['w1'] * 7 + ['w2'] * 3
FREQS_SECTIONS_1_SAMPLE = {
    'w1': [2, 2, 2, 1, 0],
    'w2': [0, 0, 0, 1, 2]
}

ITEMS_X1 = ['w1'] * 7 + ['w2'] * 3
ITEMS_X2 = ['w1'] * 6 + ['w2'] * 4
FREQS_SECTIONS_2_SAMPLE_ABS = {
    'w1': ([2, 2, 2, 1, 0], [2, 2, 2, 0, 0]),
    'w2': ([0, 0, 0, 1, 2], [0, 0, 0, 2, 2])
}
FREQS_SECTIONS_2_SAMPLE_RELATIVE = {
    'w1': ([1, 1, 1, .5, 0], [1, 1, 1, 0, 0]),
    'w2': ([0, 0, 0, .5, 1], [0, 0, 0, 1, 1])
}

def test_to_measure_code():
    for measure_type, measures in main.settings_global['mapping_measures'].items():
        for measure_text, measure_code in measures.items():
            assert wl_measure_utils.to_measure_code(main, measure_type, measure_text) == measure_code

def test_to_measure_text():
    for measure_type, measures in main.settings_global['mapping_measures'].items():
        for measure_text, measure_code in measures.items():
            assert wl_measure_utils.to_measure_text(main, measure_type, measure_code) == measure_text

    assert wl_measure_utils.to_measure_text(main, list(main.settings_global['mapping_measures'])[0], 'test') is None

def test_to_freqs_sections_1_sample():
    assert wl_measure_utils.to_freqs_sections_1_sample(
        ITEMS_TO_SEARCH, ITEMS,
        num_sub_sections = 5
    ) == FREQS_SECTIONS_1_SAMPLE

def test_to_freqs_sections_dispersion():
    assert wl_measure_utils.to_freqs_sections_dispersion(main, ITEMS_TO_SEARCH, ITEMS) == FREQS_SECTIONS_1_SAMPLE

def test_to_freqs_sections_adjusted_freq():
    assert wl_measure_utils.to_freqs_sections_adjusted_freq(main, ITEMS_TO_SEARCH, ITEMS) == FREQS_SECTIONS_1_SAMPLE

def test_to_freqs_sections_2_sample():
    assert wl_measure_utils.to_freqs_sections_2_sample(
        ITEMS_TO_SEARCH, ITEMS_X1, ITEMS_X2,
        num_sub_sections = 5,
        use_data = 'Absolute frequency'
    ) == FREQS_SECTIONS_2_SAMPLE_ABS
    assert wl_measure_utils.to_freqs_sections_2_sample(
        ITEMS_TO_SEARCH, ITEMS_X1, ITEMS_X2,
        num_sub_sections = 5,
        use_data = 'Relative frequency'
    ) == FREQS_SECTIONS_2_SAMPLE_RELATIVE

def test_to_freqs_sections_statistical_significance():
    assert wl_measure_utils.to_freqs_sections_statistical_significance(
        main, ITEMS_TO_SEARCH, ITEMS_X1, ITEMS_X2,
        test_statistical_significance = 'mann_whitney_u_test'
    ) == FREQS_SECTIONS_2_SAMPLE_RELATIVE
    assert wl_measure_utils.to_freqs_sections_statistical_significance(
        main, ITEMS_TO_SEARCH, ITEMS_X1, ITEMS_X2,
        test_statistical_significance = 'students_t_test_2_sample'
    ) == FREQS_SECTIONS_2_SAMPLE_RELATIVE

def test_to_freqs_sections_bayes_factor():
    assert wl_measure_utils.to_freqs_sections_bayes_factor(
        main, ITEMS_TO_SEARCH, ITEMS_X1, ITEMS_X2,
        measure_bayes_factor = 'students_t_test_2_sample'
    ) == FREQS_SECTIONS_2_SAMPLE_RELATIVE

def test_numpy_divide():
    numpy.testing.assert_array_equal(
        wl_measure_utils.numpy_divide(numpy.array([1] * 10), numpy.array([0] * 10)),
        numpy.array([0] * 10)
    )
    numpy.testing.assert_array_equal(
        wl_measure_utils.numpy_divide(numpy.array([1] * 10), numpy.array([0] * 10), default = 1),
        numpy.array([1] * 10)
    )

def test_numpy_log():
    numpy.testing.assert_array_equal(
        wl_measure_utils.numpy_log(numpy.array([0] * 10)),
        numpy.array([0] * 10)
    )
    numpy.testing.assert_array_equal(
        wl_measure_utils.numpy_log(numpy.array([0] * 10), default = 1),
        numpy.array([1] * 10)
    )

def test_numpy_log2():
    numpy.testing.assert_array_equal(
        wl_measure_utils.numpy_log2(numpy.array([0] * 10)),
        numpy.array([0] * 10)
    )
    numpy.testing.assert_array_equal(
        wl_measure_utils.numpy_log2(numpy.array([0] * 10), default = 1),
        numpy.array([1] * 10)
    )

if __name__ == '__main__':
    test_to_measure_code()
    test_to_measure_text()

    test_to_freqs_sections_1_sample()
    test_to_freqs_sections_dispersion()
    test_to_freqs_sections_adjusted_freq()

    test_to_freqs_sections_2_sample()
    test_to_freqs_sections_statistical_significance()
    test_to_freqs_sections_bayes_factor()

    test_numpy_divide()
    test_numpy_log()
    test_numpy_log2()
