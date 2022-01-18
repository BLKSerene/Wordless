# ----------------------------------------------------------------------
# Wordless: Checking - File
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import os
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from wl_dialogs import wl_dialogs_errs, wl_msg_boxes
from wl_utils import wl_detection, wl_misc

def check_file_paths_unsupported(main, file_paths):
    file_paths_pass = []
    file_paths_unsupported = []

    if file_paths:
        file_exts = [
            ext
            for file_type in main.settings_global['file_types']['files']
            for ext in re.findall(r'(?<=\*)\.[a-z]+', file_type)
        ]

        for file_path in file_paths:
            file_path = wl_misc.get_normalized_path(file_path)

            if os.path.splitext(file_path)[1].lower() not in file_exts:
                file_paths_unsupported.append(file_path)
            else:
                file_paths_pass.append(file_path)

    return file_paths_pass, file_paths_unsupported

def check_file_paths_empty(main, file_paths):
    file_paths_pass = []
    file_paths_empty = []

    if file_paths:
        for i, file_path in enumerate(file_paths):
            file_path = wl_misc.get_normalized_path(file_path)

            if os.stat(file_path).st_size:
                file_paths_pass.append(file_path)
            else:
                file_paths_empty.append(file_path)

    return file_paths_pass, file_paths_empty

def check_file_paths_duplicate(main, file_paths):
    file_paths_pass = []
    file_paths_duplicate = []

    if file_paths:
        file_paths_original = [file['path_original'] for file in main.settings_custom['file_area']['files_open']]

        for file_path in file_paths:
            if file_path in file_paths_original:
                file_paths_duplicate.append(file_path)
            else:
                file_paths_pass.append(file_path)

    return file_paths_pass, file_paths_duplicate

def check_files_on_loading(main, files):
    loading_pass = True

    if files:
        # Check for invalid XML files
        for file in files:
            if re.search(r'\.xml$', file['path'], flags = re.IGNORECASE):
                if file['tokenized'] == 'No' or file['tagged'] == 'No':
                    wl_msg_boxes.wl_msg_box_invalid_xml_file(main)

                    loading_pass = False
    else:
        wl_msg_boxes.wl_msg_box_no_files_selected(main)

        loading_pass = False

    return loading_pass

def check_files_on_loading_colligation(main, files):
    files_pos_tagging_unsupported = []
    loading_pass = True

    if check_files_on_loading(main, files):
        for file in files:
            if file['lang'] not in main.settings_global['pos_taggers']:
                files_pos_tagging_unsupported.append(file)

        file_paths_pos_tagging_unsupported = [file['path'] for file in files_pos_tagging_unsupported]

        if file_paths_pos_tagging_unsupported:
            dialog_err_files = wl_dialogs_errs.Wl_Dialog_Err_Files(main, title = main.tr('Error Loading Files'))

            dialog_err_files.label_err.set_text(main.tr('''
                <div>
                    The built-in POS taggers currently have no support for the following file(s), please check your language settings or provide copora that have already been POS-tagged.
                </div>
            '''))

            dialog_err_files.table_err_files.setRowCount(len(file_paths_pos_tagging_unsupported))

            for i, file_path in enumerate(file_paths_pos_tagging_unsupported):
                dialog_err_files.table_err_files.setItem(
                    i, 0,
                    QTableWidgetItem(main.tr('POS Tagging Unsupported'))
                )
                dialog_err_files.table_err_files.setItem(
                    i, 1,
                    QTableWidgetItem(file_path)
                )

            dialog_err_files.open()

        if files_pos_tagging_unsupported:
            loading_pass = False
    else:
        loading_pass = False

    return loading_pass
