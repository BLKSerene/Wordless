#
# Wordless: Text Processing
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import importlib
import json
import re

import jieba
import jieba.posseg
import nltk
import nltk.tokenize.nist
import pybo
import pymorphy2
import pythainlp
import sacremoses
import spacy
import underthesea

from wordless_text import wordless_text
from wordless_utils import wordless_conversion, wordless_unicode

def check_spacy_models(main, lang_code):
    if f'spacy_nlp_{lang_code}' not in main.__dict__:
        # Dutch
        if lang_code == 'nld':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('nl_core_news_sm')
        # English
        elif lang_code == 'eng':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('en_core_web_sm')
        # French
        elif lang_code == 'fra':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('fr_core_news_sm')
        # German
        elif lang_code == 'deu':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('de_core_news_sm')
        # Italian
        elif lang_code == 'ita':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('it_core_news_sm')
        # Portuguese
        elif lang_code == 'por':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('pt_core_news_sm')
        # Spanish
        elif lang_code == 'spa':
            main.__dict__[f'spacy_nlp_{lang_code}'] = spacy.load('es_core_news_sm')

def wordless_sentence_tokenize(main, text, lang_code, sentence_tokenizer = 'default'):
    sentences = []
    boundary_start = 0

    if lang_code not in main.settings_global['sentence_tokenizers']:
        lang_code = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang_code]

    # English
    if sentence_tokenizer == main.tr('NLTK - Punkt Sentence Tokenizer'):
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang_code in ['nob', 'nno']:
            lang_text = 'norwegian'
        # Other Languages
        elif lang_code == 'other':
            lang_text = 'english'
        else:
            lang_text = wordless_conversion.to_lang_text(main, lang_code).lower()

        for line in text.splitlines():
            sentences.extend(nltk.sent_tokenize(line, language = lang_text))
    elif 'spaCy' in sentence_tokenizer:
        check_spacy_models(main, lang_code)

        nlp = main.__dict__[f'spacy_nlp_{lang_code}']

        for line in text.splitlines():
            sentences.extend([sentence.text for sentence in nlp(line).sents])

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
        for line in text.splitlines():
            sentences.extend(pythainlp.tokenize.sent_tokenize(line))

    # Vietnamese
    elif sentence_tokenizer == 'Underthesea - Vietnamese Sentence Tokenizer':
        for line in text.splitlines():
            sentences.extend(underthesea.sent_tokenize(line))

    # Strip whitespace characters
    sentences = [sentence.strip() for sentence in sentences]

    # Record sentence boundaries
    text = text.replace('\n', '')

    for i, sentence in enumerate(sentences):
        boundary = re.search(r'^\s+', text[boundary_start + len(sentence):])

        if boundary == None:
            boundary = ''
        else:
            boundary = boundary.group()

        sentences[i] = wordless_text.Wordless_Token(sentences[i], boundary = boundary)

        boundary_start += len(sentence) + len(boundary)

    return sentences

def wordless_word_tokenize(main, sentences, lang_code, word_tokenizer = 'default'):
    token_groups = []

    if type(sentences) != list:
        sentences = [sentences]

    for i, sentence in enumerate(sentences):
        if type(sentence) != wordless_text.Wordless_Token:
            sentences[i] = wordless_text.Wordless_Token(sentence)

    if lang_code not in main.settings_global['word_tokenizers']:
        lang_code = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang_code]

    # English & Other Languages
    if word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
        treebank_tokenizer = nltk.TreebankWordTokenizer()

        for sentence in sentences:
            token_groups.append(treebank_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
        tweet_tokenizer = nltk.TweetTokenizer()

        for sentence in sentences:
            token_groups.append(tweet_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
        nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()

        for sentence in sentences:
            token_groups.append(nist_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
        toktok_tokenizer = nltk.ToktokTokenizer()

        for sentence in sentences:
            token_groups.append(toktok_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('SacreMoses - Moses Tokenizer'):
        moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang_code))

        for sentence in sentences:
            token_groups.append(moses_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('SacreMoses - Penn Treebank Tokenizer'):
        moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang_code))

        for sentence in sentences:
            token_groups.append(moses_tokenizer.penn_tokenize(sentence))
    elif 'spaCy' in word_tokenizer:
        # Languages with models
        if lang_code in ['nld', 'eng', 'fra', 'deu', 'ita', 'por', 'spa', 'other']:
            # Other Languages
            if lang_code == 'other':
                lang_code = 'eng'

            check_spacy_models(main, lang_code)

            nlp = main.__dict__[f'spacy_nlp_{lang_code}']

            for sentence in sentences:
                token_groups.append([token.text for token in nlp(str(sentence))])
        # Languages without models
        else:
            nlp = spacy.blank(wordless_conversion.to_iso_639_1(main, lang_code))

            for sentence in sentences:
                token_groups.append([token.text for token in nlp(str(sentence))])

    # Chinese
    elif word_tokenizer == main.tr('jieba - Chinese Word Tokenizer'):
        for sentence in sentences:
            token_groups.append(jieba.cut(sentence))

    # Chinese & Japanese
    elif (word_tokenizer == main.tr('Wordless - Chinese Character Tokenizer') or
          word_tokenizer == main.tr('Wordless - Japanese Kanji Tokenizer')):
        for sentence in sentences:
            tokens = []
            non_han_start = 0

            for i, char in enumerate(sentence):
                if i >= non_han_start:
                    if wordless_unicode.is_han(char):
                        tokens.append(char)

                        non_han_start += 1
                    else:
                        # English
                        if wordless_unicode.is_eng(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 == len(sentence) or not wordless_unicode.is_eng(sentence[i + j + 1]):
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                         lang_code = 'eng'))

                                    non_han_start = i + j + 1

                                    break
                        # Japanese Kana
                        elif wordless_unicode.is_kana(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 == len(sentence) or not wordless_unicode.is_kana(sentence[i + j + 1]):
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                         lang_code = 'jpn',
                                                                         word_tokenizer = main.tr('nagisa - Japanese Word Tokenizer')))

                                    non_han_start = i + j + 1

                                    break
                        # Thai
                        elif wordless_unicode.is_thai(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 == len(sentence) or not wordless_unicode.is_thai(sentence[i + j + 1]):
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                         lang_code = 'tha'))

                                    non_han_start = i + j + 1

                                    break
                        # Other Languages
                        else:
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 == len(sentence) or wordless_unicode.is_han(sentence[i + j + 1]):
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                         lang_code = 'other'))

                                    non_han_start = i + j + 1

                                    break

            token_groups.append(tokens)

    # Japanese
    elif word_tokenizer == main.tr('nagisa - Japanese Word Tokenizer'):
        import nagisa

        for sentence in sentences:
            token_groups.append(nagisa.tagging(str(sentence)).words)

    # Thai
    elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching Algorithm + TCC'):
        for sentence in sentences:
            token_groups.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'newmm'))
    elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching Algorithm'):
        for sentence in sentences:
            token_groups.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'mm'))
    elif word_tokenizer == main.tr('PyThaiNLP - Longest Matching'):
        for sentence in sentences:
            token_groups.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'longest-matching'))

    # Tibetan
    elif word_tokenizer == main.tr('pybo - Tibetan Word Tokenizer'):
        if 'pybo_bo_tokenizer' not in main.__dict__:
            main.pybo_bo_tokenizer = pybo.BoTokenizer('POS')

        for sentence in sentences:
            token_groups.append([token.content for token in main.pybo_bo_tokenizer.tokenize(sentence)])

    # Vietnamese
    elif word_tokenizer == main.tr('Underthesea - Vietnamese Word Tokenizer'):
        for sentence in sentences:
            token_groups.append(underthesea.word_tokenize(str(sentence)))

    token_groups = [list(tokens) for tokens in token_groups]

    # Remove empty tokens
    for i, tokens in enumerate(token_groups):
        token_groups[i] = [token for token in tokens if re.search(r'\S', token)]

    # Record token boundaries
    if lang_code in ['zho_cn', 'zho_tw', 'jpn', 'tha']:
        for sentence, tokens in zip(sentences, token_groups):
            token_start = 0

            for i, token in enumerate(tokens):
                if type(token) != wordless_text.Wordless_Token:
                    boundary = re.search(r'^\s+', sentence[token_start + len(token):])

                    if boundary == None:
                        boundary = ''
                    else:
                        boundary = boundary.group()

                    tokens[i] = wordless_text.Wordless_Token(token, boundary = boundary)

                    token_start += len(token) + len(boundary)
                else:
                    token_start += len(token) + len(token.boundary)

            tokens[-1] = wordless_text.Wordless_Token(tokens[-1], boundary = sentence.boundary, sentence_ending = True)
    else:
        for sentence, tokens in zip(sentences, token_groups):
            if tokens:
                tokens[-1] = wordless_text.Wordless_Token(tokens[-1], boundary = sentence.boundary, sentence_ending = True)

    return [token for tokens in token_groups for token in tokens]

def wordless_word_detokenize(main, tokens, lang_code, word_detokenizer = 'default'):
    sentence_start = 0
    sentences = []
    text = ''

    if lang_code not in main.settings_global['word_detokenizers']:
        lang_code = 'other'

    if word_detokenizer == 'default':
        word_detokenizer = main.settings_custom['word_detokenization']['word_detokenizers'][lang_code]

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
        moses_detokenizer = sacremoses.MosesDetokenizer(lang = wordless_conversion.to_iso_639_1(main, lang_code))

        for sentence in sentences:
            text += moses_detokenizer.detokenize(sentence)
    # Chinese & Japanese
    elif (word_detokenizer == main.tr('Wordless - Chinese Word Detokenizer') or
          word_detokenizer == main.tr('Wordless - Japanese Word Detokenizer')):
        # Settings - > Word Detokenization
        if type(tokens[0]) == str:
            non_cjk_start = 0

            for i, token in enumerate(tokens):
                if i >= non_cjk_start:
                    if wordless_unicode.has_han(token) or wordless_unicode.has_kana(token):
                        text += token

                        non_cjk_start += 1
                    else:
                        # English
                        if wordless_unicode.is_eng_token(token):
                            for j, token in enumerate(tokens[i:]):
                                if i + j + 1 == len(tokens) or not wordless_unicode.is_eng_token(tokens[i + j + 1]):
                                    text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                     lang_code = 'eng')

                                    non_cjk_start = i + j + 1

                                    break
                        # Thai
                        elif wordless_unicode.has_thai(token):
                            for j, token in enumerate(tokens[i:]):
                                if i + j + 1 == len(tokens) or not wordless_unicode.has_thai(tokens[i + j + 1]):
                                    text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                     lang_code = 'tha')

                                    non_cjk_start = i + j + 1

                                    break
                        # Other Languages
                        else:
                            for j, token in enumerate(tokens[i:]):
                                if (i + j + 1 == len(tokens) or
                                    wordless_unicode.has_han(tokens[i + j + 1]) or
                                    wordless_unicode.has_kana(tokens[i + j + 1])):
                                    text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                     lang_code = 'other')

                                    non_cjk_start = i + j + 1

                                    break
        else:
            text = ''.join([token + token.boundary for token in tokens])

    # Thai
    elif word_detokenizer == main.tr('Wordless - Thai Word Detokenizer'):
        # Settings -> Detokenization
        if type(tokens[0]) == str:
            text = ''.join(tokens)
        else:
            text = ''.join([token + token.boundary for token in tokens])

    return re.sub(r'\s{2,}', ' ', text)

def wordless_pos_tag(main, sentences, lang_code, pos_tagger = 'default', tagset = 'custom'):
    tokens_tagged = []

    if type(sentences) != list:
        sentences = [sentences]

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang_code]

    # Chinese
    if pos_tagger == main.tr('jieba - Chinese POS Tagger'):
        for sentence in sentences:
            tokens_tagged.extend(jieba.posseg.cut(sentence))

    # Dutch, English, French, German, Italian, Portuguese and Spanish
    elif 'spaCy' in pos_tagger:
        check_spacy_models(main, lang_code)

        nlp = main.__dict__[f'spacy_nlp_{lang_code}']

        for sentence in sentences:
            tokens_tagged.extend([(token.text, token.tag_) for token in nlp(str(sentence))])

    # English & Russian
    elif pos_tagger == main.tr('NLTK - Perceptron POS Tagger'):
        for sentence in sentences:
            tokens = wordless_word_tokenize(main, sentence, lang_code)

            tokens_tagged.extend(nltk.pos_tag(tokens, lang = lang_code))

    # Japanese
    elif pos_tagger == main.tr('nagisa - Japanese POS Tagger'):
        import nagisa

        for sentence in sentences:
            tagged_tokens = nagisa.tagging(str(sentence))

            tokens_tagged.extend(zip(tagged_tokens.words, tagged_tokens.postags))

    # Russian & Ukrainian
    elif pos_tagger == main.tr('pymorphy2 - Morphological Analyzer'):
        if lang_code == 'rus':
            morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'ru')
        elif lang_code == 'ukr':
            morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'uk')

        for sentence in sentences:
            tokens = wordless_word_tokenize(main, sentence, lang_code)

            for token in tokens:
                tokens_tagged.append((token, morphological_analyzer.parse(token)[0].tag._POS))

    # Thai
    elif pos_tagger == main.tr('PyThaiNLP - Perceptron POS Tagger - ORCHID Corpus'):
        for sentence in sentences:
            tokens = wordless_word_tokenize(main, sentence, lang_code = 'tha')

            tokens_tagged.extend(pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'orchid'))
    elif pos_tagger == main.tr('PyThaiNLP - Perceptron POS Tagger - PUD Corpus'):
        for sentence in sentences:
            tokens = wordless_word_tokenize(main, sentence, lang_code = 'tha')

            tokens_tagged.extend(pythainlp.tag.pos_tag(tokens, engine = 'perceptron', corpus = 'pud'))

    # Tibetan
    elif pos_tagger == main.tr('pybo - Tibetan POS Tagger'):
        if 'pybo_bo_tokenizer' not in main.__dict__:
            main.pybo_bo_tokenizer = pybo.BoTokenizer('POS')

        for sentence in sentences:
            tokens_tagged.extend([(token.content, token.pos) for token in main.pybo_bo_tokenizer.tokenize(sentence)])

    # Vietnamese
    elif pos_tagger == main.tr('Underthesea - Vietnamese POS Tagger'):
        for sentence in sentences:
            tokens_tagged.extend(underthesea.pos_tag(str(sentence)))

    # Convert to Universal Tagset
    if (tagset == 'custom' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
        tagset == 'universal'):

        mappings = {tag: tag_universal
                    for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang_code][pos_tagger]}

        tokens_tagged = [(token, mappings[tag])
                         for token, tag in tokens_tagged]

    return tokens_tagged

def wordless_lemmatize(main, tokens, lang_code, lemmatizer = 'default'):
    mapping_lemmas = {}
    lemmas = []

    if tokens and lang_code in main.settings_global['lemmatizers']:
        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang_code]

        # English & Other Languages
        if 'spaCy' in lemmatizer:
            check_spacy_models(main, lang_code)

            nlp = main.__dict__[f'spacy_nlp_{lang_code}']

            lemmas.extend([token.lemma_ for token in nlp(wordless_word_detokenize(main, tokens, lang_code))])

        # English
        elif lemmatizer == main.tr('NLTK - WordNet Lemmatizer'):
            word_net_lemmatizer = nltk.WordNetLemmatizer()

            for token, pos in wordless_pos_tag(main, tokens,
                                               lang_code = 'eng',
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

        # Russian & Ukrainian
        elif lemmatizer == main.tr('pymorphy2 - Morphological Analyzer'):
            if lang_code == 'rus':
                morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'ru')
            else:
                morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'uk')

            for token in tokens:
                lemmas.append(morphological_analyzer.parse(token)[0].normal_form)

        # Tibetan
        elif lemmatizer == main.tr('pybo - Tibetan Lemmatizer'):
            if 'pybo_bo_tokenizer' not in main.__dict__:
                main.pybo_bo_tokenizer = pybo.BoTokenizer('POS')

            for token in tokens:
                for token in main.pybo_bo_tokenizer.tokenize(token):
                    if token.lemma:
                        lemmas.append(token.lemma)
                    else:
                        lemmas.append(token.content)

        # Other Languages
        elif lemmatizer == main.tr('Lemmatization Lists'):
            lang_code = wordless_conversion.to_iso_639_1(main, lang_code)

            with open(f'lemmatization/Lemmatization Lists/lemmatization-{lang_code}.txt', 'r', encoding = 'utf_8_sig') as f:
                for line in f:
                    try:
                        lemma, word = line.rstrip().split('\t')

                        mapping_lemmas[word] = lemma
                    except:
                        pass

            lemmas = [mapping_lemmas.get(token, token) for token in tokens]
    else:
        lemmas = tokens

    return lemmas

def wordless_get_stop_words(main, lang_code, word_list = 'default'):
    if word_list == 'default':
        word_list = main.settings_custom['stop_words']['stop_words'][lang_code]

    lang_code_639_1 = wordless_conversion.to_iso_639_1(main, lang_code)

    # Chinese (Simplified)
    if lang_code_639_1 == 'zh_cn':
        lang_code_639_1 = 'zh'

    if word_list == 'Stopwords ISO':
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang_code_639_1 in ['nb', 'nn']:
            lang_code_639_1 = 'no'

        # Chinese (Traditional)
        if lang_code_639_1 == 'zh_tw':
            with open(r'stop_words/Stopwords ISO/stop_words_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                stop_words = json.load(f)[lang_code_639_1]
    elif word_list == 'spaCy':
        # Chinese (Traditional)
        if lang_code_639_1 == 'zh_tw':
            with open(r'stop_words/spaCy/stop_words_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            spacy_lang = importlib.import_module(f'spacy.lang.{lang_code_639_1}')

            stop_words = spacy_lang.STOP_WORDS
    elif word_list == 'NLTK':
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang_code_639_1 in ['nb', 'nn']:
            lang_code_639_1 = 'no'

        lang_text = wordless_conversion.to_lang_text(main, lang_code)

        # Greek
        if lang_text == main.tr('Greek (Modern)'):
            lang_text = main.tr('Greek')

        stop_words = nltk.corpus.stopwords.words(lang_text)

    # Thai
    elif word_list == 'PyThaiNLP':
        stop_words = pythainlp.corpus.stopwords.words('thai')

    # Custom Lists
    elif word_list == main.tr('Custom List'):
        stop_words = main.settings_custom['stop_words']['custom_lists'][lang_code]

    return sorted(stop_words)

def wordless_filter_stop_words(main, items, lang_code):
    if lang_code not in main.settings_global['stop_words']:
        lang_code == 'other'

    stop_words = wordless_get_stop_words(main, lang_code)

    if type(items[0]) == str:
        items_filtered = [token for token in items if token not in stop_words]
    elif type(items[0]) in [list, tuple, set]:
        items_filtered = [ngram
                          for ngram in items
                          if not [token for token in ngram if token in stop_words]]

    return items_filtered
