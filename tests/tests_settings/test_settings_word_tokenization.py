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

from tests import (
    wl_test_init,
    wl_test_lang_examples
)
from wordless.wl_nlp import wl_nlp_utils
from wordless.wl_settings import wl_settings_word_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_word_tokenization():
    main.settings_word_tokenization = wl_settings_word_tokenization.Wl_Settings_Word_Tokenization(main)
    main.settings_word_tokenization.load_settings(defaults = False)
    main.settings_word_tokenization.load_settings(defaults = True)
    main.settings_word_tokenization.apply_settings()

    # Reload settings
    main.switch_lang_utils_fast()
    main.settings_word_tokenization.load_settings()

    main.settings_word_tokenization.text_edit_preview_samples.setPlainText('')
    main.settings_word_tokenization.preview_changed()
    main.settings_word_tokenization.text_edit_preview_samples.setPlainText('test')
    main.settings_word_tokenization.preview_changed()

    main.settings_word_tokenization.preview_results_changed()
    main.settings_word_tokenization.worker_preview_word_tokenizer.stop()
    main.settings_word_tokenization.abort()
    main.settings_word_tokenization.update_gui('test')
    main.settings_word_tokenization.update_gui_err()

    # Force the model download to fail
    check_models_temp = wl_nlp_utils.check_models
    wl_nlp_utils.check_models = lambda parent, langs, lang_utils: False
    main.settings_word_tokenization.preview_results_changed()
    wl_nlp_utils.check_models = check_models_temp

def test_wl_worker_preview_word_tokenizer():
    main.settings_custom['word_tokenization']['preview']['preview_lang'] = 'vie'
    main.settings_custom['word_tokenization']['preview']['preview_samples'] = wl_test_lang_examples.TEXT_NEWLINES
    preview_lang = main.settings_custom['word_tokenization']['preview']['preview_lang']
    word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizer_settings'][preview_lang]

    worker = wl_settings_word_tokenization.Wl_Worker_Preview_Word_Tokenizer(
        main,
        word_tokenizer = word_tokenizer
    )
    worker.finished.connect(update_gui_newlines)
    worker.run()

    worker.finished.disconnect()
    worker.stop()
    worker.run()

def update_gui_newlines(preview_results):
    assert preview_results == wl_test_lang_examples.TEXT_NEWLINES

if __name__ == '__main__':
    test_wl_settings_word_tokenization()
    test_wl_worker_preview_word_tokenizer()
