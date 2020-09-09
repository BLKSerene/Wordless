#
# Wordless: Text - POS Tagging
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import jieba.posseg
import nltk
import pymorphy2
import pythainlp
import spacy
import underthesea

from wl_text import wl_text_utils
from wl_utils import wl_conversion

def wl_pos_tag(main, tokens, lang, pos_tagger = 'default', tagset = 'custom'):
    tokens_tagged = []

    # Check if the first token is empty
    if tokens and tokens[0] == '':
        first_token_empty = True
    else:
        first_token_empty = False

    tokens = [str(token) for token in tokens if token]

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    wl_text_utils.check_pos_taggers(
        main,
        lang = lang,
        pos_tagger = pos_tagger
    )

    # Chinese
    if pos_tagger == main.tr('jieba - Chinese POS Tagger'):
        tokens_tagged = jieba.posseg.cut(' '.join(tokens))

    # Dutch, English, French, German, Greek (Modern), Italian, Portuguese, Spanish
    elif 'spaCy' in pos_tagger:
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        doc = spacy.tokens.Doc(nlp.vocab, words = tokens)
        nlp.tagger(doc)

        if tagset == 'custom':
            tokens_tagged = [(token.text, token.tag_) for token in doc]
        elif tagset == 'universal':
            tokens_tagged = [(token.text, token.pos_) for token in doc]

    # English & Russian
    elif pos_tagger == main.tr('NLTK - Perceptron POS Tagger'):
        tokens_tagged = nltk.pos_tag(tokens, lang = lang)

    # Japanese
    elif pos_tagger == main.tr('nagisa - Japanese POS Tagger'):
        import nagisa

        tokens_tagged = zip(tokens, nagisa.postagging(tokens))

    # Russian & Ukrainian
    elif pos_tagger == main.tr('pymorphy2 - Morphological Analyzer'):
        if lang == 'rus':
            morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'uk')

        for token in tokens:
            tokens_tagged.append((token, morphological_analyzer.parse(token)[0].tag._POS))

    # Thai
    elif pos_tagger == main.tr('PyThaiNLP - Perceptron Tagger (ORCHID)'):
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
    elif pos_tagger == main.tr('PyThaiNLP - Perceptron Tagger (PUD)'):
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')

    # Tibetan
    elif pos_tagger == main.tr('botok - Tibetan POS Tagger'):
        wl_text_utils.check_word_tokenizers(main,
                                                  lang = 'bod')
        tokens = main.botok_word_tokenizer.tokenize(' '.join(tokens))

        for token in tokens:
            if token.pos:
                tokens_tagged.append((token.text, token.pos))
            else:
                tokens_tagged.append((token.text, token.chunk_type))

    # Vietnamese
    elif pos_tagger == main.tr('Underthesea - Vietnamese POS Tagger'):
        tokens_tagged = underthesea.pos_tag(' '.join(tokens))

    # Convert to Universal Tagset
    if pos_tagger.find('spaCy') == -1:
        if (tagset == 'custom' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
            tagset == 'universal'):

            mappings = {tag: tag_universal
                        for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang][pos_tagger]}
            tokens_tagged = list(tokens_tagged)

            # Issue warnings if any tag is missing from the mapping table
            for _, tag in tokens_tagged:
                if tag not in mappings:
                    print(f'Warning: tag "{tag}" is missing from the {wl_conversion.to_lang_text(main, lang)} mapping table!')

            tokens_tagged = [(token, mappings.get(tag, 'X'))
                             for token, tag in tokens_tagged]

    # Strip empty tokens and strip whitespace in tokens
    tokens_tagged = [(token.strip(), tag)
                     for token, tag in tokens_tagged
                     if token.strip()]

    # Add the first empty token (if any)
    if first_token_empty:
        tokens_tagged.insert(0, ('', ''))

    return tokens_tagged
