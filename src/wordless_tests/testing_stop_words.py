#
# Wordless: Testing - Stop Words
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

from wordless_testing import testing_init
from wordless_text import wordless_text_processing
from wordless_utils import wordless_conversion

main = testing_init.Testing_Main()

def testing_stop_words(lang, list_stop_words):
    lang_text = wordless_conversion.to_lang_text(main, lang)
    stop_words = wordless_text_processing.wordless_get_stop_words(main, lang, list_stop_words = list_stop_words)

    if stop_words:
        print(f'{lang_text} / {list_stop_words}:')
        print(f"\tFirst 10 Stop Words ({len(stop_words)} in Total): {' '.join(stop_words[:10])}")
    else:
        print(f'{lang_text} / {list_stop_words}: None')
        print('------------------------------')

for lang, lists_stop_words in main.settings_global['stop_words'].items():
    for list_stop_words in lists_stop_words:
        testing_stop_words(lang = lang,
                           list_stop_words = list_stop_words)
