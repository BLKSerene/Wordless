#
# Wordless: Text - Lemmatization
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

import nltk
import spacy

from wl_text import wl_matching, wl_pos_tagging, wl_text_utils
from wl_utils import wl_conversion, wl_misc

def wl_lemmatize(main, tokens, lang, tokenized = 'No', tagged = 'No', lemmatizer = 'default'):
    empty_offsets = []
    mapping_lemmas = {}
    lemmas = []

    tokens = [str(token) for token in tokens]

    re_tags = wl_matching.get_re_tags(main)

    if tagged == 'Yes':
        tags = [''.join(re.findall(re_tags, token)) for token in tokens]
        tokens = [re.sub(re_tags, '', token) for token in tokens]
    else:
        tags = [''] * len(tokens)

    # Record empty tokens with their tags
    for i, token in reversed(list(enumerate(tokens))):
        if not token.strip():
            empty_offsets.append(i)

            del tokens[i]
            del tags[i]
    
    if tokens and lang in main.settings_global['lemmatizers']:
        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang]

        wl_text_utils.init_word_tokenizers(
            main,
            lang = lang
        )
        wl_text_utils.init_lemmatizers(
            main,
            lang = lang,
            lemmatizer = lemmatizer
        )

        # spaCy
        if 'spacy' in lemmatizer:
            # English, German, Portuguese
            if 'srp' not in lang:
                lang = wl_conversion.remove_lang_code_suffixes(main, lang)

            nlp = main.__dict__[f'spacy_nlp_{lang}']
            doc = spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens))

            for pipe_name in nlp.pipe_names:
                nlp.get_pipe(pipe_name)(doc)

            lemmas = [token.lemma_ for token in doc]
        # English
        elif lemmatizer == 'nltk_wordnet':
            word_net_lemmatizer = nltk.WordNetLemmatizer()

            for token, pos in wl_pos_tagging.wl_pos_tag(
                main, tokens,
                lang = 'eng_us',
                pos_tagger = 'nltk_perceptron',
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
            lemmas = [
                token.dictionary_form()
                for token in main.sudachipy_word_tokenizer.tokenize(''.join(tokens))
            ]
        # Russian & Ukrainian
        elif lemmatizer == 'pymorphy2_morphological_analyzer':
            if lang == 'rus':
                morphological_analyzer = main.pymorphy2_morphological_analyzer_rus
            elif lang == 'ukr':
                morphological_analyzer = main.pymorphy2_morphological_analyzer_ukr

            for token in tokens:
                lemmas.append(morphological_analyzer.parse(token)[0].normal_form)
        # Tibetan
        elif lemmatizer == 'botok_bod':
            tokens = main.botok_word_tokenizer.tokenize(' '.join(tokens))

            for token in tokens:
                if token.lemma:
                    lemmas.append(token.lemma)
                else:
                    lemmas.append(token.text)
        # Other Languages
        elif 'lemmatization_lists' in lemmatizer:
            lang = wl_conversion.to_iso_639_1(main, lang)
            # English, German, Portuguese
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

            with open(wl_misc.get_normalized_path(f'lemmatization/Lemmatization Lists/lemmatization-{lang}.txt'), 'r', encoding = 'utf_8_sig') as f:
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

    # Insert empty lemmas with their tags
    for empty_offset in sorted(empty_offsets):
        lemmas.insert(empty_offset, '')
        tags.insert(empty_offset, '')

    return [lemma + tag for lemma, tag in zip(lemmas, tags)]
