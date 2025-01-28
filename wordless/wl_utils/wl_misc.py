# ----------------------------------------------------------------------
# Wordless: Utilities - Miscellaneous
# Copyright (C) 2018-2025  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import collections
import copy
import os
import platform
import re
import time
import traceback
import urllib

import numpy
import packaging.version
import requests
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow

from wordless.wl_utils import wl_paths

_tr = QCoreApplication.translate

def check_os():
    is_windows = False
    is_macos = False
    is_linux = False

    match platform.system():
        case 'Windows':
            is_windows = True
        case 'Darwin':
            is_macos = True
        case 'Linux':
            is_linux = True

    return is_windows, is_macos, is_linux

def get_linux_distro():
    try:
        os_release = platform.freedesktop_os_release()
    # Default to Ubuntu if undetermined
    except OSError:
        os_release = {'ID': 'ubuntu'}

    return os_release['ID']

def change_file_owner_to_user(file_path):
    # pylint: disable=no-member
    _, is_macos, is_linux = check_os()

    # Available on Unix only
    if (is_macos or is_linux) and os.getuid() == 0:
        uid = int(os.environ.get('SUDO_UID'))
        gid = int(os.environ.get('SUDO_GID'))

        os.chown(file_path, uid, gid)

def find_wl_main(widget):
    if 'main' in widget.__dict__:
        main = widget.main
    else:
        main = widget

        while not isinstance(main, QMainWindow):
            main = main.parent()

    return main

def get_wl_ver():
    with open(wl_paths.get_path_file('VERSION'), 'r', encoding = 'utf_8') as f:
        for line in f:
            if re.search(r'^[0-9]+\.[0-9]+\.[0-9]+$', line.strip()):
                wl_ver = line.strip()

                break

    return packaging.version.Version(wl_ver)

REQUESTS_TIMEOUT = 10

def wl_get_proxies(main):
    proxy_settings = main.settings_custom['general']['proxy_settings']

    if proxy_settings['use_proxy']:
        if proxy_settings['username']:
            proxy_username = urllib.parse.quote(proxy_settings['username'])
            proxy_password = urllib.parse.quote(proxy_settings['password'])

            proxy = f"http://{proxy_username}:{proxy_password}@{proxy_settings['address']}:{proxy_settings['port']}"
        else:
            proxy = f"http://{proxy_settings['address']}:{proxy_settings['port']}"

        proxies = {'http': proxy, 'https': proxy}
    else:
        proxies = None

    return proxies

def wl_download(main, url):
    err_msg = ''

    try:
        r = requests.get(url, timeout = REQUESTS_TIMEOUT, proxies = wl_get_proxies(main))

        if r.status_code != 200:
            err_msg = traceback.format_exc()
    except requests.RequestException:
        r = None
        err_msg = traceback.format_exc()

    return r, err_msg

def wl_download_file_size(main, url):
    file_size = 0

    try:
        r = requests.get(url, timeout = REQUESTS_TIMEOUT, stream = True, proxies = wl_get_proxies(main))

        if r.status_code == 200:
            file_size = int(r.headers['content-length'])

        # See: https://requests.readthedocs.io/en/latest/user/advanced/#body-content-workflow
        r.close()
    except requests.RequestException:
        pass

    # In megabytes
    return file_size / 1024 / 1024

def log_time(func):
    def wrapper(widget, *args, **kwargs):
        if isinstance(widget, QMainWindow):
            main = widget
        else:
            main = widget.main

        time_start = time.time()

        return_val = func(widget, *args, **kwargs)

        if return_val != 'skip_logging_time':
            time_elapsed = time.time() - time_start
            time_elapsed_mins = int(time_elapsed // 60)
            time_elapsed_secs = time_elapsed % 60

            msg_min = _tr('wl_misc', 'minute') if time_elapsed_mins == 1 else _tr('wl_misc', 'minutes')
            msg_time = _tr('wl_misc', '(In {} {} {:.2f} seconds)').format(time_elapsed_mins, msg_min, time_elapsed_secs)

            if (msg_cur := main.statusBar().currentMessage()):
                if _tr('wl_misc', '(In') in msg_cur:
                    main.statusBar().showMessage(f"{msg_cur.split(_tr('wl_misc', '(In'))[0].rstrip()} {msg_time}")
                else:
                    main.statusBar().showMessage(f'{msg_cur} {msg_time}')
            else:
                main.statusBar().showMessage(msg_time)

        return return_val

    return wrapper

def flatten_list(list_to_flatten):
    for item in list_to_flatten:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten_list(item)
        else:
            yield item

def merge_dicts(dicts_to_merge):
    dict_merged = {}
    len_dicts = len(dicts_to_merge)

    if any(dicts_to_merge):
        for i, dict_to_merge in enumerate(dicts_to_merge):
            if dict_to_merge:
                i_dict = i

                values_2d = isinstance((list(dict_to_merge.values())[0]), list)

                break

        if values_2d:
            defaults_2d = [[0] * len(list(dicts_to_merge[i_dict].values())[0]) for _ in range(len_dicts)]
        else:
            defaults_1d = [0] * len_dicts

        for i, dict_to_merge in enumerate(dicts_to_merge):
            for key, values in dict_to_merge.items():
                if key not in dict_merged:
                    if values_2d:
                        dict_merged[key] = copy.deepcopy(defaults_2d)
                    else:
                        dict_merged[key] = copy.copy(defaults_1d)

                dict_merged[key][i] = values

    return dict_merged

def normalize_nums(nums, normalized_min, normalized_max, reverse = False):
    nums_min = min(nums)
    nums_max = max(nums)

    if nums_min == nums_max:
        nums_normalized = [(normalized_max - normalized_min) / 2] * len(nums)
    else:
        if reverse:
            nums_normalized = [
                numpy.interp(num, [nums_min, nums_max], [normalized_max, normalized_min])
                for num in nums
            ]
        else:
            nums_normalized = [
                numpy.interp(num, [nums_min, nums_max], [normalized_min, normalized_max])
                for num in nums
            ]

    return nums_normalized
