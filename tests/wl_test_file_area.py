# ----------------------------------------------------------------------
# Wordless: Tests - File area
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

import glob
import os
import pickle
import random
import time

from PyQt5.QtCore import QObject

from tests import wl_test_init
from wordless import wl_file_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_utils import wl_paths

def wl_test_file_area(main):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui,
            files_to_open = files_to_open,
            file_type = 'observed'
        ).run()

    def open_file_ref(err_msg, files_to_open):
        assert not err_msg

        wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui_ref,
            files_to_open = files_to_open,
            file_type = 'ref'
        ).run()

    def update_gui(err_msg, new_files):
        assert not err_msg

        main.settings_custom['file_area']['files_open'].extend(new_files)

    def update_gui_ref(err_msg, new_files):
        assert not err_msg

        main.settings_custom['file_area']['files_open_ref'].extend(new_files)

    wl_test_init.clean_import_caches()
    # Reset custom settings
    main.settings_custom['file_area']['files_open'].clear()
    main.settings_custom['file_area']['files_open_ref'].clear()

    files = glob.glob('tests/files/wl_file_area/file_area/*.txt')
    random.shuffle(files)

    for file_path in files[:3]:
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

        new_file = main.settings_custom['file_area']['files_open'][-1]

        assert new_file['selected']
        assert new_file['name'] == new_file['name_old'] == os.path.splitext(os.path.split(file_path)[-1])[0]
        assert new_file['path'] == wl_paths.get_normalized_path(file_path).replace(os.path.join('tests', 'files', 'wl_file_area', 'file_area'), 'imports')
        assert new_file['path_original'] == wl_paths.get_normalized_path(file_path)
        assert new_file['encoding'] == 'utf_8'
        assert new_file['lang'] == 'eng_us'
        assert not new_file['tokenized']
        assert not new_file['tagged']

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    # Reference files
    for file_path in files[3:6]:
        time_start = time.time()

        print(f'Loading file "{os.path.split(file_path)[1]}" as reference file... ', end = '')

        table = QObject()
        table.files_to_open = []

        wl_file_area.Wl_Worker_Add_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = open_file_ref,
            file_paths = [file_path],
            table = table
        ).run()

        new_file = main.settings_custom['file_area']['files_open_ref'][-1]

        assert new_file['selected']
        assert new_file['name'] == new_file['name_old'] == os.path.splitext(os.path.split(file_path)[-1])[0]
        assert new_file['path'] == wl_paths.get_normalized_path(file_path).replace(os.path.join('tests', 'files', 'wl_file_area', 'file_area'), 'imports')
        assert new_file['path_original'] == wl_paths.get_normalized_path(file_path)
        assert new_file['encoding'] == 'utf_8'
        assert new_file['lang'] == 'eng_us'
        assert not new_file['tokenized']
        assert not new_file['tagged']

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    # Save Settings
    with open('tests/wl_settings.pickle', 'wb') as f:
        pickle.dump(main.settings_custom, f)

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    wl_test_file_area(main)
