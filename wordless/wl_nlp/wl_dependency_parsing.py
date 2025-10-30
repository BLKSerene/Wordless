# ----------------------------------------------------------------------
# Wordless: NLP - Dependency parsing
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

import bisect
import os
import shutil
import subprocess
import webbrowser

from PyQt5 import QtCore
import spacy

from wordless.wl_checks import (
    wl_checks_tokens,
    wl_checks_misc
)
from wordless.wl_dialogs import wl_dialogs
from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_texts
)
from wordless.wl_settings import wl_settings_default
from wordless.wl_utils import (
    wl_conversion,
    wl_misc,
    wl_paths
)

_tr = QtCore.QCoreApplication.translate

is_windows, is_macos, is_linux = wl_misc.check_os()

def wl_dependency_parse(main, inputs, lang, dependency_parser = 'default', force = False):
    if (
        not isinstance(inputs, str)
        and inputs
        and list(inputs)[0].head is not None
        and not force
    ):
        return inputs
    else:
        if dependency_parser == 'default':
            dependency_parser = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]

        wl_nlp_utils.init_dependency_parsers(
            main,
            lang = lang,
            dependency_parser = dependency_parser,
            tokenized = not isinstance(inputs, str)
        )

        # Currently not used
        if isinstance(inputs, str):
            if lang == 'srp_cyrl' and dependency_parser == 'stanza_srp_latn':
                inputs = wl_nlp_utils.to_srp_latn((inputs,))[0]

            texts, dependencies = wl_dependency_parse_text(main, inputs, lang, dependency_parser)

            if lang == 'srp_cyrl' and dependency_parser == 'stanza_srp_latn':
                texts = wl_nlp_utils.to_srp_cyrl(texts)

            tokens = wl_texts.to_tokens(texts, lang = lang)

            for token, (_, head_i, dependency_relation, dd, dd_no_punc) in zip(tokens, dependencies):
                token.head = tokens[head_i]
                token.dependency_relation = dependency_relation
                token.dd = dd
                token.dd_no_punc = dd_no_punc

            return tokens
        # For Profiler - Syntactic Complexity and Dependency Parser
        else:
            texts, token_properties = wl_texts.split_texts_properties(inputs)

            if lang == 'srp_cyrl' and dependency_parser == 'stanza_srp_latn':
                texts = wl_nlp_utils.to_srp_latn(texts)

            dependencies = wl_dependency_parse_tokens(main, texts, lang, dependency_parser)

            tokens = wl_texts.combine_texts_properties(texts, token_properties)

            for token, (_, head_i, dependency_relation, dd, dd_no_punc) in zip(tokens, dependencies):
                token.head = inputs[head_i]
                token.dependency_relation = dependency_relation
                token.dd = dd
                token.dd_no_punc = dd_no_punc

            wl_texts.update_token_properties(inputs, tokens)

            return inputs

# No need to preserve newlines
def wl_dependency_parse_text(main, text, lang, dependency_parser):
    tokens = []
    dependencies = []

    lines = wl_nlp_utils.clean_texts(text.splitlines())

    # spaCy
    if dependency_parser.startswith('spacy_'):
        nlp = main.__dict__[f'spacy_nlp_{wl_conversion.remove_lang_code_suffixes(lang)}']
        batch_size = main.settings_custom['files']['misc_settings']['read_files_in_chunks_lines']

        with nlp.select_pipes(disable = (
            pipeline
            for pipeline in ('senter', 'sentencizer', 'tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler')
            if nlp.has_pipe(pipeline)
        )):
            i_head_start = 0

            for doc in nlp.pipe(lines, batch_size = batch_size):
                for sentence in doc.sents:
                    i_punc_marks = [
                        i
                        for i, token in enumerate(sentence)
                        if wl_checks_tokens.is_punc(token.text)
                    ]

                    for i, token in enumerate(sentence):
                        dd = token.head.i - token.i

                        tokens.append(token.text)

                        # Calculate dependency distances with and without punctuation marks
                        if i_punc_marks and (dd < -1 or dd > 1):
                            dependencies.append((
                                token.head.text,
                                i_head_start + token.head.i,
                                token.dep_,
                                dd,
                                dd - (
                                    bisect.bisect(i_punc_marks, token.head.i)
                                    - bisect.bisect(i_punc_marks, token.i)
                                )
                            ))
                        else:
                            dependencies.append((
                                token.head.text,
                                i_head_start + token.head.i,
                                token.dep_,
                                dd,
                                dd
                            ))

                i_head_start += len(doc)
    # Stanza
    elif dependency_parser.startswith('stanza_'):
        if lang not in {'zho_cn', 'zho_tw'}:
            lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
        else:
            lang_stanza = lang

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']
        i_head_start = 0

        for doc in nlp.bulk_process(lines):
            for sentence in doc.sentences:
                i_punc_marks = [
                    i
                    for i, token in enumerate(sentence.words)
                    if wl_checks_tokens.is_punc(token.text)
                ]

                for i, token in enumerate(sentence.words):
                    dd = token.head - token.id if token.head > 0 else 0

                    tokens.append(token.text)

                    # Calculate dependency distances with and without punctuation marks
                    if i_punc_marks and (dd < -1 or dd > 1):
                        dependencies.append((
                            sentence.words[token.head - 1].text if token.head > 0 else token.text,
                            i_head_start + token.head - 1 if token.head > 0 else i_head_start + i,
                            token.deprel,
                            dd,
                            dd - (
                                bisect.bisect(i_punc_marks, token.head - 1)
                                - bisect.bisect(i_punc_marks, token.id - 1)
                            )
                        ))
                    else:
                        dependencies.append((
                            sentence.words[token.head - 1].text if token.head > 0 else token.text,
                            i_head_start + token.head - 1 if token.head > 0 else i_head_start + i,
                            token.deprel,
                            dd,
                            dd
                        ))

                i_head_start += len(sentence.words)

    return tokens, dependencies

def wl_dependency_parse_tokens(main, tokens, lang, dependency_parser):
    dependencies = []

    # spaCy
    if dependency_parser.startswith('spacy_'):
        nlp = main.__dict__[f'spacy_nlp_{wl_conversion.remove_lang_code_suffixes(lang)}']

        with nlp.select_pipes(disable = (
            pipeline
            for pipeline in ('senter', 'sentencizer')
            if nlp.has_pipe(pipeline)
        )):
            i_head_start = 0

            for doc in nlp.pipe((
                spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [True] * len(tokens))
                for tokens in wl_nlp_utils.split_tokens(main, tokens, dependency_parser)
            )):
                for sentence in doc.sents:
                    i_punc_marks = [
                        i
                        for i, token in enumerate(sentence)
                        if wl_checks_tokens.is_punc(token.text)
                    ]

                    for i, token in enumerate(sentence):
                        dd = token.head.i - token.i

                        # Calculate dependency distances with and without punctuation marks
                        if i_punc_marks and (dd < -1 or dd > 1):
                            dependencies.append((
                                token.head.text,
                                i_head_start + token.head.i,
                                token.dep_,
                                dd,
                                dd - (
                                    bisect.bisect(i_punc_marks, token.head.i)
                                    - bisect.bisect(i_punc_marks, token.i)
                                )
                            ))
                        else:
                            dependencies.append((
                                token.head.text,
                                i_head_start + token.head.i,
                                token.dep_,
                                dd,
                                dd
                            ))

                i_head_start += len(doc)
    # Stanza
    elif dependency_parser.startswith('stanza_'):
        if lang not in {'zho_cn', 'zho_tw'}:
            lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
        else:
            lang_stanza = lang

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']
        i_head_start = 0

        for doc in nlp.bulk_process([
            [tokens]
            for tokens in wl_nlp_utils.split_tokens(main, tokens, dependency_parser)
        ]):
            for sentence in doc.sentences:
                i_punc_marks = [
                    i
                    for i, token in enumerate(sentence.words)
                    if wl_checks_tokens.is_punc(token.text)
                ]

                for i, token in enumerate(sentence.words):
                    dd = token.head - token.id if token.head > 0 else 0

                    # Calculate dependency distances with and without punctuation marks
                    if i_punc_marks and (dd < -1 or dd > 1):
                        dependencies.append((
                            sentence.words[token.head - 1].text if token.head > 0 else token.text,
                            i_head_start + token.head - 1 if token.head > 0 else i_head_start + i,
                            token.deprel,
                            dd,
                            dd - (
                                bisect.bisect(i_punc_marks, token.head - 1)
                                - bisect.bisect(i_punc_marks, token.id - 1)
                            )
                        ))
                    else:
                        dependencies.append((
                            sentence.words[token.head - 1].text if token.head > 0 else token.text,
                            i_head_start + token.head - 1 if token.head > 0 else i_head_start + i,
                            token.deprel,
                            dd,
                            dd
                        ))

                i_head_start += len(sentence.words)

    return dependencies

def wl_dependency_parse_fig(
    main, inputs,
    lang, dependency_parser = 'default',
    show_pos_tags = True, show_fine_grained_pos_tags = False,
    show_lemmas = False, collapse_punc_marks = True, compact_mode = False
):
    if dependency_parser == 'default':
        dependency_parser = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]

    wl_nlp_utils.init_dependency_parsers(
        main,
        lang = lang,
        dependency_parser = dependency_parser,
        tokenized = not isinstance(inputs, str)
    )

    # Only for Settings - Dependency Parsing - Preview
    if isinstance(inputs, str):
        htmls = wl_dependency_parse_fig_text(
            main, inputs,
            lang, dependency_parser,
            show_pos_tags, show_fine_grained_pos_tags,
            show_lemmas, collapse_punc_marks, compact_mode
        )
    # Only for Dependency Parser - Generate figure
    else:
        htmls = wl_dependency_parse_fig_tokens(
            main, inputs,
            lang, dependency_parser,
            show_pos_tags, show_fine_grained_pos_tags,
            show_lemmas, collapse_punc_marks, compact_mode
        )

    return htmls

def _get_pipelines_to_disable(show_pos_tags, show_lemmas):
    if show_pos_tags and show_lemmas:
        pipelines_to_disable = ('senter', 'sentencizer')
    elif show_pos_tags and not show_lemmas:
        pipelines_to_disable = ('senter', 'sentencizer', 'lemmatizer')
    elif not show_pos_tags and show_lemmas:
        pipelines_to_disable = ('senter', 'sentencizer')
    elif not show_pos_tags and not show_lemmas:
        pipelines_to_disable = ('senter', 'sentencizer', 'tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler')

    return pipelines_to_disable

def to_displacy_sentence(lang, sentence, token_properties = None):
    words = []
    tags = []
    pos = []
    lemmas = []
    heads = []
    deps = []

    nlp = spacy.blank('en')

    # RTL languages
    if lang in {
        'ara', 'heb', 'kmr', 'fas', 'snd', 'urd',
        # Unsupported by Stanza: Aramaic, Azerbaijani, Kurdish (Sorani), Maldivian, Fulah, Mazanderani, N'Ko, Pushto, Rohingya, Syriac
        'arc', 'aze', 'ckb', 'div', 'ful', 'mzn', 'nqo', 'pus', 'rhg', 'syr'
    }:
        len_sentence = len(sentence.words)

        if token_properties is not None:
            token_properties = list(reversed(token_properties))

        for i, word in enumerate(reversed(sentence.words)):
            if token_properties is None:
                words.append(word.text)
            else:
                words.append(
                    word.text
                    + (token_properties[i]['punc_mark'] or '')
                    + (token_properties[i]['tag'] or '')
                )

            if word.xpos is not None:
                tags.append(word.xpos)
            else:
                tags.append(word.upos)

            pos.append(word.upos)

            if word.lemma is not None:
                lemmas.append(word.lemma)
            else:
                lemmas.append(word.text)

            deps.append(word.deprel)

            if word.head == 0:
                heads.append(len_sentence - word.id)
            else:
                heads.append(len_sentence - word.head)
    else:
        for i, word in enumerate(sentence.words):
            if token_properties is None:
                words.append(word.text)
            else:
                words.append(
                    word.text
                    + (token_properties[i]['punc_mark'] or '')
                    + (token_properties[i]['tag'] or '')
                )

            if word.xpos is not None:
                tags.append(word.xpos)
            else:
                tags.append(word.upos)

            pos.append(word.upos)

            if word.lemma is not None:
                lemmas.append(word.lemma)
            else:
                lemmas.append(word.text)

            deps.append(word.deprel)

            if word.head == 0:
                heads.append(word.id - 1)
            else:
                heads.append(word.head - 1)

    return spacy.tokens.Doc(nlp.vocab, words = words, tags = tags, pos = pos, lemmas = lemmas, heads = heads, deps = deps)

def wl_dependency_parse_fig_text(
    main, text,
    lang, dependency_parser,
    show_pos_tags, show_fine_grained_pos_tags,
    show_lemmas, collapse_punc_marks, compact_mode
):
    htmls = []

    options = {
        'fine_grained': show_fine_grained_pos_tags,
        'add_lemma': show_lemmas,
        'collapse_punct': collapse_punc_marks,
        'compact': compact_mode
    }

    # spaCy
    if dependency_parser.startswith('spacy_'):
        nlp = main.__dict__[f'spacy_nlp_{wl_conversion.remove_lang_code_suffixes(lang)}']
        batch_size = main.settings_custom['files']['misc_settings']['read_files_in_chunks_lines']

        with nlp.select_pipes(disable = (
            pipeline
            for pipeline in _get_pipelines_to_disable(show_pos_tags, show_lemmas)
            if nlp.has_pipe(pipeline)
        )):
            for doc in nlp.pipe(text.splitlines(), batch_size = batch_size):
                for sentence in doc.sents:
                    span_start = 0

                    for i, token in enumerate(sentence):
                        if '\n' in token.text:
                            if i > span_start:
                                htmls.append(spacy.displacy.render(
                                    doc[sentence.start + span_start : sentence.start + i],
                                    style = 'dep',
                                    minify = True,
                                    options = options
                                ))

                            span_start = i + 1

                    if span_start < len(sentence):
                        htmls.append(spacy.displacy.render(
                            doc[sentence.start + span_start: sentence.end],
                            style = 'dep',
                            minify = True,
                            options = options
                        ))
    # Stanza
    # Reference: https://github.com/stanfordnlp/stanza/pull/1069/files
    elif dependency_parser.startswith('stanza_'):
        if lang not in {'zho_cn', 'zho_tw'}:
            lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
        else:
            lang_stanza = lang

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']

        for doc in nlp.bulk_process(text.splitlines()):
            for sentence in doc.sentences:
                htmls.append(spacy.displacy.render(
                    to_displacy_sentence(lang, sentence),
                    style = 'dep',
                    minify = True,
                    options = options
                ))

    return htmls

def wl_dependency_parse_fig_tokens(
    main, sentences,
    lang, dependency_parser,
    show_pos_tags, show_fine_grained_pos_tags,
    show_lemmas, collapse_punc_marks, compact_mode
):
    htmls = []

    options = {
        'fine_grained': show_fine_grained_pos_tags,
        'add_lemma': show_lemmas,
        'collapse_punct': collapse_punc_marks,
        'compact': compact_mode
    }

    # spaCy
    if dependency_parser.startswith('spacy_'):
        nlp = main.__dict__[f'spacy_nlp_{wl_conversion.remove_lang_code_suffixes(lang)}']

        with nlp.select_pipes(disable = (
            pipeline
            for pipeline in _get_pipelines_to_disable(show_pos_tags, show_lemmas)
            if nlp.has_pipe(pipeline)
        )):
            docs = []
            token_properties = []

            for tokens in sentences:
                texts, token_properties_sentence = wl_texts.split_texts_properties(tokens)

                for token_section in wl_nlp_utils.split_tokens(main, texts, dependency_parser):
                    docs.append(spacy.tokens.Doc(nlp.vocab, words = token_section, spaces = [True] * len(token_section)))

                token_properties.extend(token_properties_sentence)

            i_tag = 0

            for doc in nlp.pipe(docs):
                for sentence in doc.sents:
                    displacy_dict = spacy.displacy.parse_deps(sentence, options = options)

                    for token, word in zip(sentence, displacy_dict['words']):
                        properties = token_properties[i_tag + token.i]
                        word['text'] += (properties['punc_mark'] or '') + (properties['tag'] or '')

                    htmls.append(spacy.displacy.render(
                        displacy_dict,
                        style = 'dep',
                        minify = True,
                        options = options,
                        manual = True
                    ))

                i_tag += len(doc)
    # Stanza
    elif dependency_parser.startswith('stanza_'):
        if lang not in {'zho_cn', 'zho_tw'}:
            lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
        else:
            lang_stanza = lang

        docs = []
        token_properties = []

        for tokens in sentences:
            texts, token_properties_sentence = wl_texts.split_texts_properties(tokens)

            for token_section in wl_nlp_utils.split_tokens(main, texts, dependency_parser):
                docs.append([token_section])

            token_properties.extend(token_properties_sentence)

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']
        i_tag = 0

        for doc in nlp.bulk_process(docs):
            for sentence in doc.sentences:
                num_words = len(sentence.words)

                displacy_dict = to_displacy_sentence(
                    lang, sentence,
                    token_properties = token_properties[i_tag : i_tag + num_words]
                )

                htmls.append(spacy.displacy.render(
                    displacy_dict,
                    style = 'dep',
                    minify = True,
                    options = options
                ))

                i_tag += num_words

    return htmls

def wl_show_dependency_graphs(parent, htmls, show_in_separate_tabs):
    # pylint: disable=consider-using-with
    DIR_PATH = os.path.join(wl_settings_default.DEFAULT_DIR_EXPS, '_dependency_parsing_figs')

    # Clean cache
    if os.path.exists(DIR_PATH):
        shutil.rmtree(DIR_PATH)

    # Inform users of figures' save location in case the browser does not start successfully
    wl_dialogs.Wl_Dialog_Info_Simple(
        parent,
        title = _tr('wl_dependency_parsing', 'Dependency Graphs Generated Successfully'),
        text = _tr('wl_dependency_parsing', '''
            <div>Dependency graphs has been successfully generated and exported under folder: {}</div>
            <br>
            <div>If the figures are not displayed automatically, you may try opening them manually using web browsers or image viewers installed on your computer, or save copies of them in other locations for later use.</div>
        ''').format(wl_paths.get_normalized_path(DIR_PATH)),
        width = 550
    ).open()

    fig_dir = wl_checks_misc.check_dir(DIR_PATH)

    # Change the owner of the figure folder to user on Linux so that figures could be opened with browsers
    if is_linux:
        wl_misc.change_file_owner_to_user(fig_dir)

    if show_in_separate_tabs:
        for html in htmls:
            fig_path = wl_checks_misc.check_new_path(os.path.join(fig_dir, 'fig.svg'))
            fig_path = wl_paths.get_normalized_path(fig_path)

            with open(fig_path, 'w', encoding = 'utf_8') as f:
                f.write(html)

            if is_windows or is_macos:
                webbrowser.open(f'file://{fig_path}')
            elif is_linux:
                wl_misc.change_file_owner_to_user(fig_path)

                subprocess.Popen(('xdg-open', f'file://{fig_path}'))
    else:
        fig_path = wl_checks_misc.check_new_path(os.path.join(fig_dir, 'fig.html'))
        fig_path = wl_paths.get_normalized_path(fig_path)

        with open(fig_path, 'w', encoding = 'utf_8') as f:
            f.write('<br>'.join(htmls))

        if is_windows or is_macos:
            webbrowser.open(f'file://{fig_path}')
        elif is_linux:
            wl_misc.change_file_owner_to_user(fig_path)

            subprocess.Popen(['xdg-open', f'file://{fig_path}'])
