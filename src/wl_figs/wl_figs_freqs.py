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

from wl_figs import wl_figs
from wl_utils import wl_sorting

_tr = QCoreApplication.translate

def wl_fig_freq(main, tokens_freq_files, fig_settings, label_x):
    file_names_selected = [*main.wl_file_area.get_selected_file_names(), _tr('wl_fig_freq', 'Total')]
    col_sort_by_file = file_names_selected.index(fig_settings['sort_by_file'])

    tokens_freq_files = wl_sorting.sorted_tokens_freq_files(
        tokens_freq_files,
        sort_by_col = col_sort_by_file
    )

    # Line Chart
    if fig_settings['graph_type'] == _tr('wl_fig_freq', 'Line Chart'):
        wl_figs.generate_line_chart(
            main, tokens_freq_files,
            fig_settings = fig_settings,
            freq_data = True,
            file_names_selected = file_names_selected,
            label_x = label_x
        )
    else:
        tokens_freq_file = [
            (token, freqs[col_sort_by_file])
            for token, freqs in tokens_freq_files
        ]

        # Word Cloud
        if fig_settings['graph_type'] == _tr('wl_fig_freq', 'Word Cloud'):
            wl_figs.generate_word_cloud(main, tokens_freq_file, fig_settings = fig_settings)

        # Network Graph
        elif fig_settings['graph_type'] == _tr('wl_fig_freq', 'Network Graph'):
            wl_figs.generate_network_graph(main, tokens_freq_file, fig_settings = fig_settings)

def wl_fig_freq_keyword_extractor(main, tokens_freq_files, fig_settings, label_x):
    file_names_selected = [_tr('wl_fig_freq_keyword_extractor', 'Reference Files'), *main.wl_file_area.get_selected_file_names(), _tr('wl_fig_freq_keyword_extractor', 'Total')]
    col_sort_by_file = file_names_selected.index(fig_settings['sort_by_file'])

    tokens_freq_files = wl_sorting.sorted_tokens_freq_files_ref(
        tokens_freq_files,
        sort_by_col = col_sort_by_file
    )

    # Line Chart
    if fig_settings['graph_type'] == _tr('wl_fig_freq_keyword_extractor', 'Line Chart'):
        wl_figs.generate_line_chart(
            main, tokens_freq_files,
            fig_settings = fig_settings,
            freq_data = True,
            file_names_selected = file_names_selected,
            label_x = label_x
        )
    # Word Cloud
    elif fig_settings['graph_type'] == _tr('wl_fig_freq_keyword_extractor', 'Word Cloud'):
        tokens_freq_file = [
            (token, freq_files[col_sort_by_file])
            for token, freq_files in tokens_freq_files
        ]

        wl_figs.generate_word_cloud(main, tokens_freq_file, fig_settings = fig_settings)
