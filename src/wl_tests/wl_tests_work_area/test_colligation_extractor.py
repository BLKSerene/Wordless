# ----------------------------------------------------------------------
# Wordless: Tests - Colligation Extractor
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

import random
import re

from wl_dialogs import wl_dialogs_misc
from wl_tests import wl_test_init

import wl_colligation_extractor

main = wl_test_init.Wl_Test_Main()

def test_colligation_extractor():
    print('Start testing module Colligation Extractor... ')

    tests_significance = list(main.settings_global['tests_significance']['collocation_extractor'].keys())
    measures_effect_size = list(main.settings_global['measures_effect_size']['collocation_extractor'].keys())
    len_diff = abs(len(tests_significance) - len(measures_effect_size))

    if len(tests_significance) > len(measures_effect_size):
        measures_effect_size += measures_effect_size * (len_diff // len(measures_effect_size)) + measures_effect_size[: len_diff % len(measures_effect_size)]
    elif len(measures_effect_size) > len(tests_significance):
        tests_significance += tests_significance * (len_diff // len(tests_significance)) + tests_significance[: len_diff % len(tests_significance)]

    files = main.settings_custom['file_area']['files_open']

    for i, (test_significance, measure_effect_size) in enumerate(zip(tests_significance, measures_effect_size)):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['colligation_extractor']['search_settings']['multi_search_mode'] = True
        main.settings_custom['colligation_extractor']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

        # Single file with search terms
        if i % 4 == 0:
            random.choice(files)['selected'] = True

            main.settings_custom['colligation_extractor']['search_settings']['search_settings'] = True
        # Single file without search terms
        elif i % 4 == 1:
            random.choice(files)['selected'] = True

            main.settings_custom['colligation_extractor']['search_settings']['search_settings'] = False
        # Multiple files with search terms
        elif i % 4 == 2:
            for file in files:
                file['selected'] = True

            main.settings_custom['colligation_extractor']['search_settings']['search_settings'] = True
        # Multiple files without search terms
        elif i % 4 == 3:
            for file in random.sample(files, 3):
                file['selected'] = True

            main.settings_custom['colligation_extractor']['search_settings']['search_settings'] = False

        files_selected = [
            re.search(r'(?<=\[)[a-z_]+(?=\])', file['name']).group()
            for file in files
            if file['selected']
        ]

        print(f"Files: {', '.join(files_selected)}")
        print(f"Search settings: {main.settings_custom['colligation_extractor']['search_settings']['search_settings']}")
        print(f'Test of Statistical significance: {test_significance}')
        print(f'Measure of effect size: {measure_effect_size}\n')

        wl_colligation_extractor.Wl_Worker_Colligation_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    main.app.quit()

    print('pass!')

def update_gui(err_msg, colligations_freqs_files, colligations_stats_files, nodes_text):
    assert not err_msg

    assert colligations_freqs_files
    assert colligations_stats_files
    assert nodes_text
    assert len(colligations_freqs_files) == len(colligations_stats_files)

    for (node, collocate), stats_files in colligations_stats_files.items():
        freqs_files = colligations_freqs_files[(node, collocate)]

        assert len(freqs_files) == len(stats_files) >= 1

        # Node
        assert node
        assert nodes_text[node]
        # Collocate
        assert collocate
        # Frequency (span positions)
        for freqs_file in freqs_files:
            assert len(freqs_file) == 10
        # Frequency (total)
        assert sum([sum(freqs_file) for freqs_file in freqs_files]) >= 0
        # p-value
        for _, p_value, _, _ in stats_files:
            assert 0 <= p_value <= 1
        # Number of Files Found
        assert len([freqs_file for freqs_file in freqs_files[:-1] if sum(freqs_file)]) >= 1

if __name__ == '__main__':
    test_colligation_extractor()
