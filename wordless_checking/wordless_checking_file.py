#
# Wordless: Checking - File
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import re

from wordless_utils import wordless_detection
from wordless_widgets import wordless_message_box

def check_files_missing(main, file_paths):
    files_missing = []
    files_ok = []

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if not os.path.exists(file_path):
            files_missing.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_missing

def check_files_empty(main, file_paths):
    files_empty = []
    files_ok = []

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if os.path.getsize(file_path) == 0:
            files_empty.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_empty

def check_files_duplicate(main, file_paths):
    files_duplicate = []
    files_ok = []

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if main.wordless_files.find_file_by_path(file_path):
            files_duplicate.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_duplicate

def check_files_unsupported(main, file_paths):
    files_unsupported = []
    files_ok = []

    file_exts = [ext
                 for file_type in main.settings_global['file_types']['files']
                 for ext in re.findall(r'(?<=\*)\.[a-z]+', file_type)]

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if os.path.splitext(file_path)[1].lower() not in file_exts:
            files_unsupported.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_unsupported

def check_files_encoding_error(main, file_paths):
    files_encoding_error = []
    files_ok = []

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if os.path.splitext(file_path)[1] in ['.htm', '.html', '.tmx', '.lrc']:
            if main.settings_custom['files']['auto_detection_settings']['detect_encodings']:
                encoding, _ = wordless_detection.detect_encoding(main, file_path)
            else:
                encoding = main.settings_custom['auto_detection']['default_settings']['default_encoding']

            try:
                open(file_path, 'r', encoding = encoding).read()
            except:
                files_encoding_error.append(file_path)
            else:
                files_ok.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_encoding_error

def check_files_loading_error(main, file_paths, encodings):
    files_loading_error = []
    files_ok = []

    for file_path, encoding in zip(file_paths, encodings):
        try:
            open(file_path, 'r', encoding = encoding).read()
        except:
            files_loading_error.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_loading_error

def check_files_loading(main, files):
    file_paths = [file['path'] for file in files]

    file_paths, files_missing = check_files_missing(main, file_paths)
    file_paths, files_empty = check_files_empty(main, file_paths)

    encodings = [file['encoding']
                 for file in files
                 if file['path'] in file_paths]

    file_paths, files_loading_error = check_files_loading_error(main, file_paths, encodings)

    wordless_message_box.wordless_message_box_error_files(main,
                                                          files_missing = files_missing,
                                                          files_empty = files_empty,
                                                          files_loading_error = files_loading_error)

    for file in main.wordless_files.get_selected_files():
        if file['path'] in files_missing + files_empty:
            main.settings_custom['files']['files_open'].remove(file)

    main.wordless_files.update_table()

    return [file for file in files if file['path'] in file_paths]
