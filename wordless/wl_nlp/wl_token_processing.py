# ----------------------------------------------------------------------
# Wordless: NLP - Token processing
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

import copy

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import (
    wl_dependency_parsing, wl_lemmatization, wl_pos_tagging, wl_stop_word_lists, wl_syl_tokenization,
    wl_texts, wl_word_detokenization
)
from wordless.wl_utils import wl_misc

# Assign part-of-speech tags
def text_pos_tag(main, text, settings):
    if settings['assign_pos_tags'] and not text.tagged:
        tokens = wl_pos_tagging.wl_pos_tag(
            main,
            inputs = text.get_tokens_flat(),
            lang = text.lang
        )

        text.update_token_properties(tokens)

# Apply lemmatization / Match inflected forms
def text_lemmatize(main, text, token_settings, search_settings = None):
    search_settings = search_settings or {
        'match_inflected_forms': False,
        'context_settings': {'incl': {'incl': False}, 'excl': {'excl': False}}
    }

    if (
        token_settings.get('apply_lemmatization', False)
        or search_settings['match_inflected_forms']
        or (
            search_settings['context_settings']['incl']['incl']
            and search_settings['context_settings']['incl']['match_inflected_forms']
        )
        or (
            search_settings['context_settings']['excl']['excl']
            and search_settings['context_settings']['excl']['match_inflected_forms']
        )
    ):
        tokens = wl_lemmatization.wl_lemmatize(
            main,
            inputs = text.get_tokens_flat(),
            lang = text.lang
        )

        text.update_token_properties(tokens)

# Syllable tokenization
def text_syl_tokenize(main, text):
    tokens = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = text.get_tokens_flat(),
        lang = text.lang,
    )

    text.update_token_properties(tokens)

# Ignore tags
def text_ignore_tags(text, settings):
    if settings['ignore_tags']:
        text.set_token_properties('tag', None)

# Use tags only
def text_use_tags_only(text, settings):
    if settings['use_tags']:
        # Calculate head references
        if text.has_token_properties('head'):
            head_refs = []

            for i_para, para in enumerate(text.tokens_multilevel):
                for i_sentence, sentence in enumerate(para):
                    for sentence_seg in sentence:
                        for token in sentence_seg:
                            head = token.head

                            for i_sentence_seg, sentence_seg in enumerate(sentence):
                                for i_token, token in enumerate(sentence_seg):
                                    if head is token:
                                        head_refs.append((i_para, i_sentence, i_sentence_seg, i_token))

        text.set_token_texts(text.get_token_properties('tag', flat = True))
        text.set_token_properties('tag', None)

        # Update head references
        if text.has_token_properties('head'):
            i_token = 0

            for para in text.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for token in sentence_seg:
                            refs = head_refs[i_token]
                            token.head = text.tokens_multilevel[refs[0]][refs[1]][refs[2]][refs[3]]

                            i_token += 1

def wl_process_tokens(main, text, token_settings, search_settings = None):
    settings = copy.deepcopy(token_settings)

    if not settings['words']:
        settings['all_lowercase'] = False
        settings['all_uppercase'] = False
        settings['title_case'] = False

    if settings['use_tags']:
        settings['apply_lemmatization'] = False

    text_pos_tag(main, text, token_settings)
    text_lemmatize(main, text, token_settings, search_settings)

    text_modified = copy.deepcopy(text)

    # Remove empty paragraphs
    text_modified.tokens_multilevel = [para for para in text_modified.tokens_multilevel if para]

    # Remove tags temporarily if text is untagged and users do not choose to assign POS tags on the fly
    if not settings['assign_pos_tags'] and not text.tagged:
        text_modified.set_token_properties('tag', '')

    # Punctuation marks
    if not settings['punc_marks']:
        for para in text_modified.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [
                        token
                        for token in sentence_seg
                        if not wl_checks_tokens.is_punc(token)
                    ]

    # Treat as all lowercase
    if settings['treat_as_all_lowercase']:
        text_modified.set_token_texts([token.lower() for token in text_modified.get_tokens_flat()])

        for para in text_modified.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for token in sentence_seg:
                        token.tag = token.tag.lower()

    # Words
    if settings['words']:
        # Lowercase
        if not settings['all_lowercase']:
            for para in text_modified.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token.islower():
                                sentence_seg[i] = ''
        # Uppercase
        if not settings['all_uppercase']:
            for para in text_modified.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token.isupper():
                                sentence_seg[i] = ''
        # Title Case
        if not settings['title_case']:
            for para in text_modified.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token.istitle():
                                sentence_seg[i] = ''
    else:
        for para in text_modified.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checks_tokens.is_word_alphabetic(token):
                            sentence_seg[i] = ''

    # Numerals
    if not settings['nums']:
        for para in text_modified.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for i, token in enumerate(sentence_seg):
                        if wl_checks_tokens.is_num(token):
                            sentence_seg[i] = ''

    # Filter stop words
    if settings['filter_stop_words']:
        stop_words = wl_stop_word_lists.wl_get_stop_word_list(main, lang = text_modified.lang)

        if main.settings_custom['stop_word_lists']['stop_word_list_settings']['case_sensitive']:
            for para in text_modified.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token in stop_words:
                                sentence_seg[i] = ''
        else:
            stop_words = {token.lower() for token in stop_words}

            for para in text_modified.tokens_multilevel:
                for sentence in para:
                    for sentence_seg in sentence:
                        for i, token in enumerate(sentence_seg):
                            if token.lower() in stop_words:
                                sentence_seg[i] = ''

    # Replace tokens with their lemmas
    if settings['apply_lemmatization']:
        text_modified.set_token_texts(text_modified.get_token_properties('lemma', flat = True))

    text_modified.update_num_tokens()

    return text_modified

def wl_process_tokens_ngram_generator(main, text, token_settings, search_settings = None):
    text_modified = wl_process_tokens(main, text, token_settings, search_settings)

    text_ignore_tags(text_modified, token_settings)
    text_use_tags_only(text_modified, token_settings)

    text_modified.update_num_tokens()

    return text_modified

def remove_empty_tokens_multilevel(tokens_multilevel, empty_tokens = True):
    # Remove empty tokens
    if empty_tokens:
        tokens_multilevel = [
            [
                [
                    [token for token in sentence_seg if token]
                    for sentence_seg in sentence
                ]
                for sentence in para
            ]
            for para in tokens_multilevel
        ]

    # Remove empty sentence segments
    tokens_multilevel = [
        [
            [sentence_seg for sentence_seg in sentence if sentence_seg]
            for sentence in para
        ]
        for para in tokens_multilevel
    ]

    # Remove empty sentences
    tokens_multilevel = [
        [sentence for sentence in para if sentence]
        for para in tokens_multilevel
    ]

    # Remove paragraphs
    tokens_multilevel = [para for para in tokens_multilevel if para]

    return tokens_multilevel

def wl_process_tokens_profiler(main, text, token_settings):
    # Punctuation marks must be preserved for some readability measures (e.g. Wheeler & Smith's Readability Formula)
    text.tokens_multilevel_with_puncs = copy.deepcopy(text.tokens_multilevel)

    text_syl_tokenize(main, text)

    text_modified = wl_process_tokens_ngram_generator(main, text, token_settings)
    text_modified.tokens_multilevel = remove_empty_tokens_multilevel(text_modified.tokens_multilevel)
    text_modified.update_num_tokens()

    return text_modified

def wl_process_tokens_concordancer(main, text, token_settings, search_settings, preserve_blank_lines = False):
    settings = copy.deepcopy(token_settings)

    text_pos_tag(main, text, token_settings)
    text_lemmatize(main, text, token_settings, search_settings)

    text_modified = copy.deepcopy(text)

    # Remove tags temporarily if text is untagged and users do not choose to assign POS tags on the fly
    if not settings['assign_pos_tags'] and not text.tagged:
        text_modified.set_token_properties('tag', '')

    # Punctuation marks
    if not settings['punc_marks']:
        tokens_flat_punc_marks = []

        for i, token in enumerate(text_modified.get_tokens_flat()):
            if wl_checks_tokens.is_punc(token):
                # Check if the first token is a punctuation mark
                if i == 0:
                    tokens_flat_punc_marks.append(wl_texts.Wl_Token('', lang = token.lang, punc_mark = token))
                else:
                    token_text = wl_word_detokenization.wl_word_detokenize(
                        main,
                        tokens = [
                            str(tokens_flat_punc_marks[-1]) + (tokens_flat_punc_marks[-1].punc_mark or ''),
                            token
                        ],
                        lang = text_modified.lang
                    )

                    tokens_flat_punc_marks[-1].punc_mark = token_text.replace(str(tokens_flat_punc_marks[-1]), '')
            else:
                tokens_flat_punc_marks.append(token)

        # Remove punctuation marks to match length
        for para in text_modified.tokens_multilevel:
            for sentence in para:
                for i, sentence_seg in enumerate(sentence):
                    sentence[i] = [token for token in sentence_seg if not wl_checks_tokens.is_punc(token)]

        # Also remove punctuation marks in heads
        for para in text_modified.tokens_multilevel:
            for sentence in para:
                for sentence_seg in sentence:
                    for token in sentence_seg:
                        if wl_checks_tokens.is_punc(token.head):
                            token.head = None

        text_modified.set_tokens(tokens_flat_punc_marks)

    if not preserve_blank_lines:
        text_modified.tokens_multilevel = remove_empty_tokens_multilevel(text_modified.tokens_multilevel, empty_tokens = False)

    text_ignore_tags(text_modified, token_settings)
    text_use_tags_only(text_modified, token_settings)

    text_modified.update_num_tokens()

    return text_modified

def wl_process_tokens_dependency_parser(main, text, token_settings, search_settings):
    # Dependency parsing
    tokens_modified = []

    for para in text.tokens_multilevel:
        for sentence in para:
            tokens_modified.extend(wl_dependency_parsing.wl_dependency_parse(
                main,
                inputs = list(wl_misc.flatten_list(sentence)),
                lang = text.lang,
            ))

    text.update_token_properties(tokens_modified)

    return wl_process_tokens_concordancer(main, text, token_settings, search_settings)

def wl_process_tokens_wordlist_generator(main, text, token_settings, generation_settings):
    # Syllabification
    if generation_settings['syllabification']:
        text_syl_tokenize(main, text)

    text_modified = wl_process_tokens_ngram_generator(main, text, token_settings)
    text_modified.tokens_multilevel = remove_empty_tokens_multilevel(text_modified.tokens_multilevel)
    text_modified.update_num_tokens()

    return text_modified

def wl_process_tokens_colligation_extractor(main, text, token_settings, search_settings):
    # Do not modify custom settings, as adding new options would clear user's custom settings
    settings = copy.deepcopy(token_settings)
    # Always assign part-of-speech tags
    settings['assign_pos_tags'] = True

    text_modified = wl_process_tokens(main, text, settings, search_settings)

    text_modified.tags = wl_texts.to_tokens(
        text_modified.get_token_properties('tag', flat = True),
        lang = text.lang
    )

    text_ignore_tags(text_modified, token_settings)
    text_use_tags_only(text_modified, token_settings)

    text_modified.update_num_tokens()

    return text_modified
