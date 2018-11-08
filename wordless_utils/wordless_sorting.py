#
# Wordless: Sorting
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

def sorted_freqs_files(freqs_files):
    def key_freqs_files(item):
        keys = []

        for value in item[1]:
            # Frequency
            keys.append(-value)

        # Tokens & N-grams
        keys.append(item[0])

        return keys

    return sorted(freqs_files.items(), key = key_freqs_files)

def sorted_freqs_file(freqs_files, i_file):
    def key_freqs_file(item):
        keys = []

        # Frequency
        keys.append(-item[1][i_file])

        # Tokens & N-grams
        keys.append(item[0])

        return keys

    return sorted(freqs_files.items(), key = key_freqs_file)

def sorted_scores_files(scores_files):
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

    return sorted(scores_files.items(), key = key_scores_files)

def sorted_scores_file(scores_files, i_file):
    def key_scores_file(item):
        keys = []

        # Score
        keys.append(-item[1][i_file])

        # Keywords
        keys.append(item[0][0])
        # Collocates
        keys.append(item[0][1])

        return keys

    return sorted(scores_files.items(), key = key_scores_file)

def sorted_scores_files_directions(scores_files_directions):
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

    return sorted(scores_files_directions.items(), key = key_scores_files_directions)

def sorted_keynesses_files(keynesses_files, sorting_order):
    def key_keynesses_files(item):
        keys = []

        for keyness in item[1]:
            # Keyness
            if sorting_order == 'ascending':
                keys.append(keyness)
            else:
                keys.append(-keyness)

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keynesses_files.items(), key = key_keynesses_files)

def sorted_keynesses_file(keynesses_files, i_file, sorting_order):
    def key_keynesses_file(item):
        keys = []

        # Keyness
        if sorting_order == 'ascending':
            keys.append(item[1][i_file])
        else:
            keys.append(-item[1][i_file])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keynesses_files.items(), key = key_keynesses_file)

def sorted_keynesses_files_stats(keynesses_files_stats):
    def key_keynesses_files_stats(item):
        keys = []

        for stats in item[1]:
            # p-value
            keys.append(stats[1])
            # Test Statistics
            keys.append(-stats[0])
            # Effect Size
            keys.append(-stats[2])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keynesses_files_stats.items(), key = key_keynesses_files_stats)
