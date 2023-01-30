# ----------------------------------------------------------------------
# Wordless: Tests - Initialization
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import copy
import glob
import os
import pickle
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QWidget

from wordless import wl_file_area
from wordless.wl_checks import wl_checks_misc
from wordless.wl_settings import wl_settings_default, wl_settings_global

# Chinese (Traditional), Danish, Dutch, English, French, German, Greek, Italian, Japanese, Russian, Spanish
SEARCH_TERMS = ['是', 'ja', 'ja', 'be', 'être', 'sein', 'είναι', 'essere', 'は', 'быть', 'esta']

# An instance of QApplication must be created before any instance of QWidget
wl_app = QApplication(sys.argv)

class Wl_Test_Main(QWidget):
    def __init__(self):
        super().__init__()

        self.app = wl_app

        # Email
        self.email = 'blkserene@gmail.com'
        self.email_html = '<a href="mailto:blkserene@gmail.com">blkserene@gmail.com</a>'

        # Default settings
        self.settings_default = wl_settings_default.init_settings_default(self)

        # Custom settings
        if os.path.exists('tests/wl_settings.pickle'):
            with open('tests/wl_settings.pickle', 'rb') as f:
                settings_custom = pickle.load(f)

            if wl_checks_misc.check_custom_settings(settings_custom, self.settings_default):
                self.settings_custom = settings_custom
            else:
                self.settings_custom = copy.deepcopy(self.settings_default)
        else:
            self.settings_custom = copy.deepcopy(self.settings_default)

        # Global settings
        self.settings_global = wl_settings_global.init_settings_global()

        # Files
        self.wl_file_area = QObject()
        self.wl_file_area.main = self
        self.wl_file_area.file_type = 'observed'
        self.wl_file_area.settings_suffix = ''

        self.wl_file_area.get_files = lambda: wl_file_area.Wrapper_File_Area.get_files(self.wl_file_area)
        self.wl_file_area.get_file_names = lambda: wl_file_area.Wrapper_File_Area.get_file_names(self.wl_file_area)
        self.wl_file_area.get_selected_files = lambda: wl_file_area.Wrapper_File_Area.get_selected_files(self.wl_file_area)
        self.wl_file_area.get_selected_file_names = lambda: wl_file_area.Wrapper_File_Area.get_selected_file_names(self.wl_file_area)
        self.wl_file_area.find_file_by_name = lambda file_name, selected_only = False: wl_file_area.Wrapper_File_Area.find_file_by_name(self.wl_file_area, file_name, selected_only)
        self.wl_file_area.find_files_by_name = lambda file_names, selected_only = False: wl_file_area.Wrapper_File_Area.find_files_by_name(self.wl_file_area, file_names, selected_only)

        self.wl_file_area_ref = QObject()
        self.wl_file_area_ref.main = self
        self.wl_file_area_ref.file_type = 'ref'
        self.wl_file_area_ref.settings_suffix = '_ref'

        self.wl_file_area_ref.get_files = lambda: wl_file_area.Wrapper_File_Area.get_files(self.wl_file_area_ref)
        self.wl_file_area_ref.get_file_names = lambda: wl_file_area.Wrapper_File_Area.get_file_names(self.wl_file_area_ref)
        self.wl_file_area_ref.get_selected_files = lambda: wl_file_area.Wrapper_File_Area.get_selected_files(self.wl_file_area_ref)
        self.wl_file_area_ref.get_selected_file_names = lambda: wl_file_area.Wrapper_File_Area.get_selected_file_names(self.wl_file_area_ref)

    def height(self):
        return 1080

# Clean cached files
def clean_import_caches():
    for file in glob.glob('imports/*.*'):
        os.remove(file)
