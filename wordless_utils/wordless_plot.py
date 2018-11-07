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

def wordless_plot_freq(main, freqs_files, plot_type,
                       use_data_file, use_pct, use_cumulative,
                       rank_min, rank_max,
                       label_x,):
    if type(list(freqs_files.keys())[0]) != str:
        freqs_files = {' '.join(ngram): freqs for ngram, freqs in freqs_files.items()}

    if plot_type == main.tr('Line Chart'):
        freqs_files = wordless_sorting.sorted_freqs_files(freqs_files)

        total_freqs = numpy.array(list(zip(*freqs_files))[1]).sum(axis = 0)
        total_freq = sum(total_freqs)

        tokens = [item[0] for item in freqs_files[rank_min - 1 : rank_max]]
        freqs = [item[1] for item in freqs_files if item[0] in tokens]

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
                    freqs[i] = [freq_cumulative + freq for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

        if use_pct:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs],
                                       label = file['name'])

            # Total Frequency
            matplotlib.pyplot.plot([sum(freq_files) / total_freq * 100 for freq_files in freqs],
                                   label = main.tr('Total'))
        else:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs],
                                       label = file['name'])

            # Total Frequency
            matplotlib.pyplot.plot([sum(freq_files) for freq_files in freqs],
                                   label = main.tr('Total'))

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.grid(True, color = 'silver')

        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        freqs_files = {token: freqs + [sum(freqs)]
                       for token, freqs in freqs_files.items()}

        if use_data_file == main.tr('Total'):
            freqs_files = wordless_sorting.sorted_freqs_file(freqs_files, -1)

            freqs_files = {token: sum(freqs)
                           for token, freqs in freqs_files[rank_min - 1 : rank_max]}
        else:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                if file['name'] == use_data_file:
                    freqs_files = wordless_sorting.sorted_freqs_file(freqs_files, i)

                    freqs_files = {token: freqs[i]
                                   for token, freqs in freqs_files[rank_min - 1 : rank_max]}

                    break

        freqs_files = {token: freq for token, freq in freqs_files.items() if freq}

        word_cloud.generate_from_frequencies(freqs_files)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()

def wordless_plot_freqs_ref(main, freqs_files, ref_file, plot_type,
                            use_data_file, use_pct, use_cumulative,
                            rank_min, rank_max,
                            label_x):
    files_selected = main.wordless_files.get_selected_files()

    for file in files_selected:
        if file['name'] == ref_file['name']:
            files_selected.remove(ref_file)

            break

    if type(list(freqs_files.keys())[0]) != str:
        freqs_files = {' '.join(ngram): freqs for ngram, freqs in freqs_files.items()}

    if plot_type == main.tr('Line Chart'):
        freqs_files = wordless_sorting.sorted_freqs_files(freqs_files)

        total_freqs = numpy.array([item[1] for item in freqs_files]).sum(axis = 0)
        total_freq_total = total_freqs[-2]
        total_freq_ref = total_freqs[-1]

        tokens = [item[0] for item in freqs_files[rank_min - 1 : rank_max]]
        freqs_observed = [item[1][:-2] for item in freqs_files if item[0] in tokens]
        freqs_total = [item[1][-2] for item in freqs_files if item[0] in tokens]
        freqs_ref = [item[1][-1] for item in freqs_files if item[0] in tokens]

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
            for i, freq_files in enumerate(freqs_observed):
                if i >= 1:
                    freqs_observed[i] = [freq_cumulative + freq for freq_cumulative, freq in zip(freqs_observed[i - 1], freq_files)]

            for i, freq_total in enumerate(freqs_total):
                if i >= 1:
                    freqs_total[i] = freqs_total[i - 1] + freq_total

            for i, freq_ref in enumerate(freqs_ref):
                if i >= 1:
                    freqs_ref[i] = freqs_ref[i - 1] + freq_ref

        if use_pct:
            for i, file in enumerate(files_selected):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs_observed],
                                       label = file['name'])

            # Total Frequency
            matplotlib.pyplot.plot([freq / total_freq_total * 100 for freq in freqs_total],
                                   label = main.tr('Total'))

            # Reference Frequency
            matplotlib.pyplot.plot([freq / total_freq_ref * 100 for freq in freqs_ref],
                                   label = ref_file['name'])
        else:
            for i, file in enumerate(files_selected):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs_observed],
                                       label = file['name'])

            # Total Frequency
            matplotlib.pyplot.plot([freq for freq in freqs_total],
                                   label = main.tr('Total'))

            # Reference Frequency
            matplotlib.pyplot.plot([freq for freq in freqs_ref],
                                   label = ref_file['name'])

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.grid(True, color = 'silver')

        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        if use_data_file == main.tr('Total'):
            freqs_files = wordless_sorting.sorted_freqs_file(freqs_files, -2)

            freqs_files = {token: freq_files[-2]
                           for token, freq_files in freqs_files[rank_min - 1 : rank_max]}
        else:
            for i, file in enumerate(files_selected):
                if file['name'] == use_data_file:
                    freqs_files = wordless_sorting.sorted_freqs_file(freqs_files, i)

                    freqs_files = {token: freq_files[i]
                                   for token, freq_files in freqs_files[rank_min - 1 : rank_max]}

                    break

        freqs_files = {token: freq for token, freq in freqs_files.items() if freq}

        word_cloud.generate_from_frequencies(freqs_files)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()

def wordless_plot_score(main, score_distribution, plot_type,
                        use_data_file,
                        rank_min, rank_max, label_x):
    score_distribution = {' '.join(collocate): scores for collocate, scores in score_distribution.items()}

    if plot_type == main.tr('Line Chart'):
        score_distribution = wordless_sorting.sorted_scores_files(score_distribution)

        collocates = [item[0] for item in score_distribution[rank_min - 1 : rank_max]]
        scores = [item[1] for item in score_distribution if item[0] in collocates]

        for i, file in enumerate(main.wordless_files.get_selected_files()):
            matplotlib.pyplot.plot([scores_files[i] for scores_files in scores], label = file['name'])

        # Total Score
        matplotlib.pyplot.plot([scores_files[-1] for scores_files in scores], label = main.tr('Total'))

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.ylabel(main.tr('Score'))
        matplotlib.pyplot.xticks(range(len(collocates)), collocates, rotation = 90)

        matplotlib.pyplot.grid(True, color = 'silver')

        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(),
                                         height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        if use_data_file == main.tr('Total'):
            score_distribution = wordless_sorting.sorted_scores_file(score_distribution, -1)

            score_distribution = {collocate: scores[-1]
                                 for collocate, scores in score_distribution[rank_min - 1 : rank_max]}
        else:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                if file['name'] == use_data_file:
                    score_distribution = wordless_sorting.sorted_scores_file(score_distribution, i)

                    score_distribution = {collocate: scores[i]
                                          for collocate, scores in score_distribution[rank_min - 1 : rank_max]}

                    break

        score_distribution = {collocate: score for collocate, score in score_distribution.items() if score}

        word_cloud.generate_from_frequencies(score_distribution)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()
