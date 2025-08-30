# ----------------------------------------------------------------------
# Tests: Results - Sample
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
from wordless.wl_results import wl_results_sample

main = wl_test_init.Wl_Test_Main()

def test_wl_dialog_results_sample():
    table = wl_test_init.Wl_Test_Table(main, tab = 'dependency_parser')
    table.settings['file_area']['files_open'] = [{'selected': True, 'lang': 'test'}]

    dialog_results_sample = wl_results_sample.Wl_Dialog_Results_Sample(
        main,
        table = table
    )

    dialog_results_sample.load_settings(defaults = True)
    dialog_results_sample.load_settings(defaults = False)

    for i in range(dialog_results_sample.combo_box_sampling_method.count()):
        dialog_results_sample.combo_box_sampling_method.setCurrentIndex(i)
        dialog_results_sample.settings_changed()
        dialog_results_sample.sample()

if __name__ == '__main__':
    test_wl_dialog_results_sample()
