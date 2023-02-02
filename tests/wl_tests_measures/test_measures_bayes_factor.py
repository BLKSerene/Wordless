# ----------------------------------------------------------------------
# Wordless: Measures - Bayes Factor
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

from tests import wl_test_init
from wordless.wl_measures import wl_measures_bayes_factor

main = wl_test_init.Wl_Test_Main()

def test_bayes_factor_log_likelihood_ratio_test():
    assert wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(main, 0, 0, 0, 0) == 0

def test_bayes_factor_students_t_test_2_sample():
    assert wl_measures_bayes_factor.bayes_factor_students_t_test_2_sample(main, [0] * 5, [0] * 5) == 0

if __name__ == '__main__':
    test_bayes_factor_log_likelihood_ratio_test()
    test_bayes_factor_students_t_test_2_sample()
