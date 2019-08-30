#
# Wordless: Tests - Text - Text Processing - Stop Words
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

import pytest

from wordless_tests import test_init
from wordless_text import wordless_text_processing
from wordless_utils import wordless_conversion

main = test_init.Test_Main()

LISTS_STOP_WORDS = []

for lang, lists_stop_words in main.settings_global['stop_words'].items():
    for list_stop_words in lists_stop_words:
        LISTS_STOP_WORDS.append((lang, list_stop_words))

@pytest.mark.parametrize('lang, list_stop_words', LISTS_STOP_WORDS)
def test_stop_words(lang, list_stop_words):
    lang_text = wordless_conversion.to_lang_text(main, lang)
    stop_words = wordless_text_processing.wordless_get_stop_words(main, lang, list_stop_words = list_stop_words)

    if list_stop_words == 'Custom List':
        # Check if custom list is empty
        assert stop_words == []
    else:
        # Check if the list is empty
        assert len(stop_words)
        # Check if there are empty tokens in the list
        assert all([stop_word for stop_word in stop_words])
