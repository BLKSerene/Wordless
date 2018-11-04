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

from wordless_utils import wordless_misc

def wordless_plot_freq(main, freq_distribution, plot_type,
                       use_data_file, use_pct, use_cumulative,
                       rank_min, rank_max,
                       label_x):
    freq_distribution = sorted(freq_distribution.items(), key = wordless_misc.multi_sorting_freqs)

    if type(freq_distribution[0][0]) != str:
        freq_distribution = [(', '.join(ngram), freqs) for ngram, freqs in freq_distribution]

    if plot_type == main.tr('Line Chart'):
        total_freqs = numpy.array(list(zip(*freq_distribution))[1]).sum(axis = 0)
        total_freq = sum(total_freqs)

        tokens = [item[0] for item in freq_distribution[rank_min - 1 : rank_max]]
        freqs = [item[1] for item in freq_distribution if item[0] in tokens]

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
            freq_files_cumulative = [0] * len(freq_distribution[0][1])

            for i, freq_files in enumerate(freqs):
                if i >= 1:
                    freqs[i] = [freq_cumulative + freq for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

        if use_pct:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                matplotlib.pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs], label = file['name'])

            # Total Frequency
            matplotlib.pyplot.plot([sum(freq_files) / total_freq * 100 for freq_files in freqs], label = main.tr('Total'))
        else:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                matplotlib.pyplot.plot([freq_files[i] for freq_files in freqs], label = file['name'])

            # Total Frequency
            matplotlib.pyplot.plot([sum(freq_files) for freq_files in freqs], label = main.tr('Total'))

        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

        matplotlib.pyplot.grid(True, color = 'silver')

        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()
    elif plot_type == main.tr('Word Cloud'):
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width(), height = QDesktopWidget().height(),
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        if use_data_file == main.tr('Total'):
            freq_distribution = {token: sum(freqs)
                                 for token, freqs in freq_distribution[rank_min - 1 : rank_max]}
        else:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                if file['name'] == use_data_file:
                    freq_distribution = {token: freqs[i]
                                         for token, freqs in freq_distribution[rank_min - 1 : rank_max]}

                    break

        freq_distribution = {token: freq for token, freq in freq_distribution.items() if freq}

        word_cloud.generate_from_frequencies(freq_distribution)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()

def wordless_plot_score(main, score_distribution, plot_type,
                        use_data_file,
                        rank_min, rank_max, label_x):
    score_distribution = sorted(score_distribution.items(), key = wordless_misc.multi_sorting_scores)
    score_distribution = [(', '.join(collocate), scores) for collocate, scores in score_distribution]

    if plot_type == main.tr('Line Chart'):
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
        word_cloud = wordcloud.WordCloud(width = QDesktopWidget().width()- 100, height = QDesktopWidget().height() - 150,
                                         background_color = 'white',
                                         max_words = rank_max - rank_min + 1)

        if use_data_file == main.tr('Total'):
            score_distribution = {collocate: scores[-1]
                                 for collocate, scores in score_distribution[rank_min - 1 : rank_max]}
        else:
            for i, file in enumerate(main.wordless_files.get_selected_files()):
                if file['name'] == use_data_file:
                    score_distribution = {collocate: scores[i]
                                         for collocate, scores in score_distribution[rank_min - 1 : rank_max]}

                    break

        score_distribution = {collocate: score for collocate, score in score_distribution.items() if score}

        word_cloud.generate_from_frequencies(score_distribution)

        matplotlib.pyplot.imshow(word_cloud, interpolation = 'bilinear')
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()
