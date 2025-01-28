# ----------------------------------------------------------------------
# Tests: NLP - Stanza
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

from tests import wl_test_init, wl_test_lang_examples
from tests.tests_nlp import (
    test_dependency_parsing,
    test_lemmatization,
    test_pos_tagging,
    test_sentiment_analysis
)
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_sentence_tokenization,
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'stanza')

def wl_test_stanza(
    lang,
    results_sentence_tokenize = None,
    results_word_tokenize = None,
    results_pos_tag = None, results_pos_tag_universal = None,
    results_lemmatize = None,
    results_dependency_parse = None,
    results_sentiment_analayze = None
):
    wl_nlp_utils.check_models(main, langs = [lang], lang_utils = [[wl_test_get_lang_util(main, lang)]])

    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    if lang in wl_nlp_utils.get_langs_stanza(main, util_type = 'word_tokenizers'):
        wl_test_sentence_tokenize(lang, results_sentence_tokenize)
        wl_test_word_tokenize(lang, test_sentence, results_word_tokenize)

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    if lang in wl_nlp_utils.get_langs_stanza(main, util_type = 'pos_taggers'):
        wl_test_pos_tag(lang, test_sentence, tokens, results_pos_tag, results_pos_tag_universal)

    if lang in wl_nlp_utils.get_langs_stanza(main, util_type = 'lemmatizers'):
        wl_test_lemmatize(lang, test_sentence, tokens, results_lemmatize)

    if lang in wl_nlp_utils.get_langs_stanza(main, util_type = 'dependency_parsers'):
        wl_test_dependency_parse(lang, test_sentence, tokens, results_dependency_parse)

    if lang in wl_nlp_utils.get_langs_stanza(main, util_type = 'sentiment_analyzers'):
        wl_test_sentiment_analyze(lang, test_sentence, tokens, results_sentiment_analayze)

def wl_test_get_lang_util(main, lang):
    if lang in ['zho_cn', 'zho_tw', 'srp_latn']:
        lang_util = f'stanza_{lang}'
    else:
        lang_util = f'stanza_{wl_conversion.remove_lang_code_suffixes(main, lang)}'

    return lang_util

def wl_test_sentence_tokenize(lang, results):
    test_text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))
    sentence_tokenizer = wl_test_get_lang_util(main, lang)

    sentences = wl_sentence_tokenization.wl_sentence_tokenize(
        main,
        text = test_text,
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    print(f'{lang} / {sentence_tokenizer}:')
    print(f'{sentences}\n')

    # The count of sentences should be more than 1
    if lang in ['ara', 'fro', 'kaz', 'pcm', 'qpm']:
        assert len(sentences) == 1
    else:
        assert len(sentences) > 1

    assert sentences == results

def wl_test_word_tokenize(lang, test_sentence, results):
    word_tokenizer = wl_test_get_lang_util(main, lang)

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang,
        word_tokenizer = word_tokenizer
    )

    print(f'{lang} / {word_tokenizer}:')
    print(f'{tokens}\n')

    # The count of tokens should be more than 1
    assert len(tokens) > 1
    # The count of tokens should be more than the length of tokens split by space
    if lang in ['chu', 'cop', 'pcm', 'orv']:
        assert len(tokens) == len(test_sentence.split())
    elif lang == 'vie':
        assert len(tokens) < len(test_sentence.split())
    else:
        assert len(tokens) > len(test_sentence.split())

    assert wl_texts.to_display_texts(tokens) == results

def wl_test_pos_tag(lang, test_sentence, tokens, results, results_universal):
    pos_tagger = wl_test_get_lang_util(main, lang)

    test_pos_tagging.wl_test_pos_tag_models(lang, pos_tagger, test_sentence, tokens, results, results_universal)

def wl_test_lemmatize(lang, test_sentence, tokens, results):
    lemmatizer = wl_test_get_lang_util(main, lang)

    test_lemmatization.wl_test_lemmatize_models(
        lang, lemmatizer, test_sentence, tokens, results,
        lang_exceptions = [
            'xcl', 'bul', 'chu', 'cop', 'ang', 'est', 'got', 'grc', 'ell', 'hin',
            'isl', 'lij', 'lit', 'glv', 'pcm', 'pol', 'orv', 'sme', 'san', 'tur',
            'cym'
        ]
    )

def wl_test_dependency_parse(lang, test_sentence, tokens, results):
    dependency_parser = wl_test_get_lang_util(main, lang)

    test_dependency_parsing.wl_test_dependency_parse_models(lang, dependency_parser, test_sentence, tokens, results)

def wl_test_sentiment_analyze(lang, test_sentence, tokens, results):
    sentiment_analyzer = wl_test_get_lang_util(main, lang)

    test_sentiment_analysis.wl_test_sentiment_analyze_models(lang, sentiment_analyzer, test_sentence, tokens, results)
