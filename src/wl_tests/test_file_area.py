#
# Wordless: Tests - File Area
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import glob
import os
import sys
import time

sys.path.append('.')

from wl_dialogs import wl_dialog_misc
from wl_tests import wl_test_init

import wl_file_area

main = wl_test_init.Wl_Test_Main()

def open_file(file_paths, update_gui):
    time_start = time.time()

    for file_path in file_paths:
        print(f'Loading file "{os.path.split(file_path)[1]}"...')

        dialog_progress = wl_dialog_misc.Wl_Dialog_Progress_Open_Files(main)

        worker_open_files = wl_file_area.Wl_Worker_Open_Files(
            main,
            dialog_progress = dialog_progress,
            update_gui = update_gui,
            file_paths = [file_path]
        )
        worker_open_files.run()
        
    print(f'Done! (In {round(time.time() - time_start, 2)} seconds)')

def test_file_area():
    new_files = []

    # Clean cached files
    for file in glob.glob('Import/*.*'):
        os.remove(file)

    # Disable encoding detection
    main.settings_custom['file_area']['auto_detection_settings']['detect_encodings'] = False

    # File types
    open_file(
        file_paths = glob.glob('wl_tests_files/wl_file_area/file_types/*.*'),
        update_gui = update_gui_file_types
    )

    # UnicodeDecodeError
    open_file(
        file_paths = glob.glob('wl_tests_files/wl_file_area/unicode_decode_error/*.*'),
        update_gui = update_gui_unicode_decode_error
    )

    # Tags
    for file_path in glob.glob('wl_tests_files/wl_file_area/tags/*.*'):
        if file_path.endswith('untokenized_untagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'No'
            main.settings_custom['files']['default_settings']['tagged'] = 'No'
        elif file_path.endswith('untokenized_tagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'No'
            main.settings_custom['files']['default_settings']['tagged'] = 'Yes'
        elif file_path.endswith('tokenized_untagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'Yes'
            main.settings_custom['files']['default_settings']['tagged'] = 'No'
        elif file_path.endswith('tokenized_tagged.txt'):
            main.settings_custom['files']['default_settings']['tokenized'] = 'Yes'
            main.settings_custom['files']['default_settings']['tagged'] = 'Yes'

        open_file(
            file_paths = [file_path],
            update_gui = update_gui_tags
        )

def update_gui_file_types(error_msg, new_files):
    assert not error_msg

    file_name = os.path.split(new_files[0]['path'])[1]
    file_text = new_files[0]['text']

    print(file_text.tokens_multilevel)
    print(file_text.tokens_flat)
    print(file_text.tags)
    print(file_text.offsets_paras)
    print(file_text.offsets_sentences)

    if file_name == 'CSV File.txt':
        assert file_text.tokens_multilevel == [[], [], [['3', '-', '2', '3', '-', '3']], [], [], [['6', '-', '2', '6', '-', '3']], [], []]
        assert file_text.tokens_flat == ['3', '-', '2', '3', '-', '3', '6', '-', '2', '6', '-', '3']
        assert file_text.offsets_paras == [0, 0, 0, 6, 6, 6, 12, 12]
        assert file_text.offsets_sentences == [0, 6]
    elif file_name == 'Excel Workbook.txt':
        assert file_text.tokens_multilevel == [[], [['B2', '&', 'C2', 'D2']], [['B3', '&', 'B4', 'C3', 'D3']], [['C4', 'D4']], [['B5', 'C5', 'D5']], [], [], [['B2', '&', 'C2', 'D2']], [['B3', '&', 'B4', 'C3', 'D3']], [['C4', 'D4']], [['B5', 'C5', 'D5']]]
        assert file_text.tokens_flat == ['B2', '&', 'C2', 'D2', 'B3', '&', 'B4', 'C3', 'D3', 'C4', 'D4', 'B5', 'C5', 'D5', 'B2', '&', 'C2', 'D2', 'B3', '&', 'B4', 'C3', 'D3', 'C4', 'D4', 'B5', 'C5', 'D5']
        assert file_text.offsets_paras == [0, 0, 4, 9, 11, 14, 14, 14, 18, 23, 25]
        assert file_text.offsets_sentences == [0, 4, 9, 11, 14, 18, 23, 25]
    elif file_name == 'HTML Page.txt':
        assert file_text.tokens_multilevel == [[], [], [['This', 'is', 'a', 'title']], [], [], [['Hello', 'world', '!']], [], []]
        assert file_text.tokens_flat == ['This', 'is', 'a', 'title', 'Hello', 'world', '!']
        assert file_text.offsets_paras == [0, 0, 0, 4, 4, 4, 7, 7]
        assert file_text.offsets_sentences == [0, 4]
    elif file_name == 'Word Document.txt':
        assert file_text.tokens_multilevel == [[], [], [['Heading']], [], [], [['This', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], [['2', '-', '2', '&', '2', '-', '3', '2', '-', '4']], [['3', '-', '2', '&', '4', '-', '2', '3', '-', '3', '3', '-', '4']], [['4', '-', '3', '4', '-', '4']], [['5', '-', '2', '5', '-', '3', '5', '-', '4', '5', '-', '4', '-', '1', '5', '-', '4', '-', '2', '5', '-', '4', '-', '3', '5', '-', '4', '-', '4']], [], [], []]
        assert file_text.tokens_flat == ['Heading', 'This', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.', '2', '-', '2', '&', '2', '-', '3', '2', '-', '4', '3', '-', '2', '&', '4', '-', '2', '3', '-', '3', '3', '-', '4', '4', '-', '3', '4', '-', '4', '5', '-', '2', '5', '-', '3', '5', '-', '4', '5', '-', '4', '-', '1', '5', '-', '4', '-', '2', '5', '-', '4', '-', '3', '5', '-', '4', '-', '4']
        assert file_text.offsets_paras == [0, 0, 0, 1, 1, 1, 13, 13, 13, 19, 19, 29, 42, 48, 77, 77, 77]
        assert file_text.offsets_sentences == [0, 1, 7, 13, 19, 29, 42, 48]
    elif file_name == 'XML File.xml':
        pass
        # assert file_text.tokens_multilevel == []
        # assert file_text.tokens_flat == []
        # assert file_text.offsets_paras == []
        # assert file_text.offsets_sentences == []

    assert file_text.tags == [[] for i in file_text.tokens_flat]

def update_gui_unicode_decode_error(error_msg, new_files):
    assert not error_msg

    assert new_files[0]['encoding'] == 'utf_8'

def update_gui_tags(error_msg, new_files):
    assert not error_msg

    file_name = os.path.split(new_files[0]['path'])[1]
    file_text = new_files[0]['text']

    print(file_text.tokens_multilevel)
    print(file_text.tokens_flat)
    print(file_text.tags)
    print(file_text.offsets_paras)
    print(file_text.offsets_sentences)

    if file_name == 'untokenized_untagged.txt':
        assert file_text.tokens_multilevel == [[], [], [['This', '<', 'TAG', '>', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['This', '<', 'TAG', '>', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [[] for i in file_text.tokens_flat]
        assert file_text.offsets_paras == [0, 0, 0, 15, 15, 15, 21, 21]
        assert file_text.offsets_sentences == [0, 9, 15]
    elif file_name == 'untokenized_tagged.txt':
        assert file_text.tokens_multilevel == [[['']], [], [['This', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['', 'This', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [['<TAG1>'], ['<TAG2>'], ['</TAG2>'], [], [], [], [], ['_TAG3'], [], [], [], [], [], [], [], [], [], [], ['<TAG4>', '</TAG4>']]
        assert file_text.offsets_paras == [0, 1, 1, 13, 13, 13, 19, 19]
        assert file_text.offsets_sentences == [0, 1, 7, 13]
    elif file_name == 'tokenized_untagged.txt':
        assert file_text.tokens_multilevel == [[], [], [['This', '<TAG>is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['This', '<TAG>is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [[] for i in file_text.tokens_flat]
        assert file_text.offsets_paras == [0, 0, 0, 12, 12, 12, 18, 18]
        assert file_text.offsets_sentences == [0, 6, 12]
    elif file_name == 'tokenized_tagged.txt':
        assert file_text.tokens_multilevel == [[['']], [], [['This', 'is', 'the', 'first', 'sentence', '.'], ['This', 'is', 'the', 'second', 'sentence', '.']], [], [], [['This', 'is', 'the', 'third', 'sentence', '.']], [], []]
        assert file_text.tokens_flat == ['', 'This', 'is', 'the', 'first', 'sentence', '.', 'This', 'is', 'the', 'second', 'sentence', '.', 'This', 'is', 'the', 'third', 'sentence', '.']
        assert file_text.tags == [['<TAG1>'], ['<TAG2>'], ['</TAG2>'], [], [], [], [], ['_TAG3'], [], [], [], [], [], [], [], [], [], [], ['<TAG4>', '</TAG4>']]
        assert file_text.offsets_paras == [0, 1, 1, 13, 13, 13, 19, 19]
        assert file_text.offsets_sentences == [0, 1, 7, 13]

    assert len(file_text.tokens_flat) == len(file_text.tags)

if __name__ == '__main__':
    test_file_area()
