# ----------------------------------------------------------------------
# Tests: Settings - Dependency Parsing
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

from tests import wl_test_init
from wordless.wl_settings import wl_settings_dependency_parsing

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_dependency_parsing():
    settings_dependency_parsing = wl_settings_dependency_parsing.Wl_Settings_Dependency_Parsing(main)
    settings_dependency_parsing.load_settings()
    settings_dependency_parsing.load_settings(defaults = True)
    settings_dependency_parsing.apply_settings()

    settings_dependency_parsing.preview_changed()
    settings_dependency_parsing.update_gui('test')
    settings_dependency_parsing.update_gui_err()

def test_wl_dialog_preview_settings():
    dialog_preview_settings = wl_settings_dependency_parsing.Wl_Dialog_Preview_Settings(main)
    dialog_preview_settings.open()
    dialog_preview_settings.load_settings()
    dialog_preview_settings.save_settings()

if __name__ == '__main__':
    test_wl_settings_dependency_parsing()
    test_wl_dialog_preview_settings()
