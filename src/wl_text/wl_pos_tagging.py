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

from wl_text import wl_text_utils, wl_word_detokenization
from wl_utils import wl_conversion

def wl_pos_tag(main, tokens, lang, pos_tagger = 'default', tagset = 'default'):
    tokens_tagged = []

    # Check if the first token is empty
    if tokens and tokens[0] == '':
        first_token_empty = True
    else:
        first_token_empty = False

    tokens = [str(token) for token in tokens if token]

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

    # spaCy
    if 'spacy' in pos_tagger:
        # Chinese, English, German, Portuguese
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens))
          
        for pipe_name in nlp.pipe_names:
            nlp.get_pipe(pipe_name)(doc)
        
        if tagset == 'default':
            tokens_tagged = [(token.text, token.tag_) for token in doc]
        elif tagset == 'universal':
            tokens_tagged = [(token.text, token.pos_) for token in doc]
    # Chinese
    elif pos_tagger == 'jieba_zho':
        tokens_tagged = jieba.posseg.cut(' '.join(tokens))
    # English & Russian
    elif pos_tagger == 'nltk_perceptron':
        lang_codes = {
            'eng_gb': 'eng',
            'eng_us': 'eng',
            'rus': 'rus'
        }

        tokens_tagged = nltk.pos_tag(tokens, lang = lang_codes[lang])
    # Japanese
    elif pos_tagger == 'nagisa_jpn':
        import nagisa

        tokens_tagged = zip(tokens, nagisa.postagging(tokens))
    elif pos_tagger == 'sudachipy_jpn':
        tokens_tagged = [
            (token.surface(), '-'.join([pos for pos in token.part_of_speech()[:4] if pos != '*']))
            for token in main.sudachipy_word_tokenizer.tokenize(' '.join(tokens))
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
        tokens = main.botok_word_tokenizer.tokenize(' '.join(tokens))

        for token in tokens:
            if token.pos:
                tokens_tagged.append((token.text, token.pos))
            else:
                tokens_tagged.append((token.text, token.chunk_type))
    # Vietnamese
    elif pos_tagger == 'underthesea_vie':
        tokens_tagged = underthesea.pos_tag(' '.join(tokens))

    # Convert to Universal Tagset
    if 'spacy' not in pos_tagger:
        if (tagset == 'default' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
            tagset == 'universal'):

            mappings = {tag: tag_universal
                        for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang][pos_tagger]}
            tokens_tagged = list(tokens_tagged)

            # Issue warnings if any tag is missing from the mapping table
            for _, tag in tokens_tagged:
                if tag not in mappings:
                    print(f'Warning: tag "{tag}" is missing from the {wl_conversion.to_lang_text(main, lang)} mapping table!')

            tokens_tagged = [
                (token, mappings.get(tag, 'X'))
                for token, tag in tokens_tagged
            ]

    # Strip empty tokens and strip whitespace in tokens
    tokens_tagged = [
        (token.strip(), tag)
        for token, tag in tokens_tagged
        if token.strip()
    ]

    # Add the first empty token (if any)
    if first_token_empty:
        tokens_tagged.insert(0, ('', ''))

    return tokens_tagged
