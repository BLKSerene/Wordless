# ----------------------------------------------------------------------
# Wordless: Tests - Measures - Readability
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

import math

import numpy

from tests import wl_test_init
from wordless.wl_measures import wl_measures_readability

class Wl_Test_Text():
    def __init__(self, tokens_multilevel, lang = 'eng_us'):
        super().__init__()

        self.main = main
        self.lang = lang
        self.tokens_multilevel = tokens_multilevel

main = wl_test_init.Wl_Test_Main()
settings = main.settings_custom['measures']['readability']

TOKENS_MULTILEVEL_0 = []
TOKENS_MULTILEVEL_12 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]], [[['This', 'is', 'a', 'sen-tence0', '.']]]]
TOKENS_MULTILEVEL_12_PROPN = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]], [[['Louisiana', 'readability', 'boxes', 'created', '.']]]]
TOKENS_MULTILEVEL_100 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]]] * 12 + [[[['This', 'is', 'a', 'sen-tence0', '.']]]]
TOKENS_MULTILEVEL_120 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'metropolis', '.']]]] * 15
TOKENS_MULTILEVEL_150 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]]] * 18 + [[[['This', 'is', 'a', 'sen-tence0', 'for', 'testing', '.']]]]

test_text_eng_0 = Wl_Test_Text(TOKENS_MULTILEVEL_0)
test_text_eng_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12)
test_text_eng_12_propn = Wl_Test_Text(TOKENS_MULTILEVEL_12_PROPN)
test_text_eng_100 = Wl_Test_Text(TOKENS_MULTILEVEL_100)
test_text_eng_120 = Wl_Test_Text(TOKENS_MULTILEVEL_120)
test_text_eng_150 = Wl_Test_Text(TOKENS_MULTILEVEL_150)

test_text_ara_0 = Wl_Test_Text(TOKENS_MULTILEVEL_0, lang = 'ara')
test_text_ara_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'ara')

test_text_deu_0 = Wl_Test_Text(TOKENS_MULTILEVEL_0, lang = 'deu_de')
test_text_deu_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'deu_de')

test_text_ita_0 = Wl_Test_Text(TOKENS_MULTILEVEL_0, lang = 'ita')
test_text_ita_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'ita')

test_text_spa_0 = Wl_Test_Text(TOKENS_MULTILEVEL_0, lang = 'spa')
test_text_spa_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'spa')
test_text_spa_100 = Wl_Test_Text(TOKENS_MULTILEVEL_100, lang = 'spa')
test_text_spa_120 = Wl_Test_Text(TOKENS_MULTILEVEL_120, lang = 'spa')
test_text_spa_150 = Wl_Test_Text(TOKENS_MULTILEVEL_150, lang = 'spa')

test_text_afr_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'afr')
test_text_nld_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'nld')
test_text_fra_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'fra')
test_text_pol_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'pol')
test_text_rus_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'rus')

test_text_other_12 = Wl_Test_Text(TOKENS_MULTILEVEL_12, lang = 'other')
test_text_other_100 = Wl_Test_Text(TOKENS_MULTILEVEL_100, lang = 'other')

def test_aari():
    aari_ara_0 = wl_measures_readability.aari(main, test_text_ara_0)
    aari_ara_12 = wl_measures_readability.aari(main, test_text_ara_12)
    aari_eng_12 = wl_measures_readability.aari(main, test_text_eng_12)

    print('Automated Arabic Readability Index:')
    print(f'\tara/0: {aari_ara_0}')
    print(f'\tara/12: {aari_ara_12}')
    print(f'\teng/12: {aari_eng_12}')

    assert aari_ara_0 == 'text_too_short'
    assert aari_ara_12 == 3.28 * 46 + 1.43 * (46 / 12) + 1.24 * (12 / 3)
    assert aari_eng_12 == 'no_support'

def test_ari():
    ari_eng_0 = wl_measures_readability.ari(main, test_text_eng_0)
    settings['ari']['use_navy_variant'] = False
    ari_eng_12 = wl_measures_readability.ari(main, test_text_eng_12)
    settings['ari']['use_navy_variant'] = True
    ari_eng_12_navy = wl_measures_readability.ari(main, test_text_eng_12)
    ari_spa_12 = wl_measures_readability.ari(main, test_text_spa_12)

    print('Automated Readability Index:')
    print(f'\teng/0: {ari_eng_0}')
    print(f'\teng/12: {ari_eng_12}')
    print(f'\teng/12-navy: {ari_eng_12_navy}')
    print(f'\tspa/12: {ari_spa_12}')

    assert ari_eng_0 == 'text_too_short'
    assert ari_eng_12 == 0.5 * (12 / 3) + 4.71 * (47 / 12) - 21.43
    assert ari_eng_12_navy == ari_spa_12 == 0.37 * (12 / 3) + 5.84 * (47 / 12) - 26.01

def test_bormuths_cloze_mean():
    m_eng_0 = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_0)
    m_eng_12 = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_12)
    m_other_12 = wl_measures_readability.bormuths_cloze_mean(main, test_text_other_12)

    print("Bormuth's Cloze Mean:")
    print(f'\teng/0: {m_eng_0}')
    print(f'\teng/12: {m_eng_12}')
    print(f'\tother/12: {m_other_12}')

    assert m_eng_0 == 'text_too_short'
    assert m_eng_12 == (
        0.886593 -
        0.083640 * (45 / 12) +
        0.161911 * ((1 / 12)**3) -
        0.021401 * (12 / 3) +
        0.000577 * ((12 / 3)**2) -
        0.000005 * ((12 / 3)**3)
    )
    assert m_other_12 == 'no_support'

def test_bormuths_gp():
    gp_eng_0 = wl_measures_readability.bormuths_gp(main, test_text_eng_0)
    gp_eng_12 = wl_measures_readability.bormuths_gp(main, test_text_eng_12)
    gp_other_12 = wl_measures_readability.bormuths_gp(main, test_text_other_12)

    print("Bormuth's Grade Placement:")
    print(f'\teng/0: {gp_eng_0}')
    print(f'\teng/12: {gp_eng_12}')
    print(f'\tother/12: {gp_other_12}')

    m = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_12)
    c = 0.35

    assert gp_eng_0 == 'text_too_short'
    assert gp_eng_12 == (
        4.275 + 12.881 * m - 34.934 * (m**2) + 20.388 * (m**3) +
        26.194 * c - 2.046 * (c**2) - 11.767 * (c**3) -
        44.285 * (m * c) + 97.620 * ((m * c)**2) - 59.538 * ((m * c)**3)
    )
    assert gp_other_12 == 'no_support'

def test_coleman_liau_index():
    grade_level_eng_0 = wl_measures_readability.coleman_liau_index(main, test_text_eng_0)
    grade_level_eng_12 = wl_measures_readability.coleman_liau_index(main, test_text_eng_12)
    grade_level_spa_12 = wl_measures_readability.coleman_liau_index(main, test_text_spa_12)

    print('Coleman-Liau Index:')
    print(f'\teng/0: {grade_level_eng_0}')
    print(f'\teng/12: {grade_level_eng_12}')
    print(f'\tspa/12: {grade_level_spa_12}')

    est_cloze_pct = 141.8401 - 0.21459 * (45 / 12 * 100) + 1.079812 * (3 / 12 * 100)

    assert grade_level_eng_0 == 'text_too_short'
    assert grade_level_eng_12 == grade_level_spa_12 == -27.4004 * (est_cloze_pct / 100) + 23.06395

def test_colemans_readability_formula():
    cloze_pct_eng_0 = wl_measures_readability.colemans_readability_formula(main, test_text_eng_0)
    settings['colemans_readability_formula']['variant'] = '1'
    cloze_pct_eng_12_1 = wl_measures_readability.colemans_readability_formula(main, test_text_eng_12)
    settings['colemans_readability_formula']['variant'] = '2'
    cloze_pct_eng_12_2 = wl_measures_readability.colemans_readability_formula(main, test_text_eng_12)
    settings['colemans_readability_formula']['variant'] = '3'
    cloze_pct_eng_12_3 = wl_measures_readability.colemans_readability_formula(main, test_text_eng_12)
    settings['colemans_readability_formula']['variant'] = '4'
    cloze_pct_eng_12_4 = wl_measures_readability.colemans_readability_formula(main, test_text_eng_12)
    cloze_pct_spa_12 = wl_measures_readability.colemans_readability_formula(main, test_text_spa_12)
    cloze_pct_other_12 = wl_measures_readability.colemans_readability_formula(main, test_text_other_12)

    print("Coleman's Readability Formula:")
    print(f'\teng/0: {cloze_pct_eng_0}')
    print(f'\teng/12-1: {cloze_pct_eng_12_1}')
    print(f'\teng/12-2: {cloze_pct_eng_12_2}')
    print(f'\teng/12-3: {cloze_pct_eng_12_3}')
    print(f'\teng/12-4: {cloze_pct_eng_12_4}')
    print(f'\tspa/12: {cloze_pct_spa_12}')
    print(f'\tother/12: {cloze_pct_other_12}')

    assert cloze_pct_eng_0 == 'text_too_short'
    assert cloze_pct_eng_12_1 == 1.29 * (9 / 12 * 100) - 38.45
    assert cloze_pct_eng_12_2 == 1.16 * (9 / 12 * 100) + 1.48 * (3 / 12 * 100) - 37.95
    assert cloze_pct_eng_12_3 == 1.07 * (9 / 12 * 100) + 1.18 * (3 / 12 * 100) + 0.76 * (0 / 12 * 100) - 34.02
    assert cloze_pct_eng_12_4 == 1.04 * (9 / 12 * 100) + 1.06 * (3 / 12 * 100) + 0.56 * (0 / 12 * 100) - 0.36 * (0 / 12) - 26.01
    assert cloze_pct_spa_12 != 'no_support'
    assert cloze_pct_other_12 == 'no_support'

def test_dale_chall_readability_formula():
    x_c50_eng_0 = wl_measures_readability.dale_chall_readability_formula(main, test_text_eng_0)
    x_c50_eng_12 = wl_measures_readability.dale_chall_readability_formula(main, test_text_eng_12)
    x_c50_spa_12 = wl_measures_readability.dale_chall_readability_formula(main, test_text_spa_12)

    print('Dale-Chall Readability Formula:')
    print(f'\teng/0: {x_c50_eng_0}')
    print(f'\teng/12: {x_c50_eng_12}')
    print(f'\tspa/12: {x_c50_spa_12}')

    assert x_c50_eng_0 == 'text_too_short'
    assert x_c50_eng_12 == 0.1579 * (1 / 12 * 100) + 0.0496 * (12 / 3) + 3.6365
    assert x_c50_spa_12 == 'no_support'

def test_dale_chall_readability_formula_new():
    x_c50_eng_0 = wl_measures_readability.dale_chall_readability_formula_new(main, test_text_eng_0)
    x_c50_eng_12 = wl_measures_readability.dale_chall_readability_formula_new(main, test_text_eng_12)
    x_c50_spa_12 = wl_measures_readability.dale_chall_readability_formula_new(main, test_text_spa_12)

    print('Dale-Chall Readability Formula (New):')
    print(f'\teng/0: {x_c50_eng_0}')
    print(f'\teng/12: {x_c50_eng_12}')
    print(f'\tspa/12: {x_c50_spa_12}')

    assert x_c50_eng_0 == 'text_too_short'
    assert x_c50_eng_12 == 64 - 0.95 * (1 / 12 * 100) - 0.69 * (12 / 3)
    assert x_c50_spa_12 == 'no_support'

def test_danielson_bryans_readability_formula():
    danielson_bryan_eng_0 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_eng_0)
    settings['danielson_bryans_readability_formula']['variant'] = '1'
    danielson_bryan_eng_12_1 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_eng_12)
    settings['danielson_bryans_readability_formula']['variant'] = '2'
    danielson_bryan_eng_12_2 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_eng_12)
    danielson_bryan_other_12 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_other_12)

    print("Danielson-Bryan's Readability Formula:")
    print(f'\teng/0: {danielson_bryan_eng_0}')
    print(f'\teng/12-1: {danielson_bryan_eng_12_1}')
    print(f'\teng/12-2: {danielson_bryan_eng_12_2}')
    print(f'\tother/12: {danielson_bryan_other_12}')

    assert danielson_bryan_eng_0 == 'text_too_short'
    assert danielson_bryan_eng_12_1 == 1.0364 * (47 / (12 - 1)) + 0.0194 * (47 / 3) - 0.6059
    assert danielson_bryan_eng_12_2 == danielson_bryan_other_12 == 131.059 - 10.364 * (47 / (12 - 1)) - 0.194 * (47 / 3)

def test_drp():
    drp_eng_0 = wl_measures_readability.drp(main, test_text_eng_0)
    drp_eng_12 = wl_measures_readability.drp(main, test_text_eng_12)
    drp_other_12 = wl_measures_readability.drp(main, test_text_other_12)

    print('Degrees of Reading Power:')
    print(f'\teng/0: {drp_eng_0}')
    print(f'\teng/12: {drp_eng_12}')
    print(f'\tother/12: {drp_other_12}')

    assert drp_eng_0 == 'text_too_short'
    m = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_12)
    assert drp_eng_12 == 100 - math.floor(m * 100 + 0.5)
    assert drp_other_12 == 'no_support'

def test_devereux_readability_index():
    grade_placement_eng_0 = wl_measures_readability.devereux_readability_index(main, test_text_eng_0)
    grade_placement_eng_12 = wl_measures_readability.devereux_readability_index(main, test_text_eng_12)
    grade_placement_spa_12 = wl_measures_readability.devereux_readability_index(main, test_text_spa_12)

    print('Devereux Readability Index:')
    print(f'\teng/0: {grade_placement_eng_0}')
    print(f'\teng/12: {grade_placement_eng_12}')
    print(f'\tspa/12: {grade_placement_spa_12}')

    assert grade_placement_eng_0 == 'text_too_short'
    assert grade_placement_eng_12 == grade_placement_spa_12 == 1.56 * (47 / 12) + 0.19 * (12 / 3) - 6.49

def test_elf():
    elf_eng_0 = wl_measures_readability.elf(main, test_text_eng_0)
    elf_eng_12 = wl_measures_readability.elf(main, test_text_eng_12)
    elf_spa_12 = wl_measures_readability.elf(main, test_text_spa_12)
    elf_other_12 = wl_measures_readability.elf(main, test_text_other_12)

    print('Easy Listening Formula:')
    print(f'\teng/0: {elf_eng_0}')
    print(f'\teng/12: {elf_eng_12}')
    print(f'\tspa/12: {elf_spa_12}')
    print(f'\tother/12: {elf_other_12}')

    assert elf_eng_0 == 'text_too_short'
    assert elf_eng_12 == (15 - 12) / 3
    assert elf_spa_12 != 'no_support'
    assert elf_other_12 == 'no_support'

def test_gl():
    gl_eng_0 = wl_measures_readability.gl(main, test_text_eng_0)
    gl_eng_12 = wl_measures_readability.gl(main, test_text_eng_12)
    gl_spa_12 = wl_measures_readability.gl(main, test_text_spa_12)
    gl_other_12 = wl_measures_readability.gl(main, test_text_other_12)

    print('Flesch-Kincaid Grade Level:')
    print(f'\teng/0: {gl_eng_0}')
    print(f'\teng/12: {gl_eng_12}')
    print(f'\tspa/12: {gl_spa_12}')
    print(f'\tother/12: {gl_other_12}')

    assert gl_eng_0 == 'text_too_short'
    assert gl_eng_12 == 0.39 * (12 / 3) + 11.8 * (15 / 12) - 15.59
    assert gl_spa_12 != 'no_support'
    assert gl_other_12 == 'no_support'

def test_re_flesch():
    flesch_re_eng_0 = wl_measures_readability.re_flesch(main, test_text_eng_0)
    flesch_re_eng_12 = wl_measures_readability.re_flesch(main, test_text_eng_12)

    settings['re']['variant_nld'] = 'Douma'
    flesch_re_nld_12_douma = wl_measures_readability.re_flesch(main, test_text_nld_12)
    settings['re']['variant_nld'] = "Brouwer's Leesindex A"
    flesch_re_nld_12_brouwer = wl_measures_readability.re_flesch(main, test_text_nld_12)

    flesch_re_fra_12 = wl_measures_readability.re_flesch(main, test_text_fra_12)
    flesch_re_deu_12 = wl_measures_readability.re_flesch(main, test_text_deu_12)
    flesch_re_ita_12 = wl_measures_readability.re_flesch(main, test_text_ita_12)
    flesch_re_rus_12 = wl_measures_readability.re_flesch(main, test_text_rus_12)

    settings['re']['variant_spa'] = 'Fernández Huerta'
    flesch_re_spa_12_fh = wl_measures_readability.re_flesch(main, test_text_spa_12)
    settings['re']['variant_spa'] = 'Szigriszt Pazos'
    flesch_re_spa_12_sp = wl_measures_readability.re_flesch(main, test_text_spa_12)

    flesch_re_afr_12 = wl_measures_readability.re_flesch(main, test_text_afr_12)
    flesch_re_other_12 = wl_measures_readability.re_flesch(main, test_text_other_12)

    print('Flesch Reading Ease:')
    print(f'\teng/0: {flesch_re_eng_0}')
    print(f'\teng/12: {flesch_re_eng_12}')
    print(f'\tnld/12-douma: {flesch_re_nld_12_douma}')
    print(f'\tnld/12-brouwer: {flesch_re_nld_12_brouwer}')
    print(f'\tfra/12: {flesch_re_fra_12}')
    print(f'\tdeu/12: {flesch_re_deu_12}')
    print(f'\tita/12: {flesch_re_ita_12}')
    print(f'\trus/12: {flesch_re_rus_12}')
    print(f'\tspa/12-fh: {flesch_re_spa_12_fh}')
    print(f'\tspa/12-sp: {flesch_re_spa_12_sp}')
    print(f'\tafr/12: {flesch_re_afr_12}')
    print(f'\tother/12: {flesch_re_other_12}')

    assert flesch_re_eng_0 == 'text_too_short'
    assert flesch_re_eng_12 == 206.835 - 0.846 * (15 / 12 * 100) - 1.015 * (12 / 3)
    assert flesch_re_nld_12_douma == 206.84 - 77 * (18 / 12) - 0.93 * (12 / 3)
    assert flesch_re_nld_12_brouwer == 195 - (200 / 3) * (18 / 12) - 2 * (12 / 3)
    assert flesch_re_fra_12 == 207 - 73.6 * (16 / 12) - 1.015 * (12 / 3)
    assert flesch_re_deu_12 == 180 - 58.5 * (15 / 12) - (12 / 3)
    assert flesch_re_ita_12 == 217 - 60 * (19 / 12) - 1.3 * (12 / 3)
    assert flesch_re_rus_12 == 206.835 - 60.1 * (13 / 12) - 1.3 * (12 / 3)
    assert flesch_re_spa_12_fh == 206.84 - 60 * (18 / 12) - 1.02 * (12 / 3)
    assert flesch_re_spa_12_sp == 206.84 - 62.3 * (18 / 12) - (12 / 3)
    assert flesch_re_afr_12 == 206.835 - 0.846 * (18 / 12 * 100) - 1.015 * (12 / 3)
    assert flesch_re_other_12 == 'no_support'

def test_re_simplified():
    flesch_re_simplified_eng_0 = wl_measures_readability.re_simplified(main, test_text_eng_0)
    flesch_re_simplified_eng_12 = wl_measures_readability.re_simplified(main, test_text_eng_12)
    flesch_re_simplified_spa_12 = wl_measures_readability.re_simplified(main, test_text_spa_12)
    flesch_re_simplified_other_12 = wl_measures_readability.re_simplified(main, test_text_other_12)

    print('Flesch Reading Ease (Simplified):')
    print(f'\teng/0: {flesch_re_simplified_eng_0}')
    print(f'\teng/12: {flesch_re_simplified_eng_12}')
    print(f'\tspa/12: {flesch_re_simplified_spa_12}')
    print(f'\tother/12: {flesch_re_simplified_other_12}')

    assert flesch_re_simplified_eng_0 == 'text_too_short'
    assert flesch_re_simplified_eng_12 == flesch_re_simplified_spa_12 == 1.599 * (9 / 12 * 100) - 1.015 * (12 / 3) - 31.517
    assert flesch_re_simplified_other_12 == 'no_support'

def test_rgl():
    rgl_eng_12 = wl_measures_readability.rgl(main, test_text_eng_12)
    rgl_eng_150 = wl_measures_readability.rgl(main, test_text_eng_150)
    rgl_spa_150 = wl_measures_readability.rgl(main, test_text_spa_150)
    rgl_other_12 = wl_measures_readability.rgl(main, test_text_other_12)

    print('FORCAST Grade Level:')
    print(f'\teng/12: {rgl_eng_12}')
    print(f'\teng/150: {rgl_eng_150}')
    print(f'\tspa/150: {rgl_spa_150}')
    print(f'\tother/12: {rgl_other_12}')

    assert rgl_eng_12 == 'text_too_short'
    assert rgl_eng_150 == rgl_spa_150 == 20.43 - 0.11 * (6 * 18 + 4)
    assert rgl_other_12 == 'no_support'

def test_cp():
    cp_spa_0 = wl_measures_readability.cp(main, test_text_spa_0)
    cp_spa_12 = wl_measures_readability.cp(main, test_text_spa_12)
    cp_eng_12 = wl_measures_readability.cp(main, test_text_eng_12)

    print('Fórmula de Comprensibilidad de Gutiérrez de Polini:')
    print(f'\tspa/0: {cp_spa_0}')
    print(f'\tspa/12: {cp_spa_12}')
    print(f'\teng/12: {cp_eng_12}')

    assert cp_spa_0 == 'text_too_short'
    assert cp_spa_12 == 95.2 - 9.7 * (45 / 12) - 0.35 * (12 / 3)
    assert cp_eng_12 == 'no_support'

def test_formula_de_crawford():
    grade_level_spa_0 = wl_measures_readability.formula_de_crawford(main, test_text_spa_0)
    grade_level_spa_12 = wl_measures_readability.formula_de_crawford(main, test_text_spa_12)
    grade_level_eng_12 = wl_measures_readability.formula_de_crawford(main, test_text_eng_12)

    print('Fórmula de Crawford:')
    print(f'\tspa/0: {grade_level_spa_0}')
    print(f'\tspa/12: {grade_level_spa_12}')
    print(f'\teng/12: {grade_level_eng_12}')

    assert grade_level_spa_0 == 'text_too_short'
    assert grade_level_spa_12 == 3 / 12 * 100 * (-0.205) + 18 / 12 * 100 * 0.049 - 3.407
    assert grade_level_eng_12 == 'no_support'

def test_fuckss_stilcharakteristik():
    stilcharakteristik_eng_0 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_eng_0)
    stilcharakteristik_eng_12 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_eng_12)
    stilcharakteristik_spa_12 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_spa_12)
    stilcharakteristik_other_12 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_other_12)

    print("Fucks's Stilcharakteristik:")
    print(f'\teng/0: {stilcharakteristik_eng_0}')
    print(f'\teng/12: {stilcharakteristik_eng_12}')
    print(f'\tspa/12: {stilcharakteristik_spa_12}')
    print(f'\tother/12: {stilcharakteristik_other_12}')

    assert stilcharakteristik_eng_0 == 'text_too_short'
    assert stilcharakteristik_eng_12 == 15 / 3
    assert stilcharakteristik_spa_12 != 'no_support'
    assert stilcharakteristik_other_12 == 'no_support'

def test_gulpease_index():
    gulpease_index_ita_0 = wl_measures_readability.gulpease_index(main, test_text_ita_0)
    gulpease_index_ita_12 = wl_measures_readability.gulpease_index(main, test_text_ita_12)
    gulpease_index_eng_12 = wl_measures_readability.gulpease_index(main, test_text_eng_12)

    print('Gulpease Index:')
    print(f'\tita/0: {gulpease_index_ita_0}')
    print(f'\tita/12: {gulpease_index_ita_12}')
    print(f'\teng/12: {gulpease_index_eng_12}')

    assert gulpease_index_ita_0 == 'text_too_short'
    assert gulpease_index_ita_12 == 89 + (300 * 3 - 10 * 45) / 12
    assert gulpease_index_eng_12 == 'no_support'

def test_fog_index():
    fog_index_eng_0 = wl_measures_readability.fog_index(main, test_text_eng_0)
    settings['fog_index']['use_navy_variant_for_eng'] = False
    fog_index_eng_12_propn = wl_measures_readability.fog_index(main, test_text_eng_12_propn)
    settings['fog_index']['use_navy_variant_for_eng'] = True
    fog_index_eng_12_navy = wl_measures_readability.fog_index(main, test_text_eng_12)
    fog_index_pol_12 = wl_measures_readability.fog_index(main, test_text_pol_12)
    fog_index_spa_12 = wl_measures_readability.fog_index(main, test_text_spa_12)

    print('Gunning Fog Index:')
    print(f'\teng/0: {fog_index_eng_0}')
    print(f'\teng/12: {fog_index_eng_12_propn}')
    print(f'\teng/12-navy: {fog_index_eng_12_navy}')
    print(f'\tpol/12: {fog_index_pol_12}')
    print(f'\tspa/12: {fog_index_spa_12}')

    assert fog_index_eng_0 == 'text_too_short'
    assert fog_index_eng_12_propn == 0.4 * (12 / 3 + 1 / 12 * 100)
    assert fog_index_eng_12_navy == ((12 + 2 * 0) / 3 - 3) / 2
    assert fog_index_pol_12 == 0.4 * (12 / 3 + 1 / 12 * 100)
    assert fog_index_spa_12 == 'no_support'

def test_mu():
    mu_spa_0 = wl_measures_readability.mu(main, test_text_spa_0)
    mu_spa_12 = wl_measures_readability.mu(main, test_text_spa_12)
    mu_eng_12 = wl_measures_readability.mu(main, test_text_eng_12)

    print('Legibilidad µ:')
    print(f'\tspa/0: {mu_spa_0}')
    print(f'\tspa/12: {mu_spa_12}')
    print(f'\teng/12: {mu_eng_12}')

    assert mu_spa_0 == 'text_too_short'
    assert mu_spa_12 == (12 / 11) * (3.75 / 7.1875) * 100
    assert mu_eng_12 == 'no_support'

def test_lensear_write():
    score_eng_0 = wl_measures_readability.lensear_write(main, test_text_eng_0)
    score_eng_12 = wl_measures_readability.lensear_write(main, test_text_eng_12)
    score_eng_100 = wl_measures_readability.lensear_write(main, test_text_eng_100)
    score_spa_100 = wl_measures_readability.lensear_write(main, test_text_spa_100)

    print('Lensear Write:')
    print(f'\teng/0: {score_eng_0}')
    print(f'\teng/12: {score_eng_12}')
    print(f'\teng/100: {score_eng_100}')
    print(f'\tspa/100: {score_spa_100}')

    assert score_eng_0 == 'text_too_short'
    assert score_eng_12 == 6 * (100 / 12) + 3 * 3 * (100 / 12)
    assert score_eng_100 == 50 + 3 * 25
    assert score_spa_100 == 'no_support'

def test_lix():
    lix_eng_0 = wl_measures_readability.lix(main, test_text_eng_0)
    lix_eng_12 = wl_measures_readability.lix(main, test_text_eng_12)
    lix_spa_12 = wl_measures_readability.lix(main, test_text_spa_12)

    print('Lix:')
    print(f'\teng/0: {lix_eng_0}')
    print(f'\teng/12: {lix_eng_12}')
    print(f'\tspa/12: {lix_spa_12}')

    assert lix_eng_0 == 'text_too_short'
    assert lix_eng_12 == 12 / 3 + 100 * (3 / 12)
    assert lix_spa_12 != 'no_support'

def test_eflaw():
    eflaw_eng_0 = wl_measures_readability.eflaw(main, test_text_eng_0)
    eflaw_eng_12 = wl_measures_readability.eflaw(main, test_text_eng_12)
    eflaw_spa_12 = wl_measures_readability.eflaw(main, test_text_spa_12)

    print('McAlpine EFLAW Readability Score:')
    print(f'\teng/0: {eflaw_eng_0}')
    print(f'\teng/12: {eflaw_eng_12}')
    print(f'\tspa/12: {eflaw_spa_12}')

    assert eflaw_eng_0 == 'text_too_short'
    assert eflaw_eng_12 == (12 + 6) / 3
    assert eflaw_spa_12 == 'no_support'

def test_osman():
    osman_ara_0 = wl_measures_readability.osman(main, test_text_ara_0)
    osman_ara_12 = wl_measures_readability.osman(main, test_text_ara_12)
    osman_eng_12 = wl_measures_readability.osman(main, test_text_eng_12)

    print('OSMAN:')
    print(f'\tara/0: {osman_ara_0}')
    print(f'\tara/12: {osman_ara_12}')
    print(f'\teng/12: {osman_eng_12}')

    assert osman_ara_0 == 'text_too_short'
    assert osman_ara_12 == 200.791 - 1.015 * (12 / 3) - 24.181 * ((3 + 23 + 3 + 0) / 12)
    assert osman_eng_12 == 'no_support'

def test_rix():
    rix_eng_0 = wl_measures_readability.rix(main, test_text_eng_0)
    rix_eng_12 = wl_measures_readability.rix(main, test_text_eng_12)
    rix_spa_12 = wl_measures_readability.rix(main, test_text_spa_12)

    print('Rix:')
    print(f'\teng/0: {rix_eng_0}')
    print(f'\teng/12: {rix_eng_12}')
    print(f'\tspa/12: {rix_spa_12}')

    assert rix_eng_0 == 'text_too_short'
    assert rix_eng_12 == rix_spa_12 == 3 / 3

def test_smog_grade():
    g_eng_12 = wl_measures_readability.smog_grade(main, test_text_eng_12)
    g_eng_120 = wl_measures_readability.smog_grade(main, test_text_eng_120)
    g_spa_120 = wl_measures_readability.smog_grade(main, test_text_spa_120)
    g_other_12 = wl_measures_readability.smog_grade(main, test_text_other_12)

    print('SMOG Grade:')
    print(f'\teng/12: {g_eng_12}')
    print(f'\teng/120: {g_eng_120}')
    print(f'\tspa/120: {g_spa_120}')
    print(f'\tother/12: {g_other_12}')

    assert g_eng_12 == 'text_too_short'
    assert g_eng_120 == 3.1291 + 1.043 * (15 ** 0.5)
    assert g_spa_120 != 'no_support'
    assert g_other_12 == 'no_support'

def test_spache_grade_lvl():
    grade_lvl_eng_12 = wl_measures_readability.spache_grade_lvl(main, test_text_eng_12)
    settings['spache_grade_lvl']['use_rev_formula'] = True
    grade_lvl_eng_100_rev = wl_measures_readability.spache_grade_lvl(main, test_text_eng_100)
    settings['spache_grade_lvl']['use_rev_formula'] = False
    grade_lvl_eng_100 = wl_measures_readability.spache_grade_lvl(main, test_text_eng_100)
    grade_lvl_spa_100 = wl_measures_readability.spache_grade_lvl(main, test_text_spa_100)

    print('Spache Grade Level:')
    print(f'\teng/12: {grade_lvl_eng_12}')
    print(f'\teng/100-rev: {grade_lvl_eng_100_rev}')
    print(f'\teng/100: {grade_lvl_eng_100}')
    print(f'\tspa/100: {grade_lvl_spa_100}')

    assert grade_lvl_eng_12 == 'text_too_short'
    assert grade_lvl_eng_100_rev == numpy.mean([0.121 * (100 / 25) + 0.082 * 25 + 0.659] * 3)
    assert grade_lvl_eng_100 == numpy.mean([0.141 * (100 / 25) + 0.086 * 25 + 0.839] * 3)
    assert grade_lvl_spa_100 == 'no_support'

def test_strain_index():
    strain_index_eng_0 = wl_measures_readability.strain_index(main, test_text_eng_0)
    strain_index_eng_12 = wl_measures_readability.strain_index(main, test_text_eng_12)
    strain_index_spa_12 = wl_measures_readability.strain_index(main, test_text_spa_12)
    strain_index_other_12 = wl_measures_readability.strain_index(main, test_text_other_12)

    print('Strain Index:')
    print(f'\teng/0: {strain_index_eng_0}')
    print(f'\teng/12: {strain_index_eng_12}')
    print(f'\tspa/12: {strain_index_spa_12}')
    print(f'\tother/12: {strain_index_other_12}')

    assert strain_index_eng_0 == 'text_too_short'
    assert strain_index_eng_12 == 15 / 10
    assert strain_index_spa_12 != 'no_support'
    assert strain_index_other_12 == 'no_support'

def test_trankle_bailers_readability_formula():
    trankle_bailers_eng_0 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_eng_0)
    settings['trankle_bailers_readability_formula']['variant'] = '1'
    trankle_bailers_eng_100_1 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_eng_100)
    settings['trankle_bailers_readability_formula']['variant'] = '2'
    trankle_bailers_eng_100_2 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_eng_100)
    trankle_bailers_spa_100 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_spa_12)
    trankle_bailers_other_100 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_other_12)

    print("Tränkle & Bailer's Readability Formula:")
    print(f'\teng/0: {trankle_bailers_eng_0}')
    print(f'\teng/12-1: {trankle_bailers_eng_100_1}')
    print(f'\teng/12-2: {trankle_bailers_eng_100_2}')
    print(f'\tspa/12: {trankle_bailers_spa_100}')
    print(f'\tother/12: {trankle_bailers_other_100}')

    assert trankle_bailers_eng_0 == 'text_too_short'
    assert trankle_bailers_eng_100_1 == 224.6814 - 79.8304 * (376 / 100) - 12.24032 * (100 / 25) - 1.292857 * 0
    assert trankle_bailers_eng_100_2 == 234.1063 - 96.11069 * (376 / 100) - 2.05444 * 0 - 1.02805 * 0
    assert trankle_bailers_spa_100 != 'no_support'
    assert trankle_bailers_other_100 == 'no_support'

def test_wstf():
    wstf_deu_0 = wl_measures_readability.wstf(main, test_text_deu_0)
    settings['wstf']['variant'] = '1'
    wstf_deu_12_1 = wl_measures_readability.wstf(main, test_text_deu_12)
    settings['wstf']['variant'] = '2'
    wstf_deu_12_2 = wl_measures_readability.wstf(main, test_text_deu_12)
    settings['wstf']['variant'] = '3'
    wstf_deu_12_3 = wl_measures_readability.wstf(main, test_text_deu_12)
    settings['wstf']['variant'] = '4'
    wstf_deu_12_4 = wl_measures_readability.wstf(main, test_text_deu_12)
    wstf_eng_12 = wl_measures_readability.wstf(main, test_text_eng_12)

    print('Wiener Sachtextformel:')
    print(f'\tdeu/0: {wstf_deu_0}')
    print(f'\tdeu/12-1: {wstf_deu_12_1}')
    print(f'\tdeu/12-2: {wstf_deu_12_2}')
    print(f'\tdeu/12-3: {wstf_deu_12_3}')
    print(f'\tdeu/12-4: {wstf_deu_12_4}')
    print(f'\teng/12: {wstf_eng_12}')

    ms = 0 / 12
    sl = 12 / 3
    iw = 3 / 12
    es = 9 / 12

    assert wstf_deu_0 == 'text_too_short'
    assert wstf_deu_12_1 == 0.1925 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875
    assert wstf_deu_12_2 == 0.2007 * ms + 0.1682 * sl + 0.1373 * iw - 2.779
    assert wstf_deu_12_3 == 0.2963 * ms + 0.1905 * sl - 1.1144
    assert wstf_deu_12_4 == 0.2744 * ms + 0.2656 * sl - 1.693
    assert wstf_eng_12 == 'no_support'

if __name__ == '__main__':
    test_aari()
    test_ari()
    test_bormuths_cloze_mean()
    test_bormuths_gp()
    test_coleman_liau_index()
    test_colemans_readability_formula()
    test_dale_chall_readability_formula()
    test_dale_chall_readability_formula_new()
    test_danielson_bryans_readability_formula()
    test_drp()
    test_devereux_readability_index()
    test_elf()
    test_gl()
    test_re_flesch()
    test_re_simplified()
    test_rgl()
    test_cp()
    test_formula_de_crawford()
    test_fuckss_stilcharakteristik()
    test_gulpease_index()
    test_fog_index()
    test_mu()
    test_lensear_write()
    test_lix()
    test_eflaw()
    test_osman()
    test_rix()
    test_smog_grade()
    test_spache_grade_lvl()
    test_strain_index()
    test_trankle_bailers_readability_formula()
    test_wstf()
