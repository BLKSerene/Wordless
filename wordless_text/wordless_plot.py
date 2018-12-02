#
# Wordless: Plots
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtWidgets import *

import matplotlib.pyplot
import numpy
import wordcloud

from wordless_utils import wordless_sorting

def wordless_plot_freq(main, tokens_freq_files, plot_type,
                       use_file, use_pct, use_cumulative,
                       rank_min, rank_max,
                       label_x):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]

    if plot_type == main.tr('Line Chart'):
        tokens_freq_files = wordless_sorting.sorted_tokens_freq_files(tokens_freq_files)

        total_freqs = numpy.array(list(zip(*tokens_freq_files))[1]).sum(axis = 0)
        total_freq = sum(total_freqs)

        tokens = [item[0] for item in tokens_freq_files[rank_min - 1 : rank_max]]
        freqs = [item[1] for item in tokens_freq_files if item[0] in tokens]

        if use_pct:
            if use_cumulative:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Percentage Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Percentage Frequency'))
        else:
            if use_cumulative:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Frequency'))

        if use_cumulative:
            for i, freq_files in enumerate(freqs):
                if i >= 1:
                    freqs[i] = [freq_cumulative + freq
                                for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

        if use_pct:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs],
                                       label = file['name'])
        else:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs],
                                       label = file['name'])

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.title(main.tr('Frequency Distribution'))
        matplotlib.pyplot.grid(True)
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        for i, file in enumerate(files):
            if file['name'] == use_file:
                tokens_freq_files = wordless_sorting.sorted_tokens_freq_file(tokens_freq_files, i)

                tokens_freq_file = {token: freqs[i]
                                    for token, freqs in tokens_freq_files[rank_min - 1 : rank_max]}

                break

        tokens_freq_file = {token: freq for token, freq in tokens_freq_file.items() if freq}

        word_cloud.generate_from_frequencies(tokens_freq_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')

        matplotlib.pyplot.title(main.tr('Frequency Distribution'))
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()

def wordless_plot_freq_ref(main, tokens_freq_files, ref_file, plot_type,
                           use_file, use_pct, use_cumulative,
                           rank_min, rank_max,
                           label_x):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]

    if type(list(tokens_freq_files.keys())[0]) != str:
        tokens_ngram = True
    else:
        tokens_ngram = False

    if tokens_ngram:
        tokens_freq_files = {' '.join(ngram): freq_files for ngram, freq_files in tokens_freq_files.items()}

    if plot_type == main.tr('Line Chart'):
        tokens_freq_files = wordless_sorting.sorted_tokens_freq_files_ref(tokens_freq_files)

        total_freqs = numpy.array([item[1] for item in tokens_freq_files]).sum(axis = 0)
        total_freq_ref = total_freqs[0]
        total_freq_total = total_freqs[-1]

        tokens = [item[0] for item in tokens_freq_files[rank_min - 1 : rank_max]]
        freqs = [item[1] for item in tokens_freq_files if item[0] in tokens]

        if use_pct:
            if use_cumulative:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Percentage Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Percentage Frequency'))
        else:
            if use_cumulative:
                matplotlib.pyplot.ylabel(main.tr('Cumulative Frequency'))
            else:
                matplotlib.pyplot.ylabel(main.tr('Frequency'))

        if use_cumulative:
            for i, freq_files in enumerate(freqs):
                if i >= 1:
                    freqs[i] = [freq_cumulative + freq
                                for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

        if use_pct:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs],
                                       label = file['name'])
        else:
            for i, file in enumerate(files):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs],
                                       label = file['name'])

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.title(main.tr('Frequency Distribution'))
        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        files.remove(ref_file)

        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        for i, file in enumerate(files):
            if file['name'] == use_file:
                tokens_freq_files = wordless_sorting.sorted_tokens_freq_file(tokens_freq_files, i + 1)

                tokens_freq_file = {token: freq_files[i + 1]
                                    for token, freq_files in tokens_freq_files[rank_min - 1 : rank_max]}

                break

        tokens_freq_file = {token: freq for token, freq in tokens_freq_file.items() if freq}

        word_cloud.generate_from_frequencies(tokens_freq_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')

        matplotlib.pyplot.title(main.tr('Frequency Distribution'))
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()

def wordless_plot_stat(main, tokens_stat_files, plot_type,
                       use_file,
                       rank_min, rank_max,
                       label_x, label_y):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]

    if type(list(tokens_stat_files.keys())[0]) != str:
        tokens_ngram = True
    else:
        tokens_ngram = False

    if tokens_ngram:
        tokens_stat_files = {' '.join(ngram): stat_files for ngram, stat_files in tokens_stat_files.items()}

    if plot_type == main.tr('Line Chart'):
        if tokens_ngram:
            tokens_stat_files = wordless_sorting.sorted_ngrams_stat_files(tokens_stat_files)
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

        matplotlib.pyplot.title(main.tr('Scores'))
        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        for i, file in enumerate(files):
            if file['name'] == use_file:
                if tokens_ngram:
                    tokens_stat_files = wordless_sorting.sorted_ngrams_stat_file(tokens_stat_files, i)
                else:
                    tokens_stat_files = wordless_sorting.sorted_tokens_stat_file(tokens_stat_files, i)

                tokens_stat_file = {token: stat_files[i]
                                     for token, stat_files in tokens_stat_files[rank_min - 1 : rank_max]}

                break

        word_cloud.generate_from_frequencies(tokens_stat_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')

        matplotlib.pyplot.title(main.tr('Statistics'))
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()

def wordless_plot_keyness(main, keywords_stat_files, ref_file, plot_type,
                          use_file,
                          rank_min, rank_max,
                          label_y):
    files = main.wordless_files.get_selected_files()
    files += [{'name': main.tr('Total')}]
    files.remove(ref_file)

    if plot_type == main.tr('Line Chart'):
        if label_y == main.tr('p-value'):
            keywords_stat_files = wordless_sorting.sorted_keywords_stat_files(keywords_stat_files,
                                                                              sorting_order = 'ascending')
        else:
            keywords_stat_files = wordless_sorting.sorted_keywords_stat_files(keywords_stat_files,
                                                                              sorting_order = 'descending')

        keywords = [item[0] for item in keywords_stat_files[rank_min - 1 : rank_max]]
        stats = [item[1] for item in keywords_stat_files if item[0] in keywords]

        for i, file in enumerate(files):
            matplotlib.pyplot.plot([stats_files[i] for stats_files in stats],
                                   label = file['name'])

        matplotlib.pyplot.xlabel(main.tr('Keywords'))

        matplotlib.pyplot.ylabel(label_y)
        matplotlib.pyplot.xticks(range(len(keywords)), keywords, rotation = 90)

        matplotlib.pyplot.title(main.tr('Keyness'))
        matplotlib.pyplot.grid(True, color = 'silver')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        for i, file in enumerate(files):
            if file['name'] == use_file:
                if label_y == main.tr('p-value'):
                    keywords_stat_files = wordless_sorting.sorted_keywords_stat_file(keywords_stat_files, i,
                                                                                     sorting_order = 'ascending')
                else:
                    keywords_stat_files = wordless_sorting.sorted_keywords_stat_file(keywords_stat_files, i,
                                                                                     sorting_order = 'descending')

                keywords_stat_file = {keyword: stat_files[i]
                                      for keyword, stat_files in keywords_stat_files[rank_min - 1 : rank_max]}

                break

        if label_y == main.tr('p-value'):
            keywords_stat_file = {keyword: 1 - p_value
                                  for keyword, p_value in keywords_stat_file.items()}

        keywords_stat_file = {keyword: stat for keyword, stat in keywords_stat_file.items() if stat}

        word_cloud.generate_from_frequencies(keywords_stat_file)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')

        matplotlib.pyplot.title(main.tr('Keyness'))
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()
