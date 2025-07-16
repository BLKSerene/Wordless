# ----------------------------------------------------------------------
# Tests: File Area
# Copyright (C) 2018-2025  Ye Lei (叶磊)
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import glob
import os
import pickle
import random
import time

from PyQt5 import QtCore

from tests import wl_test_init
from wordless import wl_file_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_utils import wl_paths

NUM_FILES_OBSERVED = 3
NUM_FILES_REF = 3
NUM_FILES_ALL = NUM_FILES_OBSERVED + NUM_FILES_REF

FILES_TESTS = glob.glob('tests/files/file_area/*.txt')
FILES_XCT_BOD = glob.glob('tests/files/file_area/xct_bod/*.txt')
FILES_MISC = glob.glob('tests/files/file_area/misc/*.txt')

LEN_FILES_TESTS_OTHERS = len(FILES_XCT_BOD) + len(FILES_MISC)

def wl_test_file_area(main):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        match files_to_open[-1]['name']:
            case '[other] No language support':
                files_to_open[-1]['lang'] = 'other'
            case '[eng_us] Starting with tags':
                files_to_open[-1]['tagged'] = True
            case '[xct] Tibetan tshegs':
                files_to_open[-1]['encoding'] = 'utf_8'
                files_to_open[-1]['lang'] = 'xct'
            case '[bod] Tibetan tshegs':
                files_to_open[-1]['encoding'] = 'utf_8'
                files_to_open[-1]['lang'] = 'bod'

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

    random.shuffle(FILES_TESTS)
    random.shuffle(FILES_MISC)

    for i, file_path in enumerate(FILES_TESTS + FILES_XCT_BOD + FILES_MISC):
        time_start = time.time()

        print(f'Loading file "{os.path.split(file_path)[1]}"... ', end = '')

        # Observed files
        if i < NUM_FILES_OBSERVED or i >= NUM_FILES_ALL:
            worker_update_gui = open_file
        # Reference files
        elif NUM_FILES_OBSERVED <= i < NUM_FILES_ALL:
            worker_update_gui = open_file_ref

        table = QtCore.QObject()
        table.files_to_open = []

        wl_file_area.Wl_Worker_Add_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = worker_update_gui,
            file_paths = (file_path,),
            table = table,
            file_area = main.wl_file_area
        ).run()

        if i < NUM_FILES_OBSERVED or i >= NUM_FILES_ALL:
            new_file = main.settings_custom['file_area']['files_open'][-1]
        elif NUM_FILES_OBSERVED <= i < NUM_FILES_ALL:
            new_file = main.settings_custom['file_area']['files_open_ref'][-1]

        assert new_file['selected']
        assert new_file['name'] == new_file['name_old'] == os.path.splitext(os.path.split(file_path)[-1])[0]

        if i < NUM_FILES_ALL:
            assert new_file['path'] == wl_paths.get_normalized_path(file_path).replace(
                os.path.join('tests', 'files', 'file_area'),
                'imports'
            )
        elif i < NUM_FILES_ALL + 2:
            assert new_file['path'] == wl_paths.get_normalized_path(file_path).replace(
                os.path.join('tests', 'files', 'file_area', 'xct_bod'),
                'imports'
            )
        else:
            assert new_file['path'] == wl_paths.get_normalized_path(file_path).replace(
                os.path.join('tests', 'files', 'file_area', 'misc'),
                'imports'
            )

        assert new_file['path_orig'] == wl_paths.get_normalized_path(file_path)

        if i < NUM_FILES_ALL or new_file['name'] in ('[xct] Tibetan tshegs', '[bod] Tibetan tshegs'):
            assert new_file['encoding'] == 'utf_8', new_file['encoding']
        else:
            assert new_file['encoding'] == 'ascii', new_file['encoding']

        match new_file['name']:
            case '[xct] Tibetan tshegs':
                assert new_file['lang'] == 'xct', new_file['lang']
            case '[bod] Tibetan tshegs':
                assert new_file['lang'] == 'bod', new_file['lang']
            case '[other] No language support':
                assert new_file['lang'] == 'other', new_file['lang']
            case _:
                assert new_file['lang'] == 'eng_us', new_file['lang']

        if new_file['name'] == '[eng_us] Starting with tags':
            assert new_file['tagged']
        else:
            assert not new_file['tagged']

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    # Save Settings
    with open('tests/wl_settings.pickle', 'wb') as f:
        pickle.dump(main.settings_custom, f)

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    wl_test_file_area(main)
