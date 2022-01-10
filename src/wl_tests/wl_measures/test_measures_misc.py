#
# Wordless: Tests - Measures - Miscellaneous
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

from wl_tests import wl_test_init
from wl_measures import wl_measures_misc

main = wl_test_init.Wl_Test_Main()

def test_modes():
    modes = wl_measures_misc.modes([1, 3, 3, 3, 2, 2, 1, 2, 5, 4])

    print(f'Modes: {modes}')

    assert modes == [2, 3]

if __name__ == '__main__':
    test_modes()
