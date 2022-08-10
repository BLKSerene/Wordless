# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Adjusted Frequency
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

from tests import wl_test_init
from wordless.wl_measures import wl_measures_adjusted_freq

main = wl_test_init.Wl_Test_Main()

def test_to_freq_sections_items():
    items_search = ['w1', 'w2']
    items = ['w1'] * 7 + ['w2'] * 3

    freq_sections_items = {
        'w1': [2, 2, 2, 1, 0],
        'w2': [0, 0, 0, 1, 2]
    }

    assert wl_measures_adjusted_freq.to_freq_sections_items(main, items_search, items) == freq_sections_items

# References:
#     Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/
#     Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University. (p. 122)
#     Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 409)
def test_carrolls_um():
    assert round(wl_measures_adjusted_freq.carrolls_um([2, 1, 1, 1, 0]), 2) == 4.31
    assert round(wl_measures_adjusted_freq.carrolls_um([4, 2, 1, 1, 0]), 3) == 6.424
    assert round(wl_measures_adjusted_freq.carrolls_um([1, 2, 3, 4, 5]), 3) == 14.108

    assert wl_measures_adjusted_freq.carrolls_um([0, 0, 0, 0, 0]) == 0

# References
#     Carroll, J. B. (1970). An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index. Computer Studies in the Humanities and Verbal Behaviour, 3(2), 61–65. https://doi.org/10.1002/j.2333-8504.1970.tb00778.x
#     Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127. (p. 115)
#     Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University. (p. 122)
def test_juillands_u():
    assert round(wl_measures_adjusted_freq.juillands_u([0, 4, 3, 2, 1]), 2) == 6.46
    assert round(wl_measures_adjusted_freq.juillands_u([2, 2, 2, 2, 2]), 0) == 10
    assert round(wl_measures_adjusted_freq.juillands_u([4, 2, 1, 1, 0]), 3) == 4.609

    assert wl_measures_adjusted_freq.juillands_u([0, 0, 0, 0, 0]) == 0

# References:
#     Rosengren, I. (1971). The quantitative concept of language and its relation to the structure of frequency dictionaries. Études de linguistique appliquée, 1, 103–127. (p. 117)
#     Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University. (p. 122)
#     Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 409)
def test_rosengres_kf():
    assert round(wl_measures_adjusted_freq.rosengrens_kf([2, 2, 2, 2, 1]), 2) == 8.86
    assert round(wl_measures_adjusted_freq.rosengrens_kf([4, 2, 1, 1, 0]), 3) == 5.863
    assert round(wl_measures_adjusted_freq.rosengrens_kf([1, 2, 3, 4, 5]), 3) == 14.053

    assert wl_measures_adjusted_freq.rosengrens_kf([0, 0, 0, 0, 0]) == 0

# References:
#     Engwall, G. (1974). Fréquence et distribution du vocabulaire dans un choix de romans français [Unpublished doctoral dissertation]. Stockholm University. (p. 122)
#     Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 409)
def test_engwalls_fm():
    assert round(wl_measures_adjusted_freq.engwalls_fm([4, 2, 1, 1, 0]), 1) == 6.4
    assert round(wl_measures_adjusted_freq.engwalls_fm([1, 2, 3, 4, 5]), 0) == 15

    assert wl_measures_adjusted_freq.engwalls_fm([0, 0, 0, 0, 0]) == 0

# Reference: Gries, S. T. (2008). Dispersions and adjusted frequencies in corpora. International Journal of Corpus Linguistics, 13(4), 403–437. https://doi.org/10.1075/ijcl.13.4.02gri (p. 409)
def test_kromers_ur():
    assert round(wl_measures_adjusted_freq.kromers_ur([2, 1, 1, 1, 0]), 1) == 4.5

    assert wl_measures_adjusted_freq.kromers_ur([0, 0, 0, 0, 0]) == 0

if __name__ == '__main__':
    test_to_freq_sections_items()

    test_carrolls_um()
    test_juillands_u()
    test_rosengres_kf()
    test_engwalls_fm()
    test_kromers_ur()
