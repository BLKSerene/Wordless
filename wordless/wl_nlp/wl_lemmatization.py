# ----------------------------------------------------------------------
# Wordless: NLP - Lemmatization
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

import nltk
from PyQt5.QtCore import QCoreApplication
import simplemma
import spacy

from wordless.wl_nlp import wl_matching, wl_nlp_utils, wl_pos_tagging, wl_word_tokenization
from wordless.wl_utils import wl_conversion

_tr = QCoreApplication.translate

def wl_lemmatize(main, inputs, lang, lemmatizer = 'default', tagged = False):
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
            lemmas = wl_lemmatize_text(main, inputs, lang, lemmatizer)
        else:
            lemmas = wl_lemmatize_tokens(main, inputs, lang, lemmatizer, tagged)
    else:
        if isinstance(inputs, str):
            lemmas = wl_word_tokenization.wl_word_tokenize_flat(main, inputs, lang = lang)
        else:
            lemmas = inputs.copy()

    return lemmas

def wl_lemmatize_text(main, inputs, lang, lemmatizer):
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
                    if token.lemma is not None:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.text)
    else:
        for line in inputs.splitlines():
            # simplemma
            if lemmatizer.startswith('simplemma_'):
                tokens = wl_word_tokenization.wl_word_tokenize_flat(main, line, lang = lang)

                if lang in ['hrv', 'srp_latn']:
                    lang = 'hbs'
                else:
                    lang = wl_conversion.to_iso_639_1(main, lang, no_suffix = True)

                lemmas.extend([simplemma.lemmatize(token, lang = lang) for token in tokens])
            # English
            elif lemmatizer == 'nltk_wordnet':
                word_net_lemmatizer = nltk.WordNetLemmatizer()

                for token, pos in wl_pos_tagging.wl_pos_tag(
                    main, line,
                    lang = 'eng_us',
                    pos_tagger = 'nltk_perceptron_eng',
                    tagset = 'universal'
                ):
                    if pos == 'ADJ':
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADJ))
                    elif pos in ['NOUN', 'PROPN']:
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.NOUN))
                    elif pos == 'ADV':
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADV))
                    elif pos in ['VERB', 'AUX']:
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.VERB))
                    else:
                        lemmas.append(word_net_lemmatizer.lemmatize(token))
            # Japanese
            elif lemmatizer == 'sudachipy_jpn':
                lemmas.extend([
                    token.dictionary_form()
                    for token in main.sudachipy_word_tokenizer.tokenize(line)
                ])
            # Russian & Ukrainian
            elif lemmatizer == 'pymorphy3_morphological_analyzer':
                if lang == 'rus':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
                elif lang == 'ukr':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

                tokens = wl_word_tokenization.wl_word_tokenize_flat(main, line, lang = lang)

                for token in tokens:
                    lemmas.append(morphological_analyzer.parse(token)[0].normal_form)
            # Tibetan
            elif lemmatizer == 'botok_bod':
                tokens = main.botok_word_tokenizer.tokenize(line)

                for token in tokens:
                    if token.lemma:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.text)

    # Remove empty lemmas and strip whitespace in tokens
    lemmas = [
        lemma_clean
        for lemma in lemmas
        if (lemma_clean := str(lemma).strip())
    ]

    return lemmas

def wl_lemmatize_tokens(main, inputs, lang, lemmatizer, tagged):
    lemma_tokens = []
    lemmas = []
    empty_offsets = []

    if tagged:
        inputs, tags = wl_matching.split_tokens_tags(main, inputs)
    else:
        tags = [''] * len(inputs)

    # Record positions of empty tokens and tags since spacy.tokens.Doc does not accept empty strings
    for i, token in reversed(list(enumerate(inputs))):
        if not token.strip():
            empty_offsets.append(i)

            del inputs[i]
            del tags[i]

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

                for token, pos in wl_pos_tagging.wl_pos_tag(
                    main, tokens,
                    lang = 'eng_us',
                    pos_tagger = 'nltk_perceptron_eng',
                    tagset = 'universal'
                ):
                    if pos == 'ADJ':
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADJ))
                    elif pos in ['NOUN', 'PROPN']:
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.NOUN))
                    elif pos == 'ADV':
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADV))
                    elif pos in ['VERB', 'AUX']:
                        lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.VERB))
                    else:
                        lemmas.append(word_net_lemmatizer.lemmatize(token))

                lemma_tokens.extend(tokens.copy())
            # Japanese
            elif lemmatizer == 'sudachipy_jpn':
                tokens_retokenized = main.sudachipy_word_tokenizer.tokenize(''.join(tokens))

                lemma_tokens.extend([token.surface() for token in tokens_retokenized])
                lemmas.extend([token.dictionary_form() for token in tokens_retokenized])
            # Russian & Ukrainian
            elif lemmatizer == 'pymorphy3_morphological_analyzer':
                if lang == 'rus':
                    morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
                elif lang == 'ukr':
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

    # Remove empty lemmas and strip whitespace around lemmas
    for i, (lemma, lemma_token) in reversed(list(enumerate(zip(lemmas, lemma_tokens)))):
        lemmas[i] = str(lemma).strip()
        lemma_tokens[i] = str(lemma_token).strip()

        if not lemmas[i]:
            del lemmas[i]
            del lemma_tokens[i]

    lemmas = wl_nlp_utils.align_tokens(inputs, lemma_tokens, lemmas, prefer_raw = True)

    # Insert empty lemmas and their tags after alignment of input and output
    for empty_offset in sorted(empty_offsets):
        lemmas.insert(empty_offset, '')
        tags.insert(empty_offset, '')

    return [lemma + tag for lemma, tag in zip(lemmas, tags)]
