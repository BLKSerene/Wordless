#
# Wordless: Text Processing
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import json
import re

import delphin.repp
import jieba
import jieba.posseg
import jpype
import nagisa
import nltk
import nltk.tokenize.nist
import numpy
import sacremoses

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
        # Chinese & Japanese
        elif (sentence_tokenizer == main.tr('Wordless - Chinese Sentence Tokenizer') or
              sentence_tokenizer == main.tr('Wordless - Japanese Sentence Tokenizer')):
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
            sentences_util = pyhanlp.SafeJClass('com.hankcs.hanlp.utility.SentencesUtil')

            for sentence in sentences_util.toSentenceList(jpype.JString(line), False):
                sentences.append(sentence)

    return sentences

def wordless_word_tokenize(main, sentences, lang_code, word_tokenizer = 'default'):
    tokens = []

    if type(sentences) == str:
        sentences = [sentences]

    if lang_code not in main.settings_global['word_tokenizers']:
        lang_code = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang_code]

    if 'HanLP' in word_tokenizer:
        import pyhanlp

    # English & Other Languages
    if word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
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
    elif word_tokenizer == main.tr('NLTK - NIST Tokenizer (International Mode)'):
        nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()

        for sentence in sentences:
            tokens.extend(nist_tokenizer.international_tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
        toktok_tokenizer = nltk.ToktokTokenizer()

        for sentence in sentences:
            tokens.extend(toktok_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Word Punctuation Tokenizer'):
        word_punct_tokenizer = nltk.WordPunctTokenizer()

        for sentence in sentences:
            tokens.extend(word_punct_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('SacreMoses - Moses Tokenizer'):
        moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang_code))

        for sentence in sentences:
            tokens.extend(moses_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('SacreMoses - Penn Treebank Tokenizer'):
        moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang_code))

        for sentence in sentences:
            tokens.extend(moses_tokenizer.penn_tokenize(sentence))
    elif word_tokenizer == main.tr('PyDelphin - Repp Tokenizer'):
        repp_tokenizer = delphin.repp.REPP.from_config('tokenization/repp_tokenizer/erg/repp.set')

        for sentence in sentences:
            tokens.extend([token.form for token in repp_tokenizer.tokenize(sentence).tokens])
    # Chinese
    elif word_tokenizer == main.tr('jieba'):
        for sentence in sentences:
            tokens.extend(jieba.cut(sentence))
    elif word_tokenizer == main.tr('HanLP - Standard Tokenizer'):
        standard_tokenizer = pyhanlp.SafeJClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in standard_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Basic Tokenizer'):
        basic_tokenizer = pyhanlp.SafeJClass('com.hankcs.hanlp.tokenizer.BasicTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in basic_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - High-speed Tokenizer'):
        speed_tokenizer = pyhanlp.SafeJClass('com.hankcs.hanlp.tokenizer.SpeedTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in speed_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Traditional Chinese Tokenizer'):
        zh_tw_tokenizer = pyhanlp.SafeJClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in zh_tw_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - URL Tokenizer'):
        url_tokenizer = pyhanlp.SafeJClass('com.hankcs.hanlp.tokenizer.URLTokenizer')

        for sentence in sentences:
            tokens.extend([token.word for token in url_tokenizer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - CRF Lexical Analyzer'):
        for sentence in sentences:
            tokens.extend([token for token in main.crf_analyzer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Perceptron Lexical Analyzer'):
        for sentence in sentences:
            tokens.extend([token for token in main.perceptron_analyzer.segment(sentence)])
    elif word_tokenizer == main.tr('HanLP - Dijkstra Segmenter'):
        DijkstraSegment = pyhanlp.SafeJClass('com.hankcs.hanlp.seg.Dijkstra.DijkstraSegment')
        dijkstra_tokenizer = DijkstraSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        for sentence in sentences:
            tokens.extend([token.word for token in dijkstra_tokenizer.seg(sentence)])
    elif word_tokenizer == main.tr('HanLP - N-shortest Path Segmenter'):
        NShortSegment = pyhanlp.SafeJClass('com.hankcs.hanlp.seg.NShort.NShortSegment')
        nshortest_tokenizer = NShortSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        for sentence in sentences:
            tokens.extend([token.word for token in nshortest_tokenizer.seg(sentence)])
    elif word_tokenizer == main.tr('HanLP - Viterbi Segmenter'):
        ViterbiSegment = pyhanlp.SafeJClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')
        viterbi_tokenizer = ViterbiSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        for sentence in sentences:
            tokens.extend([token.word for token in viterbi_tokenizer.seg(sentence)])
    # Japanese
    elif word_tokenizer == main.tr('Nagisa'):
        for sentence in sentences:
            tokens.extend(nagisa.tagging(sentence).words)

    return tokens

def wordless_word_detokenize(main, tokens, lang_code, word_detokenizer = 'default'):
    sentences = []
    text = ''

    if lang_code not in main.settings_global['word_detokenizers']:
        lang_code = 'other'

    if word_detokenizer == 'default':
        word_detokenizer = main.settings_custom['word_detokenization']['word_detokenizers'][lang_code]

    # English & Other Languages
    if word_detokenizer == main.tr('NLTK - Penn Treebank Detokenizer'):
        treebank_detokenizer = nltk.tokenize.treebank.TreebankWordDetokenizer()

        for sentence in wordless_sentence_tokenize(main, ' '.join(tokens), lang_code):
            sentences.append(treebank_detokenizer.tokenize(sentence.split()))

        text = ' '.join(sentences)
    elif word_detokenizer == main.tr('SacreMoses - Moses Detokenizer'):
        moses_detokenizer = sacremoses.MosesDetokenizer(lang = wordless_conversion.to_iso_639_1(main, lang_code))

        for sentence in wordless_sentence_tokenize(main, ' '.join(tokens), lang_code):
            sentences.append(moses_detokenizer.detokenize(sentence.split()))

        text = ' '.join(sentences)
    # Chinese & Japanese
    elif (word_detokenizer == main.tr('Wordless - Chinese Word Detokenizer') or
          word_detokenizer == main.tr('Wordless - Japanese Word Detokenizer')):
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

    return text

def wordless_pos_tag(main, text, lang_code, pos_tagger = 'default', tagset = 'default'):
    tokens_tagged = []

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang_code]

    if 'HanLP' in pos_tagger:
        import pyhanlp

    sentences = wordless_sentence_tokenize(main, text, lang_code)

    # English & Russian
    if pos_tagger == main.tr(main.tr('NLTK - Perceptron POS Tagger')):
        for sentence in sentences:
            tokens_tagged.extend(nltk.pos_tag(wordless_word_tokenize(main, sentence, lang_code), lang = lang_code))
    # Chinese
    elif pos_tagger == main.tr('jieba'):
        for sentence in sentences:
            tokens_tagged.extend(jieba.posseg.cut(sentence))
    elif pos_tagger == main.tr('HanLP - CRF Lexical Analyzer'):
        for sentence in sentences:
            tokens_tagged.extend(list(zip(*main.crf_analyzer.analyze(text).toWordTagArray())))
    elif pos_tagger == main.tr('HanLP - Perceptron Lexical Analyzer'):
        perceptron_tagger = pyhanlp.SafeJClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')()

        for sentence in sentences:
            tokens_tagged.extend(list(zip(*main.perceptron_analyzer.analyze(text).toWordTagArray())))
    # Japanese
    elif pos_tagger == main.tr('Nagisa'):
        for sentence in sentences:
            tagged_tokens = nagisa.tagging(sentence)

            tokens_tagged.extend(zip(tagged_tokens.words, tagged_tokens.postags))

    if tagset == 'default':
        tagset = main.settings_custom['pos_tagging']['tagsets'][lang_code]

    # Convert to Universal Tagset
    if tagset == 'Universal':
        tagset_source = main.settings_global['pos_taggers'][lang_code][pos_tagger]

        tokens_tagged = [(token, wordless_conversion.to_universal_tagset(main, tagset_source, tag))
                         for token, tag in tokens_tagged]

    return tokens_tagged

def wordless_lemmatize(main, tokens, lang_code, lemmatizer = 'default'):
    mapping_lemmas = {}
    lemmas = []

    if tokens and lang_code in main.settings_global['lemmatizers']:
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
        elif lemmatizer == 'Lemmatization Lists':
            lang_code = wordless_conversion.to_iso_639_1(main, lang_code)

            with open(f'lemmatization/Lemmatization Lists/lemmatization-{lang_code}.txt', 'r', encoding = 'utf_8') as f:
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

def wordless_filter_stop_words(main, items, lang_code):
    lang_text = wordless_conversion.to_lang_text(main, lang_code)
    lang_code_639_1 = wordless_conversion.to_iso_639_1(main, lang_code)

    if lang_code_639_1 == 'zh_cn':
        lang_code_639_1 = 'zh'

    if lang_code in main.settings_global['stop_words']:
        word_list = main.settings_custom['stop_words']['stop_words'][lang_code]

        if word_list == 'NLTK':
            stop_words = nltk.corpus.stopwords.words(lang_text)
        elif word_list == 'Stopwords ISO':
            if lang_code_639_1 == 'zh_tw':
                with open(r'stop_words/Stopwords ISO/stopwords_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]
            else:
                with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                    stop_words = json.load(f)[lang_code_639_1]
        elif word_list == 'stopwords-json':
            if lang_code_639_1 == 'zh_tw':
                with open(r'stop_words/stopwords-json/stopwords_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]
            else:
                with open(r'stop_words/stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
                    stop_words = json.load(f)[lang_code_639_1]
        elif word_list == 'HanLP':
            if lang_code_639_1 == 'zh_tw':
                with open(r'stop_words/HanLP/stopwords_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]
            else:
                with open(r'stop_words/HanLP/stopwords.txt', 'r', encoding = 'utf_8') as f:
                    stop_words = [line.rstrip() for line in f]

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
