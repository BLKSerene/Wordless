# ----------------------------------------------------------------------
# Tests: NLP - Sentiment analysis
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

import pytest

from tests import (
    wl_test_init,
    wl_test_lang_examples
)
from wordless.wl_nlp import (
    wl_sentiment_analysis,
    wl_texts,
    wl_word_tokenization
)

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

test_sentiment_analyzers = []

for lang, sentiment_analyzers in main.settings_global['sentiment_analyzers'].items():
    for sentiment_analyzer in sentiment_analyzers:
        if not sentiment_analyzer.startswith('stanza_'):
            test_sentiment_analyzers.append((lang, sentiment_analyzer))

@pytest.mark.parametrize('lang, sentiment_analyzer', test_sentiment_analyzers)
def test_sentiment_analyze(lang, sentiment_analyzer):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    wl_test_sentiment_analyze_models(lang, sentiment_analyzer, test_sentence, tokens, '', check_results = False)

def wl_test_sentiment_analyze_models(lang, sentiment_analyzer, test_sentence, tokens, results, check_results = True):
    # Untokenized
    sentiment_scores_untokenized = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [test_sentence],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    print(f'{lang} / {sentiment_analyzer}:')
    print(f'{sentiment_scores_untokenized}\n')

    # Tokenized
    sentiment_scores_tokenized = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [tokens],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    if check_results:
        assert sentiment_scores_untokenized == results
        assert sentiment_scores_tokenized == results
    # Check for empty results
    else:
        assert sentiment_scores_untokenized
        assert sentiment_scores_tokenized

    for sentiment_score in sentiment_scores_untokenized + sentiment_scores_tokenized:
        assert -1 <= sentiment_score <= 1

    # Newlines
    sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = list(wl_test_lang_examples.TEXT_NEWLINES),
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    for sentiment_score, char in zip(sentiment_scores, wl_test_lang_examples.TEXT_NEWLINES):
        if sentiment_score is None:
            assert char == '\n'
        else:
            assert -1 <= sentiment_score <= 1

    # Long
    if sentiment_analyzer.startswith('stanza_'):
        main.settings_custom['files']['misc_settings']['read_files_in_chunks_chars'] = 99

        sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
            main,
            inputs = ['\n'.join(wl_test_lang_examples.TOKENS_LONG)],
            lang = lang,
            sentiment_analyzer = sentiment_analyzer
        )

        assert sentiment_scores

        for sentiment_score in sentiment_scores:
            assert -1 <= sentiment_score <= 1

        sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
            main,
            inputs = [wl_texts.to_tokens(wl_test_lang_examples.TOKENS_LONG, lang = lang)],
            lang = lang,
            sentiment_analyzer = sentiment_analyzer
        )

        assert sentiment_scores

        for sentiment_score in sentiment_scores:
            assert -1 <= sentiment_score <= 1

        main.settings_custom['files']['misc_settings']['read_files_in_chunks_chars'] = main.settings_default['files']['misc_settings']['read_files_in_chunks_chars']

def test_sentiment_analyze_misc():
    # Vietnamese
    assert wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = ['Tốt', 'buồn', 'ngày'],
        lang = 'vie',
        sentiment_analyzer = 'underthesea_vie'
    ) == [1, -1, 0]

    # Empty text or tokens
    assert wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [''],
        lang = 'eng_us',
        sentiment_analyzer = 'stanza_eng'
    ) == [None]

    assert wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [[]],
        lang = 'eng_us',
        sentiment_analyzer = 'stanza_eng'
    ) == [0]

    # Empty input
    assert not wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = '',
        lang = 'eng_us'
    )

if __name__ == '__main__':
    for lang, sentiment_analyzer in test_sentiment_analyzers:
        test_sentiment_analyze(lang, sentiment_analyzer)

    test_sentiment_analyze_misc()
