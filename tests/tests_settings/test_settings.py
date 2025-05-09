# ----------------------------------------------------------------------
# Tests: Settings - Settings
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
from wordless.wl_settings import wl_settings

main = wl_test_init.Wl_Test_Main()

def test_wl_settings():
    settings = wl_settings.Wl_Settings(main)
    settings.open()
    settings.selection_changed(None, None)
    settings.load_settings()
    settings.load_settings(defaults = True)
    settings.validate_settings()
    settings.save_settings()
    settings.apply_settings()

def test_wl_settings_node():
    settings_node = wl_settings.Wl_Settings_Node(main)
    settings_node.validate_settings()
    settings_node.apply_settings()

if __name__ == '__main__':
    test_wl_settings()
    test_wl_settings_node()
