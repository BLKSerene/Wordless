#
# Wordless: Tests - Measures - Adjusted Frequency
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

from wordless_tests import wordless_test_init
from wordless_measures import wordless_measures_adjusted_freq

main = wordless_test_init.Wordless_Test_Main()

# [1] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
# [2] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 115.
# [3] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français." Dissertation, Stockholm University, 1974, p. 122.
def test_juillands_u():
    assert round(wordless_measures_adjusted_freq.juillands_u([0, 4, 3, 2, 1]), 2) == 6.46
    assert round(wordless_measures_adjusted_freq.juillands_u([2, 2, 2, 2, 2]), 0) == 10
    assert round(wordless_measures_adjusted_freq.juillands_u([4, 2, 1, 1, 0]), 3) == 4.609

# [1] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
# [2] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français." Dissertation, Stockholm University, 1974, p. 122.
# [3] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
def test_carrolls_um():
    assert round(wordless_measures_adjusted_freq.carrolls_um([2, 1, 1, 1, 0]), 2) == 4.31
    assert round(wordless_measures_adjusted_freq.carrolls_um([4, 2, 1, 1, 0]), 3) == 6.424
    assert round(wordless_measures_adjusted_freq.carrolls_um([1, 2, 3, 4, 5]), 3) == 14.108

# [1] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 117.
# [2] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français." Dissertation, Stockholm University, 1974, p. 122.
# [3] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
def test_rosengres_kf():
    assert round(wordless_measures_adjusted_freq.rosengrens_kf([2, 2, 2, 2, 1]), 2) == 8.86
    assert round(wordless_measures_adjusted_freq.rosengrens_kf([4, 2, 1, 1, 0]), 3) == 5.863
    assert round(wordless_measures_adjusted_freq.rosengrens_kf([1, 2, 3, 4, 5]), 3) == 14.053

# [1] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français." Dissertation, Stockholm University, 1974, p. 122.
# [2] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
def test_engwalls_fm():
    assert round(wordless_measures_adjusted_freq.engwalls_fm([4, 2, 1, 1, 0]), 1) == 6.4
    assert round(wordless_measures_adjusted_freq.engwalls_fm([1, 2, 3, 4, 5]), 0) == 15

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
def test_kromers_ur():
    assert round(wordless_measures_adjusted_freq.kromers_ur([2, 1, 1, 1, 0]), 1) == 4.5
