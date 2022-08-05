# ----------------------------------------------------------------------
# Wordless: Figures - Statistics
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

def wl_fig_stat(main, tokens_stat_files, fig_settings, label_x):
    file_names_selected = [*main.wl_file_area.get_selected_file_names(), _tr('wl_fig_stat', 'Total')]
    col_sort_by_file = file_names_selected.index(fig_settings['sort_by_file'])

    if fig_settings['use_data'] == _tr('wl_fig_stat', 'p-value'):
        tokens_stat_files = wl_sorting.sorted_tokens_freq_files(
            tokens_stat_files,
            sort_by_col = col_sort_by_file,
            reverse = True
        )
    else:
        tokens_stat_files = wl_sorting.sorted_tokens_freq_files(
            tokens_stat_files,
            sort_by_col = col_sort_by_file
        )

    # Line Chart
    if fig_settings['graph_type'] == _tr('wl_fig_stat', 'Line Chart'):
        wl_figs.generate_line_chart(
            main, tokens_stat_files,
            fig_settings = fig_settings,
            freq_data = False,
            file_names_selected = file_names_selected,
            label_x = label_x
        )
    else:
        tokens_stat_file = [
            (token, stat_files[col_sort_by_file])
            for token, stat_files in tokens_stat_files
        ]

        # Word Cloud
        if fig_settings['graph_type'] == _tr('wl_fig_stat', 'Word Cloud'):
            wl_figs.generate_word_cloud(main, tokens_stat_file, fig_settings = fig_settings)
        # Network Graph
        elif fig_settings['graph_type'] == _tr('wl_fig_stat', 'Network Graph'):
            wl_figs.generate_network_graph(main, tokens_stat_file, fig_settings = fig_settings)

def wl_fig_stat_keyword_extractor(main, keywords_stat_files, fig_settings, label_x):
    file_names_selected = [*main.wl_file_area.get_selected_file_names(), _tr('wl_fig_stat_keyword_extractor', 'Total')]
    col_sort_by_file = file_names_selected.index(fig_settings['sort_by_file'])

    if fig_settings['use_data'] == _tr('wl_fig_stat_keyword_extractor', 'p-value'):
        keywords_stat_files = wl_sorting.sorted_tokens_freq_files(
            keywords_stat_files,
            sort_by_col = col_sort_by_file,
            reverse = True
        )
    else:
        keywords_stat_files = wl_sorting.sorted_tokens_freq_files(
            keywords_stat_files,
            sort_by_col = col_sort_by_file
        )

    if fig_settings['graph_type'] == _tr('wl_fig_stat_keyword_extractor', 'Line Chart'):
        wl_figs.generate_line_chart(
            main, keywords_stat_files,
            fig_settings = fig_settings,
            freq_data = False,
            file_names_selected = file_names_selected,
            label_x = label_x
        )
    elif fig_settings['graph_type'] == _tr('wl_fig_stat_keyword_extractor', 'Word Cloud'):
        keywords_stat_file = [
            (keyword, stat_files[col_sort_by_file])
            for keyword, stat_files in keywords_stat_files
        ]

        wl_figs.generate_word_cloud(main, keywords_stat_file, fig_settings = fig_settings)
