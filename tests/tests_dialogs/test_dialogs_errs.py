# ----------------------------------------------------------------------
# Tests: Dialogs - Errors
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
from wordless.wl_dialogs import wl_dialogs_errs

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog_err():
    wl_dialogs_errs.Wl_Dialog_Err(main, title = 'test').open()

def test_wl_dialog_err_info_copy():
    wl_dialogs_errs.Wl_Dialog_Err_Info_Copy(main, title = 'test').open()

def test_wl_dialog_err_fatal():
    wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg = 'test').open()

def test_wl_dialog_err_download_model():
    wl_dialogs_errs.Wl_Dialog_Err_Download_Model(main, err_msg = 'test').open()

def test_wl_dialog_err_files():
    wl_dialogs_errs.Wl_Dialog_Err_Files(main, title = 'test').open()

if __name__ == '__main__':
    test_wl_dialog_err()
    test_wl_dialog_err_info_copy()
    test_wl_dialog_err_fatal()
    test_wl_dialog_err_download_model()
    test_wl_dialog_err_files()
