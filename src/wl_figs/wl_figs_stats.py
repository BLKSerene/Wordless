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

from PyQt5.QtWidgets import *

import matplotlib
import matplotlib.pyplot
import networkx
import numpy
import wordcloud

from wl_utils import wl_misc, wl_sorting

def wl_fig_stat(main, tokens_stat_files, settings, label_x, label_y):
    file_names_selected = main.wl_files.get_selected_file_names() + [main.tr('Total')]
    col_sort_by_file = file_names_selected.index(settings['sort_by_file'])

    if label_y == main.tr('p-value'):
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

    if settings['rank_min_no_limit']:
        rank_min = 1
    else:
        rank_min = settings['rank_min']

    if settings['rank_max_no_limit']:
        rank_max = None
    else:
        rank_max = settings['rank_max']

    # Line Chart
    if settings['graph_type'] == main.tr('Line Chart'):
        tokens = [item[0] for item in tokens_stat_files[rank_min - 1 : rank_max]]
        stats = [item[1] for item in tokens_stat_files if item[0] in tokens]

        for i, file_name in enumerate(file_names_selected):
            matplotlib.pyplot.plot(
                [stat_files[i] for stat_files in stats],
                label = file_name
            )

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(
            range(len(tokens)),
            labels = tokens,
            fontproperties = main.settings_custom['figs']['line_chart']['font'],
            rotation = 90
        )

        matplotlib.pyplot.ylabel(label_y)

        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
    # Word Cloud
    elif settings['graph_type'] == main.tr('Word Cloud'):
        if rank_max == None:
            max_words = len(tokens_freq_files) - rank_min + 1
        else:
            max_words = rank_max - rank_min + 1

        word_cloud = wordcloud.WordCloud(
            width = QDesktopWidget().width(),
            height = QDesktopWidget().height(),
            background_color = main.settings_custom['figs']['word_cloud']['bg_color'],
            max_words = max_words
        )

        tokens_stat_file = {
            token: stat_files[col_sort_by_file]
            for token, stat_files in tokens_stat_files[rank_min - 1 : rank_max]
        }

        # Fix zero frequencies
        for token, stat in tokens_stat_file.items():
            if stat == 0:
                tokens_stat_file[token] += 0.000000000000001
        
        # WordCloud always display data descendingly
        if label_y == main.tr('p-value'):
            tokens_stat_file = {
                token: 1 - p_value
                for token, p_value in tokens_stat_file.items()
            }

        word_cloud.generate_from_frequencies(tokens_stat_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
    # Network Graph
    elif settings['graph_type'] == main.tr('Network Graph'):
        tokens_stat_file = {
            token: stat_files[col_sort_by_file]
            for token, stat_files in tokens_stat_files[rank_min - 1 : rank_max]
        }

        graph = networkx.MultiDiGraph()
        graph.add_edges_from(tokens_stat_file)

        if main.settings_custom['figs']['network_graph']['layout'] == main.tr('Circular'):
            layout = networkx.circular_layout(graph)
        elif main.settings_custom['figs']['network_graph']['layout'] == main.tr('Kamada-Kawai'):
            layout = networkx.kamada_kawai_layout(graph)
        elif main.settings_custom['figs']['network_graph']['layout'] == main.tr('Planar'):
            layout = networkx.planar_layout(graph)
        elif main.settings_custom['figs']['network_graph']['layout'] == main.tr('Random'):
            layout = networkx.random_layout(graph)
        elif main.settings_custom['figs']['network_graph']['layout'] == main.tr('Shell'):
            layout = networkx.shell_layout(graph)
        elif main.settings_custom['figs']['network_graph']['layout'] == main.tr('Spring'):
            layout = networkx.spring_layout(graph)
        elif main.settings_custom['figs']['network_graph']['layout'] == main.tr('Spectral'):
            layout = networkx.spectral_layout(graph)

        networkx.draw_networkx_nodes(
            graph,
            pos = layout,
            node_size = 800,
            node_color = '#FFFFFF',
            alpha = 0.4
        )
        if label_y == main.tr('p-value'):
            networkx.draw_networkx_edges(
                graph,
                pos = layout,
                edgelist = tokens_stat_file,
                edge_color = '#5C88C5',
                width = wl_misc.normalize_nums(
                    tokens_stat_file.values(),
                    normalized_min = 1,
                    normalized_max = 5,
                    normalized_reversed = True
                )
            )
        else:
            networkx.draw_networkx_edges(
                graph,
                pos = layout,
                edgelist = tokens_stat_file,
                edge_color = main.settings_custom['figs']['network_graph']['edge_color'],
                width = wl_misc.normalize_nums(
                    tokens_stat_file.values(),
                    normalized_min = 1,
                    normalized_max = 5
                )
            )
        networkx.draw_networkx_labels(
            graph,
            pos = layout,
            font_family = main.settings_custom['figs']['network_graph']['node_font'],
            font_size = main.settings_custom['figs']['network_graph']['node_font_size']
        )
        networkx.draw_networkx_edge_labels(
            graph,
            pos = layout,
            edge_labels = {token: round(stat, 2)
                           for token, stat in tokens_stat_file.items()},
            font_family = main.settings_custom['figs']['network_graph']['edge_font'],
            font_size = main.settings_custom['figs']['network_graph']['edge_font_size'],
            label_pos = 0.2
        )

def wl_fig_stat_keyword(main, keywords_stat_files, files_ref, settings, label_y):
    file_names_selected = main.wl_files.get_selected_file_names() + [main.tr('Total')]
    file_names_selected = [
        file_name
        for file_name in file_names_selected
        if file_name not in files_ref
    ]
    col_sort_by_file = file_names_selected.index(settings['sort_by_file'])

    if label_y == main.tr('p-value'):
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

    if settings['rank_min_no_limit']:
        rank_min = 1
    else:
        rank_min = settings['rank_min']

    if settings['rank_max_no_limit']:
        rank_max = None
    else:
        rank_max = settings['rank_max']

    if settings['graph_type'] == main.tr('Line Chart'):
        keywords = [item[0] for item in keywords_stat_files[rank_min - 1 : rank_max]]
        stats = [item[1] for item in keywords_stat_files if item[0] in keywords]

        for i, file_name in enumerate(file_names_selected):
            matplotlib.pyplot.plot(
                [stats_files[i] for stats_files in stats],
                label = file_name
            )

        matplotlib.pyplot.xlabel(main.tr('Keyword'))

        matplotlib.pyplot.ylabel(label_y)
        matplotlib.pyplot.xticks(
            range(len(keywords)),
            labels = keywords,
            fontproperties = main.settings_custom['figs']['line_chart']['font'],
            rotation = 90
        )

        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
    elif settings['graph_type'] == main.tr('Word Cloud'):
        if rank_max == None:
            max_words = len(tokens_freq_files) - rank_min + 1
        else:
            max_words = rank_max - rank_min + 1

        word_cloud = wordcloud.WordCloud(
            width = QDesktopWidget().width(),
            height = QDesktopWidget().height(),
            background_color = main.settings_custom['figs']['word_cloud']['bg_color'],
            max_words = max_words
        )

        keywords_stat_file = {
            keyword: stat_files[col_sort_by_file]
            for keyword, stat_files in keywords_stat_files[rank_min - 1 : rank_max]
        }

        # Fix zero frequencies
        for keyword, stat in keywords_stat_file.items():
            if stat == 0:
                keywords_stat_file[keyword] += 0.000000000000001

        # WordCloud always display data descendingly
        if label_y == main.tr('p-value'):
            keywords_stat_file = {
                keyword: 1 - p_value
                for keyword, p_value in keywords_stat_file.items()
            }
        
        word_cloud.generate_from_frequencies(keywords_stat_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        