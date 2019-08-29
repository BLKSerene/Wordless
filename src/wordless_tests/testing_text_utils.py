#
# Wordless: Testing - Text Utilities
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
from wordless_text import wordless_text_utils

main = testing_init.Testing_Main()

sentence_srp_cyrl = 'Српски језик припада словенској групи језика породице индоевропских језика.[12]'
sentence_srp_latn = 'Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12]'

# Serbian (Cyrillic) -> Serbian (Latin)
print('---------- Serbian (Cyrillic) -> Serbian (Latin) ----------')
print(f'Serbian (Cyrillic): {sentence_srp_cyrl}')
print(f"Serbian (Latin): {' '.join(wordless_text_utils.to_srp_latn(sentence_srp_cyrl.split()))}")

# Serbian (Latin) -> Serbian (Cyrillic)
print('---------- Serbian (Latin) -> Serbian (Cyrillic) ----------')
print(f'Serbian (Latin): {sentence_srp_latn}')
print(f"Serbian (Cyrillic): {' '.join(wordless_text_utils.to_srp_cyrl(sentence_srp_latn.split()))}")
