# ----------------------------------------------------------------------
# Wordless: Tests - File Area (Skip CI)
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

import glob
import os
import pickle
import re
import time

from PyQt5.QtCore import QObject

from wl_dialogs import wl_dialogs_misc
from wl_tests import wl_test_init

import wl_file_area

new_files_temp = []

def wl_test_file_area(main):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui,
            files_to_open = files_to_open
        ).run()

    # Clean cached files
    for file in glob.glob('imports/*.*'):
        os.remove(file)

    file_path_loaded = [os.path.basename(file['path']) for file in main.settings_custom['file_area']['files_open']]

    for file_path in glob.glob('wl_tests_files/wl_file_area/*.txt'):
        if os.path.basename(file_path) not in file_path_loaded:
            time_start = time.time()

            print(f'Loading file "{os.path.split(file_path)[1]}"... ', end = '')

            table = QObject()
            table.files_to_open = []

            wl_file_area.Wl_Worker_Add_Files(
                main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
                update_gui = open_file,
                file_paths = [file_path],
                table = table
            ).run()

            main.settings_custom['file_area']['files_open'].extend(new_files_temp)
            new_file = main.settings_custom['file_area']['files_open'][-1]

            assert new_file['selected']
            assert new_file['tokenized'] == 'No'
            assert new_file['tagged'] == 'No'
            assert new_file['name'] == os.path.splitext(os.path.split(file_path)[-1])[0]
            assert new_file['name_old'] == new_file['name']
            assert new_file['lang'] == re.search(r'\[([a-z_]+)\]', file_path).group(1)

            print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    # Save Settings
    with open('wl_tests/wl_settings.pickle', 'wb') as f:
        pickle.dump(main.settings_custom, f)

def update_gui(err_msg, new_files):
    global new_files_temp

    assert not err_msg

    new_files_temp = new_files

if __name__ == '__main__':
    # Reset custom settings
    if os.path.exists('wl_tests/wl_settings.pickle'):
        os.remove('wl_tests/wl_settings.pickle')

    main = wl_test_init.Wl_Test_Main()

    wl_test_file_area(main)
