# ----------------------------------------------------------------------
# Tests: Widgets - Item delegates
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

from PyQt5.QtWidgets import QComboBox

from tests import wl_test_init
from wordless.wl_widgets import wl_item_delegates

main = wl_test_init.Wl_Test_Main()

def test_wl_item_delegate_uneditable():
    item_delegates = wl_item_delegates.Wl_Item_Delegate_Uneditable()
    item_delegates.createEditor(main, '', '')

def test_wl_item_delegate():
    item_delegate = wl_item_delegates.Wl_Item_Delegate(main, QComboBox)
    item_delegate.createEditor(main, 'test', 'test')
    item_delegate.set_enabled(True)

    item_delegate = wl_item_delegates.Wl_Item_Delegate(main)
    item_delegate.createEditor(main, 'test', 'test')

def test_wl_item_delegate_combo_box():
    index_editable = wl_test_init.wl_test_index(0, 0)
    index_uneditable = wl_test_init.wl_test_index(0, 1)

    item_delegate_combo_box = wl_item_delegates.Wl_Item_Delegate_Combo_Box(main, row = 0, col = 0)
    item_delegate_combo_box.createEditor(main, 'test', index_editable)
    assert item_delegate_combo_box.createEditor(main, 'test', index_uneditable) is None
    assert item_delegate_combo_box.is_editable(index_editable)
    assert not item_delegate_combo_box.is_editable(index_uneditable)

def test_wl_item_delegate_combo_box_custom():
    item_delegate_combo_box_custom = wl_item_delegates.Wl_Item_Delegate_Combo_Box_Custom(main, QComboBox, row = 0, col = 0)
    item_delegate_combo_box_custom.createEditor(main, 'test', wl_test_init.wl_test_index(0, 0))
    item_delegate_combo_box_custom.createEditor(main, 'test', wl_test_init.wl_test_index(0, 1))

if __name__ == '__main__':
    test_wl_item_delegate_uneditable()
    test_wl_item_delegate()
    test_wl_item_delegate_combo_box()
    test_wl_item_delegate_combo_box_custom()
