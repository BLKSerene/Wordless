# ----------------------------------------------------------------------
# Wordless: Tests - Work Area - N-gram Generator
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

from tests import wl_test_init
from wordless import wl_ngram_generator
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

main.settings_custom['ngram_generator']['search_settings']['multi_search_mode'] = True
main.settings_custom['ngram_generator']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

def test_ngram_generator():
    print('Start testing module N-gram Generator...')

    measures_dispersion = list(main.settings_global['measures_dispersion'].keys())
    measures_adjusted_freq = list(main.settings_global['measures_adjusted_freq'].keys())

    len_measures_dispersion = len(measures_dispersion)
    len_measures_adjusted_freq = len(measures_adjusted_freq)
    len_max_measures = max([len_measures_dispersion, len_measures_adjusted_freq])

    files = main.settings_custom['file_area']['files_open']
    i_search_sing, i_search_multi = random.sample(range(len_max_measures), 2)

    for i in range(len_max_measures):
        for file in files:
            file['selected'] = False

        # Single file without search terms
        if i == i_search_sing:
            random.choice(files)['selected'] = True

            main.settings_custom['ngram_generator']['search_settings']['search_settings'] = False
        # Multiple files without search terms
        elif i == i_search_multi:
            for file in random.sample(files, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

            main.settings_custom['ngram_generator']['search_settings']['search_settings'] = False
        # Single file with search terms
        elif i % 2 == 0:
            random.choice(files)['selected'] = True

            main.settings_custom['ngram_generator']['search_settings']['search_settings'] = True
        # Multiple files with search terms
        elif i % 2 == 1:
            for file in random.sample(files, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

            main.settings_custom['ngram_generator']['search_settings']['search_settings'] = True

        files_selected = [
            re.search(r'(?<=\[)[a-z_]+(?=\])', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        main.settings_custom['ngram_generator']['generation_settings']['measure_dispersion'] = measures_dispersion[i % len_measures_dispersion]
        main.settings_custom['ngram_generator']['generation_settings']['measure_adjusted_freq'] = measures_adjusted_freq[i % len_measures_adjusted_freq]

        print(f'[Test Round {i + 1}]')
        print(f"Files: {', '.join(files_selected)}")
        print(f"Search settings: {main.settings_custom['ngram_generator']['search_settings']['search_settings']}")
        print(f"Measure of dispersion: {main.settings_custom['ngram_generator']['generation_settings']['measure_dispersion']}")
        print(f"Measure of adjusted frequency: {main.settings_custom['ngram_generator']['generation_settings']['measure_adjusted_freq']}")

        wl_ngram_generator.Wl_Worker_Ngram_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    print('All pass!')

    main.app.quit()

def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files):
    print(err_msg)
    assert not err_msg

    len_files_selected = len(list(main.wl_file_area.get_selected_files()))

    assert len(ngrams_freq_files) == len(ngrams_stats_files) >= 1

    for ngram, freq_files in ngrams_freq_files.items():
        stats_files = ngrams_stats_files[ngram]

        # N-gram
        assert ngram
        # Frequency
        assert len(freq_files) == len_files_selected + 1
        # Dispersion & Adjusted Frequency
        assert len(stats_files) == len_files_selected + 1
        # Number of Files Found
        assert len([freq for freq in freq_files[:-1] if freq]) >= 1

if __name__ == '__main__':
    test_ngram_generator()
