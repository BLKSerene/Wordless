#
# Wordless: Figures - Figure
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import platform

import matplotlib
import matplotlib.pyplot

def show_fig():
    if platform.system() in ['Windows', 'Linux']:
        matplotlib.pyplot.get_current_fig_manager().window.showMaximized()
    # Do not maximize the window to avoid segfault on macOS
    elif platform.system() == 'Darwin':
        matplotlib.pyplot.show()
