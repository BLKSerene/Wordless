# ----------------------------------------------------------------------
# Tests: Results - Search in results
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
from wordless.wl_results import wl_results_search

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog_results_search():
    table = wl_test_init.Wl_Test_Table(main, tab = 'dependency_parser')
    table.settings['file_area']['files_open'] = [{'selected': True, 'lang': 'test'}]

    dialog_results_search = wl_results_search.Wl_Dialog_Results_Search(
        main,
        table = table
    )

    dialog_results_search.load_settings(defaults = True)
    dialog_results_search.load_settings(defaults = False)

    dialog_results_search.line_edit_search_term.setText('')
    dialog_results_search.search_settings_changed()
    dialog_results_search.line_edit_search_term.setText('test')
    dialog_results_search.search_settings_changed()

    dialog_results_search.table_item_changed()

    dialog_results_search.find_next()
    dialog_results_search.find_prev()
    dialog_results_search.find_all()
    dialog_results_search.update_gui('')
    dialog_results_search.clr_highlights()
    dialog_results_search.clr_history()

if __name__ == '__main__':
    test_wl_dialog_results_search()
