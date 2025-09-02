# ----------------------------------------------------------------------
# Tests: Figures - Statistics
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

from tests import (
    wl_test_file_area,
    wl_test_init
)
from wordless.wl_figs import wl_figs_stats
from wordless.wl_nlp import wl_texts

def test_wl_fig_stats():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')
    i_fig = 0

    for tab in (
        'wordlist_generator',
        'ngram_generator',
        'collocation_extractor',
        'colligation_extractor',
        'keyword_extractor'
    ):
        print(f'[{tab}]')

        match tab:
            case 'wordlist_generator' | 'ngram_generator' | 'keyword_extractor':
                graph_types = ['Line chart', 'Word cloud']
            case 'collocation_extractor' | 'colligation_extractor':
                graph_types = ['Line chart', 'Word cloud', 'Network graph']

        match tab:
            case 'wordlist_generator' | 'ngram_generator':
                use_datas = ["Juilland's D", "Juilland's U"]
            case'collocation_extractor' | 'colligation_extractor' | 'keyword_extractor':
                use_datas = ['Test Statistic', 'p-value', 'Bayes Factor', 'Effect Size']

        for graph_type in graph_types:
            stat_files_items = {}

            for i in range(100):
                item_1 = wl_texts.Wl_Token(str(i))
                item_2 = wl_texts.Wl_Token(str(i + 1))
                freq_1 = i # File 1
                freq_2 = i * 2 # File 2

                match tab:
                    case 'wordlist_generator' | 'keyword_extractor':
                        stat_files_items[item_1] = [
                            freq_1,
                            freq_2,
                            freq_1 + freq_2
                        ]
                    case 'ngram_generator':
                        stat_files_items[(item_1,)] = [
                            freq_1,
                            freq_2,
                            freq_1 + freq_2
                        ]
                    case 'collocation_extractor' | 'colligation_extractor':
                        stat_files_items[((item_1,), item_2)] = [
                            freq_1,
                            freq_2,
                            freq_1 + freq_2
                        ]

            no_file_1 = i_fig % wl_test_file_area.NUM_FILES_OBSERVED
            no_file_2 = (i_fig + 1) % wl_test_file_area.NUM_FILES_OBSERVED
            wl_test_init.select_test_files(main, no_files = (no_file_1, no_file_2))
            files_selected = [*main.wl_file_area.get_selected_file_names(), 'Total']

            fig_settings = main.settings_custom[tab]['fig_settings']
            fig_settings['graph_type'] = graph_type
            fig_settings['sort_by_file'] = files_selected[i_fig % 3]
            fig_settings['use_data'] = use_datas[i_fig % len(use_datas)]
            fig_settings['use_cumulative'] = (True, False)[i_fig % 2]
            fig_settings['use_pct'] = (True, False)[i_fig % 2]

            print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")
            print(f"Graph type: {fig_settings['graph_type']}")
            print(f"Sort by file: {fig_settings['sort_by_file']}")
            print(f"Use data: {fig_settings['use_data']}")
            print(f"Use cumulative data: {fig_settings['use_cumulative']}")
            print(f"Use percentage data: {fig_settings['use_pct']}\n")

            wl_figs_stats.wl_fig_stats(
                main,
                stat_files_items = stat_files_items,
                tab = tab
            )

            i_fig += 1

if __name__ == '__main__':
    test_wl_fig_stats()
