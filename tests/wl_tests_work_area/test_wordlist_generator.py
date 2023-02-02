# ----------------------------------------------------------------------
# Wordless: Tests - Work Area - Wordlist Generator
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

import re

from tests import wl_test_init
from wordless import wl_wordlist_generator
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

def test_wordlist_generator():
    measures_dispersion = list(main.settings_global['measures_dispersion'].keys())
    measures_adjusted_freq = list(main.settings_global['measures_adjusted_freq'].keys())

    len_measures_dispersion = len(measures_dispersion)
    len_measures_adjusted_freq = len(measures_adjusted_freq)

    for i in range(max([len_measures_dispersion, len_measures_adjusted_freq])):
        # Single file
        if i % 2 == 0:
            wl_test_init.select_random_files(main, num_files = 1)
        # Multiple files
        elif i % 2 == 1:
            wl_test_init.select_random_files(main, num_files = 2)

        files_selected = [
            re.search(r'(?<=\[)[a-z_]+(?=\])', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        main.settings_custom['wordlist_generator']['generation_settings']['measure_dispersion'] = measures_dispersion[i % len_measures_dispersion]
        main.settings_custom['wordlist_generator']['generation_settings']['measure_adjusted_freq'] = measures_adjusted_freq[i % len_measures_adjusted_freq]

        print(f"Files: {', '.join(files_selected)}")
        print(f"Measure of dispersion: {main.settings_custom['wordlist_generator']['generation_settings']['measure_dispersion']}")
        print(f"Measure of adjusted frequency: {main.settings_custom['wordlist_generator']['generation_settings']['measure_adjusted_freq']}")

        wl_wordlist_generator.Wl_Worker_Wordlist_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    main.app.quit()

def update_gui(err_msg, tokens_freq_files, tokens_stats_files):
    print(err_msg)
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
