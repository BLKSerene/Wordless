# ----------------------------------------------------------------------
# Tests: Results - Sort results
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
from wordless.wl_results import wl_results_search, wl_results_sort

main = wl_test_init.Wl_Test_Main()
table = wl_test_init.Wl_Test_Table(main, tab = 'concordancer')
table.dialog_results_search = wl_results_search.Wl_Dialog_Results_Search(
    main,
    table = table
)

def test_wl_dialog_results_sort_concordancer():
    dialog_results_sort_concordancer = wl_results_sort.Wl_Dialog_Results_Sort_Concordancer(
        main,
        table = table
    )

    dialog_results_sort_concordancer.load_settings(defaults = True)
    dialog_results_sort_concordancer.load_settings(defaults = False)

    main.settings_custom['concordancer']['sort_results']['sorting_rules'] = [
        ['Node', 'Ascending'],
        ['Sentiment', 'Ascending'],
        ['Token No.', 'Ascending'],
        ['File', 'Ascending'],
        ['R1', 'Ascending'],
        ['L1', 'Ascending']
    ]
    dialog_results_sort_concordancer.sort_results()
    dialog_results_sort_concordancer.update_gui([], '')

def test_table_results_sort_concordancer():
    table_results_sort_concordancer = wl_results_sort.Wl_Table_Results_Sort_Conordancer(
        main,
        table = table
    )

    table_results_sort_concordancer._add_row(texts = ['test', 'Ascending'])
    table_results_sort_concordancer.cols_to_sort.clear()
    table_results_sort_concordancer.item_changed(table_results_sort_concordancer.model().item(0, 0))
    table_results_sort_concordancer.cols_to_sort = table_results_sort_concordancer.cols_to_sort_default.copy()
    table_results_sort_concordancer.item_changed(table_results_sort_concordancer.model().item(0, 0))

    table_results_sort_concordancer.selectionModel().clearSelection()
    table_results_sort_concordancer.selection_changed()
    table_results_sort_concordancer.selectionModel().select(
        table_results_sort_concordancer.model().index(0, 0),
        QItemSelectionModel.Select
    )
    table_results_sort_concordancer.model().setRowCount(2)
    table_results_sort_concordancer.selection_changed()

    table_results_sort_concordancer.table_item_changed()
    table.set_label(0, 0, 'test')
    table.set_label(0, 2, 'test')

    main.settings_custom['concordancer']['sort_results']['sorting_rules'] = [['Node', 'Ascending']]
    table.settings['concordancer']['generation_settings']['context_len_unit'] = 'Token'
    table_results_sort_concordancer.table_item_changed()
    table.settings['concordancer']['generation_settings']['context_len_unit'] = 'Sentence'
    table_results_sort_concordancer.table_item_changed()

    table_results_sort_concordancer.cols_to_sort = []
    table_results_sort_concordancer.max_left()
    table_results_sort_concordancer.cols_to_sort = ['L1']
    table_results_sort_concordancer.max_left()
    table_results_sort_concordancer.cols_to_sort = []
    table_results_sort_concordancer.max_right()
    table_results_sort_concordancer.cols_to_sort = ['R1']
    table_results_sort_concordancer.max_right()

    table_results_sort_concordancer._add_row(texts = None)
    table_results_sort_concordancer.cols_to_sort = ['R1', 'R2', 'L1', 'L2']
    table_results_sort_concordancer._add_row(texts = ['R1', 'Ascending'])
    table_results_sort_concordancer._add_row(texts = None)
    table_results_sort_concordancer._add_row(texts = None)
    table_results_sort_concordancer._add_row(texts = None)
    table_results_sort_concordancer._add_row(row = 0)

    table_results_sort_concordancer.load_settings(defaults = True)
    table_results_sort_concordancer.load_settings(defaults = False)

if __name__ == '__main__':
    test_wl_dialog_results_sort_concordancer()
    test_table_results_sort_concordancer()
