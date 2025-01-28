# ----------------------------------------------------------------------
# Tests: Settings - Stop Word Lists
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
from wordless.wl_settings import wl_settings_stop_word_lists

main = wl_test_init.Wl_Test_Main()

def test_wl_settings_stop_word_lists():
    settings_stop_word_lists = wl_settings_stop_word_lists.Wl_Settings_Stop_Word_Lists(main)
    settings_stop_word_lists.load_settings()
    settings_stop_word_lists.load_settings(defaults = True)
    settings_stop_word_lists.apply_settings()

    settings_stop_word_lists.stop_word_list_changed(settings_stop_word_lists.table_stop_word_lists.model().item(0, 0))
    settings_stop_word_lists.preview_settings_changed()
    settings_stop_word_lists.preview_results_changed()

if __name__ == '__main__':
    test_wl_settings_stop_word_lists()
