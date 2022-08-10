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

import numpy
from PyQt5.QtCore import QCoreApplication

from wl_measures import wl_measures_statistical_significance

_tr = QCoreApplication.translate

def to_freq_sections_items(main, items_search, items_x1, items_x2, measure_bayes_factor):
    if measure_bayes_factor == _tr('wl_measures_bayes_factor', "Student's t-test (2-sample)"):
        num_sub_sections = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['num_sub_sections']
        use_data = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['use_data']

    return wl_measures_statistical_significance._to_freq_sections_items(main, items_search, items_x1, items_x2, num_sub_sections, use_data)

# Log-likelihood Ratio
# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang.
def bayes_factor_log_likelihood_ratio_test(main, c11, c12, c21, c22):
    cxx = c11 + c12 + c21 + c22

    log_likelihood_ratio = wl_measures_statistical_significance.log_likelihood_ratio_test(main, c11, c12, c21, c22)[0]
    bic = log_likelihood_ratio - numpy.log(cxx) if cxx else 0

    return bic

# Student's t-test (2-sample)
# Reference: Wilson, A. (2013). Embracing Bayes Factors for key item analysis in corpus linguistics. In M. Bieswanger, & A. Koll-Stobbe (Eds.), New Approaches to the Study of Linguistic Variability (pp. 3–11). Peter Lang.
def bayes_factor_students_t_test_2_sample(main, freqs_x1, freqs_x2):
    if any(freqs_x1) or any(freqs_x2):
        t_stat = wl_measures_statistical_significance.students_t_test_2_sample(main, freqs_x1, freqs_x2)[0]
        bic = t_stat ** 2 - numpy.log(2 * main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['num_sub_sections'])
    else:
        bic = 0

    return bic
