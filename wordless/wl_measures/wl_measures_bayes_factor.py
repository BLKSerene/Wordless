# ----------------------------------------------------------------------
# Wordless: Measures - Bayes factor
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

import numpy

from wordless.wl_measures import wl_measures_statistical_significance, wl_measure_utils

# Log-likelihood ratio test
# Reference: Wilson, A. (2013). Embracing Bayes factors for key item analysis in corpus linguistics. In M. Bieswanger & A. Koll-Stobbe (Eds.), New approaches to the study of linguistic variability (pp. 3–11). Peter Lang.
def bayes_factor_log_likelihood_ratio_test(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s

    # Modify settings temporarily
    settings_backup = main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test'].copy()
    main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test'] = main.settings_custom['measures']['bayes_factor']['log_likelihood_ratio_test'].copy()

    gs, _ = wl_measures_statistical_significance.log_likelihood_ratio_test(main, o11s, o12s, o21s, o22s)
    bics = gs - wl_measure_utils.numpy_log(oxxs)

    # Restore settings
    main.settings_custom['measures']['statistical_significance']['log_likelihood_ratio_test'] = settings_backup.copy()

    return bics

# Student's t-test (2-sample)
# Reference: Wilson, A. (2013). Embracing Bayes factors for key item analysis in corpus linguistics. In M. Bieswanger & A. Koll-Stobbe (Eds.), New approaches to the study of linguistic variability (pp. 3–11). Peter Lang.
def bayes_factor_students_t_test_2_sample(main, freqs_x1s, freqs_x2s):

    # Modify settings temporarily
    settings_backup = main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample'].copy()
    main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample'] = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample'].copy()

    t_stats, _ = wl_measures_statistical_significance.students_t_test_2_sample(main, freqs_x1s, freqs_x2s)
    num_sub_sections = main.settings_custom['measures']['bayes_factor']['students_t_test_2_sample']['num_sub_sections']
    bics = t_stats ** 2 - numpy.log(2 * num_sub_sections)

    # Restore settings
    main.settings_custom['measures']['statistical_significance']['students_t_test_2_sample'] = settings_backup.copy()

    return numpy.where(bics >= 0, bics, 0)
