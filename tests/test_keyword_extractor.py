# ----------------------------------------------------------------------
# Tests: Work Area - Keyword Extractor
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
from wordless import wl_keyword_extractor
from wordless.wl_dialogs import wl_dialogs_misc

main_global = None

def test_keyword_extractor():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['keyword_extractor']

    tests_statistical_significance = [
        test_statistical_significance
        for test_statistical_significance, vals in main.settings_global['tests_statistical_significance'].items()
        if vals['keyword']
    ]
    measures_bayes_factor = [
        measure_bayes_factor
        for measure_bayes_factor, vals in main.settings_global['measures_bayes_factor'].items()
        if vals['keyword']
    ]
    measures_effect_size = list(main.settings_global['measures_effect_size'].keys())

    for i in range(4 + len(glob.glob('tests/files/file_area/misc/*.txt'))):
        match i:
            # Single observed file & single reference file
            case 0:
                wl_test_init.select_test_files(main, no_files = [0])
                wl_test_init.select_test_files(main, no_files = [0], ref = True)
            # Single observed file & multiple reference files
            case 1:
                wl_test_init.select_test_files(main, no_files = [0])
                wl_test_init.select_test_files(main, no_files = [1, 2], ref = True)
            # Multiple observed files & single reference file
            case 2:
                wl_test_init.select_test_files(main, no_files = [1, 2])
                wl_test_init.select_test_files(main, no_files = [0], ref = True)
            # Multiple observed files & multiple reference files
            case 3:
                wl_test_init.select_test_files(main, no_files = [1, 2])
                wl_test_init.select_test_files(main, no_files = [1, 2], ref = True)
            # Miscellaneous
            case _:
                wl_test_init.select_test_files(main, no_files = [i - 1])
                wl_test_init.select_test_files(main, no_files = [0], ref = True)

        settings['generation_settings']['test_statistical_significance'] = random.choice(tests_statistical_significance)
        settings['generation_settings']['measure_bayes_factor'] = random.choice(measures_bayes_factor)
        settings['generation_settings']['measure_effect_size'] = random.choice(measures_effect_size)

        global main_global
        main_global = main

        print(f"Observed Files: {' | '.join(wl_test_init.get_test_file_names(main))}")
        print(f"Reference Files: {' | '.join(wl_test_init.get_test_file_names(main, ref = True))}")
        print(f"Test of statistical significance: {settings['generation_settings']['test_statistical_significance']}")
        print(f"Measure of Bayes factor: {settings['generation_settings']['measure_bayes_factor']}")
        print(f"Measure of effect size: {settings['generation_settings']['measure_effect_size']}")

        wl_keyword_extractor.Wl_Worker_Keyword_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

def update_gui(err_msg, keywords_freq_files, keywords_stats_files):
    print(err_msg)
    assert not err_msg

    assert keywords_freq_files
    assert keywords_stats_files
    assert len(keywords_freq_files) == len(keywords_stats_files)

    num_files_selected = len(list(main_global.wl_file_area.get_selected_files()))
    test_statistical_significance = main_global.settings_custom['keyword_extractor']['generation_settings']['test_statistical_significance']

    for keyword, stats_files in keywords_stats_files.items():
        freq_files = keywords_freq_files[keyword]

        assert len(freq_files) == len(stats_files) + 1 >= 1

        # Keyword
        assert keyword

        # Frequency (observed files)
        assert any((freq_file for freq_file in freq_files[1:-1]))
        # Frequency (total)
        assert len(freq_files) == num_files_selected + 2
        assert freq_files[-1] == sum(freq_files[1:-1])

        # p-value
        for test_stat, p_value, _, _ in stats_files:
            if test_statistical_significance == 'fishers_exact_test':
                assert test_stat is None

            if test_statistical_significance == 'none':
                assert p_value is None
            else:
                assert 0 <= p_value <= 1

        # Number of Files Found
        assert len([freq for freq in freq_files[1:-1] if freq]) >= 1

if __name__ == '__main__':
    test_keyword_extractor()
