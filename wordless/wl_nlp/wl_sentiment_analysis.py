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
import importlib

import underthesea
import vaderSentiment.vaderSentiment

from wordless.wl_nlp import wl_nlp_utils, wl_texts, wl_word_tokenization
from wordless.wl_utils import wl_conversion, wl_paths

VADER_EXCEPTIONS_ENG = [
    vaderSentiment.vaderSentiment.NEGATE,
    vaderSentiment.vaderSentiment.BOOSTER_DICT,
    vaderSentiment.vaderSentiment.SENTIMENT_LADEN_IDIOMS,
    vaderSentiment.vaderSentiment.SPECIAL_CASES
]

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

        if isinstance(inputs[0], str):
            sentiment_scores = wl_sentiment_analyze_text(main, inputs, lang, sentiment_analyzer)
        else:
            sentiment_scores = wl_sentiment_analyze_tokens(main, inputs, lang, sentiment_analyzer)
    else:
        sentiment_scores = []

    return sentiment_scores

def wl_sentiment_analyze_text(main, inputs, lang, sentiment_analyzer):
    sentiment_scores = []

    # Stanza
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
    # VADER
    elif sentiment_analyzer.startswith('vader_'):
        match lang:
            case 'hyw':
                lang_vader = 'hy'
            case 'zho_cn' | 'zho_tw' | 'srp_cyrl' | 'srp_latn' | 'mni_mtei':
                lang_vader = wl_conversion.to_iso_639_1(main, lang)
            case _:
                lang_vader = wl_conversion.to_iso_639_1(main, lang, no_suffix = True)

        if lang.startswith('eng_'):
            (
                vaderSentiment.vaderSentiment.NEGATE,
                vaderSentiment.vaderSentiment.BOOSTER_DICT,
                vaderSentiment.vaderSentiment.SENTIMENT_LADEN_IDIOMS,
                vaderSentiment.vaderSentiment.SPECIAL_CASES
            ) = VADER_EXCEPTIONS_ENG
        else:
            vader_exceptions = importlib.import_module(f'data.VADER.exceptions_{lang_vader}')

            vaderSentiment.vaderSentiment.NEGATE = vader_exceptions.NEGATE
            vaderSentiment.vaderSentiment.BOOSTER_DICT = vader_exceptions.BOOSTER_DICT
            vaderSentiment.vaderSentiment.SENTIMENT_LADEN_IDIOMS = vader_exceptions.SENTIMENT_LADEN_IDIOMS
            vaderSentiment.vaderSentiment.SPECIAL_CASES = vader_exceptions.SPECIAL_CASES

        if lang.startswith('eng_'):
            analyzer = vaderSentiment.vaderSentiment.SentimentIntensityAnalyzer()
        else:
            analyzer = vaderSentiment.vaderSentiment.SentimentIntensityAnalyzer(
                lexicon_file = wl_paths.get_path_data('VADER', f'vader_lexicon_{lang_vader}.txt'),
                emoji_lexicon = wl_paths.get_path_data('VADER', f'emoji_utf8_lexicon_{lang_vader}.txt')
            )

        for sentence in inputs:
            if lang in wl_nlp_utils.LANGS_WITHOUT_SPACES:
                sentence = ' '.join(wl_word_tokenization.wl_word_tokenize_flat(main, sentence, lang))

            sentiment_scores.append(analyzer.polarity_scores(sentence)['compound'])
    # Vietnamese
    elif sentiment_analyzer == 'underthesea_vie':
        for sentence in inputs:
            sentiment = underthesea.sentiment(sentence) # pylint: disable=no-member

            if sentiment == 'positive':
                sentiment_scores.append(1)
            elif sentiment == 'negative':
                sentiment_scores.append(-1)
            else:
                sentiment_scores.append(0)

    return sentiment_scores

def wl_sentiment_analyze_tokens(main, inputs, lang, sentiment_analyzer):
    sentiment_scores = []

    # Stanza
    if sentiment_analyzer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'stanza_nlp_{lang}']

        for tokens_input in inputs:
            # If the input is too long, use the sentiment with the highest frequency as the sentiment score of the input
            sentiments = []

            for doc in nlp.bulk_process([
                [wl_texts.to_token_texts(tokens)]
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
