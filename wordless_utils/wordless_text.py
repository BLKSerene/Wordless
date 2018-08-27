#
# Wordless: Utility Functions for Texts
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#


import re

from bs4 import BeautifulSoup
import jieba
import nltk

from wordless_utils import wordless_misc, wordless_freq

def wordless_lemmatize(tokens, lang = 'en'):
    if lang == 'en':
        lemmatizer = nltk.WordNetLemmatizer()

        for i, (token, pos) in enumerate(nltk.pos_tag(tokens)):
            if pos in ['JJ', 'JJR', 'JJS']:
                tokens[i] = lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADJ)
            elif pos in ['NN', 'NNS', 'NNP', 'NNPS']:
                tokens[i] = lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.NOUN)
            elif pos in ['RB', 'RBR', 'RBS']:
                tokens[i] = lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.ADV)
            elif pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                tokens[i] = lemmatizer.lemmatize(token, pos = nltk.corpus.wordnet.VERB)
            else:
                tokens[i] = lemmatizer.lemmatize(token)

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
    def __init__(self, file):
        with open(file.path, 'r', encoding = file.encoding_code) as f:
            tokens = []

            for line in f:
                if file.ext in ['.txt']:
                    text = line.rstrip()
                elif file.ext in ['.htm', '.html']:
                    soup = BeautifulSoup(line.rstrip(), 'lxml')
                    text = soup.get_text()
                
                if file.lang_code == 'en':
                    tokens.extend(nltk.word_tokenize(text))
                elif file.lang_code in ['zh-cn', 'zh-tw']:
                    tokens.extend(jieba.lcut(text))

        super().__init__(tokens)

        self.lang = file.lang_code
        self.delimiter = file.delimiter

    def match_tokens(self, tokens_searched,
                     ignore_case, lemmatized_forms, whole_word, regex):
        tokens_matched = set()

        # Ignore Case
        if ignore_case:
            self._concordance_index = nltk.ConcordanceIndex(self.tokens, key=lambda s:s.lower())

            tokens_matched = set([token.lower() for token in tokens_searched])
        else:
            self._concordance_index = nltk.ConcordanceIndex(self.tokens)

        for token_searched in tokens_searched:
            # Regular Expression
            if regex:
                # Whole Word
                if whole_word:
                    if token_searched[:2] != r'\b':
                        token_searched = r'\b' + token_searched
                    if token_searched[-2:] != r'\b':
                        token_searched += r'\b'

                tokens_matched = set([token for token in self._concordance_index._offsets if re.search(token_searched, token)])
            else:
                # Whole Word
                if whole_word:
                    tokens_matched.add(token_searched)
                else:
                    for token in self._concordance_index._offsets:
                        if token.find(token_searched) > -1:
                            tokens_matched.add(token)

            # Lemmatized Forms
            if lemmatized_forms:
                for token_lemmatized in wordless_lemmatize(list(tokens_matched)):
                    tokens_matched.add(token_lemmatized)

                for token, token_lemmatized in zip(self._concordance_index._offsets, wordless_lemmatize(list(self._concordance_index._offsets))):
                    if token_lemmatized in tokens_matched:
                        tokens_matched.add(token)

        return tokens_matched

    def concordance_list(self, search_term, width, lines,
                         punctuations):
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

    def wordlist(self, words, lowercase, uppercase, title_cased, numerals, punctuations,
                 ignore_case, lemmatization):
        if ignore_case:
            self.tokens = [token.lower() for token in self.tokens]
        
        if lemmatization:
            self.tokens = wordless_lemmatize(self.tokens)
        
        if words:
            if not ignore_case:
                if lowercase == False:
                    self.tokens = [token for token in self.tokens if not token.islower()]
                if uppercase == False:
                    self.tokens = [token for token in self.tokens if not token.isupper()]
                if title_cased == False:
                    self.tokens = [token for token in self.tokens if not token.istitle()]
        else:
            self.tokens = [token for token in self.tokens if not token.isalpha()]
        
        if numerals == False:
            self.tokens = [token for token in self.tokens if not token.isnumeric()]
        if punctuations == False:
            self.tokens = [token for token in self.tokens if token.isalnum()]

        return sorted(wordless_freq.Wordless_Freq_Distribution(self.tokens).items(), key = lambda x: x[1], reverse = True)

    def ngrams(self, words, lowercase, uppercase, title_cased, numerals, punctuations,
               ignore_case, lemmatization,
               ngram_size_min, ngram_size_max):
        ngrams = []

        if ignore_case:
            self.tokens = [token.lower() for token in self.tokens]

        if lemmatization:
            self.tokens = wordless_lemmatize(self.tokens)

        if punctuations == False:
            self.tokens = [token for token in self.tokens if token.isalnum()]

        for degree in range(ngram_size_min, ngram_size_max + 1):
            for ngram in nltk.ngrams(self.tokens, degree):
                ngrams.append(ngram)

        if words:
            if not ignore_case:
                if lowercase == False:
                    ngrams = [ngram for ngram in ngrams if not all(map(str.islower, tokens))]
                if uppercase == False:
                    ngrams = [ngram for ngram in ngrams if not all(map(str.isupper, tokens))]
                if title_cased == False:
                    ngrams = [ngram for ngram in ngrams if not all(map(str.istitle, tokens))]
        else:
            ngrams = [ngram for ngram in ngrams if not all(map(str.isalpha, tokens))]

        if numerals == False:
            ngrams = [ngram for ngram in ngrams if not all(map(str.isnumeric, tokens))]

        ngrams = [self.delimiter.join(tokens) for tokens in ngrams]

        return sorted(wordless_freq.Wordless_Freq_Distribution(ngrams).items(), key = lambda x: x[1], reverse = True)

    def word_cluster(self, words, lowercase, uppercase, title_cased, numerals, punctuations,
                     ignore_case, lemmatization,
                     ngram_size_min, ngram_size_max,
                     search_terms, search_term_position_left, search_term_position_middle, search_term_position_right):
        freq_distribution = self.ngrams(words, lowercase, uppercase, title_cased, numerals, punctuations,
                                        ignore_case, lemmatization,
                                        ngram_size_min, ngram_size_max)

        freq_distribution = [(ngram, freq)
                             for ngram, freq in freq_distribution
                             for search_term in search_terms
                             if (ngram.startswith(search_term + self.delimiter) or
                                 ngram.find(self.delimiter + search_term + self.delimiter) > -1 or
                                 ngram.endswith(self.delimiter + search_term))]

        for search_term in search_terms:
            if search_term_position_left == False:
                freq_distribution = [(ngram, freq)
                                     for ngram, freq in freq_distribution
                                     if not ngram.startswith(search_term + self.delimiter)]

            if search_term_position_middle == False:
                freq_distribution = [(ngram, freq)
                                     for ngram, freq in freq_distribution
                                     if ngram.find(self.delimiter + search_term + self.delimiter) == -1]

            if search_term_position_right == False:
                freq_distribution = [(ngram, freq)
                                     for ngram, freq in freq_distribution
                                     if not ngram.endswith(self.delimiter + search_term)]

        return freq_distribution
