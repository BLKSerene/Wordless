# ----------------------------------------------------------------------
# Wordless: Figures - Frequencies
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

from PyQt5.QtCore import QCoreApplication

from wordless.wl_figs import wl_figs
from wordless.wl_utils import wl_sorting

_tr = QCoreApplication.translate

def wl_fig_freqs(main, freq_files_items, tab):
    if tab == 'keyword_extractor':
        file_names_selected = [_tr('wl_fig_freqs', 'Reference Files'), *main.wl_file_area.get_selected_file_names(), _tr('wl_fig_freqs', 'Total')]
    else:
        file_names_selected = [*main.wl_file_area.get_selected_file_names(), _tr('wl_fig_freqs', 'Total')]

    fig_settings = main.settings_custom[tab]['fig_settings']
    col_sort_by_file = file_names_selected.index(fig_settings['sort_by_file'])

    if tab == 'keyword_extractor':
        freq_files_items = wl_sorting.sorted_freq_files_items_keyword_extractor(
            freq_files_items,
            sort_by_col = col_sort_by_file
        )
    else:
        freq_files_items = wl_sorting.sorted_freq_files_items(
            freq_files_items,
            sort_by_col = col_sort_by_file
        )

    # Line Chart
    if fig_settings['graph_type'] == _tr('wl_fig_freqs', 'Line Chart'):
        if tab == 'wordlist_generator':
            label_x = _tr('wl_fig_freqs', 'Token')
        elif tab == 'ngram_generator':
            label_x = _tr('wl_fig_freqs', 'N-gram')
        elif tab in ['collocation_extractor', 'colligation_extractor']:
            label_x = _tr('wl_fig_freqs', 'Collocate')
        elif tab == 'keyword_extractor':
            label_x = _tr('wl_fig_freqs', 'Keyword')

        wl_figs.generate_line_chart(
            main, freq_files_items,
            fig_settings = fig_settings,
            file_names_selected = file_names_selected,
            label_x = label_x
        )
    else:
        items_freq_file = [
            (item, freqs[col_sort_by_file])
            for item, freqs in freq_files_items
        ]

        # Word Cloud
        if fig_settings['graph_type'] == _tr('wl_fig_freqs', 'Word Cloud'):
            wl_figs.generate_word_cloud(main, items_freq_file, fig_settings = fig_settings)

        # Network Graph
        elif fig_settings['graph_type'] == _tr('wl_fig_freqs', 'Network Graph'):
            wl_figs.generate_network_graph(main, items_freq_file, fig_settings = fig_settings)
