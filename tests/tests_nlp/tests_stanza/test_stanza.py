# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza
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
    wl_sentiment_analysis, wl_word_tokenization
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

    if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
        lang_stanza = wl_conversion.remove_lang_code_suffixes(main, lang)
    else:
        lang_stanza = lang

    if lang_stanza in wl_nlp_utils.get_langs_stanza(main, util_type = 'word_tokenizers'):
        wl_test_sentence_tokenize(lang, results_sentence_tokenize)
        wl_test_word_tokenize(lang, results_word_tokenize)

    if lang_stanza in wl_nlp_utils.get_langs_stanza(main, util_type = 'pos_taggers'):
        wl_test_pos_tag(lang, results_pos_tag, results_pos_tag_universal)

    if lang_stanza in wl_nlp_utils.get_langs_stanza(main, util_type = 'lemmatizers'):
        wl_test_lemmatize(lang, results_lemmatize)

    if lang_stanza in wl_nlp_utils.get_langs_stanza(main, util_type = 'dependency_parsers'):
        wl_test_dependency_parse(lang, results_dependency_parse)

    if lang_stanza in wl_nlp_utils.get_langs_stanza(main, util_type = 'sentiment_analyzers'):
        wl_test_sentiment_analyze(lang, results_sentiment_analayze)

def wl_test_get_lang_util(main, lang):
    if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
        lang_util = f'stanza_{wl_conversion.remove_lang_code_suffixes(main, lang)}'
    else:
        lang_util = f'stanza_{lang}'

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
    if lang in ['cop', 'fro', 'kaz', 'pcm', 'qpm', 'san', 'srp_latn']:
        assert len(sentences) == 1
    else:
        assert len(sentences) > 1

    assert sentences == results

def wl_test_word_tokenize(lang, results):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
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
    if lang in ['chu', 'cop', 'grc', 'pcm', 'orv', 'san', 'tel']:
        assert len(tokens) == len(test_sentence.split())
    elif lang == 'vie':
        assert len(tokens) < len(test_sentence.split())
    else:
        assert len(tokens) > len(test_sentence.split())

    assert tokens == results

def wl_test_pos_tag(lang, results, results_universal):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    pos_tagger = wl_test_get_lang_util(main, lang)

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
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    lemmatizer = wl_test_get_lang_util(main, lang)

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

    if lang in [
        'bul', 'cop', 'grc', 'ell', 'hin', 'isl', 'lit', 'glv', 'pcm', 'pol',
        'orv', 'sme', 'san', 'cym'
    ]:
        assert len(lemmas_tokenized_long) == 101 * 10
    else:
        assert lemmas_tokenized_long == [str(i) for i in range(101) for j in range(10)]

def wl_test_dependency_parse(lang, results):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    dependency_parser = wl_test_get_lang_util(main, lang)

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

def wl_test_sentiment_analyze(lang, results):
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')
    sentiment_analyzer = wl_test_get_lang_util(main, lang)

    # Untokenized
    sentiment_scores = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [test_sentence],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )
    sentiment_scores_tokenized = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [tokens],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer
    )

    print(f'{lang} / {sentiment_analyzer}:')
    print(f'{sentiment_scores}\n')

    # Check for empty results
    assert sentiment_scores == results
    assert sentiment_scores_tokenized == results

    for sentiment_score in sentiment_scores + sentiment_scores_tokenized:
        assert -1 <= sentiment_score <= 1

    # Tagged texts
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    sentiment_scores_tokenized_tagged = wl_sentiment_analysis.wl_sentiment_analyze(
        main,
        inputs = [[token + '_TEST' for token in tokens]],
        lang = lang,
        sentiment_analyzer = sentiment_analyzer,
        tagged = True
    )

    assert sentiment_scores_tokenized_tagged == sentiment_scores_tokenized
