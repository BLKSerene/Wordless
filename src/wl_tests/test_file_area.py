#
# Wordless: Tests - File Area
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
import sys
import time

sys.path.append('.')

from wl_dialogs import wl_dialog_misc
from wl_tests import wl_test_init

import wl_file_area

main = wl_test_init.Wl_Test_Main()

def test_file_area():
    new_files = []

    # Clean cached files
    for file in glob.glob('Import/*.*'):
        os.remove(file)

    # Disable encoding detection
    main.settings_custom['file_area']['auto_detection_settings']['detect_encodings'] = False

    for file_path in glob.glob('wl_tests_files/wl_file_area/unicode_decode_error/*.*'):
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
        
        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

def update_gui(error_msg, new_files):
    assert not error_msg

    assert new_files[0]['encoding'] == 'utf_8'

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    test_file_area()
