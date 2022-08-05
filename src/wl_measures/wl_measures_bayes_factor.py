# ----------------------------------------------------------------------
# Wordless: Measures - Bayes Factor
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import collections

import numpy
from PyQt5.QtCore import QCoreApplication

from wl_measures import wl_measures_statistical_significance
from wl_nlp import wl_nlp_utils

_tr = QCoreApplication.translate

def to_freqs_sections_tokens(main, tokens, tokens_x1, tokens_x2, measure_bayes_factor):
    freqs_sections_tokens = {}

    if measure_bayes_factor == _tr('wl_measures_bayes_factor', "Student's t-test (2-sample)"):
        num_sections = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['num_sections']
        use_data = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['use_data']

    sections_x1 = wl_nlp_utils.to_sections(tokens_x1, num_sections)
    sections_x2 = wl_nlp_utils.to_sections(tokens_x2, num_sections)

    sections_freqs_x1 = [collections.Counter(section) for section in sections_x1]
    sections_freqs_x2 = [collections.Counter(section) for section in sections_x2]

    if use_data == _tr('wl_measures_bayes_factor', 'Absolute Frequency'):
        for token in tokens:
            freqs_x1 = [
                section_freqs.get(token, 0)
                for section_freqs in sections_freqs_x1
            ]
            freqs_x2 = [
                section_freqs.get(token, 0)
                for section_freqs in sections_freqs_x2
            ]

            freqs_sections_tokens[token] = (freqs_x1, freqs_x2)
    elif use_data == _tr('wl_measures_bayes_factor', 'Relative Frequency'):
        len_sections_x1 = [len(section) for section in sections_x1]
        len_sections_x2 = [len(section) for section in sections_x2]

        for token in tokens:
            freqs_x1 = [
                section_freqs.get(token, 0) / len_section
                for section_freqs, len_section in zip(sections_freqs_x1, len_sections_x1)
            ]
            freqs_x2 = [
                section_freqs.get(token, 0) / len_section
                for section_freqs, len_section in zip(sections_freqs_x2, len_sections_x2)
            ]

            freqs_sections_tokens[token] = (freqs_x1, freqs_x2)

    return freqs_sections_tokens

# Log-likelihood Ratio
# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang.
def bayes_factor_log_likelihood_ratio_test(main, c11, c12, c21, c22):
    log_likelihood_ratio = wl_measures_statistical_significance.log_likelihood_ratio_test(main, c11, c12, c21, c22)[0]
    bic = log_likelihood_ratio - numpy.log(c11 + c12 + c21 + c22)

    return bic

# Student's t-test (2-sample)
# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang.
def bayes_factor_students_t_test_2_sample(main, counts_x1, counts_x2):
    t_stat = wl_measures_statistical_significance.students_t_test_2_sample(main, counts_x1, counts_x2)[0]
    bic = t_stat ** 2 - numpy.log(2 * main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['num_sections'])

    return bic
