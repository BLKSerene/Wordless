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

import time

from wl_dialogs import wl_dialogs_misc
from wl_tests import wl_test_file_area, wl_test_init

import wl_wordlist_generator

main = wl_test_init.Wl_Test_Main()

wl_test_file_area.wl_test_file_area(main)

def test_wordlist_generator():
    time_start_total = time.time()

    print('Start testing module Wordlist Generator...')

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        wl_wordlist_generator.Wl_Worker_Wordlist_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(err_msg, tokens_freq_files, tokens_stats_files):
    assert not err_msg

    assert tokens_freq_files
    assert tokens_stats_files
    assert len(tokens_freq_files) == len(tokens_stats_files)

    for token, freq_files in tokens_freq_files.items():
        stats_files = tokens_stats_files[token]

        # Token
        assert token
        # Frequency
        assert freq_files
        # Dispersion & Adjusted Frequency
        assert stats_files

if __name__ == '__main__':
    test_wordlist_generator()
