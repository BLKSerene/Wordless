# ----------------------------------------------------------------------
# Tests: Settings - Sentence Tokenization
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
from wordless.wl_settings import wl_settings_sentence_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_sentence_tokenization():
    main.settings_sentence_tokenization = wl_settings_sentence_tokenization.Wl_Settings_Sentence_Tokenization(main)
    main.settings_sentence_tokenization.load_settings(defaults = False)
    main.settings_sentence_tokenization.load_settings(defaults = True)
    main.settings_sentence_tokenization.apply_settings()

    main.settings_sentence_tokenization.text_edit_preview_samples.setPlainText('')
    main.settings_sentence_tokenization.preview_changed()
    main.settings_sentence_tokenization.text_edit_preview_samples.setPlainText('test')
    main.settings_sentence_tokenization.preview_changed()

    main.settings_sentence_tokenization.preview_results_changed()
    main.settings_sentence_tokenization.update_gui('test')
    main.settings_sentence_tokenization.update_gui_err()

def test_wl_worker_preview_sentence_tokenizer():
    main.settings_custom['sentence_tokenization']['preview']['preview_samples'] = wl_test_lang_examples.TEXT_NEWLINES
    preview_lang = main.settings_custom['sentence_tokenization']['preview']['preview_lang']
    sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'][preview_lang]

    worker = wl_settings_sentence_tokenization.Wl_Worker_Preview_Sentence_Tokenizer(
        main,
        sentence_tokenizer = sentence_tokenizer
    )
    worker.finished.connect(update_gui_newlines)
    worker.run()

def update_gui_newlines(preview_results):
    assert preview_results == wl_nlp_utils.clean_texts(wl_test_lang_examples.TEXT_NEWLINES)

if __name__ == '__main__':
    test_wl_settings_sentence_tokenization()
    test_wl_worker_preview_sentence_tokenizer()
