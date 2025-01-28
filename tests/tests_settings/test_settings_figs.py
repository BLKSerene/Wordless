# ----------------------------------------------------------------------
# Tests: Settings - Figures
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
from wordless.wl_settings import wl_settings_figs

main = wl_test_init.Wl_Test_Main()

def test_wl_settings_figs_line_charts():
    settings_figs_line_charts = wl_settings_figs.Wl_Settings_Figs_Line_Charts(main)
    settings_figs_line_charts.change_fonts()
    settings_figs_line_charts.load_settings()
    settings_figs_line_charts.load_settings(defaults = True)
    settings_figs_line_charts.apply_settings()

def test_wl_settings_figs_word_clouds():
    settings_figs_word_clouds = wl_settings_figs.Wl_Settings_Figs_Word_Clouds(main)
    settings_figs_word_clouds.font_settings_changed()
    settings_figs_word_clouds.load_settings()
    settings_figs_word_clouds.load_settings(defaults = True)
    settings_figs_word_clouds.validate_settings()
    settings_figs_word_clouds.apply_settings()

def test_wl_settings_figs_network_graphs():
    settings_figs_network_graphs = wl_settings_figs.Wl_Settings_Figs_Network_Graphs(main)
    settings_figs_network_graphs.load_settings()
    settings_figs_network_graphs.load_settings(defaults = True)
    settings_figs_network_graphs.apply_settings()

if __name__ == '__main__':
    test_wl_settings_figs_line_charts()
    test_wl_settings_figs_word_clouds()
    test_wl_settings_figs_network_graphs()
