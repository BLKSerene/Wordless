#
# Wordless: Text Processing
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import importlib
import json
import re

import jieba
import jieba.posseg
import nagisa
import nltk
import nltk.tokenize.nist
import numpy
import pymorphy2
import pythainlp
import pyvi.ViTokenizer
import pyvi.ViPosTagger
import sacremoses
import spacy

from wordless_text import wordless_text
from wordless_utils import wordless_conversion, wordless_unicode

def wordless_sentence_tokenize(main, text, lang_code, sentence_tokenizer = 'default'):
    sentences = []
    boundary_start = 0

    if lang_code not in main.settings_global['sentence_tokenizers']:
        lang_code = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang_code]

    for line in text.splitlines():
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

            sentences.extend(nltk.sent_tokenize(line, language = lang_text))
        elif 'spaCy' in sentence_tokenizer:
            # English
            if lang_code == 'eng':
                nlp = spacy.load('en_core_web_sm')
            else:
                pass

            doc = nlp(text)

            sentences.extend([sentence.text for sentence in doc.sents])

        # Chinese & Japanese
        elif (sentence_tokenizer == main.tr('Wordless - Chinese Sentence Tokenizer') or
              sentence_tokenizer == main.tr('Wordless - Japanese Sentence Tokenizer')):
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
            sentences.extend(pythainlp.tokenize.sent_tokenize(line))

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
                        # Japanese Kana
                        if wordless_unicode.is_kana(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 < len(sentence):
                                    if not wordless_unicode.is_kana(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang_code = 'jpn',
                                                                             word_tokenizer = main.tr('nagisa - Japanese Word Tokenizer')))

                                        non_han_start = i + j + 1

                                        break
                                else:
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start:],
                                                                         lang_code = 'jpn',
                                                                         word_tokenizer = main.tr('nagisa - Japanese Word Tokenizer')))

                                    non_han_start = i + j + 1
                        # Thai
                        elif wordless_unicode.is_thai(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 < len(sentence):
                                    if not wordless_unicode.is_thai(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang_code = 'tha'))

                                        non_han_start = i + j + 1

                                        break
                                else:
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start:],
                                                                         lang_code = 'tha'))

                                    non_han_start = i + j + 1
                        # Other Languages
                        else:
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 < len(sentence):
                                    if wordless_unicode.is_han(sentence[i + j + 1]):
                                        tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                             lang_code = 'other'))

                                        non_han_start = i + j + 1

                                        break
                                else:
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start:],
                                                                         lang_code = 'other'))

                                    non_han_start = i + j + 1

            token_groups.append(tokens)

    # Japanese
    elif word_tokenizer == main.tr('nagisa - Japanese Word Tokenizer'):
        for sentence in sentences:
            token_groups.append(nagisa.tagging(str(sentence)).words)

    # Vietnamese
    elif word_tokenizer == main.tr('Pyvi - Vietnamese Word Tokenizer'):
        for sentence in sentences:
            tokens = pyvi.ViTokenizer.spacy_tokenize(sentence)[0]

            token_groups.append(tokens)

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
                    if re.search(r'^[\u2E80-\u9FFF]+$', token):
                        text += token

                        non_cjk_start += 1
                    else:
                        for j, token in enumerate(tokens):
                            if j > i and re.search(r'^[\u2E80-\u9FFF]+$', token):
                                text += wordless_word_detokenize(main, tokens[non_cjk_start:j], 'eng')

                                non_cjk_start = j

                                break
                            elif j == len(tokens) - 1:
                                text += wordless_word_detokenize(main, tokens[non_cjk_start:], 'eng')

                                non_cjk_start = j + 1

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

    return text

def wordless_pos_tag(main, sentences, lang_code, pos_tagger = 'default', tagset = 'custom'):
    tokens_tagged = []

    if type(sentences) != list:
        sentences = [sentences]

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang_code]

    # English & Russian
    if pos_tagger == main.tr(main.tr('NLTK - Perceptron POS Tagger')):
        for sentence in sentences:
            tokens = wordless_word_tokenize(main, sentence, lang_code)

            tokens_tagged.extend(nltk.pos_tag(tokens, lang = lang_code))

    # Chinese
    elif pos_tagger == main.tr('jieba - Chinese POS Tagger'):
        for sentence in sentences:
            tokens_tagged.extend(jieba.posseg.cut(sentence))

    # Japanese
    elif pos_tagger == main.tr('nagisa - Japanese POS Tagger'):
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

    # Vietnamese
    elif pos_tagger == main.tr('Pyvi - Vietnamese POS Tagger'):
        for sentence in sentences:
            tokens = wordless_word_tokenize(main, sentence, lang_code)

            tokens, tags = pyvi.ViPosTagger.postagging(' '.join(tokens))

            tokens_tagged.extend(zip(tokens, tags))

    # Convert to Universal Tagset
    if (tagset == 'custom' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
        tagset == 'universal'):
        tagset_default = main.settings_global['pos_taggers'][lang_code][pos_tagger]
        mappings = {tag: tag_universal
                    for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][tagset_default]}

        tokens_tagged = [(token, mappings[tag])
                         for token, tag in tokens_tagged]

    return tokens_tagged

def wordless_lemmatize(main, tokens, lang_code, lemmatizer = 'default'):
    mapping_lemmas = {}
    lemmas = []

    if tokens and lang_code in main.settings_global['lemmatizers']:
        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang_code]

        # English
        if lemmatizer == main.tr('NLTK - WordNet Lemmatizer'):
            word_net_lemmatizer = nltk.WordNetLemmatizer()

            for i, (token, pos) in enumerate(nltk.pos_tag(tokens)):
                if pos in ['JJ', 'JJR', 'JJS']:
                    lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADJ))
                elif pos in ['NN', 'NNS', 'NNP', 'NNPS']:
                    lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.NOUN))
                elif pos in ['RB', 'RBR', 'RBS']:
                    lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADV))
                elif pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                    lemmas.append(word_net_lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.VERB))
                else:
                    lemmas.append(word_net_lemmatizer.lemmatize(token))
        elif lemmatizer == main.tr('pymorphy2 - Morphological Analyzer'):
            if lang_code == 'rus':
                morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'ru')
            else:
                morphological_analyzer = pymorphy2.MorphAnalyzer(lang = 'uk')

            for token in tokens:
                lemmas.append(morphological_analyzer.parse(token)[0].normal_form)

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

        stop_words = nltk.corpus.stopwords.words(lang_text)

    # Thai
    elif word_list == 'PyThaiNLP':
        stop_words = pythainlp.corpus.stopwords.words('thai')

    return sorted(stop_words)

def wordless_filter_stop_words(main, items, lang_code):
    if lang_code in main.settings_global['stop_words']:
        stop_words = wordless_get_stop_words(main, lang_code)

        if type(items[0]) == str:
            items_filtered = [token for token in items if token not in stop_words]
        elif type(items[0]) in [list, tuple, set]:
            items_filtered = [ngram
                              for ngram in items
                              if not [token for token in ngram if token in stop_words]]

        return items_filtered
    else:
        return items

def wordless_preprocess_tokens(main, tokens, lang_code, settings):
    if settings['words']:
        if settings['treat_as_lowercase']:
            tokens = [token.lower() for token in tokens]

        if settings['lemmatize']:
            tokens = wordless_lemmatize(main, tokens, lang_code)

    if not settings['puncs']:
        tokens = [token for token in tokens if [char for char in token if char.isalnum()]]

    return tokens

def wordless_preprocess_tokens_tagged(main, tokens_tagged, lang_code, settings):
    if settings['treat_as_lowercase']:
        tokens_tagged = [(token.lower(), tag) for token, tag in tokens_tagged]

    if settings['lemmatize']:
        tokens_lemmatized = wordless_lemmatize(main, numpy.array(tokens_tagged)[:, 0], lang_code)

        tokens_tagged = [(token, tag)
                         for token, tag in zip(tokens_lemmatized, numpy.array(tokens_tagged)[:, 1])]

    if not settings['puncs']:
        tokens_tagged = [(token, tag)
                         for token, tag in tokens_tagged
                         if [char for char in token if char.isalnum()]]

    return tokens_tagged

def wordless_postprocess_tokens(main, tokens, lang_code, settings):
    if settings['words']:
        if not settings['treat_as_lowercase']:
            if not settings['lowercase']:
                tokens = [token for token in tokens if not token.islower()]
            if not settings['uppercase']:
                tokens = [token for token in tokens if not token.isupper()]
            if not settings['title_case']:
                tokens = [token for token in tokens if not token.istitle()]

        if settings['filter_stop_words']:
            tokens = wordless_filter_stop_words(main, tokens, lang_code)
    else:
        tokens = [token for token in tokens if not [char for char in token if char.isalpha()]]
    
    if not settings['nums']:
        tokens = [token for token in tokens if not token.isnumeric()]

    return tokens

def wordless_postprocess_freq_ngrams(main, ngrams_freq_file, lang_code, settings):
    if settings['words']:
        if not settings['treat_as_lowercase']:
            if not settings['lowercase']:
                ngrams_freq_file = {ngram: freq
                                    for ngram, freq in ngrams_freq_file.items()
                                    if not [token for token in ngram if token.islower()]}
            if not settings['uppercase']:
                ngrams_freq_file = {ngram: freq
                                    for ngram, freq in ngrams_freq_file.items()
                                    if not [token for token in ngram if token.isupper()]}
            if not settings['title_case']:
                ngrams_freq_file = {ngram: freq
                                    for ngram, freq in ngrams_freq_file.items()
                                    if not [token for token in ngram if token.istitle()]}

        if settings['filter_stop_words']:
            ngrams_filtered = wordless_filter_stop_words(main, list(ngrams_freq_file.keys()), lang_code)
            
            ngrams_freq_file = {ngram: ngrams_freq_file[ngram] for ngram in ngrams_filtered}
    else:
        ngrams_freq_file = {ngram: freq
                            for ngram, freq in ngrams_freq_file.items()
                            if not [char for char in ''.join(ngram) if char.isalpha()]}

    if not settings['nums']:
        ngrams_freq_file = {ngram: freq
                            for ngram, freq in ngrams_freq_file.items()
                            if [token for token in ngram if not token.isnumeric()]}

    return ngrams_freq_file

def wordless_postprocess_freq_collocation(main, collocates_freq_file, lang_code, settings):
    collocates = [collocate[1] for collocate in collocates_freq_file]

    collocates_filtered = wordless_postprocess_tokens(main, collocates, lang_code, settings)

    collocates_freq_file = {collocate: freq_files
                            for collocate, freq_files in collocates_freq_file.items()
                            if collocate[1] in collocates_filtered}

    return collocates_freq_file

def wordless_postprocess_freq_colligation(main, collocates_freq_file, tokens, lang_code, settings):
    tokens_filtered = wordless_postprocess_tokens(main, tokens, lang_code, settings)

    collocates_freq_file = {collocate: freq_files
                            for (collocate, freq_files), token in zip(collocates_freq_file.items(), tokens_filtered)
                            if token in tokens_filtered}

    return collocates_freq_file
