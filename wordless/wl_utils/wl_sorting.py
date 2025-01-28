# ----------------------------------------------------------------------
# Wordless: Utilities - Sorting
# Copyright (C) 2018-2025  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

# Frequency
def sorted_freq_files_items(freq_files_items, sort_by_col = 0, reverse = False):
    def key(item):
        if reverse:
            # Frequency
            keys = list(item[1])

            keys.remove(item[1][sort_by_col])
            keys.insert(0, item[1][sort_by_col])
        else:
            keys = [-freq for freq in item[1]]

            keys.remove(-item[1][sort_by_col])
            keys.insert(0, -item[1][sort_by_col])

        # Tokens/N-grams
        keys.append(item[0])

        return keys

    return sorted(freq_files_items.items(), key = key)

def sorted_freq_files_items_keyword_extractor(freq_files_items, sort_by_col = 0, reverse = False):
    def key(item):
        if reverse:
            # Frequency in observed files
            keys = list(item[1][1:])

            keys.remove(item[1][sort_by_col])
            keys.insert(0, item[1][sort_by_col])

            # Frequency in reference file
            keys.append(item[1][0])
        else:
            # Frequency in observed files
            keys = [-freq for freq in item[1][1:]]

            keys.remove(-item[1][sort_by_col])
            keys.insert(0, -item[1][sort_by_col])

            # Frequency in reference file
            keys.append(-item[1][0])

        # Keywords
        keys.append(item[0])

        return keys

    return sorted(freq_files_items.items(), key = key)

# Statistics
def sorted_stats_files_items(stats_files_items):
    def key(item):
        keys = []

        # p-value
        keys.extend([stats[1] for stats in item[1] if stats[1] is not None])

        # Test Statistic
        if item[1][0]:
            keys.extend([-stats[0] for stats in item[1] if stats[0] is not None])

        # Bayes Factor
        keys.extend([-stats[2] for stats in item[1] if stats[2] is not None])
        # Effect Size
        keys.extend([-stats[3] for stats in item[1] if stats[3] is not None])

        # Collocates/Keywords
        keys.append(item[0])

        return keys

    return sorted(stats_files_items.items(), key = key)
