# ----------------------------------------------------------------------
# Tests: Dialogs - Miscellaneous
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

from tests import wl_test_init
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog_progress():
    wl_dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, text = 'test')
    wl_dialog_progress.open()
    wl_dialog_progress.update_elapsed_time()
    wl_dialog_progress.update_progress('test')

def test_wl_dialog_progress_process_data():
    wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main).open()

def test_wl_dialog_progress_download_model():
    wl_dialogs_misc.Wl_Dialog_Progress_Download_Model(main).open()

def test_wl_dialog_restart_required():
    wl_dialogs_misc.Wl_Dialog_Restart_Required(main).open()

if __name__ == '__main__':
    test_wl_dialog_progress()
    test_wl_dialog_progress_process_data()
    test_wl_dialog_progress_download_model()
    test_wl_dialog_restart_required()
