# ----------------------------------------------------------------------
# Tests: Dialogs - Dialogs
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
from wordless.wl_dialogs import wl_dialogs

main = wl_test_init.Wl_Test_Main()

def test_get_msg_box_icon():
    wl_dialogs.get_msg_box_icon('info')
    wl_dialogs.get_msg_box_icon('warning')
    wl_dialogs.get_msg_box_icon('critical')
    wl_dialogs.get_msg_box_icon('question')

def test_wl_dialog():
    wl_dialog = wl_dialogs.Wl_Dialog(main, 'test')
    wl_dialog.open()
    wl_dialog.adjust_size()
    wl_dialog.move_to_center()

    wl_dialogs.Wl_Dialog(main, 'test', resizable = True).open()
    wl_dialogs.Wl_Dialog(main, 'test', resizable = False).open()
    wl_dialogs.Wl_Dialog(main, 'test', width = 600, height = 400, resizable = True).open()
    wl_dialogs.Wl_Dialog(main, 'test', width = 600, height = 400, resizable = False).open()
    wl_dialogs.Wl_Dialog(main, 'test', beep = True).open()
    wl_dialogs.Wl_Dialog(main, 'test', beep = False).open()

def test_wl_dialog_frameless():
    wl_dialogs.Wl_Dialog_Frameless(main).open()

def test_wl_dialog_info():
    wl_dialogs.Wl_Dialog_Info(main, 'test').open()

    wl_dialogs.Wl_Dialog_Info(main, 'test', resizable = True).open()
    wl_dialogs.Wl_Dialog_Info(main, 'test', resizable = False).open()

    wl_dialogs.Wl_Dialog_Info(main, 'test', icon = 'info').open()
    wl_dialogs.Wl_Dialog_Info(main, 'test', icon = 'warning').open()
    wl_dialogs.Wl_Dialog_Info(main, 'test', icon = 'critical').open()
    wl_dialogs.Wl_Dialog_Info(main, 'test', icon = 'question').open()

    wl_dialogs.Wl_Dialog_Info(main, 'test', no_buttons = True).open()
    wl_dialogs.Wl_Dialog_Info(main, 'test', no_buttons = False).open()

def test_wl_dialog_info_simple():
    wl_dialogs.Wl_Dialog_Info_Simple(main, 'test', 'test').open()

def test_wl_dialog_info_copy():
    wl_dialog_info_copy = wl_dialogs.Wl_Dialog_Info_Copy(main, 'test', is_plain_text = False)
    wl_dialog_info_copy.open()
    wl_dialog_info_copy.copy()
    wl_dialog_info_copy.get_info()
    wl_dialog_info_copy.set_info('test')

    wl_dialog_info_copy = wl_dialogs.Wl_Dialog_Info_Copy(main, 'test', is_plain_text = True)
    wl_dialog_info_copy.set_info('test')

def test_wl_dialog_question():
    wl_dialogs.Wl_Dialog_Question(main, 'test', 'test', default_to_yes = True).open()
    wl_dialogs.Wl_Dialog_Question(main, 'test', 'test', default_to_yes = False).open()

def test_wl_dialog_settings():
    wl_dialog_settings = wl_dialogs.Wl_Dialog_Settings(main, 'test')
    wl_dialog_settings.open()
    wl_dialog_settings.load_settings()
    wl_dialog_settings.save_settings()

if __name__ == '__main__':
    test_get_msg_box_icon()

    test_wl_dialog()
    test_wl_dialog_frameless()
    test_wl_dialog_info()
    test_wl_dialog_info_simple()
    test_wl_dialog_info_copy()
    test_wl_dialog_question()
    test_wl_dialog_settings()
