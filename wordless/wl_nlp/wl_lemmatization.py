# ----------------------------------------------------------------------
# Wordless: NLP - Lemmatization
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

import nltk
from PyQt5.QtCore import QCoreApplication
import simplemma
import spacy

from wordless.wl_nlp import (
    wl_nlp_utils,
    wl_pos_tagging,
    wl_texts,
    wl_word_tokenization
)
from wordless.wl_utils import wl_conversion

_tr = QCoreApplication.translate

def wl_lemmatize(main, inputs, lang, lemmatizer = 'default', force = False):
    if (
        not isinstance(inputs, str)
        and inputs
        and list(inputs)[0].lemma is not None
        and not force
    ):
        return inputs
    else:
        if inputs and lang in main.settings_global['lemmatizers']:
            if lemmatizer == 'default':
                lemmatizer = main.settings_custom['lemmatization']['lemmatizer_settings'][lang]

            wl_nlp_utils.init_word_tokenizers(
                main,
                lang = lang
            )
            wl_nlp_utils.init_lemmatizers(
                main,
                lang = lang,
                lemmatizer = lemmatizer,
                tokenized = not isinstance(inputs, str)
            )

            if isinstance(inputs, str):
                texts, lemmas = wl_lemmatize_text(main, inputs, lang, lemmatizer)

                return wl_texts.to_tokens(texts, lang = lang, lemmas = lemmas)
            else:
                texts, token_properties = wl_texts.split_texts_properties(inputs)

                lemmas = wl_lemmatize_tokens(main, texts, lang, lemmatizer)
                tokens = wl_texts.combine_texts_properties(texts, token_properties)
                wl_texts.set_token_properties(tokens, 'lemma', lemmas)

                wl_texts.update_token_properties(inputs, tokens)

                return inputs
        else:
            if isinstance(inputs, str):
                tokens = wl_word_tokenization.wl_word_tokenize_flat(main, inputs, lang = lang)
                wl_texts.set_token_properties(tokens, 'lemma', wl_texts.to_token_texts(tokens))

                return tokens
            else:
                wl_texts.set_token_properties(inputs, 'lemma', wl_texts.to_token_texts(inputs))

                return inputs

def wl_lemmatize_text(main, inputs, lang, lemmatizer):
    tokens = []
    lemmas = []

    # spaCy
    if lemmatizer.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['parser', 'senter', 'sentencizer']
            if nlp.has_pipe(pipeline)
        ]):
            for doc in nlp.pipe(inputs.splitlines()):
                for token in doc:
                    tokens.append(token.text)

                    if token.lemma_:
                        lemmas.append(token.lemma_)
                    else:
                        lemmas.append(token.text)
    # Stanza
    elif lemmatizer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'stanza_nlp_{lang}']
        lines = [line.strip() for line in inputs.splitlines() if line.strip()]

        for doc in nlp.bulk_process(lines):
            for sentence in doc.sentences:
                for token in sentence.words:
                    tokens.append(token.text)

                    if token.lemma is not None:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.text)
    else:
        for line in inputs.splitlines():
            # simplemma
            if lemmatizer.startswith('simplemma_'):
                tokens_line = wl_word_tokenization.wl_word_tokenize_flat(main, line, lang = lang)
                tokens_line = wl_texts.to_display_texts(tokens_line)

                if lang in ['hrv', 'srp_latn']:
                    lang = 'hbs'
                else:
                    lang = wl_conversion.to_iso_639_1(main, lang, no_suffix = True)

                tokens.extend((str(token) for token in tokens_line))
                lemmas.extend((simplemma.lemmatize(token, lang = lang) for token in tokens_line))
            # English
            elif lemmatizer == 'nltk_wordnet':
                word_net_lemmatizer = nltk.WordNetLemmatizer()

                for token in wl_pos_tagging.wl_pos_tag_universal(
                    main, line,
                    lang = 'eng_us'
                ):
                    tokens.append(str(token))

                    match token.tag_universal:
                        case 'ADJ':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.ADJ))
                        case 'NOUN' | 'PROPN':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.NOUN))
                        case 'ADV':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.ADV))
                        case 'VERB' | 'AUX':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.VERB))
                        case _:
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token)))
            # Japanese
            elif lemmatizer == 'sudachipy_jpn':
                for token in main.sudachipy_word_tokenizer.tokenize(line):
                    tokens.append(token.surface())
                    lemmas.append(token.dictionary_form())
            # Russian & Ukrainian
            elif lemmatizer == 'pymorphy3_morphological_analyzer':
                match lang:
                    case 'rus':
                        morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
                    case 'ukr':
                        morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

                for token in wl_word_tokenization.wl_word_tokenize_flat(main, line, lang = lang):
                    tokens.append(str(token))
                    lemmas.append(morphological_analyzer.parse(token)[0].normal_form)
            # Tibetan
            elif lemmatizer == 'botok_bod':
                for token in main.botok_word_tokenizer.tokenize(line):
                    tokens.append(token.text)

                    if token.lemma:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.text)

    # Strip whitespace around lemmas and remove empty lemmas
    for i, lemma in reversed(list(enumerate(lemmas))):
        lemmas[i] = str(lemma).strip()

        if not lemmas[i]:
            del tokens[i]
            del lemmas[i]

    return tokens, lemmas

def wl_lemmatize_tokens(main, inputs, lang, lemmatizer):
    lemma_tokens = []
    lemmas = []

    # spaCy
    if lemmatizer.startswith('spacy_'):
        lang_spacy = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang_spacy}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['parser', 'senter', 'sentencizer']
            if nlp.has_pipe(pipeline)
        ]):
            docs = []

            for tokens in wl_nlp_utils.split_token_list(main, inputs, lemmatizer):
                # The Japanese model do not have a lemmatizer component and Japanese lemmas are taken directly from SudachiPy
                # See: https://github.com/explosion/spaCy/discussions/9983#discussioncomment-1923647
                if lang == 'jpn':
                    docs.append(''.join(tokens))
                else:
                    docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [True] * len(tokens)))

            for doc in nlp.pipe(docs):
                for token in doc:
                    if token.lemma_:
                        lemmas.append(token.lemma_)
                    else:
                        lemmas.append(token.text)

                lemma_tokens.extend([token.text for token in doc])
    # Stanza
    elif lemmatizer.startswith('stanza_'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang_stanza = wl_conversion.remove_lang_code_suffixes(main, lang)
        else:
            lang_stanza = lang

        nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']

        for doc in nlp.bulk_process([
            [tokens]
            for tokens in wl_nlp_utils.split_token_list(main, inputs, lemmatizer)
        ]):
            for sentence in doc.sentences:
                for token in sentence.words:
                    if token.lemma is not None:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.text)

                lemma_tokens.extend([token.text for token in sentence.words])
    else:
        for tokens in wl_nlp_utils.split_token_list(main, inputs, lemmatizer):
            # simplemma
            if lemmatizer.startswith('simplemma_'):
                if lang in ['hrv', 'srp_latn']:
                    lang_simplemma = 'hbs'
                else:
                    lang_simplemma = wl_conversion.to_iso_639_1(main, lang, no_suffix = True)

                lemma_tokens.extend(tokens.copy())
                lemmas.extend([simplemma.lemmatize(token, lang = lang_simplemma) for token in tokens])
            # English
            elif lemmatizer == 'nltk_wordnet':
                word_net_lemmatizer = nltk.WordNetLemmatizer()

                for token in wl_pos_tagging.wl_pos_tag_universal(
                    main,
                    inputs = wl_texts.to_tokens(tokens, lang = 'eng_us'),
                    lang = 'eng_us'
                ):
                    match token.tag_universal:
                        case 'ADJ':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.ADJ))
                        case 'NOUN' | 'PROPN':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.NOUN))
                        case 'ADV':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.ADV))
                        case 'VERB' | 'AUX':
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token), pos = nltk.corpus.wordnet.VERB))
                        case _:
                            lemmas.append(word_net_lemmatizer.lemmatize(str(token)))

                lemma_tokens.extend(tokens.copy())
            # Japanese
            elif lemmatizer == 'sudachipy_jpn':
                for token in main.sudachipy_word_tokenizer.tokenize(''.join(tokens)):
                    lemma_tokens.append(token.surface())
                    lemmas.append(token.dictionary_form())
            # Russian & Ukrainian
            elif lemmatizer == 'pymorphy3_morphological_analyzer':
                match lang:
                    case 'rus':
                        morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
                    case 'ukr':
                        morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

                for token in tokens:
                    lemmas.append(morphological_analyzer.parse(token)[0].normal_form)

                lemma_tokens.extend(tokens.copy())
            # Tibetan
            elif lemmatizer == 'botok_bod':
                tokens_retokenized = main.botok_word_tokenizer.tokenize(''.join(tokens))

                for token in tokens_retokenized:
                    if token.lemma:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.text)

                    lemma_tokens.append(token.text)

    # Strip whitespace around lemmas and remove empty lemmas
    for i, (lemma, lemma_token) in reversed(list(enumerate(zip(lemmas, lemma_tokens)))):
        lemmas[i] = str(lemma).strip()
        lemma_tokens[i] = str(lemma_token).strip()

        if not lemmas[i]:
            del lemmas[i]
            del lemma_tokens[i]

    lemmas = wl_nlp_utils.align_tokens(inputs, lemma_tokens, lemmas, prefer_raw = True)

    return lemmas
