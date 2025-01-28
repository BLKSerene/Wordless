# ----------------------------------------------------------------------
# Tests: Settings - Word Tokenization
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
from wordless.wl_settings import wl_settings_word_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_word_tokenization():
    settings_word_tokenization = wl_settings_word_tokenization.Wl_Settings_Word_Tokenization(main)
    settings_word_tokenization.load_settings()
    settings_word_tokenization.load_settings(defaults = True)
    settings_word_tokenization.apply_settings()

    settings_word_tokenization.preview_changed()
    settings_word_tokenization.update_gui('test')
    settings_word_tokenization.update_gui_err()

if __name__ == '__main__':
    test_wl_settings_word_tokenization()
