# ----------------------------------------------------------------------
# Tests: Settings - Lemmatization
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
from wordless.wl_settings import wl_settings_lemmatization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_lemmatization():
    main.settings_lemmatization = wl_settings_lemmatization.Wl_Settings_Lemmatization(main)
    main.settings_lemmatization.load_settings(defaults = False)
    main.settings_lemmatization.load_settings(defaults = True)
    main.settings_lemmatization.apply_settings()

    main.settings_lemmatization.text_edit_preview_samples.setPlainText('')
    main.settings_lemmatization.preview_changed()
    main.settings_lemmatization.text_edit_preview_samples.setPlainText('test\n')
    main.settings_lemmatization.preview_changed()

    main.settings_lemmatization.preview_results_changed()
    main.settings_lemmatization.worker_preview_lemmatizer.stop()
    main.settings_lemmatization.abort()
    main.settings_lemmatization.update_gui('test')
    main.settings_lemmatization.update_gui_err()

def test_wl_worker_preview_lemmatizer():
    preview_lang = main.settings_custom['lemmatization']['preview']['preview_lang']
    lemmatizer = main.settings_custom['lemmatization']['lemmatizer_settings'][preview_lang]

    worker = wl_settings_lemmatization.Wl_Worker_Preview_Lemmatizer(
        main,
        lemmatizer = lemmatizer
    )
    worker.run()
    worker.stop()
    worker.run()

if __name__ == '__main__':
    test_wl_settings_lemmatization()
    test_wl_worker_preview_lemmatizer()
