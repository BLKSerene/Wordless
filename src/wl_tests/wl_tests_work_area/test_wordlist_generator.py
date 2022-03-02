# ----------------------------------------------------------------------
# Wordless: Tests - Wordlist Generator
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

import wl_wordlist_generator

main = wl_test_init.Wl_Test_Main()
files = main.settings_custom['file_area']['files_open']

def test_wordlist_generator():
    print('Start testing module Wordlist Generator...')

    measures_dispersion = list(main.settings_global['measures_dispersion'].keys())
    measures_adjusted_freq = list(main.settings_global['measures_adjusted_freq'].keys())
    len_diff = abs(len(measures_dispersion) - len(measures_adjusted_freq))

    if len(measures_dispersion) > len(measures_adjusted_freq):
        measures_adjusted_freq += measures_adjusted_freq * (len_diff // len(measures_adjusted_freq)) + measures_adjusted_freq[: len_diff % len(measures_adjusted_freq)]
    elif len(measures_adjusted_freq) > len(measures_dispersion):
        measures_dispersion += measures_dispersion * (len_diff // len(measures_dispersion)) + measures_dispersion[: len_diff % len(measures_dispersion)]

    for i, (measure_dispersion, measure_adjusted_freq) in enumerate(zip(measures_dispersion, measures_adjusted_freq)):
        for file in files:
            file['selected'] = False

        # Single file
        if i % 2 == 0:
            random.choice(files)['selected'] = True
        # Multiple files
        elif i % 2 == 1:
            for file in files:
                file['selected'] = True

        files_selected = [
            re.search(r'(?<=\[)[a-z_]+(?=\])', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        print(f"Files: {', '.join(files_selected)}")
        print(f'Measure of dispersion: {measure_dispersion}')
        print(f'Measure of adjusted frequency: {measure_adjusted_freq}\n')

        wl_wordlist_generator.Wl_Worker_Wordlist_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    print('All pass!')

    main.app.quit()

def update_gui(err_msg, tokens_freq_files, tokens_stats_files):
    assert not err_msg

    len_files_selected = len(list(main.wl_file_area.get_selected_files()))

    assert len(tokens_freq_files) == len(tokens_stats_files) >= 1

    for token, freq_files in tokens_freq_files.items():
        stats_files = tokens_stats_files[token]

        # Token
        assert token
        # Frequency
        assert len(freq_files) == len_files_selected + 1
        # Dispersion & Adjusted Frequency
        assert len(stats_files) == len_files_selected + 1
        # Number of Files Found
        assert len([freq for freq in freq_files[:-1] if freq]) >= 1

if __name__ == '__main__':
    test_wordlist_generator()
