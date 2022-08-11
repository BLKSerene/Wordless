# ----------------------------------------------------------------------
# Wordless: Tests - Figures - Frequencies
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
import re

from tests import wl_test_init
from wordless.wl_figs import wl_figs_freqs

main = wl_test_init.Wl_Test_Main()

def test_wl_fig_freqs():
    files = main.settings_custom['file_area']['files_open']

    for tab in [
        'wordlist_generator',
        'ngram_generator',
        'collocation_extractor',
        'colligation_extractor',
        'keyword_extractor'
    ]:
        print(f'[{tab}]')

        if tab in ['wordlist_generator', 'ngram_generator', 'keyword_extractor']:
            graph_types = ['Line Chart', 'Word Cloud']
            use_datas = ['Frequency']
        elif tab in ['collocation_extractor', 'colligation_extractor']:
            graph_types = ['Line Chart', 'Word Cloud', 'Network Graph']
            use_datas = ['L5', 'L4', 'L3', 'L2', 'L1', 'R1', 'R2', 'R3', 'R4', 'R5', 'Frequency']

        for graph_type in graph_types:
            freq_files_items = {}

            if graph_type == 'Network Graph':
                for node in range(10):
                    for collocate in range(10):
                        freq_1, freq_2 = random.sample(range(10000), 2)

                        freq_files_items[(str(node), str(collocate))] = [
                            max(freq_1, freq_2) - min(freq_1, freq_2),
                            min(freq_1, freq_2),
                            max(freq_1, freq_2)
                        ]
            else:
                if tab == 'keyword_extractor':
                    for item in range(100):
                        freq_1, freq_2 = random.sample(range(100), 2)

                        freq_files_items[str(item)] = [
                            random.randint(0, 100),
                            max(freq_1, freq_2) - min(freq_1, freq_2),
                            min(freq_1, freq_2),
                            max(freq_1, freq_2)
                        ]
                else:
                    for item in range(100):
                        freq_1, freq_2 = random.sample(range(100), 2)

                        freq_files_items[str(item)] = [
                            max(freq_1, freq_2) - min(freq_1, freq_2),
                            min(freq_1, freq_2),
                            max(freq_1, freq_2)
                        ]

            for file in files:
                file['selected'] = False

            for file in random.sample(files, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

            fig_settings = main.settings_custom[tab]['fig_settings']
            fig_settings['graph_type'] = graph_type
            fig_settings['sort_by_file'] = random.choice([*main.wl_file_area.get_selected_file_names(), 'Total'])
            fig_settings['use_data'] = random.choice(use_datas)
            fig_settings['use_cumulative'] = random.choice([True, False])
            fig_settings['use_pct'] = random.choice([True, False])

            files_selected = [
                re.search(r'(?<=\[)[a-z_]+(?=\])', file_name).group()
                for file_name in main.wl_file_area.get_selected_file_names()
            ]

            print(f"Files: {', '.join(files_selected)}")
            print(f"Graph Type: {fig_settings['graph_type']}")
            print(f"Sort by File: {fig_settings['sort_by_file']}")
            print(f"Use Data: {fig_settings['use_data']}")
            print(f"Use cumulative data: {fig_settings['use_cumulative']}")
            print(f"Use percentage data: {fig_settings['use_pct']}\n")

            wl_figs_freqs.wl_fig_freqs(
                main,
                freq_files_items = freq_files_items,
                tab = tab
            )

if __name__ == '__main__':
    test_wl_fig_freqs()
