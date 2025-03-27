# ----------------------------------------------------------------------
# Tests: Widgets - Editors
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
from wordless.wl_utils import wl_paths
from wordless.wl_widgets import wl_editors

main = wl_test_init.Wl_Test_Main()

def test_wl_line_edit_nonempty():
    line_edit = wl_editors.Wl_Line_Edit_Nonempty(main)
    line_edit.setText('test')
    line_edit.text_changed()
    line_edit.setText('')
    line_edit.text_changed()
    line_edit.start_editing()

def test_wl_line_edit_re():
    line_edit = wl_editors.Wl_Line_Edit_Re(main, 'test', 'test', 'test')
    line_edit.setText('test')
    line_edit.text_changed()
    line_edit.setText('')
    line_edit.text_changed()

def test_wl_line_edit_path():
    line_edit = wl_editors.Wl_Line_Edit_Path(main)
    line_edit.dialog_path_empty()
    line_edit.dialog_path_not_found()

def test_wl_line_edit_path_file():
    line_edit = wl_editors.Wl_Line_Edit_Path_File(main)
    line_edit.dialog_path_not_file()

    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('nonexistent.file'))
    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('wordless'))
    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('LICENSE'))
    line_edit.text_changed()
    assert line_edit.validate('test')

def test_wl_line_edit_path_dir():
    line_edit = wl_editors.Wl_Line_Edit_Path_Dir(main)
    line_edit.dialog_path_not_dir()

    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('nonexistent.file'))
    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('LICENSE'))
    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('wordless'))
    line_edit.text_changed()
    assert line_edit.validate('test')

def test_wl_line_edit_path_dir_confirm():
    line_edit = wl_editors.Wl_Line_Edit_Path_Dir_Confirm(main)

    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('LICENSE'))
    line_edit.text_changed()
    assert not line_edit.validate('test')
    line_edit.setText(wl_paths.get_path_file('wordless'))
    line_edit.text_changed()
    assert line_edit.validate('test')

def test_wl_text_browser():
    wl_editors.Wl_Text_Browser(main)

if __name__ == '__main__':
    test_wl_line_edit_nonempty()
    test_wl_line_edit_re()
    test_wl_line_edit_path()
    test_wl_line_edit_path_file()
    test_wl_line_edit_path_dir()
    test_wl_line_edit_path_dir_confirm()

    test_wl_text_browser()
