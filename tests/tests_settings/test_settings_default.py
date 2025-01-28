# ----------------------------------------------------------------------
# Tests: Settings - Default settings
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
from wordless.wl_settings import wl_settings_default

main = wl_test_init.Wl_Test_Main()

def test_settings_default():
    assert wl_settings_default.init_settings_default(main)

    # Check for invalid conversion of universal POS tags into content/function words
    for mappings in main.settings_default['pos_tagging']['tagsets']['mapping_settings'].values():
        for mapping in mappings.values():
            assert all(len(pos_mapping) == 5 for pos_mapping in mapping)

if __name__ == '__main__':
    test_settings_default()
