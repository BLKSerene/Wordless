# ----------------------------------------------------------------------
# Tests: Widgets - Boxes
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
from wordless.wl_widgets import wl_boxes

main = wl_test_init.Wl_Test_Main()

def test_wl_combo_box():
    wl_boxes.Wl_Combo_Box(main)

def test_wl_combo_box_adjustable():
    wl_boxes.Wl_Combo_Box_Adjustable(main)

def test_wl_combo_box_enums():
    combo_box_enums = wl_boxes.Wl_Combo_Box_Enums(main, {'test1': 1, 'test2': 2})
    assert combo_box_enums.get_val() == 1

    combo_box_enums.set_val(2)
    assert combo_box_enums.get_val() == 2

def test_wl_combo_box_yes_no():
    combo_box_yes_no = wl_boxes.Wl_Combo_Box_Yes_No(main)
    assert combo_box_yes_no.get_yes_no()

    combo_box_yes_no.set_yes_no(False)
    assert not combo_box_yes_no.get_yes_no()

def test_wl_combo_box_lang():
    wl_boxes.Wl_Combo_Box_Lang(main)

def test_wl_combo_box_encoding():
    wl_boxes.Wl_Combo_Box_Encoding(main)

def test_wl_combo_box_measure():
    mapping_measures = list(list(main.settings_global['mapping_measures'].values())[0].items())

    combo_box_measure = wl_boxes.Wl_Combo_Box_Measure(main, list(main.settings_global['mapping_measures'])[0])
    assert combo_box_measure.get_measure() == mapping_measures[0][1]

    combo_box_measure.set_measure(mapping_measures[1][1])
    assert combo_box_measure.get_measure() == mapping_measures[1][1]

def test_wl_combo_box_file_to_filter():
    table = wl_test_init.Wl_Test_Table(main)
    table.settings['file_area']['files_open'] = [{'selected': True, 'name': 'test'}]

    combo_box_file_to_filter = wl_boxes.Wl_Combo_Box_File_To_Filter(main, table)
    combo_box_file_to_filter.table_item_changed()

def test_wl_combo_box_file():
    combo_box_file = wl_boxes.Wl_Combo_Box_File(main)
    combo_box_file.wl_files_changed()
    combo_box_file.get_file()

def test_wl_combo_box_font_family():
    wl_boxes.Wl_Combo_Box_Font_Family(main)

def test_wl_spin_box():
    wl_boxes.Wl_Spin_Box(main)

def test_wl_spin_box_window():
    spin_box_window = wl_boxes.Wl_Spin_Box_Window(main)
    spin_box_window.setValue(-100)
    spin_box_window.stepBy(1)
    spin_box_window.setValue(-100)
    spin_box_window.stepBy(1)

def test_wl_spin_box_font_size():
    wl_boxes.Wl_Spin_Box_Font_Size(main)

def test_wl_spin_box_font_weight():
    wl_boxes.Wl_Spin_Box_Font_Weight(main)

def test_wl_double_spin_box():
    wl_boxes.Wl_Double_Spin_Box(main)

def test_wl_double_spin_box_alpha():
    wl_boxes.Wl_Double_Spin_Box_Alpha(main)

def test_wl_spin_box_no_limit():
    _, checkbox_no_limit = wl_boxes.wl_spin_box_no_limit(main, double = True)

    checkbox_no_limit.setChecked(True)
    checkbox_no_limit.setChecked(False)

    wl_boxes.wl_spin_box_no_limit(main, double = False)

def test_wl_spin_boxes_min_max():
    _, spin_box_min, _, spin_box_max = wl_boxes.wl_spin_boxes_min_max(main, double = True)

    spin_box_min.setValue(100)
    spin_box_max.setValue(1)

    wl_boxes.wl_spin_boxes_min_max(main, double = False)

def test_wl_spin_boxes_min_max_sync():
    checkbox_sync, _, spin_box_min, _, spin_box_max = wl_boxes.wl_spin_boxes_min_max_sync(main, double = True)

    checkbox_sync.setChecked(True)
    spin_box_min.setValue(100)
    spin_box_max.setValue(100)

    wl_boxes.wl_spin_boxes_min_max_sync(main, double = False)

def test_wl_spin_boxes_min_max_sync_window():
    checkbox_sync, _, spin_box_left, _, spin_box_right = wl_boxes.wl_spin_boxes_min_max_sync_window(main)

    checkbox_sync.setChecked(True)
    spin_box_left.setValue(100)
    spin_box_right.setValue(100)

    wl_boxes.wl_spin_boxes_min_max_sync_window(main)

def test_wl_spin_boxes_min_max_no_limit():
    (
        _,
        _, _, checkbox_min_no_limit,
        _, _, checkbox_max_no_limit
    ) = wl_boxes.wl_spin_boxes_min_max_no_limit(main, double = True, sync = True)

    checkbox_min_no_limit.setChecked(True)
    checkbox_min_no_limit.setChecked(False)
    checkbox_max_no_limit.setChecked(True)
    checkbox_max_no_limit.setChecked(False)

    wl_boxes.wl_spin_boxes_min_max_no_limit(main, double = False, sync = False)

if __name__ == '__main__':
    test_wl_combo_box()
    test_wl_combo_box_adjustable()
    test_wl_combo_box_enums()
    test_wl_combo_box_yes_no()
    test_wl_combo_box_lang()
    test_wl_combo_box_encoding()
    test_wl_combo_box_measure()
    test_wl_combo_box_file_to_filter()
    test_wl_combo_box_file()
    test_wl_combo_box_font_family()

    test_wl_spin_box()
    test_wl_spin_box_window()
    test_wl_spin_box_font_size()
    test_wl_spin_box_font_weight()

    test_wl_double_spin_box()
    test_wl_double_spin_box_alpha()

    test_wl_spin_box_no_limit()
    test_wl_spin_boxes_min_max()
    test_wl_spin_boxes_min_max_sync()
    test_wl_spin_boxes_min_max_sync_window()
    test_wl_spin_boxes_min_max_no_limit()
