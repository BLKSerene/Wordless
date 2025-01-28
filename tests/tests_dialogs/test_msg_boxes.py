# ----------------------------------------------------------------------
# Tests: Dialogs - Message boxes
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

from PyQt5.QtWidgets import QMessageBox

from tests import wl_test_init
from wordless.wl_dialogs import wl_msg_boxes

main = wl_test_init.Wl_Test_Main()

def test_wl_msg_box():
    wl_msg_boxes.Wl_Msg_Box(main, icon = QMessageBox.Information, title = 'test', text = 'test').open()

def test_wl_msg_box_info():
    wl_msg_boxes.Wl_Msg_Box_Info(main, title = 'test', text = 'test').open()

def test_wl_msg_box_warning():
    wl_msg_boxes.Wl_Msg_Box_Warning(main, title = 'test', text = 'test').open()

if __name__ == '__main__':
    test_wl_msg_box()
    test_wl_msg_box_info()
    test_wl_msg_box_warning()
