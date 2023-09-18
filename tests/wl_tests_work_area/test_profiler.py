# ----------------------------------------------------------------------
# Wordless: Tests - Work area - Profiler
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import numpy
import scipy

from tests import wl_test_init
from wordless import wl_profiler
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_utils import wl_misc

main = wl_test_init.Wl_Test_Main()

def test_profiler():
    for i in range(2):
        # Single file
        if i % 2 == 0:
            wl_test_init.select_random_files(main, num_files = 1)
        # Multiple files
        elif i % 2 == 1:
            wl_test_init.select_random_files(main, num_files = 2)

        files_selected = [
            re.search(r'(?<=\)\. ).+?$', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        print(f"Files: {' | '.join(files_selected)}")

        wl_profiler.Wl_Worker_Profiler_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui,
            profiler_tab = 'all'
        ).run()

    main.app.quit()

def update_gui(err_msg, texts_stats_files):
    print(err_msg)
    assert not err_msg

    assert len(texts_stats_files) >= 1

    count_sentences_lens = []
    count_sentence_segs_lens = []
    count_tokens_lens_syls = []
    count_tokens_lens_chars = []

    files = main.settings_custom['file_area']['files_open']

    for i, stats in enumerate(texts_stats_files):
        stats_readability = stats[0]
        len_paras_sentences = numpy.array(stats[1])
        len_paras_sentence_segs = numpy.array(stats[2])
        len_paras_tokens = numpy.array(stats[3])
        len_sentences = numpy.array(stats[4])
        len_sentence_segs = numpy.array(stats[5])
        len_tokens_syls = numpy.array(stats[6])
        len_tokens_chars = numpy.array(stats[7])
        len_types_syls = numpy.array(stats[8])
        len_types_chars = numpy.array(stats[9])
        len_syls = numpy.array(stats[10])
        stats_lexical_diversity = stats[11]

        count_paras = len(len_paras_sentences)
        count_sentences = len(len_sentences)
        count_sentence_segs = len(len_sentence_segs)
        count_tokens = len(len_tokens_chars)
        count_types = len(len_types_chars)
        count_syls = len(len_syls)
        count_chars = numpy.sum(len_tokens_chars)

        count_sentences_lens.append(collections.Counter(len_sentences))
        count_sentence_segs_lens.append(collections.Counter(len_sentence_segs))
        count_tokens_lens_syls.append(collections.Counter(len_tokens_syls))
        count_tokens_lens_chars.append(collections.Counter(len_tokens_chars))

        assert len(stats_readability) == 39

        for i, readability in enumerate(stats_readability):
            assert readability

        # Counts
        assert count_paras
        assert count_sentences
        assert count_sentence_segs
        assert count_tokens
        assert count_types
        assert count_syls
        assert count_chars

        # Lengths
        assert len_paras_sentences.size
        assert len_paras_sentence_segs.size
        assert len_paras_tokens.size
        assert len_sentences.size
        assert len_sentence_segs.size
        assert len_tokens_syls.size
        assert len_tokens_chars.size
        assert len_types_syls.size
        assert len_types_chars.size
        assert len_syls.size

        if i < len(files):
            lang = re.search(r'(?<=\[)[a-z_]+(?=\])', files[i]['name']).group()

            if lang not in main.settings_global['syl_tokenizers']:
                assert all((len_syls == 1 for len_syls in len_tokens_syls))
                assert all((len_syls == 1 for len_syls in len_types_syls))

        # Lexical Diversity
        assert len(stats_lexical_diversity) == 18

        for i, lexical_diversity in enumerate(stats_lexical_diversity):
            assert lexical_diversity > 0

        # Mean
        assert numpy.mean(len_paras_sentences) == count_sentences / count_paras
        assert numpy.mean(len_paras_sentence_segs) == count_sentence_segs / count_paras
        assert numpy.mean(len_paras_tokens) == count_tokens / count_paras
        assert numpy.mean(len_sentences) == count_tokens / count_sentences
        assert numpy.mean(len_sentence_segs) == count_tokens / count_sentence_segs
        assert numpy.mean(len_tokens_syls) == count_syls / count_tokens
        assert numpy.mean(len_tokens_chars) == count_chars / count_tokens

        # Range and interquartile range
        for lens in [
            len_paras_sentences,
            len_paras_sentence_segs,
            len_paras_tokens,
            len_sentences,
            len_sentence_segs,
            len_tokens_syls,
            len_tokens_chars
        ]:
            assert numpy.ptp(lens) == max(lens) - min(lens)
            assert scipy.stats.iqr(lens) == numpy.percentile(lens, 75) - numpy.percentile(lens, 25)

    # Count of n-token-long Sentences
    if any(count_sentences_lens):
        count_sentences_lens_files = wl_misc.merge_dicts(count_sentences_lens)
        count_sentences_lens = sorted(count_sentences_lens_files.keys())

        # The total of counts of n-token-long sentences should be equal to the count of tokens
        for i, stats in enumerate(texts_stats_files):
            len_sentences_total = sum((
                count_sentences_files[i] * len_sentence
                for len_sentence, count_sentences_files in count_sentences_lens_files.items()
            ))

            assert len_sentences_total == numpy.sum(stats[3])

        # Sentence length should never be zero
        assert 0 not in count_sentences_lens

    # Count of n-token-long Sentence Segments
    if any(count_sentence_segs_lens):
        count_sentence_segs_lens_files = wl_misc.merge_dicts(count_sentence_segs_lens)
        count_sentence_segs_lens = sorted(count_sentence_segs_lens_files.keys())

        # The total of counts of n-token-long sentence segments should be equal to the count of tokens
        for i, stats in enumerate(texts_stats_files):
            len_sentence_segs_total = sum((
                count_sentence_segs_files[i] * len_sentence_seg
                for len_sentence_seg, count_sentence_segs_files in count_sentence_segs_lens_files.items()
            ))

            assert len_sentence_segs_total == numpy.sum(stats[3])

        # Sentence segment length should never be zero
        assert 0 not in count_sentence_segs_lens

    # Count of n-syllable-long Tokens
    if any(count_tokens_lens_syls):
        count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens_syls)
        count_tokens_lens_syls = sorted(count_tokens_lens_files.keys())

        # The total of counts of n-syllable-long tokens should be equal to the count of characters
        for i, stats in enumerate(texts_stats_files):
            len_tokens_total = sum((
                count_tokens_files[i] * len_token
                for len_token, count_tokens_files in count_tokens_lens_files.items()
            ))

            assert len_tokens_total == numpy.sum(stats[6])

        # Token length should never be zero
        assert 0 not in count_tokens_lens_syls

    # Count of n-character-long Tokens
    if any(count_tokens_lens_chars):
        count_tokens_lens_files = wl_misc.merge_dicts(count_tokens_lens_chars)
        count_tokens_lens_chars = sorted(count_tokens_lens_files.keys())

        # The total of counts of n-character-long tokens should be equal to the count of characters
        for i, stats in enumerate(texts_stats_files):
            len_tokens_total = sum((
                count_tokens_files[i] * len_token
                for len_token, count_tokens_files in count_tokens_lens_files.items()
            ))

            assert len_tokens_total == numpy.sum(stats[7])

        # Token length should never be zero
        assert 0 not in count_tokens_lens_chars

if __name__ == '__main__':
    test_profiler()
