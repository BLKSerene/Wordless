# ----------------------------------------------------------------------
# Tests: Settings - Measures
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
from wordless.wl_settings import wl_settings_measures

main = wl_test_init.Wl_Test_Main()

def test_wl_settings_measures_readability():
    settings_measures_readability = wl_settings_measures.Wl_Settings_Measures_Readability(main)
    settings_measures_readability.re_changed()
    settings_measures_readability.load_settings()
    settings_measures_readability.load_settings(defaults = True)
    settings_measures_readability.apply_settings()

def test_wl_settings_measures_lexical_density_diversity():
    settings_measures_lexical_density_diversity = wl_settings_measures.Wl_Settings_Measures_Lexical_Density_Diversity(main)
    settings_measures_lexical_density_diversity.load_settings()
    settings_measures_lexical_density_diversity.load_settings(defaults = True)
    settings_measures_lexical_density_diversity.apply_settings()

def test_wl_settings_measures_dispersion():
    settings_measures_dispersion = wl_settings_measures.Wl_Settings_Measures_Dispersion(main)
    settings_measures_dispersion.load_settings()
    settings_measures_dispersion.load_settings(defaults = True)
    settings_measures_dispersion.apply_settings()

def test_wl_settings_measures_adjusted_freq():
    settings_measures_adjusted_freq = wl_settings_measures.Wl_Settings_Measures_Adjusted_Freq(main)
    settings_measures_adjusted_freq.load_settings()
    settings_measures_adjusted_freq.load_settings(defaults = True)
    settings_measures_adjusted_freq.apply_settings()

def test_wl_settings_measures_statistical_significance():
    settings_measures_statistical_significance = wl_settings_measures.Wl_Settings_Measures_Statistical_Significance(main)
    settings_measures_statistical_significance.load_settings()
    settings_measures_statistical_significance.load_settings(defaults = True)
    settings_measures_statistical_significance.apply_settings()

def test_wl_settings_measures_bayes_factor():
    settings_measures_bayes_factor = wl_settings_measures.Wl_Settings_Measures_Bayes_Factor(main)
    settings_measures_bayes_factor.load_settings()
    settings_measures_bayes_factor.load_settings(defaults = True)
    settings_measures_bayes_factor.apply_settings()

def test_wl_settings_measures_effect_size():
    settings_measures_effect_size = wl_settings_measures.Wl_Settings_Measures_Effect_Size(main)
    settings_measures_effect_size.load_settings()
    settings_measures_effect_size.load_settings(defaults = True)
    settings_measures_effect_size.apply_settings()

if __name__ == '__main__':
    test_wl_settings_measures_readability()
    test_wl_settings_measures_lexical_density_diversity()
    test_wl_settings_measures_dispersion()
    test_wl_settings_measures_adjusted_freq()
    test_wl_settings_measures_statistical_significance()
    test_wl_settings_measures_bayes_factor()
    test_wl_settings_measures_effect_size()
