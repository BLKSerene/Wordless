# ----------------------------------------------------------------------
# Wordless: Tests - Overview
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

import collections
import re
import sys
import time

sys.path.append('.')

import numpy
import pytest

from wl_dialogs import wl_dialog_misc
from wl_tests import wl_test_file_area, wl_test_init
from wl_utils import wl_misc

import wl_overview

main = wl_test_init.Wl_Test_Main()

wl_test_file_area.wl_test_file_area(main)

def test_overview():
    time_start_total = time.time()

    print('Start testing Overview...')

    for i, file_test in enumerate(main.settings_custom['file_area']['files_open']):
        for file in main.settings_custom['file_area']['files_open']:
            file['selected'] = False

        main.settings_custom['file_area']['files_open'][i]['selected'] = True
        # Record current file name
        main.settings_custom['file_cur'] = file_test['name']

        print(f'''Testing file "{file_test['name']}"... ''', end = '')

        time_start = time.time()

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Process_Data(main)

        worker_overview_table = wl_overview.Wl_Worker_Overview_Table(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui
        )
        worker_overview_table.run()

        print(f'done! (In {round(time.time() - time_start, 2)} seconds)')

    print(f'Testing completed! (In {round(time.time() - time_start_total, 2)} seconds)')

    main.app.quit()

def update_gui(error_msg, texts_stats_files):
    assert not error_msg
    
    count_tokens_lens = []
    count_sentences_lens = []

    assert texts_stats_files

    count_paras_total = len(texts_stats_files[-1][1])
    count_sentences_total = len(texts_stats_files[-1][3])
    count_tokens_total = len(texts_stats_files[-1][5])
    count_types_total = len(texts_stats_files[-1][7])
    count_syls_total = len(texts_stats_files[-1][8])
    count_chars_total = sum(texts_stats_files[-1][5])

    for stats in texts_stats_files:
        readability_statistics = stats[0]
        len_paras_in_sentence = stats[1]
        len_paras_in_token = stats[2]
        len_sentences = stats[3]
        len_tokens_in_syl = stats[4]
        len_tokens_in_char = stats[5]
        len_types_in_syl = stats[6]
        len_types_in_char = stats[7]
        len_syls = stats[8]
        ttr = stats[9]
        sttr = stats[10]

        count_paras = len(len_paras_in_sentence)
        count_sentences = len(len_sentences)
        count_tokens = len(len_tokens_in_char)
        count_types = len(len_types_in_char)
        count_syls = len(len_syls)
        count_chars = sum(len_tokens_in_char)

        count_tokens_lens.append(collections.Counter(len_tokens_in_char))
        count_sentences_lens.append(collections.Counter(len_sentences))

        # Data validation
        file_lang = re.search(r'\[([a-z_]+)\]', main.settings_custom['file_cur']).group(1)

        assert readability_statistics
        for statistic in readability_statistics:
            assert statistic

        assert len_paras_in_sentence
        assert len_paras_in_token
        assert len_sentences

        if file_lang in main.settings_global['syl_tokenizers']:
            assert len_tokens_in_syl
            assert len_types_in_syl
        else:
            assert not len_tokens_in_syl
            assert not len_types_in_syl

        assert len_tokens_in_char
        assert len_types_in_char
        assert ttr
        assert sttr

        assert numpy.mean(len_paras_in_sentence) == count_sentences / count_paras
        assert numpy.mean(len_paras_in_token) == count_tokens / count_paras
        assert numpy.mean(len_sentences) == count_tokens / count_sentences
        if file_lang in main.settings_global['syl_tokenizers']:
            assert numpy.mean(len_tokens_in_syl) == count_syls / count_tokens
        else:
            assert numpy.isnan(numpy.mean(len_tokens_in_syl))
        assert numpy.mean(len_tokens_in_char) == count_chars / count_tokens
        
    # Count of n-length Tokens
    if any(count_tokens_lens):
        count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens)
        count_tokens_lens = sorted(count_tokens_lens_files.keys())

        # The total of counts of n-length tokens should be equal to the count of characters
        for i, stats in enumerate(texts_stats_files):
            len_tokens_total = sum([
                values[i] * key
                for key, values in count_tokens_lens_files.items()
            ])

            assert len_tokens_total == sum(len_tokens_in_char)

        # Token length should never be zero
        assert 0 not in count_tokens_lens

    # Count of n-length Sentences
    if any(count_sentences_lens):
        count_sentences_lens_files = wl_misc.merge_dicts(count_sentences_lens)
        count_sentences_lens = sorted(count_sentences_lens_files.keys())

        # The total of counts of n-length sentences should be equal to the count of tokens
        for i, stats in enumerate(texts_stats_files):
            len_sentences_total = sum([
                values[i] * key
                for key, values in count_sentences_lens_files.items()
            ])

            assert len_sentences_total == len(len_tokens_in_char)

        # Sentence length should never be zero
        assert 0 not in count_sentences_lens
    
if __name__ == '__main__':
    test_overview()
