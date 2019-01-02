#
# Wordless: Sorting
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

# Frequency
def sorted_tokens_freq_files(tokens_freq_files):
    def key(item):
        keys = []

        for value in item[1]:
            # Frequency
            keys.append(-value)

        # Tokens/N-grams
        keys.append(item[0])

        return keys

    return sorted(tokens_freq_files.items(), key = key)

def sorted_tokens_freq_file(tokens_freq_files, i_file):
    def key(item):
        keys = []

        # Frequency
        keys.append(-item[1][i_file])

        # Tokens/N-grams
        keys.append(item[0])

        return keys

    return sorted(tokens_freq_files.items(), key = key)

def sorted_tokens_freq_files_ref(tokens_freq_files):
    def key(item):
        keys = []

        # Frequency in observed files
        for i, freq in enumerate(item[1]):
            if i > 0:
                keys.append(-freq)

        # Frequency in reference file
        keys.append(-item[1][0])

        # Tokens
        keys.append(item[0])

        return keys

    return sorted(tokens_freq_files.items(), key = key)

# Statistic
def sorted_tokens_stat_files(tokens_stat_files):
    def key(item):
        keys = []

        # Statistic
        for stat in item[1]:
            keys.append(-stat)

        # Tokens/N-gram
        keys.append(item[0])

        return keys

    return sorted(tokens_stat_files.items(), key = key)

def sorted_tokens_stat_file(tokens_stat_files, i_file):
    def key(item):
        keys = []

        # Statistic
        keys.append(-item[1][i_file])

        # Token/N-gram
        keys.append(item[0])

        return keys

    return sorted(tokens_stat_files.items(), key = key)

# Association
def sorted_collocates_stats_files(collocates_stats_files):
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

    return sorted(collocates_stats_files.items(), key = key)

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
            # Dispersion
            keys.append(-stats_file[4])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keywords_stats_files.items(), key = key)

def sorted_keywords_stat_files(keywords_stat_files):
    def key(item):
        keys = []

        # Statistic
        for stat in item[1]:
            keys.append(-stat)

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keywords_stat_files.items(), key = key)

def sorted_keywords_stat_file(keywords_stat_files, i_file):
    def key(item):
        keys = []

        # Statistic
        keys.append(-item[1][i_file])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(keywords_stat_files.items(), key = key)
