# ----------------------------------------------------------------------
# Wordless: Utilities - Miscellaneous
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

import collections
import copy
import os
import platform
import time

import numpy
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow

_tr = QCoreApplication.translate

def check_os():
    is_windows = False
    is_macos = False
    is_linux = False

    if platform.system() == 'Windows':
        is_windows = True
    elif platform.system() == 'Darwin':
        is_macos = True
    elif platform.system() == 'Linux':
        is_linux = True

    return is_windows, is_macos, is_linux

def get_normalized_path(path):
    path = os.path.realpath(path)
    path = os.path.normpath(path)

    return path

def get_normalized_dir(path):
    path = get_normalized_path(path)

    return os.path.dirname(path)

def get_wl_ver():
    try:
        with open('VERSION', 'r', encoding = 'utf_8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    return line.strip()

        return '?.?.?'
    except (FileNotFoundError, PermissionError):
        return '?.?.?'

def split_wl_ver(ver):
    ver_major, ver_minor, ver_patch = ver.split('.')

    if ver_major == ver_minor == ver_patch == '?':
        return '?', '?', '?'
    else:
        return int(ver_major), int(ver_minor), int(ver_patch)

def find_wl_main(widget):
    if 'main' in widget.__dict__:
        main = widget.main
    else:
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

def normalize_nums(nums, normalized_min, normalized_max, reverse = False):
    nums_min = min(nums)
    nums_max = max(nums)

    if nums_max - nums_min == 0:
        nums_normalized = [normalized_min] * len(nums)
    else:
        if reverse:
            nums_normalized = [
                numpy.interp(num, [nums_min, nums_max], [normalized_max, normalized_min])
                for num in nums
            ]
        else:
            nums_normalized = [
                numpy.interp(num, [nums_min, nums_max], [normalized_min, normalized_max])
                for num in nums
            ]

    return nums_normalized

def merge_dicts(dicts_to_merge):
    dict_merged = {}
    len_dicts = len(dicts_to_merge)

    if any(dicts_to_merge):
        for i, dict_to_merge in enumerate(dicts_to_merge):
            if dict_to_merge:
                i_dict = i

                values_2d = isinstance((list(dict_to_merge.values())[0]), list)

                break

        if values_2d:
            defaults_2d = [[0] * len(list(dicts_to_merge[i_dict].values())[0]) for _ in range(len_dicts)]
        else:
            defaults_1d = [0] * len_dicts

        for i, dict_to_merge in enumerate(dicts_to_merge):
            for key, values in dict_to_merge.items():
                if key not in dict_merged:
                    if values_2d:
                        dict_merged[key] = copy.deepcopy(defaults_2d)
                    else:
                        dict_merged[key] = copy.copy(defaults_1d)

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
        time_elapsed_mins = int(time_elapsed // 60)
        time_elapsed_secs = time_elapsed % 60

        msg_min = _tr('log_timing', 'minute') if time_elapsed_mins == 1 else _tr('log_timing', 'minutes')
        msg_time = _tr('log_timing', '(In {} {} {:.2f} seconds)').format(time_elapsed_mins, msg_min, time_elapsed_secs)

        if (msg_cur := main.statusBar().currentMessage()):
            if _tr('log_timing', '(In') in msg_cur:
                main.statusBar().showMessage(f"{msg_cur.split(_tr('log_timing', '(In'))[0].rstrip()} {msg_time}")
            else:
                main.statusBar().showMessage(f'{msg_cur} {msg_time}')
        else:
            main.statusBar().showMessage(msg_time)

        return return_val

    return wrapper
