#
# Wordless: Tests - Wordlist
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys
import time

sys.path.append('.')

import pytest

from wl_dialogs import wl_dialog_misc
from wl_tests import wl_test_file_area, wl_test_init

import wl_wordlist

main = wl_test_init.Wl_Test_Main()

wl_test_file_area.wl_test_file_area(main)

def test_wordlist():
    time_start_total = time.time()

    print('Start testing Wordlist...')

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Process_Data(main)

        worker_wordlist_table = wl_wordlist.Wl_Worker_Wordlist_Table(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui
        )
        worker_wordlist_table.run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(error_msg, tokens_freq_files, tokens_stats_files):
    assert not error_msg
    
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
    test_wordlist()
