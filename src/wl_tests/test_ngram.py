#
# Wordless: Tests - N-gram
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

import wl_ngram

main = wl_test_init.Wl_Test_Main()

wl_test_file_area.wl_test_file_area(main)

def test_ngram():
    time_start_total = time.time()

    print('Start testing N-gram...')

    # Exhaust all n-grams
    main.settings_custom['ngram']['search_settings']['search_settings'] = False

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Process_Data(main)

        worker_ngram_table = wl_ngram.Wl_Worker_Ngram_Table(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui
        )
        worker_ngram_table.run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(error_msg, ngrams_freq_files, ngrams_stats_files, ngrams_text):
    assert not error_msg

    assert ngrams_freq_files
    assert ngrams_stats_files
    assert ngrams_text
    assert len(ngrams_freq_files) == len(ngrams_stats_files) == len(ngrams_text)

    for ngram, freq_files in ngrams_freq_files.items():
        stats_files = ngrams_stats_files[ngram]

        # N-gram
        assert ngram
        assert ngrams_text[ngram]
        # Frequency
        assert freq_files
        # Dispersion & Adjusted Frequency
        assert stats_files

if __name__ == '__main__':
    test_ngram()
