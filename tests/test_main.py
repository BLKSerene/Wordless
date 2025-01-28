# ----------------------------------------------------------------------
# Tests: Main window
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
from wordless import wl_main

main = wl_test_init.Wl_Test_Main()

def test_wl_loading():
    wl_main.global_font_family = 'Arial'
    wl_main.global_font_size = 10

    wl_loading = wl_main.Wl_Loading()
    wl_loading.show_message('test')
    wl_loading.fade_in()
    wl_loading.fade_out()

def test_wl_dialog_confirm_exit():
    wl_dialog_confirm_exit = wl_main.Wl_Dialog_Confirm_Exit(main)
    wl_dialog_confirm_exit.open()
    wl_dialog_confirm_exit.load_settings()
    wl_dialog_confirm_exit.always_confirm_on_exit_changed()

def test_wl_dialog_need_help():
    wl_dialog_need_help = wl_main.Wl_Dialog_Need_Help(main)
    wl_dialog_need_help.open()

def test_wl_dialog_citing():
    wl_dialog_citing = wl_main.Wl_Dialog_Citing(main)
    wl_dialog_citing.open()
    wl_dialog_citing.load_settings()
    wl_dialog_citing.citation_changed()

def test_wl_dialog_donating():
    wl_dialog_donating = wl_main.Wl_Dialog_Donating(main)
    wl_dialog_donating.open()
    wl_dialog_donating.load_settings()
    wl_dialog_donating.donating_via_changed()

def test_wl_dialog_acks():
    wl_dialog_acks = wl_main.Wl_Dialog_Acks(main)
    wl_dialog_acks.open()

def test_wl_dialog_check_updates():
    wl_dialog_check_updates = wl_main.Wl_Dialog_Check_Updates(main)
    wl_dialog_check_updates.open()
    wl_dialog_check_updates.check_updates()
    wl_dialog_check_updates.stop_checking()
    wl_dialog_check_updates.checking_status_changed('network_err')
    wl_dialog_check_updates.checking_status_changed('checking')
    wl_dialog_check_updates.checking_status_changed('updates_available')
    wl_dialog_check_updates.checking_status_changed('no_updates')
    wl_dialog_check_updates.load_settings()
    wl_dialog_check_updates.check_updates_on_startup_changed()

    wl_dialog_check_updates = wl_main.Wl_Dialog_Check_Updates(main, on_startup = True)
    wl_dialog_check_updates.open()
    wl_dialog_check_updates.checking_status_changed('updates_available')

def test_wl_dialog_changelog():
    wl_dialog_changelog = wl_main.Wl_Dialog_Changelog(main)
    wl_dialog_changelog.open()

def test_wl_dialog_about():
    wl_dialog_changelog = wl_main.Wl_Dialog_About(main)
    wl_dialog_changelog.open()

if __name__ == '__main__':
    test_wl_loading()
    test_wl_dialog_confirm_exit()

    test_wl_dialog_need_help()
    test_wl_dialog_citing()
    test_wl_dialog_donating()
    test_wl_dialog_acks()
    test_wl_dialog_check_updates()
    test_wl_dialog_changelog()
    test_wl_dialog_about()
