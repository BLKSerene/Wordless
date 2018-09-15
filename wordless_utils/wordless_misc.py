#
# Wordless: Miscellaneous Utility Functions
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wordless_utils import wordless_text

def multiple_sorting(item):
    keys = []

    for freq in item[1]:
        keys.append(-freq)
    keys.append(item[0])

    return keys

def merge_dicts(dicts_to_be_merged):
    dict_merged = {}

    for i, dict_to_be_merged in enumerate(dicts_to_be_merged):
        for values in dict_merged.values():
            values.append(0)

        for key, value in dict_to_be_merged.items():
            if key not in dict_merged:
                dict_merged[key] = [0] * (i + 1)

            dict_merged[key][i] = value

    return dict(sorted(dict_merged.items(), key = multiple_sorting))

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

def check_search_term(function):
    def wrapper(main, *args, **kwargs):
        tab_text = main.tabs.tabText(main.tabs.indexOf(main.tabs.currentWidget()))

        if tab_text == main.tr('Wordlist'):
            settings = main.settings_custom['wordlist']
        if tab_text == main.tr('N-gram'):
            settings = main.settings_custom['ngram']
        elif tab_text == main.tr('Collocation'):
            settings = main.settings_custom['collocation']

        if (settings['multi_search'] and settings['search_terms'] or
            not settings['multi_search'] and settings['search_term']):
            return function(main, *args, **kwargs)
        else:
            QMessageBox.warning(main,
                                main.tr('Empty Search Term'),
                                main.tr('Please enter your search term(s) first!'),
                                QMessageBox.Ok)

    return wrapper

def check_results_table(function):
    def wrapper(main, table, *args, **kwargs):
        function(main, table, *args, **kwargs)

        if table.rowCount() == 0:
            table.clear_table()

            QMessageBox.information(main,
                                    main.tr('No Results'),
                                    main.tr('There are no results to be shown in the table!<br>You might want to change your settings and try it again.'),
                                    QMessageBox.Ok)

    return wrapper
