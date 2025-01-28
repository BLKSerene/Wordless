# ----------------------------------------------------------------------
# Tests: Widgets - Labels
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
from wordless.wl_widgets import wl_labels

main = wl_test_init.Wl_Test_Main()

def test_wl_label():
    wl_labels.Wl_Label('test', main)

def test_wl_label_important():
    wl_labels.Wl_Label_Important('test', main)

def test_wl_label_hint():
    wl_labels.Wl_Label_Hint('test', main)

def test_wl_label_html():
    wl_labels.Wl_Label_Html('test', main)

def test_wl_label_html_centered():
    wl_labels.Wl_Label_Html_Centered('test', main)

def test_wl_label_dialog():
    label = wl_labels.Wl_Label_Dialog('test', main)
    label.set_text('test')

def test_wl_label_dialog_no_wrap():
    wl_labels.Wl_Label_Dialog_No_Wrap('test', main)

if __name__ == '__main__':
    test_wl_label()
    test_wl_label_important()
    test_wl_label_hint()
    test_wl_label_html()
    test_wl_label_html_centered()
    test_wl_label_dialog()
    test_wl_label_dialog_no_wrap()
