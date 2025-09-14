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

from tests import wl_test_init
from wordless import wl_concordancer_parallel
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_texts

main_global = None

def test_concordancer_parallel():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['concordancer_parallel']

    for i in range(2):
        match i:
            case 0:
                settings['search_settings']['multi_search_mode'] = True
                settings['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

                wl_test_init.select_test_files(main, no_files = (0, 1, 2))
            case 1:
                settings['search_settings']['multi_search_mode'] = False
                settings['search_settings']['search_term'] = ''

                wl_test_init.select_test_files(main, no_files = (8, 9, 10))

        global main_global
        main_global = main

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")

        worker_concordancer_parallel = wl_concordancer_parallel.Wl_Worker_Concordancer_Parallel_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
        )

        worker_concordancer_parallel.finished.connect(update_gui)
        worker_concordancer_parallel.run()

def update_gui(err_msg, parallel_units, num_paras_max):
    print(err_msg)
    assert not err_msg
    assert parallel_units

    files_selected = list(main_global.wl_file_area.get_selected_files())

    # Test whether empty parallel units are removed
    if files_selected[0]['name'] == '[eng_us] Empty search term - src':
        assert parallel_units == [
            (4, [
                [
                    ['Omitted', 'source', 'text. (', 'without', 'corresponding', 'translation).'],
                    wl_texts.to_tokens(['Omitted', 'source', 'text.', ' (', 'without', 'corresponding', 'translation', ').'])
                ],
                [[], []],
                [[], []]
            ]),
            (5, [
                [[], []],
                [
                    ['Added', 'target', 'text (', 'without', 'corresponding', 'originals).'],
                    wl_texts.to_tokens(['Added', 'target', 'text', ' (', 'without', 'corresponding', 'originals', ').'])
                ],
                [[], []]
            ])
        ]
    else:
        for parallel_unit_no, parallel_units_files in parallel_units:
            # Parallel Unit No.
            assert 1 <= parallel_unit_no <= num_paras_max

            # Parallel Units
            for parallel_unit in parallel_units_files:
                assert len(parallel_unit) == 2

if __name__ == '__main__':
    test_concordancer_parallel()
