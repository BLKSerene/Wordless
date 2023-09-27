# ----------------------------------------------------------------------
# Wordless: NLP - Sentiment analysis
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

# pylint: disable=unused-argument

import collections

import dostoevsky.models
import underthesea

from wordless.wl_nlp import wl_matching, wl_nlp_utils
from wordless.wl_utils import wl_conversion

def wl_sentiment_analyze(main, inputs, lang, sentiment_analyzer = 'default', tagged = False):
    if sentiment_analyzer == 'default':
        sentiment_analyzer = main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings'][lang]

    wl_nlp_utils.init_sentiment_analyzers(
        main,
        lang = lang,
        sentiment_analyzer = sentiment_analyzer,
        tokenized = not isinstance(inputs[0], str)
    )

    if inputs:
        if isinstance(inputs[0], str):
            sentiment_scores = wl_sentiment_analyze_text(main, inputs, lang, sentiment_analyzer)
        else:
            sentiment_scores = wl_sentiment_analyze_tokens(main, inputs, lang, sentiment_analyzer, tagged)
    else:
        sentiment_scores = []

    return sentiment_scores

# A fake word tokenizer that just splits text by whitespace
class Dostoevsky_Tokenizer:
    def split(self, text, lemmatize = False):
        return [(token.strip(), None) for token in text.split()]

def wl_sentiment_analyze_text(main, inputs, lang, sentiment_analyzer):
    sentiment_scores = []

    # Stanza:
    if sentiment_analyzer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'stanza_nlp_{lang}']

        for sentence_input in inputs:
            # If the input is split into multiple sentences, use the sentiment with the highest frequency as the sentiment score of the input
            sentiments = []

            for sentence in nlp(sentence_input).sentences:
                sentiments.append(sentence.sentiment)

            if sentiments:
                sentiment_scores.append(collections.Counter(sentiments).most_common(1)[0][0] - 1)
            else:
                sentiment_scores.append(0)

    # Russian
    elif sentiment_analyzer == 'dostoevsky_rus':
        model = dostoevsky.models.FastTextSocialNetworkModel(tokenizer = Dostoevsky_Tokenizer())

        for sentiments in model.predict(inputs, k = 5):
            sentiment = sorted(sentiments.items(), key = lambda item: item[1], reverse = True)[0][0]

            if sentiment == 'positive':
                sentiment_scores.append(1)
            elif sentiment == 'negative':
                sentiment_scores.append(-1)
            elif sentiment in ['neutral', 'speech', 'skip']:
                sentiment_scores.append(0)
    # Vietnamese
    elif sentiment_analyzer == 'underthesea_vie':
        for sentence in inputs:
            sentiment = underthesea.sentiment(sentence)

            if sentiment == 'positive':
                sentiment_scores.append(1)
            elif sentiment == 'negative':
                sentiment_scores.append(-1)
            else:
                sentiment_scores.append(0)

    return sentiment_scores

def wl_sentiment_analyze_tokens(main, inputs, lang, sentiment_analyzer, tagged):
    sentiment_scores = []

    if tagged:
        inputs = [wl_matching.split_tokens_tags(main, tokens)[0] for tokens in inputs]

    # Stanza
    if sentiment_analyzer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'stanza_nlp_{lang}']

        for tokens_input in inputs:
            # If the input is too long, use the sentiment with the highest frequency as the sentiment score of the input
            sentiments = []

            for doc in nlp.bulk_process([
                [tokens]
                for tokens in wl_nlp_utils.split_token_list(main, tokens_input, sentiment_analyzer)
            ]):
                for sentence in doc.sentences:
                    sentiments.append(sentence.sentiment)

            if sentiments:
                sentiment_scores.append(collections.Counter(sentiments).most_common(1)[0][0] - 1)
            else:
                sentiment_scores.append(0)
    else:
        inputs = [' '.join(tokens) for tokens in inputs]

        sentiment_scores = wl_sentiment_analyze_text(main, inputs, lang, sentiment_analyzer)

    return sentiment_scores
