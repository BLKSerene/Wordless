# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Dependency parsing
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
from wordless.wl_nlp import wl_dependency_parsing, wl_word_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

test_dependency_parsers = []

for lang, dependency_parsers in main.settings_global['dependency_parsers'].items():
    for dependency_parser in dependency_parsers:
        if not dependency_parser.startswith(('spacy_', 'stanza_')):
            test_dependency_parsers.append((lang, dependency_parser))

@pytest.mark.parametrize('lang, dependency_parser', test_dependency_parsers)
def test_dependency_parse(lang, dependency_parser):
    # Untokenized
    dependencies = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        dependency_parser = dependency_parser
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    dependencies_tokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = tokens,
        lang = lang,
        dependency_parser = dependency_parser
    )

    print(f'{lang} / {dependency_parser}:')
    print(f'{dependencies}\n')

    # Check for empty dependencies
    assert dependencies
    assert dependencies_tokenized
    assert all(dependencies)
    assert all(dependencies_tokenized)

    for dependency in dependencies + dependencies_tokenized:
        assert len(dependency) == 4

    # Tokenization should not be modified
    assert len(tokens) == len(dependencies_tokenized)

    # Tagged texts
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    dependencies_tokenized_tagged = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = [token + '_TEST' for token in tokens],
        lang = lang,
        dependency_parser = dependency_parser,
        tagged = True
    )

    dependencies_tokenized = [
        (child + '_TEST', head + '_TEST', dependency_relation, dependency_dist)
        for child, head, dependency_relation, dependency_dist in dependencies_tokenized
    ]

    assert dependencies_tokenized_tagged == dependencies_tokenized

    # Long texts
    dependencies_tokenized_long = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = [str(i) for i in range(101) for j in range(10)],
        lang = lang,
        dependency_parser = dependency_parser
    )

    assert [dependency[0] for dependency in dependencies_tokenized_long] == [str(i) for i in range(101) for j in range(10)]

if __name__ == '__main__':
    for lang, dependency_parser in test_dependency_parsers:
        test_dependency_parse(lang, dependency_parser)
