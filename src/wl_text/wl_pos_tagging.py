#
# Wordless: Text - POS Tagging
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import jieba.posseg
import nltk
import pythainlp
import spacy
import underthesea

from wl_text import wl_text_utils, wl_word_detokenization, wl_word_tokenization
from wl_utils import wl_conversion

def wl_pos_tag(main, inputs, lang, pos_tagger = 'default', tagset = 'default'):
    tokens_tagged = []

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    wl_text_utils.init_word_tokenizers(
        main,
        lang = lang
    )
    wl_text_utils.init_pos_taggers(
        main,
        lang = lang,
        pos_tagger = pos_tagger
    )

    # Untokenized
    if type(inputs) == str:
        # Input of SudachiPy cannot be more than 49149 bytes
        if lang == 'jpn' and pos_tagger in ['spacy_jpn', 'sudachipy_jpn'] and len(inputs) > 49149 // 4:
            texts = re.split(r'\n(?=.|\n)', inputs)
        else:
            texts = [inputs]

        for text in texts:
            tokens_tagged.extend(wl_pos_tag_text(main, text, lang, pos_tagger, tagset))
    # Tokenized
    else:
        # Check if the first token is empty
        if inputs and inputs[0] == '':
            first_token_empty = True
        else:
            first_token_empty = False

        inputs = [str(token) for token in inputs if token]

        # Input of SudachiPy cannot be more than 49149 bytes
        if lang == 'jpn' and pos_tagger in ['spacy_jpn', 'sudachipy_jpn']:
            texts = wl_text_utils.to_sections_unequal(inputs, 4000)
        else:
            texts = [inputs]

        for tokens in texts:
            tokens_tagged.extend(wl_pos_tag_tokens(main, tokens, lang, pos_tagger, tagset))

    # Convert to Universal Tagset
    if not pos_tagger.startswith('spacy_'):
        if (tagset == 'default' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
            tagset == 'universal'):

            mappings = {
                tag: tag_universal
                for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang][pos_tagger]
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

    # Add the first empty token (if any)
    if type(inputs) != str and first_token_empty:
        tokens_tagged.insert(0, ('', ''))

    return tokens_tagged

def wl_pos_tag_text(main, text, lang, pos_tagger, tagset):
    tokens_tagged = []

    if pos_tagger == 'nagisa_jpn':
        # Defer import to save loading time
        import nagisa

    # spaCy
    if pos_tagger.startswith('spacy_'):
        if not lang.startswith('srp_'):
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)
        
        if tagset == 'default':
            tokens_tagged = [(token.text, token.tag_) for token in doc]
        elif tagset == 'universal':
            tokens_tagged = [(token.text, token.pos_) for token in doc]
    # Chinese
    elif pos_tagger == 'jieba_zho':
        tokens_tagged = jieba.posseg.cut(text)
    # English & Russian
    elif pos_tagger == 'nltk_perceptron':
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)
        tokens_tagged = nltk.pos_tag(tokens, lang = lang)
    # Japanese
    elif pos_tagger == 'nagisa_jpn':
        tokens_tagged = nagisa.tagging(text)
        tokens_tagged = zip(tokens_tagged.words, tokens_tagged.postags)
    elif pos_tagger == 'sudachipy_jpn':
        tokens_tagged = [
            (token.surface(), '-'.join([pos for pos in token.part_of_speech()[:4] if pos != '*']))
            for token in main.sudachipy_word_tokenizer.tokenize(text)
        ]
    # Russian & Ukrainian
    elif pos_tagger == 'pymorphy2_morphological_analyzer':
        if lang == 'rus':
            morphological_analyzer = main.pymorphy2_morphological_analyzer_rus
        elif lang == 'ukr':
            morphological_analyzer = main.pymorphy2_morphological_analyzer_ukr

        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

        for token in tokens:
            tokens_tagged.append((token, morphological_analyzer.parse(token)[0].tag._POS))
    # Thai
    elif pos_tagger.startswith('pythainlp_'):
        tokens = wl_word_tokenization.wl_word_tokenize_flat(main, text, lang = lang)

        if pos_tagger == 'pythainlp_perceptron_lst20':
            tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'lst20')
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

    # Remove empty tokens and strip whitespace in tokens
    tokens_tagged = [
        (str(token).strip(), tag)
        for token, tag in tokens_tagged
        if str(token).strip()
    ]

    return tokens_tagged

def wl_pos_tag_tokens(main, tokens, lang, pos_tagger, tagset):
    tokens_tagged = []

    if pos_tagger == 'nagisa_jpn':
        # Defer import to save loading time
        import nagisa

    lang = wl_conversion.remove_lang_code_suffixes(main, lang)

    # spaCy
    if pos_tagger.startswith('spacy_'):
        if not lang.startswith('srp_'):
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'spacy_nlp_{lang}']

        if lang != 'jpn':
            doc = spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens))
            
            for pipe_name in nlp.pipe_names:
                nlp.get_pipe(pipe_name)(doc)
        # The Japanese model do not have a tagger component and Japanese POS tags are taken directly from SudachiPy
        # See: https://github.com/explosion/spaCy/discussions/9983#discussioncomment-1910117
        else:
            doc = nlp(''.join(tokens))

        if tagset == 'default':
            tokens_tagged = [(token.text, token.tag_) for token in doc]
        elif tagset == 'universal':
            tokens_tagged = [(token.text, token.pos_) for token in doc]
    # Chinese
    elif pos_tagger == 'jieba_zho':
        tokens_tagged = jieba.posseg.cut(''.join(tokens))
    # English & Russian
    elif pos_tagger == 'nltk_perceptron':
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        tokens_tagged = nltk.pos_tag(tokens, lang = lang)
    # Japanese
    elif pos_tagger == 'nagisa_jpn':
        tokens_tagged = zip(tokens, nagisa.postagging(tokens))
    elif pos_tagger == 'sudachipy_jpn':
        tokens_tagged = [
            (token.surface(), '-'.join([pos for pos in token.part_of_speech()[:4] if pos != '*']))
            for token in main.sudachipy_word_tokenizer.tokenize(''.join(tokens))
        ]
    # Russian & Ukrainian
    elif pos_tagger == 'pymorphy2_morphological_analyzer':
        if lang == 'rus':
            morphological_analyzer = main.pymorphy2_morphological_analyzer_rus
        elif lang == 'ukr':
            morphological_analyzer = main.pymorphy2_morphological_analyzer_ukr

        for token in tokens:
            tokens_tagged.append((token, morphological_analyzer.parse(token)[0].tag._POS))
    # Thai
    elif pos_tagger == 'pythainlp_perceptron_lst20':
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'lst20')
    elif pos_tagger == 'pythainlp_perceptron_orchid':
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
    elif pos_tagger == 'pythainlp_perceptron_pud':
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')
    # Tibetan
    elif pos_tagger == 'botok_bod':
        tokens = main.botok_word_tokenizer.tokenize(''.join(tokens))

        for token in tokens:
            if token.pos:
                tokens_tagged.append((token.text, token.pos))
            else:
                tokens_tagged.append((token.text, token.chunk_type))
    # Vietnamese
    elif pos_tagger == 'underthesea_vie':
        tokens_tagged = underthesea.pos_tag(' '.join(tokens))

    # Remove empty tokens and strip whitespace in tokens
    tokens_tagged = [
        (str(token).strip(), tag)
        for token, tag in tokens_tagged
        if str(token).strip()
    ]

    # Make sure that tokenization is not modified during POS tagging
    i_tokens = 0
    i_tokens_tagged = 0

    len_tokens = len(tokens)
    len_tokens_tagged = len(tokens_tagged)

    if len_tokens != len_tokens_tagged:
        tokens_tagged_modified = []

        while i_tokens < len_tokens and i_tokens_tagged < len_tokens_tagged:
            if len(tokens[i_tokens]) != len(tokens_tagged[i_tokens_tagged][0]):
                tokens_temp = [tokens[i_tokens]]
                tokens_tagged_temp = [tokens_tagged[i_tokens_tagged][0]]
                tags_temp = [tokens_tagged[i_tokens_tagged][1]]

                while i_tokens < len_tokens and i_tokens_tagged < len_tokens_tagged:
                    len_tokens_temp = sum([len(token) for token in tokens_temp])
                    len_tokens_tagged_temp = sum([len(token) for token in tokens_tagged_temp])

                    if len_tokens_temp > len_tokens_tagged_temp:
                        tokens_tagged_temp.append(tokens_tagged[i_tokens_tagged + 1][0])
                        tags_temp.append(tokens_tagged[i_tokens_tagged + 1][1])

                        i_tokens_tagged += 1
                    elif len_tokens_temp < len_tokens_tagged_temp:
                        tokens_temp.append(tokens[i_tokens + 1])

                        i_tokens += 1
                    else:
                        if len(tokens_temp) == len(tokens_tagged_temp):
                            tokens_tagged_modified.extend([
                                (token, tag)
                                for token, tag in zip(tokens_temp, tags_temp)
                            ])
                        elif len(tokens_temp) > len(tokens_tagged_temp):
                            tokens_tagged_modified.extend([
                                (token, tags_temp[0])
                                for token in tokens_temp
                            ])
                        else:
                            tokens_tagged_modified.append((tokens_temp[0], tags_temp[0]))

                        tokens_temp = []
                        tokens_tagged_temp = []
                        tags_temp = []

                        break

                if tokens_temp:
                    if len(tokens_temp) == len(tokens_tagged_temp):
                        tokens_tagged_modified.extend([
                            (token, tag)
                            for token, tag in zip(tokens_temp, tags_temp)
                        ])
                    elif len(tokens_temp) > len(tokens_tagged_temp):
                        tokens_tagged_modified.extend([
                            (token, tags_temp[0])
                            for token in tokens_temp
                        ])
                    else:
                        tokens_tagged_modified.append((tokens_temp[0], tags_temp[0]))
            else:
                tokens_tagged_modified.append((tokens[i_tokens], tokens_tagged[i_tokens_tagged][1]))

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
        tokens_tagged = [(tokens[i], tokens_tagged[i][1]) for i in range(len(tokens))]

    return tokens_tagged
