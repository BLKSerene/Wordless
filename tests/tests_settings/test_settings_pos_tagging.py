# ----------------------------------------------------------------------
# Tests: Settings - Part-of-speech Tagging
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
from wordless.wl_settings import wl_settings_pos_tagging
from wordless.wl_widgets import wl_layouts

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_pos_tagging():
    settings_pos_tagging = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging(main)
    settings_pos_tagging.load_settings()
    settings_pos_tagging.load_settings(defaults = True)
    settings_pos_tagging.apply_settings()

    settings_pos_tagging.preview_changed()
    settings_pos_tagging.update_gui('test')
    settings_pos_tagging.update_gui_err()

def test_wl_settings_pos_tagging_tagsets():
    settings_pos_tagging_tagsets = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging_Tagsets(main)
    settings_pos_tagging_tagsets.scroll_area_settings = wl_layouts.Wl_Scroll_Area(settings_pos_tagging_tagsets)
    settings_pos_tagging_tagsets.load_settings()
    settings_pos_tagging_tagsets.load_settings(defaults = True)
    settings_pos_tagging_tagsets.apply_settings()

    settings_pos_tagging_tagsets.preview_lang_changed()
    settings_pos_tagging_tagsets.preview_pos_tagger_changed()
    settings_pos_tagging_tagsets.update_gui([['test', 'test', 'test', 'test', 'test']])
    main.settings_custom['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger']['eng_us'] = 'nltk_perceptron_eng'
    settings_pos_tagging_tagsets.reset_currently_shown_table()

if __name__ == '__main__':
    test_wl_settings_pos_tagging()
    test_wl_settings_pos_tagging_tagsets()
