# ----------------------------------------------------------------------
# Tests: NLP - Dependency parsing
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
    wl_dependency_parsing,
    wl_texts,
    wl_word_tokenization
)

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

test_dependency_parsers = []

for lang, dependency_parsers in main.settings_global['dependency_parsers'].items():
    for dependency_parser in dependency_parsers:
        if not dependency_parser.startswith(('spacy_', 'stanza_')):
            test_dependency_parsers.append((lang, dependency_parser))

@pytest.mark.parametrize('lang, dependency_parser', test_dependency_parsers)
def test_dependency_parse(lang, dependency_parser):
    tests_lang_util_skipped = False
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    match lang:
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exc_Tests_Lang_Util_Skipped(dependency_parser)

    wl_test_dependency_parse_models(lang, dependency_parser, tokens, '')
    wl_test_dependency_parse_fig_models(lang, dependency_parser, tokens)

def wl_test_dependency_parse_models(lang, dependency_parser, tokens, results):
    print(f'{lang} / {dependency_parser}:')

    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    # Untokenized
    tokens_untokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = f'\n\n{test_sentence}\n\n\n0\n\n\n',
        lang = lang,
        dependency_parser = dependency_parser
    )
    dependencies_untokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dd)
        for token in tokens_untokenized
    ]

    print(f'{dependencies_untokenized}\n')

    # Tokenized
    tokens_tokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = tokens,
        lang = lang,
        dependency_parser = dependency_parser
    )
    dependencies_tokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dd)
        for token in tokens_tokenized
    ]

    # Newline characters should be ignored
    assert dependencies_untokenized[:-1] == results

    # Check for empty dependencies
    assert dependencies_untokenized
    assert dependencies_tokenized
    assert all(dependencies_untokenized)
    assert all(dependencies_tokenized)

    for dependency in dependencies_untokenized + dependencies_tokenized:
        assert len(dependency) == 4

    # Tokenization should not be modified
    assert len(tokens) == len(dependencies_tokenized)

def wl_test_dependency_parse_fig_models(lang, dependency_parser, tokens):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    # Untokenized
    html_untokenized = wl_dependency_parsing.wl_dependency_parse_fig(
        main,
        inputs = test_sentence,
        lang = lang,
        dependency_parser = dependency_parser
    )

    # Tokenized
    html_tokenized = wl_dependency_parsing.wl_dependency_parse_fig(
        main,
        inputs = [tokens],
        lang = lang,
        dependency_parser = dependency_parser
    )

    # Check for empty HTMLs
    assert html_untokenized
    assert html_tokenized

def test__get_pipelines_to_disable():
    wl_dependency_parsing._get_pipelines_to_disable(show_pos_tags = True, show_lemmas = True)
    wl_dependency_parsing._get_pipelines_to_disable(show_pos_tags = True, show_lemmas = False)
    wl_dependency_parsing._get_pipelines_to_disable(show_pos_tags = False, show_lemmas = True)
    wl_dependency_parsing._get_pipelines_to_disable(show_pos_tags = False, show_lemmas = False)

def test_wl_show_dependency_graphs():
    htmls = wl_dependency_parsing.wl_dependency_parse_fig(
        main,
        inputs = wl_test_lang_examples.TEXT_NEWLINES,
        lang = 'eng_us',
        dependency_parser = 'stanza_eng'
    )

    wl_dependency_parsing.wl_show_dependency_graphs(main, htmls, show_in_separate_tabs = False)
    wl_dependency_parsing.wl_show_dependency_graphs(main, htmls, show_in_separate_tabs = True)

def wl_test_dependency_parse_misc():
    # Punctuation marks
    test_sentence = 'Hi, take it!'

    for dependency_parser in ('spacy_eng', 'stanza_eng'):
        tokens_untokenized = wl_dependency_parsing.wl_dependency_parse(
            main,
            inputs = test_sentence,
            lang = 'eng_us',
            dependency_parser = dependency_parser
        )

        dds_untokenized = [
            (str(token), str(token.head), token.dependency_relation, token.dd, token.dd_no_punc)
            for token in tokens_untokenized
        ]

        tokens = wl_word_tokenization.wl_word_tokenize_flat(
            main,
            text = test_sentence,
            lang = 'eng_us',
        )

        tokens_tokenized = wl_dependency_parsing.wl_dependency_parse(
            main,
            inputs = tokens,
            lang = 'eng_us',
            dependency_parser = dependency_parser
        )

        dds_tokenized = [
            (str(token), str(token.head), token.dependency_relation, token.dd, token.dd_no_punc)
            for token in tokens_tokenized
        ]

        print(f'eng_us / {dependency_parser}:')
        print(dds_untokenized)
        print(dds_tokenized)

        match dependency_parser:
            case 'spacy_eng':
                assert dds_untokenized == [('Hi', 'take', 'intj', 2, 1), (',', 'Hi', 'punct', -1, -1), ('take', 'take', 'ROOT', 0, 0), ('it', 'take', 'dobj', -1, -1), ('!', 'take', 'punct', -2, -1)]
                assert dds_tokenized == [('Hi', 'take', 'intj', 2, 1), (',', 'take', 'punct', 1, 1), ('take', 'take', 'ROOT', 0, 0), ('it', 'take', 'dobj', -1, -1), ('!', 'take', 'punct', -2, -1)]
            case 'stanza_eng':
                assert dds_untokenized == dds_tokenized == [('Hi', 'take', 'discourse', 2, 1), (',', 'Hi', 'punct', -1, -1), ('take', 'take', 'root', 0, 0), ('it', 'take', 'obj', -1, -1), ('!', 'take', 'punct', -2, -1)]

    # RTL languages
    html_untokenized = wl_dependency_parsing.wl_dependency_parse_fig(
        main,
        inputs = 'test',
        lang = 'ara'
    )

    html_tokenized = wl_dependency_parsing.wl_dependency_parse_fig(
        main,
        inputs = [[wl_texts.Wl_Token('test', lang = 'ara')]],
        lang = 'ara'
    )

    assert html_untokenized
    assert html_tokenized

    # Lemmatized
    lemmas = ['test'] * 10
    tokens_lemmatized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = wl_texts.to_tokens(['test'] * len(lemmas), lemmas = lemmas),
        lang = 'eng_us'
    )
    dependencies_lemmatized = [
        (str(token), str(token.head), token.dependency_relation, token.dd)
        for token in tokens_lemmatized
    ]

    # The preassigned lemmas should not be modified
    assert wl_texts.get_token_properties(tokens_lemmatized, 'lemma') == lemmas
    assert dependencies_lemmatized == [('test', 'test', 'compound', 1), ('test', 'test', 'compound', 1), ('test', 'test', 'compound', 1), ('test', 'test', 'compound', 1), ('test', 'test', 'compound', 1), ('test', 'test', 'compound', 4), ('test', 'test', 'compound', 3), ('test', 'test', 'compound', 2), ('test', 'test', 'compound', 1), ('test', 'test', 'root', 0)]

    # Parsed
    heads = [wl_texts.Wl_Token('head')] * 10
    tokens_parsed = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = wl_texts.to_tokens(['test'] * len(heads), heads = heads),
        lang = 'eng_us'
    )

    # The preassigned dependencies should not be modified
    assert wl_texts.get_token_properties(tokens_parsed, 'head') == heads

if __name__ == '__main__':
    for lang, dependency_parser in test_dependency_parsers:
        test_dependency_parse(lang, dependency_parser)

    test__get_pipelines_to_disable()
    test_wl_show_dependency_graphs()
    wl_test_dependency_parse_misc()
