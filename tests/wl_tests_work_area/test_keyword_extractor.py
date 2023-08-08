# ----------------------------------------------------------------------
# Wordless: Tests - Work Area - Keyword Extractor
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

import random
import re

from tests import wl_test_init
from wordless import wl_keyword_extractor
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

def test_keyword_extractor():
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

    len_tests_statistical_significance = len(tests_statistical_significance)
    len_measures_bayes_factor = len(measures_bayes_factor)
    len_measures_effect_size = len(measures_effect_size)
    len_max_measures = max([len_tests_statistical_significance, len_measures_bayes_factor, len_measures_effect_size])

    files_observed = main.settings_custom['file_area']['files_open']
    files_ref = main.settings_custom['file_area']['files_open_ref']

    i_multi_observed, i_multi_observed_ref = random.sample(range(len_max_measures), 2)

    for i in range(len_max_measures):
        for file in main.settings_custom['file_area']['files_open'] + main.settings_custom['file_area']['files_open_ref']:
            file['selected'] = False

        # Single reference file & multiple observed files
        if i == i_multi_observed:
            for file in random.sample(files_observed, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

            random.choice(files_ref)['selected'] = True
        # Multiple reference files & multiple observed files
        elif i == i_multi_observed_ref:
            for file in random.sample(files_observed, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

            for file in random.sample(files_ref, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation
        # Single reference file & single observed file
        elif i % 2 == 0:
            random.choice(files_observed)['selected'] = True
            random.choice(files_ref)['selected'] = True

        # Multiple reference files & single observed file
        elif i % 2 == 1:
            random.choice(files_observed)['selected'] = True

            for file in random.sample(files_ref, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

        file_names_observed = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]
        file_names_ref = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area_ref.get_selected_file_names()
        ]

        main.settings_custom['keyword_extractor']['generation_settings']['test_statistical_significance'] = tests_statistical_significance[i % len_tests_statistical_significance]
        main.settings_custom['keyword_extractor']['generation_settings']['measure_bayes_factor'] = measures_bayes_factor[i % len_measures_bayes_factor]
        main.settings_custom['keyword_extractor']['generation_settings']['measure_effect_size'] = measures_effect_size[i % len_measures_effect_size]

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
