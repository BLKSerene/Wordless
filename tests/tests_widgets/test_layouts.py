# ----------------------------------------------------------------------
# Tests: Widgets - Layouts
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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from tests import wl_test_init
from wordless.wl_widgets import wl_layouts

main = wl_test_init.Wl_Test_Main()

def test_wl_layout():
    wl_layouts.Wl_Layout()

def test_wl_wrapper():
    wrapper = wl_layouts.Wl_Wrapper(main)
    wrapper.load_settings()

def test_wl_wrapper_file_area():
    wl_layouts.Wl_Wrapper_File_Area(main)

def test_wl_splitter():
    wl_layouts.Wl_Splitter(Qt.Vertical, main)

def test_wl_scroll_area():
    wl_layouts.Wl_Scroll_Area(main)

def test_wl_stacked_widget_resizable():
    stacked_widget = wl_layouts.Wl_Stacked_Widget_Resizable(main)
    stacked_widget.addWidget(QLabel())
    stacked_widget.current_changed(0)

def test_wl_separator():
    wl_layouts.Wl_Separator(main, orientation = 'hor')
    wl_layouts.Wl_Separator(main, orientation = 'vert')

if __name__ == '__main__':
    test_wl_layout()
    test_wl_wrapper()
    test_wl_wrapper_file_area()
    test_wl_splitter()
    test_wl_scroll_area()
    test_wl_stacked_widget_resizable()
    test_wl_separator()
