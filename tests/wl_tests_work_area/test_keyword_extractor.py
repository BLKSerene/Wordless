# ----------------------------------------------------------------------
# Wordless: Tests - Work area - Keyword Extractor
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

# pylint: disable=unsupported-assignment-operation

import itertools
import re

from tests import wl_test_init
from wordless import wl_keyword_extractor
from wordless.wl_dialogs import wl_dialogs_misc

def test_keyword_extractor():
    main = wl_test_init.Wl_Test_Main()

    # Do not test Fisher's exact test since it is too computationally expensive
    tests_statistical_significance = [
        test_statistical_significance
        for test_statistical_significance, vals in main.settings_global['tests_statistical_significance'].items()
        if vals['keyword_extractor'] and test_statistical_significance != 'fishers_exact_test'
    ]
    measures_bayes_factor = [
        measure_bayes_factor
        for measure_bayes_factor, vals in main.settings_global['measures_bayes_factor'].items()
        if vals['keyword_extractor']
    ]
    measures_effect_size = list(main.settings_global['measures_effect_size'].keys())

    for i, (test_statistical_significance, measure_bayes_factor, measure_effect_size) in enumerate(itertools.zip_longest(
        tests_statistical_significance,
        measures_bayes_factor,
        measures_effect_size,
        fillvalue = 'none'
    )):
        # Single observed file & single reference file
        if i % 10 in [0, 3, 6, 9]:
            wl_test_init.select_random_files(main, num_files = 1)
            wl_test_init.select_random_files_ref(main, num_files = 1)
        # Single observed file & multiple reference files
        elif i % 10 in [1, 4, 7]:
            wl_test_init.select_random_files(main, num_files = 1)
            wl_test_init.select_random_files_ref(main, num_files = 2)
        # Multiple observed files & single reference file
        if i % 10 in [2, 5]:
            wl_test_init.select_random_files(main, num_files = 2)
            wl_test_init.select_random_files_ref(main, num_files = 1)
        # Multiple observed files & multiple reference files
        elif i % 10 == 8:
            wl_test_init.select_random_files(main, num_files = 2)
            wl_test_init.select_random_files_ref(main, num_files = 2)

        file_names_observed = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]
        file_names_ref = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area_ref.get_selected_file_names()
        ]

        main.settings_custom['keyword_extractor']['generation_settings']['test_statistical_significance'] = test_statistical_significance
        main.settings_custom['keyword_extractor']['generation_settings']['measure_bayes_factor'] = measure_bayes_factor
        main.settings_custom['keyword_extractor']['generation_settings']['measure_effect_size'] = measure_effect_size

        print(f"Observed files: {' | '.join(file_names_observed)}")
        print(f"Reference files: {' | '.join(file_names_ref)}")
        print(f"Test of statistical significance: {main.settings_custom['keyword_extractor']['generation_settings']['test_statistical_significance']}")
        print(f"Measure of Bayes factor: {main.settings_custom['keyword_extractor']['generation_settings']['measure_bayes_factor']}")
        print(f"Measure of effect size: {main.settings_custom['keyword_extractor']['generation_settings']['measure_effect_size']}")

        wl_keyword_extractor.Wl_Worker_Keyword_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    main.app.quit()

def update_gui(err_msg, keywords_freq_files, keywords_stats_files):
    print(err_msg)
    assert not err_msg

    assert keywords_freq_files
    assert keywords_stats_files
    assert len(keywords_freq_files) == len(keywords_stats_files)

    for keyword, stats_files in keywords_stats_files.items():
        freq_files = keywords_freq_files[keyword]

        assert len(freq_files) == len(stats_files) + 1 >= 1

        # Keyword
        assert keyword
        # Frequency (observed files)
        assert any((freq_file for freq_file in freq_files[1:-1]))
        # Frequency (total)
        assert freq_files[-1]
        assert freq_files[-1] == sum(freq_files[1:-1])
        # p-value
        for _, p_value, _, _ in stats_files:
            assert p_value is None or 0 <= p_value <= 1
        # Number of Files Found
        assert len([freq for freq in freq_files[1:-1] if freq]) >= 1

if __name__ == '__main__':
    test_keyword_extractor()
