# ----------------------------------------------------------------------
# Wordless: Tests - Work area - Collocation Extractor
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

import itertools
import re

from tests import wl_test_init
from wordless import wl_collocation_extractor
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

main.settings_custom['collocation_extractor']['search_settings']['multi_search_mode'] = True
main.settings_custom['collocation_extractor']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

def test_collocation_extractor():
    # Do not test Fisher's exact test since it is too computationally expensive
    tests_statistical_significance = [
        test_statistical_significance
        for test_statistical_significance, vals in main.settings_global['tests_statistical_significance'].items()
        if vals['collocation_extractor'] and test_statistical_significance != 'fishers_exact_test'
    ]
    measures_bayes_factor = [
        measure_bayes_factor
        for measure_bayes_factor, vals in main.settings_global['measures_bayes_factor'].items()
        if vals['collocation_extractor']
    ]
    measures_effect_size = list(main.settings_global['measures_effect_size'].keys())

    for i, (test_statistical_significance, measure_bayes_factor, measure_effect_size) in enumerate(itertools.zip_longest(
        tests_statistical_significance,
        measures_bayes_factor,
        measures_effect_size,
        fillvalue = 'none'
    )):
        # Single file
        if i % 3 in [0, 2]:
            wl_test_init.select_random_files(main, num_files = 1)
        # Multiple files
        elif i % 3 == 1:
            wl_test_init.select_random_files(main, num_files = 2)

        files_selected = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        main.settings_custom['collocation_extractor']['generation_settings']['test_statistical_significance'] = test_statistical_significance
        main.settings_custom['collocation_extractor']['generation_settings']['measure_bayes_factor'] = measure_bayes_factor
        main.settings_custom['collocation_extractor']['generation_settings']['measure_effect_size'] = measure_effect_size

        print(f"Files: {' | '.join(files_selected)}")
        print(f"Test of statistical significance: {main.settings_custom['collocation_extractor']['generation_settings']['test_statistical_significance']}")
        print(f"Measure of Bayes factor: {main.settings_custom['collocation_extractor']['generation_settings']['measure_bayes_factor']}")
        print(f"Measure of effect size: {main.settings_custom['collocation_extractor']['generation_settings']['measure_effect_size']}")

        wl_collocation_extractor.Wl_Worker_Collocation_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    main.app.quit()

def update_gui(err_msg, collocations_freqs_files, collocations_stats_files):
    print(err_msg)
    assert not err_msg

    assert collocations_freqs_files
    assert collocations_stats_files
    assert len(collocations_freqs_files) == len(collocations_stats_files)

    for (node, collocate), stats_files in collocations_stats_files.items():
        freqs_files = collocations_freqs_files[(node, collocate)]

        assert len(freqs_files) == len(stats_files) >= 1

        # Node
        assert node
        # Collocate
        assert collocate
        # Frequency (span positions)
        for freqs_file in freqs_files:
            assert len(freqs_file) == 10
        # Frequency (total)
        assert sum((sum(freqs_file) for freqs_file in freqs_files)) >= 0
        # p-value
        for _, p_value, _, _ in stats_files:
            assert p_value is None or 0 <= p_value <= 1
        # Number of Files Found
        assert len([freqs_file for freqs_file in freqs_files[:-1] if sum(freqs_file)]) >= 1

if __name__ == '__main__':
    test_collocation_extractor()
