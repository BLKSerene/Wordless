#
# Wordless: Text - Sentence Tokenization
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import botok
import nltk
import pythainlp
import razdel
import syntok.segmenter
import underthesea

from wl_text import wl_text, wl_text_utils

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

def wl_sentence_tokenize(main, text, lang, sentence_tokenizer = 'default'):
    sentences = []

    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    wl_text_utils.check_sentence_tokenizers(
        main,
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

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
    elif sentence_tokenizer == main.tr('PyThaiNLP - CRFCut'):
        sentences = pythainlp.sent_tokenize(text)
    # Tibetan
    elif sentence_tokenizer == main.tr('botok - Tibetan Sentence Tokenizer'):
        wl_text_utils.check_word_tokenizers(main, lang = 'bod')
        tokens = main.botok_word_tokenizer.tokenize(text)

        for sentence_tokens in botok.sentence_tokenizer(tokens):
            sentences.append(''.join([sentence_token.text
                                      for sentence_token in sentence_tokens[1]]))
    # Vietnamese
    elif sentence_tokenizer == main.tr('Underthesea - Vietnamese Sentence Tokenizer'):
        sentences = underthesea.sent_tokenize(text)

    # Strip spaces
    sentences = [sentence.strip() for sentence in sentences]

    sentences = wl_text_utils.record_boundary_sentences(sentences, text)

    return sentences

def wl_sentence_split(main, text):
    sentences = []
    sentence_start = 0

    tokens = text.split()
    len_tokens = len(tokens)

    for i, token in enumerate(tokens):
        if token[-1] in TERMINATORS_SENTENCE or i == len_tokens - 1:
            sentences.append(' '.join(tokens[sentence_start : i + 1]))

            sentence_start = i + 1

    return sentences

def wl_clause_tokenize(main, text, lang):
    clauses = []

    # Running text
    if type(text) in [str, wl_text.Wl_Token]:
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

def wl_clause_split(main, text):
    clauses = []
    clause_start = 0

    tokens = text.split()
    len_tokens = len(tokens)

    for i, token in enumerate(tokens):
        if token[-1] in TERMINATORS_CLAUSE or i == len_tokens - 1:
            clauses.append(' '.join(tokens[clause_start : i + 1]))

            clause_start = i + 1

    return clauses
