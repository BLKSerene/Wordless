#
# Wordless: Miscellaneous Utilities
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import copy
import os
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_widgets import wordless_message_box

def check_custom_settings(settings_custom, settings_default):
    def get_keys(settings, keys):
        for key, value in settings.items():
            keys.append(key)

            if type(value) == dict:
                get_keys(value, keys)

        return keys
    
    keys_custom = []
    keys_default = []

    keys_custom = get_keys(settings_custom, keys_custom)
    keys_default = get_keys(settings_default, keys_default)

    if keys_custom == keys_default:
        return True
    else:
        return False

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

        message_current = main.status_bar.currentMessage()

        if message_current:
            if message_current.find('(In') > - 1:
                main.status_bar.showMessage(f'{message_current.split("(")[0].rstrip()} {message_timing}')
            else:
                main.status_bar.showMessage(f'{message_current} {message_timing}')
        else:
            main.status_bar.showMessage(f'{message_timing}')

        return return_val

    return wrapper

def check_files_by_path(main, file_paths):
    files_nonexistent = []
    files_unsupported = []
    files_empty = []
    files_duplicate = []
    files_ok = []

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if not os.path.exists(file_path):
            files_nonexistent.append(file_path)
        elif os.path.splitext(file_path)[1] not in main.settings_global['file_exts']:
            files_unsupported.append(file_path)
        elif os.path.getsize(file_path) == 0:
            files_empty.append(file_path)
        elif main.wordless_files.find_file_by_path(file_path):
            files_duplicate.append(file_path)
        else:
            files_ok.append(file_path)

    wordless_message_box.wordless_message_box_error_open_files(main,
                                                               files_nonexistent = files_nonexistent,
                                                               files_unsupported = files_unsupported,
                                                               files_empty = files_empty,
                                                               files_duplicate = files_duplicate)

    return files_ok

def check_files(main, files):
    files_ok = []

    file_paths = check_files_by_path(main, [file['path'] for file in files])

    for file in files:
        if file['path'] in file_paths:
            files_ok.append(file)

    return files_ok

def merge_dicts(dicts_to_merge):
    dict_merged = {}

    if any(dicts_to_merge):
        for i, dict_to_merge in enumerate(dicts_to_merge):
            if dict_to_merge:
                i_dict = i

                values_2d = type(list(dict_to_merge.values())[0]) == list

                break
    else:
        return
    
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
