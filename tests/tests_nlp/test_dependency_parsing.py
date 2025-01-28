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

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_dependency_parsing, wl_texts, wl_word_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

test_dependency_parsers = []

for lang, dependency_parsers in main.settings_global['dependency_parsers'].items():
    for dependency_parser in dependency_parsers:
        if not dependency_parser.startswith(('spacy_', 'stanza_')):
            test_dependency_parsers.append((lang, dependency_parser))

@pytest.mark.parametrize('lang, dependency_parser', test_dependency_parsers)
def test_dependency_parse(lang, dependency_parser):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )

    wl_test_dependency_parse_models(lang, dependency_parser, test_sentence, tokens, '')

def wl_test_dependency_parse_models(lang, dependency_parser, test_sentence, tokens, results):
    # Untokenized
    tokens_untokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = test_sentence,
        lang = lang,
        dependency_parser = dependency_parser
    )
    dependencies_untokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dependency_len)
        for token in tokens_untokenized
    ]

    print(f'{lang} / {dependency_parser}:')
    print(f'{dependencies_untokenized}\n')

    # Tokenized
    tokens_tokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = tokens,
        lang = lang,
        dependency_parser = dependency_parser
    )
    dependencies_tokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dependency_len)
        for token in tokens_tokenized
    ]

    assert dependencies_untokenized == results

    # Check for empty dependencies
    assert dependencies_untokenized
    assert dependencies_tokenized
    assert all(dependencies_untokenized)
    assert all(dependencies_tokenized)

    for dependency in dependencies_untokenized + dependencies_tokenized:
        assert len(dependency) == 4

    # Tokenization should not be modified
    assert len(tokens) == len(dependencies_tokenized)

    # Tagged
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    tokens_tagged = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = [wl_texts.Wl_Token(token, tag = '_TEST') for token in tokens],
        lang = lang,
        dependency_parser = dependency_parser
    )
    dependencies_tagged = [
        (str(token), str(token.head), token.dependency_relation, token.dependency_len)
        for token in tokens_tagged
    ]

    assert dependencies_tagged == dependencies_tokenized

    # Long
    tokens_long = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = wl_texts.to_tokens(wl_test_lang_examples.TOKENS_LONG, lang = lang),
        lang = lang,
        dependency_parser = dependency_parser
    )

    assert [str(token) for token in tokens_long] == wl_test_lang_examples.TOKENS_LONG

    # Parsed
    heads_orig = ['test_head']
    tokens_parsed = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = wl_texts.to_tokens(['test'], lang = lang, heads = heads_orig),
        lang = lang,
        dependency_parser = dependency_parser
    )

    assert [str(token.head) for token in tokens_parsed] == heads_orig

def test__get_pipelines_disabled():
    wl_dependency_parsing._get_pipelines_disabled(show_pos_tags = True, show_lemmas = True)
    wl_dependency_parsing._get_pipelines_disabled(show_pos_tags = True, show_lemmas = False)
    wl_dependency_parsing._get_pipelines_disabled(show_pos_tags = False, show_lemmas = True)
    wl_dependency_parsing._get_pipelines_disabled(show_pos_tags = False, show_lemmas = False)

if __name__ == '__main__':
    for lang, dependency_parser in test_dependency_parsers:
        test_dependency_parse(lang, dependency_parser)

    test__get_pipelines_disabled()
