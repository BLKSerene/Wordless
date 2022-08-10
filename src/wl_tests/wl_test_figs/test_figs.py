# ----------------------------------------------------------------------
# Wordless: Tests - Figures - Figures
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

from wl_figs import wl_figs

def test_get_data_ranks():
    data_files_items = [(str(i), i) for i in range(100)]
    fig_settings = {
        'rank_min_no_limit': True,
        'rank_max_no_limit': False,
        'rank_min': 1,
        'rank_max': 50
    }

    assert wl_figs.get_data_ranks(data_files_items, fig_settings) == [(str(i), i) for i in range(50)]

if __name__ == '__main__':
    test_get_data_ranks()
