# ----------------------------------------------------------------------
# Wordless: Tests - Work Area - Parallel Concordancer
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import random
import re

from tests import wl_test_init
from wordless import wl_concordancer_parallel
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

main.settings_custom['concordancer_parallel']['search_settings']['multi_search_mode'] = True
main.settings_custom['concordancer_parallel']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

def test_concordancer_parallel():
    print('Start testing module Parallel Concordancer...')

    files = main.settings_custom['file_area']['files_open']

    for i in range(2):
        for file in files:
            file['selected'] = False

        files_parallel = random.sample(files, 2)

        for file in files_parallel:
            file['selected'] = True # pylint: disable=unsupported-assignment-operation

        main.settings_custom['concordancer_parallel']['generation_settings']['src_file'] = files_parallel[0]['name'] # pylint: disable=unsubscriptable-object
        main.settings_custom['concordancer_parallel']['generation_settings']['tgt_file'] = files_parallel[1]['name'] # pylint: disable=unsubscriptable-object

        files_selected = [
            re.search(r'(?<=\[)[a-z_]+(?=\])', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        print(f'[Test Round {i + 1}]')
        print(f"Files: {', '.join(files_selected)}\n")

        wl_concordancer_parallel.Wl_Worker_Concordancer_Parallel_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

    print('All pass!')

    main.app.quit()

def update_gui(err_msg, concordance_lines):
    assert not err_msg
    assert concordance_lines

    for concordance_line in concordance_lines:
        node_text, node_text_raw, node_text_search = concordance_line[1]

        no_seg, len_segs = concordance_line[3]

        # Node
        assert node_text
        assert node_text_raw
        assert node_text_search

        # Segment No.
        assert no_seg >= 0
        assert len_segs >= 1

if __name__ == '__main__':
    test_concordancer_parallel()
