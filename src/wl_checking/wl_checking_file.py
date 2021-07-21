#
# Wordless: Checking - File
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import re

from wl_dialogs import wl_dialog_error, wl_msg_box
from wl_utils import wl_detection, wl_misc

def check_file_paths_missing(main, file_paths):
    file_paths_missing = []
    file_paths_pass = []

    if file_paths:
        for file_path in file_paths:
            file_path = wl_misc.get_normalized_path(file_path)

            if os.path.exists(file_path):
                file_paths_pass.append(file_path)
            else:
                file_paths_missing.append(file_path)

    return file_paths_pass, file_paths_missing

def check_file_paths_empty(main, file_paths):
    file_paths_empty = []
    file_paths_pass = []

    if file_paths:
        for file_path in file_paths:
            file_path = wl_misc.get_normalized_path(file_path)

            # Text files
            if os.path.splitext(file_path)[1] in [
                '.txt',
                '.csv',
                '.htm',
                '.html',
                '.xml',
                '.tmx'
            ]:
                if main.settings_custom['file_area']['auto_detection_settings']['detect_encodings']:
                    encoding = wl_detection.detect_encoding(main, file_path)
                else:
                    encoding = main.settings_custom['files']['default_settings']['encoding']

                try:
                    with open(file_path, 'r', encoding = encoding) as f:
                        empty_file = True

                        for line in f:
                            if line.strip():
                                empty_file = False

                                break

                        if empty_file:
                            file_paths_empty.append(file_path)
                        else:
                            file_paths_pass.append(file_path)
                except:
                    file_paths_pass.append(file_path)
            # Other file types
            else:
                if os.stat(file_path).st_size:
                    file_paths_pass.append(file_path)
                else:
                    file_paths_empty.append(file_path)

    return file_paths_pass, file_paths_empty

def check_file_paths_unsupported(main, file_paths):
    file_paths_unsupported = []
    file_paths_pass = []

    file_exts = [ext
                 for file_type in main.settings_global['file_types']['files']
                 for ext in re.findall(r'(?<=\*)\.[a-z]+', file_type)]

    if file_paths:
        for file_path in file_paths:
            file_path = wl_misc.get_normalized_path(file_path)

            if os.path.splitext(file_path)[1].lower() not in file_exts:
                file_paths_unsupported.append(file_path)
            else:
                file_paths_pass.append(file_path)

    return file_paths_pass, file_paths_unsupported

def check_file_paths_parsing_error(main, file_paths):
    file_paths_parsing_error = []
    file_paths_pass = []

    if file_paths:
        for file_path in file_paths:
            file_path = wl_misc.get_normalized_path(file_path)

            if os.path.splitext(file_path)[1] in [
                '.txt',
                '.csv',
                '.htm',
                '.html',
                '.xml',
                '.tmx'
            ]:

                if main.settings_custom['file_area']['auto_detection_settings']['detect_encodings']:
                    encoding = wl_detection.detect_encoding(main, file_path)
                else:
                    encoding = main.settings_custom['files']['default_settings']['encoding']

                try:
                    text = ''

                    with open(file_path, 'r', encoding = encoding) as f:
                        for line in f:
                            text += line
                except Exception as e:
                    print(f'Parsing Error: {e}')

                    file_paths_parsing_error.append(file_path)
                else:
                    file_paths_pass.append(file_path)
            else:
                file_paths_pass.append(file_path)

    return file_paths_pass, file_paths_parsing_error

def check_files_on_loading(main, files):
    loading_pass = True

    if files:
        # Check for invalid XML files
        for file in files:
            if re.search(r'\.xml$', file['path'], flags = re.IGNORECASE):
                if file['tokenized'] == 'No' or file['tagged'] == 'No':
                    wl_msg_box.wl_msg_box_invalid_xml_file(main)

                    loading_pass = False
    else:
        wl_msg_box.wl_msg_box_no_files_selected(main)

        loading_pass = False

    return loading_pass

def check_files_on_loading_colligation(main, files):
    files_pos_tagging_unsupported = []
    loading_pass = True

    if files:
        # Check for invalid XML files
        for file in files:
            if re.search(r'\.xml$', file['path'], flags = re.IGNORECASE):
                if file['tokenized'] == 'No' or file['tagged'] == 'No':
                    wl_msg_box.wl_msg_box_invalid_xml_file(main)

                    return False

        for file in files:
            if file['lang'] not in main.settings_global['pos_taggers']:
                files_pos_tagging_unsupported.append(file)

        files_pos_tagging_unsupported = [file['path'] for file in files_pos_tagging_unsupported]

        wl_dialog_error.wl_dialog_error_file_load_colligation(
            main,
            files_pos_tagging_unsupported = files_pos_tagging_unsupported
        )

        if files_pos_tagging_unsupported:
            loading_pass = False
    else:
        wl_msg_box.wl_msg_box_no_files_selected(main)
        
        loading_pass = False

    return loading_pass
