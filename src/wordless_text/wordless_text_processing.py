#
# Wordless: Text - Text Processing
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import importlib
import json
import re

# See Sacremoses/Issue #61: https://github.com/alvations/sacremoses/issues/61#issuecomment-516618565
import sre_parse
sre_parse._uniq = lambda x: list(dict.fromkeys(x))

import jieba
import jieba.posseg
import nltk
import nltk.tokenize.nist
import pymorphy2
import pythainlp
import razdel
import sacremoses
import spacy
import syntok.segmenter
import underthesea

from wordless_checking import wordless_checking_token, wordless_checking_unicode
from wordless_text import wordless_matching, wordless_text, wordless_text_utils
from wordless_utils import wordless_conversion, wordless_misc

# Reference: https://stackoverflow.com/questions/9506869/are-there-character-collections-for-all-international-full-stop-punctuations/9508766#9508766
TERMINATORS_SENTENCE = [
    '!', '.', '?', '։', '؟', '۔', '܀', '܁', '܂', '߹',
    '।', '॥', '၊', '။', '።', '፧', '፨', '᙮', '᜵', '᜶', '᠃', '᠉', '᥄',
    '᥅', '᪨', '᪩', '᪪', '᪫', '᭚', '᭛', '᭞', '᭟', '᰻', '᰼', '᱾', '᱿',
    '‼', '‽', '⁇', '⁈', '⁉', '⸮', '⸼', '꓿', '꘎', '꘏', '꛳', '꛷', '꡶',
    '꡷', '꣎', '꣏', '꤯', '꧈', '꧉', '꩝', '꩞', '꩟', '꫰', '꫱', '꯫', '﹒',
    '﹖', '﹗', '！', '．', '？', '𐩖', '𐩗', '𑁇', '𑁈', '𑂾', '𑂿', '𑃀',
    '𑃁', '𑅁', '𑅂', '𑅃', '𑇅', '𑇆', '𑇍', '𑇞', '𑇟', '𑈸', '𑈹', '𑈻', '𑈼',
    '𑊩', '𑑋', '𑑌', '𑗂', '𑗃', '𑗉', '𑗊', '𑗋', '𑗌', '𑗍', '𑗎', '𑗏', '𑗐',
    '𑗑', '𑗒', '𑗓', '𑗔', '𑗕', '𑗖', '𑗗', '𑙁', '𑙂', '𑜼', '𑜽', '𑜾', '𑩂',
    '𑩃', '𑪛', '𑪜', '𑱁', '𑱂', '𖩮', '𖩯', '𖫵', '𖬷', '𖬸', '𖭄', '𛲟', '𝪈']
TERMINATORS_CLAUSE = [
    # Question and exclamation marks
    '?', '!', '？', '！',
    # Commas, colons, semi-colons
    ',', ':', ';',
    # Em dashes
    '—', '—'
]

def wordless_sentence_tokenize(main, text, lang,
                               sentence_tokenizer = 'default'):
    sentences = []

    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    wordless_text_utils.check_sentence_tokenizers(main,
                                                  lang = lang,
                                                  sentence_tokenizer = sentence_tokenizer)

    # NLTK
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
            'rus': 'russian',
            'slv': 'slovene',
            'spa': 'spanish',
            'swe': 'swedish',
            'tur': 'turkish',
            # Other languages
            'other': 'english'
        }

        sentences = nltk.sent_tokenize(text, language = lang_texts[lang])
    # spaCy
    elif sentence_tokenizer == main.tr('spaCy - Sentencizer'):
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)
        # See Issue #3479: https://github.com/explosion/spaCy/issues/3479
        doc.is_parsed = True

        sentences = [sentence.text for sentence in doc.sents]
    # syntok
    elif sentence_tokenizer == main.tr('syntok - Sentence Segmenter'):
        for para in syntok.segmenter.analyze(text):
            for sentence in para:

                sentences.append(''.join([token.spacing + token.value for token in sentence]))
    # Chinese & Japanese
    elif sentence_tokenizer in [main.tr('Wordless - Chinese Sentence Tokenizer'),
                                main.tr('Wordless - Japanese Sentence Tokenizer')]:
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
    # Russian
    elif sentence_tokenizer == main.tr('razdel - Russian Sentenizer'):
        sentences = [sentence.text for sentence in razdel.sentenize(text)]
    # Thai
    elif sentence_tokenizer == main.tr('PyThaiNLP - Thai Sentence Tokenizer'):
        sentences = pythainlp.tokenize.sent_tokenize(text)
    # Tibetan
    elif sentence_tokenizer == main.tr('Wordless - Tibetan Sentence Tokenizer'):
        sentences = text.split()
    # Vietnamese
    elif sentence_tokenizer == main.tr('Underthesea - Vietnamese Sentence Tokenizer'):
        sentences = underthesea.sent_tokenize(text)

    # Strip spaces
    sentences = [sentence.strip() for sentence in sentences]

    sentences = wordless_text_utils.record_boundary_sentences(sentences, text)

    return sentences

def wordless_sentence_split(main, text):
    sentences = []
    sentence_start = 0

    tokens = text.split()
    len_tokens = len(tokens)

    for i, token in enumerate(tokens):
        if token[-1] in TERMINATORS_SENTENCE or i == len_tokens - 1:
            sentences.append(' '.join(tokens[sentence_start : i + 1]))

            sentence_start = i + 1

    return sentences

def wordless_clause_tokenize(main, text, lang):
    clauses = []

    # Running text
    if type(text) in [str, wordless_text.Wordless_Token]:
        clause_start = 0
        len_text = len(text)

        for i, char in enumerate(text):
            if i >= clause_start:
                if i == len_text - 1:
                    clauses.append(text[clause_start:])
                else:
                    if char in TERMINATORS_CLAUSE:
                        for j, char in enumerate(text[i + 1:]):
                            if char not in TERMINATORS_CLAUSE:
                                clauses.append(text[clause_start : i + j + 1])

                                clause_start = i + j + 1

                                break
    # Tokens
    elif type(text) in [list, tuple, dict]:
        clause_start = 0
        len_text = len(text)

        for i, token in enumerate(text):
            if i >= clause_start:
                if i == len_text - 1:
                    clauses.append(text[clause_start:])
                else:
                    # Check if the token is empty
                    if token and token[-1] in TERMINATORS_CLAUSE:
                        for j, token in enumerate(text[i + 1:]):
                            if token[0] not in TERMINATORS_CLAUSE:
                                clauses.append(text[clause_start : i + j + 1])

                                clause_start = i + j + 1

                                break
    else:
        raise Exception('Input for clause tokenization must be a string of text or a list of tokens!')

    return clauses

def wordless_clause_split(main, text):
    clauses = []
    clause_start = 0

    tokens = text.split()
    len_tokens = len(tokens)

    for i, token in enumerate(tokens):
        if token[-1] in TERMINATORS_CLAUSE or i == len_tokens - 1:
            clauses.append(' '.join(tokens[clause_start : i + 1]))

            clause_start = i + 1

    return clauses

def wordless_word_tokenize(main, text, lang,
                           word_tokenizer = 'default',
                           flat_tokens = True):
    tokens_hierarchical = []

    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    # Check initialization status of word (and sentence) tokenizers
    if flat_tokens:
        wordless_text_utils.check_word_tokenizers(main,
                                                  lang = lang,
                                                  word_tokenizer = word_tokenizer)
    else:
        wordless_text_utils.check_tokenizers(main,
                                             lang = lang,
                                             word_tokenizer = word_tokenizer)

    # NLTK
    if 'NLTK' in word_tokenizer:
        sentences = wordless_sentence_tokenize(main, text, lang)

        if word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
            treebank_tokenizer = nltk.TreebankWordTokenizer()

            for sentence in sentences:
                tokens_hierarchical.append(treebank_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
            tweet_tokenizer = nltk.TweetTokenizer()

            for sentence in sentences:
                tokens_hierarchical.append(tweet_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
            nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()

            for sentence in sentences:
                tokens_hierarchical.append(nist_tokenizer.tokenize(sentence))
        elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
            toktok_tokenizer = nltk.ToktokTokenizer()

            for sentence in sentences:
                tokens_hierarchical.append(toktok_tokenizer.tokenize(sentence))
    # Sacremoses
    elif 'Sacremoses' in word_tokenizer:
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wordless_sentence_tokenize(main, text, lang)

        if word_tokenizer == main.tr('Sacremoses - Moses Tokenizer'):
            moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

            for sentence in sentences:
                tokens_hierarchical.append(moses_tokenizer.tokenize(sentence, escape = False))
        elif word_tokenizer == main.tr('Sacremoses - Penn Treebank Tokenizer'):
            moses_tokenizer = sacremoses.MosesTokenizer(lang = wordless_conversion.to_iso_639_1(main, lang))

            for sentence in sentences:
                tokens_hierarchical.append(moses_tokenizer.penn_tokenize(sentence))
    # spaCy
    elif 'spaCy' in word_tokenizer:
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)
        # See Issue #3479: https://github.com/explosion/spaCy/issues/3479
        doc.is_parsed = True

        if flat_tokens:
            tokens_hierarchical.append([token.text for token in doc])
        else:
            for sentence in doc.sents:
                tokens_hierarchical.append([token.text for token in sentence.as_doc()])
    # syntok
    elif word_tokenizer == 'syntok - Word Tokenizer':
        syntok_tokenizer = syntok.tokenizer.Tokenizer()

        if flat_tokens:
            tokens_hierarchical.append([token.value for token in syntok_tokenizer.tokenize(text)])
        else:
            for para in syntok.segmenter.analyze(text):
                for sentence in para:
                    tokens_hierarchical.append([token.value for token in sentence])
    # Chinese & Japanese
    elif ('jieba' in word_tokenizer or
          'nagisa' in word_tokenizer or
          'Wordless' in word_tokenizer):
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wordless_sentence_tokenize(main, text, lang = lang)

        # Chinese
        if word_tokenizer == main.tr('jieba - Chinese Word Tokenizer'):
            for sentence in sentences:
                tokens_hierarchical.append(jieba.cut(sentence))
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

                tokens_hierarchical.append(tokens)
        # Japanese
        elif word_tokenizer == main.tr('nagisa - Japanese Word Tokenizer'):
            import nagisa

            for sentence in sentences:
                tokens_hierarchical.append(nagisa.tagging(str(sentence)).words)
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

                tokens_hierarchical.append(tokens)
    # Russian
    elif word_tokenizer == 'razdel - Russian Word Tokenizer':
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wordless_sentence_tokenize(main, text, lang = 'rus')

        for sentence in sentences:
            tokens_hierarchical.append([token.text for token in razdel.tokenize(sentence)])
    # Thai
    elif 'PyThaiNLP' in word_tokenizer:
        # Preserve sentence boundaries
        sentences = wordless_sentence_tokenize(main, text, lang = 'tha',
                                               sentence_tokenizer = 'PyThaiNLP - Thai Sentence Tokenizer')

        if word_tokenizer == main.tr('PyThaiNLP - Maximum Matching Algorithm + TCC'):
            for sentence in sentences:
                tokens_hierarchical.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'newmm'))
        elif word_tokenizer == main.tr('PyThaiNLP - Maximum Matching Algorithm'):
            for sentence in sentences:
                tokens_hierarchical.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'mm'))
        elif word_tokenizer == main.tr('PyThaiNLP - Longest Matching'):
            for sentence in sentences:
                tokens_hierarchical.append(pythainlp.tokenize.word_tokenize(sentence, engine = 'longest-matching'))
    # Tibetan
    elif 'botok' in word_tokenizer:
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wordless_sentence_tokenize(main, text, lang = 'bod')

        botok_tokenizer = wordless_text_utils.check_botok_tokenizers(main, word_tokenizer)

        for sentence in sentences:
            tokens_hierarchical.append([token.text for token in botok_tokenizer.tokenize(sentence)])
    # Vietnamese
    elif word_tokenizer == main.tr('Underthesea - Vietnamese Word Tokenizer'):
        if flat_tokens:
            sentences = [text]
        else:
            sentences = wordless_sentence_tokenize(main, text, lang = 'vie',
                                                   sentence_tokenizer = 'Underthesea - Vietnamese Sentence Tokenizer')

        for sentence in sentences:
            tokens_hierarchical.append(underthesea.word_tokenize(str(sentence)))

    # Remove empty tokens and strip whitespace
    for i, sentence in enumerate(tokens_hierarchical):
        tokens_hierarchical[i] = [token.strip()
                                  for token in sentence
                                  if token.strip()]

    # Record token boundaries
    if lang in ['zho_cn', 'zho_tw', 'jpn']:
        for sentence in tokens_hierarchical:
            if sentence:
                sentence[-1] = wordless_text.Wordless_Token(sentence[-1], boundary = '', sentence_ending = True)
    else:
        for sentence in tokens_hierarchical:
            if sentence:
                sentence[-1] = wordless_text.Wordless_Token(sentence[-1], boundary = ' ', sentence_ending = True)

    # Clause tokenization
    if not flat_tokens:
        for i, sentence in enumerate(tokens_hierarchical):
            tokens_hierarchical[i] = wordless_clause_tokenize(main, sentence, lang)

    # Flatten tokens
    tokens_flat = list(wordless_misc.flatten_list(tokens_hierarchical))

    if flat_tokens:
        return tokens_flat
    else:
        return tokens_hierarchical

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
    elif word_detokenizer == main.tr('Sacremoses - Moses Detokenizer'):
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
            if i < non_cjk_start:
                continue

            if (wordless_checking_unicode.has_han(token) or
                wordless_checking_unicode.has_kana(token) or
                all(map(str.isnumeric, token))):
                text += token

                non_cjk_start = i + 1
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
        non_thai_start = 0

        for i, token in enumerate(tokens):
            if i < non_thai_start:
                continue

            if wordless_checking_unicode.has_thai(token):
                if type(token) == wordless_text.Wordless_Token:
                    text += token + token.boundary
                else:
                    text += token

                non_thai_start = i + 1
            else:
                # English
                if wordless_checking_unicode.is_eng_token(token):
                    for j, token in enumerate(tokens[i:]):
                        if i + j + 1 == len(tokens) or not wordless_checking_unicode.is_eng_token(tokens[i + j + 1]):
                            text += wordless_word_detokenize(main, tokens[non_thai_start : i + j + 1],
                                                             lang = 'eng')

                            non_thai_start = i + j + 1

                            break
                # Other Languages
                else:
                    for j, token in enumerate(tokens[i:]):
                        if (i + j + 1 == len(tokens) or
                            wordless_checking_unicode.has_thai(tokens[i + j + 1])):
                            text += wordless_word_detokenize(main, tokens[non_thai_start : i + j + 1],
                                                             lang = 'other')

                            non_thai_start = i + j + 1

                            break
    # Tibetan
    elif word_detokenizer == main.tr('Wordless - Tibetan Word Detokenizer'):
        non_tibetan_start = 0

        for i, token in enumerate(tokens):
            if i < non_tibetan_start:
                continue

            if wordless_checking_unicode.has_tibetan(token):
                # Check for Tibetan Mark Shad
                # See: https://w3c.github.io/tlreq/#section_breaks
                if i > 0 and token[0] == '།':
                    text += token
                else:
                    text += token

                non_tibetan_start = i + 1
            else:
                # English
                if wordless_checking_unicode.is_eng_token(token):
                    for j, token in enumerate(tokens[i:]):
                        if i + j + 1 == len(tokens) or not wordless_checking_unicode.is_eng_token(tokens[i + j + 1]):
                            text += wordless_word_detokenize(main, tokens[non_tibetan_start : i + j + 1],
                                                             lang = 'eng')

                            non_tibetan_start = i + j + 1

                            break
                # Other Languages
                else:
                    for j, token in enumerate(tokens[i:]):
                        if (i + j + 1 == len(tokens) or
                            wordless_checking_unicode.has_tibetan(tokens[i + j + 1])):
                            text += wordless_word_detokenize(main, tokens[non_tibetan_start : i + j + 1],
                                                             lang = 'other')

                            non_tibetan_start = i + j + 1

                            break

    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()

def wordless_pos_tag(main, tokens, lang,
                     pos_tagger = 'default',
                     tagset = 'custom'):
    tokens_tagged = []

    # Check if the first token is empty
    if tokens and tokens[0] == '':
        first_token_empty = True
    else:
        first_token_empty = False

    tokens = [str(token) for token in tokens if token]

    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    wordless_text_utils.check_pos_taggers(main,
                                          lang = lang,
                                          pos_tagger = pos_tagger)

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
    elif pos_tagger == main.tr('botok - Tibetan POS Tagger'):
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

        botok_tokenizer = wordless_text_utils.check_botok_tokenizers(main,
                                                                     word_tokenizer = word_tokenizer)
        tokens = botok_tokenizer.tokenize(' '.join(tokens))

        for token in tokens:
            if token.pos:
                tokens_tagged.append((token.text, token.pos))
            else:
                tokens_tagged.append((token.text, token.chunk_type))

    # Vietnamese
    elif pos_tagger == main.tr('Underthesea - Vietnamese POS Tagger'):
        tokens_tagged = underthesea.pos_tag(' '.join(tokens))

    # Convert to Universal Tagset
    if (tagset == 'custom' and main.settings_custom['pos_tagging']['to_universal_pos_tags'] or
        tagset == 'universal'):

        mappings = {tag: tag_universal
                    for tag, tag_universal, _, _ in main.settings_custom['tagsets']['mappings'][lang][pos_tagger]}
        tokens_tagged = list(tokens_tagged)

        # Issue warnings if any tag is missing from the mapping table
        for _, tag in tokens_tagged:
            if tag not in mappings:
                print(f'Warning: tag "{tag}" is missing from the {wordless_conversion.to_lang_text(main, lang)} mapping table!')

        tokens_tagged = [(token, mappings.get(tag, 'X'))
                         for token, tag in tokens_tagged]

    # Strip empty tokens and strip whitespace in tokens
    tokens_tagged = [(token.strip(), tag)
                     for token, tag in tokens_tagged
                     if token.strip()]

    # Add the first empty token (if any)
    if first_token_empty:
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

    # Record empty tokens
    for i, token in reversed(list(enumerate(tokens))):
        if not token.strip():
            empty_offsets.append(i)

            tokens.remove(token)

    wordless_text_utils.check_lemmatizers(main, lang)

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
            with open(wordless_misc.get_normalized_path('lemmatization/lemmalist-greek/lemmalist-greek.txt'), 'r', encoding = 'utf_8') as f:
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
        elif lemmatizer == main.tr('botok - Tibetan Lemmatizer'):
            word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

            botok_tokenizer = wordless_text_utils.check_botok_tokenizers(main,
                                                                         word_tokenizer = word_tokenizer)
            tokens = botok_tokenizer.tokenize(' '.join(tokens))

            for token in tokens:
                if token.lemma:
                    lemmas.append(token.lemma)
                else:
                    lemmas.append(token.text)
        # Other Languages
        elif 'Lemmatization Lists' in lemmatizer:
            lang = wordless_conversion.to_iso_639_1(main, lang)

            with open(wordless_misc.get_normalized_path(f'lemmatization/Lemmatization Lists/lemmatization-{lang}.txt'), 'r', encoding = 'utf_8_sig') as f:
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
    for empty_offset in sorted(empty_offsets):
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

    # extra-stopwords
    if 'extra-stopwords' in list_stop_words:
        LANG_TEXTS = {
            'sqi': 'albanian',
            'ara': 'arabic',
            'hye': 'armenian',
            'eus': 'basque',
            'bel': 'belarusian',
            'ben': 'bengali',
            'bul': 'bulgarian',
            'cat': 'catalan',
            'zho_cn': 'chinese',
            # Chinese (Traditional)
            'zho_tw': 'chinese-traditional',
            'hrv': 'croatian',
            'ces': 'czech',
            'dan': 'danish',
            'nld': 'dutch',
            'eng': 'english',
            'est': 'estonian',
            'fin': 'finnish',
            'fra': 'french',
            'glg': 'galician',
            'deu': 'german',
            'ell': 'greek',
            'hau': 'hausa',
            'heb': 'hebrew',
            'hin': 'hindi',
            'hun': 'hungarian',
            'isl': 'icelandic',
            'ind': 'indonesian',
            'gle': 'irish',
            'ita': 'italian',
            'jpn': 'japanese',
            'kor': 'korean',
            'kur': 'kurdish',
            'lav': 'latvian',
            'lit': 'lithuanian',
            'msa': 'malay',
            'mar': 'marathi',
            'mon': 'mongolian',
            'nep': 'nepali',
            # Norwegian Bokmål & Norwegian Nynorsk
            'nob': 'norwegian',
            'nno': 'norwegian',
            'fas': 'persian',
            'pol': 'polish',
            'por': 'portuguese',
            'ron': 'romanian',
            'rus': 'russian',
            'srp_cyrl': 'serbian-cyrillic',
            'srp_latn': 'serbian',
            'slk': 'slovak',
            'slv': 'slovenian',
            'spa': 'spanish',
            'swa': 'swahili',
            'swe': 'swedish',
            'tgl': 'tagalog',
            'tel': 'telugu',
            'tha': 'thai',
            'tur': 'turkish',
            'ukr': 'ukranian',
            'urd': 'urdu',
            'vie': 'vietnamese',
            'yor': 'yoruba'
        }

        with open(wordless_misc.get_normalized_path(f'stop_words/extra-stopwords/{LANG_TEXTS[lang]}'), 'r', encoding = 'utf_8') as f:
            stop_words = [line.rstrip() for line in f if not line.startswith('#')]
    # NLTK
    elif 'NLTK' in list_stop_words:
        LANG_TEXTS = {
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
            'slv': 'slovene',
            'spa': 'spanish',
            'swe': 'swedish',
            'tgk': 'tajik',
            'tur': 'turkish'
        }

        stop_words = nltk.corpus.stopwords.words(LANG_TEXTS[lang])
    # spaCy
    elif 'spaCy' in list_stop_words:
        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            with open(wordless_misc.get_normalized_path('stop_words/spaCy/stop_words_zh_tw.txt'), 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            # Serbian (Cyrillic) & Serbian (Latin)
            if lang_639_1 == 'sr_cyrl':
                spacy_lang = importlib.import_module('spacy.lang.sr')

                stop_words = spacy_lang.STOP_WORDS
            elif lang_639_1 == 'sr_latn':
                spacy_lang = importlib.import_module('spacy.lang.sr')

                stop_words = spacy_lang.STOP_WORDS
                stop_words = wordless_text_utils.to_srp_latn(stop_words)
            else:
                spacy_lang = importlib.import_module(f'spacy.lang.{lang_639_1}')

                stop_words = spacy_lang.STOP_WORDS
    # Stopwords ISO
    elif 'Stopwords ISO' in list_stop_words:
        # Norwegian Bokmål & Norwegian Nynorsk
        if lang_639_1 in ['nb', 'nn']:
            lang_639_1 = 'no'

        # Chinese (Traditional)
        if lang_639_1 == 'zh_tw':
            with open(wordless_misc.get_normalized_path('stop_words/Stopwords ISO/stop_words_zh_tw.txt'), 'r', encoding = 'utf_8') as f:
                stop_words = [line.rstrip() for line in f]
        else:
            with open(wordless_misc.get_normalized_path('stop_words/Stopwords ISO/stopwords_iso.json'), 'r', encoding = 'utf_8') as f:
                stop_words = json.load(f)[lang_639_1]
    # Greek (Ancient)
    elif list_stop_words == main.tr('grk-stoplist - Greek (Ancient) Stop Words'):
        with open(wordless_misc.get_normalized_path('stop_words/grk-stoplist/stoplist-greek.txt'), 'r', encoding = 'utf_8') as f:
            stop_words = [line.rstrip() for line in f.readlines()]
    # Thai
    elif list_stop_words == main.tr('PyThaiNLP - Thai Stop Words'):
        stop_words = pythainlp.corpus.common.thai_stopwords()
    # Custom Lists
    elif list_stop_words == main.tr('Custom List'):
        stop_words = main.settings_custom['stop_words']['custom_lists'][lang]

    # Remove empty tokens
    stop_words = [stop_word for stop_word in stop_words if stop_word]

    return sorted(set(stop_words))

def wordless_filter_stop_words(main, items, lang):
    if lang not in main.settings_global['stop_words']:
        lang == 'other'

    stop_words = wordless_get_stop_words(main, lang)

    # Check if the list is empty
    if items:
        if type(items[0]) == str:
            items_filtered = [token for token in items if token not in stop_words]
        elif type(items[0]) in [list, tuple, set]:
            items_filtered = [ngram
                              for ngram in items
                              if not [token for token in ngram if token in stop_words]]
    else:
        items_filtered = []

    return items_filtered
