# ----------------------------------------------------------------------
# Wordless: NLP - Sentiment analysis
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

# pylint: disable=unused-argument

import collections

import underthesea
import vaderSentiment.vaderSentiment

from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_texts
)
from wordless.wl_utils import wl_conversion

def wl_sentiment_analyze(main, inputs, lang, sentiment_analyzer = 'default'):
    if sentiment_analyzer == 'default':
        sentiment_analyzer = main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings'][lang]

    if inputs:
        wl_nlp_utils.init_sentiment_analyzers(
            main,
            lang = lang,
            sentiment_analyzer = sentiment_analyzer,
            tokenized = not isinstance(inputs[0], str)
        )

        # Only for Settings - Sentiment Analysis - Preview
        if isinstance(inputs[0], str):
            sentiment_scores = wl_sentiment_analyze_text(main, inputs, lang, sentiment_analyzer)
        # Only for Concordancer - Sentiment Score
        else:
            sentiment_scores = wl_sentiment_analyze_tokens(main, inputs, lang, sentiment_analyzer)
    else:
        sentiment_scores = []

    return sentiment_scores

def wl_sentiment_analyze_text(main, sentences, lang, sentiment_analyzer):
    sentiment_scores = []

    # Stanza
    if sentiment_analyzer.startswith('stanza_'):
        if lang != 'zho_cn':
            lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
        else:
            lang_stanza = lang

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']

        for sentence in sentences:
            if (sentence := sentence.strip()):
                # If the input is split into multiple sentences, use the sentiment with the highest frequency as the sentiment score of the input
                sentiments = []

                for sentenge_seg in nlp(sentence).sentences:
                    sentiments.append(sentenge_seg.sentiment)

                sentiment_scores.append(collections.Counter(sentiments).most_common(1)[0][0] - 1)
            else:
                sentiment_scores.append(None)
    # VADER
    elif sentiment_analyzer == 'vader_eng':
        analyzer = vaderSentiment.vaderSentiment.SentimentIntensityAnalyzer()

        for sentence in sentences:
            if (sentence := sentence.strip()):
                sentiment_scores.append(analyzer.polarity_scores(sentence)['compound'])
            else:
                sentiment_scores.append(None)
    # Vietnamese
    elif sentiment_analyzer == 'underthesea_vie':
        for sentence in sentences:
            if (sentence := sentence.strip()):
                sentiment = underthesea.sentiment(sentence) # pylint: disable=no-member

                match sentiment:
                    case 'positive':
                        sentiment_scores.append(1)
                    case 'negative':
                        sentiment_scores.append(-1)
                    case _:
                        sentiment_scores.append(0)
            else:
                sentiment_scores.append(None)

    return sentiment_scores

def wl_sentiment_analyze_tokens(main, sentences, lang, sentiment_analyzer):
    sentiment_scores = []

    # Stanza
    if sentiment_analyzer.startswith('stanza_'):
        if lang != 'zho_cn':
            lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
        else:
            lang_stanza = lang

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']

        for sentence_tokens in sentences:
            # If the input is too long, use the sentiment with the highest frequency as the sentiment score of the input
            sentiments = []

            for doc in nlp.bulk_process([
                [wl_texts.to_token_texts(tokens)]
                for tokens in wl_nlp_utils.split_tokens(main, sentence_tokens, sentiment_analyzer)
            ]):
                for sentence in doc.sentences:
                    sentiments.append(sentence.sentiment)

            if sentiments:
                sentiment_scores.append(collections.Counter(sentiments).most_common(1)[0][0] - 1)
            else:
                sentiment_scores.append(0)
    else:
        sentences = (' '.join(tokens) for tokens in sentences)

        sentiment_scores = wl_sentiment_analyze_text(main, sentences, lang, sentiment_analyzer)

    return sentiment_scores
