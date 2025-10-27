# ----------------------------------------------------------------------
# Tests: Settings - General
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

from tests import wl_test_init
from wordless.wl_settings import wl_settings_general

main = wl_test_init.Wl_Test_Main()

def test_wl_settings_general():
    settings_general = wl_settings_general.Wl_Settings_General(main)

    settings_general.checkbox_use_proxy.setChecked(True)
    settings_general.proxy_settings_changed()
    settings_general.checkbox_use_proxy.setChecked(False)
    settings_general.proxy_settings_changed()

    settings_general.load_settings(defaults = False)
    settings_general.load_settings(defaults = True)
    settings_general.apply_settings()

def test_wl_settings_general_imp():
    settings_general_imp = wl_settings_general.Wl_Settings_General_Imp(main)
    settings_general_imp.detect_encodings_changed()

    main.settings_custom['general']['imp']['files']['default_path'] = __file__
    settings_general_imp.check_path('files')

    path_nonexistent = os.path.join(os.path.split(__file__)[0], 'test')
    main.settings_custom['general']['imp']['files']['default_path'] = path_nonexistent
    main.settings_default['general']['imp']['files']['default_path'] = path_nonexistent
    settings_general_imp.check_path('files')

    settings_general_imp.load_settings(defaults = False)
    settings_general_imp.load_settings(defaults = True)
    settings_general_imp.validate_settings()
    settings_general_imp.apply_settings()

    os.rmdir(path_nonexistent)

def test_wl_settings_general_exp():
    settings_general_exp = wl_settings_general.Wl_Settings_General_Exp(main)
    settings_general_exp.tables_default_type_changed()

    settings_general_exp.check_path('tables')
    main.settings_custom['general']['exp']['tables']['default_path'] = 'path_nonexistent'
    settings_general_exp.check_path('tables')

    settings_general_exp.load_settings(defaults = False)
    settings_general_exp.load_settings(defaults = True)
    settings_general_exp.validate_settings()
    settings_general_exp.apply_settings()

if __name__ == '__main__':
    test_wl_settings_general()
    test_wl_settings_general_imp()
    test_wl_settings_general_exp()
