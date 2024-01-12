# ----------------------------------------------------------------------
# Wordless: NLP - POS tagging
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

import khmernltk
import laonlp
import nltk
import pythainlp
import spacy
import underthesea

from wordless.wl_nlp import wl_nlp_utils, wl_word_tokenization
from wordless.wl_utils import wl_conversion

UNIVERSAL_TAGSETS_SPACY = [
    'spacy_cat', 'spacy_dan', 'spacy_fra', 'spacy_ell', 'spacy_mkd',
    'spacy_nob', 'spacy_por', 'spacy_rus', 'spacy_spa', 'spacy_ukr'
]

def wl_pos_tag(main, inputs, lang, pos_tagger = 'default', tagset = 'default'):
    tokens_tagged = []

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'][lang]

    if tagset == 'default' and main.settings_custom['pos_tagging']['pos_tagger_settings']['to_universal_pos_tags']:
        tagset = 'universal'

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

    # Untokenized
    if isinstance(inputs, str):
        # spaCy
        if pos_tagger.startswith('spacy_'):
            lang_spacy = wl_conversion.remove_lang_code_suffixes(main, lang)
            nlp = main.__dict__[f'spacy_nlp_{lang_spacy}']
            lines = [line.strip() for line in inputs.splitlines() if line.strip()]

            with nlp.select_pipes(disable = [
                pipeline
                for pipeline in ['parser', 'lemmatizer', 'senter', 'sentencizer']
                if nlp.has_pipe(pipeline)
            ]):
                for doc in nlp.pipe(lines):
                    if tagset in ['default', 'raw']:
                        tokens_tagged.extend([(token.text, token.tag_) for token in doc])
                    elif tagset == 'universal':
                        tokens_tagged.extend([(token.text, token.pos_) for token in doc])
        # Stanza
        elif pos_tagger.startswith('stanza_'):
            if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
                lang_stanza = wl_conversion.remove_lang_code_suffixes(main, lang)
            else:
                lang_stanza = lang

            nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']
            lines = [line.strip() for line in inputs.splitlines() if line.strip()]

            for doc in nlp.bulk_process(lines):
                for sentence in doc.sentences:
                    if tagset in ['default', 'raw']:
                        for token in sentence.words:
                            if token.xpos is not None:
                                tokens_tagged.append((token.text, token.xpos))
                            else:
                                tokens_tagged.append((token.text, token.upos))
                    elif tagset == 'universal':
                        tokens_tagged.extend([(token.text, token.upos) for token in sentence.words])
        else:
            for line in inputs.splitlines():
                tokens_tagged.extend(wl_pos_tag_text(main, line, lang, pos_tagger))
    # Tokenized
    else:
        # Record positions of empty tokens since spacy.tokens.Doc does not accept empty strings
        empty_offsets = []

        for i, token in reversed(list(enumerate(inputs))):
            if not token.strip():
                empty_offsets.append(i)

                del inputs[i]

        # spaCy
        if pos_tagger.startswith('spacy_'):
            lang_spacy = wl_conversion.remove_lang_code_suffixes(main, lang)
            nlp = main.__dict__[f'spacy_nlp_{lang_spacy}']

            with nlp.select_pipes(disable = [
                pipeline
                for pipeline in ['parser', 'lemmatizer', 'senter', 'sentencizer']
                if nlp.has_pipe(pipeline)
            ]):
                docs = []

                for tokens in wl_nlp_utils.split_token_list(main, inputs, pos_tagger):
                    # The Japanese model do not have a tagger component and Japanese POS tags are taken directly from SudachiPy
                    # See: https://github.com/explosion/spaCy/discussions/9983#discussioncomment-1910117
                    if lang == 'jpn':
                        docs.append(''.join(tokens))
                    else:
                        docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [True] * len(tokens)))

                for doc in nlp.pipe(docs):
                    if tagset in ['default', 'raw']:
                        tokens_tagged.extend([(token.text, token.tag_) for token in doc])
                    elif tagset == 'universal':
                        tokens_tagged.extend([(token.text, token.pos_) for token in doc])
        # Stanza
        elif pos_tagger.startswith('stanza_'):
            if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
                lang_stanza = wl_conversion.remove_lang_code_suffixes(main, lang)
            else:
                lang_stanza = lang

            nlp = main.__dict__[f'stanza_nlp_{lang_stanza}']

            for doc in nlp.bulk_process([
                [tokens]
                for tokens in wl_nlp_utils.split_token_list(main, inputs, pos_tagger)
            ]):
                for sentence in doc.sentences:
                    if tagset in ['default', 'raw']:
                        for token in sentence.words:
                            if token.xpos is not None:
                                tokens_tagged.append((token.text, token.xpos))
                            else:
                                tokens_tagged.append((token.text, token.upos))
                    elif tagset == 'universal':
                        tokens_tagged.extend([(token.text, token.upos) for token in sentence.words])
        else:
            for tokens in wl_nlp_utils.split_token_list(main, inputs, pos_tagger):
                tokens_tagged.extend(wl_pos_tag_tokens(main, tokens, lang, pos_tagger))

    # Remove empty tokens (e.g. SudachiPy) and strip whitespace around tokens and tags
    tokens_tagged = [
        (token_clean, tag.strip())
        for token, tag in tokens_tagged
        if (token_clean := token.strip())
    ]

    if not isinstance(inputs, str):
        tokens_tagged_tokens = [item[0] for item in tokens_tagged]
        tokens_tagged_tags = [item[1] for item in tokens_tagged]
        tokens_tagged_tags = wl_nlp_utils.align_tokens(inputs, tokens_tagged_tokens, tokens_tagged_tags)

        tokens_tagged = list(zip(inputs, tokens_tagged_tags))

        # Insert empty tokens after alignment of input and output
        for empty_offset in sorted(empty_offsets):
            tokens_tagged.insert(empty_offset, ('', ''))

    # Convert to universal POS tags
    if (
        tagset == 'universal'
        and (
            (
                not pos_tagger.startswith('spacy_')
                and not pos_tagger.startswith('stanza_')
            )
            or pos_tagger in UNIVERSAL_TAGSETS_SPACY
        )
    ):
        mappings = {
            tag: tag_universal
            for tag, tag_universal, _, _ in main.settings_custom['pos_tagging']['tagsets']['mapping_settings'][lang][pos_tagger]
        }

        tokens_tagged = [
            (token, mappings.get(tag, 'X'))
            for token, tag in list(tokens_tagged)
        ]

    return tokens_tagged

def wl_pos_tag_text(main, text, lang, pos_tagger):
    tokens_tagged = []

    # English & Russian
    if pos_tagger.startswith('nltk_perceptron_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)
        tokens_tagged = nltk.pos_tag(tokens, lang = lang)
    # Japanese
    elif pos_tagger == 'sudachipy_jpn':
        tokens_tagged = [
            (token.surface(), '-'.join([pos for pos in token.part_of_speech()[:4] if pos != '*']))
            for token in main.sudachipy_word_tokenizer.tokenize(text)
        ]
    # Khmer
    elif pos_tagger == 'khmer_nltk_khm':
        tokens_tagged = khmernltk.pos_tag(text)
    # Korean
    elif pos_tagger == 'python_mecab_ko_mecab':
        tokens_tagged = main.python_mecab_ko_mecab.pos(text)
    # Lao
    elif pos_tagger.startswith('laonlp_'):
        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

        if pos_tagger == 'laonlp_seqlabeling':
            tokens_tagged = laonlp.pos_tag(tokens, corpus = 'SeqLabeling')
        if pos_tagger == 'laonlp_yunshan_cup_2020':
            tokens_tagged = laonlp.pos_tag(tokens, corpus = 'yunshan_cup_2020')
    # Russian & Ukrainian
    elif pos_tagger == 'pymorphy3_morphological_analyzer':
        if lang == 'rus':
            morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
        elif lang == 'ukr':
            morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

        for token in tokens:
            tokens_tagged.append((token, morphological_analyzer.parse(token)[0].tag._POS))
    # Thai
    elif pos_tagger.startswith('pythainlp_'):
        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

        if pos_tagger == 'pythainlp_perceptron_blackboard':
            tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'blackboard')
        elif pos_tagger == 'pythainlp_perceptron_orchid':
            tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
        elif pos_tagger == 'pythainlp_perceptron_pud':
            tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')
    # Tibetan
    elif pos_tagger == 'botok_bod':
        tokens = main.botok_word_tokenizer.tokenize(text)

        for token in tokens:
            if token.pos:
                tokens_tagged.append((token.text, token.pos))
            else:
                tokens_tagged.append((token.text, token.chunk_type))
    # Vietnamese
    elif pos_tagger == 'underthesea_vie':
        tokens_tagged = underthesea.pos_tag(text)

    return list(tokens_tagged)

def wl_pos_tag_tokens(main, tokens, lang, pos_tagger):
    tokens_tagged = []

    lang = wl_conversion.remove_lang_code_suffixes(main, lang)

    # English & Russian
    if pos_tagger.startswith('nltk_perceptron_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        tokens_tagged = nltk.pos_tag(tokens, lang = lang)
    # Japanese
    elif pos_tagger == 'sudachipy_jpn':
        tokens_tagged = [
            (token.surface(), '-'.join([pos for pos in token.part_of_speech()[:4] if pos != '*']))
            for token in main.sudachipy_word_tokenizer.tokenize(''.join(tokens))
        ]
    # Khmer
    elif pos_tagger == 'khmer_nltk_khm':
        tokens_tagged = khmernltk.pos_tag(''.join(tokens))
    # Korean
    elif pos_tagger == 'python_mecab_ko_mecab':
        tokens_tagged = wl_pos_tag_text(main, ' '.join(tokens), lang = 'kor', pos_tagger = 'python_mecab_ko_mecab')
    # Lao
    elif pos_tagger.startswith('laonlp_'):
        if pos_tagger == 'laonlp_seqlabeling':
            tokens_tagged = laonlp.pos_tag(tokens, corpus = 'SeqLabeling')
        if pos_tagger == 'laonlp_yunshan_cup_2020':
            tokens_tagged = laonlp.pos_tag(tokens, corpus = 'yunshan_cup_2020')
    # Russian & Ukrainian
    elif pos_tagger == 'pymorphy3_morphological_analyzer':
        if lang == 'rus':
            morphological_analyzer = main.pymorphy3_morphological_analyzer_rus
        elif lang == 'ukr':
            morphological_analyzer = main.pymorphy3_morphological_analyzer_ukr

        for token in tokens:
            tokens_tagged.append((token, morphological_analyzer.parse(token)[0].tag._POS))
    # Thai
    elif pos_tagger == 'pythainlp_perceptron_blackboard':
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'blackboard')
    elif pos_tagger == 'pythainlp_perceptron_orchid':
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
    elif pos_tagger == 'pythainlp_perceptron_pud':
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')
    # Tibetan
    elif pos_tagger == 'botok_bod':
        tokens_retokenized = main.botok_word_tokenizer.tokenize(''.join(tokens))

        for token in tokens_retokenized:
            if token.pos:
                tokens_tagged.append((token.text, token.pos))
            else:
                tokens_tagged.append((token.text, token.chunk_type))
    # Vietnamese
    elif pos_tagger == 'underthesea_vie':
        tokens_tagged = underthesea.pos_tag(' '.join(tokens))

    return list(tokens_tagged)
