# ----------------------------------------------------------------------
# Wordless: Measures - Bayes Factor
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

from wl_measures import wl_measures_bayes_factor
from wl_tests import wl_test_init

main = wl_test_init.Wl_Test_Main()

def test_to_freq_sections_items():
    items_search = ['w1', 'w2']
    items_x1 = ['w1'] * 7 + ['w2'] * 3
    items_x2 = ['w1'] * 6 + ['w2'] * 4

    freq_sections_items = {
        'w1': ([1, 1, 1, .5, 0], [1, 1, 1, 0, 0]),
        'w2': ([0, 0, 0, .5, 1], [0, 0, 0, 1, 1])
    }

    assert wl_measures_bayes_factor.to_freq_sections_items(main, items_search, items_x1, items_x2, measure_bayes_factor = "Student's t-test (2-sample)") == freq_sections_items

def test_bayes_factor_log_likelihood_ratio_test():
    assert wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(main, 0, 0, 0, 0) == 0

def test_bayes_factor_students_t_test_2_sample():
    assert wl_measures_bayes_factor.bayes_factor_students_t_test_2_sample(main, [0] * 5, [0] * 5) == 0

if __name__ == '__main__':
    test_to_freq_sections_items()

    test_bayes_factor_log_likelihood_ratio_test()
    test_bayes_factor_students_t_test_2_sample()
