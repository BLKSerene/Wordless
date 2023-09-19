# ----------------------------------------------------------------------
# Wordless: Tests - Work area - N-gram Generator
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
from wordless import wl_ngram_generator
from wordless.wl_dialogs import wl_dialogs_misc

main_global = None

def test_ngram_generator():
    main = wl_test_init.Wl_Test_Main()

    main.settings_custom['ngram_generator']['search_settings']['multi_search_mode'] = True
    main.settings_custom['ngram_generator']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

    measures_dispersion = list(main.settings_global['measures_dispersion'].keys())
    measures_adjusted_freq = list(main.settings_global['measures_adjusted_freq'].keys())

    for i, (measure_dispersion, measure_adjusted_freq) in enumerate(itertools.zip_longest(
        measures_dispersion,
        measures_adjusted_freq,
        fillvalue = 'none'
    )):
        # Single file
        if i % 3 in [0, 2]:
            wl_test_init.select_random_files(main, num_files = 1)
        # Multiple files
        elif i % 3 == 1:
            wl_test_init.select_random_files(main, num_files = 2)

        global main_global # pylint: disable=global-statement
        main_global = main

        files_selected = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        main.settings_custom['ngram_generator']['generation_settings']['measure_dispersion'] = measure_dispersion
        main.settings_custom['ngram_generator']['generation_settings']['measure_adjusted_freq'] = measure_adjusted_freq

        print(f"Files: {' | '.join(files_selected)}")
        print(f"Measure of dispersion: {main.settings_custom['ngram_generator']['generation_settings']['measure_dispersion']}")
        print(f"Measure of adjusted frequency: {main.settings_custom['ngram_generator']['generation_settings']['measure_adjusted_freq']}")

        wl_ngram_generator.Wl_Worker_Ngram_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    main.app.quit()

def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
    print(err_msg)
    assert not err_msg

    assert len(ngrams_freq_files) == len(ngrams_stats_files) >= 1

    num_files_selected = len(list(main_global.wl_file_area.get_selected_files()))

    for ngram, freq_files in ngrams_freq_files.items():
        stats_files = ngrams_stats_files[ngram]

        # N-gram
        assert ngram
        # Frequency
        assert len(freq_files) == num_files_selected + 1
        # Dispersion & Adjusted Frequency
        assert len(stats_files) == num_files_selected + 1
        # Number of Files Found
        assert len([freq for freq in freq_files[:-1] if freq]) >= 1

if __name__ == '__main__':
    test_ngram_generator()
