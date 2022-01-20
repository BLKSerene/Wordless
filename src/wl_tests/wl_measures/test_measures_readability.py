# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Readability
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

import numpy

from wl_tests import wl_test_init
from wl_measures import wl_measures_readability

main = wl_test_init.Wl_Test_Main()

TOKENS_MULTILEVEL_12 = [[['This', 'is', 'a', 'sentence', '.'], ['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sen-tence0', '.']]]
TOKENS_MULTILEVEL_12_PROPN = [[['This', 'is', 'a', 'sentence', '.'], ['This', 'is', 'a', 'sentence', '.']], [['Louisiana', 'metropolis', 'boxes', 'created', '.']]]
TOKENS_MULTILEVEL_100 = [[['This', 'is', 'a', 'sentence', '.'], ['This', 'is', 'a', 'sentence', '.']]] * 12 + [[['This', 'is', 'a', 'sen-tence0', '.']]]
TOKENS_MULTILEVEL_120 = [[['This', 'is', 'a', 'sentence', '.'], ['This', 'is', 'a', 'metropolis', '.']]] * 15
TOKENS_MULTILEVEL_150 = [[['This', 'is', 'a', 'sentence', '.'], ['This', 'is', 'a', 'sentence', '.']]] * 18 + [[['This', 'is', 'a', 'sen-tence0', 'for', 'testing', '.']]]

class Wl_Test_Text():
    def __init__(self, tokens_multilevel = TOKENS_MULTILEVEL_12, lang = 'eng_us'):
        super().__init__()

        self.main = main
        self.lang = lang
        self.tokens_multilevel = tokens_multilevel

test_text_eng_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12)
test_text_eng_12_propn = Wl_Test_Text(TOKENS_MULTILEVEL_12_PROPN)
test_text_eng_100 = Wl_Test_Text(TOKENS_MULTILEVEL_100)
test_text_eng_120 = Wl_Test_Text(TOKENS_MULTILEVEL_120)
test_text_eng_150 = Wl_Test_Text(TOKENS_MULTILEVEL_150)
test_text_spa_12 = Wl_Test_Text(lang = 'spa')
test_text_spa_120 = Wl_Test_Text(tokens_multilevel = TOKENS_MULTILEVEL_120, lang = 'spa')
test_text_spa_150 = Wl_Test_Text(tokens_multilevel = TOKENS_MULTILEVEL_150, lang = 'spa')
test_text_other_12 = Wl_Test_Text(lang = 'other')

def test_automated_readability_index():
    ari_eng_12 = wl_measures_readability.automated_readability_index(main, test_text_eng_12)
    ari_spa_12 = wl_measures_readability.automated_readability_index(main, test_text_spa_12)
    ari_other_12 = wl_measures_readability.automated_readability_index(main, test_text_other_12)

    print(f'Automated Readability Index:')
    print(f'\t{ari_eng_12} (eng/12)')
    print(f'\t{ari_spa_12} (spa/12)')
    print(f'\t{ari_other_12} (other/12)')

    assert ari_eng_12 == ari_spa_12 == ari_other_12 == 0.5 * (12 / 3) + 4.71 * (47 / 12) - 21.43

def test_coleman_liau_index():
    grade_level_eng_12 = wl_measures_readability.coleman_liau_index(main, test_text_eng_12)
    grade_level_spa_12 = wl_measures_readability.coleman_liau_index(main, test_text_spa_12)
    grade_level_other_12 = wl_measures_readability.coleman_liau_index(main, test_text_other_12)

    print(f'Coleman-Liau Index:')
    print(f'\t{grade_level_eng_12} (eng/12)')
    print(f'\t{grade_level_spa_12} (spa/12)')
    print(f'\t{grade_level_other_12} (other/12)')

    est_cloze_pct = 141.8401 - 0.21459 * (45 / 12 * 100) + 1.079812 * (3 / 12 * 100)

    assert grade_level_eng_12 == grade_level_spa_12 == grade_level_other_12 == -27.4004 * (est_cloze_pct / 100) + 23.06395

def test_dale_chall_readability_score():
    x_c50_eng_12 = wl_measures_readability.dale_chall_readability_score(main, test_text_eng_12)
    x_c50_spa_12 = wl_measures_readability.dale_chall_readability_score(main, test_text_spa_12)
    x_c50_other_12 = wl_measures_readability.dale_chall_readability_score(main, test_text_other_12)

    print(f'Dale-Chall Readibility Score:')
    print(f'\t{x_c50_eng_12} (eng/12)')
    print(f'\t{x_c50_spa_12} (spa/12)')
    print(f'\t{x_c50_other_12} (other/12)')

    assert x_c50_eng_12 == 0.1579 * (1 / 12) + 0.0496 * (12 / 3) + 3.6365
    assert x_c50_spa_12 == x_c50_other_12 == wl_measures_readability.NO_SUPPORT

def test_devereux_readability_index():
    grade_placement_eng_12 = wl_measures_readability.devereux_readability_index(main, test_text_eng_12)
    grade_placement_spa_12 = wl_measures_readability.devereux_readability_index(main, test_text_spa_12)
    grade_placement_other_12 = wl_measures_readability.devereux_readability_index(main, test_text_other_12)

    print(f'Devereux Readability Index:')
    print(f'\t{grade_placement_eng_12} (eng/12)')
    print(f'\t{grade_placement_spa_12} (spa/12)')
    print(f'\t{grade_placement_other_12} (other/12)')

    assert grade_placement_eng_12 == grade_placement_spa_12 == grade_placement_other_12 == 1.56 * (47 / 12) + 0.19 * (12 / 3) - 6.49

def test_flesch_reading_ease():
    flesch_re_eng_12 = wl_measures_readability.flesch_reading_ease(main, test_text_eng_12)
    flesch_re_spa_12 = wl_measures_readability.flesch_reading_ease(main, test_text_spa_12)
    flesch_re_other_12 = wl_measures_readability.flesch_reading_ease(main, test_text_other_12)

    print(f'Flesch Reading Ease:')
    print(f'\t{flesch_re_eng_12} (eng/12)')
    print(f'\t{flesch_re_spa_12} (spa/12)')
    print(f'\t{flesch_re_other_12} (other/12)')

    assert flesch_re_eng_12 == 206.835 - 0.846 * (15 / 12 * 100) - 1.015 * (12 / 3)
    assert flesch_re_spa_12 != wl_measures_readability.NO_SUPPORT
    assert flesch_re_other_12 == wl_measures_readability.NO_SUPPORT

def test_flesch_reading_ease_simplified():
    flesch_re_simplified_eng_12 = wl_measures_readability.flesch_reading_ease_simplified(main, test_text_eng_12)
    flesch_re_simplified_spa_12 = wl_measures_readability.flesch_reading_ease_simplified(main, test_text_spa_12)
    flesch_re_simplified_other_12 = wl_measures_readability.flesch_reading_ease_simplified(main, test_text_other_12)

    print(f'Flesch Reading Ease (Simplified):')
    print(f'\t{flesch_re_simplified_eng_12} (eng/12)')
    print(f'\t{flesch_re_simplified_spa_12} (spa/12)')
    print(f'\t{flesch_re_simplified_other_12} (other/12)')

    assert flesch_re_simplified_eng_12 == 1.599 * (9 / 12 * 100) - 1.015 * (12 / 3) - 31.517
    assert flesch_re_simplified_spa_12 != wl_measures_readability.NO_SUPPORT
    assert flesch_re_simplified_other_12 == wl_measures_readability.NO_SUPPORT

def test_flesch_kincaid_grade_level():
    gl_eng_12 = wl_measures_readability.flesch_kincaid_grade_level(main, test_text_eng_12)
    gl_spa_12 = wl_measures_readability.flesch_kincaid_grade_level(main, test_text_spa_12)
    gl_other_12 = wl_measures_readability.flesch_kincaid_grade_level(main, test_text_other_12)

    print(f'Flesch-Kincaid Grade Level:')
    print(f'\t{gl_eng_12} (eng/12)')
    print(f'\t{gl_spa_12} (spa/12)')
    print(f'\t{gl_other_12} (other/12)')

    assert gl_eng_12 == 0.39 * (12 / 3) + 11.8 * (15 / 12) - 15.59
    assert gl_spa_12 != wl_measures_readability.NO_SUPPORT
    assert gl_other_12 == wl_measures_readability.NO_SUPPORT

def test_forcast_grade_level():
    rgl_eng_12 = wl_measures_readability.forcast_grade_level(main, test_text_eng_12)
    rgl_eng_150 = wl_measures_readability.forcast_grade_level(main, test_text_eng_150)
    rgl_spa_150 = wl_measures_readability.forcast_grade_level(main, test_text_spa_150)
    rgl_other_12 = wl_measures_readability.forcast_grade_level(main, test_text_other_12)

    print(f'FORCAST Grade Level:')
    print(f'\t{rgl_eng_12} (eng/12)')
    print(f'\t{rgl_eng_150} (eng/150)')
    print(f'\t{rgl_spa_150} (spa/150)')
    print(f'\t{rgl_other_12} (other/12)')

    assert rgl_eng_12 == wl_measures_readability.TEXT_TOO_SHORT
    assert rgl_eng_150 == 20.43 - 0.11 * (6 * 18 + 4)
    assert rgl_spa_150 != wl_measures_readability.NO_SUPPORT
    assert rgl_other_12 == wl_measures_readability.NO_SUPPORT

def test_gunning_fog_index():
    fog_index_eng_12_propn = wl_measures_readability.gunning_fog_index(main, test_text_eng_12_propn)
    fog_index_spa_12 = wl_measures_readability.gunning_fog_index(main, test_text_spa_12)
    fog_index_other_12 = wl_measures_readability.gunning_fog_index(main, test_text_other_12)

    print(f'Gunning Fog Index:')
    print(f'\t{fog_index_eng_12_propn} (eng/12)')
    print(f'\t{fog_index_spa_12} (spa/12)')
    print(f'\t{fog_index_other_12} (other/12)')

    assert fog_index_eng_12_propn == 0.4 * (12 / 3 + 1 / 12 * 100)
    assert fog_index_spa_12 == fog_index_other_12 == wl_measures_readability.NO_SUPPORT

def test_smog_grade():
    g_eng_12 = wl_measures_readability.smog_grade(main, test_text_eng_12)
    g_eng_120 = wl_measures_readability.smog_grade(main, test_text_eng_120)
    g_spa_120 = wl_measures_readability.smog_grade(main, test_text_spa_120)
    g_other_12 = wl_measures_readability.smog_grade(main, test_text_other_12)

    print(f'SMOG Grade:')
    print(f'\t{g_eng_12} (eng/12)')
    print(f'\t{g_eng_120} (eng/120)')
    print(f'\t{g_spa_120} (spa/120)')
    print(f'\t{g_other_12} (other/12)')

    assert g_eng_12 == wl_measures_readability.TEXT_TOO_SHORT
    assert g_eng_120 == 3.1291 + 1.043 * (15 ** 0.5)
    assert g_spa_120 != wl_measures_readability.NO_SUPPORT
    assert g_other_12 == wl_measures_readability.NO_SUPPORT

def test_spache_grade_level():
    grade_level_eng_12 = wl_measures_readability.spache_grade_level(main, test_text_eng_12)
    grade_level_eng_100 = wl_measures_readability.spache_grade_level(main, test_text_eng_100)
    grade_level_spa_12 = wl_measures_readability.spache_grade_level(main, test_text_spa_12)
    grade_level_other_12 = wl_measures_readability.spache_grade_level(main, test_text_other_12)

    print(f'Spache Grade Level:')
    print(f'\t{grade_level_eng_12} (eng/12)')
    print(f'\t{grade_level_eng_100} (eng/100)')
    print(f'\t{grade_level_spa_12} (spa/12)')
    print(f'\t{grade_level_other_12} (other/12)')

    assert grade_level_eng_12 == wl_measures_readability.TEXT_TOO_SHORT
    assert grade_level_eng_100 == numpy.mean([0.141 * (100 / 25) + 0.086 * (25 / 100 * 100) + 0.839] * 3)
    assert grade_level_spa_12 == grade_level_other_12 == wl_measures_readability.NO_SUPPORT

def test_write_score():
    score_eng_12 = wl_measures_readability.write_score(main, test_text_eng_12)
    score_eng_100 = wl_measures_readability.write_score(main, test_text_eng_100)
    score_spa_12 = wl_measures_readability.write_score(main, test_text_spa_12)
    score_other_12 = wl_measures_readability.write_score(main, test_text_other_12)

    print(f'Write Score:')
    print(f'\t{score_eng_12} (eng/12)')
    print(f'\t{score_eng_100} (eng/100)')
    print(f'\t{score_spa_12} (spa/12)')
    print(f'\t{score_other_12} (other/12)')

    assert score_eng_12 == wl_measures_readability.TEXT_TOO_SHORT
    assert score_eng_100 == 50 + 3 * 25
    assert score_spa_12 != wl_measures_readability.NO_SUPPORT
    assert score_other_12 == wl_measures_readability.NO_SUPPORT

if __name__ == '__main__':
    test_automated_readability_index()
    test_coleman_liau_index()
    test_dale_chall_readability_score()
    test_devereux_readability_index()
    test_flesch_reading_ease()
    test_flesch_reading_ease_simplified()
    test_flesch_kincaid_grade_level()
    test_forcast_grade_level()
    test_gunning_fog_index()
    test_smog_grade()
    test_spache_grade_level()
    test_write_score()
