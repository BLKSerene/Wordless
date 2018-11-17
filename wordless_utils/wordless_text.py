#
# Wordless: Text
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import collections
import copy
import json
import re

from bs4 import BeautifulSoup
import delphin.repp
import jieba
import jieba.posseg
import jpype
import nltk
import nltk.tokenize.nist

from wordless_utils import wordless_conversion

def wordless_sentence_tokenize(main, text, lang_code, sentence_tokenizer = 'default'):
    sentences = []

    if lang_code not in main.settings_global['sentence_tokenizers']:
        lang_code = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang_code]

    if 'HanLP' in sentence_tokenizer:
        import pyhanlp

    for line in text.splitlines():
        # English
        if sentence_tokenizer == main.tr('NLTK - Punkt Sentence Tokenizer'):
            if lang_code == 'other':
                lang_text = 'english'
            else:
                lang_text = wordless_conversion.to_lang_text(main, lang_code).lower()

            sentences.extend(nltk.sent_tokenize(line, language = lang_text))
        # Chinese
        elif sentence_tokenizer == main.tr('Wordless - Chinese Sentence Tokenizer'):
            i_sentence = 0

            for i, char in enumerate(line):
                if i >= i_sentence and char in ['。', '！', '？', '!', '?']:
                    for j, char in enumerate(line):
                        if j > i and char not in ['。', '！', '？', '!', '?', '’', '”', '）', ')']:
                            sentences.append(line[i_sentence : j])

                            i_sentence = j

                            break

            if i_sentence <= len(line):
                sentences.append(line[i_sentence:])

        elif sentence_tokenizer == main.tr('HanLP - Sentence Segmenter'):
            sentences_util = jpype.JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')

            sentences = standard_tokenizer.SEGMENT.seg2sentence(line, False)

    return sentences

def wordless_word_tokenize(main, sentences, lang_code, word_tokenizer = 'default'):
    tokens = []

    if type(sentences) == str:
        sentences = [sentences]

    if lang_code not in main.settings_global['word_tokenizers']:
        lang_code = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang_code]

    # English
    if word_tokenizer == main.tr('NLTK - Treebank Tokenizer'):
        treebank_tokenizer = nltk.TreebankWordTokenizer()

        for sentence in sentences:
            tokens.extend(treebank_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
        tweet_tokenizer = nltk.TweetTokenizer()

        for sentence in sentences:
            tokens.extend(tweet_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
        nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()

        for sentence in sentences:
            tokens.extend(nist_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
        toktok_tokenizer = nltk.ToktokTokenizer()

        for sentence in sentences:
            tokens.extend(toktok_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Word Punctuation Tokenizer'):
        word_punct_tokenizer = nltk.WordPunctTokenizer()

        for sentence in sentences:
            tokens.extend(nltk.word_punct_tokenizer(sentence))
    elif word_tokenizer == main.tr('PyDelphin - Repp Tokenizer'):
        repp_tokenizer = delphin.repp.REPP.from_config('tokenization/repp_tokenizer/erg/repp.set')

        for sentence in sentences:
            tokens.extend([token.form for token in repp_tokenizer.tokenize(sentence).tokens])
    # Chinese
    elif word_tokenizer == main.tr('jieba - With HMM'):
        for sentence in sentences:
            tokens.extend(jieba.cut(sentence))
    elif word_tokenizer == main.tr('jieba - Without HMM'):
        for sentence in sentences:
            tokens.extend(jieba.cut(sentence, HMM = False))
    elif word_tokenizer == main.tr('HanLP - Standard Tokenizer'):
        standard_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in standard_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Basic Tokenizer'):
        basic_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.BasicTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in basic_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - High-speed Tokenizer'):
        speed_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.SpeedTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in speed_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Traditional Chinese Tokenizer'):
        zh_tw_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in zh_tw_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - URL Tokenizer'):
        url_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.URLTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in url_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - CRF Lexical Analyzer'):
        crf_tokenizer = jpype.JClass('com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer')()

        for sentence in sentences:
            tokens.extend([token for token in crf_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Perceptron Lexical Analyzer'):
        perceptron_tokenizer = jpype.JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')()

        for sentence in sentences:
            tokens.extend([token for token in perceptron_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Dijkstra Segmenter'):
        DijkstraSegment = jpype.JClass('com.hankcs.hanlp.seg.Dijkstra.DijkstraSegment')
        dijkstra_tokenizer = DijkstraSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        for sentence in sentences:
            tokens.extend([token.word for token in dijkstra_tokenizer.seg(sentence)])
    elif word_tokenizer == main.tr('HanLP - N-shortest Path Segmenter'):
        NShortSegment = jpype.JClass('com.hankcs.hanlp.seg.NShort.NShortSegment')
        nshortest_tokenizer = NShortSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        for sentence in sentences:
            tokens.extend([token.word for token in nshortest_tokenizer.seg(sentence)])
    elif word_tokenizer == main.tr('HanLP - Viterbi Segmenter'):
        ViterbiSegment = jpype.JClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')
        viterbi_tokenizer = ViterbiSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        for sentence in sentences:
            tokens.extend([token.word for token in viterbi_tokenizer.seg(sentence)])
    elif word_tokenizer == main.tr('Wordless - Single Character Splitter'):
        tokens = [char for sentence in sentences for char in sentence]

    return tokens

def wordless_word_detokenize(main, tokens, lang_code, word_detokenizer = 'default'):
    text = ''

    if word_detokenizer == 'default':
        word_detokenizer = main.settings_custom['word_detokenization']['word_detokenizers'][lang_code]

    if word_detokenizer == main.tr('NLTK - Moses Detokenizer'):
        texts = []

        moses_detokenizer = nltk.tokenize.treebank.TreebankWordDetokenizer()

        for sentence in wordless_sentence_tokenize(main, ' '.join(tokens), lang_code):
            texts.append(moses_detokenizer.tokenize(sentence.split()))

        text = ' '.join(texts)
    elif word_detokenizer == main.tr('Wordless - Chinese Word Detokenizer'):
        non_cjkv_start = 0

        for i, token in enumerate(tokens):
            if i >= non_cjkv_start:
                if re.search(r'[\u2E80-\u9FFF]', token):
                    text += token

                    non_cjkv_start += 1
                else:
                    for j, token in enumerate(tokens):
                        if j > i and re.search(r'[\u2E80-\u9FFF]', token):
                            text += wordless_word_detokenize(main, tokens[non_cjkv_start:j], 'eng')

                            non_cjkv_start = j

                            break
                        elif j == len(tokens) - 1:
                            text += wordless_word_detokenize(main, tokens[non_cjkv_start:], 'eng')

                            non_cjkv_start = j + 1

                            break

    return text

def wordless_pos_tag(main, text, lang_code, pos_tagger = 'default', tagset = 'default'):
    tokens_tagged = []

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang_code]

    sentences = wordless_sentence_tokenize(main, text, lang_code)

    if pos_tagger == main.tr(main.tr('NLTK - Perceptron POS Tagger')):
        for sentence in sentences:
            tokens_tagged.extend(nltk.pos_tag(wordless_word_tokenize(main, sentence, lang_code), lang = lang_code))
    elif pos_tagger == main.tr('jieba'):
        for sentence in sentences:
            tokens_tagged.extend(jieba.posseg.cut(sentence))
    elif pos_tagger == main.tr('HanLP - CRF Lexical Analyzer'):
        crf_tagger = jpype.JClass('com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer')()

        for sentence in sentences:
            tokens_tagged.extend(list(zip(*crf_tagger.analyze(text).toWordTagArray())))
    elif pos_tagger == main.tr('HanLP - Perceptron Lexical Analyzer'):
        perceptron_tagger = jpype.JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')()

        for sentence in sentences:
            tokens_tagged.extend(list(zip(*perceptron_tagger.analyze(text).toWordTagArray())))

    if tagset == 'default':
        tagset = main.settings_custom['pos_tagging']['tagsets'][lang_code]

    # Convert to Universal Tagset
    if tagset == 'Universal':
        tagset_source = main.settings_global['pos_taggers'][lang_code][pos_tagger]

        tokens_tagged = [(token, wordless_conversion.to_universal_tagset(main, tagset_source, tag))
                         for token, tag in tokens_tagged]

    return tokens_tagged

def wordless_lemmatize(main, tokens, lang_code, lemmatizer = 'default'):
    lemma_list = {}
    lemmas = []

    if tokens and lang_code in main.settings_global['lemmatizers']:
        tokens = list(tokens)

        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang_code]

        if lemmatizer == 'NLTK':
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
        elif lemmatizer == 'e_lemma.txt':
            with open('lemmatization/e_lemma.txt', 'r', encoding = 'utf_16') as f:
                for line in f:
                    if not line.startswith(';'):
                        lemma, words = line.rstrip().split('->')

                        for word in words.split(','):
                            lemma_list[word.strip()] = lemma.strip()

            lemmas = [lemma_list.get(token, token) for token in tokens]

        elif lemmatizer == 'Lemmatization Lists':
            lang_code = wordless_conversion.to_iso_639_1(main, lang_code)

            with open(f'lemmatization/Lemmatization Lists/lemmatization-{lang_code}.txt', 'r', encoding = 'utf_8') as f:
                for line in f:
                    try:
                        lemma, word = line.rstrip().split('\t')

                        lemma_list[word] = lemma
                    except:
                        pass

            lemmas = [lemma_list.get(token, token) for token in tokens]
    else:
        lemmas = tokens

    return lemmas

def wordless_filter_stop_words(main, items, lang_code):
    lang_text = wordless_conversion.to_lang_text(main, lang_code)
    lang_code_639_1 = wordless_conversion.to_iso_639_1(main, lang_code)

    if lang_code_639_1 == 'zh_CN':
        lang_code_639_1 = 'zh'

    if lang_code in main.settings_global['stop_words']:
        word_list = main.settings_custom['stop_words']['stop_words'][lang_code]

        if word_list == 'NLTK':
            stop_words = nltk.corpus.stopwords.words(lang_text)
        elif word_list == 'Stopwords ISO':
            if lang_code_639_1 == 'zh_TW':
                with open(r'stop_words/Stopwords ISO/stopwords_zh_TW.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]
            else:
                with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                    stop_words = json.load(f)[lang_code_639_1]
        elif word_list == 'stopwords-json':
            if lang_code_639_1 == 'zh_TW':
                with open(r'stop_words/stopwords-json/stopwords_zh_TW.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]
            else:
                with open(r'stop_words/stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
                    stop_words = json.load(f)[lang_code_639_1]
        elif word_list == 'HanLP':
            if lang_code_639_1 == 'zh_TW':
                with open(r'stop_words/HanLP/stopwords_zh_TW.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]
            else:
                with open(r'stop_words/HanLP/stopwords.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]

        if type(items[0]) == str:
            items_filtered = [token for token in items if token not in stop_words]
        elif type(items[0]) in [list, tuple, set]:
            items_filtered = [ngram for ngram in items if not [token for token in ngram if token in stop_words]]

        return items_filtered
    else:
        return items

def check_context(i, tokens, context_settings,
                  search_terms_inclusion, search_terms_exclusion):
    len_tokens = len(tokens)

    # Inclusion
    if context_settings['inclusion'] and search_terms_inclusion:
        inclusion_matched = False

        for search_term in search_terms_inclusion:
            if inclusion_matched:
                break

            for j in range(context_settings['inclusion_context_window_left'],
                           context_settings['inclusion_context_window_right'] + 1):
                if i + j < 0 or i + j > len_tokens - 1:
                    continue

                if j != 0:
                    if tokens[i + j : i + j + len(search_term)] == list(search_term):
                        inclusion_matched = True

                        break
    else:
        inclusion_matched = True

    # Exclusion
    exclusion_matched = True

    if context_settings['exclusion'] and search_terms_exclusion:
        for search_term in search_terms_exclusion:
            if not exclusion_matched:
                break

            for j in range(context_settings['exclusion_context_window_left'],
                           context_settings['exclusion_context_window_right'] + 1):
                if i + j < 0 or i + j > len_tokens - 1:
                    continue

                if j != 0:
                    if tokens[i + j : i + j + len(search_term)] == list(search_term):
                        exclusion_matched = False

                        break

    if inclusion_matched and exclusion_matched:
        return True
    else:
        return False

class Wordless_Text():
    def __init__(self, main, file, merge_puncs = False):
        self.main = main
        self.lang_code = file['lang_code']

        self.paras = []
        self.para_offsets = []
        self.sentences = []
        self.sentence_offsets = []
        self.tokens = []

        with open(file['path'], 'r', encoding = file['encoding_code']) as f:
            for line in f:
                if file['ext_code'] in ['.txt']:
                    text = line.rstrip()
                elif file['ext_code'] in ['.htm', '.html']:
                    soup = BeautifulSoup(line.rstrip(), 'lxml')
                    text = soup.get_text()

                if text:
                    self.paras.append(text)
                    self.para_offsets.append(len(self.tokens))

                    for sentence in wordless_sentence_tokenize(main, text, file['lang_code']):
                        self.sentences.append(sentence)
                        self.sentence_offsets.append(len(self.tokens))

                        self.tokens.extend(wordless_word_tokenize(main, sentence, file['lang_code']))

    def match_search_terms(self, search_terms, puncs,
                           ignore_case, match_inflected_forms, match_whole_word, use_regex):
        ngrams_matched = set()

        if puncs:
            tokens_text = self.tokens.copy()
        else:
            tokens_text = [token for token in self.tokens if [char for char in token if char.isalnum()]]

        search_terms = [wordless_word_tokenize(self.main, search_term, self.lang_code)
                        for search_term in search_terms]

        if use_regex:
            for ngram_search in search_terms:
                len_ngram_search = len(ngram_search)

                if match_whole_word:
                    ngram_search = [fr'(^|\s){token}(\s|$)' for token in ngram_search]

                if ignore_case:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for ngram_text in nltk.ngrams(tokens_text, len_ngram_search):
                    ngram_matched = True

                    for token_search, token_text in zip(ngram_search, ngram_text):
                        if not re.search(token_search, token_text, flags = flags):
                            ngram_matched = False

                            break

                    if ngram_matched:
                        ngrams_matched.add(ngram_text)
        else:
            for ngram_search in search_terms:
                len_ngram_search = len(ngram_search)

                ngram_search = [re.escape(token) for token in ngram_search]

                if match_whole_word:
                    ngram_search = [fr'(^|\s){token}(\s|$)' for token in ngram_search]

                if ignore_case:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for ngram_text in nltk.ngrams(tokens_text, len_ngram_search):
                    matched = True

                    for token_search, token_text in zip(ngram_search, ngram_text):
                        if not re.search(token_search, token_text, flags = flags):
                            matched = False

                            break

                    if matched:
                        ngrams_matched.add(ngram_text)

        if match_inflected_forms:
            tokens_text_lemma = wordless_lemmatize(self.main, tokens_text, self.lang_code)
            ngrams_matched_lemma = [wordless_lemmatize(self.main, ngram, self.lang_code)
                                    for ngram in ngrams_matched | set([tuple(search_term) for search_term in search_terms])]

            for ngram_matched_lemma in ngrams_matched_lemma:
                len_ngram_matched_lemma = len(ngram_matched_lemma)

                ngram_matched_lemma = [re.escape(token) for token in ngram_matched_lemma]
                ngram_matched_lemma = [fr'(^|\s){token}(\s|$)' for token in ngram_matched_lemma]

                if ignore_case:
                    flags = re.IGNORECASE
                else:
                    flags = 0

                for (ngram_text, ngram_text_lemma) in zip(nltk.ngrams(tokens_text, len_ngram_matched_lemma),
                                                          nltk.ngrams(tokens_text_lemma, len_ngram_matched_lemma)):
                    matched = True

                    for token_text_lemma, token_matched_lemma in zip(ngram_text_lemma, ngram_matched_lemma):
                        if not re.search(token_matched_lemma, token_text_lemma, flags = flags):
                            matched = False

                            break

                    if matched:
                        ngrams_matched.add(ngram_text)

        return ngrams_matched
