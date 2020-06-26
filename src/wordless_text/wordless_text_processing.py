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
