#
# Wordless: Miscellaneous Utility Functions
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import collections
import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import wordless_message, wordless_text

def multi_sorting(item):
    keys = []

    for value in item[1]:
        if isinstance(value, collections.Iterable):
            mid = len(value) // 2

            keys.extend([-val for val in value[mid:]])
            keys.extend([-val for val in value[:mid]])
        else:
            keys.append(-value)

    keys.append(item[0])

    return keys

def merge_dicts(dicts_to_be_merged):
    dict_merged = {}

    values_2d = isinstance(list(dicts_to_be_merged[0].values())[0], collections.Iterable)
    
    if values_2d:
        value_2d = [[0] * len(list(dicts_to_be_merged[0].values())[0]) for i in range(len(dicts_to_be_merged))]
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
