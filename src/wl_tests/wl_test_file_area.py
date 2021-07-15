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
import pickle
import re
import sys
import time

sys.path.append('.')

from wl_checking import wl_checking_misc
from wl_tests import wl_test_init
from wl_text import wl_text

def wl_test_file_area(main):
    new_files = []

    # Clean cached files
    for file in glob.glob('Import/*.*'):
        os.remove(file)

    file_path_loaded = [os.path.basename(file['path']) for file in main.settings_custom['files']['files_open']]
    
    for file_path in glob.glob('wl_tests/files/wl_file_area/*.*'):
        if os.path.basename(file_path) not in file_path_loaded:
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = round(file_size_bytes / 1024 / 1024, 2)

            time_start = time.time()

            print(f'Opening file "{os.path.split(file_path)[1]}" ({file_size_mb} MB)...', end = '')

            new_file = main.wl_files._new_file(file_path)
            
            assert new_file['selected'] == True
            assert new_file['tokenized'] == 'No'
            assert new_file['tagged'] == 'No'
            assert new_file['name'] == os.path.splitext(os.path.split(file_path)[-1])[0]
            assert new_file['name_old'] == new_file['name']
            assert new_file['lang'] == re.search(r'\[([a-z_]+)\]', file_path).group(1)

            new_files.append(new_file)

            print(f' done (in {round(time.time() - time_start, 2)} seconds)!')
    
    main.settings_custom['files']['files_open'].extend(new_files)

    # Save Settings
    with open('wl_tests/wl_settings.pickle', 'wb') as f:
        pickle.dump(main.settings_custom, f)

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    wl_test_file_area(main)
