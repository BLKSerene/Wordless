# ----------------------------------------------------------------------
# Tests: Measures - Dispersion
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

from tests import wl_test_init
from wordless.wl_measures import wl_measures_dispersion

main = wl_test_init.Wl_Test_Main()

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri | pp. 406, 410
TOKENS = 'b a m n i b e u p k | b a s a t b e w q n | b c a g a b e s t a | b a g h a b e a a t | b a h a a b e a x a'.replace('|', '').split()
DISTS = [2, 10, 2, 9, 2, 5, 2, 3, 3, 1, 3, 2, 1, 3, 2]

def test__get_dists():
    assert list(wl_measures_dispersion._get_dists(TOKENS, 'a')) == DISTS
    assert not list(wl_measures_dispersion._get_dists(TOKENS, 'aa'))

def test_ald():
    assert round(wl_measures_dispersion.ald(main, TOKENS, 'a'), 3) == 0.628
    assert wl_measures_dispersion.ald(main, TOKENS, 'aa') == 0

def test_arf():
    assert round(wl_measures_dispersion.arf(main, TOKENS, 'a'), 1) == 10.8
    assert wl_measures_dispersion.arf(main, TOKENS, 'aa') == 0

def test_awt():
    assert wl_measures_dispersion.awt(main, TOKENS, 'a') == 3.18
    assert wl_measures_dispersion.awt(main, TOKENS, 'aa') == 0

# Reference: Carroll, J. B. (1970). An alternative to Juillands's usage coefficient for lexical frequencies. ETS Research Bulletin Series, 1970(2), i–15. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x | p. 13
def test_carrolls_d2():
    assert round(wl_measures_dispersion.carrolls_d2(main, [2, 1, 1, 1, 0]), 4) == 0.8277
    assert wl_measures_dispersion.carrolls_d2(main, [0, 0, 0, 0]) == 0

# References:
#     Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri | p. 416
#     Lijffijt, J., & Gries, S. T. (2012). Correction to Stefan Th. Gries’ “dispersions and adjusted frequencies in corpora” International Journal of Corpus Linguistics, 17(1), 147–149. https://doi.org/10.1075/ijcl.17.1.08lij | p. 148
def test_griess_dp():
    main.settings_custom['measures']['dispersion']['griess_dp']['apply_normalization'] = False

    assert round(wl_measures_dispersion.griess_dp(main, [3, 3, 3]), 0) == 0
    assert wl_measures_dispersion.griess_dp(main, [0, 0, 0, 0]) == 0

    main.settings_custom['measures']['dispersion']['griess_dp']['apply_normalization'] = True

    assert round(wl_measures_dispersion.griess_dp(main, [2, 1, 0]), 1) == 0.5
    assert wl_measures_dispersion.griess_dp(main, [0, 0, 0, 0]) == 0

# Reference: Carroll, J. B. (1970). An alternative to Juillands's usage coefficient for lexical frequencies. ETS Research Bulletin Series, 1970(2), i–15. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x | p. 14
def test_juillands_d():
    assert round(wl_measures_dispersion.juillands_d(main, [0, 4, 3, 2, 1]), 4) == 0.6464
    assert wl_measures_dispersion.juillands_d(main, [0, 0, 0, 0]) == 0

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri | p. 408
def test_lynes_d3():
    assert round(wl_measures_dispersion.lynes_d3(main, [1, 2, 3, 4, 5]), 3) == 0.944
    assert wl_measures_dispersion.lynes_d3(main, [0, 0, 0, 0]) == 0

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri | p. 407
def test_rosengrens_s():
    assert round(wl_measures_dispersion.rosengrens_s(main, [1, 2, 3, 4, 5]), 3) == 0.937
    assert wl_measures_dispersion.rosengrens_s(main, [0, 0, 0, 0]) == 0

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri | p. 408
def test_zhangs_distributional_consistency():
    assert round(wl_measures_dispersion.zhangs_distributional_consistency(main, [1, 2, 3, 4, 5]), 3) == 0.937
    assert wl_measures_dispersion.zhangs_distributional_consistency(main, [0, 0, 0, 0]) == 0

if __name__ == '__main__':
    test__get_dists()
    test_ald()
    test_arf()
    test_awt()

    test_carrolls_d2()
    test_griess_dp()
    test_juillands_d()
    test_lynes_d3()
    test_rosengrens_s()
    test_zhangs_distributional_consistency()
