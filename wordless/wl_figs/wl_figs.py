# ----------------------------------------------------------------------
# Wordless: Figures - Figures
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

import re

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDesktopWidget
import matplotlib
import matplotlib.pyplot
import networkx
import numpy
import wordcloud

from wordless.wl_utils import wl_misc

_tr = QCoreApplication.translate

def get_data_ranks(data_files_items, fig_settings):
    if fig_settings['rank_min_no_limit']:
        rank_min = 1
    else:
        rank_min = fig_settings['rank_min']

    if fig_settings['rank_max_no_limit']:
        rank_max = None
    else:
        rank_max = fig_settings['rank_max']

    return data_files_items[rank_min - 1 : rank_max]

def generate_line_chart(
    main,
    data_files_items, fig_settings,
    file_names_selected, label_x
): # pylint: disable=unused-argument
    data_files_items = get_data_ranks(data_files_items, fig_settings)

    items = [item for item, vals in data_files_items]
    vals = numpy.array([vals for item, vals in data_files_items])

    # Frequency data
    if fig_settings['use_data'] == _tr('wl_figs', 'Frequency') or re.search(_tr('wl_figs', r'^[LR][1-9][0-9]*$'), fig_settings['use_data']):
        if fig_settings['use_cumulative']:
            vals = numpy.cumsum(vals, axis = 0)

        if fig_settings['use_pct']:
            total_freqs = numpy.array([vals for item, vals in data_files_items]).sum(axis = 0)

            for i, (file_name, total_freq) in enumerate(zip(file_names_selected, total_freqs)):
                matplotlib.pyplot.plot(vals[:, i] / total_freq * 100, label = file_name)
        else:
            for i, file_name in enumerate(file_names_selected):
                matplotlib.pyplot.plot(vals[:, i], label = file_name)

        if fig_settings['use_cumulative']:
            if fig_settings['use_pct']:
                matplotlib.pyplot.ylabel(_tr('wl_figs', 'Cumulative Percentage Frequency'))
            else:
                matplotlib.pyplot.ylabel(_tr('wl_figs', 'Cumulative Frequency'))
        else:
            if fig_settings['use_pct']:
                matplotlib.pyplot.ylabel(_tr('wl_figs', 'Percentage Frequency'))
            else:
                matplotlib.pyplot.ylabel(_tr('wl_figs', 'Frequency'))
    # Non-frenquency data
    else:
        for i, file_name in enumerate(file_names_selected):
            matplotlib.pyplot.plot(vals[:, i], label = file_name)

        matplotlib.pyplot.ylabel(fig_settings['use_data'])

    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.xticks(
        range(len(items)),
        labels = items,
        rotation = 90
    )

    matplotlib.pyplot.grid(True, color = 'silver')
    matplotlib.pyplot.legend()

def generate_word_cloud(main, data_file_items, fig_settings):
    data_file_items = get_data_ranks(data_file_items, fig_settings)

    items = [item for item, val in data_file_items]
    # Convert to numpy.float64 to fix zeros
    vals = numpy.array([val for item, val in data_file_items], dtype = numpy.float64)

    val_min = numpy.min(vals[vals != -numpy.inf]) if vals[vals != -numpy.inf].size > 0 else -10
    val_max = numpy.max(vals[vals != numpy.inf]) if vals[vals != numpy.inf].size > 0 else 10

    # Fix +/-inf
    vals = numpy.where(vals != numpy.inf, vals, val_max * 10)
    vals = numpy.where(vals != -numpy.inf, vals, val_min * 10)

    # Fix negative data
    if vals[vals < 0].size > 0:
        vals += (-numpy.min(vals)) + 1e-15

    # Fix zeros
    if vals[vals == 0].size > 0:
        vals += 1e-15

    # WordCloud always displays data descendingly
    if fig_settings['use_data'] == _tr('wl_figs', 'p-value'):
        vals = 1 - vals

    desktop_widget = QDesktopWidget()

    word_cloud = wordcloud.WordCloud(
        width = desktop_widget.width(),
        height = desktop_widget.height(),
        background_color = main.settings_custom['figs']['word_clouds']['bg_color'],
    )
    word_cloud.generate_from_frequencies(dict(zip(items, vals)))

    matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
    matplotlib.pyplot.axis('off')

def generate_network_graph(main, data_file_items, fig_settings):
    data_file_items = dict(get_data_ranks(data_file_items, fig_settings))

    graph = networkx.MultiDiGraph()
    graph.add_edges_from(data_file_items)

    graph_layout = main.settings_custom['figs']['network_graphs']['layout']

    if graph_layout == _tr('wl_figs', 'Circular'):
        layout = networkx.circular_layout(graph)
    elif graph_layout == _tr('wl_figs', 'Kamada-Kawai'):
        layout = networkx.kamada_kawai_layout(graph)
    elif graph_layout == _tr('wl_figs', 'Planar'):
        layout = networkx.planar_layout(graph)
    elif graph_layout == _tr('wl_figs', 'Random'):
        layout = networkx.random_layout(graph)
    elif graph_layout == _tr('wl_figs', 'Shell'):
        layout = networkx.shell_layout(graph)
    elif graph_layout == _tr('wl_figs', 'Spring'):
        layout = networkx.spring_layout(graph)
    elif graph_layout == _tr('wl_figs', 'Spectral'):
        layout = networkx.spectral_layout(graph)

    networkx.draw_networkx_nodes(
        graph,
        pos = layout,
        node_size = 800,
        node_color = '#FFFFFF',
        alpha = 0.4
    )

    if fig_settings['use_data'] == _tr('wl_figs', 'p-value'):
        precision = main.settings_custom['tables']['precision_settings']['precision_p_vals']
        reverse = True
    else:
        precision = main.settings_custom['tables']['precision_settings']['precision_decimals']
        reverse = False

    data_file_items = {
        item: round(val, precision)
        for item, val in data_file_items.items()
    }

    networkx.draw_networkx_edges(
        graph,
        pos = layout,
        edgelist = data_file_items,
        edge_color = main.settings_custom['figs']['network_graphs']['edge_color'],
        width = wl_misc.normalize_nums(
            data_file_items.values(),
            normalized_min = 1,
            normalized_max = 5,
            reverse = reverse
        )
    )

    networkx.draw_networkx_labels(
        graph,
        pos = layout,
        font_family = main.settings_custom['figs']['network_graphs']['node_font'],
        font_size = main.settings_custom['figs']['network_graphs']['node_font_size']
    )
    networkx.draw_networkx_edge_labels(
        graph,
        pos = layout,
        edge_labels = data_file_items,
        label_pos = 0.2,
        font_family = main.settings_custom['figs']['network_graphs']['edge_font'],
        font_size = main.settings_custom['figs']['network_graphs']['edge_font_size']
    )

def show_fig():
    matplotlib.pyplot.get_current_fig_manager().window.showMaximized()
