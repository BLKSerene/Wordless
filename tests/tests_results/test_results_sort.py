# ----------------------------------------------------------------------
# Tests: Results - Sort
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

from tests import wl_test_init
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_results import (
    wl_results_search,
    wl_results_sort
)

main = wl_test_init.Wl_Test_Main()

table = wl_test_init.Wl_Test_Table(main, tab = 'concordancer')
table.dialog_results_search = wl_results_search.Wl_Dialog_Results_Search(
    main,
    table = table
)

for i in range(13):
    table.set_label(0, i, 'test')

def test_wl_dialog_results_sort_concordancer():
    dialog = wl_results_sort.Wl_Dialog_Results_Sort_Concordancer(
        main,
        table = table
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)

    dialog.sort()
    dialog.worker_results_sort_concordancer.stop()

    table.settings['concordancer']['generation_settings']['calc_sentiment_scores'] = True
    table.headers_float = {3}

    dialog.settings['sorting_rules'] = [
        ['Node', 'Ascending'],
        ['Sentiment', 'Ascending'],
        ['Token No.', 'Ascending'],
        ['Sentence Segment No.', 'Ascending'],
        ['Sentence No.', 'Ascending'],
        ['Paragraph No.', 'Ascending'],
        ['File', 'Ascending'],
        ['R1', 'Ascending'],
        ['L1', 'Ascending']
    ]

    for col in range(3):
        table.set_label(0, col, 'test')

    dialog.update_gui(
        '',
        [[table.indexWidget(table.model().index(0, col)) for col in range(3)] + [0.1] + ['test'] * 9]
    )
    dialog.update_gui(
        '',
        [[table.indexWidget(table.model().index(0, col)) for col in range(3)] + ['test'] * 10]
    )
    dialog.update_gui(
        '',
        [[table.indexWidget(table.model().index(0, col)) for col in range(3)] + [None] * 10]
    )

def test_table_results_sort_concordancer():
    table_results_sort = wl_results_sort.Wl_Table_Results_Sort_Conordancer(
        main,
        table = table
    )

    table_results_sort._add_row(texts = ['test', 'Ascending'])
    table_results_sort.cols_to_sort.clear()
    table_results_sort.item_changed(table_results_sort.model().item(0, 0))
    table_results_sort.cols_to_sort = table_results_sort.cols_to_sort_default.copy()
    table_results_sort.item_changed(table_results_sort.model().item(0, 0))

    table_results_sort.selectionModel().clearSelection()
    table_results_sort.selection_changed()
    table_results_sort.selectionModel().select(
        table_results_sort.model().index(0, 0),
        QtCore.QItemSelectionModel.Select
    )
    table_results_sort.model().setRowCount(2)
    table_results_sort.selection_changed()

    table_results_sort.table_item_changed()
    table.set_label(0, 0, 'test')
    table.set_label(0, 2, 'test')

    main.settings_custom['concordancer']['results_sort']['sorting_rules'] = [['Node', 'Ascending']]
    table.settings['concordancer']['generation_settings']['context_len_unit'] = 'Token'
    table_results_sort.table_item_changed()
    table.settings['concordancer']['generation_settings']['context_len_unit'] = 'Sentence'
    table_results_sort.table_item_changed()

    table_results_sort.cols_to_sort = []
    table_results_sort.max_left()
    table_results_sort.cols_to_sort = ['L1']
    table_results_sort.max_left()
    table_results_sort.cols_to_sort = []
    table_results_sort.max_right()
    table_results_sort.cols_to_sort = ['R1']
    table_results_sort.max_right()

    table_results_sort._add_row(texts = None)
    table_results_sort.cols_to_sort = ['R1', 'R2', 'L1', 'L2']
    table_results_sort._add_row(texts = ['R1', 'Ascending'])
    table_results_sort._add_row(texts = None)
    table_results_sort._add_row(texts = None)
    table_results_sort._add_row(texts = None)
    table_results_sort._add_row(row = 0)

    table_results_sort.load_settings(defaults = True)
    table_results_sort.load_settings(defaults = False)

def test_wl_worker_results_sort_concordancer():
    dialog = wl_results_sort.Wl_Dialog_Results_Sort_Concordancer(
        main,
        table = table
    )
    worker = wl_results_sort.Wl_Worker_Results_Sort_Concordancer(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )

    main.settings_custom['concordancer']['results_sort']['sorting_rules'] = [
        ['Node', 'Ascending'],
        ['Sentiment', 'Ascending'],
        ['Token No.', 'Ascending'],
        ['Sentence Segment No.', 'Ascending'],
        ['Sentence No.', 'Ascending'],
        ['Paragraph No.', 'Ascending'],
        ['File', 'Ascending'],
        ['L1', 'Ascending'],
        ['R1', 'Ascending']
    ]
    dialog.table_sort.cols_to_sort = ['R1', 'R2', 'L1', 'L2']
    worker.run()

    table.settings['concordancer']['generation_settings']['calc_sentiment_scores'] = True
    worker.run()

    table.headers_float = {3}
    table.set_item(0, 3, 'test', val = 0.123456789)
    worker.run()

    worker.stop()
    worker.run()

if __name__ == '__main__':
    test_wl_dialog_results_sort_concordancer()
    test_table_results_sort_concordancer()
    test_wl_worker_results_sort_concordancer()
