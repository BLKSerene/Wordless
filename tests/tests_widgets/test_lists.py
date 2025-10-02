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

from PyQt5 import QtCore
from PyQt5 import QtGui

from tests import wl_test_init
from wordless.wl_widgets import wl_lists

main = wl_test_init.Wl_Test_Main()

def test_wl_list_add_ins_del_clr():
    list_add_ins_del_clr_editable = wl_lists.Wl_List_Add_Ins_Del_Clr(main, editable = True, drag_drop = True)
    list_add_ins_del_clr = wl_lists.Wl_List_Add_Ins_Del_Clr(main, editable = False)
    list_add_ins_del_clr.items_old = ['test']

    list_add_ins_del_clr.model().setStringList(('test', 'test'))
    list_add_ins_del_clr.selectAll()
    list_add_ins_del_clr.dropEvent(QtGui.QDropEvent(QtCore.QPointF(100, 100), QtCore.Qt.MoveAction, QtCore.QMimeData(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.dropEvent(QtGui.QDropEvent(QtCore.QPointF(10, 10), QtCore.Qt.MoveAction, QtCore.QMimeData(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier))

    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Home, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.clearSelection()
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Insert, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Delete, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Clear, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Return, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_A, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.selectAll()
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Insert, QtCore.Qt.NoModifier))
    list_add_ins_del_clr.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Return, QtCore.Qt.NoModifier))

    list_add_ins_del_clr_editable.model().setStringList(('test', 'test'))
    list_add_ins_del_clr_editable.selectAll()
    list_add_ins_del_clr_editable.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace, QtCore.Qt.NoModifier))
    list_add_ins_del_clr_editable.keyPressEvent(QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Up, QtCore.Qt.NoModifier))

    list_add_ins_del_clr.model().setStringList([' '])
    list_add_ins_del_clr.items_old = ['test']
    list_add_ins_del_clr.data_changed(topLeft = wl_test_init.wl_test_index(0, 0))
    list_add_ins_del_clr.model().setStringList(['test'])
    list_add_ins_del_clr.data_changed(topLeft = wl_test_init.wl_test_index(0, 0))

    list_add_ins_del_clr.selectionModel().clearSelection()
    list_add_ins_del_clr.selection_changed()
    list_add_ins_del_clr.selectionModel().select(list_add_ins_del_clr.model().index(0, 0), QtCore.QItemSelectionModel.Select)
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

if __name__ == '__main__':
    test_wl_list_add_ins_del_clr()
    test_wl_list_add_ins_del_clr_imp_exp()
