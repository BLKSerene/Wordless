# ----------------------------------------------------------------------
# Wordless: Tests - Collocation Extractor
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

import time

from wl_dialogs import wl_dialogs_misc
from wl_tests import wl_test_init

import wl_collocation_extractor

main = wl_test_init.Wl_Test_Main()

def test_collocation_extractor():
    time_start_total = time.time()

    print('Start testing module Collocation Extractor...')

    # Exhaust all collocations
    main.settings_custom['collocation_extractor']['search_settings']['search_settings'] = False

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        wl_collocation_extractor.Wl_Worker_Collocation_Extractor_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(err_msg, collocations_freqs_files, collocations_stats_files, nodes_text):
    assert not err_msg

    assert collocations_freqs_files
    assert collocations_stats_files
    assert nodes_text
    assert len(collocations_freqs_files) == len(collocations_stats_files)

    for (node, collocate), stats_files in collocations_stats_files.items():
        freqs_files = collocations_freqs_files[(node, collocate)]

        # Node
        assert node
        assert nodes_text[node]
        # Collocate
        assert collocate
        # Frequency
        assert freqs_files
        # Statistics
        assert stats_files

if __name__ == '__main__':
    test_collocation_extractor()
