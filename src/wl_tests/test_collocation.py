#
# Wordless: Tests - Collocation
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import random
import sys
import time

sys.path.append('.')

import pytest

from wl_dialogs import wl_dialog_misc
from wl_tests import wl_test_file_area, wl_test_init

import wl_collocation

main = wl_test_init.Wl_Test_Main()

wl_test_file_area.wl_test_file_area(main)

def test_collocation():
    time_start_total = time.time()

    print('Start testing Collocation...')

    # Exhaust all collocations
    main.settings_custom['collocation']['search_settings']['search_settings'] = False

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Process_Data(main)

        worker_collocation_table = wl_collocation.Wl_Worker_Collocation_Table(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui
        )
        worker_collocation_table.run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(error_msg, collocations_freqs_files, collocations_stats_files, nodes_text):
    assert not error_msg

    assert collocations_freqs_files
    assert collocations_stats_files
    assert nodes_text
    assert len(collocations_freqs_files) == len(collocations_stats_files)

    for (node, collocate), stats_files in collocations_stats_files.items():
        freqs_files = collocations_freqs_files[(node, collocate)]

        # Node
        assert node
        assert nodes_text[node]
        # Collocate
        assert collocate
        # Frequency
        assert freqs_files
        # Statistics
        assert stats_files

if __name__ == '__main__':
    test_collocation()
