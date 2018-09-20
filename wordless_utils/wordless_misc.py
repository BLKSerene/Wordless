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

def convert_lang(main, lang):
    # Text -> Code
    if lang[0].isupper():
        return main.file_langs[lang]
    # Code -> Text
    else:
        for lang_text, lang_code in main.file_langs.items():
            if lang_code == lang:
                return lang_text

def convert_ext(main, ext):
    # Text -> Code
    return main.file_exts[ext].split(' (')[0]

def convert_encoding(main, encoding, lang = None):
    # Text -> Code
    if encoding.find('(') > -1:
        encoding_code = main.file_encodings[encoding]
        encoding_lang = encoding.split('(')[0]

        return (encoding_code, encoding_lang)

    # Code -> Text
    else:
        for encoding_text, encoding_code in main.file_encodings.items():
            if encoding == encoding_code:
                # Distinguish between different languages
                if lang:
                    if encoding_text.find(lang) > -1:
                        return encoding_text
                else:
                    return encoding_text

def convert_word_delimiter(lang):
    if lang in ['jpn', 'kor', 'zho-cn', 'zho-tw']:
        word_delimiter = ''
    else:
        word_delimiter = ' '

    return word_delimiter

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
    def wrapper(main, tab, *args, **kwargs):
        if tab.name == tab.tr('N-gram'):
            settings = main.settings['ngram']
        elif tab.name == tab.tr('Collocation'):
            settings = main.settings['collocation']

        if settings['show_all'] or (not settings['show_all'] and settings['search_terms']):
            function(main, *args, **kwargs)
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
