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

from tests import (
    wl_test_init,
    wl_test_lang_examples
)
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_pos_tagging
)
from wordless.wl_settings import wl_settings_pos_tagging
from wordless.wl_widgets import wl_layouts

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_pos_tagging():
    main.settings_pos_tagging = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging(main)
    main.settings_pos_tagging.load_settings(defaults = False)
    main.settings_pos_tagging.load_settings(defaults = True)
    main.settings_pos_tagging.apply_settings()

    # Reload settings
    main.switch_lang_utils_fast()
    main.settings_pos_tagging.load_settings()

    main.settings_pos_tagging.text_edit_preview_samples.setPlainText('')
    main.settings_pos_tagging.preview_changed()
    main.settings_pos_tagging.text_edit_preview_samples.setPlainText('test\n')
    main.settings_pos_tagging.preview_changed()

    main.settings_pos_tagging.checkbox_to_universal_pos_tags.setChecked(False)
    main.settings_pos_tagging.preview_results_changed()

    main.settings_pos_tagging_universal = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging(main)
    main.settings_pos_tagging_universal.load_settings()
    main.settings_pos_tagging_universal.checkbox_to_universal_pos_tags.setChecked(True)
    main.settings_pos_tagging_universal.preview_results_changed()

    main.settings_pos_tagging.preview_changed()
    main.settings_pos_tagging.update_gui('test')
    main.settings_pos_tagging.update_gui_err()

    # Force the model download to fail
    check_models_temp = wl_nlp_utils.check_models
    wl_nlp_utils.check_models = lambda parent, langs, lang_utils: False
    main.settings_pos_tagging.preview_results_changed()
    wl_nlp_utils.check_models = check_models_temp

def test_wl_worker_preview_pos_tagger():
    main.settings_custom['pos_tagging']['preview']['preview_samples'] = wl_test_lang_examples.TEXT_NEWLINES
    preview_lang = main.settings_custom['pos_tagging']['preview']['preview_lang']
    pos_tagger = main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'][preview_lang]

    worker = wl_settings_pos_tagging.Wl_Worker_Preview_Pos_Tagger(
        main,
        pos_tagger = pos_tagger,
        tagset = 'raw',
        separator = main.settings_custom['pos_tagging']['pos_tagger_settings']['separator_between_tokens_pos_tags']
    )
    worker.finished.connect(update_gui_newlines)
    worker.run()

def update_gui_newlines(preview_results):
    assert preview_results == wl_test_lang_examples.TEXT_NEWLINES.replace('0', '0_LS')

def test_wl_settings_pos_tagging_tagsets():
    main.settings_pos_tagging_tagsets = wl_settings_pos_tagging.Wl_Settings_Pos_Tagging_Tagsets(main)
    main.settings_pos_tagging_tagsets.scroll_area_settings = wl_layouts.Wl_Scroll_Area(main.settings_pos_tagging_tagsets)
    main.settings_pos_tagging_tagsets.load_settings(defaults = False)
    main.settings_pos_tagging_tagsets.load_settings(defaults = True)

    # Reload settings
    main.switch_lang_utils_fast()
    main.settings_pos_tagging.load_settings()

    main.settings_custom['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger']['eng_us'] = 'nltk_perceptron_eng'
    main.settings_pos_tagging_tagsets.preview_lang_changed()
    main.settings_custom['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger']['eng_us'] = 'spacy_eng'
    main.settings_pos_tagging_tagsets.preview_lang_changed()

    main.settings_pos_tagging_tagsets.preview_pos_tagger_changed()
    main.settings_pos_tagging_tagsets.update_gui([['test', 'test', 'test', 'test', 'test']])
    main.settings_custom['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger']['eng_us'] = 'nltk_perceptron_eng'
    main.settings_pos_tagging_tagsets.reset_currently_shown_table()

    main.settings_pos_tagging_tagsets.pos_tag_mappings_loaded = True
    main.settings_pos_tagging_tagsets.apply_settings()

# Check missing and extra universal tagset mappings
def test_wl_settings_pos_tagging_tagsets_universal_tagsets():
    universal_tagsets_spacy = set()
    universal_tagsets_stanza = set()

    for mappings in main.settings_default['pos_tagging']['tagsets']['mapping_settings'].values():
        for pos_tagger in mappings:
            if pos_tagger.startswith('spacy_') or pos_tagger == 'modern_botok_bod':
                universal_tagsets_spacy.add(pos_tagger)
            elif pos_tagger.startswith('stanza_'):
                universal_tagsets_stanza.add(pos_tagger)

    for tagsets_mappings, tagsets_universal in (
        (universal_tagsets_spacy, wl_pos_tagging.UNIVERSAL_TAGSETS_SPACY),
        (universal_tagsets_stanza, wl_pos_tagging.UNIVERSAL_TAGSETS_STANZA)
    ):
        for tagset in tagsets_universal:
            assert tagset in tagsets_mappings, f'Missing universal tagset mapping for {tagset} found!'

        for tagset in tagsets_mappings:
            assert tagset in tagsets_universal, f'Extra universal tagset mapping for {tagset} found!'

def test_wl_worker_fetch_data_tagsets():
    wl_settings_pos_tagging.Wl_Worker_Fetch_Data_Tagsets(
        main,
        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress(main, '')
    ).run()

if __name__ == '__main__':
    test_wl_settings_pos_tagging()
    test_wl_worker_preview_pos_tagger()

    test_wl_settings_pos_tagging_tagsets()
    test_wl_worker_fetch_data_tagsets()
    test_wl_settings_pos_tagging_tagsets_universal_tagsets()
