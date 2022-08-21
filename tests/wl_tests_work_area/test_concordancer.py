# ----------------------------------------------------------------------
# Wordless: Tests - Work Area - Concordancer
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
from wordless import wl_concordancer
from wordless.wl_dialogs import wl_dialogs_misc

main = wl_test_init.Wl_Test_Main()

main.settings_custom['concordancer']['search_settings']['multi_search_mode'] = True
main.settings_custom['concordancer']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

def test_concordancer():
    print('Start testing module Concordancer...')

    files = main.settings_custom['file_area']['files_open']

    for i in range(2):
        for file in files:
            file['selected'] = False

        # Single file
        if i == 0:
            random.choice(files)['selected'] = True
        # Multiple files
        elif i == 1:
            for file in random.sample(files, 2):
                file['selected'] = True # pylint: disable=unsupported-assignment-operation

        files_selected = [
            re.search(r'(?<=\[)[a-z_]+(?=\])', file_name).group()
            for file_name in main.wl_file_area.get_selected_file_names()
        ]

        print(f'[Test Round {i + 1}]')
        print(f"Files: {', '.join(files_selected)}\n")

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

    print('All pass!')

    main.app.quit()

def update_gui_table(err_msg, concordance_lines):
    assert not err_msg
    assert concordance_lines

    file_names = list(main.wl_file_area.get_selected_file_names())

    for concordance_line in concordance_lines:
        left_text, left_text_raw, left_text_search = concordance_line[0]
        node_text, node_text_raw, node_text_search = concordance_line[1]
        right_text, right_text_raw, right_text_search = concordance_line[2]

        sentiment = concordance_line[3]
        no_token, len_tokens = concordance_line[4]
        no_sentence_seg, len_sentence_segs = concordance_line[5]
        no_sentence, len_sentences = concordance_line[6]
        no_para, len_paras = concordance_line[7]
        file_name = concordance_line[8]

        # Left
        assert left_text
        assert left_text_raw
        assert left_text_search
        # Node
        assert node_text
        assert node_text_raw
        assert node_text_search
        # Right
        assert right_text
        assert right_text_raw
        assert right_text_search

        # Sentiment
        assert sentiment == 'No Support' or -1 <= sentiment <= 1
        # Token No.
        assert no_token >= 0
        assert len_tokens >= 1
        # Sentence Segment No.
        assert no_sentence_seg >= 0
        assert len_sentence_segs >= 1
        # Sentence No.
        assert no_sentence >= 0
        assert len_sentences >= 1
        # Paragraph No.
        assert no_para >= 0
        assert len_paras >= 1
        # File
        assert file_name in file_names

def update_gui_fig(err_msg, points, labels):
    assert not err_msg
    assert points
    assert len(labels) == 5

    for point in points:
        assert len(point) == 2

if __name__ == '__main__':
    test_concordancer()
