# ----------------------------------------------------------------------
# Tests: Work Area - Colligation Extractor
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

import glob
import random

from tests import wl_test_init
from wordless import wl_colligation_extractor
from wordless.wl_dialogs import wl_dialogs_misc

main_global = None

def test_colligation_extractor():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['colligation_extractor']

    settings['search_settings']['multi_search_mode'] = True
    settings['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

    tests_statistical_significance = [
        test_statistical_significance
        for test_statistical_significance, vals in main.settings_global['tests_statistical_significance'].items()
        if vals['collocation']
    ]
    measures_bayes_factor = [
        measure_bayes_factor
        for measure_bayes_factor, vals in main.settings_global['measures_bayes_factor'].items()
        if vals['collocation']
    ]
    measures_effect_size = list(main.settings_global['measures_effect_size'].keys())

    for i in range(2 + len(glob.glob('tests/files/file_area/misc/*.txt'))):
        match i:
            # Single file
            case 0:
                wl_test_init.select_test_files(main, no_files = [0])
            # Multiple files
            case 1:
                wl_test_init.select_test_files(main, no_files = [1, 2])
            # Miscellaneous
            case _:
                # Excluding files without POS tagging support and tagged files without POS tags
                if (
                    main.settings_custom['file_area']['files_open'][i + 1]['lang'] == 'eng_us'
                    and main.settings_custom['file_area']['files_open'][i + 1]['name'] != '[eng_us] Tags at start of text'
                ):
                    wl_test_init.select_test_files(main, no_files = [i + 1])
                else:
                    continue

        settings['generation_settings']['test_statistical_significance'] = random.choice(tests_statistical_significance)
        settings['generation_settings']['measure_bayes_factor'] = random.choice(measures_bayes_factor)
        settings['generation_settings']['measure_effect_size'] = random.choice(measures_effect_size)

        global main_global
        main_global = main

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")
        print(f"Test of statistical significance: {settings['generation_settings']['test_statistical_significance']}")
        print(f"Measure of Bayes factor: {settings['generation_settings']['measure_bayes_factor']}")
        print(f"Measure of effect size: {settings['generation_settings']['measure_effect_size']}")

        wl_colligation_extractor.Wl_Worker_Colligation_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

def update_gui(err_msg, colligations_freqs_files, colligations_stats_files):
    print(err_msg)
    assert not err_msg

    assert colligations_freqs_files
    assert colligations_stats_files
    assert len(colligations_freqs_files) == len(colligations_stats_files)

    num_files_selected = len(list(main_global.wl_file_area.get_selected_files()))
    test_statistical_significance = main_global.settings_custom['colligation_extractor']['generation_settings']['test_statistical_significance']

    for (node, collocate), stats_files in colligations_stats_files.items():
        freqs_files = colligations_freqs_files[(node, collocate)]

        assert len(freqs_files) == len(stats_files) >= 1

        # Node
        assert node
        # Collocate
        assert collocate

        # Frequency (span positions)
        for freqs_file in freqs_files:
            assert len(freqs_file) == 10

        # Frequency (total)
        assert len(freqs_files) == num_files_selected + 1
        assert sum((sum(freqs_file) for freqs_file in freqs_files)) >= 0

        # Test Statistic & p-value
        assert len(stats_files) == num_files_selected + 1

        for test_stat, p_value, _, _ in stats_files:
            if test_statistical_significance == 'fishers_exact_test':
                assert test_stat is None

            if test_statistical_significance == 'none':
                assert p_value is None
            else:
                assert 0 <= p_value <= 1

        # Number of Files Found
        assert len([freqs_file for freqs_file in freqs_files[:-1] if sum(freqs_file)]) >= 1

if __name__ == '__main__':
    test_colligation_extractor()
