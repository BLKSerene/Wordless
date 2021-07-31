#
# Wordless: Tests - File Area (Skip CI)
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import glob
import os
import pickle
import re
import sys
import time

sys.path.append('.')

from wl_dialogs import wl_dialog_misc
from wl_tests import wl_test_init

import wl_file_area

def wl_test_file_area(main):
    new_files = []

    # Clean cached files
    for file in glob.glob('Import/*.*'):
        os.remove(file)

    file_path_loaded = [os.path.basename(file['path']) for file in main.settings_custom['file_area']['files_open']]

    for file_path in glob.glob('wl_tests_files/wl_file_area/*.txt'):
        if os.path.basename(file_path) not in file_path_loaded:
            time_start = time.time()

            print(f'Loading file "{os.path.split(file_path)[1]}"... ', end = '')

            dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Open_Files(main)

            worker_open_files = wl_file_area.Wl_Worker_Open_Files(
                main,
                dialog_progress = dialog_progress,
                update_gui = update_gui,
                file_paths = [file_path]
            )
            worker_open_files.run()

            new_file = main.settings_custom['file_area']['files_open'][-1]

            assert new_file['selected'] == True
            assert new_file['tokenized'] == 'No'
            assert new_file['tagged'] == 'No'
            assert new_file['name'] == os.path.splitext(os.path.split(file_path)[-1])[0]
            assert new_file['name_old'] == new_file['name']
            assert new_file['lang'] == re.search(r'\[([a-z_]+)\]', file_path).group(1)

            print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    # Save Settings
    with open('wl_tests/wl_settings.pickle', 'wb') as f:
        pickle.dump(main.settings_custom, f)

def update_gui(error_msg, new_files):
    assert not error_msg

    main.settings_custom['file_area']['files_open'].extend(new_files)

if __name__ == '__main__':
    # Reset custom settings
    if os.path.exists('wl_tests/wl_settings.pickle'):
        os.remove('wl_tests/wl_settings.pickle')

    main = wl_test_init.Wl_Test_Main()

    wl_test_file_area(main)
