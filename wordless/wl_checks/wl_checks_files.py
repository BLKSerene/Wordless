# ----------------------------------------------------------------------
# Wordless: Checks - Files
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

import os
import re

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_errs
from wordless.wl_utils import wl_paths

def check_file_paths_unsupported(main, file_paths):
    file_paths_ok = []
    file_paths_unsupported = []

    if file_paths:
        file_exts = [
            ext
            for file_type in main.settings_global['file_types']['files']
            for ext in re.findall(r'(?<=\*)\.[a-z]+', file_type)
        ]

        for file_path in file_paths:
            file_path = wl_paths.get_normalized_path(file_path)

            if os.path.splitext(file_path)[1].lower() not in file_exts:
                file_paths_unsupported.append(file_path)
            else:
                file_paths_ok.append(file_path)

    return file_paths_ok, file_paths_unsupported

def check_file_paths_empty(main, file_paths): # pylint: disable=unused-argument
    file_paths_ok = []
    file_paths_empty = []

    if file_paths:
        for file_path in file_paths:
            file_path = wl_paths.get_normalized_path(file_path)

            if os.stat(file_path).st_size:
                file_paths_ok.append(file_path)
            else:
                file_paths_empty.append(file_path)

    return file_paths_ok, file_paths_empty

def check_file_paths_dup(main, new_file_paths, file_paths = None):
    file_paths_ok = []
    file_paths_dup = []

    if new_file_paths:
        if file_paths is None:
            file_paths = [file['path_orig'] for file in main.settings_custom['file_area']['files_open']]

        for new_file_path in new_file_paths:
            if new_file_path in file_paths + file_paths_ok:
                file_paths_dup.append(new_file_path)
            else:
                file_paths_ok.append(new_file_path)

    return file_paths_ok, file_paths_dup

def check_err_file_area(main, err_msg):
    if err_msg:
        # Use exec_() instead of open() here to prevent the dialog from being hidden on OS X 10.11 with PyQt 5.10
        wl_dialogs_errs.Wl_Dialog_Err_Fatal(main, err_msg).exec_()
        wl_checks_work_area.wl_status_bar_msg_err_fatal(main)

    return not err_msg
