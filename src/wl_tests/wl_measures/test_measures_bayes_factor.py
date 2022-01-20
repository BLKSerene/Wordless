# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Bayes Factor
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

from wl_tests import wl_test_init
from wl_measures import wl_measures_bayes_factor

main = wl_test_init.Wl_Test_Main()

# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang. (p. 7)
def test_bayes_factor_log_likelihood_ratio_test():
    assert round(wl_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(22.22, 9611 + 144925), 2) == 10.27
