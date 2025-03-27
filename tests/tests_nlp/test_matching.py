# ----------------------------------------------------------------------
# Tests: NLP - Matching
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

import re

from tests import wl_test_init
from wordless.wl_nlp import wl_matching, wl_texts

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

main.settings_custom['files']['tags']['header_tag_settings'] = [
    ['Nonembedded', 'Header', '<teiHeader>', '</teiHeader>'],
    ['Nonembedded', 'Header', '<[ tei <[Header ]>', '<[/ tei <[Header ]>'],

    ['Nonembedded', 'Header', '<>', '</>'],
    ['Nonembedded', 'Header', '< >', '</ >'],
    ['Nonembedded', 'Header', '<_?>', '</_?>']
]
main.settings_custom['files']['tags']['body_tag_settings'] = [
    ['Embedded', 'Part of Speech', '_*', 'N/A'],
    ['Embedded', 'Part of Speech', '_', 'N/A'],
    ['Embedded', 'Part of Speech', '/_,', 'N/A'],

    ['Nonembedded', 'Others', '<*>', '</*>'],
    ['Nonembedded', 'Others', '[( **T **AG** )]', '[(/ **T **AG** )]'],

    ['Nonembedded', 'Others', '[]', '[/]'],
    ['Nonembedded', 'Others', '[ ]', '[/ ]'],
    ['Nonembedded', 'Others', '<_?>', '</_?>']
]
main.settings_custom['files']['tags']['xml_tag_settings'] = [
    ['Nonembedded', 'Paragraph', '<p>', '</p>'],
    ['Nonembedded', 'Paragraph', '<_ p p _>', '<_/ p p _>'],

    ['Nonembedded', 'Paragraph', '<>', '</>'],
    ['Nonembedded', 'Paragraph', '< >', '</ >'],
    ['Nonembedded', 'Paragraph', '<_?>', '</_?>']
]

def test_split_tag_embedded():
    assert wl_matching.split_tag_embedded(r'_') == ('_', '')

    assert wl_matching.split_tag_embedded(r'_*') == ('_', '*')
    assert wl_matching.split_tag_embedded(r'_/*') == ('_/', '*')
    assert wl_matching.split_tag_embedded(r'_**') == ('_', '**')
    assert wl_matching.split_tag_embedded(r'_*T*AG*') == ('_', '*T*AG*')

    assert wl_matching.split_tag_embedded(r'_TAG') == ('_', 'TAG')
    assert wl_matching.split_tag_embedded(r'_/TAG') == ('_/', 'TAG')
    assert wl_matching.split_tag_embedded(r'_/T_AG') == ('_/', 'T_AG')

    assert wl_matching.split_tag_embedded(r'_') == ('_', '')
    assert wl_matching.split_tag_embedded(r'_/,') == ('_', '/,')

def test_split_tag_nonembedded():
    assert wl_matching.split_tag_nonembedded(r'<>', tag_type = 'body') == ('<', '', '>')

    assert wl_matching.split_tag_nonembedded(r'<*>', tag_type = 'body') == ('<', '*', '>')
    assert wl_matching.split_tag_nonembedded(r'< **T **AG** >', tag_type = 'body') == ('<', ' **T **AG** ', '>')
    assert wl_matching.split_tag_nonembedded(r'<*TAG*>', tag_type = 'body') == ('<', '*TAG*', '>')
    assert wl_matching.split_tag_nonembedded(r'<*TAG*>', tag_type = 'header') == ('<*', 'TAG', '*>')

    assert wl_matching.split_tag_nonembedded(r'<TAG>', tag_type = 'body') == ('<', 'TAG', '>')
    assert wl_matching.split_tag_nonembedded(r'<[ _T <[AG? ]>', tag_type = 'body') == ('<[', ' _T <[AG? ', ']>')

    assert wl_matching.split_tag_nonembedded(r'<>', tag_type = 'body') == ('<', '', '>')
    assert wl_matching.split_tag_nonembedded(r'< >', tag_type = 'body') == ('<', ' ', '>')
    assert wl_matching.split_tag_nonembedded(r'<_?>', tag_type = 'body') == ('<', '_?', '>')

def test_replace_wildcards_in_tag_name():
    assert wl_matching.replace_wildcards_in_tag_name('*', '.+?', 'body') == '.+?'
    assert wl_matching.replace_wildcards_in_tag_name('**T**AG**', '.+?', 'body') == '.+?T.+?AG.+?'
    assert wl_matching.replace_wildcards_in_tag_name('*', '.+?', 'header') == r'\*'

    assert wl_matching.replace_wildcards_in_tag_name(' *', '.+?', 'body', escape = True) == r'\ .+?'
    assert wl_matching.replace_wildcards_in_tag_name(' *', '.+?', 'body', escape = False) == r' .+?'

def test_get_re_tags():
    re_tags_header = wl_matching.get_re_tags(main, tag_type = 'header')
    re_tags_body = wl_matching.get_re_tags(main, tag_type = 'body')
    re_tags_xml = wl_matching.get_re_tags(main, tag_type = 'xml')

    assert re_tags_header == r'</?teiHeader>|<\[/?\ tei\ <\[Header\ \]>|</?>|</?\ >|</?_\?>'
    assert re_tags_body == r'_\S+(?=\s|$)|_(?=\s|$)|/_,(?=\s|$)|</?.+?>|\[\(/?\ .+?T\ .+?AG.+?\ \)\]|\[/?\]|\[/?\ \]|</?_\?>'
    assert re_tags_xml == r'</?p>|<_/?\ p\ p\ _>|</?>|</?\ >|</?_\?>'

    re_tags_header = re.compile(re_tags_header)
    re_tags_body = re.compile(re_tags_body)
    re_tags_xml = re.compile(re_tags_xml)

    assert re_tags_header.findall(r'<teiHeader>token</teiHeader>') == ['<teiHeader>', '</teiHeader>']
    assert re_tags_header.findall(r'<[ tei <[Header ]>token<[/ tei <[Header ]>') == ['<[ tei <[Header ]>', '<[/ tei <[Header ]>']

    assert re_tags_header.findall(r'<>token</>') == ['<>', '</>']
    assert re_tags_header.findall(r'< >token</ >') == ['< >', '</ >']
    assert re_tags_header.findall(r'<_?>token</_?>') == ['<_?>', '</_?>']

    assert re_tags_body.findall(r'token_TAG') == ['_TAG']
    assert re_tags_body.findall(r'token_/T_AG') == ['_/T_AG']
    assert re_tags_body.findall(r'token_') == ['_']
    assert re_tags_body.findall(r'token/_,') == ['/_,']

    assert re_tags_body.findall(r'<TAG>token</TAG>') == ['<TAG>', '</TAG>']
    assert re_tags_body.findall(r'[( *T [(AG? )]token[(/ *T [(AG? )]') == ['[( *T [(AG? )]', '[(/ *T [(AG? )]']

    assert re_tags_body.findall(r'[]token[/]') == ['[]', '[/]']
    assert re_tags_body.findall(r'[ ]token[/ ]') == ['[ ]', '[/ ]']
    assert re_tags_body.findall(r'<_?>token</_?>') == ['<_?>', '</_?>']

    assert re_tags_xml.findall(r'<p>token</p>') == ['<p>', '</p>']
    assert re_tags_xml.findall(r'<_ p p _>token<_/ p p _>') == ['<_ p p _>', '<_/ p p _>']

    assert re_tags_xml.findall(r'<>token</>') == ['<>', '</>']
    assert re_tags_xml.findall(r'< >token</ >') == ['< >', '</ >']
    assert re_tags_xml.findall(r'<_?>token</_?>') == ['<_?>', '</_?>']

def test_get_re_tags_with_tokens():
    re_tags_header = wl_matching.get_re_tags_with_tokens(main, tag_type = 'header')
    re_tags_body = wl_matching.get_re_tags_with_tokens(main, tag_type = 'body')
    re_tags_xml = wl_matching.get_re_tags_with_tokens(main, tag_type = 'xml')

    print(re_tags_header)
    print(re_tags_body)
    print(re_tags_xml)

    assert re_tags_header == r'<teiHeader>.*?</teiHeader>|<\[\ tei\ <\[Header\ \]>.*?<\[/\ tei\ <\[Header\ \]>|<>.*?</>|<\ >.*?</\ >|<_\?>.*?</_\?>'
    assert re_tags_body == r'\S*_\S+(?=\s|$)|\S*_(?=\s|$)|\S*/_,(?=\s|$)|<.+?>.*?</.+?>|\[\(\ .+?T\ .+?AG.+?\ \)\].*?\[\(/\ .+?T\ .+?AG.+?\ \)\]|\[\].*?\[/\]|\[\ \].*?\[/\ \]|<_\?>.*?</_\?>'
    assert re_tags_xml == r'<p>.*?</p>|<_\ p\ p\ _>.*?<_/\ p\ p\ _>|<>.*?</>|<\ >.*?</\ >|<_\?>.*?</_\?>'

    re_tags_header = re.compile(re_tags_header)
    re_tags_body = re.compile(re_tags_body)
    re_tags_xml = re.compile(re_tags_xml)

    assert re_tags_header.findall(r'token <teiHeader>token</teiHeader> token') == ['<teiHeader>token</teiHeader>']
    assert re_tags_header.findall(r'token <[ tei <[Header ]>token<[/ tei <[Header ]> token') == ['<[ tei <[Header ]>token<[/ tei <[Header ]>']

    assert re_tags_header.findall(r'token <>token</> token') == ['<>token</>']
    assert re_tags_header.findall(r'token < >token</ > token') == ['< >token</ >']
    assert re_tags_header.findall(r'token <_?>token</_?> token') == ['<_?>token</_?>']

    assert re_tags_body.findall(r'token token_TAG token') == ['token_TAG']
    assert re_tags_body.findall(r'token token/T_AG token') == ['token/T_AG']
    assert re_tags_body.findall(r'token token_ token') == ['token_']
    assert re_tags_body.findall(r'token token/_, token') == ['token/_,']

    assert re_tags_body.findall(r'token <TAG>token</TAG> token') == ['<TAG>token</TAG>']
    assert re_tags_body.findall(r'token [( *T [(AG? )]token[(/ *T [(AG? )] token') == ['[( *T [(AG? )]token[(/ *T [(AG? )]']

    assert re_tags_body.findall(r'token []token[/] token') == ['[]token[/]']
    assert re_tags_body.findall(r'token [ ]token[/ ] token') == ['[ ]token[/ ]']
    assert re_tags_body.findall(r'token <_?>token</_?> token') == ['<_?>token</_?>']

    assert re_tags_xml.findall(r'token <p>token</p> token') == ['<p>token</p>']
    assert re_tags_xml.findall(r'token <_ p p _>token<_/ p p _> token') == ['<_ p p _>token<_/ p p _>']

    assert re_tags_xml.findall(r'token <>token</> token') == ['<>token</>']
    assert re_tags_xml.findall(r'token < >token</ > token') == ['< >token</ >']
    assert re_tags_xml.findall(r'token <_?>token</_?> token') == ['<_?>token</_?>']

def init_token_settings(assign_pos_tags = False, ignore_tags = False, use_tags = False):
    return {
        'assign_pos_tags': assign_pos_tags,
        'ignore_tags': ignore_tags,
        'use_tags': use_tags
    }

def init_search_settings(
    multi_search_mode = False, search_term = '', search_terms = None,
    match_case = False, match_whole_words = False, match_inflected_forms = False,
    use_regex = False,
    match_without_tags = False, match_tags = False,
    match_dependency_relations = False
):
    search_terms = search_terms or []

    return {
        'multi_search_mode': multi_search_mode,
        'search_term': search_term,
        'search_terms': search_terms,

        'match_case': match_case,
        'match_whole_words': match_whole_words,
        'match_inflected_forms': match_inflected_forms,
        'use_regex': use_regex,
        'match_without_tags': match_without_tags,
        'match_tags': match_tags,

        'match_dependency_relations': match_dependency_relations
    }

def test_check_search_terms():
    SEARCH_SETTINGS_1 = init_search_settings(multi_search_mode = True, search_terms = ['test'])
    SEARCH_SETTINGS_2 = init_search_settings(multi_search_mode = False, search_term = 'test')
    SEARCH_SETTINGS_3 = init_search_settings(multi_search_mode = False, search_term = '')

    assert wl_matching.check_search_terms(SEARCH_SETTINGS_1, True) == set(['test'])
    assert wl_matching.check_search_terms(SEARCH_SETTINGS_2, True) == set(['test'])
    assert not wl_matching.check_search_terms(SEARCH_SETTINGS_3, True)
    assert not wl_matching.check_search_terms(SEARCH_SETTINGS_1, False)

def test_check_search_settings():
    TOKEN_SETTINGS_1 = init_token_settings(ignore_tags = True)
    TOKEN_SETTINGS_2 = init_token_settings(use_tags = True)
    TOKEN_SETTINGS_3 = init_token_settings()

    SEARCH_SETTINGS_1 = init_search_settings(match_inflected_forms = True, match_without_tags = True)
    SEARCH_SETTINGS_2 = init_search_settings(match_inflected_forms = True, match_tags = True)
    SEARCH_SETTINGS_3 = init_search_settings(match_inflected_forms = True)
    SEARCH_SETTINGS_4 = init_search_settings(match_without_tags = True)
    SEARCH_SETTINGS_5 = init_search_settings(match_tags = True)
    SEARCH_SETTINGS_6 = init_search_settings(match_dependency_relations = True)
    SEARCH_SETTINGS_7 = init_search_settings()

    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_1) == SEARCH_SETTINGS_3
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_2) == SEARCH_SETTINGS_3
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_3) == SEARCH_SETTINGS_3
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_4) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_5) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_6) == SEARCH_SETTINGS_6
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_1, SEARCH_SETTINGS_7) == SEARCH_SETTINGS_7

    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_1) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_2) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_3) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_4) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_5) == SEARCH_SETTINGS_7
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_6) == SEARCH_SETTINGS_6
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_2, SEARCH_SETTINGS_7) == SEARCH_SETTINGS_7

    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_1) == SEARCH_SETTINGS_1
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_2) == SEARCH_SETTINGS_5
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_3) == SEARCH_SETTINGS_3
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_4) == SEARCH_SETTINGS_4
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_5) == SEARCH_SETTINGS_5
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_6) == SEARCH_SETTINGS_6
    assert wl_matching.check_search_settings(TOKEN_SETTINGS_3, SEARCH_SETTINGS_7) == SEARCH_SETTINGS_7

def compare_tokens_matched(tokens_matched, tokens_expected):
    tokens_matched = [token.display_text() for token in tokens_matched]

    print(f'Tokens matched: {sorted(tokens_matched)}')
    print(f'Tokens expected: {sorted(tokens_expected)}\n')

    assert set(tokens_matched) == set(tokens_expected)

def compare_ngrams_matched(ngrams_matched, ngrams_expected):
    ngrams_matched = [tuple(token.display_text() for token in ngram) for ngram in ngrams_matched]

    print(f'Tokens matched: {sorted(ngrams_matched)}')
    print(f'Tokens expected: {sorted(ngrams_expected)}\n')

    assert set(ngrams_matched) == set(ngrams_expected)

def compare_context_matched(context_matched, context_expected):
    context_matched = (
        {tuple(token.display_text() for token in ngram) for ngram in context_matched[0]},
        {tuple(token.display_text() for token in ngram) for ngram in context_matched[1]}
    )

    print(f'Tokens matched: {sorted(context_matched)}')
    print(f'Tokens expected: {sorted(context_expected)}\n')

    assert context_matched == context_expected

def test_match_tokens():
    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['tAke'],
        tokens = wl_texts.to_tokens(
            ['take', 'TAKE', 'Take', 'tAke', 'TaKE', 'TaKEs', 'test'],
            lang = 'eng_us',
            tags = ['', '', '', '', '', '', '_TAKE']
        ),
        lang = 'eng_us',
        settings = init_search_settings()
    ), ['take', 'TAKE', 'Take', 'tAke', 'TaKE', 'TaKEs', 'test_TAKE'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['tAke'],
        tokens = wl_texts.to_tokens(
            ['take', 'TAKE', 'Take', 'tAke', 'TaKE', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_case = True)
    ), ['tAke'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['take'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'taking', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True)
    ), ['take'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['took'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'taking', 'test'],
            lemmas = ['take', 'take', 'take', 'take', 'take', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_inflected_forms = True)
    ), ['take', 'takes', 'took', 'taken', 'taking'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['took_NN'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'test_NN'],
            lang = 'eng_us',
            tags = ['', '_NN', '_NN', '_NNP', ''],
            lemmas = ['take', 'take', 'take', 'take', 'test']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_inflected_forms = True)
    ), ['takes_NN', 'took_NN', 'taken_NNP'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['took_NN'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'test_NN'],
            lang = 'eng_us',
            tags = ['', '_NN', '_NN', '_NNP', ''],
            lemmas = ['take', 'take', 'take', 'take', 'test']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True, match_inflected_forms = True)
    ), ['takes_NN', 'took_NN'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['take[sn]'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'taking', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(use_regex = True)
    ), ['takes', 'taken'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['takes'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'test'],
            lang = 'eng_us',
            tags = ['', '_NN', '_NN', '_JJ']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_without_tags = True)
    ), ['takes_NN'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['_NN'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'test_NN'],
            lang = 'eng_us',
            tags = ['', '_NN', '_NN', '_NNP', '']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True, match_tags = True)
    ), ['takes_NN', 'took_NN'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['aux'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'test_NN'],
            lang = 'eng_us',
            dependency_relations = ['ROOT', 'nsubj', 'advmod', 'aux', 'auxpass']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_dependency_relations = True)
    ), ['aux', 'auxpass'])

    compare_tokens_matched(wl_matching.match_tokens(
        main,
        search_terms = ['aux'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'taken', 'test_NN'],
            lang = 'eng_us',
            dependency_relations = ['ROOT', 'nsubj', 'advmod', 'aux', 'auxpass']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True, match_dependency_relations = True)
    ), ['aux'])

def test_match_ngrams():
    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['tAke WaLK'],
        tokens = wl_texts.to_tokens(
            ['take', 'TAKE', 'WaLK', 'test'],
            lang = 'eng_us',
            tags = ['', '', '', '_wAlk']
        ),
        lang = 'eng_us',
        settings = init_search_settings()
    ), [('take', 'WaLK'), ('take', 'test_wAlk'), ('TAKE', 'WaLK'), ('TAKE', 'test_wAlk')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['tAke WaLK'],
        tokens = wl_texts.to_tokens(
            ['take', 'tAke', 'WALK', 'WaLK', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_case = True)
    ), [('tAke', 'WaLK')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['take walk'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'walk', 'walked', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True)
    ), [('take', 'walk')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['take walk'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'walk', 'walked', 'test'],
            lang = 'eng_us',
            lemmas = ['take', 'take', 'walk', 'walk', 'test'],
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_inflected_forms = True)
    ), [('take', 'walk'), ('take', 'walked'), ('takes', 'walk'), ('takes', 'walked')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['took_NN walked_NN'],
        tokens = wl_texts.to_tokens(
            ['take', 'took', 'walk', 'walked', 'test'],
            lang = 'eng_us',
            tags = ['', '_NNP', '_NN', '_NNP', '_JJ'],
            lemmas = ['take', 'take', 'walk', 'walk', 'test'],
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_inflected_forms = True)
    ), [('took_NNP', 'walk_NN'), ('took_NNP', 'walked_NNP')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['took_NN walked_NN'],
        tokens = wl_texts.to_tokens(
            ['take', 'took', 'walk', 'walked', 'test'],
            lang = 'eng_us',
            tags = ['_NN', '_NNP', '_NN', '_NNP', '_JJ'],
            lemmas = ['take', 'take', 'walk', 'walk', 'test'],
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True, match_inflected_forms = True)
    ), [('take_NN', 'walk_NN')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['took|taken walk(s|ing)'],
        tokens = wl_texts.to_tokens(
            ['took', 'taken', 'takes', 'walks', 'walking', 'walked', 'test'],
            lang = 'eng_us'
        ),
        lang = 'eng_us',
        settings = init_search_settings(use_regex = True)
    ), [('took', 'walks'), ('took', 'walking'), ('taken', 'walks'), ('taken', 'walking')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['takes walks', 'took walked'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'walk', 'walks', 'walked', 'test'],
            lang = 'eng_us',
            tags = ['', '_NN', '_NN', '', '_NN', '_NN', '_TAKES']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_without_tags = True)
    ), [('takes_NN', 'walks_NN'), ('took_NN', 'walked_NN')])

    compare_ngrams_matched(wl_matching.match_ngrams(
        main,
        search_terms = ['_NN _JJ'],
        tokens = wl_texts.to_tokens(
            ['take', 'takes', 'took', 'walk', 'walks', 'walked', 'test_JJ'],
            lang = 'eng_us',
            tags = ['', '_NN', '_NNP', '', '_JJ', '_JJS', '']
        ),
        lang = 'eng_us',
        settings = init_search_settings(match_whole_words = True, match_tags = True)
    ), [('takes_NN', 'walks_JJ')])

def test_match_search_terms_tokens():
    compare_tokens_matched(wl_matching.match_search_terms_tokens(
        main,
        tokens = wl_texts.to_tokens(['take'], lang = 'eng_us'),
        lang = 'eng_us',
        token_settings = init_token_settings(),
        search_settings = init_search_settings(search_term = 'take')
    ), ['take'])

def test_match_search_terms_ngrams():
    compare_ngrams_matched(wl_matching.match_search_terms_ngrams(
        main,
        tokens = wl_texts.to_tokens(['take', 'walk'], lang = 'eng_us'),
        lang = 'eng_us',
        token_settings = init_token_settings(),
        search_settings = init_search_settings(search_term = 'take walk')
    ), [('take', 'walk')])

def init_context_settings(
    incl = False,
    incl_multi_search_mode = False, incl_search_term = '', incl_search_terms = None,
    incl_context_window_left = -5, incl_context_window_right = 5,
    excl = False,
    excl_multi_search_mode = False, excl_search_term = '', excl_search_terms = None,
    excl_context_window_left = -5, excl_context_window_right = 5,
):
    incl_search_terms = incl_search_terms or []
    excl_search_terms = excl_search_terms or []

    context_settings = {
        'incl': init_search_settings(),
        'excl': init_search_settings()
    }

    context_settings['incl']['incl'] = incl
    context_settings['incl']['multi_search_mode'] = incl_multi_search_mode
    context_settings['incl']['search_term'] = incl_search_term
    context_settings['incl']['search_terms'] = incl_search_terms

    context_settings['incl']['context_window_left'] = incl_context_window_left
    context_settings['incl']['context_window_right'] = incl_context_window_right

    context_settings['excl']['excl'] = excl
    context_settings['excl']['multi_search_mode'] = excl_multi_search_mode
    context_settings['excl']['search_term'] = excl_search_term
    context_settings['excl']['search_terms'] = excl_search_terms

    context_settings['excl']['context_window_left'] = excl_context_window_left
    context_settings['excl']['context_window_right'] = excl_context_window_right

    return context_settings

def test_match_search_terms_context():
    compare_context_matched(wl_matching.match_search_terms_context(
        main,
        tokens = wl_texts.to_tokens(['take'], lang = 'eng_us'),
        lang = 'eng_us',
        token_settings = init_token_settings(),
        context_settings = init_context_settings()
    ), (set(), set()))

    compare_context_matched(wl_matching.match_search_terms_context(
        main,
        tokens = wl_texts.to_tokens(['take', 'walk'], lang = 'eng_us'),
        lang = 'eng_us',
        token_settings = init_token_settings(),
        context_settings = init_context_settings(incl = True, incl_search_term = 'take walk')
    ), ({('take', 'walk')}, set()))

    compare_context_matched(wl_matching.match_search_terms_context(
        main,
        tokens = wl_texts.to_tokens(['take', 'walk'], lang = 'eng_us'),
        lang = 'eng_us',
        token_settings = init_token_settings(),
        context_settings = init_context_settings(excl = True, excl_search_term = 'take walk')
    ), (set(), {('take', 'walk')}))

    compare_context_matched(wl_matching.match_search_terms_context(
        main,
        tokens = wl_texts.to_tokens(['take', 'walk'], lang = 'eng_us'),
        lang = 'eng_us',
        token_settings = init_token_settings(),
        context_settings = init_context_settings(
            incl = True, incl_search_term = 'take walk',
            excl = True, excl_search_term = 'take walk'
        )
    ), ({('take', 'walk')}, {('take', 'walk')}))

def test_check_context():
    assert wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(incl = False, excl = False),
        search_terms_incl = {},
        search_terms_excl = {}
    )
    assert wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(incl = False, excl = False),
        search_terms_incl = {('take', 'walk')},
        search_terms_excl = {('take', 'walk')}
    )

    assert wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(incl = True, incl_search_term = 'test'),
        search_terms_incl = {('take', 'walk'), ('test', 'test')},
        search_terms_excl = {}
    )
    assert not wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(incl = True, incl_search_term = 'test'),
        search_terms_incl = {('take', 'test')},
        search_terms_excl = {}
    )
    assert not wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(incl = True, incl_search_term = 'test'),
        search_terms_incl = {},
        search_terms_excl = {}
    )

    assert wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(excl = True, excl_search_term = 'test'),
        search_terms_incl = {},
        search_terms_excl = {('take', 'test')}
    )
    assert not wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(excl = True, excl_search_term = 'test'),
        search_terms_incl = {},
        search_terms_excl = {('take', 'walk'), ('test', 'test')}
    )
    assert wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(excl = True, excl_search_term = 'test'),
        search_terms_incl = {},
        search_terms_excl = {}
    )

    assert wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(
            incl = True, incl_search_term = 'test',
            excl = True, excl_search_term = 'test'
        ),
        search_terms_incl = {('take', 'walk')},
        search_terms_excl = {('take', 'test')}
    )
    assert not wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(
            incl = True, incl_search_term = 'test',
            excl = True, excl_search_term = 'test'
        ),
        search_terms_incl = {('take', 'walk')},
        search_terms_excl = {('take', 'walk')}
    )
    assert not wl_matching.check_context(
        i = 0,
        tokens = ['test'] * 5 + ['take', 'walk'],
        context_settings = init_context_settings(
            incl = True, incl_search_term = 'test',
            excl = True, excl_search_term = 'test'
        ),
        search_terms_incl = {},
        search_terms_excl = {}
    )

if __name__ == '__main__':
    test_split_tag_embedded()
    test_split_tag_nonembedded()
    test_replace_wildcards_in_tag_name()
    test_get_re_tags()
    test_get_re_tags_with_tokens()

    test_check_search_terms()
    test_check_search_settings()

    test_match_tokens()
    test_match_ngrams()
    test_match_search_terms_tokens()
    test_match_search_terms_ngrams()

    test_match_search_terms_context()
    test_check_context()
