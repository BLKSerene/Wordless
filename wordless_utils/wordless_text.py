#
# Wordless: Text
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import json
import re

from bs4 import BeautifulSoup
import jieba
import nltk

from wordless_utils import wordless_conversion, wordless_distribution, wordless_misc

def wordless_word_tokenize(text, lang):
    tokens = []

    if lang == 'eng':
        tokens.extend(nltk.word_tokenize(text))
    elif lang in ['zho-cn', 'zho-tw']:
        tokens.extend(jieba.lcut(text))
    else:
        tokens.extend(nltk.word_tokenize(text))

    return tokens

def wordless_lemmatize(main, tokens, lang, lemmatizer = ''):
    lang_text = wordless_conversion.to_lang_text(main, lang)

    if lang_text in main.settings_global['lemmatizers']:
        lemmas = []

        if not lemmatizer:
            lemmatizer = main.settings_custom['lemmatization'][lang]

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
            lemma_list = {}

            with open('lemmatization/e_lemma.txt', 'r', encoding = 'utf_16') as f:
                for line in f:
                    if not line.startswith(';'):
                        lemma, words = line.rstrip().split('->')

                        for word in words.split(','):
                            lemma_list[word.strip()] = lemma.strip()

            lemmas = [lemma_list.get(token, token) for token in tokens]

        elif lemmatizer == 'Lemmatization Lists':
            lang = wordless_misc.convert_lang_code(main, lang)
            lemma_list = {}

            with open(f'lemmatization/Lemmatization Lists/lemmatization-{lang}.txt', 'r', encoding = 'utf_8') as f:
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

def wordless_filter_stop_words(main, tokens, lang_code):
    lang_text = wordless_conversion.to_lang_text(main, lang_code)
    lang_code_639_3 = lang_code
    lang_code_639_1 = wordless_conversion.to_iso_639_1(main, lang_code_639_3)

    if lang_text in main.settings_global['stop_words']:
        word_list = main.settings_custom['stop_words'][lang_code_639_3]

        if word_list == 'NLTK':
            if lang_text == 'Spanish (Castilian)':
                lang_text = 'Spanish'

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

        return [token for token in tokens if token not in stop_words]
    else:
        return tokens

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
                     case_sensitive, lemmatized_forms, whole_word, regex):
        tokens_matched = set()

        tokens = set(self.tokens)

        # Case sensitive
        if not case_sensitive:
            tokens_matched = set([token for token in tokens if token.lower() in search_terms])

        for search_term in search_terms:
            # Use regular expression & match whole word only
            if regex:
                if whole_word:
                    if search_term[:2] != r'\b':
                        search_term = r'\b' + search_term
                    if search_term[-2:] != r'\b':
                        search_term += r'\b'

                tokens_matched = set([token for token in tokens if re.search(search_term, token)])
            else:
                if whole_word:
                    tokens_matched.add(search_term)
                else:
                    for token in tokens:
                        if token.find(search_term) > -1:
                            tokens_matched.add(token)

            # Match all lemmatized forms
            if lemmatized_forms:
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

    def ngram(self, settings):
        search_terms = self.match_tokens(settings['search_terms'],
                                         settings['ignore_case'],
                                         settings['lemmatization'],
                                         settings['whole_word'],
                                         settings['regex'])

        if settings['ignore_case']:
            self.tokens = [token.lower() for token in self.tokens]

        if settings['lemmatization']:
            self.tokens = wordless_lemmatize(self.main, self.tokens, self.lang)

        if settings['punctuations'] == False:
            self.tokens = [token for token in self.tokens if token.isalnum()]

        if settings['allow_skipped_tokens'] == 0:
            ngrams = list(nltk.everygrams(self.tokens, settings['ngram_size_min'], settings['ngram_size_max']))
        else:
            ngrams = []

            for i in range(settings['ngram_size_min'], settings['ngram_size_max'] + 1):
                ngrams.extend(list(nltk.skipgrams(self.tokens, i, settings['allow_skipped_tokens'])))

        if settings['words']:
            if not settings['ignore_case']:
                if settings['lowercase'] == False:
                    ngrams = [ngram for ngram in ngrams if not all(map(str.islower, ngram))]
                if settings['uppercase'] == False:
                    ngrams = [ngram for ngram in ngrams if not all(map(str.isupper, ngram))]
                if settings['title_cased'] == False:
                    ngrams = [ngram for ngram in ngrams if not all(map(str.istitle, ngram))]
        else:
            ngrams = [ngram for ngram in ngrams if not all(map(str.isalpha, ngram))]

        if settings['numerals'] == False:
            ngrams = [ngram for ngram in ngrams if not all(map(str.isnumeric, ngram))]

        freq_distribution = wordless_distribution.Wordless_Freq_Distribution(ngrams)

        if not settings['show_all']:
            freq_distribution = {ngram: freq
                                 for ngram, freq in freq_distribution.items()
                                 for search_term in search_terms
                                 if search_term in ngram and
                                 settings['keyword_position_min'] <= ngram.index(search_term) + 1 <= settings['keyword_position_max']}

        freq_distribution = {self.word_delimiter.join(ngram): freq for ngram, freq in freq_distribution.items()}

        return freq_distribution

    def collocation(self, settings):
        search_terms = self.match_tokens(settings['search_terms'],
                                         settings['ignore_case'],
                                         settings['lemmatization'],
                                         settings['whole_word'],
                                         settings['regex'])

        if settings['ignore_case']:
            self.tokens = [token.lower() for token in self.tokens]

        if settings['lemmatization']:
            self.tokens = wordless_lemmatize(self.main, self.tokens, self.lang)

        if settings['punctuations'] == False:
            self.tokens = [token for token in self.tokens if token.isalnum()]

        if settings['search_for'] == self.main.tr('Bigrams'):
            finder = nltk.collocations.BigramCollocationFinder.from_words(self.tokens)
            assoc_measure = self.main.assoc_measures_bigram[settings['assoc_measure']]
        elif settings['search_for'] == self.main.tr('Trigrams'):
            finder = nltk.collocations.TrigramCollocationFinder.from_words(self.tokens)
            assoc_measure = self.main.assoc_measures_trigram[settings['assoc_measure']]
        elif settings['search_for'] == self.main.tr('Quadgrams'):
            finder = nltk.collocations.QuadgramCollocationFinder.from_words(self.tokens)
            assoc_measure = self.main.assoc_measures_quadgram[settings['assoc_measure']]

        score_distribution = {collocate: score for collocate, score in finder.score_ngrams(assoc_measure)}

        if not settings['show_all']:
            score_distribution = {collocate: score
                                  for collocate, score in score_distribution.items()
                                  for search_term in search_terms
                                  if search_term in collocate}

        score_distribution = {self.word_delimiter.join(collocate): score for collocate, score in score_distribution.items()}

        return score_distribution
