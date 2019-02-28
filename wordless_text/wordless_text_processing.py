#
# Wordless: Text - Text Processing
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import importlib
import itertools
import json
import re

import jieba
import jieba.posseg
import nltk
import nltk.tokenize.nist
import pymorphy2
import pythainlp
import sacremoses
import spacy
import underthesea

from wordless_checking import wordless_checking_unicode
from wordless_text import wordless_matching, wordless_text, wordless_text_utils
from wordless_utils import wordless_conversion

def wordless_sentence_tokenize(main, text, lang,
                               sentence_tokenizer = 'default'):
    sentences = []

    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    if sentence_tokenizer == main.tr('NLTK - Punkt Sentence Tokenizer'):
        lang_texts = {
            'ces': 'czech',
            'dan': 'danish',
            'nld': 'dutch',
            'eng': 'english',
            'est': 'estonian',
            'fin': 'finnish',
            'fra': 'french',
            'deu': 'german',
            # Greek (Modern)
            'ell': 'greek',
            'ita': 'italian',
            # Norwegian Bokmål & Norwegian Nynorsk
            'nob': 'norwegian',
            'nno': 'norwegian',
            'pol': 'polish',
            'por': 'portuguese',
            'slv': 'slovene',
            'spa': 'spanish',
            'swe': 'swedish',
            'tur': 'turkish',
            # Other Languages
            'other': 'english'
        }

        sentences = nltk.sent_tokenize(text, language = lang_texts[lang])
    elif 'spaCy' in sentence_tokenizer:
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        sentences = [sentence.text for sentence in nlp(text).sents]
    # Chinese & Japanese
    elif (sentence_tokenizer == main.tr('Wordless - Chinese Sentence Tokenizer') or
          sentence_tokenizer == main.tr('Wordless - Japanese Sentence Tokenizer')):
        for line in text.splitlines():
            sentence_start = 0

            for i, char in enumerate(line):
                if i >= sentence_start and char in ['。', '！', '？', '!', '?']:
                    for j, char in enumerate(line):
                        if j > i and char not in ['。', '！', '？', '!', '?', '’', '”', '）', ')']:
                            sentences.append(line[sentence_start : j])

                            sentence_start = j

                            break

            if sentence_start <= len(line):
                sentences.append(line[sentence_start:])
    # Thai
    elif sentence_tokenizer == 'PyThaiNLP - Thai Sentence Tokenizer':
        sentences = pythainlp.tokenize.sent_tokenize(text)
    # Tibetan
    elif sentence_tokenizer == 'Wordless - Tibetan Sentence Tokenizer':
        sentences = text.split()
    # Vietnamese
    elif sentence_tokenizer == 'Underthesea - Vietnamese Sentence Tokenizer':
        sentences = underthesea.sent_tokenize(text)

    sentences = wordless_text_utils.record_boundary_sentences(sentences, text)

    return sentences

def wordless_word_tokenize(main, text, lang,
                           word_tokenizer = 'default',
                           keep_sentences = False):
    tokens_sentences = []

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    if 'NLTK' in word_tokenizer:
        sentences = wordless_sentence_tokenize(main, text, lang,
                                               sentence_tokenizer = main.tr('NLTK - Punkt Sentence Tokenizer'))

        if word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
            treebank_tokenizer = nltk.TreebankWordTokenizer()

            for sentence in sentences:
                tokens_sentences.append(treebank_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
            tweet_tokenizer = nltk.TweetTokenizer()

            for sentence in sentences:
                tokens_sentences.append(tweet_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
            nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()

            for sentence in sentences:
                tokens_sentences.append(nist_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
            toktok_tokenizer = nltk.ToktokTokenizer()

            for sentence in sentences:
                tokens_sentences.append(toktok_tokenizer.tokenize(sentence))

        if not keep_sentences:
            tokens_sentences = [itertools.chain.from_iterable(tokens_sentences)]
    elif 'SacreMoses' in word_tokenizer:
        if keep_sentences:
            sentences = wordless_sentence_tokenize(main, text, lang)
        else:
            sentences = [text]

        if word_tokenizer == main.tr('SacreMoses - Moses Tokenizer'):
            moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

            for sentence in sentences:
                tokens_sentences.append(moses_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('SacreMoses - Penn Treebank Tokenizer'):
            moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

            for sentence in sentences:
                tokens_sentences.append(moses_tokenizer.penn_tokenize(sentence))
    elif 'spaCy' in word_tokenizer:
        # Other Languages
        if lang == 'other':
            lang = 'eng'

        # Languages with models
        if lang in ['nld', 'eng', 'fra', 'deu', 'ell', 'ita', 'por', 'spa']:
            nlp = main.__dict__[f'spacy_nlp_{lang}']
        # Languages without models
        else:
            nlp = spacy.blank(wordless_conversion.to_iso_639_1(main, lang))

        doc = nlp(text)

        if keep_sentences:
            for sentence in doc.sents:
                tokens_sentences.append([token.text for token in sentence.as_doc()])
        else:
            tokens_sentences.append([token.text for token in doc])

    # Chinese & Japanese
    elif ('jieba' in word_tokenizer or
          'nagisa' in word_tokenizer or
          'Wordless' in word_tokenizer):
        if keep_sentences:
            sentences = wordless_sentence_tokenize(main, text, lang = lang)
        else:
            sentences = [text]

        # Chinese
        if word_tokenizer == main.tr('jieba - Chinese Word Tokenizer'):
            for sentence in sentences:
                tokens_sentences.append(jieba.cut(sentence))
        elif word_tokenizer == main.tr('Wordless - Chinese Character Tokenizer'):
            for sentence in sentences:
                tokens = []
                non_han_start = 0

                for i, char in enumerate(sentence):
                    if i >= non_han_start:
                        if wordless_checking_unicode.is_han(char):
                            tokens.append(char)

                            non_han_start += 1
                        else:
                            # English
                            if wordless_checking_unicode.is_eng(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wordless_checking_unicode.is_eng(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'eng'))

                                        non_han_start = i + j + 1

                                        break
                            # Other Languages
                            else:
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or wordless_checking_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'other'))

                                        non_han_start = i + j + 1

                                        break

                tokens_sentences.extend(tokens)
        # Japanese
        elif word_tokenizer == main.tr('nagisa - Japanese Word Tokenizer'):
            import nagisa

            for sentence in sentences:
                tokens_sentences.append(nagisa.tagging(str(sentence)).words)
        elif word_tokenizer == main.tr('Wordless - Japanese Kanji Tokenizer'):
            for sentence in sentences:
                tokens = []
                non_han_start = 0

                for i, char in enumerate(sentence):
                    if i >= non_han_start:
                        if wordless_checking_unicode.is_han(char):
                            tokens.append(char)

                            non_han_start += 1
                        else:
                            # Japanese Kana
                            if wordless_checking_unicode.is_kana(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wordless_checking_unicode.is_kana(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'jpn'))

                                        non_han_start = i + j + 1

                                        break
                            # English
                            elif wordless_checking_unicode.is_eng(char):
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or not wordless_checking_unicode.is_eng(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'eng'))

                                        non_han_start = i + j + 1

                                        break
                            # Other Languages
                            else:
                                for j, char in enumerate(sentence[i:]):
                                    if i + j + 1 == len(sentence) or wordless_checking_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang = 'other'))

                                        non_han_start = i + j + 1

                                        break

                tokens_sentences.extend(tokens)
    # Thai
    elif 'PyThaiNLP' in word_tokenizer:
        sentences = wordless_sentence_tokenize(main, text, lang = 'tha',
                                                   sentence_tokenizer = 'PyThaiNLP - Thai Sentence Tokenizer')

        if word_tokenizer == main.tr('PyThaiNLP - Maximum Matching Algorithm + TCC'):
            for sentence in sentences:
                tokens_sentences.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'newmm'))
        elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching Algorithm'):
            for sentence in sentences:
                tokens_sentences.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'mm'))
        elif word_tokenizer == main.tr('PyThaiNLP - Longest Matching'):
            for sentence in sentences:
                tokens_sentences.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'longest-matching'))
    # Tibetan
    elif word_tokenizer == main.tr('pybo - Tibetan Word Tokenizer'):
        if keep_sentences:
            sentences = wordless_sentence_tokenize(main, text, lang = 'bod')
        else:
            sentences = [text]

        for sentence in sentences:
            tokens_sentences.append([token.content for token in main.pybo_bo_tokenizer.tokenize(sentence)])
    # Vietnamese
    elif word_tokenizer == main.tr('Underthesea - Vietnamese Word Tokenizer'):
        if keep_sentences:
            sentences = wordless_sentence_tokenize(main, text, lang = 'vie',
                                                   sentence_tokenizer = 'Underthesea - Vietnamese Sentence Tokenizer')
        else:
            sentences = [text]

        for sentence in sentences:
            tokens_sentences.append(underthesea.word_tokenize(str(sentence)))

    # Remove empty tokens and strip whitespace
    for i, tokens in enumerate(tokens_sentences):
        tokens_sentences[i] = [token.strip()
                               for token in tokens
                               if token.strip()]

    # Record token boundaries
    if lang in ['zho_cn', 'zho_tw', 'jpn']:
        for tokens in tokens_sentences:
            tokens[-1] = wordless_text.Wordless_Token(tokens[-1], boundary = '', sentence_ending = True)
    else:
        for tokens in tokens_sentences:
            tokens[-1] = wordless_text.Wordless_Token(tokens[-1], boundary = ' ', sentence_ending = True)

    return tokens_sentences

def wordless_word_detokenize(main, tokens, lang,
                             word_detokenizer = 'default'):
    sentence_start = 0
    sentences = []
    text = ''

    if lang not in main.settings_global['word_detokenizers']:
        lang = 'other'

    if word_detokenizer == 'default':
        word_detokenizer = main.settings_custom['word_detokenization']['word_detokenizers'][lang]

    for i, token in enumerate(tokens):
        if type(token) == wordless_text.Wordless_Token and token.sentence_ending:
            sentences.append(tokens[sentence_start : i + 1])

            sentence_start = i + 1
        elif i == len(tokens) - 1:
            sentences.append(tokens[sentence_start:])

    # English & Other Languages
    if word_detokenizer == main.tr('NLTK - Penn Treebank Detokenizer'):
        treebank_detokenizer = nltk.tokenize.treebank.TreebankWordDetokenizer()

        for sentence in sentences:
            text += treebank_detokenizer.tokenize(tokens)
    elif word_detokenizer == main.tr('SacreMoses - Moses Detokenizer'):
        moses_detokenizer = sacremoses.MosesDetokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

        for sentence in sentences:
            text += moses_detokenizer.detokenize(sentence)
    # Chinese
    elif word_detokenizer == main.tr('Wordless - Chinese Word Detokenizer'):
        non_cjk_start = 0

        for i, token in enumerate(tokens):
            if i >= non_cjk_start:
                if (wordless_checking_unicode.has_han(token) or
                    all(map(str.isnumeric, token))):
                    text += token

                    non_cjk_start += 1
                else:
                    # English
                    if wordless_checking_unicode.is_eng_token(token):
                        for j, token in enumerate(tokens[i:]):
                            if i + j + 1 == len(tokens) or not wordless_checking_unicode.is_eng_token(tokens[i + j + 1]):
                                text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                 lang = 'eng')

                                non_cjk_start = i + j + 1

                                break
                    # Other Languages
                    else:
                        for j, token in enumerate(tokens[i:]):
                            if (i + j + 1 == len(tokens) or
                                wordless_checking_unicode.has_han(tokens[i + j + 1])):
                                text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                 lang = 'other')

                                non_cjk_start = i + j + 1

                                break
    elif word_detokenizer == main.tr('Wordless - Japanese Word Detokenizer'):
        non_cjk_start = 0

        for i, token in enumerate(tokens):
            if i >= non_cjk_start:
                if (wordless_checking_unicode.has_han(token) or
                    wordless_checking_unicode.has_kana(token) or
                    all(map(str.isnumeric, token))):
                    text += token

                    non_cjk_start += 1
                else:
                    # English
                    if wordless_checking_unicode.is_eng_token(token):
                        for j, token in enumerate(tokens[i:]):
                            if i + j + 1 == len(tokens) or not wordless_checking_unicode.is_eng_token(tokens[i + j + 1]):
                                text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                 lang = 'eng')

                                non_cjk_start = i + j + 1

                                break
                    # Other Languages
                    else:
                        for j, token in enumerate(tokens[i:]):
                            if (i + j + 1 == len(tokens) or
                                wordless_checking_unicode.has_han(tokens[i + j + 1]) or
                                wordless_checking_unicode.has_kana(tokens[i + j + 1])):
                                text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                 lang = 'other')

                                non_cjk_start = i + j + 1

                                break
    # Thai
    elif word_detokenizer in main.tr('Wordless - Thai Word Detokenizer'):
        # Settings -> Detokenization -> Preview
        if type(tokens[0]) == str:
            text = ''.join(tokens)
        else:
            for token in tokens:
                if type(token) == wordless_text.Wordless_Token:
                    text += token.boundary
                else:
                    text += token
    # Tibetan
    elif word_detokenizer == main.tr('Wordless - Tibetan Word Detokenizer'):
        for i, token in enumerate(tokens):
            # Check for Tibetan Mark Shad
            # See: https://w3c.github.io/tlreq/#section_breaks
            if i > 0 and token[0] == '།':
                text += f' {token}'
            else:
                text += token

    return re.sub(r'\s{2,}', ' ', text)

def wordless_pos_tag(main, tokens, lang,
                     pos_tagger = 'default',
                     tagset = 'custom'):
    tokens_tagged = []

    tokens = [str(token) for token in tokens]

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

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
    elif pos_tagger == main.tr('pybo - Tibetan POS Tagger'):
        tokens_tagged = [(token.content, token.pos) for token in main.pybo_bo_tokenizer.tokenize(' '.join(tokens))]

    # Vietnamese
    elif pos_tagger == main.tr('Underthesea - Vietnamese POS Tagger'):
        tokens_tagged = underthesea.pos_tag(' '.join(tokens))

    # Convert to Universal Tagset
    if (tagset == 'custom' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
        tagset == 'universal'):

        mappings = {tag: tag_universal
                    for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang][pos_tagger]}

        tokens_tagged = [(token, mappings[tag])
                         for token, tag in tokens_tagged]

    # Strip empty tokens and strip whitespace in tokens
    tokens_tagged = [(token.strip(), tag)
                     for token, tag in tokens_tagged
                     if token.strip()]

    # Check if the first token is empty
    if tokens[0] == '':
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

    # Record empty tokens
    for i, token in reversed(list(enumerate(tokens))):
        if not token.strip():
            tokens.remove(token)

            empty_offsets.append(i)

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
            with open(r'lemmatization/lemmalist-greek/lemmalist-greek.txt', 'r', encoding = 'utf_8') as f:
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
        elif lemmatizer == main.tr('pybo - Tibetan Lemmatizer'):
            for token in main.pybo_bo_tokenizer.tokenize(' '.join(tokens)):
                if token.lemma:
                    lemmas.append(token.lemma)
                else:
                    lemmas.append(token.content)
        # Other Languages
        elif 'Lemmatization Lists' in lemmatizer:
            lang = wordless_conversion.to_iso_639_1(main, lang)

            with open(f'lemmatization/Lemmatization Lists/lemmatization-{lang}.txt', 'r', encoding = 'utf_8_sig') as f:
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
    for empty_offset in empty_offsets:
        lemmas.insert(empty_offset, '')

    return [lemma + tag for lemma, tag in zip(lemmas, tags)]

def wordless_get_stop_words(main, lang,
                            list_stop_words = 'default'):
    if list_stop_words == 'default':
        list_stop_words = main.settings_custom['stop_words']['stop_words'][lang]

    lang_639_1 = wordless_conversion.to_iso_639_1(main, lang)

    # Chinese (Simplified)
    if lang_639_1 == 'zh_cn':
        lang_639_1 = 'zh'

    if 'Stopwords ISO' in list_stop_words:
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang_639_1 in ['nb', 'nn']:
            lang_639_1 = 'no'

        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            with open(r'stop_words/Stopwords ISO/stop_words_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                stop_words = json.load(f)[lang_639_1]
    elif 'spaCy' in list_stop_words:
        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            with open(r'stop_words/spaCy/stop_words_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            spacy_stop_words = importlib.import_module(f'spacy.lang.{lang_639_1}.stop_words')

            stop_words = spacy_stop_words.STOP_WORDS
    elif 'NLTK' in list_stop_words:
        lang_texts = {
            'ara': 'arabic',
            'aze': 'azerbaijani',
            'dan': 'danish',
            'nld': 'dutch',
            'eng': 'english',
            'fin': 'finnish',
            'fra': 'french',
            'deu': 'german',
            'ell': 'greek',
            'hun': 'hungarian',
            'ind': 'indonesian',
            'ita': 'italian',
            'kaz': 'kazakh',
            'nep': 'nepali',
            # Norwegian Bokmål & Norwegian Nynorsk
            'nob': 'norwegian',
            'nno': 'norwegian',
            'por': 'portuguese',
            'ron': 'romanian',
            'rus': 'russian',
            'spa': 'spanish',
            'swe': 'swedish',
            'tur': 'turkish'
        }

        stop_words = nltk.corpus.stopwords.words(lang_texts[lang])
    # Greek (Ancient)
    elif list_stop_words == main.tr('grk-stoplist - Greek (Ancient) Stop Words'):
        with open(r'stop_words/grk-stoplist/stoplist-greek.txt', 'r', encoding = 'utf_8') as f:
            stop_words = [line.rstrip() for line in f.readlines()]
    # Thai
    elif list_stop_words == main.tr('PyThaiNLP - Thai Stop Words'):
        stop_words = pythainlp.corpus.stopwords.words('thai')
    # Custom Lists
    elif list_stop_words == main.tr('Custom List'):
        stop_words = main.settings_custom['stop_words']['custom_lists'][lang]

    return sorted(stop_words)

def wordless_filter_stop_words(main, items, lang):
    if lang not in main.settings_global['stop_words']:
        lang == 'other'

    stop_words = wordless_get_stop_words(main, lang)

    if type(items[0]) == str:
        items_filtered = [token for token in items if token not in stop_words]
    elif type(items[0]) in [list, tuple, set]:
        items_filtered = [ngram
                          for ngram in items
                          if not [token for token in ngram if token in stop_words]]

    return items_filtered
