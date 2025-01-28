# ----------------------------------------------------------------------
# Tests: Work Area - Concordancer
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
from wordless import wl_concordancer
from wordless.wl_dialogs import wl_dialogs_misc

main_global = None

def test_concordancer():
    main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

    settings = main.settings_custom['concordancer']

    settings['search_settings']['multi_search_mode'] = True
    settings['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

    for i in range(2 + len(glob.glob('tests/files/file_area/misc/*.txt'))):
        match i:
            # Single file
            case 0:
                settings['generation_settings']['calc_sentiment_scores'] = False

                wl_test_init.select_test_files(main, no_files = [0])
            # Multiple files
            case 1:
                settings['generation_settings']['calc_sentiment_scores'] = True

                wl_test_init.select_test_files(main, no_files = [1, 2])
            # Miscellaneous
            case _:
                settings['generation_settings']['calc_sentiment_scores'] = True

                wl_test_init.select_test_files(main, no_files = [i + 1])

        global main_global
        main_global = main

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")

        wl_concordancer.Wl_Worker_Concordancer_Table(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui_table
        ).run()
        wl_concordancer.Wl_Worker_Concordancer_Fig(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui_fig
        ).run()

def update_gui_table(err_msg, concordance_lines):
    print(err_msg)
    assert not err_msg
    assert concordance_lines

    file_names_selected = list(main_global.wl_file_area.get_selected_file_names())

    for concordance_line in concordance_lines:
        assert len(concordance_line) == 9

        left_tokens_raw, left_tokens_search = concordance_line[0]
        node_tokens_raw, node_tokens_search = concordance_line[1]
        right_tokens_raw, right_tokens_search = concordance_line[2]

        sentiment = concordance_line[3]
        no_token, len_tokens = concordance_line[4]
        no_sentence_seg, len_sentence_segs = concordance_line[5]
        no_sentence, len_sentences = concordance_line[6]
        no_para, len_paras = concordance_line[7]
        file_name = concordance_line[8]

        # Node
        assert node_tokens_raw
        assert node_tokens_search

        # Left & Right
        assert left_tokens_raw or right_tokens_raw
        assert left_tokens_raw == [] or all(left_tokens_raw)
        assert right_tokens_raw == [] or all(right_tokens_raw)
        assert left_tokens_search or right_tokens_search
        assert left_tokens_search == [] or all(left_tokens_search)
        assert right_tokens_search == [] or all(right_tokens_search)

        # Sentiment
        if main_global.settings_custom['concordancer']['generation_settings']['calc_sentiment_scores']:
            if file_name == '[other] No language support':
                assert sentiment == 'No language support'
            else:
                assert -1 <= sentiment <= 1
        else:
            assert sentiment is None

        # Token No.
        assert no_token >= 1
        assert len_tokens >= 1
        # Sentence Segment No.
        assert no_sentence_seg >= 1
        assert len_sentence_segs >= 1
        # Sentence No.
        assert no_sentence >= 1
        assert len_sentences >= 1
        # Paragraph No.
        assert no_para >= 1
        assert len_paras >= 1
        # File
        assert file_name in file_names_selected

def update_gui_fig(err_msg, points, labels):
    assert not err_msg
    assert points
    assert len(labels) == 5

    for point in points:
        assert len(point) == 2

if __name__ == '__main__':
    test_concordancer()
