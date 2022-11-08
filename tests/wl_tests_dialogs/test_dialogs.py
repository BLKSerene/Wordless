# ----------------------------------------------------------------------
# Wordless: Tests - Dialogs - Dialogs
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

from tests import wl_test_init
from wordless.wl_dialogs import wl_dialogs

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog():
    wl_dialogs.Wl_Dialog(main, title = 'test')

def test_wl_dialog_frameless():
    wl_dialogs.Wl_Dialog_Frameless(main)

def test_wl_dialog_info():
    wl_dialogs.Wl_Dialog_Info(main, title = 'test')

def test_wl_dialog_settings():
    wl_dialogs.Wl_Dialog_Settings(main, title = 'test')

def test_wl_dialog_err():
    wl_dialogs.Wl_Dialog_Err(main, title = 'test')

if __name__ == '__main__':
    test_wl_dialog()
    test_wl_dialog_frameless()
    test_wl_dialog_info()
    test_wl_dialog_settings()
    test_wl_dialog_err()
