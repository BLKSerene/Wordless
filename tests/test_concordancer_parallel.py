# ----------------------------------------------------------------------
# Tests: Work Area - Parallel Concordancer
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

import glob

from tests import wl_test_init
from wordless import wl_concordancer_parallel
from wordless.wl_dialogs import wl_dialogs_misc

def test_concordancer_parallel():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['concordancer_parallel']

    settings['search_settings']['multi_search_mode'] = True
    settings['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

    for i in range(2):
        match i:
            case 0:
                wl_test_init.select_test_files(main, no_files = [0, 1, 2])
            case 1:
                wl_test_init.select_test_files(
                    main,
                    no_files = list(range(1, 3 + len(glob.glob('tests/files/file_area/misc/*.txt'))))
                )

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")

        wl_concordancer_parallel.Wl_Worker_Concordancer_Parallel_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

def update_gui(err_msg, concordance_lines):
    print(err_msg)
    assert not err_msg
    assert concordance_lines

    for concordance_line in concordance_lines:
        assert len(concordance_line) == 2

        parallel_unit_no, len_parallel_units = concordance_line[0]

        # Parallel Unit No.
        assert parallel_unit_no >= 1
        assert len_parallel_units >= 1

        # Parallel Units
        for parallel_unit in concordance_line[1]:
            assert len(parallel_unit) == 2

if __name__ == '__main__':
    test_concordancer_parallel()
