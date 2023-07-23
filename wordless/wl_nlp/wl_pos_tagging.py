# ----------------------------------------------------------------------
# Wordless: NLP - POS Tagging
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

import jieba.posseg
import khmernltk
import nltk
import pythainlp
import spacy
import underthesea

from wordless.wl_nlp import wl_nlp_utils, wl_word_tokenization
from wordless.wl_utils import wl_conversion

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
        pos_tagger = pos_tagger
    )

    # Untokenized
    if isinstance(inputs, str):
        # spaCy
        if pos_tagger.startswith('spacy_'):
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)
            nlp = main.__dict__[f'spacy_nlp_{lang}']

            with nlp.select_pipes(disable = [
                pipeline
                for pipeline in ['parser', 'lemmatizer', 'senter', 'sentencizer']
                if nlp.has_pipe(pipeline)
            ]):
                for doc in nlp.pipe(inputs.splitlines()):
                    if tagset in ['default', 'raw']:
                        tokens_tagged.extend([(token.text, token.tag_) for token in doc])
                    elif tagset == 'universal':
                        tokens_tagged.extend([(token.text, token.pos_) for token in doc])
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
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)
            nlp = main.__dict__[f'spacy_nlp_{lang}']

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
                        docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens)))

                for doc in nlp.pipe(docs):
                    if tagset in ['default', 'raw']:
                        tokens_tagged.extend([(token.text, token.tag_) for token in doc])
                    elif tagset == 'universal':
                        tokens_tagged.extend([(token.text, token.pos_) for token in doc])
        else:
            for tokens in wl_nlp_utils.split_token_list(main, inputs, pos_tagger):
                tokens_tagged.extend(wl_pos_tag_tokens(main, tokens, lang, pos_tagger))

    # Remove empty tokens (e.g. SudachiPy) and strip whitespace around tokens and tags
    tokens_tagged = [
        (token_clean, tag.strip())
        for token, tag in tokens_tagged
        if (token_clean := token.strip())
    ]

    # Make sure that tokenization is not modified during POS tagging
    if not isinstance(inputs, str):
        i_tokens = 0
        i_tokens_tagged = 0

        len_tokens = len(inputs)
        len_tokens_tagged = len(tokens_tagged)

        if len_tokens != len_tokens_tagged:
            tokens_tagged_modified = []

            while i_tokens < len_tokens and i_tokens_tagged < len_tokens_tagged:
                # Different token
                if len(inputs[i_tokens]) != len(tokens_tagged[i_tokens_tagged][0]):
                    tokens_temp = [inputs[i_tokens]]
                    tokens_tagged_temp = [tokens_tagged[i_tokens_tagged][0]]
                    tags_temp = [tokens_tagged[i_tokens_tagged][1]]

                    # Align tokens
                    while i_tokens < len_tokens - 1 or i_tokens_tagged < len_tokens_tagged - 1:
                        if lang in ['zho_cn', 'zho_tw', 'khm', 'jpn', 'kor', 'tha', 'bod']:
                            len_tokens_temp = sum((len(token) for token in tokens_temp))
                            len_tokens_tagged_temp = sum((len(token) for token in tokens_tagged_temp))
                        else:
                            # Compare length in characters with whitespace
                            len_tokens_temp = len(' '.join(tokens_temp))
                            len_tokens_tagged_temp = len(' '.join(tokens_tagged_temp))

                        if len_tokens_temp > len_tokens_tagged_temp:
                            tokens_tagged_temp.append(tokens_tagged[i_tokens_tagged + 1][0])
                            tags_temp.append(tokens_tagged[i_tokens_tagged + 1][1])

                            i_tokens_tagged += 1
                        elif len_tokens_temp < len_tokens_tagged_temp:
                            tokens_temp.append(inputs[i_tokens + 1])

                            i_tokens += 1
                        else:
                            len_tokens_temp_tokens = len(tokens_temp)
                            len_tokens_tagged_temp_tokens = len(tokens_tagged_temp)

                            if len_tokens_temp_tokens > len_tokens_tagged_temp_tokens:
                                tags_temp.extend([tags_temp[-1]] * (len_tokens_temp_tokens - len_tokens_tagged_temp_tokens))
                            elif len_tokens_temp_tokens < len_tokens_tagged_temp_tokens:
                                tags_temp = tags_temp[:len_tokens_temp_tokens]

                            tokens_tagged_modified.extend(list(zip(tokens_temp, tags_temp)))

                            tokens_temp = []
                            tokens_tagged_temp = []
                            tags_temp = []

                            break

                    if tokens_temp:
                        len_tokens_temp_tokens = len(tokens_temp)
                        len_tokens_tagged_temp_tokens = len(tokens_tagged_temp)

                        if len_tokens_temp_tokens > len_tokens_tagged_temp_tokens:
                            tags_temp.extend([tags_temp[-1]] * (len_tokens_temp_tokens - len_tokens_tagged_temp_tokens))
                        elif len_tokens_temp_tokens < len_tokens_tagged_temp_tokens:
                            tags_temp = tags_temp[:len_tokens_temp_tokens]

                        tokens_tagged_modified.extend(list(zip(tokens_temp, tags_temp)))
                else:
                    tokens_tagged_modified.append((inputs[i_tokens], tokens_tagged[i_tokens_tagged][1]))

                i_tokens += 1
                i_tokens_tagged += 1

            len_tokens_tagged_modified = len(tokens_tagged_modified)

            if len_tokens < len_tokens_tagged_modified:
                tokens_tagged = tokens_tagged_modified[:len_tokens]
            elif len_tokens > len_tokens_tagged_modified:
                tokens_tagged = tokens_tagged_modified + [tokens_tagged_modified[-1]] * (len_tokens - len_tokens_tagged_modified)
            else:
                tokens_tagged = tokens_tagged_modified.copy()
        else:
            tokens_tagged = [(token, token_tagged[1]) for token, token_tagged in zip(inputs, tokens_tagged)]

        # Insert empty tokens after alignment of input and output
        for empty_offset in sorted(empty_offsets):
            tokens_tagged.insert(empty_offset, ('', ''))

    # Convert to Universal Tagset
    if not pos_tagger.startswith('spacy_') and tagset == 'universal':
        mappings = {
            tag: tag_universal
            for tag, tag_universal, _, _ in main.settings_custom['pos_tagging']['tagsets']['mapping_settings'][lang][pos_tagger]
        }
        tokens_tagged = list(tokens_tagged)

        # Issue warnings if any tag is missing from the mapping table
        for _, tag in tokens_tagged:
            if tag not in mappings:
                print(f'Warning: tag "{tag}" is missing from the {wl_conversion.to_lang_text(main, lang)} mapping table!')

        tokens_tagged = [
            (token, mappings.get(tag, 'X'))
            for token, tag in tokens_tagged
        ]

    return tokens_tagged

def wl_pos_tag_text(main, text, lang, pos_tagger):
    tokens_tagged = []

    # Chinese
    if pos_tagger == 'jieba_zho':
        tokens_tagged = jieba.posseg.cut(text)
    # English & Russian
    elif pos_tagger.startswith('nltk_perceptron_'):
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

    # Chinese
    if pos_tagger == 'jieba_zho':
        tokens_tagged = jieba.posseg.cut(''.join(tokens))
    # English & Russian
    elif pos_tagger.startswith('nltk_perceptron_'):
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
