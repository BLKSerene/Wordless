# ----------------------------------------------------------------------
# Tests: Results - Search
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
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_texts
from wordless.wl_results import wl_results_search

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog_results_search():
    table = wl_test_init.Wl_Test_Table(main, tab = 'concordancer')
    table.settings['file_area']['files_open'] = [{'selected': True, 'lang': 'test'}]

    dialog = wl_results_search.Wl_Dialog_Results_Search(
        main,
        table = table
    )

    dialog.load_settings(defaults = True)
    dialog.load_settings(defaults = False)

    dialog.line_edit_search_term.setText('')
    dialog.settings_changed()
    dialog.line_edit_search_term.setText('test')
    dialog.settings_changed()

    dialog.multi_search_mode_changed()
    dialog.table_item_changed()

    for row in range(2):
        table.set_label(row, 0, 'test')
        table.set_item(row, 1, 'test')
        table.set_item(row, 2, 'test')
        table.set_item(row, 3, 'test')

    table.model().item(0, 1).tokens_search = [wl_texts.Wl_Token('test')]

    table.selectRow(0)
    dialog.find_next()
    dialog.find_next()
    table.clearSelection()
    dialog.find_next()

    dialog.find_prev()
    dialog.find_prev()
    table.clearSelection()
    dialog.find_prev()

    dialog.items_found.clear()
    dialog.find_all()
    dialog.worker_results_search.stop()

    dialog.update_gui('')
    dialog.items_found.clear()
    dialog.update_gui('')

    dialog.items_found = [(table, 0, 0)]
    dialog.clr_highlights()
    dialog.clr_history()

def test_wl_worker_results_search():
    table = wl_test_init.Wl_Test_Table(main, tab = 'concordancer')
    table.headers_int = {2}
    table.settings['file_area']['files_open'] = [{'selected': True, 'lang': 'test'}]
    table.settings['concordancer']['search_settings']['search_term'] = 'test'

    for row in range(2):
        table.set_label(row, 0, 'test')
        table.set_item(row, 1, 'test')
        table.set_item(row, 2, 'test')
        table.set_item(row, 3, 'test')

    table.model().item(0, 1).tokens_search = [wl_texts.Wl_Token('test')]
    table.selectRow(0)

    dialog = wl_results_search.Wl_Dialog_Results_Search(
        main,
        table = table
    )
    dialog.settings['search_term'] = 'test'

    worker = wl_results_search.Wl_Worker_Results_Search(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, ''),
        dialog = dialog
    )
    worker.run()
    worker.stop()
    worker.run()

if __name__ == '__main__':
    test_wl_dialog_results_search()
    test_wl_worker_results_search()
