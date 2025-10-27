# ----------------------------------------------------------------------
# Tests: Settings - Sentiment Analysis
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
from wordless.wl_settings import wl_settings_sentiment_analysis

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def test_wl_settings_sentiment_analysis():
    main.settings_sentiment_analysis = wl_settings_sentiment_analysis.Wl_Settings_Sentiment_Analysis(main)
    main.settings_sentiment_analysis.load_settings(defaults = False)
    main.settings_sentiment_analysis.load_settings(defaults = True)
    main.settings_sentiment_analysis.apply_settings()

    main.settings_sentiment_analysis.text_edit_preview_samples.setPlainText('')
    main.settings_sentiment_analysis.preview_changed()
    main.settings_sentiment_analysis.text_edit_preview_samples.setPlainText('test')
    main.settings_sentiment_analysis.preview_changed()

    main.settings_sentiment_analysis.preview_results_changed()
    main.settings_sentiment_analysis.update_gui('0.123456789')
    main.settings_sentiment_analysis.update_gui_err()

    # Force the model download to fail
    worker_download_model_stanza_temp = wl_nlp_utils.Wl_Worker_Download_Model_Stanza
    wl_nlp_utils.Wl_Worker_Download_Model_Stanza = wl_test_init.Wl_Worker_Download_Model_Stanza_Err_Msg
    main.settings_sentiment_analysis.preview_results_changed()
    wl_nlp_utils.Wl_Worker_Download_Model_Stanza = worker_download_model_stanza_temp

def test_wl_worker_preview_sentiment_analyzer():
    main.settings_custom['sentiment_analysis']['preview']['preview_samples'] = wl_test_lang_examples.TEXT_NEWLINES
    preview_lang = main.settings_custom['sentiment_analysis']['preview']['preview_lang']
    sentiment_analyzer = main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings'][preview_lang]

    worker = wl_settings_sentiment_analysis.Wl_Worker_Preview_Sentiment_Analyzer(
        main,
        sentiment_analyzer = sentiment_analyzer
    )
    worker.finished.connect(update_gui_newlines)
    worker.run()

def update_gui_newlines(preview_results):
    precision = main.settings_custom['tables']['precision_settings']['precision_decimals']

    assert preview_results == wl_test_lang_examples.TEXT_NEWLINES.replace('0', f'{0:.{precision}f}')

if __name__ == '__main__':
    test_wl_settings_sentiment_analysis()
    test_wl_worker_preview_sentiment_analyzer()
