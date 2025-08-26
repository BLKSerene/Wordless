# ----------------------------------------------------------------------
# Tests: File Area - Miscellaneous
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

import os
import time

from PyQt5 import QtCore

from tests import wl_test_init
from wordless import wl_file_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_texts
from wordless.wl_utils import wl_threading

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def add_file(file_paths, update_gui, file_type = 'observed'):
    def open_file(err_msg, files_to_open):
        assert not err_msg

        if files_to_open[-1]['path'].endswith('encoding_manually_changed.txt'):
            files_to_open[-1]['encoding'] = 'windows_1252'

        main.worker_open_files = wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            update_gui = update_gui,
            files_to_open = files_to_open,
            file_type = file_type
        )

        main.thread_open_files = QtCore.QThread()
        wl_threading.start_worker_in_thread(main.worker_open_files, main.thread_open_files, update_gui)

        print(f'Done! (In {round(time.time() - time_start, 2)} seconds)\n')

    time_start = time.time()

    for file_path in file_paths:
        print(f'Opening file "{os.path.split(file_path)[1]}"...')

        table = QtCore.QObject()
        table.files_to_open = []

        main.worker_add_files = wl_file_area.Wl_Worker_Add_Files(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = ''),
            file_paths = [file_path],
            table = table,
            file_area = main.wl_file_area
        )

        main.thread_add_files = QtCore.QThread()
        wl_threading.start_worker_in_thread(main.worker_add_files, main.thread_add_files, open_file)

# Check if underscores in tokenized Vietnamese files are removed
def test_file_area_vie():
    wl_test_init.clean_import_caches()

    main.settings_custom['file_area']['dialog_open_corpora']['auto_detect_encodings'] = False
    main.settings_custom['file_area']['dialog_open_corpora']['auto_detect_langs'] = False

    main.settings_custom['files']['default_settings']['encoding'] = 'utf_8'
    main.settings_custom['files']['default_settings']['lang'] = 'vie'
    main.settings_custom['files']['default_settings']['tokenized'] = True
    main.settings_custom['files']['default_settings']['tagged'] = False

    add_file(
        file_paths = ('tests/files/wl_file_area/misc/vie_tokenized.txt',),
        update_gui = update_gui_vie,
        file_type = 'observed'
    )
    add_file(
        file_paths = ('tests/files/wl_file_area/misc/vie_tokenized.txt',),
        update_gui = update_gui_vie,
        file_type = 'ref'
    )

def update_gui_vie(err_msg, new_files):
    assert not err_msg

    file_text = new_files[0]['text']

    print(file_text.tokens_multilevel)

    for para in file_text.tokens_multilevel:
        for sentence in para:
            for sentence_seg in sentence:
                for token in sentence_seg:
                    assert not wl_texts.RE_VIE_TOKENIZED.search(token)

# Check if the text is re-decoded when the encoding settings are manually changed after auto-detection
def test_file_area_encoding_manually_changed():
    wl_test_init.clean_import_caches()

    main.settings_custom['file_area']['dialog_open_corpora']['auto_detect_encodings'] = False
    main.settings_custom['file_area']['dialog_open_corpora']['auto_detect_langs'] = False

    main.settings_custom['files']['default_settings']['encoding'] = 'utf_8'
    main.settings_custom['files']['default_settings']['lang'] = 'eng_us'
    main.settings_custom['files']['default_settings']['tokenized'] = False
    main.settings_custom['files']['default_settings']['tagged'] = False

    add_file(
        file_paths = ('tests/files/wl_file_area/misc/encoding_manually_changed.txt',),
        update_gui = update_gui_encoding_manually_changed
    )

def update_gui_encoding_manually_changed(err_msg, new_files):
    assert not err_msg

    print(new_files[0]['text'].to_token_texts())

    # Garbled text intentionally made
    assert new_files[0]['encoding'] == 'windows_1252'
    assert new_files[0]['text'].to_token_texts() == [[[['Å½']]]]

if __name__ == '__main__':
    test_file_area_vie()
    test_file_area_encoding_manually_changed()
