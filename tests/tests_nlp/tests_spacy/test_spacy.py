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

from tests import wl_test_init, wl_test_lang_examples
from tests.tests_nlp import test_dependency_parsing, test_lemmatization, test_pos_tagging
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_sentence_tokenization,
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'spacy')

def wl_test_spacy(
    lang,
    results_sentence_tokenize_trf = None, results_sentence_tokenize_lg = None,
    results_word_tokenize = None,
    results_pos_tag = None, results_pos_tag_universal = None,
    results_lemmatize = None,
    results_dependency_parse = None
):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    wl_nlp_utils.check_models(main, langs = [lang], lang_utils = [[f'spacy_{lang_no_suffix}']])

    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    wl_test_sentence_tokenize(lang, results_sentence_tokenize_trf, results_sentence_tokenize_lg)
    wl_test_word_tokenize(lang, test_sentence, results_word_tokenize)

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    if lang != 'other':
        wl_test_pos_tag(lang, test_sentence, tokens, results_pos_tag, results_pos_tag_universal)
        wl_test_lemmatize(lang, test_sentence, tokens, results_lemmatize)
        wl_test_dependency_parse(lang, test_sentence, tokens, results_dependency_parse)

def wl_test_sentence_tokenize(lang, results_trf, results_lg):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    test_text = ''.join(getattr(wl_test_lang_examples, f'TEXT_{lang.upper()}'))

    if lang == 'other':
        sentence_tokenizer_trf = 'spacy_sentencizer'
    else:
        sentence_tokenizer_trf = f'spacy_dependency_parser_{lang_no_suffix}'

    sentences_trf = wl_sentence_tokenization.wl_sentence_tokenize(
        main,
        text = test_text,
        lang = lang,
        sentence_tokenizer = sentence_tokenizer_trf
    )

    print(f'{lang} / {sentence_tokenizer_trf}:')
    print(f'{sentences_trf}\n')

    # The count of sentences should be more than 1
    if lang not in ['zho_cn']:
        assert len(sentences_trf) > 1

    assert sentences_trf == results_trf

    if not wl_nlp_utils.LANGS_SPACY[lang_no_suffix].endswith('_trf'):
        sentence_tokenizer_lg = f'spacy_sentence_recognizer_{lang_no_suffix}'

        sentences_lg = wl_sentence_tokenization.wl_sentence_tokenize(
            main,
            text = test_text,
            lang = lang,
            sentence_tokenizer = sentence_tokenizer_lg
        )

        print(f'{lang} / {sentence_tokenizer_lg}:')
        print(f'{sentences_lg}\n')

        # The count of sentences should be more than 1
        assert len(sentences_lg) > 1

        assert sentences_lg == results_lg

def wl_test_word_tokenize(lang, test_sentence, results):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    word_tokenizer = f'spacy_{lang_no_suffix}'

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
    assert len(tokens) > len(test_sentence.split())

    assert wl_texts.to_display_texts(tokens) == results

def wl_test_pos_tag(lang, test_sentence, tokens, results, results_universal):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    pos_tagger = f'spacy_{lang_no_suffix}'

    test_pos_tagging.wl_test_pos_tag_models(lang, pos_tagger, test_sentence, tokens, results, results_universal)

def wl_test_lemmatize(lang, test_sentence, tokens, results):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    lemmatizer = f'spacy_{lang_no_suffix}'

    test_lemmatization.wl_test_lemmatize_models(lang, lemmatizer, test_sentence, tokens, results)

def wl_test_dependency_parse(lang, test_sentence, tokens, results):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    dependency_parser = f'spacy_{lang_no_suffix}'

    test_dependency_parsing.wl_test_dependency_parse_models(lang, dependency_parser, test_sentence, tokens, results)
