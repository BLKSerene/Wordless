# ----------------------------------------------------------------------
# Wordless: Tests - N-gram Generator
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
from wl_tests import wl_test_file_area, wl_test_init

import wl_ngram_generator

main = wl_test_init.Wl_Test_Main()

wl_test_file_area.wl_test_file_area(main)

def test_ngram_generator():
    time_start_total = time.time()

    print('Start testing module N-gram Generator...')

    # Exhaust all n-grams
    main.settings_custom['ngram_generator']['search_settings']['search_settings'] = False

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        wl_ngram_generator.Wl_Worker_Ngram_Generator_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(err_msg, ngrams_freq_files, ngrams_stats_files, ngrams_text):
    assert not err_msg

    assert ngrams_freq_files
    assert ngrams_stats_files
    assert ngrams_text
    assert len(ngrams_freq_files) == len(ngrams_stats_files) == len(ngrams_text)

    for ngram, freq_files in ngrams_freq_files.items():
        stats_files = ngrams_stats_files[ngram]

        # N-gram
        assert ngram
        assert ngrams_text[ngram]
        # Frequency
        assert freq_files
        # Dispersion & Adjusted Frequency
        assert stats_files

if __name__ == '__main__':
    test_ngram_generator()
