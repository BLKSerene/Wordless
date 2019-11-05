#
# Wordless: Checking - File
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import re

from wordless_dialogs import wordless_dialog_error, wordless_msg_box
from wordless_utils import wordless_detection, wordless_misc

def check_files_missing(main, files):
    files_missing = []
    files_ok = []

    if files:
        # Wordless files
        if type(files[0]) == dict:
            for file in files:
                if os.path.exists(file['path']):
                    files_ok.append(file)
                else:
                    files_missing.append(file)
        # File paths
        elif type(files[0]) == str:
            for file_path in files:
                file_path = wordless_misc.get_normalized_path(file_path)

                if os.path.exists(file_path):
                    files_ok.append(file_path)
                else:
                    files_missing.append(file_path)

    return files_ok, files_missing

def check_files_empty(main, files):
    files_empty = []
    files_ok = []

    if files:
        # Wordless files
        if type(files[0]) == dict:
            for file in files:
                file_path = file['path']

                # Text files
                if os.path.splitext(file_path)[1] in ['.txt',
                                                      '.csv',
                                                      '.htm',
                                                      '.html',
                                                      '.xml',
                                                      '.tmx',
                                                      '.lrc']:
                    try:
                        with open(file_path, 'r', encoding = file['encoding']) as f:
                            empty_file = True

                            for line in f:
                                if line.strip():
                                    empty_file = False

                                    break

                            if empty_file:
                                files_empty.append(file)
                            else:
                                files_ok.append(file)
                    except:
                        files_ok.append(file)
                # Other file types
                else:
                    if os.stat(file_path).st_size:
                        files_ok.append(file)
                    else:
                        files_empty.append(file)
        # File paths
        elif type(files[0]) == str:
            for file_path in files:
                file_path = wordless_misc.get_normalized_path(file_path)

                # Text files
                if os.path.splitext(file_path)[1] in ['.txt',
                                                      '.csv',
                                                      '.htm',
                                                      '.html',
                                                      '.xml',
                                                      '.tmx',
                                                      '.lrc']:
                    if main.settings_custom['files']['auto_detection_settings']['detect_encodings']:
                        encoding, _ = wordless_detection.detect_encoding(main, file_path)
                    else:
                        encoding = main.settings_custom['auto_detection']['default_settings']['default_encoding']

                    try:
                        with open(file_path, 'r', encoding = encoding) as f:
                            empty_file = True

                            for line in f:
                                if line.strip():
                                    empty_file = False

                                    break

                            if empty_file:
                                files_empty.append(file_path)
                            else:
                                files_ok.append(file_path)
                    except:
                        files_ok.append(file_path)
                # Other file types
                else:
                    if os.stat(file_path).st_size:
                        files_ok.append(file_path)
                    else:
                        files_empty.append(file_path)

    return files_ok, files_empty

def check_files_duplicate(main, files):
    files_duplicate = []
    files_ok = []

    if files:
        # Wordless files
        if type(files[0]) == dict:
            for file in files:
                if main.wordless_files.find_file_by_path(file['path']):
                    files_duplicate.append(file)
                else:
                    files_ok.append(file)
        # File paths
        elif type(files[0]) == str:
            for file_path in files:
                    file_path = wordless_misc.get_normalized_path(file_path)

                    if main.wordless_files.find_file_by_path(file_path):
                        files_duplicate.append(file_path)
                    else:
                        files_ok.append(file_path)

    return files_ok, files_duplicate

def check_files_unsupported(main, files):
    files_unsupported = []
    files_ok = []

    file_exts = [ext
                 for file_type in main.settings_global['file_types']['files']
                 for ext in re.findall(r'(?<=\*)\.[a-z]+', file_type)]

    if files:
        # Wordless files
        if type(files[0]) == dict:
            for file in files:
                if os.path.splitext(file['path'])[1].lower() not in file_exts:
                    files_unsupported.append(file)
                else:
                    files_ok.append(file)
        # File paths
        elif type(files[0]) == str:
            for file_path in files:
                file_path = wordless_misc.get_normalized_path(file_path)

                if os.path.splitext(file_path)[1].lower() not in file_exts:
                    files_unsupported.append(file_path)
                else:
                    files_ok.append(file_path)

    return files_ok, files_unsupported

def check_files_parsing_error(main, files):
    files_parsing_error = []
    files_ok = []

    if files:
        # Wordless files
        if type(files[0]) == dict:
            for file in files:
                file_path = file['path']

                if os.path.splitext(file_path)[1] in ['.csv',
                                                      '.htm',
                                                      '.html',
                                                      '.xml',
                                                      '.tmx',
                                                      '.lrc']:
                    try:
                        with open(file_path, 'r', encoding = file['encoding']) as f:
                            for line in f:
                                pass
                    except:
                        files_parsing_error.append(file)
                    else:
                        files_ok.append(file)
                else:
                    files_ok.append(file)
        # File paths
        elif type(files[0]) == str:
            for file_path in files:
                file_path = wordless_misc.get_normalized_path(file_path)

                if os.path.splitext(file_path)[1] in ['.csv',
                                                      '.htm',
                                                      '.html',
                                                      '.xml',
                                                      '.tmx',
                                                      '.lrc']:
                    if main.settings_custom['files']['auto_detection_settings']['detect_encodings']:
                        encoding, _ = wordless_detection.detect_encoding(main, file_path)
                    else:
                        encoding = main.settings_custom['auto_detection']['default_settings']['default_encoding']

                    try:
                        with open(file_path, 'r', encoding = encoding) as f:
                            for line in f:
                                pass
                    except:
                        files_parsing_error.append(file_path)
                    else:
                        files_ok.append(file_path)
                else:
                    files_ok.append(file_path)

    return files_ok, files_parsing_error

def check_files_decoding_error(main, files):
    files_decoding_error = []
    files_ok = []

    if files:
        # Wordless files
        if type(files[0]) == dict:
            for file in files:
                try:
                    with open(file['path'], 'r', encoding = file['encoding']) as f:
                        for line in f:
                            pass
                except:
                    files_decoding_error.append(file)
                else:
                    files_ok.append(file)
        # File paths
        elif type(files[0]) == str:
            for file_path in files:
                file_path = wordless_misc.get_normalized_path(file_path)

                if main.settings_custom['files']['auto_detection_settings']['detect_encodings']:
                    encoding, _ = wordless_detection.detect_encoding(main, file_path)
                else:
                    encoding = main.settings_custom['auto_detection']['default_settings']['default_encoding']

                try:
                    with open(file_path, 'r', encoding = encoding) as f:
                        for line in f:
                            pass
                except:
                    files_decoding_error.append(file_path)
                else:
                    files_ok.append(file_path)

    return files_ok, files_decoding_error

def check_files_on_loading(main, files):
    loading_ok = True

    if files:
        files_ok, files_missing = check_files_missing(main, files)
        files_ok, files_empty = check_files_empty(main, files_ok)
        files_ok, files_decoding_error = check_files_decoding_error(main, files_ok)

        # Extract file paths
        files_missing = [file['path'] for file in files_missing]
        files_empty = [file['path'] for file in files_empty]
        files_decoding_error = [file['path'] for file in files_decoding_error]

        wordless_dialog_error.wordless_dialog_error_file_load(main,
                                                              files_missing = files_missing,
                                                              files_empty = files_empty,
                                                              files_decoding_error = files_decoding_error)

        if files_missing or files_empty or files_decoding_error:
            loading_ok = False
    else:
        wordless_msg_box.wordless_msg_box_no_files_selected(main)
        
        loading_ok = False

    return loading_ok

def check_files_on_loading_colligation(main, files):
    files_pos_tagging_not_supported = []
    loading_ok = True

    if files:
        files_ok, files_missing = check_files_missing(main, files)
        files_ok, files_empty = check_files_empty(main, files_ok)
        files_ok, files_decoding_error = check_files_decoding_error(main, files_ok)

        for file in files_ok:
            if file['lang'] not in main.settings_global['pos_taggers']:
                files_pos_tagging_not_supported.append(file)

        # Extract file paths
        files_missing = [file['path'] for file in files_missing]
        files_empty = [file['path'] for file in files_empty]
        files_decoding_error = [file['path'] for file in files_decoding_error]
        files_pos_tagging_not_supported = [file['path'] for file in files_pos_tagging_not_supported]

        wordless_dialog_error.wordless_dialog_error_file_load_colligation(main,
                                                                          files_missing = files_missing,
                                                                          files_empty = files_empty,
                                                                          files_decoding_error = files_decoding_error,
                                                                          files_pos_tagging_not_supported = files_pos_tagging_not_supported)

        if files_missing or files_empty or files_decoding_error or files_pos_tagging_not_supported:
            loading_ok = False
    else:
        wordless_msg_box.wordless_msg_box_no_files_selected(main)
        
        loading_ok = False

    return loading_ok
