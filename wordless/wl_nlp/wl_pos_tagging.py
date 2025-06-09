# ----------------------------------------------------------------------
# Wordless: NLP - POS tagging
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

import copy

import khmernltk
import laonlp
import nltk
from PyQt5 import QtCore
import pythainlp
import spacy
import underthesea

from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_conversion

_tr = QtCore.QCoreApplication.translate

UNIVERSAL_TAGSETS_SPACY = {
    'spacy_cat', 'spacy_dan', 'spacy_fra', 'spacy_ell', 'spacy_mkd',
    'spacy_nob', 'spacy_por', 'spacy_rus', 'spacy_spa', 'spacy_ukr',
    'modern_botok_bod'
}
UNIVERSAL_TAGSETS_STANZA = {
    'stanza_sqi', 'stanza_xcl', 'stanza_hye', 'stanza_hyw', 'stanza_eus',
    'stanza_bxr', 'stanza_dan', 'stanza_fra', 'stanza_nds', 'stanza_ell',
    'stanza_heb', 'stanza_hun', 'stanza_lij', 'stanza_glv', 'stanza_mar',
    'stanza_pcm', 'stanza_qpm', 'stanza_por', 'stanza_rus', 'stanza_san',
    'stanza_snd', 'stanza_hsb', 'stanza_tel'
}

def to_content_function(universal_pos_tag):
    match universal_pos_tag:
        case 'ADJ' | 'ADV' | 'INTJ' | 'NOUN' | 'PROPN' | 'NUM' | 'VERB' | 'SYM' | 'X' | 'NOUN/NUM' | 'SYM/X':
            return _tr('wl_pos_tagging', 'Content words')
        case 'ADP' | 'AUX' | 'CONJ' | 'CCONJ' | 'SCONJ' | 'DET' | 'PART' | 'PRON' | 'PUNCT' | 'ADP/SCONJ' | 'PUNCT/SYM':
            return _tr('wl_pos_tagging', 'Function words')
        case _:
            return None

def wl_pos_tag(main, inputs, lang, pos_tagger = 'default', tagset = 'default', separator = 'default', force = False):
    if (
        not isinstance(inputs, str)
        and inputs
        and any(
            list(inputs)[0].tag is not None
            for token in inputs
        )
        and not force
    ):
        return inputs
    else:
        texts_tagged = []
        tags = []

        settings = main.settings_custom['pos_tagging']

        if pos_tagger == 'default':
            pos_tagger = settings['pos_tagger_settings']['pos_taggers'][lang]

        if tagset == 'default' and settings['pos_tagger_settings']['to_universal_pos_tags']:
            tagset = 'universal'

        if separator == 'default':
            separator = main.settings_custom['pos_tagging']['pos_tagger_settings']['separator_between_tokens_pos_tags']

        wl_nlp_utils.init_word_tokenizers(
            main,
            lang = lang
        )
        wl_nlp_utils.init_pos_taggers(
            main,
            lang = lang,
            pos_tagger = pos_tagger,
            tokenized = not isinstance(inputs, str)
        )

        tags_universal = []

        if isinstance(inputs, str):
            # spaCy and modern-botok
            if pos_tagger.startswith('spacy_') or pos_tagger == 'modern_botok_bod':
                lang_spacy = wl_conversion.remove_lang_code_suffixes(lang)
                nlp = main.__dict__[f'spacy_nlp_{lang_spacy}']
                lines = (line.strip() for line in inputs.splitlines() if line.strip())

                with nlp.select_pipes(disable = (
                    pipeline
                    for pipeline in ('parser', 'lemmatizer', 'senter', 'sentencizer')
                    if nlp.has_pipe(pipeline)
                )):
                    for doc in nlp.pipe(lines):
                        for token in doc:
                            texts_tagged.append(token.text)

                            # modern-botok's model has no fine-grained POS tags
                            if pos_tagger == 'modern_botok_bod':
                                tags.append(token.pos_)
                            else:
                                match tagset:
                                    case 'default' | 'raw':
                                        tags.append(token.tag_)
                                    # Convert empty universal POS tags to "X" (e.g. those for numbers in the Romanian model)
                                    case 'universal':
                                        tags.append(token.pos_.strip() if token.pos_.strip() else 'X')

                            # Apply custom mappings only to spaCy's models not adopting the Universal Dependencies tagset
                            if pos_tagger not in UNIVERSAL_TAGSETS_SPACY:
                                # Convert empty universal POS tags to "X" (e.g. those for numbers in the Romanian model)
                                tags_universal.append(token.pos_.strip() if token.pos_.strip() else 'X')
            # Stanza
            elif pos_tagger.startswith('stanza_'):
                if lang not in ('zho_cn', 'zho_tw', 'srp_latn'):
                    lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
                else:
                    lang_stanza = lang

                nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']
                lines = (line.strip() for line in inputs.splitlines() if line.strip())

                for doc in nlp.bulk_process(lines):
                    for sentence in doc.sentences:
                        for token in sentence.words:
                            texts_tagged.append(token.text)

                            match tagset:
                                case 'default' | 'raw':
                                    tags.append(token.xpos if token.xpos else token.upos)
                                case 'universal':
                                    tags.append(token.upos)

                            # Apply custom mappings only to Stanza's models not adopting the Universal Dependencies tagset
                            if pos_tagger not in UNIVERSAL_TAGSETS_STANZA:
                                tags_universal.append(token.upos)
            else:
                for line in inputs.splitlines():
                    tokens_tagged_line, tags_line = wl_pos_tag_text(main, line, lang, pos_tagger)

                    texts_tagged.extend(tokens_tagged_line)
                    tags.extend(tags_line)
        else:
            texts, token_properties = wl_texts.split_texts_properties(inputs)

            # spaCy and modern-botok
            if pos_tagger.startswith('spacy_') or pos_tagger == 'modern_botok_bod':
                lang_spacy = wl_conversion.remove_lang_code_suffixes(lang)
                nlp = main.__dict__[f'spacy_nlp_{lang_spacy}']

                with nlp.select_pipes(disable = (
                    pipeline
                    for pipeline in ('parser', 'lemmatizer', 'senter', 'sentencizer')
                    if nlp.has_pipe(pipeline)
                )):
                    docs = []

                    for tokens in wl_nlp_utils.split_token_list(main, texts, pos_tagger):
                        # The Japanese model do not have a tagger component and Japanese POS tags are taken directly from SudachiPy
                        # See: https://github.com/explosion/spaCy/discussions/9983#discussioncomment-1910117
                        if lang == 'jpn':
                            docs.append(''.join(tokens))
                        else:
                            docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [True] * len(tokens)))

                    for doc in nlp.pipe(docs):
                        for token in doc:
                            texts_tagged.append(token.text)

                            # modern-botok's model has no fine-grained POS tags
                            if pos_tagger == 'modern_botok_bod':
                                tags.append(token.pos_)
                            else:
                                match tagset:
                                    case 'default' | 'raw':
                                        tags.append(token.tag_)
                                    # Convert empty universal POS tags to "X" (e.g. those for numbers in the Romanian model)
                                    case 'universal':
                                        tags.append(token.pos_.strip() if token.pos_.strip() else 'X')

                            # Apply custom mappings only to spaCy's models not adopting the Universal Dependencies tagset
                            if pos_tagger not in UNIVERSAL_TAGSETS_SPACY:
                                # Convert empty universal POS tags to "X" (e.g. those for numbers in the Romanian model)
                                tags_universal.append(token.pos_.strip() if token.pos_.strip() else 'X')
            # Stanza
            elif pos_tagger.startswith('stanza_'):
                if lang not in ('zho_cn', 'zho_tw', 'srp_latn'):
                    lang_stanza = wl_conversion.remove_lang_code_suffixes(lang)
                else:
                    lang_stanza = lang

                nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']

                for doc in nlp.bulk_process([
                    [tokens]
                    for tokens in wl_nlp_utils.split_token_list(main, texts, pos_tagger)
                ]):
                    for sentence in doc.sentences:
                        for token in sentence.words:
                            texts_tagged.append(token.text)

                            match tagset:
                                case 'default' | 'raw':
                                    tags.append(token.xpos if token.xpos else token.upos)
                                case 'universal':
                                    tags.append(token.upos)

                            # Apply custom mappings only to Stanza's models not adopting the Universal Dependencies tagset
                            if pos_tagger not in UNIVERSAL_TAGSETS_STANZA:
                                tags_universal.append(token.upos)
            else:
                for tokens in wl_nlp_utils.split_token_list(main, texts, pos_tagger):
                    results = wl_pos_tag_tokens(main, tokens, lang, pos_tagger)

                    texts_tagged.extend(results[0])
                    tags.extend(results[1])

        # Custom mapping is available only for spaCy's and Stanza's models adopting the Universal Dependencies tagset and other POS taggers
        if (
            not pos_tagger.startswith(('spacy_', 'stanza_'))
            or pos_tagger in UNIVERSAL_TAGSETS_SPACY | UNIVERSAL_TAGSETS_STANZA
        ):
            mappings = {
                tag: tag_universal
                for tag, tag_universal, _, _, _ in settings['tagsets']['mapping_settings'][lang][pos_tagger]
            }

            # Convert empty tags (to be removed later) to "X"
            tags_universal = [(mappings[tag.strip()] if tag.strip() else 'X') for tag in tags]

        # Remove empty tokens (e.g. SudachiPy) and strip whitespace around tokens and tags
        for i, token in reversed(list(enumerate(texts_tagged))):
            if (token_clean := token.strip()):
                texts_tagged[i] = token_clean
            else:
                del texts_tagged[i]
                del tags[i]
                del tags_universal[i]

        if not isinstance(inputs, str):
            tags = wl_nlp_utils.align_tokens(texts, texts_tagged, tags)
            tags_universal = wl_nlp_utils.align_tokens(texts, texts_tagged, tags_universal)

        # Convert to content/function words using universal POS tags for spaCy's and Stanza's models not adopting the Universal Dependencies tagset
        if (
            pos_tagger.startswith(('spacy_', 'stanza_'))
            and pos_tagger not in UNIVERSAL_TAGSETS_SPACY | UNIVERSAL_TAGSETS_STANZA
        ):
            content_functions = [to_content_function(tag) for tag in tags_universal]
        # Convert to content/function words using raw POS tags for spaCy's and Stanza's models adopting the Universal Dependencies tagsets and other POS taggers
        else:
            mappings = {
                tag: content_function
                for tag, _, content_function, _, _ in settings['tagsets']['mapping_settings'][lang][pos_tagger]
            }

            content_functions = [mappings[tag] for tag in tags]

        # Convert to universal POS tags for spaCy's and Stanza's models adopting the Universal Dependencies tagset and other POS taggers
        if (
            tagset == 'universal'
            and (
                not pos_tagger.startswith(('spacy_', 'stanza_'))
                or pos_tagger in UNIVERSAL_TAGSETS_SPACY | UNIVERSAL_TAGSETS_STANZA
            )
        ):
            tags = tags_universal.copy()

        # Add separators between tokens and POS tags
        tags = [f'{separator}{tag}' for tag in tags]

        if isinstance(inputs, str):
            return wl_texts.to_tokens(
                texts_tagged,
                lang = lang,
                tags = tags,
                tags_universal = tags_universal,
                content_functions = content_functions
            )
        else:
            tokens = wl_texts.combine_texts_properties(texts, token_properties)
            wl_texts.set_token_properties(tokens, 'tag', tags)
            wl_texts.set_token_properties(tokens, 'tag_universal', tags_universal)
            wl_texts.set_token_properties(tokens, 'content_function', content_functions)

            wl_texts.update_token_properties(inputs, tokens)

            return inputs

def wl_pos_tag_universal(main, inputs, lang, pos_tagger = 'default', tagged = False):
    if (
        isinstance(inputs, str)
        or (
            not isinstance(inputs, str)
            and inputs
            and inputs[0].tag_universal is None
        )
    ):
        # Assign universal POS tags to tagged files without modifying original tags
        if tagged:
            tokens = wl_pos_tag(main, copy.deepcopy(inputs), lang, pos_tagger, force = True)

            wl_texts.set_token_properties(
                inputs,
                'tag_universal',
                wl_texts.get_token_properties(tokens, 'tag_universal')
            )
            wl_texts.set_token_properties(
                inputs,
                'content_function',
                wl_texts.get_token_properties(tokens, 'content_function')
            )
        else:
            inputs = wl_pos_tag(main, inputs, lang, pos_tagger)

    return inputs

def wl_pos_tag_text(main, text, lang, pos_tagger):
    tokens_tagged = []
    tags = []

    match pos_tagger:
        # English & Russian
        case 'nltk_perceptron_eng' | 'nltk_perceptron_rus':
            tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)
            tokens = wl_texts.to_token_texts(tokens)
            lang = wl_conversion.remove_lang_code_suffixes(lang)

            for token, tag in nltk.pos_tag(tokens, lang = lang):
                tokens_tagged.append(token)
                tags.append(tag)
        # Japanese
        case 'sudachipy_jpn':
            for token in main.sudachipy_word_tokenizer.tokenize(text):
                tokens_tagged.append(token.surface())
                tags.append('-'.join((pos for pos in token.part_of_speech()[:4] if pos != '*')))
        # Khmer
        case 'khmer_nltk_khm':
            for token, tag in khmernltk.pos_tag(text):
                tokens_tagged.append(token)
                tags.append(tag)
        # Korean
        case 'python_mecab_ko_mecab':
            for token, tag in main.python_mecab_ko_mecab.pos(text):
                tokens_tagged.append(token)
                tags.append(tag)
        # Lao
        case 'laonlp_seqlabeling' | 'laonlp_yunshan_cup_2020':
            tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)
            tokens = wl_texts.to_token_texts(tokens)

            if pos_tagger == 'laonlp_seqlabeling':
                results = laonlp.pos_tag(tokens, corpus = 'SeqLabeling')
            if pos_tagger == 'laonlp_yunshan_cup_2020':
                results = laonlp.pos_tag(tokens, corpus = 'yunshan_cup_2020')

            tokens_tagged = [token for token, _ in results]
            tags = [tag for _, tag in results]
        # Russian & Ukrainian
        case 'pymorphy3_morphological_analyzer':
            match lang:
                case 'rus':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
                case 'ukr':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

            tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

            for token in tokens:
                tokens_tagged.append(token)
                tags.append(morphological_analyzer.parse(token)[0].tag._POS)
        # Thai
        case 'pythainlp_perceptron_blackboard' | 'pythainlp_perceptron_orchid' | 'pythainlp_perceptron_pud':
            tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)
            tokens = wl_texts.to_token_texts(tokens)

            match pos_tagger:
                case 'pythainlp_perceptron_blackboard':
                    results = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'blackboard')
                case 'pythainlp_perceptron_orchid':
                    results = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
                case 'pythainlp_perceptron_pud':
                    results = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')

            tokens_tagged = [token for token, _ in results]
            tags = [tag for _, tag in results]
        # Tibetan
        case 'botok_xct':
            for token in main.__dict__['botok_word_tokenizer'].tokenize(text):
                tokens_tagged.append(token.text)
                tags.append(token.pos if token.pos else token.chunk_type)
        # Vietnamese
        case 'underthesea_vie':
            for token, tag in underthesea.pos_tag(text):
                tokens_tagged.append(token)
                tags.append(tag)

    return tokens_tagged, tags

def wl_pos_tag_tokens(main, tokens, lang, pos_tagger):
    tokens_tagged = []
    tags = []

    lang = wl_conversion.remove_lang_code_suffixes(lang)

    match pos_tagger:
        # English & Russian
        case 'nltk_perceptron_eng' | 'nltk_perceptron_rus':
            lang = wl_conversion.remove_lang_code_suffixes(lang)

            for token, tag in nltk.pos_tag(tokens, lang = lang):
                tokens_tagged.append(token)
                tags.append(tag)
        # Japanese
        case 'sudachipy_jpn':
            for token in main.sudachipy_word_tokenizer.tokenize(''.join(tokens)):
                tokens_tagged.append(token.surface())
                tags.append('-'.join((
                    pos
                    for pos in token.part_of_speech()[:4]
                    if pos != '*'
                )))
        # Khmer
        case 'khmer_nltk_khm':
            for token, tag in khmernltk.pos_tag(''.join(tokens)):
                tokens_tagged.append(token)
                tags.append(tag)
        # Korean
        case 'python_mecab_ko_mecab':
            tokens_tagged, tags = wl_pos_tag_text(
                main,
                ' '.join(tokens),
                lang = 'kor',
                pos_tagger = 'python_mecab_ko_mecab'
            )
        # Lao
        case 'laonlp_seqlabeling' | 'laonlp_yunshan_cup_2020':
            if pos_tagger == 'laonlp_seqlabeling':
                results = laonlp.pos_tag(tokens, corpus = 'SeqLabeling')
            if pos_tagger == 'laonlp_yunshan_cup_2020':
                results = laonlp.pos_tag(tokens, corpus = 'yunshan_cup_2020')

            tokens_tagged = [token for token, _ in results]
            tags = [tag for _, tag in results]
        # Russian & Ukrainian
        case 'pymorphy3_morphological_analyzer':
            match lang:
                case 'rus':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
                case 'ukr':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

            for token in tokens:
                tokens_tagged.append(token)
                tags.append(morphological_analyzer.parse(token)[0].tag._POS)
        # Thai
        case 'pythainlp_perceptron_blackboard' | 'pythainlp_perceptron_orchid' | 'pythainlp_perceptron_pud':
            match pos_tagger:
                case 'pythainlp_perceptron_blackboard':
                    results = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'blackboard')
                case 'pythainlp_perceptron_orchid':
                    results = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
                case 'pythainlp_perceptron_pud':
                    results = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')

            tokens_tagged = [token for token, _ in results]
            tags = [tag for _, tag in results]
        # Tibetan
        case 'botok_xct':
            for token in main.__dict__['botok_word_tokenizer'].tokenize(''.join(tokens)):
                tokens_tagged.append(token.text)
                tags.append(token.pos if token.pos else token.chunk_type)
        # Vietnamese
        case 'underthesea_vie':
            for token, tag in underthesea.pos_tag(' '.join(tokens)):
                tokens_tagged.append(token)
                tags.append(tag)

    return tokens_tagged, tags
