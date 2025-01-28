# ----------------------------------------------------------------------
# Tests: Measures - Readability
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

import math

import numpy

from tests import wl_test_init
from wordless.wl_measures import wl_measures_readability

main = wl_test_init.Wl_Test_Main()
settings = main.settings_custom['measures']['readability']

TOKENS_MULTILEVEL_0 = []
TOKENS_MULTILEVEL_12 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]], [[['This', 'is', 'a', 'sen-tence0', '.']]]]
TOKENS_MULTILEVEL_12_PREP = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]], [[['From', 'beginning', 'to', 'end', '.']]]]
TOKENS_MULTILEVEL_12_PROPN = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]], [[['Louisiana', 'readability', 'boxes', 'created', '.']]]]
TOKENS_MULTILEVEL_12_HYPHEN = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]], [[['This', 'is', 'a-', 'sen-tence0', '.']]]]
TOKENS_MULTILEVEL_100 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]]] * 12 + [[[['This', 'is', 'a', 'sen-tence0', '.']]]]
TOKENS_MULTILEVEL_100_PREP = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]]] * 12 + [[[['I', 'am', 'behind', 'you', '.']]]]
TOKENS_MULTILEVEL_100_CONJ = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]]] * 12 + [[[['Go', 'ahead', 'and', 'turn', '.']]]]
TOKENS_MULTILEVEL_120 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'metropolis', '.']]]] * 15
TOKENS_MULTILEVEL_150 = [[[['This', 'is', 'a', 'sentence', '.']], [['This', 'is', 'a', 'sentence', '.']]]] * 18 + [[[['This', 'is', 'a', 'sen-tence0', 'for', 'testing', '.']]]]

test_text_eng_0 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_0)
test_text_eng_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12)
test_text_eng_12_prep = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12_PREP)
test_text_eng_12_propn = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12_PROPN)
test_text_eng_12_hyphen = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12_HYPHEN)
test_text_eng_100 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_100)
test_text_eng_100_prep = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_100_PREP)
test_text_eng_100_conj = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_100_CONJ)
test_text_eng_120 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_120)
test_text_eng_150 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_150)

test_text_ara_0 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_0, lang = 'ara')
test_text_ara_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'ara')
test_text_ara_faseeh = wl_test_init.Wl_Test_Text(main, [[[['\u064B\u064B\u0621']]]], lang = 'ara')

test_text_deu_0 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_0, lang = 'deu_de')
test_text_deu_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'deu_de')
test_text_deu_120 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_120, lang = 'deu_de')

test_text_ita_0 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_0, lang = 'ita')
test_text_ita_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'ita')

test_text_spa_0 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_0, lang = 'spa')
test_text_spa_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'spa')
test_text_spa_100 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_100, lang = 'spa')
test_text_spa_120 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_120, lang = 'spa')
test_text_spa_150 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_150, lang = 'spa')

test_text_tha_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'tha')
test_text_tha_100 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_100, lang = 'tha')

test_text_vie_0 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_0, lang = 'vie')
test_text_vie_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'vie')

test_text_afr_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'afr')
test_text_nld_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'nld')
test_text_fra_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'fra')
test_text_pol_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'pol')
test_text_rus_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'rus')
test_text_ukr_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'ukr')

test_text_other_12 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_12, lang = 'other')
test_text_other_100 = wl_test_init.Wl_Test_Text(main, TOKENS_MULTILEVEL_100, lang = 'other')

def test_rd():
    rd_ara_0 = wl_measures_readability.rd(main, test_text_ara_0)
    settings['rd']['variant'] = 'Policy One'
    rd_ara_12_policy_1 = wl_measures_readability.rd(main, test_text_ara_12)
    settings['rd']['variant'] = 'Policy Two'
    rd_ara_12_policy_2 = wl_measures_readability.rd(main, test_text_ara_12)
    rd_eng_12 = wl_measures_readability.rd(main, test_text_eng_12)

    assert rd_ara_0 == 'text_too_short'
    assert rd_ara_12_policy_1 == 4.41434307 * (45 / 12) - 13.46873475
    assert rd_ara_12_policy_2 == 0.97569509 * (45 / 12) + 0.37237998 * (12 / 3) - 0.90451827 * (12 / 5) - 1.06000414
    assert rd_eng_12 == 'no_support'

def test_aari():
    aari_ara_0 = wl_measures_readability.aari(main, test_text_ara_0)
    aari_ara_12 = wl_measures_readability.aari(main, test_text_ara_12)
    aari_eng_12 = wl_measures_readability.aari(main, test_text_eng_12)

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

    assert ari_eng_0 == 'text_too_short'
    assert ari_eng_12 == 0.5 * (12 / 3) + 4.71 * (47 / 12) - 21.43
    assert ari_eng_12_navy == ari_spa_12 == 0.37 * (12 / 3) + 5.84 * (47 / 12) - 26.01

def test_bormuths_cloze_mean():
    m_eng_0 = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_0)
    m_eng_12 = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_12)
    m_other_12 = wl_measures_readability.bormuths_cloze_mean(main, test_text_other_12)

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
    cloze_pct_tha_12 = wl_measures_readability.colemans_readability_formula(main, test_text_tha_12)
    cloze_pct_other_12 = wl_measures_readability.colemans_readability_formula(main, test_text_other_12)

    assert cloze_pct_eng_0 == 'text_too_short'
    assert cloze_pct_eng_12_1 == 1.29 * (9 / 12 * 100) - 38.45
    assert cloze_pct_eng_12_2 == 1.16 * (9 / 12 * 100) + 1.48 * (3 / 12 * 100) - 37.95
    assert cloze_pct_eng_12_3 == 1.07 * (9 / 12 * 100) + 1.18 * (3 / 12 * 100) + 0.76 * (0 / 12 * 100) - 34.02
    assert cloze_pct_eng_12_4 == 1.04 * (9 / 12 * 100) + 1.06 * (3 / 12 * 100) + 0.56 * (0 / 12 * 100) - 0.36 * (0 / 12) - 26.01
    assert cloze_pct_tha_12 != 'no_support'
    assert cloze_pct_other_12 == 'no_support'

def test_crawfords_readability_formula():
    grade_level_spa_0 = wl_measures_readability.crawfords_readability_formula(main, test_text_spa_0)
    grade_level_spa_12 = wl_measures_readability.crawfords_readability_formula(main, test_text_spa_12)
    grade_level_eng_12 = wl_measures_readability.crawfords_readability_formula(main, test_text_eng_12)

    assert grade_level_spa_0 == 'text_too_short'
    assert grade_level_spa_12 == 3 / 12 * 100 * (-0.205) + 18 / 12 * 100 * 0.049 - 3.407
    assert grade_level_eng_12 == 'no_support'

def test_x_c50():
    x_c50_eng_0 = wl_measures_readability.x_c50(main, test_text_eng_0)
    settings['x_c50']['variant'] = 'Original'
    x_c50_eng_12_orig = wl_measures_readability.x_c50(main, test_text_eng_12)
    settings['x_c50']['variant'] = 'Powers-Sumner-Kearl'
    x_c50_eng_12_psk = wl_measures_readability.x_c50(main, test_text_eng_12)
    settings['x_c50']['variant'] = 'New'
    x_c50_eng_12_new = wl_measures_readability.x_c50(main, test_text_eng_12)
    x_c50_spa_12 = wl_measures_readability.x_c50(main, test_text_spa_12)

    assert x_c50_eng_0 == 'text_too_short'
    assert x_c50_eng_12_orig == 0.1579 * (1 / 12 * 100) + 0.0496 * (12 / 3) + 3.6365
    assert x_c50_eng_12_psk == 3.2672 + 0.1155 * (1 / 12 * 100) + 0.0596 * (12 / 3)
    assert x_c50_eng_12_new == 64 - 0.95 * (1 / 12 * 100) - 0.69 * (12 / 3)
    assert x_c50_spa_12 == 'no_support'

def test_danielson_bryans_readability_formula():
    danielson_bryan_eng_0 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_eng_0)
    settings['danielson_bryans_readability_formula']['variant'] = '1'
    danielson_bryan_eng_12_1 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_eng_12)
    settings['danielson_bryans_readability_formula']['variant'] = '2'
    danielson_bryan_eng_12_2 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_eng_12)
    danielson_bryan_other_12 = wl_measures_readability.danielson_bryans_readability_formula(main, test_text_other_12)

    assert danielson_bryan_eng_0 == 'text_too_short'
    assert danielson_bryan_eng_12_1 == 1.0364 * (47 / (12 - 1)) + 0.0194 * (47 / 3) - 0.6059
    assert danielson_bryan_eng_12_2 == danielson_bryan_other_12 == 131.059 - 10.364 * (47 / (12 - 1)) - 0.194 * (47 / 3)

def test_dawoods_readability_formula():
    dawood_ara_0 = wl_measures_readability.dawoods_readability_formula(main, test_text_ara_0)
    dawood_ara_12 = wl_measures_readability.dawoods_readability_formula(main, test_text_ara_12)
    dawood_eng_12 = wl_measures_readability.dawoods_readability_formula(main, test_text_eng_12)

    assert dawood_ara_0 == 'text_too_short'
    assert dawood_ara_12 == (-0.0533) * (45 / 12) - 0.2066 * (12 / 3) + 5.5543 * (12 / 5) - 1.0801
    assert dawood_eng_12 == 'no_support'

def test_drp():
    drp_eng_0 = wl_measures_readability.drp(main, test_text_eng_0)
    drp_eng_12 = wl_measures_readability.drp(main, test_text_eng_12)
    drp_other_12 = wl_measures_readability.drp(main, test_text_other_12)

    assert drp_eng_0 == 'text_too_short'
    m = wl_measures_readability.bormuths_cloze_mean(main, test_text_eng_12)
    assert drp_eng_12 == 100 - math.floor(m * 100 + 0.5)
    assert drp_other_12 == 'no_support'

def test_devereux_readability_index():
    grade_placement_eng_0 = wl_measures_readability.devereux_readability_index(main, test_text_eng_0)
    grade_placement_eng_12 = wl_measures_readability.devereux_readability_index(main, test_text_eng_12)
    grade_placement_spa_12 = wl_measures_readability.devereux_readability_index(main, test_text_spa_12)

    assert grade_placement_eng_0 == 'text_too_short'
    assert grade_placement_eng_12 == 1.56 * (47 / 12) + 0.19 * (12 / 3) - 6.49
    assert grade_placement_spa_12 != 'text_too_short'

def test_dickes_steiwer_handformel():
    dickes_steiwer_eng_0 = wl_measures_readability.dickes_steiwer_handformel(main, test_text_eng_0)
    dickes_steiwer_eng_12 = wl_measures_readability.dickes_steiwer_handformel(main, test_text_eng_12)
    dickes_steiwer_spa_12 = wl_measures_readability.dickes_steiwer_handformel(main, test_text_spa_12)

    assert dickes_steiwer_eng_0 == 'text_too_short'
    assert dickes_steiwer_eng_12 == 235.95993 - numpy.log(45 / 12 + 1) * 73.021 - numpy.log(12 / 3 + 1) * 12.56438 - 5 / 12 * 50.03293
    assert dickes_steiwer_spa_12 != 'text_too_short'

def test_elf():
    elf_eng_0 = wl_measures_readability.elf(main, test_text_eng_0)
    elf_eng_12 = wl_measures_readability.elf(main, test_text_eng_12)
    elf_spa_12 = wl_measures_readability.elf(main, test_text_spa_12)
    elf_other_12 = wl_measures_readability.elf(main, test_text_other_12)

    assert elf_eng_0 == 'text_too_short'
    assert elf_eng_12 == (15 - 12) / 3
    assert elf_spa_12 != 'no_support'
    assert elf_other_12 == 'no_support'

def test_gl():
    gl_eng_0 = wl_measures_readability.gl(main, test_text_eng_0)
    gl_eng_12 = wl_measures_readability.gl(main, test_text_eng_12)
    gl_spa_12 = wl_measures_readability.gl(main, test_text_spa_12)
    gl_other_12 = wl_measures_readability.gl(main, test_text_other_12)

    assert gl_eng_0 == 'text_too_short'
    assert gl_eng_12 == 0.39 * (12 / 3) + 11.8 * (15 / 12) - 15.59
    assert gl_spa_12 != 'no_support'
    assert gl_other_12 == 'no_support'

def test_re_flesch():
    flesch_re_eng_0 = wl_measures_readability.re_flesch(main, test_text_eng_0)
    settings['re']['use_powers_sumner_kearl_variant_for_all_langs'] = True
    flesch_re_eng_12_psk = wl_measures_readability.re_flesch(main, test_text_eng_12)
    settings['re']['use_powers_sumner_kearl_variant_for_all_langs'] = False
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
    flesch_re_ukr_12 = wl_measures_readability.re_flesch(main, test_text_ukr_12)

    flesch_re_afr_12 = wl_measures_readability.re_flesch(main, test_text_afr_12)
    flesch_re_other_12 = wl_measures_readability.re_flesch(main, test_text_other_12)

    assert flesch_re_eng_0 == 'text_too_short'
    assert flesch_re_eng_12_psk == -2.2029 + 4.55 * (15 / 12) + 0.0778 * (12 / 3)
    assert flesch_re_eng_12 == 206.835 - 84.6 * (15 / 12) - 1.015 * (12 / 3)
    assert flesch_re_nld_12_douma == 206.84 - 77 * (18 / 12) - 0.93 * (12 / 3)
    assert flesch_re_nld_12_brouwer == 195 - (200 / 3) * (18 / 12) - 2 * (12 / 3)
    assert flesch_re_fra_12 == 207 - 73.6 * (16 / 12) - 1.015 * (12 / 3)
    assert flesch_re_deu_12 == 180 - 58.5 * (15 / 12) - (12 / 3)
    assert flesch_re_ita_12 == 217 - 60 * (19 / 12) - 1.3 * (12 / 3)
    assert flesch_re_rus_12 == 206.835 - 60.1 * (13 / 12) - 1.3 * (12 / 3)
    assert flesch_re_spa_12_fh == 206.84 - 60 * (18 / 12) - 1.02 * (12 / 3)
    assert flesch_re_spa_12_sp == 206.84 - 62.3 * (18 / 12) - (12 / 3)
    assert flesch_re_ukr_12 == 206.84 - 28.3 * (13 / 12) - 5.93 * (12 / 3)
    assert flesch_re_afr_12 == 206.835 - 0.846 * (18 / 12 * 100) - 1.015 * (12 / 3)
    assert flesch_re_other_12 == 'no_support'

def test_re_farr_jenkins_paterson():
    re_farr_jenkins_paterson_eng_0 = wl_measures_readability.re_farr_jenkins_paterson(main, test_text_eng_0)
    settings['re_farr_jenkins_paterson']['use_powers_sumner_kearl_variant'] = False
    re_farr_jenkins_paterson_eng_12 = wl_measures_readability.re_farr_jenkins_paterson(main, test_text_eng_12)
    settings['re_farr_jenkins_paterson']['use_powers_sumner_kearl_variant'] = True
    re_farr_jenkins_paterson_eng_12_psk = wl_measures_readability.re_farr_jenkins_paterson(main, test_text_eng_12)
    re_farr_jenkins_paterson_spa_12 = wl_measures_readability.re_farr_jenkins_paterson(main, test_text_spa_12)
    re_farr_jenkins_paterson_other_12 = wl_measures_readability.re_farr_jenkins_paterson(main, test_text_other_12)

    assert re_farr_jenkins_paterson_eng_0 == 'text_too_short'
    assert re_farr_jenkins_paterson_eng_12 == 1.599 * (9 / 12 * 100) - 1.015 * (12 / 3) - 31.517
    assert re_farr_jenkins_paterson_eng_12_psk == 8.4335 - 0.0648 * (9 / 12 * 100) + 0.0923 * (12 / 3)
    assert re_farr_jenkins_paterson_spa_12 != 'no_support'
    assert re_farr_jenkins_paterson_other_12 == 'no_support'

def test_rgl():
    rgl_eng_12 = wl_measures_readability.rgl(main, test_text_eng_12)
    rgl_eng_150 = wl_measures_readability.rgl(main, test_text_eng_150)
    rgl_spa_150 = wl_measures_readability.rgl(main, test_text_spa_150)
    rgl_other_12 = wl_measures_readability.rgl(main, test_text_other_12)

    assert rgl_eng_12 == 'text_too_short'
    assert rgl_eng_150 == rgl_spa_150 == 20.43 - 0.11 * (6 * 18 + 4)
    assert rgl_other_12 == 'no_support'

def test_fuckss_stilcharakteristik():
    stilcharakteristik_eng_0 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_eng_0)
    stilcharakteristik_eng_12 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_eng_12)
    stilcharakteristik_spa_12 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_spa_12)
    stilcharakteristik_other_12 = wl_measures_readability.fuckss_stilcharakteristik(main, test_text_other_12)

    assert stilcharakteristik_eng_0 == 'text_too_short'
    assert stilcharakteristik_eng_12 == 15 / 3
    assert stilcharakteristik_spa_12 != 'no_support'
    assert stilcharakteristik_other_12 == 'no_support'

def test_gulpease():
    gulpease_index_ita_0 = wl_measures_readability.gulpease(main, test_text_ita_0)
    gulpease_index_ita_12 = wl_measures_readability.gulpease(main, test_text_ita_12)
    gulpease_index_eng_12 = wl_measures_readability.gulpease(main, test_text_eng_12)

    assert gulpease_index_ita_0 == 'text_too_short'
    assert gulpease_index_ita_12 == 89 + (300 * 3 - 10 * 45) / 12
    assert gulpease_index_eng_12 == 'no_support'

def test_fog_index():
    fog_index_eng_0 = wl_measures_readability.fog_index(main, test_text_eng_0)
    settings['fog_index']['variant_eng'] = 'Original'
    fog_index_eng_12_propn_orig = wl_measures_readability.fog_index(main, test_text_eng_12_propn)
    settings['fog_index']['variant_eng'] = 'Powers-Sumner-Kearl'
    fog_index_eng_12_pron_psk = wl_measures_readability.fog_index(main, test_text_eng_12_propn)
    settings['fog_index']['variant_eng'] = 'Navy'
    fog_index_eng_12_navy = wl_measures_readability.fog_index(main, test_text_eng_12)
    fog_index_spa_12 = wl_measures_readability.fog_index(main, test_text_spa_12)

    assert fog_index_eng_0 == 'text_too_short'
    assert fog_index_eng_12_propn_orig == 0.4 * (12 / 3 + 1 / 12 * 100)
    assert fog_index_eng_12_pron_psk == 3.0680 + 0.0877 * (12 / 3) + 0.0984 * (1 / 12 * 100)
    assert fog_index_eng_12_navy == ((12 + 2 * 0) / 3 - 3) / 2
    assert fog_index_spa_12 == 'no_support'

def test_cp():
    cp_spa_0 = wl_measures_readability.cp(main, test_text_spa_0)
    cp_spa_12 = wl_measures_readability.cp(main, test_text_spa_12)
    cp_eng_12 = wl_measures_readability.cp(main, test_text_eng_12)

    assert cp_spa_0 == 'text_too_short'
    assert cp_spa_12 == 95.2 - 9.7 * (45 / 12) - 0.35 * (12 / 3)
    assert cp_eng_12 == 'no_support'

def test_mu():
    mu_spa_0 = wl_measures_readability.mu(main, test_text_spa_0)
    mu_spa_12 = wl_measures_readability.mu(main, test_text_spa_12)
    mu_eng_12 = wl_measures_readability.mu(main, test_text_eng_12)

    assert mu_spa_0 == 'text_too_short'
    assert mu_spa_12 == (12 / 11) * (3.75 / 7.1875) * 100
    assert mu_eng_12 == 'no_support'

def test_lensear_write_formula():
    score_eng_0 = wl_measures_readability.lensear_write_formula(main, test_text_eng_0)
    score_eng_12 = wl_measures_readability.lensear_write_formula(main, test_text_eng_12)
    score_eng_100 = wl_measures_readability.lensear_write_formula(main, test_text_eng_100)
    score_spa_100 = wl_measures_readability.lensear_write_formula(main, test_text_spa_100)

    assert score_eng_0 == 'text_too_short'
    assert score_eng_12 == 6 * (100 / 12) + 3 * 3 * (100 / 12)
    assert score_eng_100 == 50 + 3 * 25
    assert score_spa_100 == 'no_support'

def test_lix():
    lix_eng_0 = wl_measures_readability.lix(main, test_text_eng_0)
    lix_eng_12 = wl_measures_readability.lix(main, test_text_eng_12)
    lix_spa_12 = wl_measures_readability.lix(main, test_text_spa_12)

    assert lix_eng_0 == 'text_too_short'
    assert lix_eng_12 == 12 / 3 + 100 * (3 / 12)
    assert lix_spa_12 != 'no_support'

def test_lorge_readability_index():
    lorge_eng_0 = wl_measures_readability.lorge_readability_index(main, test_text_eng_0)
    settings['lorge_readability_index']['use_corrected_formula'] = True
    lorge_eng_12_corrected = wl_measures_readability.lorge_readability_index(main, test_text_eng_12_prep)
    settings['lorge_readability_index']['use_corrected_formula'] = False
    lorge_eng_12 = wl_measures_readability.lorge_readability_index(main, test_text_eng_12_prep)
    lorge_spa_12 = wl_measures_readability.lorge_readability_index(main, test_text_spa_12)

    assert lorge_eng_0 == 'text_too_short'
    assert lorge_eng_12_corrected == 12 / 3 * 0.06 + 2 / 12 * 0.1 + 2 / 12 * 0.1 + 1.99
    assert lorge_eng_12 == 12 / 3 * 0.07 + 2 / 12 * 13.01 + 2 / 12 * 10.73 + 1.6126
    assert lorge_spa_12 == 'no_support'

def test_luong_nguyen_dinhs_readability_formula():
    readability_vie_0 = wl_measures_readability.luong_nguyen_dinhs_readability_formula(main, test_text_vie_0)
    readability_vie_12 = wl_measures_readability.luong_nguyen_dinhs_readability_formula(main, test_text_vie_12)
    readability_eng_12 = wl_measures_readability.luong_nguyen_dinhs_readability_formula(main, test_text_eng_12)

    assert readability_vie_0 == 'text_too_short'
    assert readability_vie_12 == 0.004 * (46 / 3) + 0.1905 * (46 / 12) + 2.7147 * 12 / 12 - 0.7295
    assert readability_eng_12 == 'no_support'

def test_eflaw():
    eflaw_eng_0 = wl_measures_readability.eflaw(main, test_text_eng_0)
    eflaw_eng_12 = wl_measures_readability.eflaw(main, test_text_eng_12)
    eflaw_spa_12 = wl_measures_readability.eflaw(main, test_text_spa_12)

    assert eflaw_eng_0 == 'text_too_short'
    assert eflaw_eng_12 == (12 + 6) / 3
    assert eflaw_spa_12 == 'no_support'

def test_nwl():
    nwl_deu_0 = wl_measures_readability.nwl(main, test_text_deu_0)
    settings['nwl']['variant'] = '1'
    nwl_deu_12_1 = wl_measures_readability.nwl(main, test_text_deu_12)
    settings['nwl']['variant'] = '2'
    nwl_deu_12_2 = wl_measures_readability.nwl(main, test_text_deu_12)
    settings['nwl']['variant'] = '3'
    nwl_deu_12_3 = wl_measures_readability.nwl(main, test_text_deu_12)
    nwl_eng_12 = wl_measures_readability.nwl(main, test_text_eng_12)

    sw = 5 / 5 * 100
    s_100 = 3 / 12 * 100
    ms = 0 / 12 * 100
    sl = 12 / 3
    iw = 3 / 12 * 100

    assert nwl_deu_0 == 'text_too_short'
    assert nwl_deu_12_1 == 0.2032 * sw - 0.1715 * s_100 + 0.1594 * ms - 0.0746 * ms - 0.145
    assert nwl_deu_12_2 == 0.2081 * sw - 0.207 * s_100 + 0.1772 * ms + 0.7498
    assert nwl_deu_12_3 == 0.2373 * ms + 0.2433 * sl + 0.1508 * iw - 3.9203
    assert nwl_eng_12 == 'no_support'

def test_nws():
    nws_deu_0 = wl_measures_readability.nws(main, test_text_deu_0)
    settings['nws']['variant'] = '1'
    nws_deu_12_1 = wl_measures_readability.nws(main, test_text_deu_12)
    settings['nws']['variant'] = '2'
    nws_deu_12_2 = wl_measures_readability.nws(main, test_text_deu_12)
    settings['nws']['variant'] = '3'
    nws_deu_12_3 = wl_measures_readability.nws(main, test_text_deu_12)
    nws_eng_12 = wl_measures_readability.nws(main, test_text_eng_12)

    ms = 0 / 12 * 100
    sl = 12 / 3
    iw = 3 / 12 * 100
    es = 9 / 12 * 100

    assert nws_deu_0 == 'text_too_short'
    assert nws_deu_12_1 == 0.1925 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875
    assert nws_deu_12_2 == 0.2007 * ms + 0.1682 * sl + 0.1373 * iw - 2.779
    assert nws_deu_12_3 == 0.2963 * ms + 0.1905 * sl - 1.1144
    assert nws_eng_12 == 'no_support'

def test__get_num_syls_ara():
    assert wl_measures_readability._get_num_syls_ara('') == 0
    assert wl_measures_readability._get_num_syls_ara('\u064E\u0627') == 2
    assert wl_measures_readability._get_num_syls_ara('\u064Ea') == 1
    assert wl_measures_readability._get_num_syls_ara('\u064E') == 1
    assert wl_measures_readability._get_num_syls_ara('\u064B') == 2

def test_osman():
    osman_ara_0 = wl_measures_readability.osman(main, test_text_ara_0)
    osman_ara_12 = wl_measures_readability.osman(main, test_text_ara_12)
    osman_ara_faseeh = wl_measures_readability.osman(main, test_text_ara_faseeh)
    osman_eng_12 = wl_measures_readability.osman(main, test_text_eng_12)

    assert osman_ara_0 == 'text_too_short'
    assert osman_ara_12 == 200.791 - 1.015 * (12 / 3) - 24.181 * ((3 + 26 + 3 + 0) / 12)
    assert osman_ara_faseeh == 200.791 - 1.015 * (1 / 1) - 24.181 * ((0 + 5 + 1 + 1) / 1)
    assert osman_eng_12 == 'no_support'

def test_rix():
    rix_eng_0 = wl_measures_readability.rix(main, test_text_eng_0)
    rix_eng_12 = wl_measures_readability.rix(main, test_text_eng_12)
    rix_spa_12 = wl_measures_readability.rix(main, test_text_spa_12)

    assert rix_eng_0 == 'text_too_short'
    assert rix_eng_12 == rix_spa_12 == 3 / 3

def test_smog_grading():
    g_eng_12 = wl_measures_readability.smog_grading(main, test_text_eng_12)
    g_eng_120 = wl_measures_readability.smog_grading(main, test_text_eng_120)
    g_eng_120 = wl_measures_readability.smog_grading(main, test_text_eng_120)
    g_deu_120 = wl_measures_readability.smog_grading(main, test_text_deu_120)
    g_spa_120 = wl_measures_readability.smog_grading(main, test_text_spa_120)
    g_other_12 = wl_measures_readability.smog_grading(main, test_text_other_12)

    assert g_eng_12 == 'text_too_short'
    assert g_eng_120 == 3.1291 + 1.043 * numpy.sqrt(15)
    assert g_deu_120 == numpy.sqrt(15 / 30 * 30) - 2
    assert g_spa_120 != 'no_support'
    assert g_other_12 == 'no_support'

def test_spache_readability_formula():
    grade_lvl_eng_12 = wl_measures_readability.spache_readability_formula(main, test_text_eng_12)
    settings['spache_readability_formula']['use_rev_formula'] = True
    grade_lvl_eng_100_rev = wl_measures_readability.spache_readability_formula(main, test_text_eng_100)
    settings['spache_readability_formula']['use_rev_formula'] = False
    grade_lvl_eng_100 = wl_measures_readability.spache_readability_formula(main, test_text_eng_100)
    grade_lvl_spa_100 = wl_measures_readability.spache_readability_formula(main, test_text_spa_100)

    assert grade_lvl_eng_12 == 'text_too_short'
    assert grade_lvl_eng_100_rev == numpy.mean([0.121 * (100 / 25) + 0.082 * 25 + 0.659] * 3)
    assert grade_lvl_eng_100 == numpy.mean([0.141 * (100 / 25) + 0.086 * 25 + 0.839] * 3)
    assert grade_lvl_spa_100 == 'no_support'

def test_strain_index():
    strain_index_eng_0 = wl_measures_readability.strain_index(main, test_text_eng_0)
    strain_index_eng_12 = wl_measures_readability.strain_index(main, test_text_eng_12)
    strain_index_spa_12 = wl_measures_readability.strain_index(main, test_text_spa_12)
    strain_index_other_12 = wl_measures_readability.strain_index(main, test_text_other_12)

    assert strain_index_eng_0 == 'text_too_short'
    assert strain_index_eng_12 == 15 / 10
    assert strain_index_spa_12 != 'no_support'
    assert strain_index_other_12 == 'no_support'

def test_trankle_bailers_readability_formula():
    trankle_bailers_eng_0 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_eng_0)
    settings['trankle_bailers_readability_formula']['variant'] = '1'
    trankle_bailers_eng_100_prep_1 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_eng_100_prep)
    settings['trankle_bailers_readability_formula']['variant'] = '2'
    trankle_bailers_eng_100_conj_2 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_eng_100_conj)
    trankle_bailers_tha_100 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_tha_100)
    trankle_bailers_other_100 = wl_measures_readability.trankle_bailers_readability_formula(main, test_text_other_100)

    assert trankle_bailers_eng_0 == 'text_too_short'
    assert trankle_bailers_eng_100_prep_1 == 224.6814 - numpy.log(372 / 100 + 1) * 79.8304 - numpy.log(100 / 25 + 1) * 12.24032 - 1 * 1.292857
    assert trankle_bailers_eng_100_conj_2 == 234.1063 - numpy.log(374 / 100 + 1) * 96.11069 - 0 * 2.05444 - 1 * 1.02805
    assert trankle_bailers_tha_100 != 'no_support'
    assert trankle_bailers_other_100 == 'no_support'

def test_td():
    td_eng_0 = wl_measures_readability.td(main, test_text_eng_0)
    td_eng_12 = wl_measures_readability.td(main, test_text_eng_12)
    td_spa_12 = wl_measures_readability.td(main, test_text_spa_12)
    td_other_12 = wl_measures_readability.td(main, test_text_other_12)

    assert td_eng_0 == 'text_too_short'
    assert td_eng_12 == (15 / 12) * numpy.log(12 / 3)
    assert td_spa_12 != 'no_support'
    assert td_other_12 == 'no_support'

def test_wheeler_smiths_readability_formula():
    wheeler_smith_eng_0 = wl_measures_readability.wheeler_smiths_readability_formula(main, test_text_eng_0)
    wheeler_smith_eng_12 = wl_measures_readability.wheeler_smiths_readability_formula(main, test_text_eng_12_hyphen)
    wheeler_smith_spa_12 = wl_measures_readability.wheeler_smiths_readability_formula(main, test_text_spa_12)
    wheeler_smith_other_12 = wl_measures_readability.wheeler_smiths_readability_formula(main, test_text_other_12)

    assert wheeler_smith_eng_0 == 'text_too_short'
    assert wheeler_smith_eng_12 == (12 / 4) * (3 / 12) * 10
    assert wheeler_smith_spa_12 != 'no_support'
    assert wheeler_smith_other_12 == 'no_support'

if __name__ == '__main__':
    test_rd()
    test_aari()
    test_ari()
    test_bormuths_cloze_mean()
    test_bormuths_gp()
    test_coleman_liau_index()
    test_colemans_readability_formula()
    test_crawfords_readability_formula()
    test_x_c50()
    test_danielson_bryans_readability_formula()
    test_dawoods_readability_formula()
    test_drp()
    test_devereux_readability_index()
    test_dickes_steiwer_handformel()
    test_elf()
    test_gl()
    test_re_flesch()
    test_re_farr_jenkins_paterson()
    test_rgl()
    test_fuckss_stilcharakteristik()
    test_gulpease()
    test_fog_index()
    test_cp()
    test_mu()
    test_lensear_write_formula()
    test_lix()
    test_lorge_readability_index()
    test_luong_nguyen_dinhs_readability_formula()
    test_eflaw()
    test_nwl()
    test_nws()
    test__get_num_syls_ara()
    test_osman()
    test_rix()
    test_smog_grading()
    test_spache_readability_formula()
    test_strain_index()
    test_trankle_bailers_readability_formula()
    test_td()
    test_wheeler_smiths_readability_formula()
