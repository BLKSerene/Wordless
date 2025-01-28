# ----------------------------------------------------------------------
# Wordless: Figures - Frequencies
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

from PyQt5.QtCore import QCoreApplication

from wordless.wl_figs import wl_figs
from wordless.wl_nlp import wl_texts
from wordless.wl_utils import wl_sorting

_tr = QCoreApplication.translate

def wl_fig_freqs(main, freq_files_items, tab):
    fig_settings = main.settings_custom[tab]['fig_settings']

    # Tokens / Keywords
    if freq_files_items and isinstance(list(freq_files_items.keys())[0], str):
        freq_files_items = {
            item.display_text(): freq_files
            for item, freq_files in freq_files_items.items()
        }
    # N-grams
    elif freq_files_items and isinstance(list(freq_files_items.keys())[0][0], str):
        freq_files_items = {
            ' '.join(wl_texts.to_display_texts(item)): freq_files
            for item, freq_files in freq_files_items.items()
        }
    # Collocations / Colligations
    else:
        if fig_settings['graph_type'] == _tr('wl_figs_freqs', 'Network graph'):
            freq_files_items = {
                (' '.join(wl_texts.to_display_texts(node)), collocate.display_text()): freq_files
                for (node, collocate), freq_files in freq_files_items.items()
            }
        else:
            freq_files_items = {
                ' '.join(wl_texts.to_display_texts(node)) + ', ' + collocate.display_text(): freq_files
                for (node, collocate), freq_files in freq_files_items.items()
            }

    if tab == 'keyword_extractor':
        file_names_selected = [
            _tr('wl_figs_freqs', 'Reference files'),
            *main.wl_file_area.get_selected_file_names(),
            _tr('wl_figs_freqs', 'Total')
        ]
    else:
        file_names_selected = [
            *main.wl_file_area.get_selected_file_names(),
            _tr('wl_figs_freqs', 'Total')
        ]

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
    if fig_settings['graph_type'] == _tr('wl_figs_freqs', 'Line chart'):
        if tab == 'wordlist_generator':
            label_x = _tr('wl_figs_freqs', 'Token')
        elif tab == 'ngram_generator':
            label_x = _tr('wl_figs_freqs', 'N-gram')
        elif tab in ['collocation_extractor', 'colligation_extractor']:
            label_x = _tr('wl_figs_freqs', 'Collocate')
        elif tab == 'keyword_extractor':
            label_x = _tr('wl_figs_freqs', 'Keyword')

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
        if fig_settings['graph_type'] == _tr('wl_figs_freqs', 'Word cloud'):
            wl_figs.generate_word_cloud(main, items_freq_file, fig_settings = fig_settings)

        # Network Graph
        elif fig_settings['graph_type'] == _tr('wl_figs_freqs', 'Network graph'):
            wl_figs.generate_network_graph(main, items_freq_file, fig_settings = fig_settings)
