# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Sentiment analysis
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_sentiment_analysis, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()
wl_test_init.change_default_tokenizers(main)

test_sentiment_analyzers = []

for lang, sentiment_analyzers in main.settings_global['sentiment_analyzers'].items():
    for sentiment_analyzer in sentiment_analyzers:
        test_sentiment_analyzers.append((lang, sentiment_analyzer))

@pytest.mark.parametrize('lang, sentiment_analyzer', test_sentiment_analyzers)
def test_sentiment_analyze(lang, sentiment_analyzer):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    # Untokenized
    sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [test_sentence],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )
    sentiment_scores_tokenized = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [tokens],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    # Tagged texts
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    sentiment_scores_tokenized_tagged = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [[token + '_TEST' for token in tokens]],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer,
        tagged = True
    )

    print(f'{lang} / {sentiment_analyzer}:')
    print(f'{sentiment_scores}\n')

    # Check for empty results
    assert sentiment_scores
    assert sentiment_scores_tokenized

    for sentiment_score in sentiment_scores + sentiment_scores_tokenized:
        assert -1 <= sentiment_score <= 1

    # Tagged texts
    assert sentiment_scores_tokenized_tagged == sentiment_scores_tokenized

if __name__ == '__main__':
    for lang, sentiment_analyzer in test_sentiment_analyzers:
        test_sentiment_analyze(lang, sentiment_analyzer)
