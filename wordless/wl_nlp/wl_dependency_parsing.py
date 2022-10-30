# ----------------------------------------------------------------------
# Wordless: NLP - Dependency Parsing
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

import os

import numpy
import spacy

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from wordless.wl_checking import wl_checking_misc
from wordless.wl_nlp import wl_nlp_utils
from wordless.wl_utils import wl_conversion

def wl_dependency_parse(main, inputs, lang, dependency_parser = 'default'):
    if dependency_parser == 'default':
        dependency_parser = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]

    wl_nlp_utils.init_dependency_parsers(main, lang, dependency_parser)

    if isinstance(inputs, str):
        dependencies = wl_dependency_parse_text(main, inputs, lang, dependency_parser)
    else:
        dependencies = wl_dependency_parse_tokens(main, inputs, lang, dependency_parser)

    return dependencies

def wl_dependency_parse_text(main, inputs, lang, dependency_parser):
    dependencies = []

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter', 'sentencizer']
            if nlp.has_pipe(pipeline)
        ]):
            for doc in nlp.pipe(inputs.splitlines()):
                dependencies.extend([
                    (token.text, token.head.text, token.dep_, numpy.abs(token.i - token.head.i))
                    for token in doc
                ])

    return dependencies

def wl_dependency_parse_tokens(main, inputs, lang, dependency_parser):
    dependencies = []

    inputs = [str(token) for token in inputs]

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter', 'sentencizer']
            if nlp.has_pipe(pipeline)
        ]):
            docs = []

            for tokens in wl_nlp_utils.split_token_list(main, inputs, dependency_parser):
                docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens)))

            for doc in nlp.pipe(docs):
                dependencies.extend([
                    (token.text, token.head.text, token.dep_, numpy.abs(token.i - token.head.i))
                    for token in doc
                ])

    return dependencies

def wl_dependency_parse_fig(
    main, inputs, lang, dependency_parser = 'default',
    show_pos_tags = True, show_lemmas = False, compact_mode = False
):
    if dependency_parser == 'default':
        dependency_parser = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]

    wl_nlp_utils.init_dependency_parsers(main, lang, dependency_parser)

    if isinstance(inputs, str):
        wl_dependency_parse_fig_text(main, inputs, lang, dependency_parser, show_pos_tags, show_lemmas, compact_mode)
    else:
        wl_dependency_parse_fig_tokens(main, inputs, lang, dependency_parser, show_pos_tags, show_lemmas, compact_mode)

def get_pipelines_disabled(show_pos_tags, show_lemmas):
    if show_pos_tags and show_lemmas:
        pipelines_disabled = ['senter', 'sentencizer']
    elif show_pos_tags and not show_lemmas:
        pipelines_disabled = ['lemmatizer', 'senter', 'sentencizer']
    elif not show_pos_tags and show_lemmas:
        pipelines_disabled = ['senter', 'sentencizer']
    elif not show_pos_tags and not show_lemmas:
        pipelines_disabled = ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter', 'sentencizer']

    return pipelines_disabled

def wl_dependency_parse_fig_text(main, inputs, lang, dependency_parser, show_pos_tags, show_lemmas, compact_mode):
    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in get_pipelines_disabled(show_pos_tags, show_lemmas)
            if nlp.has_pipe(pipeline)
        ]):
            fig_dir = wl_checking_misc.check_dir('exports/_dependency_parsing_figs')
            fig_path = wl_checking_misc.check_new_path(os.path.join(fig_dir, 'fig.svg'))

            html = spacy.displacy.render(nlp.pipe(inputs.splitlines()), style = 'dep', page = True, options = {
                'add_lemma': show_lemmas,
                'collapse_punct': False,
                'compact': compact_mode,
            })

            with open(fig_path, 'w', encoding = 'utf_8') as f:
                f.write(html)

            QDesktopServices.openUrl(QUrl.fromLocalFile(fig_path))

def wl_dependency_parse_fig_tokens(main, inputs, lang, dependency_parser, show_pos_tags, show_lemmas, compact_mode):
    inputs = [str(token) for token in inputs]

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in get_pipelines_disabled(show_pos_tags, show_lemmas)
            if nlp.has_pipe(pipeline)
        ]):
            docs = []
            fig_dir = wl_checking_misc.check_dir('exports/_dependency_parsing_figs')
            fig_path = wl_checking_misc.check_new_path(os.path.join(fig_dir, 'fig.svg'))

            for tokens in wl_nlp_utils.split_token_list(main, inputs, dependency_parser):
                docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens)))

            html = spacy.displacy.render(nlp.pipe(docs), style = 'dep', page = True, options = {
                'add_lemma': show_lemmas,
                'collapse_punct': False,
                'compact': compact_mode,
            })

            with open(fig_path, 'w', encoding = 'utf_8') as f:
                f.write(html)

            QDesktopServices.openUrl(QUrl.fromLocalFile(fig_path))
