# ----------------------------------------------------------------------
# Tests: Utilities - Sorting
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

from wordless.wl_utils import wl_sorting

def test_sorted_freq_files_items():
    freq_files_items = {
        'a': [10, 10],
        'b': [5, 5],
        'c': [5, 10]
    }
    freq_files_items_sorted_0 = [
        ('a', [10, 10]),
        ('c', [5, 10]),
        ('b', [5, 5])
    ]
    freq_files_items_sorted_1 = [
        ('b', [5, 5]),
        ('c', [5, 10]),
        ('a', [10, 10])
    ]

    assert wl_sorting.sorted_freq_files_items(freq_files_items, sort_by_col = 0, reverse = False) == freq_files_items_sorted_0
    assert wl_sorting.sorted_freq_files_items(freq_files_items, sort_by_col = 0, reverse = True) == freq_files_items_sorted_1

def test_sorted_freq_files_items_keyword_extractor():
    freq_files_items = {
        'a': [10, 10, 10],
        'b': [5, 5, 10],
        'c': [5, 10, 20]
    }
    freq_files_items_sorted_1 = [
        ('c', [5, 10, 20]),
        ('a', [10, 10, 10]),
        ('b', [5, 5, 10])
    ]
    freq_files_items_sorted_2 = [
        ('b', [5, 5, 10]),
        ('a', [10, 10, 10]),
        ('c', [5, 10, 20])
    ]

    assert wl_sorting.sorted_freq_files_items_keyword_extractor(freq_files_items, sort_by_col = 1, reverse = False) == freq_files_items_sorted_1
    assert wl_sorting.sorted_freq_files_items_keyword_extractor(freq_files_items, sort_by_col = 2, reverse = True) == freq_files_items_sorted_2

def test_sorted_stats_files_items():
    stats_files_items = {
        'a': [[10, .8, 10, 10], [10, .8, 10, 10]],
        'b': [[10, .8, 10, 10], [10, .6, 10, 10]],
        'c': [[10, .6, 10, 10], [10, .4, 10, 10]]
    }
    stats_files_items_sorted = [
        ('c', [[10, .6, 10, 10], [10, .4, 10, 10]]),
        ('b', [[10, .8, 10, 10], [10, .6, 10, 10]]),
        ('a', [[10, .8, 10, 10], [10, .8, 10, 10]])
    ]

    assert wl_sorting.sorted_stats_files_items(stats_files_items) == stats_files_items_sorted

if __name__ == '__main__':
    test_sorted_freq_files_items()
    test_sorted_freq_files_items_keyword_extractor()
    test_sorted_stats_files_items()
