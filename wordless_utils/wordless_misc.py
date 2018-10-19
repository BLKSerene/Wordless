#
# Wordless: Miscellaneous Utility Functions
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import os
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import wordless_dialog
from wordless_utils import wordless_text

def log_timing(message):
    def decorater(func):

        def wrapper(widget, *args, **kwargs):
            if isinstance(widget, QMainWindow):
                main = widget
            else:
                main = widget.main

            time_start = time.time()

            func(widget, *args, **kwargs)

            time_elapsed = time.time() - time_start
            time_elapsed_min = int(time_elapsed // 60)
            time_elapsed_sec = time_elapsed % 60

            if time_elapsed_min == 0:
                main.status_bar.showMessage(main.tr(f'{message}! (In {time_elapsed_sec:.2f} seconds)'))
            elif time_elapsed_min == 1:
                main.status_bar.showMessage(main.tr(f'{message}! (In 1 minute {time_elapsed_sec:.2f} seconds)'))
            else:
                main.status_bar.showMessage(main.tr(f'{message}! (In {time_elapsed_min} minutes {time_elapsed_sec:.2f} seconds)'))

        return wrapper

    return decorater

def multi_sorting(item):
    keys = []

    for value in item[1]:
        if type(value) == list:
            mid = len(value) // 2

            keys.extend([-val for val in value[mid:]])
            keys.extend([-val for val in value[:mid]])
        else:
            keys.append(-value)

    keys.append(item[0])

    return keys

def merge_dicts(dicts_to_be_merged):
    dict_merged = {}

    if any(dicts_to_be_merged):
        for i, dict_to_be_merged in enumerate(dicts_to_be_merged):
            if dict_to_be_merged:
                i_dict = i

                values_2d = type(list(dict_to_be_merged.values())[0]) == list

                break
    else:
        return
    
    if values_2d:
        value_2d = [[0] * len(list(dicts_to_be_merged[i_dict].values())[0]) for i in range(len(dicts_to_be_merged))]
    else:
        value_1d = [0] * len(dicts_to_be_merged)

    for i, dict_to_be_merged in enumerate(dicts_to_be_merged):
        for key, values in dict_to_be_merged.items():
            if key not in dict_merged:
                if values_2d:
                    dict_merged[key] = copy.deepcopy(value_2d)
                else:
                    dict_merged[key] = copy.copy(value_1d)

            dict_merged[key][i] = values

    return dict_merged

def check_file_existence(main, files):
    files_found = []
    files_missing = []

    if type(files) != list:
        files = [files]

    for file in files:
        if os.path.exists(file['path']):
            files_found.append(file)
        else:
            files_missing.append(file['path'])

    if files_missing:
        QMessageBox.warning(main,
                            main.tr('Files Missing'),
                            main.tr('The following files no longer exist:<br>{}<br>Please check and try again.'.format('<br>'.join(files_missing))))

    return files_found
