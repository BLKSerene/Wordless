# ----------------------------------------------------------------------
# Tests: Work Area - N-gram Generator
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
from wordless import wl_ngram_generator
from wordless.wl_dialogs import wl_dialogs_misc

main_global = None

def test_ngram_generator():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['ngram_generator']

    settings['search_settings']['multi_search_mode'] = True
    settings['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

    measures_dispersion = list(main.settings_global['measures_dispersion'])
    measures_adjusted_freq = list(main.settings_global['measures_adjusted_freq'])

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
                wl_test_init.select_test_files(main, no_files = [i + 1])

        global main_global
        main_global = main

        settings['generation_settings']['measure_dispersion'] = random.choice(measures_dispersion)
        settings['generation_settings']['measure_adjusted_freq'] = random.choice(measures_adjusted_freq)

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")
        print(f"Measure of dispersion: {settings['generation_settings']['measure_dispersion']}")
        print(f"Measure of adjusted frequency: {settings['generation_settings']['measure_adjusted_freq']}")

        wl_ngram_generator.Wl_Worker_Ngram_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
    print(err_msg)
    assert not err_msg

    assert len(ngrams_freq_files) == len(ngrams_stats_files) >= 1

    num_files_selected = len(list(main_global.wl_file_area.get_selected_files()))
    settings = main_global.settings_custom['ngram_generator']['generation_settings']

    measure_dispersion = settings['measure_dispersion']
    measure_adjusted_freq = settings['measure_adjusted_freq']

    for ngram, freq_files in ngrams_freq_files.items():
        stats_files = ngrams_stats_files[ngram]

        # N-gram
        assert ngram

        # Frequency
        assert len(freq_files) == num_files_selected + 1

        # Dispersion & Adjusted Frequency
        assert len(stats_files) == num_files_selected + 1

        for dispersion, adjusted_freq in stats_files:
            if measure_dispersion == 'none':
                assert dispersion is None
            else:
                assert dispersion >= 0

            if measure_adjusted_freq == 'none':
                assert adjusted_freq is None
            else:
                assert adjusted_freq >= 0

        # Number of Files Found
        assert len([freq for freq in freq_files[:-1] if freq]) >= 1

if __name__ == '__main__':
    test_ngram_generator()
