# ----------------------------------------------------------------------
# Wordless: Figures - Figures
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

import os
import re

import matplotlib
import matplotlib.pyplot
import networkx
import numpy
import PIL
import PIL.Image
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import wordcloud

from wordless.wl_dialogs import wl_dialogs
from wordless.wl_utils import (
    wl_excs,
    wl_misc,
    wl_paths
)

_tr = QtCore.QCoreApplication.translate

# Restore Matplotlib's default settings
def restore_matplotlib_rcparams():
    matplotlib.pyplot.rcParams['savefig.facecolor'] = 'auto'

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
    restore_matplotlib_rcparams()

    data_files_items = get_data_ranks(data_files_items, fig_settings)

    items = [item for item, vals in data_files_items]
    vals = numpy.array([vals for item, vals in data_files_items])

    # Frequency data
    if (
        fig_settings['use_data'] == _tr('wl_figs', 'Frequency')
        or re.search(_tr('wl_figs', r'^[LR][1-9][0-9]*$'), fig_settings['use_data'])
    ):
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
    # Non-frequency data
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
    restore_matplotlib_rcparams()

    data_file_items = get_data_ranks(data_file_items, fig_settings)

    items = [item for item, val in data_file_items]
    # Convert to numpy.float64 to fix zeros
    vals = numpy.array([val for item, val in data_file_items], dtype = numpy.float64)

    val_min = numpy.min(vals[vals != -numpy.inf]) if vals[vals != -numpy.inf].size > 0 else -10
    val_max = numpy.max(vals[vals != numpy.inf]) if vals[vals != numpy.inf].size > 0 else 10

    # Fix +/-inf
    vals = numpy.where(vals != numpy.inf, vals, val_max * 10)
    vals = numpy.where(vals != -numpy.inf, vals, val_min * 10)

    # WordCloud always displays data descendingly
    if fig_settings['use_data'] == _tr('wl_figs', 'p-value'):
        vals = 1 - vals

    # Fix negative numbers
    if vals[vals < 0].size > 0:
        vals += (-numpy.min(vals)) + 1e-15

    # Fix zeros
    if vals[vals == 0].size > 0:
        vals += 1e-15

    settings = main.settings_custom['figs']['word_clouds']
    desktop_widget = QtWidgets.QDesktopWidget()

    if settings['font_settings']['font'] == 'Droid Sans Mono':
        font_path = wordcloud.wordcloud.FONT_PATH
    elif settings['font_settings']['font'] == 'GNU Unifont':
        font_path = wl_paths.get_path_data('unifont-16.0.04.otf')
    elif settings['font_settings']['font'] == _tr('wl_figs', 'Custom'):
        font_path = settings['font_settings']['font_path']

    if settings['font_settings']['relative_scaling'] == -0.01:
        relative_scaling = 'auto'
    else:
        relative_scaling = settings['font_settings']['relative_scaling']

    if settings['font_settings']['font_color'] == _tr('wl_figs', 'Monochrome'):
        color_func = lambda *args, **kwargs: settings['font_settings']['font_color_monochrome'] # pylint: disable=unnecessary-lambda-assignment
    elif settings['font_settings']['font_color'] == _tr('wl_figs', 'Colormap'):
        color_func = None

    if settings['bg_settings']['bg_color_transparent']:
        # Modify Matplotlib's global settings
        matplotlib.pyplot.rcParams['savefig.facecolor'] = (0, 0, 0, 0)

        bg_color = None
        mode = 'RGBA'
    else:
        bg_color = settings['bg_settings']['bg_color']
        mode = 'RGB'

    try:
        if settings['mask_settings']['mask_settings']:
            mask = numpy.array(PIL.Image.open(settings['mask_settings']['mask_path']))
        else:
            mask = None

        word_cloud = wordcloud.WordCloud(
            width = desktop_widget.width(),
            height = desktop_widget.height(),
            font_path = font_path,
            min_font_size = settings['font_settings']['font_size_min'],
            max_font_size = settings['font_settings']['font_size_max'],
            relative_scaling = relative_scaling,
            color_func = color_func,
            colormap = settings['font_settings']['font_color_colormap'],
            background_color = bg_color,
            mode = mode,
            mask = mask,
            # Known issue: Error when background is transparent and contour width > 0
            # Reference: https://github.com/amueller/word_cloud/issues/501
            contour_width = settings['mask_settings']['contour_width'],
            contour_color = settings['mask_settings']['contour_color'],
            # The ratio of times to try horizontal fitting as opposed to vertical, ranging from 0 to 1 inclusive
            prefer_horizontal = settings['advanced_settings']['prefer_hor'] / 100,
            repeat = settings['advanced_settings']['allow_repeated_words']
        )

        word_cloud.generate_from_frequencies(dict(zip(items, vals)))

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
    # Invalid mask image
    except (FileNotFoundError, PermissionError, PIL.UnidentifiedImageError) as exc:
        mask_path = settings['mask_settings']['mask_path']

        if not os.path.exists(mask_path):
            err_title = _tr('wl_figs', 'Mask Image Not Found')
            err_msg = _tr('wl_figs', 'The specified mask image "{}" for generating the word cloud cannot be found.').format(mask_path)
            err_exc = wl_excs.Wl_Exc_Word_Cloud_Mask_Nonexistent()
        elif os.path.isdir(mask_path):
            err_title = _tr('wl_figs', 'Mask Image Is a Folder')
            err_msg = _tr('wl_figs', 'The specified mask image "{}" for generating the word cloud is a folder rather than a file.').format(mask_path)
            err_exc = wl_excs.Wl_Exc_Word_Cloud_Mask_Is_Dir()
        else:
            err_title = _tr('wl_figs', 'Mask Image Not Supported')
            err_msg = _tr('wl_figs', 'The specified mask image "{}" for generating the word cloud is not supported.').format(mask_path)
            err_exc = wl_excs.Wl_Exc_Word_Cloud_Mask_Unsupported()

        wl_dialogs.Wl_Dialog_Info_Simple(
            main,
            title = err_title,
            text = _tr('wl_figs', '''
                <div>{}</div>
                <br>
                <div>Please check your mask image or specify another one in <b>Menu → Preferences → Settings → Figures → Word Clouds → Mask Settings → Mask Path</b>.</div>
            ''').format(err_msg),
            icon = 'critical'
        ).open()

        raise err_exc from exc
    # Invalid font file
    except OSError as exc:
        font_path = settings['font_settings']['font_path']

        if not os.path.exists(font_path):
            err_title = _tr('wl_figs', 'Font File Not Found')
            err_msg = _tr('wl_figs', 'The specified font file "{}" for generating the word cloud cannot be found.').format(font_path)
            err_exc = wl_excs.Wl_Exc_Word_Cloud_Font_Nonexistent()
        elif os.path.isdir(font_path):
            err_title = _tr('wl_figs', 'Font File Is a Folder')
            err_msg = _tr('wl_figs', 'The specified font file "{}" for generating the word cloud is a folder rather than a file.').format(font_path)
            err_exc = wl_excs.Wl_Exc_Word_Cloud_Font_Is_Dir()
        else:
            err_title = _tr('wl_figs', 'Font File Not Supported')
            err_msg = _tr('wl_figs', 'The specified font file "{}" for generating the word cloud is not supported.').format(font_path)
            err_exc = wl_excs.Wl_Exc_Word_Cloud_Font_Unsupported()

        wl_dialogs.Wl_Dialog_Info_Simple(
            main,
            title = err_title,
            text = _tr('wl_figs', '''
                <div>{}</div>
                <br>
                <div>Please check your font file or specify another one in <b>Menu → Preferences → Settings → Figures → Word Clouds → Font Settings → Font</b>.</div>
            ''').format(err_msg),
            icon = 'critical'
        ).open()

        raise err_exc from exc

def generate_network_graph(main, data_file_items, fig_settings):
    restore_matplotlib_rcparams()

    data_file_items = dict(get_data_ranks(data_file_items, fig_settings))
    settings = main.settings_custom['figs']['network_graphs']

    graph = networkx.MultiDiGraph()
    graph.add_edges_from(data_file_items)

    pos = settings['advanced_settings']['layout'](graph)

    if settings['node_settings']['same_as_node_color']:
        border_color = None
    else:
        border_color = settings['node_settings']['border_color']

    networkx.draw_networkx_nodes(
        graph,
        pos = pos,
        node_shape = settings['node_settings']['node_shape'],
        node_size = settings['node_settings']['node_size'],
        node_color = settings['node_settings']['node_color'],
        alpha = settings['node_settings']['node_opacity'],
        linewidths = settings['node_settings']['border_width'],
        edgecolors = border_color
    )

    networkx.draw_networkx_labels(
        graph,
        pos = {node: (x, y + 0.05) for node, (x, y) in pos.items()},
        font_family = settings['node_label_settings']['font_family'],
        font_size = settings['node_label_settings']['font_size'],
        font_weight = settings['node_label_settings']['font_weight'],
        font_color = settings['node_label_settings']['font_color'],
        alpha = settings['node_label_settings']['label_opacity'],
        horizontalalignment = settings['node_label_settings']['hor_alignment'],
        verticalalignment = settings['node_label_settings']['vert_alignment']
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
        pos = pos,
        edgelist = data_file_items,
        width = wl_misc.normalize_nums(
            data_file_items.values(),
            normalized_min = settings['edge_settings']['edge_width_min'],
            normalized_max = settings['edge_settings']['edge_width_max'],
            reverse = reverse
        ),
        connectionstyle = settings['edge_settings']['connection_style'],
        style = settings['edge_settings']['edge_style'],
        edge_color = settings['edge_settings']['edge_color'],
        alpha = settings['edge_settings']['edge_opacity'],
        arrowstyle = settings['edge_settings']['arrow_style'],
        arrowsize = settings['edge_settings']['arrow_size'],
        # Used to determine edge positions
        node_shape = settings['node_settings']['node_shape'],
        node_size = settings['node_settings']['node_size']
    )

    networkx.draw_networkx_edge_labels(
        graph,
        pos = pos,
        edge_labels = data_file_items,
        label_pos = settings['edge_label_settings']['label_position'],
        rotate = settings['edge_label_settings']['rotate_labels'],
        font_family = settings['edge_label_settings']['font_family'],
        font_size = settings['edge_label_settings']['font_size'],
        font_weight = settings['edge_label_settings']['font_weight'],
        font_color = settings['edge_label_settings']['font_color'],
        alpha = settings['edge_label_settings']['label_opacity'],
        horizontalalignment = settings['edge_label_settings']['hor_alignment'],
        verticalalignment = settings['edge_label_settings']['vert_alignment'],
        # Used to determine edge label positions
        connectionstyle = settings['edge_settings']['connection_style']
    )

def show_fig():
    matplotlib.pyplot.get_current_fig_manager().window.showMaximized()
