# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Dispersion
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
from wl_measures import wl_measures_dispersion

main = wl_test_init.Wl_Test_Main()

# Reference: Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def test_carrolls_d2():
    assert round(wl_measures_dispersion.carrolls_d2([2, 1, 1, 1, 0]), 4) == 0.8277

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 416)
def test_griess_dp():
    assert round(wl_measures_dispersion.griess_dp([3, 3, 3]), 0) == 0

# Reference: Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora” International Journal of Corpus Linguistics, 17(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij (p. 148)
def test_griess_dp_norm():
    assert round(wl_measures_dispersion.griess_dp_norm([2, 1, 0]), 1) == 0.5

# Reference: Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
def test_juillands_d():
    assert round(wl_measures_dispersion.juillands_d([0, 4, 3, 2, 1]), 4) == 0.6464

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 408)
def test_lynes_d3():
    assert round(wl_measures_dispersion.lynes_d3([1, 2, 3, 4, 5]), 3) == 0.944

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 407)
def test_rosengrens_s():
    assert round(wl_measures_dispersion.rosengrens_s([1, 2, 3, 4, 5]), 3) == 0.937

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 408)
def test_zhangs_distributional_consistency():
    assert round(wl_measures_dispersion.zhangs_distributional_consistency([1, 2, 3, 4, 5]), 3) == 0.937
