#
# Wordless: Text
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import collections
import json
import re

from bs4 import BeautifulSoup
import delphin.repp
import jieba
import jpype
import nltk

from wordless_utils import wordless_conversion

def wordless_sentence_tokenize(main, text, lang_code, sentence_tokenizer = 'Default'):
    if lang_code not in ['eng', 'ces', 'dan', 'nld', 'est', 'fin', 'fra', 'deu', 'ell', 'ita',
                         'nor', 'pol', 'por', 'slv', 'spa', 'swe', 'tur']:
        lang_code = 'eng'

    lang_text = wordless_conversion.to_lang_text(main, lang_code)

    return nltk.sent_tokenize(text, language = lang_text.lower())

def wordless_word_tokenize(main, text, lang_code, word_tokenizer = 'Default'):
    tokens = []

    if lang_code not in ['eng', 'zho_CN', 'zho_TW', 'ces', 'dan', 'nld', 'est', 'fin', 'fra', 'deu', 'ell', 'ita',
                         'nor', 'pol', 'por', 'slv', 'spa', 'swe', 'tur']:
        lang_code = 'other'

    if word_tokenizer == 'Default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang_code]

    if word_tokenizer.find('HanLP') > -1:
        import pyhanlp

    # English
    if word_tokenizer == main.tr('NLTK - Treebank Tokenizer'):
        sentences = wordless_sentence_tokenize(main, text, lang_code)

        for sentence in sentences:
            tokens.extend(nltk.TreebankWordTokenizer().tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
        sentences = wordless_sentence_tokenize(main, text, lang_code)

        for sentence in sentences:
            tokens.extend(nltk.ToktokTokenizer().tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
        sentences = wordless_sentence_tokenize(main, text, lang_code)

        for sentence in sentences:
            tokens.extend(nltk.casual_tokenize(sentence))
    elif word_tokenizer == main.tr('NLTK - Word Punctuation Tokenizer'):
        tokens = nltk.wordpunct_tokenize(text)
    elif word_tokenizer == main.tr('PyDelphin - Repp Tokenizer'):
        repp_tokenizer = delphin.repp.REPP.from_config('tokenization/repp_tokenizer/repp.set')
        sentences = wordless_sentence_tokenize(main, text, lang_code)

        for sentence in sentences:
            tokens.extend([token.form for token in repp_tokenizer.tokenize(text).tokens])
    elif word_tokenizer == main.tr('NLTK - Regular-Expression Tokenizer'):
        tokens = nltk.regexp_tokenize(text, main.settings_custom['word_tokenization']['regex_tokenizers'][lang_code], gaps = True)
    # Chinese
    elif word_tokenizer == main.tr('jieba (“结巴”中文分词) - With HMM'):
        tokens = jieba.cut(text)
    elif word_tokenizer == main.tr('jieba (“结巴”中文分词) - Without HMM'):
        tokens = jieba.cut(text, HMM = False)
    elif word_tokenizer == main.tr('HanLP - Standard Tokenizer'):
        standard_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')

        tokens = [token.word for token in standard_tokenizer.segment(text)]
    elif word_tokenizer == main.tr('HanLP - NLP Tokenizer'):
        nlp_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')

        tokens = [token.word for token in nlp_tokenizer.segment(text)]
    elif word_tokenizer == main.tr('HanLP - N-shortest Path Tokenizer'):
        NShortSegment = jpype.JClass('com.hankcs.hanlp.seg.NShort.NShortSegment')
        nshortest_tokenizer = NShortSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        tokens = [token.word for token in nshortest_tokenizer.seg(text)]
    elif word_tokenizer == main.tr('HanLP - Dijkstra Tokenizer'):
        DijkstraSegment = jpype.JClass('com.hankcs.hanlp.seg.Dijkstra.DijkstraSegment')
        dijkstra_tokenizer = DijkstraSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        tokens = [token.word for token in dijkstra_tokenizer.seg(text)]
    elif word_tokenizer == main.tr('HanLP - Viterbi Tokenizer'):
        ViterbiSegment = jpype.JClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')
        viterbi_tokenizer = ViterbiSegment().enableCustomDictionary(False).enablePlaceRecognize(True).enableOrganizationRecognize(True)

        tokens = [token.word for token in viterbi_tokenizer.seg(text)]
    elif word_tokenizer == main.tr('HanLP - CRF Tokenizer'):
        crf_tokenizer = jpype.JClass('com.hankcs.hanlp.model.crf.CRFLexicalAnalyzer')

        tokens = [token for token in crf_tokenizer().analyze(text).toWordArray()]
    elif word_tokenizer == main.tr('HanLP - High-speed Tokenizer'):
        highspeed_tokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.SpeedTokenizer')

        tokens = [token.word for token in highspeed_tokenizer.segment(text)]

    return tokens

def wordless_lemmatize(main, tokens, lang_code, lemmatizer = 'Default'):
    lemmas = []
    lemma_list = {}

    if lang_code in main.settings_global['lemmatizers']:
        if lemmatizer == 'Default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang_code]

        if lemmatizer == 'NLTK':
            lemmatizer_nltk = nltk.WordNetLemmatizer()

            for i, (token, pos) in enumerate(nltk.pos_tag(tokens)):
                if pos in ['JJ', 'JJR', 'JJS']:
                    lemmas.append(lemmatizer_nltk.lemmatize(token, pos = nltk.corpus.wordnet.ADJ))
                elif pos in ['NN', 'NNS', 'NNP', 'NNPS']:
                    lemmas.append(lemmatizer_nltk.lemmatize(token, pos = nltk.corpus.wordnet.NOUN))
                elif pos in ['RB', 'RBR', 'RBS']:
                    lemmas.append(lemmatizer_nltk.lemmatize(token, pos = nltk.corpus.wordnet.ADV))
                elif pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                    lemmas.append(lemmatizer_nltk.lemmatize(token, pos = nltk.corpus.wordnet.VERB))
                else:
                    lemmas.append(lemmatizer_nltk.lemmatize(token))
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

        return lemmas
    else:
        return tokens

def wordless_filter_stop_words(main, items, lang_code):
    lang_text = wordless_conversion.to_lang_text(main, lang_code)
    lang_code_639_3 = lang_code
    lang_code_639_1 = wordless_conversion.to_iso_639_1(main, lang_code_639_3)

    if lang_code_639_3 in main.settings_global['stop_words']:
        word_list = main.settings_custom['stop_words']['stop_words'][lang_code_639_3]

        if word_list == 'NLTK':
            stop_words = nltk.corpus.stopwords.words(lang_text)
        elif word_list == 'Stopwords ISO':
            if lang_code_639_1 == 'zh_cn':
                lang_code_639_1 = 'zh'

            with open(r'stop_words/Stopwords ISO/stopwords_iso.json', 'r', encoding = 'utf_8') as f:
                stop_words = json.load(f)[lang_code_639_1]
        elif word_list == 'stopwords-json':
            if lang_code_639_1 == 'zh_cn':
                lang_code_639_1 = 'zh'

            with open(r'stop_words/stopwords-json/stopwords-all.json', 'r', encoding = 'utf_8') as f:
                stop_words = json.load(f)[lang_code_639_1]

        if type(items[0]) == str:
            items_filtered = [token for token in items if token not in stop_words]
        elif type(items[0]) in [list, tuple, set]:
            items_filtered = [ngram for ngram in items if not [token for token in ngram if token in stop_words]]

        return items_filtered
    else:
        return items

# Overload to fix a bug for left_context
def find_concordance(self, word, width=80, lines=25):
    """
    Find the concordance lines given the query word.
    """
    half_width = (width - len(word) - 2) // 2
    context = width // 4  # approx number of words of context

    # Find the instances of the word to create the ConcordanceLine
    concordance_list = []
    offsets = self.offsets(word)
    if offsets:
        for i in offsets:
            query_word = self._tokens[i]
            # Find the context of query word.
            left_context = self._tokens[max(0, i-context):i]
            right_context = self._tokens[i+1:i+context]
            # Create the pretty lines with the query_word in the middle.
            left_print= ' '.join(left_context)[-half_width:]
            right_print = ' '.join(right_context)[:half_width]
            # The WYSIWYG line of the concordance.
            line_print = ' '.join([left_print, query_word, right_print])
            # Create the ConcordanceLine
            concordance_line = nltk.text.ConcordanceLine(left_context, query_word,
                                                         right_context, i,
                                                         left_print, right_print, line_print)
            concordance_list.append(concordance_line)
    return concordance_list[:lines]

nltk.ConcordanceIndex.find_concordance = find_concordance

class Wordless_Text(nltk.Text):
    def __init__(self, main, file):
        tokens = []

        with open(file['path'], 'r', encoding = file['encoding_code']) as f:
            for line in f:
                if file['ext_code'] in ['.txt']:
                    text = line.rstrip()
                elif file['ext_code'] in ['.htm', '.html']:
                    soup = BeautifulSoup(line.rstrip(), 'lxml')
                    text = soup.get_text()

                tokens.extend(wordless_word_tokenize(text, file['lang_code']))

        super().__init__(tokens)

        self.main = main
        self.lang = file['lang_code']
        self.word_delimiter = file['word_delimiter']

    def match_tokens(self, search_terms,
                     ignore_case, match_inflected_forms, match_whole_word, use_regex):
        tokens_matched = set()

        tokens = set(self.tokens)

        # Ignore case
        if ignore_case:
            tokens_matched = set([token for token in tokens if token.lower() in search_terms])

        for search_term in search_terms:
            # Use regular expression & match whole word only
            if use_regex:
                if match_whole_word:
                    if search_term[:2] != r'\b':
                        search_term = r'\b' + search_term
                    if search_term[-2:] != r'\b':
                        search_term += r'\b'

                tokens_matched = set([token for token in tokens if re.search(search_term, token)])
            else:
                if match_whole_word:
                    tokens_matched.add(search_term)
                else:
                    for token in tokens:
                        if token.find(search_term) > -1:
                            tokens_matched.add(token)

            # Match all inflected forms
            if match_inflected_forms:
                for token_lemmatized in wordless_lemmatize(self.main, list(tokens_matched), self.lang):
                    tokens_matched.add(token_lemmatized)

                for token, token_lemmatized in zip(tokens, wordless_lemmatize(self.main, tokens, self.lang)):
                    if token_lemmatized in tokens_matched:
                        tokens_matched.add(token)

        return tokens_matched

    def concordance_list(self, search_term, width, lines, punctuations):
        concordance_results = self._concordance_index.find_concordance(search_term, width, lines)

        # Punctuations
        if not punctuations:
            for i, concordance_line in enumerate(concordance_results):
                for j, token in reversed(list(enumerate(concordance_line.left))):
                    if not any(map(str.isalnum, token)):
                        if j == 0:
                            del concordance_line.left[j]
                        else:
                            concordance_line.left[j - 1:j + 1] = ['{} {}'.format(concordance_line.left[j - 1], token)]

                for j, token in reversed(list(enumerate(concordance_line.right))):
                    if not any(map(str.isalnum, token)):
                        if j == 0:
                            concordance_results[i] = nltk.text.ConcordanceLine(concordance_line.left,
                                                                               concordance_line.query + token,
                                                                               concordance_line.right,
                                                                               concordance_line.offset,
                                                                               concordance_line.left_print,
                                                                               concordance_line.right_print,
                                                                               concordance_line.line)
                        else:
                            concordance_line.right[j - 1:j + 1] = ['{} {}'.format(concordance_line.right[j - 1], token)]

        # Check for empty context
        concordance_results = sorted(concordance_results, key = lambda x: x.offset)
        if concordance_results[0].left == []:
            concordance_results[0] = nltk.text.ConcordanceLine(['<Start of File>'],
                                                               concordance_results[0].query,
                                                               concordance_results[0].right,
                                                               concordance_results[0].offset,
                                                               '<Start of File>',
                                                               concordance_results[0].right_print,
                                                               concordance_results[0].line)
        if concordance_results[-1].right == []:
            concordance_results[-1] = nltk.text.ConcordanceLine(concordance_results[-1].left,
                                                                concordance_results[-1].query,
                                                                ['<End of File>'],
                                                                concordance_results[-1].offset,
                                                                concordance_results[-1].left_print,
                                                                '<End of File>',
                                                                concordance_results[-1].line)

        return concordance_results
