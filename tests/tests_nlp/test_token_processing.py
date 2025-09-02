# ----------------------------------------------------------------------
# Tests: NLP - Token processing
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

from tests import wl_test_init
from wordless.wl_nlp import wl_token_processing

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

def text_test(tokens = None, lang = 'eng_us'):
    tokens = tokens or [[[['test']]]]

    return wl_test_init.Wl_Test_Text(main, tokens_multilevel = tokens, lang = lang)

def test_text_pos_tag():
    wl_token_processing.text_pos_tag(
        main,
        text_test(),
        settings = {'assign_pos_tags': True}
    )

def test_text_lemmatize():
    wl_token_processing.text_lemmatize(
        main,
        text_test(),
        token_settings = {'apply_lemmatization': True}
    )

def test_text_syl_tokenize():
    wl_token_processing.text_syl_tokenize(
        main,
        text_test()
    )

def test_text_ignore_tags():
    wl_token_processing.text_ignore_tags(
        text_test(),
        settings = {'ignore_tags': True}
    )

def test_text_use_tags_only():
    wl_token_processing.text_use_tags_only(
        text_test(),
        settings = {'use_tags': True}
    )

def test_text_filter_stop_words():
    main.settings_custom['stop_word_lists']['stop_word_list_settings']['case_sensitive'] = True
    wl_token_processing.text_filter_stop_words(
        main,
        text_test(tokens = [[[['is']]]]),
        settings = {'filter_stop_words': True}
    )

    main.settings_custom['stop_word_lists']['stop_word_list_settings']['case_sensitive'] = False
    wl_token_processing.text_filter_stop_words(
        main,
        text_test(tokens = [[[['is']]]]),
        settings = {'filter_stop_words': True}
    )

def test_remove_empty_tokens():
    wl_token_processing.remove_empty_tokens([[['test']]])

def test_remove_empty_paras():
    wl_token_processing.remove_empty_paras([[['test']]])

def test_wl_process_tokens():
    text = text_test(tokens = [[[['test', '0']]]])
    text.tokens_multilevel[0][0][0][0].syls = ['test']
    text.tokens_multilevel[0][0][0][0].lemma = 'test'

    wl_token_processing.wl_process_tokens(
        main,
        text,
        token_settings = {
            'words': False,
            'nums': False,
            'punc_marks': False,
            'treat_as_all_lowercase': True,
            'assign_pos_tags': False,
            'use_tags': True
        }
    )

    text = text_test()
    text.tokens_multilevel[0][0][0][0].tag = 'test'

    wl_token_processing.wl_process_tokens(
        main,
        text,
        token_settings = {
            'words': True,
            'all_lowercase': False,
            'all_uppercase': False,
            'title_case': False,
            'nums': False,
            'punc_marks': True,
            'treat_as_all_lowercase': True,
            'apply_lemmatization': False,
            'assign_pos_tags': True,
            'use_tags': False
        }
    )

    text = text_test(tokens = [[[['test', 'TEST', 'Test']]]])
    text.tokens_multilevel[0][0][0][0].syls = ['test']

    wl_token_processing.wl_process_tokens(
        main,
        text,
        token_settings = {
            'words': True,
            'all_lowercase': True,
            'all_uppercase': False,
            'title_case': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': True,
            'assign_pos_tags': False,
            'use_tags': False
        }
    )

def test_wl_process_tokens_ngram_generator():
    wl_token_processing.wl_process_tokens_ngram_generator(
        main,
        text_test(),
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        }
    )

def test_wl_process_tokens_profiler():
    wl_token_processing.wl_process_tokens_profiler(
        main,
        text_test(),
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        },
        tab = 'all'
    )

    text = text_test(lang = 'pol')
    # Skip POS tagging and dependency parsing
    text.tokens_multilevel[0][0][0][0].tag_universal = 'test'

    wl_token_processing.wl_process_tokens_profiler(
        main,
        text,
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        },
        tab = 'readability'
    )

def test_wl_process_tokens_wordlist_generator():
    wl_token_processing.wl_process_tokens_wordlist_generator(
        main,
        text_test(),
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        },
        generation_settings = {
            'show_syllabified_forms': True
        }
    )

def test_wl_process_tokens_colligation_extractor():
    wl_token_processing.wl_process_tokens_colligation_extractor(
        main,
        text_test(),
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        },
        search_settings = {}
    )

def test_wl_process_tokens_concordancer():
    text = text_test(tokens = [[[[',', ',', 'test'], ['test']]]])
    text.tokens_multilevel[0][0][0][0].head = text.tokens_multilevel[0][0][0][0]

    wl_token_processing.wl_process_tokens_concordancer(
        main,
        text,
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': False,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        },
        search_settings = {}
    )

def test_wl_process_tokens_dependency_parser():
    wl_token_processing.wl_process_tokens_dependency_parser(
        main,
        text_test(),
        token_settings = {
            'words': False,
            'nums': True,
            'punc_marks': True,
            'treat_as_all_lowercase': False,
            'apply_lemmatization': False,
            'filter_stop_words': False,
            'assign_pos_tags': False,
            'ignore_tags': False,
            'use_tags': False
        },
        search_settings = {}
    )

if __name__ == '__main__':
    test_text_pos_tag()
    test_text_lemmatize()
    test_text_syl_tokenize()
    test_text_ignore_tags()
    test_text_use_tags_only()
    test_text_filter_stop_words()

    test_remove_empty_tokens()
    test_remove_empty_paras()

    test_wl_process_tokens()
    test_wl_process_tokens_ngram_generator()
    test_wl_process_tokens_profiler()
    test_wl_process_tokens_wordlist_generator()
    test_wl_process_tokens_colligation_extractor()
    test_wl_process_tokens_concordancer()
    test_wl_process_tokens_dependency_parser()
