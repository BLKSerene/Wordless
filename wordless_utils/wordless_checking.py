#
# Wordless: Checking
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import re

from wordless_widgets import wordless_message_box

# Settings
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

# Files
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

def check_files_failed_to_open(main, file_paths):
    files_failed_to_open = []
    files_ok = []

    for file_path in file_paths:
        file_path = os.path.normpath(file_path)

        if os.path.splitext(file_path)[1] in ['.tmx']:
            if main.settings_custom['file']['auto_detection_settings']['detect_encodings']:
                encoding_code, _ = wordless_detection.detect_encoding(main, file_path)
            else:
                encoding_code = main.settings_custom['encoding_detection']['default_settings']['default_encoding']

            try:
                open(file_path, 'r', encoding = encoding_code).read()
            except UnicodeDecodeError:
                files_failed_to_open.append(file_path)
            else:
                files_ok.append(file_path)
        else:
            files_ok.append(file_path)

    return files_ok, files_failed_to_open

def check_files_all(main, file_paths):
    file_paths, files_missing = check_files_missing(main, file_paths)
    file_paths, files_empty = check_files_empty(main, file_paths)
    file_paths, files_duplicate = check_files_duplicate(main, file_paths)
    file_paths, files_unsupported = check_files_unsupported(main, file_paths)
    file_paths, files_failed_to_open = check_files_failed_to_open(main, file_paths)

    return (file_paths,
            files_missing, files_empty, files_duplicate, files_unsupported, files_failed_to_open)

def check_new_name(new_name, names):
    i = 2

    if new_name in names:
        while True:
            new_name_valid = f'{new_name} ({i})'

            if new_name_valid in names:
                i += 1
            else:
                break
    else:
        new_name_valid = new_name

    return new_name_valid

def check_new_path(new_path):
	i = 2

	if os.path.exists(new_path) and os.path.isfile(new_path):
		while True:
			path_head, ext = os.path.splitext(new_path)
			new_path_valid = f'{path_head} ({i}){ext}'

			if os.path.exists(new_path_valid) and os.path.isfile(new_path_valid):
				i += 1
			else:
				break
	else:
		new_path_valid = new_path

	return new_path_valid
