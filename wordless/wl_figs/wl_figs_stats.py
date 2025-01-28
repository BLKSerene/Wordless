# ----------------------------------------------------------------------
# Wordless: Figures - Statistics
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

def wl_fig_stats(main, stat_files_items, tab):
    fig_settings = main.settings_custom[tab]['fig_settings']

    # Tokens / Keywords
    if stat_files_items and isinstance(list(stat_files_items.keys())[0], str):
        stat_files_items = {
            item.display_text(): stat_files
            for item, stat_files in stat_files_items.items()
        }
    # N-grams
    elif stat_files_items and isinstance(list(stat_files_items.keys())[0][0], str):
        stat_files_items = {
            ' '.join(wl_texts.to_display_texts(item)): stat_files
            for item, stat_files in stat_files_items.items()
        }
    # Collocations / Colligations
    else:
        if fig_settings['graph_type'] == _tr('wl_figs_stats', 'Network graph'):
            stat_files_items = {
                (' '.join(wl_texts.to_display_texts(node)), collocate.display_text()): stat_files
                for (node, collocate), stat_files in stat_files_items.items()
            }
        else:
            stat_files_items = {
                ' '.join(wl_texts.to_display_texts(node)) + ', ' + collocate.display_text(): stat_files
                for (node, collocate), stat_files in stat_files_items.items()
            }

    file_names_selected = [*main.wl_file_area.get_selected_file_names(), _tr('wl_figs_stats', 'Total')]
    col_sort_by_file = file_names_selected.index(fig_settings['sort_by_file'])

    if fig_settings['use_data'] == _tr('wl_figs_stats', 'p-value'):
        stat_files_items = wl_sorting.sorted_freq_files_items(
            stat_files_items,
            sort_by_col = col_sort_by_file,
            reverse = True
        )
    else:
        stat_files_items = wl_sorting.sorted_freq_files_items(
            stat_files_items,
            sort_by_col = col_sort_by_file
        )

    # Line Chart
    if fig_settings['graph_type'] == _tr('wl_figs_stats', 'Line chart'):
        if tab == 'wordlist_generator':
            label_x = _tr('wl_figs_stats', 'Token')
        elif tab == 'ngram_generator':
            label_x = _tr('wl_figs_stats', 'N-gram')
        elif tab in ['collocation_extractor', 'colligation_extractor']:
            label_x = _tr('wl_figs_stats', 'Collocate')
        elif tab == 'keyword_extractor':
            label_x = _tr('wl_figs_stats', 'Keyword')

        wl_figs.generate_line_chart(
            main, stat_files_items,
            fig_settings = fig_settings,
            file_names_selected = file_names_selected,
            label_x = label_x
        )
    else:
        stat_file_items = [
            (item, stat_files[col_sort_by_file])
            for item, stat_files in stat_files_items
        ]

        # Word Cloud
        if fig_settings['graph_type'] == _tr('wl_figs_stats', 'Word cloud'):
            wl_figs.generate_word_cloud(main, stat_file_items, fig_settings = fig_settings)
        # Network Graph
        elif fig_settings['graph_type'] == _tr('wl_figs_stats', 'Network graph'):
            wl_figs.generate_network_graph(main, stat_file_items, fig_settings = fig_settings)
