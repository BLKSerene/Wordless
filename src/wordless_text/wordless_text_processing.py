#
# Wordless: Text - Text Processing
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import importlib
import json
import re

import botok
import jieba
import jieba.posseg
import nltk
import nltk.tokenize.nist
import pymorphy2
import pythainlp
import razdel
import sacremoses
import spacy
import syntok.segmenter
import underthesea

from wordless_checking import wordless_checking_token, wordless_checking_unicode
from wordless_text import wordless_matching, wordless_text, wordless_text_utils
from wordless_utils import wordless_conversion, wordless_misc

def wordless_pos_tag(main, tokens, lang,
                     pos_tagger = 'default',
                     tagset = 'custom'):
    tokens_tagged = []

    # Check if the first token is empty
    if tokens and tokens[0] == '':
        first_token_empty = True
    else:
        first_token_empty = False

    tokens = [str(token) for token in tokens if token]

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    wordless_text_utils.check_pos_taggers(main,
                                          lang = lang,
                                          pos_tagger = pos_tagger)

    # Chinese
    if pos_tagger == main.tr('jieba - Chinese POS Tagger'):
        tokens_tagged = jieba.posseg.cut(' '.join(tokens))

    # Dutch, English, French, German, Greek (Modern), Italian, Portuguese, Spanish
    elif 'spaCy' in pos_tagger:
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        doc = spacy.tokens.Doc(nlp.vocab, words = tokens)
        nlp.tagger(doc)

        tokens_tagged = [(token.text, token.tag_) for token in doc]

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
    elif pos_tagger == main.tr('PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus'):
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid')
    elif pos_tagger == main.tr('PyThaiNLP - Perceptron POS Tagger - PUD Corpus'):
        tokens_tagged = pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud')

    # Tibetan
    elif pos_tagger == main.tr('botok - Tibetan POS Tagger'):
        wordless_text_utils.check_word_tokenizers(main,
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
    if (tagset == 'custom' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
        tagset == 'universal'):

        mappings = {tag: tag_universal
                    for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang][pos_tagger]}
        tokens_tagged = list(tokens_tagged)

        # Issue warnings if any tag is missing from the mapping table
        for _, tag in tokens_tagged:
            if tag not in mappings:
                print(f'Warning: tag "{tag}" is missing from the {wordless_conversion.to_lang_text(main, lang)} mapping table!')

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

def wordless_lemmatize(main, tokens, lang,
                       text_type = ('untokenized', 'untagged'),
                       lemmatizer = 'default'):
    empty_offsets = []
    mapping_lemmas = {}
    lemmas = []

    tokens = [str(token) for token in tokens]

    re_tags_all = wordless_matching.get_re_tags(main, tags = 'all')
    re_tags_pos = wordless_matching.get_re_tags(main, tags = 'pos')
    re_tags_non_pos = wordless_matching.get_re_tags(main, tags = 'non_pos')

    if text_type[1] == 'tagged_both':
        tags = [''.join(re.findall(re_tags_all, token)) for token in tokens]
        tokens = [re.sub(re_tags_all, '', token) for token in tokens]
    elif text_type[1] == 'tagged_pos':
        tags = [''.join(re.findall(re_tags_pos, token)) for token in tokens]
        tokens = [re.sub(re_tags_pos, '', token) for token in tokens]
    elif text_type[1] == 'tagged_non_pos':
        tags = [''.join(re.findall(re_tags_non_pos, token)) for token in tokens]
        tokens = [re.sub(re_tags_non_pos, '', token) for token in tokens]
    else:
        tags = [''] * len(tokens)

    # Record empty tokens
    for i, token in reversed(list(enumerate(tokens))):
        if not token.strip():
            empty_offsets.append(i)

            tokens.remove(token)

    wordless_text_utils.check_lemmatizers(main, lang)

    if tokens and lang in main.settings_global['lemmatizers']:
        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang]

        # Dutch, English, French, German, Greek (Modern), Italian, Portuguese, Spanish
        if 'spaCy' in lemmatizer:
            nlp = main.__dict__[f'spacy_nlp_{lang}']

            doc = spacy.tokens.Doc(nlp.vocab, words = tokens)
            nlp.tagger(doc)

            lemmas = [token.lemma_ for token in doc]
        # English
        elif lemmatizer == main.tr('NLTK - WordNet Lemmatizer'):
            word_net_lemmatizer = nltk.WordNetLemmatizer()

            for token, pos in wordless_pos_tag(main, tokens,
                                               lang = 'eng',
                                               pos_tagger = 'NLTK - Perceptron POS Tagger',
                                               tagset = 'universal'):
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
        # Greek (Ancient)
        elif lemmatizer == main.tr('lemmalist-greek - Greek (Ancient) Lemma List'):
            with open(wordless_misc.get_normalized_path('lemmatization/lemmalist-greek/lemmalist-greek.txt'), 'r', encoding = 'utf_8') as f:
                for line in f.readlines():
                    line = line.rstrip()

                    if line:
                        lemma, *words = line.split()

                        for word in words:
                            mapping_lemmas[word] = lemma
        # Russian & Ukrainian
        elif lemmatizer == main.tr('pymorphy2 - Morphological Analyzer'):
            if lang == 'rus':
                morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'ru')
            else:
                morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'uk')

            for token in tokens:
                lemmas.append(morphological_analyzer.parse(token)[0].normal_form)
        # Tibetan
        elif lemmatizer == main.tr('botok - Tibetan Lemmatizer'):
            wordless_text_utils.check_word_tokenizers(main,
                                                      lang = 'bod')
            tokens = main.botok_word_tokenizer.tokenize(' '.join(tokens))

            for token in tokens:
                if token.lemma:
                    lemmas.append(token.lemma)
                else:
                    lemmas.append(token.text)
        # Other Languages
        elif 'Lemmatization Lists' in lemmatizer:
            lang = wordless_conversion.to_iso_639_1(main, lang)

            with open(wordless_misc.get_normalized_path(f'lemmatization/Lemmatization Lists/lemmatization-{lang}.txt'), 'r', encoding = 'utf_8_sig') as f:
                for line in f:
                    try:
                        lemma, word = line.rstrip().split('\t')

                        mapping_lemmas[word] = lemma
                    except:
                        pass
    else:
        lemmas = tokens

    if mapping_lemmas:
        lemmas = [mapping_lemmas.get(token, token) for token in tokens]

    # Insert empty lemmas
    for empty_offset in sorted(empty_offsets):
        lemmas.insert(empty_offset, '')

    return [lemma + tag for lemma, tag in zip(lemmas, tags)]
