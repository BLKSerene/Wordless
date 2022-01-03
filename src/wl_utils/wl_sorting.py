#
# Wordless: Utilities - Sorting
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

# Frequency
def sorted_tokens_freq_files(tokens_freq_files, sort_by_col = 0, reverse = False):
    def key(item):
        keys = []

        # Frequency
        for value in item[1]:
            keys.append(-value)

        keys.remove(-item[1][sort_by_col])

        if reverse:
            keys.insert(0, item[1][sort_by_col])
        else:
            keys.insert(0, -item[1][sort_by_col])

        # Tokens/N-grams
        keys.append(item[0])

        return keys

    return sorted(tokens_freq_files.items(), key = key)

def sorted_tokens_freq_files_ref(tokens_freq_files, sort_by_col = 0, reverse = False):
    def key(item):
        keys = []

        # Frequency in observed files
        for i, freq in enumerate(item[1]):
            if i > 0:
                keys.append(-freq)

        keys.remove(-item[1][sort_by_col])
        
        if reverse:
            keys.insert(0, item[1][sort_by_col])
        else:
            keys.insert(0, -item[1][sort_by_col])

        # Frequency in reference file
        keys.append(-item[1][0])

        # Tokens
        keys.append(item[0])

        return keys

    return sorted(tokens_freq_files.items(), key = key)

# Association
def sorted_collocations_stats_files(collocations_stats_files):
    def key(item):
        keys = []

        for stats_file in item[1]:
            # p-value
            keys.append(stats_file[1])
            # Test Statistic
            if stats_file[0]:
                keys.append(-stats_file[0])
            # Bayes Factor
            if stats_file[2]:
                keys.append(-stats_file[2])
            # Effect Size
            keys.append(-stats_file[3])

        # Collocates
        keys.append(item[0])

        return keys

    return sorted(collocations_stats_files.items(), key = key)

# Keyness
def sorted_keywords_stats_files(keywords_stats_files):
    def key(item):
        keys = []

        for stats_file in item[1]:
            # p-value
            keys.append(stats_file[1])
            # Test Statistic
            if stats_file[0]:
                keys.append(-stats_file[0])
            # Bayes Factor
            if stats_file[2]:
                keys.append(-stats_file[2])
            # Effect Size
            keys.append(-stats_file[3])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keywords_stats_files.items(), key = key)
