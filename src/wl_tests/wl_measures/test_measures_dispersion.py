#
# Wordless: Tests - Measures - Dispersion
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wl_tests import wl_test_init
from wl_measures import wl_measures_dispersion

main = wl_test_init.Wl_Test_Main()

# Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
def test_juillands_d():
    assert round(wl_measures_dispersion.juillands_d([0, 4, 3, 2, 1]), 4) == 0.6464

# Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
def test_carrolls_d2():
    assert round(wl_measures_dispersion.carrolls_d2([2, 1, 1, 1, 0]), 4) == 0.8277

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 408.
def test_lynes_d3():
    assert round(wl_measures_dispersion.lynes_d3([1, 2, 3, 4, 5]), 3) == 0.944

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 407.
def test_rosengrens_s():
    assert round(wl_measures_dispersion.rosengrens_s([1, 2, 3, 4, 5]), 3) == 0.937

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 408.
def test_zhangs_distributional_consistency():
    assert round(wl_measures_dispersion.zhangs_distributional_consistency([1, 2, 3, 4, 5]), 3) == 0.937

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 416.
def test_griess_dp():
    assert round(wl_measures_dispersion.griess_dp([3, 3, 3]), 0) == 0

# Lijffijt, Jefrey, and Stefan Th. Gries. "Correction to Stefan Th. Gries’ “Dispersions and adjusted frequencies in corpora”" International Journal of Corpus Linguistics, vol. 17, no. 1, 2012, pp. 148.
def test_griess_dp_norm():
    assert round(wl_measures_dispersion.griess_dp_norm([2, 1, 0]), 1) == 0.5
