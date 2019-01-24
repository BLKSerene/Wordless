#
# Wordless: Checking - Miscellaneous
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import os
import pathlib

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

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        pathlib.Path(dir_name).mkdir(parents = True, exist_ok = True)

    return dir_name

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
