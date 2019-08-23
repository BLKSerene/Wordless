#
# Wordless: Figures - Statistics
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

def wordless_fig_stat(main, tokens_stat_files,
                      settings, label_x, label_y):
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
        if label_y == main.tr('p-value'):
            tokens_stat_files = list(reversed(wordless_sorting.sorted_tokens_stat_files(tokens_stat_files)))
        else:
            tokens_stat_files = wordless_sorting.sorted_tokens_stat_files(tokens_stat_files)

        tokens = [item[0] for item in tokens_stat_files[rank_min - 1 : rank_max]]
        stats = [item[1] for item in tokens_stat_files if item[0] in tokens]

        for i, file in enumerate(files):
            matplotlib.pyplot.plot([stat_files[i] for stat_files in stats],
                                   label = file['name'])

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.ylabel(label_y)

        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
    # Word Cloud
    elif settings['graph_type'] == main.tr('Word Cloud'):
        if rank_max == None:
            max_words = len(tokens_freq_files) - rank_min + 1
        else:
            max_words = rank_max - rank_min + 1

        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = max_words)

        for i, file in enumerate(files):
            if file['name'] == settings['use_file']:
                if label_y == main.tr('p-value'):
                    tokens_stat_files = list(reversed(wordless_sorting.sorted_tokens_stat_file(tokens_stat_files, i)))
                else:
                    tokens_stat_files = wordless_sorting.sorted_tokens_stat_file(tokens_stat_files, i)

                tokens_stat_file = {token: stat_files[i]
                                     for token, stat_files in tokens_stat_files[rank_min - 1 : rank_max]}

                break

        # Fix zero frequencies
        for token, stat in tokens_stat_file.items():
            if stat == 0:
                tokens_stat_file[token] += 0.000000000000001

        word_cloud.generate_from_frequencies(tokens_stat_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
    # Network Graph
    elif settings['graph_type'] == main.tr('Network Graph'):
        for i, file in enumerate(files):
            if file['name'] == settings['use_file']:
                if label_y == main.tr('p-value'):
                    tokens_stat_files = list(reversed(wordless_sorting.sorted_tokens_stat_file(tokens_stat_files, i)))
                else:
                    tokens_stat_files = wordless_sorting.sorted_tokens_stat_file(tokens_stat_files, i)

                tokens_stat_file = {token: stat_files[i]
                                     for token, stat_files in tokens_stat_files[rank_min - 1 : rank_max]}

                break

        graph = networkx.MultiDiGraph()
        graph.add_edges_from(tokens_stat_file)

        layout = networkx.spring_layout(graph)

        networkx.draw_networkx_nodes(graph,
                                     pos = layout,
                                     node_size = 800,
                                     node_color = '#FFFFFF',
                                     alpha = 0.4)
        if label_y == main.tr('p-value'):
            networkx.draw_networkx_edges(graph,
                                     pos = layout,
                                     edgelist = tokens_stat_file,
                                     edge_color = '#5C88C5',
                                     width = wordless_misc.normalize_nums(tokens_stat_file.values(),
                                                                          normalized_min = 1,
                                                                          normalized_max = 5,
                                                                          normalized_reversed = True))
        else:
            networkx.draw_networkx_edges(graph,
                                         pos = layout,
                                         edgelist = tokens_stat_file,
                                         edge_color = '#5C88C5',
                                         width = wordless_misc.normalize_nums(tokens_stat_file.values(),
                                                                              normalized_min = 1,
                                                                              normalized_max = 5))
        networkx.draw_networkx_labels(graph,
                                      pos = layout,
                                      font_size = 10)
        networkx.draw_networkx_edge_labels(graph,
                                           pos = layout,
                                           edge_labels = {token: round(stat, 2)
                                                          for token, stat in tokens_stat_file.items()},
                                           font_size = 8,
                                           label_pos = 0.2)

def wordless_fig_stat_ref(main, keywords_stat_files, ref_file,
                          settings, label_y):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]
    files.remove(ref_file)

    if settings['rank_min_no_limit']:
        rank_min = 1
    else:
        rank_min = settings['rank_min']

    if settings['rank_max_no_limit']:
        rank_max = None
    else:
        rank_max = settings['rank_max']

    if settings['graph_type'] == main.tr('Line Chart'):
        if label_y == main.tr('p-value'):
            keywords_stat_files = list(reversed(wordless_sorting.sorted_keywords_stat_files(keywords_stat_files)))
        else:
            keywords_stat_files = wordless_sorting.sorted_keywords_stat_files(keywords_stat_files)

        keywords = [item[0] for item in keywords_stat_files[rank_min - 1 : rank_max]]
        stats = [item[1] for item in keywords_stat_files if item[0] in keywords]

        for i, file in enumerate(files):
            matplotlib.pyplot.plot([stats_files[i] for stats_files in stats],
                                   label = file['name'])

        matplotlib.pyplot.xlabel(main.tr('Keywords'))

        matplotlib.pyplot.ylabel(label_y)
        matplotlib.pyplot.xticks(range(len(keywords)), keywords, rotation = 90)

        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
    elif settings['graph_type'] == main.tr('Word Cloud'):
        if rank_max == None:
            max_words = len(tokens_freq_files) - rank_min + 1
        else:
            max_words = rank_max - rank_min + 1

        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = max_words)

        for i, file in enumerate(files):
            if file['name'] == settings['use_file']:
                if label_y == main.tr('p-value'):
                    keywords_stat_files = list(reversed(wordless_sorting.sorted_keywords_stat_file(keywords_stat_files, i)))
                else:
                    keywords_stat_files = wordless_sorting.sorted_keywords_stat_file(keywords_stat_files, i)

                keywords_stat_file = {keyword: stat_files[i]
                                      for keyword, stat_files in keywords_stat_files[rank_min - 1 : rank_max]}

                break

        if label_y == main.tr('p-value'):
            keywords_stat_file = {keyword: 1 - p_value
                                  for keyword, p_value in keywords_stat_file.items()}

        keywords_stat_file = {keyword: stat for keyword, stat in keywords_stat_file.items() if stat}

        # Fix zero frequencies
        for keyword, stat in keywords_stat_file.items():
            if stat == 0:
                keywords_stat_file[keyword] += 0.000000000000001
        
        word_cloud.generate_from_frequencies(keywords_stat_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        