#
# Wordless: Tests - Text - Text Utilities
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

from wordless_tests import test_init
from wordless_text import wordless_text_utils

main = test_init.Test_Main()

SENTENCE_SRP_CYRL = 'Српски језик припада словенској групи језика породице индоевропских језика.[12]'
SENTENCE_SRP_LATN = 'Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12]'

# Serbian (Cyrillic) -> Serbian (Latin)
def test_srp_cyrl_to_latn():
    tokens_srp_cyrl = SENTENCE_SRP_CYRL.split()

    assert ' '.join(wordless_text_utils.to_srp_latn(tokens_srp_cyrl)) == SENTENCE_SRP_LATN

# Serbian (Latin) -> Serbian (Cyrillic)
def test_srp_latn_to_cyrl():
    tokens_srp_latn = SENTENCE_SRP_LATN.split()

    assert ' '.join(wordless_text_utils.to_srp_cyrl(tokens_srp_latn)) == SENTENCE_SRP_CYRL
