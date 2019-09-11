#
# Wordless: Utilities - Miscellaneous
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import collections
import copy
import os
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy

def get_abs_path(path):
    path = os.path.realpath(path)
    path = os.path.normpath(path)

    return path

def find_wordless_main(widget):
    main = widget

    while not isinstance(main, QMainWindow):
        main = main.parent()

    return main

def flatten_list(list_to_flatten):
    for item in list_to_flatten:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten_list(item)
        else:
            yield item

def normalize_nums(nums, normalized_min, normalized_max, normalized_reversed = False):
    nums_min = min(nums)
    nums_max = max(nums)

    if nums_max - nums_min == 0:
        nums_normalized = [normalized_min] * len(nums)
    else:
        if normalized_reversed:
            nums_normalized = [numpy.interp(num, [nums_min, nums_max], [normalized_max, normalized_min])
                               for num in nums]
        else:
            nums_normalized = [numpy.interp(num, [nums_min, nums_max], [normalized_min, normalized_max])
                               for num in nums]

    return nums_normalized

def merge_dicts(dicts_to_merge):
    dict_merged = {}

    if any(dicts_to_merge):
        for i, dict_to_merge in enumerate(dicts_to_merge):
            if dict_to_merge:
                i_dict = i

                values_2d = type(list(dict_to_merge.values())[0]) == list

                break

        if values_2d:
            value_2d = [[0] * len(list(dicts_to_merge[i_dict].values())[0]) for i in range(len(dicts_to_merge))]
        else:
            value_1d = [0] * len(dicts_to_merge)

        for i, dict_to_merge in enumerate(dicts_to_merge):
            for key, values in dict_to_merge.items():
                if key not in dict_merged:
                    if values_2d:
                        dict_merged[key] = copy.deepcopy(value_2d)
                    else:
                        dict_merged[key] = copy.copy(value_1d)

                dict_merged[key][i] = values

    return dict_merged

def log_timing(func):
    def wrapper(widget, *args, **kwargs):
        if isinstance(widget, QMainWindow):
            main = widget
        else:
            main = widget.main

        time_start = time.time()

        return_val = func(widget, *args, **kwargs)

        time_elapsed = time.time() - time_start
        time_elapsed_min = int(time_elapsed // 60)
        time_elapsed_sec = time_elapsed % 60

        if time_elapsed_min == 0:
            message_timing = main.tr(f'(In {time_elapsed_sec:.2f} seconds)')
        elif time_elapsed_min == 1:
            message_timing = main.tr(f'(In 1 minute {time_elapsed_sec:.2f} seconds)')
        else:
            message_timing = main.tr(f'(In {time_elapsed_min} minutes {time_elapsed_sec:.2f} seconds)')

        message_current = main.statusBar().currentMessage()

        if message_current:
            if message_current.find('(In') > - 1:
                main.statusBar().showMessage(f'{message_current.split("(")[0].rstrip()} {message_timing}')
            else:
                main.statusBar().showMessage(f'{message_current} {message_timing}')
        else:
            main.statusBar().showMessage(f'{message_timing}')

        return return_val

    return wrapper
