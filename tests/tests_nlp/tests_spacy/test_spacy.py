# ----------------------------------------------------------------------
# Tests: NLP - spaCy
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
from tests.tests_nlp import (
    test_dependency_parsing,
    test_lemmatization,
    test_pos_tagging,
    test_sentence_tokenization,
    test_word_tokenization
)
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_word_tokenization
)
from wordless.wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'spacy')

def wl_test_spacy(
    lang,
    results_sentence_tokenize_dependency_parser = None,
    results_sentence_tokenize_sentence_recognizer = None,
    results_word_tokenize = None,
    results_pos_tag = None, results_pos_tag_universal = None,
    results_lemmatize = None,
    results_dependency_parse = None
):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(lang)
    wl_nlp_utils.check_models(main, langs = [lang], lang_utils = [[f'spacy_{lang_no_suffix}']])

    if lang != 'other':
        wl_test_sentence_tokenize(
            lang,
            results_sentence_tokenize_dependency_parser,
            results_sentence_tokenize_sentence_recognizer
        )

    wl_test_word_tokenize(lang, results_word_tokenize)

    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    if lang != 'other':
        wl_test_pos_tag(lang, tokens, results_pos_tag, results_pos_tag_universal)
        wl_test_lemmatize(lang, tokens, results_lemmatize)
        wl_test_dependency_parse(lang, tokens, results_dependency_parse)

def wl_test_sentence_tokenize(lang, results_dependency_parser, results_sentence_recognizer):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(lang)

    test_sentence_tokenization.wl_test_sentence_tokenize_models(
        lang = lang,
        sentence_tokenizer = f'spacy_dependency_parser_{lang_no_suffix}',
        results = results_dependency_parser
    )
    test_sentence_tokenization.wl_test_sentence_tokenize_models(
        lang = lang,
        sentence_tokenizer = f'spacy_sentence_recognizer_{lang_no_suffix}',
        results = results_sentence_recognizer
    )

def wl_test_word_tokenize(lang, results):
    if lang == 'other':
        lang = 'eng_us'

    word_tokenizer = f'spacy_{wl_conversion.remove_lang_code_suffixes(lang)}'

    test_word_tokenization.wl_test_word_tokenize_models(lang, word_tokenizer, results)

def wl_test_pos_tag(lang, tokens, results, results_universal):
    pos_tagger = f'spacy_{wl_conversion.remove_lang_code_suffixes(lang)}'

    test_pos_tagging.wl_test_pos_tag_models(lang, pos_tagger, tokens, results, results_universal)

def wl_test_lemmatize(lang, tokens, results):
    lemmatizer = f'spacy_{wl_conversion.remove_lang_code_suffixes(lang)}'

    test_lemmatization.wl_test_lemmatize_models(lang, lemmatizer, tokens, results)

def wl_test_dependency_parse(lang, tokens, results):
    dependency_parser = f'spacy_{wl_conversion.remove_lang_code_suffixes(lang)}'

    test_dependency_parsing.wl_test_dependency_parse_models(lang, dependency_parser, tokens, results)
    test_dependency_parsing.wl_test_dependency_parse_fig_models(lang, dependency_parser, tokens)
