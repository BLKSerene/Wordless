#
# Wordless: Tests - Text - Stop Word Lists
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init
from wl_text import wl_stop_word_lists
from wl_utils import wl_conversion

test_stop_word_lists = []

main = wl_test_init.Wl_Test_Main()

for lang, stop_word_lists in main.settings_global['stop_word_lists'].items():
    if 'custom' not in stop_word_lists:
        stop_word_lists.append('Missing Custom List')

    for stop_word_list in stop_word_lists:
        test_stop_word_lists.append((lang, stop_word_list))

@pytest.mark.parametrize('lang, stop_word_list', test_stop_word_lists)
def test_get_stop_word_list(lang, stop_word_list):
    lang_text = wl_conversion.to_lang_text(main, lang)

    print(f'{lang_text} ({lang}) / {stop_word_list}:')

    stop_words = wl_stop_word_lists.wl_get_stop_word_list(main, lang, stop_word_list = stop_word_list)

    print(stop_words)

    if stop_word_list == 'custom':
        # Check if custom list is empty
        assert stop_words == []
    else:
        # Check for missing custom lists
        assert stop_word_list != 'Missing Custom List'
        # Check if the list is empty
        assert len(stop_words)
        # Check if there are empty tokens in the list
        assert all([stop_word for stop_word in stop_words])

if __name__ == '__main__':
    for lang, stop_word_list in test_stop_word_lists:
        test_get_stop_word_list(lang, stop_word_list)
