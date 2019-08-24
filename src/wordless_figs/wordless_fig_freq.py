#
# Wordless: Figures - Frequency
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

from PyQt5.QtWidgets import *

import matplotlib
import matplotlib.pyplot
import networkx
import numpy
import wordcloud

from wordless_utils import wordless_misc, wordless_sorting

def wordless_fig_freq(main, tokens_freq_files,
                      settings, label_x):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]

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
        tokens_freq_files = wordless_sorting.sorted_tokens_freq_files(tokens_freq_files)

        total_freqs = numpy.array(list(zip(*tokens_freq_files))[1]).sum(axis = 0)
        total_freq = sum(total_freqs)

        tokens = [item[0] for item in tokens_freq_files[rank_min - 1 : rank_max]]
        freqs = [item[1] for item in tokens_freq_files if item[0] in tokens]

        if settings['use_pct']:
            if settings['use_cumulative']:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Percentage Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Percentage Frequency'))
        else:
            if settings['use_cumulative']:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Frequency'))

        if settings['use_cumulative']:
            for i, freq_files in enumerate(freqs):
                if i >= 1:
                    freqs[i] = [freq_cumulative + freq
                                for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

        if settings['use_pct']:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs],
                                       label = file['name'])
        else:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs],
                                       label = file['name'])

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.grid(True)
        matplotlib.pyplot.legend()
    # Word Cloud
    elif settings['graph_type'] == main.tr('Word Cloud'):
        if rank_max == None:
            max_words = len(tokens_freq_files) - rank_min + 1
        else:
            max_words = rank_max - rank_min + 1

        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = main.settings_custom['figs']['word_cloud']['bg_color'],
                                         max_words = max_words)

        for i, file in enumerate(files):
            if file['name'] == settings['use_file']:
                tokens_freq_files = wordless_sorting.sorted_tokens_freq_file(tokens_freq_files, i)

                tokens_freq_file = {token: freqs[i]
                                    for token, freqs in tokens_freq_files[rank_min - 1 : rank_max]}

                break

        # Fix zero frequencies
        for token, freq in tokens_freq_file.items():
            if freq == 0:
                tokens_freq_file[token] += 0.000000000000001

        word_cloud.generate_from_frequencies(tokens_freq_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
    # Network Graph
    elif settings['graph_type'] == main.tr('Network Graph'):
        for i, file in enumerate(files):
            if file['name'] == settings['use_file']:
                tokens_freq_files = wordless_sorting.sorted_tokens_freq_file(tokens_freq_files, i)

                tokens_freq_file = {token: freqs[i]
                                    for token, freqs in tokens_freq_files[rank_min - 1 : rank_max]}

                break

        graph = networkx.MultiDiGraph()
        graph.add_edges_from(tokens_freq_file)

        layout = networkx.spring_layout(graph)

        networkx.draw_networkx_nodes(graph,
                                     pos = layout,
                                     node_size = 800,
                                     node_color = '#FFFFFF',
                                     alpha = 0.4)
        networkx.draw_networkx_edges(graph,
                                     pos = layout,
                                     edgelist = tokens_freq_file,
                                     edge_color = '#5C88C5',
                                     width = wordless_misc.normalize_nums(tokens_freq_file.values(), 1, 5))
        networkx.draw_networkx_labels(graph,
                                      pos = layout,
                                      font_size = 10)
        networkx.draw_networkx_edge_labels(graph,
                                           pos = layout,
                                           edge_labels = tokens_freq_file,
                                           font_size = 8,
                                           label_pos = 0.2)

def wordless_fig_freq_ref(main, tokens_freq_files, ref_file,
                          settings, label_x):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]

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
        tokens_freq_files = wordless_sorting.sorted_tokens_freq_files_ref(tokens_freq_files)

        total_freqs = numpy.array([item[1] for item in tokens_freq_files]).sum(axis = 0)
        total_freq_ref = total_freqs[0]
        total_freq_total = total_freqs[-1]

        tokens = [item[0] for item in tokens_freq_files[rank_min - 1 : rank_max]]
        freqs = [item[1] for item in tokens_freq_files if item[0] in tokens]

        if settings['use_pct']:
            if settings['use_cumulative']:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Percentage Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Percentage Frequency'))
        else:
            if settings['use_cumulative']:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Frequency'))

        if settings['use_cumulative']:
            for i, freq_files in enumerate(freqs):
                if i >= 1:
                    freqs[i] = [freq_cumulative + freq
                                for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

        if settings['use_pct']:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs],
                                       label = file['name'])
        else:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs],
                                       label = file['name'])

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
    # Word Cloud
    elif settings['graph_type'] == main.tr('Word Cloud'):
        files.remove(ref_file)

        if rank_max == None:
            max_words = len(tokens_freq_files) - rank_min + 1
        else:
            max_words = rank_max - rank_min + 1

        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = main.settings_custom['figs']['word_cloud']['bg_color'],
                                         max_words = max_words)

        for i, file in enumerate(files):
            if file['name'] == settings['use_file']:
                tokens_freq_files = wordless_sorting.sorted_tokens_freq_file(tokens_freq_files, i + 1)

                tokens_freq_file = {token: freq_files[i + 1]
                                    for token, freq_files in tokens_freq_files[rank_min - 1 : rank_max]}

                break

        tokens_freq_file = {token: freq for token, freq in tokens_freq_file.items() if freq}

        # Fix zero frequencies
        for token, freq in tokens_freq_file.items():
            if freq == 0:
                tokens_freq_file[token] += 0.000000000000001

        word_cloud.generate_from_frequencies(tokens_freq_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')

        matplotlib.pyplot.axis('off')
