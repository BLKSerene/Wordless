#
# Wordless: Sorting
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

def sorted_freqs_files(freqs):
    def key_freqs_files(item):
        keys = []

        for value in item[1]:
            # Frequency
            keys.append(-value)

        # Tokens & N-grams
        keys.append(item[0])

        return keys

    return sorted(freqs.items(), key = key_freqs_files)

def sorted_freqs_file(freqs, i_file):
    def key_freqs_file(item):
        keys = []

        # Frequency
        keys.append(-item[1][i_file])

        # Tokens & N-grams
        keys.append(item[0])

        return keys

    return sorted(freqs.items(), key = key_freqs_file)

def sorted_scores_files(scores):
    def key_scores_files(item):
        keys = []

        for score in item[1]:
            # Score
            keys.append(-score)

        # Keywords
        keys.append(item[0][0])
        # Collocates
        keys.append(item[0][1])

        return keys

    return sorted(scores.items(), key = key_scores_files)

def sorted_scores_file(scores, i_file):
    def key_scores_file(item):
        keys = []

        # Score
        keys.append(-item[1][i_file])

        # Keywords
        keys.append(item[0][0])
        # Collocates
        keys.append(item[0][1])

        return keys

    return sorted(scores.items(), key = key_scores_file)

def sorted_scores_files_directions(scores):
    def key_scores_files_directions(item):
        keys = []

        for scores in item[1]:
            # Score (Right)
            keys.append(-scores[1])
            # Score (Left)
            keys.append(-scores[0])

        # Keywords
        keys.append(item[0][0])
        # Collocates
        keys.append(item[0][1])

        return keys

    return sorted(scores.items(), key = key_scores_files_directions)

def sorted_keyness_files(keyness):
    def key_keyness_files(item):
        keys = []

        for stats in item[1]:
            # p-value
            keys.append(stats[1])
            # Test Statistics
            keys.append(stats[0])
            # Effect Size
            keys.append(stats[2])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keyness.items(), key = key_keyness_files)