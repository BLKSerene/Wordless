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

import random

from tests import wl_test_init
from wordless.wl_figs import wl_figs

main = wl_test_init.Wl_Test_Main()

def test_get_data_ranks():
    data_files_items = [(str(i), i) for i in range(100)]
    fig_settings = {
        'rank_min_no_limit': True,
        'rank_max_no_limit': False,
        'rank_min': 1,
        'rank_max': 50
    }

    assert wl_figs.get_data_ranks(data_files_items, fig_settings) == [(str(i), i) for i in range(50)]

def test_generate_line_chart():
    files = main.settings_custom['file_area']['files_open']

    for file in files:
        file['selected'] = False

    for file in random.sample(files, 2):
        file['selected'] = True

    wl_figs.generate_line_chart(
        main,
        data_files_items = [
            (str(item), [random.randrange(0, 10000), random.randrange(0, 10000)])
            for item in range(100)
        ],
        fig_settings = main.settings_custom['wordlist_generator']['fig_settings'],
        file_names_selected = main.wl_file_area.get_selected_file_names(),
        label_x = 'Tokens'
    )

def test_generate_word_cloud():
    wl_figs.generate_word_cloud(
        main,
        data_file_items = [
            (str(item), random.randrange(0, 10000))
            for item in range(100)
        ],
        fig_settings = main.settings_custom['wordlist_generator']['fig_settings'],
    )

def test_generate_network_graph():
    wl_figs.generate_network_graph(
        main,
        data_file_items = [
            ((str(node), str(collocate)), random.uniform(0, 1))
            for node in range(10)
            for collocate in range(10)
        ],
        fig_settings = main.settings_custom['collocation_extractor']['fig_settings'],
    )

if __name__ == '__main__':
    test_get_data_ranks()

    test_generate_line_chart()
    test_generate_word_cloud()
    test_generate_network_graph()
