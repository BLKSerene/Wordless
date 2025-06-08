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

from PyQt5 import QtWidgets

from tests import wl_test_init
from wordless.wl_widgets import wl_buttons

main = wl_test_init.Wl_Test_Main()

def test_wl_button():
    wl_buttons.Wl_Button('test', main)

def test_wl_button_browse():
    wl_buttons.Wl_Button_Browse(main, 'test', QtWidgets.QLineEdit(), 'test', ['test'])

def test_wl_button_color_transparent():
    button = wl_buttons.Wl_Button_Color(main)
    button.get_color()
    button.set_color('test')

    _, checkbox_transparent = wl_buttons.wl_button_color_transparent(main)
    checkbox_transparent.setChecked(True)
    checkbox_transparent.setChecked(False)

def test_wl_button_restore_default_vals():
    wl_buttons.Wl_Button_Restore_Default_Vals(main, 'test')

if __name__ == '__main__':
    test_wl_button()
    test_wl_button_browse()
    test_wl_button_color_transparent()
    test_wl_button_restore_default_vals()
