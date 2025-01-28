# ----------------------------------------------------------------------
# Wordless: Measures - Measure Utilities
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

import collections

import numpy
from PyQt5.QtCore import QCoreApplication

from wordless.wl_nlp import wl_nlp_utils

_tr = QCoreApplication.translate

def to_measure_code(main, measure_type, measure_text):
    return main.settings_global['mapping_measures'][measure_type][measure_text]

def to_measure_text(main, measure_type, measure_code):
    for text, code in main.settings_global['mapping_measures'][measure_type].items():
        if code == measure_code:
            return text

    return None

def to_freqs_sections_1_sample(items_to_search, items, num_sub_sections):
    freq_sections_items = {}

    freq_items_sections = [
        collections.Counter(section)
        for section in wl_nlp_utils.to_sections(items, num_sub_sections)
    ]

    for item in items_to_search:
        freq_sections_items[item] = [
            freq_tokens.get(item, 0)
            for freq_tokens in freq_items_sections
        ]

    return freq_sections_items

def to_freqs_sections_dispersion(main, items_to_search, items):
    num_sub_sections = main.settings_custom['measures']['dispersion']['general_settings']['num_sub_sections']

    return to_freqs_sections_1_sample(items_to_search, items, num_sub_sections)

def to_freqs_sections_adjusted_freq(main, items_to_search, items):
    num_sub_sections = main.settings_custom['measures']['adjusted_freq']['general_settings']['num_sub_sections']

    return to_freqs_sections_1_sample(items_to_search, items, num_sub_sections)

def to_freqs_sections_2_sample(items_to_search, items_x1, items_x2, num_sub_sections, use_data):
    freq_sections_items = {}

    sections_x1 = wl_nlp_utils.to_sections(items_x1, num_sub_sections)
    sections_x2 = wl_nlp_utils.to_sections(items_x2, num_sub_sections)

    freq_items_sections_x1 = [collections.Counter(section) for section in sections_x1]
    freq_items_sections_x2 = [collections.Counter(section) for section in sections_x2]

    if use_data == _tr('wl_measure_utils', 'Absolute frequency'):
        for item in items_to_search:
            freqs_x1 = [
                freq_items.get(item, 0)
                for freq_items in freq_items_sections_x1
            ]
            freqs_x2 = [
                freq_items.get(item, 0)
                for freq_items in freq_items_sections_x2
            ]

            freq_sections_items[item] = (freqs_x1, freqs_x2)
    elif use_data == _tr('wl_measure_utils', 'Relative frequency'):
        len_sections_x1 = [len(section) for section in sections_x1]
        len_sections_x2 = [len(section) for section in sections_x2]

        for item in items_to_search:
            freqs_x1 = [
                freq_items.get(item, 0) / len_section
                for freq_items, len_section in zip(freq_items_sections_x1, len_sections_x1)
            ]
            freqs_x2 = [
                freq_items.get(item, 0) / len_section
                for freq_items, len_section in zip(freq_items_sections_x2, len_sections_x2)
            ]

            freq_sections_items[item] = (freqs_x1, freqs_x2)

    return freq_sections_items

def to_freqs_sections_statistical_significance(main, items_to_search, items_x1, items_x2, test_statistical_significance):
    if test_statistical_significance == 'mann_whitney_u_test':
        num_sub_sections = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['num_sub_sections']
        use_data = main.settings_custom['measures']['statistical_significance']['mann_whitney_u_test']['use_data']
    elif test_statistical_significance == 'students_t_test_2_sample':
        num_sub_sections = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['num_sub_sections']
        use_data = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample']['use_data']

    return to_freqs_sections_2_sample(items_to_search, items_x1, items_x2, num_sub_sections, use_data)

def to_freqs_sections_bayes_factor(main, items_to_search, items_x1, items_x2, measure_bayes_factor):
    if measure_bayes_factor == 'students_t_test_2_sample':
        num_sub_sections = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['num_sub_sections']
        use_data = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['use_data']

    return to_freqs_sections_2_sample(items_to_search, items_x1, items_x2, num_sub_sections, use_data)

def numpy_divide(a, b, default = 0):
    if default:
        return numpy.divide(a, b, out = numpy.full_like(b, default, dtype = float), where = b > 0)
    else:
        return numpy.divide(a, b, out = numpy.zeros_like(b, dtype = float), where = b > 0)

def numpy_log(a, default = 0):
    if default:
        return numpy.log(a, out = numpy.full_like(a, default, dtype = float), where = a > 0)
    else:
        return numpy.log(a, out = numpy.zeros_like(a, dtype = float), where = a > 0)

def numpy_log2(a, default = 0):
    if default:
        return numpy.log2(a, out = numpy.full_like(a, default, dtype = float), where = a > 0)
    else:
        return numpy.log2(a, out = numpy.zeros_like(a, dtype = float), where = a > 0)

def numpy_log10(a, default = 0):
    if default:
        return numpy.log10(a, out = numpy.full_like(a, default, dtype = float), where = a > 0)
    else:
        return numpy.log10(a, out = numpy.zeros_like(a, dtype = float), where = a > 0)
