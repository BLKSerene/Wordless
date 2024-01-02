# ----------------------------------------------------------------------
# Wordless: Tests - NLP - spaCy
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

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import (
    wl_dependency_parsing, wl_lemmatization, wl_nlp_utils, wl_pos_tagging, wl_sentence_tokenization,
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

    wl_test_sentence_tokenize(lang, results_sentence_tokenize_trf, results_sentence_tokenize_lg)
    wl_test_word_tokenize(lang, results_word_tokenize)

    if lang != 'other':
        wl_test_pos_tag(lang, results_pos_tag, results_pos_tag_universal)
        wl_test_lemmatize(lang, results_lemmatize)
        wl_test_dependency_parse(lang, results_dependency_parse)

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

def wl_test_word_tokenize(lang, results):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
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

    assert tokens == results

def wl_test_pos_tag(lang, results, results_universal):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    pos_tagger = f'spacy_{lang_no_suffix}'

    # Untokenized
    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = test_sentence,
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = test_sentence,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )
    tokens_tagged_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    print(f'{lang} / {pos_tagger}:')
    print(tokens_tagged)
    print(f'{tokens_tagged_universal}\n')

    # Check for empty tags
    assert tokens_tagged == results
    assert tokens_tagged_universal == results_universal
    assert tokens_tagged_tokenized
    assert tokens_tagged_universal_tokenized
    assert all((tag for token, tag in tokens_tagged))
    assert all((tag for token, tag in tokens_tagged_universal))
    assert all((tag for token, tag in tokens_tagged_tokenized))
    assert all((tag for token, tag in tokens_tagged_universal_tokenized))
    # Universal tags should not all be "X"
    assert any((tag for token, tag in tokens_tagged_universal if tag != 'X'))
    assert any((tag for token, tag in tokens_tagged_universal_tokenized if tag != 'X'))

    # Tokenization should not be modified
    assert len(tokens) == len(tokens_tagged_tokenized) == len(tokens_tagged_universal_tokenized)

    # Long texts
    tokens_tagged_tokenized_long = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = [str(i) for i in range(101) for j in range(10)],
        lang = lang,
        pos_tagger = pos_tagger
    )

    assert [token[0] for token in tokens_tagged_tokenized_long] == [str(i) for i in range(101) for j in range(10)]

def wl_test_lemmatize(lang, results):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    lemmatizer = f'spacy_{lang_no_suffix}'

    # Untokenized
    lemmas = wl_lemmatization.wl_lemmatize(
        main,
        inputs = test_sentence,
        lang = lang,
        lemmatizer = lemmatizer
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )
    lemmas_tokenized = wl_lemmatization.wl_lemmatize(
        main,
        inputs = tokens,
        lang = lang,
        lemmatizer = lemmatizer
    )

    print(f'{lang} / {lemmatizer}:')
    print(f'{lemmas}\n')

    # Check for empty lemmas
    assert lemmas == results
    assert lemmas_tokenized
    assert all(lemmas)
    assert all(lemmas_tokenized)

    # Tokenization should not be modified
    assert len(tokens) == len(lemmas_tokenized)

    # Tagged texts
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    lemmas_tokenized_tagged = wl_lemmatization.wl_lemmatize(
        main,
        inputs = [token + '_TEST' for token in tokens],
        lang = lang,
        lemmatizer = lemmatizer,
        tagged = True
    )

    assert lemmas_tokenized_tagged == [lemma + '_TEST' for lemma in lemmas_tokenized]

    # Long texts
    lemmas_tokenized_long = wl_lemmatization.wl_lemmatize(
        main,
        inputs = [str(i) for i in range(101) for j in range(10)],
        lang = lang,
        lemmatizer = lemmatizer
    )

    assert lemmas_tokenized_long == [str(i) for i in range(101) for j in range(10)]

def wl_test_dependency_parse(lang, results):
    lang_no_suffix = wl_conversion.remove_lang_code_suffixes(main, lang)
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    dependency_parser = f'spacy_{lang_no_suffix}'

    # Untokenized
    dependencies = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = test_sentence,
        lang = lang,
        dependency_parser = dependency_parser
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
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
    assert dependencies == results
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
