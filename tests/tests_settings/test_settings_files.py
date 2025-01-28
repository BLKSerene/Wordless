# ----------------------------------------------------------------------
# Tests: Settings - Files
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
from wordless.wl_settings import wl_settings_files

main = wl_test_init.Wl_Test_Main()

def test_wl_settings_files():
    settings_files = wl_settings_files.Wl_Settings_Files(main)
    settings_files.load_settings()
    settings_files.load_settings(defaults = True)
    settings_files.apply_settings()

def test_wl_settings_files_tags():
    settings_files_tags = wl_settings_files.Wl_Settings_Files_Tags(main)
    settings_files_tags.load_settings()
    settings_files_tags.load_settings(defaults = True)
    settings_files_tags.apply_settings()

def test_wl_table_tags():
    table_tags = wl_settings_files.Wl_Table_Tags(
        main,
        settings_tags = 'header_tag_settings',
        defaults_row = ['Non-embedded', 'Header', '<TAG>', '']
    )

    table_tags.item_changed(table_tags.model().item(0, 0))
    table_tags._add_row()
    table_tags.reset_table()
    table_tags.get_tags()

def test_wl_table_tags_header():
    wl_settings_files.Wl_Table_Tags_Header(main)

def test_wl_table_tags_body():
    wl_settings_files.Wl_Table_Tags_Body(main)

def test_wl_table_tags_xml():
    table_tags_xml = wl_settings_files.Wl_Table_Tags_Xml(main)
    table_tags_xml.item_changed(table_tags_xml.model().item(0, 0))

if __name__ == '__main__':
    test_wl_settings_files()
    test_wl_settings_files_tags()

    test_wl_table_tags()
    test_wl_table_tags_header()
    test_wl_table_tags_body()
    test_wl_table_tags_xml()
