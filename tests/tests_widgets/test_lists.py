# ----------------------------------------------------------------------
# Tests: Widgets - Lists
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

from PyQt5.QtCore import QItemSelectionModel

from tests import wl_test_init
from wordless.wl_widgets import wl_lists

main = wl_test_init.Wl_Test_Main()

def test_wl_list_add_ins_del_clr():
    wl_lists.Wl_List_Add_Ins_Del_Clr(main, editable = True, drag_drop = True)
    wl_lists.Wl_List_Add_Ins_Del_Clr(main, editable = False)

    list_add_ins_del_clr = wl_lists.Wl_List_Add_Ins_Del_Clr(main)
    list_add_ins_del_clr.items_old = ['test']

    list_add_ins_del_clr.model().setStringList([' '])
    list_add_ins_del_clr.data_changed(topLeft = wl_test_init.wl_test_index(0, 0))
    list_add_ins_del_clr.model().setStringList(['test'])
    list_add_ins_del_clr.data_changed(topLeft = wl_test_init.wl_test_index(0, 0))

    list_add_ins_del_clr.selectionModel().clearSelection()
    list_add_ins_del_clr.selection_changed()
    list_add_ins_del_clr.selectionModel().select(list_add_ins_del_clr.model().index(0, 0), QItemSelectionModel.Select)
    list_add_ins_del_clr.selection_changed()

    list_add_ins_del_clr.get_selected_rows()

    list_add_ins_del_clr._add_item(text = '', row = None)
    list_add_ins_del_clr._add_item(text = 'test', row = 0)

    list_add_ins_del_clr._add_items(['test'], row = None)
    list_add_ins_del_clr._add_items(['test'], row = 0)

    list_add_ins_del_clr.add_item()
    list_add_ins_del_clr.ins_item()
    list_add_ins_del_clr.del_item()
    list_add_ins_del_clr.clr_list()
    list_add_ins_del_clr.load_items(['test'])

def test_wl_list_add_ins_del_clr_imp_exp():
    list_add_ins_del_clr_imp_exp = wl_lists.Wl_List_Add_Ins_Del_Clr_Imp_Exp(
        main,
        new_item_text = 'test',
        settings = 'search_terms',
        exp_file_name = 'test.txt'
    )

    list_add_ins_del_clr_imp_exp.model().setStringList([])
    list_add_ins_del_clr_imp_exp.data_changed()
    list_add_ins_del_clr_imp_exp.model().setStringList(['test'])
    list_add_ins_del_clr_imp_exp.data_changed()

def test_wl_list_search_terms():
    wl_lists.Wl_List_Search_Terms(main)

def test_wl_list_stop_words():
    list_stop_words = wl_lists.Wl_List_Stop_Words(main)
    list_stop_words.data_changed_default()
    list_stop_words.selection_changed_default()
    list_stop_words.switch_to_custom()
    list_stop_words.switch_to_default()

if __name__ == '__main__':
    test_wl_list_add_ins_del_clr()
    test_wl_list_add_ins_del_clr_imp_exp()

    test_wl_list_search_terms()
    test_wl_list_stop_words()
