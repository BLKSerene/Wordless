#
# Wordless: Tests - Overview
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import collections
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
    time_start = time.time()

    print('Start testing Overview...')

    files = main.wl_files.get_selected_files()

    dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Process_Data(main)

    worker_overview_table = wl_overview.Wl_Worker_Overview_Table(
        main,
        dialog_progress = dialog_progress,
        update_gui = update_gui
    )
    worker_overview_table.run()

    print(f'Testing of Overview has been completed! (In {round(time.time() - time_start, 2)} seconds)')

def update_gui(texts_stats_files):
    count_tokens_lens = []
    count_sentences_lens = []

    count_paras_total = len(texts_stats_files[-1][0])
    count_sentences_total = len(texts_stats_files[-1][2])
    count_tokens_total = len(texts_stats_files[-1][3])
    count_types_total = len(texts_stats_files[-1][4])
    count_chars_total = sum(texts_stats_files[-1][3])

    for stats in texts_stats_files:
        len_paras_in_sentence = stats[0]
        len_paras_in_token = stats[1]
        len_sentences = stats[2]
        len_tokens = stats[3]
        len_types = stats[4]
        ttr = stats[5]
        sttr = stats[6]

        count_paras = len(len_paras_in_sentence)
        count_sentences = len(len_sentences)
        count_tokens = len(len_tokens)
        count_types = len(len_types)
        count_chars = sum(len_tokens)

        count_tokens_lens.append(collections.Counter(len_tokens))
        count_sentences_lens.append(collections.Counter(len_sentences))

        # Data validation
        assert numpy.mean(len_paras_in_sentence) == count_sentences / count_paras
        assert numpy.mean(len_paras_in_token) == count_tokens / count_paras
        assert numpy.mean(len_sentences) == count_tokens / count_sentences
        assert numpy.mean(len_tokens) == count_chars / count_tokens
        
    # Count of n-length Tokens
    if any(count_tokens_lens):
        count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens)
        count_tokens_lens = sorted(count_tokens_lens_files.keys())

        # The total of counts of n-length tokens should be equal to the count of characters
        for i, stats in enumerate(texts_stats_files):
            len_tokens_total = sum([values[i] * key
                                    for key, values in count_tokens_lens_files.items()])

            assert len_tokens_total == sum(stats[3])

        # Token length should never be zero
        assert 0 not in count_tokens_lens

    # Count of n-length Sentences
    if any(count_sentences_lens):
        count_sentences_lens_files = wl_misc.merge_dicts(count_sentences_lens)
        count_sentences_lens = sorted(count_sentences_lens_files.keys())

        # The total of counts of n-length sentences should be equal to the count of tokens
        for i, stats in enumerate(texts_stats_files):
            len_sentences_total = sum([values[i] * key
                                       for key, values in count_sentences_lens_files.items()])

            assert len_sentences_total == len(stats[3])

        # Sentence length should never be zero
        assert 0 not in count_sentences_lens
    
if __name__ == '__main__':
    test_overview()
