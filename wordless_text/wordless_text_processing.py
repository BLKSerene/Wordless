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

from wordless_checking import wordless_checking_unicode
from wordless_text import wordless_matching, wordless_text
from wordless_utils import wordless_conversion

def check_spacy_models(main, lang):
    if f'spacy_nlp_{lang}' not in main.__dict__:
        # Dutch
        if lang == 'nld':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('nl_core_news_sm')
        # English
        elif lang == 'eng':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('en_core_web_sm')
        # French
        elif lang == 'fra':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('fr_core_news_sm')
        # German
        elif lang == 'deu':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('de_core_news_sm')
        # Italian
        elif lang == 'ita':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('it_core_news_sm')
        # Portuguese
        elif lang == 'por':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('pt_core_news_sm')
        # Spanish
        elif lang == 'spa':
            main.__dict__[f'spacy_nlp_{lang}'] = spacy.load('es_core_news_sm')

def wordless_sentence_tokenize(main, text, lang,
                               sentence_tokenizer = 'default'):
    sentences = []
    boundary_start = 0

    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    # English
    if sentence_tokenizer == main.tr('NLTK - Punkt Sentence Tokenizer'):
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang in ['nob', 'nno']:
            lang_text = 'norwegian'
        # Other Languages
        elif lang == 'other':
            lang_text = 'english'
        else:
            lang_text = wordless_conversion.to_lang_text(main, lang).lower()

        for line in text.splitlines():
            sentences.extend(nltk.sent_tokenize(line, language = lang_text))
    elif 'spaCy' in sentence_tokenizer:
        check_spacy_models(main, lang)

        nlp = main.__dict__[f'spacy_nlp_{lang}']

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

def wordless_word_tokenize(main, sentences, lang,
                           word_tokenizer = 'default'):
    token_groups = []

    if type(sentences) != list:
        sentences = [sentences]

    for i, sentence in enumerate(sentences):
        if type(sentence) != wordless_text.Wordless_Token:
            sentences[i] = wordless_text.Wordless_Token(sentence)

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

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
        moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

        for sentence in sentences:
            token_groups.append(moses_tokenizer.tokenize(sentence))
    elif word_tokenizer == main.tr('SacreMoses - Penn Treebank Tokenizer'):
        moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

        for sentence in sentences:
            token_groups.append(moses_tokenizer.penn_tokenize(sentence))
    elif 'spaCy' in word_tokenizer:
        # Languages with models
        if lang in ['nld', 'eng', 'fra', 'deu', 'ita', 'por', 'spa', 'other']:
            # Other Languages
            if lang == 'other':
                lang = 'eng'

            check_spacy_models(main, lang)

            nlp = main.__dict__[f'spacy_nlp_{lang}']

            for sentence in sentences:
                token_groups.append([token.text for token in nlp(str(sentence))])
        # Languages without models
        else:
            nlp = spacy.blank(wordless_conversion.to_iso_639_1(main, lang))

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
                        # Japanese Kana
                        elif wordless_checking_unicode.is_kana(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 == len(sentence) or not wordless_checking_unicode.is_kana(sentence[i + j + 1]):
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                         lang = 'jpn',
                                                                         word_tokenizer = main.tr('nagisa - Japanese Word Tokenizer')))

                                    non_han_start = i + j + 1

                                    break
                        # Thai
                        elif wordless_checking_unicode.is_thai(char):
                            for j, char in enumerate(sentence[i:]):
                                if i + j + 1 == len(sentence) or not wordless_checking_unicode.is_thai(sentence[i + j + 1]):
                                    tokens.extend(wordless_word_tokenize(main, sentence[non_han_start : i + j + 1],
                                                                         lang = 'tha'))

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
    if lang in ['zho_cn', 'zho_tw', 'jpn', 'tha']:
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

    # Remove empty tokens and strip whitespace
    tokens = [token.strip()
              for tokens in token_groups
              for token in tokens
              if not re.search(r'^\s*$', token)]

    return tokens

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
    # Chinese & Japanese
    elif (word_detokenizer == main.tr('Wordless - Chinese Word Detokenizer') or
          word_detokenizer == main.tr('Wordless - Japanese Word Detokenizer')):
        # Settings - > Word Detokenization
        if type(tokens[0]) == str:
            non_cjk_start = 0

            for i, token in enumerate(tokens):
                if i >= non_cjk_start:
                    if wordless_checking_unicode.has_han(token) or wordless_checking_unicode.has_kana(token):
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
                        # Thai
                        elif wordless_checking_unicode.has_thai(token):
                            for j, token in enumerate(tokens[i:]):
                                if i + j + 1 == len(tokens) or not wordless_checking_unicode.has_thai(tokens[i + j + 1]):
                                    text += wordless_word_detokenize(main, tokens[non_cjk_start : i + j + 1],
                                                                     lang = 'tha')

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

def wordless_pos_tag(main, tokens, lang,
                     pos_tagger = 'default',
                     tagset = 'custom'):
    tokens_tagged = []

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    # Chinese
    if pos_tagger == main.tr('jieba - Chinese POS Tagger'):
        tokens_tagged = jieba.posseg.cut(' '.join(tokens))

    # Dutch, English, French, German, Italian, Portuguese and Spanish
    elif 'spaCy' in pos_tagger:
        check_spacy_models(main, lang)

        nlp = main.__dict__[f'spacy_nlp_{lang}']

        tokens_tagged = [(token.text, token.tag_) for token in nlp(' '.join(tokens))]

    # English & Russian
    elif pos_tagger == main.tr('NLTK - Perceptron POS Tagger'):
        tokens_tagged = nltk.pos_tag(tokens, lang = lang)

    # Japanese
    elif pos_tagger == main.tr('nagisa - Japanese POS Tagger'):
        import nagisa

        tagged_tokens = nagisa.tagging(' '.join(tokens))

        tokens_tagged = zip(tagged_tokens.words, tagged_tokens.postags)

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
        if 'pybo_bo_tokenizer' not in main.__dict__:
            main.pybo_bo_tokenizer = pybo.BoTokenizer('POS')

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
                     if not re.search(r'^\s*$', token)]

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

    re_tags_all = wordless_matching.get_re_tags(main, tags = 'all')
    re_tags_pos = wordless_matching.get_re_tags(main, tags = 'pos')
    re_tags_non_pos = wordless_matching.get_re_tags(main, tags = 'non_pos')

    # Record empty tokens
    for i, token in enumerate(tokens):
        if re.search(r'^\s*$', token):
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

        # English & Other Languages
        if 'spaCy' in lemmatizer:
            check_spacy_models(main, lang)

            nlp = main.__dict__[f'spacy_nlp_{lang}']

            for token in tokens:
                doc = nlp(str(token))

                if doc:
                    lemmas.append(doc[0].lemma_)
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
            if 'pybo_bo_tokenizer' not in main.__dict__:
                main.pybo_bo_tokenizer = pybo.BoTokenizer('POS')

            for token in tokens:
                for token in main.pybo_bo_tokenizer.tokenize(token):
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
                            word_list = 'default'):
    if word_list == 'default':
        word_list = main.settings_custom['stop_words']['stop_words'][lang]

    lang_639_1 = wordless_conversion.to_iso_639_1(main, lang)

    # Chinese (Simplified)
    if lang_639_1 == 'zh_cn':
        lang_639_1 = 'zh'

    if 'Stopwords ISO' in word_list:
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
    elif 'spaCy' in word_list:
        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            with open(r'stop_words/spaCy/stop_words_zh_tw.txt', 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            spacy_lang = importlib.import_module(f'spacy.lang.{lang_639_1}')

            stop_words = spacy_lang.STOP_WORDS
    elif 'NLTK' in word_list:
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang_639_1 in ['nb', 'nn']:
            lang_639_1 = 'no'

        lang_text = wordless_conversion.to_lang_text(main, lang)

        # Greek (Modern)
        if lang_text == main.tr('Greek (Modern)'):
            lang_text = main.tr('Greek')

        stop_words = nltk.corpus.stopwords.words(lang_text)
    # Greek (Ancient)
    elif word_list == main.tr('grk-stoplist - Greek (Ancient) Stop Words'):
        with open(r'stop_words/grk-stoplist/stoplist-greek.txt', 'r', encoding = 'utf_8') as f:
            stop_words = [line.rstrip() for line in f.readlines()]
    # Thai
    elif word_list == main.tr('PyThaiNLP - Thai Stop Words'):
        stop_words = pythainlp.corpus.stopwords.words('thai')
    # Custom Lists
    elif word_list == main.tr('Custom List'):
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
