#
# Wordless: Plots
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from matplotlib import pyplot

from wordless_utils import wordless_misc

def wordless_plot_freq(main, freq_distribution, rank_min, rank_max, use_pct, use_cumulative, label_x):
    total_freqs = [sum(freqs_file) for freqs_file in zip(*freq_distribution.values())]
    total_freq = sum(total_freqs)

    freq_distribution = sorted(freq_distribution.items(), key = wordless_misc.multi_sorting)

    tokens = [item[0] for item in freq_distribution[rank_min - 1 : rank_max - 1]]
    freqs = [item[1] for item in freq_distribution if item[0] in tokens]

    if use_pct:
        if use_cumulative:
            pyplot.ylabel(main.tr('Cumulative Percentage Frequency'))
        else:
            pyplot.ylabel(main.tr('Percentage Frequency'))
    else:
        if use_cumulative:
            pyplot.ylabel(main.tr('Cumulative Frequency'))
        else:
            pyplot.ylabel(main.tr('Frequency'))

    if use_cumulative:
        freq_files_cumulative = [0] * len(freq_distribution[0][1])

        for i, freq_files in enumerate(freqs):
            if i >= 1:
                freqs[i] = [freq_cumulative + freq for freq_cumulative, freq in zip(freqs[i - 1], freq_files)]

    if use_pct:
        for i, file in enumerate(main.wordless_files.get_selected_files()):
            pyplot.plot([freq_files[i] / total_freqs[i] * 100  for freq_files in freqs], label = file['name'])

        # Total Frequency
        pyplot.plot([sum(freq_files) / total_freq * 100 for freq_files in freqs], label = main.tr('Total'))
    else:
        for i, file in enumerate(main.wordless_files.get_selected_files()):
            pyplot.plot([freq_files[i] for freq_files in freqs], label = file['name'])

        # Total Frequency
        pyplot.plot([sum(freq_files) for freq_files in freqs], label = main.tr('Total'))

    pyplot.xlabel(label_x)
    pyplot.xticks(range(len(tokens)), tokens, rotation = 90)

    pyplot.grid(True, color = 'silver')

    pyplot.legend()
    pyplot.show()

def wordless_plot_score(main, score_distribution, rank_min, rank_max, label_x):
    score_distribution = sorted(score_distribution.items(), key = wordless_misc.multi_sorting)

    collocates = [item[0] for item in score_distribution[rank_min - 1 : rank_max - 1]]
    scores = [item[1] for item in score_distribution if item[0] in collocates]

    for i, file in enumerate(main.wordless_files.get_selected_files()):
        pyplot.plot([scores_files[i] for scores_files in scores], label = file['name'])

    # Total Score
    pyplot.plot([scores_files[-1] for scores_files in scores], label = main.tr('Total'))

    pyplot.xlabel(label_x)
    pyplot.ylabel(main.tr('Score'))
    pyplot.xticks(range(len(collocates)), [', '.join(collocate) for collocate in collocates], rotation = 90)

    pyplot.grid(True, color = 'silver')

    pyplot.legend()
    pyplot.show()

