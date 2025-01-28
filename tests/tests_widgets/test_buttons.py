# ----------------------------------------------------------------------
# Tests: Widgets - Buttons
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

from PyQt5.QtWidgets import QLineEdit

from tests import wl_test_init
from wordless.wl_widgets import wl_buttons

main = wl_test_init.Wl_Test_Main()

def test_wl_button():
    wl_buttons.Wl_Button('test', main)

def test_wl_button_browse():
    wl_buttons.Wl_Button_Browse(main, 'test', QLineEdit(), 'test', ['test'])

def test_wl_button_color():
    button = wl_buttons.Wl_Button_Color(main)
    button.get_color()
    button.set_color('test')

    _, checkbox_transparent = wl_buttons.wl_button_color(main, allow_transparent = True)
    checkbox_transparent.setChecked(True)
    checkbox_transparent.setChecked(False)

    wl_buttons.wl_button_color(main, allow_transparent = False)

def test_wl_button_restore_defaults():
    wl_buttons.Wl_Button_Restore_Defaults(main, 'test')

if __name__ == '__main__':
    test_wl_button()
    test_wl_button_browse()
    test_wl_button_color()
    test_wl_button_restore_defaults()
